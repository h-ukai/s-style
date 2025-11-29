# main.py
# Python 3.11 / Flask アプリエントリポイント
# - create_app() でアプリを組み立て、gunicorn のエントリは app = create_app()
# - 互換 URL は /app/blueprints/{public,api,tasks}.py 側に実装・登録される想定
# - CORS は /api/* のみ限定付与（環境変数で許可オリジン指定）
# - セッションは Flask-Session（Redis 推奨、環境変数で設定）
# - 構造化ログ（JSON）と一括エラーハンドラを実装
# - 必須環境変数の起動時検査を実装

from __future__ import annotations

import json
import logging
import os
import sys
import time
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from flask import Flask, jsonify, make_response, render_template, request, g
from werkzeug.middleware.proxy_fix import ProxyFix

# 依存: pip install flask flask-cors flask-session redis
from flask_cors import CORS
from flask_session import Session

# ====== 必須環境変数のキー（不足時は起動エラー）======
REQUIRED_ENV_VARS = [
    # 運用上のベースURL（外部リンク生成などで使用）
    "APP_BASE_URL",
    # CORS 許可オリジン（カンマ区切り）。/api のみ適用
    "CORS_ALLOW_ORIGINS",
    # セッション暗号鍵
    "FLASK_SECRET_KEY",
]

# 任意（あると望ましい）環境変数
OPTIONAL_ENV_VARS = [
    # Flask-Session（Redis）の接続。例: redis://:password@host:6379/0
    "SESSION_REDIS_URL",
    # Cookie 属性
    "SESSION_COOKIE_NAME",
    "SESSION_COOKIE_SAMESITE",  # "Lax" 推奨
    "SESSION_COOKIE_SECURE",    # "true"/"false"
    "SESSION_COOKIE_HTTPONLY",  # "true"/"false"
    # テンプレの動作切替など
    "APP_ENV",                  # "production"/"staging"/"development"
]

# ====== 構造化ログ（JSON） ======
class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "severity": record.levelname,
            "time": datetime.now(timezone.utc).isoformat(),
            "message": record.getMessage(),
            "logger": record.name,
        }
        # request スコープの情報（可能なら付与）
        try:
            if hasattr(g, "request_id"):
                payload["request_id"] = g.request_id
            if request:
                payload["httpRequest"] = {
                    "requestMethod": request.method,
                    "requestUrl": request.url,
                    "remoteIp": request.headers.get("X-Forwarded-For", request.remote_addr),
                    "userAgent": request.headers.get("User-Agent"),
                }
        except Exception:
            pass
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


def _configure_logging() -> None:
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    # 既存ハンドラをクリアして JSON 出力に統一
    for h in list(root.handlers):
        root.removeHandler(h)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    root.addHandler(handler)


# ====== アプリファクトリ ======
def create_app() -> Flask:
    _configure_logging()
    logger = logging.getLogger(__name__)
    logger.info("starting create_app()")

    _validate_required_env()

    app = Flask(
        __name__,
        template_folder=os.path.join("app", "templates"),
        static_folder=os.path.join("app", "static"),
    )

    # 逆プロキシ配下（App Engine / Cloud Run）ヘッダ補正
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)  # type: ignore

    # 基本設定
    app.config["SECRET_KEY"] = os.environ["FLASK_SECRET_KEY"]
    app.config["SESSION_TYPE"] = "redis" if os.environ.get("SESSION_REDIS_URL") else "filesystem"
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_USE_SIGNER"] = True

    # Cookie 設定（既定は安全寄り）
    app.config["SESSION_COOKIE_NAME"] = os.environ.get("SESSION_COOKIE_NAME", "sid")
    app.config["SESSION_COOKIE_SAMESITE"] = os.environ.get("SESSION_COOKIE_SAMESITE", "Lax")
    app.config["SESSION_COOKIE_SECURE"] = _to_bool(os.environ.get("SESSION_COOKIE_SECURE", "true"))
    app.config["SESSION_COOKIE_HTTPONLY"] = _to_bool(os.environ.get("SESSION_COOKIE_HTTPONLY", "true"))

    # Redis セッション設定
    if app.config["SESSION_TYPE"] == "redis":
        try:
            from redis import Redis
            app.config["SESSION_REDIS"] = Redis.from_url(os.environ["SESSION_REDIS_URL"])
        except Exception as e:
            logger.error("failed to configure Redis session", exc_info=e)
            raise

    # Flask-Session 初期化
    Session(app)

    # CORS: /api/* のみ限定（許可オリジンは env 経由）
    allow_origins = _parse_csv(os.environ.get("CORS_ALLOW_ORIGINS", ""))
    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": allow_origins,
                "supports_credentials": True,
                "methods": ["GET", "POST", "OPTIONS"],
                "allow_headers": ["Content-Type", "X-Requested-With"],
                "max_age": 600,
            }
        },
    )

    # リクエストID / セキュリティヘッダ / 開始時刻 付与
    @app.before_request
    def _before_request() -> None:
        g.request_id = request.headers.get("X-Request-Id", str(uuid.uuid4()))
        g.start_time = time.time()

    @app.after_request
    def _after_request(resp):
        # セキュリティヘッダ
        resp.headers.setdefault("X-Content-Type-Options", "nosniff")
        resp.headers.setdefault("X-Frame-Options", "DENY")
        resp.headers.setdefault("Referrer-Policy", "no-referrer-when-downgrade")
        # レイテンシをログへ
        latency_ms = int((time.time() - getattr(g, "start_time", time.time())) * 1000)
        logging.getLogger("access").info(
            f"{request.method} {request.path} {resp.status_code} {latency_ms}ms"
        )
        return resp

    # ====== Blueprint 登録（互換 URL の受け口）======
    # public: /, /index.html, /index2.html, /show/<path>, /form, /auth/setsid, /admin/storage/delete
    # api:    /api/* 旧 _myjson 機能分割（GET中心、必要時のみPOST）
    # tasks:  /tasks/* Cloud Tasks / Cron 用（OIDC検証、POST限定、冪等）
    try:
        from app.blueprints.public import bp as public_bp
        app.register_blueprint(public_bp)  # ルート直下で互換
    except Exception as e:
        logger.warning("public blueprint not found or failed to register", exc_info=e)

    try:
        from app.blueprints.api import bp as api_bp
        app.register_blueprint(api_bp, url_prefix="/api")
    except Exception as e:
        logger.warning("api blueprint not found or failed to register", exc_info=e)

    try:
        from app.blueprints.tasks import bp as tasks_bp
        app.register_blueprint(tasks_bp, url_prefix="/tasks")
    except Exception as e:
        logger.warning("tasks blueprint not found or failed to register", exc_info=e)

    # 旧 GAE のウォームアップや健全性チェック
    @app.route("/_ah/warmup")
    @app.route("/healthz")
    def healthz():
        return make_response("ok", 200)

    # ====== エラーハンドラ（HTML / API で形式を出し分け）======
    @app.errorhandler(404)
    def handle_404(err):
        if _is_api_request():
            return jsonify({"ok": False, "error": {"code": 404, "message": "not found"}}), 404
        # 互換テンプレ（sorry.html）がない環境でも落ちないようフォールバック
        try:
            return render_template("sorry.html", code=404, message="ページが見つかりません"), 404
        except Exception:
            return make_response("Not Found", 404)

    @app.errorhandler(400)
    def handle_400(err):
        if _is_api_request():
            return jsonify({"ok": False, "error": {"code": 400, "message": "bad request"}}), 400
        try:
            return render_template("sorry.html", code=400, message="不正なリクエストです"), 400
        except Exception:
            return make_response("Bad Request", 400)

    @app.errorhandler(500)
    def handle_500(err):
        logging.getLogger(__name__).error("unhandled error", exc_info=err)
        if _is_api_request():
            return jsonify({"ok": False, "error": {"code": 500, "message": "internal error"}}), 500
        try:
            return render_template("sorry.html", code=500, message="サーバ内部エラーが発生しました"), 500
        except Exception:
            return make_response("Internal Server Error", 500)

    logger.info("create_app() completed")
    return app


# gunicorn エントリ（例：gunicorn -b :$PORT main:app）
app = create_app()


# ====== 補助関数 ======
def _validate_required_env() -> None:
    missing = [k for k in REQUIRED_ENV_VARS if not os.environ.get(k)]
    if missing:
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")

def _parse_csv(v: str) -> list[str]:
    return [s.strip() for s in (v or "").split(",") if s.strip()]

def _to_bool(v: Optional[str]) -> bool:
    return str(v or "").lower() in ("1", "true", "yes", "on")

def _is_api_request() -> bool:
    # /api/* または Accept: application/json を優先
    if request.path.startswith("/api/"):
        return True
    accept = request.headers.get("Accept", "")
    return "application/json" in accept.lower()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
s-style Python 3.11 Flask Application

/test/ プレフィックス付きでルーティングテストを行うためのアプリケーション
"""

import os
from flask import Flask, Blueprint, redirect, request

# Flask アプリケーション初期化
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Blueprint for /test prefix
test_bp = Blueprint('test', __name__, url_prefix='/test')


# =============================================================================
# Django テンプレート互換カスタムフィルタ
# =============================================================================

@app.template_filter('default_if_none')
def default_if_none(value, default=''):
    """Django の default_if_none フィルタ互換"""
    if value is None:
        return default
    return value


@app.template_filter('slice')
def slice_filter(value, arg):
    """Django の slice フィルタ互換 (例: slice:":10")"""
    if value is None:
        return ''
    try:
        # ":10" -> slice(None, 10)
        # "5:10" -> slice(5, 10)
        parts = arg.split(':')
        if len(parts) == 2:
            start = int(parts[0]) if parts[0] else None
            end = int(parts[1]) if parts[1] else None
            return value[start:end]
        return value
    except:
        return value


@app.template_filter('floatformat')
def floatformat(value, arg='-1'):
    """Django の floatformat フィルタ互換"""
    if value is None:
        return ''
    try:
        decimal_places = abs(int(arg))
        return f'{float(value):.{decimal_places}f}'
    except:
        return value


@app.template_filter('iriencode')
def iriencode(value):
    """Django の iriencode フィルタ互換 - URLエンコード"""
    if value is None:
        return ''
    from urllib.parse import quote
    return quote(str(value), safe='')


# =============================================================================
# NDB コンテキストミドルウェア
# =============================================================================
try:
    from google.cloud import ndb
    ndb_client = ndb.Client()

    @app.before_request
    def before_request():
        """リクエスト前に NDB コンテキストを開始"""
        from flask import g
        g.ndb_context = ndb_client.context()
        g.ndb_context.__enter__()

    @app.teardown_request
    def teardown_request(exception=None):
        """リクエスト後に NDB コンテキストをクリーンアップ"""
        from flask import g
        if hasattr(g, 'ndb_context'):
            try:
                g.ndb_context.__exit__(None, None, None)
            except:
                pass
except ImportError:
    # ローカル開発時は NDB なしでも動作可能
    pass


# =============================================================================
# ハンドラーのインポート
# =============================================================================
from application.index import index_route
from application.index2 import index2_route
from application.form import form_route
from application.jcache import getjson_route, cronworker_route, jsonservice_route
from application.editwhatsnew import editwhatsnew_route
from application.show import show_route
from application.chkauth import setsid_route


# =============================================================================
# ルート定義
# =============================================================================

# Index routes
@test_bp.route('/', methods=['GET', 'POST', 'OPTIONS'])
@test_bp.route('', methods=['GET', 'POST', 'OPTIONS'])
@test_bp.route('/index.html', methods=['GET', 'POST', 'OPTIONS'])
def index():
    """Index page handler"""
    return index_route()


# Index2 route
@test_bp.route('/index2.html', methods=['GET', 'POST', 'OPTIONS'])
def index2():
    """Index2 page handler"""
    return index2_route()


# Form routes
@test_bp.route('/form/', methods=['GET', 'POST', 'OPTIONS'])
@test_bp.route('/form/form.html', methods=['GET', 'POST', 'OPTIONS'])
def form():
    """Form page handler"""
    return form_route()


@test_bp.route('/mobile/form/', methods=['GET', 'POST', 'OPTIONS'])
@test_bp.route('/mobile/form/form.html', methods=['GET', 'POST', 'OPTIONS'])
def form_mobile():
    """Mobile form page handler"""
    return form_route()


# JSON service
@test_bp.route('/jsonservice', methods=['GET', 'POST'])
def jsonservice():
    """JSON service handler"""
    return jsonservice_route()


# Task routes (Cron/Task Queue)
@test_bp.route('/tasks/getjson', methods=['GET', 'POST'])
def getjson():
    """Get JSON data task handler"""
    return getjson_route()


@test_bp.route('/tasks/cronworker', methods=['GET'])
def cronworker():
    """Cron worker handler"""
    return cronworker_route()


# Edit What's New
@test_bp.route('/editwhatsnew', methods=['GET', 'POST'])
def editwhatsnew():
    """Edit What's New page handler"""
    return editwhatsnew_route()


# Show route
@test_bp.route('/show/<path:path>', methods=['GET', 'POST'])
def show(path):
    """Property display handler"""
    return show_route()


# Auth/Session route
@test_bp.route('/auth/setsid', methods=['GET', 'POST'])
def setsid():
    """Set session ID handler"""
    return setsid_route()


# =============================================================================
# Blueprint 登録
# =============================================================================
app.register_blueprint(test_bp)


# =============================================================================
# 開発サーバー起動
# =============================================================================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=True)

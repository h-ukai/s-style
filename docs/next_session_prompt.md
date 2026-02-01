# s-style Python 3 マイグレーション実装プロンプト

## 背景
Google App Engine Python 2.7 で動作している s-style を Python 3.x に移行する。
メール送信・データ更新のAPIサーバー側（s-style-hrd/migration-src）は既にPython 3.11で実装済み。

## 実装方針

- **ソースコードはすべて `s-style/migration-src` に保存する**
- **エンドポイント `/test/` 以下でデプロイしてテストする**
- **Python 2.7 (src/) には触れない**
- 本番移行前に `/test/` で動作確認を完了させる
- s-style-hrd/migration-src は参考例として参照

## 参照ドキュメント
- `docs/python3_migration_analysis.md` - 詳細調査結果

---

## 実装状況

### 完了済み

| 機能 | ファイル | 状態 |
|------|----------|------|
| Flaskアプリ | main.py | ✅ 完了 |
| トップページ | application/index.py | ✅ 完了 |
| サブページ | application/index2.py | ✅ 完了 |
| フォーム・メール送信 | application/form.py | ✅ 完了（s-style-hrd API経由） |
| 物件表示 | application/show.py | ✅ 完了 |
| お知らせ編集 | application/editwhatsnew.py | ✅ 完了 |
| 認証 | application/chkauth.py | ✅ 完了 |
| JSONキャッシュ | application/jcache.py | ✅ 完了 |
| Secret Manager | application/secret_manager.py | ✅ 完了 |
| 設定 | application/config.py | ✅ 完了 |
| 定時処理（cronworker/getjson） | jcache.py, cron.yaml | ✅ 完了 |
| テンプレート変換 | templates/*.html | ✅ 完了 |

### テンプレート変換詳細

Django テンプレート構文から Jinja2 への変換が完了：

| Django 構文 | Jinja2 構文 | 変換スクリプト |
|-------------|-------------|----------------|
| `\|filter:"arg"` | `\|filter("arg")` | convert_templates.py |
| `{% ifchanged var %}` | `{% if loop.first or loop.previtem.attr != var %}` | convert_templates.py |
| `{% ifequal a b %}` | `{% if a == b %}` | convert_templates.py |
| `{% endifequal %}` | `{% endif %}` | convert_templates.py |

カスタムフィルタ（main.py で定義）：
- `default_if_none` - Noneの場合にデフォルト値を返す
- `slice` - 文字列スライス（例: `":10"`）
- `floatformat` - 小数点フォーマット
- `iriencode` - URLエンコード

### 未実装（必要に応じて追加）

| 機能 | 状態 | 備考 |
|------|------|------|
| allblobdelete | 未実装 | Blobstore全削除（GCS版が必要なら実装） |
| セッション管理 | 簡易実装 | 必要に応じて拡張 |

---

## 定期実行（Cron/Task）のマイグレーション判定

### マイグレーション対象（実際に動作している）

| 機能 | 状態 | 説明 |
|------|------|------|
| **cronworker** | ✅ 実装済み | 毎時実行、getjsonにタスク投入 |
| **getjson** | ✅ 実装済み | JSONデータ取得＆キャッシュ |

### マイグレーション対象外（タイポ・未使用）

| 機能 | ファイル | 理由 |
|------|----------|------|
| **bksorttask** | bksorttask.py | **タイポで未動作** - 除外済み |
| getOsusumebkdata 等 | task.py | cron.yamlでコメントアウト済み - 除外済み |

---

## ディレクトリ構成

```
s-style/
├── src/                     # Python 2.7（触らない）
├── docs/                    # ドキュメント
└── migration-src/           # ← Python 3.11 作業ディレクトリ
    ├── main.py              # Flask アプリ
    ├── app.yaml             # service: test-service
    ├── dispatch.yaml        # /test/* → test-service
    ├── cron.yaml            # 定時処理設定
    ├── requirements.txt     # 依存関係
    ├── application/
    │   ├── __init__.py
    │   ├── config.py
    │   ├── secret_manager.py
    │   ├── jcache.py
    │   ├── index.py
    │   ├── index2.py
    │   ├── form.py
    │   ├── show.py
    │   ├── editwhatsnew.py
    │   └── chkauth.py
    ├── templates/           # src/templatesからコピー済み
    └── static_dir/          # src/static_dirからコピー済み
```

---

## デプロイ前の確認事項

1. **Secret Manager** に SMTP 設定が登録されていること
   - `smtp-server`, `smtp-port`, `smtp-user`, `smtp-password`

2. **Cloud Tasks** キュー `mintask` が作成されていること
   ```bash
   gcloud tasks queues create mintask --location=asia-northeast1
   ```

---

## 確認コマンド

```bash
# ローカル実行
cd s-style/migration-src
pip install -r requirements.txt
flask run --port=8080

# テスト環境にデプロイ（s-styleプロジェクト）
cd s-style/migration-src
gcloud app deploy app.yaml dispatch.yaml --project=s-style

# 注意: cron.yaml は既存の定時処理を上書きするため、慎重にデプロイすること
# gcloud app deploy cron.yaml --project=s-style
```

---

## テストエンドポイント確認状況（2026-02-01）

| URL | 状態 |
|-----|------|
| https://s-style.appspot.com/test/ | ✅ 正常 |
| https://s-style.appspot.com/test/form/ | ✅ 正常 |
| https://s-style-hrd.appspot.com/test/ | ✅ 正常 |

---

## 残課題

1. **GCS バケット設定**: s-style から s-style-hrd-jcache への読み取り権限設定
   - 現在はキャッシュが空のためデータ表示なし
   - cronworker/getjson が動作すればデータが蓄積される

2. **cron.yaml のデプロイ**: Cloud Scheduler API の有効化が必要
   - 既存の定時処理と競合する可能性があるため要確認

---

## テスト完了後の本番移行

### 1. app.yaml の修正

**静的ファイルのパス変更** (`/test/` プレフィックスを削除):

```yaml
# 変更前（テスト用）
- url: /test/css
  static_dir: static_dir/css
- url: /test/js
  static_dir: static_dir/js
- url: /test/cmn_img
  static_dir: static_dir/cmn_img
- url: /test/top_img
  static_dir: static_dir/top_img

# 変更後（本番用）
- url: /css
  static_dir: static_dir/css
- url: /js
  static_dir: static_dir/js
- url: /cmn_img
  static_dir: static_dir/cmn_img
- url: /top_img
  static_dir: static_dir/top_img
```

**サービス名の変更**:
```yaml
# 変更前
service: test-service

# 変更後
service: default  # または新しいサービス名
```

**動的ルートの変更**:
```yaml
# 変更前
- url: /test/.*
  script: auto

# 変更後
- url: /.*
  script: auto
```

### 2. main.py の修正

**Blueprint の url_prefix 変更**:
```python
# 変更前
test_bp = Blueprint('test', __name__, url_prefix='/test')

# 変更後（本番用は別の Blueprint を追加、または url_prefix を削除）
# url_prefix='' または url_prefix なしで登録
```

### 3. jcache.py の修正

**cronworker のタスクURL変更**:
```python
# 変更前
'relative_uri': f'/test/tasks/getjson?msgID={p}',

# 変更後
'relative_uri': f'/tasks/getjson?msgID={p}',
```

### 4. dispatch.yaml の修正

```yaml
# 変更前
- url: "*/test/*"
  service: test-service

# 変更後（本番ルーティング）
- url: "*/*"
  service: default  # または新しいサービス名
```

### 5. cron.yaml のデプロイ

⚠️ **注意**: cron.yaml のデプロイは既存の全ての定時処理を上書きします。

- Cloud Scheduler API の有効化が必要
- 既存の Python 2.7 側の cron 設定と統合するか、完全に置き換えるか検討が必要

### 6. GCS バケット設定

s-style プロジェクトから `s-style-hrd-jcache` バケットへのアクセス権設定:
- s-style のサービスアカウントに Storage Object Viewer 権限を付与
- または s-style 専用のバケットを作成し、`GCS_BUCKET_NAME` 環境変数で指定

### 7. 旧サービスの停止

Python 2.7 の旧サービスを停止:
```bash
gcloud app versions stop <version-id> --service=default --project=s-style
```

# s-style Python 3 マイグレーション調査報告書

## 概要

| 項目 | s-style (メイン) | s-style-hrd/migration-src |
|------|------------------|---------------------------|
| Python バージョン | **2.7** | **3.11（移行済み）** |
| フレームワーク | webapp2 | Flask |
| データベース | db.Model / ndb.Model | ndb.Model |
| メール送信 | GAE Mail API | SMTP（API化済み） |

## 1. s-style メインプロジェクト分析

### 1.1 ディレクトリ構造

```
s-style/
├── src/
│   ├── main.py                 # Flask版（新・未完成）
│   ├── main_old.py             # webapp2版（現行）
│   ├── app.yaml                # GAE設定（python27）
│   ├── application/
│   │   ├── models/
│   │   │   └── address.py      # db.Model使用
│   │   ├── index.py            # メイン画面
│   │   ├── index2.py           # サブ画面
│   │   ├── form.py             # フォーム・メール送信
│   │   ├── show.py             # 物件表示
│   │   ├── chkauth.py          # 認証チェック
│   │   ├── session.py          # セッション管理
│   │   ├── jcache.py           # JSONキャッシュ
│   │   ├── bksorttask.py       # ソートタスク
│   │   ├── allblobdelete.py    # BLOB削除
│   │   └── cloudstorage/       # GCSクライアント
│   ├── templates/              # Jinja2テンプレート
│   └── static_dir/             # 静的ファイル
└── csvupload/                  # CSVアップロード
```

### 1.2 app.yaml（現行）

```yaml
application: s-style
version: 1
runtime: python27          # ← 移行対象
api_version: 1
threadsafe: true

handlers:
- url: /
  script: main.app
- url: /form/(.*)
  script: main.app
- url: /show/.*
  script: main.app
# ... 他多数
```

### 1.3 使用ライブラリ・API

| カテゴリ | ライブラリ | 移行先 |
|----------|-----------|--------|
| Webフレームワーク | webapp2 | Flask |
| データベース | google.appengine.ext.db | google.appengine.ext.ndb |
| メール | google.appengine.api.mail | SMTP (migration-src参照) |
| HTTP取得 | google.appengine.api.urlfetch | requests / urllib3 |
| BLOB | google.appengine.ext.blobstore | Cloud Storage |
| キャッシュ | google.appengine.api.memcache | Redis / Memorystore |
| タスク | google.appengine.api.taskqueue | Cloud Tasks |
| テンプレート | google.appengine.ext.webapp.template | Jinja2 |

---

## 2. Python 2 → 3 構文変更必須箇所

### 2.1 致命的エラー（即時修正必要）

| ファイル | 行 | 問題コード | 修正後 |
|----------|-----|-----------|--------|
| allblobdelete.py | 55 | `except Exception, e:` | `except Exception as e:` |
| cs.py | 50,52,54 | `print PlainText` | `print(PlainText)` |
| bksorttask.py | 38 | `sort(cmp=lambda...)` | `sort(key=functools.cmp_to_key(...))` |

### 2.2 モジュール変更

| ファイル | 変更前 | 変更後 |
|----------|--------|--------|
| cloudstorage_api.py | `import StringIO` | `from io import StringIO` |
| cloudstorage_api.py | `urllib.urlencode()` | `urllib.parse.urlencode()` |
| storage_api.py | `import urlparse` | `from urllib import parse` |
| cloudstorage/common.py | `xrange()` | `range()` |
| cloudstorage/common.py | `.iteritems()` | `.items()` |

### 2.3 バイト・文字列処理

```python
# 変更前（Python 2）
res = urlfetch.fetch(url)
data = json.loads(res.content)

# 変更後（Python 3）
res = requests.get(url)
data = res.json()  # または json.loads(res.content.decode('utf-8'))
```

---

## 3. migration-src 分析結果

### 3.1 メール送信API（実装済み）

**ファイル:** `migration-src/application/messageManager.py`

```python
@classmethod
def _send_mail(cls, sender, emailto, subject, body=None, html=None):
    """Send email using SMTP (migration from Mail API)"""
    smtp_config = get_smtp_config()  # Secret Manager から取得

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_config['server'], smtp_config['port'], context=context) as server:
        server.login(smtp_config['user'], smtp_config['password'])
        server.send_message(message)
```

**呼び出しAPI:**
```python
messageManager.post(
    corp="s-style",
    sub="件名",
    body="本文",
    mailto="tanto"  # または "member" / "each"
)
```

### 3.2 Secret Manager 設定（実装済み）

**ファイル:** `migration-src/application/secret_manager.py`

```python
def get_smtp_config():
    return {
        'server': get_secret('smtp-server'),
        'port': int(get_secret('smtp-port')),
        'user': get_secret('smtp-user'),
        'password': get_secret('smtp-password'),
    }
```

### 3.3 メール受信（IMAP実装済み）

- `email_receiver.py` でIMAPポーリング
- 10分ごとのCronで実行
- 受信メールを内部メッセージに変換

---

## 4. マイグレーションプラン

### Phase 1: 構文修正（即時対応）

1. **except文法修正** - allblobdelete.py
2. **print関数化** - cs.py
3. **sort(cmp=)修正** - bksorttask.py
4. **モジュールインポート修正** - cloudstorage/*

### Phase 2: フレームワーク移行

1. **webapp2 → Flask**
   - main_old.py のルーティングを main.py に統合
   - RequestHandler → Flask ルート関数
   - self.response.out.write() → return Response()

2. **テンプレート移行**
   - google.appengine.ext.webapp.template → Jinja2
   - テンプレート自体は互換性あり（変更最小限）

### Phase 3: GAE API移行

| 旧API | 新API | 対応方法 |
|-------|-------|----------|
| db.Model | ndb.Model | モデル定義書き換え |
| mail.EmailMessage | SMTP | **migration-src のコードを流用** |
| urlfetch | requests | ライブラリ置換 |
| blobstore | Cloud Storage | GCSクライアント更新 |
| memcache | Redis/Memorystore | 設定変更 |
| taskqueue | Cloud Tasks | API呼び出し変更 |

### Phase 4: メール送信統合

**s-style の form.py を修正:**

```python
# 変更前（GAE Mail API）
from google.appengine.api import mail

message = mail.EmailMessage()
message.sender = config.ADMIN_EMAIL
message.to = email
message.subject = 's-styleサイトからの登録'
message.body = msgbody
message.send()

# 変更後（migration-srcのAPIを呼び出し）
from application.messageManager import messageManager

messageManager._send_mail(
    sender=config.ADMIN_EMAIL,
    emailto=email,
    subject='s-styleサイトからの登録',
    body=msgbody
)
```

**または、REST API化してHTTP呼び出し:**
```python
import requests
requests.post('https://s-style-hrd.appspot.com/api/send-mail', json={
    'to': email,
    'subject': 's-styleサイトからの登録',
    'body': msgbody
})
```

### Phase 5: app.yaml更新

```yaml
# 変更後
runtime: python311
entrypoint: gunicorn -b :$PORT main:app

handlers:
- url: /static
  static_dir: static_dir
- url: /.*
  script: auto
  secure: always
```

### Phase 6: requirements.txt作成

```
Flask==3.0.0
gunicorn==21.2.0
google-cloud-ndb==2.3.0
google-cloud-storage==2.14.0
google-cloud-secret-manager==2.18.0
google-cloud-tasks==2.16.0
requests==2.31.0
Jinja2==3.1.2
```

---

## 5. ファイル別修正一覧

| ファイル | 修正内容 | 優先度 |
|----------|----------|--------|
| app.yaml | runtime: python311 | HIGH |
| main_old.py → main.py | webapp2 → Flask | HIGH |
| form.py | メール送信をSMTPに変更 | HIGH |
| allblobdelete.py | except文法、blobstore→GCS | HIGH |
| bksorttask.py | sort(cmp=)修正 | HIGH |
| cs.py | print関数化 | HIGH |
| cloudstorage/*.py | StringIO, urllib修正 | MEDIUM |
| models/address.py | db.Model → ndb.Model | MEDIUM |
| session.py | Expando見直し | MEDIUM |
| chkauth.py | urlfetch → requests | MEDIUM |
| httpaccess.py | urlfetch → requests | MEDIUM |
| jcache.py | memcache見直し | LOW |
| index.py, index2.py | テンプレート処理更新 | LOW |
| show.py | セッション処理更新 | LOW |

---

## 6. 注意事項

### 6.1 メール送信の選択肢

1. **migration-src のコードを直接流用**（推奨）
   - messageManager.py の _send_mail() をコピー
   - Secret Manager の設定を共有

2. **REST API化して呼び出し**
   - migration-src に /api/send-mail エンドポイントを追加
   - s-style から HTTP POST で呼び出し

3. **外部サービス利用**
   - SendGrid / Mailgun などのSaaS
   - より信頼性が高いが設定が必要

### 6.2 データベース互換性

- `db.Model` と `ndb.Model` は同じDatastoreを参照可能
- キー形式の違いに注意（`db.Key` vs `ndb.Key`）
- 既存データは移行なしでアクセス可能

### 6.3 セッション管理

- `db.Expando` は `ndb.Expando` に置換
- または Redis/Memorystore への移行を検討

---

## 7. 推定作業量

| フェーズ | 内容 | ファイル数 |
|----------|------|-----------|
| Phase 1 | 構文修正 | 5-10 |
| Phase 2 | Flask移行 | 10-15 |
| Phase 3 | API移行 | 15-20 |
| Phase 4 | メール統合 | 2-3 |
| Phase 5-6 | 設定更新 | 2-3 |

**合計:** 約30-50ファイルの修正

---

## 8. 結論

s-style-hrd/migration-src には既にPython 3.11対応のメール送信・受信機能が実装されている。s-styleメインプロジェクトのマイグレーションでは、このコードを流用することで効率的に移行が可能。

主な作業は：
1. Python 2構文のPython 3化
2. webapp2 → Flask への移行
3. GAE固有API → Cloud API への移行
4. メール送信をmigration-srcの実装に統合
5. 現在のpy2.7に触れないままエンドポイント/test/以下に/migration-srcを展開してルーティングテストを可能にすることこの際py2.7のデプロイは禁止されているのでpy3.11のプロジェクトホスティングfunctionのみデプロイすること

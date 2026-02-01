# -*- coding: utf-8 -*-
"""
s-style 設定ファイル
"""

import os

# API接続先（s-style-hrd の API サーバー）
DATABASE_URL = 'https://s-style-hrd.appspot.com/'

# メール設定
BASE_URL = 'https://s-style.appspotmail.com'
ADMIN_EMAIL = 'info001@s-style.appspotmail.com'
ADMIN_EMAIL_BASE = '@s-style-hrd.appspotmail.com'
ADMIN_SYSTEM_ID = 'systemID0023232@memberlist'

# GCP設定
GCP_PROJECT = os.environ.get('GCP_PROJECT', 's-style-hrd')
GCS_BUCKET_NAME = os.environ.get('GCS_BUCKET_NAME', 's-style-hrd-jcache')

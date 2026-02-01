# -*- coding: utf-8 -*-
"""
Secret Manager utility module

Cloud Secret Manager からシークレットを取得するユーティリティ
"""

import os
import logging
from functools import lru_cache
from google.cloud import secretmanager

# プロジェクトIDは環境変数から取得
PROJECT_ID = os.environ.get('GCP_PROJECT', 's-style-hrd')

# Secret Manager クライアント（遅延初期化）
_client = None


def _get_client():
    """Secret Manager クライアントを取得（シングルトン）"""
    global _client
    if _client is None:
        _client = secretmanager.SecretManagerServiceClient()
    return _client


@lru_cache(maxsize=32)
def get_secret(secret_id: str) -> str:
    """
    Secret Manager からシークレットを取得

    Args:
        secret_id: シークレットID（例: 'smtp-server', 'smtp-password'）

    Returns:
        シークレットの値（文字列）
    """
    try:
        client = _get_client()
        name = f"projects/{PROJECT_ID}/secrets/{secret_id}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        logging.error("Failed to get secret '%s': %s", secret_id, str(e))
        raise


def get_smtp_config():
    """SMTP設定を取得"""
    return {
        'server': get_secret('smtp-server'),
        'port': int(get_secret('smtp-port')),
        'user': get_secret('smtp-user'),
        'password': get_secret('smtp-password'),
    }

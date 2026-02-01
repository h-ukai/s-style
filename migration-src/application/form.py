# -*- coding: utf-8 -*-
"""
Form handler - Flask version

問い合わせフォーム処理
s-style-hrd のメール送信 API を呼び出す
"""

import os
import logging
import requests as http_requests

from flask import request, render_template, make_response
from application import config


# メール送信先（複数アドレスはセミコロン区切り）
MAIL_RECIPIENTS = 's-style.s8@nifty.com;warao.shikyo@gmail.com;fuminori.yokoyama@gmail.com'

# reCAPTCHA サイトキー
RECAPTCHA_SITE_KEY = os.environ.get('RECAPTCHA_SITE_KEY', '6LfRxU4aAAAAAD6BDE23lHzfDy3OX2h8qqV-bH2Q')

# s-style-hrd メール送信 API エンドポイント（本番URL優先、フォールバックでテストURL）
MAIL_API_BASE = 'https://s-style-hrd.appspot.com'
MAIL_API_ENDPOINTS = [
    '/api/send-form-mail',        # 本番URL（将来）
    '/test/api/send-form-mail',   # テストURL（現在）
]


def form_route():
    """Form page handler"""
    tmpl_val = {}
    tmpl_val['sitekey'] = RECAPTCHA_SITE_KEY
    tmpl_val['ref'] = request.args.get('ref', '')

    # テンプレートが期待する data 変数を追加
    bkID = request.args.get('bkID', '') or request.form.get('bkID', '')
    tmpl_val['data'] = {'bkdata': {'bkID': bkID}}

    if request.method == 'OPTIONS':
        # CORS preflight
        response = make_response('')
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        return response

    # フォーム送信処理
    get_new_regist = request.form.get('new_regist')
    if get_new_regist:
        try:
            _send_form_mail_via_api(MAIL_RECIPIENTS)
            tmpl_val['submit'] = True
        except Exception as e:
            logging.error(f'Form mail send error: {e}')
            tmpl_val['error'] = True

    # テンプレート選択（/form/ or /mobile/form/）
    path = request.path
    if path.startswith('/test/mobile/') or path.startswith('/mobile/'):
        template_name = 'formm.html'
    else:
        template_name = 'form.html'

    response = make_response(render_template(template_name, **tmpl_val))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'

    return response


def _send_form_mail_via_api(recipients):
    """
    s-style-hrd のメール送信 API を呼び出してフォームデータを送信

    本番URLを先に試し、失敗したらテストURLにフォールバック

    Args:
        recipients: 送信先メールアドレス（セミコロン区切り）
    """
    # フォームデータを本文に変換
    msgbody = ''
    for key, value in request.form.items():
        msgbody += f'{key} : {value}\n'

    # API リクエスト
    payload = {
        'sender': f'"Form sender utility" <{config.ADMIN_EMAIL}>',
        'recipients': recipients,
        'subject': 's-styleサイトからの登録',
        'body': msgbody
    }

    last_error = None

    # 本番URL → テストURL の順に試行
    for endpoint in MAIL_API_ENDPOINTS:
        url = MAIL_API_BASE + endpoint
        try:
            res = http_requests.post(
                url,
                json=payload,
                timeout=30,
                headers={
                    'Content-Type': 'application/json',
                    'User-Agent': 'www.s-style.ne.jp'
                }
            )
            res.raise_for_status()
            logging.info(f'Form mail sent via API ({endpoint}): {res.status_code}')
            return  # 成功したら終了

        except Exception as e:
            logging.warning(f'Failed to send via {endpoint}: {e}')
            last_error = e
            continue  # 次のエンドポイントを試行

    # すべて失敗した場合
    logging.error(f'All mail API endpoints failed')
    raise last_error

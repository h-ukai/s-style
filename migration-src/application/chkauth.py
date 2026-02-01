# -*- coding: utf-8 -*-
"""
Authentication handler - Flask version
"""

import re
import json
import datetime
import requests as http_requests
from flask import request, make_response
from application import config

DEFAULT_Auth_Day = 1


def setsid_route():
    """Set session ID handler"""
    sid = request.values.get("sid", "")
    tmpl_val = {}

    # TODO: セッション処理を実装
    if sid:
        tmpl_val['sid'] = sid
    else:
        tmpl_val['sid'] = ''

    html = f'''
    <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "https://www.w3.org/TR/html4/loose.dtd">
    <html>
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf8">
    <title>auth_iframe_contents</title>
    </head>
    <body>
    sid ={tmpl_val['sid']}
    </body>
    </html>
    '''

    response = make_response(html)
    response.headers['p3p'] = 'CP="CAO PSA OUR"'
    return response


def chkauth_by_sid(sid):
    """
    セッションIDで認証チェック

    Args:
        sid: セッションID

    Returns:
        bool: 認証済みならTrue
    """
    if not sid:
        return False

    try:
        url = f"{config.DATABASE_URL}jsonservice?com=chkAuthbysid&corp=s-style&site=www.s-style.ne.jp&sid={sid}"
        res = http_requests.get(
            url,
            timeout=120,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'www.s-style.ne.jp'
            }
        )

        strbuf = res.text
        if re.search('error', strbuf, re.IGNORECASE) is None:
            resdic = res.json()
            if resdic.get("Auth") == "True":
                return True
    except Exception:
        pass

    return False

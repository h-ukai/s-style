# -*- coding: utf-8 -*-
"""
Index2 page handler - Flask version
"""

from flask import request, render_template, make_response


def index2_route():
    """Index2 page handler"""
    tmpl_val = {}

    # CORS ヘッダー設定
    response = make_response(render_template('index2.html', **tmpl_val))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'

    return response

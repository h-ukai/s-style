# -*- coding: utf-8 -*-
"""
Index page handler - Flask version
"""

import re
import os
from flask import request, render_template, redirect
from application.jcache import jcache


def index_route():
    """Index page handler"""
    # CORS ヘッダー（必要に応じて）
    tmpl_val = {}

    view = request.args.get('view')
    user_agent = request.user_agent.string or ''

    # フィーチャーフォン判定
    pattern = 'DoCoMo|KDDI|DDIPOKET|UP\\.Browser|J-PHONE|Vodafone|SoftBank|J-PHONE|WILLCOM|DDIPOCKET'
    if re.search(pattern, user_agent):
        return redirect('/mobile/', code=301)

    # テンプレート選択
    template_name = 'index.html'
    tmpl_val['bkdataurl'] = 'https://s-style-hrd.appspot.com/show/s-style/hon/www.s-style.ne.jp/bkdata/article.html?media=web&id='

    if view == 'mobile':
        return redirect('/mobile/', code=301)
    elif view == 'smartphone':
        tmpl_val['bkdataurl'] = 'https://s-style-hrd.appspot.com/show/s-style/hon/www.s-style.ne.jp.sh/bkdata/article.html?media=web&id='
        template_name = 'index-sp.html'
    elif view != 'pc':
        # スマートフォン判定
        sp_pattern = 'iPhone|Android.*Mobile|Windows.*Phone'
        if re.search(sp_pattern, user_agent):
            template_name = 'index-sp.html'

    # キャッシュからデータ取得
    # 709005: sおすすめ
    dat = jcache.getdict("709005") or []
    if dat and len(dat) > 1:
        dat.sort(key=lambda x: x.get('bk', {}).get('bkdata', {}).get('hykpint', ""), reverse=True)
    tmpl_val['osusume'] = dat

    # 693780: sプレミアム
    dat = jcache.getdict("693780") or []
    if dat and len(dat) > 1:
        dat.sort(key=lambda x: x.get('bk', {}).get('bkdata', {}).get('kknnngp', ""), reverse=True)
    tmpl_val['premium'] = dat

    # 1899136: 広告可（新着）
    dat = jcache.getdict("1899136") or []
    if dat and len(dat) > 1:
        dat.sort(key=lambda x: x.get('bk', {}).get('bkdata', {}).get('kknnngp', ""), reverse=True)
    tmpl_val['newdata'] = dat

    # namedata: 物件リストボックス
    dat = jcache.getdict("namedata") or []
    tmpl_val['bukenlistbox'] = dat

    return render_template(template_name, **tmpl_val)

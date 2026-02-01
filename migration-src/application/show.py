# -*- coding: utf-8 -*-
"""
Show handler - Flask version

物件表示ハンドラ
"""

from flask import request, render_template, redirect
from application.jcache import jcache


def show_route():
    """Property display handler"""
    tmpl_val = {}
    tmpl_val['sid'] = ''
    tmpl_val['auth'] = False

    # TODO: セッション認証処理を実装
    auth = False

    templ = 'bklist.html'
    entitys = {}
    tmpl_val["applicationpagebase"] = "userpagebase.html"

    value1 = request.args.get("value1")
    value2 = request.args.get("value2")
    entity1 = request.args.get("entity1")
    entity2 = request.args.get("entity2")
    dataKey = request.args.get("datakey")
    media = request.args.get("media", "web")

    if value1 and entity1:
        bklist = jcache.getdict(dataKey)
        if bklist is None:
            bklist = []

        result_list = []
        for bkd in bklist:
            bkdata = bkd.get('bk', {}).get('bkdata', {})

            # フィルタリング
            match1 = bkdata.get(entity1, "") == value1
            match2 = (
                bkdata.get(entity2, "") == value2 or
                (entity2 is None and value2 is None) or
                (entity2 == "icons" and value2 in bkdata.get("icons", []))
            )

            if match1 and match2:
                kukkTnsiKbn = bkdata.get("kukkTnsiKbn", "")
                if kukkTnsiKbn in ["広告可", "一部可（インターネット）", "広告可（但し要連絡）"]:
                    bkd['bk']['bkdata']['kukkk'] = True
                elif auth:
                    bkd['bk']['bkdata']['kukkk'] = False
                    bkd['bk']['bkdata']['kkkybku'] = ["この物件は会員のみ公開しております。"] + bkdata.get("kkkybku", [])
                else:
                    tempdic = {
                        'bkID': bkdata.get("bkID", ""),
                        'kukkk': False,
                        'kkkybku': ["この物件は会員のみ公開しております。", "新規会員登録／ログインはこちらです。"]
                    }
                    bkd['bk']['bkdata'] = tempdic

                result_list.append(bkd)

        # 1件のみの場合はリダイレクト
        if len(result_list) == 1:
            bk_id = result_list[0]['bk']['bkdata']['bkID']
            return redirect(f"https://s-style-hrd.appspot.com/show/s-style/hon/www.s-style.ne.jp/bkdata/article.html?media={media}&id={bk_id}")

        # 0件の場合
        if len(result_list) == 0:
            return ''

        entitys["bkdatalist"] = result_list
        entitys["bkdataurl"] = f"https://s-style-hrd.appspot.com/show/s-style/hon/www.s-style.ne.jp/bkdata/article.html?media={media}&id="
        entitys["entity1"] = entity1
        entitys["value1"] = value1
        entitys["entity2"] = entity2
        entitys["value2"] = value2
        entitys["dataKey"] = dataKey
        entitys["media"] = media
    else:
        tmpl_val['error_msg'] = 'リストの情報が取得できませんでした。'
        templ = "sorry.html"

    tmpl_val["data"] = entitys
    return render_template(templ, **tmpl_val)

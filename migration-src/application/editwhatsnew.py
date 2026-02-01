# -*- coding: utf-8 -*-
"""
Edit What's New handler - Flask version
"""

from flask import request, render_template
from google.cloud import ndb


class dbwhatsnew(ndb.Model):
    """What's New データモデル"""
    datakey = ndb.StringProperty()
    enableshow = ndb.BooleanProperty(default=False)
    date = ndb.StringProperty(required=True)
    text = ndb.StringProperty()
    bkID = ndb.StringProperty()


def editwhatsnew_route():
    """Edit What's New page handler"""
    key = request.values.get("key")
    submit = request.values.get("submit")
    isadd = request.values.get("isadd")
    bkID = request.values.get("bkID")
    date = request.values.get("date")
    text = request.values.get("text")
    enableshow = request.values.get("enableshow")

    if enableshow == "True":
        enableshow = True
    else:
        enableshow = False

    # 新規追加
    if isadd == "True" and date:
        dbwt = dbwhatsnew(enableshow=enableshow, date=date, text=text, bkID=bkID)
        dbwt.put()

    # 削除
    if submit == "削除" and key:
        wt_key = ndb.Key(urlsafe=key)
        wt = wt_key.get()
        if wt:
            wt.key.delete()

    # 保存
    if submit == "保存" and key:
        wt_key = ndb.Key(urlsafe=key)
        wt = wt_key.get()
        if wt:
            wt.bkID = bkID
            wt.date = date
            wt.text = text
            wt.enableshow = enableshow
            wt.put()

    # 一覧取得
    query = dbwhatsnew.query().order(-dbwhatsnew.date)
    items = query.fetch(1000)

    return render_template('editwhatsnew.html', list=items)

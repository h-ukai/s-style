# -*- coding: utf-8 -*-
#

import os
#from google.appengine.ext import webapp
import webapp2
from google.appengine.ext.webapp import template
from application import sessionxx
from jcache import jcache
import urllib
from application.chkauth import dbsession

class Show(webapp2.RequestHandler):

    def get(self):
        self.tmpl_val = {}
        #https://localhost:8080/show/bklist.html?datakey=623121&entity=ttmnmi&listkey=%E3%82%A8%E3%83%AB%E3%82%B6%E6%98%9F%E3%83%B6%E4%B8%98&media=web
        dssn = dbsession(self.request,self.response)
        sid = dssn.getsid()
        if sid:
            self.tmpl_val['sid'] = sid
        else:
            self.tmpl_val['sid'] = ''

        auth = dssn.chkauth(self.request, self.response)
        if auth:
            self.tmpl_val['auth'] = True
        else:
            self.tmpl_val['auth'] = False

        templ = 'bklist.html'
        self.tmpl_val = {}
        entitys = {}
        self.tmpl_val["applicationpagebase"] = u"userpagebase.html"
        value1 = self.request.get("value1")
        value2 = self.request.get("value2")
        entity1 = self.request.get("entity1")
        entity2 = self.request.get("entity2")
        dataKey = self.request.get("datakey")
        media = self.request.get("media")
        if value1 and entity1:
            bklist = jcache.getdict(dataKey)
            list = []
            for bkd in bklist:
                if bkd['bk']['bkdata'].get(entity1,"") == value1 and (bkd['bk']['bkdata'].get(entity2,"") == value2 or (entity2 == None and value2 == None) or (entity2=="icons" and value2 in bkd['bk']['bkdata'].get("icons",[]))):
                    if bkd['bk']['bkdata'].get("kukkTnsiKbn","") in [u"広告可",u"一部可（インターネット）",u"広告可（但し要連絡）"]:
                        bkd['bk']['bkdata']['kukkk'] = True
                    elif auth:
                        bkd['bk']['bkdata']['kukkk'] = False
                        bkd['bk']['bkdata']['kkkybku'] = [u"この物件は会員のみ公開しております。"] + bkd['bk']['bkdata'].get("kkkybku",[])
                    else:
                        tempdic = {'bkID': bkd['bk']['bkdata'].get("bkID",""),'kukkk' : False,'kkkybku' : [u"この物件は会員のみ公開しております。",u"新規会員登録／ログインはこちらです。"]}
                        #tempdic = {'bkID': bkd['bk']['bkdata'].get("bkID",""),'kukkk' : False,'kkkybku' : [u"この物件は会員のみ公開しております。",u"会員様はここからご覧蒙ださい。",u"新規会員登録／ログインはこちらです。"]}
                        bkd['bk']['bkdata'] = tempdic
                    list.append(bkd)
            if len(list) == 1:
                self.redirect(str("https://s-style-hrd.appspot.com/show/s-style/hon/www.s-style.ne.jp/bkdata/article.html?media=" + media + u"&id=" + list[0]['bk']['bkdata']['bkID']), False)
                return
            if len(list) == 0:
                return
            entitys["bkdatalist"] = list
            entitys["bkdataurl"] = u"https://s-style-hrd.appspot.com/show/s-style/hon/www.s-style.ne.jp/bkdata/article.html?media=" + media + u"&id="
            entitys["entity1"] = entity1
            entitys["value1"] = value1
            entitys["entity2"] = entity2
            entitys["value2"] = value2
            entitys["dataKey"] = dataKey
            entitys["media"] = media
        else:
            self.tmpl_val['error_msg'] = u'リストの情報が取得できませんでした。'
            templ =  u"sorry.html"
        self.tmpl_val["data"] = entitys
        path = os.path.dirname(__file__) + '/../templates/' + templ
        self.response.out.write(template.render(path, self.tmpl_val))

    def post(self):

        self.get()



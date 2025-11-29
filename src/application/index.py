#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import re
import os
from jcache import jcache

#from google.appengine.ext import webapp
import webapp2
from google.appengine.ext.webapp import template
from google.appengine.api import mail
from application.editwhatsnew import dbwahatsnew

class Index(webapp2.RequestHandler):
    def get(self):
        self.post()

    def post(self):
        try:
            referer = self.response.headers['Referer']
        except:
            referer = ''
        try:
            origin = self.response.headers['Origin']
        except:
            origin = ''
        # この方法でOriginやRefererが取れるので
        # 必要に応じてチェック処理などを入れるといいのでは。
        # ちなみにtry〜exceptを使わないと、存在しない場合Key Errorが発生しますよ

        # これはあちこちのサイトでよく言われている処理
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        # IE8は、これがないとうまく動きませんでした。
        self.response.headers['Access-Control-Allow-Headers'] = '*'
        # GET/POSTなど、必要に応じて許可するメソッドを指定します。
        # POSTの場合はOPTIONSも指定する必要があります。
        self.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        #self.response.headers['Content-Type'] = 'text/plain;charset=UTF-8'

        self.tmpl_val = {}

        view = self.request.get('view')
        # https://www.s-style.ne.jp/mobile/
        user_agent = self.request.user_agent
        pattern = 'DoCoMo|KDDI|DDIPOKET|UP\.Browser|J-PHONE|Vodafone|SoftBank|J-PHONE|WILLCOM|DDIPOCKET'
        prog = re.compile(pattern)
        result = prog.search(user_agent)
        path = os.path.join( os.getcwd(),'templates','index.html')
        self.tmpl_val['bkdataurl'] = 'https://s-style-hrd.appspot.com/show/s-style/hon/www.s-style.ne.jp/bkdata/article.html?media=web&id='
        if result or view == 'mobile':
            self.redirect('/mobile/', permanent = True)
        else:
            if view == 'pc':
                pass
            elif view == 'smartphone':
                self.tmpl_val['bkdataurl'] = 'https://s-style-hrd.appspot.com/show/s-style/hon/www.s-style.ne.jp.sh/bkdata/article.html?media=web&id='
                path = os.path.join( os.getcwd(),'templates','index-sp.html')
            else:
                pattern = 'iPhone|Android.*Mobile|Windows.*Phone'
                prog = re.compile(pattern)
                result = prog.search(user_agent)
                if result:
                    path = os.path.join( os.getcwd(),'templates','index-sp.html')


        #params = [709005,693780,1899136,1915096] #sおすすめ ,sプレミアム,広告可,全物件

        dat = jcache.getdict("709005")
        if dat != None and len(dat)>1:
            dat.sort(key=lambda x:x['bk']['bkdata'].get('hykpint',""), reverse=True)
        self.tmpl_val['osusume'] = dat

        dat = jcache.getdict("693780")
        if dat != None and len(dat)>1:
            dat.sort(key=lambda x:x['bk']['bkdata']['kknnngp'], reverse=True)
        self.tmpl_val['premium'] = dat

        dat = jcache.getdict("1899136")
        if dat != None and len(dat)>1:
            dat.sort(key=lambda x:x['bk']['bkdata']['kknnngp'], reverse=True)
        self.tmpl_val['newdata'] = dat

        dat = jcache.getdict("namedata")
        self.tmpl_val['bukenlistbox'] = dat

        """
        commstr = u"jsonservice?com=BKdataicon&icon=sおすすめ&media=web"
        dat1 = httpaccess.get_data_mem(commstr)
        if dat1 != None and len(dat1)>1:
            dat = dat1.get("bkdatalist",None)
            dat.sort(key=lambda x:x["bkdata"].get('hykpint',""), reverse=True)
            dat1["bkdatalist"]=dat
        self.tmpl_val['osusume'] = dat1

        commstr = u"jsonservice?com=BKdataicon&icon=sプレミアム&media=web"
        dat1 = httpaccess.get_data_mem(commstr)
        if dat1 != None and len(dat1)>1:
            dat = dat1.get("bkdatalist",None)
            dat.sort(key=lambda x:x["bkdata"].get('hykpint',""), reverse=True)
            dat1["bkdatalist"]=dat
        self.tmpl_val['premium'] = dat1

        kknnngp = datetime.datetime.now()
        kknnngp = timemanager.utc2jst_date(kknnngp)
        kknnngp = timemanager.add_months(kknnngp,-1)

        commstr = u"kknnngpl=" + kknnngp.strftime("%Y/%m/%d") # %H:%M:%S
        #commstr = ""
        commstr = commstr + u"&isidkd=1&dtsyuri=物件&kukkTnsiKbn=一部可（インターネット）"
        dat = httpaccess.search_data_mem(commstr)
        if dat != None and len(dat)>1:
            dat.sort(key=lambda x:x['bk']['kknnngp'], reverse=True)
        self.tmpl_val['newdata'] = dat
        """

        self.response.out.write(template.render(path, self.tmpl_val))

    def options(self):
        # 何らかの処理を行う
        # POSTの場合は、このoptionsも指定して下さい。
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = '*'
        self.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'

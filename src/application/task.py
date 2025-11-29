#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import datetime
#from google.appengine.ext import webapp
import webapp2
from httpaccess import httpaccess
from application import timemanager

class getOsusumebkdata(webapp2.RequestHandler):

    def get(self):
        commstr = u"jsonservice?com=BKdataicon&icon=sおすすめ&media=web"
        dat = httpaccess.get_data(commstr)
        self.response.out.write(dat)

class getPremiumbkdata(webapp2.RequestHandler):

    def get(self):
        commstr = u"jsonservice?com=BKdataicon&icon=sプレミアム&media=web"
        dat = httpaccess.get_data(commstr)
        self.response.out.write(dat)

class searchNewbkdata(webapp2.RequestHandler):

    def get(self):
        kknnngp = datetime.datetime.now()
        #amanedb側で日本時間から変換するので日本時間にしておく
        kknnngp = timemanager.utc2jst_date(kknnngp)
        kknnngp = timemanager.add_months(kknnngp,-1)
        
        commstr = u"kknnngpl=" + kknnngp.strftime("%Y/%m/%d") # %H:%M:%S
        #commstr = ""
        commstr = commstr + u"&isidkd=1&dtsyuri=物件&kukkTnsiKbn=一部可（インターネット）"
        dat = httpaccess.search_data(commstr)
            
        self.response.out.write(dat)



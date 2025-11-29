# -*- coding: utf-8 -*-

#from google.appengine.ext import webapp
import webapp2
from google.appengine.ext import db
from google.appengine.ext.webapp import template
import os

class dbwahatsnew(db.Model):
    datakey = db.StringProperty(verbose_name="key")
    enableshow = db.BooleanProperty(verbose_name="表示")
    date = db.StringProperty(verbose_name="日付",required=True)
    text = db.StringProperty(verbose_name="本文")
    bkID = db.StringProperty(verbose_name="物権番号")
    def put(self):
        self.datakey = str(db.Model.put(self))
        db.Model.put(self)

class editwhatsnew(webapp2.RequestHandler):
    def post(self):
        self.get()
    def get(self):
        key = self.request.get("key")
        submit = self.request.get("submit")
        isadd = self.request.get("isadd")
        bkID = self.request.get("bkID")
        date = self.request.get("date")
        text = self.request.get("text")
        enableshow = self.request.get("enableshow")
        if enableshow == "True" :
            enableshow = True
        else:
            enableshow = False
        if isadd == u"True":
            dbwt = dbwahatsnew(enableshow=enableshow , date=date,text=text,bkID=bkID)
            dbwt.put()
        if submit == u"削除":   
            wt = db.get(key)
            wt.delete()
        if submit == u"保存":
            wt = db.get(key)
            wt.bkID = bkID
            wt.date = date
            wt.text = text
            wt.enableshow = enableshow
            wt.put()
        dbwt = dbwahatsnew.all()
        dbwt.order("-date")
        list=dbwt.fetch(1000, 0)
        l = []
        for e in list:
            l.append(e)
        path = os.path.join( os.getcwd(),'templates','editwhatsnew.html')
        self.response.out.write(template.render(path, {"list":l}))
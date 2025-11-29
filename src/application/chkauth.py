#!/usr/local/bin/python
# -*- coding: utf-8 -*-


from google.appengine.api import urlfetch
import config
import re
#from google.appengine.ext import webapp
import webapp2
from application import session
import datetime
import cs
import base64
import json

DEFAULT_Auth_Day = 1

class dbsession(session.Session):

    def __init__(self, req, res, sid_name = session.DEFAULT_SID_NAME,sid=None):
        if sid:
            self.sid_value = sid
        else:
            session.Session.__init__(self,req, res, sid_name)


    def chkauth(self, request, response):
        if self.chk_ssn() : #セッションがある場合
            try:
                limit = self.get_ssn_data('timelimit')
                now = datetime.datetime.utcnow()
                if self.get_ssn_data('timelimit') < datetime.datetime.utcnow() :#タイムリミットを過ぎたとき
                    if self.getauth():
                        return True
                    else:
                        return False
                else:
                    if self.get_ssn_data('auth'):
                        return True
                    else:
                        return False
            except:
                if self.getauth():
                    return True
                else:
                    return False
        else: #セッションがない場合
            self.new_ssn()
            return False

    def getsid(self):
        if not self.sid_value:
            self.new_ssn()
        return self.sid_value

    def getauth(self):
        url = config.DATABASE_URL + "/jsonservice?com=chkAuthbysid&corp=s-style&site=www.s-style.ne.jp&sid=" + self.sid_value
        res = urlfetch.fetch( url = url, method=urlfetch.GET,
        deadline=120 ,
        headers={'Content-Type': 'application/x-www-form-urlencoded',
                 'User-Agent': 'www.chikusaku-mansion'} )
        strbuf = str(res.content)
        self.set_ssn_data('timelimit',datetime.datetime.utcnow() + datetime.timedelta(DEFAULT_Auth_Day))
        if re.search('error', strbuf) == None and re.search('Error', strbuf) == None :
            resdic = json.loads(res.content)
            if resdic.get("Auth") == "True":
                self.set_ssn_data('auth',True)
                return True
            else:
                self.set_ssn_data('auth',False)
                return False
        return False

class setsid(webapp2.RequestHandler):
    def get(self):
        self.post()
    def post(self):
        sid = self.request.get("sid")
        self.tmpl_val = {}
        dssn = dbsession(self.request,self.response)
        dssn.new_ssn(sid = sid)
        k = 'auth'
        v = True
        if sid:
            if dssn.getsid() <> sid:
                self.tmpl_val['sid'] = dssn.new_ssn(ssl=False, sid=sid)
            else:
                self.tmpl_val['sid'] = sid
        else:
            self.tmpl_val['sid'] = ''
            v = False
        dssn.set_ssn_data(k, v)
        k = 'timelimit'
        v = datetime.datetime.utcnow() + datetime.timedelta(DEFAULT_Auth_Day)
        dssn.set_ssn_data(k, v)


        self.response.headers['p3p']='CP="CAO PSA OUR"'
        """
        #Set-Cookie とかの処理
        2self.response.headers.add_header(
        3    "P3P",
        4    "CP=CAO PSA OUR"
        5)

        """
        str = u"""
        <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "https://www.w3.org/TR/html4/loose.dtd">
        <html>
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf8">
        <title>auth_iframe_contents</title>
        </head>
        <body>
        sid =""" + self.tmpl_val['sid'] + u"""
        </body>
        </html>
        """
        self.response.out.write(str)
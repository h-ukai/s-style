#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#
"""
将来memcacheを使うといいよ・・・・
Another login utility sample on Google AppEngine : Session

Author    : OKAZAKI Hiroki (okaz@teshigoto.net, https://www.teshigoto.net/)
Version   : $Id: session.py,v 1.3 2009/02/10 04:33:51 okaz Exp $
Copyright : Copyright (c) 2009 OKAZAKI Hiroki
License   : Python
"""

import os
import re
import time
import random
import hashlib
from google.appengine.api import memcache

from google.appengine.ext import db


class SessionDb(db.Expando):
    sid = db.StringProperty()


DEFAULT_SID_NAME = 'alu_001'

class Session():

    def __init__(self, req, res, sid_name=DEFAULT_SID_NAME):
        self.sid_name = sid_name
        self.req = req
        self.res = res
        if sid_name in req.cookies:
            self.sid_value = req.cookies[sid_name]
        else:
            self.sid_value = ''

    def new_ssn(self, ssl=False):
        if not self.sid_value:
            random.seed()
            random_str = str(random.random()) + str(random.random())
            random_str = random_str + str(time.time())
            random_str = random_str + os.environ['REMOTE_ADDR']
            self.sid_value = hashlib.sha256(random_str).hexdigest()

        cookie_val = self.sid_name + '=' + self.sid_value + ';path=/;expires=Tue, 1-Jan-2030 00:00:00 GMT' #サイトごとにクッキーを使いわけるなら設定すること
        if ssl:
            cookie_val += ';secure'

        self.res.headers.add_header('Set-Cookie', str(cookie_val))
        self.res.headers.add_header("P3P","CP=CAO PSA OUR")

        ssn_db = SessionDb(sid=self.sid_value)
        ssn_db.put()
        memcache.set(self.sid_value, ssn_db)
        return self.sid_value

    def dbdelete(self):
        if self.sid_value:
            ssn_db = SessionDb.all()
            ssn_db.filter('sid =', self.sid_value)
            ssn = ssn_db.fetch(1000)
            db.delete(ssn)
            memcache.delete(self.sid_value)
        #self.sid_value = None #2012/12/13 コメントアウト

    def destroy_ssn(self):
        self.dbdelete
        expires = time.strftime("%a, %d-%b-%Y %H:%M:%S GMT", time.gmtime(0))
        cookie_val = self.sid_name + '=null' + ';expires=' + expires
        self.res.headers.add_header('Set-Cookie', str(cookie_val))
        self.sid_value = None
        return self.sid_value

    def get_ssn_data(self, k):
        """
        ssn_db = SessionDb.all()
        ssn_db.filter('sid =', self.sid_value)
        ssn = ssn_db.fetch(1)

        return ssn[0]._dynamic_properties[k]
        """
        ssn=self.get_ssn()
        try:
            rs = ssn._dynamic_properties.get(k,None)
        except :
            rs = None
        return rs

    def set_ssn_data(self, k, v):
        """
        ssn_db = SessionDb.all()
        ssn_db.filter('sid =', self.sid_value)
        ssn = ssn_db.fetch(1)
        ssn[0]._dynamic_properties[k] = v
        ssn[0].put()
        """
        ssn = self.get_ssn()
        ssn._dynamic_properties[k] = v
        ssn.put()
        memcache.set(self.sid_value, ssn)


    def chk_ssn(self):
        ssn_db = SessionDb.all()
        ssn_db.filter('sid =', self.sid_value)
        count = 0
        for i in ssn_db:
            count += 1
        if count == 1:
            return True
        else:
            return False

    def get_ssn(self):
        ssn = memcache.get(self.sid_value)
        if not ssn:
            ssn_db = SessionDb.all()
            ssn_db.filter('sid =', self.sid_value)
            ssn = ssn_db.fetch(1)
            #Memcache
            if len(ssn):
                memcache.set(self.sid_value, ssn[0])
                return ssn[0]
            else:
                ssn_db = SessionDb(sid=self.sid_value)
                ssn_db.put()
                memcache.set(self.sid_value, ssn_db)
                return ssn_db
        return ssn

#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#
"""Another login utility sample on Google AppEngine : Session

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
import datetime
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


    def new_ssn(self, ssl=False, sid=None):
        if sid:
            if not self.chk_ssn() or sid !=self.sid_value:
                self.sid_value = sid
                ssn_db = SessionDb(sid=self.sid_value)
                ssn_db.put()
            self.sid_value = sid
        else:
            random.seed()
            random_str = str(random.random()) + str(random.random())
            random_str = random_str + str(time.time())
            random_str = random_str + os.environ['REMOTE_ADDR']
            self.sid_value = hashlib.sha256(random_str).hexdigest()
            ssn_db = SessionDb(sid=self.sid_value)
            ssn_db.put()

        cookie_val = self.sid_name + '=' + self.sid_value + ';path=/;expires=Tue, 1-Jan-2030 00:00:00 GMT'
        if ssl:
            cookie_val += ';secure'

        self.res.headers.add_header('Set-Cookie', str(cookie_val))


        return self.sid_value

    def destroy_ssn(self):
        ssn_db = SessionDb.all()
        ssn_db.filter('sid =', self.sid_value)
        ssn = ssn_db.fetch(1)
        db.delete(ssn)

        expires = time.strftime("%a, %d-%b-%Y %H:%M:%S GMT", time.gmtime(0))
        cookie_val = self.sid_name + '=null' + ';expires=' + expires
        self.res.headers.add_header('Set-Cookie', str(cookie_val))

        return self.sid_value

    def get_ssn_data(self, k):
        ssn_db = SessionDb.all()
        ssn_db.filter('sid =', self.sid_value)
        ssn = ssn_db.fetch(1)
        try:
            res = ssn[0]._dynamic_properties[k]
        except:
            res = None
        return res

    def set_ssn_data(self, k, v):
        ssn_db = SessionDb.all()
        ssn_db.filter('sid =', self.sid_value)
        ssn = ssn_db.fetch(1)
        ssn[0]._dynamic_properties[k] = v
        ssn[0].put()

    def chk_ssn(self):
        ssn_db = SessionDb.all()
        ssn_db.filter('sid =', self.sid_value)
        count = 0
        for i in ssn_db:
            if count > 0:
                i.delete()
            count += 1

        if count > 0:
            return True
        else:
            return False


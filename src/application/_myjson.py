# -*- coding: utf-8 -*-

# Copyright 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Utility classes and methods for use with simplejson and appengine.

Provides both a specialized simplejson encoder, GqlEncoder, designed to simplify
encoding directly from GQL results to JSON. A helper function, encode, is also
provided to further simplify usage.

  GqlEncoder: Adds support for GQL results and properties to simplejson.
  encode(input): Direct method to encode GQL objects as JSON.


このページから呼び出されるデータは基本的にFloatが整形される ***,***,***.*****ので注意

"""
#from google.appengine.ext import webapp
import webapp2
from django.utils import simplejson
import datetime
import timemanager
import re
import config
from google.appengine.api import memcache
from GqlEncoder import GqlJsonEncoder
import urllib

class jsonservice(webapp2.RequestHandler):


    def gettime(self,timestr,add=None):
        res = None
        if timestr:
            if re.compile(".*/.*/.* .*:.*:.*").match(timestr, 1):
                res = timemanager.jst2utc_date(datetime.datetime.strptime(timestr, "%Y/%m/%d %H:%M:%S"))
            elif re.compile(".*/.*/.*").match(timestr, 1):
                res = timemanager.jst2utc_date(datetime.datetime.strptime(timestr, "%Y/%m/%d"))
            elif re.compile(".*/.*").match(timestr, 1):
                res = timemanager.jst2utc_date(datetime.datetime.strptime(timestr, "%Y/%m"))
            if add:
                res += datetime.timedelta(days=add)
        return res

    def bklistGenerator(self,list):
        res = ""
        list_key=MesThread.bbs_key.get_value_for_datastore(thread)
        for i in range(0,list.count(1000000),50):
            if not res == "":
                s = GqlJsonEncoder(ensure_ascii=False).encode(db.get(list[i:i+50]))
                res = res[0:-1] + ", " + s[1:]
            else:
                res += GqlJsonEncoder(ensure_ascii=False).encode(db.get(list[i:i+50]))
        return res

    def _send_mail(self, email):
        msgbody = ''
        for key in self.request.arguments():
            msgbody += key + " : " + self.request.get(key) + "\n"
        message = mail.EmailMessage()
        message.sender = '"Another login utility" <' + config.ADMIN_EMAIL + '>'
        message.to = email
        message.subject = 'regist confirmation'
        message.body = msgbody
        message.send()

    def makedata(self,bkd,media):
        query_str = u"SELECT * FROM Blob WHERE CorpOrg_key = '" + bkd.nyrykkisyID + u"' AND Branch_Key = '" + bkd.nyrykstnID + u"' AND bkID = '" + bkd.bkID + u"' AND media = '" + media + u"' ORDER BY pos ASC"
        blobs = db.GqlQuery (query_str)
        b2 = []
        heimenzu = None
        for c in blobs:
            if c.pos != u"平面図":
                b2.append(c)
            else :
                heimenzu = c
        kakakuM = None
        if bkd.kkkuCnryu:
            kakakuM = GqlJsonEncoder.floatfmt(int(bkd.kkkuCnryu/100)/100)
        tknngt = None
        if bkd.cknngtSirk:
            # tknngt = bkd.cknngtSirk.year 20016/10/16
            tknngt = timemanager.utc2jst_date(bkd.cknngtSirk).year
            if int(tknngt) < 1989:
                tknngt = u"昭和" + str(tknngt-1925) + u"年"
            elif int(tknngt) >= 1989:
                tknngt = u"平成" + str(tknngt-1988) + u"年"
            else:
                tknngt = tknngt + u"年"
        data = GqlJsonEncoder.GQLmoneyfmt(bkd)
        entitys = {"bkdata":data,"picdata":b2,"kakakuM":kakakuM,"tknngtG":tknngt,"heimenzu":heimenzu}
        return entitys

    def get(self,**kwargs):
        self.post()

    def post(self,**kwargs):

        self.source = self.request.get("source")
        self.com = self.request.get("com")
        self.search_key = self.request.get("search_key")
        self.callback = self.request.get("callback")
        GqlJsonEncoder.fieldname = self.request.get("fieldname")
        GqlJsonEncoder.floatformat = self.request.get("floatformat")

        self.corp_name = "s-style" #本来はあり得ない企業名で初期化することそうすればmemberを得られない

        """
        #セッションチェック
        ssn = session.Session(self.request, self.response)
        if ssn.chk_ssn():
            user = ssn.get_ssn_data('user')
            corp = user.CorpOrg_key_name
        """

        try:
    #https://s-style-hrd.appspot.com/jsonservice?com=getcache&key=
    #com：getcache
    #memcacheからデータを取得します
    #パラメータ：
    #戻り値：{"bklistkey":}
            elif self.com == "getcache":
                key = self.request.get("key")
                """
                #セッションチェック
                ssn = session.Session(self.request, self.response)
                if ssn.chk_ssn():
                    user = ssn.get_ssn_data('user')
                    corp = user.CorpOrg_key_name
                """
                cacheddata = memcache.get(key)
                entitys = {"data":cacheddata}

            else:
                entitys = {"result":"error","error_msg":"Undefined Commande"}
            #データを得る
            #"SELECT * FROM Greeting where content >= :1 and content < :2 ", search_key, search_key + u"\uFFFD"
            #プロパティのトリミングはクライアント側でやってもらう
            self.response.content_type='application/json'
            if self.callback:
                    self.response.out.write("%s(%s);" %
                            (self.callback, GqlJsonEncoder(ensure_ascii=False).encode(entitys)))
#                            (self.callback, self.listGenerator(entitys)))
            else:
                self.response.out.write(GqlJsonEncoder(ensure_ascii=False).encode(entitys))
#                self.response.out.write(self.listGenerator(entitys))

            #GqlEncoder(ensure_ascii=False).encode(mymodel)

        except:
            entitys = {"result":"error","error_msg":traceback.format_exc()}
            self.response.content_type='application/json'
            if self.callback:
                    self.response.out.write("%s(%s);" %
                            (self.callback, GqlJsonEncoder(ensure_ascii=False).encode(entitys)))
            else:
                self.response.out.write(GqlJsonEncoder(ensure_ascii=False).encode(entitys))



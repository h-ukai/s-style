#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from __future__ import with_statement
try:
    import simplejson as json
except ImportError:
    import json


import os
from google.appengine.api import app_identity

import cloudstorage as gcs

from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.api import urlfetch
from google.appengine.api import taskqueue
import config
import re
#from google.appengine.ext import webapp
import webapp2
import logging


class jcachedata(db.Model):
    timestamp = db.DateTimeProperty(verbose_name=u"更新年月日",auto_now=True)
    listid = db.StringProperty(required=True)
    blob_key = db.StringProperty()
    blob_url = db.StringProperty()
    stored = db.BooleanProperty(default=False)
    cached = db.BooleanProperty(default=False)
    data = db.TextProperty()


class jcache(object):
    MB = 1000000
    @classmethod
    def get(cls,key,mode=None,reqhn=None):
        if key:
            logging.info('jcache.get:key:' + key)
            jcache_db = jcachedata.get_by_key_name(key)
            if not jcache_db:
                #raise jcacheError(u"jcache.Nodatainjcache_dbError:" + key)
                return None
            if jcache_db.cached:
                data = memcache.get(key,None)
                #data = None #テスト用
                if data:
                    return data
            filename = jcache_db.blob_key
            logging.info('jcache.get:filename:' + filename)

            with gcs.open(filename, 'r') as f:
                    blob_concat = f.read()
            """
            start = 0
            end = blobstore.MAX_BLOB_FETCH_SIZE - 1
            step = blobstore.MAX_BLOB_FETCH_SIZE - 1
            while start < file_size:
                blob_concat += blobstore.fetch_data(blob_key, start, end)
                temp_end = end
                start = temp_end + 1
                end = temp_end + step
            """
            return blob_concat
        else:
            raise jcacheError(u"jcache.blob_infoError:" + key)

    @classmethod
    def getdict(cls,key):
        try:
            data = cls.get(key)
            datadict = json.loads(data)
        except:
            datadict = None
        return datadict

    @classmethod
    def put(cls,key,data):
        logging.info('jcache.put:key:' + key)
        if data and len(data)>10:
            if len(data) > cls.MB*32:
                raise jcacheError(u"jcache.oversizeError:key " + key +u"size " + str(len(data)))
            jcache_db = jcachedata.get_or_insert(key,listid = key)
            memcache.delete(key, seconds=0)
            if len(data) < cls.MB and key:
                if memcache.add(key, data, 7200):
                    jcache_db.cached = True
                else:
                    jcache_db.cached = False
            elif key:
                jcache_db.cached = False

            # ファイル作成
            #file_name = files.blobstore.create(mime_type='application/json', _blobinfo_uploaded_filename=key)
            # ファイルの中身を書き込む
            # Open the file and write to it
            if key:
                bucket_name = os.environ.get('BUCKET_NAME',
                                 app_identity.get_default_gcs_bucket_name())
                bucket = '/' + bucket_name
                filename = bucket + '/' +key
                #with files.open(key, 'a') as f:
                write_retry_params = gcs.RetryParams(backoff_factor=1.1)
                with gcs.open(filename, 'w',
                              content_type='text/plain',
                              retry_params=write_retry_params) as f:
                    f.write(data)
                    f.close()
                # files.finalize(file_name)
                # ファイルデータを格納 (flush)
                # Blob キーを取得
                jcache_db.blob_key = filename
                jcache_db.stored = True
                jcache_db.put()
                logging.info('jcache.put:filename:' + filename)
                return True
            else:
                jcache_db.stored = False
                jcache_db.put()
                raise jcacheError(u"jcache.put.keyError:" + key)
        return False

class jsonsearvebklistdata(webapp2.RequestHandler):
    #https://www.s-style.ne.jp/jsonservice?msgID=709005
    def get(self):
        key = self.request.get('msgID',None)
        data = jcache.get(key)
        callback = self.request.get("callback")
        if callback:
            self.response.headers['Content-Type'] = "text/javascript"
            self.response.headers['charset'] = "utf-8"
            self.response.out.write(callback + "(" + data + ")" )
            #self.response.out.write("%s(%s);" % (callback, data))
        else:
            self.response.headers['Content-Type'] = "application/json"
            self.response.he_myjsons['charset'] = "utf-8"
            self.response.out.write(data)

class getjson(webapp2.RequestHandler):
    def get(self):
        self.post()
    def post(self):
        #/tasks/getjson?msgID=606251
        #ローカルテスト時にコメントアウト
        if( int(self.request.headers.environ['HTTP_X_APPENGINE_TASKRETRYCOUNT']) > 3):
            logging.error('jog retry error(over 3 times)')
            return
        #TaskQueueはPOSTでアクセスするので注意！！
        key = self.request.get('msgID',None)
        url = config.DATABASE_URL + "jsonservice?com=getBKlistKeyonly&key=" + key
        res = urlfetch.fetch( url = url, method=urlfetch.GET,
            deadline=120 ,
            headers={'Content-Type': 'application/x-www-form-urlencoded',
                     'User-Agent': 'www.s-style.ne.jp'} )
        bklist = ""
        strbuf = str(res.content)
        if re.search('error', strbuf) == None and re.search('Error', strbuf) == None :
            bklist = json.loads(strbuf)
        else:
            raise jcacheError(u"jcache.dataError:" + key + " " + url)

        chanksize = 30
        listcount = len(bklist)
        jsondata = ""


        """
        keylist = bklist[0:chanksize]
        keys = ",".join(keylist)
        url = config.DATABASE_URL + "jsonservice?com=getBKlistbykeylist&media=web&field=normal&keylist=" + keys
        res = urlfetch.fetch( url = url, method=urlfetch.GET,
            deadline=120 ,
            headers={'Content-Type': 'application/x-www-form-urlencoded',
                     'User-Agent': 'www.chikusaku-mansion'} )
        strbuf = str(res.content)
        if re.search('error', strbuf) == None and re.search('Error', strbuf) == None :
            jsondata += strbuf
        else:
            raise jcacheError(u"jcache.dataError:" + key + " " + url)
        jcache.put(key,jsondata)
        self.response.out.write(jcache.get(key))
        return
        """

        for i in range(0,listcount,chanksize):
            keylist = bklist[i:i+chanksize]
            keys = ",".join(keylist)
            url = config.DATABASE_URL + "jsonservice?com=getBKlistbykeylist&media=web&field=normal&keylist=" + keys
            res = urlfetch.fetch( url = url, method=urlfetch.GET,
                deadline=120 ,
                headers={'Content-Type': 'application/x-www-form-urlencoded',
                         'User-Agent': 'www.s-style.ne.jp'} )
            strbuf = str(res.content)
            if re.search('error', strbuf) == None and re.search('Error', strbuf) == None :
                jsondata += strbuf[1:-1] + ","
            else:
                raise jcacheError(u"jcache.dataError:" + key + " " + url)
        jsondata = "[" + jsondata[0:-1]+"]"
        jcache.put(key,jsondata)
        self.response.out.write(jcache.get(key))


class getjsonold(webapp2.RequestHandler):
    def get(self):
        self.post()
    def post(self):

        if( int(self.request.headers.environ['HTTP_X_APPENGINE_TASKRETRYCOUNT']) > 3):
            logging.error('jog retry error(over 3 times)')
            return

        #TaskQueueはPOSTでアクセスするので注意！！
        key = self.request.get('msgID',None)
        #url = config.DATABASE_URL + "/jsonservice?com=getBKlistKey&field=normal&key=" + key
        url = config.DATABASE_URL + "/jsonservice?com=getBKlistbymesID&media=web&field=normal&mesID=" + key
        res = urlfetch.fetch( url = url, method=urlfetch.GET,
            deadline=120 ,
            headers={'Content-Type': 'application/x-www-form-urlencoded',
                     'User-Agent': 'www.s-style.ne.jp'} )
        strbuf = str(res.content)
        jcache.put(key,strbuf)
        self.response.out.write(jcache.get(key))

class cronworker(webapp2.RequestHandler):
    def get(self):
        params = [709005,693780,1899136,1915096] #sおすすめ ,sプレミアム,広告可,全物件
        mytask = taskqueue.Queue('mintask')
        for p in params:
            task = taskqueue.Task(url='/tasks/getjson',params={"msgID":str(p)},target='memdb')
            #task = taskqueue.Task(url='/tasks/getjson',params={"msgID":str(p)})
            mytask.add(task)

class jcacheError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
#!/usr/local/bin/python
# -*- coding: utf-8 -*-


from google.appengine.api import urlfetch

from django.utils import simplejson
from google.appengine.api import memcache
import time
import config

class httpaccess(object):

    @classmethod
    def get_urlfetch(cls,key):
        url = config.DATABASE_URL + key
        res = urlfetch.fetch( url = url, method=urlfetch.GET,
        deadline=120 ,
        headers={'Content-Type': 'application/x-www-form-urlencoded',
                 'User-Agent': 'chikusaku-mansion'} )
        try:
            datadict = simplejson.loads(res.content)
        except:
            datadict = None
        #data[0]['info'],bk,key
        #for item in simplejson.loads(content)['responseData']['results']:
        #xml = res.content
        
        return datadict

    @classmethod
    def get_data_mem(cls,key):
        data = None
        data = memcache.get(key)
        return data
        """
        if data is not None:
            return data
        else:
            cls.get_data(key)
        """
    @classmethod
    def get_data(cls,key):
        
        data = cls.get_urlfetch(key)
        # Add a value if it doesn't exist in the cache, with a cache expiration of 1 hour.
        if data:
            if isinstance(data,list) or not data.get("result","")=="error":
                memcache.add(key, data, 72000)
            else:
                data = None
        return data

    @classmethod
    def search_data(cls,key):
        #https://s-style-hrd.appspot.com/jsonservice?com=searchbkdata&dtsyuri=サンプル&submit=新規ページへ保存して検索
        #戻り値：{"bklistkey":}
        key2=None
        dat2=None
        dat = cls.get_data(u"jsonservice?com=searchbkdata&submit=新規ページへ保存して検索2&" + key)
        if dat != None :
            bklistkey = str(dat.get("bklistkey",""))
            key2 = u"jsonservice?com=getfolbyID&id="  + bklistkey
            dat2 = cls.get_data(key2)            
            count1 = 0
            while count1 < 300 : #５分待つ
                title = dat2.get(u"表題","")
                if title.split(" ")[0]==u"検索結果":
                    key3 = u"jsonservice?com=getBKlistKey&field=normal&key=" + bklistkey
                    dat3 = cls.get_data(key3)
                    break
                time.sleep(10) #１０秒待つ
                count1 += 1
                dat2 = cls.get_data(key2)
            if dat3 != None :
                memcache.add(u"allbkdata", dat3, 72000)
            else:
                raise TaskError("error:" + key2)
        else:
            raise TaskError(u"error:jsonservice?com=searchbkdata&submit=新規ページへ保存して検索2&" + key)
        return dat3

    @classmethod
    def search_data_mem(cls,key):
        #https://s-style-hrd.appspot.com/jsonservice?com=searchbkdata&dtsyuri=サンプル&submit=新規ページへ保存して検索
        #戻り値：{"bklistkey":}
        dat = cls.get_data_mem(u"allbkdata")
        return dat


class TaskError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
# -*- coding: utf-8 -*-
"""
JSON Cache module - Flask version (Python 3.11)

キャッシュされた物件データを提供
"""

import json
import os
import re
import logging

from flask import request, make_response
from google.cloud import ndb
from google.cloud import storage
from google.cloud import tasks_v2

from application import config


class jcachedata(ndb.Model):
    """JSON キャッシュデータモデル"""
    timestamp = ndb.DateTimeProperty(auto_now=True)
    listid = ndb.StringProperty(required=True)
    blob_key = ndb.StringProperty()
    blob_url = ndb.StringProperty()
    stored = ndb.BooleanProperty(default=False)
    cached = ndb.BooleanProperty(default=False)
    data = ndb.TextProperty()


class jcache:
    """JSON キャッシュユーティリティクラス"""
    MB = 1000000
    BUCKET_NAME = os.environ.get('GCS_BUCKET_NAME', 's-style-hrd-jcache')

    @classmethod
    def _get_storage_client(cls):
        """GCS クライアントを取得"""
        return storage.Client()

    @classmethod
    def get(cls, key, mode=None, reqhn=None):
        """キャッシュからデータを取得"""
        if not key:
            raise jcacheError("jcache.blob_infoError: key is empty")

        logging.info(f'jcache.get:key:{key}')
        jcache_db = jcachedata.get_by_id(key)

        if not jcache_db:
            return None

        filename = jcache_db.blob_key
        if not filename:
            return None

        logging.info(f'jcache.get:filename:{filename}')

        try:
            client = cls._get_storage_client()
            object_name = filename.split('/')[-1] if '/' in filename else filename

            bucket = client.bucket(cls.BUCKET_NAME)
            blob = bucket.blob(object_name)
            data = blob.download_as_text()
            return data
        except Exception as e:
            logging.error(f'jcache.get error: {e}')
            return None

    @classmethod
    def getdict(cls, key):
        """キャッシュからデータを取得し、辞書として返す"""
        try:
            data = cls.get(key)
            if data:
                return json.loads(data)
        except Exception as e:
            logging.error(f'jcache.getdict error for key {key}: {e}')
        return None

    @classmethod
    def put(cls, key, data):
        """データをキャッシュに保存"""
        logging.info(f'jcache.put:key:{key}')

        if not data or len(data) <= 10:
            return False

        if len(data) > cls.MB * 32:
            raise jcacheError(f"jcache.oversizeError:key {key} size {len(data)}")

        jcache_db = jcachedata.get_by_id(key)
        if not jcache_db:
            jcache_db = jcachedata(id=key, listid=key)

        if not key:
            jcache_db.stored = False
            jcache_db.put()
            raise jcacheError(f"jcache.put.keyError:{key}")

        try:
            client = cls._get_storage_client()
            bucket = client.bucket(cls.BUCKET_NAME)
            blob = bucket.blob(key)
            blob.upload_from_string(data, content_type='application/json')

            jcache_db.blob_key = f'/{cls.BUCKET_NAME}/{key}'
            jcache_db.stored = True
            jcache_db.cached = False
            jcache_db.put()

            logging.info(f'jcache.put:filename:/{cls.BUCKET_NAME}/{key}')
            return True

        except Exception as e:
            logging.error(f'jcache.put error: {e}')
            jcache_db.stored = False
            jcache_db.put()
            raise


class jcacheError(Exception):
    """jcache エラークラス"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def getjson_route():
    """
    getjson ハンドラ - タスクキューから呼び出される
    """
    import requests as http_requests

    retry_count = request.headers.get('X-CloudTasks-TaskRetryCount', '0')
    if int(retry_count) > 3:
        logging.error('getjson retry error (over 3 times)')
        return 'retry limit exceeded', 200

    key = request.args.get('msgID') or request.form.get('msgID')
    if not key:
        return 'msgID required', 400

    try:
        url = f"{config.DATABASE_URL}jsonservice?com=getBKlistKeyonly&key={key}"
        res = http_requests.get(
            url,
            timeout=120,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'www.s-style.ne.jp'
            }
        )

        strbuf = res.text
        if re.search('error', strbuf, re.IGNORECASE):
            raise jcacheError(f"jcache.dataError:{key} {url}")

        bklist = json.loads(strbuf)

        chunksize = 30
        listcount = len(bklist)
        jsondata = ""

        for i in range(0, listcount, chunksize):
            keylist = bklist[i:i+chunksize]
            keys = ",".join(keylist)
            url = f"{config.DATABASE_URL}jsonservice?com=getBKlistbykeylist&media=web&field=normal&keylist={keys}"

            res = http_requests.get(
                url,
                timeout=120,
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'User-Agent': 'www.s-style.ne.jp'
                }
            )

            strbuf = res.text
            if re.search('error', strbuf, re.IGNORECASE):
                raise jcacheError(f"jcache.dataError:{key} {url}")

            jsondata += strbuf[1:-1] + ","

        jsondata = "[" + jsondata[:-1] + "]"
        jcache.put(key, jsondata)

        return jcache.get(key) or '', 200

    except Exception as e:
        logging.error(f'getjson error: {e}')
        return str(e), 500


def cronworker_route():
    """
    cronworker ハンドラ - Cron から呼び出される
    """
    # sおすすめ, sプレミアム, 広告可, 全物件
    params = [709005, 693780, 1899136, 1915096]

    project = os.environ.get('GCP_PROJECT', 's-style-hrd')
    location = os.environ.get('CLOUD_TASKS_LOCATION', 'asia-northeast1')
    queue = os.environ.get('CLOUD_TASKS_QUEUE', 'mintask')

    try:
        client = tasks_v2.CloudTasksClient()
        parent = client.queue_path(project, location, queue)

        for p in params:
            task = {
                'app_engine_http_request': {
                    'http_method': tasks_v2.HttpMethod.POST,
                    'relative_uri': f'/test/tasks/getjson?msgID={p}',
                }
            }

            client.create_task(request={'parent': parent, 'task': task})
            logging.info(f'Task created for msgID: {p}')

        return 'Tasks queued', 200

    except Exception as e:
        logging.error(f'cronworker error: {e}')
        return str(e), 500


def jsonservice_route():
    """
    JSON データ提供ハンドラ
    """
    key = request.args.get('msgID')
    if not key:
        return 'msgID required', 400

    data = jcache.get(key)
    callback = request.args.get('callback')

    if callback:
        response = make_response(f'{callback}({data})')
        response.headers['Content-Type'] = 'text/javascript; charset=utf-8'
    else:
        response = make_response(data or '')
        response.headers['Content-Type'] = 'application/json; charset=utf-8'

    return response

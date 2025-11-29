#!/usr/local/bin/python
# -*- coding: utf-8 -*-

#from google.appengine.ext import webapp
import webapp2
#from django.utils import simplejson
import json
from google.appengine.api import taskqueue
from jcache import jcache
import logging
from models.address import address2

class bksorttask(webapp2.RequestHandler):
    def get(self):
        mytask = taskqueue.Queue('mintask')
        task = taskqueue.Task(url='/tasks/bksrot',params={})
        mytask.add(task)

class bksort(webapp2.RequestHandler):
    def get(self):
        self.post()

    def post(self):
        """
        if( int(self.request.headers.environ['HTTP_X_APPENGINE_TASKRETRYCOUNT']) > 3):
            logging.error('jog retry error(over 3 times)')
            return
        """
        self.setdat()

    def setdat(self):
        datakey1 = "1915096"  #全物件
        dat1 = jcache.getdict(datakey1)
        if dat1 != None and len(dat1)>1:
            for x in dat1:
                if not (x['bk']['bkdata'].get('tdufknmi') or x['bk']['bkdata'].get('shzicmi1')):
                    pass
            dat1.sort(cmp=lambda x,y:cmp([x['bk']['bkdata'].get('tdufknmi'),x['bk']['bkdata'].get('shzicmi1'),x['bk']['bkdata'].get('shzicmi2')],[y['bk']['bkdata'].get('tdufknmi'),y['bk']['bkdata'].get('shzicmi1'),y['bk']['bkdata'].get('shzicmi2')]), reverse=False)
        dat2 = address2.all()
        dat2.filter("shikutyosonmei =",u'名古屋市千種区' )
        dat2.order("todofukenmei")
        dat2.order("shikutyosonmei")
        dat2.order("ooazatyotyome")
        c1=0
        c2=0
        """
        #売買賃貸区分
        bbchntikbn = db.StringProperty(verbose_name=u"売買賃貸区分", choices=set([u"売買", u"賃貸", u"その他"]))
        #取扱い種類
        dtsyuri = db.StringProperty(verbose_name=u"データ種類", choices=set([u"物件",u"事例",u"予約",u"商談中",u"査定中",u"重複",u"停止",u"競売",u"現場",u"サンプル", u"その他"]))
        #物件種別
        bkknShbt = db.StringProperty(verbose_name=u"物件種別", choices=set([u"土地", u"戸建住宅等", u"マンション等", u"住宅以外の建物全部", u"住宅以外の建物一部",u"賃貸一戸建",u"賃貸マンション",u"賃貸土地",u"賃貸外全",u"賃貸外一", u"その他"]))
        #物件種目
        bkknShmk = db.StringProperty(verbose_name=u"物件種目", choices=set([u"売地", u"借地権", u"底地権",u"新築戸建",u"中古戸建",u"新築テラス",u"中古テラス", u"店舗", u"店舗付住宅", u"住宅付店舗",u"新築マンション",u"中古マンション",u"新築タウン",u"中古タウン",u"新築リゾート",u"中古リゾート",u"店舗事務所", u"ビル", u"工場", u"マンション", u"倉庫", u"アパート", u"寮", u"旅館", u"ホテル", u"別荘", u"リゾート", u"文化住宅", u"貸家",u"テラス",u"マンション",u"タウン",u"間借り",u"居住用地",u"事業用地",u"店舗戸建",u"旅館等",u"寮",u"住宅付店舗戸建",u"店舗事務所",u"店舗一部",u"事務所",u"住宅付店舗一部",u"マンション一室",u"その他"]))
                 土地    新築戸建    中古戸建    中古ﾏﾝｼｮﾝ    物件収益    賃貸物件
        """
        cdata = [{'todofukenmei':'','shikutyosonmei':'','ooazatyotyome':'','tochi':0,'shinko':0,'cyuko':0,'cyukoman':0,'syueki':0,'chin':0}]
        if dat1 == None:
            dat1 = [{'bk':{'bkdata':{'shzicmi2':""}}}]
        l1 = len(dat1)
        l2 = dat2.count()
        if l2 == 0:
            dat2 = address2(todofukenmei='',shikutyosonmei='',ooazatyotyome='')
            dat2.put()
            dat2 = [dat2]
        c = 1
        logging.info('l1:' + str(l1) + ' l2:'+ str(l2))
        while 1:
            d1 = dat1[c1]
            d2 = dat2[c2]
            if (d1['bk']['bkdata'].get('tdufknmi') > d2.todofukenmei) or(d1['bk']['bkdata'].get('tdufknmi') == d2.todofukenmei and d1['bk']['bkdata'].get('shzicmi1') > d2.shikutyosonmei) or (d1['bk']['bkdata'].get('tdufknmi') == d2.todofukenmei and d1['bk']['bkdata'].get('shzicmi1') == d2.shikutyosonmei and d1['bk']['bkdata'].get('shzicmi2') > d2.ooazatyotyome):
                if cdata[-1]['ooazatyotyome'] ==  d2.ooazatyotyome :
                    pass
                else:
                    obj={'todofukenmei':d2.todofukenmei,'shikutyosonmei':d2.shikutyosonmei,'ooazatyotyome':d2.ooazatyotyome}
                    if cdata[-1]['shikutyosonmei'] != obj['shikutyosonmei']:
                        c = 1
                    if (c+1) % 4 == 0 or c % 4 == 0:
                        obj['gray']=True
                    c += 1
                    if not cdata[-1].get('left',False) or (cdata[-1].get('todofukenmei') != d2.todofukenmei or cdata[-1].get('shikutyosonmei') != d2.shikutyosonmei):
                        obj['left']=True
                    cdata.append(obj)
                c2 += 1
                if c2 >= l2 : #d2が先に終わってしまった場合
                    while 1 :
                        if d1['bk']['bkdata'].get('shzicmi2') == u'小木東１丁目':
                            pass

                        if cdata[-1]['ooazatyotyome'] ==  d1['bk']['bkdata'].get('shzicmi2'):
                            obj=cdata[-1]
                        else:
                            obj={'todofukenmei':d1['bk']['bkdata'].get('tdufknmi'),'shikutyosonmei':d1['bk']['bkdata'].get('shzicmi1'),'ooazatyotyome':d1['bk']['bkdata'].get('shzicmi2')}
                            if cdata[-1]['shikutyosonmei'] != obj['shikutyosonmei']:
                                c = 1
                            if (c+1) % 4 == 0 or c % 4 == 0:
                                obj['gray']=True
                            c += 1
                            if not cdata[-1].get('left',False) or (cdata[-1].get('todofukenmei') != d1['bk']['bkdata'].get('tdufknmi') or cdata[-1].get('shikutyosonmei') != d1['bk']['bkdata'].get('shzicmi1')):
                                obj['left']=True
                            cdata.append(obj)
                        if d1['bk']['bkdata'].get('bbchntikbn') == u'賃貸':
                            obj['chin']=obj.get('chin',0)+1
                        else:
                            if u's収益' in d1['bk']['bkdata'].get('icons',[]):
                                obj['syueki']=obj.get('syueki',0)+1
                            if d1['bk']['bkdata'].get('bkknShmk') == u'売地':
                                obj['tochi']=obj.get('tochi',0)+1
                            if d1['bk']['bkdata'].get('bkknShmk') == u'新築戸建':
                                obj['shinko']=obj.get('shinko',0)+1
                            if d1['bk']['bkdata'].get('bkknShmk') == u'中古戸建':
                                obj['cyuko']=obj.get('cyuko',0)+1
                            if d1['bk']['bkdata'].get('bkknShmk') == u'中古マンション':
                                obj['cyukoman']=obj.get('cyukoman',0)+1
                        c1 += 1
                        if c1 == l1:
                            break
                        d1 = dat1[c1]
                    break
            else:
                if cdata[-1]['ooazatyotyome'] ==  d1['bk']['bkdata'].get('shzicmi2'):
                    obj=cdata[-1]
                else:
                    obj={'todofukenmei':d1['bk']['bkdata'].get('tdufknmi'),'shikutyosonmei':d1['bk']['bkdata'].get('shzicmi1'),'ooazatyotyome':d1['bk']['bkdata'].get('shzicmi2')}
                    if cdata[-1]['shikutyosonmei'] != obj['shikutyosonmei']:
                        c = 1
                    if (c+1) % 4 == 0 or c % 4 == 0:
                        obj['gray']=True
                    c += 1
                    if not cdata[-1].get('left',False) or (cdata[-1].get('todofukenmei') != d1['bk']['bkdata'].get('tdufknmi') or cdata[-1].get('shikutyosonmei') != d1['bk']['bkdata'].get('shzicmi1')):
                        obj['left']=True
                    cdata.append(obj)
                if d1['bk']['bkdata'].get('bbchntikbn') == u'賃貸':
                    obj['chin']=obj.get('chin',0)+1
                else:
                    if u's収益' in d1['bk']['bkdata'].get('icons',[]):
                        obj['syueki']=obj.get('syueki',0)+1
                    if d1['bk']['bkdata'].get('bkknShmk') == u'売地':
                        obj['tochi']=obj.get('tochi',0)+1
                    if d1['bk']['bkdata'].get('bkknShmk') == u'新築戸建':
                        obj['shinko']=obj.get('shinko',0)+1
                    if d1['bk']['bkdata'].get('bkknShmk') == u'中古戸建':
                        obj['cyuko']=obj.get('cyuko',0)+1
                    if d1['bk']['bkdata'].get('bkknShmk') == u'中古マンション':
                        obj['cyukoman']=obj.get('cyukoman',0)+1
                c1 += 1
                if c1 >= l1 : #d1データが先に終わってしまったら
                    while 1 :
                        if cdata[-1]['ooazatyotyome'] ==  d2.ooazatyotyome :
                            pass
                        else:
                            obj={'todofukenmei':d2.todofukenmei,'shikutyosonmei':d2.shikutyosonmei,'ooazatyotyome':d2.ooazatyotyome}
                            if cdata[-1]['shikutyosonmei'] != obj['shikutyosonmei']:
                                c = 1
                            if (c+1) % 4 == 0 or c % 4 == 0:
                                obj['gray']=True
                            c += 1
                            if not cdata[-1].get('left',False) or (cdata[-1].get('todofukenmei') != d2.todofukenmei or cdata[-1].get('shikutyosonmei') != d2.shikutyosonmei):
                                obj['left']=True
                            cdata.append(obj)
                        c2 += 1
                        if c2 == l2:
                            break
                        d2 = dat2[c2]
                    break
        cdata.pop(0)
        jdata = json.dumps(cdata)
        jcache.put('namedata',jdata)
        self.response.out.write(jdata)
        """
        for d in dat:
            obj={}
            obj['name'] = d['bk']['bkdata'].get('ttmnmi')
            obj['count'] = 0
            for d2 in dat2:
                if d2['bk']['bkdata'].get('ttmnmi') == d['bk']['bkdata'].get('ttmnmi'):
                    obj['count'] += 1
            cdata.append(obj)
        """
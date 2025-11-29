# -*- coding: utf-8 -*-
#      位置参照情報ダウンロードサービス
#      https://nlftp.mlit.go.jp/isj/index.html
#      地名データ

from google.appengine.ext import db
import datetime

class address1(db.Model):
    #市区町村コード
    cityno = db.StringProperty(verbose_name=u"市区町村コード")
    #都道府県名
    todofukenmei = db.StringProperty(verbose_name=u"都道府県名")
    #市区町村名
    shikutyosonmei = db.StringProperty(verbose_name=u"市区町村名")


class address2(db.Model):
    #都道府県名
    todofukenmei = db.StringProperty(verbose_name=u"都道府県名")
    #市区町村名
    shikutyosonmei = db.StringProperty(verbose_name=u"市区町村名")
    #大字・町丁目
    ooazatyotyome = db.StringProperty(verbose_name=u"大字・町丁目")

class address3(db.Model):
    #都道府県名
    todofukenmei = db.StringProperty(verbose_name=u"都道府県名")
    #市区町村名
    shikutyosonmei = db.StringProperty(verbose_name=u"市区町村名")
    #大字・町丁目
    ooazatyotyome = db.StringProperty(verbose_name=u"大字・町丁目")
    #街区符号・地番
    gaikubanchi = db.StringProperty(verbose_name=u"街区符号・番地")
    #座標系番号
    zahyoukeibangou = db.IntegerProperty(verbose_name=u"座標系番号")
    # Ｘ座標
    x = db.FloatProperty(verbose_name=u"Ｘ座標")
    # Ｙ座標
    y = db.FloatProperty(verbose_name=u"Ｙ座標")    
    #緯度
    lat = db.FloatProperty(verbose_name=u"緯度")
    #経度
    lng = db.FloatProperty(verbose_name=u"経度")    
    #住居表示フラグ
    jukyohyojiflg = db.StringProperty(verbose_name=u"住居表示フラグ")
    #代表フラグ
    daihyoflg = db.StringProperty(verbose_name=u"代表フラグ")
    #更新前履歴フラグ
    kousinmaerirekiflg = db.StringProperty(verbose_name=u"更新前履歴フラグ")
    #更新後履歴フラグ
    kousingorirekiflg = db.StringProperty(verbose_name=u"更新後履歴フラグ")
    
    
    
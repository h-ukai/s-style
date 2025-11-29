#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

class UtcTzinfo(datetime.tzinfo):
    # Coordinated Universal 

    def utcoffset(self, dt):
        return datetime.timedelta(0)

    def dst(self, dt):
        return datetime.timedelta(0)

    def tzname(self, dt):
        return 'UTC'

    def olsen_name(self):
        return 'UTC'

class JstTzinfo(datetime.tzinfo):
    # Japanese Standard Time

    def utcoffset(self, dt):
        return datetime.timedelta(hours=9)

    def dst(self, dt):
        return datetime.timedelta(0)

    def tzname(self, dt):
        return 'JST'

    def olsen_name(self):
        return 'Asia/Tokyo'

def utc2jst_date(value):
    if value:
        value = value.replace(tzinfo=UtcTzinfo()).astimezone(JstTzinfo())
    return value

def jst2utc_date(value):
    if value:
        value = value.replace(tzinfo=JstTzinfo()).astimezone(UtcTzinfo())
    return value

def utc2jst_gql(gql):    
    properties = gql.properties().items()
    for field, value in properties:
        v =  getattr(gql, field)
        if isinstance( v, datetime.datetime):
            setattr(gql,field,utc2jst_date(v))
    return gql

def jst2utc_gql(gql):    
    properties = gql.properties().items()
    for field, value in properties:
        v =  getattr(gql, field)
        if isinstance( v, datetime.datetime):
            setattr(gql,field,jst2utc_date(v))
    return gql


"""月末、月初のdatetime.dateオブジェクトを返す。
Oracleのadd_months互換の月加減。
"""
from calendar import monthrange

def first_day(date):
    """月初を返す"""
    return datetime.date(date.year, date.month, 1)

def is_last_day(date):
    """月末日付ならTrueを返す"""
    return days_of_month(date.year, date.month) == date.day

def days_of_month(year,month):
    """年,月の日数を返す"""
    return monthrange(year, month)[1]

def last_day(date):
    """月末を返す"""
    return datetime.date(year=date.year, month=date.month, day=days_of_month(date.year, date.month))

def add_months(date,months):
    """月を加減する。
    dateにはdatetime.dateクラスのオブジェクト
    monthsには整数で月数を指定する。
    月末をOracleのadd_months互換の方法で処理する。
    例えば、
    2007年2月28日（月末）に1ヶ月足すと3月31日（月末）。
    2008年2月29日（月末）に1ヶ月足すと2008年3月31日（月末）。
    2008年2月28日（月末ではない）に1ヶ月足すと2008年3月28日（同じ日）。
    """
    if months==0:
        return date

    year, month = divmod(date.month + months, 12)
    year = year + date.year

    #ちょうど割り切れたら12月で、マイナス1年。
    if month == 0:
        month = 12
        year = year - 1

    #入力日付がその月の月末なら、加算後月の日数を。
    #そうじゃなければ入力日付の日。
    day = date.day
    if date.day > days_of_month(year, month):
        day = days_of_month(year, month)
    return datetime.date(year=year, month=month, day=day)

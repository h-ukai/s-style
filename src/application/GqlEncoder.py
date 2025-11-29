# -*- coding: utf-8 -*-

from django.utils import simplejson
from google.appengine.ext import db
import datetime
import time
from google.appengine.api import users
from decimal import *
import locale
import timemanager

class GqlJsonEncoder(simplejson.JSONEncoder):

    """Extends JSONEncoder to add support for GQL results and properties.

  Adds support to simplejson JSONEncoders for GQL results and properties by
  overriding JSONEncoder's default method.
    """
    fieldname = ""
    floatformat = ""
# TODO Improve coverage for all of App Engine's Property types.

    def default(self, obj):
        """Tests the input object, obj, to encode as JSON."""
        if hasattr(obj, '__json__'):
            return getattr(obj, '__json__')()

        if isinstance(obj, db.GqlQuery):
            return list(obj)
        
        elif isinstance(obj, db.Model):
            properties = obj.properties().items()
            output = {}
            for field, value in properties:
                try:
                    v =  getattr(obj, field)
                except:
                    continue
                """
                if isinstance(v, db.Model):
                    #output[obj.properties()[field].verbose_name] = str(v.key())
                    v = str(v.key())
                if self.floatformat == "true" and isinstance( v, float):
                    v =  self.floatfmt(v)
                if self.fieldname == "normal":
                    output[field] = v
                else:
                        output[obj.properties()[field].verbose_name] = v
                """
                if v :
                    if isinstance(v, db.Model):
                        #output[obj.properties()[field].verbose_name] = str(v.key())
                        v = str(v.key())
                    if self.floatformat == "true" and isinstance( v, float):
                        v =  self.floatfmt(v)
                    if self.fieldname == "normal":
                        output[field] = v
                    else:
                        output[obj.properties()[field].verbose_name] = v
                
            return output
        elif isinstance(obj, db.FloatProperty):
            pass
        elif isinstance(obj, db.Key):
            return str(obj)
        elif isinstance(obj, db.GeoPt):
            output =""
            output = str(getattr(obj, "lat")) + "," + str(getattr(obj, "lon"))
            return output
        elif isinstance(obj, datetime.datetime):
            output = ""
            output = timemanager.utc2jst_date(obj).strftime("%Y/%m/%d %H:%M:%S")
            """
            output = {}
            fields = ['day', 'hour', 'microsecond', 'minute', 'month', 'second',
                'year']
            methods = ['ctime', 'isocalendar', 'isoformat', 'isoweekday',
                'timetuple']
            for field in fields:
                output[field] = getattr(obj, field)
            for method in methods:
                output[method] = getattr(obj, method)()
            output['epoch'] = time.mktime(obj.timetuple())
            """
            return output

        elif isinstance(obj, time.struct_time):
            return list(obj)

        elif isinstance(obj, users.User):
            output = {}
            methods = ['nickname', 'email', 'auth_domain']
            for method in methods:
                output[method] = getattr(obj, method)()
            return output

        return simplejson.JSONEncoder.default(self, obj)

    @classmethod
    def moneyfmt(cls,value, places=2, curr='', sep=',', dp='.',
             pos='', neg='-', trailneg=''):
        if not value:
            return ""
        """Decimal を通貨表現の文字列に変換します。
        places:  小数点以下の値を表すのに必要な桁数
        curr:    符号の前に置く通貨記号 (オプションで、空でもかまいません)
        sep:     桁のグループ化に使う記号、オプションです (コンマ、ピリオド、
                 スペース、または空)
        dp:      小数点 (コンマまたはピリオド)
                 小数部がゼロの場合には空にできます。
        pos:     正数の符号オプション: '+', 空白または空文字列
        neg:     負数の符号オプション: '-', '(', 空白または空文字列
        trailneg:後置マイナス符号オプション:  '-', ')', 空白または空文字列
    
        >>> d = Decimal('-1234567.8901')
        >>> moneyfmt(d, curr='$')
        '-$1,234,567.89'
        >>> moneyfmt(d, places=0, sep='.', dp='', neg='', trailneg='-')
        '1.234.568-'
        >>> moneyfmt(d, curr='$', neg='(', trailneg=')')
        '($1,234,567.89)'
        >>> moneyfmt(Decimal(123456789), sep=' ')
        '123 456 789.00'
        >>> moneyfmt(Decimal('-0.02'), neg='<', trailneg='>')
        '<.02>'
    
        """
        value =  Decimal(str(value))
        q = Decimal((0, (1,), -places))    # 小数点以下2桁 --> '0.01'
        sign, digits, exp = value.quantize(q).as_tuple()
        assert exp == -places    
        result = []
        digits = map(str, digits)
        build, next = result.append, digits.pop
        if sign:
            build(trailneg)
        for i in range(places):
            if digits:
                build(next())
            else:
                build('0')
        build(dp)
        i = 0
        while digits:
            build(next())
            i += 1
            if i == 3 and digits:
                i = 0
                build(sep)
        build(curr)
        if sign:
            build(neg)
        else:
            build(pos)
        result.reverse()
        return ''.join(result)

    @classmethod
    def GQLmoneyfmt(cls,gql):
        if not gql:
            return ""
        properties = gql.properties().items()
        output = {}
        for field, value in properties:
            v =  getattr(gql, field)
            if v:
                if isinstance( v, float):
                    v =  cls.floatfmt(v)
                output[field] = v                

        return output

    @classmethod
    def floatfmt(cls,num):
        result = ""
        mark = ""
        if num:
            nums = str(num).split(".")[0]
            if nums[0] == "+" or nums[0] == "-":
                mark = nums.pop(0)
            for i,e in enumerate(reversed(nums)):
                if not i == 0 and i % 3 == 0:
                    result = e + "," + result
                else:
                    result = e + result
            if len(str(num).split(".")) == 2:
                if int(str(num).split(".")[1]):
                    result = result + "." + str(int(str(num).split(".")[1]))
        return mark + result

    @classmethod
    def floatfmt2(cls,num):
        if num:
            locale.setlocale(locale.LC_ALL, "")
            if len(str(num).split(".")) == 2:
                if int(str(num).split(".")[1]):
                    result = locale.format("%.3f", num, grouping=True)
                else:
                    result = locale.format("%.3d", num, grouping=True)                    
            else:
                result = locale.format("%.3d", num, grouping=True)
        return result

def JsonEncode(input):
    """
    Encode an input GQL object as JSON

    Args:
      input: A GQL object or DB property.

    Returns:
      A JSON string based on the input object.

    Raises:
      TypeError: Typically occurs when an input object contains an unsupported
        type.
    """
    return GqlJsonEncoder().encode(input)

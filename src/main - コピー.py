#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#

#from google.appengine.ext.webapp import template
##from google.appengine.ext import webapp
import webapp2

from application.index import Index
from application.index2 import Index2
from application.form import form
from application.jcache import cronworker
from application.jcache import getjson
from application.jcache import jsonsearvebklistdata
from application.editwhatsnew import editwhatsnew
from application.bksorttask import bksort
from application.show import Show
from application.chkauth import setsid
from application.allblobdelete import allblobdelete
#def main():


#    application = webapp.WSGIApplication([
app = webapp2.WSGIApplication([
                                          ('/', Index),
                                          ('/index.html', Index),
                                          ('/index2.html', Index2),
                                          ('/form/', form),
                                          ('/form/form.html', form),
                                          ('/mobile/form/', form),
                                          ('/mobile/form/form.html', form),
                                          ('/jsonservice', jsonsearvebklistdata),
                                          ('/tasks/getjson', getjson),
                                          ('/tasks/cronworker', cronworker),
                                          ('/tasks/bksort', bksort),
                                          ('/editwhatsnew', editwhatsnew),
                                          ('/show/.*', Show),
                                          ('/auth/setsid', setsid),
                                          ('/allblobdelete',allblobdelete)
                                           ],debug=True)
"""
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
"""
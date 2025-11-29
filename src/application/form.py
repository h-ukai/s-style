#!/usr/local/bin/python
# -*- coding: utf-8 -*-


import os
import config

#from google.appengine.ext import webapp
import webapp2
from google.appengine.ext.webapp import template
from google.appengine.api import mail

class form(webapp2.RequestHandler):

    def get(self):
        self.post()

    def post(self):
        try:
            referer = self.response.headers['Referer']
        except:
            referer = ''
 
        try:
            origin = self.response.headers['Origin']
        except:
            origin = ''
        # この方法でOriginやRefererが取れるので
        # 必要に応じてチェック処理などを入れるといいのでは。
        # ちなみにtry〜exceptを使わないと、存在しない場合Key Errorが発生しますよ

        # これはあちこちのサイトでよく言われている処理
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        # IE8は、これがないとうまく動きませんでした。
        self.response.headers['Access-Control-Allow-Headers'] = '*'
        # GET/POSTなど、必要に応じて許可するメソッドを指定します。
        # POSTの場合はOPTIONSも指定する必要があります。
        self.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        #self.response.headers['Content-Type'] = 'text/plain;charset=UTF-8'

        path = self.request.path
        pathParts = path.split(u'/') 
        dir1  = pathParts[1]

        self.tmpl_val = {}
        self.tmpl_val["ref"] = self.request.get('ref')

        self.tmpl_val['sitekey'] = '6LfRxU4aAAAAAD6BDE23lHzfDy3OX2h8qqV-bH2Q'


#        user_email = 'warao.shikyo@gmail.com;fuminori.yokoyama@gmail.com'
        user_email = 's-style.s8@nifty.com;warao.shikyo@gmail.com;fuminori.yokoyama@gmail.com'
        get_new_regist = self.request.get('new_regist')
        if get_new_regist:
            self._send_confirm(user_email)
            self.tmpl_val["submit"]=True
        if dir1 == "form":
            path = os.path.join( os.getcwd(),'templates','form.html')
        else:
            path = os.path.join( os.getcwd(),'templates','formm.html')
            
        self.response.out.write(template.render(path, self.tmpl_val))

    def _send_confirm(self, email):
        msgbody = ''
        """
        for key in self.request.arguments():
            msgbody += key + " : " + self.request.get(key) + "\n"
        """
        for n,v in self.request.POST.multi._items:
            msgbody += n + " : " + v + "\n"
        message = mail.EmailMessage()
        message.sender = '"Form sender utility" <' + config.ADMIN_EMAIL + '>'
        message.to = email
        message.subject = 's-styleサイトからの登録'
        message.body = msgbody
        message.send()

    def options(self):
        # 何らかの処理を行う
        # POSTの場合は、このoptionsも指定して下さい。
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = '*'
        self.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'

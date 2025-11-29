'''
Created on 2015/07/05

@author: hiroshi
'''

import datetime
import logging
from google.appengine.ext import blobstore
import webapp2
import time

class allblobdelete(webapp2.RequestHandler):
    def get(self):
        self.count = self.request.get("cout")
        c = 0
        if self.count:
            c = int(self.count)
        c += 1
        limit = 300
        try:
            query = blobstore.BlobInfo.all()
            #query.filter("filename =","namedata")
            countall = query.count(100000)
            logging.info('count:' + str(countall))
            blobs = query.fetch(limit)
            #index = blobs.count(limit)
            index = 0
            for blob in blobs:
                index += 1
                #logging.info(str((c-1)*limit + index) + ' filename:' + blob.filename)
                b = blobstore.BlobInfo.get(blob.key())
                b.delete()
                #logging.info(' deletedefilename:' + blob.filename)
            self.response.out.write( '<html>' )
            self.response.out.write( '<head>' )
            if index == limit:
                self.response.out.write( '<META HTTP-EQUIV="REFRESH" CONTENT="10;URL=/allblobdelete?cout=' + str(c) + '">')
            self.response.out.write( '</head>' )


            self.response.out.write( '<body>' )
            hour = datetime.datetime.now().time().hour
            minute = datetime.datetime.now().time().minute
            second = datetime.datetime.now().time().second
            self.response.headers['Content-Type'] = 'text/html'
            self.response.out.write(str(countall) + ' :' + str((c-1)*limit+index) + ' items deleted at ' + str(hour) + ':' + str(minute) + ':' + str(second))
            if index == limit:
                self.response.out.write( 'Again after 10seconds.' )
            else:
                self.response.out.write( 'OK all jobs complete.' )
            self.response.out.write( '</body>' )
            self.response.out.write( '</html>' )

        except Exception, e:
            self.response.out.write('Error is: ' + repr(e) + '\n')
            pass

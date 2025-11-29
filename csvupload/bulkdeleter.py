# -*- coding: utf-8 -*-
"""
http://d.hatena.ne.jp/sugyan/20090711/1247302622

対象とするkind名とアプリケーションのディレクトリを指定して実行するだけ。

$ ./bulkdeleter.py --kind=HogeFugaPiyo ../application/
bulkloaderで使う他のオプションを指定することもできる、はず。

$ ./bulkdeleter.py --kind=HogeFugaPiyo --num_threads=50 --batch_size=50 ../application/

"""
import getopt
import sys
sys.path.extend([
        'C:\\Program Files (x86)\\Google\\google_appengine\\',
        'C:\\Program Files (x86)\\Google\\google_appengine\\lib\\antlr3\\'
        ])
from google.appengine.ext import db
from google.appengine.tools import appcfg
from google.appengine.tools import bulkloader
from google.appengine.tools.bulkloader import (
    BulkExporterThread,
    CheckOutputFile,
    Exporter)


# CheckOutputFile 無効化
CheckOutputFile.func_code = (lambda x: x).func_code

# Exporterは不要なのでDummyのインスタンスを返すようにする
def DummyExporter(kind):
    class dummy:
        def initialize(self, filename, exporter_opts):
            pass
        def finalize(self):
            pass
        def output_entities(self, entity_generator):
            pass
    return dummy()
Exporter.RegisteredExporter.func_code = DummyExporter.func_code

# 削除処理(BulkExporterThreadのTransferItemメソッドを横取りする)
def delete(self, item):
    retval = self.request_manager.GetEntities(item)
    # 取得してきたentitiesを全削除
    db.delete(retval.keys)
    retval.entities = []
    retval.keys = []
    return retval

BulkExporterThread.TransferItem.im_func.func_code = delete.func_code


if __name__ == '__main__':
    # 引数, オプションを追加
    sys.argv.insert(1, 'download_data')
    sys.argv.insert(2, '--filename=')
    sys.argv.insert(3, '--config_file=' + sys.argv[0])
    # 引数で指定したkind名でModelクラスを定義
    opts, unused_args =  getopt.getopt(sys.argv[2:], None, bulkloader.FLAG_SPEC)
    kind = [x[1] for x in opts if x[0] == '--kind'][0]
    exec "class %s(db.Model): pass" % kind

    appcfg.main(sys.argv)
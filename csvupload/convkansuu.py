#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#

'''
Created on 2011/03/04
町丁目に含まれる漢数字をアラビア文字全角に変換します。
@author: casper

def load(loader_path, application_id, kind_name, email):
    
    appengineのremote_apiからcsvファイルを取得する
    
    command_template = "%s download_data --email=%s --config_file=%s --filename=%s --kind=%s --url=http://%s.appspot.com/remote_api"
    command = command_template % (appcfg_path,
                                  email, 
                                  os.path.abspath(loader_path),
                                  get_csv_filename(application_id, kind_name),
                                  kind_name,
                                  application_id)
    os.system(command)
    
このようにコマンドラインから使う

>>> from csvupload import convkansuu
>>> convkansuu.trance()

'''

# CSVファイルの読み込み
import csv 
import codecs, cStringIO
import application.zenhan
import re

"""
街区レベル位置参照情報 (2009年版) データ形式　漢数字丁目をアラビア数字に変換
"""
def trance(): 
   
    dir = "C:\\Users\\casper\\PythonWorkspace\\amanedb\\src\\csvupload\\"
    filename = "23_2009.csv"
    csvfile = open(dir + filename)
    writer = UnicodeWriter(file(dir + "changed_" + filename, 'w'),lineterminator="\n")
 
    for row in UnicodeReader(csvfile,csv.excel,"shift_jis"):
        row[2] = application.zenhan.h2z(henkan(row[2]))    # 行の中の3番目の要素
        writer.writerow(row)
    csvfile.close()
"""
郵便番号全国版ファイル用半角カナ全角変換
エディタでutf-8にエンコードしてからでないとなぜか文字化けする。
>>> from csvupload import convkansuu
>>> convkansuu.tranceziphanzen()
"""

def tranceziphanzen(): 
    dir = "C:\\Users\\casper\\PythonWorkspace\\amanedb\\src\\csvupload\\"
    filename = "KEN_ALL.CSV"
    csvfile = open(dir + filename)
    writer = UnicodeWriter(file(dir + "changed_" + filename, 'w'),lineterminator="\n")
    for row in UnicodeReader(csvfile,csv.excel,"utf-8"):
        row[3] = application.zenhan.h2z(row[3])
        row[4] = application.zenhan.h2z(row[4])
        row[5] = application.zenhan.h2z(row[5])
        writer.writerow(row)
    csvfile.close()

"""
郵便番号全国版ファイル用半角カナ全角変換
変換済みのchanged_KEN_ALL.CSVを使う
>>> from csvupload import convkansuu
>>> convkansuu.makeaddress1()
"""

def makeaddress1(): 
    dir = "C:\\Users\\casper\\PythonWorkspace\\amanedb\\src\\csvupload\\"
    filename = "changed_KEN_ALL.CSV"
    csvfile = open(dir + filename)
    writer = UnicodeWriter(file(dir + "Address1.csv" , 'w'),lineterminator="\n")
    newrow = []
    checker = 0
    for row in UnicodeReader(csvfile,csv.excel,"utf-8"):
        if checker != row[0]:
            checker = row[0]
            newrow = [row[0],row[6],row[7]]
            writer.writerow(newrow)
    csvfile.close()

"""
街区レベル位置参照情報 (2009年版) データ形式　漢数字丁目をアラビア数字に変換
変換済みのchanged_23_2009.csvを使う
>>> from csvupload import convkansuu
>>> convkansuu.makeaddress2()

"""
def makeaddress2(): 
    dir = "C:\\Users\\casper\\PythonWorkspace\\amanedb\\src\\csvupload\\"
    filename = "changed_23_2009.csv"
    csvfile = open(dir + filename)
    writer = UnicodeWriter(file(dir + "Address2.csv" , 'w'),lineterminator="\n")
    newrow = []
    checker = 0
    for row in UnicodeReader(csvfile,csv.excel,"utf-8"):
        if checker != row[2]:
            checker = row[2]
            newrow = [row[0],row[1],row[2]]
            writer.writerow(newrow)
    csvfile.close()


"""
郵便番号大口事業所半角カナ全角変換
エディタでutf-8にエンコードしてからでないとなぜかエラーが出る。
>>> from csvupload import convkansuu
>>> convkansuu.trancejigyosyohanzen()
"""
def trancejigyosyohanzen(): 
    dir = "C:\\Users\\casper\\PythonWorkspace\\amanedb\\src\\csvupload\\"
    filename = "JIGYOSYOutf8.CSV"
    csvfile = open(dir + filename)
    writer = UnicodeWriter(file(dir + "changed_" + filename, 'w'),lineterminator="\n")
    for row in UnicodeReader(csvfile,csv.excel,"utf-8"): #utf-8　shift_jis
        row[1] = application.zenhan.h2z(row[1])
        writer.writerow(row)
    csvfile.close()

"""
沿線データレインズ仕様置換
沿線の追加新幹線の追加によって原本の沿線データとはすでに相違がある。
今後の訂正はm_stationutf8.csvを訂正して行うこと
エディタでutf-8にエンコードしてからでないとなぜかエラーが出る。

>>> from csvupload import convkansuu
>>> convkansuu.convensen()
"""
def convensen(): 
    dir = "C:\\Users\\casper\\PythonWorkspace\\amanedb\\src\\csvupload\\"
    filename = "m_stationutf8.csv"
    csvfile = open(dir + filename)
    writer = UnicodeWriter(file(dir + "changed_" + filename, 'w'),lineterminator="\n")
    for row in UnicodeReader(csvfile,csv.excel,"utf-8"): #utf-8　shift_jis
        try:
            if ensenlist[row[8]] != "廃線" and ensenlist[row[8]] != "統合":
                row[8] = ensenlist[row[8]]
                writer.writerow(row)
        except KeyError:
            row[8] = "<no args>"
            writer.writerow(row)
    csvfile.close()

"""
沿線データ作成
沿線の追加新幹線の追加によって原本の沿線データとはすでに相違がある。
changed_m_stationutf8.csvが必要

>>> from csvupload import convkansuu
>>> convkansuu.makeline()
"""

def makeline():
    dir = "C:\\Users\\casper\\PythonWorkspace\\amanedb\\src\\csvupload\\"
    filename = "changed_m_stationutf8.csv"
    csvfile = open(dir + filename)
    writer = UnicodeWriter(file(dir + "line.csv", 'w'),lineterminator="\n")
    newrow = []
    checker = 0
    for row in UnicodeReader(csvfile,csv.excel,"utf-8"):
        if checker != row[8]:
            checker = row[8]
            newrow = [row[0],row[1],row[3],row[6],row[7],row[8],row[10]]
            writer.writerow(newrow)
    csvfile.close()


kanlist = {u'一':1, u'二':2, u'三':3, u'四':4, u'五':5,
           u'六':6, u'七':7, u'八':8, u'九':9}

def kton(s, c, mult):
    if s:
        return kanlist[c]*mult if c else mult
    else:
        return 0

def ntos(n):
    return unicode(n) if n != 0 else ''

def henkan(s):
    return re.sub(u'(([二三四五六七八九]?)十)?([一二三四五六七八九])?(丁目)',
        lambda m: ntos(
           kton(m.group(1), m.group(2), 10) +
           kton(m.group(3), m.group(3), 1)
           ) + m.group(4),
      s)

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

ensenlist = {

u"JR函館本線(函館～長万部)":u"函館線",
u"JR函館本線(長万部～小樽)":u"函館線",
u"JR函館本線(小樽～旭川)":u"函館線",
u"JR室蘭本線(長万部・室蘭～苫小牧)":u"室蘭線",
u"JR室蘭本線(苫小牧～岩見沢)":u"室蘭線",
u"JR根室本線(滝川～新得)":u"根室線",
u"JR根室本線(新得～釧路)":u"根室線",
u"JR根室本線(花咲線)(釧路～根室)":u"根室線",
u"JR千歳線":u"千歳線",
u"JR石勝線":u"石勝線",
u"JR日高本線":u"日高線",
u"JR札沼線":u"札沼線",
u"JR留萌本線":u"留萌線",
u"JR富良野線":u"富良野線",
u"JR宗谷本線":u"宗谷線",
u"JR石北本線":u"石北線",
u"JR釧網本線":u"釧網線",
u"JR海峡線":u"海峡線",
u"JR江差線":u"江差線",
u"JR東北本線(八戸～青森)":u"東北線",
u"JR奥羽本線(新庄～青森)":u"奥羽線",
u"JR大湊線(はまなすベイライン大湊線)":u"大湊線",
u"JR五能線":u"五能線",
u"JR津軽線":u"津軽線",
u"JR八戸線":u"八戸線",
u"JR岩泉線":u"岩泉線",
u"JR大船渡線(ドラゴンレール大船渡線)":u"大船渡線",
u"JR釜石線(銀河ドリームライン釜石線)":u"釜石線",
u"JR北上線":u"北上線",
u"JR田沢湖線":u"田沢湖線",
u"JR花輪線(十和田八幡平四季彩ライン)":u"花輪線",
u"JR山田線":u"山田線",
u"JR羽越本線":u"羽越線",
u"JR男鹿線":u"男鹿線",
u"JR奥羽本線(山形線)(福島～新庄)":u"奥羽線",
u"JR仙山線":u"仙山線",
u"JR左沢線(フルーツライン左沢線)":u"左沢線",
u"JR米坂線":u"米坂線",
u"JR陸羽西線(奥の細道最上川ライン)":u"陸羽西線",
u"JR陸羽東線(奥の細道湯けむりライン)":u"陸羽東線",
u"JR仙石線":u"仙石線",
u"JR石巻線":u"石巻線",
u"JR気仙沼線":u"気仙沼線",
u"JR磐越西線(郡山～会津若松)":u"磐越西線",
u"JR磐越西線(森と水とロマンの鉄道)":u"磐越西線",
u"JR只見線":u"只見線",
u"JR磐越東線(ゆうゆうあぶくまライン)":u"磐越東線",
u"JR常磐線(取手～いわき)":u"常磐線",
u"JR常磐線(いわき～仙台)":u"常磐線",
u"JR東北本線(黒磯～利府・盛岡)":u"東北線",
u"JR東海道本線(東京～熱海)":u"東海道線",
u"JR山手線":u"山手線",
u"JR南武線":u"南武線",
u"JR鶴見線":u"鶴見線",
u"JR武蔵野線":u"武蔵野線",
u"JR横浜線":u"横浜線",
u"JR根岸線":u"根岸線",
u"JR横須賀線":u"横須賀線",
u"JR相模線":u"相模線",
u"JR中央本線(東京～塩尻)":u"中央線",
u"JR中央線(快速)":u"中央線",
u"JR中央・総武線":u"総武中央線",
u"JR総武本線":u"総武線",
u"JR青梅線":u"青梅線",
u"JR五日市線":u"五日市線",
u"JR八高線(八王子～高麗川)":u"八高線",
u"JR八高線(高麗川～高崎)":u"八高線",
u"JR東北本線(宇都宮線)":u"宇都宮線",
u"JR常磐線(上野～取手)":u"常磐緩行線",
u"JR埼京線":u"埼京線",
u"JR川越線":u"川越線",
u"JR高崎線":u"高崎線",
u"JR外房線":u"外房線",
u"JR内房線":u"内房線",
u"JR京葉線":u"京葉線",
u"JR成田線":u"成田線",
u"JR成田エクスプレス":u"統合",
u"JR鹿島線":u"鹿島線",
u"JR久留里線":u"久留里線",
u"JR東金線":u"東金線",
u"JR京浜東北線":u"京浜東北線",
u"JR湘南新宿ライン":u"湘南新宿宇",
u"JR烏山線":u"烏山線",
u"JR吾妻線":u"吾妻線",
u"JR信越本線":u"信越線",
u"JR水郡線":u"水郡線",
u"JR水戸線":u"水戸線",
u"JR日光線":u"日光線",
u"JR両毛線":u"両毛線",
u"JR上越線":u"上越線",
u"JR小海線(八ヶ岳高原線)":u"小海線",
u"JR身延線":u"身延線",
u"JR信越本線(篠ノ井～直江津)":u"信越線",
u"JR信越本線(直江津～新潟)":u"信越線",
u"JR北陸本線(富山～直江津)":u"北陸線",
u"JR白新線":u"白新線",
u"JR飯山線":u"飯山線",
u"JR越後線":u"越後線",
u"JR大糸線":u"大糸線",
u"JR弥彦線":u"弥彦線",
u"JR中央本線(名古屋～塩尻)":u"中央線",
u"JR篠ノ井線":u"篠ノ井線",
u"JR飯田線(豊橋～天竜峡)":u"飯田線",
u"JR飯田線(天竜峡～辰野)":u"飯田線",
u"JR北陸本線(米原～富山)":u"北陸線",
u"JR高山本線":u"高山線",
u"JR城端線":u"城端線",
u"JR氷見線":u"氷見線",
u"JR七尾線":u"七尾線",
u"JR北陸本線(敦賀～敦賀港)":u"北陸線",
u"JR越美北線(九頭竜線)":u"越美北線",
u"JR小浜線":u"小浜線",
u"JR東海道本線(熱海～浜松)":u"東海道線",
u"JR東海道本線(浜松～岐阜)":u"東海道線",
u"JR東海道本線(岐阜～美濃赤坂・米原)":u"東海道線",
u"JR伊東線":u"伊東線",
u"JR御殿場線":u"御殿場線",
u"JR武豊線":u"武豊線",
u"JR太多線":u"太多線",
u"JR関西本線(名古屋～亀山)":u"関西線",
u"JR関西本線(亀山～加茂)":u"関西線",
u"JR紀勢本線":u"紀勢線",
u"JR草津線":u"草津線",
u"JR参宮線":u"参宮線",
u"JR名松線":u"名松線",
u"JR東海道本線(琵琶湖線)(米原～京都)":u"東海道線",
u"JR東海道本線(京都線)(京都～大阪)":u"東海道線",
u"JR東海道本線(神戸線)(大阪～神戸)":u"東海道線",
u"JR湖西線":u"湖西線",
u"JR関西本線(大和路線)(加茂～ＪＲ難波)":u"関西線",
u"JR山陽本線(神戸線)(神戸～姫路)":u"山陽線",
u"JR山陽本線(姫路～岡山)":u"山陽線",
u"JR山陽本線(岡山～三原)":u"山陽線",
u"JR山陽本線(三原～岩国)":u"山陽線",
u"JR山陽本線(岩国～門司)":u"山陽線",
u"JR山陽本線(兵庫～和田岬)":u"山陽線",
u"JR山陰本線(嵯峨野線)(京都～園部)":u"山陰線",
u"JR山陰本線(園部～豊岡)":u"山陰線",
u"JR山陰本線(豊岡～米子)":u"山陰線",
u"JR片町線(学研都市線)":u"片町線",
u"JR奈良線":u"奈良線",
u"JR舞鶴線":u"舞鶴線",
u"JR大阪環状線":u"環状線",
u"JR桜島線(ゆめ咲線)":u"桜島線",
u"JR東西線":u"ＪＲ東西線",
u"JR阪和線(天王寺～和歌山)":u"阪和線",
u"JR阪和線(鳳～東羽衣)":u"阪和線",
u"JR関西空港線":u"関西空港線",
u"JR福知山線(宝塚線)(新大阪～篠山口)":u"福知山線",
u"JR福知山線(篠山口～福知山)":u"福知山線",
u"JR赤穂線":u"赤穂線",
u"JR加古川線":u"加古川線",
u"JR姫新線(姫路～佐用)":u"姫新線",
u"JR姫新線(佐用～新見)":u"姫新線",
u"JR播但線":u"播但線",
u"JR和歌山線":u"和歌山線",
u"JR桜井線":u"桜井線",
u"JR紀勢本線(きのくに線)(新宮～和歌山)":u"紀勢線",
u"JR紀勢本線(和歌山～和歌山市)":u"紀勢線",
u"JRおおさか東線":u"おおさか東",
u"JR山陰本線(米子～益田)":u"山陰線",
u"JR山陰本線(益田～下関)":u"山陰線",
u"JR伯備線":u"伯備線",
u"JR因美線":u"因美線",
u"JR境線":u"境線",
u"JR木次線":u"木次線",
u"JR三江線":u"三江線",
u"JR山口線":u"山口線",
u"JR宇野線":u"宇野線",
u"JR本四備讃線(瀬戸大橋線)":u"備讃線",
u"JR吉備線":u"吉備線",
u"JR芸備線":u"芸備線",
u"JR津山線":u"津山線",
u"JR呉線":u"呉線",
u"JR可部線":u"可部線",
u"JR福塩線":u"福塩線",
u"JR宇部線":u"宇部線",
u"JR美祢線":u"美祢線",
u"JR小野田線":u"小野田線",
u"JR岩徳線":u"岩徳線",
u"JR土讃線":u"土讃線",
u"JR高徳線":u"高徳線",
u"JR徳島線(よしの川ブルーライン)":u"徳島線",
u"JR牟岐線":u"牟岐線",
u"JR鳴門線":u"鳴門線",
u"JR予讃線":u"予讃線",
u"JR予讃・内子線":u"内子線",
u"JR予土線(しまんとグリーンライン)":u"予土線",
u"JR博多南線":u"博多南線",
u"JR鹿児島本線(下関・門司港～博多)":u"鹿児島線",
u"JR鹿児島本線(博多～八代)":u"鹿児島線",
u"JR鹿児島本線(川内～鹿児島)":u"鹿児島線",
u"JR長崎本線(鳥栖～長崎)":u"長崎線",
u"JR日豊本線(門司港～佐伯)":u"日豊線",
u"JR日豊本線(佐伯～鹿児島中央)":u"日豊線",
u"JR篠栗線(福北ゆたか線)":u"篠栗線",
u"JR筑肥線(姪浜～西唐津)":u"筑肥線",
u"JR筑豊本線(若松線)(若松～折尾)":u"筑豊線",
u"JR筑豊本線(福北ゆたか線)(折尾～桂川)":u"筑豊線",
u"JR筑豊本線(原田線)(桂川～原田)":u"筑豊線",
u"JR久大本線(ゆふ高原線)":u"久大線",
u"JR日田彦山線":u"日田彦山線",
u"JR後藤寺線":u"後藤寺線",
u"JR香椎線(海の中道線)(西戸崎～香椎)":u"香椎線",
u"JR香椎線(香椎～宇美)":u"香椎線",
u"JR佐世保線":u"佐世保線",
u"JR筑肥線(西唐津～伊万里)":u"筑肥線",
u"JR唐津線":u"唐津線",
u"JR大村線":u"大村線",
u"JR豊肥本線(阿蘇高原線)":u"豊肥線",
u"JR三角線":u"三角線",
u"JR肥薩線(えびの高原線)(八代～吉松)":u"肥薩線",
u"JR肥薩線(吉松～隼人)":u"肥薩線",
u"JR宮崎空港線":u"宮崎空港線",
u"JR日南線":u"日南線",
u"JR吉都線(えびの高原線)":u"吉都線",
u"JR指宿枕崎線":u"指宿枕崎線",
u"東武東上線":u"東武東上線",
u"東武伊勢崎線":u"伊勢崎線",
u"東武日光線":u"東武日光線",
u"東武野田線":u"東武野田線",
u"東武亀戸線":u"東武亀戸線",
u"東武大師線":u"統合",
u"東武越生線":u"東武越生線",
u"東武宇都宮線":u"東武宇都宮線",
u"東武鬼怒川線":u"鬼怒川線",
u"東武佐野線":u"東武佐野線",
u"東武桐生線":u"東武桐生線",
u"東武小泉線":u"東武小泉線",
u"西武池袋線":u"西武池袋線",
u"西武秩父線":u"池袋秩父線",
u"西武有楽町線":u"西武有楽町",
u"西武豊島線":u"廃線",
u"西武狭山線":u"西武狭山線",
u"西武山口線":u"西武山口線",
u"西武新宿線":u"西武新宿線",
u"西武拝島線":u"西武拝島線",
u"西武西武園線":u"廃線",
u"西武国分寺線":u"国分寺線",
u"西武多摩湖線":u"多摩湖線",
u"西武多摩川線":u"西武多摩川",
u"京成本線":u"京成本線",
u"京成押上線":u"京成押上線",
u"京成金町線":u"京成金町線",
u"京成千葉線":u"京成千葉線",
u"京成千原線":u"京成千原線",
u"京成成田空港線(成田スカイアクセス)":u"成田空港線",
u"京王京王線":u"京王線",
u"京王相模原線":u"相模原線",
u"京王高尾線":u"京王高尾線",
u"京王競馬場線":u"廃線",
u"京王動物園線":u"廃線",
u"京王井の頭線":u"井の頭線",
u"小田急小田原線":u"小田急線",
u"小田急江ノ島線":u"江ノ島線",
u"小田急多摩線":u"多摩線",
u"東急東横線":u"東横線",
u"東急目黒線":u"目黒線",
u"東急田園都市線":u"田園都市線",
u"東急大井町線":u"大井町線",
u"東急池上線":u"池上線",
u"東急多摩川線":u"東急多摩川",
u"東急世田谷線":u"世田谷線",
u"東急こどもの国線":u"廃線",
u"京急本線":u"京浜急行線",
u"京急空港線":u"京急空港線",
u"京急大師線":u"京急大師線",
u"京急逗子線":u"京急逗子線",
u"京急久里浜線":u"久里浜線",
u"東京メトロ銀座線":u"銀座線",
u"東京メトロ丸ノ内線":u"丸ノ内線",
u"東京メトロ丸ノ内方南":u"丸ノ内方南",
u"東京メトロ日比谷線":u"日比谷線",
u"東京メトロ東西線":u"東西線",
u"東京メトロ千代田線":u"千代田線",
u"東京メトロ有楽町線":u"有楽町線",
u"東京メトロ有楽町新線":u"有楽町線",
u"東京メトロ半蔵門線":u"半蔵門線",
u"東京メトロ南北線":u"南北線",
u"東京メトロ副都心線":u"副都心線",
u"相鉄本線":u"相鉄線",
u"相鉄いずみ野線":u"いずみ野線",
u"名鉄名古屋本線":u"名鉄本線",
u"名鉄豊川線":u"豊川線",
u"名鉄西尾線":u"西尾線",
u"名鉄蒲郡線":u"蒲郡線",
u"名鉄三河線":u"三河線",
u"名鉄豊田線":u"豊田線",
u"名鉄空港線":u"名鉄空港線",
u"名鉄常滑線":u"常滑線",
u"名鉄河和線":u"河和線",
u"名鉄知多新線":u"知多新線",
u"名鉄築港線":u"築港線",
u"名鉄瀬戸線":u"瀬戸線",
u"名鉄津島線":u"津島線",
u"名鉄尾西線":u"尾西線",
u"名鉄犬山線":u"犬山線",
u"名鉄各務原線":u"各務原線",
u"名鉄広見線":u"広見線",
u"名鉄小牧線":u"小牧線",
u"名鉄犬山モノレール線":u"廃線",
u"名鉄竹鼻線":u"竹鼻線",
u"名鉄羽島線":u"統合",
u"近鉄難波線":u"阪神なんば線",
u"近鉄橿原線":u"橿原線",
u"近鉄南大阪線":u"南大阪線",
u"近鉄養老線":u"養老鉄道",
u"近鉄大阪線":u"近鉄大阪線",
u"近鉄伊賀線":u"伊賀鉄道",
u"近鉄吉野線":u"吉野線",
u"近鉄湯の山線":u"湯の山線",
u"近鉄山田線":u"伊勢志摩線",
u"近鉄鳥羽線":u"統合",
u"近鉄天理線":u"天理線",
u"近鉄道明寺線":u"道明寺線",
u"近鉄内部線":u"内部線",
u"近鉄八王子線":u"統合",
u"近鉄志摩線":u"伊勢志摩線",
u"近鉄生駒線":u"生駒線",
u"近鉄田原本線":u"田原本線",
u"近鉄御所線":u"御所線",
u"近鉄鈴鹿線":u"鈴鹿線",
u"近鉄奈良線":u"近鉄奈良線",
u"近鉄信貴線":u"信貴線",
u"近鉄長野線":u"長野線",
u"近鉄けいはんな線":u"けいはんな",
u"近鉄西信貴ケーブル":u"西信貴鋼索",
u"近鉄京都線":u"近鉄京都線",
u"近鉄生駒ケーブル":u"生駒鋼索線",
u"近鉄名古屋線":u"名古屋線",
u"南海本線":u"南海本線",
u"南海空港線":u"南海空港線",
u"南海和歌山港線":u"和歌山港線",
u"南海高師浜線":u"高師浜線",
u"南海加太線":u"加太線",
u"南海多奈川線":u"多奈川線",
u"南海高野線(りんかんサンライン)":u"高野線",
u"南海高野山ケーブル":u"高野山鋼索",
u"南海汐見橋線":u"汐見橋線",
u"京阪本線":u"京阪本線",
u"京阪宇治線":u"京阪宇治線",
u"京阪交野線":u"京阪交野線",
u"京阪鴨東線":u"京阪鴨東線",
u"京阪男山ケーブル":u"京阪鋼索線",
u"京阪石山坂本線":u"京阪石坂線",
u"京阪京津線":u"京阪京津線",
u"京阪中之島線":u"中之島線",
u"阪急神戸本線":u"阪急神戸線",
u"阪急宝塚本線":u"阪急宝塚線",
u"阪急京都本線":u"阪急京都線",
u"阪急今津線":u"阪急今津線",
u"阪急甲陽線":u"阪急甲陽線",
u"阪急伊丹線":u"阪急伊丹線",
u"阪急箕面線":u"阪急箕面線",
u"阪急千里線":u"阪急千里線",
u"阪急嵐山線":u"阪急嵐山線",
u"阪神本線":u"阪神本線",
u"阪神なんば線":u"なんば線",
u"阪神武庫川線":u"武庫川線",
u"西鉄天神大牟田線":u"西鉄大牟田",
u"西鉄太宰府線":u"西鉄太宰府",
u"西鉄甘木線":u"西鉄甘木線",
u"西鉄貝塚線":u"西鉄貝塚線",
u"札幌市営地下鉄東西線":u"地下東西線",
u"札幌市営地下鉄南北線":u"地下南北線",
u"札幌市営地下鉄東豊線":u"地下東豊線",
u"札幌市電山鼻線":u"札幌市電",
u"函館市電２系統":u"函館市電支",
u"函館市電５系統":u"函館市電本",
u"北海道ちほく高原鉄道":u"廃線",
u"津軽鉄道":u"津鉄",
u"弘南鉄道弘南線":u"弘南線  ",
u"弘南鉄道大鰐線":u"大鰐線",
u"十和田観光電鉄":u"十和田観光",
u"いわて銀河鉄道":u"ＩＧＲ線",
u"青い森鉄道":u"青い森鉄道  ",
u"三陸鉄道北リアス線":u"北リアス線",
u"三陸鉄道南リアス線":u"南リアス線",
u"秋田内陸縦貫鉄道":u"秋田縦貫線",
u"由利高原鉄道":u"由利高原線",
u"山形鉄道フラワー長井線":u"フラワ長井",
u"くりはら田園鉄道":u"廃線",
u"阿武隈急行":u"阿武隈急行",
u"仙台市営地下鉄南北線":u"仙台南北線",
u"福島交通飯坂線":u"福島交通",
u"会津鉄道":u"会津鉄道",
u"仙台空港線":u"仙台空港線",
u"都営大江戸線":u"大江戸線",
u"都営浅草線":u"都営浅草線",
u"都営三田線":u"都営三田線",
u"都営新宿線":u"都営新宿線",
u"都営都電荒川線":u"都電荒川線",
u"秩父鉄道":u"秩父鉄道",
u"埼玉高速鉄道":u"埼玉高速線",
u"いすみ鉄道":u"いすみ鉄道",
u"つくばエクスプレス":u"つくばＥＸ",
u"みなとみらい線":u"みなとＭ線",
u"ゆりかもめ":u"ゆりかもめ",
u"わたらせ渓谷鐵道":u"わたらせ線",
u"ユーカリが丘線":u"ユーカリ線",
u"伊豆箱根鉄道大雄山線":u"大雄山線",
u"ひたちなか海浜鉄道湊線":u"ひたち海浜",
u"横浜市営地下鉄ブルーライン":u"横浜ブルー",
u"横浜新都市交通　シーサイドライン":u"シーサイド",
u"関東鉄道常総線":u"関鉄常総線",
u"関東鉄道竜ヶ崎線":u"竜ヶ崎線",
u"江ノ島電鉄線":u"江ノ電",
u"埼玉新都市交通伊奈線":u"伊奈線",
u"鹿島鉄道":u"廃線",
u"鹿島臨海鉄道大洗鹿島線":u"大洗鹿島線",
u"芝山鉄道":u"芝山鉄道",
u"小湊鉄道":u"小湊鐵道",
u"湘南モノレール":u"湘南モノレ",
u"上信電鉄":u"上信電鉄",
u"上毛電気鉄道":u"上毛電鉄",
u"新京成電鉄線":u"新京成線",
u"真岡鐵道":u"真岡鉄道",
u"千葉都市モノレール１号線":u"千葉モノレ",
u"千葉都市モノレール２号線":u"千葉モノレ",
u"流鉄流山線":u"流山線",
u"多摩モノレール":u"多摩モノレ",
u"銚子電鉄線":u"銚子電鉄",
u"東京モノレール":u"東京モノレ",
u"東京臨海高速鉄道":u"りんかい線",
u"東葉高速鉄道":u"東葉高速線",
u"箱根登山鉄道":u"箱根登山線",
u"北総鉄道":u"北総線",
u"野岩鉄道会津鬼怒川線":u"野岩鉄道",
u"日暮里・舎人ライナー":u"日暮里舎人",
u"横浜市営地下鉄グリーンライン":u"横浜グリー",
u"富士急行":u"富士急",
u"北越急行ほくほく線":u"ほくほく線",
u"しなの鉄道":u"しなの鉄道",
u"上田電鉄別所線":u"上田電鉄",
u"長野電鉄長野線":u"長電長野線",
u"長野電鉄屋代線":u"長電屋代線",
u"松本電鉄上高地線":u"松本電鉄",
u"富山地鉄本線":u"地鉄本線",
u"富山地鉄立山線":u"地鉄立山線",
u"富山地鉄不二越・上滝線":u"不二越線",
u"神岡鉄道":u"廃線",
u"黒部峡谷鉄道":u"黒部峡谷",
u"富山地鉄市内線":u"富山市内線",
u"万葉線":u"万葉線",
u"富山ライトレール":u"富山ライト",
u"北陸鉄道石川線":u"北鉄石川線",
u"北陸鉄道浅野川線":u"浅野川線",
u"のと鉄道七尾線":u"のと七尾線",
u"えちぜん鉄道勝山永平寺線":u"勝山線",
u"えちぜん鉄道三国芦原線":u"三国芦原線",
u"福井鉄道福武線":u"福鉄線",
u"富山地鉄富山都心線":u"富山都心線",
u"伊豆急行":u"伊豆急",
u"伊豆箱根鉄道駿豆線":u"駿豆線",
u"岳南鉄道":u"岳南鉄道",
u"静岡鉄道静岡清水線":u"静鉄",
u"天竜浜名湖鉄道":u"浜名湖鉄道",
u"遠州鉄道":u"遠鉄",
u"大井川鐵道大井川本線":u"大井川鐵道",
u"大井川鐵道井川線":u"井川線",
u"西名古屋港線(あおなみ線)":u"あおなみ線",
u"東海交通事業城北線":u"城北線",
u"愛知環状鉄道":u"愛知環状線",
u"東部丘陵線(リニモ)":u"リニモ",
u"名古屋市営地下鉄東山線":u"東山線",
u"名古屋市営地下鉄名城線":u"名城線",
u"名古屋市営地下鉄名港線":u"名港線",
u"名古屋市営地下鉄鶴舞線":u"鶴舞線",
u"名古屋市営地下鉄桜通線":u"桜通線",
u"名古屋市営地下鉄上飯田線":u"上飯田線",
u"桃花台新交通":u"廃線",
u"豊橋鉄道渥美線":u"豊橋鉄道線",
u"豊橋鉄道東田本線":u"豊橋市内線",
u"豊橋鉄道運動公園前線":u"豊橋市内線",
u"ゆとりーとライン":u"ＧＢ志段味",
u"明知鉄道":u"明知鉄道",
u"長良川鉄道越美南線":u"長良川鉄道",
u"樽見鉄道":u"樽見線",
u"三岐鉄道三岐線":u"三岐線",
u"三岐鉄道北勢線":u"三岐北勢線",
u"伊勢鉄道":u"伊勢鉄道",
u"伊賀鉄道伊賀線":u"伊賀鉄道",
u"養老鉄道養老線":u"養老鉄道",
u"近江鉄道本線":u"近江鉄道線",
u"近江鉄道多賀線":u"多賀線",
u"近江鉄道八日市線":u"八日市線",
u"信楽高原鐵道":u"信楽鉄道",
u"嵯峨野観光鉄道":u"嵯峨野観光",
u"叡山電鉄叡山本線":u"叡電",
u"叡山電鉄鞍馬線":u"叡電",
u"北近畿タンゴ鉄道宮福線":u"宮福線",
u"北近畿タンゴ鉄道宮津線":u"宮津線",
u"京都市営地下鉄烏丸線":u"烏丸線",
u"京都市営地下鉄東西線":u"京都東西線",
u"京福電鉄嵐山本線":u"嵐電本線",
u"京福電鉄北野線":u"嵐電北野線",
u"北大阪急行電鉄":u"北急線",
u"能勢電鉄妙見線":u"能勢電",
u"泉北高速鉄道線":u"泉北高速線",
u"水間鉄道":u"水間鉄道",
u"大阪市営地下鉄御堂筋線":u"御堂筋線",
u"大阪市営地下鉄谷町線":u"谷町線",
u"大阪市営地下鉄四つ橋線":u"四つ橋線",
u"大阪市営地下鉄中央線":u"大阪市中央線",
u"大阪市営地下鉄千日前線":u"千日前線",
u"大阪市営地下鉄堺筋線":u"堺筋線",
u"大阪市営地下鉄長堀鶴見緑地線":u"長堀鶴見線",
u"大阪市営地下鉄南港ポートタウン線":u"ニュトラム",
u"大阪モノレール線":u"大阪モノレ",
u"大阪モノレール彩都線":u"彩都線",
u"阪堺電軌上町線":u"上町線",
u"阪堺電軌阪堺線":u"阪堺線",
u"神戸高速東西線":u"神戸東西線",
u"神戸高速南北線":u"神戸南北線",
u"神鉄有馬線":u"神鉄有馬線",
u"神鉄三田線":u"神鉄三田線",
u"神鉄公園都市線":u"公園都市線",
u"神鉄粟生線":u"神鉄粟生線",
u"北神急行電鉄":u"北神急行",
u"山陽電鉄本線":u"山電本線",
u"山陽電鉄網干線":u"山電網干線",
u"能勢電鉄日生線":u"能勢電",
u"三木鉄道":u"廃線",
u"北条鉄道":u"北条線",
u"智頭急行":u"智頭急行",
u"神戸市営地下鉄西神線":u"西神山手線",
u"神戸市営地下鉄山手線":u"西神山手線",
u"神戸市営地下鉄海岸線(夢かもめ)":u"海岸線",
u"神戸新交通ポートアイランド線":u"ポトライナ",
u"神戸新交通六甲アイランド線":u"アイランド",
u"紀州鉄道":u"紀州鉄道",
u"わかやま電鉄貴志川線":u"貴志川線",
u"大阪市営地下鉄今里筋線":u"今里筋線",
u"若桜鉄道":u"若桜鉄道",
u"一畑電車北松江線":u"一畑松江線",
u"一畑電車大社線":u"一畑大社線",
u"水島臨海鉄道":u"水島臨海線",
u"井原鉄道":u"井原鉄道",
u"岡山電軌東山本線":u"岡電東山線",
u"岡山電軌清輝橋線":u"岡電清輝橋",
u"スカイレールサービス":u"みどり坂線",
u"アストラムライン":u"アストラム",
u"広電１系統":u"広電本線 ",
u"広電１系統(宇品線)":u"広電宇品線",
u"広電２系統(宮島線)":u"広電宮島線",
u"広電３系統(己斐線)":u"統合",
u"広電５系統(皆実線)":u"広電皆実線",
u"広電５系統(比治山線)":u"統合",
u"広電６系統(江波線)":u"統合",
u"広電６系統江波線":u"広電江波線",
u"広電７系統(都心線)":u"統合",
u"広電８系統(横川線)":u"広電横川線",
u"広電９系統(白島線)":u"広電白島線",
u"錦川鉄道錦川清流線":u"錦川鉄道",
u"阿佐海岸鉄道阿佐東線":u"阿佐東線",
u"琴電琴平線":u"琴電琴平線",
u"琴電長尾線":u"琴電長尾線",
u"琴電志度線":u"琴電志度線",
u"伊予鉄道郡中線":u"伊予郡中線",
u"伊予鉄道高浜線":u"伊予高浜線",
u"伊予鉄道横河原線":u"伊予横河原",
u"伊予鉄道１系統(環状線)":u"伊予環状線",
u"伊予鉄道２系統(環状線)":u"統合",
u"伊予鉄道３系統(市駅線)":u"伊予城南線",
u"伊予鉄道５系統(松山駅前線)":u"統合",
u"伊予鉄道６系統(本町線)":u"伊予本町線",
u"土佐くろしお鉄道中村線":u"統合",
u"土佐くろしお鉄道宿毛線":u"中村宿毛線",
u"土佐くろしお鉄道ごめん・なはり線":u"後免なはり",
u"土佐電鉄ごめん線":u"土電後免線",
u"土佐電鉄伊野線":u"土電伊野線",
u"土佐電鉄桟橋線":u"土電桟橋線",
u"甘木鉄道":u"甘木鉄道",
u"平成筑豊鉄道伊田線":u"筑豊鉄道",
u"平成筑豊鉄道糸田線":u"筑豊鉄道",
u"平成筑豊鉄道田川線":u"筑豊鉄道",
u"福岡市営地下鉄空港線":u"福岡空港線",
u"福岡市営地下鉄箱崎線":u"福岡箱崎線",
u"福岡市営地下鉄七隈線":u"福岡七隈線",
u"北九州高速鉄道":u"小倉モノレ",
u"筑豊電気鉄道":u"筑豊電鉄線",
u"松浦鉄道西九州線(有田～伊万里)":u"松浦鉄道",
u"松浦鉄道西九州線(伊万里～佐世保)":u"松浦鉄道",
u"島原鉄道":u"島原鉄道",
u"長崎電軌１系統":u"長電本線",
u"長崎電軌３系統":u"長電桜町線",
u"長崎電軌４系統":u"長電蛍茶屋",
u"長崎電軌５系統":u"長電大浦線",
u"熊本電鉄本線":u"熊電",
u"熊本電鉄上熊本線":u"上熊本線",
u"南阿蘇鉄道高森線":u"高森線",
u"くま川鉄道湯前線":u"くま川鉄道",
u"肥薩おれんじ鉄道":u"おれんじ線",
u"熊本市電２系統":u"健軍線",
u"熊本市電３系統":u"統合",
u"鹿児島市電１系統":u"鹿市電谷山 ",
u"鹿児島市電２系統":u"鹿市電唐湊",
u"ゆいレール":u"ゆいレール",
u"平成筑豊鉄道門司港レトロ観光線":u"門司レトロ",
u"東北新幹線":u"東北新幹線",
u"秋田新幹線":u"秋田新幹線",
u"東海道新幹線":u"東海道新幹線",
u"長野新幹線":u"長野新幹線",
u"上越新幹線":u"上越新幹線",
u"山陽新幹線":u"山陽新幹線",
u"九州新幹線":u"九州新幹線"

}


"""
cnvk 0.9.3 - 全角・半角・ひらがな・カタカナ等を変換する簡単なモジュールです

Author:
    yuka2py

Lisence:
    Artistic License 2.0

Usage:
    import cnvk
    text = cnvk.convert(text, cnvk.H_ALPHA, cnvk.H_NUM) #英数字を半角に変換
    text = cnvk.convert(text, cnvk.H_ALPHA, cnvk.H_NUM, {u"-":u"－"}) #追加の変換を dict で指示
    text = cnvk.convert(text, cnvk.HIRA2KATA, cnvk.H_KATA) #ひらがなも含め、半角カタカナに変換
    text = cnvk.convert(text, cnvk.Z_KATA, cnvk.KATA2HIRA) #カタカナも含め、全角ひらがなに変換
    text = cnvk.convert(text, cnvk.HAC, skip=u"＄＆") #u"＄" と u"＆" 以外の ASCII 文字を半角に変換
"""
    
def convert(text, *maps, **ops):
    """ 変換マップを指定して、文字列を変換します。
    追加の変換マップを dict や tuple で簡単に利用できます。
    処理をスキップする文字を指定することが出来ます。
    
    args:
        text: 変換元のテキスト。unicode を必要とします。
        maps: 変換マップの指定。tuple, dict または tuple を返す関数（callable オブジェクト）で指定。
                    マップは指定された順序に実行されます。
        skip: 変換しない除外文字の指定。tuple または文字列で指定
                    tuple で指定すると各要素を除外。文字列で指定すると含まれる全ての文字を除外。
    return:
        converted unicode string
    
    built-in maps:
        H_SPACE (HS): スペースを半角に統一
        H_NUM (HN): 数字を半角に統一
        H_ALPHA (HA): 英字を半角に統一
        H_KIGO (HKG): ASCII記号を半角に統一
        H_KATA (HK): カタカナを半角カタカナに統一
        H_ASCII (HAC): アスキー文字を半角に統一（スペースを除く）（＝H_NUM + H_ALPHA + H_KIGO）
        Z_SPACE (ZS): スペースを全角に統一
        Z_NUM (ZN): 数字を全角に統一
        Z_ALPHA (ZA): 英字を全角に統一
        Z_KIGO (ZKG): ASCII記号を全角に統一
        Z_KATA (ZK): カタカナを全角に統一
        Z_ASCII (ZAC): アスキー文字を全角に統一（スペースを除く）（＝Z_NUM + Z_ALPHA + Z_KIGO）
        HIRA2KATA (H2K): ひらがなをカタカナに変換
        KATA2HIRA (K2H): カタカナをひらがなに変換
    """
    if "skip" in ops:
        skip = ops["skip"]
        if isinstance(skip, basestring):
            skip = tuple(skip)
        def replace(text, fr, to):
            return text if fr in skip else text.replace(fr, to)
    else:
        def replace(text, fr, to):
            return text.replace(fr, to)

    for map in maps:
        if callable(map):
            map = map()
        elif isinstance(map, dict):
            map = map.items()
        for fr, to in map:
            text = replace(text, fr, to)

    return text

H_SPACE = HS = ((u"　",u" "),)
H_NUM = HN = (
    (u"０",u"0"),(u"１",u"1"),(u"２",u"2"),(u"３",u"3"),(u"４",u"4"),
    (u"５",u"5"),(u"６",u"6"),(u"７",u"7"),(u"８",u"8"),(u"９",u"9"),
    )
H_ALPHA = HA = (
    (u"ａ",u"a"),(u"ｂ",u"b"),(u"ｃ",u"c"),(u"ｄ",u"d"),(u"ｅ",u"e"),
    (u"ｆ",u"f"),(u"ｇ",u"g"),(u"ｈ",u"h"),(u"ｉ",u"i"),(u"ｊ",u"j"),
    (u"ｋ",u"k"),(u"ｌ",u"l"),(u"ｍ",u"m"),(u"ｎ",u"n"),(u"ｏ",u"o"),
    (u"ｐ",u"p"),(u"ｑ",u"q"),(u"ｒ",u"r"),(u"ｓ",u"s"),(u"ｔ",u"t"),
    (u"ｕ",u"u"),(u"ｖ",u"v"),(u"ｗ",u"w"),(u"ｘ",u"x"),(u"ｙ",u"y"),(u"ｚ",u"z"),
    (u"Ａ",u"A"),(u"Ｂ",u"B"),(u"Ｃ",u"C"),(u"Ｄ",u"D"),(u"Ｅ",u"E"),
    (u"Ｆ",u"F"),(u"Ｇ",u"G"),(u"Ｈ",u"H"),(u"Ｉ",u"I"),(u"Ｊ",u"J"),
    (u"Ｋ",u"K"),(u"Ｌ",u"L"),(u"Ｍ",u"M"),(u"Ｎ",u"N"),(u"Ｏ",u"O"),
    (u"Ｐ",u"P"),(u"Ｑ",u"Q"),(u"Ｒ",u"R"),(u"Ｓ",u"S"),(u"Ｔ",u"T"),
    (u"Ｕ",u"U"),(u"Ｖ",u"V"),(u"Ｗ",u"W"),(u"Ｘ",u"X"),(u"Ｙ",u"Y"),(u"Ｚ",u"Z"),
    )
H_KIGO = HKG = (
    (u"．",u"."),(u"，",u","),(u"！",u"!"),(u"？",u"?"),(u"”",u'"'),
    (u"’",u"'"),(u"‘",u"`"),(u"＠",u"@"),(u"＿",u"_"),(u"：",u":"),
    (u"；",u";"),(u"＃",u"#"),(u"＄",u"$"),(u"％",u"%"),(u"＆",u"&"),
    (u"（",u"("),(u"）",u")"),(u"‐",u"-"),(u"＝",u"="),(u"＊",u"*"),
    (u"＋",u"+"),(u"－",u"-"),(u"／",u"/"),(u"＜",u"<"),(u"＞",u">"),
    (u"［",u"["),(u"￥",u"\\"),(u"］",u"]"),(u"＾",u"^"),(u"｛",u"{"),
    (u"｜",u"|"),(u"｝",u"}"),(u"～",u"~")
    )
H_KATA = HK = (
    (u"ァ",u"ｧ"),(u"ィ",u"ｨ"),(u"ゥ",u"ｩ"),(u"ェ",u"ｪ"),(u"ォ",u"ｫ"),
    (u"ッ",u"ｯ"),(u"ャ",u"ｬ"),(u"ュ",u"ｭ"),(u"ョ",u"ｮ"),
    (u"ガ",u"ｶﾞ"),(u"ギ",u"ｷﾞ"),(u"グ",u"ｸﾞ"),(u"ゲ",u"ｹﾞ"),(u"ゴ",u"ｺﾞ"),
    (u"ザ",u"ｻﾞ"),(u"ジ",u"ｼﾞ"),(u"ズ",u"ｽﾞ"),(u"ゼ",u"ｾﾞ"),(u"ゾ",u"ｿﾞ"),
    (u"ダ",u"ﾀﾞ"),(u"ヂ",u"ﾁﾞ"),(u"ヅ",u"ﾂﾞ"),(u"デ",u"ﾃﾞ"),(u"ド",u"ﾄﾞ"),
    (u"バ",u"ﾊﾞ"),(u"ビ",u"ﾋﾞ"),(u"ブ",u"ﾌﾞ"),(u"ベ",u"ﾍﾞ"),(u"ボ",u"ﾎﾞ"),
    (u"パ",u"ﾊﾟ"),(u"ピ",u"ﾋﾟ"),(u"プ",u"ﾌﾟ"),(u"ペ",u"ﾍﾟ"),(u"ポ",u"ﾎﾟ"),
    (u"ヴ",u"ｳﾞ"),
    (u"ア",u"ｱ"),(u"イ",u"ｲ"),(u"ウ",u"ｳ"),(u"エ",u"ｴ"),(u"オ",u"ｵ"),
    (u"カ",u"ｶ"),(u"キ",u"ｷ"),(u"ク",u"ｸ"),(u"ケ",u"ｹ"),(u"コ",u"ｺ"),
    (u"サ",u"ｻ"),(u"シ",u"ｼ"),(u"ス",u"ｽ"),(u"セ",u"ｾ"),(u"ソ",u"ｿ"),
    (u"タ",u"ﾀ"),(u"チ",u"ﾁ"),(u"ツ",u"ﾂ"),(u"テ",u"ﾃ"),(u"ト",u"ﾄ"),
    (u"ナ",u"ﾅ"),(u"ニ",u"ﾆ"),(u"ヌ",u"ﾇ"),(u"ネ",u"ﾈ"),(u"ノ",u"ﾉ"),
    (u"ハ",u"ﾊ"),(u"ヒ",u"ﾋ"),(u"フ",u"ﾌ"),(u"ヘ",u"ﾍ"),(u"ホ",u"ﾎ"),
    (u"マ",u"ﾏ"),(u"ミ",u"ﾐ"),(u"ム",u"ﾑ"),(u"メ",u"ﾒ"),(u"モ",u"ﾓ"),
    (u"ヤ",u"ﾔ"),(u"ユ",u"ﾕ"),(u"ヨ",u"ﾖ"),
    (u"ラ",u"ﾗ"),(u"リ",u"ﾘ"),(u"ル",u"ﾙ"),(u"レ",u"ﾚ"),(u"ロ",u"ﾛ"),
    (u"ワ",u"ﾜ"),(u"ヲ",u"ｦ"),(u"ン",u"ﾝ"),
    (u"。",u"｡"),(u"、",u"､"),(u"゛",u"ﾞ"),(u"゜",u"ﾟ"),
    (u"「",u"｢"),(u"」",u"｣"),(u"・",u"･"),(u"ー",u"ｰ"),
    )
HIRA2KATA = (
    (u"ぁ",u"ァ"),(u"ぃ",u"ィ"),(u"ぅ",u"ゥ"),(u"ぇ",u"ェ"),(u"ぉ",u"ォ"),
    (u"っ",u"ッ"),(u"ゃ",u"ャ"),(u"ゅ",u"ュ"),(u"ょ",u"ョ"),
    (u"が",u"ガ"),(u"ぎ",u"ギ"),(u"ぐ",u"グ"),(u"げ",u"ゲ"),(u"ご",u"ゴ"),
    (u"ざ",u"ザ"),(u"じ",u"ジ"),(u"ず",u"ズ"),(u"ぜ",u"ゼ"),(u"ぞ",u"ゾ"),
    (u"だ",u"ダ"),(u"ぢ",u"ヂ"),(u"づ",u"ヅ"),(u"で",u"デ"),(u"ど",u"ド"),
    (u"ば",u"バ"),(u"び",u"ビ"),(u"ぶ",u"ブ"),(u"べ",u"ベ"),(u"ぼ",u"ボ"),
    (u"ぱ",u"パ"),(u"ぴ",u"ピ"),(u"ぷ",u"プ"),(u"ぺ",u"ペ"),(u"ぽ",u"ポ"),
    (u"ヴ",u"ヴ"),
    (u"あ",u"ア"),(u"い",u"イ"),(u"う",u"ウ"),(u"え",u"エ"),(u"お",u"オ"),
    (u"か",u"カ"),(u"き",u"キ"),(u"く",u"ク"),(u"け",u"ケ"),(u"こ",u"コ"),
    (u"さ",u"サ"),(u"し",u"シ"),(u"す",u"ス"),(u"せ",u"セ"),(u"そ",u"ソ"),
    (u"た",u"タ"),(u"ち",u"チ"),(u"つ",u"ツ"),(u"て",u"テ"),(u"と",u"ト"),
    (u"な",u"ナ"),(u"に",u"ニ"),(u"ぬ",u"ヌ"),(u"ね",u"ネ"),(u"の",u"ノ"),
    (u"は",u"ハ"),(u"ひ",u"ヒ"),(u"ふ",u"フ"),(u"へ",u"ヘ"),(u"ほ",u"ホ"),
    (u"ま",u"マ"),(u"み",u"ミ"),(u"む",u"ム"),(u"め",u"メ"),(u"も",u"モ"),
    (u"や",u"ヤ"),(u"ゆ",u"ユ"),(u"よ",u"ヨ"),
    (u"ら",u"ラ"),(u"り",u"リ"),(u"る",u"ル"),(u"れ",u"レ"),(u"ろ",u"ロ"),
    (u"わ",u"ワ"),(u"を",u"ヲ"),(u"ん",u"ン"),
    )

Z_SPACE = ZS = ((u" ",u"　"),)
Z_NUM = ZN = lambda: ((h, z) for z, h in H_NUM)
Z_ALPHA = ZA = lambda: ((h, z) for z, h in H_ALPHA)
Z_KIGO = ZKG = lambda: ((h, z) for z, h in H_KIGO)
Z_KATA = ZK = lambda: ((h, z) for z, h in H_KATA)
KATA2HIRA = lambda: ((k, h) for h, k in HIRA2KATA)
H_ASCII = HAC = lambda: ((fr, to) for map in (H_ALPHA, H_NUM, H_KIGO) for fr, to in map)
Z_ASCII = ZAC = lambda: ((h, z) for z, h in H_ASCII())
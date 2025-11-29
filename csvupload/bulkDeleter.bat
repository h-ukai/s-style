stop

rem これは未完成
rem データを入れ替える時に使う

rem http://d.hatena.ne.jp/sugyan/20090711/1247302622

rem 対象とするkind名とアプリケーションのディレクトリを指定して実行するだけ。

rem $ ./bulkdeleter.py --kind=HogeFugaPiyo ../application/
rem bulkloaderで使う他のオプションを指定することもできる、はず。

rem $ ./bulkdeleter.py --kind=HogeFugaPiyo --num_threads=50 --batch_size=50 ../application/

rem 本体の場所 C:\Program Files (x86)\Google\google_appengine\google\appengine\tools

rem ローカルサーバー用

rem とりあえずここまで下記を編集して完成させること


cd C:\Program Files (x86)\Google\google_appengine\google\appengine\tools

C:\Users\casper\PythonWorkspace\amanedb\csvupload\bulkdeleter.py --kind=address2 C:\Users\casper\PythonWorkspace\amanedb\

rem 全国沿線駅
appcfg.py upload_data --config_file=src\bulkloader.yaml --filename=C:\Users\casper\PythonWorkspace\amanedb\csvupload\m_station.csv --num_threads=4 --kind=Station --url=http://localhost:8080/_ah/remote_api --email=warao.shikyo@gmail.com --passin src

rem 所在地１address1

rem 所在地２address2
bulkdeleter.py  --kind=address2 C:\Users\casper\PythonWorkspace\amanedb\

rem 所在地３address3 
appcfg.py upload_data --config_file=src\bulkloader.yaml --filename=C:\Users\casper\PythonWorkspace\amanedb\csvupload\changed_23_2009.csv --num_threads=4 --kind=address3 --url=http://localhost:8080/_ah/remote_api --email=warao.shikyo@gmail.com --passin src

rem 全国郵便番号
appcfg.py upload_data --config_file=src\bulkloader.yaml --db_filename=C:\Users\casper\PythonWorkspace\amanedb\bulkloader-progress-20110307.110919.sql3 --filename=C:\Users\casper\PythonWorkspace\amanedb\csvupload\changed_KEN_ALL.CSV --num_threads=10 --rps_limit=200 --batch_size=5 --kind=ziplist --url=http://localhost:8080/_ah/remote_api --email=warao.shikyo@gmail.com --passin src





rem 本番サーバー用

rem 全国沿線駅
appcfg.py upload_data --config_file=src\bulkloader.yaml --filename=C:\Users\casper\PythonWorkspace\amanedb\csvupload\m_station.csv --num_threads=4 --kind=Station src

rem 所在地１address1
appcfg.py upload_data --config_file=src\bulkloader.yaml --filename=C:\Users\casper\PythonWorkspace\amanedb\csvupload\address1.csv --num_threads=4 --kind=address1 src

rem 所在地２address2
appcfg.py upload_data --config_file=src\bulkloader.yaml --filename=C:\Users\casper\PythonWorkspace\amanedb\csvupload\address2.csv --num_threads=4 --kind=address2 src

rem 所在地３address3 
appcfg.py upload_data --config_file=src\bulkloader.yaml --filename=C:\Users\casper\PythonWorkspace\amanedb\csvupload\changed_23_2009.csv --kind=address3 --num_threads=10 --rps_limit=200 --batch_size=5 src

rem 全国郵便番号
appcfg.py upload_data --config_file=src\bulkloader.yaml --filename=C:\Users\casper\PythonWorkspace\amanedb\csvupload\changed_KEN_ALL.CSV --num_threads=10 --rps_limit=200 --batch_size=5 --kind=ziplist src



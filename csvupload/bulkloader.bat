
rem データの転送が中断された場合には、--db_filename=... 引数を付けることで中断された箇所から転送を再開できます。
rem BadRequestErrorが出た場合は URL　データストアの名前　HRの場合はs~　などをチェック
cd C:\Users\casper\PythonWorkspace\s-style

rem ローカルサーバー用

rem 所在地２address2
rem appcfg.py upload_data --config_file=csvupload\bulkloader-address2.yaml --filename=C:\Users\casper\PythonWorkspace\s-style\csvupload\address2.csv --num_threads=4 --kind=address2 --url=http://localhost:8080/_ah/remote_api --email=warao.shikyo@gmail.com --passin src
appcfg.py upload_data --filename=C:\Users\casper\PythonWorkspace\s-style\csvupload\address2.csv --config_file=csvupload\bulkloader-address2.yaml --num_threads=4 --url=http://localhost:8080/_ah/remote_api --application=dev~s-style --kind=address2 --email=warao.shikyo@gmail.com --passin src


rem 本番サーバー用

cd C:\Users\casper\PythonWorkspace\s-style

rem 所在地２address2
rem appcfg.py upload_data --config_file=csvupload\bulkloader-address2.yaml --filename=C:\Users\casper\PythonWorkspace\s-style\csvupload\address2.csv --num_threads=4 --kind=address2 src
appcfg.py upload_data --filename=C:\Users\casper\PythonWorkspace\s-style\csvupload\address2.csv --config_file=csvupload\bulkloader-address2.yaml --num_threads=4 --url=http://s-style.appspot.com/_ah/remote_api --application=s~s-style --kind=address2 --email=warao.shikyo@gmail.com --passin src

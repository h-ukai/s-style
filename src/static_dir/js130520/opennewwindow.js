/*
 * 東日本REINS 新システム
 * Copyright (C) 2009. REAL ESTATE INFORMATION NETWORK FOR EAST JAPAN.
 */

var win;

/**
 * 所在地選択子画面を表示する。
 *
 * @param snimt 遷移元	// 1:参照 2:登録 3:それ以外
 * @param stksr 途中選択可否	// 0:途中選択可 1:途中選択否
 * @param dtshri データ種類
 * @param trhktiyu 取引態様
 * @param yubnBngu1Name=yubnBngu1 郵便番号前テキストボックス名
 * @param yubnBngu2Name=yubnBngu2 郵便番号後テキストボックス名
 * @param tdufknmiName=tdufknmi 都道府県テキストボックス名
 * @param shzicmi1Name=shzicmi1 所在地１テキストボックス名
 * @param shzicmi2Name=shzicmi2 所在地２テキストボックス名
 * @param random 付与ランダムID
 *
 */
function openShzic(snimt, stksr, dtshri, trhktiyu, yubnBngu1Name, yubnBngu2Name, tdufknmiName, shzicmi1Name, shzicmi2Name, random) {
    var newWin = window.open("/reins/blank.html", "InputGuideWindow", "location=0,menubar=0,toolbar=0,resizable=1,scrollbars=1,status=1");
    var formName = "childFormShzic";


    newWin.resizeTo(650,800);
    newWin.focus();
    newWin.document.open();

    writeHeader(newWin);

    writeForm(newWin, formName, "/reins/ktgyoumu/KG006_001.do", random);

    writeInput(newWin, snimt, "snimt");
    writeInput(newWin, stksr, "stksr");
    writeInput(newWin, dtshri, "dtshri");
    writeInput(newWin, trhktiyu, "trhktiyu");
    writeInput(newWin, yubnBngu1Name, "yubnBngu1Name");
    writeInput(newWin, yubnBngu2Name, "yubnBngu2Name");
    writeInput(newWin, tdufknmiName, "tdufknmiName");
    writeInput(newWin, shzicmi1Name, "shzicmi1Name");
    writeInput(newWin, shzicmi2Name, "shzicmi2Name");

    writeFooter(newWin);

    newWin.document.close();

    return submitNewWin(newWin, formName);

}

/**
 * 沿線選択子画面を表示する。
 *
 * @param snimt 遷移元	// 1:参照 2:登録 3:それ以外
 * @param stksr 途中選択可否	// 0:途中選択可 1:途中選択否
 * @param dtshri データ種類
 * @param trhktiyu 取引態様
 * @param ensenmiName=yubnBngu1 郵便番号前テキストボックス名
 * @param fromekimiName=yubnBngu2 郵便番号後テキストボックス名
 * @param toekimiName=tdufknmi 都道府県テキストボックス名
 * @param random 付与ランダムID
 *
 */
function openEnsen(snimt, stksr, dtshri, trhktiyu, ensenmiName, fromekimiName, toekimiName, random) {
    var newWin = window.open("/reins/blank.html", "InputGuideWindow", "location=0,menubar=0,toolbar=0,resizable=1,scrollbars=1,status=1");
    var formName = "childFormEnsn";


    newWin.resizeTo(650,800);
    newWin.focus();
    newWin.document.open();

    writeHeader(newWin);

    writeForm(newWin, formName, "/reins/ktgyoumu/KG007_001.do", random);

    writeInput(newWin, snimt, "snimt");
    writeInput(newWin, stksr, "stksr");
    writeInput(newWin, dtshri, "dtshri");
    writeInput(newWin, trhktiyu, "trhktiyu");
    writeInput(newWin, ensenmiName, "ensenmiName");
    writeInput(newWin, fromekimiName, "fromekimiName");
    writeInput(newWin, toekimiName, "toekimiName");

    writeFooter(newWin);

    newWin.document.close();

    return submitNewWin(newWin, formName);

}

/**
 * ファイルアップロード小画面を表示する。
 *
 * @param logicFileField 論理ファイル名
 * @param physicalFileFierd 物理ファイル名
 * @param thmbsizehgt サムネイルサイズ 高さ
 * @param thmbsizewth サムネイルサイズ 幅
 * @param kg008callflg 呼び出しフラグ
 * @param random 付与ランダムID
 *
 */
function openFileUp(logicFileField, physicalFileFierd, thmbsizehgt, thmbsizewth, kg008callflg, random) {
    var newWin = window.open("/reins/blank.html", "FileUploadWindow", "location=0,menubar=0,toolbar=0,resizable=1,scrollbars=1,status=1");
    var formName = "childFormUpload";

    newWin.resizeTo(700,650);
    newWin.focus();
    newWin.document.open();

    writeHeader(newWin);

    writeForm(newWin, formName, "/reins/ktgyoumu/KG008_001.do", random);

    writeInput(newWin, logicFileField, "logicFileField");
    writeInput(newWin, physicalFileFierd, "physicalFileFierd");
    writeInput(newWin, thmbsizehgt, "thmbsizehgt");
    writeInput(newWin, thmbsizewth, "thmbsizewth");
    writeInput(newWin, kg008callflg, "kg008callflg");

    writeFooter(newWin);

    newWin.document.close();

    return submitNewWin(newWin, formName);

}

/**
 * GIS検索子画面を表示する。
 *
 * @param random 付与ランダムID
 *
 */
function openGis(random) {

    if ( !win || win.closed ) {
    win = window.open("/reins/blank.html", "GisWindow", "width=1000,height=675,location=0,menubar=0,toolbar=0,resizable=1,scrollbars=1,status=1");
    var formName = "childFormGis";
    
    win.focus();
    win.document.open();

    writeHeader(win);

    writeForm(win, formName, "/reins/gis/GS001_001.do", random);

    writeFooter(win);

    win.document.close();

    return submitNewWin(win, formName);
    
    } else {
    
    win.close();
    win = window.open("/reins/blank.html", "GisWindow", "width=1000,height=675,location=0,menubar=0,toolbar=0,resizable=1,scrollbars=1,status=1");
    var formName = "childFormGis";

    win.focus();
    win.document.open();

    writeHeader(win);

    writeForm(win, formName, "/reins/gis/GS001_001.do", random);

    writeFooter(win);

    win.document.close();

    return submitNewWin(win, formName);
    
    }
}

/**
 * 子画面のheader部分を記述する。
 * 記述する順番は、以下の通り。
 *  writeHeader
 *  writeForm
 *  writeInput
 *  writeFooter
 *
 * @param newWin 子画面windowオブジェクト
 */
function writeHeader(newWin) {
    newWin.document.write('<html>');
    newWin.document.write('<body>');
    
    return newWin;
}

/**
 * 子画面のform部分を記述する。
 * 記述する順番は、以下の通り。
 *  writeHeader
 *  writeForm
 *  writeInput
 *  writeFooter
 *
 * @param newWin 子画面windowオブジェクト
 * @param childFormId 子画面で作成したformId
 * @param path リクエストURI
 * @param random 付与ランダムID
 */
function writeForm(newWin, childFormId, path, random) {
    newWin.document.write('<form id="');
    newWin.document.write(childFormId);
    newWin.document.write('" name="');
    newWin.document.write(childFormId);
    newWin.document.write('" action="');
    newWin.document.write(path);
    newWin.document.write('?r=');
    newWin.document.write(random);
    newWin.document.write('" method="post">');
    
    return newWin;
}

/**
 * 子画面のInputタグ部分を記述する。
 * 記述する順番は、以下の通り。
 *  writeHeader
 *  writeForm
 *  writeInput
 *  writeFooter
 *
 * @param newWin 子画面windowオブジェクト
 * @param param 子画面のInputタグのvalueプロパティ値
 * @param paramName 子画面のInputタグのnameプロパティ値
 */
function writeInput(newWin, param, paramName) {
    newWin.document.write('<input type="hidden" name="');
    newWin.document.write(paramName);
    newWin.document.write('" value="');
    newWin.document.write(param);
    newWin.document.write('" />');
    
    return newWin;
}

/**
 * 子画面のFooter部分を記述する。
 * 記述する順番は、以下の通り。
 *  writeHeader
 *  writeForm
 *  writeInput
 *  writeFooter
 *
 * @param newWin 子画面windowオブジェクト
 */
function writeFooter(newWin) {
    newWin.document.write('</form>');
    newWin.document.write('</body>');
    newWin.document.write('</html>');
    
    return newWin;
}

/**
 * 新規で作成した子画面をsubmitする。
 * 
 * @param newWin 子画面windowオブジェクト
 * @param childFormId 子画面で作成したformId
 *
 */
function submitNewWin(newWin, childFormId) {

    var frm = newWin.document.getElementById(childFormId);
    if (frm != null) {
        frm.submit();
    }

    return newWin;
}

/**
 * 印刷プレビュー画面を開く。
 * スクロールあり、メニューバーあり
 * 
 * @param url パス
 * @param title 画面タイトル
 */
function openPrintPreview(form,title){
    var newWin = window.open(
        "/reins/blank.html",
        title,
        "location=0,menubar=0,toolbar=0,resizable=1,scrollbars=1,status=0"
        );
    form.target = title;
    form.submit();
    newWin.focus();
    
    return newWin;
}

/**
 * 画像表示サブウィンドウを開く。
 * （呼び出し元にimpath/imnameの変数が必要です）
 *
 * @param name
 * @param filepath 画像ファイルへのパス
 * @param url1 サブウィンドウJSPへのアクションパス
 * @param url2 共通画像ダウンロードのアクションパス
 * @param random
 */
function openImageView(name, filePath, url1, url2, random) {
    return openImageViewSubmit(name, filePath, url1, url2, random);
}

/**
 * 画像表示サブウィンドウを開く。
 *
 * @param name
 * @param filepath 画像ファイルへのパス
 * @param url1 サブウィンドウJSPへのアクションパス
 * @param url2 共通画像ダウンロードのアクションパス
 * @param random
 */
function openImageViewSubmit(name, filePath, url1, url2, random) {
    var newWin = window.open('/reins/blank.html', 'newWin', 'resizable=1,scrollbars=1');
    newWin.document.write('<html>');
    newWin.document.write('<body>');
    newWin.document.write('<form id="childForm" name="childForm" action="');

    newWin.document.write(url1);
    newWin.document.write('?r=');
    newWin.document.write(random);
    newWin.document.write('" method="post">');

    newWin.document.write('</form>');
    newWin.document.write('</body>');
    newWin.document.write('</html>');

    impath = url2 + "?filePath=" + filePath;
    imname = name;
    var frm = newWin.document.getElementById('childForm');
    frm.submit();
    
    return newWin;
}

/**
 * 画像表示サブウィンドウの描画。
 * （サブウィンドウから呼ばれる）
 *
 * @param newWin サブウィンドウ
 */
function newWinrewrite(newWin) {
    newWin.reWrite(imname, impath);
}

/**
 * PDFダウンロードサブウィンドウを開く。
 *
 * @param PDF取得ロジックへのアクションパス
 * @param bkknId 物件ID
 * @param random
 */
function openPdfDownLoad(url, bkknId, random, kduFlg, knskFlg) {
    return openPdfDownLoadSubmit(url, bkknId, random, kduFlg, knskFlg);
}

function openPdfDownLoadSubmit(url, bkknId, random, kduFlg, knskFlg) {
    location.href=url + "?bkknId=" + bkknId + "&kduFlg=" + kduFlg + "&knskFlg=" + knskFlg + "&r=" + random;
}

/**
 * PDFダウンロードサブウィンドウを開く。
 *
 * @param PDF取得ロジックへのアクションパス
 * @param fileName ファイル名
 * @param random
 */
function openPdfDownLoadByName(url, fileName, random, dlName) {
    return openPdfDownLoadByNameSubmit(url, fileName, random, dlName);
}

function openPdfDownLoadByNameSubmit(url, fileName, random, dlName) {
    location.href=url + "?fileName=" + fileName + "&r=" + random + "&dlFileName=" + encodeURIComponent(dlName);
}

/**
 * PDF一括ダウンロードサブウィンドウを開く。
 *
 * @param PDF取得ロジックへのアクションパス
 * @param bkknId(カンマ区切りで複数件指定可能)
 * @param random
 */
function openPluralPdfDownLoad(url, bkknId, bkknBngu, random, kduFlg, knskFlg) {

	var tmpString = bkknId.toString();
	var tmpArray = tmpString.split(",");
	if (tmpArray.length > 20) {
		alert("２０件を超える図面は一度にダウンロードできません。");
		return false;
	}else if(tmpArray.length == 0 || tmpString.length == 0) {
		alert("ダウンロードする図面が指定されていません。一覧に表示されているチェックボックスを１つ以上チェックした上で、もう一度ボタンを押してください。");
		return false;
	}

    return openPluralPdfDownLoadSubmit(url, bkknId, bkknBngu, random, kduFlg, knskFlg);
}

function openPluralPdfDownLoadSubmit(url, bkknId, bkknBngu, random, kduFlg, knskFlg) {
    location.href=url + "?bkknId=" + bkknId + "&kduFlg=" + kduFlg + "&bkknBngu=" + bkknBngu + "&knskFlg=" + knskFlg + "&r=" + random;
}

/*
 * 東日本REINS 新システム
 * Copyright (C) 2009. REAL ESTATE INFORMATION NETWORK FOR EAST JAPAN.
 */

/**
 * 画像押下による、画面表示／非表示切替機能。<br />
 * 表示／非表示切替により、表示画像も変更する。<br />
 * （表示画像1と表示画像2をそれぞれ入れ替える）<br />
 * <br />
 * ※表示画像ソースは、imgディレクトリ配下に保存されていることを前提とする。<br />
 * <br />
 * 【例】<br />
 * <input type=image" id="opener01" src="/img/btn_input_off.gif"
 *  onClick="changeDisplay('opener01','hideTable1','/img/btn_input_off.gif','/img/btn_input_on.gif')"
 * ><br />
 * <table class="innerTable hidetub" id="hideTable1"><br />
 * 
 * @auther Ryuichi Kaiura
 * @param id inputタグ img要素のID
 * @param hiddenId 非表示対象（tableタグ）のID 
 * @param imgPth1 表示画像1
 * @param imgPth2 表示画像2
 */
function changeDisplay(id, hiddenId, imgPth1, imgPth2){

    // imgタグの内容を取得
    var img = document.getElementById(id);

    // imgのPathを取得（/img/配下に必ず格納されていることを前提）
    var imgSrc = img.src.slice(img.src.indexOf("/img/",0),9999);
    
    // img.srcのパスを切替
    var imgNewSrc = imgSrc == imgPth1.slice(imgPth1.indexOf("/img/",0),9999) ? imgPth2 : imgPth1;

    // 切替画像を読み込み
    img.src = imgNewSrc;
    img.onload;
    
    // 非表示にする対象のオブジェクトを非表示にする
    var elem = document.getElementById(hiddenId);
    var elemClassName = elem.className;
    var HIDE_TUB = "hidetub";
    if (elemClassName.indexOf(HIDE_TUB) >= 0) {
        // 非表示（hidetubあり）の場合は削除
        elemClassName = elemClassName.replace(HIDE_TUB,"");
        elemClassName = elemClassName.replace(/^\s+|\s+$/g, "");
    } else {
        // 表示（hidetubなし）の場合は追加
        if (elemClassName != "") {
            elemClassName = elemClassName + " ";
        } 
        elemClassName = elemClassName + HIDE_TUB;
    }
    
    // 2008/06/11 Kaiura Ryuichi 
    elem.className = elemClassName;

}

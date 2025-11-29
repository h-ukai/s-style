
/**
 * 非表示領域項目の入力有無による、画面表示／非表示切替機能。<br />
 * 
 * changeDisplayと同一引数
 *
 * @auther kitagawa
 * @param id imgタグのID
 * @param hiddenId 非表示対象のID 
 * @param imgPth1 表示画像1
 * @param imgPth2 表示画像2
 * 2008/09/04 北川 SI2_NT_0755とSI1_BK_0115
 */

function hideTableChiledNodeValue(image_Id, table_Id ,on_img_Path, off_img_Path){

    var openflg = false ;

    var hideTableEle = document.getElementById(table_Id);
    
    if ( hideTableEle != null ) {

        // select タグ属性の入力有無判定
        var selectTags = hideTableEle.getElementsByTagName("select");
        openflg = checkSelectElementSetValue( selectTags ) ;

        if ( openflg == false ) {
            // input タグ属性の入力有無判定
            var inputTags = hideTableEle.getElementsByTagName("input");
            openflg = checkInputElementSetValue(inputTags) ;
        }
        // 2008/09/04 北川 SI2_NT_0755とSI1_BK_0115 Begin
        if ( openflg == false ) {
            // textarea タグ属性の入力有無判定
            var inputTags = hideTableEle.getElementsByTagName("textarea");
            openflg = checkTextareaElementSetValue(inputTags) ;
        }
        // 2008/09/04 北川 SI2_NT_0755とSI1_BK_0115 End
        // 入力値有と判断した場合は、hidetagを開く
        if ( openflg ) {
            changeDisplay(image_Id, table_Id , on_img_Path, off_img_Path )
        }

    }

}
        // 2008/09/04 北川 SI2_NT_0755 Begin
function checkTextareaElementSetValue(textAreaTag){

    for (var i = 0; i < textAreaTag.length; i++ ) {
        if ( textAreaTag[i].value.length > 0 ) return true ;
    }

    return false ;
}
        // 2008/09/04 北川 SI2_NT_0755 End
/**
 * 非表示領域項目の入力有無による、画面表示／非表示切替機能。<br />
 * ■selectタグ属性判定部■<br />
 * selectタグエレメントの要素をinputに <br />
 * selectedIndexが「0」以上の場合は、デフォルト値以外が選択されている<br />
 * と判断し、trueを返却<br />
 * selectedIndexが「0」の場合は、デフォルト値が選択されている<br />
 * と判断し、falseを返却<br />
 * <br />
 * 
 * @auther kitagawa
 * @param selectTags selectタグエレメント要素
 */


function checkSelectElementSetValue( selectTags ) {
    for (var i = 0; i < selectTags.length; i++ ) {
        if ( selectTags[i].selectedIndex > 0 ) return true ;
    }

    return false ;
}

/**
 * 非表示領域項目の入力有無による、画面表示／非表示切替機能。<br />
 * ■inputタグ属性判定部■<br />
 * inputタグエレメントの要素でvalue属性に値が存在する場合には<br />
 * 入力データ有と判断し、trueを返却<br />
 * inputタグエレメントの要素でvalue属性に値が存在しない場合には<br />
 * 入力データ有と判断し、falseを返却<br />
 * <br />
 * <br />
 * 
 * @auther kitagawa
 * @param inputTags inputタグエレメント要素
 */

function checkInputElementSetValue( inputTags ) {
    for (var i = 0; i < inputTags.length; i++ ) {
        switch (inputTags[i].type) {
            case 'text' :
            case 'password' :
            case 'file' :
                if ( inputTags[i].value.length > 0 ) return true ;
                break ;

            case 'checkbox' :
            case 'radio' :
                if ( inputTags[i].checked ) return true ;
                break ;

            case 'submit' :
            case 'reset' :
            case 'hidden' :
            case 'image' :
            case 'button' :
            default :
        }
    }

    return false ;
}

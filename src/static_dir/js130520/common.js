/**
 * 利用ブラウザを判定する。
 */
function getBrowserName() {
   var userAgent = navigator.userAgent;
   userAgent = userAgent.toUpperCase();
   
   if (userAgent.indexOf("SAFARI") > -1) {
        return "Safari";
   }
   if (userAgent.indexOf("FIREFOX") > -1) {
        return "Firefox";
   }
   if (userAgent.indexOf("OPERA") > -1) {
        return "Opera";
   }
   if (userAgent.indexOf("NETSCAPE") > -1) {
        return "Netscape";
   }
   if (userAgent.indexOf("MSIE 7") > -1) {
        return "IE7";
   }
   if (userAgent.indexOf("MSIE") > -1) {
        return "IE";
   }
   if (userAgent.indexOf("MOZILLA/4") > -1) {
        return "Netscape";
   }
   if (userAgent.indexOf("MOZILLA") > -1) {
        return "Mozilla";
   }
   return null;
}

/**
 * 利用OSを判定する。
 */
function getPlatform() {
    var platform = navigator.platform;
    platform = platform.toUpperCase();
    if (platform.indexOf("WIN") > -1) {
        return "Win";
    }
    if (platform.indexOf("MAC") > -1) {
        return "Mac";
    }
    return null;
}

/**
 * ログイン画面からメニュー画面に遷移する。(IE）
 */
function openMenu(url){
    window.open(url,"menu","location=0,menubar=0,toolbar=0,resizable=1,scrollbars=1,status=1");
}

/**
 * マウスの右クリックを抑止する。
 * （IE、Firefox：oncontextmenuからイベント取得）
 */
function disabledRightClick(e){

    if (e != null)  {
        // イベントの伝播を防止 
        disabledPropagation(e);
    } else {
        window.event.returnValue = false;
    }
}

/**
 * マウスのクリックを抑止する。
 * onclickからイベント取得。
 * 左クリックの抑止動作：新しいウィンドウ／タブを開く操作
 * 右クリックの抑止動作：Safariの右クリック抑止。
 * 中クリックの抑止動作：新しいウィンドウ／タブを開く操作
 */
function dispatchClick(e){
    
    var keycode;
    
    if (e != null) {
        keycode = e.which;
        platform = getPlatform(e);
        if (platform == "Mac") {
            if (keycode == '1'){
                // 左クリック
                // 新しいウィンドウを開く操作の抑止
                disabledCreateNewWindow(e);
            } else if (keycode == '3'){
                // 右クリック抑止
                disabledRightClick(e);
            }
        } else if (platform == "Win") {
            if (keycode == '1' || keycode == '2'){
                // 左クリック、または、中クリック
                // 新しいウィンドウを開く操作の抑止
                disabledCreateNewWindow(e);
            } 
        }
    } else {
        keycode = window.event.keyCode;
        if (keycode == '0') {
            // 新しいウィンドウを開く操作の抑止
            disabledCreateNewWindow(e);
        }
    }
}

/**
 * キーボード操作抑止（Safari）
 */
function disableSafariKeydown(keyCodeArray,keychar,e) {

    var keycode = keyCodeArray[0];
    var control = keyCodeArray[1];
    var shift = keyCodeArray[2];
    var option = keyCodeArray[3];
    var command = keyCodeArray[4];
    
    if (command && keycode == '49'){
            // イベントの伝播を防止 
            disabledPropagation(e);
        
    } 
    else if (keycode == '8' || (shift && keycode == '8')) { // delete、Shift + delete
        if(e.target.tagName == "INPUT" 	|| e.target.tagName == "TEXTAREA") {
            // INPUTタグ、TEXTAREAタグのうち、入力可能項目の場合はdelete押下を許可
            if ( e.target.type == "file"
             || e.target.type == "password"
             || e.target.type == "text"
             || e.target.type == "textarea") {
                if (e.target.readOnly == true) {
               	    // イベントの伝播を防止
                    disabledPropagation(e);
                } else {
	                return;
	            }
            } else {
                // イベントの伝播を防止 
                disabledPropagation(e);
            }
        } else {
            // イベントの伝播を防止 
            disabledPropagation(e); 
        }
    } else if (command && option) {
        if ( keycode == '70' || keycode == '77' // Command + Option + F、Command + Option + M
        || keycode == '69' || keycode == '66' // Command + Option + E、Command + Option + B
        || keycode == '85' // Command + Option + U
        ) {
            // イベントの伝播を防止 
            disabledPropagation(e);
        }
    } else if (command && shift) {
        if (keycode == '72' || keycode == '66' //  Command + Shift + H、Command + Shift + B
        ){
            // イベントの伝播を防止 
            disabledPropagation(e); 
        }
    } else if (command) {
        if (keycode == '84' || keycode == '76' || keycode == '81' // Command + T、Command + L、Command + Q
        || keycode == '87' || keycode == '78' || keycode == '221'  // Command + W、Command + N、 
        || keycode == '219' || keycode == '36' // Command + ]、Command + [、Command + Home
        || keycode == '37' || keycode == '39' // Command + ←、Command + →
        || keycode == '82' || keycode == '79' || keycode == '83' // Command + R、Command + O、Command + S
        || keycode == '68' || keycode == '191' // Command + D、Command + /
        ) {
            // イベントの伝播を防止 
            disabledPropagation(e);  
        }
    }
}

/**
 * キーボード操作抑止（IE）
 */
function disableIeKeydown(keyCodeArray) {
        
    var keycode = keyCodeArray[0];
    var ctrl = keyCodeArray [1];
    var shift = keyCodeArray[2];
    var alt = keyCodeArray[3];
    
    if (keycode == '114' || keycode == '115' || keycode == '116' // F3、F4、F5
    || keycode == '117' // F6
    ) { 
        window.event.keyCode = '0';
        window.event.returnValue = false;
    } else if (keycode == '8' || (shift && keycode == '8')) { // BackSpace、Shift + BackSpace
        if( event.srcElement.tagName == "INPUT" || event.srcElement.tagName == "TEXTAREA") {
            // INPUTタグ、TEXTAREAタグのうち、入力可能項目の場合はBackSpace押下を許可
            if ( event.srcElement.type == "file"
             || event.srcElement.type == "password"
             || event.srcElement.type == "text"
             || event.srcElement.type == "textarea") {
                if (event.srcElement.readOnly == true) {
			        window.event.keyCode = 0;
                	window.event.returnValue = false;
                } else {
	                return;
                }
            } else {
                window.event.returnValue = false;
            } 
        } else {
            window.event.returnValue = false;
        }
    } else if (ctrl && shift && keycode == '74'){ // Ctrl + Shift + J
        window.event.returnValue = false;
    } else if (ctrl) {        
       if (keycode == '69' || keycode == '87' || keycode == '78' // Ctrl + E、Ctrl + W、Ctrl + N
       || keycode == '116' || keycode == '82' || keycode == '76' // Ctrl + F5、Ctrl + R、Ctrl + L
       || keycode == '68' || keycode == '72' || keycode == '73' // Ctrl + D、Ctrl + H、Ctrl + I
       || keycode == '74' || keycode == '84' // Ctrl + J、Ctrl + T
       ) {
            window.event.returnValue = false;
        } else if (keycode == '79') { // Ctrl + O
            window.event.keyCode = 0;
            window.event.returnValue = false;
        }
    } else if (shift) {
        if (keycode == '121') { // Shift + F10
            window.event.returnValue = false;
        }
    } else if (alt) {
        if (keycode == '68' || keycode == '39' || keycode == '37' // Alt + D、Alt + →、Alt + ←
        ) {
            window.event.returnValue = false;
        } else if (keycode == '36') { // Alt + Home
            alert("この操作は使用できません");
            window.event.returnValue = false;
        }
    }     
}

/**
 * キーボード操作抑止（Firefox）
 */
function disableFirefoxKeydown(keyCodeArray,keychar,e) {
    
    var keycode = keyCodeArray[0];
    var ctrl = keyCodeArray[1];
    var shift = keyCodeArray[2];
    var alt = keyCodeArray[3];
    
    if (ctrl && shift && ( keycode == '82' || keycode == '84' // Ctrl + Shift + R、Ctrl + Shift + T
     || keycode == '87' || keycode == '68') // Ctrl + Shift + W、Ctrl + Shift + D
    ) {
        // イベントの伝播を防止 
        disabledPropagation(e);    
    } else if (keycode == '8' || (shift && keycode == '8')) { // BackSpace、Shift + BackSpace
        if(e.target.tagName == "INPUT" || e.target.tagName == "TEXTAREA") {
            // INPUTタグ、TEXTAREAタグのうち、入力可能項目の場合はBackSpace押下を許可
            if ( e.target.type == "file"
             || e.target.type == "password"
             || e.target.type == "text"
             || e.target.type == "textarea") {
                if (e.target.readOnly == true) {
               	    // イベントの伝播を防止
                    disabledPropagation(e);
                } else {
	                return;
	            }
            } else {
                // イベントの伝播を防止 
                disabledPropagation(e);
            } 
        } else {
            // イベントの伝播を防止 
            disabledPropagation(e); 
        }
    } else if (
        (keycode == '116' || (ctrl && keycode == '116' )) // F5、Ctrl + F5 
        || (ctrl && keycode == '115') || keycode == '117' // Ctrl + F4、F6
    ) {
        // イベントの伝播を防止 
        disabledPropagation(e);
    } else if (ctrl) {
        if (keycode == '87' || keycode == '78' || keycode == '76' // Ctrl + W、Ctrl + N、Ctrl + L
        || keycode == '66' || keycode == '72' || keycode == '73' // Ctrl + B、Ctrl + H、Ctrl + I
        || keycode == '68' || keycode == '79' || keycode == '82' // Ctrl + D、Ctrl + O、Ctrl + R
        || keycode == '74' || keycode == '75' || keycode == '84' // Ctrl + J、Ctrl + K、Ctrl + T
        || keycode == '83' || keycode == '85' || keycode == '69' // Ctrl + S、Ctrl + U、Ctrl + E
        ) {
            // イベントの伝播を防止 
            disabledPropagation(e);
        }
    } else if (shift){
        if (keycode == '13') { // Shift + Enter
            // イベントの伝播を防止 
            disabledPropagation(e);
         }
    } else if (alt) {
        if (keycode == '13') { // Alt + Enter 
            if (document.getElementsByTagName("a") ){ // Alt + Enter (aタグ上の場合）
                // イベントの伝播を防止 
                disabledPropagation(e);
            }
        } else if (
           keycode == '39' || keycode == '37' // Alt + →、Alt + ←
        || keycode == '68' || keycode == '115' // Alt + D、Alt + F4
        ) {
            // イベントの伝播を防止 
            disabledPropagation(e);
        }
    }
}

/**
 * キーボード押下に関連した処理の抑止
 */
function dispatchKeydown(e) { 

    var browserName = getBrowserName();

    keyCodeArray = getKeyCode(e);

    // キーコードの文字を取得 
    keychar = String.fromCharCode(keyCodeArray[0]).toUpperCase(); 

    if (browserName == "Safari") {
        // ブラウザがSafariの場合の抑止
        disableSafariKeydown(keyCodeArray,keychar,e);
    } else if (browserName == "Firefox") {
        // ブラウザがFirefoxの場合の抑止
        disableFirefoxKeydown(keyCodeArray,keychar,e);
    } else if (browserName == "IE" || browserName == "IE7") {
        // ブラウザがIEの場合の抑止
        disableIeKeydown(keyCodeArray);
    }

    return;

} 

/**
 * マウスクリックとキー入力の組み合わせを抑止する。抑止対象は以下。
 * ・Shift＋マウスクリック（ハイパーリンクの別ウィンドウ表示を抑止）
 * ・Ctrl＋マウスクリック、Ctrl＋Shift+マウスクリック（前、後ろに新しいタブを作成しての表示を抑止）
 * ・option＋マウスクリック（ダウンロード）
 * ・中ボタンクリック
 */
function disabledCreateNewWindow(e){  
    
    keyCodeArray = getKeyCode(e);
    
    var curCtrl = keyCodeArray[1];
    var curShift = keyCodeArray[2];
    var option = keyCodeArray[3];
    var command = keyCodeArray[4];

    if (document.getElementsByTagName("a")) {
        if (curCtrl || curShift || (curCtrl && curShift)) {
            if (e != null) {
                // Mozilla(Firefox, NN) and Opera 
                disabledPropagation(e);
            } else {
                userAgent = getBrowserName();
                // Internet Explorer
                if (userAgent == "IE7") {
                    if (curCtrl || (curCtrl && curShift)) {
                        alert("この操作は使用できません");
                    }
                }
                window.event.returnValue = false;
            }
        } else if (option || command) {
            if (e != null) {
                disabledPropagation(e);
            }
        } else {
            // 中ボタン押下抑止
            if(e != null) {
                // Mozilla(Firefox, NN) and Opera
                var keycode = e.which;
                if(keycode == '2') {
                    disabledPropagation(e);
                }
            } else {
                // Internet Explorer
                var button = window.event.button & 4;
                if(button == '4') {
                    userAgent = getBrowserName();
                    if (userAgent == "IE7") {
                        alert("この操作は使用できません");
                    }
                    window.event.returnValue = false;
                }
            }
        }
    }
} 

/**
 * 入力されたキーコードを取得する。
 */
function getKeyCode(e){

    // キーコード、CtrlKey、ShiftKey、AltKeyの押下状態を格納
    returnCode = new Array(5);
    
    // Mozilla(Firefox, NN) and Opera 
    if (e != null) { 
        returnCode[0] = e.which;
        returnCode[1] = typeof e.modifiers == 'undefined' ? e.ctrlKey : e.modifiers & Event.CONTROL_MASK; 
        returnCode[2] = typeof e.modifiers == 'undefined' ? e.shiftKey : e.modifiers & Event.SHIFT_MASK; 
        returnCode[3] = typeof e.modifiers == 'undefined' ? e.altKey : e.modifiers & Event.ALT_MASK;
        returnCode[4] = typeof e.modifiers == 'undefined' ? e.metaKey : e.modifiers & Event.META_MASK;
        
    // Internet Explorer 
    } else { 
        returnCode[0] = window.event.keyCode; 
        returnCode[1] = window.event.ctrlKey; 
        returnCode[2] = window.event.shiftKey; 
        returnCode[3] = window.event.altKey; 
    } 
    return returnCode;
}

/**
 * イベントの伝播をストップする。
 */
function disabledPropagation(e) {
    
    // イベントの伝播を防止     
    e.preventDefault();
    e.stopPropagation();
    
}


document.onmousedown = dispatchClick;
document.onclick = dispatchClick;
document.oncontextmenu = disabledRightClick;
document.onkeydown = dispatchKeydown;
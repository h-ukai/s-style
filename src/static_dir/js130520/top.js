
function acom_IPverck(checkVers) {
    mes = "～　お使いのブラウザは、" + checkVers[1];
    flg = checkVers[0];
    if(flg){
        mes = mes + "です。～　";
        document.write(mes.fontcolor("blue"))
    }else{
        if(checkVers[1] == ""){
            mes = "～　お使いのブラウザでは、ＲＥＩＮＳ　ＩＰ型のご利用はできません。～　";
            document.write(mes.fontcolor("red"))
        }else{
            mes = mes + "です。ＲＥＩＮＳ　ＩＰ型のご利用はできません。～　";
            document.write(mes.fontcolor("red"))
        }
    }
}

function acom_IPver(){
    checkVers = new Array(2);
    checkVers[0] = false;
    checkVers[1] = "";
    userA = navigator.userAgent;

    if( navigator.appName.charAt(0)=="N" ){
        
        if(userA.indexOf("Firefox") > -1){
            num = userA.indexOf("Firefox");
            nVersion = userA.charAt(num+8);
            if(nVersion == 1){
                checkVers[0] = false;
                checkVers[1] = nVersion + ".x　";
            }
            else if(nVersion == 2){
                checkVers[0] = true;
                checkVers[1] = nVersion + ".x　";
            }
            else if(nVersion == 3){
                checkVers[0] = true;
                checkVers[1] = nVersion + ".x　";
            }
            else{
                checkVers[0] = false;
            }
            checkVers[1] = "Firefox " + checkVers[1];
        }else if(userA.indexOf("Safari") > -1){
            appVer = userA.substr(userA.indexOf("AppleWebKit"));
            appVer = appVer.substr(eval(appVer.indexOf("/"))+1,1);
            version = eval(appVer)-2;
            if(version==2){
                checkVers[1] = "2.x　";
            }
            else if(version==3){
                checkVers[1] = "3.x　";
            }
            else{
                checkVers[1] = "(バージョン対象外)　";
            }
            checkVers[1] = "Safari " + checkVers[1];
            checkVers[0] = false;
        }else {
            if(navigator.appVersion.charAt(0)==5){
                if(userA.indexOf("Netscape") > -1){
                    num = userA.indexOf("Netscape");
                    nVersion = userA.substr(num);
                    num = nVersion.indexOf("/");
                    nVersion = nVersion.substr(num+1,1);
                    checkVers[1] = nVersion + ".x　";
                    checkVers[1] = "Netscape " + checkVers[1];
                }
            }else{
                if(navigator.appVersion.charAt(0)==2){
                    checkVers[1] = "2.x　";
                }
                if(navigator.appVersion.charAt(0)==3){
                    checkVers[1] = "3.x　";
                }
                if(navigator.appVersion.charAt(0)==4){
                    checkVers[1] = "4.x　";
                }
                checkVers[1] = "Netscape " + checkVers[1];
            }
            checkVers[0] = false;
        }
    }
    else if( navigator.appName.charAt(0)=="M" ){
        if(navigator.appVersion.charAt(0)==2){
            checkVers[1] = "3.x　";
            checkVers[0] = false;
        }
        if(navigator.appVersion.charAt(0)==3){
            checkVers[1] = "3.x　";
            checkVers[0] = false;
        }
        if(navigator.appVersion.charAt(0)==4){
            if(navigator.appVersion.indexOf("MSIE 5") != -1){
                tmpNum = userA.indexOf("MSIE 5");
                tmpVer = userA.substr(tmpNum+5,3);
                if(tmpVer == "5.5"){
                    checkVers[0] = true;
                }
                else if(tmpVer > "5.5"){
                    checkVers[0] = true;
                }
                else{
                    checkVers[0] = false;
                }
                checkVers[1] = tmpVer + "　";
            } else {
                tmpNum = userA.indexOf("MSIE");
                tmpVer = userA.charAt(tmpNum+5);
                if(eval(tmpVer) < 6){
                    checkVers[0] = false;
                    checkVers[1] = "4.x　";
                } else {
                    checkVers[0] = true;
                    checkVers[1] = tmpVer.charAt(0) + ".x　";
                }
            }
        }
        checkVers[1] = "InternetExplorer " + checkVers[1];
        if(userA.indexOf("Opera")>-1){
            checkVers[0] = false;
            checkVers[1] = "";
        }
    }
    
    if ( userA.indexOf("Mac") > -1) {
        if(userA.indexOf("SAFARI") == -1){
            checkVers[0] = false;
        }
        if(userA.indexOf("Safari") > -1){
            appVer = userA.substr(userA.indexOf("AppleWebKit"));
            appVer = appVer.substr(eval(appVer.indexOf("/"))+1,1);
            version = eval(appVer)-2;
            if(version==2){
                checkVers[1] = "2.x　";
                checkVers[0] = false;
            }
            else if(version==3){
                checkVers[1] = "3.x　";
                checkVers[0] = true;
            }
            else{
                checkVers[1] = "(バージョン対象外)　";
                checkVers[0] = false;
            }
            checkVers[1] = "Safari " + checkVers[1];
        }
        if(checkVers[1] != ""){
            checkVers[1] = "Macintosh版 " + checkVers[1];
        }
    }

    return checkVers;
}

function openMenu(url){
    window.open(url,"menu","width=1024,height=768,resizable=1,scrollbars=1,status=1");
}



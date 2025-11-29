/*
 * 新規　2008/10/14 李文勇 SI1_BK_0540
 *
 * 改修履歴
 * 2008/08/14 田 SI2_NT_0295
 * 2008/10/03 あら川 SI2_NT_1007
 *
*/
function HTMLDecode(text)
{
	var temp = document.createElement("div");
	temp.innerHTML = text;
	var output = temp.innerText || temp.textContent;
	temp = null;
	return output;
}
var timer;
var newwindow;
var logicFileField;
var physicalFileField;
//判断新ウインドウ閉まる
function isClosed() {
	if (newwindow.closed == true) {
		
		logicFileField=document.getElementById("logicFileField").value;
		physicalFileField=document.getElementById("physicalFileFierd").value;

        // 2008/08/14 田 SI2_NT_0295 新しく追加の画像参照の修正 Begin
        var ssnPth = document.getElementById("ssnPth").value;
        
        physicalFileField = ssnPth + physicalFileField;
        // 2008/08/14 田 SI2_NT_0295 新しく追加の画像参照の修正 End

		if (null != logicFileField && "" != logicFileField) {
		// 2008/08/25 徐 新追加画像の時、画像削除の修正 Begin
		// addOne(logicFileField,-1,"",physicalFileField);
		// 2008/10/03 あら川 SI2_NT_1007 BEGIN
		    addOne(logicFileField,0,"",physicalFileField,"","gazuAdd");
		//    addOne(logicFileField,-1,"",physicalFileField,"","gazuAdd");
		// 2008/10/03 あら川 SI2_NT_1007 END
		// 2008/08/25 徐 新追加画像の時、画像削除の修正 End
			document.getElementById("logicFileField").value="";
			document.getElementById("physicalFileFierd").value="";
		}
		window.clearInterval(timer);
	}
}


//画像参照
function openpic(id) {
	var pfname;
	var tid;
	if (id==10) {
		tid="bkknGzuFlpth10";
	} else {
		tid="bkknGzuFlpth0"+id;
	}
	pfname=document.getElementById(tid).value;

	var url1 = HTMLDecode(document.getElementById('contextPath').value) +  "/bkkn/KG010_001_OP.do";
	var url2 = HTMLDecode(document.getElementById('contextPath').value) +  "/bkkn/KG010_001.do";
	//openImageView('物件',pfname,
    //		'${pageContext.request.contextPath}/bkkn/KG010_001_OP.do', 
    //		'${pageContext.request.contextPath}/bkkn/KG010_001.do', 
	//		'${reins:generateRandomID()}');
	var randomID = document.getElementById('randomID').value;
	openImageView('物件',pfname, url1, url2, randomID);
}

//2008/08/26 クライアントがFirfoxの時、画像追加の修正 徐凱 Mod Begin
//画像を追加window open
//function openAddWindow(logicFileField,physicalFileFierd) {
function openAddWindow(randomID) {
	var feature;
	var innerTable;
	innerTable=document.getElementById("innerTable");
	if (innerTable.rows.length<22)
	{
		feature ="menubar=no,toolbar=no,location=no,"; 
		feature+="scrollbars=yes,resizable=yes,status=no,modal=yes"; 

//	    //window.open('/reins/ktgyoumu/KG008_001.do?logicFileField=lfiled1&physicalFileFierd=pfiled1&thmbsizehgt=800&thmbsizewth=600&kg008callflg=0',null,feature);
//		//MakePopFull('/reins/ktgyoumu/KG008_001.do?logicFileField=lfiled1&physicalFileFierd=pfiled1&thmbsizehgt=800&thmbsizewth=600&kg008callflg=0',null);
//		//openFileUp(logicFileField,physicalFileFierd,"160","210","0", "${reins:generateRandomID()}");

		// newwindow=openFileUp("logicFileField","physicalFileFierd","210","160","0", "${reins:generateRandomID()}");
		newwindow=openFileUp("logicFileField","physicalFileFierd","210","160","0", randomID);
		timer=window.setInterval("isClosed()",500);
		return false;

	} else {
		alert ("10件を超える画像追加は実施できません。");
		return false;
	}
}
//2008/08/26 クライアントがFirfoxの時、画像追加方の修正 徐凱 Mod End
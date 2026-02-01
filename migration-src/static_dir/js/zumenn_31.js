/*
 * 新規　2008/10/14 李文勇 SI1_BK_0540
 *
 * 改修履歴
 * 2008/08/08 孫海軍 仕様変更の330-3
 * 2008/07/29 キン小宇 SI2_NT_068 
 * 2008/09/12 李文勇 SI2_NT_0765
 * 2008/07/25 李文勇 SI2_NT_070
 * 2008/10/09 星勝也 SI2_NT_1075
 * 2008/11/05 星勝也 SI3_NT_0105
*/
function HTMLDecode(text)
{
	var temp = document.createElement("div");
	temp.innerHTML = text;
	var output = temp.innerText || temp.textContent;
	temp = null;
	return output;
}
function setFilePath(zmnFlpth, zmnFlmi)
{
	  if (null != window.document.getElementById('zmnFlpth') ){
          window.document.getElementById('zmnFlpth').value=zmnFlpth;
      }
      if (null != window.document.getElementById('zmnFlmi')){
          window.document.getElementById('zmnFlmi').value=zmnFlmi;
          window.document.getElementById('browser').style.display="";
      }
      if (null != window.document.getElementById('zmnName')){
      	 window.document.getElementById('zmnName').value=zmnFlmi;
      }
      if (null != window.document.getElementById('zmnFlag')){
      	 window.document.getElementById('zmnFlag').value="1";
      }
}
//入力画面用 2008/08/22 徐凱 ADD
function browser(bkknId, randomID){
	var flag = window.document.getElementById('zmnFlag').value;
	
	if('0' == flag){
	//SI2_NT_068 靳小宇  20080729 /bkkn/KG010_003.do を/ktgyoumu/KG010_003.doに変更しました
	//SI2_NT_068 靳小宇  20080804 　変更を取り消し
	// 2008/08/08 孫海軍 仕様変更の330-3 Begin
	    var openPdfDownLoad_url = HTMLDecode(document.getElementById('contextPath').value) +  "/bkkn/KG010_002.do";
		//openPdfDownLoad('${pageContext.request.contextPath}/bkkn/KG010_002.do', 
		//				'${BkknForm.ttZmnBean.bkknId}', 
		//				'${reins:generateRandomID()}',
		//				'0');
		// SI3_NT_0105 MOD 星勝也 BEGIN
		// openPdfDownLoad(openPdfDownLoad_url, bkknId, randomID,'0');
		openPdfDownLoad(openPdfDownLoad_url, bkknId, randomID,'0', '0');
		// SI3_NT_0105 MOD 星勝也 END
        // 2008/08/08 孫海軍 仕様変更の330-3 End
	}else{
	    var openPdfDownLoadByName_url = HTMLDecode(document.getElementById('contextPath').value) +  "/bkkn/KG010_003.do";
		var filepath = document.getElementById('zmnFlpth').value; 
		//SI2_NT_068 靳小宇  20080729 /bkkn/KG010_003.do を/bkkn/KG010_003.doに変更しました
		//SI2_NT_068 靳小宇  20080804 　変更を取り消し
		//SI2_NT_0765 李文勇　20080912
    	//openPdfDownLoadByName('${pageContext.request.contextPath}/bkkn/KG010_003.do',
    	//					  document.getElementById('zmnFlpth').value ,
    	//					  '${reins:generateRandomID()}', 
    	//					  document.getElementById('zmnFlmi').value);
    	openPdfDownLoadByName(openPdfDownLoadByName_url,
    					  document.getElementById('zmnFlpth').value ,
    					  randomID, 
    					  document.getElementById('zmnFlmi').value);
	}
	return false;
}
// 確認画面用  2008/08/22 徐凱 ADD
// SI2_NT_070 李文勇 ADD 20080725 START
// 2008/08/22 徐凱　MOD　START
//function browser2(filepath){
//			//var filepath = document.getElementById('zmnFlpth').value;
//			//SI2_NT_068 靳小宇  20080729 /bkkn/KG010_003.do を/ktgyoumu/KG010_003.doに変更しました
//			//SI2_NT_068 靳小宇  20080804 　変更を取り消し
//            openPdfDownLoadByName('${pageContext.request.contextPath}/bkkn/KG010_003.do',
//              				 	   filepath ,
//              				 	   '${reins:generateRandomID()}');
//}
function browser2(bkknid, randomID){
	var flag = window.document.getElementById('zmnFlag').value;
	if ('0'==flag) {
	//存在図面が変更しないの場合
	    var openPdfDownLoad_url = HTMLDecode(document.getElementById('contextPath').value) +  "/bkkn/KG010_002.do";
		//openPdfDownLoad('${pageContext.request.contextPath}/bkkn/KG010_002.do',
		//				 bkknid,
		//				'${reins:generateRandomID()}',
		//				'0');
		// SI3_NT_0105 MOD 星勝也 BEGIN
		// openPdfDownLoad(openPdfDownLoad_url, bkknid,randomID,'0');
		openPdfDownLoad(openPdfDownLoad_url, bkknid,randomID,'0','0');
		// SI3_NT_0105 MOD 星勝也 END
	} else {
	//存在図面が変更の場合
		//SI2_NT_0765 李文勇　20080912
		var openPdfDownLoadByName_url = HTMLDecode(document.getElementById('contextPath').value) +  "/bkkn/KG010_003.do";
		//openPdfDownLoadByName('${pageContext.request.contextPath}/bkkn/KG010_003.do',
		//					  window.document.getElementById('zmntempPath').value ,
		//					  '${reins:generateRandomID()}',
		//					  document.getElementById('zmnFlmi').value);
		openPdfDownLoadByName(openPdfDownLoadByName_url,
							  window.document.getElementById('zmntempPath').value ,
							  randomID,
							  document.getElementById('zmnFlmi').value);
	}
}
// 2008/08/22 徐凱　MOD　END
// SI2_NT_070 李文勇 ADD 20080725 END

// SI2_NT_1075 MOD 星勝也 BEGIN
function openZmnUploadEx(randomID){

      var zmnFlmi = document.getElementById('zmnFlmi').value;
	  var openZmnUpload_url = HTMLDecode(document.getElementById('contextPath').value) +  "/zmn/ZK009_FORW001.do";
      if (zmnFlmi.length > 0) { 
          //openZmnUpload(1,
          //              'この物件には既に図面が登録されています。\n図面を差し替えてもよろしいですか？',
          //              'logicFileField','physicalFileFierd',
          //              '${pageContext.request.contextPath}/zmn/ZK009_FORW001.do',
          //              '${reins:generateRandomID()}');
          openZmnUpload(1,
                        'この物件には既に図面が登録されています。\n図面を差し替えてもよろしいですか？',
                        'logicFileField','physicalFileFierd',
                        openZmnUpload_url,
                        randomID);
      } else {
          //openZmnUpload(0,
          //              'この物件には既に図面が登録されています。\n図面を差し替えてもよろしいですか？',
          //              'logicFileField','physicalFileFierd',
          //              '${pageContext.request.contextPath}/zmn/ZK009_FORW001.do',
          //              '${reins:generateRandomID()}');
          openZmnUpload(0,
                        'この物件には既に図面が登録されています。\n図面を差し替えてもよろしいですか？',
                        'logicFileField','physicalFileFierd',
                        openZmnUpload_url,
                        randomID);
      }
}
// SI2_NT_1075 MOD 星勝也 END
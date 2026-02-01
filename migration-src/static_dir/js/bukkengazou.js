/*
 * 修正履歴
 * 
 * 2008/08/07 田 SI2_NT_0282 画像説明入力チェック
 * 2008/08/14 田 SI2_NT_0295 新しく追加の画像参照の修正
 * 2008/10/18 海浦隆一 SI1_BK_0185
 */
//物件画像の追加と削除　START
var optArray;
var pId;
var pos;
var posArray;
var width=400;
var height=300;
function bkknGazouInit(){
    var fileArr;
    var str;
    var fName;
    str=document.getElementById("options").value;
    optArray=str.split(",");

    var gzuErrPosString = document.getElementById("gzuErrPos").value;
    var posArray = gzuErrPosString.split(",");
    
    for (var i=1;i<=10;i++){

    fName="file"+i;
        // 2008/08/14 田 SI2_NT_0295 新しく追加の画像参照の修正 Begin
        var file=document.getElementById(fName).value;
        if (file!=",,,") {
            fileArr=file.split(",");
            // 2008/10/18 海浦隆一 SI1_BK_0185 BEGIN
            if (fileArr[0]!="" && fileArr[3]!="") {
            // 2008/10/18 海浦隆一 SI1_BK_0185 END
	            // 2008/08/07 田 SI2_NT_0282 画像説明入力チェック Begin
	            var flg = isErrArea(i, posArray);
				// 2008/08/25 徐 新追加画像の時、画像削除の修正 Begin
	            if (flg) {
	            // addOne(fileArr[0],fileArr[1],fileArr[2],fileArr[3],1,"init");
	              addOne(HTMLDecode(fileArr[0]),fileArr[1],fileArr[2],HTMLDecode(fileArr[3]),1,"init");
	            } else {
	            // addOne(fileArr[0],fileArr[1],fileArr[2],fileArr[3],0,"init");
	              //addOne(fileArr[0],fileArr[1],fileArr[2],fileArr[3],0,"init");
	              addOne(HTMLDecode(fileArr[0]),fileArr[1],fileArr[2],HTMLDecode(fileArr[3]),0,"init");
            // 2008/10/18 海浦隆一 SI1_BK_0185 BEGIN
            }
            // 2008/08/25 徐 新追加画像の時、画像削除の修正 End
            // 2008/08/14 田 SI2_NT_0295 新しく追加の画像参照の修正 End
            } else {
                document.getElementById(fName).value = "";
            }
            // 2008/10/18 海浦隆一 SI1_BK_0185 END
        }
    }
}
// 2008/08/07 田 SI2_NT_0282 画像説明入力チェック End

function makeOptions(vName,knd) {

    var strOptions;
    strOptions="";
    strOptions+="<select id='"+vName+"' name='"+vName+"' size='1'>";
    strOptions+="<option value=''></option>";
    for (var i=0;i<optArray.length;i+=2) {
        if (parseInt(knd)==optArray[i]) {
            strOptions+="<option value='"+optArray[i]+"' selected>"+optArray[i+1]+"</option>";
        } else {
            strOptions+="<option value='"+optArray[i]+"'>"+optArray[i+1]+"</option>";
        }

    }
    strOptions+="</select>";
    document.getElementById(vName).value=knd;
    return strOptions;
}

//半角TO全角関数 
function ToDBC(txtstring) 
{ 
    var tmp = ""; 
    for(var i=0;i<txtstring.length;i++) 
    { 
        if(txtstring.charCodeAt(i)==32) { 
            tmp= tmp+ String.fromCharCode(12288); 
        } 
        if(txtstring.charCodeAt(i)<127) 
        { 
            tmp=tmp+String.fromCharCode(txtstring.charCodeAt(i)+65248); 
        } 
    } 
    return tmp; 
} 

// 2008/08/07 田 SI2_NT_0282 画像説明入力チェック Begin
// 2008/08/25 徐 新追加画像の時、画像削除の修正 Begin
// 画像を追加する
// function addOne(filename,gazoubunrui,gazousetsumei,pfilename, errFlg)
// {

// 2008/11/25 関 SIK_0126 START
function HTMLEncode(html)
{
	var temp = document.createElement ("div");
	(temp.textContent != null) ? (temp.textContent = html) : (temp.innerText = html);
	var output = temp.innerHTML;
	temp = null;
	return output;
}

function HTMLDecode(text)
{
	var temp = document.createElement("div");
	temp.innerHTML = text;
	var output = temp.innerText || temp.textContent;
	temp = null;
	return output;
}
// 2008/11/25 関 SIK_0126 END

function addOne(filename,gazoubunrui,gazousetsumei,pfilename, errFlg,comeFrom)
{
// 2008/08/25 徐 新追加画像の時、画像削除の修正 End
// 2008/08/07 田 SI2_NT_0282 画像説明入力チェック End
    var html="";
    var innerTable;
    var oTR1;
    var oTR2;
    var oTD1;
    var oTD2;
    var oTD3;
    var oTD4;
    var i=0;
    var strId;
    var tmpNum;
    var tmpId;

    innerTable=document.getElementById("innerTable");
    oTR1=innerTable.insertRow(innerTable.rows.length);
    tmpNum=oTR1.rowIndex;

    if (tmpNum==1){
        strId=""+tmpNum
    } else {
        strId=""+(tmpNum/2);
        tmpId="0"+(tmpNum/2);
    }

    if (tmpId=="010") {
        tmpId="10"    
    }
    
    //<TR>1
    oTD1=oTR1.insertCell(0);
    oTD1.innerHTML="画像"+ToDBC(strId);
    oTD1.id="画像"+strId;
    oTD1.className="centerTd indexTableColorA tdWidthA";
    oTD2=oTR1.insertCell(1);
    oTD2.innerHTML="<input type='text' id='bkknGzuFlmi"+tmpId+"' name='bkknGzuFlmi"+tmpId+"' value='"+HTMLEncode(filename)+"' class='inputType2forGzuFileName' readonly/>"+"<input type='hidden' id='ObkknGzuFlpth"+tmpId+"' name='ObkknGzuFlpth"+tmpId+"' value='"+pfilename+"'/>";
    oTD2.className="leftTd valueTableColorB tdWidthC";    
    var n1="bkknGzuFlmi"+tmpId;
    document.getElementById(n1).value=filename;
    document.getElementById("bkknGzuFlpth"+tmpId).value=pfilename;

    oTD3=oTR1.insertCell(2);
    oTD3.className="leftTd valueTableColorB tdWidth";
    oTD3.colSpan=2;
    oTD3.innerHTML="";
    html="<div align='right'>";
    html+="<input type='image' src='../img/btn_gazou_sanshou.gif' value='画像参照' onclick='openpic("+strId+");return false;'/>";
    html+="<input type='image' src='../img/btn_gazou_sakujho.gif' value='画像削除' onclick='deleteConfirm("+strId+");return false;'/>"
    html+="</div>";
    oTD3.innerHTML=html;

    //<TR>2
    oTR2=innerTable.insertRow(innerTable.rows.length);
    oTD1=oTR2.insertCell(0);
    oTD1.innerHTML="画像"+ToDBC(strId)+"分類";
    oTD1.id="画像"+strId+"分類";
    oTD1.className="centerTd indexTableColorA tdWidthA";

    oTD2=oTR2.insertCell(1);
    oTD2.className="leftTd valueTableColorB tdWidthC";
    html=makeOptions("bkknGzuBnri"+tmpId,gazoubunrui);
    oTD2.innerHTML=html;

    oTD3=oTR2.insertCell(2);
    oTD3.className="enterTd indexTableColorC";
    oTD3.innerHTML="画像"+ToDBC(strId)+"説明";
    oTD3.id="画像"+strId+"説明";
    
    oTD4=oTR2.insertCell(3);
    oTD4.className="leftTd valueTableColorB";
    html="";

    // 2008/08/07 田 SI2_NT_0282 画像説明入力チェック Begin
    if (errFlg=="1") {
        html="<input type='text' maxlength='20' id='bkknGzuStmi"+tmpId+"' name='bkknGzuStmi"+tmpId+"' class='imeActive inputType2byte11to20 errArea' value='"+gazousetsumei+"'/>";
    } else {
        html="<input type='text' maxlength='20' id='bkknGzuStmi"+tmpId+"' name='bkknGzuStmi"+tmpId+"' class='imeActive inputType2byte11to20' value='"+gazousetsumei+"'/>";
    }
    // 2008/08/07 田 SI2_NT_0282 画像説明入力チェック End
    
    oTD4.innerHTML=html;
    var sm="bkknGzuStmi"+tmpId;
    document.getElementById(sm).value=gazousetsumei;
	// 2008/08/25 徐 新追加画像の時、画像削除の修正 Begin    
    if (comeFrom=="gazuAdd") {
    	var isNew = "gazu"+tmpId+"IsNew";
    	document.getElementById(isNew).value="1";
    }
	// 2008/08/25 徐 新追加画像の時、画像削除の修正 End
}

/*
 * 項目反転チェック
 */
function isErrArea(i, posArray){
/*
    var gzuErrPosString = document.getElementById("gzuErrPos").value;

    // 画像全部OKの場合
    if (gzuErrPosString.length<1) {
      return false;
    }
  
    var posArray = gzuErrPosString.split(",");
     */ 
    for (var j=0;j<posArray.length;j++) {
      if (posArray[j]==i) {
        return true;
      }
    }
    
    return false;
}

function deleteConfirm(rowIndex)
{
    // 2008/08/07 田 SI2_NT_0282 画像説明入力チェック Begin
    var gzuErrPosString = document.getElementById("gzuErrPos").value;
    
    var index = gzuErrPosString.indexOf(rowIndex);
    var replaceVlaue = "";

    if (index == gzuErrPosString.length-1) {
        replaceVlaue = rowIndex;
    } else {
        replaceVlaue = rowIndex+",";
    }
    gzuErrPosString = gzuErrPosString.replace(replaceVlaue,"");
    //var posArray = gzuErrPosString.split(",");
    posArray = gzuErrPosString.split(",");
    var newValue = "";
    for (var j=0;j<posArray.length;j++) {
        if (posArray[j] != "" && posArray[j] > rowIndex) {
          posArray[j] = posArray[j]-1;
        }
    }
    newValue = posArray.toString();
    document.getElementById("gzuErrPos").value = newValue;
    // 2008/08/07 田 SI2_NT_0282 画像説明入力チェック End
    
    //図面はらくらく登録の場合判定　徐凱　2008/08/19　BEGIN
    var zmn=document.getElementById("zmn").value;
    var funcMode=document.getElementById("funcMode").value;
    var msg="らくらく登録で使用されている可能性がありますが、削除してよろしいですか？";
	// 2008/08/25 徐 新追加画像の時、画像削除の修正 Begin    
    var isNew;
    var tmpId;
    var zmnFlag;
    if (rowIndex<10) {
       tmpId="gazu0"+rowIndex+"IsNew";
    }else{
       tmpId="gazu"+rowIndex+"IsNew";
    }
    isNew=document.getElementById(tmpId).value;
    zmnFlag=document.getElementById("zmnFlag").value;
    
    if ((funcMode=="bkknhnku") 
    	|| (funcMode=="bkknsiturk") 
    	|| (funcMode=="bkknsiykmnt") ) {
	    //if (zmn=="03") {
	    if (zmn=="03" && zmnFlag=="0" && isNew=="0") {
	    	if (confirm(msg)) {
	    	 	deleteGazu(rowIndex);
	    		
	    	}
	    } else {
	    	deleteGazu(rowIndex);
	    }
    } else {
    	deleteGazu(rowIndex);
    }
	// 2008/08/25 徐 新追加画像の時、画像削除の修正 End    
/* 
    var vTable=document.getElementById("innerTable");
    var rowCount = vTable.rows.length;
    var i=0;
    var checkedId;
    var tmpId;
    
    var bkknGzuFlmi;
    var bkknGzuBnri;
    var bkknGzuStmi;
    var bkknGzuFlpth;
    
    if (rowCount==3) {
        vTable.deleteRow(1);
        vTable.deleteRow(1);
    } else{
        vTable.deleteRow(2*rowIndex);
        vTable.deleteRow(2*rowIndex);    
    }

    for(i=rowIndex;i<vTable.rows.length/2;i++)
    {
        var strId;
        var strId1;
        var tmp;
        var tmp1;
        var checkedId;
        var tmpId;
        if (i<10) {
            tmpId="0"+i;
        }else{
            tmpId=i
        }
        
        if ((i+1)==10) {
            tNext=""+(i+1);
        } else {
            tNext="0"+(i+1);
        }

        //<TR>1
        vTable.rows[2*i].cells[0].innerHTML = "画像"+i;
        strId="bkknGzuFlmi"+tNext;
        tmp=document.getElementById(strId).value;
        strId1="bkknGzuFlpth"+tNext;
        tmp1=document.getElementById(strId1).value;
        html="";
        html+="<input type='text' id='bkknGzuFlmi"+tmpId+"' name='bkknGzuFlmi"+tmpId+"' value='"+tmp+"'readonly>"+"<input type='hidden' id='ObkknGzuFlpth"+tmpId+"' name='ObkknGzuFlpth"+tmpId+"' value='"+tmp1+"'/>";
        vTable.rows[2*i].cells[1].innerHTML=html;
        document.getElementById("bkknGzuFlmi"+tmpId).value=tmp;
        document.getElementById("bkknGzuFlpth"+tmpId).value=tmp1;        

        html="<div align='right'>";
        html+="<input type='image' src='../img/btn_gazou_sanshou.gif' value='画像参照' onclick='openpic("+i+");return false;'/>";
        html+="<input type='image' src='../img/btn_gazou_sakujho.gif' value='画像削除' onclick='deleteOne("+i+");return false;'/>";    
        html+="</div>";
        vTable.rows[2*i].cells[2].innerHTML=html;

        //<TR>2
        vTable.rows[2*i+1].cells[0].innerHTML = "画像"+i+"分類";
        checkedId=document.getElementById("bkknGzuBnri"+tNext).value;
        html=makeOptions("bkknGzuBnri"+tmpId,checkedId);
        vTable.rows[2*i+1].cells[1].innerHTML=html;

        vTable.rows[2*i+1].cells[2].innerHTML = "画像"+i+"説明";
        strId="bkknGzuStmi"+tNext;
        tmp=document.getElementById(strId).value;
        
        html="";
        if (isErrArea(i, posArray) ) {
          html="<input type='text' maxlength='20' id='bkknGzuStmi"+tmpId+"' name='bkknGzuStmi"+tmpId+"' class='imeActive inputType2byte11to20 errArea' value='"+tmp+"'>";
        } else {
          html="<input type='text' maxlength='20' id='bkknGzuStmi"+tmpId+"' name='bkknGzuStmi"+tmpId+"' class='imeActive inputType2byte11to20' value='"+tmp+"'>";
        }
        
        vTable.rows[2*i+1].cells[3].innerHTML=html;
        document.getElementById("bkknGzuStmi"+tmpId).value=tmp;
    }
    
    rowCount=vTable.rows.length;

    for (var j=10;j>rowCount/2-1;j--) {
        if (j!=10) {
            bkknGzuFlmi="bkknGzuFlmi0"+j;
            bkknGzuBnri="bkknGzuBnri0"+j;
            bkknGzuStmi="bkknGzuStmi0"+j;
            bkknGzuFlpth="bkknGzuFlpth0"+j;
        } else {
            bkknGzuFlmi="bkknGzuFlmi"+j;
            bkknGzuBnri="bkknGzuBnri"+j;
            bkknGzuStmi="bkknGzuStmi"+j;
            bkknGzuFlpth="bkknGzuFlpth"+j;
        }

        document.getElementById(bkknGzuFlmi).value="";
        document.getElementById(bkknGzuBnri).value="";
        document.getElementById(bkknGzuStmi).value="";
        document.getElementById(bkknGzuStmi).value="";
        document.getElementById(bkknGzuFlpth).value="";
    }*/
}

function deleteGazu(rowIndex) {

    var vTable=document.getElementById("innerTable");
    var rowCount = vTable.rows.length;
    var i=0;
    var checkedId;
    var tmpId;

    var bkknGzuFlmi;
    var bkknGzuBnri;
    var bkknGzuStmi;
    var bkknGzuFlpth;
    var gazuIsNew;
    
    if (rowCount==3) {
        vTable.deleteRow(1);
        vTable.deleteRow(1);
    } else{
        vTable.deleteRow(2*rowIndex);
        vTable.deleteRow(2*rowIndex);    
    }

    for(i=rowIndex;i<vTable.rows.length/2;i++)
    {
        var strId;
        var strId1;
        var tmp;
        var tmp1;
        var checkedId;
        var tmpId;
        if (i<10) {
            tmpId="0"+i;
        }else{
            tmpId=i;
        }
        
        if ((i+1)==10) {
            tNext=""+(i+1);
        } else {
            tNext="0"+(i+1);
        }
        // 2008/10/18 海浦隆一 SI1_BK_0185 BEGIN
        tmp = HTMLDecode(document.getElementById("file"+(i+1)).value);
        document.getElementById("file"+i).value = tmp;
        // 2008/10/18 海浦隆一 SI1_BK_0185 END
        
        //<TR>1
        // SI1KK_BJ_0050 徐凱 2008/09/03 MOD Begin 
        // vTable.rows[2*i].cells[0].innerHTML = "画像"+i;
        vTable.rows[2*i].cells[0].innerHTML = "画像"+ToDBC(""+i);
        // SI1KK_BJ_0050 徐凱 2008/09/03 MOD End
        vTable.rows[2*i].cells[0].id = "画像"+ToDBC(""+i);
        //
        strId="bkknGzuFlmi"+tNext;
        tmp=document.getElementById(strId).value;
        strId1="bkknGzuFlpth"+tNext;
        tmp1=document.getElementById(strId1).value;
        html="";
        // 2008/10/18 海浦隆一 SI1_BK_0185 BEGIN
        html+="<input type='text' id='bkknGzuFlmi"+tmpId+"' class='inputType2forGzuFileName' name='bkknGzuFlmi"+tmpId+"' value='"+tmp+"'readonly>"+"<input type='hidden' id='ObkknGzuFlpth"+tmpId+"' name='ObkknGzuFlpth"+tmpId+"' value='"+tmp1+"'/>";
        // html+="<input type='text' id='bkknGzuFlmi"+tmpId+"' name='bkknGzuFlmi"+tmpId+"' value='"+tmp+"'readonly>"+"<input type='hidden' id='ObkknGzuFlpth"+tmpId+"' name='ObkknGzuFlpth"+tmpId+"' value='"+tmp1+"'/>";
        // 2008/10/18 海浦隆一 SI1_BK_0185 END
        vTable.rows[2*i].cells[1].innerHTML=html;
        document.getElementById("bkknGzuFlmi"+tmpId).value=tmp;
        document.getElementById("bkknGzuFlpth"+tmpId).value=tmp1;        

        html="<div align='right'>";
        html+="<input type='image' src='../img/btn_gazou_sanshou.gif' value='画像参照' onclick='openpic("+i+");return false;'/>";
        html+="<input type='image' src='../img/btn_gazou_sakujho.gif' value='画像削除' onclick='deleteConfirm("+i+");return false;'/>";    
        html+="</div>";
        vTable.rows[2*i].cells[2].innerHTML=html;

        //<TR>2
        // SI1KK_BJ_0050 徐凱 2008/09/03 MOD Begin
        // vTable.rows[2*i+1].cells[0].innerHTML = "画像"+i+"分類";
        vTable.rows[2*i+1].cells[0].innerHTML = "画像"+ToDBC(""+i)+"分類";
        // SI1KK_BJ_0050 徐凱 2008/09/03 MOD End
        // 2008/10/18 海浦隆一 SI1_BK_0185 BEGIN
        vTable.rows[2*i+1].cells[0].id = "画像"+ToDBC(""+i)+"分類";
        // 2008/10/18 海浦隆一 SI1_BK_0185 END
        checkedId=document.getElementById("bkknGzuBnri"+tNext).value;
        html=makeOptions("bkknGzuBnri"+tmpId,checkedId);
        vTable.rows[2*i+1].cells[1].innerHTML=html;
		// SI1KK_BJ_0050 徐凱 2008/09/03 MOD Begin
        // vTable.rows[2*i+1].cells[2].innerHTML = "画像"+i+"説明";
        vTable.rows[2*i+1].cells[2].innerHTML = "画像"+ToDBC(""+i)+"説明";
        // 2008/10/18 海浦隆一 SI1_BK_0185 BEGIN
        vTable.rows[2*i+1].cells[2].id = "画像"+ToDBC(""+i)+"説明";
        // 2008/10/18 海浦隆一 SI1_BK_0185 END
        // SI1KK_BJ_0050 徐凱 2008/09/03 MOD End
        strId="bkknGzuStmi"+tNext;
        tmp=document.getElementById(strId).value;
        
        html="";
        if (isErrArea(i, posArray) ) {
          html="<input type='text' maxlength='20' id='bkknGzuStmi"+tmpId+"' name='bkknGzuStmi"+tmpId+"' class='imeActive inputType2byte11to20 errArea' value='"+tmp+"'>";
        } else {
          html="<input type='text' maxlength='20' id='bkknGzuStmi"+tmpId+"' name='bkknGzuStmi"+tmpId+"' class='imeActive inputType2byte11to20' value='"+tmp+"'>";
        }
        
        vTable.rows[2*i+1].cells[3].innerHTML=html;
        document.getElementById("bkknGzuStmi"+tmpId).value=tmp;
	// 2008/08/25 徐 新追加画像の時、画像削除の修正 Begin        
        strId="gazu"+tNext+"IsNew";
        tmp=document.getElementById(strId).value;
        document.getElementById("gazu"+tmpId+"IsNew").value=tmp;
    }
	// 2008/08/25 徐 新追加画像の時、画像削除の修正 End    
    rowCount=vTable.rows.length;

    for (var j=10;j>rowCount/2-1;j--) {
        if (j!=10) {
            bkknGzuFlmi="bkknGzuFlmi0"+j;
            bkknGzuBnri="bkknGzuBnri0"+j;
            bkknGzuStmi="bkknGzuStmi0"+j;
            bkknGzuFlpth="bkknGzuFlpth0"+j;
            // 2008/08/25 徐 新追加画像の時、画像削除の修正 Begin
            gazuIsNew="gazu0"+j+"IsNew";
            // 2008/08/25 徐 新追加画像の時、画像削除の修正 End
        } else {
            bkknGzuFlmi="bkknGzuFlmi"+j;
            bkknGzuBnri="bkknGzuBnri"+j;
            bkknGzuStmi="bkknGzuStmi"+j;
            bkknGzuFlpth="bkknGzuFlpth"+j;
            // 2008/08/25 徐 新追加画像の時、画像削除の修正 Begin
            gazuIsNew="gazu"+j+"IsNew";
            // 2008/08/25 徐 新追加画像の時、画像削除の修正 End
        }
        document.getElementById(bkknGzuFlmi).value=" ";
        document.getElementById(bkknGzuBnri).value=" ";
        document.getElementById(bkknGzuStmi).value=" ";
        document.getElementById(bkknGzuFlpth).value=" ";
        // 2008/08/25 徐 新追加画像の時、画像削除の修正 Begin
        document.getElementById(gazuIsNew).value="";
        // 2008/08/25 徐 新追加画像の時、画像削除の修正 End
        // 2008/10/18 海浦隆一 SI1_BK_0185 BEGIN
        document.getElementById("file"+j).value=",,,";
        // 2008/10/18 海浦隆一 SI1_BK_0185 END
    }
}

//図面はらくらく登録の場合判定　徐凱　2008/08/19　END
//物件画像の追加と削除　END
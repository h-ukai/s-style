/*
 * 新規　2008/10/14 李文勇 SI1_BK_0540
 *
 * 改修履歴
 * PT_0064 平田 2008/10/29
 * SY_0011 劉宏博 2009/01/06
 *
*/
function openOptionNewWinSubmit (path, random, dtShri, bkknShbt) {

	var feature
	var pos;
	var width=800;
	var height=600;

	// 設備・条件 入力ガイド
    pos="width="+width+",height="+height+",left="+(window.screen.width-width)/2 + ",top="+(window.screen.height-height)/2;
   	feature =pos+",menubar=no,toolbar=no,location=no,"; 
	feature+="scrollbars=yes,resizable=yes,status=no,modal=yes";
	// 2008/08/13 田 PH3 BUG対応展開 Begin
	//PT_0064 平田 2008/10/29 START
	var newWin = window.open('/reins/blank.html', 'win', feature);
	//var newWin = window.open('', 'win', feature);
	//PT_0064 平田 2008/10/29 END
    // 2008/08/13 田 PH3 BUG対応展開 End
    newWin.document.write('<html>');
    newWin.document.write('<body>');
    newWin.document.write('<form id="Bkkn" name="BkknForm" action="');
    newWin.document.write(path);
    
    newWin.document.write('?r=');
    newWin.document.write(random);
    newWin.document.write('" method="post">');

    newWin.document.write('<input type="hidden" name="dtShri" value="');
    newWin.document.write(dtShri);
    newWin.document.write('" />');

    newWin.document.write('<input type="hidden" name="bkknShbt" value="');
    newWin.document.write(bkknShbt);
    newWin.document.write('"/>');
    
    newWin.document.write('<input type="hidden" name="optId" value="');
    newWin.document.write(document.forms[0].optId.value);
    newWin.document.write('"/>');
    
    newWin.document.write('</form>');
    newWin.document.write('</body>');
    newWin.document.write('</html>');
    var frm = newWin.document.getElementById('Bkkn');
    frm.submit();
    
    // 2008/08/13 田 PH3 BUG対応展開 Begin
    newWin.focus();
    // 2008/08/13 田 PH3 BUG対応展開 End

}

function showConfirm() {

  var temp = "重複する物件がありますが、登録しますか？";
//this.document.forms[0].tyofukuFlag.value = "1";
  var tyofukuFlag = document.getElementById("tyofukuFlag").value;
//alert(tyofukuFlag);

  if(1 == tyofukuFlag){
    if(confirm(temp)){
        document.forms[0].action = document.forms[0].contextPath.value + "/bkkn/BK000_013.do?r=" + document.forms[0].randomID.value;
	    // 2009/01/06 劉宏博 SY_0011 Begin
	    // document.forms[0].submit();
	    submitFirst();
	    // 2009/01/06 劉宏博 SY_0011 End
    } else {
    	document.forms[0].tyofukuFlag.value = "0";
    }

   }
   
  //return true;
  return false;
}
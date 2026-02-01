<!--

var set_key;
var set_string_width = 8;

function FollowList (set_memberID){
	$("#div_flist").show();
	$("#div_slist").show();
	$("#btn_slist").show();
	$("#div_mlist").hide();
	
	$("#tblfhead").empty();
	$("#tblfbody").empty();
	$("#tblf tfoot.nav").empty();
	
	$(".sortableHeader").removeClass('sortDesc').removeClass('sortAsc');
	
	// フォロー一覧を表示
    $.ajax({
        url: ajaxURL,
        dataType: "jsonp",
        type: "GET",
        data: {
			com: "getfol",
			memberID: set_memberID
		},
		success: function(rows) {
			$("#tblf tfoot.nav").append("<tr><td colspan=6><div class=pagination></div><div class=paginationTitle>Page</div><div class=selectPerPage></div><div class=status></div></td></tr>");
				
			$("#tblfhead").append($("<tr/>").attr("id","trl_h"));
			var val_h;
			var val_count = 0;
			var val_count_part = new Array();
			
			for (var j=0;j<flist.length;j++) {
				// 文字数を取得
				val_count_part[j] = strLength(flist[j]);
				
				if (flist[j] == "済") {
					val_h = "済み";
				}
				else if (flist[j] == "本文") {
					val_h = "メモ";
				}
				else {
					val_h = flist[j];
				}
				$("#trl_h").append($("<td/>").attr("id","tdl_h" + j).attr("sort",val_h).attr("bgcolor","#c9b7a1").text(val_h));
			}
			//テーブルとして表示するため、htmlを構築
			for (var i=0;i<rows.length;i++) {
				$("#tblfbody").append($("<tr/>").attr("id","trl" + i));
				var row = rows[i];
				for (var j=0;j<flist.length;j++) {
					// 文字数を取得
					var tmpString = strLength(row[flist[j]]);
					val_count_part[j] = (tmpString > val_count_part[j] ? tmpString : val_count_part[j]);
					
					if (flist[j] == "key") {
						$("#trl" + i).append($("<td/>").attr("class","tdl_keys").attr("bgcolor","#c9b7a1").attr("onclick","SelectFollow('"+row[flist[j]]+"', 'trl"+i+"');").text(row[flist[j]]));
					}
					else if (flist[j] == "済"){
						$("#trl" + i).append($("<td/>").attr("bgcolor","#ebe6e1").append("<input value=\""+row['key']+"\" type=\"checkbox\" onChange=\"FollowDone(this.value, this.checked)\""+(row[flist[j]] != "" ? " checked" : "")+">"));
					}
					else if (flist[j] == "アクション") {
						var action_flg = false;
						for (var app_i = 0; app_i < app_list.length; app_i ++) {
							if (row[flist[j]] == app_list[app_i]) {
								$("#trl" + i).append($("<td/>").attr("bgcolor","white").attr("id","tdl" + i)
									.attr("ondblclick","ModalDisplayText('addeditfol','"+row['key']+"','tdl"+i+"','kindname"+i+"',app_list,act_list);")
									.append($("<span/>").attr("id","kindname"+i).attr("class","resleft").text(row[flist[j]])));
								action_flg = true;
							}
						}
						if (!action_flg) {
							for (var act_i = 0; act_i < act_list.length; act_i ++) {
								if (row[flist[j]] == act_list[act_i]) {
									$("#trl" + i).append($("<td/>").attr("bgcolor","white").attr("id","tdl" + i)
										.attr("ondblclick","ModalDisplayText('addeditfol','"+row['key']+"','tdl"+i+"','kindname"+i+"',app_list,act_list);")
										.append($("<span/>").attr("id","kindname"+i).attr("class","resright").text(row[flist[j]])));
									action_flg = true;
								}
							}
							if (!action_flg && row[flist[j]]) {
								$("#trl" + i).append($("<td/>").attr("bgcolor","white").attr("id","tdl" + i)
									.attr("ondblclick","ModalDisplayText('addeditfol','"+row['key']+"','tdl"+i+"','kindname"+i+"',app_list,act_list);")
									.append($("<span/>").attr("id","kindname"+i).attr("class","reselse").text(row[flist[j]])));
								action_flg = true;
							}
							else if (!action_flg && !row[flist[j]]) {
								$("#trl" + i).append($("<td/>").attr("bgcolor","white").attr("id","tdl" + i)
									.attr("ondblclick","ModalDisplayText('addeditfol','"+row['key']+"','tdl"+i+"','kindname"+i+"',app_list,act_list);")
									.append($("<span/>").attr("id","kindname"+i).attr("class","reselse")));
							}
						}
					}
					else if (flist[j] == "本文") {
						if (row[flist[j]]) {
							$("#trl" + i).append($("<td/>").attr("id","body"+i).attr("class","modal").attr("bgcolor","white").attr("ondblclick","ModalDisplayTextarea('addeditfol','"+row['key']+"','','body"+i+"');").text(row[flist[j]]));
						}
						else {
							$("#trl" + i).append($("<td/>").attr("id","body"+i).attr("class","modal").attr("bgcolor","white").attr("ondblclick","ModalDisplayTextarea('addeditfol','"+row['key']+"','','body"+i+"');"));
						}
					}
					else if (flist[j] == "表題") {
						if (row[flist[j]]) {
							$("#trl" + i).append($("<td/>").attr("id","subject"+i).attr("bgcolor","white").attr("ondblclick","ModalDisplayText('addeditfol','subject','"+row['key']+"','subject"+i+"','','');").text(row[flist[j]]));
						}
						else {
							$("#trl" + i).append($("<td/>").attr("id","subject"+i).attr("bgcolor","white").attr("ondblclick","ModalDisplayText('addeditfol','subject','"+row['key']+"','subject"+i+"','','');"));
						}
					}
					else if (flist[j] == "予定日") {
						if (row[flist[j]]) {
							$("#trl" + i).append($("<td/>").attr("id","reservation"+i).attr("bgcolor","white").attr("ondblclick","ModalDisplayText('addeditfol','reservation','"+row['key']+"','reservation"+i+"','','');").text(row[flist[j]]));
						}
						else {
							$("#trl" + i).append($("<td/>").attr("id","reservation"+i).attr("bgcolor","white").attr("ondblclick","ModalDisplayText('addeditfol','reservation','"+row['key']+"','reservation"+i+"','','');"));
						}
					}
					else if (flist[j] == "予定終了日") {
						if (row[flist[j]]) {
							$("#trl" + i).append($("<td/>").attr("id","reservationend"+i).attr("bgcolor","white").attr("ondblclick","ModalDisplayText('addeditfol','reservationend','"+row['key']+"','reservationend"+i+"','','');").text(row[flist[j]]));
						}
						else {
							$("#trl" + i).append($("<td/>").attr("id","reservationend"+i).attr("bgcolor","white").attr("ondblclick","ModalDisplayText('addeditfol','reservationend','"+row['key']+"','reservationend"+i+"','','');"));
						}
					}
					else {
						if (row[flist[j]]) {
							$("#trl" + i).append($("<td/>").attr("bgcolor","white").text(row[flist[j]]));
						}
					}
				}
				
				// 表最後のkeyをセット
				set_key = rows[(rows.length - 1)]['key'];
				$('#tblf').jTPS();
				
/*
				$('#tblf tbody tr td.tdl_keys').live('click',
					function (e) {
						$('#tblf tbody').children('tr').children('td').removeClass('selectRow_follow');
						$(this).children('td').addClass('selectRow_follow');
					}
				);
*/
				$('#tblf tbody tr:not(.stubCell)').live('mouseover mouseout',
					function (e) {
						e.type == 'mouseover' ? $(this).children('td').addClass('hilightRow_follow') : $(this).children('td').removeClass('hilightRow_follow');
					}
				);
			}
			for (var j=0;j<val_count_part.length;j++) {
				$("#tdl_h" + j).attr("style","width: "+(val_count_part[j] * set_string_width)+"px;");
				val_count += val_count_part[j];
			}
			$("#tblf").attr("width",(val_count * set_string_width));
			// スクロール位置を一番下部にセット
			$("#div_flist").scrollTop(10000);
			// フォローに対応した物件一覧を表示
			ThingList (set_key);
		}
	});
}
function ThingList (set_follow_key){
	// データの読み込みかどうかの確認
	if (!reading_lists_flg) {
		reading_lists_flg = true;
		// 初期化
		$("#tblshead").empty();
		$("#tblsbody").empty();
		$("#tbls tfoot.nav").empty();
		$(".sortableHeader").removeClass('sortDesc').removeClass('sortAsc');
		set_key = set_follow_key;
		
		// フォローに対応した物件一覧を表示
	    $.ajax({
	        url: ajaxURL ,
	        dataType: "jsonp",
	        type: "GET",
	        data: {
				com: "getBKlistKey",
				key: set_follow_key
	        },
			success: function(rows) {
				$("#tbls tfoot.nav").append("<tr><td colspan=8><div class=pagination></div><div class=paginationTitle>Page</div><div class=selectPerPage></div><div class=status></div></td></tr>");
				
				$("#tblshead").append($("<tr/>").attr("id","trs_h"));
				var val_h;
				var val_count = 0;
				var val_count_part = new Array();
				
				val_count += 1;
				$("#trs_h").append($("<td/>").attr("id","tds_h-1").attr("sort"," ").attr("bgcolor","#c9b7a1"));
				for (var j=0;j<slist.length;j++) {
					// 文字数を取得
					val_count_part[j] = strLength(slist[j]);
					$("#trs_h").append($("<td/>").attr("id","tds_h" + j).attr("sort",slist[j]).attr("bgcolor","#c9b7a1").text(slist[j]));
				}
			
				var row1;
				var row2;
	            //テーブルとして表示するため、htmlを構築
				for (var i=0;i<rows.length;i++) {
					$.each(rows[i], function(i_0){
						if (i_0 == "物件") {
							row1 = rows[i][i_0];
						}
						else if (i_0 == "情報") {
							row2 = rows[i][i_0];
						}
					});
					if (row1 != null) {
						$("#tblsbody").append($("<tr/>").attr("id","trs" + i));
						$("#trs" + i).append($("<td/>").attr("bgcolor","#c9b7a1").append("<input name=\"thingCheck\" value=\""+row1['物件番号']+"\" type=\"checkbox\">"));
						for (var j=0;j<slist.length;j++) {
							
							if (slist[j] == "物件番号"){
								$("#trs" + i).append($("<td/>").attr("bgcolor","#ebe6e1").attr("onclick","ThingCall('"+row1[slist[j]]+"');").text(row1[slist[j]]));
								// 文字数を取得
								var tmpString = strLength(row1[slist[j]]);
								val_count_part[j] = (tmpString > val_count_part[j] ? tmpString : val_count_part[j]);
							}
							else if (slist[j] == "作成状況"){
								if (row1[slist[j]] != null && row1[slist[j]] != "") {
									$("#trs" + i).append($("<td/>").attr("bgcolor","white").text(row1[slist[j]]));
									// 文字数を取得
									var tmpString = strLength(row1[slist[j]]);
									val_count_part[j] = (tmpString > val_count_part[j] ? tmpString : val_count_part[j]);
								}
								else {
									$("#trs" + i).append($("<td/>").attr("bgcolor","white"));
								}
							}
							else if (slist[j] == "メモ") {
								if (row2[slist[j]] != null && row2[slist[j]] != "") {
									$("#trs" + i).append($("<td/>").attr("id","memo"+i).attr("bgcolor","white").attr("ondblclick","ModalDisplayTextarea('addeditBKlist','"+set_follow_key+"','"+rows[i]['key']+"','memo"+i+"');").text(row2[slist[j]]));
									// 文字数を取得
									var tmpString = strLength(row2[slist[j]]);
									val_count_part[j] = (tmpString > val_count_part[j] ? tmpString : val_count_part[j]);
								}
								else {
									$("#trs" + i).append($("<td/>").attr("id","memo"+i).attr("bgcolor","white").attr("ondblclick","ModalDisplayTextarea('addeditBKlist','"+set_follow_key+"','"+rows[i]['key']+"','memo"+i+"');"));
								}
							}
							else if (slist[j] == "送信済"){
								if (row2[slist[j]] != null && row2[slist[j]] != "") {
									$("#trs" + i).append($("<td/>").attr("bgcolor","white").append("<input id=\"send"+i+"\" value=\""+row2[slist[j]]+"\" type=\"checkbox\" onChange=\"ThingSend('"+ set_follow_key +"', '"+ rows[i]['key'] +"', this.checked, "+i+")\" checked>"));
									// 文字数を取得
									var tmpString = strLength(row2[slist[j]]);
									val_count_part[j] = (tmpString > val_count_part[j] ? tmpString : val_count_part[j]);
								}
								else {
									$("#trs" + i).append($("<td/>").attr("bgcolor","white").append("<input id=\"send"+i+"\" value=\""+row2[slist[j]]+"\" type=\"checkbox\" onChange=\"ThingSend('"+ set_follow_key +"', '"+ rows[i]['key'] +"', this.checked, "+i+")\">"));
								}
							}
							else if (slist[j] == "送信日時") {
								if (row2[slist[j]] != null && row2[slist[j]] != "") {
									$("#trs" + i).append($("<td/>").attr("id","senddate"+i).attr("bgcolor","white").attr("ondblclick","ModalDisplayText('addeditBKlist','"+set_follow_key+"','"+rows[i]['key']+"','senddate"+i+"','"+i+"','');").text(row2[slist[j]]));
									// 文字数を取得
									var tmpString = strLength(row2[slist[j]]);
									val_count_part[j] = (tmpString > val_count_part[j] ? tmpString : val_count_part[j]);
								}
								else {
									$("#trs" + i).append($("<td/>").attr("id","senddate"+i).attr("bgcolor","white").attr("ondblclick","ModalDisplayText('addeditBKlist','"+set_follow_key+"','"+rows[i]['key']+"','senddate"+i+"','"+i+"','');"));
								}
							}
							else {
								if (row1[slist[j]] != null && row1[slist[j]] != "") {
									$("#trs" + i).append($("<td/>").attr("bgcolor","white").text(row1[slist[j]]));
									// 文字数を取得
									var tmpString = strLength(row1[slist[j]]);
									val_count_part[j] = (tmpString > val_count_part[j] ? tmpString : val_count_part[j]);
								}
								else if (row2[slist[j]] != null && row2[slist[j]] != "") {
									$("#trs" + i).append($("<td/>").attr("bgcolor","white").text(row2[slist[j]]));
									// 文字数を取得
									var tmpString = strLength(row2[slist[j]]);
									val_count_part[j] = (tmpString > val_count_part[j] ? tmpString : val_count_part[j]);
								}
								else {
									$("#trs" + i).append($("<td/>").attr("bgcolor","white"));
								}
							}
						}
					}
					$('#tbls').jTPS();
					$('#tbls tbody tr:not(.stubCell)').live('mouseover mouseout',
						function (e) {
							e.type == 'mouseover' ? $(this).children('td').addClass('hilightRow_follow') : $(this).children('td').removeClass('hilightRow_follow');
						}
					);
				}
				$("#tds_h-1").attr("style","width: "+(2 * set_string_width)+"px;");
				val_count += 2;
				for (var j=0;j<val_count_part.length;j++) {
					$("#tds_h" + j).attr("style","width: "+(val_count_part[j] * set_string_width)+"px;");
					val_count += val_count_part[j];
				}
				$("#tbls").attr("width",(val_count * set_string_width));
				$("#div_slist").scrollTop(0);
				reading_lists_flg = false;
			}
		});
	}
}
function MemberList (set_tantoID, set_action, set_date){
	// データの読み込みかどうかの確認
	if (!reading_listm_flg) {
		reading_listm_flg = true;
		// 初期化
		$("#div_flist").hide();
		$("#div_slist").hide();
		$("#btn_slist").hide();
		$("#div_mlist").show();
	
		// 初期化
		$("#tblmhead").empty();
		$("#tblmbody").empty();
		$(".sortableHeader").removeClass('sortDesc').removeClass('sortAsc');
		if (set_action == undefined) set_action = "";
		if (set_date == undefined) set_date = "";
		// 顧客一覧を表示
	    $.ajax({
	        url: ajaxURL ,
	        dataType: "jsonp",
	        type: "GET",
	        data: {
				com: "getmemAction",
				action: set_action,
				tantoID: set_tantoID,
				datetime: set_date
	        },
			success: function(rows) {
				$("#tblmhead").append($("<tr/>").attr("id","trm_h"));
				var val_h;
				for (var j=0;j<mlist.length;j++) {
					if (mlist[j] == "メンバーID") {
						val_h = "顧客番号";
					}
					else if (mlist[j] == "氏名") {
						val_h = "顧客名";
					}
					else if (mlist[j] == "電話") {
						val_h = "電話番号";
					}
					else if (mlist[j] == "FAX") {
						val_h = "FAX番号";
					}
					else {
						val_h = mlist[j];
					}
				
					$("#trm_h").append($("<td/>").attr("sort",val_h).attr("bgcolor","#c9b7a1").text(val_h));
				}
	            //テーブルとして表示するため、htmlを構築
				for (var i=0;i<rows.length;i++) {
					$("#tblmbody").append($("<tr/>").attr("id","trm" + i));
					var row = rows[i];
					for (var j=0;j<mlist.length;j++) {
						if(row[mlist[j]]!=null){
							if (mlist[j] == "メンバーID") {
								$("#trm" + i).append($("<td/>").attr("bgcolor","#c9b7a1").attr("onclick","FollowCall('"+row[mlist[j]]+"');").text(row[mlist[j]]));
							}
							else {
								$("#trm" + i).append($("<td/>").attr("bgcolor","white").text(row[mlist[j]]));
							}
						}
						else
						{
							$("#trm" + i).append($("<td/>").attr("bgcolor","white").text(""));
						}
					}
					// 表最後のkeyをセット
					$('#tblm').jTPS();
					$('#tblm tbody tr:not(.stubCell)').live('mouseover mouseout',
						function (e) {
							e.type == 'mouseover' ? $(this).children('td').addClass('hilightRow_follow') : $(this).children('td').removeClass('hilightRow_follow');
						}
					);
				}
				reading_listm_flg = false;
			}
		});
	}
}

//物件番号をクリックした場合
function ThingCall(bkID) {
	document.location = bkeditFile + bkID;
}

//顧客IDをクリックした場合
function FollowCall(memberID) {
	document.location = followFile + memberID;
}

function CalList (set_memberID){
	// データの読み込みかどうかの確認
	if (!reading_calendar_flg) {
		reading_calendar_flg = true;
		// 初期化
		DD = new Date();
		thisMonth = (DD.getYear() < 2000 ? (DD.getYear() + 1900) : DD.getYear()) +"/"+ (DD.getMonth() + 1);
		$("#tblcbody").empty();
		$(".sortableHeader").removeClass('sortDesc').removeClass('sortAsc');
		// カレンダーを表示
	    $.ajax({
	        url: ajaxURL ,
	        dataType: "jsonp",
	        type: "GET",
	        data: {
				com: "getcal",
				tantoID: set_memberID,
				yearmonth: thisMonth
	        },
			success: function(rows) {
	            //テーブルとして表示するため、htmlを構築
				for (var i = 0, j = -1, i_1 = 0; i < rows.length; i ++, j ++) {
	//				$("#tblcbody").append($("<tr/>").attr("id","trc" + i_1));
					if (i == 0 || (i < rows.length && (rows[i]['日付'].replace(/[0-9]{4}\/([0-9]{2})\/[0-9]{2}/,'$1') != rows[j]['日付'].replace(/[0-9]{4}\/([0-9]{2})\/[0-9]{2}/,'$1')))) {
						$("#tblcbody").append($("<tr/>").attr("id","trc" + i_1));
						if (i == 0) {
							$("#trc" + i_1).append($("<th>").attr("id","day").attr("align","left").attr("bgcolor","white").text(rows[i]['日付'].replace(/[0-9]{4}\/[0]{0,1}([1-9]{1,2}[0]{0,1})\/[0-9]{2}/,'$1月')));
						}
						else {
							$("#trc" + i_1).append($("<th>").attr("id","day").attr("align","left").attr("bgcolor","white").text(rows[i]['日付'].replace(/[0-9]{4}\/[0]{0,1}([1-9]{1,2}[0]{0,1})\/[0-9]{2}/,'$1月')));
						}
						i_1 ++;
					}
					$("#tblcbody").append($("<tr/>").attr("id","trc" + i_1));
					var day = rows[i]['日付'].replace(/[0-9]{4}\/[0-9]{2}\/[0]{0,1}([1-9]{1,2}[0]{0,1})/,'$1');
					if (day.length == 2) {
						$("#trc" + i_1).append($("<th>").attr("id","day").attr("bgcolor","white")
							.text("　" + day + "日（" + rows[i]['曜日'] + "）" + "　　" + rows[i]['六曜']));
					}
					else {
						$("#trc" + i_1).append($("<th>").attr("id","day").attr("bgcolor","white")
							.text("　 " + day + "日（" + rows[i]['曜日'] + "）" + "　　" + rows[i]['六曜']));
					}
					i_1 ++;
				
					var countCheck;
					var i_3 = 0;
					var actionListValue = new Array();
					var actionListCount = new Array();
					var actionDate;
				
					$.each(rows[i]['予定'], function(i_2){
						countCheck = rows[i]['予定'][i_2]['アクション'];
						if (i_3 == 0) {
							actionListValue[i_3] = countCheck;
							actionListCount[i_3] = 1;
							i_3 ++;
						}
						else if (jQuery.inArray (countCheck, actionListValue) >= 0) {
							actionListCount[jQuery.inArray (countCheck, actionListValue)] = actionListCount[jQuery.inArray (countCheck, actionListValue)] + 1;
						}
						else {
							actionListValue[i_3] = countCheck;
							actionListCount[i_3] = 1;
							i_3 ++;
						}
					});
				
					//現在日付取得
					actionDate = rows[i]['日付'];
					for (i_4 = 0; i_4 < actionListValue.length; i_4 ++) {
						action_key = actionListValue[i_4];
						if (actionListCount[i_4] > 1) {
							actionListValue[i_4] = actionListValue[i_4] + "（" + actionListCount[i_4] + "）";
						}
						$("#tblcbody").append($("<tr/>").attr("id","trc" + i_1));
	//					$("#trc" + i_1).append($("<td>").attr("id","day").attr("bgcolor","white").attr("onclick","MemberList('"+set_tantoID+"','"+action_key+"','"+actionDate+"')").text("　　・" + actionListValue[i_4]));
						$("#trc" + i_1).append($("<td>").attr("id","day").attr("bgcolor","white").attr("onclick","MemberList('"+set_tantoID+"','"+action_key+"')").text("　　・" + actionListValue[i_4]));
						i_1 ++;
					}
					$('#tblc').jTPS({perPages:['ALL']});
					$('#tblc tbody tr:not(.stubCell)').live('mouseover mouseout',
						function (e) {
							e.type == 'mouseover' ? $(this).children('td').addClass('hilightRow_follow') : $(this).children('td').removeClass('hilightRow_follow');
						}
					);
				}
				reading_calendar_flg = false;
			}
		});
	}
}

function StillList (set_tantoID){
	// データの読み込みかどうかの確認
	if (!reading_still_flg) {
		reading_still_flg = true;
		// 初期化
		DD = new Date();
		thisMonth = (DD.getYear() < 2000 ? (DD.getYear() + 1900) : DD.getYear()) +"/"+ (DD.getMonth() + 1);
		$("#still").empty();
		// 未フォロー情報を表示
	    $.ajax({
	        url: ajaxURL ,
	        dataType: "jsonp",
	        type: "GET",
	        data: {
				com: "getaction",
				tantoID: set_tantoID,
				yearmonth: thisMonth
	        },
			success: function(rows) {
	            //テーブルとして表示するため、htmlを構築
				$.each(rows, function(i) {
					$("#still").append($("<li>").append($("<a>").attr("href","#").attr("onclick","MemberList('"+set_tantoID+"','"+i+"')").text(i + "（" + rows[i] + "）")));
				});
				reading_still_flg = false;
			}
		});
	}
}

function bkIDExists (set_follow_key,set_bk_key){
	
	var returnVal = false;
	
    $.ajax({
        url: ajaxURL,
        dataType: "jsonp",
        type: "GET",
        data: {
			com: "getBKlistKey",
			key: set_follow_key
        },
		success: function(rows) {
            //テーブルとして表示するため、htmlを構築
			for (var i=0;i<rows.length;i++) {
				$.each(rows[i], function(i_1){
					if (i_1 == "物件") {
						if (rows[i][i_1] != null && rows[i][i_1]['物件番号'] == set_bk_key) {
							returnVal = 1;
						}
					}
				});
			}
			if (returnVal != 1) {
				returnVal = -1;
			}
		}
	});
	
	return (returnVal);
}


function FollowDone(key_val, done_val) {
	$.ajax({
		url: ajaxURL,
        dataType: "jsonp",
        type: "POST",
		data: {
			com  : "addeditfol",
			key  : key_val,
			done : done_val
		}
	});
}

function ThingSend(key_val, bk_id, send_val, i) {
	
	var thisDatetime;
	if (send_val) {
		thisDatetime = getDatetime();
		$.ajax({
			url: ajaxURL,
	        dataType: "jsonp",
	        type: "POST",
			data: {
				com       : "addeditBKlist",
				meskey    : key_val,
				bklistkey : bk_id,
				send      : send_val,
				senddate  : thisDatetime
			}
		});
	}
	else {
		$.ajax({
			url: ajaxURL,
	        dataType: "jsonp",
	        type: "POST",
			data: {
				com       : "addeditBKlist",
				meskey    : key_val,
				bklistkey : bk_id,
				send      : send_val
			}
		});
	}
	document.getElementById("senddate" + i).innerHTML = (send_val ? thisDatetime : "");
}

function ThingDelete(key_val) {
	
	var bk_list_val = "";
	
	//チェックされたチェックボックスの値のリスト
	bk_list_val += $("input[name='thingCheck']:checked").map( function() {
		return $(this).val();
	}).get().join(",");
	
	$.ajax({
		url: ajaxURL,
        dataType: "jsonp",
        type: "POST",
		data: {
			com       : "removeBK",
			key       : key_val,
			bkID      : bk_list_val
		},
		success: function(data) {
			ThingList (key_val);
		}
	});
}

function FollowInsert (FollowDone_val, FollowKindname_val, FollowSubject_val, FollowBody_val, FollowReservation_val, FollowReservationend_val,FollowMailto) {
	
	$("#trmf7").empty();
	$("#overThingInputLayer").css({height:280});
	
	var followIDCheck = false;
	
	$.ajax({
		url: ajaxURL,
		dataType: "jsonp",
		type: "POST",
		data: {
			com            : "addeditfol",
			memfrom        : set_memberID,
			done           : FollowDone_val,
			kindname       : FollowKindname_val,
			subject        : FollowSubject_val,
			body           : FollowBody_val,
			reservation    : FollowReservation_val,
			reservationend : FollowReservationend_val,
			mailto         : FollowMailto
		},
		success: function(data) {
			FollowList (set_memberID);
			// カレンダーを表示
			CalList (set_tantoID);
			// 未フォローを表示
			StillList (set_tantoID);
			
			$("#glayLayer").hide();
			$("#overFollowInputLayer").hide();
		}
	});

/*
		$.ajax({
			url: ajaxURL,
			dataType: "jsonp",
			type: "GET",
			data: {
				com: "getfol",
				memberID: set_memberID
			},
			success: function(rows) {
				//テーブルとして表示するため、htmlを構築
				for (var i=0;i<rows.length;i++) {
					if (rows[i]['key'] == FollowID_val) {
						followIDCheck = true;
					}
				}
				if (!followIDCheck) {
					$.ajax({
						url: ajaxURL,
						dataType: "jsonp",
						type: "POST",
						data: {
							com            : "addeditfol",
							memfrom        : set_memberID,
							done           : FollowDone_val,
							kindname       : FollowKindname_val,
							subject        : FollowSubject_val,
							body           : FollowBody_val,
							reservation    : FollowReservation_val,
							reservationend : FollowReservationend_val
						},
						success: function(data) {
							FollowList (set_memberID);
						}
					});
				}
			}
		});
		$("#glayLayer").hide();
		$("#overThingInputLayer").hide();
*/
/*		if ($("#tdmf7").size() == 0) {
			$("#tblmf").append($("<tr/>").attr("id","trmf7"));
			$("#trmf7").append($("<td/>").attr("id","tdmf7").attr("colspan","4").attr("align","center"));
			$("#tdmf7").append($("<font>").attr("color","#FF0000").text("入力内容を確認して下さい"));
			$("#overThingInputLayer").css({height:300});
		}
*/
}

function BkInsert (set_follow_key, input_bkID_val, input_memo_val, input_send_val) {
	
	$("#trmt4").empty();
	$("#overThingInputLayer").css({height:180});
	
	var bkIDCheck;
	
	if (
		!isNaN(input_bkID_val) &&
		input_bkID_val != ""
	) {
		
		var bkIDCheck = false;
	
		$.ajax({
			url: ajaxURL,
			dataType: "jsonp",
			type: "GET",
			data: {
				com: "getBKlistKey",
				key: set_follow_key
			},
			success: function(rows) {
				//テーブルとして表示するため、htmlを構築
				for (var i=0;i<rows.length;i++) {
					$.each(rows[i], function(i_1){
						if (i_1 == "物件") {
							if (rows[i][i_1] != null && rows[i][i_1]['物件番号'] == input_bkID_val) {
								bkIDCheck = true;
							}
						}
					});
				}
				if (!bkIDCheck) {
					$.ajax({
						url: ajaxURL,
						dataType: "jsonp",
						type: "POST",
						data: {
							com    : "addeditBKlist",
							meskey : set_follow_key,
							bkID   : input_bkID_val,
							memo   : input_memo_val,
							send   : input_send_val
				
						},
						success: function(data) {
							ThingList (set_follow_key);
						}
					});
				}
			}
		});
		$("#glayLayer").hide();
		$("#overThingInputLayer").hide();
	}
	else {
		if ($("#tdmt4").size() == 0) {
			$("#tblmt").append($("<tr/>").attr("id","trmt4"));
			$("#trmt4").append($("<td/>").attr("id","tdmt4").attr("colspan","2").attr("align","center"));
			$("#tdmt4").append($("<font>").attr("color","#FF0000").text("入力内容を確認して下さい"));
			$("#overThingInputLayer").css({height:200});
		}
	}
}

// 更新処理（フォローコメント）
function FollowBody (com, key, new_body, id) {
	objtoedit = document.getElementById(id);
	old_body = objtoedit.innerHTML;
	objtoedit.innerHTML="Saving.....";
	
	$.ajax({
		url: ajaxURL,
        dataType: "jsonp",
        type: "POST",
		data: {
			com  : com,
			key  : key,
			body : new_body
		},
		error: objtoedit.innerHTML=old_body,
		success: objtoedit.innerHTML=new_body
	});
}
// 更新処理（フォローアクション）
function FollowKindname (com, key, new_body, spanId, id, set_tantoID, app_list, act_list) {
	objtoedit = document.getElementById(id);
	old_body = objtoedit.innerHTML;
	objtoedit.innerHTML="Saving.....";
	
	$.ajax({
		url: ajaxURL,
        dataType: "jsonp",
        type: "POST",
		data: {
			com  : com,
			key  : key,
			kindname : new_body
		},
		error: objtoedit.innerHTML=old_body,
		success: function(data){
			var action_flg = false;
			$("#"+spanId).empty();
			for (var app_i = 0; app_i < app_list.length; app_i ++) {
				if (new_body == app_list[app_i]) {
					$("#" + spanId).append($("<span/>").attr("id",id).attr("class","resleft").text(new_body));
					action_flg = true;
				}
			}
			if (!action_flg) {
				for (var act_i = 0; act_i < act_list.length; act_i ++) {
					if (new_body == act_list[act_i]) {
						$("#" + spanId).append($("<span/>").attr("id",id).attr("class","resright").text(new_body));
						action_flg = true;
					}
				}
				if (!action_flg) {
					$("#" + spanId).append($("<span/>").attr("id",id).attr("class","reselse").text(new_body));
					action_flg = true;
				}
			}
			// カレンダーを表示
			$("#tblcbody").empty();
			CalList (set_tantoID);
			// 未フォローを表示
			$("#still").empty();
			StillList (set_tantoID);
		}
	});
}
// 更新処理（フォロー表題）
function FollowSubject (com, key, new_body, id, set_tantoID) {
	objtoedit = document.getElementById(id);
	old_body = objtoedit.innerHTML;
	objtoedit.innerHTML="Saving.....";
	
	$.ajax({
		url: ajaxURL,
        dataType: "jsonp",
        type: "POST",
		data: {
			com  : com,
			key  : key,
			subject : new_body
		},
		error: objtoedit.innerHTML=old_body,
		success: objtoedit.innerHTML=new_body
	});
}
// 更新処理（フォロー予定日）
function FollowReservation (com, key, new_body, id, set_tantoID) {
	objtoedit = document.getElementById(id);
	old_body = objtoedit.innerHTML;
	objtoedit.innerHTML="Saving.....";
	
	$.ajax({
		url: ajaxURL,
        dataType: "jsonp",
        type: "POST",
		data: {
			com  : com,
			key  : key,
			reservation : new_body
		},
		error: objtoedit.innerHTML=old_body,
		success: function(data){
			objtoedit.innerHTML=new_body;
			// カレンダーを表示
			$("#tblcbody").empty();
			CalList (set_tantoID);
			// 未フォローを表示
			$("#still").empty();
			StillList (set_tantoID);
		}
	});
}
// 更新処理（フォロー予定終了日）
function FollowReservationend (com, key, new_body, id, set_tantoID) {
	objtoedit = document.getElementById(id);
	old_body = objtoedit.innerHTML;
	objtoedit.innerHTML="Saving.....";
	
	$.ajax({
		url: ajaxURL,
        dataType: "jsonp",
        type: "POST",
		data: {
			com  : com,
			key  : key,
			reservationend : new_body
		},
		error: objtoedit.innerHTML=old_body,
		success: objtoedit.innerHTML=new_body
	});
}
// 更新処理（物件送信日時）
function BKSenddate (com, key, sub_key, new_body, id, i) {
	objtoedit = document.getElementById(id);
	var old_body = objtoedit.innerHTML;
	objtoedit.innerHTML="Saving.....";
	
	if (new_body != "") {
		$.ajax({
			url: ajaxURL,
	        dataType: "jsonp",
	        type: "POST",
			data: {
				com       : com,
				meskey    : key,
				bklistkey : sub_key,
				send      : true,
				senddate  : new_body
			},
			error: objtoedit.innerHTML=old_body,
			success: objtoedit.innerHTML=new_body
		});
		document.getElementById("send" + i).checked = true;
	}
	else {
		$.ajax({
			url: ajaxURL,
	        dataType: "jsonp",
	        type: "POST",
			data: {
				com       : com,
				meskey    : key,
				bklistkey : sub_key,
				send      : false
			},
			error: objtoedit.innerHTML=old_body,
			success: objtoedit.innerHTML=new_body
		});
		document.getElementById("send" + i).checked = false;
	}
}
// 更新処理（物件メモ）
function BkMemo (com, key, sub_key, new_body, id) {
	objtoedit = document.getElementById(id);
	var old_body = objtoedit.innerHTML;
	objtoedit.innerHTML="Saving.....";
	
	$.ajax({
		url: ajaxURL,
        dataType: "jsonp",
        type: "POST",
		data: {
			com       : com,
			meskey    : key,
			bklistkey : sub_key,
			memo      : new_body
		},
		error: objtoedit.innerHTML=old_body,
		success: objtoedit.innerHTML=new_body
	});
}
// フォローkey選択
function SelectFollow (id, tr_id) {
	$('#tblf tbody').children('tr').children('td').removeClass('selectRow_follow');
	$('#'+tr_id).children('td').addClass('selectRow_follow');
	ThingList(id);
}

// 現在の日時を取得
function getDatetime () {
	var DD = new Date();
	var year = (DD.getYear() < 2000 ? (DD.getYear() + 1900) : DD.getYear());
	var month = ((DD.getMonth() + 1) < 10 ? "0" + (DD.getMonth() + 1) : (DD.getMonth() + 1));
	var date = (DD.getDate() < 10 ? "0" + DD.getDate() : DD.getDate());
	var hours = (DD.getHours() < 10 ? "0" + DD.getHours() : DD.getHours());
	var minutes = (DD.getMinutes() < 10 ? "0" + DD.getMinutes() : DD.getMinutes());
	var seconds = (DD.getSeconds() < 10 ? "0" + DD.getSeconds() : DD.getSeconds());
	
	var strDate = year + "/" + month + "/" + date + " " + hours + ":" + minutes + ":" + seconds;
	
	return strDate;
}
// 文字数カウント
function strLength(strSrc){
	len = 0;
	strSrc = escape(strSrc);
	for(i = 0; i < strSrc.length; i++, len++){
		if(strSrc.charAt(i) == "%"){
			if(strSrc.charAt(++i) == "u"){
				i += 3;
				len++;
			}
			i++;
		}
	}
	return len;
}
//-->
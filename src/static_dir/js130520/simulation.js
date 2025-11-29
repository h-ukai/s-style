//simulation.js
//返済額を計算する
function CalcRepaymentMoney()
{
	var msg = "";
	var Debt_Money;
	var RepaymentCount;
	var Month_Rate;
	var Bonus_Rate;
	var Paymentmonthlysum=0;
	var PaymentBonus=0;
	var Paymentnensum=0;
	var bonus;

	//返済額フィールドクリア
	$("#txt_repayment_everymonth").val('');
	$("#txt_repayment_bonus").val('');
	$("#txt_repayment_year").val('');
	
	//入力チェック
	if($("#txt_debtmoney").val().length == 0) {
		msg = msg + "借入金額が未入力です。\n";
	} else if(isNaN($("#txt_debtmoney").val())) {
		msg = msg + "借入金額は半角数値で入力してください。\n";
	} else if($("#txt_debtmoney").val() <= 0) {
		msg += "借入金額を正しく入力して下さい。\n";
	}

	if($("#txt_rate").val().length == 0) {
		msg = msg + "金利が未入力です。\n";
	} else if(isNaN($("#txt_rate").val())) {
		msg = msg + "金利は半角数値で入力してください。\n";
	} else if($("#txt_rate").val() < 0) {
		msg += "金利は0以上の値を入力して下さい。\n";
	}

	if($("#txt_kikan").val().length == 0) {
		msg = msg + "借入期間が未入力です。\n";
	} else if(isNaN($("#txt_kikan").val())) {
		msg = msg + "借入期間は半角数値で入力してください。\n";
	} else if($("#txt_kikan").val() < 0) {
		msg += "借入期間は0以上の整数で入力して下さい。\n";
	}

	if(isNaN($("#txt_bonus").val())) {
		msg = msg + "内ボーナス返済分は半角数値で入力してください。\n";
	} else if($("#txt_bonus").val() < 0) {
		msg += "内ボーナス返済分は0以上の整数で入力して下さい。\n";
	}

	if(msg != ""){	// 入力内容に問題があったら
		alert(msg);
		return;
	} else {
		Debt_Money = parseFloat($("#txt_debtmoney").val()) * 10000;
		if($("#txt_bonus").val().length == 0){
			bonus = 0;
			$("#txt_bonus").val('0');
		}else{
			bonus = parseFloat($("#txt_bonus").val()) * 10000;
		}

		Month_Rate = parseFloat($("#txt_rate").val()) / 100 / 12;
		Bonus_Rate = parseFloat($("#txt_rate").val()) / 100 / 2;
		RepaymentCount = parseFloat($("#txt_kikan").val())*12;
		
		//毎月返済額計算(対象額=(借入金額-ボーナス返済額))
		Paymentmonthlysum = parseInt((Debt_Money - bonus) * Month_Rate * Math.pow((1 + Month_Rate),RepaymentCount) / (Math.pow((1 + Month_Rate),RepaymentCount) - 1));
		//ボーナス返済額(1回分)計算
		if(bonus > 0){
			PaymentBonus = parseInt(bonus * Bonus_Rate * Math.pow((1 + Bonus_Rate),RepaymentCount/6) / (Math.pow((1 + Bonus_Rate),RepaymentCount/6) - 1));
		}else{
			PaymentBonus=0;
		}
		//年間返済額
		Paymentnensum = Paymentmonthlysum * 12 + PaymentBonus * 2;
		
		$("#txt_repayment_everymonth").val(number_format(Paymentmonthlysum));
		$("#txt_repayment_bonus").val(number_format(PaymentBonus));
		$("#txt_repayment_year").val(number_format(parseInt(Paymentnensum/10000)));
		
		//計算エラーの時の処理
		if ( $("#txt_repayment_everymonth").val() == "NaN" || $("#txt_repayment_everymonth").val() <= 0){
			$("#txt_repayment_everymonth").val('0');
		}
		if ( $("#txt_repayment_bonus").val() == "NaN" || $("#txt_repayment_bonus").val() <= 0 ){
			$("#txt_repayment_bonus").val('0');
		}
		if ( $("#txt_repayment_year").val() == "NaN" || $("#txt_repayment_year").val() <= 0 ){
			$("#txt_repayment_year").val('0');
		}
	}
}



//計算した返済額を残元金計算フォームに設定
function set_calc(){
	if($("#txt_repayment_everymonth").val() == "" || ($("#txt_repayment_year").val() != "" && $("#txt_repayment_year").val() < 0)){
		alert("計算結果が不正です");
		return;
	} else {
		$("#txt_debtmoney2").val($("#txt_debtmoney").val());
		$("#txt_bonus2").val($("#txt_bonus").val());
		$("#txt_rate2").val($("#txt_rate").val());
		$("#txt_kikan2").val($("#txt_kikan").val());
		alert("「残元金計算期間」を入力後、「計算する」ボタンを押してください");
		$("#txt_zankikan_end").focus();
	}
}

//残元金を計算する
function CalcZanRepaymentMoney(){
	
	var msg = "";
	var Debt_Money;
	var RepaymentCount;
	var Month_Rate;
	var Bonus_Rate;
	var ZanRepaymentMoney=0;
	var Paymentmonthlysum=0;
	var PaymentBonus=0;
	var Paymentnensum=0;
	var bonus;
	var endpayY;
	var endpayM;
	var endpyakikan=0;
	
	//残元金、支払済金額フィールドクリア
	$("#txt_repayment_zangaku").val("");
	$("#txt_repayment_everymonth2").val("");
	$("#txt_repayment_bonus2").val("");
	$("#txt_repayment_year2").val("");
	
	//入力チェック
	if($("#txt_debtmoney2").val().length == 0) {
		msg = msg + "借入金額が未入力です。\n";
	} else if(isNaN($("#txt_debtmoney2").val())) {
		msg = msg + "借入金額は半角数値で入力してください。\n";
	} else if($("#txt_debtmoney2").val() <= 0) {
		msg += "借入金額を正しく入力して下さい。\n";
	}

	if($("#txt_rate2").val().length == 0) {
		msg = msg + "金利が未入力です。\n";
	} else if(isNaN($("#txt_rate2").val())) {
		msg = msg + "金利は半角数値で入力してください。\n";
	} else if($("#txt_rate2").val() < 0) {
		msg += "金利は0以上の値を入力して下さい。\n";
	}

	if($("#txt_kikan2").val().length == 0) {
		msg = msg + "借入期間が未入力です。\n";
	} else if(isNaN($("#txt_kikan2").val())) {
		msg = msg + "借入期間は半角数値で入力してください。\n";
	} else if($("#txt_kikan2").val() < 0) {
		msg += "借入期間は0以上の整数で入力して下さい。\n";
	}

	if(isNaN($("#txt_bonus2").val())) {
		msg = msg + "内ボーナス返済分は半角数値で入力してください。\n";
	} else if($("#txt_bonus2").val() < 0) {
		msg += "内ボーナス返済分は0以上の整数で入力して下さい。\n";
	}

	if($("#txt_zankikan_end").val().length == 0 || $("#txt_zankikan_end2").val().length == 0){
		msg = msg + "残元金計算期間が未入力です。\n";
	} else if(isNaN($("#txt_zankikan_end").val()) || isNaN($("#txt_zankikan_end2").val())){
		msg = msg + "残元金計算期間は半角数値で入力してください。\n";
	}

	
	if(msg!=""){// 入力内容に問題があったら
		alert(msg);
		return;
	} else {
		Debt_Money = parseFloat($("#txt_debtmoney2").val()) * 10000;
		if($("#txt_bonus2").val().length == 0){
			bonus=0;
			$("#txt_bonus2").val('0');
		}else{
			bonus=parseFloat($("#txt_bonus2").val()) * 10000;
		}
		Month_Rate = parseFloat($("#txt_rate2").val()) / 100 / 12;
		Bonus_Rate = parseFloat($("#txt_rate2").val()) / 100 / 2;
		RepaymentCount = parseFloat($("#txt_kikan2").val())*12;
		if($("#txt_zankikan_end").val().length == 0){
			endpayY = 0;
		}else{
			endpayY =parseFloat($("#txt_zankikan_end").val()) * 12;
		}
		if($("#txt_zankikan_end2").val().length){
			endpayM = 0;
		}else{
			endpayM =parseFloat($("#txt_zankikan_end2").val());
		}
		endpyakikan = endpayY + endpayM;
		
		//毎月返済額計算(対象額=(借入金額-ボーナス返済額))
		Paymentmonthlysum = parseInt((Debt_Money - bonus) * Month_Rate * Math.pow((1 + Month_Rate),RepaymentCount) / (Math.pow((1 + Month_Rate),RepaymentCount) - 1));
		//ボーナス返済額(1回分)計算
		if(bonus>0){
			PaymentBonus = parseInt(bonus * Bonus_Rate * Math.pow((1 + Bonus_Rate),RepaymentCount/6) / (Math.pow((1 + Bonus_Rate),RepaymentCount/6) - 1));
		}else{
			PaymentBonus=0;
		}
		//年間返済額
		Paymentnensum = Paymentmonthlysum * 12 + PaymentBonus * 2;
		
		//残債残元金
		payzana = Paymentmonthlysum * (Math.pow((1 + Month_Rate),(RepaymentCount-endpyakikan)) - 1) / (Month_Rate * Math.pow((1 + Month_Rate),(RepaymentCount-endpyakikan)));
		payzanb = PaymentBonus * (Math.pow((1 + Bonus_Rate),(RepaymentCount-endpyakikan) / 6) - 1) / (Bonus_Rate * Math.pow((1 + Bonus_Rate),(RepaymentCount-endpyakikan) / 6));
		payzan = payzana + payzanb;

		a = parseInt(parseInt(Debt_Money/10000) - parseInt(payzan/10000));
		b = parseInt((parseInt((Paymentmonthlysum * endpyakikan) / 10000) + parseInt((PaymentBonus * (endpyakikan / 6)) / 10000)) - a);
		
		$("#txt_repayment_zangaku").val(number_format(parseInt(payzan/10000)));
		$("#txt_repayment_everymonth2").val(number_format(a));
		$("#txt_repayment_year2").val(number_format(parseInt(a + b)));
		$("#txt_repayment_bonus2").val(number_format(b));
		
		//計算エラーの時の処理
		if (($("#txt_repayment_zangaku").val() =="NaN") || ($("#txt_repayment_zangaku").val() <= 0)){
			$("#txt_repayment_zangaku").val('0');
		}
		if (($("#txt_repayment_everymonth2").val() == "NaN") || ($("#txt_repayment_everymonth2").val() <= 0)){
			$("#txt_repayment_everymonth2").val('0');
		}
		if (($("#txt_repayment_year2").val() == "NaN") || ($("#txt_repayment_year2").val() <= 0)){
			$("#txt_repayment_year2").val('0');
		}
		if (($("#txt_repayment_bonus2").val() == "NaN") || ($("#txt_repayment_bonus2").val() <= 0)){
			$("#txt_repayment_bonus2").val('0');
		}
	}
}

/**
 * php の number_format と同じ動作をする
 *
**/
function number_format(num){
	return (num.toString().replace( /([0-9]+?)(?=(?:[0-9]{3})+$)/g , '$1,' ));
}

/* 桁区切のカンマを消す。引数FigureNumは、カンマ入りの1バイト数字文字列 */
function fig2num(FigureNum){
    var Numeric = FigureNum;

    //カンマをすべて消す
    var Separator = Numeric.indexOf(',',0);
    while (Separator != -1){
        Numeric = Numeric.substring(0, Separator) + Numeric.substring(Separator+1, Numeric.length);
        Separator = Numeric.indexOf(',',0);
    }
    //カンマ消去後の数値を返して終了！
    return Numeric;
}


$(function(){
	$("#noscript_attention").hide();
});
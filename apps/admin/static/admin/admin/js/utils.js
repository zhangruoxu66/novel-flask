//获取指定的URL参数值 http://localhost/pages/setmeal_detail.html?id=3&name=jack
function getUrlParam(paraName) {
    var url = document.location.toString();
    //alert(url);
    var arrObj = url.split("?");
    if (arrObj.length > 1) {
        var arrPara = arrObj[1].split("&");
        var arr;
        for (var i = 0; i < arrPara.length; i++) {
            arr = arrPara[i].split("=");
            if (arr != null && arr[0] == paraName) {
                return arr[1];
            }
        }
        return "";
    }
    else {
        return "";
    }
}

//获得当前日期，返回字符串
function getToday() {
    var today = new Date();
    var year = today.getFullYear();
    var month = today.getMonth() + 1;//0表示1月，1表示2月
    var day = today.getDate();
    return (year + "-" + month + "-" + day);
}

//获得指定日期后指定天数的日期
function getSpecifiedDate(date,days) {
    date.setDate(date.getDate() + days);//获取指定天之后的日期
    var year = date.getFullYear();
    var month = date.getMonth() + 1;
    var day = date.getDate();
    return (year + "-" + month + "-" + day);
}

/**
 * 校验日期是否早于今天
 * @returns
 */
function isDateEarlierThanToday(date) {
	date = date.replace(/-/g, '');
	date = Number(new Date().Format(date));
	var today = Number(new Date().Format("yyyyMMdd"));
	return date < today;
}

function prefix0BeforeInteger(num, length) {
    return (Array(length).join('0') + num).slice(-length);
}

/**
 * 手机号校验
 1--以1为开头；
 2--第二位可为3,4,5,7,8,中的任意一位；
 3--最后以0-9的9个整数结尾。
 */
function checkTelephone(telephone) {
    var reg=/^[1][3,4,5,7,8][0-9]{9}$/;
    if (!reg.test(telephone)) {
        return false;
    } else {
        return true;
    }
}

/**
 * 邮箱校验
 */
function checkEmail(email){
    var reg_email = /^\w+@\w+\.\w+$/;
    var flag = reg_email.test(email);
    return flag;
}

/**
 * 身份证号码校验
 * 身份证号码为15位或者18位，15位时全为数字，18位前17位为数字，最后一位是校验位，可能为数字或字符X
 */
function checkIdCard(idCard){
    var reg = /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/;
    if(reg.test(idCard)){
        return true;
    }else{
        return false;
    }
}

//对Date的扩展，将 Date 转化为指定格式的String
// 月(M)、日(d)、小时(h)、分(m)、秒(s)、季度(q) 可以用 1-2 个占位符，
// 年(y)可以用 1-4 个占位符，毫秒(S)只能用 1 个占位符(是 1-3 位的数字)
Date.prototype.Format = function (fmt) { //author: meizz
    var o = {
        "M+": this.getMonth() + 1, //月份
        "d+": this.getDate(), //日
        "H+": this.getHours(), //小时
        "m+": this.getMinutes(), //分
        "s+": this.getSeconds(), //秒
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度
        "S": this.getMilliseconds() //毫秒
    };
    if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
        if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
}

//正整数验证
function isPInt(str) {
	var g = /^[1-9]*[1-9][0-9]*$/;
	return g.test(str);
}

var clock = '';//定时器对象，用于页面30秒倒计时效果
var nums = 60;
var validateCodeButton;
//基于定时器实现30秒倒计时效果
function doLoop() {
    validateCodeButton.disabled = true;//将按钮置为不可点击
    nums--;
    if (nums > 0) {
        validateCodeButton.value = nums + '秒后重新获取';
    } else {
        clearInterval(clock); //清除js定时器
        validateCodeButton.disabled = false;
        validateCodeButton.value = '重新获取验证码';
        nums = 60; //重置时间
    }
}

function getRecentDay(day){
    return getRecentDatetime(day, 0, 0, 0, 0);
}

function getRecentMinute(minute){
    return getRecentDatetime(0, 0, minute, 0, 0);
}

function getRecentDatetime(day, hour, minute, sec, mil){
        if (!day) {day = 0}
        if (!hour) {hour = 0}
        if (!minute) {minute = 0}
        if (!sec) {sec = 0}
        if (!mil) {mil = 0}

        var today = new Date();
        console.log(today);
        var targetday_milliseconds=today.getTime() + 1000*60*60*24*day + 1000*60*60*hour + 1000*60*minute + 1000*sec + mil;
        today.setTime(targetday_milliseconds);
        var tYear = today.getFullYear();
        var tMonth = today.getMonth();
        var tDate = today.getDate();
        var tHours = today.getHours();
        var tMinutes = today.getMinutes();
        var tSeconds = today.getSeconds();
        tMonth = doHandleMonth(tMonth + 1);
        tDate = doHandleMonth(tDate);
        tHours = doHandleMonth(tHours);
        tMinutes = doHandleMonth(tMinutes);
        tSeconds = doHandleMonth(tSeconds);
        return tYear + "-" + tMonth + "-" + tDate + " " + tHours + ":" + tMinutes + ":" + tSeconds;
}

function doHandleMonth(month){
    var m = month;
    if(month.toString().length == 1){
        m = "0" + month;
    }
    return m;
}

/**
  *@number:需要格式化的数字
  *@decimals:小数点位数
  *@separator:千分位分割符
 **/
function formatNumber(number, decimals, separator){
    if(isNaN(Number(number))) {
        return "0"
    }
    let _separator = separator||",";
    let _decimals = decimals||2;
    let numberStr = number.toFixed(_decimals);
    let splitArray = numberStr.split(".");
    let left = splitArray[0];
    let right = splitArray[1];
    let array = left.split('').reverse();
    let array2 = [];
    for (let i = 0; i < array.length; i++){
        if(i>0&&i%3===0) {
            array2.push(_separator);
        }
        array2.push(array[i]);
    }
    return array2.reverse().join("") + "." + right;
}
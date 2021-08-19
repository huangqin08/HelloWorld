/**
 * 表单提交时验证
 * @returns {boolean}
 */


// function checkForm() {
//     var Form = document.getElementById("formId");
//     var bool = true;
//     if (!InputUsernameBlur()) bool = false;
//     if (!InputPasswordBlur()) bool = false;
//     if (!InputRepasswordBlur()) bool = false;
//     if (!InputEmailBlur()) bool = false;
//     if (bool==true) {
//         Form.submit();
//     }
//     return bool;
// }

/**
 * 用户名输入框失去焦点
 */
$('#InputUsernam').blur(function () {
    click_username()
});
function click_username(){
    // console.log('焦点事件开始');
    var uname = $("#InputUsernam").val();
    var ename = $("#errorName");
    /* 用户名为空/不为空 */
    if (uname=="") {
        ename.html("用户名不能为空。");
        return false;
    }
    else {
        ename.html("");
    }
    /* 密码长度 */
    if (uname.length<4 || uname.length>16) {
        ename.html("长度为4-16。");
        return false;
    }
    else {
        ename.html("");
    }
//    通过ajax查询用户名是否已被注册
    var username = $('#InputUsernam').val();
    // console.log(username);
    $.getJSON('/user/check_user',{username:username},function (data){
        // console.log(data)
            $('#InputUsernam').next().html(data.msg);
            $('#InputUsernam').next().show();
    });
    // console.log('焦点事件结束');
    return true;
}

/**
 * 密码输入框失去焦点
 */
$('#InputPassword').blur(function (){
    click_password()
});
function click_password(){
    var pwd = $("#InputPassword").val();
    var epwd = $("#errorPassword");
    /* 密码为空/不为空 */
    if (pwd=="") {
        epwd.html("密码不为空。");
        return false;
    }
    else {
        epwd.html('');
    }
    /* 密码长度 */
    if (pwd.length<6 || pwd.length>16) {
        epwd.html("长度为6-16。");
        return false;
    }
    else {
        epwd.html('');
    }
    return true;
}

/**
 * 邮箱输入框失去焦点
 */
$('#InputEmail').blur(function (){
    click_email()
});
function click_email(){

    var email = $("#InputEmail").val();
    var eemail = $("#errorEmail");
    /* 邮箱不为空 */
    if (email=="") {
        eemail.html("邮箱不为空。");
        return false;
    }
    else {
        eemail.html('');
    }
    /* 邮箱格式验证 */
    var reg=/^\w+@\w+(\.[a-zA-Z]{2,3}){1,2}$/;
    if (reg.test(email)==false) {
        eemail.html("邮箱格式错误。");
        return false;
    }
    else {
        eemail.html('');
    }
    return true;
}


/**
 * 确认密码输入框失去焦点
 */
$('#InputRepassword').blur(function (){
    click_repassword()
});
function click_repassword(){
    var rpwd = $("#InputRepassword").val();
    var erpwd = $("#errorRepassword");
    /* 确认密码不为空 */
    if (rpwd=="") {
        erpwd.html("确认密码不为空。");
        return false;
    }
    else {
        erpwd.html('');
    }
    /* 确认密码与密码不一致 */
    var pwd = $("#InputPassword").val();
    if (pwd!= rpwd) {
        erpwd.html("密码不一致。");
        return false;
    }
    else {
        erpwd.html('');
    }
    return true;
}


/**
 * 手机号码输入框失去焦点
 */
$('#InputPhone').blur(function (){
    click_phone()
});
function click_phone(){

    var phone = $("#InputPhone").val();
    var ephone = $("#errorPhone");
    /* 手机号码为空/不为空 */
    if (phone=="") {
        ephone.html("手机号码不为空。");
        return false;
    }
    else {
        ephone.html('');
    }
    /* 手机号码长度 */
    if (phone.length < 11 || phone.length > 11 ) {
        ephone.html("长度为11位。");
        return false;
    }
    else {
        ephone.html('');
    }
    return true;

}


$('#submitButton').on('click', function () {
    // console.log('事件开始')
    var bool = true;
    if (!click_username()) bool = false;
    if (!click_password()) bool = false;
    if (!click_repassword()) bool = false;
    if (!click_email()) bool = false;
    if (!click_phone()) bool = false;
    if (bool==true) {
        $('#formId').submit()
    }
});

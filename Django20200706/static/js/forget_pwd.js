/**
 * 手机号码输入框失去焦点
 */
$('#phone').blur(function (){
    click_phone()
});
function click_phone(){

    var phone = $("#phone").val();
    var ephone = $("#errorphone");
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



$('#send_code').click(function () {
    //
    var phone = $('#phone').val();
    click_phone();
    // 通过ajax发送请求
        $.getJSON('/user/send_code',{phone:phone},function (data) {
            alert(data.msg)
        })
});

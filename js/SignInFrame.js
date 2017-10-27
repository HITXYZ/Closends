var flag = {
    "email":false,
    "password":false
};
$(function () {
    // 邮箱输入初判断
    $("#emailInput").focus(function () {
        document.getElementById("mail-tips").style.display="none";
        document.getElementById("mail-error").style.display="none";
        document.getElementById("sign_in_error").style.display="none";
    })
    $("#emailInput").blur(function () {
        var email = $("#emailInput").val();
        var pattern_email=/\b(^['_A-Za-z0-9-]+(\.['_A-Za-z0-9-]+)*@([A-Za-z0-9-])+(\.[A-Za-z0-9-]+)*((\.[A-Za-z0-9]{2,})|(\.[A-Za-z0-9]{2,}\.[A-Za-z0-9]{2,}))$)\b/;
        if(!pattern_email.test(email))
        {
            document.getElementById("mail-error").style.display="block";
            flag.email = false;
        }else{
            document.getElementById("mail-error").style.display="none";
            flag.email = true;
        }
        if(email.length == 0){
            document.getElementById("mail-tips").style.display="block";
            flag.email = false;
        }
        return;
    })

    //密码输入初判断
    $("#passwordInput").focus(function () {
        document.getElementById("password-tips").style.display="none";
        document.getElementById("password-error").style.display="none";
        document.getElementById("sign_in_error").style.display="none";
    })
    $("#passwordInput").blur(function () {

        var password = $("#passwordInput").val();
        var pattern_password = /\b(^['A-Za-z0-9]{8,16}$)\b/;
        if (!pattern_password.test(password)) {
            document.getElementById("password-error").style.display="block";
            flag.password = false;
        }else{
            document.getElementById("password-error").style.display="none";
            flag.password = true;
        }
        if(password.length == 0){
            document.getElementById("password-tips").style.display="block";
            flag.password = false;
        }
        return;
    })

    $("#form").submit(function(){
        //综合判断
        if(flag.email&flag.password == false){
            return false;
        }
        return true;
    });
});
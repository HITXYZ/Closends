function load(){
    var window_width=document.documentElement.clientWidth;
    if(window_width<=1000){
        document.getElementById("sideshow").style.display="none";
        $("#main-wrapper").css("marginLeft",0);
    }else if(window_width<=1200) {
        document.getElementById("sideshow").style.display="block";
        document.getElementById("sideshow").style.width="240px";
        $("#main-wrapper").css("marginLeft",240);
    }else{
        document.getElementById("sideshow").style.display="block";
        document.getElementById("sideshow").style.width="480px";
        $("#main-wrapper").css("marginLeft",480);
    }
    return;
}
function backtoSignUp() {
    document.getElementById("sign_up_error").style.display="none";
    document.getElementById("sign_up_form").style.display="block";
    return;
}
var flag = {
    "nickname":false,
    "password":false,
    "mail":false,
};
$(function(){
    //窗口大小变化实时监测
    $(window).resize(function () {
        var window_width=document.documentElement.clientWidth;
        if(window_width<=1000){
            document.getElementById("sideshow").style.display="none";
            $("#main-wrapper").css("marginLeft",0);
        }else if(window_width<=1200) {
            document.getElementById("sideshow").style.display="block";
            document.getElementById("sideshow").style.width="240px";
            $("#main-wrapper").css("marginLeft",240);
        }else{
            document.getElementById("sideshow").style.display="block";
            document.getElementById("sideshow").style.width="480px";
            $("#main-wrapper").css("marginLeft",480);
        }
        return;
    })
    // mail验证
    $("#mail").focus(function () {
        document.getElementById("mail-tips").style.display="none";
        document.getElementById("mail-error").style.display="none";
        document.getElementById("mail-ok").style.display="none";
        return;
    })
    $("#mail").blur(function(){
        var mail = $(this).val();
        var pattern=/\b(^['_A-Za-z0-9-]+(\.['_A-Za-z0-9-]+)*@([A-Za-z0-9-])+(\.[A-Za-z0-9-]+)*((\.[A-Za-z0-9]{2,})|(\.[A-Za-z0-9]{2,}\.[A-Za-z0-9]{2,}))$)\b/;
        if(!pattern.test(mail))
        {
            document.getElementById("mail-error").style.display="block";
            document.getElementById("mail-ok").style.display="none";
        }else{
            document.getElementById("mail-error").style.display="none";
            document.getElementById("mail-ok").style.display="block";
            flag.mail = true;
        }
        if(mail.length == 0){
            document.getElementById("mail-tips").style.display="block";
            flag.mail = false;
        }
        return;
    });

    // 用户名校验
    $("#nickname").focus(function () {
        document.getElementById("nickname-tips").style.display="none";
        document.getElementById("nickname-error").style.display="none";
        document.getElementById("nickname-ok").style.display="none";
        return;
    })
    $("#nickname").blur(function(){
        var nickname = $(this).val();
        // 校验规则，可调整
        var pattern =  /^[\u4e00-\u9fff\w]{1,12}$/;
        if(!pattern.test(nickname)){
            document.getElementById("nickname-error").style.display="block";
            document.getElementById("nickname-ok").style.display="none";
            flag.nickname = false;
        }
        else{
            document.getElementById("nickname-error").style.display="none";
            document.getElementById("nickname-ok").style.display="block";
            flag.nickname = true;
        }
        if(nickname.length == 0){
            document.getElementById("nickname-tips").style.display="block";
        }
        return;
    });

    // 密码校验
    $("#password1").focus(function () {
        document.getElementById("password1-tips").style.display="none";
        document.getElementById("password1-error").style.display="none";
        document.getElementById("password1-ok").style.display="none";
        return;
    })
    $("#password1").blur(function(){
        var password1=$(this).val();
        var pattern = /\b(^['A-Za-z0-9]{8,16}$)\b/;
        if (!pattern.test(password1)) {
            document.getElementById("password1-error").style.display="block";
            document.getElementById("password1-ok").style.display="none";
        }else{
            document.getElementById("password1-error").style.display="none";
            document.getElementById("password1-ok").style.display="block";
            //flag.password=true;
        }
        if (password1.length==0){
            document.getElementById("password2-ok").style.display="none";
            document.getElementById("password1-tips").style.display="block";
        }
        //更新确认密码栏状态
        var password2 = $("#password2").val();
        if (password2!=$("#password1").val()) {
            if(password1.length!=0&&password2.length!=0){
                document.getElementById("password2-error").style.display="block";
                document.getElementById("password2-ok").style.display="none";
            }
            flag.password = false;
        }
        else{
            document.getElementById("password2-error").style.display="none";
            if(password1.length!=0 && pattern.test(password1)) {
                document.getElementById("password2-ok").style.display = "block";
            }
            flag.password = true;
        }
        return;
    });

    // 密码重复校验
    $("#password2").focus(function () {
        document.getElementById("password2-tips").style.display="none";
        document.getElementById("password2-error").style.display="none";
        document.getElementById("password2-ok").style.display="none";
        return;
    })
    $("#password2").blur(function(){

        var password2 = $(this).val();
        var pattern = /\b(^['A-Za-z0-9]{8,16}$)\b/;
        if (password2!=$("#password1").val()) {
            document.getElementById("password2-error").style.display="block";
            document.getElementById("password2-ok").style.display="none";
            flag.password = false;
        }
        else{
            document.getElementById("password2-error").style.display="none";
            if($("#password1").val().length!=0 && pattern.test($("#password1").val())) {
                document.getElementById("password2-ok").style.display = "block";
            }
            flag.password = true;
        }
        if (password2.length==0){
            document.getElementById("password2-tips").style.display="block";
        }
        return;
    });

    $("#form").submit(function(){
        var ok = flag.nickname&&flag.password&&flag.mail;
        if(ok==false){
            //alert("您的注册信息存在问题");
            //history.back();
            return false;
        }
        return true;
    });
});
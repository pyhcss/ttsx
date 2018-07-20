$(function () {
    var error_name = true;
    var error_pwd = true;
    var error_captcha = true;
    var error = true;

    $("#id_captcha_1").attr("placeholder","请输入验证码");

    $('.captcha').click(function () {
    $.getJSON("/captcha/refresh/", function (result) {
        $('.captcha').attr('src', result['image_url']);
        $('#id_captcha_0').val(result['key'])
        });
    });

    $('#username').blur(function () {
        username();
    });

    $('#pwd').blur(function () {
        userpwd();
    });

    $("#id_captcha_1").blur(function () {
        captcha();
    });

    function username(){
        var len = $('#username').val().length;
        if(len == 0)
        {
            error_name=true;
            $('#username').next().html("请输入用户名");
            $('#username').next().show();
        }
        else if(len<5 || len>20)
        {
            error_name=true;
            $('#username').next().html("用户名错误");
            $('#username').next().show();
        }
        else
        {
            error_name=false;
            $('#username').next().hide();
        }
    }

    function userpwd(){
        var len = $('#pwd').val().length;
        if(len == 0)
        {
            error_pwd=true;
            $('#pwd').next().html("请输入密码");
            $('#pwd').next().show();
        }
        else if(len<8)
        {
            error_pwd=true;
            $('#pwd').next().html("密码错误");
            $('#pwd').next().show();
        }
        else
        {
            error_pwd=false;
            $('#pwd').next().hide();
        }
    }

    function captcha() {
        len = $('#id_captcha_1').val().length;
        if(len == 0)
        {
            error_captcha = true;
            $(".yanzheng_error").html("请输入验证码");
            $(".yanzheng_error").show();
        }
        else if(len != 4)
        {
            error_captcha = true;
            $(".yanzheng_error").html("验证码错误");
            $(".yanzheng_error").show();
        }
        else{
            error_captcha = false;
            $(".yanzheng_error").hide();
        }
    }

    function usernamepd() {
        $.ajaxSettings.async = false;
        $.get("/user/nameycl/"+$('#username').val(),function (data) {
            if(data.data == 1)
            {
                error = false;
                $('#username').next().hide();
            }
            else
            {
                error = true;
                $('#username').next().html("用户名或密码错误");
                $('#username').next().show();
            }
        });
        $.ajaxSettings.async = true;
    }

    function cookie() {
        if($("#jzyhm").is(':checked'))
        {
            $.get("/user/cookie/"+$('#username').val());
        }
        else
        {
            $.get("/user/cookie/")
        }

    }

    $('#from_login').submit(function(){
        username();
        userpwd();
        captcha();
        cookie();

        if(error_captcha == false && error_name == false && error_pwd == false)
        {
            usernamepd();
        }
        else
        {
            return false;
        }

        if(error == true)
        {
           return false;
        }
        else
        {
           return true;
        }

    });

});


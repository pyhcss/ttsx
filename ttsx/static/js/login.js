$(function () {
    var error_name = true;
    var error_pwd = true;
    var error_username = true;
    var error_userpwd = true;

    $('#username').blur(function () {
        username();
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

    $('#pwd').blur(function () {
        userpwd();
    });

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

    function usernamepd() {
        $.ajaxSettings.async = false;
        $.get("/user/nameycl/"+$('#username').val(),function (data) {
            if(data.data == 1)
            {
                error_username = false;
                $('#username').next().hide();
            }
            else
            {
                error_username = true;
                $('#username').next().html("用户名错误");
                $('#username').next().show();
            }
        });
        $.ajaxSettings.async = true;
    }

    function userpwdpd(){
        $.ajaxSettings.async = false;
        $.post("/user/pwd_cl",{"name":$('#username').val(),"pwd":$('#pwd').val()},function (data) {
            if(data.data == 1)
            {
                error_userpwd = false;
                $('#pwd').next().hide();
            }
            else
            {
                error_userpwd = true;
                $('#pwd').next().html("密码错误");
                $('#pwd').next().show();
            }
        });
        $.ajaxSettings.async = true;
    }
    function cookie() {
        if($("#jzyhm").is(':checked')){
            $.get("/user/cookie/"+$('#username').val());
        }
    }

    $('#from_login').submit(function(){
        username();
        userpwd();
        cookie();

        if(error_name == false && error_pwd == false)
        {
           usernamepd();
        }
        if(error_username == true)
        {
            return false;
        }
        if(error_name == false && error_pwd == false)
        {
            userpwdpd();
        }
        if(error_userpwd == true)
        {
            return false;
        }
        if(error_username == false && error_userpwd == false)
        {
            return true;
        }

    });

});


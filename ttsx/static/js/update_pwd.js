function sendEmailCode() {
	// $(".n_err_tip").hide();
    $(".n_but_con").removeAttr("onclick");
    var username = $("#user_name").val();
    if (!username || username.length < 5) {
        $('#user_name').next().html("请填写正确的用户名");
        $('#user_name').next().show();
        $(".n_but_con").attr("onclick", "sendEmailCode();");
        return;
    }
    else {
    	$('#user_name').next().hide();
	}
    var imageCodeId = $("#id_captcha_0").val();
    var imageCode = $("#id_captcha_1").val();
    if (!imageCode) {
        $(".n_yanzheng .n_error_tip").html("请填写验证码");
        $(".n_yanzheng .n_error_tip").show();
        $(".n_but_con").attr("onclick", "sendEmailCode();");
        return;
    }
    else if (imageCode.length != 4) {
        $(".n_yanzheng .n_error_tip").html("请填写正确的验证码");
        $(".n_yanzheng .n_error_tip").show();
        $(".n_but_con").attr("onclick", "sendEmailCode();");
        return;
    }
    else {
    	$(".n_yanzheng .n_error_tip").hide();
	}
    $.get(
        "/user/emailcode",
        {"username": username, "captcha_0": imageCodeId, "captcha_1": imageCode},
        function(data) {
        	if (0 == data.errcode){
        		$(".n_yanzheng .n_error_tip").html(data.errmsg);
        		$(".n_yanzheng .n_error_tip").show();
        		var duration = 60;
            	var timeObj = setInterval(function() {
                duration = duration - 1;
                $(".n_but_con").css({"width":"67px"});
                $(".n_but1").html("已发送");
                $(".n_but2").html(duration + "秒");
                if (1 == duration) {
                    clearInterval(timeObj);
                    $(".n_but_con").css({"width":"82px"});
                    $(".n_but1").html("获取邮箱");
                    $(".n_but2").html("验证码");
                    $(".n_but_con").attr("onclick", "sendEmailCode();")
                }
            	}, 1000, 60)
			} else {
				$(".n_yanzheng .n_error_tip").html(data.errmsg);
        		$(".n_yanzheng .n_error_tip").show();
        		$.get("/captcha/refresh/",function(data) {
					$(".n_yanzheng img").attr({'src':data.image_url});
					$("#id_captcha_0").attr({'value':data.key})
                });
        		$(".n_but_con").attr("onclick", "sendEmailCode();");
			}
        })
	}

$(function(){
	var error_name = true;
	var error_password = true;
	var error_check_password = true;
	var error_email = true;
	var error_captcha = true;

	$("#user_name").blur(function() {
		check_user();
    });

	$("#id_captcha_1").blur(function() {
		check_captcha();
    });

	$('#pwd').blur(function() {
		check_pwd();
	});

	$('#cpwd').blur(function() {
		check_cpwd();
	});

	$('#email').blur(function() {
		check_email();
	});

	function check_user() {
		var username = $("#user_name").val();
		if (!username || username.length < 5) {
        	$('#user_name').next().html("请填写正确的用户名");
        	$('#user_name').next().show();
        	error_name = true;
		} else {
    		$('#user_name').next().hide();
    		error_name = false;
		}
    }

    function check_captcha() {
		var text = $(".n_yanzheng .n_error_tip").html().substr($(".n_yanzheng .n_error_tip").html().length-4);
		if (text == "发送成功") {
			$(".n_yanzheng .n_error_tip").hide();
			error_captcha = false;
        } else{
			$(".n_yanzheng .n_error_tip").html("请先获取邮箱验证码");
			$(".n_yanzheng .n_error_tip").show();
			error_captcha = true;
		}
    }

	function check_pwd(){
		var len = $('#pwd').val().length;
		if(len<8||len>20) {
			$('#pwd').next().html('密码最少8位，最长20位');
			$('#pwd').next().show();
			error_password = true;
		} else {
			$('#pwd').next().hide();
			error_password = false;
		}
	}

	function check_cpwd(){
		var pass = $('#pwd').val();
		var cpass = $('#cpwd').val();

		if(pass!=cpass) {
			$('#cpwd').next().html('两次输入的密码不一致');
			$('#cpwd').next().show();
			error_check_password = true;
		} else {
			$('#cpwd').next().hide();
			error_check_password = false;
		}
	}

	function check_email(){
		var email_code = $("#email").val();
		if (!email_code || email_code.length != 6) {
        	$('#email').next().html("请填写正确的邮箱验证码");
        	$('#email').next().show();
        	error_email = true;
		} else {
    		$('#email').next().hide();
    		error_email = false;
		}
	}

    $('.captcha').click(function () {
    	$.getJSON("/captcha/refresh/", function (result) {
        	$('.captcha').attr('src', result['image_url']);
        	$('#id_captcha_0').val(result['key'])
    	});
	});

	$('#reg_form').submit(function() {
		check_user();
		check_pwd();
		check_cpwd();
		check_email();
		check_captcha();

		if(error_name == false && error_password == false && error_check_password == false && error_email == false && error_captcha == false) {
			$.post(
				"/user/updatepwd",
				{"name":$("#user_name").val(),"captcha":$("#email").val(),"pwd":$("#pwd").val(),"csrfmiddlewaretoken":$("input[name='csrfmiddlewaretoken']").val()},
				function(data) {
					if (data.errcode == 0){
						$("#cpwd").next().html(data.errmsg);
						$("#cpwd").next().show();
					} else {
						$("#cpwd").next().html(data.errmsg);
						$("#cpwd").next().show();
						$.get("/captcha/refresh/",function(data) {
							$(".n_yanzheng img").attr({'src':data.image_url});
							$("#id_captcha_0").attr({'value':data.key});
                		});
					}
                }
			);
			return false;
		} else {
			return false;
		}
	});
});
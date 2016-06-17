
jQuery(document).ready(function() {
		
	    /*
		 *         Fullscreen background
		 *             */
	$.backstretch("login/assets/img/backgrounds/1.jpg");
/*
	$("#form-submite").submit(function(){
		var username = $(".form-username").val();
		var password = $(".form-password").val();
		if (username.length == 0 || password.length == 0){
			alert('please input the username or password')
			return
		}
		var data_send = {
			'username': username,
			'password': $.md5(password)
		}
		alert($.md5(password))
		var jqxhr = $.ajax('/api/user_login',
        {
            dataType:'json',
            type:'POST',
            contentType:'application/json',
            data:$.toJSON(data_send)
        }
    ).done(function (data) {

        if (data['errrorCode'] == 10000){
            alert('注册成功')
        }
        
    }).fail(function (xhr,status) {
        alert('the username or password is error')
    });
	});
	*/
		    /*
			 *         Form validation
			 *  */
		    $('.login_form-zxl input[type="text"], .login-form input[type="password"], .login-form textarea').on('focus', function() {
						$(this).removeClass('input-error');
						    });
			    
			    $('.login_form_zxl').on('submit', function(e) {
					alert('dddddddddddddddddddd')
					var useranme = $(".form-username").val();
					var password = $(".form-password").val();
					if (username.length == 0 || password.length == 0){
						alert('please input the username or password !');
						return ;

					}
					alert('successs!');
					

				 });

				    
				    
});

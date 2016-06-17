/**
 * Created by zxl on 16-5-8.
 */
$(document).ready(function(){
  $("#js-mobile_ipt").change(function(){
      var input_ = $(this).val();
      if (input_.length == 0){
          $('#js-mobile_label').css("visibility", 'visible')
      }
      else{
           $('#js-mobile_label').css("visibility", 'hidden')
      }
  });
    
    $("#js-mobile_pwd_ipt").change(function(){
      var input_ = $(this).val();
      if (input_.length == 0){
          $('#js-password_label').css("visibility", 'visible')
      }
      else{
           $('#js-password_label').css("visibility", 'hidden')
      }
  });

    $("#js-mobile_vcode_ipt").change(function(){
      var input_ = $(this).val();
      if (input_.length == 0){
          $('#js-mobile_vcode_label').css("visibility", 'visible')
      }
      else{
           $('#js-mobile_vcode_label').css("visibility", 'hidden')
      }
  });
    
});
function regis() {
    var email = $('#js-mobile_ipt').val();
    var password = $('#js-mobile_pwd_ipt').val();
    var verifycode = $('#js-mobile_vcode_ipt').val()
    if (email.length == 0) {
        alert('请输入您的邮箱')
        return false;
    }
    if (password.length == 0){
        alert('请输入您的注册密码')
        return false;
    }
    //匹配一般的常见的邮箱
    var reg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/
    if (reg.test(email) == false){
        alert('您输入的邮箱不合法，请重新输入')
        return false
    }
    reg = /^([a-zA-Z0-9_-]){8,32}/
    if (reg.test(password) == false){
        alert('请输入8到32位的密码,只能使用字母、数字和_')
        return false
    }
    if (verifycode.length != 6){
        alert('请输入您的verifycode')
    }
    alert('信息正确')
    var data_send = {
        'account': email,
        'password': $.md5(password),
        'verifycode': verifycode
    }
    var jqxhr = $.ajax('/api/register',
        {
            dataType:'json',
            type:'POST',
            contentType:'application/json',
            data:$.toJSON(data_send)
        }
    ).done(function (data) {
        /*
        if (data['errrorCode'] == 10000){
            alert('注册成功')
        }*/
        alert('注册成功')
    }).fail(function (xhr,status) {
        alert('失败')
    });
}
function getverifycode() {
    var email = $('#js-mobile_ipt').val();
    var reg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/
    if (reg.test(email) == false){
        alert('您输入的邮箱不合法，请重新输入')
        return false
    }
    var data_send = {
        email:email,
        type:0
    }
    var jqxhr = $.ajax('/api/get/verify_code',
        {
            dataType:'json',
            type:'POST',
            contentType:'application/json',
            data:$.toJSON(data_send)
        }
    ).done(function (data) {
        if (data['errorCode'] == 10000) {
            alert('验证码发送成功，请到邮件查看')
        }
        else {
             alert(data['errorMsg'])
        }
        
    }).fail(function (xhr,status) {
        alert('请求失败')
    });

}




































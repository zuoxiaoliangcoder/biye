/**
 * Created by zxl on 16-6-2.
 */
$(document).ready(function() {
    $("#button_submite").on('click', function (e) {
		var username = $('#inputFirstName').val();
        var email = $('#inputEmail').val();
		var cur_pass = $('#inputCurrnetPassword').val();
		var new_pass = $('#inputNewPassword').val();
		var com_pass = $('#inputConfirmNewPassword').val();
		var note = $('#inputNote').val();
		
		var telnec = new Array();
		/*$("input[name=server]").each(function(){
			if ($(this).attr("checked")){
                alert('value: '+$(this).val())
				telnec.push($(this).val());
			}
		});*/
        $('input[name="server"]:checked').each(function(){
             alert('value: '+$(this).val());
            telnec.push($(this).val());
        });
        alert('jinqul');
		alert(telnec);
		var level = $(':radio[name="radio"]:checked').val();
		var data_send = {
			'username': username,
			'email': email,
			'curPass':  $.md5(cur_pass),
			'newPass': $.md5(new_pass),
			'comPass': $.md5(com_pass),
			'note': note,
			'telnec': telnec,
			'level': level
		};
		var jqxhr = $.ajax('/'+username+'/info_change',
            {
				dataType: 'json',
				type: 'POST',
				contentType: 'application/json',
				data: $.toJSON(data_send)
            }
		).done(function(data){
			if (data['errorCode'] == 10000){
				alert('修改成功')
				/*location.reload(true) */
			}	
			}).fail(function(xhr, status){
				alert('失败')
		});


    });
});

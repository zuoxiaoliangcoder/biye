/*
 *	www.templatemo.com
 *******************************************************/

/* HTML document is loaded. DOM is ready. 
-----------------------------------------*/
$(document).ready(function() {

	/* Mobile menu */
	$('.mobile-menu-icon').click(function () {
		$('.templatemo-left-nav').slideToggle();
	});

	/* Close the widget when clicked on close button */
	$('.templatemo-content-widget .fa-times').click(function () {
		$(this).parent().slideUp(function () {
			$(this).hide();
		});
	});
	

	/*$('#myCollModal').modal({
		keyboard: true
	});*/

	$('#myCollModal').modal('hide');
	/*window.setTimeout(function () {
		$('#myCollModal').modal('hide')

	}, 3000);*/

	var username = $('#username').val();
	var jqxhr = $.ajax('/' + username + '/collection',
		{
			dataType: 'json',
			type: 'GET',
			contentType: 'application/json',
		}
	).done(function (data) {
		if (data['errorCode'] == 10000) {
			var follows = data['books'];
			var ul = $('#my-collections');
			for (var i = 0; i < follows.length; i++) {
				var href = '/books/detail/' + follows[i]['index'];
				var title = follows[i]['title']
				var li = '<li><a href=\'' + href + '\'>' + title + '</a></li>';
				ul.append(li)
			}
		}
		else alert('huoqu shibai')
	}).fail(function (xhr, status) {
		alert(status, xhr)
	});
	getfollows()
});




	


	//$('#follows').change(function() {
		function getfollows()
	   {
	    //var username = $('#username_card').val()
	    var username = 'shawn'

	    document.getElementById('follows').length=0


        var jqxhr = $.ajax('/'+username+ '/follows',
            {
                dataType:'json',
                type:'GET',
                contentType:'application/json',
            }
        ).done(function (data) {
            var follows = data['follows']

            for(var i = 0; i < follows.length; i++){
                var y = document.createElement('option');
                y.text = follows[i]['username'];
                y.value = follows[i]['userId'];
                document.getElementById('follows').add(y);
            }
        }).fail(function (xhr,status) {
            alert('失败')
        });
	}
	

function shoucang(obj){
     user_id = $('#userId').val();
     user_name = $('#username').val();
     data_send = {
        'bookId': obj.toString()
     }
     var jqxhr = $.ajax('/'+user_name+'/collection',
        {
            dataType:'json',
            type:'POST',
            contentType:'application/json',
            data:$.toJSON(data_send)
        }
    ).done(function (data) {
        if (data['errorCode'] == 10000){
  			alert('collection success')
        }
    }).fail(function (xhr,status) {
        alert('collection失败')
    });
}

function info_change(user_id){
    $('#info-change-form').submit()
}
function show_info_modal() {
	$('#info-change-modal').modal('show');
}
function delete_col(book_id){
	var jqxhr = $.ajax('/book/delete/'+book_id,
		{
			dataType: 'json',
			type: 'GET',
			contentType: 'application/json',
		}
	).done(function (data) {
		if (data['errorCode'] == 10000) {
			alert('取消收藏成功')
		}
	}).fail(function (xhr, status) {
		alert(status, xhr)
	});
}

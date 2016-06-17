$(document).ready(function() {
    if (!window.console) window.console = {};
    if (!window.console.log) window.console.log = function() {};

    $("#messageform").on("submit", function() {
        newMessage($(this));
        return false;
    });
    $("#messageform").on("keypress", function(e) {
        if (e.keyCode == 13) {
            newMessage($(this));
            return false;
        }
    });
    $("#message").select();
    updater.start();

});


function newMessage(form) {

    var message = form.formToDict();

    var value = 'zzy';



    message['toUser'] = value;

    updater.socket.send(JSON.stringify(message));
    form.find("input[type=text]").val("").select();
}

jQuery.fn.formToDict = function() {
    var fields = this.serializeArray();
    var json = {};
    for (var i = 0; i < fields.length; i++) {
        json[fields[i].name] = fields[i].value;
    }
    if (json.next) delete json.next;
    return json;
};

var updater = {
    socket: null,

    start: function() {
        var user_id = $('#userId').val();
        var url = "ws://" + "127.0.0.1:8004"+ "/api/chatsocket?userId=" + user_id;
        updater.socket = new WebSocket(url);

        updater.socket.onmessage = function(event) {
            updater.showMessage(JSON.parse(event.data));
        }

    },

    showMessage: function(message) {

        var existing = $("#m" + message.id);
        if (existing.length > 0) return;
        var node = $(message.html);

        node.hide();
        $("#inbox").append(node);
        if ($('#inbox').find('.message').size() > 10){
            $("#inbox").find('.message').eq(0).remove()
        }


        node.slideDown();
    }
};

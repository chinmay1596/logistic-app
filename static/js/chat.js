
function getMessages() {
    if (!scrolling) {
        $.get('support/reply/customer/<int:pk>/', function (messages) {
            console.log(messages);
            $('#msg-list').html(messages);
            var chatlist = document.getElementById('msg-list-div');
            chatlist.scrollTop = chatlist.scrollHeight;
        });
    }
    scrolling = false;
}

var scrolling = false;
$(function () {
    $('#msg-list-div').on('scroll', function () {
        scrolling = true;
    });
    refreshTimer = setInterval(getMessages, 500);
});



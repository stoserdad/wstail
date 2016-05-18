/**
 * Created by bender on 28.04.16.
 */
$(function(){
    var sock;
    sock = new WebSocket('ws://' + document.location.host + '/websocket');
    var onmouse = true;
            $('#log').mouseenter(function () {
                onmouse = false;
            });
            $('#log').mouseout(function () {
                onmouse = true;
            });
    if(sock){
        sock.onopen = function() {
            console.log('connect.');
        };
        sock.onclose = function(){
             $('#viewLog').removeClass('button-success');
             $('#viewLog').addClass('button-error');
             $('.fa').removeClass('fa-check');
             $('.fa').addClass('fa-close');
        };
        sock.onmessage = function(e){
            $('#log').append(e.data + '\n');
            if (onmouse){
                $('#log').scrollTop($('#log').get(0).scrollHeight);
            };
        };
        $('#viewLog').click(function(){
            var current = $('#viewLog').attr('status');
            if (current === '1') {
                sock.send('start');
                console.log('start');
                $('.fa').removeClass('fa-close');
                $('.fa').addClass('fa-check');
                $('#viewLog').attr('status', '0');
            } else if (current === '0'){
                sock.send('stop');
                console.log('stop');
                $('.fa').removeClass('fa-check');
                $('.fa').addClass('fa-close');
                $('#viewLog').attr('status', '1');
            }
        });
        $('#viewLog').removeClass('button-error');
        $('#viewLog').addClass('button-success');
    }
});

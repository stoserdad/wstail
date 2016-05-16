/**
 * Created by bender on 28.04.16.
 */
$(function(){
    var sock;
    sock = new WebSocket('ws://' + document.location.host + '/websocket');
    if(sock){
        sock.onopen = function() {
            console.log('Законнектились');
        };
        sock.onclose = function(){
            sock.send('stopViewLog');
        };
        sock.onmessage = function(e){
            $('#log').append(e.data + '\n');
        };
        $('#viewLog').click(function(){
            var current = $('#viewLog').attr('status');
            if (current === '1') {
                sock.send('start');
                console.log('start');
                $('#viewLog').attr('status', '0');
            } else if (current === '0'){
                sock.send('stop');
                // sock.close();
                console.log('stop');
                $('#viewLog').attr('status', '1');
            }
        });
    }
});

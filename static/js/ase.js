/**
 * Created by bender on 23.05.16.
 */
$(function () {
    setTimeout( function() {
        //noinspection JSUnresolvedFunction
        $.post('http://' + document.location.host + '/ase', function (data) {
            if (data > 0) {
                $('#pid').text('Сервис запущен. PID: ' + data);
                $('#start').attr('disabled', true);
            } else {
                $('#pid').text('Сервис не запущен.');
            }
        });
        setTimeout(arguments.callee, 3000);
    },3000 );
    var sock = new WebSocket('ws://' + document.location.host + '/wsase');
    if (sock) {
        $('#ws').addClass('button-success').append('ws on');
    }
    sock.onclose = function () {
                $('#ws').removeClass('button-success');
                $('#ws').addClass('button-error').text('ws off');
            };
    $('#start').click(function () {
        $('#log').empty();
        if (sock){
            sock.send('start');
            sock.onmessage = function(e) {
                $('#log').append(e.data + '\n');
            };
            $('#start').attr('disabled', true);
            $.post('http://' + document.location.host + '/ase', function (data) {
                if (data > 0) {
                    $('#pid').text('Сервис запущен. PID: ' + data);
                }
            });
        }
    });
    $('#stop').click(function () {
        $('#log').empty();
        if (sock){
            sock.send('stop');
            sock.onmessage = function(e) {
                $('#log').append(e.data + '\n');
            };
            $('#start').removeAttr('disabled');
            $('#pid').text('Сервис не запущен.');
        }
    });
    $('#restart').click(function () {
        $('#log').empty();
        if (sock) {
            sock.send('restart');
            sock.onmessage = function (e) {
                $('#log').append(e.data + '\n');
            };
        }
    });
});

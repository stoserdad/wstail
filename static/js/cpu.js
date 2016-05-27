/**
 * Created by bender on 18.05.16.
 */
$(function() {
    var sock = new WebSocket('ws://' + document.location.host + '/wscpu');
    if(sock) {
        sock.onopen = function () {
            console.log('connect.');
        };
        var cpu = '';

        sock.onmessage = function (e) {
            $('#log').append(e.data + '\n');
            cpu = $.parseJSON(e.data);
        };

        $.post('http://' + document.location.host + '/size', function (data) {
            var c = $.parseJSON(data);

            var smoothie = new SmoothieChart();
            smoothie.streamTo(document.getElementById("smoothie-chart"));

            var lines = [];

            for(var i=0; i<c.cnt; i++){
                lines.push(new TimeSeries);
            }
            setInterval(function() {
                for(var i=0; i<c.cnt; i++){
                    lines[i].append(new Date().getTime(), cpu.cpu[i]);
                }
            }, 100);
            for(var j=0; j<c.cnt; j++){
                smoothie.addTimeSeries(lines[j]);
            }
        });
    }
});


            // dataPoints
//             var datas = [];
//             for (var f = 0; f < c.cnt; f++) {
//                 eval('var dataPoints' + f + '= new Array()')
//             }
//             for (var l = 0; l < c.cnt; l++) {
//                 datas.push({
//                     type: 'line',
//                     dataPoints: eval('dataPoints' + l)
//                 })
//             }
//             var chart = new CanvasJS.Chart("chartContainer", {
//                 title: {
//                     text: "CPU Usage"
//                 },
//                 toolTip: {
//                     shared: true
//                 },
//                 legend: {
//                     verticalAlign: "top",
//                     horizontalAlign: "center",
//                     fontSize: 14,
//                     fontWeight: "bold",
//                     fontFamily: "calibri",
//                     fontColor: "dimGrey"
//                 },
//                 data: datas
//             });
//             var updateInterval = 50;
//             var yValue = [];
//             var time = new Date;
//             var updateChart = function (count) {
//                 count = count || 10;
//                 // count is number of times loop runs to generate random dataPoints.
//                 for (var i = 0; i < count; i++) {
//                     // add interval duration to time
//                     time.setTime(time.getTime() + updateInterval);
//                     // generating random values
//                     for (var j = 0; j < c.cnt; j++) {
//                         yValue[j] = cpu.cpu[j]
//                     }
//                     for (var k = 0; k < c.cnt; k++) {
//                         eval('dataPoints' + k).push({
//                             x: time.getTime(),
//                             y: yValue[k]
//                         })
//                     }
//                 }
//                 chart.render();
//             };
//             updateChart(3000);
//             setInterval(function () {
//                 updateChart()
//             }, updateInterval);
//         })
//     }
// });

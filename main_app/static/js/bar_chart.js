google.charts.load('current', {'packages':['bar']});
google.charts.setOnLoadCallback(drawStuff);
var evaluation_count = parseInt($("#evaluation_count").val());
var evaluator_count = parseInt($("#evaluator_count").val());
function drawStuff() {
  var data = new google.visualization.arrayToDataTable([
    ['Title', 'Value'],
    ["Evaluator", evaluator_count],
    ["Response", evaluation_count],
  ]);

  var options = {
    title: '',
    width: 900,
    legend: { position: 'none' },
    chart: { title: '',
             subtitle: '' },
    bars: 'horizontal', // Required for Material Bar Charts.
    axes: {
      x: {
        0: { side: 'top', label: 'Response Count'} // Top x-axis.
      }
    },
    bar: { groupWidth: "90%" }
  };

  var chart = new google.charts.Bar(document.getElementById('top_x_div'));
  chart.draw(data, options);
};
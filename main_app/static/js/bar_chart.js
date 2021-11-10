google.charts.load('current', {'packages':['bar']});
google.charts.setOnLoadCallback(drawStuff);

function drawStuff() {
  var data = new google.visualization.arrayToDataTable([
    ['Response', 'Rate'],
    ["Strongly Agree", 0],
    ["Agree", 0],
    ["Uncertain", 0],
    ["Disagree", 0],
    ['Strongly Disagree', 0]
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
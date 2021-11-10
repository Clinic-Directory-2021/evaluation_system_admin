
google.charts.load("current", {packages:["corechart"]});
      google.charts.setOnLoadCallback(drawChart);
      
      function drawChart() {
        var evaluation_count = parseInt($("#evaluation_count").val());
        var evaluator_count = parseInt($("#evaluator_count").val());
        var data = google.visualization.arrayToDataTable([
          ['Tag', 'Percent'],
          ['Total Response',evaluation_count],
          ['Total Evaluator',evaluator_count],
        ]);

        var options = {
          title: '',
          pieHole: 0.5,
        };

        var chart = new google.visualization.PieChart(document.getElementById('donutchart'));
        chart.draw(data, options);
      }
    
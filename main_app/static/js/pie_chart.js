



google.charts.load("current", {packages:["corechart"]});
      google.charts.setOnLoadCallback(drawChart);
      function drawChart() {
        var strongly_agree = parseInt($("#strongly_agree").val());
        var agree =  parseInt($("#agree").val());
        var uncertain =  parseInt($("#uncertain").val());
        var disagree =  parseInt($("#disagree").val());
        var strongly_disagree =  parseInt($("#strongly_disagree").val());
        var data = google.visualization.arrayToDataTable([
            ['response', 'percentage'],
            ['Strongly Agree',  strongly_agree],
            ['Agree',  agree],
            ['Uncertain',uncertain],
            ['Disagree', disagree],
            ['Strongly Disagree', strongly_disagree],
        ]);

      var options = {
        legend: 'Agree',
        pieSliceText: 'percentage',
        title: 'Response Pie Chart',
        pieStartAngle: 100,
      };

        var chart = new google.visualization.PieChart(document.getElementById('piechart'));
        chart.draw(data, options);
      }
      // Load the Visualization API and the piechart package.
      google.load('visualization', '1.0', {'packages':['corechart']});
      // Set a callback to run when the Google Visualization API is loaded.
      google.setOnLoadCallback(drawChart);

      // Callback that creates and populates a data table,
      // instantiates the pie chart, passes in the data and
      // draws it.
      function drawChart() {
        // Create the data table.
        var data = google.visualization.arrayToDataTable([
          ['Location', 'Crime Rate', { role: 'style' }],
         ['Palo Alto', 22.45, '#3B596A'],            // RGB value
         ['Mountain View', 22.12, '#427676'],            // English color name
         ['Redwood City', 23.40, '#3F9A82'],
         ['California', 26.58, '#A1CD73'],
         ['National', 28.3, '#ECDB60'],
         ]);
        // Set chart options
        var options = {
            legend: 'none',
            title: 'Property Crime Rate Comparison',
            chartArea: {width: '50%'},
            hAxis: {
              title: 'Incidents Per 1,000 Residents',
              minValue: 0
          }

      };
        // Instantiate and draw our chart, passing in some options.
        var chart = new google.visualization.BarChart(document.getElementById('crime_chart_div'));
        chart.draw(data, options);
        var taxData = new google.visualization.DataTable();
      taxData.addColumn('number', 'X');
      taxData.addColumn('number', 'Tax History');
      taxData.addRows([
        [2006, 8.152],   [2006.3, 9.200],  [2006.6, 10.000],  [2007, 10.482],  [2007.3, 10.400],  [2007.6, 10.460],
        [2008, 10.482],  [2008.3, 10.482],  [2008.6, 10.600],  [2009, 10.881],  [2009.3, 11.200], [2009.6, 11.450],
        [2010, 11.630], [2010.3, 11.630], [2010.6, 11.650], [2011, 11.630], [2011.3, 11.700], [2011.6, 10.800],
        [2012, 10.212], [2012.3, 10.260], [2012.6, 11.100], [2013, 11.280], [2013.3, 11.800], [2013.6, 12.000],
        [2014, 12.569], [2014.3, 12.600], [2014.6, 12.680], [2015, 12.803]
      ]);
      var options = {
        legend: 'none',
        colors: ['#3B596A'],
        hAxis: {
          title: 'Year'
        },
        vAxis: {
          title: 'Property Taxe Rate'
        }

      };
      var taxChart = new google.visualization.LineChart(document.getElementById('tax_chart_div'));
      taxChart.draw(taxData, options);
    }

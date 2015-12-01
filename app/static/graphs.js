// Load the Visualization API and the piechart package.
google.load('visualization', '1.0', {'packages':['corechart','table']});
// Set a callback to run when the Google Visualization API is loaded.
google.setOnLoadCallback(drawChart);
// Callback that creates and populates a data table,
// instantiates the pie chart, passes in the data and
// draws it.
function drawChart() {
    // Create the data table.
    var violent_data = google.visualization.arrayToDataTable([
      ['Location', 'Violent Crime Rate', { role: 'style' }],
     [document.getElementById('crimeInfo').getAttribute('data-city'), parseFloat(document.getElementById('crimeInfo').getAttribute('data-violent-crime-rate')), '#3B596A'],            // RGB value
     ['California', 4.02, '#A1CD73'],
     ['National Median', 3.8, '#ECDB60'],
     ]);
    // Set chart options
    var vio_options = {
        legend: 'none',
        title: 'Violent Crime Rate Comparison',
        chartArea: {width: '50%'},
        hAxis: {
          title: 'Incidents Per 1,000 Residents',
          minValue: 0
      }

    };
    // Instantiate and draw our chart, passing in some options.
    var chart1 = new google.visualization.BarChart(document.getElementById('violent_crime_chart_div'));
    chart1.draw(violent_data, vio_options);

    // Create the data table.
    var prop_data = google.visualization.arrayToDataTable([
      ['Location', 'Violent Crime Rate', { role: 'style' }],
     [document.getElementById('crimeInfo').getAttribute('data-city'), parseFloat(document.getElementById('crimeInfo').getAttribute('data-property-crime-rate')), '#3B596A'],            // RGB value
     ['California', 26.58, '#A1CD73'],
     ['National Median', 27.3, '#ECDB60'],
     ]);
     console.log(document.getElementById('crimeInfo').getAttribute('data-city'));
    // Set chart options
    var prop_options = {
        legend: 'none',
        title: 'Property Crime Rate Comparison',
        chartArea: {width: '50%'},
        hAxis: {
          title: 'Incidents Per 1,000 Residents',
          minValue: 0
      }

    };
    // Instantiate and draw our chart, passing in some options.
    var chart2 = new google.visualization.BarChart(document.getElementById('property_crime_chart_div'));
    chart2.draw(prop_data, prop_options);


    // Create the data table.
    var mile_data = google.visualization.arrayToDataTable([
      ['Location', 'Crimes Per Square Mile', { role: 'style' }],
     [document.getElementById('crimeInfo').getAttribute('data-city'), parseFloat(document.getElementById('crimeInfo').getAttribute('data-crime-per-mile')), '#3B596A'],           // RGB value
     ['California', 89, '#A1CD73'],
     ['National Median', 37.9, '#ECDB60'],
     ]);
    // Set chart options
    var mile_options = {
        legend: 'none',
        title: 'Crimes Per Square Mile Comparison',
        chartArea: {width: '50%'},
        hAxis: {
          minValue: 0
      }

    };
    // Instantiate and draw our chart, passing in some options.
    var chart3 = new google.visualization.BarChart(document.getElementById('mile_crime_chart_div'));
    chart3.draw(mile_data, mile_options);


    var taxData = new google.visualization.DataTable();
  taxData.addColumn('number', 'X');
  taxData.addColumn('number', 'Tax Rate');
  taxData.addRows([
    [2010, parseInt(document.getElementById('taxData').getAttribute('data-2010-tax')) / parseInt(document.getElementById('taxAssessData').getAttribute('data-2010-tax'))],
    [2011, parseInt(document.getElementById('taxData').getAttribute('data-2011-tax')) / parseInt(document.getElementById('taxAssessData').getAttribute('data-2011-tax'))],
    [2012, parseInt(document.getElementById('taxData').getAttribute('data-2012-tax')) / parseInt(document.getElementById('taxAssessData').getAttribute('data-2012-tax'))],
    [2013, parseInt(document.getElementById('taxData').getAttribute('data-2013-tax')) / parseInt(document.getElementById('taxAssessData').getAttribute('data-2013-tax'))],
    [2014, parseInt(document.getElementById('taxData').getAttribute('data-2014-tax')) / parseInt(document.getElementById('taxAssessData').getAttribute('data-2014-tax'))]
  ]);
  var options = {
    legend: 'none',
    colors: ['#3B596A'],
    title: 'Tax Rate Per Year',
    chartArea:{width: '50%'},
    hAxis: {
      title: 'Year'
    }
  };
  var taxChart = new google.visualization.LineChart(document.getElementById('tax_chart_div'));
  taxChart.draw(taxData, options);

  Number.prototype.format = function(n, x) {
    var re = '\\d(?=(\\d{' + (x || 3) + '})+' + (n > 0 ? '\\.' : '$') + ')';
    return this.toFixed(Math.max(0, ~~n)).replace(new RegExp(re, 'g'), '$&,');
  };

  var taxTableData = new google.visualization.DataTable();
  taxTableData.addColumn('number', 'Year');
  taxTableData.addColumn('string', 'Property Tax');
  taxTableData.addColumn('string', 'Tax Assessment');
  taxTableData.addRows([
    [2014, "$"+parseInt(document.getElementById('taxData').getAttribute('data-2014-tax')).format() , "$"+parseInt(document.getElementById('taxAssessData').getAttribute('data-2014-tax')).format()],
    [2013, "$"+parseInt(document.getElementById('taxData').getAttribute('data-2013-tax')).format() , "$"+parseInt(document.getElementById('taxAssessData').getAttribute('data-2013-tax')).format()],
    [2012, "$"+parseInt(document.getElementById('taxData').getAttribute('data-2012-tax')).format() , "$"+parseInt(document.getElementById('taxAssessData').getAttribute('data-2012-tax')).format()],
    [2011, "$"+parseInt(document.getElementById('taxData').getAttribute('data-2011-tax')).format() , "$"+parseInt(document.getElementById('taxAssessData').getAttribute('data-2011-tax')).format()],
    [2010, "$"+parseInt(document.getElementById('taxData').getAttribute('data-2010-tax')).format() , "$"+parseInt(document.getElementById('taxAssessData').getAttribute('data-2010-tax')).format()]
  ]);

  var taxTable = new google.visualization.Table(document.getElementById('tax_table_div'));
  taxTable.draw(taxTableData, {showRowNumber: false, width:'100%', height: '100%'});
};

$(window).resize(function(){
  drawChart();
});

$(document).ready(function(){
  drawChart();
});

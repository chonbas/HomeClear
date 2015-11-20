$(document).ready(function(){
  $(".reportTabs").hide();
  $("#basicInfo").show();

  $("#schoolInfoBtn").click(function(){
    $("#basicInfo").hide();
    $("#crimeInfo").hide();
    $("#geoInfo").hide();
    $("#miscInfo").hide();
    $("#schoolInfo").show();
  });

  $("#basicInfoBtn").click(function(){
    $("#basicInfo").show();
    $("#crimeInfo").hide();
    $("#geoInfo").hide();
    $("#miscInfo").hide();
    $("#schoolInfo").hide();
  });

  $("#crimeInfoBtn").click(function(){
    $("#basicInfo").hide();
    $("#crimeInfo").show();
    $("#geoInfo").hide();
    $("#miscInfo").hide();
    $("#schoolInfo").hide();
  });

  $("#geoInfoBtn").click(function(){
    $("#basicInfo").hide();
    $("#crimeInfo").hide();
    $("#geoInfo").show();
    $("#miscInfo").hide();
    $("#schoolInfo").hide();
  });

  $("#miscInfoBtn").click(function(){
    $("#basicInfo").hide();
    $("#crimeInfo").hide();
    $("#geoInfo").hide();
    $("#miscInfo").show();
    $("#schoolInfo").hide();
  });
});

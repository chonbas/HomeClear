$(document).ready(function(){
  $(".reportTabs").hide();
  $("#basicInfo").show();
});

$("#schoolInfoBtn a").click(function(){
  $("#basicInfo").hide();
  $("#crimeInfo").hide();
  $("#geoInfo").hide();
  $("#miscInfo").hide();
  $("#schoolInfo").show();
});

$("#basicInfoBtn a").click(function(){
  $("#basicInfo").show();
  $("#crimeInfo").hide();
  $("#geoInfo").hide();
  $("#miscInfo").hide();
  $("#schoolInfo").hide();
});

$("#crimeInfoBtn a").click(function(){
  $("#basicInfo").hide();
  $("#crimeInfo").show();
  $("#geoInfo").hide();
  $("#miscInfo").hide();
  $("#schoolInfo").hide();
});

$("#geoInfoBtn a").click(function(){
  $("#basicInfo").hide();
  $("#crimeInfo").hide();
  $("#geoInfo").show();
  $("#miscInfo").hide();
  $("#schoolInfo").hide();
});

$("#miscInfoBtn a").click(function(){
  $("#basicInfo").hide();
  $("#crimeInfo").hide();
  $("#geoInfo").hide();
  $("#miscInfo").show();
  $("#schoolInfo").hide();
});

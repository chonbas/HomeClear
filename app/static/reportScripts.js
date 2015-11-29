$(document).ready(function(){
  $(".reportTabs").hide();
  $("#basicInfo").show();
});

$("#schoolInfoBtn a").click(function(){
  $("#basicInfo").hide();
  $("#crimeInfo").hide();
  $("#taxInfo").hide();
  $("#geoInfo").hide();
  $("#miscInfo").hide();
  $("#schoolInfo").show();
});

$("#basicInfoBtn a").click(function(){
  $("#basicInfo").show();
  $("#taxInfo").hide();
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
  $("#taxInfo").hide();
  $("#schoolInfo").hide();
});

$("#geoInfoBtn a").click(function(){
  $("#basicInfo").hide();
  $("#crimeInfo").hide();
  $("#geoInfo").show();
  $("#taxInfo").hide();
  $("#miscInfo").hide();
  $("#schoolInfo").hide();
});

$("#miscInfoBtn a").click(function(){
  $("#basicInfo").hide();
  $("#crimeInfo").hide();
  $("#geoInfo").hide();
  $("#miscInfo").show();
  $("#schoolInfo").hide();
  $("#taxInfo").hide();
});

$("#taxInfoBtn a").click(function(){
  $("#basicInfo").hide();
  $("#crimeInfo").hide();
  $("#geoInfo").hide();
  $("#taxInfo").show();
  $("#miscInfo").hide();
  $("#schoolInfo").hide();
});

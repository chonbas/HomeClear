$(document).ready(function(){
  $("#hideFilters").hide();
  $("#showFilters").show();
  $('#submit').hide();
  $("#filters").hide();


  $("#showFilters").click(function(){
    $("#showFilters").hide();
    $("#hideFilters").show();
    $("#filters").show();
  });

  $("#hideFilters").click(function(){
    $("#hideFilters").hide();
    $("#showFilters").show();
    $("#filters").hide();
  });

});

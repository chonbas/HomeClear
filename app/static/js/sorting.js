$("#SortPriceLoHi").click(function(){
  tinysort('ul#listings>li',{attr:"data-price"});
});
$("#SortPriceHiLo").click(function(){
  tinysort('ul#listings>li',{attr:"data-price",order:"desc"});
});
$("#SortSqFtLoHi").click(function(){
  tinysort('ul#listings>li',{attr:"data-sqft"});
});
$("#SortSqFtHiLo").click(function(){
  tinysort('ul#listings>li',{attr:"data-sqft",order:"desc"});
});
$("#SortBedLoHi").click(function(){
  tinysort('ul#listings>li',{attr:"data-bedrooms"});
});
$("#SortBedHiLo").click(function(){
  tinysort('ul#listings>li',{attr:"data-bedrooms",order:"desc"});
});
$("#SortBathLoHi").click(function(){
  tinysort('ul#listings>li',{attr:"data-bathrooms"});
});
$("#SortBathHiLo").click(function(){
  tinysort('ul#listings>li',{attr:"data-bathrooms",order:"desc"});
});
$("#SortLotSqFtLoHi").click(function(){
  tinysort('ul#listings>li',{attr:"data-sqft"});
});
$("#SortLotSqFtHiLo").click(function(){
  tinysort('ul#listings>li',{attr:"data-sqft",order:"desc"});
});

function initMap() {
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 15,
    center: {lat: 37.4411882, lng: -122.1454357}
  });

    var geocoder = new google.maps.Geocoder();
    var address = document.getElementById('address').innerHTML;
    var lati = parseFloat(document.getElementById('coords').getAttribute("data-lat"));
    var longi = parseFloat(document.getElementById('coords').getAttribute("data-lng"));
    var pos = {'lat': lati, 'lng':longi};
    map.setCenter(pos);
    var marker = new google.maps.Marker({
      map: map,
      position: pos//results[0].geometry.location
    });
};

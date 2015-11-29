function initMap() {
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 13,
    center: {lat: 37.4411882, lng: -122.1454357}
  });

    var geocoder = new google.maps.Geocoder();
    var count = 1;
    $('.listingInfo').each(function(i, obj) {
      var address = this.getAttribute("data-address");
      geocoder.geocode({'address': address}, function(results, status) {
      if (status === google.maps.GeocoderStatus.OK) {
        map.setCenter(results[0].geometry.location);
        var marker = new google.maps.Marker({
          map: map,
          label: ""+count,
          position: results[0].geometry.location,
        });
      } else {
        console.log('Geocode was not successful for the following reason: ' + status);
      }
      count++;
    });

  });
};

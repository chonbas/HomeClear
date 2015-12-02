function initMap() {
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 13,
    center: {lat: 37.4411882, lng: -122.1454357}
  });

    var geocoder = new google.maps.Geocoder();
    $('.listingInfo').each(function(i, obj) {
      var address = this.getAttribute("data-address");
      var lati = parseFloat(this.getAttribute("data-lat"));
      var longi = parseFloat(this.getAttribute("data-lng"));
      var image = "/static/icons/"+this.getAttribute('data-color')+"/number_" + this.getAttribute("data-index") + ".png";
      var pos = {'lat': lati, 'lng':longi};
      map.setCenter(pos);
      var marker = new google.maps.Marker({
        map: map,
        icon: image,
        position: pos,
      });
    });
};

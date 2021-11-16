function initMap() {
  var latlng = new google.maps.LatLng(35.702047, 139.450598);
  var opts = {
    zoom: 14,
    center: latlng,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };
  var map = new google.maps.Map(document.getElementById("map"), opts);

  var m_latlng1 = new google.maps.LatLng(35.702047, 139.450598);
  var marker1 = new google.maps.Marker({
    position: m_latlng1,
    map: map
  });
}

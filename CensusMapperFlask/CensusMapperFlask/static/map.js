function main(zoomval, lat, lng) {

  zoomval = typeof zoomval === 'undefined' ? 4 : zoomval;
  lat = typeof lat === 'undefined' ? 40 : lat;
  lng = typeof lng === 'undefined' ? -98.5 : lng;
  
  // Define the map options
  var cartodbMapOptions = {
    zoom: zoomval,
    center: new google.maps.LatLng(lat, lng),
    disableDefaultUI: true,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };
  
  // Init the map
  var map = new google.maps.Map(document.getElementById("map"),cartodbMapOptions);
  
  // move zoom buttons to lower right
  map.setOptions({zoomControl: true,
    zoomControlOptions: {
      style: google.maps.ZoomControlStyle.SMALL,
      position: google.maps.ControlPosition.RIGHT_BOTTOM
    }
  });
  
  // add search bar to upper right
  add_search_box(map);
  
  // Define the map style to appear very minimalistic and washed out
  var mapStyle = [{stylers: [{ saturation: -65 }, { gamma: 1 }] }, 
    {featureType: "administrative", stylers: [{ saturation: -75 }, { gamma: 2.26 }] }, 
    {featureType: "water", elementType: "labels", stylers: [{ visibility: "off" }] }, 
    {featureType: "administrative.locality", elementType: "labels.text", stylers: [{ visibility: 'off' }] },
    {featureType: "administrative.locality", elementType: "labels.icon", stylers: [{ visibility: 'off' }] },
    {featureType: "administrative.neighborhood", stylers: [{ visibility: 'off' }] }, 
    {featureType: "administrative.land_parcel", stylers: [{ visibility: 'off' }] }, 
    {featureType: "road", stylers: [{ visibility: "simplified" }, { saturation: -99 }, { gamma: 2.22 }] }, 
    {featureType: "poi", elementType: "labels", stylers: [{ visibility: "off" }] }, 
    {featureType: "landscape", elementType: "labels", stylers: [{ visibility: "off" }] }, 
    {featureType: "road.arterial", stylers: [{ visibility: 'off' }] }, 
    {featureType: "road.local", elementType: "labels", stylers: [{ visibility: 'off' }] }, 
    {featureType: "transit", stylers: [{ visibility: 'off' }] }, 
    {featureType: "road", elementType: "labels", stylers: [{ visibility: 'off' }] }, 
    {featureType: "poi", stylers: [{ saturation: -55 }] } 
  ];
  
  map.setOptions({styles: mapStyle});
  
  return map;
  
};

function add_tiles(map, sqlquery, cartocss) {
  
  cartodb.createLayer(map, {
    user_name: 'censusmapper',
    type: 'cartodb',
    sublayers: [{
      sql: sqlquery,
      cartocss: cartocss
    }]
  })
  .addTo(map)
  
};

function add_search_box(map) {
  
  var input = document.getElementById('pac-input');
  map.controls[google.maps.ControlPosition.TOP_RIGHT].push(input);
  
  var searchBox = new google.maps.places.SearchBox(input);
  
  google.maps.event.addListener(searchBox, 'places_changed', function() {
    var places = searchBox.getPlaces();
    var place = places[0];
    if (place.geometry.viewport) {
      map.fitBounds(place.geometry.viewport);
      if (map.getZoom() > 8) {
        map.setZoom(8);
      }
    } else {
      map.setCenter(place.geometry.location);
      map.setZoom(12);
    }
  })
}

function add_legend(innerHTML) {
  
  if (typeof innerHTML !== 'undefined') {
    // Create a div to hold the control.
    var controlDiv = document.createElement('div');
    
    // Set CSS styles for the DIV containing the control
    // Setting padding to 5 px will offset the control
    // from the edge of the map.
    controlDiv.style.padding = '10px';
    
    // Set CSS for the control border.
    var controlUI = document.createElement('div');
    controlUI.style.backgroundColor = 'white';
    controlUI.style.borderStyle = 'solid';
    controlUI.style.borderWidth = '1px';
    controlUI.style.borderColor = '#DDDDDD';
    controlUI.style.cursor = 'pointer';
    controlUI.style.textAlign = 'left';
    controlDiv.appendChild(controlUI);
    
    // Set CSS for the control interior.
    var controlText = document.createElement('div');
    controlText.style.fontFamily = 'Helvetica,Arial,sans-serif';
    controlText.style.fontSize = '14px';
    controlText.style.paddingTop = '5px';
    controlText.style.paddingBottom = '5px';
    controlText.style.paddingLeft = '5px';
    controlText.style.paddingRight = '5px';
    controlText.innerHTML = innerHTML;
    controlUI.appendChild(controlText);
    
    map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(controlDiv);
  }
  
};

function adjust_height() {
  var height = window.innerHeight;
  document.getElementById("map").style.height = height - 56 + 'px';
};


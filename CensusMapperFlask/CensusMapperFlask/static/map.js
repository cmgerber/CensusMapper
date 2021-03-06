var layers=[];
var markersArray=[];

function main(zoomval, lat, lng) {

  //zoomval = typeof zoomval === 'undefined' ? 4 : zoomval;
  //lat = typeof lat === 'undefined' ? 40 : lat;
  //lng = typeof lng === 'undefined' ? -98.5 : lng;
  
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
  
  cartodb.createLayer(map, {
    user_name: 'censusmapper',
    type: 'cartodb',
    sublayers: [{
      sql: 'select * from censusgeo',
      cartocss: '#censusgeo {polygon-opacity: 0; line-opacity:0}'
    }]
  })
  .addTo(map)
  .on('done', function(layer) {
    layers.push(layer);
    var sublayer = layer.getSubLayer(0);
    sublayer.remove();
  });
  
  return map;
  
};

function add_tiles(sqlquery, cartocss) {
  
  var layer = layers[0];
  
  layer.createSubLayer({
      sql: sqlquery,
      cartocss: cartocss
    });
  
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
};

function add_gmaps_places(map,keyword) {
  
  var service = new google.maps.places.PlacesService(map);
  
  function performSearch() {
    var request = {
      bounds: map.getBounds(),
      keyword: keyword
    };
    service.radarSearch(request, callback);
  };
  
  function callback(results, status) {
    if (status != google.maps.places.PlacesServiceStatus.OK) {
      alert(status);
      return;
    }
    for (var i = 0, result; result = results[i]; i++) {
      createMarker(result);
    }
  };
  
  function createMarker(place) {
    var marker = new google.maps.Marker({
      map: map,
      position: place.geometry.location,
      icon: {
        // Star
        path: 'M 0,-24 6,-7 24,-7 10,4 15,21 0,11 -15,21 -10,4 -24,-7 -6,-7 z',
        fillColor: '#ffff00',
        fillOpacity: 1,
        scale: 1/4,
        strokeColor: '#bd8d2c',
        strokeWeight: 1
      }
    });
    markersArray.push(marker);
  };
  
  remove_gmaps_places();
  performSearch();
  //google.maps.event.addListener(map, 'bounds_changed', performSearch);
};

function remove_gmaps_places() {
  for (var i = 0; i < markersArray.length; i++ ) {
    markersArray[i].setMap(null);
  }
  markersArray = [];
}

function remove_legend() {
  // delete old legend if necessary
  var oldlegend = document.getElementById('legendbox');
  if (oldlegend) {
    oldlegend.parentNode.removeChild(oldlegend);
  };
};

function add_legend(titletext, colorarray, valuearray) {
  
  // delete old legend if necessary
  remove_legend();
  
  // Create a div to hold the control.
  var controlDiv = document.createElement('div');
  controlDiv.setAttribute('id', 'legendbox');
  
  // add legend div
  var legendDiv = document.createElement('div');
  legendDiv.setAttribute('id', 'my-legend');
  controlDiv.appendChild(legendDiv);
  
  // add title
  var titleDiv = document.createElement('div');
  titleDiv.setAttribute('id', 'legend-title');
  titleDiv.innerHTML = titletext;
  legendDiv.appendChild(titleDiv);
  
  // add scale
  var scaleDiv = document.createElement('div');
  scaleDiv.setAttribute('id', 'legend-scale');
  legendDiv.appendChild(scaleDiv);
  
  // add labels container
  var labelDiv = document.createElement('ul');
  labelDiv.setAttribute('id', 'legend-labels');
  scaleDiv.appendChild(labelDiv);
  
  // add individual labels
  for (var i = 0; i < valuearray.length; i++) {
    var labelItem = document.createElement('li');
    labelItem.innerHTML = "<span style='background:rgb("+colorarray[i+1][1][0]+","+colorarray[i+1][1][1]+","+colorarray[i+1][1][2]+")'></span>"+valuearray[i]
    labelDiv.appendChild(labelItem)
  }
  
  map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(controlDiv);
  
};

function adjust_height() {
  var height = window.innerHeight;
  document.getElementById("map").style.height = height - 56 + 'px';
};


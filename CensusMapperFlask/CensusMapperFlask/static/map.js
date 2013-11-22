function main(zoomval, lat, lng) {
  
  // Define the map options
  var cartodbMapOptions = {
    zoom: zoomval,
    center: new google.maps.LatLng(lat, lng),
    disableDefaultUI: true,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };
  
  // Init the map
  var map = new google.maps.Map(document.getElementById("map"),cartodbMapOptions);
  map.setOptions({zoomControl: true,
    zoomControlOptions: {
      style: google.maps.ZoomControlStyle.SMALL,
      position: google.maps.ControlPosition.RIGHT_BOTTOM
    }
  });
  map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(add_legend());
  
  // Define the map styles
  var mapStyle = [{stylers: [{ saturation: -65 }, { gamma: 1.52 }] }, 
    {featureType: "administrative", stylers: [{ saturation: -95 }, { gamma: 2.26 }] }, 
    {featureType: "water", elementType: "labels", stylers: [{ visibility: "off" }] }, 
    {featureType: "administrative.locality", stylers: [{ visibility: 'off' }] }, 
    {featureType: "road", stylers: [{ visibility: "simplified" }, { saturation: -99 }, { gamma: 2.22 }] }, 
    {featureType: "poi", elementType: "labels", stylers: [{ visibility: "off" }] }, 
    {featureType: "road.arterial", stylers: [{ visibility: 'off' }] }, 
    {featureType: "road.local", elementType: "labels", stylers: [{ visibility: 'off' }] }, 
    {featureType: "transit", stylers: [{ visibility: 'off' }] }, 
    {featureType: "road", elementType: "labels", stylers: [{ visibility: 'off' }] }, 
    {featureType: "poi", stylers: [{ saturation: -55 }] } 
  ];
  
  map.setOptions({styles: mapStyle});
  
  // Tile style
  var cartocss = "#censusgeo { polygon-fill: rgb(178,226,226); line-width: .1; line-color: #444444; polygon-opacity: 0; line-opacity: 0;[ measure <= 1.00 ] { polygon-fill: rgb(179,0,0)}[ measure <= 0.40 ] { polygon-fill: rgb(227,51,74)}[ measure <= 0.25 ] { polygon-fill: rgb(252,89,141)}[ measure <= 0.15 ] { polygon-fill: rgb(253,138,204)}[ measure <= 0.05 ] { polygon-fill: rgb(254,217,240)} [zoom <= 4][geotype = 'state'] { polygon-opacity: 0.8; line-opacity: 1; } [zoom > 4][zoom <= 8][geotype = 'county'] { polygon-opacity: 0.8; line-opacity: 1; } [zoom > 8][geotype = 'tract'] { polygon-opacity: 0.8; line-opacity: 1; }}";
  
  var sqlquery = "SELECT a.cartodb_id,a.geotype,a.the_geom_webmercator, sum(case when b.fieldid in ('B03002012') then cast(b.value as float) else 0 end)/(sum(case when b.fieldid in ('B01001001') then cast(b.value as float) else 0 end) + 1) measure FROM censusgeo a JOIN censusdata b ON a.fipscode = b.fipscode GROUP BY a.cartodb_id, a.geotype, a.the_geom_webmercator";
  
  cartodb.createLayer(map, {
  user_name: 'censusmapper',
  type: 'cartodb',
  sublayers: [{
  sql: sqlquery,
  cartocss: cartocss
  }]
  })
  .addTo(map) // add the layer to our map which already contains 1 sublayer
  
  };

function add_legend() {
  
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
  controlUI.style.borderColor = '#dddddd';
  controlUI.style.cursor = 'pointer';
  controlUI.style.textAlign = 'center';
  controlUI.title = 'Click to set the map to Home';
  controlDiv.appendChild(controlUI);
  
  // Set CSS for the control interior.
  var controlText = document.createElement('div');
  controlText.style.fontFamily = 'Arial,sans-serif';
  controlText.style.fontSize = '12px';
  controlText.style.paddingLeft = '4px';
  controlText.style.paddingRight = '4px';
  controlText.innerHTML = '<strong>Home</strong>';
  controlUI.appendChild(controlText);

  return controlDiv
  
};

function adjust_height() {
  var height = window.innerHeight;
  document.getElementById("map").style.height = height - 56 + 'px';
};


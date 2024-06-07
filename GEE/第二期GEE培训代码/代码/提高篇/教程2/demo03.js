//https://code.earthengine.google.com/adaa13f8b35aed1c6834a95dba885ba8

// https://developers.google.com/maps/documentation/javascript/style-reference
var DARK = [
  {
    elementType: 'geometry', 
    stylers: [{color: '#242f3e'}]
  },
  {
    elementType: 'labels.text.stroke', 
    stylers: [{color: '#242f3e'}]
  },
  {
    elementType: 'labels.text.fill', 
    stylers: [{color: '#746855'}]},
  {
    featureType: 'administrative.locality',
    elementType: 'labels.text.fill',
    stylers: [{color: '#d59563'}]
  },
  {
    featureType: 'poi',
    elementType: 'labels.text.fill',
    stylers: [{color: '#d59563'}]
  },
  {
    featureType: 'poi.park',
    elementType: 'geometry',
    stylers: [{color: '#263c3f'}]
  },
  {
    featureType: 'poi.park',
    elementType: 'labels.text.fill',
    stylers: [{color: '#6b9a76'}]
  },
  {
    featureType: 'road',
    elementType: 'geometry',
    stylers: [{color: '#38414e'}]
  },
  {
    featureType: 'road',
    elementType: 'geometry.stroke',
    stylers: [{color: '#212a37'}]
  },
  {
    featureType: 'road',
    elementType: 'labels.text.fill',
    stylers: [{color: '#9ca5b3'}]
  },
  {
    featureType: 'road.highway',
    elementType: 'geometry',
    stylers: [{color: '#746855'}]
  },
  {
    featureType: 'road.highway',
    elementType: 'geometry.stroke',
    stylers: [{color: '#1f2835'}]
  },
  {
    featureType: 'road.highway',
    elementType: 'labels.text.fill',
    stylers: [{color: '#f3d19c'}]
  },
  {
    featureType: 'transit',
    elementType: 'geometry',
    stylers: [{color: '#2f3948'}]
  },
  {
    featureType: 'transit.station',
    elementType: 'labels.text.fill',
    stylers: [{color: '#d59563'}]
  },
  {
    featureType: 'water',
    elementType: 'geometry',
    stylers: [{color: '#17263c'}]
  },
  {
    featureType: 'water',
    elementType: 'labels.text.fill',
    stylers: [{color: '#515c6d'}]
  },
  {
    featureType: 'water',
    elementType: 'labels.text.stroke',
    stylers: [{color: '#17263c'}]
  }
];

var GRAY = [
  { 
    stylers: [ { saturation: -100 } ]
  },
  { 
    elementType: 'labels',
    stylers: [ { lightness: 20 } ]
  },
  { 
    featureType: 'road',
    elementType: 'geometry',
    stylers: [ { visibility: 'simplified' } ]
  },
  { 
    featureType: 'road',
    elementType: 'labels',
    stylers: [ { visibility: 'off' } ]
  },
  { 
    elementType: 'labels.icon',
    stylers: [ { visibility: 'off' } ]
  },
  { 
    featureType: 'poi',
    elementType: 'all',
    stylers: [ { visibility: 'off' }]
  }
];

Map.setOptions("SATELLITE",{"DARK": DARK, "GRAY": GRAY});

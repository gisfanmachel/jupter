//代码链接：https://code.earthengine.google.com/afca0ad6613ccbfa8fdb27315538728c

var srtm = ee.Image('USGS/SRTMGL1_003');
var center = ee.Geometry.Point([116.40766601562495, 39.903161161259945]);
Map.centerObject(center, 6);
var visParam = {
  min: 0,
  max: 6000, 
  palette: ["0000ff", "00ff00", "30b855", "ff0000", "ffff00"]
};
Map.addLayer(srtm, visParam, "dem");
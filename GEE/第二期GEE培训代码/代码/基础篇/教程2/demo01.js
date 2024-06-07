//链接：https://code.earthengine.google.com/c7192e4e2e16b3574454fd49155e0863

var center = /* color: #d63000 */ee.Geometry.Point([115.12226562499995, 38.29398766489544]);
var zoom = 9;
var leftMap = ui.Map();
leftMap.centerObject(center, zoom);
var rightMap = ui.Map();
rightMap.centerObject(center, zoom);
leftMap.setControlVisibility(false);
rightMap.setControlVisibility(false);
leftMap.setControlVisibility({zoomControl: true});
var linker = new ui.Map.Linker([leftMap, rightMap]);
var splitPanel = ui.SplitPanel({
  firstPanel: leftMap,
  secondPanel: rightMap,
  orientation: 'horizontal',
  wipe: true
});
ui.root.clear();
ui.root.add(splitPanel);

//RGB
var landsat = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
                .filterDate('2017-01-01', '2018-01-01')
                .median();
landsat = landsat.addBands(landsat.normalizedDifference(['B5', 'B4']).rename("NDVI"));
var vis = {bands: ['B4', 'B3', 'B2'], min: 0, max: 3000};
leftMap.addLayer(landsat, vis, "rgb");

//NDVI
var visNDVI = {
  min: 0,
  max: 1,
  palette: 'FFFFFF,CE7E45,DF923D,F1B555,FCD163,99B718,74A901,66A000,529400,' +
      '3E8601,207401,056201,004C00,023B01,012E01,011D01,011301'
};
rightMap.addLayer(landsat.select("NDVI"), visNDVI, 'NDVI');
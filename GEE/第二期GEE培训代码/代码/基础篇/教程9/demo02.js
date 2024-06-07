//代码链接：https://code.earthengine.google.com/d9c638abe6c820555958f86faab4effa


Map.setOptions("SATELLITE");
var image = ee.Image("LANDSAT/LC08/C01/T1_TOA/LC08_123037_20180611");
Map.centerObject(image, 7);
var visParam = {
  min: 0, 
  max: 0.3,
  bands: ["B4", "B3", "B2"]
};
Map.addLayer(image, visParam, "rawIamge");
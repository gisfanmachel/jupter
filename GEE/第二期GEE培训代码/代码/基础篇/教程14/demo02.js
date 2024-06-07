//代码链接：https://code.earthengine.google.com/4ced5efab20131311a04982fe45e28b7


//reduce image bands to single band
Map.setOptions("SATELLITE");
var image = ee.Image("LANDSAT/LC08/C01/T1_TOA/LC08_123037_20180611")
              .select("B[1-7]");
Map.centerObject(image, 7);
var visParam = {
  min: 0, 
  max: 0.3,
  bands: ["B4", "B3", "B2"]
};
Map.addLayer(image, visParam, "rawIamge");

var mean = image.reduce(ee.Reducer.mean());
print("image reduce value is: ", mean);
Map.addLayer(mean, {}, "meanImage");
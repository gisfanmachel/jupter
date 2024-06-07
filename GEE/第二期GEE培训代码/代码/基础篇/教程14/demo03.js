//代码链接：https://code.earthengine.google.com/947474fa6357871e3f6b9a0b31fe0510


var roi = /* color: #d63000 */ee.Geometry.Point([114.87507324218745, 33.405947169322516]),
    l8 = ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA");
    
Map.centerObject(roi, 7);
Map.setOptions("SATELLITE");
var sCol = l8.filterDate("2018-1-1", "2019-1-1")
             .filterBounds(roi)
             .map(ee.Algorithms.Landsat.simpleCloudScore)
             .map(function(image) {
               return image.updateMask(image.select("cloud").lte(10));
             })
             .select("B[1-7]");
  
var mean = sCol.mean();
print("imageCollection to image", mean);
// 和上面的结果一样，上面的写法只是GEE将这个方法封装了一下
// var mean = sCol.reduce(ee.Reducer.mean());
var visParam = {
  min: 0, 
  max: 0.3,
  bands: ["B4", "B3", "B2"]
};
Map.addLayer(mean, visParam, "meanImage");
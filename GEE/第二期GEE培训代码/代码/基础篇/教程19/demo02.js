//代码链接：https://code.earthengine.google.com/978b48b39785c8e78891c0c103afc65c

//导入外部的库
var lib = require("users/wangweihappy0/myTraining:training01/require/lib");
var geometry = /* color: #d63000 */ee.Geometry.Polygon(
        [[[115.73063354492183, 38.0283609762046],
          [115.83225708007808, 38.02727921876993],
          [115.8336303710937, 38.09756022187834],
          [115.73338012695308, 38.09539873615892]]]);
var l8NDVI = ee.ImageCollection("LANDSAT/LC08/C01/T1_RT_TOA")
              .filterDate("2018-2-1", "2018-5-1")
              .filterBounds(geometry)
              .map(lib.l8NDVI) //调用lib中的NDVI方法
              .select("NDVI")
              .mosaic()
              .clip(geometry);
Map.centerObject(geometry, 11);
var visParam = {
  min: -0.2, 
  max: 0.8,
  palette: 'FFFFFF, CE7E45, DF923D, F1B555, FCD163, 99B718, 74A901, 66A000, 529400,' +
    '3E8601, 207401, 056201, 004C00, 023B01, 012E01, 011D01, 011301'
};
print(l8NDVI);
Map.addLayer(l8NDVI, visParam, "NDVI");
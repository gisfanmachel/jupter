//代码链接：https://code.earthengine.google.com/cb2135ad59bd77d1b2a6a661615a0717


//ee.Filter.inList
var roi = /* color: #ffc82d */ee.Geometry.Polygon(
        [[[116.39748737502077, 39.8337451562542],
          [116.56228229689577, 39.8358542417612],
          [116.55678913283327, 39.95596503308958],
          [116.40847370314577, 39.94964866100854]]]);
Map.centerObject(roi, 8);  

var sCol = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA')
             .filter(ee.Filter.inList({
               leftField: "system:index", 
               rightValue: ["LC08_123032_20170115", "LC08_123032_20180118"]
             }));
             
print(sCol);
var image = sCol.mean();
var visParam = {
  min: 0, 
  max: 0.3,
  bands: ["B4", "B3", "B2"]
};
Map.addLayer(image, visParam, "mosaicImage");
Map.addLayer(roi, {color: "red"}, "roi");
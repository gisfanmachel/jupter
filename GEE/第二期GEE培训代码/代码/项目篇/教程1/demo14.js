//代码链接：https://code.earthengine.google.com/a6205d1e98581649a8f8b0d6b6580bfd

//remap
var roi = /* color: #999900 */ee.Geometry.Polygon(
        [[[116.21437502022764, 39.62355024325724],
          [116.82960939522764, 39.75881346356145],
          [116.75270509835264, 40.213367999414956],
          [115.97816896554014, 40.17140672221596]]]);
Map.centerObject(roi, 8);

var landCover = ee.ImageCollection("MODIS/006/MCD12Q1")
                  .select("LC_Type1")
                  .first()
                  .clip(roi);
                  
Map.addLayer(landCover);

var newLandCover = landCover.remap({
  from: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17],
  to: [1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2]
});
Map.addLayer(newLandCover);
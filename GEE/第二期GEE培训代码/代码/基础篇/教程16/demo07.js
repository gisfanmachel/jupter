//代码链接：https://code.earthengine.google.com/e4ef71603e32f2d02acbbba9aeec897b


var l8 = ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA");
var roi = /* color: #d63000 */ee.Geometry.Polygon(
        [[[116.33401967309078, 39.8738616709093],
          [116.46882950954137, 39.87808443916675],
          [116.46882978521751, 39.94772261856061],
          [116.33952185055819, 39.943504136461144]]]);
var selectCol = l8.filterBounds(roi)
                  .filterDate("2017-1-1", "2017-12-31")
                  .map(ee.Algorithms.Landsat.simpleCloudScore)
                  .sort("system:time_start");
                  
var l8Img = selectCol.mosaic().clip(roi);
Map.addLayer(l8Img, {bands: ["B3", "B2", "B1"], min:0, max:0.3}, "l8");
Map.centerObject(roi, 12);

var exportCol = selectCol.map(function(img) {
  img = img.clip(roi);
  return img.multiply(768).uint8();
});
print("image count is: ", exportCol.size());
//导出指定区域的时间序列的rgb影像，帧率12，分辨率30，区域是roi区域
Export.video.toDrive({
  collection: exportCol.select(["B3", "B2", "B1"]),
  description: "Drive-exportL8Video",
  fileNamePrefix: "l8Video",
  folder: "training01",
  scale: 30,
  framesPerSecond: 12,
  region: roi
});
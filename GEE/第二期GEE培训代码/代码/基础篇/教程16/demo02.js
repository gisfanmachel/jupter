//代码链接：https://code.earthengine.google.com/b152149a698551c80b73f54ff1a5ec17

var l8 = ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA");
var roi = /* color: #d63000 */ee.Geometry.Polygon(
      [[[116.33401967309078, 39.8738616709093],
        [116.46882950954137, 39.87808443916675],
        [116.46882978521751, 39.94772261856061],
        [116.33952185055819, 39.943504136461144]]]);
var selectCol = l8.filterBounds(roi)
                 .filterDate("2017-1-1", "2018-6-1")
                 .map(ee.Algorithms.Landsat.simpleCloudScore)
                 .map(function(img) {
                    img = img.updateMask(img.select("cloud").lt(1));
                    return img;
                 })
                 .sort("system:time_start");
var l8Img = selectCol.mosaic().clip(roi);
Map.addLayer(l8Img, {bands: ["B3", "B2", "B1"], min:0, max:0.3}, "l8");
Map.centerObject(roi, 12);
Map.addLayer(roi, {color: "red"}, "roi");

// To Drive
//导出文件到Drive，名称为l8Img，分辨率30米，区域是roi区域
Export.image.toDrive({
  image: l8Img.select(["B3", "B2", "B1"]),
  description: "Drive-l8ImageDrive",
  fileNamePrefix: "l8Img1",
  folder: "training01",
  scale: 30,
  region: roi,
  maxPixels: 1e13
});
//代码链接：https://code.earthengine.google.com/2d790f643bdf6c753ca2c2a454243bf4


var l8 = ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA");
var roi = /* color: #d63000 */ee.Geometry.Polygon(
      [[[116.33401967309078, 39.8738616709093],
        [116.46882950954137, 39.87808443916675],
        [116.46882978521751, 39.94772261856061],
        [116.33952185055819, 39.943504136461144]]]);
var selectCol = l8.filterBounds(roi)
                 .filterDate("2017-8-1", "2017-12-1")
                 .map(function(image) {
                   return image.addBands(image.normalizedDifference(["B5", "B4"]).rename("NDVI"));
                 })
                 .sort("system:time_start");
print("select imageCollection", selectCol);

var l8Img = selectCol.mosaic().clip(roi);
Map.addLayer(l8Img, {bands: ["B4", "B3", "B2"], min:0, max:0.3}, "l8");
Map.centerObject(roi, 12);
Map.addLayer(roi, {color: "red"}, "roi");

var exportImage = selectCol.select("NDVI")
                           .toBands();
print("exportImage", exportImage);

Export.image.toDrive({
  image: exportImage,
  description: "Drive-multiImage",
  fileNamePrefix: "multiImage1",
  folder: "training01",
  scale: 30,
  region: roi,
  maxPixels: 1e13,
  crs: "EPSG:4326"
});
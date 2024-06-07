//代码链接：https://code.earthengine.google.com/503bbeef6489185343e5e4582314847a


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

var exportImgCol = selectCol.select("NDVI");
print("exportImgCol", exportImgCol);


//evaluate
var indexList = exportImgCol.reduceColumns(ee.Reducer.toList(), ["system:index"])
                            .get("list");
indexList.evaluate(function(indexs) {
  for (var i=0; i<indexs.length; i++) {
    var image = exportImgCol.filter(ee.Filter.eq("system:index", indexs[i]))
                            .first();
    exportImage(image, roi, "imgCol-"+indexs[i]);
  }
});

function exportImage(image, region, fileName) {
  Export.image.toDrive({
    image: image,
    description: "Drive-"+fileName,
    fileNamePrefix: fileName,
    folder: "training01",
    scale: 30,
    region: region,
    maxPixels: 1e13,
    crs: "EPSG:4326"
  });
}
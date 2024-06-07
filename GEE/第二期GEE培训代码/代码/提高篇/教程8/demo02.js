var roi = /* color: #d63000 */ee.Geometry.Polygon(
        [[[114.58599519845029, 33.34330275580846],
          [114.60590791817685, 33.343876372210005],
          [114.60419130440732, 33.36079635603699],
          [114.58530855294248, 33.359936097239135]]]);
Map.centerObject(roi, 10);
Map.setOptions("SATELLITE");
//NDVI: (B05 - B04)/(B05 + B04)
function NDVI(image) {
  var ndvi = image.normalizedDifference(["B5", "B4"]);
  return image.addBands(ndvi.rename("NDVI"));
}
var sCol = ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA")
             .filterBounds(roi)
             .filterDate("2018-1-1", "2019-1-1")
             .map(ee.Algorithms.Landsat.simpleCloudScore)
             .map(function(image) {
               return image.updateMask(image.select("cloud").lte(0));
             })
             .map(NDVI)
             .select("NDVI");
             
var visParam = {
  min: -1, 
  max: 1,
  palette: ["FFFFFF", "CE7E45", "DF923D", "F1B555", "FCD163", 
            "99B718", "74A901", "66A000", "529400", "3E8601", 
            "207401", "056201", "004C00", "023B01", "012E01", 
            "011D01", "011301"]
};
Map.addLayer(sCol.select("NDVI").mean(), visParam, "NDVI");
Map.addLayer(roi, {color: "red"}, "roi");
sCol = sCol.map(function(image) {
  var dict = image.reduceRegion({
    reducer: ee.Reducer.mean(), 
    geometry: roi, 
    scale: 30, 
    maxPixels: 1e13,
    tileScale: 4
  });
  dict = ee.Dictionary(dict);
  var ndvi = ee.Number(dict.get("NDVI"));
  image = image.set("ndvi", ndvi);
  var time_start = ee.Date(ee.Number(image.get("system:time_start")));
  image = image.set("date", time_start.format("YYYY-MM-dd"));
  return image;
});
print("sCol", sCol);
var dataList = sCol.reduceColumns(ee.Reducer.toList(2, 2), ["ndvi", "date"])
                   .get("list");
print("dataList", dataList);

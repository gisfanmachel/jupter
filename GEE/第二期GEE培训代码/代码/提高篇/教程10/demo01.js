//ui.Chart.array.values
var roi = /* color: #d63000 */ee.Geometry.Polygon(
        [[[114.58599519845029, 33.34330275580846],
          [114.60590791817685, 33.343876372210005],
          [114.60419130440732, 33.36079635603699],
          [114.58530855294248, 33.359936097239135]]]);
Map.centerObject(roi, 10);
Map.setOptions("SATELLITE");
//EVI: 2.5*(B05 - B04) / (B05 + 6*B04 - 7.5*B02 + 1)
function EVI(image) {
  var nir = image.select("B5");
  var red = image.select("B4");
  var blue = image.select("B2");
  var evi = image.expression(
    "2.5 * (B5 - B4) / (B5 + 6*B4 - 7.5*B2 + 1)",
    {
      "B5": nir,
      "B4": red,
      "B2": blue
    }
  );
  return image.addBands(evi.rename("EVI"));
}
//NDVI: (B05 - B04)/(B05 + B04)
function NDVI(image) {
  var ndvi = image.normalizedDifference(["B5", "B4"]);
  return image.addBands(ndvi.rename("NDVI"));
}
var sCol = ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA")
             .filterBounds(roi)
             .filterDate("2018-1-1", "2019-1-1")
             .map(NDVI)
             .map(EVI)
             .select(["NDVI", "EVI"]);
var visParam = {
  min: -1, 
  max: 1,
  palette: ["FFFFFF", "CE7E45", "DF923D", "F1B555", "FCD163", 
            "99B718", "74A901", "66A000", "529400", "3E8601", 
            "207401", "056201", "004C00", "023B01", "012E01", 
            "011D01", "011301"]
};
Map.addLayer(sCol.select("NDVI").mean(), visParam, "NDVI");
Map.addLayer(sCol.select("EVI").mean(), visParam, "EVI");
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
  var evi = ee.Number(dict.get("EVI"));
  image = image.set("ndvi", ndvi);
  image = image.set("evi", evi);
  var time_start = ee.Date(ee.Number(image.get("system:time_start")));
  image = image.set("date", time_start.format("YYYY-MM-dd"));
  return image;
});
print("sCol", sCol);
var dataList = sCol.reduceColumns(ee.Reducer.toList(3), ["ndvi", "evi", "date"])
                   .get("list");
//显示植被指数列表
dataList.evaluate(function(dList) {
  print("data list is", dList);
  var yValues = [];
  var xValues = [];
  for (var i=0; i<dList.length; i++) {
    var data = dList[i];
    yValues.push([data[0], data[1]]);
    xValues.push(data[2]);
  }
  var chart = ui.Chart.array.values(ee.List(yValues), 0, ee.List(xValues))
                .setSeriesNames(["NDVI", "EVI"])
                .setOptions({
                  title: "NDVI和EVI值列表", 
                  hAxis: {title: "日期"},
                  vAxis: {title: "植被指数"},
                  legend: null,
                  lineWidth:1,
                  pointSize:2
                });
  print(chart);  
});

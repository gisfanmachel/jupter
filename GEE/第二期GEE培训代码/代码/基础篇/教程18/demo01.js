//代码链接：https://code.earthengine.google.com/a1728ab6f7df3c155525c08b1893c247

//ui.Chart.array.values
var roi = ee.Geometry.Point([114.59457826729795, 33.3533404972818]);
Map.centerObject(roi, 10);
Map.setOptions("SATELLITE");
Map.style().set("cursor", "crosshair");

var sCol = ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA")
             .filterBounds(roi)
             .filterDate("2018-1-1", "2019-1-1")
             .map(function(image){
               return image.addBands(image.normalizedDifference(["B5", "B4"]).rename("NDVI"));
             });

var visParam = {
  min: -0.2, 
  max: 0.8,
  palette: ["FFFFFF", "CE7E45", "DF923D", "F1B555", "FCD163", 
            "99B718", "74A901", "66A000", "529400", "3E8601", 
            "207401", "056201", "004C00", "023B01", "012E01", 
            "011D01", "011301"]
};
Map.addLayer(sCol.select("NDVI").mean(), visParam, "NDVI");
Map.addLayer(roi, {color: "red"}, "roi");

var dataList = sCol.select("NDVI")
                   .getRegion(roi, 30);
dataList = ee.List(dataList);
print("NDVI data list is", dataList);
//显示NDVI值列表
dataList.evaluate(function(dList) {
  var diList = [];
  var dateList = [];
  for (var i=1; i<dList.length; i++) {
    var data = dList[i];
    diList.push(data[4]);
    dateList.push(ee.Date(data[3]).format("YYYY-MM-dd"));
  }
  var chart = ui.Chart.array.values(ee.List(diList), 0, ee.List(dateList))
                .setSeriesNames(["NDVI"])
                .setOptions({
                  title: "NDVI值列表", 
                  hAxis: {title: "日期"},
                  vAxis: {title: "NDVI值"},
                  legend: null,
                  lineWidth:1,
                  pointSize:2
                });
  print(chart);  
});
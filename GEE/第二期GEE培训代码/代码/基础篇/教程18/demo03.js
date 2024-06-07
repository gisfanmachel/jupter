//代码链接：https://code.earthengine.google.com/ccba40b1b97345ffad2935b8f88d90ed

//ui.Chart.image.doySeries
var roi = /* color: #00ffff */ee.Geometry.Polygon(
        [[[114.59114503975889, 33.35455928709266],
          [114.59114503975889, 33.35183490983753],
          [114.59869814034482, 33.35183490983753],
          [114.59818315621396, 33.35642328555932]]]);
Map.centerObject(roi, 7);

Map.setOptions("SATELLITE");
Map.style().set("cursor", "crosshair");
var l8Col = ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA")
              .filterBounds(roi)
              .filterDate("2018-1-1", "2019-1-1")
              .map(function(image) {
                return image.addBands(image.normalizedDifference(["B5", "B4"]).rename("NDVI"));
              })
              .select("NDVI");
              
var visParam = {
  min: -0.2, 
  max: 0.8,
  palette: ["FFFFFF", "CE7E45", "DF923D", "F1B555", "FCD163", 
            "99B718", "74A901", "66A000", "529400", "3E8601", 
            "207401", "056201", "004C00", "023B01", "012E01", 
            "011D01", "011301"]
};
Map.addLayer(l8Col.mean(), visParam, "NDVI");
Map.addLayer(roi, {color: "red"}, "roi");


var chart = ui.Chart.image.doySeries({
                imageCollection: l8Col,
                region: roi,
                regionReducer: ee.Reducer.mean(),
                scale: 30
              })
              .setSeriesNames(["NDVI"])
              .setOptions({
                title: "NDVI列表", 
                hAxis: {title: "day of year"},
                vAxis: {title: "ndvi value"},
                legend: null,
                lineWidth:1,
                pointSize:2
              });
print(chart);
//代码链接：https://code.earthengine.google.com/171d7a9110c76d5cf7cff65a0b049505


//ui.Chart.image.histogram
var roi = /* color: #ffc82d */ee.Geometry.Polygon(
        [[[114.56631860180869, 33.33621936057971],
          [114.57095345898642, 33.336506192580465],
          [114.57026681347861, 33.340378332142684],
          [114.56631860180869, 33.33994810291467]]]);
Map.centerObject(roi, 7);

Map.setOptions("SATELLITE");
Map.style().set("cursor", "crosshair");
var image = ee.Image("LANDSAT/LC08/C01/T1_TOA/LC08_123037_20180611");
image = image.addBands(image.normalizedDifference(["B5", "B4"]).rename("NDVI"));
var visParam = {
  min: -0.2, 
  max: 0.8,
  palette: ["FFFFFF", "CE7E45", "DF923D", "F1B555", "FCD163", 
            "99B718", "74A901", "66A000", "529400", "3E8601", 
            "207401", "056201", "004C00", "023B01", "012E01", 
            "011D01", "011301"]
};
Map.addLayer(image.select("NDVI"), visParam, "NDVI");
Map.addLayer(roi, {color: "red"}, "roi");

var chart = ui.Chart.image.histogram({
                image: image.select("NDVI"), 
                region: roi, 
                scale: 30
              })
              .setOptions({
                title: "NDVI Histogram",
                hAxis: {title: "ndvi"},
                vAxis: {title: "count"}
              });

print(chart);
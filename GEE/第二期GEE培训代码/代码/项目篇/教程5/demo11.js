//代码链接：https://code.earthengine.google.com/502304d17ad7c0be0e732e1d59feb60d


//ee.Reducer.pearsonsCorrelation
var roi = /* color: #98ff00 */ee.Geometry.Polygon(
        [[[115.28627108398433, 36.67525024180043],
          [115.30000399414058, 36.671945893730204],
          [115.30000399414058, 36.696174483898005],
          [115.28215121093746, 36.69507334992879]]]);
Map.centerObject(roi, 8);

var l8Col = ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA")
              .filterBounds(roi)
              .filterDate("2019-1-1", "2019-2-1")
              .select(["B5", "B4"]);
print("l8Col", l8Col);

var image = l8Col.mean().clip(roi);
Map.addLayer(image, {}, "image");
Map.addLayer(roi, {color:"red"}, "roi");

var values = image.reduceRegion({
  reducer: ee.Reducer.toList(),
  geometry: roi,
  scale: 30
});

var chart = ui.Chart.array.values({
                array:values.get("B4"), 
                axis:0, 
                xLabels: values.get("B5")
              })
              .setSeriesNames(["value"])
              .setOptions({
                hAxis: {title: "B5" },
                vAxis: {title: "B4" },
                pointSize: 1,
                legend: 'none'
              });
print(chart);

var pc = image.reduceRegion({
  reducer: ee.Reducer.pearsonsCorrelation(), 
  geometry: roi,
  scale: 30
});
print("pearsonsCorrelation", pc);
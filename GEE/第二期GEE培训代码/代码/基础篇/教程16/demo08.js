//代码链接：https://code.earthengine.google.com/4e9db4069da5cb2f488a5be28aa01b7f


var l8 = ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA");
var roi = /* color: #d63000 */ee.Geometry.Polygon(
        [[[116.33401967309078, 39.8738616709093],
          [116.46882950954137, 39.87808443916675],
          [116.46882978521751, 39.94772261856061],
          [116.33952185055819, 39.943504136461144]]]);
var selectCol = l8.filterBounds(roi)
                  .filterDate("2017-1-1", "2017-12-31")
                  .map(function(image) {
                    return image.addBands(image.normalizedDifference(["B5", "B4"]).rename("NDVI"));
                  })
                  .map(function(image) {
                    return image.clip(roi);
                  })
                  .sort("system:time_start");
                  
Map.addLayer(selectCol.mosaic(), {bands: ["B3", "B2", "B1"], min:0, max:0.3}, "l8");
Map.centerObject(roi, 12);

var chart = ui.Chart.image.doySeries({
  imageCollection: selectCol.select("NDVI"),
  region: roi,
  regionReducer: ee.Reducer.mean(),
  scale: 30
});
print(chart);
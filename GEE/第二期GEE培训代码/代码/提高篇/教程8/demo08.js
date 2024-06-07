//代码链接：https://code.earthengine.google.com/6afa0e0b4eac99056a2cdd00d4bb1a7b


//reduce image to single value
var roi = /* color: #98ff00 */ee.Geometry.Polygon(
        [[[114.62959747314449, 33.357067677774594],
          [114.63097076416011, 33.32896028884253],
          [114.68315582275386, 33.33125510961763],
          [114.68178253173824, 33.359361757948754]]]);
Map.centerObject(roi, 7);
Map.setOptions("SATELLITE");
var image = ee.Image("LANDSAT/LC08/C01/T1_TOA/LC08_123037_20180611");
var ndvi = image.normalizedDifference(["B5", "B4"]).rename("NDVI");
var visParam = {
  min: -0.2, 
  max: 0.8,
  palette: ["FFFFFF", "CE7E45", "DF923D", "F1B555", "FCD163", 
            "99B718", "74A901", "66A000", "529400", "3E8601", 
            "207401", "056201", "004C00", "023B01", "012E01", 
            "011D01", "011301"]
};
Map.addLayer(ndvi, visParam, "NDVI");
Map.addLayer(roi, {color: "red"}, "roi");

var dict = ndvi.reduceRegion({
  reducer: ee.Reducer.mean()
             .combine(ee.Reducer.min(), null, true)
             .combine(ee.Reducer.max(), null, true),
  geometry: roi, 
  scale: 30
});
print("reduceRegion value is: ", dict);
print("ndvi mean is: ", ee.Number(dict.get("NDVI_mean")));
print("ndvi min is: ", ee.Number(dict.get("NDVI_min")));
print("ndvi max is: ", ee.Number(dict.get("NDVI_max")));
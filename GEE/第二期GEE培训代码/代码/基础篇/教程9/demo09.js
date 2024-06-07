//代码链接：https://code.earthengine.google.com/c5f63a9cdf51216fae3504fe73310d09


var roi = /* color: #98ff00 */ee.Geometry.Polygon(
        [[[114.62959747314449, 33.357067677774594],
          [114.63097076416011, 33.32896028884253],
          [114.68315582275386, 33.33125510961763],
          [114.68178253173824, 33.359361757948754]]]);
Map.centerObject(roi, 7);
Map.setOptions("SATELLITE");

var l8Col = ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA")
              .filterBounds(roi)
              .filterDate("2018-1-1", "2019-1-1")
              .map(ee.Algorithms.Landsat.simpleCloudScore)
              .map(function(image) {
                return image.updateMask(image.select("cloud").lte(20));
              })
              .map(function(image) {
                var ndvi = image.normalizedDifference(["B5", "B4"]).rename("NDVI");
                return image.addBands(ndvi);
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
Map.addLayer(l8Col.median(), visParam, "NDVI");
Map.addLayer(roi, {color: "red"}, "roi");
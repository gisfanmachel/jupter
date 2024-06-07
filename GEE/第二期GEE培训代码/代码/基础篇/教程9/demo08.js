//代码链接：https://code.earthengine.google.com/ec873a14301216fee25b35e1e54a74e8


var roi = /* color: #98ff00 */ee.Geometry.Polygon(
        [[[114.62959747314449, 33.357067677774594],
          [114.63097076416011, 33.32896028884253],
          [114.68315582275386, 33.33125510961763],
          [114.68178253173824, 33.359361757948754]]]);
Map.centerObject(roi, 7);
Map.setOptions("SATELLITE");

var l8Col = ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA")
              .filterBounds(roi)
              .filterDate("2018-1-1", "2019-1-1");

var visParam = {
  min: 0, 
  max: 0.3,
  bands: ["B4", "B3", "B2"]
};
Map.addLayer(l8Col, visParam, "image");
Map.addLayer(roi, {color: "red"}, "roi");
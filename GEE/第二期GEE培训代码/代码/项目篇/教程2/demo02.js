//代码链接：https://code.earthengine.google.com/0f211b9eea4be686341f14ec78538507

var roi = /* color: #d63000 */ee.Geometry.Polygon(
        [[[117.19846835579438, 31.338582945998613],
          [117.96476474251313, 31.352657172321162],
          [117.93455234016938, 31.822923403887454],
          [117.20396151985688, 31.792580050380295]]]);
Map.centerObject(roi, 9);
Map.addLayer(roi, {color: "red"}, "roi");
var l8Col = ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA")
              .filterBounds(roi)
              .filterDate("2017-1-1", "2019-1-1")
              //影像去云
              .map(ee.Algorithms.Landsat.simpleCloudScore)
              .map(function(image) {
                return image.updateMask(image.select("cloud").lte(10));
              });
print(l8Col);
//代码链接：https://code.earthengine.google.com/36526fe68072ae143203d5297aea555b


//非监督分类
var roi = /* color: #d63000 */ee.Geometry.Polygon(
        [[[114.02191591378232, 33.78358088957628],
          [114.03290224190732, 32.814844755032674],
          [115.04913759346982, 32.85638443066918],
          [115.01617860909482, 33.8018413803568]]]);
Map.centerObject(roi, 7);
Map.setOptions("SATELLITE");
Map.addLayer(roi, {color: "00ff00"}, "roi");

var l8Col = ee.ImageCollection("LANDSAT/LC08/C01/T1_SR")
              .filterBounds(roi)
              .filterDate("2018-5-1", "2018-10-1")
              .filter(ee.Filter.lte("CLOUD_COVER", 50));
print("l8Col", l8Col); 
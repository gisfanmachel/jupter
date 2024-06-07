//代码链接：https://code.earthengine.google.com/013201af8c095f310a6e4c15317b6af0


//非监督分类
var roi = /* color: #d63000 */ee.Geometry.Polygon(
        [[[114.02191591378232, 33.78358088957628],
          [114.03290224190732, 32.814844755032674],
          [115.04913759346982, 32.85638443066918],
          [115.01617860909482, 33.8018413803568]]]);
Map.centerObject(roi, 7);
Map.setOptions("SATELLITE");
Map.addLayer(roi, {color: "00ff00"}, "roi");

//Landsat8 SR数据去云
function rmCloud(image) {
  var cloudShadowBitMask = (1 << 3);
  var cloudsBitMask = (1 << 5);
  var qa = image.select("pixel_qa");
  var mask = qa.bitwiseAnd(cloudShadowBitMask).eq(0)
                 .and(qa.bitwiseAnd(cloudsBitMask).eq(0));
  return image.updateMask(mask);
}

//缩放
function scaleImage(image) {
  var time_start = image.get("system:time_start");
  image = image.multiply(0.0001);
  image = image.set("system:time_start", time_start);
  return image;
}

var l8Col = ee.ImageCollection("LANDSAT/LC08/C01/T1_SR")
              .filterBounds(roi)
              .filterDate("2018-5-1", "2018-10-1")
              .filter(ee.Filter.lte("CLOUD_COVER", 50))
              .map(rmCloud)
              .map(scaleImage);
print("l8Col", l8Col);

var l8Image = l8Col.median().clip(roi);
var visParam = {
  min: 0,
  max: 0.3,
  bands: ["B4", "B3", "B2"]
};
Map.addLayer(l8Image, visParam, "l8Image");
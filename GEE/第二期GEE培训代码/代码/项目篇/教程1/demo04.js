//代码链接：https://code.earthengine.google.com/f2e44c9ff8c4040f773bb03f95fed291


//非监督分类
var roi = /* color: #d63000 */ee.Geometry.Polygon(
        [[[114.02191591378232, 33.78358088957628],
          [114.03290224190732, 32.814844755032674],
          [115.04913759346982, 32.85638443066918],
          [115.01617860909482, 33.8018413803568]]]);
Map.centerObject(roi, 7);
Map.setOptions("SATELLITE");
Map.addLayer(roi, {color: "00ff00"}, "roi", false);

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

//添加NDVI
function NDVI(image) {
  return image.addBands(image.normalizedDifference(["B5", "B4"]).rename("NDVI"));
}

var l8Col = ee.ImageCollection("LANDSAT/LC08/C01/T1_SR")
              .filterBounds(roi)
              .filterDate("2018-5-1", "2018-10-1")
              .filter(ee.Filter.lte("CLOUD_COVER", 50))
              .map(rmCloud)
              .map(scaleImage)
              .map(NDVI);
print("l8Col", l8Col);

var l8Image = l8Col.select(["B1", "B2", "B3", "B4", "B5", "B6", "B7", "NDVI"])
                   .median()
                   .clip(roi);
var visParam = {
  min: 0,
  max: 0.3,
  bands: ["B4", "B3", "B2"]
};
Map.addLayer(l8Image, visParam, "l8Image");

var sampleRoi = /* color: #98ff00 */ee.Geometry.Polygon(
        [[[114.62959747314449, 33.357067677774594],
          [114.63097076416011, 33.32896028884253],
          [114.68315582275386, 33.33125510961763],
          [114.68178253173824, 33.359361757948754]]]);
Map.addLayer(sampleRoi, {color: "red"}, "sampleRoi", false);

//生成训练使用的样本数据
var training = l8Image.sample({
  region: roi,
  scale: 30,
  numPixels:5000
});

print("training", training.limit(1));
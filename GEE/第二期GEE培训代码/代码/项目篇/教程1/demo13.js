//代码链接：https://code.earthengine.google.com/0493aeb1ab7c8db10bb6397329bdc755


//监督分类 
var roi = /* color: #d63000 */ee.Geometry.Polygon(
        [[[103.90797119140626, 19.300461796064834],
          [104.6770141601562, 18.791603753190085],
          [105.3526733398437, 18.52096883329724],
          [105.7811401367187, 18.54180220057951],
          [105.7976196289062, 19.300461796064834],
          [105.0011108398437, 20.122686131769573],
          [104.6001098632812, 19.719859112799057],
          [104.0453002929687, 19.761221836922864]]]);
Map.centerObject(roi, 8);
Map.addLayer(roi, {color: "red"}, "roi");

/**
forest 0
urban 1
paddyrice 2
water 3
crop 4
*/       
var sampleData = ee.FeatureCollection("users/wangweihappy0/training01/l8ClassifySample");
Map.addLayer(sampleData, {}, "sampleData");

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

//NDVI
function NDVI(image) {
  return image.addBands(
    image.normalizedDifference(["B5", "B4"])
         .rename("NDVI"));
}

//NDWI
function NDWI(image) {
  return image.addBands(
    image.normalizedDifference(["B3", "B5"])
         .rename("NDWI"));
}
  
//NDBI
function NDBI(image) {
  return image.addBands(
    image.normalizedDifference(["B6", "B5"])
         .rename("NDBI"));
}
          
var l8Col = ee.ImageCollection("LANDSAT/LC08/C01/T1_SR")
              .filterBounds(roi)
              .filterDate("2018-1-1", "2019-1-1")
              .map(rmCloud)
              .map(scaleImage)
              .map(NDVI)
              .map(NDWI)
              .map(NDBI);
              
//DEM
var srtm = ee.Image("USGS/SRTMGL1_003");
var dem = ee.Algorithms.Terrain(srtm);
var elevation = dem.select("elevation");
var slope = dem.select("slope");

var bands = [
  "B1", "B2", "B3", "B4", "B5", "B6", "B7",
  "NDBI", "NDWI", "NDVI","SLOPE", "ELEVATION"
];
var l8Image = l8Col.median()
                   .addBands(elevation.rename("ELEVATION"))
                   .addBands(slope.rename("SLOPE"))
                   .clip(roi)
                   .select(bands);

var rgbVisParam = {
  min: 0,
  max: 0.3,
  bands: ["B4", "B3", "B2"]
};
Map.addLayer(l8Image, rgbVisParam, "l8Image");

//切分生成训练数据和验证数据
sampleData = sampleData.randomColumn('random');
var sample_training = sampleData.filter(ee.Filter.lte("random", 0.7)); 
var sample_validate  = sampleData.filter(ee.Filter.gt("random", 0.7));

print("sample_training", sample_training);
print("sample_validate", sample_validate);

//生成监督分类训练使用的样本数据
var training = l8Image.sampleRegions({
  collection: sample_training, 
  properties: ["type"], 
  scale: 30
});
//生成监督分类验证使用的样本数据
var validation = l8Image.sampleRegions({
  collection: sample_validate, 
  properties: ["type"], 
  scale: 30
});

//初始化分类器
var classifier = ee.Classifier.cart().train({
  features: training, 
  classProperty: "type",
  inputProperties: bands
});

//影像数据调用classify利用训练数据训练得到分类结果
var classified = l8Image.classify(classifier);
//训练结果的混淆矩阵
var trainAccuracy = classifier.confusionMatrix();

//验证数据集合调用classify进行验证分析得到分类验证结果
var validated = validation.classify(classifier);
//验证结果的混淆矩阵
var testAccuracy = validated.errorMatrix("type", "classification");
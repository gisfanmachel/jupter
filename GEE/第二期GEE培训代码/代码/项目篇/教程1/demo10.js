//代码链接：https://code.earthengine.google.com/f2b77fb73a225ec82f636db5aef36f1f


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

var l8Image = l8Col.median()
                   .addBands(elevation.rename("ELEVATION"))
                   .addBands(slope.rename("SLOPE"))
                   .clip(roi);

var rgbVisParam = {
  min: 0,
  max: 0.3,
  bands: ["B4", "B3", "B2"]
};
Map.addLayer(l8Image, rgbVisParam, "l8Image");
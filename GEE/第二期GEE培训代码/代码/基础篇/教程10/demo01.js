//代码链接：https://code.earthengine.google.com/840d1a63702dd8c4999f377d78c16cb4

var roi = /* color: #00ffff */ee.Geometry.Polygon(
        [[[114.55646972656245, 38.93885857738322],
          [114.68967895507808, 38.958083016248054],
          [114.66770629882808, 39.04132865562038],
          [114.55097656249995, 39.02959481857095]]]);
var dem = ee.Image('USGS/SRTMGL1_003');
Map.centerObject(roi, 10);
var visParam = {min:0, max:3000, palette:["green", "blue", "red"]};
Map.addLayer(dem, visParam, "dem");

//aspect
var aspect = ee.Terrain.aspect(dem);
var cosImg = aspect.divide(180).multiply(Math.PI).cos();
Map.addLayer(cosImg, {min:-1, max:1}, "cosImg", false);

//hillshade
var hillshade = ee.Terrain.hillshade(dem);
Map.addLayer(hillshade, {}, "hillshade", false);

//slope
var slope = ee.Terrain.slope(dem);
Map.addLayer(slope, {min:0, max:60}, "slope", false);

//products
var products = ee.Terrain.products(dem);
Map.addLayer(products, {}, "products", false);

//fillMinima
var fillMinima = ee.Terrain.fillMinima(dem, 10);
Map.addLayer(fillMinima, {}, "fillMinima", false);

//compute 计算感兴趣区域的海拔均值
var meanDict = dem.reduceRegion({
  reducer: ee.Reducer.mean(),
  geometry: roi,
  scale:30
});
print(meanDict);
var mean = meanDict.get("elevation");
print("mean evelation: ", mean);

Map.addLayer(roi, {}, "roi");
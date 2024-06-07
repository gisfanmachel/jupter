//https://code.earthengine.google.com/4d0bbb2197468656b3abb135eca8f1b1

var vb_rgba = ee.Image("users/wangweihappy0/training02/vb_rgba"),
    vb_rgbn = ee.Image("users/wangweihappy0/training02/vb_rgbn"),
    roi = /* color: #d63000 */ee.Geometry.Polygon(
        [[[-73.31626302530043, -3.4487961454954026],
          [-73.31601089762671, -3.4487774040333297],
          [-73.31601626204531, -3.4485230555828665],
          [-73.31627107192833, -3.448541797049963]]]);
vb_rgba = vb_rgba.select(["red", "green", "blue"], ["r", "g", "b"]);
Map.centerObject(vb_rgba, 19);
Map.addLayer(vb_rgba, {}, "vb_rgba");
Map.addLayer(vb_rgbn, {}, "vb_rgbn");
Map.addLayer(roi, {}, "roi");

var ndvi = vb_rgbn.normalizedDifference(["nir", "red"]).rename("ndvi");
var visParam = {
  min:0,
  max:0.8,
  palette: 'FFFFFF, CE7E45, DF923D, F1B555, FCD163, 99B718, 74A901, 66A000, 529400,' +
    '3E8601, 207401, 056201, 004C00, 023B01, 012E01, 011D01, 011301'
};
Map.addLayer(ndvi, visParam, "ndvi");
//缩放
vb_rgba = vb_rgba.unitScale(0, 255);
vb_rgbn = vb_rgbn.multiply(0.00001);
vb_rgbn = vb_rgbn.addBands(ndvi);

var droneImage = vb_rgbn.addBands(vb_rgba);
print("droneImage", droneImage);
//生成训练使用的样本数据
var training = droneImage.sample({
  region: roi,
  scale: 1,
  numPixels:1000
});
print("training", training.limit(1));
//初始化非监督分类器
var count = 2;
var clusterer = ee.Clusterer.wekaKMeans(count)
                  .train(training);
//调用影像或者矢量集合中的cluster方法进行非监督分类
var result = droneImage.cluster(clusterer);
print("result", result);
Map.addLayer(result.randomVisualizer(), {}, "result");

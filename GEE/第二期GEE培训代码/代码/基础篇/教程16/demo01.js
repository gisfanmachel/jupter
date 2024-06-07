//代码链接：https://code.earthengine.google.com/89448dd9683aaabd84bb8bec70569efa


var l8 = ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA");
var roi = /* color: #d63000 */ee.Geometry.Polygon(
      [[[116.33401967309078, 39.8738616709093],
        [116.46882950954137, 39.87808443916675],
        [116.46882978521751, 39.94772261856061],
        [116.33952185055819, 39.943504136461144]]]);
var selectCol = l8.filterBounds(roi)
                 .filterDate("2017-1-1", "2018-6-1")
                 .map(ee.Algorithms.Landsat.simpleCloudScore)
                 .map(function(img) {
                    img = img.updateMask(img.select("cloud").lt(1));
                    return img;
                 })
                 .sort("system:time_start");
var l8Img = selectCol.mosaic().clip(roi);
Map.addLayer(l8Img, {bands: ["B3", "B2", "B1"], min:0, max:0.3}, "l8");
Map.centerObject(roi, 12);
Map.addLayer(roi, {color: "red"}, "roi");

//export To Asset
Export.image.toAsset({
  image: l8Img.select("B1"),
  description: "Asset-l8ImgB1-01",
  assetId: "training01/l8ImgB1-01",
  scale: 30,
  region: roi
});


//这里导出的landsat8筛选的影像，只包含三个波段B3、B2、B1，
//其中B3值采用mean方式计算，B2值采用sample方式计算，B1采用max方式计算
//区域就是设置的roi，分辨率30米
Export.image.toAsset({
  image: l8Img.select(["B3", "B2", "B1"]),
  description: "Asset-l8Img-02",
  assetId: "training01/l8Img-02",
  scale: 30,
  region: roi,
  pyramidingPolicy: {
    'B3': 'mean',
    'B2': 'sample',
    'B1': 'max'
  }
});
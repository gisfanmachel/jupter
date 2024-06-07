//https://code.earthengine.google.com/fa3621f7cc0135c0a9175bcbd3555161

var mcd15a3h = ee.ImageCollection("MODIS/006/MCD15A3H");
var fCol = ee.FeatureCollection("USDOS/LSIB/2013");
var sCol = fCol.filter(ee.Filter.eq("name", "Taiwan"));
print("select sCol", sCol);
Map.centerObject(sCol, 9);
Map.addLayer(sCol, {color: "red"}, "roi");
var lai = mcd15a3h.filterDate("2018-3-1", "2018-5-1")
                  .select("Lai")
                  .mosaic()
                  .multiply(0.1)
                  .clip(sCol);
var visParam = {
  min: 0,
  max: 1,
  palette: ['e1e4b4', '999d60', '2ec409', '0a4b06'],
};
Map.addLayer(lai, visParam, "lai");
Export.image.toDrive({
  image: lai,
  description: "LAI",
  folder: "training02",
  fileNamePrefix: "LAI",
  region: sCol.geometry().bounds(), //设置范围
  scale: 500, //分辨率
  crs: "EPSG:4326", //设置投影方式
  maxPixels: 1e13 //设置最大像素值
});

//代码链接：https://code.earthengine.google.com/88272b04de8d5aa6e6a11d059bf61185


//使用的是GEE中世界地区边界这个数据集，展示的是中国台湾省
var countries = ee.FeatureCollection("ft:1tdSwUL7MVpOauSgRzqVTOwdfy17KDbw-1d9omPw");
print(countries.limit(1));
var taiwan = countries.filter(ee.Filter.eq("Country", "Taiwan"));
Map.addLayer(taiwan, {color: "red"}, "taiwan");
Map.centerObject(taiwan, 6);

//导出的还是我们的宝岛台湾省，格式是KML格式
Export.table.toDrive({
  collection:ee.FeatureCollection(taiwan),
  description: "Drive-taiwan",
  fileNamePrefix: "taiwan",
  fileFormat: "KML",
  folder: "training01"
});
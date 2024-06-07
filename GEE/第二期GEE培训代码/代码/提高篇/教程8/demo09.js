//代码链接：https://code.earthengine.google.com/b55fdbd6cf62f3b9dc8249001ab76dc4


//roi选取的是中国陆地区域，数据使用的是modis地标分类数据集合
var countries = ee.FeatureCollection("ft:1tdSwUL7MVpOauSgRzqVTOwdfy17KDbw-1d9omPw"),
    mcd12q1 = ee.ImageCollection("MODIS/006/MCD12Q1");
var roi = countries.filter(ee.Filter.eq("Country", "Taiwan"));
Map.centerObject(roi, 7);
Map.addLayer(roi, {}, "roi");
var bounds = roi.geometry().bounds();
var landCover = mcd12q1.filterDate("2016-1-1", "2017-1-1")
                      .select("LC_Type1")
                      .first()
                      .clip(roi);
print("landCover", landCover);
//直接加载到地图上的样子
Map.addLayer(landCover);

var image = ee.Image.constant(1)
              .addBands(landCover);
var dict = image.reduceRegion({
  reducer: ee.Reducer.count().group({
    groupField: 1,
    groupName: "landType" //组类别名称命名为了landType
  }),
  geometry: roi, 
  scale: 500,
  maxPixels: 1e13
});
print(dict);
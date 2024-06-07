//roi选取的是中国陆地区域，数据使用的是modis地标分类数据集合
var countries = ee.FeatureCollection("ft:1tdSwUL7MVpOauSgRzqVTOwdfy17KDbw-1d9omPw"),
    mcd12q1 = ee.ImageCollection("MODIS/006/MCD12Q1");
var roi = countries.filter(ee.Filter.or(
  ee.Filter.eq("Country", "China"), 
  ee.Filter.eq("Country", "Taiwan")
));
Map.centerObject(roi, 3);
var bounds = ee.Image().toByte()
               .paint(roi, null, 2);
Map.addLayer(bounds, {palette: "red"}, "bounds");

var start_year = 2002;
var end_year = 2018;
var mcd15a3h = ee.ImageCollection('MODIS/006/MCD15A3H')
                .select("Lai")
                .map(function(image) {
                  var time_start = image.get("system:time_start");
                  image = image.multiply(0.1);
                  image = image.set("system:time_start", time_start);
                  return image;
                });

var yearList = ee.List.sequence(start_year, end_year);
var yearImgs = yearList.map(function(year) {
  year = ee.Number(year).toInt();
  var _sdate = ee.Date.fromYMD(year, 1, 1);
  var _edate = ee.Date.fromYMD(year.add(1), 1, 1);
  var tempCol = mcd15a3h.filterDate(_sdate, _edate);
  var yearImg = tempCol.max().clip(roi);
  yearImg = yearImg.set("count", tempCol.size());
  yearImg = yearImg.set("year", year);
  yearImg = yearImg.set("system:index", ee.String(year));
  return yearImg;
});

var yearImgCol = ee.ImageCollection.fromImages(yearImgs)
                   .filter(ee.Filter.gt("count", 0));
print("yearImgCol", yearImgCol);

// 使用缩略图来制作展示
var params = {
  crs: 'EPSG:3857',
  framesPerSecond: 2,
  region: roi.geometry().bounds(),
  min: 0.0,
  max: 10.0,
  palette: ["FEFF7E", "71EB2E", "3EB868", "276A9B", "0D1079"],
  dimensions: 720,
};
print(ui.Thumbnail(yearImgCol, params));

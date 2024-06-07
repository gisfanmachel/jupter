var l8 = ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA");
var roi = /* color: #0b4a8b */ee.Geometry.Point([116.40735205726082, 39.88350152818114]);
var start_year = 2013;
var end_year = 2018;
var lxCol = l8.filterDate(ee.Date.fromYMD(start_year, 1, 1), ee.Date.fromYMD(end_year+1, 1, 1))
              .filterBounds(roi)
              .map(ee.Algorithms.Landsat.simpleCloudScore)
              .map(function(image) {
                return image.updateMask(image.select("cloud").lte(10));
              });
print("raw image collection", lxCol);
var yearList = ee.List.sequence(2013, 2018);
var monthList = ee.List.sequence(1, 12);
var imgList = yearList.map(function(year) {
  year = ee.Number(year);
  var monthImgList = monthList.map(function(month) {
    month = ee.Number(month);
    var _sdate = ee.Date.fromYMD(year, month, 1);
    var _edate = _sdate.advance(1, "month");
    var tempCol = lxCol.filterDate(_sdate, _edate);
    var img = tempCol.median();
    var _date = _sdate.format("yyyyMM");
    img = img.set("year", year);
    img = img.set("date", _date);
    img = img.set("system:index", _date);
    img = img.set("system:time_start", _sdate.millis());
    img = img.set("count", tempCol.size());
    return img;
  });
  return monthImgList;
});
imgList = imgList.flatten();
print("img list", imgList);
var imgCol = ee.ImageCollection.fromImages(imgList);
print("month image collection has none bands", imgCol);
imgCol = imgCol.filter(ee.Filter.gt("count", 0));
print("month image collection do not has none bands", imgCol);

var visParam = {
  min: 0, 
  max: 0.3,
  bands: ["B4", "B3", "B2"]
};
var image = imgCol.filter(ee.Filter.eq("date", "201404")).first();
Map.centerObject(roi, 8);
Map.addLayer(image, visParam, "monthImage");

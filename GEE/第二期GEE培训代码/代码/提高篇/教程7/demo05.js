var mod10a1 = ee.ImageCollection("MODIS/006/MOD10A1");
var roi = /* color: #0b4a8b */ee.Geometry.Point([116.40735205726082, 39.88350152818114]);
var start_date = ee.Date("2013-1-1");
var end_date = ee.Date("2014-1-1");
var step = 5;
var lxCol = mod10a1.filterDate(start_date, end_date);
print("raw image collection", lxCol);
var dayNum = end_date.difference(start_date, "day");
var dayList = ee.List.sequence(0, dayNum.subtract(1), step);
print("dayList", dayList);

var dayImgList = dayList.map(function(day) {
  day = ee.Number(day);
  var _sdate = start_date.advance(day, "day");
  var _edate = start_date.advance(day.add(step), "day");
  var tempCol = lxCol.filterDate(_sdate, _edate);
  var image = tempCol.mean();
  image = image.set("start_date", _sdate);
  image = image.set("end_date", _edate);
  image = image.set("count", tempCol.size());
  return image;
});
print("raw dayImgList", dayImgList);
var dayImgCol = ee.ImageCollection.fromImages(dayImgList)
                  .filter(ee.Filter.gt("count", 0));
print("select dayImgCol",dayImgCol);

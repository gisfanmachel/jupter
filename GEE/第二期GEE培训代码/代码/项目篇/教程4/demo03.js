var roi = ee.Geometry.Polygon(
        [[[97.35198840029386, 38.44010528815348],
          [97.35198840029386, 38.164216161700466],
          [97.82714709170011, 38.164216161700466],
          [97.82714709170011, 38.44010528815348]]], null, false);
Map.centerObject(roi, 10);
Map.addLayer(roi, {color: "red"}, "roi", false);
var fCol = ee.FeatureCollection("users/wangweihappy0/training02/halahu_year_bounds");
print("fCol", fCol);
Map.addLayer(fCol, {color: "blue"}, "fCol", false);
var startDate = ee.Date("2014-1-1");
var endDate = ee.Date("2015-1-1");
var step = 5;
var sCol = ee.ImageCollection("MODIS/006/MOD10A1")
            .filterDate(startDate, endDate)
            .select(["NDSI_Snow_Cover", "NDSI_Snow_Cover_Class"]);
var dayNum = endDate.difference(startDate, "day");
var dayList = ee.List.sequence(0, dayNum.subtract(1), step);
print("dayList", dayList);
var dayImgList = dayList.map(function(day) {
  day = ee.Number(day);
  var _sdate = startDate.advance(day, "day");
  var _edate = startDate.advance(day.add(step), "day");
  var tempCol = sCol.filterDate(_sdate, _edate);
  var image = tempCol.mosaic();
  image = image.set("start_date", _sdate);
  image = image.set("end_date", _edate);
  image = image.set("count", tempCol.size());
  image = image.set("system:index", _sdate.format("yyyyMMdd"));
  return image;
});
print("raw dayImgList", dayImgList);
var dayImgCol = ee.ImageCollection.fromImages(dayImgList)
                  .filter(ee.Filter.gt("count", 0));
print("select dayImgCol",dayImgCol);

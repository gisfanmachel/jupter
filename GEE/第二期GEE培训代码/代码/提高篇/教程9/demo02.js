var l8 = ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA");
var roi = /* color: #0b4a8b */ee.Geometry.Point([116.40735205726082, 39.88350152818114]);
var start_year = 2013;
var end_year = 2018;
var sCol = l8.filterDate(ee.Date.fromYMD(start_year, 1, 1), ee.Date.fromYMD(end_year+1, 1, 1))
              .filterBounds(roi)
              .map(ee.Algorithms.Landsat.simpleCloudScore)
              .map(function(image) {
                return image.updateMask(image.select("cloud").lte(10));
              })
              .map(function(image) {
                var time_start = ee.Date(image.get("system:time_start"));
                var date = time_start.format("yyyyMM");
                image = image.set("date", date);
                return image;
              });
print("raw image collection", sCol);

var firCol = sCol.distinct(["date"]);
var secCol = sCol;
var filter = ee.Filter.equals({leftField:"date", rightField:"date"});
var join = ee.Join.saveAll("matches");
var results = join.apply(firCol, secCol, filter);
var newImgCol = results.map(function(image) {
  var mImg = ee.ImageCollection.fromImages(image.get("matches"))
              .mean();
  var date = image.get("date");
  mImg = mImg.set("date", date);
  mImg = mImg.set("system:index", date);
  mImg = mImg.set("system:time_start", ee.Date.parse("yyyyMM", date).millis());
  return mImg;
});
newImgCol = ee.ImageCollection(newImgCol)
            .sort("system:time_start");
print("month mean imageCollection", newImgCol);
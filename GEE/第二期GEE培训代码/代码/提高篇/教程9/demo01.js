var mod10a1 = ee.ImageCollection("MODIS/006/MOD10A1");
var start_date = "2018-1-1";
var end_date = "2019-1-1";
var sCol = mod10a1.filterDate(start_date, end_date)
                  .map(function(image) {
                    var time_start = ee.Date(image.get("system:time_start"));
                    var date = time_start.format("yyyyMM");
                    image = image.set("date", date);
                    return image;
                  });
                  
print("raw imageCollection", sCol);
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

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
var yearImgList = yearList.map(function(year) {
  year = ee.Number(year);
  var _sdate = ee.Date.fromYMD(year, 1, 1);
  var _edate = ee.Date.fromYMD(year.add(1), 1, 1);
  
  var tempCol = lxCol.filterDate(_sdate, _edate);
  var img = tempCol.median();
  img = img.set("year", year);
  img = img.set("system:index", ee.String(year.toInt()));
  return img;
});
var yearImgCol = ee.ImageCollection.fromImages(yearImgList);
print("year image collection", yearImgCol);
var visParam = {
  min: 0, 
  max: 0.3,
  bands: ["B4", "B3", "B2"]
};
var image = yearImgCol.filter(ee.Filter.eq("year", 2014)).first();
Map.centerObject(roi, 8);
Map.addLayer(image, visParam, "yearImage");

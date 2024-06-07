//代码链接：https://code.earthengine.google.com/7bab9febeead95c65940ec6d45e091fc


// imageCollection save all join
var roi = /* color: #00ff00 */ee.Geometry.Point([116.30968014024995, 39.92236280064687]);
var s2 = ee.ImageCollection("COPERNICUS/S2");
var firCol = s2.filterBounds(roi)
               .filterDate("2018-1-1", "2018-3-1");
print("first sentinel imageCollection", firCol);

var secCol = s2.filterBounds(roi)
               .filterDate("2018-2-1", "2018-4-1");
print("second sentinel imageCollection", secCol);

var filter = ee.Filter.equals({
  leftField: "system:index", 
  rightField: "system:index" 
});
var join = ee.Join.saveAll("matches");
var result = join.apply(firCol, secCol, filter);
print("result is", result);
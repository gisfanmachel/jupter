//代码链接：https://code.earthengine.google.com/2781650f3a987a3e26710d51fc414da4


// imageCollection save best join
var roi = /* color: #00ff00 */ee.Geometry.Point([116.30968014024995, 39.92236280064687]);
var s2 = ee.ImageCollection("COPERNICUS/S2");
var firCol = s2.filterBounds(roi)
               .filterDate("2018-1-1", "2018-3-1");
print("first sentinel imageCollection", firCol);

var secCol = s2.filterBounds(roi)
               .filterDate("2018-2-1", "2018-4-1");
print("second sentinel imageCollection", secCol);

var filter = ee.Filter.maxDifference({
  difference: 20*24*60*60*1000, 
  leftField: "system:time_start", 
  rightField: "system:time_start"
});
var join = ee.Join.saveBest("bestMatch", "timeDiff");
var result = join.apply(firCol, secCol, filter);
print("result is", result);
//代码链接：https://code.earthengine.google.com/7a5dd175fa56b7bef960c1cfdb4ce1d3

//Large Scale International Boundary Lines (LSIB)
var fCol = ee.FeatureCollection("USDOS/LSIB/2013");

var sCol = fCol.limit(10);
print("pre sCol", sCol);

sCol = sCol.map(function(feature) {
  var area = feature.area();
  feature = feature.set("area", area);
  return feature;
});
print("add area properties", sCol);
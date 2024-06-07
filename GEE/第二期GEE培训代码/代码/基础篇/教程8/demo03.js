//代码链接：https://code.earthengine.google.com/25603d0a4194b849da2cc87a3fb5a859

//Large Scale International Boundary Lines (LSIB)
var fCol = ee.FeatureCollection("USDOS/LSIB/2013");
var roi = /* color: #bf04c2 */ee.Geometry.Point([120.92596957445573, 23.827835588423437]);
var sCol = fCol.filterBounds(roi);
print("select sCol", sCol);

Map.centerObject(roi, 9);
Map.addLayer(sCol, {color: "red"}, "roi");
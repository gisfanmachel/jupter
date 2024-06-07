//代码链接：https://code.earthengine.google.com/fe35dfd5a3ddab4a147548a1632fef8f

//Large Scale International Boundary Lines (LSIB)
var fCol = ee.FeatureCollection("USDOS/LSIB/2013");
var roi = /* color: #bf04c2 */ee.Geometry.Point([120.92596957445573, 23.827835588423437]);
var sCol = fCol.filterBounds(roi);
print("select sCol", sCol);

Map.centerObject(roi, 6);
var empty = ee.Image().toByte();
var outline = ee.Image()
                .toByte()
                .paint({
                  featureCollection:sCol,
                  color:0,
                  width:3
                });
Map.addLayer(outline, {palette: "ff0000"}, "outline");
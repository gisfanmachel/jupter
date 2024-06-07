//代码链接：https://code.earthengine.google.com/36cbe7c2f9ee685a83f629ea04fde6e2

var polygon1 = /* color: #d63000 */ee.Geometry.Polygon(
        [[[116.18363255709164, 39.73608336682765],
          [116.62857884615414, 39.75297820506206],
          [116.60660618990414, 40.08580181855619],
          [116.15067357271664, 40.077395868796174]]]);
var polygon2 = /* color: #ffc82d */ee.Geometry.Polygon(
        [[[116.45728060961198, 40.23636657920226],
          [116.42981478929948, 39.97166693527704],
          [116.82806918383073, 39.95903650847623],
          [116.88849398851823, 40.20700637790917]]]);
         

Map.centerObject(polygon1, 9);
Map.addLayer(polygon1, {color: "red"}, "polygon1");
Map.addLayer(polygon2, {color: "blue"}, "polygon2");

//polygon area
print("polygon area is: ", polygon1.area());
//polygon bounds
print("polygon bounds is: ", polygon1.bounds());
//polygon center point
print("polygon centroid is: ", polygon1.centroid());
//polygon coordinates
print("polygon coordinates is: ", polygon1.coordinates());

//check intersects
print("polygon1 and polygon2 is intersects ?", polygon1.intersects(polygon2));
var intersec = polygon1.intersection(polygon2);
Map.addLayer(intersec, {}, "intersec");

//outer 2000m
var bufferPolygon1 = polygon1.buffer(2000);
Map.addLayer(bufferPolygon1, {color:"ff00ff"}, "bufferPolygon1");
//innner 2000m
var bufferPolygon2 = polygon1.buffer(-2000);
Map.addLayer(bufferPolygon2, {color:"00ffff"}, "bufferPolygon2");

//difference
var differ = bufferPolygon1.difference(bufferPolygon2);
Map.addLayer(differ, {color:"green"}, "differ");
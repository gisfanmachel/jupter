//代码链接：https://code.earthengine.google.com/6bcbf82ebedcb626cf1e2e08c29c76f8

var polygon = /* color: #d63000 */ee.Geometry.Polygon(
        [[[116.18363255709164, 39.73608336682765],
          [116.62857884615414, 39.75297820506206],
          [116.60660618990414, 40.08580181855619],
          [116.15067357271664, 40.077395868796174]]]);
         
var feature = ee.Feature(polygon, {year: 2019, count: 100});
Map.centerObject(feature, 9);

//add property
feature = feature.set("desc", "polygon");
print("new feature", feature);
print("feature area", feature.area());
print("feature year", feature.get("year"));

Map.addLayer(feature, {color: "red"}, "feature");

var outterBuffer = feature.buffer(1000);
var innerBuffer = feature.buffer(-1000);
var differ = outterBuffer.difference(innerBuffer);
Map.addLayer(differ, {color: "green"}, "differ");
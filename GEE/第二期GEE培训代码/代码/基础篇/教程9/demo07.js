//代码链接：https://code.earthengine.google.com/54a567e0d3b52d5c317a1be5ab253eb5


//reduceToVectors
var roi = /* color: #999900 */ee.Geometry.Polygon(
        [[[116.21437502022764, 39.62355024325724],
          [116.82960939522764, 39.75881346356145],
          [116.75270509835264, 40.213367999414956],
          [115.97816896554014, 40.17140672221596]]]);
Map.centerObject(roi, 8);
var image = ee.Image("NOAA/DMSP-OLS/NIGHTTIME_LIGHTS/F182012")
              .select("stable_lights")
              .clip(roi);

var mask = image.gt(30).add(image.gt(60));
mask = mask.updateMask(mask);
mask = mask.addBands(image);
print("mask", mask);

var vectors = mask.reduceToVectors({
  reducer: ee.Reducer.mean(),
  geometry: roi, 
  scale: 1000,
  geometryType: "polygon", 
  maxPixels: 1e13
});

print("vectors", vectors);

Map.addLayer(mask.select("stable_lights"), {min:1, max:2, palette: ["red", "green"]}, "image");

var display = ee.Image()
                .toByte()
                .paint({
                  featureCollection: vectors, 
                  color: null,
                  width: 1
                });
Map.addLayer(display, {palette: "blue"}, "display");
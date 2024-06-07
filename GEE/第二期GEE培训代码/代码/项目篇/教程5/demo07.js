//代码链接：https://code.earthengine.google.com/b903a9afaa7104efa468cc21b831731a

//linearRegression
var roi = /* color: #98ff00 */ee.Geometry.Polygon(
        [[[115.28627108398433, 36.67525024180043],
          [115.30000399414058, 36.671945893730204],
          [115.30000399414058, 36.696174483898005],
          [115.28215121093746, 36.69507334992879]]]);
Map.centerObject(roi, 8);

var l8Col = ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA")
              .filterBounds(roi)
              .filterDate("2019-1-1", "2019-2-1")
              .select(["B5", "B4", "B3"]);
print("l8Col", l8Col);

var image = l8Col.mean().clip(roi);
Map.addLayer(roi, {color:"red"}, "roi");


// b3 = a0 + a1 * b5 + a2 * b4
var lr = ee.Image.constant(1)
            .addBands(image)
            .reduceRegion({
              reducer: ee.Reducer.linearRegression(3,1), 
              geometry: roi, 
              scale: 30
            });
print("linearRegression", lr);
var roi = /* color: #d63000 */ee.Geometry.Polygon(
        [[[117.19846835579438, 31.338582945998613],
          [117.96476474251313, 31.352657172321162],
          [117.93455234016938, 31.822923403887454],
          [117.20396151985688, 31.792580050380295]]]);
Map.centerObject(roi, 9);
var bounds= ee.Image().toByte()
              .paint({
                featureCollection: ee.FeatureCollection([ee.Feature(roi)]),
                color: null,
                width: 1
              });
Map.addLayer(bounds, {palette: "red"}, "bounds");
var startDate = ee.Date("2013-1-1");
var endDate  =ee.Date("2019-1-1");
var l8Col = ee.ImageCollection("LANDSAT/LC08/C01/T1_SR")
              .filterBounds(roi)
              .filterDate(startDate, endDate)
              .filter(ee.Filter.lte("CLOUD_COVER", 50))
              .map(function(image) {
                var cloudShadowBitMask = 1 << 3;
                var cloudsBitMask = 1 << 5;
                var snowBitMask = 1 << 4;
                var qa = image.select('pixel_qa');
                var mask = qa.bitwiseAnd(cloudShadowBitMask).eq(0)
                             .and(qa.bitwiseAnd(cloudsBitMask).eq(0))
                             .and(qa.bitwiseAnd(snowBitMask).eq(0));
                return image.updateMask(mask);
              })
              .map(function(image) {
                var time_start = image.get("system:time_start");
                image = image.multiply(0.0001);
                image = image.set("system:time_start", time_start);
                return image;
              });
print("l8Col", l8Col);
var vis = {
  min:0,
  max:0.3,
  bands:["B4", "B3", "B2"]
};
Map.addLayer(l8Col.filterDate("2013-1-1", "2014-1-1").median().clip(roi), vis, "2013");
Map.addLayer(l8Col.filterDate("2014-1-1", "2015-1-1").median().clip(roi), vis, "2014");
Map.addLayer(l8Col.filterDate("2015-1-1", "2016-1-1").median().clip(roi), vis, "2015");
Map.addLayer(l8Col.filterDate("2016-1-1", "2017-1-1").median().clip(roi), vis, "2016");
Map.addLayer(l8Col.filterDate("2017-1-1", "2018-1-1").median().clip(roi), vis, "2017");
Map.addLayer(l8Col.filterDate("2018-1-1", "2019-1-1").median().clip(roi), vis, "2018");

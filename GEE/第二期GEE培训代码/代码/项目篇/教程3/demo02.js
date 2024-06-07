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
              })
              .map(function(image) {
                return image.addBands(image.normalizedDifference(["B3", "B6"])
                            .rename("MNDWI"));
              })
              .select(["B4", "B3", "B2", "MNDWI"]);
print("l8Col", l8Col);
var vis1 = {
  min:0,
  max:0.3,
  bands:["B4", "B3", "B2"]
};
Map.addLayer(l8Col.median().clip(roi), vis1, "l8RGB");
var vis2 = {
  min: -1,
  max: 1
};
Map.addLayer(l8Col.median().select("MNDWI").clip(roi), vis2, "l8MNDWI");

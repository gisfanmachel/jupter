var MYD11A2 = ee.ImageCollection("MODIS/006/MYD11A2");
var roi = /* color: #98ff00 */ee.Geometry.Polygon(
        [[[115.8532392366792, 38.32541689504168],
          [116.6991865023042, 38.295244855891625],
          [116.6552411898042, 38.92194363390602],
          [115.9740888460542, 38.92194363390602]]]);
          
var startDate = "2014-01-01";
var endDate = "2014-12-31";
Map.centerObject(roi, 9);
Map.addLayer(roi, {}, "roi");

var sCol = MYD11A2.filterDate(startDate, endDate)
                  .select("LST_Night_1km")
                  .map(function(image) {
                    var time_end = ee.Date(image.get("system:time_end"))
                                     .format("D");
                    var doy = ee.Image.constant(ee.Number.parse(time_end))
                                .rename("doy")
                                .toUint16();
                    var lst = image.multiply(0.02)
                                   .subtract(273.15)
                                   .rename("lst");
                    return lst.addBands(doy);
                  }).sort("system:time_start");
print("sCol", sCol);
var sdayImg = sCol.map(function(image) {
                    image = image.updateMask(image.select("lst").gte(0));
                    return image;
                  })
                  .select(["doy", "lst"])
                  .reduce(ee.Reducer.min(2).setOutputs(["doy", "lst"]))
                  .select("doy")
                  .clip(roi);
var edayImg = sCol.map(function(image) {
                    image = image.updateMask(image.select("lst").gte(20));
                    return image;
                  })
                  .select(["doy", "lst"])
                  .reduce(ee.Reducer.min(2).setOutputs(["doy", "lst"]))
                  .select("doy")
                  .clip(roi);

var visParams = {
  min:0,
  max:250,
  palette:["0000ff","00ff00","ff0000"]
};
Map.addLayer(sdayImg, visParams, "sdayImg");
Map.addLayer(edayImg, visParams, "edayImg");

var l8Img = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
              .filterDate(startDate, endDate)
              .filterBounds(roi)
              .map(function(image) {
                var ndvi = image.normalizedDifference(["B5","B4"]);
                return image.addBands(ndvi.rename("NDVI"));
              })
              .map(function(image) {
                var doy = ee.Number.parse(ee.Date(image.get("system:time_start")).format("D"));
                image = image.updateMask(sdayImg.lte(doy).and(edayImg.gte(doy)));
                return image;
              })
              .select("NDVI")
              .mean();

print("l8Img", l8Img);
var ndviVis = {
  min:-0.2,
  max:0.8,
  palette: 'FFFFFF, CE7E45, DF923D, F1B555, FCD163, 99B718, 74A901, 66A000, 529400,' +
    '3E8601, 207401, 056201, 004C00, 023B01, 012E01, 011D01, 011301'
};
Map.addLayer(l8Img, ndviVis, "NDVI");

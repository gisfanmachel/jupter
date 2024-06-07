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
              .select("MNDWI");
print("l8Col", l8Col);

//大津算法（otsu）
function otsu(histogram) {
  var counts = ee.Array(ee.Dictionary(histogram).get('histogram'));
  var means = ee.Array(ee.Dictionary(histogram).get('bucketMeans'));
  var size = means.length().get([0]);
  var total = counts.reduce(ee.Reducer.sum(), [0]).get([0]);
  var sum = means.multiply(counts).reduce(ee.Reducer.sum(), [0]).get([0]);
  var mean = sum.divide(total);
  var indices = ee.List.sequence(1, size);
  var bss = indices.map(function(i) {
    var aCounts = counts.slice(0, 0, i);
    var aCount = aCounts.reduce(ee.Reducer.sum(), [0]).get([0]);
    var aMeans = means.slice(0, 0, i);
    var aMean = aMeans.multiply(aCounts)
        .reduce(ee.Reducer.sum(), [0]).get([0])
        .divide(aCount);
    var bCount = total.subtract(aCount);
    var bMean = sum.subtract(aCount.multiply(aMean)).divide(bCount);
    return aCount.multiply(aMean.subtract(mean).pow(2)).add(
           bCount.multiply(bMean.subtract(mean).pow(2)));
  });
  return means.sort(bss).get([-1]);
}

var yearList = ee.List.sequence(startDate.get("year"), ee.Number(endDate.get("year")).subtract(1));
print("yearList", yearList);
var yearImgList = yearList.map(function(year) {
  year = ee.Number(year).toInt();
  var tempCol = l8Col.filterDate(ee.Date.fromYMD(year, 1, 1), ee.Date.fromYMD(year.add(1), 1, 1));
  var yearImg = tempCol.median().clip(roi);
  var histogram = yearImg.reduceRegion({
    reducer: ee.Reducer.histogram(), 
    geometry: roi, 
    scale: 30,
    maxPixels: 1e13,
    tileScale: 8
  });
  var threshold = otsu(histogram.get("MNDWI"));
  var mask = yearImg.gte(threshold);
  var water = mask.updateMask(mask).rename("water");
  water = water.set("year", year);
  water = water.set("threshold", threshold);
  water = water.set("system:index", ee.String(year.toInt()));
  return water.toByte();
});
var yearImgCol = ee.ImageCollection.fromImages(yearImgList);
print("yearImgCol", yearImgCol);
Map.addLayer(yearImgCol.filter(ee.Filter.eq("year", 2013)), {palette: "red"}, "2013");

var l8 = ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA"),
    geometry = /* color: #d63000 */ee.Geometry.Point([114.49000404217372, 33.25441034937943]);
Map.centerObject(geometry, 6);
Map.addLayer(geometry);

//NDVI: (B05 - B04)/(B05 + B04)
function NDVI(image) {
  var ndvi = image.normalizedDifference(["B5", "B4"]);
  return image.addBands(ndvi.rename("NDVI"));
}
var ndviCol = l8.filterBounds(geometry)
               .filterDate('2015-4-1','2015-10-1')
               .map(NDVI)
               .select("NDVI")
               .map(function(image) {
                 image = image.where(image.gte(0.3), 1);
                 image = image.where(image.lt(0.3), 0);
                 return image;
               });
print("ndviCol", ndviCol);
var count = ndviCol.size();
Map.addLayer(ndviCol, {min:0, max:1}, "ndviCol");
var newImg = ndviCol.toBands();
var sumImg = newImg.reduce(ee.Reducer.sum());
Map.addLayer(sumImg, {}, "all-sum");
Map.addLayer(sumImg.updateMask(sumImg.eq(0)), {palette: "red"}, "equal-min");
Map.addLayer(sumImg.updateMask(sumImg.eq(count)), {palette: "blue"}, "equal-max");

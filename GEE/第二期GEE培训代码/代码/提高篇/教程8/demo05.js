var l8 = ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA"),
    roi = /* color: #d63000 */ee.Geometry.Point([-101.17656249999999, 35.804180120545844]);
var scol = l8.filterDate("2018-1-1", "2018-4-1")
             .filterBounds(roi)
             .map(function(image){
               var time_start = image.get("system:time_start");
               var doy = ee.Number.parse(ee.Date(time_start).format("D")).toInt();
               image = image.addBands(ee.Image.constant(doy).toByte().rename("doy"));
               return image;
             })
             .select(["B1", "doy"]);
print("scol", scol);
Map.addLayer(scol, {}, "scol");
// ee.Reducer.min()
var nscol = scol.map(function(image) {
  image = image.addBands(ee.Image.pixelLonLat());
  return image;
});
print("nscol", nscol);
var img_min1 = nscol.reduce(ee.Reducer.min(4).setOutputs(["B1_min", "doy", "lon", "lat"]));
Map.addLayer(img_min1, {}, "img_min1");
Map.centerObject(roi, 9);
Map.addLayer(roi, {color:"red"}, "roi");

var roi = ee.Geometry.Polygon(
        [[[116.30779856285369, 38.66613315895223],
          [116.30779856285369, 38.61679196369789],
          [116.37646311363494, 38.61679196369789],
          [116.37646311363494, 38.66613315895223]]], null, false);
Map.centerObject(roi, 8);  
Map.addLayer(roi, {color: "red"}, "roi");
var sCol = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA')
             .filterBounds(roi)
             .filterDate("2018-1-1", "2019-1-1")
             .map(ee.Algorithms.Landsat.simpleCloudScore)
             .map(function(image) {
               image = image.updateMask(image.select("cloud").lte(10));
               return image;
             })
             .map(function(image) {
               var ndvi = image.normalizedDifference(["B5", "B4"]).rename("NDVI");
               return image.addBands(ndvi);
             })
             .select("NDVI")
             .map(function(image) {
               var dict = image.reduceRegion({
                 reducer: ee.Reducer.mean(),
                 geometry: roi,
                 scale: 30,
                 maxPixels: 1e13,
                 tileScale: 4
               });
               var ndvi = ee.Number(ee.Dictionary(dict).get("NDVI"));
               image = image.set("ndvi", ndvi);
               return image;
             });
print("raw image collection", sCol);
sCol = sCol.filter(ee.Filter.gte("ndvi", 0.3));
print("select image collection", sCol);

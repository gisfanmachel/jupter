//https://code.earthengine.google.com/d9ce598460d32be2f06adaef21521b6f

var l8 = ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA"),
    roi = 
    /* color: #0b4a8b */
    /* displayProperties: [
      {
        "type": "rectangle"
      }
    ] */
    ee.Geometry.Polygon(
        [[[116.83702540926652, 38.634464840091724],
          [116.83702540926652, 38.49809751139009],
          [117.10619044832902, 38.49809751139009],
          [117.10619044832902, 38.634464840091724]]], null, false);
Map.centerObject(roi, 8);
var image = l8.filterBounds(roi)
              .filterDate("2018-4-1", "2018-8-1")
              .map(ee.Algorithms.Landsat.simpleCloudScore)
              .map(function(image) {
                return image.updateMask(image.select("cloud").lte(5));
              })
              .map(function(image) {
                return image.addBands(image.normalizedDifference(["B5", "B4"]).rename("NDVI"));
              })
              .median()
              .select("NDVI")
              .clip(roi);
var chart = ui.Chart.image.histogram({
  image: image, 
  region: roi, 
  scale: 30
});
print("NDVI", chart);

Map.addLayer(image, {min:-0.1, max:0.8}, "gray NDVI");

// 设置两个值间隔样式 intervals
var sld_intervals =
  '<RasterSymbolizer>' +
    '<ColorMap  type="intervals" extended="false" >' +
      '<ColorMapEntry color="#ff0000" quantity="0.1" label="0.1" opacity="1"/>' +
      '<ColorMapEntry color="#00ff00" quantity="0.2" label="0.2" opacity="0"/>' +
      '<ColorMapEntry color="#0000ff" quantity="0.35" label="0.35" opacity="1"/>' +
      '<ColorMapEntry color="#ffff00" quantity="0.5" label="0.5" opacity="1"/>' +
      '<ColorMapEntry color="#000000" quantity="1" label="1" opacity="1"/>' +
    '</ColorMap>' +
  '</RasterSymbolizer>';
Map.addLayer(image.sldStyle(sld_intervals), {}, 'SLD intervals');

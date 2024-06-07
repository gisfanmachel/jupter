// Function to mask clouds using the Sentinel-2 QA band.
function maskS2clouds(image) {
  var qa = image.select('QA60')

  // Bits 10 and 11 are clouds and cirrus, respectively.
  var cloudBitMask = 1 << 10;
  var cirrusBitMask = 1 << 11;

  // Both flags should be set to zero, indicating clear conditions.
  var mask = qa.bitwiseAnd(cloudBitMask).eq(0).and(
             qa.bitwiseAnd(cirrusBitMask).eq(0))

  // Return the masked and scaled data, without the QA bands.
  return image.updateMask(mask).divide(10000)
      .select("B.*")
      .copyProperties(image, ["system:time_start"])
}


// Load Sentinel-2 TOA reflectance data.
var collection = ee.ImageCollection('COPERNICUS/S2')
    .filterBounds(table)
    .filterDate( '2019-04-01', '2019-10-30')
    // Pre-filter to get less cloudy granules.
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))
    .map(maskS2clouds)

var composite = collection.median()

// clip
var clipped = composite.clipToCollection(table);

// 进行图像显示
Map.setCenter(108.5, 30.7, 9);

var classNames = zy.merge(jz).merge(sx).merge(ss).merge(qt);
var bands = ['B2', 'B3', 'B4', 'constant'];
var training = clipped.select(bands).sampleRegions({
  collection: classNames,
  properties: ['landc'],
  scale: 10
});

var classifier = ee.Classifier.svm().train(training,'landc',bands)
var classified = clippedall.select(bands).classify(classifier)

//display result
Map.centerObject(table, 9);
Map.addLayer(classified,
{min: 1, max: 5, palette: ['green','red','blue','#15ffef','#4ffff3','#fb90ff']},'classification')

//export image
Export.image.toDrive({
  image: classified,
  description: "classified",
  fileNamePrefix: "classified",
  scale:10,
  region: c7,
  crs: "EPSG:4326",
  maxPixels: 99999999999
  })
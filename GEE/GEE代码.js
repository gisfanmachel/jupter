﻿# 三峡库区的水系

// This example uses the Sentinel-2 QA band to cloud mask
// the collection.  The Sentinel-2 cloud flags are less
// selective, so the collection is also pre-filtered by the
// CLOUDY_PIXEL_PERCENTAGE flag, to use only relatively
// cloud-free granule.

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

// Map the function over one year of data and take the median.
// Load Sentinel-2 TOA reflectance data.
var collection = ee.ImageCollection('COPERNICUS/S2')
    .filterBounds(table)
    .filterDate('2019-11-15', '2019-12-30')
    // Pre-filter to get less cloudy granules.
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
    .map(maskS2clouds)

var composite = collection.median()

// 进行裁剪
var clipped = composite.clip(table);
// 进行图像显示
Map.setCenter(116.33, 40.0, 9);
Map.addLayer(clipped, {bands: ['B11', 'B3', 'B4'], min: 0, max:0.3}, 'RGB')


var classNames = jz.merge(gef).merge(shuixi).merge(linc);
var bands = ['B2', 'B3', 'B4',  'B8',  'B11',  'B6'];
var training = clipped.select(bands).sampleRegions({
  collection: classNames,
  properties: ['landc'],
  scale: 10
});

var classifier = ee.Classifier.cart().train(training,'landc',bands)
var classified = clipped.select(bands).classify(classifier)

Map.centerObject(table, 9);
Map.addLayer(classified,
{min: 1, max: 6, palette: ['red','blue','yellow','green']},'classification')
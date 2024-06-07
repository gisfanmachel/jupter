//代码链接：https://code.earthengine.google.com/4dbdbf1f20122323096b3756609f052c

var roi = /* color: #0b4a8b */ee.Geometry.Polygon(
        [[[115.22447911987308, 38.97207826950874],
          [117.64147130737308, 39.07450027191289],
          [117.55358068237308, 40.67633196985795],
          [114.91686193237308, 40.576272152256934]]]);
Map.centerObject(roi, 7);

// SimpleCloudScore, an example of computing a cloud-free composite with L8
// by selecting the least-cloudy pixel from the collection.
// Compute a cloud score.  This expects the input image to have the common
// band names: ["red", "blue", etc], so it can work across sensors.
var cloudScore = function(img) {
  // A helper to apply an expression and linearly rescale the output.
  var rescale = function(img, exp, thresholds) {
    return img.expression(exp, {img: img})
        .subtract(thresholds[0]).divide(thresholds[1] - thresholds[0]);
  };

  // Compute several indicators of cloudyness and take the minimum of them.
  var score = ee.Image(1.0);
  // Clouds are reasonably bright in the blue band.
  score = score.min(rescale(img, 'img.blue', [0.1, 0.3]));

  // Clouds are reasonably bright in all visible bands.
  score = score.min(rescale(img, 'img.red + img.green + img.blue', [0.2, 0.8]));

  // Clouds are reasonably bright in all infrared bands.
  score = score.min(rescale(img, 'img.nir + img.swir1 + img.swir2', [0.3, 0.8]));

  // However, clouds are not snow.
  var ndsi = img.normalizedDifference(['green', 'swir1']);
  return score.min(rescale(ndsi, 'img', [0.8, 0.6]));
};

function addCloudScore(image) {
  // A mapping from a common name to the sensor-specific bands.
  var S2_BANDS = ['B2',   'B3',    'B4',  'B8',  'B11',    'B12'];
  var STD_NAMES = ['blue', 'green', 'red', 'nir', 'swir1', 'swir2'];

  image = image.divide(10000);
  // Invert the cloudscore so 1 is least cloudy, and rename the band.
  var score = cloudScore(image.select(S2_BANDS, STD_NAMES));
  score = score.multiply(100).byte();
  return image.addBands(score.rename('cloud'));
}

function rmCloud(image) {
  return image.updateMask(image.select("cloud").lte(20));
}

var image = ee.ImageCollection('COPERNICUS/S2')
              .filterDate('2018-1-1', '2019-1-1')
              .filterBounds(roi)
              .map(addCloudScore)
              .map(rmCloud)
              .median()
              .clip(roi);
var rgbVis = {
  min: 0,
  max: 0.3,
  bands: ['B4', 'B3', 'B2'],
};

Map.addLayer(image, rgbVis, 'RGB');
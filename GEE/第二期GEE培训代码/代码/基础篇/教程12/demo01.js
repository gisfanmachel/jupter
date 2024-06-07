//代码链接：https://code.earthengine.google.com/3f7e50ebdfbbc74aa6355aa2b2a94ccc


var roi = /* color: #0b4a8b */ee.Geometry.Polygon(
        [[[115.22447911987308, 38.97207826950874],
          [117.64147130737308, 39.07450027191289],
          [117.55358068237308, 40.67633196985795],
          [114.91686193237308, 40.576272152256934]]]);
Map.centerObject(roi, 7);

function rmCloud(image) {
  var mask = image.select("cloud").lte(10);
  return image.updateMask(mask);
}

var image = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA')
              .filterDate('2018-01-01', '2019-1-1')
              .filterBounds(roi)
              .map(ee.Algorithms.Landsat.simpleCloudScore)
              .map(rmCloud)
              .median()
              .clip(roi);

var visParams = {
  bands: ['B4', 'B3', 'B2'],
  min: 0,
  max: 0.3
};
Map.addLayer(image, visParams, "image");
//代码链接：https://code.earthengine.google.com/dc10f7a140c1f3bd2fe51aa30dfab0a8


var roi = /* color: #0b4a8b */ee.Geometry.Polygon(
        [[[115.22447911987308, 38.97207826950874],
          [117.64147130737308, 39.07450027191289],
          [117.55358068237308, 40.67633196985795],
          [114.91686193237308, 40.576272152256934]]]);
Map.centerObject(roi, 7);

function rmCloud(image) {
  var qa = image.select('QA60');
  var cloudBitMask = 1 << 10;
  var cirrusBitMask = 1 << 11;
  var mask = qa.bitwiseAnd(cloudBitMask).eq(0)
               .and(qa.bitwiseAnd(cirrusBitMask).eq(0));
  return image.updateMask(mask);
}

var image = ee.ImageCollection('COPERNICUS/S2')
              .filterDate('2018-1-1', '2019-1-1')
              .filterBounds(roi)
              .map(rmCloud)
              .median()
              .clip(roi);
var rgbVis = {
  min: 0,
  max: 3000,
  bands: ['B4', 'B3', 'B2'],
};

Map.addLayer(image, rgbVis, 'RGB');
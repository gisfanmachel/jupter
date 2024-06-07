//代码链接：https://code.earthengine.google.com/6c7863acf90a59607fd4ec2cd6beadde


var roi = /* color: #0b4a8b */ee.Geometry.Polygon(
        [[[115.22447911987308, 38.97207826950874],
          [117.64147130737308, 39.07450027191289],
          [117.55358068237308, 40.67633196985795],
          [114.91686193237308, 40.576272152256934]]]);
Map.centerObject(roi, 7);

function rmCloud(image) {
  var cloudShadowBitMask = (1 << 3);
  var cloudsBitMask = (1 << 5);
  var qa = image.select("pixel_qa");
  var mask = qa.bitwiseAnd(cloudShadowBitMask).eq(0)
                 .and(qa.bitwiseAnd(cloudsBitMask).eq(0));
  return image.updateMask(mask);
}

var image = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
              .filterDate('2018-01-01', '2019-1-1')
              .filterBounds(roi)
              .map(rmCloud)
              .median()
              .clip(roi);

var visParams = {
  bands: ['B4', 'B3', 'B2'],
  min: 0,
  max: 3000
};
Map.addLayer(image, visParams, "image");
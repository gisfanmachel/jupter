//代码链接：https://code.earthengine.google.com/7b7d7091dd1c341b0fc5fabbfe0ca04d


var fCol1 = ee.FeatureCollection([
  ee.Feature(null, {count: 1}),
  ee.Feature(null, {count: 2}),
  ee.Feature(null, {count: 3})
]);

var fCol2 = ee.FeatureCollection([
  ee.Feature(null, {count: 11}),
  ee.Feature(null, {count: 21}),
  ee.Feature(null, {count: 31})
]);

var fCol3 = fCol1.merge(fCol2);
print("fCol3", fCol3);
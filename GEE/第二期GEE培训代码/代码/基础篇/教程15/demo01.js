//代码链接：https://code.earthengine.google.com/fecd6f248a863e9068fa5d44e6856720

// featureCollection simple join
var primaryCol = ee.FeatureCollection([
  ee.Feature(null, {p1: 0, p2: "a"}),
  ee.Feature(null, {p1: 1, p2: "b"}),
  ee.Feature(null, {p1: 2, p2: "c"})
]);

var secondaryCol = ee.FeatureCollection([
  ee.Feature(null, {p3: 1, p4: "d"}),
  ee.Feature(null, {p3: 2, p4: "e"}),
  ee.Feature(null, {p3: 3, p4: "f"})
]);

var filter = ee.Filter.equals({
  leftField: "p1",
  rightField: "p3"
});
var join = ee.Join.simple();
var result = join.apply(primaryCol, secondaryCol, filter);

print("join result", result);
//代码链接：https://code.earthengine.google.com/077bd8d668812a3ace2b0e9ab35261fd

// featureCollection save all join
var primaryCol = ee.FeatureCollection([
  ee.Feature(null, {p1: 0, p2: "a"}),
  ee.Feature(null, {p1: 1, p2: "b"}),
  ee.Feature(null, {p1: 2, p2: "c"})
]);

var secondaryCol = ee.FeatureCollection([
  ee.Feature(null, {p3: 1, p4: "d"}),
  ee.Feature(null, {p3: 1, p4: "e"}),
  ee.Feature(null, {p3: 2, p4: "f"}),
  ee.Feature(null, {p3: 3, p4: "g"})
]);

var filter = ee.Filter.equals({
  leftField: "p1",
  rightField: "p3"
});
var join = ee.Join.saveAll("matches");
var result = join.apply(primaryCol, secondaryCol, filter);

print("join result", result);
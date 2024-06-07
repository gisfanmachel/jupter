//代码链接：https://code.earthengine.google.com/695291abbce2ae89ebc84931a31043a3


// featureCollection save best join
var primaryCol = ee.FeatureCollection([
  ee.Feature(null, {p1: 0, p2: "a"}),
  ee.Feature(null, {p1: 1, p2: "b"}),
  ee.Feature(null, {p1: 2, p2: "c"})
]);

var secondaryCol = ee.FeatureCollection([
  ee.Feature(null, {p3: 3, p4: "d"}),
  ee.Feature(null, {p3: 4, p4: "e"}),
  ee.Feature(null, {p3: 5, p4: "f"}),
  ee.Feature(null, {p3: 6, p4: "g"})
]);


var filter = ee.Filter.maxDifference({
  difference: 2, 
  leftField: "p1", 
  rightField: "p3"
});

var join = ee.Join.saveBest("bestMatch", "timeDiff");
var result = join.apply(primaryCol, secondaryCol, filter);

print("join result", result);
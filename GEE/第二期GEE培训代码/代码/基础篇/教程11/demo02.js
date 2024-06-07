//代码链接：https://code.earthengine.google.com/a5176abcbbb9c50c179fda7b9e21131f


//1. loop
var roi = /* color: #d63000 */ee.Geometry.Point([120.96699218749995, 23.74985033115684]);
var fCol = ee.FeatureCollection("USDOS/LSIB/2013")
             .filterBounds(roi);
print("fCol", fCol);

//(1) map() 使用map方式
var sCol1 = fCol.map(function(feature) {
  var area = feature.area();
  feature = feature.set("area", area);
  return feature;
});
print("sCol1", sCol1);

//(2) iterate() 使用iterate方式
var fColList = fCol.iterate(function(data, list){
  data = ee.Feature(data);
  list = ee.List(list);
  var area = data.area();
  data = data.set("area", area);
  return list.add(data);
}, ee.List([]));
var sCol2 = ee.FeatureCollection(ee.List(fColList));
print("sCol2", sCol2);

//(3) evaluate() 使用异步方式
var fIds = fCol.reduceColumns(ee.Reducer.toList(), ["system:index"])
               .get("list");
fIds.evaluate(function(ids) {
  print("ids is: ", ids.length);
  var fList = [];
  
  for (var i=0; i<ids.length; i++) {
    var feature = fCol.filter(ee.Filter.eq("system:index", ids[i]))
                      .first();
    feature = ee.Feature(feature);
    var area = feature.area();
    feature = feature.set("area", area);
    fList.push(feature);
  }
  var sCol3 = ee.FeatureCollection(fList);
  print("sCol3", sCol3);
});
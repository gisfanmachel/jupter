//代码链接：https://code.earthengine.google.com/7b42d16645c9f25a764c3d125449adc6


//1. loop
var roi = /* color: #0b4a8b */ee.Geometry.Polygon(
        [[[120.95600585937495, 23.860418455104288],
          [121.10981445312495, 23.860418455104288],
          [121.12080078124995, 23.960853112476986],
          [120.94501953124995, 23.960853112476986]]]);
var l8Col = ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA")
              .filterBounds(roi)
              .filterDate("2018-1-1", "2018-6-1")
              .map(function(image){
                return image.addBands(image.normalizedDifference(["B5", "B4"]).rename("NDVI"));
              })
              .select("NDVI")
              .sort("system:time_start");
print("l8Col", l8Col);

//(1) map() 使用map方式
var sCol1 = l8Col.map(function(image) {
  var dict = image.reduceRegion({
    reducer: ee.Reducer.mean(),
    geometry: roi,
    scale: 30
  });
  var ndvi = ee.Number(dict.get("NDVI"));
  image = image.set("ndvi", ndvi);
  return image;
});
print("sCol1", sCol1);

//(2) iterate() 使用iterate方式
var imgColList = sCol1.iterate(function(data, list){
  data = ee.Image(data);
  list = ee.List(list);
  var preNDVI = ee.Image(list.get(-1)).get("ndvi");
  preNDVI = ee.Number(preNDVI);
  var curNDVI = ee.Number(data.get("ndvi"));
  var differ = curNDVI.subtract(preNDVI);
  data = data.set("differ", differ);
  return list.add(data);
}, ee.List([sCol1.first()]));
imgColList = ee.List(imgColList);
imgColList = imgColList.slice(1);
var sCol2 = ee.ImageCollection.fromImages(imgColList);
print("sCol2", sCol2);

//(3) evaluate() 使用异步方式
var imgIds = l8Col.reduceColumns(ee.Reducer.toList(), ["system:index"])
                .get("list");
imgIds.evaluate(function(ids) {
  print("ids is: ", ids.length);
  var imageList = [];
  
  for (var i=0; i<ids.length; i++) {
    var image = l8Col.filter(ee.Filter.eq("system:index", ids[i]))
                     .first();
    image = ee.Image(image);
    var dict = image.reduceRegion({
      reducer: ee.Reducer.mean(),
      geometry: roi,
      scale: 30
    });
    var ndvi = ee.Number(dict.get("NDVI"));
    image = image.set("ndvi", ndvi);
    imageList.push(image);
  }
  var sCol3 = ee.ImageCollection.fromImages(imageList);
  print("sCol3", sCol3);
});
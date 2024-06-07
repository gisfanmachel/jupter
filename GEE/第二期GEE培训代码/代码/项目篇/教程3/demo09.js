var roi = /* color: #d63000 */ee.Geometry.Polygon(
        [[[117.19846835579438, 31.338582945998613],
          [117.96476474251313, 31.352657172321162],
          [117.93455234016938, 31.822923403887454],
          [117.20396151985688, 31.792580050380295]]]);
Map.centerObject(roi, 9);
var bounds= ee.Image().toByte()
              .paint({
                featureCollection: ee.FeatureCollection([ee.Feature(roi)]),
                color: null,
                width: 1
              });
Map.addLayer(bounds, {palette: "red"}, "bounds");

var imgList = [];
var start_year = 2013;
var end_year = 2018;
for (var year=start_year; year<=end_year; year++) {
  var img = ee.Image("users/wangweihappy0/training02/chaohu-mndwi-"+year);
  Map.addLayer(img, {palette: "red"}, ""+year, false);
  imgList.push(img);
}
var imgCol = ee.ImageCollection.fromImages(imgList);
var dataList = imgCol.reduceColumns(ee.Reducer.toList(2), ["area", "year"])
                     .get("list");
dataList.evaluate(function(datas) {
  print("datas is", datas);
  var areaValue = [];
  var yearValue = [];
  for (var i=0; i<datas.length; i++) {
    areaValue.push(datas[i][0]);
    yearValue.push(ee.Number(datas[i][1]).toInt());
  }
  var chart = ui.Chart.array.values(ee.List(areaValue), 0, ee.List(yearValue))
                .setSeriesNames(['巢湖面积'])
                .setOptions({
                  title: "巢湖面积年度变化", 
                  hAxis: {title: '年份'},
                  vAxis: {title: "面积（平方公里）"},
                  legend: null,
                  lineWidth: 1, 
                  pointSize: 2
                });
  print("水域面积年度变化", chart);
});

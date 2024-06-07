var roi = ee.Geometry.Polygon(
        [[[97.35198840029386, 38.44010528815348],
          [97.35198840029386, 38.164216161700466],
          [97.82714709170011, 38.164216161700466],
          [97.82714709170011, 38.44010528815348]]], null, false);
Map.centerObject(roi, 10);
Map.addLayer(roi, {color: "red"}, "roi", false);

var syear = 2014;
var eyear = 2015;
var fCol = ee.FeatureCollection("users/wangweihappy0/training02/halahuIceArea")
            .filter(ee.Filter.and(ee.Filter.gte("year", syear), ee.Filter.lte("year", eyear)))
            .map(function(feature) {
              var area_ice = feature.get("area_ice");
              area_ice = ee.Algorithms.If(area_ice, ee.Number(area_ice), 0);
              area_ice = ee.Number(area_ice);
              feature = feature.set("area_ice", area_ice);
              var area_cloud = feature.get("area_cloud");
              area_cloud = ee.Algorithms.If(area_cloud, ee.Number(area_cloud), 0);
              area_cloud = ee.Number(area_cloud);
              feature = feature.set("area_cloud", area_cloud);
              var area_water = feature.get("area_water");
              area_water = ee.Algorithms.If(area_water, ee.Number(area_water), 0);
              area_water = ee.Number(area_water);
              feature = feature.set("area_water", area_water);
              var percent = area_ice.divide(area_ice.add(area_water));
              feature = feature.set("percent", percent);
              return feature;
            })
            .sort("start_date");

var fList = fCol.reduceColumns(
                  ee.Reducer.toList(2), 
                  ["start_date", "percent"]
                ).get("list");
fList.evaluate(function(datas) {
  print("datas is", datas);
  var yValue = [];
  var xValue = [];
  for (var i=0; i<datas.length; i++) {
    xValue.push(datas[i][0]);
    yValue.push(datas[i][1]);
  }
  var chart = ui.Chart.array.values(ee.List(yValue), 0, ee.List(xValue))
                .setSeriesNames(["比例"])
                .setOptions({
                  title: "冰面积/总面积比例", 
                  hAxis: {title: "年份"},
                  vAxis: {title: "比例"},
                  legend: null,
                  lineWidth:1,
                  pointSize:2
                });
  print("比例变化", chart);
});

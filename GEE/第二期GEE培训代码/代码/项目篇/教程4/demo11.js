var roi = ee.Geometry.Polygon(
        [[[97.35198840029386, 38.44010528815348],
          [97.35198840029386, 38.164216161700466],
          [97.82714709170011, 38.164216161700466],
          [97.82714709170011, 38.44010528815348]]], null, false);
Map.centerObject(roi, 10);
Map.addLayer(roi, {color: "red"}, "roi", false);

var syear = 2014;
var eyear = 2015;
/***
  * 
  * SG滤波方法
  * 
  * */
function sgFilter (y, window_size, order) {
  var half_window = (window_size - 1)/2;
  var deriv = 0;
  var order_range = ee.List.sequence(0,order);
  var k_range = ee.List.sequence(-half_window, half_window);
  
  //b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
  var b = ee.Array(k_range.map(function (k) { return order_range.map(function(o) { return ee.Number(k).pow(o)})}));
  // m = np.linalg.pinv(b).A[deriv] 
  var mPI = b.matrixPseudoInverse();
  var impulse_response = (mPI.slice({axis: 0, start: deriv, end: deriv+1})).project([1]);
  //firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
  var y0 = y.get(0);
  var firstvals = y.slice(1, half_window+1).reverse().map(
    function(e) { return ee.Number(e).subtract(y0).abs().multiply(-1).add(y0) }
  );
  
  //lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
  var yend = y.get(-1);
  var lastvals = y.slice(-half_window-1,-1).reverse().map(
    function(e) { return ee.Number(e).subtract(yend).abs().add(yend) }
  );
  
  // y = np.concatenate((firstvals, y, lastvals))
  var y_ext = firstvals.cat(y).cat(lastvals);
  
  // np.convolve( m, y, mode='valid')
  var runLength = ee.List.sequence(0, y_ext.length().subtract(window_size));
  
  var smooth = runLength.map(function(i) {
    return ee.Array(y_ext.slice(ee.Number(i), ee.Number(i).add(window_size))).multiply(impulse_response).reduce("sum", [0]).get([0]);
  });
  return smooth;
}

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
  xValue = ee.List(xValue);
  yValue = ee.List(yValue);
  
  var window_size = 7;
  var order = 2;
  var smoothValue = sgFilter(yValue, window_size, order);
  smoothValue = smoothValue.map(function(data) {
    data = ee.Number(data);
    data = ee.Algorithms.If(
      data.gte(0), ee.Algorithms.If(data.lte(1), data, 1), 0
    );
    return ee.Number(data);
  });
  
  var chart = ui.Chart.array.values(smoothValue, 0, xValue)
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

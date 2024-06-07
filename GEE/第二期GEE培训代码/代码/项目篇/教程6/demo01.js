var roi = /* color: #d63000 */ee.Geometry.Polygon(
        [[[116.53858050234476, 38.85065269356215],
          [116.58561571962991, 38.83861983850178],
          [116.61720141298929, 38.864822112835554],
          [116.58355578310648, 38.891549176798144],
          [116.55025347597757, 38.87765235804812]]]);
Map.centerObject(roi, 11);
var bounds= ee.Image().toByte()
              .paint({
                featureCollection: ee.FeatureCollection([ee.Feature(roi)]),
                color: null,
                width: 1
              });
Map.addLayer(bounds, {palette: "red"}, "bounds");
var startDate = ee.Date("2015-1-1");
var endDate = ee.Date("2017-1-1");
var l8Col = ee.ImageCollection("LANDSAT/LC08/C01/T1_SR")
              .filterBounds(roi)
              .filterDate(startDate, endDate)
              .map(function(image) {
                var cloudShadowBitMask = 1 << 3;
                var cloudsBitMask = 1 << 5;
                var snowBitMask = 1 << 4;
                var qa = image.select('pixel_qa');
                var mask = qa.bitwiseAnd(cloudShadowBitMask).eq(0)
                             .and(qa.bitwiseAnd(cloudsBitMask).eq(0))
                             .and(qa.bitwiseAnd(snowBitMask).eq(0));
                return image.updateMask(mask);
              })
              .map(function(image) {
                var time_start = image.get("system:time_start");
                image = image.multiply(0.0001);
                image = image.set("system:time_start", time_start);
                return image;
              })
              .map(function(image) {
                return image.addBands(image.normalizedDifference(['B5', 'B4']).rename('NDVI'));
              })
              .select("NDVI")
              .map(function(image) {
                var date = ee.Date(image.get("system:time_start"));
                var years = date.difference(ee.Date("1970-01-01"), "year");
                var yearImg = ee.Image.constant(years);
                image = image.addBands(ee.Image.constant(1).rename("constant"))
                             .addBands(yearImg.rename("t"))
                             .addBands(yearImg.multiply(2 * Math.PI).sin().rename("sin"))
                             .addBands(yearImg.multiply(2 * Math.PI).cos().rename("cos"))
                             .toDouble();
                return image;
              }).sort("system:time_start");
print("l8Col", l8Col);
var vars = ee.List(["constant", "t", "cos", "sin"]);
//使用LinearRegression实现线性拟合
var trend = l8Col.select(vars.add("NDVI"))
                 .reduce(ee.Reducer.linearRegression(4, 1));
//系数转换为多波段影像
var coef = trend.select("coefficients")
                .arrayProject([0])
                .arrayFlatten([vars]);
//计算拟合数据
var result = l8Col.map(function(image) {
  var fitted = image.select(vars)
                    .multiply(coef)
                    .reduce("sum")
                    .rename("fitted");
  return image.addBands(fitted);
});
print("result", result);
var visParam = {
  min: -0.2, 
  max: 0.8,
  palette: 'FFFFFF, CE7E45, DF923D, F1B555, FCD163, 99B718, 74A901, 66A000, 529400,' +
    '3E8601, 207401, 056201, 004C00, 023B01, 012E01, 011D01, 011301'
};
var rawNDVI = l8Col.filter(ee.Filter.eq("system:index", "LC08_123033_20150721"))
                   .first()
                   .select("NDVI")
                   .clip(roi);
Map.addLayer(rawNDVI, visParam, "rawNDVI");
var fitNDVI = result.filter(ee.Filter.eq("system:index", "LC08_123033_20150721"))
                    .first()
                    .select("fitted")
                    .clip(roi);
Map.addLayer(fitNDVI, visParam, "fitNDVI");
//图表展示
var chart = ui.Chart.image.series({
              imageCollection: result.select(["fitted", "NDVI"]),
              region: roi, 
              reducer: ee.Reducer.mean(),
              scale: 30
            })
            .setSeriesNames(["fitted", "NDVI"])
            .setOptions({
              title: "NDVI时间序列函数",
              lineWidth: 1,
              pointSize: 2,
            });
print("chart", chart);

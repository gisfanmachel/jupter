//代码链接：https://code.earthengine.google.com/e0dd90f40a8724762ee2381f867b6494

//linearRegression
var roi = /* color: #00ff00 */ee.Geometry.Point([115.28959384407551, 36.684019932846866]);
Map.centerObject(roi, 8);

var l8Col = ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA")
              .filterBounds(roi)
              .filterDate("2018-1-1", "2019-1-1")
              .map(function(image) {
                //添加常量
                return image.addBands(ee.Image.constant(1).rename("constant"));
              })
              .select(["constant", "B5", "B4"]);
print("l8Col", l8Col);

Map.addLayer(roi, {color:"red"}, "roi");

var trend = l8Col.reduce(ee.Reducer.linearRegression(2, 1));
print("trend", trend);
var xValues = ee.List(["constant", "B5"]);

//trend就是线性回归拟合的参数结果
//从计算结果中获取系数集合（coefficients）波段
//arrayProject：将系数集合降维
//arrayFlatten：将单波段的影像转换为指定参数的多波段影像
//这个图像就是线性回归计算出来的系数影像。
var coefficients = trend.select("coefficients")
                        .arrayProject([0])
                        .arrayFlatten([xValues]);
print("linearRegression coefficients", coefficients);

//将计算的拟合结果添加到影像集合的每一张影像中
var fittedImgCol = l8Col.map(function(image) {
  image = xValues.iterate(function(value, img) {
    value = ee.String(value);
    img = ee.Image(img);
    //提取指定x对应的拟合系数，也就是 y = a0 + a1 * x1 + ... 中的a0, a1...
    var coef = coefficients.select(value);
    return img.addBands(coef.rename(value.cat("_c")));
  }, image);
  image = ee.Image(image);
  
  //将系数带入 y = a0 + a1 * x1 + ... 中生成预测的影像，命名为fitted
  var fittedImg = image.select(xValues)
                       .multiply(coefficients)
                       .reduce("sum")
                       .rename("fitted");
  //将预测结果添加到影像中
  image = image.addBands(fittedImg);
  return image;
});

print("fittedImgCol", fittedImgCol);

Map.addLayer(l8Col.first().select("B4"), {}, "B4");
Map.addLayer(fittedImgCol.first(), {bands: ["fitted"]}, "fitted");
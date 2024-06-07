//代码链接：https://code.earthengine.google.com/35e009c96ff94094d04b8f0dbb8f2b8b


//linearRegression
var roi = /* color: #00ff00 */ee.Geometry.Point([115.28959384407551, 36.684019932846866]);
Map.centerObject(roi, 8);

var l8Col = ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA")
              .filterBounds(roi)
              .filterDate("2018-1-1", "2019-1-1")
              .select(["B5", "B4"]);
print("l8Col", l8Col);

Map.addLayer(roi, {color:"red"}, "roi");

var coefficients = l8Col.reduce(ee.Reducer.linearFit());
print("linearFit coefficients", coefficients);

var coefValues = ee.List(["scale", "offset"]);
//将计算的拟合结果添加到影像集合的每一张影像中
var fittedImgCol = l8Col.map(function(image) {
  image = coefValues.iterate(function(value, img) {
    value = ee.String(value);
    img = ee.Image(img);
    //提取指定x对应的拟合系数，也就是 y = a0 + a1 * x1 + ... 中的a0, a1...
    var coef = coefficients.select(value);
    return img.addBands(coef);
  }, image);
  image = ee.Image(image);
  //添加常量
  image = image.addBands(ee.Image.constant(1).rename("constant"));
  //将系数带入 y = a0 + a1 * x1 + ... 中生成预测的影像，命名为fitted
  var fittedImg = image.select(["B5", "constant"])
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
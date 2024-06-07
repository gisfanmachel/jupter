//代码链接：https://code.earthengine.google.com/48870eea2ac4520d58f21782e17a3d5e

//RMSE MSE R-square

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
var residuals = trend.select("residuals")
                     .arrayProject([0])
                     .arrayFlatten([["residuals"]]);
var RMSE = residuals;
var MSE = RMSE.pow(2);

var n = l8Col.select("B4").count();
var p = ee.Image.constant(2);
var one = ee.Image.constant(1);
var VAR = l8Col.select("B4")
               .reduce(ee.Reducer.sampleVariance());

var R_square = one.subtract(MSE.divide(VAR)).rename("r_square");
print("R_square", R_square);

var R_adjSquare = one.subtract(
                      n.subtract(one)
                      .multiply(one.subtract(R_square))
                      .divide(n.subtract(p).subtract(one))
                    ).rename("r_square_adj");
print("R_adjSquare", R_adjSquare);
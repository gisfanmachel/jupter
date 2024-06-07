//代码链接：https://code.earthengine.google.com/ad78fdab76bf38a392dc74eea7b0972c


//RMSE MSE R-square

//自变量
var x1 = [ 
  -0.05, 0.25,0.60,0, 0.25,0.20, 0.15,0.05,
  -0.15, 0.15, 0.20, 0.10,0.40,0.45,0.35,
  0.30, 0.50,0.50, 0.40,-0.05, -0.05,-0.10,
  0.20,0.10,0.50,0.60,-0.05,0, 0.05, 0.55
];

var x2 = [
  5.50,6.75,7.25,5.50,7.00,6.50,6.75,5.25,
  5.25,6.00, 6.50,6.25,7.00,6.90,6.80,6.80,
  7.10,7.00,6.80,6.50, 6.25,6.00,6.50,7.00,
  6.80,6.80,6.50,5.75,5.80,6.80
];

//因变量
var y = [
  7.38,8.51,9.52,7.50,9.33,8.28,8.75,7.87,
  7.10,8.00, 7.89,8.15,9.10,8.86,8.90,8.87,
  9.26,9.00,8.75,7.95, 7.65,7.27,8.00,8.50,
  8.75,9.21,8.27,7.67,7.93,9.26
];

x1 = ee.List(x1);
x2 = ee.List(x2);
y = ee.List(y);
//线性规划
var indexList = ee.List.sequence(0, y.length().subtract(1));
var arrList = indexList.iterate(function(index, list) {
  index = ee.Number(index);
  list = ee.List(list);
  var cellList = ee.List([
    x1.get(index), 
    x2.get(index),
    y.get(index)
  ]);
  return list.add(cellList);
}, ee.List([]));
arrList = ee.List(arrList);
var lf = arrList.reduce(ee.Reducer.linearRegression(2, 1));
lf = ee.Dictionary(lf);
print(lf);

var coefficients = ee.Array(lf.get("coefficients"));
var residuals = ee.Array(lf.get("residuals"));

var xArray = ee.Array(arrList)
               .slice(1, 0, 2);
var arrShape = xArray.length().toList();
var n = ee.Number(arrShape.get(0));
coefficients = coefficients.transpose()
                           .repeat(0, n);
                           
var y_pred = xArray.multiply(coefficients).reduce(ee.Reducer.sum(), [1]);
var y_raw = ee.Array([y]).transpose();
print("raw y values", y_raw);
print("predict y values", y_pred);

//自己计算 RMSE
var RMSE_self = y_raw.subtract(y_pred)
                .pow(2)
                .reduce(ee.Reducer.mean(), [0])
                .get([0, 0])
                .sqrt();
print("self RMSE", RMSE_self);

//get from gee result
var RMSE = residuals.get([0]);
print("RMSE", RMSE);

var MSE = RMSE.pow(2);
print("MSE", MSE);

var VAR = y_raw.reduce(ee.Reducer.sampleVariance(), [0])
                .get([0, 0]);

var R_square = ee.Number(1)
                .subtract(MSE.divide(VAR));
print("R_square", R_square);

var p = 2;
var R_adjSquare = ee.Number(1)
                    .subtract(
                      n.subtract(1)
                      .multiply(ee.Number(1).subtract(R_square))
                      .divide(n.subtract(p).subtract(1))
                    );
print("R_adjSquare", R_adjSquare);
//代码链接：https://code.earthengine.google.com/a8e6b66dbd623b918d1e3a78c2176b83


//linearRegression

//自变量
var x0 = ee.List.repeat(1, 30);

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
var y1 = [
  7.38,8.51,9.52,7.50,9.33,8.28,8.75,7.87,
  7.10,8.00, 7.89,8.15,9.10,8.86,8.90,8.87,
  9.26,9.00,8.75,7.95, 7.65,7.27,8.00,8.50,
  8.75,9.21,8.27,7.67,7.93,9.26
];
var y2 = [
  8.38,9.51,10.52,8.50,10.33,9.28,9.75,8.87,
  8.10,9.00, 8.89,9.15,10.10,9.86,9.90,9.87,
  10.26,10.00,9.75,8.95, 8.65,8.27,9.00,9.50,
  9.75,10.21,9.27,8.67,8.93,10.26
];

x1 = ee.List(x1);
x2 = ee.List(x2);
y1 = ee.List(y1);
y2 = ee.List(y2);

// y1 = a0 + a1 * x1 + a2 * x2
// y2 = a0 + a1 * x1 + a2 * x2
var indexList = ee.List.sequence(0, x1.length().subtract(1));
var arrList = indexList.iterate(function(index, list) {
  index = ee.Number(index);
  list = ee.List(list);
  var cellList = ee.List([
    x0.get(index), 
    x1.get(index), 
    x2.get(index),
    y1.get(index),
    y2.get(index)
  ]);
  return list.add(cellList);
}, ee.List([]));
arrList = ee.List(arrList);
var lf = arrList.reduce(ee.Reducer.linearRegression(3, 2));
print(lf);
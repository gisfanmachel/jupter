//代码链接：https://code.earthengine.google.com/7fe84e1489933fecee106e115eed64e6

//linearFit
//自变量
var x1 = [ 
  -0.05, 0.25,0.60,0, 0.25,0.20, 0.15,0.05,
  -0.15, 0.15, 0.20, 0.10,0.40,0.45,0.35,
  0.30, 0.50,0.50, 0.40,-0.05, -0.05,-0.10,
  0.20,0.10,0.50,0.60,-0.05,0, 0.05, 0.55
];

//因变量
var y = [
  7.38,8.51,9.52,7.50,9.33,8.28,8.75,7.87,
  7.10,8.00, 7.89,8.15,9.10,8.86,8.90,8.87,
  9.26,9.00,8.75,7.95, 7.65,7.27,8.00,8.50,
  8.75,9.21,8.27,7.67,7.93,9.26
];

x1 = ee.List(x1);
y = ee.List(y);

var chart = ui.Chart.array.values({
                array:y, 
                axis:0, 
                xLabels: x1
              })
              .setSeriesNames(["x1"])
              .setOptions({
                hAxis: {title: "x1" },
                vAxis: {title: "y" },
                pointSize: 1,
                legend: 'none'
              });
print(chart);

var arrList = x1.zip(y);
var lf = arrList.reduce(ee.Reducer.linearFit());
print(lf);
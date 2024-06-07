//代码链接：https://code.earthengine.google.com/540b0be138358829ef1338244015a320

//linearRegression
//自变量
var x1 = [ 
  -0.05, 0.25,0.60,0, 0.25,0.20, 0.15,0.05,
  -0.15, 0.15, 0.20, 0.10,0.40,0.45,0.35,
  0.30, 0.50,0.50, 0.40,-0.05, -0.05,-0.10,
  0.20,0.10,0.50,0.60,-0.05,0, 0.05, 0.55
];

//因变量
var y1 = [
  7.38,8.51,9.52,7.50,9.33,8.28,8.75,7.87,
  7.10,8.00, 7.89,8.15,9.10,8.86,8.90,8.87,
  9.26,9.00,8.75,7.95, 7.65,7.27,8.00,8.50,
  8.75,9.21,8.27,7.67,7.93,9.26
];

var y2 = [
  5.50,6.75,7.25,5.50,7.00,6.50,6.75,5.25,
  5.25,6.00, 6.50,6.25,7.00,6.90,6.80,6.80,
  7.10,7.00,6.80,6.50, 6.25,6.00,6.50,7.00,
  6.80,6.80,6.50,5.75,5.80,6.80
];

x1 = ee.List(x1);
y1 = ee.List(y1);
y2 = ee.List(y2);

var chart1 = ui.Chart.array.values({
                array:y1, 
                axis:0, 
                xLabels: x1
              })
              .setSeriesNames(["x1"])
              .setOptions({
                hAxis: {title: "x1" },
                vAxis: {title: "y1" },
                pointSize: 1,
                legend: 'none'
              });
print("chart1", chart1);

var chart2 = ui.Chart.array.values({
                array:y2, 
                axis:0, 
                xLabels: x1
              })
              .setSeriesNames(["x1"])
              .setOptions({
                hAxis: {title: "x1" },
                vAxis: {title: "y2" },
                pointSize: 1,
                legend: 'none'
              });
print("chart2", chart2);

// y1 = a1 * x1 and y2 = a1 * x1
var indexList = ee.List.sequence(0, x1.length().subtract(1));
var arrList = indexList.iterate(function(index, list) {
  index = ee.Number(index);
  list = ee.List(list);
  var cellList = ee.List([
    x1.get(index), y1.get(index), y2.get(index)  
  ]);
  return list.add(cellList);
}, ee.List([]));
arrList = ee.List(arrList);
var lr = arrList.reduce(ee.Reducer.linearRegression(1, 2));
print(lr);
//代码链接：https://code.earthengine.google.com/017bf6a09ccd8ac68b9ff6a3ad69f52c


//1. loop
var dataDict = ee.Dictionary({
  year: 1999,
  name: "LSW",
  count: 100,
  age: 18,
  desc: "测试用例"
});
print("dataDict : ", dataDict);

//(1) map() 使用map方式
var newDataDict1 = dataDict.map(function(key, value) {
  key = ee.String(key);
  var newValue = ee.Algorithms.If(key.compareTo("count").eq(0), ee.Number(value).add(100), value);
  return newValue;
});
print("newDataDict1 : ", newDataDict1);

//(2) evaluate() 使用异步方式
dataDict.evaluate(function(datas) {
  print("datas is: ", datas);
  var newDataDict2 = {};
  for (var key in datas) {
    var value = datas[key];
    if (key === "count") {
      value += 100;
    }
    newDataDict2[key] = value;
  }
  print("newDataDict2 : ", newDataDict2);
});
//代码链接：https://code.earthengine.google.com/135f2106091f45054dede76506f08a28


//1. loop
var dataList = ee.List.sequence(1, 10);
print("dataList : ", dataList);
//(1) not command，非常不推荐的方式
var total = dataList.size().getInfo();
var newDataList1 = [];
for (var i=0; i<total; i++) {
  newDataList1.push(ee.Number(dataList.get(i)).pow(2));
}
print("newDataList1 : ", ee.List(newDataList1));

//(2) map() 使用map方式
var newDataList2 = dataList.map(function(data) {
  data = ee.Number(data);
  return data.pow(2);
});
print("newDataList2 : ", newDataList2);

//(3) iterate() 使用iterate方式
var newDataList3 = dataList.iterate(function(data, list) {
  data = ee.Number(data);
  list = ee.List(list);
  return list.add(data.pow(2));
}, ee.List([]));
print("newDataList3 : ", newDataList3);

//(4) evaluate() 使用异步方式
dataList.evaluate(function(datas) {
  print("datas is: ", datas);
  var newDataList4 = [];
  for (var i=0; i<datas.length; i++) {
    newDataList4.push(Math.pow(datas[i], 2));
  }
  print("newDataList4 : ", newDataList4);
});
//https://code.earthengine.google.com/10a3a4e15291c01380534a45fcd3efee

//////////////////////// ee.String 字符串 //////////////////////
var ee_str1 = ee.String("this is string.");
//拼接字符串
var ee_str2 = ee.String("second string");
var ee_str3 = ee_str1.cat(" ").cat(ee_str2);
print("concatenates more strings", ee_str3);

var ee_str4 = ee.String("This is landsat8 image.");
//获取子字符串，字符串的起始索引0
print("get substring", ee_str4.slice(1, 6));
//分割字符串
print("split string to list", ee_str4.split(" "));

//////////////////////// ee.Number 数值 //////////////////////
var ee_num1 = ee.Number(100.01);
print("ee number is", ee_num1);

// 绝对值 abs
print("ee abs is", ee.Number(-100).abs());

// 浮点型转换类型 toInt ...
print("float to int", ee_num1.toInt());

//近似值 round ceil floor
var ee_num2 = ee.Number(1.4);
print("ee num2 round", ee_num2.round());
print("ee num2 ceil", ee_num2.ceil());
print("ee num2 floor", ee_num2.floor());

//四则运算 add subtract multiply divide mod 
print("add values", ee_num1.add(ee_num2));
print("divide values", ee_num1.divide(ee_num2));

//////////////////////// ee.Date 日期 ////////////////////////
var ee_date1 = ee.Date("2017-01-01");
print("ee_date1 is", ee_date1);
//http://joda-time.sourceforge.net/apidocs/org/joda/time/format/DateTimeFormat.html
var ee_date2 = ee.Date.parse("yyyyDDD", "2017010");
print("ee date2 is", ee_date2);
print("ee date2 year is", ee_date2.get("year"));

//获取后一天，单位可以是'year', 'month' 'week', 'day', 'hour', 'minute', or 'second'
var ee_date4 = ee.Date("2017-1-10");
var next_date = ee_date4.advance(1, "day");
print("next date is", next_date);
var pre_date = ee_date4.advance(-1, "day");
print("pre date is", pre_date);

//日期间隔，单位可以是'year', 'month' 'week', 'day', 'hour', 'minute', or 'second'
var ee_date5 = ee.Date("2017-1-1");
var ee_date6 = ee.Date("2017-1-10");
print("days number", ee_date6.difference(ee_date5, "day"));

//获取指定格式的日期返回值，比如当前是一年中的第几天
var doy1 = ee_date6.format("DDD");
print("day of year1", doy1);

//////////////////////// ee.Dictionary 字典 ////////////////////////
var ee_dict1 = ee.Dictionary({
  name: "AA",
  age: 10,
  desc: "this is a boy"
});
print("keys is", ee_dict1.keys());
print("values is", ee_dict1.values());
print("age is ", ee_dict1.get("age"));
print("name is ", ee_dict1.get("name"));


//////////////////////// ee.List 列表 ////////////////////////
var ee_list1 = ee.List([1,2,3,4,5]);
print("ee list create first method", ee_list1);

//列表初始化除了可以直接使用Js数组，还可以使用内部方法
var ee_list2 = ee.List.sequence(1, 5);
print("ee list create second method", ee_list2);
print("ee_list2[1] = ", ee_list2.get(1));
print("length ", ee_list2.length());
print("size ", ee_list2.size());

//添加元素
var ee_list3 = ee.List([1,2,3]);
ee_list3 = ee_list3.add(4);
print("ee_list3 is", ee_list3);
print("insert index", ee_list3.insert(0, 9));

//提取部分List
print("slice list", ee_list1.slice(1, 3));

//to string
var ee_list4 = ee.List(["a", "b", "c"]);
print("join string", ee_list4.join("-"));

////////////////////////// ee.Array 数组 ////////////////////////
var ee_arr1 = ee.Array([[1,2], [2,2]]);
print("ee_arr1 is", ee_arr1);
var ee_arr2 = ee.Array(ee.List([[1,1], [3,3]]));

//加、减、除、乘计算
print("add result ", ee_arr1.add(ee_arr2));
print("subtract result", ee_arr1.subtract(ee_arr2));
print("divide result", ee_arr1.divide(ee_arr2));
print("multiply result", ee_arr1.multiply(ee_arr2));

//axis 0 1
print("axis 0", ee_arr2.reduce(ee.Reducer.sum(), [0]));
print("axis 1", ee_arr2.reduce(ee.Reducer.sum(), [1]));


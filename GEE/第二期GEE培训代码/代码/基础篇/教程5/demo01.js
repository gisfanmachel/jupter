//https://code.earthengine.google.com/99dd5001aafcc56a1be2d231487b4979
print("-----------数据类型-----------");
var num_a = 1; //整数
var num_b = 2.1; //保留小数
var num_c = 1e2; //科学计数法
print(num_a);


var str_1 = "hello world!"; //双引号
var str_2 = 'hello world!'; //单引号，两者不能混用
print(str_1);
print(str_2);

var bool_1 = true; //布尔值表示的就是真假
var bool_2 = false;

var dict = { "name": "bili", "age": 12, "desc": "he is good!" };
print(dict.name); //获取制定key的对象
print(dict['name']);

var arr_num = [1,2,3]; //数字数组
var arr_str = ["a", "b", "c" ]; //字符串数组
var arr_mul = [1,2, "a"]; //混合数组
print(arr_num[0]); //数组的索引是从0开始，最后一位是 (arr.length() - 1)

var x = null;
print(x);

var y;
print(y);

print("-----------数学运算-----------");
//数学运算
var a1 = 10;
var a2 = 20;
//数字运算的加、减、乘、除、求余
print(a1 + a2); 
print(a1 - a2);
print(a1 * a2);
print(a1 / a2);
print(a2 % a1);
//累加，就是对自己本身加1
var a3 = ++a1;
print("a3: " + a3 + " a1: " + a1);
//递减，就是对自己本身减1
var a4 = --a2;
print("a4: " + a4 + " a2: " + a2);
// +=, -=, *=, /=, %=
var a5 = 10;
a5 += 1;
print("a5: " + a5);

//字符串连接
var b1 = "hello";
var b2 = "GEE";
print(b1 + " " + b2);

//字符串和数字连接
print(b1 + " " + a5);

print("-----------控制循环语句-----------");
//if...else...
var seen = true;
if (seen) {
  print("find it");
} else {
  print("not find it");
}

//for循环
var sum = 0;
for (var i=0; i<=10; i++) {
  sum += i;
}
print("sum is: " + sum);


print("-----------方法（函数）-----------");
//方法一：直接定义
function mySum1(a, b) {
  return a + b;
}
//方法二：使用定义变量方式定义
var mySum2 = function(a, b) {
  return a + b;
};
//方法三：在对象内部定义函数，主要是为了封装某些方法，
//        只有特定的对象才能使用
var funcObj = {
  mySum3: function(a, b) {
    return a + b;
  }
};

print(mySum1(1, 2));
print(mySum2(1, 2));
print(funcObj.mySum3(1, 2));

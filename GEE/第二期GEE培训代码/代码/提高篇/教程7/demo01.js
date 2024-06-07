//ee.Algorithms.If(condition, trueCase, falseCase)
var a = ee.List.sequence(1, 10);
var count = a.size();
print("count", count);
var message1 = "";
if (count.eq(4)) {
  message1 = "count is 4";
} else {
  message1 = "count is not 4";
}
print(message1);
var message2 = ee.Algorithms.If(count.eq(4), "count is 4", "count is not 4");
print(message2);

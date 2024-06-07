//代码链接：https://code.earthengine.google.com/3615a4cf766f184c1ebf27d08854c7f4

//Large Scale International Boundary Lines (LSIB)
var fCol = ee.FeatureCollection("USDOS/LSIB/2013");

var sCol = fCol.limit(100);
print("select sCol", sCol);
var result = sCol.reduceColumns(ee.Reducer.toList(), ["system:index"])
                 .get("list");
print(result);
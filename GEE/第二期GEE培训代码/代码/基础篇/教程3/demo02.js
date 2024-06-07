//链接：https://code.earthengine.google.com/5856c34ed8e5f8763117ac20b2663487

var table = ee.FeatureCollection("users/wangweihappy0/shpDemo");
Map.centerObject(table, 7);
Map.addLayer(table, {color: "red"}, "table");

print("area is", table.geometry().area());
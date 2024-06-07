var mod09ga = ee.ImageCollection("MODIS/006/MOD09GA");
var sCol = mod09ga.filterDate("2018-1-1", "2019-1-1")
                  .map(function(image) {
                    var time_start = ee.Date(image.get("system:time_start"));
                    var month = time_start.get("month");
                    image = image.set("month", ee.Number(month).toInt());
                    return image;
                  });
print("raw image collection", sCol);
sCol = sCol.filter(ee.Filter.inList("month", [1,3, 5]));
print("select 1、3、5 data", sCol);

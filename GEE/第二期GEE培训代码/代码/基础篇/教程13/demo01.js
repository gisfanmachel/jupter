//代码链接：https://code.earthengine.google.com/6777c3e9e438be2ce7580df110ab410f


var sCol = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA')
             .filterDate('2015-01-01', '2015-04-01')
             .filter(ee.Filter.and(
              ee.Filter.eq("WRS_PATH", 44),
              ee.Filter.eq('WRS_ROW', 34)
             ));
print("select image collection: ", sCol);
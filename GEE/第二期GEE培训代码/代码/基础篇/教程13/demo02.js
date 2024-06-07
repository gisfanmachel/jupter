//代码链接：https://code.earthengine.google.com/53391ca528d53229331ea11e8dd4c3fa


var sCol = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA')
             .filterDate('2015-01-01', '2015-02-01')
             .filter(ee.Filter.or(
              ee.Filter.eq("WRS_PATH", 44),
              ee.Filter.eq('WRS_ROW', 34)
             ));
print("select image collection: ", sCol);
var gldas = ee.ImageCollection("NASA/GLDAS/V021/NOAH/G025/T3H");
var fCol = ee.FeatureCollection("USDOS/LSIB/2013");
var sCol = fCol.filter(ee.Filter.eq("name", "Taiwan"));
print("select sCol", sCol);
Map.centerObject(sCol, 9);
Map.addLayer(sCol, {color: "red"}, "roi");
var tem = gldas.filterDate("2018-3-1", "2018-4-1")
              .select("Tair_f_inst")
              .first()
              .subtract(273.15);
print("tem", tem);
var visParams = {
  min: -40,
  max: 50,
  palette: [
    '040274', '040281', '0502a3', '0502b8', '0502ce', '0502e6',
    '0602ff', '235cb1', '307ef3', '269db1', '30c8e2', '32d3ef',
    '3be285', '3ff38f', '86e26f', '3ae237', 'b5e22e', 'd6e21f',
    'fff705', 'ffd611', 'ffb613', 'ff8b13', 'ff6e08', 'ff500d',
    'ff0000', 'de0101', 'c21301', 'a71001', '911003'
  ],
};
Map.addLayer(tem, visParams, "lai");
Export.image.toDrive({
  image: tem.clip(sCol),
  description: "tem",
  folder: "training02",
  fileNamePrefix: "tem",
  region: sCol.geometry().bounds(), //设置范围
  crs: "EPSG:4326", //设置投影方式
  crsTransform: [0.25,0,-180,0,-0.25,90],
  maxPixels: 1e13 //设置最大像素值
});

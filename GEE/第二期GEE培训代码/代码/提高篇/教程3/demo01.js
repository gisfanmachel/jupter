//https://code.earthengine.google.com/b8b166a5d48181cbf721ca12ab45d137

var vb_rgba = ee.Image("users/wangweihappy0/training02/vb_rgba"),
    vb_rgbn = ee.Image("users/wangweihappy0/training02/vb_rgbn");
//输出无人机影像的分辨率
print("vb_rgba scale", vb_rgba.projection().nominalScale());
print("vb_rgbn scale", vb_rgbn.projection().nominalScale());
vb_rgba = vb_rgba.select(["red", "green", "blue"], ["r", "g", "b"]);
Map.centerObject(vb_rgba, 19);
Map.addLayer(vb_rgba, {}, "vb_rgba");
Map.addLayer(vb_rgbn, {}, "vb_rgbn");
var ndvi = vb_rgbn.normalizedDifference(["nir", "red"]).rename("ndvi");
var visParam = {
  min:0,
  max:0.8,
  palette: 'FFFFFF, CE7E45, DF923D, F1B555, FCD163, 99B718, 74A901, 66A000, 529400,' +
    '3E8601, 207401, 056201, 004C00, 023B01, 012E01, 011D01, 011301'
};
Map.addLayer(ndvi, visParam, "ndvi");

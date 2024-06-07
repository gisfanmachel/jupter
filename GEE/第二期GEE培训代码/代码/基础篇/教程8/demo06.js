//代码链接：https://code.earthengine.google.com/2317ae07c52b1f603ddbd8f22f8f36d3

var counties = ee.FeatureCollection("ft:1S4EB6319wWW2sWQDPhDvmSBIVrD3iEmCLYB7nMM");
var properties = ['Census 2000 Population'];
var image = counties
  .filter(ee.Filter.neq('Census 2000 Population', null))
  .reduceToImage({
    properties: properties,
    reducer: ee.Reducer.mean()
  });
print("generate image", image);
Map.setCenter(-99.976, 40.38, 5);
Map.addLayer(image, {min:1000, max:100000, palette: ["green", "blue", "red"]});
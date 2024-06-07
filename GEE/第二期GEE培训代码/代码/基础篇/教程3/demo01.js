//链接：https://code.earthengine.google.com/1a91f3dd8cd92d86901411b976940042

var image = ee.Image("users/wangweihappy0/imgDemo");
Map.centerObject(image, 8);
Map.addLayer(image, {min:300, max:330}, "image");

var chart = ui.Chart.image.histogram({
  image: image, 
  region: image.geometry().bounds(),
  scale: 500
});
print("histogram: ", chart);
//代码链接：https://code.earthengine.google.com/4be21ab79682abdff5ba277b3e1dd10c


var image = ee.Image("LANDSAT/LC08/C01/T1_TOA/LC08_123037_20180611");
print("image", image);

print("image bandNames", image.bandNames());
print("image bandTypes", image.bandTypes());
print("image date", image.date());
print("image id", image.id());
print("cloud cover", image.get("CLOUD_COVER"));
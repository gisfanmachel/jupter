//代码链接：https://code.earthengine.google.com/6e675b0075662d84878de0777a63d181

/**
 * NDVI = (nir - red) / (nir + red)
 * */
function l8NDVI(image) {
  return image.addBands(image.normalizedDifference(["B5", "B4"]).rename("NDVI"));
}

exports.l8NDVI = l8NDVI;
//代码链接：https://code.earthengine.google.com/b9d3974134621d4cfab8c26f855e4823


//NDWI: (G - NIR)/(G + NIR)
function NDWI(image) {
  return image.addBands(
    image.normalizedDifference(["B3", "B5"])
         .rename("NDWI")
  );
}

//MNDWI: (G - SWIR)/(G + SWIR)
function MNDWI(image) {
  return image.addBands(
    image.normalizedDifference(["B3", "B6"])
         .rename("MNDWI")
  );
}
  
  
//AWEI_nsh: 4 * (G - SWIR1) - (0.25 * NIR + 2.75 * SWIR2)
function AWEI_nsh(image) {
  var awei_nsh = image.expression(
    "4 * (G - SWIR1) - (0.25 * NIR + 2.75 * SWIR2)",
    {
      "G": image.select("B3"),
      "NIR": image.select("B5"),
      "SWIR1": image.select("B6"),
      "SWIR2": image.select("B7")
    }
  );
  return image.addBands(awei_nsh.rename("AWEI_nsh"));
}

//AWEI_sh: B + 2.5 * G - 1.5 * (NIR + SWIR1) - 0.25 * SWIR2
function AWEI_sh(image) {
  var awei_sh = image.expression(
    "B + 2.5 * G - 1.5 * (NIR + SWIR1) - 0.25 * SWIR2",
    {
      "B": image.select("B2"),
      "G": image.select("B3"),
      "NIR": image.select("B5"),
      "SWIR1": image.select("B6"),
      "SWIR2": image.select("B7")
    }
  );
  return image.addBands(awei_sh.rename("AWEI_sh"));
}
  
  
//WI_2015: 1.7204 + 171*G + 3*R - 70*NIR - 45*SWIR1 - 71*SWIR2
function WI_2015(image) {
  var wi_2015 = image.expression(
    "1.7204 + 171*G + 3*R - 70*NIR - 45*SWIR1 - 71*SWIR2",
    {
      "G": image.select("B3"),
      "R": image.select("B4"),
      "NIR": image.select("B5"),
      "SWIR1": image.select("B6"),
      "SWIR2": image.select("B7")
    }
  );
  return image.addBands(wi_2015.rename("WI_2015"));
}

var roi = /* color: #d63000 */ee.Geometry.Polygon(
        [[[117.19846835579438, 31.338582945998613],
          [117.96476474251313, 31.352657172321162],
          [117.93455234016938, 31.822923403887454],
          [117.20396151985688, 31.792580050380295]]]);
Map.centerObject(roi, 9);
Map.addLayer(roi, {color: "red"}, "roi");
var l8Col = ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA")
              .filterBounds(roi)
              .filterDate("2017-1-1", "2019-1-1")
              //影像去云
              .map(ee.Algorithms.Landsat.simpleCloudScore)
              .map(function(image) {
                return image.updateMask(image.select("cloud").lte(10));
              })
              //水体指数
              .map(NDWI)
              .map(MNDWI)
              .map(AWEI_nsh)
              .map(AWEI_sh)
              .map(WI_2015);

//融合裁剪
var l8Image = l8Col.median().clip(roi);
Map.addLayer(l8Image, {min:0, max:0.3, bands:["B4", "B3", "B2"]}, "l8Image", false);

//直方图
print(ui.Chart.image.histogram({
  image: l8Image.select("NDWI"),
  region: roi,
  scale:500
}));

//OTSU
var otsu = function(histogram) {
  var counts = ee.Array(ee.Dictionary(histogram).get('histogram'));
  var means = ee.Array(ee.Dictionary(histogram).get('bucketMeans'));
  var size = means.length().get([0]);
  var total = counts.reduce(ee.Reducer.sum(), [0]).get([0]);
  var sum = means.multiply(counts).reduce(ee.Reducer.sum(), [0]).get([0]);
  var mean = sum.divide(total);
  
  var indices = ee.List.sequence(1, size);
  
  // Compute between sum of squares, where each mean partitions the data.
  var bss = indices.map(function(i) {
    var aCounts = counts.slice(0, 0, i);
    var aCount = aCounts.reduce(ee.Reducer.sum(), [0]).get([0]);
    var aMeans = means.slice(0, 0, i);
    var aMean = aMeans.multiply(aCounts)
        .reduce(ee.Reducer.sum(), [0]).get([0])
        .divide(aCount);
    var bCount = total.subtract(aCount);
    var bMean = sum.subtract(aCount.multiply(aMean)).divide(bCount);
    return aCount.multiply(aMean.subtract(mean).pow(2)).add(
           bCount.multiply(bMean.subtract(mean).pow(2)));
  });
  // print(ui.Chart.array.values(ee.Array(bss), 0, means));
  // Return the mean value corresponding to the maximum BSS.
  return means.sort(bss).get([-1]);
};

var histogram = l8Image.select("NDWI")
                      .reduceRegion({
                        reducer: ee.Reducer.histogram(), 
                        geometry: roi, 
                        scale: 30,
                        maxPixels: 1e13
                      });
var threshold = otsu(histogram.get("NDWI"));
print("threshold", threshold);
//OTSU阈值，展示结果
var result = l8Image.select("NDWI")
                    .updateMask(l8Image.select("NDWI").gte(threshold));
Map.addLayer(result, {palette: "ff0000"}, "NDWI", false);


//accuracy
var all_sample = water.merge(nowater);
var real_img1 = ee.Image.constant(1).clip(water);
real_img1 = real_img1.unmask(0);
var real_img2 = ee.Image.constant(4).clip(nowater);
real_img2 = real_img2.unmask(0);
real_img2 = real_img2.where(real_img1.eq(1), 0);
var real_img = real_img1.add(real_img2);
real_img = real_img.clip(all_sample);
var pre_img = result.unmask(4).clip(all_sample);
real_img = real_img.where(pre_img.eq(1).and(real_img.eq(4)), 2);
real_img = real_img.where(pre_img.eq(4).and(real_img.eq(1)), 3);
var newImg = ee.Image.constant(1).rename("count");
newImg = newImg.addBands(real_img.rename("lake"));
var acc_dict = newImg.reduceRegion({
  reducer: ee.Reducer.count().group({
    groupField: 1, 
    groupName: 'index',
  }), 
  geometry: all_sample, 
  scale: 30,
  maxPixels: 1e13
});
var temp_groups = ee.List(ee.Dictionary(acc_dict).get("groups"));
var temp_counts = ee.List.repeat(0, 4);
var counts = temp_groups.iterate(function (data, list){
  data = ee.Dictionary(data);
  list = ee.List(list);
  var index = ee.Number(data.get("index"));
  var count = ee.Number(data.get("count"));
  list = list.set(index.subtract(1), count);
  return list;
}, temp_counts);
counts = ee.List(counts);
var arr = ee.Array([
  [
    ee.Number(counts.get(0)).toInt(), 
    ee.Number(counts.get(1)).toInt()
  ], 
  [
    ee.Number(counts.get(2)).toInt(),
    ee.Number(counts.get(3)).toInt()
  ]
]);
var conf = ee.ConfusionMatrix(arr);
print("array is: ", conf.array());
print("accuracy is: ", conf.accuracy());
print("kappa is: ", conf.kappa());
print("consumersAccuracy is: ", conf.consumersAccuracy());
print("producersAccuracy is: ", conf.producersAccuracy());
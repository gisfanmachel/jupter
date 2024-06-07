//代码链接：https://code.earthengine.google.com/38d9128d66e558d85c0bead7bc9f8440


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

//直方图展示结果
print(ui.Chart.image.histogram({
  image: l8Image.select("NDWI"),
  region: roi,
  scale:500
}));
print(ui.Chart.image.histogram({
  image: l8Image.select("MNDWI"),
  region: roi,
  scale:500
}));
print(ui.Chart.image.histogram({
  image: l8Image.select("AWEI_nsh"),
  region: roi,
  scale:500
}));
print(ui.Chart.image.histogram({
  image: l8Image.select("AWEI_sh"),
  region: roi,
  scale:500
}));
print(ui.Chart.image.histogram({
  image: l8Image.select("WI_2015"),
  region: roi,
  scale:500
}));

//人工确认阈值，展示结果
Map.addLayer(
  l8Image.select("NDWI")
         .updateMask(l8Image.select("NDWI").gte(0.2)), 
  {palette: "ff0000"}, 
  "NDWI",
  false
);
Map.addLayer(
  l8Image.select("MNDWI")
         .updateMask(l8Image.select("MNDWI").gte(0.6)), 
  {palette: "ff0000"}, 
  "MNDWI",
  false
);
Map.addLayer(
  l8Image.select("AWEI_nsh")
         .updateMask(l8Image.select("AWEI_nsh").gte(0.2)), 
  {palette: "ff0000"}, 
  "AWEI_nsh",
  false
);
Map.addLayer(
  l8Image.select("AWEI_sh")
         .updateMask(l8Image.select("AWEI_sh").gte(0.3)), 
  {palette: "ff0000"}, 
  "AWEI_sh",
  false
);
Map.addLayer(
  l8Image.select("WI_2015")
         .updateMask(l8Image.select("WI_2015").gte(14)), 
  {palette: "ff0000"}, 
  "WI_2015",
  false
);
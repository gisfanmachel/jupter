//代码链接：https://code.earthengine.google.com/ff3da5203bcc2f6b8a0cf2d238a21997


//非监督分类
var roi = /* color: #d63000 */ee.Geometry.Polygon(
        [[[114.02191591378232, 33.78358088957628],
          [114.03290224190732, 32.814844755032674],
          [115.04913759346982, 32.85638443066918],
          [115.01617860909482, 33.8018413803568]]]);
Map.centerObject(roi, 7);
Map.setOptions("SATELLITE");
Map.addLayer(roi, {color: "00ff00"}, "roi", false);

//Landsat8 SR数据去云
function rmCloud(image) {
  var cloudShadowBitMask = (1 << 3);
  var cloudsBitMask = (1 << 5);
  var qa = image.select("pixel_qa");
  var mask = qa.bitwiseAnd(cloudShadowBitMask).eq(0)
                 .and(qa.bitwiseAnd(cloudsBitMask).eq(0));
  return image.updateMask(mask);
}

//缩放
function scaleImage(image) {
  var time_start = image.get("system:time_start");
  image = image.multiply(0.0001);
  image = image.set("system:time_start", time_start);
  return image;
}

//添加NDVI
function NDVI(image) {
  return image.addBands(image.normalizedDifference(["B5", "B4"]).rename("NDVI"));
}

var l8Col = ee.ImageCollection("LANDSAT/LC08/C01/T1_SR")
              .filterBounds(roi)
              .filterDate("2018-5-1", "2018-10-1")
              .filter(ee.Filter.lte("CLOUD_COVER", 50))
              .map(rmCloud)
              .map(scaleImage)
              .map(NDVI);
print("l8Col", l8Col);

var l8Image = l8Col.select(["B1", "B2", "B3", "B4", "B5", "B6", "B7", "NDVI"])
                   .median()
                   .clip(roi);
var visParam = {
  min: 0,
  max: 0.3,
  bands: ["B4", "B3", "B2"]
};
Map.addLayer(l8Image, visParam, "l8Image");

var sampleRoi = /* color: #98ff00 */ee.Geometry.Polygon(
        [[[114.62959747314449, 33.357067677774594],
          [114.63097076416011, 33.32896028884253],
          [114.68315582275386, 33.33125510961763],
          [114.68178253173824, 33.359361757948754]]]);
Map.addLayer(sampleRoi, {color: "red"}, "sampleRoi", false);

//生成训练使用的样本数据
var training = l8Image.sample({
  region: roi,
  scale: 30,
  numPixels:5000
});

print("training", training.limit(1));

//初始化非监督分类器
var count = 10;
var clusterer = ee.Clusterer.wekaKMeans(count)
                  .train(training);
                  
//调用影像或者矢量集合中的cluster方法进行非监督分类
var result = l8Image.cluster(clusterer);
print("result", result);

//添加图例方式封装成为了一个方法
//palette: 颜色列表
//names: 图例说明列表
function addLegend(palette, names) {
  //图例的底层Panel
  var legend = ui.Panel({
    style: {
      position: 'bottom-right',
      padding: '5px 10px'
    }
  });
  //图例标题
  var title = ui.Label({
    value: '类别',
    style: {
      fontWeight: 'bold',
      color: "red",
      fontSize: '16px'
    }
  });
  legend.add(title);
  
  //添加每一列图例颜色以及说明
  var addLegendLabel = function(color, name) {
        var showColor = ui.Label({
          style: {
            backgroundColor: '#' + color,
            padding: '8px',
            margin: '0 0 4px 0'
          }
        });

        var desc = ui.Label({
          value: name,
          style: {margin: '0 0 4px 8px'}
        });
        //颜色和说明是水平放置
        return ui.Panel({
          widgets: [showColor, desc],
          layout: ui.Panel.Layout.Flow('horizontal')
        });
  };
  
  //添加所有的图例列表
  for (var i = 0; i < palette.length; i++) {
    var label = addLegendLabel(palette[i], names[i]); 
    legend.add(label);
  }  
  
  ui.root.insert(0, legend);
}

//颜色列表和说明列表
var palette = ["ff0000","00ff00","0000ff",
              "ff00ff","ffff00","00ffff",
              "ffffff","000000","FF8C00",
              "ADFF2F"];
var names = ["分类A","分类B","分类C","分类D",
             "分类E","分类F","分类G","分类H",
             "分类I","分类J"];
//添加图例
addLegend(palette, names);
var visParam = {
  min: 0,
  max: count-1,
  palette: palette
};
Map.addLayer(result, visParam, "result");
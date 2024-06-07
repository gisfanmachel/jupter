//代码链接：https://code.earthengine.google.com/9cb0b5f389e8113292eb26329d3ccf78
var roi = /* color: #009999 */ee.Geometry.Polygon(
        [[[116.01215820312495, 35.01173039395982],
          [116.00117187499995, 34.89917580755738],
          [116.15498046874995, 34.912690517484585],
          [116.17145996093745, 35.025226554463565]]]),
    l8 = ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA");

/**
 * 定义相关常量和变量
 * @type {Object}
 */
var app = {
  data: {
    startDate: "2017-1-1",
    endDate: "2018-1-1",
    cloudScore: 50,
    l8Col: null,
    mapClickFlag: false,
    showNDVILayer: true,
    rawLayer: null,
    ndviLayer: null,
    selectImageKey: null,
    clickPoint: null
  },
  config: {
    ndviVisParam: {
      min: -0.2, 
      max: 0.8,
      palette: 'FFFFFF, CE7E45, DF923D, F1B555, FCD163, 99B718, 74A901, 66A000, 529400,' +
        '3E8601, 207401, 056201, 004C00, 023B01, 012E01, 011D01, 011301'
    },
    rgbVisParam: {
      min: 0, 
      max: 0.3,
      bands: ["B4", "B3", "B2"]
    }
  },
  ui: {}
};

/**
 * 定义Landsat 8公共方法
 * @type {Object}
 */
var Landsat8 = {
  //NDWI: (B03 - B05)/(B03 + B05)
  NDWI: function(image) {
      return image.addBands(image.normalizedDifference(["B3", "B5"])
          .rename("NDWI"));
  },
  
  //NDVI: (B05 - B04)/(B05 + B04)
  NDVI: function(img) {
    var ndvi = img.normalizedDifference(["B5","B4"]);
    return img.addBands(ndvi.rename("NDVI"));
  },
  
  //EVI: 2.5*(B05 - B04) / (B05 + 6*B04 - 7.5*B02 + 1)
  EVI: function(img) {
    var nir = img.select("B5");
    var red = img.select("B4");
    var blue = img.select("B2");
    var evi = img.expression(
      "2.5 * (B5 - B4) / (B5 + 6*B4 - 7.5*B2 + 1)",
      {
        "B5": nir,
        "B4": red,
        "B2": blue
      }
    );
    return img.addBands(evi.rename("EVI"));
  },
  
  //LSWI: (B05 - B6)/(B06 + B6)
  LSWI: function(img) {
    var lswi = img.normalizedDifference(["B5","B6"]);
    return img.addBands(lswi.rename("LSWI"));
  },
  
  /**
   * 通过日期、区域、云量筛选数据
   * @param  {[type]} startDate [description]
   * @param  {[type]} endDate   [description]
   * @param  {[type]} region    [description]
   * @param  {[type]} cloud     [description]
   * @return {[type]}           [description]
   */
  getL8ImageCollection : function(startDate, endDate, region, cloud) {
    var dataset = l8.filterDate(startDate, endDate)
                    .filterBounds(region)
                    .map(ee.Algorithms.Landsat.simpleCloudScore)
                    .map(function(image) {
                      return image.updateMask(image.select("cloud").lte(cloud));
                    })
                    .map(Landsat8.NDVI)
                    .map(Landsat8.NDWI)
                    .map(Landsat8.EVI)
                    .map(Landsat8.LSWI);
    return dataset;
  }
};

/**
 * 显示边界
 * @param  {[type]} region [description]
 * @return {[type]}        [description]
 */
function showBounds(region) {
  var outline = ee.Image()
                  .toByte()
                  .paint({
                    featureCollection:region,
                    color:0,
                    width:1.5
                  });
  Map.addLayer(outline, {palette: "ff0000"}, "bounds");
}

/**
 * 导出影像数据
 * @param  {[type]} image    [description]
 * @param  {[type]} region   [description]
 * @param  {[type]} desc     [description]
 * @param  {[type]} fileName [description]
 * @return {[type]}          [description]
 */
function exportImageToDrive(image, region, desc, fileName) {
    Export.image.toDrive({
        image: image,
        description: desc,
        folder: "training01", 
        fileNamePrefix: fileName,
        crs: "EPSG:4326",
        region: region,
        scale: 30,
        maxPixels: 1e13
    });
}

/**
 * 地图点击事件
 * @param  {[type]} coords)        {                                print("click map point         is: " + coords.lon + " " + coords.lat);    if (app.data.mapClickFlag) {      var point [description]
 * @param  {[type]} region:point   [description]
 * @param  {[type]} regionReducer: ee.Reducer.mean() [description]
 * @param  {[type]} scale:30                                                      }  [description]
 * @return {[type]}                [description]
 */
Map.onClick(function(coords) {
    print("click map point is: " + coords.lon + " " + coords.lat);
    if (app.data.mapClickFlag) {
      var point = ee.Geometry.Point(coords.lon, coords.lat);
      if (app.data.clickPoint !== null) {
        Map.remove(app.data.clickPoint);
      }
      app.data.clickPoint = null;
      app.data.clickPoint = Map.addLayer(point, {color: "red"}, "clickPoint");
      //normal
      var chart = ui.Chart.image.doySeries({
          imageCollection: app.data.l8Col.select(["NDVI", "EVI", "NDWI", "LSWI"]), 
          region:point, 
          regionReducer: ee.Reducer.mean(), 
          scale:30
      }).setOptions({
        title: "Index Line",
        hAxis: {title: "Day Of Year"},
        vAxis: {title: "Index Value"},
        series: {
          0: { lineWidth: 1, pointSize: 2 },
          1: { lineWidth: 1, pointSize: 2 },
          2: { lineWidth: 1, pointSize: 2 },
          3: { lineWidth: 1, pointSize: 2 }
        }
      });
      print(chart);
    }
  }
);

/**
 * 查找卫星影像
 * @return {[type]} [description]
 */
function searchLandsatImages () {
  app.data.l8Col = Landsat8.getL8ImageCollection(app.data.startDate, app.data.endDate, roi, app.data.cloudScore);
  var l8Ids = app.data.l8Col.reduceColumns(ee.Reducer.toList(), ["system:index"])
                            .get("list");
  l8Ids.evaluate(function(ids) {
    print("select images length is: " + ids.length);
    app.ui.rawImagePanel.select.items().reset(ids);
    app.ui.rawImagePanel.select.setValue(app.ui.rawImagePanel.select.items().get(0));
  });
}

/**
 * 切换卫星影像
 * @param  {[type]} key [description]
 * @return {[type]}     [description]
 */
function showLandsatImage(key) {
  if (app.data.rawLayer !== null) {
    Map.remove(app.data.rawLayer);
  }
  app.data.rawLayer = null;
  
  if (app.data.ndviLayer !== null) {
    Map.remove(app.data.ndviLayer);
  }
  app.data.ndviLayer = null;
  
  print("show landsat8 image id is: " + key);
  app.data.selectImageKey = key;
  var image = ee.Image(app.data.l8Col.filter(ee.Filter.eq("system:index", key)).first());
  app.data.rawLayer = Map.addLayer(image, app.config.rgbVisParam, "RGB-"+key);
  
  if (app.data.showNDVILayer) {
    app.data.ndviLayer = Map.addLayer(image.select("NDVI"), app.config.ndviVisParam, "NDVI-"+key);
  }
}

/**
 * 导出NDVI结果
 * @return {[type]} [description]
 */
function exportNDVIResult() {
  var key = app.data.selectImageKey;
  var image = ee.Image(app.data.l8Col.filter(ee.Filter.eq("system:index", key)).first());
  var ndvi = image.select("NDVI");
  exportImageToDrive(image, roi, key, key);
}

/**
 * 展示NDVI缩略图
 * @return {[type]} [description]
 */
function showNDVIThumbnail() {
  var key = app.data.selectImageKey;
  var image = ee.Image(app.data.l8Col.filter(ee.Filter.eq("system:index", key)).first());
  var thumbnail = ui.Thumbnail({
    image: image.select("NDVI").visualize(app.config.ndviVisParam),
    params: {
      dimensions: "256x256",  //缩略图大小
      region: roi.toGeoJSON(), //地理信息
      format: "png"  //缩略图图片格式
    },
    //显示内容宽和高
    style: {height: "300px", width: "300px"},
    //点击缩略图触发事件
    onClick: function() {
      print("click thumbnail");
    }
  });
  print(thumbnail);
}

/***
 * 初始化UI界面
 * */
function initUI() {
  
  app.ui = {};
  /////////////////////////////////////
  app.ui.titlePanel = {
    panel: ui.Panel({
      widgets: [
        ui.Label({
          value: "UI Demo",
          style: {
            color: "0000ff",
            fontSize: "30px"
          }
        })
      ]
    })
  };
  
  /////////////////////////////////////
  var rawImageTitle = ui.Label({
    value:"筛选原始Landsat8影像",
    style: {
      fontWeight: "bold",
      fontSize: "16px"
    }
  });
  var startLabel = ui.Label("起始时间: yyyy-mm-dd");
  var startTextbox = ui.Textbox({
    placeholder: "起始时间: yyyy-mm-dd",
    value: app.data.startDate,
    onChange: function(value) {
      print("录入的起始时间: " + value);
      app.data.startDate = value;
    }
  });
  
  var endLabel = ui.Label("结束时间: yyyy-mm-dd");
  var endTextbox = ui.Textbox({
    placeholder: "结束时间: yyyy-mm-dd",
    value: app.data.endDate,
    onChange: function(value) {
      print("录入的结束时间: " + value);
      app.data.endDate = value;
    }
  });
  
  var cloudLabel = ui.Label("筛选云量");
  var cloudSlider = ui.Slider({
    min:1,
    max:100,
    value:app.data.cloudScore,
    step:1,
    direction: "horizontal",
    onChange: function(value) {
      print("slider1 change value is:"+ value);
      app.data.cloudScore = parseInt(value, 10);
    }
  });
  
  var searchBtn = ui.Button({
    label: "查找Landsat8原始影像",
    onClick: searchLandsatImages
  });
  
  var showImages = ui.Select({
    items: [],
    placeholder: "显示Landsat8原始影像",
    onChange: showLandsatImage
  });
  
  app.ui.rawImagePanel = {
    panel: ui.Panel({
      widgets: [
        rawImageTitle, 
        startLabel, startTextbox, 
        endLabel, endTextbox, 
        cloudLabel, cloudSlider,
        searchBtn,
        showImages
      ],
      style: {
        border : "1px solid black"
      }
    }),
    select: showImages
  };
  
  /////////////////////////////////////
  var processTitle = ui.Label({
    value:"处理Landsat8影像",
    style: {
      fontWeight: "bold",
      fontSize: "16px"
    }
  });
  var mapClickCB = ui.Checkbox("开启地图点击事件", app.data.mapClickFlag);
  mapClickCB.onChange(function(checked){
    print("地图点击事件：" + checked);
    app.data.mapClickFlag = checked;
  });
  
  var showNDVICB = ui.Checkbox("加载NDVI图层", app.data.showNDVILayer);
  showNDVICB.onChange(function(checked){
    print("加载NDVI图层：" + checked);
    app.data.showNDVILayer = checked;
  });
  
  var showThumbnailBtn = ui.Button({
    label: "展示NDVI图层缩略图",
    onClick: showNDVIThumbnail
  });
  
  var exportNDVIBtn = ui.Button({
    label: "导出NDVI图层",
    onClick: exportNDVIResult
  });
  
  
  app.ui.processPanel = {
    panel: ui.Panel({
      widgets: [
        processTitle, 
        mapClickCB,
        showNDVICB,
        showThumbnailBtn,
        exportNDVIBtn
      ],
      style: {
        border : "1px solid black"
      }
    })
  };
  
  
  var main = ui.Panel({
      widgets: [
        app.ui.titlePanel.panel,
        app.ui.rawImagePanel.panel,
        app.ui.processPanel.panel
      ],
      style: {width: "300px", padding: '8px'}
    });
  ui.root.insert(0, main);
}

/***
 * 
 * main
 * */
function main() {
  Map.style().set('cursor', 'crosshair');
  Map.centerObject(roi, 10);
  Map.setOptions("SATELLITE");
  
  initUI();
  showBounds(roi);
}

main();
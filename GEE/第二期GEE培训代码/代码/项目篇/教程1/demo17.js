//代码链接：https://code.earthengine.google.com/363e3a6befc0a2c720d3fd9e01e93095


//监督分类 
var roi = /* color: #d63000 */ee.Geometry.Polygon(
        [[[103.90797119140626, 19.300461796064834],
          [104.6770141601562, 18.791603753190085],
          [105.3526733398437, 18.52096883329724],
          [105.7811401367187, 18.54180220057951],
          [105.7976196289062, 19.300461796064834],
          [105.0011108398437, 20.122686131769573],
          [104.6001098632812, 19.719859112799057],
          [104.0453002929687, 19.761221836922864]]]);
Map.centerObject(roi, 8);
Map.addLayer(roi, {color: "red"}, "roi");

/**
forest 0
urban 1
paddyrice 2
water 3
crop 4
*/

var palette = ["ff0000","00ff00", "0000ff","ff00ff", "00ffff"];
var names = ["森林", "人造地表","水稻","水体","耕地"];

function addLegend(palette, names, position, isReturn) {
  // set position of panel
  var legend = ui.Panel({
    style: {
      position: position,
      padding: '8px 15px'
    }
  });
   
  // Create legend title
  var legendTitle = ui.Label({
    value: '类别',
    style: {
      fontWeight: 'bold',
      fontSize: '18px',
      margin: '0 0 4px 0',
      padding: '0'
      }
  });
   
  // Add the title to the panel
  legend.add(legendTitle);
   
  // Creates and styles 1 row of the legend.
  var makeRow = function(color, name) {
   
        // Create the label that is actually the colored box.
        var colorBox = ui.Label({
          style: {
            backgroundColor: '#' + color,
            // Use padding to give the box height and width.
            padding: '8px',
            margin: '0 0 4px 0'
          }
        });
   
        // Create the label filled with the description text.
        var description = ui.Label({
          value: name,
          style: {margin: '0 0 4px 6px'}
        });
   
        // return the panel
        return ui.Panel({
          widgets: [colorBox, description],
          layout: ui.Panel.Layout.Flow('horizontal')
        });
  };
   
  
  // name of the legend
  var count = palette.length;
  // Add color and and names
  for (var i = 0; i < count; i++) {
    legend.add(makeRow(palette[i], names[i]));
  }  
  
  if (isReturn === false) {
    ui.root.insert(0, legend);
  } else {
    return legend;
  }
}


var classified = ee.Image("users/wangweihappy0/training01/l8Classifiedmap");
var result = classified.clip(roi).toByte();
var visParam = {
  min: 1,
  max: palette.length,
  palette: palette
};
Map.addLayer(result, visParam, "image"); 
addLegend(palette, names, 'bottom-left', false);

function caculateArea01(result) {
  var dict = ee.Image.pixelArea()
              .addBands(result)
              .reduceRegion({
                reducer:ee.Reducer.sum().group({
                  groupField:1,
                  groupName:'type',
                }),
                geometry:result.geometry().bounds(),
                scale:30,
                maxPixels:1e13
              });
  var groups = ee.List(dict.get("groups"));
  var typeNames = ee.List(names);
  var featureList = groups.map(function(group){
    group = ee.Dictionary(group);
    var area = ee.Number(group.get("sum"));
    area = area.divide(1000000);
    var type = ee.Number(group.get("type"));
    var f = ee.Feature(null, {
      "type": type, 
      "area": area, 
      "name": typeNames.get(type.subtract(1))
    });
    return f;
  });
  var areaFCol = ee.FeatureCollection(featureList);
  var totalArea = ee.Number(areaFCol.aggregate_sum("area"));
  areaFCol = areaFCol.map(function(f){
    var _area = ee.Number(f.get("area"));
    f = f.set("percent", _area.divide(totalArea));
    f = f.set("totalArea", totalArea);
    return f;
  });
  print("caculateArea01", areaFCol);
}

function caculateArea02(result) {
  var wkt_text = 'PROJCS["unnamed",GEOGCS["WGS 84", DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]], AUTHORITY["EPSG","4326"]],PROJECTION["Albers_Conic_Equal_Area"],PARAMETER["standard_parallel_1",25],PARAMETER["standard_parallel_2",47],PARAMETER["latitude_of_center",0],PARAMETER["longitude_of_center",105],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["Meter",1]]';
  var crs = ee.Projection(wkt_text);
  var dict = result.addBands(result.rename("type"))
                  .reduceRegion({
                    reducer: ee.Reducer.count().group({
                      groupField:1,
                      groupName:'type',
                    }),
                    geometry:result.geometry().bounds(),
                    scale:30,
                    maxPixels:1e13,
                    crs: crs
                  });
  var groups = ee.List(dict.get("groups"));
  var typeNames = ee.List(names);
  var featureList = groups.map(function(group){
    group = ee.Dictionary(group);
    var pixelCount = ee.Number(group.get("count"));
    var area = pixelCount.multiply(30 * 30);
    area = area.divide(1000000);
    var type = ee.Number(group.get("type"));
    var f = ee.Feature(null, {
      "type": type, 
      "area": area, 
      "name": typeNames.get(type.subtract(1))
    });
    return f;
  });
  var areaFCol = ee.FeatureCollection(featureList);
  var totalArea = ee.Number(areaFCol.aggregate_sum("area"));
  areaFCol = areaFCol.map(function(f){
    var _area = ee.Number(f.get("area"));
    f = f.set("percent", _area.divide(totalArea));
    f = f.set("totalArea", totalArea);
    return f;
  });
  print("caculateArea02", areaFCol);
}

caculateArea01(result);
caculateArea02(result);
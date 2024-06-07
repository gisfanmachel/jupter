//https://code.earthengine.google.com/d3737835f68cd60525a26cd849047ed7

var image = ee.Image('CGIAR/SRTM90_V4');
// 设置两个值间隔样式 intervals
var sld_intervals =
  '<RasterSymbolizer>' +
    '<ColorMap  type="intervals" extended="false" >' +
      '<ColorMapEntry color="#0000ff" quantity="50" label="(-,50]"/>' +
      '<ColorMapEntry color="#00ff00" quantity="100" label="(50,100]" />' +
      '<ColorMapEntry color="#007f30" quantity="200" label="(100,200]" />' +
      '<ColorMapEntry color="#30b855" quantity="300" label="(200,300]" />' +
      '<ColorMapEntry color="#ff0000" quantity="400" label="(300,400]" />' +
      '<ColorMapEntry color="#ffff00" quantity="1000" label="(400,1000]" />' +
    '</ColorMap>' +
  '</RasterSymbolizer>';

// 设置两个值之间平滑过度样式 ramp
var sld_ramp =
  '<RasterSymbolizer>' +
    '<ColorMap type="ramp" extended="false" >' +
      '<ColorMapEntry color="#0000ff" quantity="50" label="50"/>' +
      '<ColorMapEntry color="#00ff00" quantity="100" label="100" />' +
      '<ColorMapEntry color="#007f30" quantity="200" label="200" />' +
      '<ColorMapEntry color="#30b855" quantity="300" label="300" />' +
      '<ColorMapEntry color="#ff0000" quantity="400" label="400" />' +
      '<ColorMapEntry color="#ffff00" quantity="500" label="500" />' +
    '</ColorMap>' +
  '</RasterSymbolizer>';

// 设置值相等模式 equal values
var sld_values =
  '<RasterSymbolizer>' +
    '<ColorMap type="values" extended="false" >' +
      '<ColorMapEntry color="#0000ff" quantity="0" label="0"/>' +
      '<ColorMapEntry color="#00ff00" quantity="100" label="100" />' +
      '<ColorMapEntry color="#007f30" quantity="200" label="200" />' +
      '<ColorMapEntry color="#30b855" quantity="300" label="300" />' +
      '<ColorMapEntry color="#ff0000" quantity="400" label="400" />' +
      '<ColorMapEntry color="#ffff00" quantity="500" label="500" />' +
    '</ColorMap>' +
  '</RasterSymbolizer>';
  
Map.setCenter(-76.8054, 42.0289, 8);
Map.addLayer(image, {}, "dem");
Map.addLayer(image.sldStyle(sld_intervals), {}, 'SLD intervals');
Map.addLayer(image.sldStyle(sld_ramp), {}, 'SLD ramp');
Map.addLayer(image.sldStyle(sld_values), {}, 'SLD values');

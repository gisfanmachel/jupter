//代码链接：https://code.earthengine.google.com/e1044048d1a45e38cff1542272417828

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

var l8Col = ee.ImageCollection("LANDSAT/LC08/C01/T1_SR")
              .filterBounds(roi)
              .filterDate("2018-1-1", "2019-1-1");
var srtm = ee.Image("USGS/SRTMGL1_003");
print("l8Col", l8Col);
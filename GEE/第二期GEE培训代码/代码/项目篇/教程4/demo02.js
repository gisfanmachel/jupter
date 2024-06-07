var roi = ee.Geometry.Polygon(
        [[[97.35198840029386, 38.44010528815348],
          [97.35198840029386, 38.164216161700466],
          [97.82714709170011, 38.164216161700466],
          [97.82714709170011, 38.44010528815348]]], null, false);
Map.centerObject(roi, 10);
Map.addLayer(roi, {color: "red"}, "roi", false);
var fCol = ee.FeatureCollection("users/wangweihappy0/training02/halahu_year_bounds");
print("fCol", fCol);
Map.addLayer(fCol, {color: "blue"}, "fCol", false);
var startDate = ee.Date("2014-1-1");
var endDate = ee.Date("2019-1-1");
var sCol = ee.ImageCollection("MODIS/006/MOD10A1")
            .filterDate(startDate, endDate)
            .select(["NDSI_Snow_Cover", "NDSI_Snow_Cover_Class"]);
var snowCover = sCol.select('NDSI_Snow_Cover').first();
var vis = {
  min: 0.0,
  max: 100.0,
  palette: ['black', '0dffff', '0524ff', 'ffffff'],
};
Map.addLayer(snowCover, vis, 'SnowCover');

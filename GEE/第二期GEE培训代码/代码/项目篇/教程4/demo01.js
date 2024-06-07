var roi = 
    /* color: #d63000 */
    /* displayProperties: [
      {
        "type": "rectangle"
      }
    ] */
    ee.Geometry.Polygon(
        [[[97.35198840029386, 38.44010528815348],
          [97.35198840029386, 38.164216161700466],
          [97.82714709170011, 38.164216161700466],
          [97.82714709170011, 38.44010528815348]]], null, false);
Map.centerObject(roi, 10);
Map.addLayer(roi, {color: "red"}, "roi");
var fCol = ee.FeatureCollection("users/wangweihappy0/training02/halahu_year_bounds");
print("fCol", fCol);
Map.addLayer(fCol, {color: "blue"}, "fCol");

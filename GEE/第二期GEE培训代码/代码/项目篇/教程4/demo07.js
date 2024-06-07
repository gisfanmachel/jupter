var roi = ee.Geometry.Polygon(
        [[[97.35198840029386, 38.44010528815348],
          [97.35198840029386, 38.164216161700466],
          [97.82714709170011, 38.164216161700466],
          [97.82714709170011, 38.44010528815348]]], null, false);
Map.centerObject(roi, 10);
Map.addLayer(roi, {color: "red"}, "roi", false);

var year = 2014;
var fCol = ee.FeatureCollection("users/wangweihappy0/training02/halahuIceArea")
            .filter(ee.Filter.eq("year", year))
            .map(function(feature) {
              var area_ice = feature.get("area_ice");
              area_ice = ee.Algorithms.If(area_ice, ee.Number(area_ice), 0);
              area_ice = ee.Number(area_ice);
              feature = feature.set("area_ice", area_ice);
              var area_cloud = feature.get("area_cloud");
              area_cloud = ee.Algorithms.If(area_cloud, ee.Number(area_cloud), 0);
              area_cloud = ee.Number(area_cloud);
              feature = feature.set("area_cloud", area_cloud);
              var area_water = feature.get("area_water");
              area_water = ee.Algorithms.If(area_water, ee.Number(area_water), 0);
              area_water = ee.Number(area_water);
              feature = feature.set("area_water", area_water);
              var percent = area_ice.divide(area_ice.add(area_water));
              feature = feature.set("percent", percent);
              return feature;
            })
            .sort("start_date");
print(fCol);

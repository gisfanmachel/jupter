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
var endDate = ee.Date("2015-1-1");
var step = 5;
var sCol = ee.ImageCollection("MODIS/006/MOD10A1")
            .filterDate(startDate, endDate)
            .select(["NDSI_Snow_Cover", "NDSI_Snow_Cover_Class"]);

var dayNum = endDate.difference(startDate, "day");
var dayList = ee.List.sequence(0, dayNum.subtract(1), step);
print("dayList", dayList);

var dayImgList = dayList.map(function(day) {
  day = ee.Number(day);
  var _sdate = startDate.advance(day, "day");
  var _edate = startDate.advance(day.add(step), "day");
  var tempCol = sCol.filterDate(_sdate, _edate);
  var image = tempCol.mosaic();
  image = image.set("start_date", _sdate);
  image = image.set("end_date", _edate);
  image = image.set("year", _sdate.get("year"));
  image = image.set("count", tempCol.size());
  image = image.set("system:index", _sdate.format("yyyyMMdd"));
  return image;
});
print("raw dayImgList", dayImgList);
var dayImgCol = ee.ImageCollection.fromImages(dayImgList)
                  .filter(ee.Filter.gt("count", 0))
                  .map(function(image) {
                    var NDSI_Snow_Cover = image.select("NDSI_Snow_Cover");
                    var NDSI_Snow_Cover_Class = image.select("NDSI_Snow_Cover_Class");
                    NDSI_Snow_Cover_Class = NDSI_Snow_Cover_Class.updateMask(NDSI_Snow_Cover_Class.eq(237));
                    NDSI_Snow_Cover_Class = NDSI_Snow_Cover_Class.unmask(250);
                    NDSI_Snow_Cover_Class = NDSI_Snow_Cover_Class.updateMask(NDSI_Snow_Cover.mask().not());
                    NDSI_Snow_Cover = NDSI_Snow_Cover.unmask(NDSI_Snow_Cover_Class).clip(roi);
                    return NDSI_Snow_Cover.toByte();
                  })
                  .map(function(image) {
                    //水
                    image = image.where(image.eq(237).or(image.lte(40).and(image.gt(0))), 1);
                    //云
                    image = image.where(image.eq(250), 2);
                    //冰
                    image = image.where(image.gt(40).and(image.lte(100)), 3);
                    image = image.updateMask(image.gt(0));
                    return image;
                  });
print("select dayImgCol",dayImgCol);

dayImgCol = dayImgCol.limit(1).map(function(image) {
  var year = ee.Number(image.get("year"));
  var tempFCol = fCol.filter(ee.Filter.eq("year", year));
  var areaImage = ee.Image.pixelArea();
  areaImage = areaImage.addBands(image).clip(tempFCol);
  var dict = areaImage.reduceRegion({
    reducer: ee.Reducer.sum().group({
      groupField: 1, 
      groupName: "class"
    }), 
    geometry: tempFCol.geometry(),
    scale: 30,
    maxPixels: 1e13,
    tileScale: 16
  });
  var temp_areas = ee.List.repeat(0, 3);
  var groups = ee.List(dict.get("groups"));
  var areas = groups.iterate(function(data, list){
    data = ee.Dictionary(data);
    list = ee.List(list);
    var _class = ee.Number(data.get("class"));
    var _area = ee.Number(data.get("sum"));
    list = list.set(_class.subtract(1), _area);
    return list;
  }, temp_areas);
  areas = ee.List(areas);
  var area_water = areas.get(0);
  var area_cloud = areas.get(1);
  var area_ice = areas.get(2);
  image = image.set("area_water", area_water);
  image = image.set("area_cloud", area_cloud);
  image = image.set("area_ice", area_ice);
  return image;
});
print("dayImgCol first", dayImgCol);

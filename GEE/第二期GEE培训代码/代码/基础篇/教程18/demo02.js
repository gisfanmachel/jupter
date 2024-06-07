//代码链接：https://code.earthengine.google.com/00091cbb4e2fba91f3894e129b099383

//ui.Chart.feature.byProperty
//美国城市温度
var fCol = ee.FeatureCollection("ft:1G3RZbWoTiCiYv_LEwc7xKZq8aYoPZlL5_KuVhyDM")
             .limit(1);
             
print(fCol);
  
var months = {
  avg_temp_jan: 1,
  avg_temp_apr: 4,
  avg_temp_jul: 7,
  avg_temp_oct: 10
};

var chart = ui.Chart.feature.byProperty(fCol, months, "city_name")
    .setChartType("ScatterChart")
    .setOptions({
      title: "City Month Temp List",
      hAxis: {
        title: "Month",
        ticks: [{v: 1, f: "January"},
                {v: 4, f: "April"},
                {v: 7, f: "July"},
                {v: 10, f: "October"}]
      },
      vAxis: {
        title: "Temp"
      },
      lineWidth: 1,
      pointSize: 3
});
print(chart);
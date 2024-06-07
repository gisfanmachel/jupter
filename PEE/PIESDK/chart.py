# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   chart.py
@Time    :   2020/8/7 下午7:30
@Author  :   lsw
@Version :   1.0
@Contact :   shi_weihappy@126.com
@License :   (C)Copyright 2019-2020, lsw
@Desc    :   None
"""
from pyecharts.charts import Bar, Line, Pie, Scatter, Boxplot, Gauge, Radar
from pyecharts import options as opts
from pie.object import PIEObject

#更新pyecharts的默认资源路径
from pyecharts.globals import CurrentConfig, NotebookType
custom_host = "https://cdn.bootcdn.net/ajax/libs/echarts/4.8.0/"
CurrentConfig.ONLINE_HOST = custom_host
CurrentConfig.NOTEBOOK_TYPE = NotebookType.JUPYTER_NOTEBOOK

class PIEChart(PIEObject):
    def __init__(self):
        super(PIEChart, self).__init__()
        self.pre = None
        self.statement = None

    @staticmethod
    def initJupyterLabEnv():
        CurrentConfig.NOTEBOOK_TYPE = NotebookType.JUPYTER_LAB

    @staticmethod
    def initJupyterNotebookEnv():
        CurrentConfig.NOTEBOOK_TYPE = NotebookType.JUPYTER_NOTEBOOK

    @staticmethod
    def name():
        return "PIEChart"

    @staticmethod
    def loadJavaScript(chart):
        return chart.load_javascript()

    @staticmethod
    def renderChart(chart):
        return chart.render_notebook()

    @staticmethod
    def _render(chart):
        if CurrentConfig.NOTEBOOK_TYPE == NotebookType.JUPYTER_LAB:
            return chart
        else:
            return PIEChart.renderChart(chart)

    @staticmethod
    def _bar(**kwargs):
        """
        绘制条形图
        :param kwargs:
        :return:
        """
        _legend = kwargs.get("legend", [])
        _series = kwargs.get("series", [])
        if len(_legend) != len(_series):
            print("参数 legend 和 series 不对应")
            return None
        _title = kwargs.get("title", "")
        _xAxisName = kwargs.get("xAxisName", "")
        _yAxis = [str(x) for x in kwargs.get("yAxis", [])]
        _yAxisName = kwargs.get("yAxisName", "")

        _chart = Bar()
        _chart = _chart.set_global_opts(
            title_opts=opts.TitleOpts(title=_title),
            tooltip_opts=opts.TooltipOpts(
                is_show=True,
                trigger="axis"
            ),
            legend_opts=opts.LegendOpts(pos_right=25, pos_top=30),
            yaxis_opts=opts.AxisOpts(
                type_="category",
                boundary_gap=True,
                name=_yAxisName),
            xaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                name=_xAxisName
            )
        )
        _chart = _chart.add_xaxis(xaxis_data=_yAxis)
        for i in range(len(_legend)):
            _chart = _chart.add_yaxis(
                series_name=_legend[i],
                y_axis=_series[i],
                label_opts=opts.LabelOpts(is_show=False)
            )
        _chart = _chart.reversal_axis()
        return PIEChart._render(_chart)

    @staticmethod
    def _line(**kwargs):
        """
        绘制折线图
        :param kwargs:
        :return:
        """
        _legend = kwargs.get("legend", '')
        _series = kwargs.get("series", [])
        _smooth = kwargs.get("smooth", False)
        _title = kwargs.get("title", "")
        _xAxis = [str(x) for x in kwargs.get("xAxis", [])]
        _xAxisName = kwargs.get("xAxisName", "")
        _yAxisName = kwargs.get("yAxisName", "")

        _chart = Line()
        _chart = _chart.set_global_opts(
            title_opts=opts.TitleOpts(title=_title),
            tooltip_opts=opts.TooltipOpts(
                is_show=True,
                trigger="axis"
            ),
            legend_opts=opts.LegendOpts(pos_right=25, pos_top=30),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                boundary_gap=True,
                splitline_opts=opts.SplitLineOpts(is_show=True),
                name=_xAxisName),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                name=_yAxisName
            )
        )
        _chart = _chart.add_xaxis(xaxis_data=_xAxis)
        _chart = _chart.add_yaxis(
            series_name=_legend,
            y_axis=_series,
            symbol="emptyCircle",
            is_symbol_show=True,
            label_opts=opts.LabelOpts(is_show=False),
            is_smooth=_smooth
            )
        return PIEChart._render(_chart)

    @staticmethod
    def _column(**kwargs):
        """
        绘制直方图
        :param kwargs:
        :return:
        """
        _legend = kwargs.get("legend", [])
        _series = kwargs.get("series", [])
        if len(_legend) != len(_series):
            print("参数 legend 和 series 不对应")
            return None
        _title = kwargs.get("title", "")
        _xAxisName = kwargs.get("xAxisName", "")
        _xAxis = [str(x) for x in kwargs.get("xAxis", [])]
        _yAxisName = kwargs.get("yAxisName", "")

        _chart = Bar()
        _chart = _chart.set_global_opts(
            title_opts=opts.TitleOpts(title=_title),
            tooltip_opts=opts.TooltipOpts(
                is_show=True,
                trigger="axis"
            ),
            legend_opts=opts.LegendOpts(pos_right=25, pos_top=30),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                boundary_gap=True,
                name=_xAxisName),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                name=_yAxisName
            )
        )
        _chart = _chart.add_xaxis(xaxis_data=_xAxis)
        for i in range(len(_legend)):
            _chart = _chart.add_yaxis(
                series_name=_legend[i],
                y_axis=_series[i],
                label_opts=opts.LabelOpts(is_show=False)
            )
        return PIEChart._render(_chart)

    @staticmethod
    def _pie(**kwargs):
        """
        绘制饼图
        :param kwargs:
        :return:
        """
        _legend = kwargs.get("legend", [])
        _series = kwargs.get("series", [])
        if len(_legend) != len(_series):
            print("参数 legend 和 series 不对应")
            return None
        _seriesName = kwargs.get("seriesName", False)
        _title = kwargs.get("title", "")

        _chart = Pie()
        _chart = _chart.set_global_opts(
            title_opts=opts.TitleOpts(title=_title),
            tooltip_opts=opts.TooltipOpts(
                is_show=True,
                trigger="item",
                formatter="{a} <br/>{b}: {c} ({d}%)"
            ),
            legend_opts=opts.LegendOpts(
                orient="vertical",
                pos_left=0,
                pos_top=20)
        )
        _chart = _chart.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        _chart = _chart.add(
            series_name=_seriesName,
            data_pair=[list(z) for z in zip(_legend, _series)]
        )
        return PIEChart._render(_chart)

    @staticmethod
    def _scatter(**kwargs):
        """
        绘制散点图
        :param kwargs:
        :return:
        """
        _legend = kwargs.get("legend", [])
        _series = kwargs.get("series", [])
        if len(_legend) != len(_series):
            print("参数 legend 和 series 不对应")
            return None
        _symbolSize = kwargs.get("symbolSize", 5)
        _title = kwargs.get("title", "")
        _xAxis = [str(x) for x in kwargs.get("xAxis", [])]
        _xAxisName = kwargs.get("xAxisName", "")
        _yAxisName = kwargs.get("yAxisName", "")

        _chart = Scatter()
        _chart = _chart.set_global_opts(
            title_opts=opts.TitleOpts(title=_title),
            tooltip_opts=opts.TooltipOpts(
                is_show=True,
                trigger="axis"
            ),
            legend_opts=opts.LegendOpts(pos_right=25, pos_top=30),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                boundary_gap=True,
                splitline_opts=opts.SplitLineOpts(is_show=True),
                name=_xAxisName),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                name=_yAxisName
            )
        )
        _chart = _chart.add_xaxis(xaxis_data=_xAxis)
        for i in range(len(_legend)):
            _chart = _chart.add_yaxis(
                series_name=_legend[i],
                y_axis=_series[i],
                label_opts=opts.LabelOpts(is_show=False),
                symbol_size=_symbolSize
            )
        return PIEChart._render(_chart)

    @staticmethod
    def _boxplot(**kwargs):
        """
        绘制箱形图
        :param kwargs:
        :return:
        """
        _legend = kwargs.get("legend", [])
        _series = kwargs.get("series", [])
        if len(_legend) != len(_series):
            print("参数 legend 和 series 不对应")
            return None
        _title = kwargs.get("title", "")
        _xAxis = [str(x) for x in kwargs.get("xAxis", [])]
        _xAxisName = kwargs.get("xAxisName", "")
        _yAxisName = kwargs.get("yAxisName", "")

        _chart = Boxplot()
        _chart = _chart.set_global_opts(
            title_opts=opts.TitleOpts(title=_title),
            tooltip_opts=opts.TooltipOpts(trigger="item", axis_pointer_type="shadow"),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                boundary_gap=True,
                splitarea_opts=opts.SplitAreaOpts(is_show=False),
                splitline_opts=opts.SplitLineOpts(is_show=False),
                name=_xAxisName
            ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                name=_yAxisName,
                splitarea_opts=opts.SplitAreaOpts(is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)),
            ),
        )
        _chart = _chart.add_xaxis(xaxis_data=_xAxis)
        for i in range(len(_legend)):
            _chart = _chart.add_yaxis(
                series_name=_legend[i],
                y_axis=_series[i],
                label_opts=opts.LabelOpts(is_show=False),
            )
        return PIEChart._render(_chart)

    @staticmethod
    def _gauge(**kwargs):
        """
        绘制仪表盘
        :param kwargs:
        :return:
        """
        _title = kwargs.get("title", "")
        # 某项指标 比如：达标率
        _target = kwargs.get("target", "")
        # 指标进度
        _rate = kwargs.get("rate", "")

        _chart = Gauge()
        _chart = _chart.add(series_name=_title,
                            data_pair=[[_target, _rate]])
        _chart = _chart.set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),
            tooltip_opts=opts.TooltipOpts(is_show=True),
        )
        return PIEChart._render(_chart)

    @staticmethod
    def _radar(**kwargs):
        _legend = kwargs.get("legend", [])
        _series = kwargs.get("series", [])
        if len(_legend) != len(_series):
            print("参数 legend 和 series 不对应")
            return None
        # 不同维度表 格式[{"name":维度名称,"max":最大值,"min":最小值}]
        _schema = kwargs.get("schema", [])
        _title = kwargs.get("title", "")

        _chart = Radar()
        _chart = _chart.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        _chart = _chart.set_global_opts(
            title_opts=opts.TitleOpts(title=_title), legend_opts=opts.LegendOpts())
        _chart = _chart.add_schema(schema=_schema)
        for i in range(len(_legend)):
            _chart = _chart.add(
                series_name=_legend[i],
                data=_series[i],
            )
        return PIEChart._render(_chart)

    @staticmethod
    def ChartArray(**kwargs):
        """
        绘制图表
        :param kwargs:
        :return:
        """
        _chart_type = kwargs.get("chartType")
        if _chart_type == "line":
            return PIEChart._line(**kwargs)
        elif _chart_type == "bar":
            return PIEChart._bar(**kwargs)
        elif _chart_type == "column":
            return PIEChart._column(**kwargs)
        elif _chart_type == "pie":
            return PIEChart._pie(**kwargs)
        elif _chart_type == "scatter":
            return PIEChart._scatter(**kwargs)
        elif _chart_type == "boxplot":
            return PIEChart._boxplot(**kwargs)
        elif _chart_type == "gauge":
            return PIEChart._gauge(**kwargs)
        elif _chart_type == "radar":
            return PIEChart._radar(**kwargs)
        else:
            return None

    @staticmethod
    def ChartImage(images, xSeries, **kwargs):
        """
        绘制影像列表图表
        :param images:
        :param xSeries:
        :param kwargs:
        :return:
        """
        result = []
        for i in range(len(images)):
            data = images[i].getInfo()
            data = data if data else {}
            x = xSeries[i]
            data["xValue"] = x
            result.append(data)

        xAxis = []
        series = list()
        for i in range(len(result)):
            _values = list(result[i].values())
            for j in range(len(_values) - 1):
                if "yScale" in kwargs and isinstance(_values[j], (int, float)):
                    yValue = _values[j] * float(kwargs.get("yScale"))
                else:
                    yValue = _values[j]
                if len(series) < len(_values) - 1:
                    series.append([yValue])
                else:
                    series.insert(j, yValue)
                    # series[j].append(yValue)
            xAxis.append(_values[len(_values) - 1])
        kwargs["xAxis"] = xAxis
        kwargs["series"] = series
        return PIEChart.ChartArray(**kwargs)



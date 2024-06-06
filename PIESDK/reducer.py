# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   reducer.py
@Time    :   2020/8/6 下午3:31
@Author  :   lsw
@Version :   1.0
@Contact :   shi_weihappy@126.com
@License :   (C)Copyright 2019-2020, lsw
@Desc    :   None
"""

from pie.object import PIEObject
from pie.utils.error import ArgsIsNull

def _generatePIEReducer(pre, statement):
    """
    生成 PIEReducer 的对象
    :param pre:
    :param statement:
    :return:
    """
    _object = PIEReducer()
    _object.pre = pre
    _object.statement = statement
    return _object

class PIEReducer(PIEObject):
    def __init__(self, args=None):
        super(PIEReducer, self).__init__()
        self.pre = None
        self.statement = None
        if args is None:
            return
        _name = type(args).__name__
        if _name == self.name() or _name == PIEObject.name():
            self.pre = args.pre
            self.statement = args.statement

    @staticmethod
    def name():
        return "PIEReducer"

    def sum(self):
        """
        求和
        :return:
        """
        _obj = self.getStatement(
            functionName="Reducer.sum",
            arguments={}
        )
        return _generatePIEReducer(self, _obj)

    def max(self, numInputs=1):
        """
        求最大值
        :param numInputs:
        :return:
        """
        if numInputs is None:
            raise ArgsIsNull("numInputs")

        _obj = self.getStatement(
            functionName="Reducer.max",
            arguments={"numInput": int(numInputs)}
        )
        return _generatePIEReducer(self, _obj)

    def min(self, numInputs=1):
        """
        求最小值
        :param numInputs:
        :return:
        """
        if numInputs is None:
            raise ArgsIsNull("numInputs")

        _obj = self.getStatement(
            functionName="Reducer.min",
            arguments={"numInput": int(numInputs)}
        )
        return _generatePIEReducer(self, _obj)

    def mean(self):
        """
        求均值
        :return:
        """
        _obj = self.getStatement(
            functionName="Reducer.mean",
            arguments={}
        )
        return _generatePIEReducer(self, _obj)

    def median(self, maxBuckets=None, minBucketWidth=None, maxRaw=None):
        """
        求中值
        :param maxBuckets:
        :param minBucketWidth:
        :param maxRaw:
        :return:
        """
        _obj = self.getStatement(
            functionName="Reducer.median",
            arguments={
                "maxBuckets": self.formatValue(maxBuckets),
                "minBucketWidth": self.formatValue(minBucketWidth),
                "maxRaw": self.formatValue(maxRaw)
            }
        )
        return _generatePIEReducer(self, _obj)

    def fixedHistogram(self, minValue, maxValue, steps):
        """
        计算直方图
        :param minValue:
        :param maxValue:
        :param steps:
        :return:
        """
        if minValue is None or maxValue is None or steps is None:
            raise ArgsIsNull("min,max,steps")

        _obj = self.getStatement(
            functionName="Reducer.fixedHistogram",
            arguments={
                "min": self.formatValue(minValue),
                "max": self.formatValue(maxValue),
                "steps": self.formatValue(steps)
            }
        )
        return _generatePIEReducer(self, _obj)

    def toList(self, tupleSize=1, numOptional=None):
        """
        将数据转为列表
        :param tupleSize:
        :param numOptional:
        :return:
        """
        if not tupleSize:
            raise ArgsIsNull("tupleSize")

        _obj = self.getStatement(
            functionName="Reducer.toList",
            arguments={
                "tupleSize": self.formatValue(tupleSize),
                "numOptional": self.formatValue(numOptional)
            }
        )
        return _generatePIEReducer(self, _obj)

    def count(self):
        """
        统计数量
        :return:
        """
        _obj = self.getStatement(
            functionName="Reducer.count",
            arguments={}
        )
        return _generatePIEReducer(self, _obj)

    def percentile(self, percentiles, outputNames=None):
        """
        按照指定的百分比取值
        :param percentiles:
        :param outputNames:
        :return:
        """
        if percentiles is None:
            raise ArgsIsNull('参数不能为空')
        _obj = self.getStatement(
            functionName="Reducer.percentile",
            arguments={
                "percentiles": self.formatValue(percentiles),
                "outputNames": self.formatValue(outputNames)
            }
        )
        return _generatePIEReducer(self, _obj)

    def first(self):
        """
        获取第一个元素
        :return:
        """
        _obj = self.getStatement(
            functionName="Reducer.first",
            arguments={
            }
        )
        return _generatePIEReducer(self, _obj)

    def last(self):
        """
        获取最后一个元素
        :return:
        """
        _obj = self.getStatement(
            functionName="Reducer.last",
            arguments={}
        )

        return _generatePIEReducer(self, _obj)

    def linearFit(self):
        """
        做线性回归拟合
        :return:
        """
        _obj = self.getStatement(
            functionName="Reducer.linearFit",
            arguments={}
        )
        return _generatePIEReducer(self, _obj)

    def linearRegression(self, numX, numY):
        """
        做线性回归拟合
        :param numX:
        :param numY:
        :return:
        """
        if numX is None or numY is None:
            raise ArgsIsNull("numX,numY")

        _obj = self.getStatement(
            functionName="Reducer.linearRegression",
            arguments={
                "numX": self.formatValue(numX),
                "numY": self.formatValue(numY)
            }
        )
        return _generatePIEReducer(self, _obj)

    def pearsonsCorrelation(self):
        """
        计算皮尔逊系数
        :return:
        """
        _obj = self.getStatement(
            functionName="Reducer.pearsonsCorrelation",
            arguments={}
        )
        return _generatePIEReducer(self, _obj)

    def stdDev(self):
        """

        :return:
        """
        _obj = self.getStatement(
            functionName="Reducer.stdDev",
            arguments={}
        )
        return _generatePIEReducer(self, _obj)

    def variance(self):
        """

        :return:
        """
        _obj = self.getStatement(
            functionName="Reducer.variance",
            arguments={},
        )
        return _generatePIEReducer(self, _obj)

    def mode(self):
        """
        计算模
        :return:
        """
        _obj = self.getStatement(
            functionName="Reducer.mode",
            arguments={}
        )
        return _generatePIEReducer(self, _obj)

    def minMax(self):
        """
        计算最大最小值
        :return:
        """
        _obj = self.getStatement(
            functionName="Reducer.minMax",
            arguments={}
        )
        return _generatePIEReducer(self, _obj)

    def covariance(self):
        """

        :return:
        """
        _obj = self.getStatement(
            functionName="Reducer.covariance",
            arguments={}
        )
        return _generatePIEReducer(self, _obj)

    def sensSlope(self):
        """

        :return:
        """
        _obj = self.getStatement(
            functionName="Reducer.sensSlope",
            arguments={}
        )
        return _generatePIEReducer(self, _obj)

Reducer = PIEReducer()


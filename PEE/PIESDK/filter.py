# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   filter.py
@Time    :   2020/8/2 上午11:11
@Author  :   lsw
@Version :   1.0
@Contact :   shi_weihappy@126.com
@License :   (C)Copyright 2019-2020, lsw
@Desc    :   None
"""

from pie.object import PIEObject
from pie.utils.error import ArgsIsNull

def _generatePIEFilter(pre, statement):
    """
    生成 PIEFilter 的对象
    :param pre:
    :param statement:
    :return:
    """
    _filter = PIEFilter()
    _filter.pre = pre
    _filter.statement = statement
    return _filter


class PIEFilter(PIEObject):
    def __init__(self, args=None):
        """
        初始化过滤条件
        :param args:
        """
        super(PIEFilter, self).__init__()
        if type(args).__name__ == self.name() \
            or type(args).__name__ == PIEObject.name():
            self.pre = args.pre
            self.statement = args.statement
        else:
            self.pre = None
            self.statement = None

    @staticmethod
    def name():
        return "PIEFilter"

    def date(self, start, end):
        """
        按照日期条件过滤
        :param start:
        :param end:
        :return:
        """
        if start is None:
            raise ArgsIsNull('start')
        if end is None:
            raise ArgsIsNull('end')

        _right = self.getStatement(
            arguments={
                "start": self.formatValue(start),
                "end": self.formatValue(end)
            },
            functionName="DateRange"
        )
        _obj = self.getStatement(
            arguments={
                "leftField": "system:time_start",
                "rightValue": _right
            },
            functionName="Filter.dateRangeContains"
        )
        return _generatePIEFilter(self, _obj)

    def bounds(self, geometry, absIntersect=True):
        """
        按照范围条件过滤
        :param geometry:
        :param absIntersect:
        :return:
        """
        if not geometry:
            raise ArgsIsNull('geometry')
        _obj = self.getStatement(
            arguments={
                "leftField": ".all",
                "rightValue": self.formatValue(geometry),
                "absIntersect": absIntersect
            },
            functionName="Filter.intersects"
        )
        return _generatePIEFilter(self, _obj)

    def eq(self, name, value):
        """
        按照指定属性过滤所有等于指定值的数据
        :param name:
        :param value:
        :return:
        """
        if name is None:
            raise ArgsIsNull('name')
        if value is None:
            raise ArgsIsNull("value")
        _obj = self.getStatement(
            arguments={
                "leftField": self.formatValue(name),
                "rightValue": self.formatValue(value)
            },
            functionName="Filter.equals"
        )
        return _generatePIEFilter(self, _obj)

    def neq(self, name, value):
        """
        按照指定属性过滤所有不等于指定值的数据
        :param name:
        :param value:
        :return:
        """
        if name is None:
            raise ArgsIsNull('name')
        if value is None:
            raise ArgsIsNull("value")
        _obj = self.getStatement(
            arguments={
                "leftField": self.formatValue(name),
                "rightValue": self.formatValue(value)
            },
            functionName="Filter.notEquals"
        )
        return _generatePIEFilter(self, _obj)

    def lt(self, name, value):
        """
        按照指定属性过滤所有小于指定值的数据
        :param name:
        :param value:
        :return:
        """
        if name is None:
            raise ArgsIsNull('name')
        if value is None:
            raise ArgsIsNull("value")
        _obj = self.getStatement(
            arguments={
                "leftField": self.formatValue(name),
                "rightValue": self.formatValue(value)
            },
            functionName="Filter.lessThan"
        )
        return _generatePIEFilter(self, _obj)

    def lte(self, name, value):
        """
        按照指定属性过滤所有小于等于指定值的数据
        :param name:
        :param value:
        :return:
        """
        if name is None:
            raise ArgsIsNull('name')
        if value is None:
            raise ArgsIsNull("value")
        _obj = self.getStatement(
            arguments={
                "leftField": self.formatValue(name),
                "rightValue": self.formatValue(value)
            },
            functionName="Filter.lessThanEquals"
        )
        return _generatePIEFilter(self, _obj)

    def gt(self, name, value):
        """
        按照指定属性过滤所有大于指定值的数据
        :param name:
        :param value:
        :return:
        """
        if name is None:
            raise ArgsIsNull('name')
        if value is None:
            raise ArgsIsNull("value")
        _obj = self.getStatement(
            arguments={
                "leftField": self.formatValue(name),
                "rightValue": self.formatValue(value)
            },
            functionName="Filter.greaterThan"
        )
        return _generatePIEFilter(self, _obj)

    def gte(self, name, value):
        """
        按照指定属性过滤所有大于等于指定值的数据
        :param name:
        :param value:
        :return:
        """
        if name is None:
            raise ArgsIsNull('name')
        if value is None:
            raise ArgsIsNull("value")
        _obj = self.getStatement(
            arguments={
                "leftField": self.formatValue(name),
                "rightValue": self.formatValue(value)
            },
            functionName="Filter.greaterThanEquals"
        )
        return _generatePIEFilter(self, _obj)

    def Or(self, rightFilter):
        """

        :param rightFilter:
        :return:
        """
        if rightFilter is None:
            raise ArgsIsNull('rightFilter')
        _obj = self.getStatement(
            functionName="Filter.or",
            arguments={
                "leftFilter": self.statement,
                "rightFilter": self.formatValue(rightFilter)
            }
        )
        return _generatePIEFilter(self, _obj)

    def And(self, rightFilter):
        """

        :param rightFilter:
        :return:
        """
        if rightFilter is None:
            raise ArgsIsNull('filter')
        _obj = self.getStatement(
            functionName="Filter.and",
            arguments={
                "leftFilter": self.statement,
                "rightFilter": self.formatValue(rightFilter)
            }
        )
        return _generatePIEFilter(self, _obj)

    def dayOfYear(self, start, end):
        """

        :param start:
        :param end:
        :return:
        """
        if start is None:
            raise ArgsIsNull('start')
        if end is None:
            raise ArgsIsNull("end")
        _obj = self.getStatement(
            functionName="Filter.dayOfYear",
            arguments={
                "start": self.formatValue(start),
                "end": self.formatValue(end)
            }
        )
        return _generatePIEFilter(self, _obj)

    def calendarRange(self, start, end, field="day_of_year"):
        """

        :param start:
        :param end:
        :param field:
        :return:
        """
        if start is None:
            raise ArgsIsNull('start')
        if end is None:
            raise ArgsIsNull("end")
        if field is None:
            raise ArgsIsNull("field")

        _obj = self.getStatement(
            functionName="Filter.calendarRange",
            arguments={
                "start": self.formatValue(start),
                "end": self.formatValue(end),
                "field": self.formatValue(field)
            }
        )
        return _generatePIEFilter(self, _obj)

    def inList(self, field, lists):
        """

        :param field:
        :param lists:
        :return:
        """
        if field is None:
            raise ArgsIsNull('field')
        if lists is None:
            raise ArgsIsNull("lists")
        _obj = self.getStatement(
            functionName="Filter.inList",
            arguments={
                "field": self.formatValue(field),
                "list": self.formatValue(lists)
            }
        )
        return _generatePIEFilter(self, _obj)

    def maxDifference(self, difference, name, value):
        """
        返回一个筛选器，如果对象的指定字段值在给定参考值的给定数值范围内则通过
        :param difference:
        :param name:
        :param value:
        :return:
        """
        if difference is None:
            raise ArgsIsNull('difference')
        if name is None:
            raise ArgsIsNull("name")
        if value is None:
            raise ArgsIsNull("value")
        _obj = self.getStatement(
            arguments={
                "difference": self.formatValue(difference),
                "leftField": self.formatValue(name),
                "rightValue": self.formatValue(value)
            },
            functionName="Filter.maxDifference"
        )
        return _generatePIEFilter(self, _obj)

    def stringContains(self, name, value):
        """
        返回一个筛选器，如果过滤对象中指定属性的值中包含指定值则通过
        :param name:
        :param value:
        :return:
        """
        if name is None:
            raise ArgsIsNull('name')
        if value is None:
            raise ArgsIsNull("value")
        _obj = self.getStatement(
            arguments={
                "leftField": self.formatValue(name),
                "rightValue": self.formatValue(value)
            },
            functionName="Filter.stringContains"
        )
        return _generatePIEFilter(self, _obj)

    def stringStartsWith(self, name, value):
        """
        返回一个筛选器，如果过滤对象中指定属性的值以指定值为开头则通过
        :param name:
        :param value:
        :return:
        """
        if name is None:
            raise ArgsIsNull('name')
        if value is None:
            raise ArgsIsNull("value")
        _obj = self.getStatement(
            arguments={
                "leftField": self.formatValue(name),
                "rightValue": self.formatValue(value)
            },
            functionName="Filter.stringStartsWith"
        )
        return _generatePIEFilter(self, _obj)

    def stringEndsWith(self, name, value):
        """
        返回一个筛选器，如果过滤对象中指定属性的值以指定值为结尾则通过
        :param name:
        :param value:
        :return:
        """
        if name is None:
            raise ArgsIsNull('name')
        if value is None:
            raise ArgsIsNull("value")
        _obj = self.getStatement(
            arguments={
                "leftField": self.formatValue(name),
                "rightValue": self.formatValue(value)
            },
            functionName="Filter.stringEndsWith"
        )
        return _generatePIEFilter(self, _obj)

    def notNull(self, lists):
        """
        返回一个筛选器，如果过滤对象的所有指定属性的属性值都不为空则通过
        :param lists:
        :return:
        """
        if lists is None:
            raise ArgsIsNull('lists')
        _obj = self.getStatement(
            functionName="Filter.notNull",
            arguments={
                "list": self.formatValue(lists),
            }
        )
        return _generatePIEFilter(self, _obj)

    def Not(self, rightFilter):
        """
        返回一个筛选器，若当前筛选器结果为不通过则通过
        :param rightFilter:
        :return:
        """
        if rightFilter is None:
            raise ArgsIsNull('rightFilter')
        _obj = self.getStatement(
            functionName="Filter.not",
            arguments={
                "rightFilter": self.formatValue(rightFilter)
            }
        )
        return _generatePIEFilter(self, _obj)

    def contains(self, geo):
        """
        生成过滤器，用于筛选过滤对象中包含于给定空间范围的部分
        :param geo:
        :return:
        """
        if geo is None:
            raise ArgsIsNull('geo')
        _obj = self.getStatement(
            functionName="Filter.contains",
            arguments={
                "geo": self.formatValue(geo)
            }
        )
        return _generatePIEFilter(self, _obj)

    def withinDistance(self, geo, distance, proj):
        """
        生成过滤器，用于筛选过滤对象中距离给定空间范围的距离在预定距离内的部分
        :param geo:
        :param distance:
        :param proj:
        :return:
        """
        if geo is None:
            raise ArgsIsNull('distance')
        if distance is None:
            raise ArgsIsNull("distance")
        _obj = self.getStatement(
            functionName="Filter.withinDistance",
            arguments={
                "geo": self.formatValue(geo),
                "distance": self.formatValue(distance),
                "proj": self.formatValue(proj)
            }
        )
        return _generatePIEFilter(self, _obj)

Filter = PIEFilter()
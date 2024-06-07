# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   feature.py
@Time    :   2020/8/2 上午11:11
@Author  :   lsw
@Version :   1.0
@Contact :   shi_weihappy@126.com
@License :   (C)Copyright 2019-2020, lsw
@Desc    :   None
"""

from pie.object import PIEObject, _generatePIEObject
from pie.utils.error import ArgsIsNull

def _generatePIEString(pre, statement):
    """
    生成 PIEString 对象
    :param pre:
    :param statement:
    :return:
    """
    from pie.string import PIEString
    _object = PIEString()
    _object.pre = pre
    _object.statement = statement
    return _object

def _generatePIENumber(pre, statement):
    """
    生成 PIENumber 对象
    :param pre:
    :param statement:
    :return:
    """
    from pie.number import PIENumber
    _object = PIENumber()
    _object.pre = pre
    _object.statement = statement
    return _object

def _generatePIEList(pre, statement):
    """
    生成 PIEList 对象
    :param pre:
    :param statement:
    :return:
    """
    from pie.list import PIEList
    _object = PIEList()
    _object.pre = pre
    _object.statement = statement
    return _object

def _generatePIEGeometry(pre, statement):
    """
    生成 PIEGeometry 的对象
    :param pre:
    :param statement:
    :return:
    """
    from pie.vector.geometry import PIEGeometry
    _object = PIEGeometry()
    _object.pre = pre
    _object.statement = statement
    return _object

def _generatePIEFeature(pre, statement):
    """
    生成 PIEFeature 的对象
    :param pre:
    :param statement:
    :return:
    """
    _object = PIEFeature()
    _object.pre = pre
    _object.statement = statement
    return _object

class PIEFeature(PIEObject):
    def __init__(self, geometry=None, properties=None):
        super(PIEFeature, self).__init__()
        self.pre = None
        self.statement = None
        if geometry is None:
            return

        if type(geometry).__name__ == self.name() \
            or type(geometry).__name__ == PIEObject.name():
            self.pre = geometry.pre
            self.statement = geometry.statement
        else:
            self.statement = self.getStatement(
                functionName="Feature.constructors",
                arguments={
                    "geometry": self.formatValue(geometry),
                    "properties": properties
                }
            )

    @staticmethod
    def name():
        return "PIEFeature"

    def setGeometry(self, geometry):
        """
        设置Feature的Geometry
        :param geometry:
        :return:
        """
        if geometry is None:
            raise ArgsIsNull('geometry')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Feature.setGeometry",
            arguments={
                "input": _input,
                "geometry": self.formatValue(geometry)
            }
        )
        return _generatePIEFeature(self, _obj)

    def geometry(self, maxError=None, proj=None, geodesics=None):
        """
        获取矢量数据的几何图形
        :param maxError:
        :param proj:
        :param geodesics:
        :return:
        """
        _input = self.statement
        _obj = self.getStatement(
            functionName="Feature.getGeometry",
            arguments={
                "input": _input,
                "maxError": self.formatValue(maxError),
                "proj": self.formatValue(proj),
                "geodesics": self.formatValue(geodesics)
            },
            compress="polyline"
        )
        return _generatePIEGeometry(self, _obj)

    def id(self):
        _input = self.statement
        _obj = self.getStatement(
            functionName="Feature.id",
            arguments={
                "input": _input
            },
            compute=True

        )
        return _generatePIEString(self, _obj)

    def set(self, key, value):
        """
        设置属性和对应的值
        :param key:
        :param value:
        :return:
        """
        if key is None or value is None:
            raise ArgsIsNull('key,value')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Feature.set",
            arguments={
                "input": _input,
                "key": self.formatValue(key),
                "value": self.formatValue(value)
            }
        )
        return _generatePIEFeature(self, _obj)

    def get(self, key):
        """
        获取指定属性的值
        :param key:
        :return:
        """
        if key is None:
            raise ArgsIsNull('key')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Feature.get",
            arguments={
                "input": _input,
                "property": self.formatValue(key)
            },
            compute=True
        )
        return _generatePIEObject(self, _obj)

    def propertyNames(self):
        """
        返回属性名称列表
        :return:
        """
        _input = self.statement
        _obj = self.getStatement(
            functionName="Feature.propertyNames",
            arguments={
                "input": _input
            },
            compute=True
        )
        return _generatePIEString(self, _obj)

    def setMulti(self, properties):
        """

        :param properties:
        :return:
        """
        if properties is None:
            raise ArgsIsNull("properties")
        _input = self.statement
        _obj = self.getStatement(
            functionName="Feature.setMulti",
            arguments={
                "input": _input,
                "properties": self.formatValue(properties)
            }
        )
        return _generatePIEFeature(self, _obj)

    def getNumber(self, property):
        """

        :param property:
        :return:
        """
        if property is None:
            raise ArgsIsNull("property")
        _input = self.statement
        _obj = self.getStatement(
            functionName="Feature.getNumber",
            arguments={
                "input": _input,
                "property": self.formatValue(property)
            },
            compute=True
        )
        return _generatePIENumber(self, _obj)
    def getString(self, property):
        """

        :param property:
        :return:
        """
        if property is None:
            raise ArgsIsNull("property")
        _input = self.statement
        _obj = self.getStatement(
            functionName="Feature.getString",
            arguments={
                "input": _input,
                "property": self.formatValue(property)
            },
            compute=True
        )
        return _generatePIEString(self, _obj)

    def getArray(self, property):
        """

        :param property:
        :return:
        """
        if property is None:
            raise ArgsIsNull("property")
        _input = self.statement
        _obj = self.getStatement(
            functionName="Feature.getArray",
            arguments={
                "input": _input,
                "property": self.formatValue(property)
            },
            compute=True
        )
        return _generatePIEList(self, _obj)

    def containedIn(self, right, proj=None):
        """
        是否被右边的矢量数据包含
        :param right:
        :param proj:
        :return:
        """
        if right is None:
            raise ArgsIsNull('right')
        _obj = self.getStatement(
            functionName="Feature.containedIn",
            arguments={
                "feature": self.statement,
                "right":self.formatValue(right),
                "proj": self.formatValue(proj)
            },
            compute=True
        )
        return _generatePIENumber(self, _obj)

    def contains(self, right, proj=None):
        """
        是否包含右边的矢量数据
        :param right:
        :param proj:
        :return:
        """
        if right is None:
            raise ArgsIsNull('right')
        _obj = self.getStatement(
            functionName="Feature.contains",
            arguments={
                "feature": self.statement,
                "right": self.formatValue(right),
                "proj": self.formatValue(proj)
            },
            compute=True
        )
        return _generatePIENumber(self, _obj)

    def difference(self, right, proj=None):
        """
        获取两个矢量数据的差集
        :param right:
        :param proj:
        :return:
        """
        if right is None:
            raise ArgsIsNull('right')
        _obj = self.getStatement(
            functionName="Feature.difference",
            arguments={
                "feature": self.statement,
                "right": self.formatValue(right),
                "proj": self.formatValue(proj)
            }
        )
        return _generatePIEFeature(self, _obj)

    def disjoint(self, right, proj=None):
        """
        判断两个Geometry是否具有共同点
        :param right:
        :param proj:
        :return:
        """
        if right is None:
            raise ArgsIsNull('right')
        _obj = self.getStatement(
            functionName="Feature.disjoint",
            arguments={
                "feature": self.statement,
                "right": self.formatValue(right),
                "proj": self.formatValue(proj)
            },
            compute=True
        )
        return _generatePIENumber(self, _obj)

    def intersects(self, right, proj=None):
        """
        判断两个Geometry是否相交
        :param right:
        :param proj:
        :return:
        """
        if right is None:
            raise ArgsIsNull('right')
        _obj = self.getStatement(
            functionName="Feature.intersects",
            arguments={
                "feature": self.statement,
                "right": self.formatValue(right),
                "proj": self.formatValue(proj)
            },
            compute=True
        )
        return _generatePIENumber(self, _obj)

    def intersection(self, right, proj=None):
        """
        获取两个Geometry的交集
        :param right:
        :param proj:
        :return:
        """
        if right is None:
            raise ArgsIsNull('right')
        _obj = self.getStatement(
            functionName="Feature.intersection",
            arguments={
                "feature": self.statement,
                "right": self.formatValue(right),
                "proj": self.formatValue(proj)
            }
        )
        return _generatePIEFeature(self, _obj)

    def union(self, right, proj=None):
        """
        获取两个Geometry的并集
        :param right:
        :param proj:
        :return:
        """
        if right is None:
            raise ArgsIsNull('right')
        _obj = self.getStatement(
            functionName="Feature.union",
            arguments={
                "feature": self.statement,
                "right": self.formatValue(right),
                "proj": self.formatValue(proj)
            }
        )
        return _generatePIEFeature(self, _obj)

    def withinDistance(self, right, distance=1, proj=None):
        """
        判断两个Geometry是否相交
        :param right:
        :param distance:
        :param proj:
        :return:
        """
        if right is None:
            raise ArgsIsNull('right')
        if distance is None:
            distance = 1
        _obj = self.getStatement(
            functionName="Feature.withinDistance",
            arguments={
                "feature": self.statement,
                "right": self.formatValue(right),
                "distance": self.formatValue(distance),
                "proj": self.formatValue(proj)
            },
            compute=True
        )
        return _generatePIENumber(self, _obj)

    def simplify(self, proj=None):
        """
        简化Geometry
        :param proj:
        :return:
        """
        _obj = self.getStatement(
            functionName="Feature.simplify",
            arguments={
                "feature": self.statement,
                "proj": self.formatValue(proj)
            }
        )
        return _generatePIEFeature(self, _obj)

    def dissolve(self, proj=None):
        """
        将所有的Geometry融合
        :param proj:
        :return:
        """
        _obj = self.getStatement(
            functionName="Feature.dissolve",
            arguments={
                "feature": self.statement,
                "proj": self.formatValue(proj)
            }
        )
        return _generatePIEFeature(self, _obj)

    def buffer(self, distance, proj=None):
        """
        为Geometry做缓冲
        :param distance:
        :param proj:
        :return:
        """
        if distance is None:
            distance = 0
        _obj = self.getStatement(
            functionName="Feature.buffer",
            arguments={
                "feature": self.statement,
                "distance": self.formatValue(distance),
                "proj": self.formatValue(proj)
            }
        )
        return _generatePIEFeature(self, _obj)

    def area(self, proj=None):
        """
        计算Geometry的面积
        :param proj:
        :return:
        """
        _obj = self.getStatement(
            functionName="Feature.area",
            arguments={
                "feature": self.statement,
                "proj": self.formatValue(proj)
            },
            compute=True
        )
        return _generatePIENumber(self, _obj)

    def length(self, proj=None):
        """
        计算Geometry的线段长度
        :param proj:
        :return:
        """
        _obj = self.getStatement(
            functionName="Feature.length",
            arguments={
                "feature": self.statement,
                "proj": self.formatValue(proj)
            },
            compute=True
        )
        return _generatePIENumber(self, _obj)


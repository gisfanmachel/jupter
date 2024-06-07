# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   imageCollection.py
@Time    :   2020/8/2 上午11:11
@Author  :   lsw
@Version :   1.0
@Contact :   shi_weihappy@126.com
@License :   (C)Copyright 2019-2020, lsw
@Desc    :   None
"""

from .object import PIEObject, _generatePIEObject
from .filter import PIEFilter
from .utils.error import ArgsIsNull

def _generatePIEImage(pre, statement):
    """
    生成 PIEImage 对象
    :param pre:
    :param statement:
    :return:
    """
    from .image import PIEImage
    _object = PIEImage()
    _object.pre = pre
    _object.statement = statement
    return _object

def _generatePIEString(pre, statement):
    """
    生成 PIEString 对象
    :param pre:
    :param statement:
    :return:
    """
    from .string import PIEString
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
    from .number import PIENumber
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
    from .list import PIEList
    _object = PIEList()
    _object.pre = pre
    _object.statement = statement
    return _object


def _generatePIEImageCollection(pre, statement):
    """
    生成 PIEImageCollection 的对象
    :param pre:
    :param statement:
    :return:
    """
    _object = PIEImageCollection()
    _object.pre = pre
    _object.statement = statement
    return _object

class PIEImageCollection(PIEObject):
    def __init__(self, args=None):
        """
        初始化影像集合
        :param args:
        """
        super(PIEImageCollection, self).__init__()
        self.pre = None
        if not args:
            self.statement = None
        elif isinstance(args, str):
            self.statement = self.getStatement(
                functionName="ImageCollection.load",
                arguments={
                    "id": args,
                }
            )
        elif type(args).__name__ == self.name() \
                    or type(args).__name__ == PIEObject.name():
            self.pre = args
            if args and args.statement is not None:
                self.statement = args.statement
            else:
                self.statement = args
        else:
            self.statement = None

    @staticmethod
    def name():
        return "PIEImageCollection"

    @classmethod
    def load(cls, collectionId):
        """
        加载影像
        :param collectionId:
        :return:
        """
        return PIEImageCollection(collectionId)

    def filter(self, pieFilter):
        """
        过滤影像集合
        :param pieFilter:
        :return:
        """
        if not pieFilter:
            raise ArgsIsNull('参数不能为空')
        _collection = self.statement
        _filter = pieFilter.statement
        _obj = self.getStatement(
            functionName="Collection.filter",
            arguments={
                "collection": _collection,
                "filter": _filter
            }
        )
        return _generatePIEImageCollection(self, _obj)

    def filterDate(self, start, end):
        """
        按照指定日期过滤影像集合
        :param start:
        :param end:
        :return:
        """
        _collection = self.statement
        _filter = PIEFilter().date(start, end)
        _filter = _filter.statement
        _obj = self.getStatement(
            functionName="Collection.filter",
            arguments={
                "collection": _collection,
                "filter": _filter
            }
        )
        return _generatePIEImageCollection(self, _obj)

    def filterBounds(self, geometry):
        """
        按照指定空间范围过滤影像集合
        :param geometry:
        :return:
        """
        if not geometry:
            raise ArgsIsNull('参数不能为空')
        _collection = self.statement
        _filter = PIEFilter().bounds(geometry)
        _filter = _filter.statement
        _obj = self.getStatement(
            functionName="Collection.filter",
            arguments={
                "collection": _collection,
                "filter": _filter
            }
        )
        return _generatePIEImageCollection(self, _obj)

    def select(self, args):
        """
        筛选指定的波段
        :param args:
        :return:
        """
        if not args:
            raise ArgsIsNull('参数不能为空')
        _collection = self.statement
        _obj = self.getStatement(
            functionName="ImageCollection.select",
            arguments={
                "collection": _collection,
                "bandSelectors": self.formatValue(args)
            }
        )
        return _generatePIEImageCollection(self, _obj)

    def setMaskValue(self, value):
        """

        :param value:
        :return:
        """
        _collection = self.statement
        _obj = self.getStatement(
            functionName="ImageCollection.setMaskValue",
            arguments={
                "collection": _collection,
                "nodata": self.formatValue(value)
            }
        )
        return _generatePIEImageCollection(self, _obj)

    def mosaic(self):
        """
        影像集合融合
        :return:
        """
        _obj = self.getStatement(
            functionName="ImageCollection.mosaic",
            arguments={"collection": self.statement}
        )
        return _generatePIEImage(self, _obj)

    def qualityMosaic(self, args):
        """
        影像集合融合
        :param args:
        :return:
        """
        _collection = self.statement
        _obj = self.getStatement(
            functionName="ImageCollection.qualityMosaic",
            arguments={
                "collection": _collection,
                "bandSelectors": self.formatValue(args)
            }
        )
        return _generatePIEImage(self, _obj)

    def min(self):
        """
        获取最小值
        :return:
        """
        _obj = self.getStatement(
            functionName="ImageCollection.min",
            arguments={"collection": self.statement}
        )
        return _generatePIEImage(self, _obj)

    def max(self):
        """
        获取最大值
        :return:
        """
        _obj = self.getStatement(
            functionName="ImageCollection.max",
            arguments={"collection": self.statement}
        )
        return _generatePIEImage(self, _obj)

    def median(self):
        """
        获取中值
        :return:
        """
        _obj = self.getStatement(
            functionName="ImageCollection.median",
            arguments={"collection": self.statement}
        )
        return _generatePIEImage(self, _obj)

    def mean(self):
        """
        获取均值
        :return:
        """
        _obj = self.getStatement(
            functionName="ImageCollection.mean",
            arguments={"collection": self.statement}
        )
        return _generatePIEImage(self, _obj)

    def sum(self):
        """
        计算求和
        :return:
        """
        _obj = self.getStatement(
            functionName="ImageCollection.sum",
            arguments={"collection": self.statement}
        )
        return _generatePIEImage(self, _obj)

    def first(self):
        """
        获取影像集合第一张影像
        :return:
        """
        _obj = self.getStatement(
            functionName="Collection.first",
            arguments={"collection": self.statement}
        )
        return _generatePIEImage(self, _obj)

    def getAt(self, index):
        """
        获取指定位置的影像
        :param index
        :return:
        """
        if index is None:
            raise ArgsIsNull('参数不能为空')
        _obj = self.getStatement(
            functionName="Collection.getAt",
            arguments={
                "collection": self.statement,
                "index": self.formatValue(index)
            }
        )
        return _generatePIEImage(self, _obj)

    def size(self):
        """
        获取集合中元素的数量
        :return:
        """
        _obj = self.getStatement(
            functionName="Collection.size",
            arguments={"collection": self.statement},
            compute=True
        )
        return _generatePIEImage(self, _obj)

    def map(self, algorithm, dropNulls=None):
        """
        循环集合
        :param algorithm:
        :param dropNulls:
        :return:
        """
        if not algorithm:
            raise ArgsIsNull('参数不能为空')
        _objElement = {
            "type": "Function",
            "arguments": [
                "_MAPPING_VAR_0_0"
            ]
        }
        _images = [_generatePIEImage(self, _objElement)]
        _imageMap = map(algorithm, _images)
        _body = list(_imageMap)[0].statement
        _baseAlgorithm = {
            "type": "Function",
            "arguments": [
                "_MAPPING_VAR_0_0"
            ],
            "body": _body
        }
        _collection = self.statement
        _obj = self.getStatement(
            functionName="Collection.map",
            arguments={
                "collection": _collection,
                "baseAlgorithm": _baseAlgorithm
            }
        )
        return _generatePIEImageCollection(self, _obj)

    def fromImages(self, images):
        """
        生成新的影像
        :param images:
        :return:
        """
        if not images:
            raise ArgsIsNull('参数不能为空')
        _collection = self.statement
        _obj = self.getStatement(
            functionName="ImageCollection.fromImages",
            arguments={
                "collection": _collection,
                "images": self.formatValue(images),
            }
        )
        return _generatePIEImageCollection(self, _obj)

    def reduceColumns(self, reducer, selectors, weightSelectors=None):
        """
        统计计算指定属性的值列表
        :param reducer:
        :param selectors:
        :param weightSelectors:
        :return:
        """
        if not reducer:
            raise ArgsIsNull('参数不能为空')
        _collection = self.statement
        _reducer = reducer.statement if reducer else None
        _obj = self.getStatement(
            functionName="Collection.reduceColumns",
            arguments={
                "collection": _collection,
                "reducer": _reducer,
                "selectors": selectors,
                "weightSelectors": weightSelectors
            },
            compute=True
        )
        return _generatePIEImageCollection(self, _obj)
    def id(self):
        _obj = self.getStatement(
            functionName="ImageCollection.id",
            arguments={
                "collection": self.statement
            },
            compute=True
        )
        return _generatePIEString(self, _obj)
    def propertyNames(self):
        _obj = self.getStatement(
            functionName="ImageCollection.propertyNames",
            arguments={
                "collection": self.statement
            },
            compute=True
        )
        return _generatePIEList(self, _obj)
    def set(self, key, value):
        """
        设置属性和对应的值
        :param key:
        :param value:
        :return:
        """
        if key is None and value is None:
            raise ArgsIsNull('参数不能为空')
        _input = self.statement
        _obj = self.getStatement(
            functionName="ImageCollection.set",
            arguments={
                "input": _input,
                "key": key,
                "value": value
            }
        )
        return _generatePIEImageCollection(self, _obj)
    def get(self, key):
        if key is None:
            raise ArgsIsNull('参数不能为空')
        _obj = self.getStatement(
            functionName="ImageCollection.get",
            arguments={
                "collection": self.statement,
                "key": key
            },
            compute=True
        )
        return _generatePIEObject(self, _obj)
    def setMulti(self, properties):
        if properties is None:
            raise ArgsIsNull('参数不能为空')
        _obj = self.getStatement(
            functionName="ImageCollection.setMulti",
            arguments={
                "collection": self.statement,
                "properties": properties
            }
        )
        return _generatePIEImageCollection(self, _obj)
    def getNumber(self, property):
        if property is None:
            raise ArgsIsNull('参数不能为空')
        _obj = self.getStatement(
            functionName="ImageCollection.getNumber",
            arguments={
                "collection": self.statement,
                "property": property
            },
            compute=True
        )
        return _generatePIENumber(self, _obj)
    def getString(self, property):
        if property is None:
            raise ArgsIsNull('参数不能为空')
        _obj = self.getStatement(
            functionName="ImageCollection.getString",
            arguments={
                "collection": self.statement,
                "property": property
            },
            compute=True
        )
        return _generatePIEString(self, _obj)
    def reduce(self, reducer):
        if reducer is None:
            raise ArgsIsNull('参数不能为空')
        _obj = self.getStatement(
            functionName="ImageCollection.reduce",
            arguments={
                "input": self.statement,
                "reducer": self.formatValue(reducer)
            }
        )
        return _generatePIEImage(self, _obj)

    def count(self):
        _obj = self.getStatement(
            functionName="ImageCollection.count",
            arguments={
                "collection": self.statement
            },
        )
        return _generatePIEImage(self, _obj)

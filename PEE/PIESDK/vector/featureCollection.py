# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   featureCollection.py
@Time    :   2020/8/2 上午11:11
@Author  :   lsw
@Version :   1.0
@Contact :   shi_weihappy@126.com
@License :   (C)Copyright 2019-2020, lsw
@Desc    :   None
"""

from pie.object import PIEObject, _generatePIEObject
from pie.filter import PIEFilter
from pie.vector.geometry import PIEGeometry
from pie.utils.error import ArgsIsNull
from pie.vector.feature import PIEFeature

def _generatePIEDictionary(pre, statement):
    """
    生成 PIEDictionary 对象
    :param pre:
    :param statement:
    :return:
    """
    from pie.dictionary import PIEDictionary
    _object = PIEDictionary()
    _object.pre = pre
    _object.statement = statement
    return _object

def _generatePIEImage(pre, statement):
    """
    生成 PIEImage 对象
    :param pre:
    :param statement:
    :return:
    """
    from pie.image.image import PIEImage
    _object = PIEImage()
    _object.pre = pre
    _object.statement = statement
    return _object

def _generatePIEConfusionMatrix(pre, statement, dType=None, array=None):
    """
    生成 PIEConfusionMatrix 对象
    :param pre:
    :param statement:
    :param dType:
    :param array:
    :return:
    """
    from pie.confusionMatrix import PIEConfusionMatrix
    _object = PIEConfusionMatrix(dType, array)
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

def _generatePIEFeatureCollection(pre, statement):
    """
    生成 PIEFeatureCollection 的对象
    :param pre:
    :param statement:
    :return:
    """
    _object = PIEFeatureCollection()
    _object.pre = pre
    _object.statement = statement
    return _object

class PIEFeatureCollection(PIEObject):
    def __init__(self, args=None, column=None):
        """
        初始化矢量集合
        :param args:
        :param column:
        """
        super(PIEFeatureCollection, self).__init__()
        self.pre = None
        self.statement = None
        if args is None:
            return
        if isinstance(args, str):
            self.statement = self.getStatement(
                functionName="FeatureCollection.load",
                arguments={"id": args}
            )
        elif isinstance(args, list):
            _features = []
            for arg in args:
                _features.append(self.formatValue(arg)) #arg.statement
            self.statement = self.getStatement(
                functionName="FeatureCollection.constructors",
                arguments={"features": _features}
            )
        elif type(args).__name__ == PIEGeometry.name():
            self.pre = args
            _features = [PIEFeature(args, None).statement]
            self.statement = self.getStatement(
                functionName="FeatureCollection.constructors",
                arguments={"features": _features}
            )
        elif type(args).__name__ == PIEFeature.name():
            self.pre = args
            _features = [args.statement]
            self.statement = self.getStatement(
                functionName="FeatureCollection.constructors",
                arguments={"features": _features}
            )
        elif type(args).__name__ == self.name() \
                or type(args).__name__ == PIEObject.name():
            self.pre = args
            self.statement = args.statement
        else:
            self.statement = None

    @staticmethod
    def name():
        return "PIEFeatureCollection"

    @classmethod
    def load(cls, collectionId):
        return PIEFeatureCollection(collectionId)

    def style(self, style):
        """
        矢量数据渲染绘制成影像对象
        :param style:
        :return:
        """
        if style is None:
            raise ArgsIsNull("style")
        _obj = self.getStatement(
            functionName="FeatureCollection.style",
            arguments={
                "featureCollection": self.statement,
                "style": self.formatValue(style)
            }
        )
        return _generatePIEImage(None, _obj)

    def sort(self, property, ascending = True):
        """
        按照指定属性拍下
        :param property:
        :param ascending:
        :return:
        """
        collection = self.statement
        obj = {
            "type": "Invocation",
            "arguments": {
                "collection": collection,
                "property": property,
                "ascending": ascending
            },
            "functionName": "Collection.sort"
        }
        return _generatePIEFeatureCollection(self, obj)

    def filter(self, pieFilter):
        """
        矢量数据过滤
        :param pieFilter:
        :return:
        """
        if pieFilter is None:
            raise ArgsIsNull('pieFilter')

        _collection = self.statement
        _filter = pieFilter.statement
        _obj = self.getStatement(
            functionName="Collection.filter",
            arguments={
                "collection": _collection,
                "filter": self.formatValue(_filter)
            }
        )
        return _generatePIEFeatureCollection(self, _obj)

    def filterDate(self, start, end):
        """
        矢量数据日期过滤
        :param start:
        :param end:
        :return:
        """
        if start is None or end is None:
            raise ArgsIsNull("start,end")
        _collection = self.statement
        _filter = PIEFilter()
        _filter = self.formatValue(_filter.date(start, end))
        _obj = self.getStatement(
            functionName="Collection.filter",
            arguments={
                "collection": _collection,
                "filter": _filter
            }
        )
        return _generatePIEFeatureCollection(self, _obj)

    def filterBounds(self, geometry, absIntersect=True):
        """
        矢量数据范围过滤
        :param geometry:
        :param absIntersect:
        :return:
        """
        if geometry is None:
            raise ArgsIsNull("geometry")
        _collection = self.statement
        _filter = PIEFilter()
        _filter = self.formatValue(_filter.bounds(geometry, absIntersect))
        _obj = self.getStatement(
            functionName="Collection.filter",
            arguments={
                "collection": _collection,
                "filter": _filter
            }
        )
        return _generatePIEFeatureCollection(self, _obj)

    def first(self):
        """
        获取矢量集合的第一个矢量数据
        :return:
        """
        _obj = self.getStatement(
            functionName="Collection.first",
            arguments={"collection": self.statement}
        )
        return _generatePIEFeature(self, _obj)

    def getAt(self, index):
        """
        获取指定编号的矢量数据
        :param index:
        :return:
        """
        if index is None:
            raise ArgsIsNull("index")
        _obj = self.getStatement(
            functionName="Collection.getAt",
            arguments={
                "collection": self.statement,
                "index": self.formatValue(index)
            }
        )
        return _generatePIEFeature(self, _obj)

    def size(self):
        """
        获得矢量数据中的元素个数
        :return:
        """
        _obj = self.getStatement(
            functionName="Collection.size",
            arguments={"collection": self.statement},
            compute=True
        )
        return _generatePIENumber(self, _obj)

    def map(self, algorithm, dropNulls=None):
        """
        循环遍历矢量集合
        :param algorithm:
        :param dropNulls:
        :return:
        """
        _objElement = {
            "type": "Function",
            "arguments": [
                "_MAPPING_VAR_0_0"
            ]
        }
        _features = list([_generatePIEFeature(self, _objElement)])
        _featureMap = list(map(algorithm, _features))
        _body = self.formatValue(_featureMap[0])
        _baseAlgorithm = {
            "type": "Function",
            "arguments": [
                "_MAPPING_VAR_0_0"
            ],
            "body": _body
        }
        _obj = self.getStatement(
            functionName="Collection.map",
            arguments={
                "collection": self.statement,
                "baseAlgorithm": _baseAlgorithm
            }
        )
        return _generatePIEFeatureCollection(self, _obj)

    def reduceColumns(self, reducer, selectors, weightSelectors=None):
        """
        统计指定属性值列表
        :param reducer:
        :param selectors:
        :param weightSelectors:
        :return:
        """
        if reducer is None or selectors is None:
            raise ArgsIsNull("reducer,selectors")

        _collection = self.statement
        _obj = self.getStatement(
            functionName="Collection.reduceColumns",
            arguments={
                "collection": _collection,
                "reducer": self.formatValue(reducer),
                "selectors": selectors,
                "weightSelectors": weightSelectors
            },
            compute=True
        )
        return _generatePIEDictionary(self, _obj)

    def id(self):
        """

        :return:
        """
        _input = self.statement
        _obj = self.getStatement(
            functionName="FeatureCollection.id",
            arguments={
                "collection": _input
            },
            compute=True
        )
        return _generatePIEString(self, _obj)

    def propertyNames(self):
        """

        :return:
        """
        _input = self.statement
        _obj = self.getStatement(
            functionName="FeatureCollection.propertyNames",
            arguments={
                "collection": _input
            },
            compute=True
        )
        return _generatePIEList(self, _obj)
    def get(self, key):
        """
        获取指定属性的值
        :param key:
        :return:
        """
        if key is None:
            raise ArgsIsNull("key")
        _obj = self.getStatement(
            functionName="FeatureCollection.get",
            arguments={
                "input": self.statement,
                "key": self.formatValue(key)
            },
            compute=True
        )
        return _generatePIEObject(self, _obj)

    def set(self, key, value):
        """
        设置指定属性的指定值
        :param key:
        :param value:
        :return:
        """
        if key is None or value is None:
            raise ArgsIsNull("key,value")
        _obj = self.getStatement(
            functionName="FeatureCollection.set",
            arguments={
                "input": self.statement,
                "key": self.formatValue(key),
                "value": self.formatValue(value)
            }
        )
        return _generatePIEFeatureCollection(self, _obj)

    def setMulti(self, properties):
        """

        :param properties:
        :return:
        """
        if properties is None:
            raise ArgsIsNull('properties')
        _input = self.statement
        _obj = self.getStatement(
            functionName="FeatureCollection.setMulti",
            arguments={
                "collection": _input,
                "properties": properties
            }
        )
        return _generatePIEFeatureCollection(self, _obj)

    def getNumber(self, property):
        """

        :param property:
        :return:
        """
        if property is None:
            raise ArgsIsNull('property')
        _input = self.statement
        _obj = self.getStatement(
            functionName="FeatureCollection.getNumber",
            arguments={
                "collection": _input,
                "property": property
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
            raise ArgsIsNull('property')
        _input = self.statement
        _obj = self.getStatement(
            functionName="FeatureCollection.getString",
            arguments={
                "collection": _input,
                "property": property
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
            raise ArgsIsNull('property')
        _input = self.statement
        _obj = self.getStatement(
            functionName="FeatureCollection.getArray",
            arguments={
                "collection": _input,
                "property": property
            },
            compute=True
        )
        return _generatePIEList(self, _obj)

    def geometries(self, tolerance=0):
        """

        :param tolerance:
        :return:
        """
        _input = self.statement
        _obj = self.getStatement(
            functionName="FeatureCollection.geometries",
            arguments={
                "collection": _input,
                "tolerance": tolerance
            },
            compress = "polyline"
        )
        return _generatePIEList(self, _obj)

    def randomColumn(self, columnName="random", seed=0, distribution="uniform"):
        """

        @param columnName:
        @param seed:
        @param distribution:
        @return:
        """
        _obj = self.getStatement(functionName="FeatureCollection.randomColumn",
                                 arguments={
                                     "collection": self.statement,
                                     "columnName": columnName,
                                     "seed": seed,
                                     "distribution": distribution,
                                 })
        return _generatePIEFeatureCollection(self, _obj)

    def limit(self, count=1):
        """

        @param count:
        @return:
        """
        if count is None or count <= 0:
            count = 1
        _collection = self.statement
        _obj = self.getStatement(functionName="Collection.limit",
                                 arguments={
                                     "collection": _collection,
                                     "count": count
                                 })
        return _generatePIEFeatureCollection(self, _obj)

    def merge(self, fCollection):
        """

        @param fCollection:
        @return:
        """
        if fCollection is None:
            raise ArgsIsNull("fCollection")
        _collection = self.formatValue(fCollection)
        _obj = self.getStatement(functionName="FeatureCollection.merge",
                                 arguments={
                                     "collection1": self.statement,
                                     "collection2": _collection
                                 })
        return _generatePIEFeatureCollection(self, _obj)

    def union(self):
        """

        @return:
        """
        _collection = self.statement
        _obj = self.getStatement(functionName="FeatureCollection.union",
                                 arguments={
                                     "collection": _collection
                                 })
        return _generatePIEFeatureCollection(self, _obj)

    def classify(self, classifier, outputName="classification"):
        """

        @param classifier:
        @param outputName:
        @return:
        """
        if classifier is None:
            raise ArgsIsNull("classifier")
        _obj = self.getStatement(functionName="FeatureCollection.classify",
                                 arguments={
                                     "collection": self.statement,
                                     "classifier": self.formatValue(classifier),
                                     "outputName": outputName
                                 })

        return _generatePIEFeatureCollection(self, _obj)

    def errorMatrix(self, actual, predicted, order=None):
        """

        @param actual:
        @param predicted:
        @param order:
        @return:
        """
        if actual is None or predicted is None:
            raise ArgsIsNull("actual,predicted")
        _obj = self.getStatement(functionName="FeatureCollection.errorMatrix",
                                 arguments={
                                     "collection": self.statement,
                                     "actual": actual,
                                     "predicted": predicted,
                                     "order": order,
                                 })
        return _generatePIEConfusionMatrix(self, _obj)

    def aggregate_count(self, property):
        """
        :param property:
        :return:
        """
        if property is None:
            raise ArgsIsNull("property")

        _collection = self.statement
        _obj = self.getStatement(
            functionName="Collection.aggregate_count",
            arguments={
                "collection": _collection,
                "property": property
            },
            compute=True
        )
        return _generatePIEObject(self, _obj)

    def aggregate_first(self, property):
        """
        :param property:
        :return:
        """
        if property is None:
            raise ArgsIsNull("property")

        _collection = self.statement
        _obj = self.getStatement(
            functionName="Collection.aggregate_first",
            arguments={
                "collection": _collection,
                "property": property
            },
            compute=True
        )
        return _generatePIEObject(self, _obj)

    def aggregate_array(self, property):
        """
        :param property:
        :return:
        """
        if property is None:
            raise ArgsIsNull("property")

        _collection = self.statement
        _obj = self.getStatement(
            functionName="Collection.aggregate_array",
            arguments={
                "collection": _collection,
                "property": property
            },
            compute=True
        )
        return _generatePIEObject(self, _obj)

    def aggregate_sum(self, property):
        """
        :param property:
        :return:
        """
        if property is None:
            raise ArgsIsNull("property")

        _collection = self.statement
        _obj = self.getStatement(
            functionName="Collection.aggregate_sum",
            arguments={
                "collection": _collection,
                "property": property
            },
            compute=True
        )
        return _generatePIEObject(self, _obj)

    def aggregate_min(self, property):
        """
        :param property:
        :return:
        """
        if property is None:
            raise ArgsIsNull("property")

        _collection = self.statement
        _obj = self.getStatement(
            functionName="Collection.aggregate_min",
            arguments={
                "collection": _collection,
                "property": property
            },
            compute=True
        )
        return _generatePIEObject(self, _obj)

    def aggregate_max(self, property):
        """
        :param property:
        :return:
        """
        if property is None:
            raise ArgsIsNull("property")

        _collection = self.statement
        _obj = self.getStatement(
            functionName="Collection.aggregate_max",
            arguments={
                "collection": _collection,
                "property": property
            },
            compute=True
        )
        return _generatePIEObject(self, _obj)

    def aggregate_mean(self, property):
        """
        :param property:
        :return:
        """
        if property is None:
            raise ArgsIsNull("property")

        _collection = self.statement
        _obj = self.getStatement(
            functionName="Collection.aggregate_mean",
            arguments={
                "collection": _collection,
                "property": property
            },
            compute=True
        )
        return _generatePIEObject(self, _obj)

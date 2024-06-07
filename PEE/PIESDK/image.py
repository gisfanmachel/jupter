# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   image.py
@Time    :   2020/8/2 上午11:10
@Author  :   lsw
@Version :   1.0
@Contact :   shi_weihappy@126.com
@License :   (C)Copyright 2019-2020, lsw
@Desc    :   None
"""
from .object import PIEObject, _generatePIEObject
from .projection import PIEProjection
from .utils.error import ArgsIsNull, ArgsTypeIsWrong
import numpy as np

def _generatePIEFeatureCollection(pre, statement):
    """
    生成 PIEFeatureCollection 的对象
    :param pre:
    :param statement:
    :return:
    """
    from .featureCollection import PIEFeatureCollection
    _object = PIEFeatureCollection()
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

def _generatePIEDictionary(pre, statement):
    """
    生成 PIEDictionary 对象
    :param pre:
    :param statement:
    :return:
    """
    from .dictionary import PIEDictionary
    _object = PIEDictionary()
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
    from .geometry import PIEGeometry
    _object = PIEGeometry()
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
    _object = PIEImage()
    _object.pre = pre
    _object.statement = statement
    return _object

class PIEImage(PIEObject):
    def __init__(self, args=None):
        """
        初始化Image类
        :param args:
        """
        super(PIEImage, self).__init__()
        self.pre = None

        if isinstance(args, (int, float, np.ndarray)):
            self.statement = self.getStatement(
                functionName="Image.constant",
                arguments={"value": args}
            )
        elif isinstance(args, str) and args:
            self.statement = self.getStatement(
                functionName="Image.load",
                arguments={"id": args}
            )
        elif args and type(args).__name__ == self.name():
            self.pre = args.pre
            self.statement = args.statement
        elif args and type(args).__name__ == "PIENumber":
            self.statement = self.getStatement(
                functionName="Image.constant",
                arguments={"value": self.formatValue(args)}
            )
        else:
            self.statement = None

    @staticmethod
    def name():
        return "PIEImage"

    @classmethod
    def load(cls, imageId):
         return PIEImage(imageId)

    @classmethod
    def constant(cls, bandValue):
        return PIEImage(bandValue)

    def pixelArea(self):
        """
        生成一张影像，每一个像素都是当前像素的具体面积
        :return:
        """
        _obj = self.getStatement(
            functionName="Image.pixelArea",
            arguments={}
        )
        return _generatePIEImage(None, _obj)

    def id(self):
        """
        返回影像的ID
        :return:
        """
        _obj = self.getStatement(functionName="Image.id",
                                 arguments={
                                     "input": self.statement
                                 }, compute=True)
        return _generatePIEString(self, _obj)

    def geometry(self, maxError=None, proj=None, geodesics=None):
        """

        :param maxError:
        :param proj:
        :param geodesics:
        :return:
        """
        _input = self.statement
        _obj = self.getStatement(
            functionName="Image.getGeometry",
            arguments={
                "input": _input,
                "maxError": maxError,
                "proj": proj,
                "geodesics": geodesics
            },
            compress="polyline"
        )
        return _generatePIEGeometry(self, _obj)

    def bandNames(self):
        """
        返回影像的波段名称列表
        :return:
        """
        _obj = self.getStatement(functionName="Image.bandNames",
                                 arguments={
                                     "input": self.statement
                                 }, compute=True)
        return _generatePIEList(self, _obj)

    def bandTypes(self):
        _obj = self.getStatement(
            functionName="Image.bandTypes",
            arguments={
                "input": self.statement
            },
            compute=True
        )
        return _generatePIEDictionary(self, _obj)

    def propertyNames(self):
        """
        返回影像的属性名称列表
        :return:
        """
        _obj = self.getStatement(functionName="Image.propertyNames",
                                 arguments={
                                     "input": self.statement
                                 }, compute=True)

        return _generatePIEList(self, _obj)

    def rename(self, names):
        """
        重新命名影像波段名称
        :param names:
        :return:
        """
        if not names:
            raise ArgsIsNull('names')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Image.rename",
            arguments={
                "input": _input,
                "names": names
            }
        )
        return _generatePIEImage(self, _obj)

    def setMaskValue(self, value):
        """
        设置影像的无效值
        :param value:
        :return:
        """
        if value is None:
            raise ArgsIsNull('value')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Image.setMaskValue",
            arguments={
                "input": _input,
                "nodata": value
            }
        )
        return _generatePIEImage(self, _obj)

    def select(self, args):
        """
        选择影像中指定波段名称或者波段名称列表的所有波段
        :param args: 波段名称String或者波段名称列表List
        :return:
        """
        if not args:
            raise ArgsIsNull('args')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Image.select",
            arguments={
                "input": _input,
                "bandSelectors": args
            }
        )
        return _generatePIEImage(self, _obj)

    def addBands(self, srcImage, names=None, overwrite=False):
        """
        影像添加波段
        :param srcImage:
        :param names:
        :param overwrite:
        :return:
        """
        _dst_img = self.statement
        if not srcImage:
            raise ArgsIsNull('srcImage')
        _src_img = self.formatValue(srcImage)
        if not _src_img:
            raise ArgsIsNull("srcImage")
        _obj = self.getStatement(
            functionName="Image.addBands",
            arguments={
                "dstImg": _dst_img,
                "srcImg": _src_img,
                "names": names,
                "overwrite": overwrite
            }
        )
        return _generatePIEImage(self, _obj)

    def add(self, value):
        """
        影像相加
        :param value: 数值或者影像ID或者影像
        :return:
        """
        if not value:
            raise ArgsIsNull('value')
        _image1 = self.statement
        _image2 = PIEImage().constant(value)
        _obj = self.getStatement(
            functionName="Image.add",
            arguments={
                "image1": _image1,
                "image2": self.formatValue(_image2)
            }
        )
        return _generatePIEImage(self, _obj)

    def subtract(self, value):
        """
        影像相减
        :param value:
        :return:
        """
        if not value:
            raise ArgsIsNull('value')
        _image1 = self.statement
        _image2 = PIEImage().constant(value)
        _obj = self.getStatement(
            functionName="Image.subtract",
            arguments={
                "image1": _image1,
                "image2": self.formatValue(_image2)
            }
        )
        return _generatePIEImage(self, _obj)

    def multiply(self, value):
        """
        影像乘以某个常数
        :param value:
        :return:
        """
        if not value:
            raise ArgsIsNull('value')
        _image1 = self.statement
        _image2 = PIEImage().constant(value)
        _obj = self.getStatement(
            functionName="Image.multiply",
            arguments={
                "image1": _image1,
                "image2": self.formatValue(_image2)
            }
        )
        return _generatePIEImage(self, _obj)

    def divide(self, value):
        """
        影像除以某个常数
        :param value:
        :return:
        """
        if not value:
            raise ArgsIsNull('value')
        _image1 = self.statement
        _image2 = PIEImage().constant(value)
        _obj = self.getStatement(
            functionName="Image.divide",
            arguments={
                "image1": _image1,
                "image2": self.formatValue(_image2)
            }
        )
        return _generatePIEImage(self, _obj)

    def power(self, value):
        """

        :param value:
        :return:
        """
        if not isinstance(value, (int, float)):
            raise ArgsTypeIsWrong("value, (int, float)")
        _image1 = self.statement
        _image2 = self.formatValue(PIEImage().constant(value))
        _obj = self.getStatement(
            functionName="Image.power",
            arguments={
                "image1": _image1,
                "image2": _image2
            }
        )
        return _generatePIEImage(self, _obj)

    def exp(self):
        """
        对影像进行以自然常数e为底的指数运算
        :return:
        """
        _image = self.statement
        _obj = self.getStatement(
            functionName="Image.exp",
            arguments={
                "image": _image,
            }
        )
        return _generatePIEImage(self, _obj)

    def expression(self, expression, kwargs):
        """
        影像表达式计算
        :param expression:
        :param kwargs:
        :return:
        """
        if not expression:
            raise ArgsIsNull("expression")
        if not kwargs:
            raise ArgsIsNull("kwargs")
        
        _default_name = "DEFAULT_EXPRESSION_IMAGE"
        _vars = list()
        _vars.append(_default_name)
        _arguments = dict()
        _arguments[_default_name] = self.statement

        for key, value in kwargs.items():
            _vars.append(key)
            if type(value).__name__ != "PIEImage":
                raise ArgsTypeIsWrong()
            _arguments[str(key)] = value.statement

        _obj = self.getStatement(
            arguments=_arguments,
            function=self.getStatement(
                functionName="Image.parseExpression",
                arguments={
                    "expression": expression,
                    "argName": _default_name,
                    "vars": _vars
                }
            )
        )
        return _generatePIEImage(self, _obj)

    def expressionFunction(self, func, map):
        """

        :param func:dict format function
        :param kwargs:dict variable
        :return:
        """

        if not func or not map:
            raise ArgsIsNull('func、map')
        expressionFunc = func.get('expression')
        return self.expression(expressionFunc, map)

    def convolve(self, kernel):
        """
        影像做卷积
        :param kernel:
        :return:
        """
        if not kernel:
            raise ArgsIsNull('kernel')
        _image = self.statement
        _kernel = self.formatValue(kernel)
        _obj = self.getStatement(
            functionName="Image.convolve",
            arguments={
                "image": _image,
                "kernel": _kernel
            }
        )
        return _generatePIEImage(self, _obj)

    def clip(self, geometry):
        """
        按照指定的矢量数据裁剪影像
        :param geometry:
        :return:
        """
        if not geometry:
            raise ArgsIsNull('geometry')
        _input = self.statement
        _geometry = self.formatValue(geometry)
        _obj = self.getStatement(
            functionName="Image.clip",
            arguments={
                "input": _input,
                "geometry": _geometry,
                "evenOdd": True
            }
        )
        return _generatePIEImage(self, _obj)

    def reproject(self, crsProject, crsTransform=None, scale=None):
        """
        影像重投影
        :param crsProject:
        :param crsTransform:
        :param scale:
        :return:
        """
        _image = self.statement
        if isinstance(crsProject, str):
            projection = PIEProjection(crsProject, crsTransform, "")
            _crs = self.formatValue(projection)

        _obj = self.getStatement(
            functionName="Image.reproject",
            arguments={
                "image": _image,
                "crs": _crs,
                "crsTransform": crsTransform,
                "scale": scale,
            }
        )
        return _generatePIEImage(self, _obj)

    def paint(self, featureCollection, color='yellow', width=1):
        """
        绘制矢量数据
        :param featureCollection:
        :param color:
        :param width:
        :return:
        """
        if not featureCollection:
            raise ArgsIsNull('featureCollection')
        _input = self.statement
        _featureCollection = self.formatValue(featureCollection)
        _obj = self.getStatement(
            functionName="Image.paint",
            arguments={
                "input": _input,
                "featureCollection": _featureCollection,
                "color": color,
                "radius": 1,
                "width": width
            }
        )
        return _generatePIEImage(self, _obj)

    def reduce(self, reducer):
        if not reducer:
            raise ArgsIsNull('reducer')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Image.reduce",
            arguments={
                "input": _input,
                "reducer": self.formatValue(reducer)
            }
        )
        return _generatePIEImage(self, _obj)

    def reduceRegion(self, reducer, geometry, scale=None):
        """
        统计指定区域信息
        :param reducer:
        :param geometry:
        :param scale:
        :return:
        """
        _image = self.statement
        _reducer = self.formatValue(reducer) if reducer else None
        _geometry = self.formatValue(geometry) if geometry else None
        _obj = self.getStatement(
            functionName="Image.reduceRegion",
            arguments={
                "image": _image,
                "reducer": _reducer,
                "geometry": _geometry,
                "scale": scale
            },
            compute=True
        )
        return _generatePIEDictionary(self, _obj)

    def sample(self, region, scale, projection, factor, numPixels, seed=None, dropNulls=None, tileScale=None, geometries=None):
        """

        @param region:
        @param scale:
        @param projection:
        @param factor:
        @param numPixels:
        @param seed:
        @param dropNulls:
        @param tileScale:
        @param geometries:
        @return:
        """
        if not region or not scale or not numPixels:
            raise ArgsIsNull("region, scale, projection, factor, numPixels")
        _obj = self.getStatement(functionName="Image.sample",
                                 arguments={"image": self.statement,
                                            "region": self.formatValue(region),
                                            "scale": scale,
                                            "factor": factor,
                                            "projection": projection,
                                            "numPixels": numPixels,
                                            "dropNulls": dropNulls,
                                            "tileScale": tileScale,
                                            "geometries": geometries},
                                 compute=True,
        )
        return _generatePIEObject(self, _obj)

    def sampleRegions(self, collection, properties, scale, projection=None, tileScale=None, geometries=None):
        """

        @param collection:
        @param properties:
        @param scale:
        @param projection:
        @param tileScale:
        @param geometries:
        @return:
        """
        if not collection or not properties or not scale:
            raise ArgsIsNull("collection, properties, scale")
        _obj = self.getStatement(functionName="Image.sampleRegions",
                                 arguments={"image": self.statement,
                                            "collection": self.formatValue(collection),
                                            "properties": properties,
                                            "scale": scale,
                                            "projection": projection,
                                            "tileScale": tileScale,
                                            "geometries": geometries},
                                 compute=True,

        )

        return _generatePIEFeatureCollection(self, _obj)


    def cluster(self, clusterer, outputName="cluster"):
        """

        @param clusterer:
        @param outputName:
        @return:
        """
        if not clusterer:
            raise ArgsIsNull(clusterer)
        _obj = self.getStatement(functionName="Image.cluster",
                                 arguments={"input": self.statement,
                                            "clusterer": self.formatValue(clusterer),
                                            "outputName": outputName},
                                 compute=True,)

        return _generatePIEImage(self, _obj)

    def classify(self, classifier, outputName="classify"):
        """

        @param classifier:
        @param outputName:
        @return:
        """
        if not classifier:
            raise ArgsIsNull("classifier")
        _obj = self.getStatement(functionName="Image.classify",
                                 arguments={"input": self.statement,
                                            "classifier": self.formatValue(classifier),
                                            "outputName": outputName},
                                 compute=True,)

        return _generatePIEImage(self, _obj)


    def eq(self, value):
        """
        生成二值图，所有等于指定值的像素都变为1，其余为0
        :param value:
        :return:
        """
        if value is None:
            raise ArgsIsNull("value")
        _image1 = self.statement
        _image2 = PIEImage(value).statement
        _obj = self.getStatement(
            functionName="Image.eq",
            arguments={
                "image1": _image1,
                "image2": _image2
            }
        )
        return _generatePIEImage(self, _obj)

    def lt(self, value):
        """
        生成二值图，所有小于指定值的像素都变为1，其余为0
        :param value:
        :return:
        """
        if value is None:
            raise ArgsIsNull("value")
        _image1 = self.statement
        _image2 = PIEImage(value).statement
        _obj = self.getStatement(
            functionName="Image.lt",
            arguments={
                "image1": _image1,
                "image2": _image2
            }
        )
        return _generatePIEImage(self, _obj)

    def lte(self, value):
        """
        生成二值图，所有小于等于指定值的像素都变为1，其余为0
        :param value:
        :return:
        """
        if value is None:
            raise ArgsIsNull("value")
        _image1 = self.statement
        _image2 = PIEImage(value).statement
        _obj = self.getStatement(
            functionName="Image.lte",
            arguments={
                "image1": _image1,
                "image2": _image2
            }
        )
        return _generatePIEImage(self, _obj)

    def gt(self, value):
        """
        生成二值图，所有大于指定值的像素都变为1，其余为0
        :param value:
        :return:
        """
        if value is None:
            raise ArgsIsNull("value")
        _image1 = self.statement
        _image2 = PIEImage(value).statement
        _obj = self.getStatement(
            functionName="Image.gt",
            arguments={
                "image1": _image1,
                "image2": _image2
            }
        )
        return _generatePIEImage(self, _obj)

    def gte(self, value):
        """
        生成二值图，所有大于等于指定值的像素都变为1，其余为0
        :param value:
        :return:
        """
        if value is None:
            raise ArgsIsNull("value")
        _image1 = self.statement
        _image2 = PIEImage(value).statement
        _obj = self.getStatement(
            functionName="Image.gte",
            arguments={
                "image1": _image1,
                "image2": _image2
            }
        )
        return _generatePIEImage(self, _obj)

    def And(self, value):
        """
        逻辑与判断
        :param value:
        :return:
        """
        if value is None:
            raise ArgsIsNull("value")
        _image1 = self.statement
        _image2 = PIEImage(value).statement
        _obj = self.getStatement(
            functionName="Image.and",
            arguments={
                "image1": _image1,
                "image2": _image2
            }
        )
        return _generatePIEImage(self, _obj)

    def Or(self, value):
        """
        逻辑或判断
        :param value:
        :return:
        """
        if value is None:
            raise ArgsIsNull("value")
        _image1 = self.statement
        _image2 = PIEImage(value).statement
        _obj = self.getStatement(
            functionName="Image.or",
            arguments={
                "image1": _image1,
                "image2": _image2
            }
        )
        return _generatePIEImage(self, _obj)

    def Not(self):
        """
        逻辑非判断
        :return:
        """
        _image1 = self.statement
        _obj = self.getStatement(
            functionName="Image.not",
            arguments={
                "image1": _image1
            }
        )
        return _generatePIEImage(self, _obj)

    def bitwiseAnd(self, value):
        """
        按位与判断
        :param value:
        :return:
        """
        if value is None:
            raise ArgsIsNull("value")
        _image1 = self.statement
        _image2 = PIEImage(value).statement
        _obj = self.getStatement(
            functionName="Image.bitwiseAnd",
            arguments={
                "image1": _image1,
                "image2": _image2
            }
        )
        return _generatePIEImage(self, _obj)

    def bitwiseOr(self, value):
        """
        按位或判断
        :param value:
        :return:
        """
        if value is None:
            raise ArgsIsNull("value")
        _image1 = self.statement
        _image2 = PIEImage(value).statement
        _obj = self.getStatement(
            functionName="Image.bitwiseOr",
            arguments={
                "image1": _image1,
                "image2": _image2
            }
        )
        return _generatePIEImage(self, _obj)

    def bitwiseXor(self, value):
        """
        按位异或判断
        :param value:
        :return:
        """
        if value is None:
            raise ArgsIsNull("value")
        _image1 = self.statement
        _image2 = PIEImage(value).statement
        _obj = self.getStatement(
            functionName="Image.bitwiseXor",
            arguments={
                "image1": _image1,
                "image2": _image2
            }
        )
        return _generatePIEImage(self, _obj)

    def bitwiseNot(self):
        """
        按位非判断
        :return:
        """
        _image1 = self.statement
        _obj = self.getStatement(
            functionName="Image.bitwiseNot",
            arguments={
                "image1": _image1
            }
        )
        return _generatePIEImage(self, _obj)

    def leftShift(self, value):
        """
        左移
        :param value:
        :return:
        """
        if value is None:
            raise ArgsIsNull("value")
        _image1 = self.statement
        _image2 = PIEImage(value).statement
        _obj = self.getStatement(
            functionName="Image.leftShift",
            arguments={
                "image1": _image1,
                "image2": _image2
            }
        )
        return _generatePIEImage(self, _obj)

    def rightShift(self, value):
        """
        右移
        :param value:
        :return:
        """
        if value is None:
            raise ArgsIsNull("value")
        _image1 = self.statement
        _image2 = PIEImage(value).statement
        _obj = self.getStatement(
            functionName="Image.rightShift",
            arguments={
                "image1": _image1,
                "image2": _image2
            }
        )
        return _generatePIEImage(self, _obj)

    def where(self, condition, value):
        """

        :param condition:
        :param value:
        :return:
        """
        if not condition:
            raise ArgsIsNull("condition, value")
        _image = self.statement
        _image1 = condition.statement
        _image2 = PIEImage(value).statement
        _obj = self.getStatement(
            functionName="Image.where",
            arguments={
                "image": _image,
                "image1": _image1,
                "image2": _image2
            }
        )
        return _generatePIEImage(self, _obj)

    def updateMask(self, value):
        """
        影像做掩膜
        :param value:
        :return:
        """
        if not value:
            raise ArgsIsNull("value")
        _image1 = self.statement
        _image2 = PIEImage(value).statement
        _obj = self.getStatement(
            functionName="Image.updateMask",
            arguments={
                "image1": _image1,
                "image2": _image2
            }
        )
        return _generatePIEImage(self, _obj)

    def toDouble(self):
        """
        影像类型转换为 double 类型
        :return:
        """
        _obj = self.getStatement(functionName="Image.toDouble", arguments={"input": self.statement}) #
        return _generatePIEImage(self, _obj)

    def toFloat(self):
        """
        影像类型转换为 float 类型
        :return:
        """
        _obj = self.getStatement(functionName="Image.toFloat", arguments={"input": self.statement})
        return _generatePIEImage(self, _obj)

    def toUInt32(self):
        """
        影像类型转换为 uint32 类型
        :return:
        """
        _obj = self.getStatement(functionName="Image.toUInt32")
        return _generatePIEImage(self, _obj)

    def toInt32(self):
        """
        影像类型转换为 int32 类型
        :return:
        """
        _obj = self.getStatement(functionName="Image.toInt32")
        return _generatePIEImage(self, _obj)

    def toUInt16(self):
        """
        影像类型转换为 uint16 类型
        :return:
        """
        _obj = self.getStatement(functionName="Image.toUInt16")
        return _generatePIEImage(self, _obj)

    def toInt16(self):
        """
        影像类型转换为 int16 类型
        :return:
        """
        _obj = self.getStatement(functionName="Image.toInt16")
        return _generatePIEImage(self, _obj)

    def toByte(self):
        """
        影像类型转换为 Byte 类型
        :return:
        """
        _obj = self.getStatement(functionName="Image.toByte")
        return _generatePIEImage(self, _obj)


    def toArray(self, key):
        """

        :param key:
        :return:
        """
        if not key:
            raise ArgsIsNull("key")
        _input = self.statement
        _obj = self.getStatement(
            functionName="Image.toArray",
            arguments={
                "input": _input,
                "key": key
            },
        )
        return _generatePIEImage(self, _obj)

    def log(self):
        """
        计算自然对数
        :return:
        """
        _obj = self.getStatement(
            functionName="Image.log",
            arguments={"image1": self.statement}
        )
        return _generatePIEImage(self, _obj)

    def log10(self):
        """
        计算以10为底的对数
        :return:
        """
        _obj = self.getStatement(
            functionName="Image.log10",
            arguments={"image1": self.statement}
        )
        return _generatePIEImage(self, _obj)

    def sin(self):
        """
        计算正弦函数
        :return:
        """
        _obj = self.getStatement(
            functionName="Image.sin",
            arguments={"image1": self.statement}
        )
        return _generatePIEImage(self, _obj)

    def cos(self):
        """
        计算余弦函数
        :return:
        """
        _obj = self.getStatement(
            functionName="Image.cos",
            arguments={"image1": self.statement}
        )
        return _generatePIEImage(self, _obj)

    def tan(self):
        """
        计算正切函数
        :return:
        """
        _obj = self.getStatement(
            functionName="Image.tan",
            arguments={"image1": self.statement}
        )
        return _generatePIEImage(self, _obj)

    def asin(self):
        """
        计算反正弦函数
        :return:
        """
        _obj = self.getStatement(
            functionName="Image.asin",
            arguments={"image1": self.statement}
        )
        return _generatePIEImage(self, _obj)

    def acos(self):
        """
        计算反余弦函数
        :return:
        """
        _obj = self.getStatement(
            functionName="Image.acos",
            arguments={"image1": self.statement}
        )
        return _generatePIEImage(self, _obj)

    def atan(self):
        """
        计算反正切函数
        :return:
        """
        _obj = self.getStatement(
            functionName="Image.atan",
            arguments={"image1": self.statement}
        )
        return _generatePIEImage(self, _obj)

    def sqrt(self):
        """
        计算开方
        :return:
        """
        _obj = self.getStatement(
            functionName="Image.sqrt",
            arguments={"image1": self.statement}
        )
        return _generatePIEImage(self, _obj)

    def abs(self):
        """
        计算绝对值
        :return:
        """
        _obj = self.getStatement(
            functionName="Image.abs",
            arguments={"image1": self.statement}
        )
        return _generatePIEImage(self, _obj)

    def date(self):
        _input = self.statement
        _obj = self.getStatement(
            functionName="Image.date",
            arguments={
                "input": _input
            },
            compute=True
        )
        return _generatePIEString(self, _obj)
    def get(self, key):
        """
        获取指定属性名称的值
        :param key:
        :return:
        """
        _obj = self.getStatement(
            functionName="Image.get",
            arguments={
                "input": self.statement,
                "key": key
            },
            compute=True
        )
        return _generatePIEImage(self, _obj)

    def set(self, key, value):
        """
        增加或者更新属性值
        :param key:
        :param value:
        :return:
        """
        _input = self.statement
        _obj = self.getStatement(
            functionName="Image.set",
            arguments={
                "input": _input,
                "key": key,
                "value": value
            }
        )
        return _generatePIEImage(self, _obj)

    def setMulti(self, properties):
        if properties is None:
            raise ArgsIsNull("properties")
        _input = self.statement
        _obj = self.getStatement(
            functionName="Image.setMulti",
            arguments={
                "input": _input,
                "properties": self.formatValue(properties)
            }
        )
        return _generatePIEImage(self, _obj)
    def getNumber(self, property):
        if property is None:
            raise ArgsIsNull("property")
        _input = self.statement
        _obj = self.getStatement(
            functionName="Image.getNumber",
            arguments={
                "input": _input,
                "property": self.formatValue(property)
            },
            compute=True
        )
        return _generatePIENumber(self, _obj)
    def getString(self, property):
        if property is None:
            raise ArgsIsNull("property")
        _input = self.statement
        _obj = self.getStatement(
            functionName="Image.getString",
            arguments={
                "input": _input,
                "property": self.formatValue(property)
            },
            compute=True
        )
        return _generatePIEString(self, _obj)
    def matrixMultiply(self, right):
        if right is None:
            raise ArgsIsNull("right")
        _obj = self.getStatement(
            functionName="Image.matrixMultiply",
            arguments={
                "left": self.statement,
                "right": self.formatValue(right)
            }
        )
        return _generatePIEImage(self, _obj)

    def arrayProject(self):
        _obj = self.getStatement(
            functionName="Image.arrayProject",
            arguments={
                "image1": self.statement
            }
        )
        return _generatePIEImage(self, _obj)

    def arrayFlatten(self, value):
        if value is None:
            raise ArgsIsNull("value")
        _obj = self.getStatement(
            functionName="Image.arrayFlatten",
            arguments={
                "image1": self.statement,
                "value": value
            }
        )
        return _generatePIEImage(self, _obj)










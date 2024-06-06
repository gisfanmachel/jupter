# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   algo.py
@Time    :   2020/8/6 下午5:19
@Author  :   liuxiaodong
@Version :   1.0
@Contact :   2152550864@qq.com
@License :   (C)Copyright 2019-2020, liuxiaodong
@Desc    :   None
"""
from .object import PIEObject

def _generatePIEAlgo(pre, statement):
    """
    生成PIEAlgo对象
    @param pre:
    @param statement:
    @return:
    """
    _object = PIEAlgo()
    _object.pre = pre
    _object.statement = statement
    return _object

class PIEAlgo(PIEObject):

    def __init__(self, *args):
        super(PIEAlgo, self).__init__()
        self.name = "PIEAlgo"
        self.pre = None
        self.statement = None

    def vectorToRaster(self, collection, description, fileFormat,
                       image, dimensions, field, dataType):
        """

        @param collection:
        @param description:
        @param fileFormat:
        @param image:
        @param dimensions:
        @param field:
        @param dataType:
        @return:
        """
        _obj = self.getStatement(functionName="Algo.vectorToRaster",
                                 arguments={
                                    'collection': self.formatValue(collection),
                                    'description': description,
                                    'fileFormat': fileFormat,
                                    'image': image,
                                    'dimensions': dimensions,
                                    'field': field,
                                    'dataType': dataType,
                                 })

        return _generatePIEAlgo(self, _obj)

    def rasterToVector(self, image, description, assetId, pyramidingPolicy,
                       dimensions, region, scale, crs, crsTransform, maxPixels):
        """

        @param image:
        @param description:
        @param assetId:
        @param pyramidingPolicy:
        @param dimensions:
        @param region:
        @param scale:
        @param crs:
        @param crsTransform:
        @param maxPixels:
        @return:
        """
        _obj = self.getStatement(functionName="Algo.rasterToVector",
                                 arguments={
                                     'image': self.formatValue(image),
                                     'description': description,
                                     'assetId': assetId,
                                     'pyramidingPolicy': pyramidingPolicy,
                                     'dimensions': dimensions,
                                     'region': self.formatValue(region),
                                     'scale': scale,
                                     'crs': crs,
                                     'crsTransform': crsTransform,
                                     'maxPixels': maxPixels,
                                 })
        return _generatePIEAlgo(self, _obj)
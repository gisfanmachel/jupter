# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   common.py
@Time    :   2020/8/6 下午5:19
@Author  :   liuxiaodong
@Version :   1.0
@Contact :   2152550864@qq.com
@License :   (C)Copyright 2019-2020, liuxiaodong
@Desc    :   None
"""
import math
from pie.object import PIEObject
import os

def _generatePIECommon(pre, statement):
    """
    生成PIECommon对象
    @param pre:
    @param statement:
    @return:
    """
    _object = PIECommon()
    _object.pre = pre
    _object.statement = statement
    return _object

class PIECommon(PIEObject):
    def __init__(self):
        super(PIECommon, self).__init__()
        self.pre = None
        self.statement = None

    @staticmethod
    def name():
        return "PIECommon"

    def vectorToRaster(self, collection, description, fileFormat,
                       image, dimensions, field, dataType):
        """
        矢量转栅格数据
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

        return _generatePIECommon(self, _obj)

    def rasterToVector(self, image, description, assetId, pyramidingPolicy,
                       dimensions, region, scale, crs, crsTransform, maxPixels):
        """
        栅格数据转矢量数据
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
        return _generatePIECommon(self, _obj)

    def OTSU(self, input):
        """
        大津法求解阈值
        :param input: 集合对象，标签是像素值，值是像素个数
        :return:
        """
        if isinstance(input, dict):
            return None
        if type(input).__name__ == PIEObject.name():
            input = input.getInfo()

        keys = input.keys()
        values = input.values()

        total0 = 0
        count0 = 0
        for key, value in input.items():
            total0 = total0 + key * value
            count0 = count0 + value

        h0 = total0 / count0
        max = 0
        maxIndex = 0
        size = len(keys)
        for i in range(size - 1):
            total1 = 0
            count1 = 0
            for j in range(i + 1):
                total1 = total1 + keys[j] * values[j]
                count1 = count1 + values[j]
            h1 = total1 * 1.0 / count1
            w1 = count1

            total2 = total0 - total1
            count2 = count0 - count1
            h2 = total2 * 1.0 / count2
            w2 = count2

            temp = math.pow((h0 - h1), 2) * w1 + math.pow((h0 - h2), 2) * w2
            if max < temp:
                max = temp
                maxIndex = keys[i]
        return maxIndex

Common = PIECommon()
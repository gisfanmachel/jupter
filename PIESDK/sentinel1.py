# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   sentinel1.py
@Time    :   2020/8/6 下午5:19
@Author  :   liuxiaodong
@Version :   1.0
@Contact :   2152550864@qq.com
@License :   (C)Copyright 2019-2020, liuxiaodong
@Desc    :   哨兵1处理算法
"""
from .object import PIEObject
from .utils.error import ArgsIsNull
from .image import PIEImage

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

class PIEPlugin_Sentinel1(PIEObject):
    def __init__(self):
        super(PIEPlugin_Sentinel1, self).__init__()
        self.pre = None
        self.statement = None

    @staticmethod
    def name():
        return "PIEPlugin_Sentinel1"

    @staticmethod
    def coastlineExtract(image):
        """
        海岸线监测
        :param image:
        :return:
        """
        if image is None:
            raise ArgsIsNull("image")
        _obj = PIEPlugin_Sentinel1().getStatement(
            functionName="Image.coastlineExtract",
            arguments={
              "image1": PIEPlugin_Sentinel1.formatValue(image)
            }
        )
        return _generatePIEImage(PIEPlugin_Sentinel1, _obj)

    @staticmethod
    def shipDetection(image):
        """
        舰船识别
        :param image:
        :return:
        """
        if image is None:
            raise ArgsIsNull("image")
        _obj = PIEPlugin_Sentinel1().getStatement(
            functionName="Image.shipDetection",
            arguments={
                "image1": PIEPlugin_Sentinel1.formatValue(image)
            }
        )
        return _generatePIEImage(PIEPlugin_Sentinel1, _obj)


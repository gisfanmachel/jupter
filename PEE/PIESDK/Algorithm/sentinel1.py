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
from pie.object import PIEObject
from pie.utils.error import ArgsIsNull

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

class PIESentinel1(PIEObject):
    def __init__(self):
        super(PIESentinel1, self).__init__()
        self.pre = None
        self.statement = None

    @staticmethod
    def name():
        return "PIESentinel1"

    def coastlineExtract(self, image):
        """
        海岸线监测
        :param image:
        :return:
        """
        if image is None:
            raise ArgsIsNull("image")

        _obj = self.getStatement(
            functionName="Image.coastlineExtract",
            arguments={
              "image1": self.formatValue(image)
            }
        )
        return _generatePIEImage(self, _obj)

    def shipDetection(self, image):
        """
        舰船识别
        :param image:
        :return:
        """
        if image is None:
            raise ArgsIsNull("image")

        _obj = self.getStatement(
            functionName="Image.shipDetection",
            arguments={
                "image1": self.formatValue(image)
            }
        )
        return _generatePIEImage(self, _obj)

Sentinel1 = PIESentinel1()
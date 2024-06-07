# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   gf3.py
@Time    :   2020/8/6 下午5:19
@Author  :   liuxiaodong
@Version :   1.0
@Contact :   2152550864@qq.com
@License :   (C)Copyright 2019-2020, liuxiaodong
@Desc    :   None
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

class PIEGF3(PIEObject):
    def __init__(self):
        super(PIEGF3, self).__init__()
        self.pre = None
        self.statement = None

    @staticmethod
    def name():
        return "PIEGF3"

    def coastlineExtract(self, input):
        """
        海岸线识别
        :param input:
        :return:
        """
        if input is None:
            raise ArgsIsNull("input")
        _obj = self.getStatement(
            functionName="Image.coastlineExtract",
            arguments={
                "image1": self.formatValue(input)
            }
        )
        return _generatePIEImage(self, _obj)

    def shipDetection(self, input):
        """
        船体识别
        :param input:
        :return:
        """
        if input is None:
            raise ArgsIsNull("input")
        _obj = self.getStatement(
            functionName="Image.shipDetection",
            arguments={
                "image1": self.formatValue(input)
            }
        )
        return _generatePIEImage(self, _obj)

GF3 = PIEGF3()

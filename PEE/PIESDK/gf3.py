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

class PIEPlugin_GF3(PIEObject):
    def __init__(self):
        super(PIEPlugin_GF3, self).__init__()
        self.pre = None
        self.statement = None

    @staticmethod
    def name():
        return "PIEPlugin_GF3"

    @staticmethod
    def coastlineExtract(input):

        _obj = PIEPlugin_GF3().getStatement(functionName="Image.coastlineExtract",
                                            arguments={
                                                "image1": PIEPlugin_GF3.formatValue(input)
                                            })

        return _generatePIEImage(PIEPlugin_GF3, _obj)

    @staticmethod
    def shipDetection(input):
        _obj = PIEPlugin_GF3().getStatement(functionName="Image.shipDetection",
                                            arguments={
                                                "image1": PIEPlugin_GF3.formatValue(input)
                                            })

        return _generatePIEImage(PIEPlugin_GF3, _obj)

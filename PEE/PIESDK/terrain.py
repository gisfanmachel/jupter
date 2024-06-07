# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   terrain.py
@Time    :   2020/8/6 下午1:27
@Author  :   lsw
@Version :   1.0
@Contact :   shi_weihappy@126.com
@License :   (C)Copyright 2019-2020, lsw
@Desc    :   None
"""

from .object import PIEObject
from .image import PIEImage
from .utils.error import ArgsIsNull

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

class PIETerrain(PIEObject):
    def __init__(self, args=None):
        """
        初始化高程类Terrain
        :param args:
        """
        super(PIETerrain, self).__init__()
        self.pre = None
        if not args:
            self.statement = None
        else:
            if isinstance(args, str):
                self.statement = self.getStatement(
                    arguments= {"id": args},
                    functionName="Image.load"
                )
            elif type(args).__name__ == self.name():
                self.pre = args.pre
                self.statement = args.statement
            else:
                self.statement = None

    @staticmethod
    def name():
        return "PIETerrain"

    def slope(self):
        """
        计算坡度
        :return:
        """
        _obj = self.getStatement(functionName="Terrain.slope")
        return _generatePIEImage(self, _obj)

    def hillShade(self, image, altitude=45, azimuth=315, zScaleFactor=1):
        """
        计算山体阴影
        :param image:
        :param altitude:
        :param azimuth:
        :param zScaleFactor:
        :return:
        """
        if image is None:
            raise ArgsIsNull("image")
        _obj = self.getStatement(
            functionName="Terrain.hillShade",
            arguments={
                "input": self.formatValue(image),
                "altitude": self.formatValue(altitude),
                "azimuth": self.formatValue(azimuth),
                "zScaleFactor": self.formatValue(zScaleFactor)
            }
        )
        return _generatePIEImage(self, _obj)

    def aspect(self):
        """
        计算坡向
        :return:
        """
        _obj = self.getStatement(
            functionName="Terrain.aspect",
            arguments={
             "input": self.statement
            }
        )

        return _generatePIEImage(self, _obj)
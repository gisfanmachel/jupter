# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   kernel.py
@Time    :   2020/8/6 下午3:31
@Author  :   lsw
@Version :   1.0
@Contact :   shi_weihappy@126.com
@License :   (C)Copyright 2019-2020, lsw
@Desc    :   None
"""

from pie.object import PIEObject
from pie.utils.error import ArgsIsNull

def _generatePIEKernel(pre, statement):
    """
    生成 PIEKernel 的对象
    :param pre:
    :param statement:
    :return:
    """
    _object = PIEKernel()
    _object.pre = pre
    _object.statement = statement
    return _object

class PIEKernel(PIEObject):
    def __init__(self, args=None):
        super(PIEKernel, self).__init__()
        if type(args).__name__ == self.name() \
            or type(args).__name__ == PIEObject.name() :
            self.pre = args.pre
            self.statement = args.statement
        else:
            self.pre = None
            self.statement = None

    @staticmethod
    def name():
        return "PIEKernel"

    def fixed(self, width, height, weights, x=-1, y=-1, normalize=False):
        """

        @param width:
        @param height:
        @param weights:
        @param x:
        @param y:
        @param normalize:
        @return:
        """
        _input = self.statement
        width = width if width else -1
        height = height if height else -1
        x = x if x else -1
        y = y if y else -1
        normalize = normalize if normalize else False
        _obj = self.getStatement(functionName="Kernel.fixed",
                                 arguments={
                                     "input": _input,
                                     "width": self.formatValue(width),
                                     "height": self.formatValue(height),
                                     "weights": self.formatValue(weights),
                                     "x": self.formatValue(x),
                                     "y": self.formatValue(y),
                                     "normalize": self.formatValue(normalize),
                                 })
        return _generatePIEKernel(self, _obj)


    def statsNeighbour(self, magnitude, normalize):
        """

        @param magnitude:
        @param normalize:
        @return:
        """
        _input = self.statement
        _obj = self.getStatement(functionName="Kernel.statsNeighbour",
                                 arguments={"input": _input,
                                            "magnitude": self.formatValue(magnitude),
                                            "normalize": self.formatValue(normalize)})
        return _generatePIEKernel(self, _obj)


    def sobel(self, magnitude, normalize):
        """

        :param magnitude:
        :param normalize:
        :return:
        """
        _input = self.statement
        _obj = self.getStatement(
            functionName="Kernel.sobel",
            arguments={
                "input": _input,
                "magnitude": self.formatValue(magnitude),
                "normalize": self.formatValue(normalize)
            }
        )
        return _generatePIEKernel(self, _obj)

    def lowPass(self):
        """
        :return:
        """
        _obj = self.getStatement(functionName="Kernel.lowPass",
                                 arguments={"input": self.statement})

        return _generatePIEKernel(self, _obj)

    def summary(self):
        """
        :return:
        """
        _obj = self.getStatement(functionName="Kernel.summary",
                                 arguments={
                                     "input": self.statement
                                 })
        return _generatePIEKernel(self, _obj)

    def horizontal(self):
        """
        :return:
        """
        _obj = self.getStatement(functionName="Kernel.horizontal",
                                 arguments={"input": self.statement})
        return _generatePIEKernel(self, _obj)

    def vertical(self):
        """
        :return:
        """
        _obj = self.getStatement(functionName="Kernel.vertical",
                                 arguments={"input": self.statement})

        return _generatePIEKernel(self, _obj)

    def laplacian(self):
        """
        :return:
        """
        _obj = self.getStatement(functionName="Kernel.laplacian",
                                 arguments={"input": self.statement})
        return _generatePIEKernel(self, _obj)

    def median(self, kSize):
        if kSize is None:
            raise ArgsIsNull('kSize')
        _obj = self.getStatement(
            functionName="Kernel.median",
            arguments={
                "input": self.statement,
                "kSize": self.formatValue(kSize)
            }
        )
        return _generatePIEKernel(self, _obj)

    def mean(self, kSize):
        if kSize is None:
            raise ArgsIsNull('kSize')
        _obj = self.getStatement(
            functionName="Kernel.mean",
            arguments={
                "input": self.statement,
                "kSize": self.formatValue(kSize)
            }
        )
        return _generatePIEKernel(self, _obj)

    def h8FM(self, imagePF, imageValid, imageB7, imageB13, imageCha, imageB4):
        if any((imagePF, imageValid, imageB7, imageB13, imageCha, imageB4)) is None:
            raise ArgsIsNull()
        _obj = self.getStatement(
            functionName="Kernel.h8FM",
            arguments={
                "input": self.statement,
                "imagePF": self.formatValue(imagePF),
                "imageValid": self.formatValue(imageValid),
                "imageB7": self.formatValue(imageB7),
                "imageB13": self.formatValue(imageB13),
                "imageCha": self.formatValue(imageCha),
                "imageB4": self.formatValue(imageB4)
            }
        )
        return _generatePIEKernel(self, _obj)



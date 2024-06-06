# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   classifierDT.py
@Time    :   2020/8/6 下午5:19
@Author  :   liuxiaodong
@Version :   1.0
@Contact :   2152550864@qq.com
@License :   (C)Copyright 2019-2020, liuxiaodong
@Desc    :   None
"""

from pie.object import PIEObject


def _generatePIEConfusionMatrix(pre, statement, type=None, array=None):
    """
    生成PIEConfusionMatrix对象
    :param pre:
    :param statement:
    :param type:
    :param array:
    :return:
    """
    from pie.confusionMatrix import PIEConfusionMatrix
    _object = PIEConfusionMatrix(type, array)
    _object.pre = pre
    _object.statement = statement
    return _object


def _generatePIEClassifierKNN(pre, statement):
    """
    生成 PIEClassifierKNN 对象
    @param pre:
    @param statement:
    @return:
    """
    _object = PIEClassifierKNN()
    _object.pre = pre
    _object.statement = statement
    return _object


def _generatePIEClassifierDT(pre, statement):
    from pie.Classifier.classifierDT import PIEClassifierDT
    dictionary = PIEClassifierDT()
    dictionary.pre = pre
    dictionary.statement = statement


class PIEClassifierKNN(PIEObject):
    def __init__(self, options=None):
        super(PIEClassifierKNN, self).__init__()
        self.pre = None
        self.statement = self.getStatement(
            functionName="Classifier.knnConstructors",
            arguments={
                "options":self.formatValue(options)
            }
        )

    @staticmethod
    def name():
        return "PIEClassifierKNN"

    def train(self, features, classProperty, inputProperties, subsampling=None, subsamplingSeed=None):
        """
        训练分类器
        @param features:
        @param classProperty:
        @param inputProperties:
        @param subsampling:
        @param subsamplingSeed:
        @return:
        """
        _input = self.statement
        _obj = self.getStatement(
            functionName="Classifier.train",
            arguments={
                 "input": _input,
                 "features": self.formatValue(features),
                 "classProperty": self.formatValue(classProperty),
                 "inputProperties": self.formatValue(inputProperties),
                 "subsampling": self.formatValue(subsampling),
                 "subsamplingSeed": self.formatValue(subsamplingSeed)
            }
        )
        return _generatePIEClassifierKNN(self, _obj)

    def confusionMatrix(self):
        """
        计算混淆矩阵
        @return:
        """
        _input = self.statement
        _obj = self.getStatement(
            functionName="Classifier.confusionMatrix",
            arguments={
                "input": _input
            }
        )
        return _generatePIEConfusionMatrix(self, _obj)

    def explain(self):
        _input = self.statement
        _obj = self.getStatement(
            functionName="Classifier.explain",
            arguments={
                "input": _input
            }
        )
        return _generatePIEClassifierDT(self, _obj)

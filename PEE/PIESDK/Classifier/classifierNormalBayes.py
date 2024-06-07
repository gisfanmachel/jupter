# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   classifierNormalBayes.py
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


def _generatePIEClassifierNormalBayes(pre, statement):
    """
    生成 PIEClassifierNormalBayes 对象
    :param pre:
    :param statement:
    :return:
    """
    _object = PIEClassifierNormalBayes()
    _object.pre = pre
    _object.statement = statement
    return _object


def _generatePIEClassifierDT(pre, statement):
    from pie.Classifier.classifierDT import PIEClassifierDT
    dictionary = PIEClassifierDT()
    dictionary.pre = pre
    dictionary.statement = statement


class PIEClassifierNormalBayes(PIEObject):
    def __init__(self, options=None):
        super(PIEClassifierNormalBayes).__init__()
        self.pre = None
        self.statement = self.getStatement(
            functionName="Classifier.normalBayesConstructors",
            arguments={
                "options":self.formatValue(options)
            },
        )

    @staticmethod
    def name():
        return "PIEClassifierNormalBayes"

    def train(self, features, classProperty, inputProperties, subsampling=None, subsamplingSeed=None):
        """
        Start train NormalBayes model
        @param features:
        @param classProperty:
        @param inputProperties:
        @param subsampling:
        @param subsamplingSeed:
        @return:
        """
        _input =  self.statement
        _obj = self.getStatement(
            functionName="Classifier.train",
            arguments={"input": _input,
                       "features": self.formatValue(features),
                       "classProperty": self.formatValue(classProperty),
                       "inputProperties": self.formatValue(inputProperties),
                       "subsampling": self.formatValue(subsampling),
                       "subsamplingSeed": self.formatValue(subsamplingSeed)}
        )
        return _generatePIEClassifierNormalBayes(self, _obj)

    def confusionMatrix(self):
        """
        计算混淆矩阵
        :return:
        """
        _obj = self.getStatement(
            functionName="Classifier.confusionMatrix",
            arguments={"input": self.statement}
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


# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   classifierSVM.py
@Time    :   2020/8/6 下午5:19
@Author  :   liuxiaodong
@Version :   1.0
@Contact :   2152550864@qq.com
@License :   (C)Copyright 2019-2020, liuxiaodong
@Desc    :   None
"""
from .object import PIEObject

def _generatePIEConfusionMatrix(pre, statement, type=None, array=None):
    """
    生成PIEConfusionMatrix对象
    :param pre:
    :param statement:
    :param type:
    :param array:
    :return:
    """
    from .confusionMatrix1 import PIEConfusionMatrix
    _object = PIEConfusionMatrix(type, array)
    _object.pre = pre
    _object.statement = statement
    return _object

def _generatePIEClassifierSVM(pre, statement):
    """
    生成 PIEClassifierSVM 对象
    :param pre:
    :param statement:
    :return:
    """
    _object = PIEClassifierSVM()
    _object.pre = pre
    _object.statement = statement
    return _object

class PIEClassifierSVM(PIEObject):
    def __init__(self):
        super(PIEClassifierSVM).__init__()
        self.pre = None
        self.statement = self.getStatement(
            functionName="Classifier.svmConstructors",
            arguments={},
        )

    def train(self, features, classProperty, inputProperties, subsampling=None, subsamplingSeed=None):
        """
        Start train SVM model
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
            arguments={"input": _input,
                       "features": self.formatValue(features),
                       "classProperty": self.formatValue(classProperty),
                       "inputProperties": self.formatValue(inputProperties),
                       "subsampling": self.formatValue(subsampling),
                       "subsamplingSeed": self.formatValue(subsamplingSeed)}
        )
        return _generatePIEClassifierSVM(self, _obj)

    def confusionMatrix(self):
        """

        :return:
        """
        _obj = self.getStatement(functionName="Classifier.confusionMatrix",
                                 arguments={"input": self.statement})
        return _generatePIEConfusionMatrix(self, _obj)
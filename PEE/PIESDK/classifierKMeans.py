# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   classifierKMean.py
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

def _generatePIEClustererKMeans(pre, statement, nClusters):
    """
    生成 PIEClustererKMeans 对象
    :param pre:
    :param statement:
    :return:
    """
    _object = PIEClustererKMeans(nClusters)
    _object.pre = pre
    _object.statement = statement
    return _object

class PIEClustererKMeans(PIEObject):
    def __init__(self, nClusters):
        super(PIEClustererKMeans, self).__init__()
        self.pre = None
        self.nClusters = nClusters
        self.statement = self.getStatement(
            functionName="Clusterer.kMeansConstructors",
            arguments={"nClusters": self.formatValue(nClusters)
                       })

    def train(self, features):
        """
        Start train KMeans model
        @param features:
        @return:
        """
        _input = self.statement
        _obj = self.getStatement(functionName="Clusterer.kMeansTrain",
                                 arguments={
                                     "input": _input,
                                     "features": self.formatValue(features)
                                 })

        return _generatePIEClustererKMeans(self, _obj)

    def confusionMatrix(self):

        _obj = self.getStatement(functionName="Classifier.confusionMatrix",
                                 arguments={"input": self.statement})
        return _generatePIEConfusionMatrix(self, _obj)
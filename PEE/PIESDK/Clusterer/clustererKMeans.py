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

from pie.object import PIEObject

def _generatePIEObject(pre, statement):
    """
    生成 PIEObject 对象
    :param pre:
    :param statement:
    :return:
    """
    _object = PIEObject()
    _object.pre = pre
    _object.statement = statement
    return _object

class PIEClustererKMeans(PIEObject):
    def __init__(self, nClusters=None):
        super(PIEClustererKMeans, self).__init__()
        self.pre = None
        self.nClusters = nClusters
        self.statement = self.getStatement(
            functionName="Clusterer.kMeansConstructors",
            arguments={
                "nClusters": self.formatValue(nClusters)
            }
        )

    @staticmethod
    def name():
        return "PIEClustererKMeans"

    def train(self, features):
        """
        Start train KMeans model
        @param features:
        @return:
        """
        _input = self.statement
        _obj = self.getStatement(
            functionName="Clusterer.kMeansTrain",
            arguments={
                 "input": _input,
                 "features": self.formatValue(features)
            }
        )
        return _generatePIEObject(self, _obj)

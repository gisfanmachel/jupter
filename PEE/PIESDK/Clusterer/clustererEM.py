# -*- coding: utf-8 -*-
# author:liuxiaodong 
# contact: 2152550864@qq.com
# datetime:2021/5/7 9:41
# software: PyCharm

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

class PIEClustererEM(PIEObject):
    def __init__(self, nClusters):
        super(PIEClustererEM, self).__init__()
        self.name = "PIEClustererEM"
        self.pre = None
        _obj = self.getStatement(
            functionName="Clusterer.emConstructors",
            arguments={
                "nClusters": self.formatValue(nClusters)
            }
        )
        self.nClusters = nClusters
        self.statement = _obj

    @staticmethod
    def name():
        return "PIEClustererEM"

    def train(self, features):
        """
        构造训练器
        @param features:
        @return:
        """
        _input = self.statement
        _obj = self.getStatement(
            functionName="Clusterer.emTrain",
            arguments={
                 "input": _input,
                 "features": self.formatValue(features),
            }
        )
        return _generatePIEObject(self, _obj)

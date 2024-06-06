# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   confusionMatrix.py
@Time    :   2020/8/6 下午5:19
@Author  :   liuxiaodong
@Version :   1.0
@Contact :   2152550864@qq.com
@License :   (C)Copyright 2019-2020, liuxiaodong
@Desc    :   None
"""
from .object import PIEObject

def _generatePIENumber(pre, statement):
    """
    生成 PIENumber 对象
    :param pre:
    :param statement:
    :return:
    """
    from .number import PIENumber
    _object = PIENumber()
    _object.pre = pre
    _object.statement = statement
    return _object

class PIEConfusionMatrix(PIEObject):
    def __init__(self, type=None, array=None):
        super(PIEConfusionMatrix, self).__init__()
        self.name = "PIEConfusionMatrix"
        self.pre = None
        self.statement = self.getStatement(
            functionName="ConfusionMatrix.constructors",
            arguments={
                'type': type,
                'array': array,
            }
        )

    def acc(self):
        """
        计算混淆矩阵的精度
        :return:
        """
        _obj = self.getStatement(functionName="ConfusionMatrix.acc",
                                 arguments={
                                     "input": self.statement})

        return _generatePIENumber(self, _obj)

    def kappa(self):
        """
        计算混淆矩阵的kappa系数
        :return:
        """
        _obj = self.getStatement(functionName="ConfusionMatrix.kappa",
                                 arguments={
                                     "input": self.statement})

        return _generatePIENumber(self, _obj)

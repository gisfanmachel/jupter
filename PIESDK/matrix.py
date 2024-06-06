# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   matrix.py
@Time    :   2020/10/10 上午10:15
@Author  :   lsw
@Version :   1.0
@Contact :   shi_weihappy@126.com
@License :   (C)Copyright 2019-2020, lsw
@Desc    :   None
"""

from pie.object import PIEObject

def _generatePIEMatrix(pre, statement):
    """
    生成 PIEMatrix 对象
    :param pre:
    :param statement:
    :return:
    """
    _object = PIEMatrix()
    _object.pre = pre
    _object.statement = statement
    return _object

class PIEMatrix(PIEObject):
    def __init__(self, matrixArray=None, matrixRow=None, matrixColumn=None):
        super(PIEMatrix, self).__init__()
        if matrixArray is not None:
            self.pre = matrixArray
            self.statement = self.getStatement(
                functionName="Matrix.constructors",
                arguments={
                    "array": self.formatValue(matrixArray),
                    "row": matrixRow,
                    "column": matrixColumn
                }
            )
        else:
            self.pre = None
            self.statement = self.getStatement(functionName="Matrix.constructors",
                                               arguments={"array": None,
                                                          "row": matrixRow,
                                                          "column": matrixColumn
                                                          }
            )

    @staticmethod
    def name():
        return "PIEMatrix"

    def sdet(self):
        """

        :return:
        """
        _obj = self.getStatement(
            functionName="Matrix.sdet",
            arguments={"input": self.statement}
        )
        return _generatePIEMatrix(self, _obj)

    def multiply(self, input):
        """

        :param input:
        :return:
        """
        _matrix1 = self.statement
        _obj = self.getStatement(
            functionName="Matrix.multiply",
            arguments={
                "matrix1": _matrix1,
                "matrix2": self.formatValue(input)
            }
        )
        return _generatePIEMatrix(self, _obj)

    def transpose(self):
        """

        :return:
        """
        _obj = self.getStatement(
            functionName="Matrix.transpose",
            arguments={"input": self.statement}
        )
        return _generatePIEMatrix(self, _obj)

    def inverse(self):
        """

        :return:
        """
        _obj = self.getStatement(
            functionName="Matrix.inverse",
            arguments={"input": self.statement}
        )
        return _generatePIEMatrix(self, _obj)
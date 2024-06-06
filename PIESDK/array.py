# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   array.py
@Time    :   2020/10/9 下午3:19
@Author  :   lsw
@Version :   1.0
@Contact :   shi_weihappy@126.com
@License :   (C)Copyright 2019-2020, lsw
@Desc    :   None
"""
from pie.object import PIEObject, _generatePIEObject
from pie.utils.error import ArgsIsNull

def _generatePIENumber(pre, statement):
    """
    生成 PIENumber 对象
    :param pre:
    :param statement:
    :return:
    """
    from pie.number import PIENumber
    _object = PIENumber()
    _object.pre = pre
    _object.statement = statement
    return _object

def _generatePIEDictionary(pre, statement):
    """
    生成 PIEDictionary 对象
    :param pre:
    :param statement:
    :return:
    """
    from pie.dictionary import PIEDictionary
    _object = PIEDictionary()
    _object.pre = pre
    _object.statement = statement
    return _object

def _generatePIEArray(pre, statement):
    """
    生成 PIEArray 对象
    :param pre:
    :param statement:
    :return:
    """
    _object = PIEArray()
    _object.pre = pre
    _object.statement = statement
    return _object

class PIEArray(PIEObject):
    def __init__(self,args=None, pixelType=7, row=0, col=1, deepth=0):
        super(PIEArray, self).__init__()
        if args is None:
            self.pre = None
            self.statement = None
        else:
            if type(args).__name__ == self.name() \
                    or type(args).__name__ == PIEObject.name():
                self.pre = args.pre
                self.statement = args.statement
            else:
                self.pre = None
                self.statement = self.getStatement(
                    functionName="Array.constructors",
                    arguments={"args": self.formatValue(args),
                               "pixelType":pixelType,
                               "row": row,
                               "col": col,
                               "deepth": deepth}
                )

    @staticmethod
    def name():
        return "PIEArray"

    def add(self, value):
        """
        数组相加
        :param value:
        :return:
        """
        if value is None:
            raise ArgsIsNull('value')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Array.add",
            arguments={
                "input": _input,
                "value": self.formatValue(value)
            }
        )
        return _generatePIEArray(self, _obj)

    def reduce(self, reducer, axes):
        """
        统计计算
        :param reducer:
        :param axes:
        :return:
        """
        if reducer is None or axes is None:
            raise ArgsIsNull('reduce,axes')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Array.reduce",
            arguments={
                "input": _input,
                "reducer": self.formatValue(reducer),
                "axes":self.formatValue(axes)
            }
        )
        return _generatePIEObject(self, _obj)

    def get(self, index):
        """
        返回指定索引的数据
        :param index:
        :return:
        """
        if index is None:
            raise ArgsIsNull('index')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Array.get",
            arguments={
                "input": _input,
                "position": self.formatValue(index)
            }
        )
        return _generatePIEObject(self, _obj)

    def length(self):
        """
        返回数组长度
        :return:
        """
        _obj = self.getStatement(
            functionName="Array.length",
            compute=True
        )
        return _generatePIENumber(self, _obj)

    def matrixMultiply(self, right):
        """
        数组计算
        :param right:
        :return:
        """
        if right is None:
            raise ArgsIsNull('right')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Array.matrixMultiply",
            arguments={
                "left": _input,
                "right": self.formatValue(right)
            },
            compute=True
        )
        return _generatePIEArray(self, _obj)

    def matrixQRDecomposition(self):
        """

        :return:
        """
        _input = self.statement
        _obj = self.getStatement(
            functionName="Array.matrixQRDecomposition",
            arguments={
                "input": _input,
            }
        )
        return _generatePIEDictionary(self, _obj)

    def bitsToArray(self, input):
        """

        :param input:
        :return:
        """
        if input is None:
            raise ArgsIsNull('input')
        _obj = self.getStatement(
            functionName="Array.bitsToArray",
            arguments={
                "input":self.formatValue(input),
            }
        )
        return _generatePIEArray(self, _obj)

    def cat(self, arrays, axis=0):
        """

        :param arrays:
        :param axis:
        :return:
        """
        if arrays is None:
            raise ArgsIsNull('arrays')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Array.cat",
            arguments={
                "input":_input,
                "arrays":self.formatValue(arrays),
                "axis":self.formatValue(axis)
            },
        )
        return _generatePIEArray(self, _obj)

    def abs(self):
        """

        :return:
        """
        _input = self.statement
        _obj = self.getStatement(
            functionName="Array.abs",
            arguments={
                "input":_input
            },
        )
        return _generatePIEArray(self, _obj)

    def accum(self, axis, reducer=None):
        """

        :param axis:
        :param reducer:
        :return:
        """
        if axis is None:
            raise ArgsIsNull('axis')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Array.accum",
            arguments={
                "input":_input,
                "axis":self.formatValue(axis),
                "reducer":self.formatValue(reducer)
            }
        )
        return _generatePIEArray(self, _obj)

    def slice(self, axis=0, start=0, end=None, step=1):
        """

        :param axis:
        :param start:
        :param end:
        :param step:
        :return:
        """
        if axis is None:
            raise ArgsIsNull('axis')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Array.slice",
            arguments={
                "input":_input,
                "axis":self.formatValue(axis),
                "start":self.formatValue(start),
                "end":self.formatValue(end),
                "step":self.formatValue(step)
            },
        )
        return _generatePIEArray(self, _obj)

    def transpose(self, axis1=0, axis2=1):
        if axis1 is None or axis2 is None:
            raise  ArgsIsNull("axis1,axis2")
        _input = self.statement
        _obj = self.getStatement(
            functionName="Array.transpose",
            arguments={
                "input":_input,
                "axis1":self.formatValue(axis1),
                "axis2":self.formatValue(axis2)
            },
        )
        return _generatePIEArray(self, _obj)

    def subtract(self, right):
        """

        :param right:
        :return:
        """
        if right is None:
            raise ArgsIsNull('right')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Array.subtract",
            arguments={
                "input":_input,
                "right":self.formatValue(right)
            }
        )
        return _generatePIEArray(self, _obj)

    def multiply(self, right):
        """

        :param right:
        :return:
        """
        if right is None:
            raise ArgsIsNull('right')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Array.multiply",
            arguments={
                "input": _input,
                "right": self.formatValue(right)
            }
        )
        return _generatePIEArray(self, _obj)

    def divide(self, right):
        """

        :param right:
        :return:
        """
        if right is None:
            raise ArgsIsNull('right')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Array.divide",
            arguments={
                "input": _input,
                "right": self.formatValue(right)
            }
        )
        return _generatePIEArray(self, _obj)

    def And(self, right):
        """

        :param right:
        :return:
        """
        if right is None:
            raise ArgsIsNull('right')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Array.and",
            arguments={
                "input": _input,
                "right": self.formatValue(right)
            }
        )
        return _generatePIEArray(self, _obj)

    def Or(self, right):
        """

        :param right:
        :return:
        """
        if right is None:
            raise ArgsIsNull('right')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Array.or",
            arguments={
                "input": _input,
                "right": self.formatValue(right)
            }
        )
        return _generatePIEArray(self, _obj)

    def Not(self):
        """

        :return:
        """
        _input = self.statement
        _obj = self.getStatement(
            functionName="Array.not",
            arguments={
                "input": _input
            }
        )
        return _generatePIEArray(self, _obj)

    def bitwiseAnd(self, right):
        """

        :param right:
        :return:
        """
        if right is None:
            raise ArgsIsNull('right')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Array.bitwiseAnd",
            arguments={
                "input": _input,
                "right": self.formatValue(right)
            }
        )
        return _generatePIEArray(self, _obj)

    def bitwiseNot(self):
        """

        :return:
        """
        _input = self.statement
        _obj = self.getStatement(
            functionName="Array.bitwiseNot",
            arguments={
                "input": _input
            }
        )
        return _generatePIEArray(self, _obj)

    def bitwiseOr(self, right):
        """

        :param right:
        :return:
        """
        if right is None:
            raise ArgsIsNull('right')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Array.bitwiseOr",
            arguments={
                "input": _input,
                "right": self.formatValue(right)
            }
        )
        return _generatePIEArray(self, _obj)

    def bitwiseXor(self, right):
        """

        :param right:
        :return:
        """
        if right is None:
            raise ArgsIsNull('right')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Array.bitwiseXor",
            arguments={
                "input": _input,
                "right": self.formatValue(right)
            }
        )
        return _generatePIEArray(self, _obj)

    def matrixDeterminant(self):
        """

        :return:
        """
        _input = self.statement
        _obj = self.getStatement(
            functionName="Array.matrixDeterminant",
            arguments={
                "input": _input
            }
        )
        return _generatePIEArray(self, _obj)

    def matrixDiagonal(self):
        """

        :return:
        """
        _input = self.statement
        _obj = self.getStatement(
            functionName="Array.matrixDiagonal",
            arguments={
                "input": _input
            }
        )
        return _generatePIEArray(self, _obj)

    def matrixToDiag(self):
        """

        :return:
        """
        _input = self.statement
        _obj = self.getStatement(
            functionName="Array.matrixToDiag",
            arguments={
                "input": _input
            }
        )
        return _generatePIEArray(self, _obj)

    def matrixTrace(self):
        """

        :return:
        """
        _input = self.statement
        _obj = self.getStatement(
            functionName="Array.matrixTrace",
            arguments={
                "input": _input
            }
        )
        return _generatePIEArray(self, _obj)

    def matrixTranspose(self):
        """

        :return:
        """
        _input = self.statement
        _obj = self.getStatement(
            functionName="Array.matrixTranspose",
            arguments={
                "input": _input
            }
        )
        return _generatePIEArray(self, _obj)

    def matrixInverse(self):
        """

        :return:
        """
        _input = self.statement
        _obj = self.getStatement(
            functionName="Array.matrixInverse",
            arguments={
                "input": _input
            }
        )
        return _generatePIEArray(self, _obj)

    def matrixFnorm(self):
        """

        :return:
        """
        _input = self.statement
        _obj = self.getStatement(
            functionName="Array.matrixFnorm",
            arguments={
                "input": _input
            }
        )
        return _generatePIEArray(self, _obj)

    def matrixPseudoInverse(self):
        """

        :return:
        """
        _input = self.statement
        _obj = self.getStatement(
            functionName="Array.matrixPseudoInverse",
            arguments={
                "input": _input
            }
        )
        return _generatePIEArray(self, _obj)

    def matrixCholeskyDecomposition(self):
        """

        :return:
        """
        _input = self.statement
        _obj = self.getStatement(
            functionName="Array.matrixCholeskyDecomposition",
            arguments={
                "input": _input
            }
        )
        return _generatePIEArray(self, _obj)

    def matrixSolve(self, right):
        """

        :param right:
        :return:
        """
        if right is None:
            raise ArgsIsNull('right')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Array.matrixSolve",
            arguments={
                "left": _input,
                "right": self.formatValue(right)
            }
        )
        return _generatePIEArray(self, _obj)

    def matrixLUDecomposition(self):
        """

        :return:
        """
        _input = self.statement
        _obj = self.getStatement(
            functionName="Array.matrixLUDecomposition",
            arguments={
                "input": _input
            }
        )
        return _generatePIEArray(self, _obj)

    def matrixSingularValueDecomposition(self):
        """

        :return:
        """
        _input = self.statement
        _obj = self.getStatement(
            functionName="Array.matrixSingularValueDecomposition",
            arguments={
                "input": _input
            }
        )
        return _generatePIEArray(self, _obj)
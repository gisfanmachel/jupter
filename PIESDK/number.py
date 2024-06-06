# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   number.py
@Time    :   2020/10/9 下午5:20
@Author  :   lsw
@Version :   1.0
@Contact :   shi_weihappy@126.com
@License :   (C)Copyright 2019-2020, lsw
@Desc    :   None
"""
from pie.object import PIEObject
from pie.utils.error import ArgsIsNull

def _generatePIENumber(pre, statement):
    """
    生成 PIENumber 对象
    :param pre:
    :param statement:
    :return:
    """
    _object = PIENumber()
    _object.pre = pre
    _object.statement = statement
    return _object

class PIENumber(PIEObject):
    def __init__(self, args=None):
        super(PIENumber, self).__init__()
        self.pre = None
        self.statement = None
        if args is None:
            return

        _name = type(args).__name__
        if _name == self.name() \
            or _name == PIEObject.name():
            self.pre = args.pre
            self.statement = args.statement
        elif _name == "bool":
            self.statement = self.getStatement(
                functionName="Number.constructors",
                arguments={
                    "args": 1 if args else 0
                }
            )
        elif _name == "str":
            if len(args.split(".")) > 1:
                args = float(args)
            else:
                args = int(args)
            self.statement = self.getStatement(
                functionName="Number.constructors",
                arguments={
                    "args": args
                }
            )
        elif _name == "int" or _name == "float":
            self.statement = self.getStatement(
                functionName="Number.constructors",
                arguments={
                    "args": args
                }
            )

    @staticmethod
    def name():
        return "PIENumber"

    def abs(self):
        """
        计算绝对值
        :return:
        """
        _obj = self.getStatement(
            functionName="Number.abs",
            arguments={"input": self.statement}
        )
        return _generatePIENumber(self, _obj)

    def log(self):
        """
        计算自然对数
        :return:
        """
        _obj = self.getStatement(
            functionName="Number.log",
            arguments={"input": self.statement}
        )
        return _generatePIENumber(self, _obj)

    def log10(self):
        """
        计算以10为底的对数
        :return:
        """
        _obj = self.getStatement(
            functionName="Number.log10",
            arguments={"input": self.statement}
        )
        return _generatePIENumber(self, _obj)

    def acos(self):
        """
        反余弦函数
        :return:
        """
        _obj = self.getStatement(
            functionName="Number.acos",
            arguments={"input": self.statement}
        )
        return _generatePIENumber(self, _obj)

    def asin(self):
        """
        反正弦函数
        :return:
        """
        _obj = self.getStatement(
            functionName="Number.asin",
            arguments={"input": self.statement}
        )
        return _generatePIENumber(self, _obj)

    def atan(self):
        """
        反正切函数
        :return:
        """
        _obj = self.getStatement(
            functionName="Number.atan",
            arguments={"input": self.statement}
        )
        return _generatePIENumber(self, _obj)

    def cos(self):
        """
        余弦函数
        :return:
        """
        _obj = self.getStatement(
            functionName="Number.cos",
            arguments={"input": self.statement}
        )
        return _generatePIENumber(self, _obj)

    def sin(self):
        """
        正弦函数
        :return:
        """
        _obj = self.getStatement(
            functionName="Number.sin",
            arguments={"input": self.statement}
        )
        return _generatePIENumber(self, _obj)

    def tan(self):
        """
        正切函数
        :return:
        """
        _obj = self.getStatement(
            functionName="Number.tan",
            arguments={"input": self.statement}
        )
        return _generatePIENumber(self, _obj)

    def sqrt(self):
        """
        开平方
        :return:
        """
        _obj = self.getStatement(
            functionName="Number.sqrt",
            arguments={"input": self.statement}
        )
        return _generatePIENumber(self, _obj)

    def round(self):
        """
        四舍五入函数
        :return:
        """
        _obj = self.getStatement(
            functionName="Number.round",
            arguments={"input": self.statement}
        )
        return _generatePIENumber(self, _obj)

    def floor(self):
        """
        向下取整函数
        :return:
        """
        _obj = self.getStatement(
            functionName="Number.floor",
            arguments={"input": self.statement}
        )
        return _generatePIENumber(self, _obj)

    def ceil(self):
        """
        向上取整函数
        :return:
        """
        _obj = self.getStatement(
            functionName="Number.ceil",
            arguments={"input": self.statement}
        )
        return _generatePIENumber(self, _obj)

    def add(self, value):
        """
        求和
        :param value:
        :return:
        """
        if value is None:
            raise ArgsIsNull('参数不能为空')

        _input = self.statement
        _obj = self.getStatement(
            functionName="Number.add",
            arguments={
                "input": _input,
                "value": self.formatValue(value)
            }
        )
        return _generatePIENumber(self, _obj)

    def subtract(self, value):
        """
        相减
        :param value:
        :return:
        """
        if value is None:
            raise ArgsIsNull('参数不能为空')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Number.subtract",
            arguments={
                "input": _input,
                "value": self.formatValue(value)
            }
        )
        return _generatePIENumber(self, _obj)

    def multiply(self, value):
        """
        相乘
        :param value:
        :return:
        """
        if value is None:
            raise ArgsIsNull('参数不能为空')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Number.multiply",
            arguments={
                "input": _input,
                "value": self.formatValue(value)
            }
        )
        return _generatePIENumber(self, _obj)

    def divide(self, value):
        """
        相除
        :param value:
        :return:
        """
        if value is None:
            raise ArgsIsNull('参数不能为空')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Number.divide",
            arguments={
                "input": _input,
                "value": self.formatValue(value)
            }
        )
        return _generatePIENumber(self, _obj)

    def eq(self, value):
        """
        判断相等
        :param value:
        :return:
        """
        if value is None:
            raise ArgsIsNull('参数不能为空')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Number.eq",
            arguments={
                "input": _input,
                "value": self.formatValue(value)
            }
        )
        return _generatePIENumber(self, _obj)

    def neq(self, value):
        """
        判断不相等
        :param value:
        :return:
        """
        if value is None:
            raise ArgsIsNull('参数不能为空')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Number.neq",
            arguments={
                "input": _input,
                "value": self.formatValue(value)
            }
        )
        return _generatePIENumber(self, _obj)

    def pow(self, value):
        """
        计算N次方
        :param value:
        :return:
        """
        if value is None:
            raise ArgsIsNull('参数不能为空')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Number.pow",
            arguments={
                "input": _input,
                "value": self.formatValue(value)
            }
        )
        return _generatePIENumber(self, _obj)

    def max(self, value):
        """
        计算最大值
        :param value:
        :return:
        """
        if value is None:
            raise ArgsIsNull('参数不能为空')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Number.max",
            arguments={
                "input": _input,
                "value": self.formatValue(value)
            }
        )
        return _generatePIENumber(self, _obj)

    def min(self, value):
        """
        最小值
        :param value:
        :return:
        """
        if value is None:
            raise ArgsIsNull('参数不能为空')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Number.min",
            arguments={
                "input": _input,
                "value": self.formatValue(value)
            }
        )
        return _generatePIENumber(self, _obj)

    def lt(self, value):
        """
        判断小于
        :param value:
        :return:
        """
        if value is None:
            raise ArgsIsNull('参数不能为空')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Number.lt",
            arguments={
                "input": _input,
                "value": self.formatValue(value)
            }
        )
        return _generatePIENumber(self, _obj)

    def lte(self, value):
        """
        小于等于
        :param value:
        :return:
        """
        if value is None:
            raise ArgsIsNull('参数不能为空')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Number.lte",
            arguments={
                "input": _input,
                "value": self.formatValue(value)
            }
        )
        return _generatePIENumber(self, _obj)

    def And(self, value):
        """
        逻辑并
        :param value:
        :return:
        """
        if value is None:
            raise ArgsIsNull('参数不能为空')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Number.and",
            arguments={
                "input": _input,
                "value": self.formatValue(value)
            }
        )
        return _generatePIENumber(self, _obj)

    def Not(self):
        """
        逻辑非
        :return:
        """
        _obj = self.getStatement(
            functionName="Number.not",
            arguments={"input": self.statement}
        )
        return _generatePIENumber(self, _obj)

    def Or(self, value):
        """
        逻辑或
        :param value:
        :return:
        """
        if value is None:
            raise ArgsIsNull('参数不能为空')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Number.or",
            arguments={
                "input": _input,
                "value": self.formatValue(value)
            }
        )
        return _generatePIENumber(self, _obj)

    def toByte(self):
        """
        转为byte
        :return:
        """
        _obj = self.getStatement(
            functionName="Number.toByte",
            arguments={"input": self.statement}
        )
        return _generatePIENumber(self, _obj)

    def toDouble(self):
        """
        转为double
        :return:
        """
        _obj = self.getStatement(
            functionName="Number.toDouble",
            arguments={"input": self.statement}
        )
        return _generatePIENumber(self, _obj)

    def toFloat(self):
        """
        转为float
        :return:
        """
        _obj = self.getStatement(
            functionName="Number.toFloat",
            arguments={"input": self.statement}
        )
        return _generatePIENumber(self, _obj)

    def toInt(self):
        """
        转为int
        :return:
        """
        _obj = self.getStatement(
            functionName="Number.toInt",
            arguments={"input": self.statement}
        )
        return _generatePIENumber(self, _obj)

    def toInt16(self):
        """
        转为int16
        :return:
        """
        _obj = self.getStatement(
            functionName="Number.toInt16",
            arguments={"input": self.statement}
        )
        return _generatePIENumber(self, _obj)

    def exp(self):
        """
        计算e为底
        :return:
        """
        _obj = self.getStatement(
            functionName="Number.exp",
            arguments={"input": self.statement}
        )
        return _generatePIENumber(self, _obj)


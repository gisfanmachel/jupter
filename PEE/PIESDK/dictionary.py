# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   dictionary.py
@Time    :   2020/10/10 上午10:14
@Author  :   lsw
@Version :   1.0
@Contact :   shi_weihappy@126.com
@License :   (C)Copyright 2019-2020, lsw
@Desc    :   None
"""
from pie.object import PIEObject, _generatePIEObject
from pie.utils.error import ArgsIsNull

def _generatePIEArray(pre, statement):
    """
    生成 PIEArray 对象
    :param pre:
    :param statement:
    :return:
    """
    from pie.array import PIEArray
    _object = PIEArray()
    _object.pre = pre
    _object.statement = statement
    return _object

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

def _generatePIEList(pre, statement):
    """
    生成 PIEList 对象
    :param pre:
    :param statement:
    :return:
    """
    from pie.list import PIEList
    _object = PIEList()
    _object.pre = pre
    _object.statement = statement
    return _object

def _generatePIEString(pre, statement):
    """
    生成 PIEString 对象
    :param pre:
    :param statement:
    :return:
    """
    from pie.string import PIEString
    _object = PIEString()
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
    _object = PIEDictionary()
    _object.pre = pre
    _object.statement = statement
    return _object

class PIEDictionary(PIEObject):
    def __init__(self, args=None):
        super(PIEDictionary, self).__init__()
        self.pre = None
        self.statement = None
        if not args:
            return

        if type(args).__name__ == self.name() \
            or type(args).__name__ == PIEObject.name():
            self.pre = args.pre
            self.statement = args.statement
        else:
            self.pre = None
            self.statement = self.getStatement(
                functionName="Dictionary.constructors",
                arguments={
                    "args": self.formatValue(args)
                }
            )

    @staticmethod
    def name():
        return "PIEDictionary"

    def fromLists(self, keys, values):
        """
        通过列表数据生成字典数据
        :param keys:
        :param values:
        :return:
        """
        if not keys or not values:
            raise ArgsIsNull("keys,values")

        _obj = self.getStatement(
            functionName="Dictionary.fromLists",
            arguments={
                "keys": self.formatValue(keys),
                "values": self.formatValue(values)
            }
        )
        return _generatePIEDictionary(self, _obj)

    def get(self, key):
        """
        返回指定key的值
        :param key:
        :return:
        """
        if key is None:
            raise ArgsIsNull('key')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Dictionary.get",
            arguments={
                "input": _input,
                "key": self.formatValue(key)
            },
            compute=True
        )
        return _generatePIEObject(self, _obj)

    def keys(self):
        """
        返回字典的key列表
        :return:
        """
        _input = self.statement
        _obj = self.getStatement(
            functionName="Dictionary.keys",
            arguments={
                "input": _input
            }
        )
        return _generatePIEList(self, _obj)

    def values(self):
        """
        返回字典的值列表
        :return:
        """
        _input = self.statement
        _obj = self.getStatement(
            functionName="Dictionary.values",
            arguments={
                "input": _input
            }
        )
        return _generatePIEList(self, _obj)

    def size(self):
        """
        返回字典的大小
        :return:
        """
        _input = self.statement
        _obj = self.getStatement(
            functionName="Dictionary.size",
            arguments={
                "input": _input
            }
        )
        return _generatePIENumber(self, _obj)

    def getString(self, key):
        """
        返回指定key的字符串值
        :param key:
        :return:
        """
        if key is None:
            raise ArgsIsNull('key')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Dictionary.getString",
            arguments={
                "input": _input,
                "key": self.formatValue(key)
            }
        )
        return _generatePIEString(self, _obj)

    def getNumber(self, key):
        """
        返回指定key数值的值
        :param key:
        :return:
        """
        if key is None:
            raise ArgsIsNull('key')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Dictionary.getNumber",
            arguments={
                "input": _input,
                "key": self.formatValue(key)
            }
        )
        return _generatePIENumber(self, _obj)

    def getArray(self, key):
        """
        返回指定key的数组值
        :param key:
        :return:
        """
        if key is None:
            raise ArgsIsNull('key')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Dictionary.getArray",
            arguments={
                "input": _input,
                "key": self.formatValue(key)
            }
        )
        return _generatePIEArray(self, _obj)

    def contains(self, key):
        """
        判断字典是否包含指定的key
        :param key:
        :return:
        """
        if key is None:
            raise ArgsIsNull('key')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Dictionary.contains",
            arguments={
                "input": _input,
                "key": self.formatValue(key)
            }
        )
        return _generatePIEObject(self, _obj)

    def set(self, key, value=None):
        """
        设置指定key的值
        :param key:
        :param value:
        :return:
        """
        if key is None:
            raise ArgsIsNull('key')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Dictionary.set",
            arguments={
                "input": _input,
                "key": self.formatValue(key),
                "value": self.formatValue(value)
            },
            compute=True
        )
        return _generatePIEDictionary(self, _obj)

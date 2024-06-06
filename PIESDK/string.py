# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   string.py
@Time    :   2020/10/10 上午10:16
@Author  :   lsw
@Version :   1.0
@Contact :   shi_weihappy@126.com
@License :   (C)Copyright 2019-2020, lsw
@Desc    :   字符串处理算法
"""
from pie.object import PIEObject
from pie.utils.error import ArgsIsNull
import datetime
import pytz

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
    _object = PIEString()
    _object.pre = pre
    _object.statement = statement
    return _object

class PIEString(PIEObject):
    def __init__(self, args=None):
        super(PIEString, self).__init__()
        self.pre = None
        self.statement = None
        if args is None:
            return

        _name = type(args).__name__
        if _name in ["str", "int","float","bool"]:
            self.statement = self.getStatement(
                functionName="String.constructors",
                arguments={
                    "args": args
                }
            )
        elif _name in [self.name(), PIEObject.name(), "PIENumber"]:
            self.pre = args.pre
            self.statement = args.statement
        elif _name == "list":
            self.statement = {
                "type": "Invocation",
                "arguments": {
                    "args": ",".join(args)
                },
                "functionName": "String.constructors"
            }
        elif isinstance(args, datetime.datetime):
            utc_tz = pytz.timezone("UTC")
            args = args.replace(tzinfo=utc_tz).strftime("%Y-%m-%d %H:%M:%S")
            self.statement = {
                "type": "Invocation",
                "arguments": {
                    "args": args
                },
                "functionName": "String.constructors"
            }


    @staticmethod
    def name():
        return "PIEString"

    def cat(self, str2):
        """
        拼接字符串
        :param str2:
        :return:
        """
        if str2 is None:
            raise ArgsIsNull("str2")
        _str1 = self.statement
        _obj = self.getStatement(
            functionName="String.cat",
            arguments={
                "str1": _str1,
                "str2": self.formatValue(str2)
            }
        )
        return _generatePIEString(self, _obj)

    def compareTo(self, str2):
        """
        比较两个字符串
        :param str2:
        :return:
        """
        if str2 is None:
            raise ArgsIsNull("str2")
        _str1 = self.statement
        _obj = self.getStatement(
            functionName="String.compareTo",
            arguments={
                "str1": _str1,
                "str2": self.formatValue(str2)
            }
        )
        return _generatePIEString(self, _obj)

    def index(self, pattern):
        """
        获取索引
        :param pattern:
        :return:
        """
        if pattern is None:
            raise ArgsIsNull("pattern")

        _input = self.statement
        _obj = self.getStatement(
            functionName="String.index",
            arguments={
                "input": _input,
                "pattern": self.formatValue(pattern)
            },
            compute=True
        )
        return _generatePIENumber(self, _obj)

    def length(self):
        """
        返回字符串长度
        :return:
        """
        _obj = self.getStatement(
            functionName="String.length",
            compute=True
        )
        return _generatePIENumber(self, _obj)

    def replace(self, regex, replacement=""):
        """
        替换字符串
        :param regex:
        :param replacement:
        :return:
        """
        if regex is None:
            raise ArgsIsNull("regex")
        if not replacement:
            replacement = ""
        _input = self.statement
        _obj = self.getStatement(
            functionName="String.replace",
            arguments={
                "input": _input,
                "regex": self.formatValue(regex),
                "replacement": self.formatValue(replacement)
            }
        )
        return _generatePIEString(self, _obj)

    def slice(self, start, end):
        """
        返回自字符串
        :param start:
        :param end:
        :return:
        """
        if start is None:
            raise ArgsIsNull("start")
        if end is None:
            raise ArgsIsNull("end")
        _input = self.statement
        _obj = self.getStatement(
            functionName="String.slice",
            arguments={
                "input": _input,
                "start": self.formatValue(start),
                "end": self.formatValue(end)
            }
        )
        return _generatePIEString(self, _obj)

    def split(self, regex):
        """
        字符串分割
        :param regex:
        :return:
        """
        if regex is None:
            raise ArgsIsNull("regex")
        _input = self.statement
        _obj = self.getStatement(
            functionName="String.split",
            arguments={
                "input": _input,
                "regex": self.formatValue(regex)
            }
        )
        return _generatePIEString(self, _obj)

    def rindex(self, pattern):
        """

        :param pattern:
        :return:
        """
        if pattern is None:
            raise ArgsIsNull("patter")
        _input = self.statement
        _obj = self.getStatement(
            functionName="String.rindex",
            arguments={
                "input": _input,
                "pattern": self.formatValue(pattern)
            }
        )
        return _generatePIENumber(self, _obj)

    def match(self, regex, flags=""):
        """

        :param regex:
        :param flags:
        :return:
        """
        if regex is None:
            raise ArgsIsNull("regex")
        _input = self.statement
        _obj = self.getStatement(
            functionName="String.match",
            arguments={
                "input": _input,
                "regex": self.formatValue(regex),
                "flags": self.formatValue(flags)
            }
        )
        return _generatePIEList(self, _obj)
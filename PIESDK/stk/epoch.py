# -*- coding: utf-8 -*-
# author:liuxiaodong 
# contact: 2152550864@qq.com
# datetime:2021/5/7 14:19
# software: PyCharm
# python versions: Python3.7
# file: epoch.py
# license: (C)Copyright 2019-2020

from pie.object import PIEObject
from pie.utils.error import ArgsIsNull

def _generatePIEEpoch(pre, statement):
    """
    构造PIEEpoch对象
    @param pre:
    @param statement:
    @return:
    """
    _object = PIEEpoch()
    _object.pre = pre
    _object.statement = statement
    return _object

class PIEEpoch(PIEObject):
    def __init__(self, year=1970, month=1, day=1,  hour=0, minute=0, second=0):
        """
        Epoch对象构造函数
        @param year:年
        @param month:月
        @param day:日
        @param hour:小时
        @param minute:分钟
        @param second:秒
        """
        super(PIEEpoch, self).__init__()
        self.pre = None
        _obj = self.getStatement(
            functionName="Epoch.constructors",
            arguments={
                 "year": year,
                 "month": month,
                 "day": day,
                 "hour": hour,
                 "minute": minute,
                 "second": second,
            }
        )
        self.statement = _obj

    @staticmethod
    def name():
        return "PIESTKEpoch"

    def fromString(self, inputString):
        """
        @param inputString:
        @return:
        """
        if inputString is None:
            raise ArgsIsNull("inputString")
        _obj = self.getStatement(
            functionName="Epoch.fromString",
            arguments={
                "input": inputString,
            }
        )
        return _generatePIEEpoch(self, _obj)

    def addYears(self, right):
        """
        @param right:
        @return:
        """
        if right is None:
            raise ArgsIsNull("right")
        _input = self.statement
        _obj = self.getStatement(
            functionName="Epoch.addYears",
            arguments={
             "input": _input,
             "right": right,
            }
        )
        return _generatePIEEpoch(self, _obj)

    def addMonth(self, right):
        """
        @param right:
        @return:
        """
        if right is None:
            raise ArgsIsNull("right")
        _input = self.statement
        _obj = self.getStatement(
            functionName="Epoch.addMonth",
            arguments={
             "input": _input,
             "right": right,
            }
        )
        return _generatePIEEpoch(self, _obj)

    def addDays(self, right):
        """

        @param right:
        @return:
        """
        if right is None:
            raise ArgsIsNull("right")
        _input = self.statement
        _obj = self.getStatement(
            functionName="Epoch.addDays",
            arguments={
                 "input": _input,
                 "right": right,
            }
        )
        return _generatePIEEpoch(self, _obj)

    def addSecs(self, right):
        """

        @param right:
        @return:
        """
        if right is None:
            raise ArgsIsNull("right")
        _input = self.statement
        _obj = self.getStatement(functionName="Epoch.addSecs",
                                 arguments={
                                     "input": _input,
                                     "right": right,
                                 })
        return _generatePIEEpoch(self, _obj)

    def addMSecs(self, right):
        """

        @param right:
        @return:
        """
        if right is None:
            raise ArgsIsNull("right")
        _input = self.statement
        _obj = self.getStatement(
            functionName="Epoch.addMSecs",
            arguments={
             "input": _input,
             "right": right
            }
        )
        return _generatePIEEpoch(self, _obj)

    def daysTo(self, right):
        """

        @param right:
        @return:
        """
        if right is None:
            raise ArgsIsNull("right")
        _input = self.statement
        _obj = self.getStatement(
            functionName="Epoch.daysTo",
            arguments={
             "input": _input,
             "right": right,
            }
        )
        return _generatePIEEpoch(self, _obj)

    def secsTo(self, right):
        """

        @param right:
        @return:
        """
        if right is None:
            raise ArgsIsNull("right")
        _input = self.statement
        _obj = self.getStatement(
            functionName="Epoch.secsTo",
            arguments={
             "input": _input,
             "right": right,
            }
        )
        return _generatePIEEpoch(self, _obj)

    def msecsTo(self, right):
        """

        @param right:
        @return:
        """
        if right is None:
            raise ArgsIsNull("right")
        _input = self.statement
        _obj = self.getStatement(
            functionName="Epoch.msecsTo",
            arguments={
             "input": _input,
             "right": right,
            }
        )
        return _generatePIEEpoch(self, _obj)

    def setSecsSinceEpoch(self, right):
        """

        @param right:
        @return:
        """
        if right is None:
            raise ArgsIsNull("right")
        _input = self.statement
        _obj = self.getStatement(
            functionName="Epoch.setSecsSinceEpoch",
            arguments={
             "input": _input,
             "right": right,
            }
        )
        return _generatePIEEpoch(self, _obj)

    def setMSecsSinceEpoch(self, right):
        """

        @param right:
        @return:
        """
        if right is None:
            raise ArgsIsNull("right")
        _input = self.statement
        _obj = self.getStatement(
            functionName="Epoch.setMSecsSinceEpoch",
            arguments={
             "input": _input,
             "right": right,
            }
        )
        return _generatePIEEpoch(self, _obj)

    def toSecsSinceEpoch(self, right):
        """

        @param right:
        @return:
        """
        if right is None:
            raise ArgsIsNull("right")
        _input = self.statement
        _obj = self.getStatement(functionName="Epoch.toSecsSinceEpoch",
                                 arguments={
                                     "input": _input,
                                     "right": right,
                                 })
        return _generatePIEEpoch(self, _obj)

    def toMSecsSinceEpoch(self, right):
        """

        @param right:
        @return:
        """
        if right is None:
            raise ArgsIsNull("right")
        _input = self.statement
        _obj = self.getStatement(functionName="Epoch.toMSecsSinceEpoch",
                                 arguments={
                                     "input": _input,
                                     "right": right,
                                 })
        return _generatePIEEpoch(self, _obj)

    def toStdString(self, right):
        """

        @param right:
        @return:
        """
        if right is None:
            raise ArgsIsNull("right")
        _input = self.statement
        _obj = self.getStatement(functionName="Epoch.toStdString",
                                 arguments={
                                     "input": _input,
                                     "right": right,
                                 })
        return _generatePIEEpoch(self, _obj)

    def isNull(self):
        """
        @return:
        """
        _input = self.statement
        _obj = self.getStatement(functionName="Epoch.isNull",
                                 arguments={
                                     "input": _input,
                                 })
        return _generatePIEEpoch(self, _obj)

    def isValid(self):
        """

        @return:
        """
        _input = self.statement
        _obj = self.getStatement(functionName="Epoch.isValid",
                                 arguments={
                                     "input": _input,
                                 })
        return _generatePIEEpoch(self, _obj)

    def overloadingAssignment(self, right):
        """

        @param right:
        @return:
        """
        if right is None:
            raise ArgsIsNull("right")
        _input = self.statement
        _obj = self.getStatement(functionName="Epoch.overloadingAssignment",
                                 arguments={
                                     "input": _input,
                                     "right": right,
                                 })
        return _generatePIEEpoch(self, _obj)

    def overloadingEqual(self, right):
        """

        @param right:
        @return:
        """
        if right is None:
            raise ArgsIsNull("right")
        _input = self.statement
        _obj = self.getStatement(functionName="Epoch.overloadingEqual",
                                 arguments={
                                     "input": _input,
                                     "right": right,
                                 })
        return _generatePIEEpoch(self, _obj)

    def overloadingNotEqual(self, right):
        """

        @param right:
        @return:
        """
        if right is None:
            raise ArgsIsNull("right")
        _input = self.statement
        _obj = self.getStatement(functionName="Epoch.overloadingNotEqual",
                                 arguments={
                                     "input": _input,
                                     "right": right,
                                 })
        return _generatePIEEpoch(self, _obj)

    def overloadingLess(self, right):
        """

        @param right:
        @return:
        """
        if right is None:
            raise ArgsIsNull("right")
        _input = self.statement
        _obj = self.getStatement(functionName="Epoch.overloadingLess",
                                 arguments={
                                     "input": _input,
                                     "right": right,
                                 })
        return _generatePIEEpoch(self, _obj)

    def overloadingLessEqual(self, right):
        """

        @param right:
        @return:
        """
        if right is None:
            raise ArgsIsNull("right")
        _input = self.statement
        _obj = self.getStatement(functionName="Epoch.overloadingLessEqual",
                                 arguments={
                                     "input": _input,
                                     "right": right,
                                 })
        return _generatePIEEpoch(self, _obj)

    def overloadingGreater(self, right):
        """

        @param right:
        @return:
        """
        if right is None:
            raise ArgsIsNull("right")
        _input = self.statement
        _obj = self.getStatement(functionName="Epoch.overloadingGreater",
                                 arguments={
                                     "input": _input,
                                     "right": right,
                                 })
        return _generatePIEEpoch(self, _obj)

    def overloadingGreaterEqual(self, right):
        """

        @param right:
        @return:
        """
        if right is None:
            raise ArgsIsNull("right")
        _input = self.statement
        _obj = self.getStatement(functionName="Epoch.overloadingGreaterEqual",
                                 arguments={
                                     "input": _input,
                                     "right": right,
                                 })
        return _generatePIEEpoch(self, _obj)

    def getYear(self):
        """
        @return:
        """
        _input = self.statement
        _obj = self.getStatement(functionName="Epoch.getYear",
                                 arguments={
                                     "input": _input,
                                 })
        return _generatePIEEpoch(self, _obj)

    def getMonth(self):
        """
        @return:
        """
        _input = self.statement
        _obj = self.getStatement(functionName="Epoch.getMonth",
                                 arguments={
                                     "input": _input,
                                 })
        return _generatePIEEpoch(self, _obj)

    def getDay(self):
        """
        @return:
        """
        _input = self.statement
        _obj = self.getStatement(functionName="Epoch.getDay",
                                 arguments={
                                     "input": _input,
                                 })
        return _generatePIEEpoch(self, _obj)

    def getHour(self):
        """
        @return:
        """
        _input = self.statement
        _obj = self.getStatement(functionName="Epoch.getHour",
                                 arguments={
                                     "input": _input,
                                 })
        return _generatePIEEpoch(self, _obj)

    def getMinute(self):
        """
        @return:
        """
        _input = self.statement
        _obj = self.getStatement(functionName="Epoch.getMinute",
                                 arguments={
                                     "input": _input,
                                 })
        return _generatePIEEpoch(self, _obj)

    def getSecond(self):
        """
        @return:
        """
        _input = self.statement
        _obj = self.getStatement(functionName="Epoch.getSecond",
                                 arguments={
                                     "input": _input,
                                 })
        return _generatePIEEpoch(self, _obj)

    def toMJD(self):
        """
        @return:
        """
        _input = self.statement
        _obj = self.getStatement(functionName="Epoch.toMJD",
                                 arguments={
                                     "input": _input,
                                 })
        return _generatePIEEpoch(self, _obj)

    def toJD(self):
        """
        @return:
        """
        _input = self.statement
        _obj = self.getStatement(functionName="Epoch.toJD",
                                 arguments={
                                     "input": _input,
                                 })
        return _generatePIEEpoch(self, _obj)

    def fromMJDbyDouble(self, right):
        """
        @param right:
        @return:
        """
        if right is None:
            raise ArgsIsNull("right")
        _input = self.statement
        _obj = self.getStatement(functionName="Epoch.fromMJDbyDouble",
                                 arguments={
                                     "input": _input,
                                     "right": right,
                                 })
        return _generatePIEEpoch(self, _obj)

    def fromStdString(self, right):
        """

        @param right:
        @return:
        """
        if right is None:
            raise ArgsIsNull("right")
        _input = self.statement
        _obj = self.getStatement(functionName="Epoch.fromStdString",
                                 arguments={
                                     "input": _input,
                                     "right": right,
                                 })
        return _generatePIEEpoch(self, _obj)

    def isLeapYear(self, right):
        """

        @param right:
        @return:
        """
        if right is None:
            raise ArgsIsNull("right")
        _input = self.statement
        _obj = self.getStatement(functionName="Epoch.isLeapYear",
                                 arguments={
                                     "input": _input,
                                     "right": right,
                                 })
        return _generatePIEEpoch(self, _obj)

    def judgeTimeLegal(self, right):
        """

        @param right:
        @return:
        """
        if right is None:
            raise ArgsIsNull("right")
        _input = self.statement
        _obj = self.getStatement(functionName="Epoch.judgeTimeLegal",
                                 arguments={
                                     "input": _input,
                                     "right": right,
                                 })
        return _generatePIEEpoch(self, _obj)

    def fromMJDbyInt(self, right):
        """

        @param right:
        @return:
        """
        if right is None:
            raise ArgsIsNull("right")
        _input = self.statement
        _obj = self.getStatement(functionName="Epoch.fromMJDbyInt",
                                 arguments={
                                     "input": _input,
                                     "right": right,
                                 })
        return _generatePIEEpoch(self, _obj)


    def toIntJD(self):
        """
        @return:
        """
        _input = self.statement
        _obj = self.getStatement(functionName="Epoch.toIntJD",
                                 arguments={
                                     "input": _input,
                                 })
        return _generatePIEEpoch(self, _obj)

    def toIntMJD(self):
        """
        @return:
        """
        _input = self.statement
        _obj = self.getStatement(functionName="Epoch.toIntMJD",
                                 arguments={
                                     "input": _input,
                                 })
        return _generatePIEEpoch(self, _obj)

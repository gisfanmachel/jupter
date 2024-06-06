# -*- coding: utf-8 -*-
# author:liuxiaodong 
# contact: 2152550864@qq.com
# datetime:2021/5/7 13:38
# software: PyCharm
# python versions: Python3.7
# file: orbit.py
# license: (C)Copyright 2019-2020

from pie.object import PIEObject

def _generatePIEString(pre, statement):
    """

    @param pre:
    @param statement:
    @return:
    """
    from pie.string import PIEString
    _object = PIEString()
    _object.pre = pre
    _object.statement = statement
    return _object

def _generatePIEFeature(pre, statement):
    """

    @param pre:
    @param statement:
    @return:
    """
    from pie.vector.feature import PIEFeature
    _object = PIEFeature()
    _object.pre = pre
    _object.statement = statement
    return _object

def _generatePIESTKOrbit(pre, statement):
    """
    构造PIESTKOrbit对象
    @param pre:
    @param statement:
    @return:
    """
    _object = PIESTKOrbit()
    _object.pre = pre
    _object.statement = statement
    return _object

class PIESTKOrbit(PIEObject):
    def __init__(self):
        super(PIESTKOrbit, self).__init__()
        self.pre = None
        self.statement = None

    @staticmethod
    def name():
        return "PIESTKOrbit"

    def propagatorTwobody(self, startEpoch, endEpoch, time, elementKepler):
        """
        @param startEpoch:
        @param endEpoch:
        @param time:
        @param elementKepler:
        @return:
        """
        _obj = self.getStatement(
            functionName="Orbit.propagatorTwobody",
             arguments={
                 "startEpoch": self.formatValue(startEpoch) if startEpoch else None,
                 "endEpoch": self.formatValue(endEpoch) if endEpoch else None,
                 "time": time,
                 "elementKepler": self.formatValue(elementKepler) if elementKepler else None,
             }
        )
        return _generatePIESTKOrbit(self, _obj)

    def propagatorSGP4(self, startEpoch, endEpoch, time, elementTwoLine):
        """
        @param startEpoch:
        @param endEpoch:
        @param time:
        @param elementTwoLine:
        @return:
        """
        _obj = self.getStatement(
            functionName="Orbit.propagatorSGP4",
            arguments={
                 "startEpoch": self.formatValue(startEpoch) if startEpoch else None,
                 "endEpoch": self.formatValue(endEpoch) if endEpoch else None,
                 "time": time,
                 "elementTowLine": self.formatValue(elementTwoLine) if elementTwoLine else None,
            }
        )
        return _generatePIESTKOrbit(self, _obj)

    def toFeature(self):
        """
        @return:
        """
        _input = self.statement
        _obj = self.getStatement(
            functionName="Orbit.toFeature",
            arguments={
                "input": _input,
            }
        )
        return _generatePIEFeature(self, _obj)


    def toJson(self):
        """
        @return:
        """
        _input = self.statement
        _obj = self.getStatement(
            functionName="Orbit.toJson",
            arguments={
                "input": _input,
            }
        )
        return _generatePIEString(self, _obj)

Orbit = PIESTKOrbit()
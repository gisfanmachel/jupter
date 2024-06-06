# -*- coding: utf-8 -*-
# author:liuxiaodong 
# contact: 2152550864@qq.com
# datetime:2021/5/7 13:30
# software: PyCharm
# python versions: Python3.7
# file: elementtwoline.py
# license: (C)Copyright 2019-2020

from pie.object import PIEObject

def _generatePIESTKElementTwoLine(pre, statement):
    """
    构造PIESTKElementTwoLine对象
    @param pre:
    @param statement:
    @return:
    """
    _object = PIESTKElementTwoLine()
    _object.pre = pre
    _object.statement = statement
    return _object

class PIESTKElementTwoLine(PIEObject):
    def __init__(self, line1=None, line2=None, norad=None):
        super(PIESTKElementTwoLine, self).__init__()
        self.pre = None
        _obj = self.getStatement(functionName="ElementTwoLine.constructors",
                                 arguments={
                                     "line1": self.formatValue(line1),
                                     "line2": self.formatValue(line2),
                                     "norad": norad,
                                 })
        self.statement = _obj

    @staticmethod
    def name():
        return "PIESTKElementTwoLine"

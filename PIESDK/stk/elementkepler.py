# -*- coding: utf-8 -*-
# author:liuxiaodong 
# contact: 2152550864@qq.com
# datetime:2021/5/7 13:19
# software: PyCharm
# python versions: Python3.7
# file: elementkepler.py
# license: (C)Copyright 2019-2020

from pie.object import PIEObject

def _generatePIESTKElementKepler(pre, statement):
    """
    构造STKElementKepler对象
    @param pre:
    @param statement:
    @return:
    """
    _object = PIESTKElementKepler()
    _object.pre = pre
    _object.statement = statement
    return _object

class PIESTKElementKepler(PIEObject):
    def __init__(self, epoch=None, semimajorAxis=None, eccentricity=None, inclination=None, argPerigee=None, raan=None, meanAnomaly=None):
        """
        Keplerelement对象构造函数
        @param epoch:历元
        @param semimajorAxis:半长轴
        @param eccentricity:偏心率
        @param inclination:倾角
        @param argPerigee:近地点幅角
        @param raan:升交点赤经
        @param meanAnomaly:平近点角
        """
        super(PIESTKElementKepler, self).__init__()
        self.pre = None
        _obj = self.getStatement(functionName="ElementKepler.constructors",
                                 arguments={
                                     "epoch": self.formatValue(epoch),
                                     "semimajorAxis": semimajorAxis,
                                     "eccentricity": eccentricity,
                                     "inclination": inclination,
                                     "argPerigee": argPerigee,
                                     "raan": raan,
                                     "meanAnomaly": meanAnomaly,
                                 })
        self.statement = _obj

    @staticmethod
    def name():
        return "PIESTKElementKepler"
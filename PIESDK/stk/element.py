# -*- coding:utf-8 -*-
"""
@Project :   PyCharm
@File    :   element.py
@Time    :   2021/11/11 17:13 下午
@Author  :   lsw
@Version :   1.0
@Contact :   shi_weihappy@126.com
@License :   (C)Copyright 2020-2021, lsw
@Desc    :   None
"""
from pie.STK.elementtwoline import PIESTKElementTwoLine
from pie.STK.elementkepler import PIESTKElementKepler
class Element(object):
    def __init__(self):
        super(Element, self).__init__()
    @staticmethod
    def Kepler(epoch, semimajorAxis, eccentricity, inclination, argPerigee, raan, meanAnomaly):
        return PIESTKElementKepler(epoch, semimajorAxis, eccentricity, inclination, argPerigee, raan, meanAnomaly)

    @staticmethod
    def TwoLine(line1, line2, norad):
        return PIESTKElementTwoLine(line1, line2, norad)


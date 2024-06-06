# -*- coding: utf-8 -*-
# author:liuxiaodong 
# contact: 2152550864@qq.com
# datetime:2021/5/7 14:07
# software: PyCharm
# python versions: Python3.7
# file: orbitpoint.py
# license: (C)Copyright 2019-2020

from pie.object import PIEObject

class PIEOrbitPoint(PIEObject):
    def __init__(self, epoch, position, velocity):
        super(PIEOrbitPoint, self).__init__()
        self.pre = None
        self.statement = self.getStatement(
            functionName="OrbitPoint.constructors",
            arguments={
                 "epoch": self.formatValue(epoch),
                 "position": self.formatValue(position),
                 "velocity": self.formatValue(velocity)
            }
        )

    @staticmethod
    def name():
        return "PIESTKOrbitPoint"




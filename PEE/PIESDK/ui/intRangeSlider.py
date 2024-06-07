# -*- coding: utf-8 -*-
# author:liuxiaodong 
# contact: 2152550864@qq.com
# datetime:2021/5/17 15:22
# software: PyCharm
# python versions: Python3.7
# file: intrangeslider.py
# license: (C)Copyright 2019-2021 liuxiaodong
from ipywidgets.widgets import IntRangeSlider



class PIEIntRangeSlider(IntRangeSlider):
    def __init__(self):
        super(PIEIntRangeSlider, self).__init__()
        self.name = "PIEIntRangeSlider"

    def name(self):
        return self.name


    def setValue(self, value: tuple):
        self.value = value

    def getValue(self):
        return self.value

    def setMin(self, value: int):
        self.min = value

    def getMin(self):
        return self.min

    def setMax(self, value: int):
        self.max = value

    def getMax(self):
        return self.max

    def setStep(self, value: int):
        self.step = value

    def getStep(self):
        return self.step

    def setDescription(self, value: str):
        self.description = value

    def getDescription(self):
        return self.description

    def setDisabled(self, value: bool):
        self.disabled = value

    def setContinuousUpdate(self, value: bool):
        self.continuous_update = value

    def setOrientation(self, value: str):
        self.orientation = value

    def setReadout(self, vaule: bool):
        self.readout = vaule

    def setReadoutFormat(self, value: bool):
        self.readout_format = value


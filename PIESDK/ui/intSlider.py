# -*- coding: utf-8 -*-
# author:liuxiaodong 
# contact: 2152550864@qq.com
# datetime:2021/5/13 14:53
# software: PyCharm
# python versions: Python3.7
# file: intslider.py
# license: (C)Copyright 2019-2020

from ipywidgets.widgets import IntSlider


class PIEIntSlider(IntSlider):
    def __init__(self):
        super(PIEIntSlider, self).__init__()
        self.name = PIEIntSlider

    def name(self):
        return self.name

    def setValue(self, value):
        self.value = value

    def getValue(self):
        return self.value

    def setMin(self, value):
        self.min = value

    def getMin(self):
        return self.min

    def setMax(self, value):
        self.max = value

    def getMax(self):
        return self.max

    def setStep(self, value):
        self.step = value

    def getStep(self):
        return self.step

    def setDescription(self, description):
        """

        @param description:
        @return:
        """
        self.description = description

    def getDescription(self):
        """

        @return:
        """
        return self.description





# -*- coding: utf-8 -*-
# author:liuxiaodong 
# contact: 2152550864@qq.com
# datetime:2021/5/17 16:43
# software: PyCharm
# python versions: Python3.7
# file: floatprogress.py
# license: (C)Copyright 2019-2021 liuxiaodong
from ipywidgets.widgets import FloatProgress



class PIEFloatProgress(FloatProgress):
    def __init__(self):
        super(PIEFloatProgress, self).__init__()
        self.name = "PIEFloatProgress"

    def name(self):
        return self.name

    def setValue(self, value: int):
        self.value = value

    def setMin(self, value: int):
        self.min = value

    def setMax(self, value:int):
        self.max = value

    def setDescription(self, value: str):
        self.description = value

    def setBarStyle(self, value: str):
        self.bar_style = value

    def setStyle(self, value: dict):
        self.style = value

    def setOrientation(self, value: str):
        self.orientation = value


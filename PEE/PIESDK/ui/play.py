# -*- coding: utf-8 -*-
# author:liuxiaodong 
# contact: 2152550864@qq.com
# datetime:2021/5/17 13:16
# software: PyCharm
# python versions: Python3.7
# file: play.py
# license: (C)Copyright 2019-2021 liuxiaodong
from ipywidgets.widgets import Play



class PIEPlay(Play):
    def __init__(self):
        super(PIEPlay, self).__init__()
        self.name = "PIEPlay"

    def name(self):
        return self.name

    def setValue(self, value: int):
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

    def setInterval(self, value: int):
        self.interval = value

    def setDescription(self, value: str):
        self.description = value

    def getDescription(self):
        return self.description

    def setDisabled(self, value: bool):
        self.disabled = value

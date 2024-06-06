# -*- coding: utf-8 -*-
# author:liuxiaodong 
# contact: 2152550864@qq.com
# datetime:2021/5/17 10:38
# software: PyCharm
# python versions: Python3.7
# file: intprogress.py
# license: (C)Copyright 2019-2021 liuxiaodong
from ipywidgets.widgets import IntProgress



class PIEIntProgress(IntProgress):
    def __init__(self):
        super(PIEIntProgress, self).__init__()
        self.name = "PIEIntProgress"

    def name(self):
        return self.name

    def setValue(self, value: int):
        self.value = value

    def setMin(self, value: int):
        self.min = value

    def setMax(self, value: int):
        self.max = value

    def setDescription(self, value: str):
        self.description = value

    def getDescription(self):
        return self.description

    def setBarStyle(self, value: str):
        """

        @param value: 'success', 'info', 'warning', 'danger' or ''
        @return:
        """
        self.bar_style = value

    def setStyle(self, value: dict):
        """

        @param value: {'bar_color': 'maroon'}
        @return:
        """
        self.style = value

    def setOrientation(self, value: str):
        self.orientation = value



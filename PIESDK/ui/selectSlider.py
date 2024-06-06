# -*- coding: utf-8 -*-
# author:liuxiaodong 
# contact: 2152550864@qq.com
# datetime:2021/5/17 10:11
# software: PyCharm
# python versions: Python3.7
# file: selectslider.py
# license: (C)Copyright 2019-2021 liuxiaodong
from ipywidgets.widgets import SelectionSlider




class PIESelectionSlider(SelectionSlider):
    def __init__(self, *args, **kwargs):
        if len(kwargs.get("options", ())) == 0:
            kwargs['options'] = ['a', 'b', 'c']
        super(PIESelectionSlider, self).__init__(*args, **kwargs)
        self.name = "PIESelectionSlider"
        self.options = [1, 2, 3]

    def name(self):
        return self.name

    def setOptions(self, value: list):
        self.options = value

    def getOptions(self):
        return self.options

    def setValue(self, value: str):
        self.value = value

    def setDescription(self, value: str):
        self.description = value

    def getDescription(self):
        return self.description

    def setDisabled(self, value: bool):
        self.disabled = value

    def setContinuousUpdate(self, value: bool):
        self.continuous_update = value

    def setOrientation(self, value: str):
        """

        @param value: horizontal or vertical
        @return:
        """
        self.orientation = value

    def setReadout(self, value: bool):
        self.readout = value


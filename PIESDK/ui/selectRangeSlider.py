# -*- coding: utf-8 -*-
# author:liuxiaodong 
# contact: 2152550864@qq.com
# datetime:2021/5/17 10:26
# software: PyCharm
# python versions: Python3.7
# file: selectrangeslider.py
# license: (C)Copyright 2019-2021 liuxiaodong
from ipywidgets.widgets import SelectionRangeSlider



class PIESelectionRangeSlider(SelectionRangeSlider):
    def __init__(self, *args, **kwargs):
        if len(kwargs.get("options", ())) == 0:
            kwargs['options'] = [1, 2, 3]
        super(PIESelectionRangeSlider, self).__init__(*args, **kwargs)
        self.name = "PIESelectionRangeSlider"


    def name(self):
        return self.name

    def setOptions(self, value: list):
        self.options = value

    def getOptions(self):
        return self.options

    def setIndex(self, value: tuple):
        self.index = value

    def setDescription(self, value: str):
        self.description = value

    def getDescription(self):
        return self.description

    def setDisabled(self, value: bool):
        self.disabled = value

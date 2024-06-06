# -*- coding: utf-8 -*-
# author:liuxiaodong 
# contact: 2152550864@qq.com
# datetime:2021/5/17 10:20
# software: PyCharm
# python versions: Python3.7
# file: selectmultiple.py
# license: (C)Copyright 2019-2021 liuxiaodong
from ipywidgets.widgets import SelectMultiple



class PIESelectMultiple(SelectMultiple):
    def __init__(self):
        super(PIESelectMultiple, self).__init__()
        self.name = "PIESelectMultiple"

    def name(self):
        return self.name

    def setOptions(self, value:list):
        self.options = value

    def getOptions(self):
        return self.options

    def setValue(self, value):
        self.value = value

    def setDescription(self, value):
        self.description = value

    def getDescription(self):
        return self.description

    def setDisabled(self, value:bool):
        self.disabled = value
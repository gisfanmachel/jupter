# -*- coding: utf-8 -*-
# author:liuxiaodong 
# contact: 2152550864@qq.com
# datetime:2021/5/14 14:02
# software: PyCharm
# python versions: Python3.7
# file: combobox.py
# license: (C)Copyright 2019-2021 liuxiaodong
from ipywidgets.widgets import Combobox


class PIECombobox(Combobox):
    def __init__(self):
        super(PIECombobox, self).__init__()
        self.name = "PIECombobox"

    def name(self):
        return self.name

    def setValue(self, value):
        self.value = value

    def getValue(self):
        return self.value

    def setPlaceholder(self, value):
        self.placeholder = value

    def getPlaceholder(self):
        return self.placeholder

    def setOptions(self, options:list):
        self.options = options

    def getOptions(self):
        return self.options

    def setDescription(self, value):
        self.description = value

    def getDescription(self):
        return self.description

    def setDisabled(self, value:bool):
        self.disabled = value


# -*- coding: utf-8 -*-
# author:liuxiaodong 
# contact: 2152550864@qq.com
# datetime:2021/5/14 9:36
# software: PyCharm
# python versions: Python3.7
# file: textarea.py
# license: (C)Copyright 2019-2021 liuxiaodong
from ipywidgets.widgets import Textarea

class PIETextArea(Textarea):
    def __init__(self):
        super(PIETextArea, self).__init__()
        self.name = "PIETextArea"

    def name(self):
        return self.name

    def setValue(self, value:str):
        self.value = value

    def getValue(self):
        return self.value

    def setPlaceholder(self, value):
        self.placeholder = value

    def getPlaceholder(self):
        return self.placeholder

    def setDescription(self, value):
        self.description = value

    def getDescription(self):
        return self.description

    def setDisabled(self, value:bool):
        self.disabled = value

    def getDisabled(self):
        return self.disabled

    def onChange(self, callback=None):
        if callback:
            def _callback(change):
                callback(change["new"])
            self.observe(_callback, 'value')




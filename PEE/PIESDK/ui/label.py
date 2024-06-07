# -*- coding: utf-8 -*-
# author:liuxiaodong 
# contact: 2152550864@qq.com
# datetime:2021/5/14 9:27
# software: PyCharm
# python versions: Python3.7
# file: label.py
# license: (C)Copyright 2019-2021 liuxiaodong
from ipywidgets.widgets import Label

class PIELabel(Label):
    def __init__(self):
        super(PIELabel, self).__init__()
        self.name = "PIELabel"

    def name(self):
        return self.name

    def setValue(self, value):
        self.value = value

    def getValue(self):
        return self.value



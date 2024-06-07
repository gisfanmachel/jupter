# -*- coding: utf-8 -*-
# author:liuxiaodong 
# contact: 2152550864@qq.com
# datetime:2021/5/14 14:08
# software: PyCharm
# python versions: Python3.7
# file: box.py
# license: (C)Copyright 2019-2021 liuxiaodong
from ipywidgets.widgets import Box

class PIEBox(Box):
    def __init__(self):
        super(PIEBox, self).__init__()
        self.name = "PIEBox"

    def name(self):
        return self.name

    def setBoxStyle(self, style):
        self.box_style = style

    def getBoxStyle(self):
        return self.box_style

    def setChildren(self, children:list):
        self.children = children

    def getChildren(self):
        return self.children

    def setObserve(self, handler, name=None, type='change'):
        self.observe(handler, name, type)




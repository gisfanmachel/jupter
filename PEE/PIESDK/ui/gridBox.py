# -*- coding: utf-8 -*-
# author:liuxiaodong 
# contact: 2152550864@qq.com
# datetime:2021/5/14 14:18
# software: PyCharm
# python versions: Python3.7
# file: gridbox.py
# license: (C)Copyright 2019-2021 liuxiaodong
from ipywidgets.widgets import GridBox



class PIEGridBox(GridBox):
    def __init__(self):
        super(PIEGridBox, self).__init__()
        self.name = "PIEGridBox"

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

    def setObserve(self, handler, name, type):
        self.observe(handler, name, type)
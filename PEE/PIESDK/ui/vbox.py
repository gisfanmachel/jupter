# -*- coding: utf-8 -*-
# author:liuxiaodong 
# contact: 2152550864@qq.com
# datetime:2021/5/14 9:20
# software: PyCharm
# python versions: Python3.7
# file: vbox.py
# license: (C)Copyright 2019-2021 liuxiaodong
from ipywidgets.widgets import VBox



class PIEVbox(VBox):
    def __init__(self, children=()):
        super(PIEVbox, self).__init__()
        self.name = "PIEVbox"
        self.children = children

    def name(self):
        return self.name

    def setBoxStyle(self, style):
        self.box_style = style

    def getBoxStyle(self):
        return self.box_style

    def setLayout(self, layout):
        self.layout = layout

    def getLayout(self):
        return self.layout

    def setChildren(self, children:list):
        self.children = children

    def getChildren(self):
        return self.children
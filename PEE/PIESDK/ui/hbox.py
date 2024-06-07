# -*- coding: utf-8 -*-
# author:liuxiaodong 
# contact: 2152550864@qq.com
# datetime:2021/5/13 16:59
# software: PyCharm
# python versions: Python3.7
# file: hbox.py
# license: (C)Copyright 2019-2021 liuxiaodong

from ipywidgets.widgets import HBox


class PIEHbox(HBox):
    def __init__(self, children=()):
        super(PIEHbox, self).__init__()
        self.name = "PIEHbox"
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
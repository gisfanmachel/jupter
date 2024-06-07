# -*- coding: utf-8 -*-
# author:liuxiaodong 
# contact: 2152550864@qq.com
# datetime:2021/5/14 15:07
# software: PyCharm
# python versions: Python3.7
# file: layout.py
# license: (C)Copyright 2019-2021 liuxiaodong
from ipywidgets.widgets import Layout



class PIELayout(Layout):
    def __init__(self):
        super(PIELayout, self).__init__()
        self.name = "PIELayout"

    def name(self):
        return self.name

    def setPadding(self, padding:str):
        self.padding = padding

    def setWidth(self, width = None):
        self.width = width

    def setHeight(self, height = None):
        self.height = height

    def setMaxHeight(self, value = None):
        self.max_height = value

    def setMinHeight(self, value = None):
        self.min_height = value

    def setMaxWidth(self, value = None):
        self.max_width = value

    def setMinWidth(self, value = None):
        self.min_width = value

    def setLeft(self, value = None):
        self.left = value

    def setRight(self, value = None):
        self.right = value

    def setTop(self, value = None):
        self.top = value

    def setBottom(self, value = None):
        self.bottom = value

    def setOrder(self, value = None):
        self.order = value


# -*- coding: utf-8 -*-
# author:liuxiaodong 
# contact: 2152550864@qq.com
# datetime:2021/5/14 15:31
# software: PyCharm
# python versions: Python3.7
# file: gridspacelayout.py
# license: (C)Copyright 2019-2021 liuxiaodong
from ipywidgets.widgets import GridspecLayout



class PIEGridspecLayout(GridspecLayout):
    def __init__(self):
        super(PIEGridspecLayout, self).__init__()
        self.name = "PIEGridspecLayout"

    def name(self):
        return self.name

    def setRows(self, value:int):
        self.n_rows = value

    def setColumns(self, value = None):
        self.n_columns = value

    def setHeight(self, value = None):
        self.height = value

    def setWidth(self, value = None):
        self.width = value




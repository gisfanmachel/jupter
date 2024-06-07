# -*- coding: utf-8 -*-
# author:liuxiaodong 
# contact: 2152550864@qq.com
# datetime:2021/5/17 9:53
# software: PyCharm
# python versions: Python3.7
# file: tobbelbuttons.py
# license: (C)Copyright 2019-2021 liuxiaodong
from ipywidgets.widgets import ToggleButton



class PIEToggleButton(ToggleButton):
    def __init__(self):
        super(PIEToggleButton, self).__init__()
        self.name = "PIEToggleButton"

    def name(self):
        return self.name

    def setValue(self, value: bool):
        self.value = value

    def setDescription(self, value: str):
        self.description = value

    def getDescription(self):
        return self.description

    def setDisabled(self, value: bool):
        self.disabled = value

    def setButtonStyle(self, value:str):
        """
        @param value: 'success', 'info', 'warning', 'danger' or ''
        @return:
        """
        self.button_style = value

    def setIcon(self, value:str):
        self.icon = value

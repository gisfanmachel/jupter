# -*- coding: utf-8 -*-
# author:liuxiaodong 
# contact: 2152550864@qq.com
# datetime:2021/5/13 15:10
# software: PyCharm
# python versions: Python3.7
# file: colorpicker.py
# license: (C)Copyright 2019-2020

from ipywidgets.widgets import ColorPicker


class PIEColorPicker(ColorPicker):
    def __init__(self):
        super(PIEColorPicker, self).__init__()
        self.name = "PIEColorPicker"

    def name(self):
        return self.name

    def setConcise(self, concise: bool):
        self.concise = concise

    def getConcise(self):
        return self.concise

    def setValue(self, value):
        self.value = value

    def getValue(self):
        return self.value

    def setDescription(self, description):
        """

        @param description:
        @return:
        """
        self.description = description

    def getDescription(self):
        """

        @return:
        """
        return self.description

    def setDisabled(self, value:bool):
        """

        @param value:
        @return:
        """
        self.disabled = value
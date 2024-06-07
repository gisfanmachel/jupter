# -*- coding: utf-8 -*-
# author:liuxiaodong 
# contact: 2152550864@qq.com
# datetime:2021/5/13 15:46
# software: PyCharm
# python versions: Python3.7
# file: floattext.py
# license: (C)Copyright 2019-2020

from ipywidgets.widgets import FloatText


class PIEFloatText(FloatText):
    def __init__(self):
        super(PIEFloatText, self).__init__()
        self.name = "PIEFloatText"

    def name(self):
        return self.name

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
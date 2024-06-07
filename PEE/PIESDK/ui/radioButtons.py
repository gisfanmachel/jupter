# -*- coding: utf-8 -*-
# author:liuxiaodong 
# contact: 2152550864@qq.com
# datetime:2021/5/13 16:11
# software: PyCharm
# python versions: Python3.7
# file: radiobuttons.py
# license: (C)Copyright 2019-2021 liuxiaodong

from ipywidgets.widgets import RadioButtons


class PIERadioButtons(RadioButtons):
    def __init__(self):
        super(PIERadioButtons, self).__init__()
        self.name = "PIERadioButtons"

    def name(self):
        return self.name

    def setValue(self, value):
        self.value = value

    def getValue(self):
        return self.value

    def setOptions(self, options:list):
        self.options = options

    def getOptions(self):
        return self.options

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
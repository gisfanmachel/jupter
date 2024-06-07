# -*- coding: utf-8 -*-
# author:liuxiaodong 
# contact: 2152550864@qq.com
# datetime:2021/5/13 14:43
# software: PyCharm
# python versions: Python3.7
# file: dropdown.py
# license: (C)Copyright 2019-2020

from ipywidgets.widgets import Dropdown


class PIEDropDown(Dropdown):
    def __init__(self):
        super(PIEDropDown, self).__init__()
        self.name = "PIEDropDown"

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

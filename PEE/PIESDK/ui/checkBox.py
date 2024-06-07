# -*- coding: utf-8 -*-
# author:liuxiaodong 
# contact: 2152550864@qq.com
# datetime:2021/5/13 16:09
# software: PyCharm
# python versions: Python3.7
# file: checkbox.py
# license: (C)Copyright 2019-2021 liuxiaodong

from ipywidgets.widgets import Checkbox


class PIECheckbox(Checkbox):
    def __init__(self):
        super(PIECheckbox, self).__init__()
        self.name = "PIECheckbox"

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

    def setIndent(self, value: bool):
        self.indent = value

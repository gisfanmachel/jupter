# -*- coding: utf-8 -*-
# author:liuxiaodong 
# contact: 2152550864@qq.com
# datetime:2021/5/13 14:37
# software: PyCharm
# python versions: Python3.7
# file: text.py
# license: (C)Copyright 2019-2020

from ipywidgets.widgets import Text


class PIEText(Text):
    def __init__(self):
        super(PIEText, self).__init__()
        self.name = "PIEText"

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

    def getPlaceholder(self):
        """

        @return:
        """
        return self.placeholder

    def setPlaceholder(self, value):
        """

        @param value:
        @return:
        """

        self.placeholder = value

    def onChange(self, callback=None):
        if callback:
            def _callback(change):
                callback(change["new"])
            self.observe(_callback, 'value')
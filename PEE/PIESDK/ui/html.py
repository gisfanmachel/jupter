# -*- coding: utf-8 -*-
# author:liuxiaodong 
# contact: 2152550864@qq.com
# datetime:2021/5/13 14:50
# software: PyCharm
# python versions: Python3.7
# file: html.py
# license: (C)Copyright 2019-2020

from ipywidgets.widgets import HTML


class PIEHTML(HTML):
    def __init__(self):
        super(PIEHTML, self).__init__()
        self.name = PIEHTML

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
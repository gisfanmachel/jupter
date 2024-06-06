# -*- coding: utf-8 -*-
# author:liuxiaodong 
# contact: 2152550864@qq.com
# datetime:2021/5/13 14:18
# software: PyCharm
# python versions: Python3.7
# file: button.py
# license: (C)Copyright 2019-2020

from ipywidgets.widgets import Button

class PIEButton(Button):
    def __init__(self):
        super(PIEButton, self).__init__()
        self.name = "PIEButton"

    def name(self):
        """

        @return:
        """
        return self.name

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

    def setButtonStyle(self, style):
        """

        @param state: 控件显示状态，'success', 'info', 'warning', 'danger', or ''
        @return:
        """
        self.button_style = style

    def getButtonStyle(self):
        """

        @return:
        """
        return self.button_style

    def setToolTip(self, content):
        """

        @param content:
        @return:
        """
        self.tooltip = content

    def getToolTip(self):
        """

        @return:
        """
        return self.tooltip

    def setIcon(self, icon):
        """

        @param icon:
        @return:
        """
        self.icon = icon

    def getIcon(self):
        """

        @return:
        """
        return self.icon

    def onClick(self, callback=None, remove=False):
        """
        @param callback:
        @param remove:
        @return:
        """
        if callback:
            self.on_click(callback, remove)









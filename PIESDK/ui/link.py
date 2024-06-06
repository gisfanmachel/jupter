# -*- coding: utf-8 -*-
# author:liuxiaodong 
# contact: 2152550864@qq.com
# datetime:2021/5/14 15:48
# software: PyCharm
# python versions: Python3.7
# file: link.py
# license: (C)Copyright 2019-2021 liuxiaodong
from ipywidgets.widgets import jslink
from ipywidgets.widgets.widget_link import Link


class PIELink(Link):
    def __init__(self, source, target):
        super(PIELink, self).__init__(source, target)
        self.name = "PIELink"
        self.source = source
        self.target = target

    def name(self):
        return self.name

    def __call__(self):
        return Link(self.source, self.target)

    def unlink(self):
        return self.close()

def jsLink(source, target):
    return PIELink(source, target)




# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   __init__.py.py
@Time    :   2022/7/27 09:51
@Author  :   lishiwei
@Version :   1.0
@Contact :   shi_weihappy@126.com
@License :   (C)Copyright 2021-2022, lishiwei
@Desc    :   None
"""
import os

if os.environ.get("PIE_FOLIUM") == "1":
    from pie.map.piefolium import PIEMap as Map
else:
    from pie.map.pieleaflet import PIEMap as Map

#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "chenxw"
"""
gee python study
Date：2020-12-09
"""
# -*- coding: utf-8 -*-
__author__ = 'gisfanmachel@gmail.com'

import ee
from IPython.display import Image
import os

os.environ['HTTP_PROXY'] = 'http://127.0.0.1:1080'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:1080'

ee.Initialize()
print(ee.Image('USGS/SRTMGL1_003').getInfo())

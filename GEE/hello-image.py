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

# 如果本地是通过代理上网，这里代码设置代理
# 如果直接通过vpn上网，不用设置代理
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:1080'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:1080'

ee.Initialize()
image1 = ee.Image('srtm90_v4')
path = image1.getDownloadUrl({
    'scale': 30,
    'crs': 'EPSG:4326',
    'region': '[[-120, 35], [-119, 35], [-119, 34], [-120, 34]]'
})
# 获取下载地址
print(path)
thumb_url=image1.getThumbURL({
    "crs":"EPSG:4326",
    "min":0,
    "max":5000
})
print(thumb_url)
Image(url=thumb_url)
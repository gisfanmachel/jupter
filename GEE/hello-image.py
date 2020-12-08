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
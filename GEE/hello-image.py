#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = "chenxw"
"""
gee python study
Date：2020-12-09
"""
# -*- coding: utf-8 -*-
__author__ = 'gisfanmachel@gmail.com'

import platform
import uuid

platformType = platform.system().lower()
import ee
from IPython.display import Image
import os
import requests

# 如果本地是通过代理上网，这里代码设置代理
# 如果直接通过vpn上网，不用设置代理
if platformType == "windows":
    os.environ['HTTP_PROXY'] = 'http://127.0.0.1:10809'
    os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:10809'
else:
    os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
    os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
key_path = "C:/license/private-key.json"
# ee.Initialize()
# 通过gloud的服务账号认证
# 这里的认证是python环境的认证
service_account = 'gisfanmachel@ee-gisfanmachel.iam.gserviceaccount.com'
credentials = ee.ServiceAccountCredentials(service_account, key_path)
ee.Initialize(credentials)


def download_file(url, file_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)


# 设置读取的图像数据
image1 = ee.Image('srtm90_v4')
path = image1.getDownloadUrl({
    'scale': 30,
    'crs': 'EPSG:4326',
    'region': '[[-120, 35], [-119, 35], [-119, 34], [-120, 34]]'
})

# 获取图像下载地址
print(path)
file_path = "file_{}.zip".format(uuid.uuid4())
download_file(path, file_path)

# 获取缩略图
thumb_url = image1.getThumbURL({
    "crs": "EPSG:4326",
    "min": 0,
    "max": 5000
})
print(thumb_url)
image_path = "image_{}.jpg".format(uuid.uuid4())  # 本地文件路径和文件名
download_file(thumb_url, image_path)

# 显示图像,在notebook里会起作用
Image(url=thumb_url)

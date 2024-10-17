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

# # 如果本地是通过代理上网，这里代码设置代理
# # 如果直接通过vpn上网，不用设置代理
# if platformType == "windows":
#     os.environ['HTTP_PROXY'] = 'http://127.0.0.1:10809'
#     os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:10809'
# else:
#     os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
#     os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
#
key_path = "C:/license/private-key.json"
# # 通过gloud的服务账号认证
# service_account = 'gisfanmachel@ee-gisfanmachel.iam.gserviceaccount.com'
# credentials = ee.ServiceAccountCredentials(service_account, key_path)
# ee.Initialize(credentials)

import subprocess

# 定义本地文件路径和 GEE 资产 ID
local_tif = 'c:/data/boat_region1.tif'  # 本地的 .tif 文件路径

# legacy assets
# asset_id = 'users/gisfanmachel/your_asset_name'  # 目标资产 ID

# cloud assets
asset_id = 'projects/ee-gisfanmachel2/assets/boat_region1'  # 目标资产 ID

# 构建设置代理的命令
if platformType == "windows":
    proxy_command = ["set", "http_proxy=http://127.0.0.1:10809"]
    proxy2_command = ["export", "https_proxy=http://127.0.0.1:10809"]
else:
    proxy_command = ["set", "http_proxy=http://127.0.0.1:7890"]
    proxy2_command = ["set", "https_proxy=http://127.0.0.1:7890"]

if platformType == "windows":
    earthengine_exe_path = "C:/Users/63241/miniconda3/envs/django422_py310/Scripts/earthengine"
else:
    earthengine_exe_path = "/usr/local/bin/earthengine"
# 构建gee认证的命令
# 需要切换到安装了 earthengine-api 的目录下
# c:/Users/63241/miniconda3/envs/django422_py310/Scripts/earthengine --service_account_file=C:/license/private-key.json authenticate --quiet
# earthengine authenticate
authenticate_command = [
    earthengine_exe_path, 'authenticate', '--quiet',
    '--service_account_file=' + key_path
]

# c:/Users/63241/miniconda3/envs/django422_py310/Scripts/earthengine upload image --asset_id=projects/ee-gisfanmachel2/assets/boat_region1 c:/data/boat_region1.tif
# 构建 earthengine upload image 命令
upload_command = [
    earthengine_exe_path, 'upload', 'image',
    '--asset_id=' + asset_id,
    local_tif
]

# 执行命令行上传
try:
    subprocess.run(proxy_command, check=True)
    subprocess.run(proxy2_command, check=True)
    subprocess.run(authenticate_command, check=True)
    subprocess.run(upload_command, check=True)
    print(f"Successfully uploaded {local_tif} to {asset_id}")
except subprocess.CalledProcessError as e:
    print(f"Error occurred: {e}")

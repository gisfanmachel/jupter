# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   pieHttp.py
@Time    :   2020/8/2 上午11:11
@Author  :   lsw
@Version :   1.0
@Contact :   shi_weihappy@126.com
@License :   (C)Copyright 2019-2020, lsw
@Desc    :   None
"""
import os
import json
import requests
from hashlib import md5
import datetime
import time
import uuid
from getpass import getpass
from pie.utils.config import config
from pie.utils.error import ConfigInitError, LoginFailError

def getHeaders(x_api, x_token=None):
    """
    获取头文件信息
    :param x_api:
    :param x_token:
    :return:
    """
    if not x_api:
        return None
    # 网关请求API
    # 请求参数-网关的版本
    # 网关请求AppId
    # 请求头时间戳
    headers = {
        'x-api': x_api,
        'x-gw-version': "2",
        'x-host-app-id': "engine",
        'x-app': "sKEBZOCL7RNk3LVRelo9",
        "Content-Type": "application/json;charset=UTF-8"
    }
    datestr = str(int(time.mktime(datetime.datetime.now().timetuple()) * 1000))
    headers['x-ts'] = datestr
    # UUID值
    _uuid = str(uuid.uuid4())
    headers['x-nonce'] = _uuid
    # WEB, IOS，ANDROID，IPAD，WINDOWS，MAC
    headers['x-client'] = "WEB"
    # 请求环境：TEST(测试)、PRE（预发）、PROD（生产, 不传时的默认值
    headers['x-stage'] = "PROD"
    # 设备ID，该值在启用了加解密插件功能时需要（非必填）
    headers['x-did'] = ""
    # App版本号，在移动端app接入时需要，后期会配合灰度插件使用（非必填）
    headers['x-app-version'] = ""
    # 只在网关开启对应api的t验证token开关时需要（非必填）
    # 需要参与签名的头信息，用英文逗号分隔，公共参数都需要参与签名（非必填）
    # 签名值（非必填）
    x_sign = f"2&sKEBZOCL7RNk3LVRelo9&54ae8cc80be247ca8d8d8c1e7f678b05&{x_api}&{datestr}&{_uuid}&WEB"
    if x_token:
        headers['x-token'] = x_token
        headers['x-sign-headers'] = "x-token"
        headers['x-sign'] = md5(f"{x_sign}&{x_token}".encode('utf8')).hexdigest()
    else:
        headers['x-token'] = ""
        headers['x-sign-headers'] = ""
        headers['x-sign'] = md5(x_sign.encode('utf8')).hexdigest()
    return headers

def GET(urlInfo, params=None, headers=None):
    """
    封装的GET方法
    :param urlInfo:
    :param params:
    :param headers:
    :return:
    """
    url = urlInfo.get("url")
    x_api = urlInfo.get("x-api")
    try:
        if not headers:
            headers = getHeaders(x_api, getCredentials())
        if params:
            if isinstance(params, str):
                params = json.loads(params)
            response = requests.get(
                url=url,
                params=params,
                headers=headers
            )
        else:
            response = requests.get(
                url=url,
                headers=headers
            )
        status_code = response.status_code
        # print("GET response data", response)
        if status_code == 200 or status_code == 201:
            return response.json()
        elif status_code == 401:
            if reLogin():
                headers = getHeaders(x_api, getCredentials())
                return GET(urlInfo, params, headers)
            else:
                return None
    except Exception as e:
        print("GET error is: {}".format(e))
        return None

def POST(urlInfo, params=None, headers=None):
    """
    封装的POST方法
    :param urlInfo:
    :param params:
    :param headers:
    :return:
    """
    url = urlInfo.get("url")
    x_api = urlInfo.get("x-api")
    try:
        if not headers:
            headers = getHeaders(x_api, getCredentials())
        if params:
            response = requests.post(
                url=url,
                json=params,
                headers=headers
            )
        else:
            response = requests.post(
                url=url,
                headers=headers
            )
        status_code = response.status_code
        if status_code == 200 or status_code == 201:
            return response.json()
        elif status_code == 401:
            print(response.json().get("message"))
            if reLogin():
                headers = getHeaders(x_api, getCredentials())
                return POST(urlInfo, params, headers)
            else:
                return None
    except Exception as e:
        print("POST error is: {}".format(e))
        return None

def PUT(urlInfo, params=None, headers=None):
    """
    封装的PUT方法
    :param urlInfo:
    :param params:
    :param headers:
    :return:
    """
    url = urlInfo.get("url")
    x_api = urlInfo.get("x-api")
    try:
        if not headers:
            headers = getHeaders(x_api, getCredentials())
        if params:
            if isinstance(params, dict):
                params = json.dumps(params)
            response = requests.put(
                url=url,
                data=params,
                headers=headers
            )
        else:
            response = requests.put(
                url=url,
                headers=headers
            )
        status_code = response.status_code
        if status_code == 200 or status_code == 201:
            return response.json()
        elif status_code == 401:
            if reLogin():
                headers = getHeaders(x_api, getCredentials())
                return PUT(urlInfo, params, headers)
            else:
                return None
    except Exception as e:
        print("PUT error is: {}".format(e))
        return None

def DELETE(urlInfo, params=None, headers=None):
    """
    封装的DELETE方法
    :param urlInfo:
    :param params:
    :param headers:
    :return:
    """
    url = urlInfo.get("url")
    x_api = urlInfo.get("x-api")
    try:
        if not headers:
            headers = getHeaders(x_api, getCredentials())
        if params:
            if isinstance(params, dict):
                params = json.dumps(params)
            response = requests.delete(
                url=url,
                data=params,
                headers=headers
            )
        else:
            response = requests.delete(
                url=url,
                headers=headers
            )
        status_code = response.status_code
        print("DELETE response data", response)
        if status_code == 200 or status_code == 201:
            return response.json()
        elif status_code == 401:
            if reLogin():
                headers = getHeaders(x_api, getCredentials())
                return DELETE(urlInfo, params, headers)
            else:
                return None
    except Exception as e:
        print("PUT error is: {}".format(e))
        return None

def loginByUser(name=None, password=None):
    """
    通过用户名密码登录
    :param name:
    :param password:
    :return:
    """
    if name is None or password is None:
        raise LoginFailError()

    _login_url = config.getLoginURL()
    _credentials_file = config.getCredentialsFile()
    _user_file = config.getUserFile()
    if not _login_url or not _credentials_file or not _user_file:
        raise ConfigInitError()

    _credentials_file = config.getCredentialsFile()
    _user_file = config.getUserFile()
    if os.path.exists(_credentials_file):
        os.remove(_credentials_file)
    if os.path.exists(_user_file):
        os.remove(_user_file)
    params = {
        "appKey": "vESyouczCS3mTKZ2oyo4O",
        "loginAccount": name,
        "password": md5(password.encode('utf8')).hexdigest()
    }
    response = POST(urlInfo=_login_url,
                    params=params,
                    headers=getHeaders(_login_url.get("x-api")))
    if response:
        _data = response.get("data", {})
        if not _data:
            raise LoginFailError()
        token = _data.get("token", None)
        teamInfoResp = _data.get("teamInfoResp", [])
        if len(teamInfoResp) > 0:
            teamId = teamInfoResp[0].get("teamId", None)
        else:
            teamId = None
        if not token:
            raise LoginFailError()
        _storageToken(token, _credentials_file)
        _storageUserInfo(name, password, teamId, _user_file)
    else:
        raise LoginFailError()

def loginByAuth(isNew=False):
    """
    通过鉴权登录
    :param isNew:
    :return:
    """
    _login_url = config.getLoginURL()
    _credentials_file = config.getCredentialsFile()
    _user_file = config.getUserFile()
    if not _login_url or not _credentials_file or not _user_file:
        raise ConfigInitError()

    if isNew:
        name = input("请输入用户名称：")
        password = getpass("请输入用户密码：")
    else:
        name = None
        password = None
    if checkCredentials(name, password):
        return

    if not isNew and reLogin():
        return

    if name is None or password is None:
        name = input("请输入用户名称：")
        password = getpass("请输入用户密码：")

    loginByUser(name, password)

def login(isNew=False, name=None, password=None):
    """
    登录接口
    :param isNew:
    :param name:
    :param password:
    :return:
    """
    if name is None or password is None:
        loginByAuth(isNew)
    else:
        loginByUser(name, password)


def reLogin():
    """
    重新登录接口
    :return:
    """
    _login_url = config.getLoginURL()
    _credentials_file = config.getCredentialsFile()
    _user_file = config.getUserFile()
    if not _login_url or not _credentials_file or not _user_file:
        raise ConfigInitError()
    user = getUserInfo()
    if os.path.exists(_credentials_file):
        os.remove(_credentials_file)
    if os.path.exists(_user_file):
        os.remove(_user_file)
    if not user:
        return None
    name = user.get("name", None)
    password = user.get("password", None)
    params = {
        "appKey": "vESyouczCS3mTKZ2oyo4O",
        "loginAccount": name,
        "password": md5(password.encode('utf8')).hexdigest()
    }
    response = POST(urlInfo=_login_url,
                   params=params,
                   headers=getHeaders(_login_url.get("x-api")))
    if response:
        _data = response.get("data", {})
        if not _data:
            _data = {}
        token = _data.get("token", None)
        if not token:
            raise LoginFailError()
        _storageToken(token, _credentials_file)
        teamInfoResp = _data.get("teamInfoResp", [])
        if len(teamInfoResp) > 0:
            teamId = teamInfoResp[0].get("teamId", None)
        else:
            teamId = None
        _storageUserInfo(name, password, teamId, _user_file)
        return True
    else:
        raise LoginFailError()

def _storageToken(token, credentials_file):
    """
    存储token信息
    :param token:
    :param credentials_file:
    :return:
    """
    if os.path.exists(credentials_file):
        os.remove(credentials_file)
    credentials_path = os.path.dirname(credentials_file)
    if not os.path.exists(credentials_path):
        os.makedirs(credentials_path)
    with open(credentials_file, "w+", encoding="UTF-8") as f:
        # print("write : {}".format(token))
        f.write(token)

def _storageUserInfo(name, password, teamId, user_file):
    """
    存储用户信息
    :param name:
    :param password:
    :param teamId:
    :param user_file
    :return:
    """
    if os.path.exists(user_file):
        os.remove(user_file)
    user_path = os.path.dirname(user_file)
    if not os.path.exists(user_path):
        os.makedirs(user_path)
    with open(user_file, "w+",  encoding="UTF-8") as f:
        print(f"登录的用户是: {name}")
        f.write(f"{name}\n{password}\n{teamId}")

def getUserInfo():
    """
    获取本地存储的用户信息
    :return:
    """
    _user_file = config.getUserFile()
    if os.path.exists(_user_file):
        try:
            with open(_user_file, "r", encoding="UTF-8") as f:
                lines = f.readlines()
                if len(lines) < 3:
                    print("local user file is wrong!")
                    return None
            return {
                "name": lines[0].strip("\n"),
                "password": lines[1].strip("\n"),
                "teamId": lines[2].strip("\n")
            }
        except Exception as e:
            print("open file fail, error is: {}".format(e))
            return None
    else:
        return None

def getCredentials():
    """
    获取本地验证信息
    :return:
    """
    _credentials_file = config.getCredentialsFile()

    if os.path.exists(_credentials_file):
        try:
            with open(_credentials_file, "r", encoding="UTF-8") as f:
                _credentials = f.read().strip("\n")
            return _credentials
        except Exception as e:
            print("open file fail, error is: {}".format(e))
            return None
    else:
        return None

def checkCredentials(name=None, password=None):
    """
    检测本地的验证信息是否合法
    :param name:
    :param password:
    :return:
    """
    if name is not None and password is not None:
        return False
    return _checkToken()
    
def _checkToken():
    """
    检查Token是否有效
    :return:
    """
    _token = getCredentials()
    if not _token:
        return False
    _check_url = config.getCheckURL()
    body = {
        "appId": "sKEBZOCL7RNk3LVRelo9",
        "accessToken": _token
    }
    response = POST(_check_url, params=body)
    if not response:
        return False
    return int(response.get("code", -1)) == 0

def _refreshToken():
    """
    刷新Token
    :return:
    """
    _refresh_url = config.getRefreshURL()
    response = GET(_refresh_url)
    if not response or not response.get("data", None):
        return False
    _credentials_file = config.getCredentialsFile()
    _storageToken(response.data, _credentials_file)
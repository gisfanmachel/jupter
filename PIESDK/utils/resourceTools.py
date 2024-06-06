# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   resourceTools.py
@Time    :   2022/1/28 10:59
@Author  :   lishiwei
@Version :   1.0
@Contact :   shi_weihappy@126.com
@License :   (C)Copyright 2020-2021, lishiwei
@Desc    :   None
"""
from pie.utils.config import config
from pie.utils.pieHttp import GET, getCredentials, POST


def getUserAssets():
    """
    查询用户的个人资源
    :return:
    """
    urlInfo = config.getQueryCatalogURL()
    def recur_get(url_Info):
        result = GET(url_Info)
        _result = []
        _code = result.get("code")
        if _code != 0:
            return _result
        _data = result.get("data", [])
        for d in _data:
            _type = d.get("type")
            if _type == 1:
                _uuid = d.get("uuid")
                _url = urlInfo.get("url") + "?" + "parentId={}".format(_uuid)
                _urlInfo = {"url": _url, "x-api": urlInfo.get("x-api")}
                _result.extend(recur_get(_urlInfo))
            elif _type == 2 or _type == 3 or _type == 4:
                _result.append(d)
        return _result
    return recur_get(urlInfo)

def getUserAllAssets():
    """
    查询用户的个人资源包括目录
    :return:
    """
    urlInfo = config.getQueryCatalogURL()
    def recur_get(url_Info):
        result = GET(url_Info)
        _result = []
        _code = result.get("code")
        if _code != 0:
            return _result
        _data = result.get("data", [])
        for d in _data:
            _type = d.get("type")
            if _type == 1:
                _uuid = d.get("uuid")
                _url = urlInfo.get("url") + "?" + "parentId={}".format(_uuid)
                _urlInfo = {"url": _url, "x-api": urlInfo.get("x-api")}
                _result.append(d)
                _result.extend(recur_get(_urlInfo))
            elif _type == 2 or _type == 3 or _type == 4:
                _result.append(d)
        return _result
    return recur_get(urlInfo)

def checkStorageFiles(paths):
    """
    检测资源地址是否存在
    :param paths:
    :return:
    """
    # 获取文件列表
    data_list = getUserAssets()
    _exist_file = {}
    for _data in data_list:
        _fullPath = _data.get("fullPath")
        _fullPathList = _fullPath.split("/")
        _exist_file["/".join(_fullPathList[2:])] = 1
    _info = {}
    for _path in paths:
        if _path in _exist_file:
            _info[_path] = 1
        else:
            _info[_path] = 0
    return _info

def checkStorageFileIsExist(path):
    # 获取文件列表
    data_list = getUserAllAssets()
    _exist_file = {}
    for _data in data_list:
        _fullPath = _data.get("fullPath")
        _fullPathList = _fullPath.split("/")
        _exist_file["/".join(_fullPathList[2:])] = 1
    return path in _exist_file

def generateStorageURLs(paths):
    """
    生成下载资源的链接地址
    :param paths:
    :return:
    """
    # 获取文件列表
    data_list = getUserAssets()
    _exist_file = {}
    for _data in data_list:
        _fullPath = _data.get("fullPath")
        _fullPathList = _fullPath.split("/")
        _exist_file["/".join(_fullPathList[2:])] = _data

    # 查询指定文件的ID
    _fileSize = 0
    _uuids = []
    _info = {}
    for _path in paths:
        if _path in _exist_file:
            _data = _exist_file[_path]
            _fileSize += float(_data.get("fileSize", 0))
            _uuid = _data.get("uuid")
            _uuids.append(_uuid)
            _info[_uuid] = _path
    # 查询是否有足够的下载资源
    url = config.getUserResourceStorageURL()
    result = GET(url)
    _data = result.get("data", {})
    _code = result.get("code")
    if _code != 0:
        print("查询用户资源流量失败")
        return []
    _notUseDownload = _data.get("notUseDownload", -1)
    if _notUseDownload < _fileSize:
        print("没有足够的流量下载资源")
        return []

    url = config.getUserResourceUriURL()
    _urls = []
    for _uuid in _uuids:
        _url = url.get("url").format(uuid=_uuid, token=getCredentials())
        result = GET({
            "url": _url,
            "x-api": url.get("x-api")
        })
        _data = result.get("data", "")
        _code = result.get("code")
        if _code != 0:
            print("查询不到指定的数据")
            continue
        _urls.append({
            "file": _info.get(_uuid),
            "url": _data
        })
    return _urls


def insertNewFolder(path):
    if not path or path == "/":
        return "0"
    
    data_list = getUserAllAssets()
    exist_list = {}
    for _data in data_list:
        #只保留目录
        if _data.get("type") == 1:
            _fullPath = _data["fullPath"]
            _fullPathList = _fullPath.split("/")
            exist_list["/".join(_fullPathList[2:])] = _data
    _data = exist_list.get(path)
    if _data:
        return _data["uuid"]

    _path_list = path.split("/")
    _new_folder_list = []
    _parentId = None
    for i in range(len(_path_list)):
        _key = "/".join(_path_list[:i+1])
        _data = exist_list.get(_key)
        if _data:
            _parentId = _data.get("uuid")
            continue
        _new_folder_list.append(_path_list[i])

    for _folder in _new_folder_list:
        _url = config.insertCatalogURL()
        _params = {
            "name": _folder,
            "description": _folder,
            "isPublic": 0,
            "type": 1,
            "parentId": _parentId,
        }
        response = POST(urlInfo=_url, params=_params)
        if response:
            _parentId = response.get("data")
    return _parentId
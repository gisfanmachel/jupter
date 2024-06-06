# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   taskTools.py
@Time    :   2022/1/28 14:18
@Author  :   lishiwei
@Version :   1.0
@Contact :   shi_weihappy@126.com
@License :   (C)Copyright 2020-2021, lishiwei
@Desc    :   None
"""
from pie.utils.config import config
from pie.utils.pieHttp import GET, POST, DELETE

def getTaskList():
    """
    :return:
    """
    url = config.getTaskListURL()
    result = GET(url)
    _code = result.get("code")
    if _code != 0:
        print(f"获取任务列表详细信息失败！")
        return None
    _datas = result.get("data", [])
    _newDatas = []
    for _data in _datas:
        _newDatas.append({
            "taskId": _data.get("taskId"),
            "description": _data.get("description"),
            "createTime": _data.get("createTime"),
            "updateTime": _data.get("updateTime"),
            "startTime": _data.get("startTime"),
            "type": _data.get("type"),
            "status": _data.get("status"),
            "progress": _data.get("progress"),
            "message": _data.get("message")
        })
    return _newDatas

def getTaskDetail(taskId):
    """
    :param taskId:
    :return:
    """
    url = config.getTaskDetailURL()
    result = GET({
        "url": url.get("url").format(taskId=taskId),
        "x-api": url.get("x-api")
    })
    _data = result.get("data", {})
    _code = result.get("code")
    if _code != 0:
        print(f"获取任务{taskId}详细信息失败！")
        return None
    return {
        "taskId": _data.get("taskId"),
        "description": _data.get("description"),
        "createTime": _data.get("createTime"),
        "updateTime": _data.get("updateTime"),
        "startTime": _data.get("startTime"),
        "type": _data.get("type"),
        "status": _data.get("status"),
        "message": _data.get("message")
    }

def cancelTask(taskId):
    """

    :param taskId:
    :return:
    """
    url = config.getCancelTaskURL()
    result = POST({
        "url": url.get("url").format(taskId=taskId),
        "x-api": url.get("x-api")
    })
    _code = result.get("code")
    if _code != 0:
        print(f"取消任务{taskId}失败！")
        return None
    _data = result.get("data", {})
    return _data

def clearTask():
    """
    :return:
    """
    url = config.getClearTaskURL()
    result = DELETE(url)
    _code = result.get("code")
    if _code != 0:
        print(f"清空任务失败！")
        return None
    _data = result.get("data", {})
    return _data
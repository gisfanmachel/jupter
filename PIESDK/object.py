# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   object.py
@Time    :   2020/8/4 下午5:24
@Author  :   lsw
@Version :   1.0
@Contact :   shi_weihappy@126.com
@License :   (C)Copyright 2019-2020, lsw
@Desc    :   None
"""
from pie.utils.config import config
from pie.utils.common import encodeURIComponent, encodeJSON, decodeJSON
from pie.utils.pieHttp import POST
from pie.utils.polyline_geojson import decodeGeoJSON

def _generatePIEObject(pre, statement):
    """
    生成 PIEObject 对象
    :param pre:
    :param statement:
    :return:
    """
    _object = PIEObject()
    _object.pre = pre
    _object.statement = statement
    return _object

class PIEObject(object):
    """
    基本对象类
    """
    def __init__(self):
        super(PIEObject, self).__init__()
        self._statement = None
        self._pre = None
        self._print_url = config.getPrintURL()
        self._compute_url = config.getComputeURL()

    @property
    def statement(self):
        return self._statement

    @statement.setter
    def statement(self, value):
        self._statement = value

    @property
    def pre(self):
        return self._pre

    @pre.setter
    def pre(self, value):
        self._pre = value

    @staticmethod
    def name():
        """
        获取类的名称
        :return:
        """
        return "PIEObject"

    @staticmethod
    def formatValue(value):
        if isinstance(value, PIEObject):
            return value.statement
        else:
            return value

    def getStatement(self, functionName=None, arguments=None, compute=False, function=None, compress=None):
        """
        获取配置信息
        :param functionName:
        :param arguments:
        :param compute:
        :param function:
        :param compress:
        :return:
        """
        if arguments is None:
            arguments = {"input": self.statement}
        _obj = {
            "type": "Invocation",
            "arguments": arguments
        }
        if functionName:
            _obj["functionName"] = functionName
        if function:
            _obj["function"] = function
        if compute:
            _obj["pTag"] = "c"
        if compress:
            _obj["compress"] = compress
        return _obj

    def getInfo(self, callback=None):
        """
        获取Python可用的真实数据
        :param callback:
        :return:
        """
        if not self.statement:
            print("数据错误")
            return None
        _url = self._print_url
        if self.statement.get("pTag", None) == "c":
            _url = self._compute_url
        else:
            _pre = self.pre
            while _pre:
                _pre_statement = _pre.statement
                if _pre_statement and _pre_statement.get("pTag", None) == "c":
                    _url = self._compute_url
                _pre = _pre.pre
        statement = encodeJSON(self.statement)
        statement = encodeURIComponent(statement)
        response = POST(urlInfo=_url, params={"statement": statement})
        result = None
        compress = self.statement.get("compress", None)
        if response.get("message", None) == "success" \
            and response.get("code", None) == 0:
            data = response.get("data", None)
            if compress == "polyline":
                if isinstance(data, str):
                    result = decodeGeoJSON(decodeJSON(data))
                elif isinstance(data, list) or isinstance(data, tuple):
                    result = []
                    for d in data:
                        if isinstance(d, str):
                            result.append(decodeGeoJSON(decodeJSON(d)))
                        else:
                            result.append(d)
                elif isinstance(data, dict):
                    result = {}
                    for (k, v) in data.items():
                        result[k] = decodeGeoJSON(decodeJSON(v))
            else:
                result = data
        if callback:
            callback(result)
        return result

    def serialize(self):
        """
        序列化对象
        :return:
        """
        return encodeJSON(self.statement)

    def toString(self):
        """
        对象转为字符串
        :return:
        """
        return encodeJSON(self.statement)
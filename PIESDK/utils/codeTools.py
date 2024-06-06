# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   codeTools.py
@Time    :   2021/12/30 12:31
@Author  :   lishiwei
@Version :   1.0
@Contact :   shi_weihappy@126.com
@License :   (C)Copyright 2020-2021, lishiwei
@Desc    :   None
"""
from IPython.display import Javascript
import urllib.parse
from pie.utils.config import config
from pie.utils.pieHttp import POST
from pie.utils.common import encodeURIComponent, encodeJSON

def parseCell(index):
    index = str(index)
    return Javascript("const code = Jupyter.notebook.get_cell(parseInt("+index+")).get_text(); IPython.notebook.kernel.execute(`pieCode = '${encodeURI(code)}'`);")

def generateLink(pieCode):
    """
    生成指定cell的代码链接
    :param pieCode:
    :return:
    """
    code = urllib.parse.unquote(pieCode)
    urlInfo = config.getSaveShareCode()
    content = encodeURIComponent(encodeJSON(code))
    params = {
        "content": content,
        "picture": "",
        "description": "分享代码",
        "isPublic": True,
    }
    response = POST(urlInfo=urlInfo, params=params)
    shareURL = None
    if response:
        _data = response.get("data", {})
        _id = _data.get("id")
        shareURL = f"https://engine.piesat.cn/engine-share/shareCode.html?id={_id}"
    return shareURL

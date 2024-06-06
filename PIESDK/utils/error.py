# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   error.py
@Time    :   2020/8/5 下午2:27
@Author  :   lsw
@Version :   1.0
@Contact :   shi_weihappy@126.com
@License :   (C)Copyright 2019-2020, lsw
@Desc    :   None
"""

class PIEBaseException(Exception):
    def __init__(self, msg=None):
        super(PIEBaseException, self).__init__()
        self.msg = msg

    def __str__(self):
        return self.msg

class LoginFailError(PIEBaseException):
    """
    登录失败异常
    """
    def __init__(self, msg=None):
        super(LoginFailError, self).__init__(msg)
        if not msg:
            self.msg = "用户名和密码不匹配！"

class ConfigInitError(PIEBaseException):
    """
    配置初始化的异常
    """
    def __init__(self, msg=None):
        super(ConfigInitError, self).__init__(msg)
        if not msg:
            self.msg = "配置初始化异常！"

class CredentialsLostError(PIEBaseException):
    """
    缺少验证文件
    """
    def __init__(self, msg=None):
        super(CredentialsLostError, self).__init__(msg)
        if not msg:
            self.msg = "验证文件初始化异常！"

class ArgsIsNull(PIEBaseException):
    """
    输入的参数为空
    """
    def __init__(self, value = None):
        super(ArgsIsNull, self).__init__()
        if value is None:
            self.msg = "输入的参数不能为空！"
        else:
            self.msg = f"输入的参数 {value} 不能为空！"

class ArgsTypeIsWrong(PIEBaseException):
    """
    输入的参数类型错误
    """
    def __init__(self, msg = None):
        super(ArgsTypeIsWrong, self).__init__(msg)
        if not msg:
            self.msg = "输入的参数类型不正确！"

class ArgsRangeIsError(PIEBaseException):
    """
    输入的参数值范围不正确
    """
    def __init__(self, value = None):
        super(ArgsRangeIsError, self).__init__()
        if value is None:
            self.msg = "输入的参数值范围不正确！"
        else:
            self.msg = f"输入的参数 {value} 范围不正确！"

class NotFoundValue(PIEBaseException):
    """
    查找不到指定的数据
    """
    def __init__(self, msg = None):
        super(NotFoundValue, self).__init__(msg)
        if not msg:
            self.msg = "查找不到指定的数据！"

class FileIsExist(PIEBaseException):
    """
    文件已经存在
    """
    def __init__(self, value = None):
        super(FileIsExist, self).__init__(value)
        if value is None:
            self.msg = f"文件已经存在！"
        else:
            self.msg = f"文件 {value} 已经存在！"

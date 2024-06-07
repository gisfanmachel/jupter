# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/_jsuperpy\data\ex.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 1589 bytes
__all__ = [
 "DatasourceReadOnlyError", "DatasourceOpenedFailedError", "ObjectDisposedError",
 "DatasourceCreatedFailedError"]

class DatasourceReadOnlyError(Exception):
    __doc__ = "\n    数据源为只读时的异常。在进行某些功能需要写入数据到数据源或修改数据源中数据，而数据源为只读时将会返回该异常信息。\n    "

    def __init__(self, message):
        Exception.__init__(self)
        self.message = "The data source is read-only and cannot write data : %s " % message

    def __str__(self):
        return self.message

    __repr__ = __str__


class DatasourceOpenedFailedError(Exception):
    __doc__ = "数据源打开失败异常"

    def __init__(self, message):
        Exception.__init__(self)
        self.message = "Failed to open the data source : %s" % message

    def __str__(self):
        return self.message

    __repr__ = __str__


class DatasourceCreatedFailedError(Exception):
    __doc__ = "数据源创建失败异常"

    def __init__(self, message):
        Exception.__init__(self)
        self.message = "Failed to create the data source : %s" % message

    def __str__(self):
        return self.message

    __repr__ = __str__


class ObjectDisposedError(RuntimeError):
    __doc__ = "\n    对象被释放后的异常对象。在检查 Python 实例中绑定的 java 对象被释放后会抛出该异常。\n    "

    def __init__(self, message):
        RuntimeError.__init__(self)
        self.message = "%s has been disposed." % message

    def __str__(self):
        return self.message

    __repr__ = __str__

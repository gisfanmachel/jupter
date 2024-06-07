# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/_jsuperpy\data\_jvm.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 602 bytes
from .._gateway import get_jvm

class JVMBase(object):

    def __init__(self):
        self._jvm = get_jvm()
        self._java_object = None

    @property
    def _jobject(self):
        """Py4J 映射的 Java 对象"""
        if self._java_object is None:
            self._java_object = self._make_java_object()
        return self._java_object

    def _make_java_object(self):
        pass

    @classmethod
    def _get_object_handle(cls, java_object):
        if java_object is None:
            return 0
        return get_jvm().com.supermap.data.InternalHandleHelper.getHandle(java_object)

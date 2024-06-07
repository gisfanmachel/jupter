# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/_version.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 303 bytes


def get_version():
    return "10.1.0.0"


def is_objects_java_release():
    try:
        from . import _jsuperpy as supermap
    except ImportError as e:
        try:
            from . import _csuperpy as supermap
        finally:
            e = None
            del e

    if supermap.internal_tag() == "iobjects-java":
        return True
    return False

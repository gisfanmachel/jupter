# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/_locales\__init__.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 4823 bytes
from .conf import *
import inspect
__all__ = [
 "i18n"]

class _Translater:

    def __init__(self):
        import importlib
        try:
            l_module = importlib.import_module(language_module)
            self._translate = getattr(l_module, locale_member_name)
        except:
            self._translate = {}

    def translate(self, key: str, default_value):
        return self._translate.get(key, default_value)


class _TranslateKeyBuilder:

    def __init__(self):
        self._module_name = None
        self._clz_name = None
        self._method_name = None

    def module_name(self, module_name: str):
        self._module_name = module_name
        self._clz_name = None
        self._method_name = None

    def clz_name(self, clz_name: str):
        self._clz_name = clz_name
        self._method_name = None

    def method_name(self, method_name: str):
        self._method_name = method_name

    def get_key(self):
        key = self._module_name
        if hasattr(self, "_clz_name"):
            if self._clz_name is not None:
                key = key + "." + self._clz_name
        if hasattr(self, "_method_name"):
            if self._method_name is not None:
                key = key + "." + self._method_name
        return key


_t_builder = _TranslateKeyBuilder()
_t = _Translater()

def _translate(default_value):
    return _t.translate(_t_builder.get_key(), default_value)


def _is_current_module_member(current_module, member):
    member_module = inspect.getmodule(member)
    return hasattr(member_module, "__name__") and inspect.getmodule(current_module).__name__ == member_module.__name__


def _is_iobjectspy_module(mo):
    mo_module = inspect.getmodule(mo)
    return hasattr(mo_module, "__name__") and "iobjectspy" in mo_module.__name__


def _is_private(obj):
    if hasattr(obj, "__name__"):
        name = getattr(obj, "__name__")
    else:
        name = str(obj)
    if name == "__init__":
        return False
    return name.startswith("_")


def _translate_method_docstrings(method):
    try:
        _t_builder.method_name(method.__name__)
        if not _is_private(method):
            locale_doc = _translate(None)
            if locale_doc is not None:
                if len(locale_doc) > 0:
                    method.__doc__ = locale_doc
    except Exception as e:
        try:
            import traceback
            print("\n".join([method.__name__, traceback.format_exc()]))
        finally:
            e = None
            del e


def _filter_translate_member(parent):

    def verify(item):
        name, member = item
        return not _is_private(name) and _is_iobjectspy_module(member) and _is_current_module_member(parent, member)

    return verify


def _translate_class_docstrings(clz):
    try:
        _t_builder.clz_name(clz.__name__)
        locale_doc = _translate(clz.__doc__)
        if locale_doc is not None:
            if len(locale_doc) > 0:
                clz.__doc__ = locale_doc
        for name, member in list(filter(_filter_translate_member(clz), inspect.getmembers(clz))):
            if inspect.isfunction(member) or inspect.ismethod(member):
                _translate_method_docstrings(member)

    except Exception as e:
        try:
            import traceback
            traceback.print_exc()
        finally:
            e = None
            del e


def _translate_module_docstrings(mo):
    try:
        _t_builder.module_name(mo.__name__)
        locale_doc = _translate(mo.__doc__)
        if locale_doc is not None:
            if len(locale_doc) > 0:
                mo.__doc__ = locale_doc
        for name, member in list(filter(_filter_translate_member(mo), inspect.getmembers(mo))):
            if inspect.isclass(member):
                _translate_class_docstrings(member)

    except Exception as e:
        try:
            import traceback
            traceback.print_exc()
        finally:
            e = None
            del e


import importlib, sys

def _hook_iobjectspy_module(mod):
    if _is_iobjectspy_module(mod):
        if inspect.ismodule(mod):
            _translate_module_docstrings(mod)
        else:
            if inspect.isclass(mod):
                _translate_class_docstrings(mod)
            else:
                if inspect.ismethod(mod):
                    _translate_method_docstrings(mod)
    return mod


class IobjectsPyLoader:

    def load_module(self, fullname):
        iobjectspy_module = importlib.import_module(fullname)
        _hook_iobjectspy_module(iobjectspy_module)
        return iobjectspy_module


class IobjectsPyFinder:

    def __init__(self):
        self._skip = set()
        self._loader = IobjectsPyLoader()

    def find_module(self, fullname, path=None):
        if fullname in self._skip:
            return
        if "iobjectspy" in fullname:
            self._skip.add(fullname)
            return self._loader
        return


def i18n():
    if hook:
        sys.meta_path.insert(0, IobjectsPyFinder())

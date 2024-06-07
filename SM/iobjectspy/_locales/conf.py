# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/_locales\conf.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 1025 bytes
default_language_module = "iobjectspy._locales.iobjectspy"
import importlib, locale
language_all = locale.getdefaultlocale()[0]
language_short = language_all.split("_")[0]
language_short = "en"
try:
    importlib.import_module(default_language_module + "_" + language_all)
    language_module = default_language_module + "_" + language_all
except Exception:
    try:
        importlib.import_module(default_language_module + "_" + language_short)
        language_module = default_language_module + "_" + language_short
    except Exception:
        language_module = default_language_module

import os
hook = os.environ.get("DISABLEICLIENTPYI18N") is None
locale_member_name = "iobjectspy_locale"

# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\analyst\_tabular\base\base_estimater.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 423 bytes
"""
@author: YangRuijie
@license: 
@contact: yangruijie@supermap.com
@software: 
@file: base_estimater.py
@time: 5/21/20 12:28 PM
@desc:
"""

class BaseEstimater:

    def __init__(self):
        pass

    def estimate_line(self, features):
        raise NotImplementedError

    def estimate_file(self, input_data, out_data, out_dataset_name=None):
        raise NotImplementedError

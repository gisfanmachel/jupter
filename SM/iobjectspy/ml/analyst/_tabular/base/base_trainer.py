# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\analyst\_tabular\base\base_trainer.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 484 bytes
"""
@author: YangRuijie
@license: 
@contact: yangruijie@supermap.com
@software: 
@file: base_trainer.py
@time: 5/21/20 12:26 PM
@desc:
"""

class BaseTrainer:

    def __init__(self):
        pass

    def find_best_params(self):
        raise NotImplementedError

    def train(self, train_data_path, config, lr, output_model_path, output_model_name, model_params=None, test_size=0.2, **kwargs):
        raise NotImplementedError

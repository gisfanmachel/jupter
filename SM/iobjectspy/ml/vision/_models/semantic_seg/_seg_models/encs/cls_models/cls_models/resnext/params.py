# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_seg_models\encs\cls_models\cls_models\resnext\params.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 614 bytes


def get_conv_params(**params):
    default_conv_params = {'kernel_initializer':"glorot_uniform", 
     'use_bias':False, 
     'padding':"valid"}
    default_conv_params.update(params)
    return default_conv_params


def get_bn_params(**params):
    default_bn_params = {
     'axis': 3, 
     'momentum': 0.99, 
     'epsilon': 2e-05, 
     'center': True, 
     'scale': True}
    default_bn_params.update(params)
    return default_bn_params

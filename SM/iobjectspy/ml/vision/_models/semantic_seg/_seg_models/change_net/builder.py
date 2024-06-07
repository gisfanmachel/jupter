# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_seg_models\change_net\builder.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 973 bytes
"""
@author: YangRuijie
@license: 
@contact: yangruijie@supermap.com
@software: 
@file: builder.py
@time: 7/23/19 6:35 AM
@desc:
"""
from keras import Model, Input
from keras.layers import Conv2D
from keras.layers import Activation
from keras.layers import Subtract
from ..._seg_models import Unet
from _seg_models.utils import to_tuple, get_layer_number

def build_change_unet(model_extract, input_shape=(None, None, 3), classes=1, activation='sigmoid'):
    inp1 = Input(input_shape)
    inp2 = Input(input_shape)
    model_1 = model_extract(inp1)
    model_2 = model_extract(inp2)
    subtract_layers = Subtract(name="subtract_feature")([model_2, model_1])
    x = Conv2D(classes, (3, 3), padding="same", name="change_conv")(subtract_layers)
    x = Activation(activation, name=activation)(x)
    model = Model(inputs=[inp1, inp2], outputs=x)
    return model

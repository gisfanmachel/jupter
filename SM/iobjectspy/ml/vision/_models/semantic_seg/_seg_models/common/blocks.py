# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_seg_models\common\blocks.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 682 bytes
from keras.layers import Conv2D
from keras.layers import Activation
from keras.layers import BatchNormalization

def Conv2DBlock(n_filters, kernel_size, activation='relu', use_batchnorm=True, name='conv_block', **kwargs):
    """Extension of Conv2D layer with batchnorm"""

    def layer(input_tensor):
        x = Conv2D(n_filters, kernel_size, use_bias=not use_batchnorm, name=name + "_conv", **kwargs)(input_tensor)
        if use_batchnorm:
            x = BatchNormalization(name=(name + "_bn"))(x)
        x = Activation(activation, name=(name + "_" + activation))(x)
        return x

    return layer

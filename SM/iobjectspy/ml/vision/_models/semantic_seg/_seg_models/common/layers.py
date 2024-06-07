# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_seg_models\common\layers.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 3623 bytes
from keras.engine import Layer
from keras.engine import InputSpec
from keras.utils import conv_utils
from keras.legacy import interfaces
from keras.utils.generic_utils import get_custom_objects
from .functions import resize_images

class ResizeImage(Layer):
    __doc__ = 'ResizeImage layer for 2D inputs.\n    Repeats the rows and columns of the data\n    by factor[0] and factor[1] respectively.\n    # Arguments\n        factor: int, or tuple of 2 integers.\n            The upsampling factors for rows and columns.\n        data_format: A string,\n            one of `"channels_last"` or `"channels_first"`.\n            The ordering of the dimensions in the inputs.\n            `"channels_last"` corresponds to inputs with shape\n            `(batch, height, width, channels)` while `"channels_first"`\n            corresponds to inputs with shape\n            `(batch, channels, height, width)`.\n            It defaults to the `image_data_format` value found in your\n            Keras config file at `~/.keras/keras.json`.\n            If you never set it, then it will be "channels_last".\n        interpolation: A string, one of `nearest` or `bilinear`.\n            Note that CNTK does not support yet the `bilinear` upscaling\n            and that with Theano, only `factor=(2, 2)` is possible.\n    # Input shape\n        4D tensor with shape:\n        - If `data_format` is `"channels_last"`:\n            `(batch, rows, cols, channels)`\n        - If `data_format` is `"channels_first"`:\n            `(batch, channels, rows, cols)`\n    # Output shape\n        4D tensor with shape:\n        - If `data_format` is `"channels_last"`:\n            `(batch, upsampled_rows, upsampled_cols, channels)`\n        - If `data_format` is `"channels_first"`:\n            `(batch, channels, upsampled_rows, upsampled_cols)`\n    '

    @interfaces.legacy_upsampling2d_support
    def __init__(self, factor=(2, 2), data_format='channels_last', interpolation='nearest', **kwargs):
        (super(ResizeImage, self).__init__)(**kwargs)
        self.data_format = data_format
        self.factor = conv_utils.normalize_tuple(factor, 2, "factor")
        self.input_spec = InputSpec(ndim=4)
        if interpolation not in ('nearest', 'bilinear'):
            raise ValueError('interpolation should be one of "nearest" or "bilinear".')
        self.interpolation = interpolation

    def compute_output_shape(self, input_shape):
        if self.data_format == "channels_first":
            height = self.factor[0] * input_shape[2] if input_shape[2] is not None else None
            width = self.factor[1] * input_shape[3] if input_shape[3] is not None else None
            return (input_shape[0],
             input_shape[1],
             height,
             width)
        if self.data_format == "channels_last":
            height = self.factor[0] * input_shape[1] if input_shape[1] is not None else None
            width = self.factor[1] * input_shape[2] if input_shape[2] is not None else None
            return (input_shape[0],
             height,
             width,
             input_shape[3])

    def call(self, inputs):
        return resize_images(inputs, self.factor[0], self.factor[1], self.data_format, self.interpolation)

    def get_config(self):
        config = {'factor':self.factor, 
         'data_format':self.data_format}
        base_config = super(ResizeImage, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))


get_custom_objects().update({"ResizeImage": ResizeImage})

# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_seg_models\encs\cls_models\cls_models\ef_net\initializers.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 2455 bytes
import numpy as np, tensorflow as tf
import keras.backend as K
from keras.initializers import Initializer
from keras.utils.generic_utils import get_custom_objects

class EfficientConv2DKernelInitializer(Initializer):
    __doc__ = "Initialization for convolutional kernels.\n\n    The main difference with tf.variance_scaling_initializer is that\n    tf.variance_scaling_initializer uses a truncated normal with an uncorrected\n    standard deviation, whereas here we use a normal distribution. Similarly,\n    tf.contrib.layers.variance_scaling_initializer uses a truncated normal with\n    a corrected standard deviation.\n\n    Args:\n      shape: shape of variable\n      dtype: dtype of variable\n      partition_info: unused\n\n    Returns:\n      an initialization for the variable\n    "

    def __call__(self, shape, dtype=K.floatx(), **kwargs):
        kernel_height, kernel_width, _, out_filters = shape
        fan_out = int(kernel_height * kernel_width * out_filters)
        return tf.random_normal(shape,
          mean=0.0, stddev=(np.sqrt(2.0 / fan_out)), dtype=dtype)


class EfficientDenseKernelInitializer(Initializer):
    __doc__ = "Initialization for dense kernels.\n\n    This initialization is equal to\n      tf.variance_scaling_initializer(scale=1.0/3.0, mode='fan_out',\n                                      distribution='uniform').\n    It is written out explicitly here for clarity.\n\n    Args:\n      shape: shape of variable\n      dtype: dtype of variable\n\n    Returns:\n      an initialization for the variable\n    "

    def __call__(self, shape, dtype=K.floatx(), **kwargs):
        """Initialization for dense kernels.

        This initialization is equal to
          tf.variance_scaling_initializer(scale=1.0/3.0, mode='fan_out',
                                          distribution='uniform').
        It is written out explicitly here for clarity.

        Args:
          shape: shape of variable
          dtype: dtype of variable

        Returns:
          an initialization for the variable
        """
        init_range = 1.0 / np.sqrt(shape[1])
        return tf.random_uniform(shape, (-init_range), init_range, dtype=dtype)


conv_kernel_initializer = EfficientConv2DKernelInitializer()
dense_kernel_initializer = EfficientDenseKernelInitializer()
get_custom_objects().update({'EfficientDenseKernelInitializer':EfficientDenseKernelInitializer, 
 'EfficientConv2DKernelInitializer':EfficientConv2DKernelInitializer})

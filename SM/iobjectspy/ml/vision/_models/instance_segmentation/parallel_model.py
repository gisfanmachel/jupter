# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\instance_segmentation\parallel_model.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 7190 bytes
"""
Mask R-CNN
Multi-GPU Support for Keras.

Copyright (c) 2017 Matterport, Inc.
Licensed under the MIT License (see LICENSE for details)
Written by Waleed Abdulla

Ideas and a small code snippets from these sources:
https://github.com/fchollet/keras/issues/2436
https://medium.com/@kuza55/transparent-multi-gpu-training-on-tensorflow-with-keras-8b0016fd9012
https://github.com/avolkov1/keras_experiments/blob/master/keras_exp/multigpu/
https://github.com/fchollet/keras/blob/master/keras/utils/training_utils.py
"""
import keras.backend as K
import keras.layers as KL
import keras.models as KM
import tensorflow as tf

class ParallelModel(KM.Model):
    __doc__ = "Subclasses the standard Keras Model and adds multi-GPU support.\n    It works by creating a copy of the model on each GPU. Then it slices\n    the inputs and sends a slice to each copy of the model, and then\n    merges the outputs together and applies the loss on the combined\n    outputs.\n    "

    def __init__(self, keras_model, gpu_count):
        """Class constructor.
        keras_model: The Keras model to parallelize
        gpu_count: Number of GPUs. Must be > 1
        """
        super(ParallelModel, self).__init__()
        self.inner_model = keras_model
        self.gpu_count = gpu_count
        merged_outputs = self.make_parallel()
        super(ParallelModel, self).__init__(inputs=(self.inner_model.inputs), outputs=merged_outputs)

    def __getattribute__(self, attrname):
        """Redirect loading and saving methods to the inner model. That's where
        the weights are stored."""
        if "load" in attrname or "save" in attrname:
            return getattr(self.inner_model, attrname)
        return super(ParallelModel, self).__getattribute__(attrname)

    def summary(self, *args, **kwargs):
        """Override summary() to display summaries of both, the wrapper
        and inner models."""
        (super(ParallelModel, self).summary)(*args, **kwargs)
        (self.inner_model.summary)(*args, **kwargs)

    def make_parallelParse error at or near `LOAD_DICTCOMP' instruction at offset 4
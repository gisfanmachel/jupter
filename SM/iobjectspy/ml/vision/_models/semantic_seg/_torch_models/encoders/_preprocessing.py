# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_torch_models\encoders\_preprocessing.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 527 bytes
import numpy as np

def preprocess_input(x, mean=None, std=None, input_space='RGB', input_range=None, **kwargs):
    if np.argmin(x.shape) < 1:
        x = np.transpose(x, (1, 2, 0))
    elif input_space == "BGR":
        x = x[(..., None[None:-1])].copy()
    if input_range is not None:
        if x.max() > 1 and input_range[1] == 1:
            x = x / 255.0
    if mean is not None:
        mean = np.array(mean)
        x = x - mean
    if std is not None:
        std = np.array(std)
        x = x / std
    return x

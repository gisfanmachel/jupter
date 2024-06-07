# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_seg_models\encs\cls_models\cls_models\resnext\preprocessing.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 346 bytes
import numpy as np
from skimage.transform import resize

def preprocess_input(x, size=None):
    """input standardizing function
    Args:
        x: numpy.ndarray with shape (H, W, C)
        size: tuple (H_new, W_new), resized input shape
    Return:
        x: numpy.ndarray
    """
    if size:
        x = resize(x, size) * 255
    return x

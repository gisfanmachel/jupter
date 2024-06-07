# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_torch_models\util\_toolkit.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 469 bytes
from numbers import Number
import numpy as np

def annealing_cos(start, end, pct):
    """Cosine anneal from `start` to `end` as pct goes from 0.0 to 1.0."""
    cos_out = np.cos(np.pi * pct) + 1
    return end + (start - end) / 2 * cos_out


def get_annealing_cos(start, end):

    def annealing_cos_private(pct):
        cos_out = np.cos(np.pi * pct) + 1
        return end + (start - end) / 2 * cos_out

    return annealing_cos_private

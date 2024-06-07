# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_seg_models\encs\cls_models\cls_models\ef_net\preprocessing.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 1214 bytes
import numpy as np
from skimage.transform import resize
MEAN_RGB = [123.675, 116.28, 103.53]
STDDEV_RGB = [58.395, 57.120000000000005, 57.375]
MAP_INTERPOLATION_TO_ORDER = {
 'nearest': 0, 
 'bilinear': 1, 
 'biquadratic': 2, 
 'bicubic': 3}

def center_crop_and_resize(image, image_size, crop_padding=32, interpolation='bicubic'):
    assert image.ndim in {2, 3}
    assert interpolation in MAP_INTERPOLATION_TO_ORDER.keys()
    h, w = image.shape[None[:2]]
    padded_center_crop_size = int(image_size / (image_size + crop_padding) * min(h, w))
    offset_height = (h - padded_center_crop_size + 1) // 2
    offset_width = (w - padded_center_crop_size + 1) // 2
    image_crop = image[(offset_height[:padded_center_crop_size + offset_height],
     offset_width[:padded_center_crop_size + offset_width])]
    resized_image = resize(image_crop,
      (
     image_size, image_size),
      order=(MAP_INTERPOLATION_TO_ORDER[interpolation]),
      preserve_range=True)
    return resized_image


def preprocess_input(x):
    assert x.ndim in (3, 4)
    assert x.shape[-1] == 3
    x = x - np.array(MEAN_RGB)
    x = x / np.array(STDDEV_RGB)
    return x

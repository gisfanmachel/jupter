# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\change_detection.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 11296 bytes
"""
@author: YangRuijie
@license: 
@contact: yangruijie@supermap.com
@software: 
@file: change_detection.py
@time: 7/23/19 6:14 AM
@desc:
"""
import os, tempfile, rasterio
from rasterio.plot import reshape_as_image, reshape_as_raster
from rasterio.windows import Window
import numpy as np
from ..... import import_tif, raster_to_vector, DatasetType
from _jsuperpy.data._util import get_output_datasource, check_output_datasource
from toolkit._toolkit import stretch_n, stretch_min_max, view_bar, get_input_dataset
from .base_keras_models import Estimation

class ChangeEstimation(Estimation):

    def __init__(self, model_path, config):
        super().__init__(model_path, config)
        self.model_input = config.ModelInput[0]
        self.model_output = config.ModelOutput[0]
        if np.argmin(self.model_input.Shape) == 0:
            self.band_order = "first"
            self.seg_size = self.model_input.Shape[1]
            self.out_width_height = [self.model_output.Shape[1], self.model_output.Shape[2]]
            self.output_msk_num = self.model_output.Shape[0]
            if self.model_input.Shape[1] != self.model_input.Shape[2]:
                raise ValueError("Model input width and height should be equal!")
        else:
            self.band_order = "last"
            self.seg_size = self.model_input.Shape[1]
            self.out_width_height = [self.model_output.Shape[0], self.model_output.Shape[1]]
            self.output_msk_num = self.model_output.Shape[-1]
            if self.model_input.Shape[1] != self.model_input.Shape[0]:
                raise ValueError("Model input width and height should be equal!")
        self.is_stretch = config.IsStretch
        self.model_path = model_path

    def estimate_img(self, before_img, after_image, coversize, out_ds, out_dataset_name, **kwargs):
        self.half_oversize = coversize
        self._predict_with_rasterio(before_img, after_image, out_ds, out_dataset_name)

    def _predict_with_rasterioParse error at or near `COME_FROM' instruction at offset 1726_0
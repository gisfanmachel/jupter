# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_torch_models\encoders\_base.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 1331 bytes
import torch
import torch.nn as nn
from typing import List
from collections import OrderedDict
from . import _utils as utils

class EncoderMixin:
    __doc__ = "Add encoder functionality such as:\n        - output channels specification of feature tensors (produced by encoder)\n        - patching first convolution for arbitrary input channels\n    "

    @property
    def out_channels(self):
        """Return channels dimensions for each tensor of forward output of encoder"""
        return self._out_channels[None[:self._depth + 1]]

    def set_in_channels(self, in_channels):
        """Change first convolution chennels"""
        if in_channels == 3:
            return
        self._in_channels = in_channels
        if self._out_channels[0] == 3:
            self._out_channels = tuple([in_channels] + list(self._out_channels)[1[:None]])
        utils.patch_first_conv(model=self, in_channels=in_channels)

    def get_stages(self):
        """Method should be overridden in encoder"""
        raise NotImplementedError

    def make_dilated(self, stage_list, dilation_list):
        stages = self.get_stages()
        for stage_indx, dilation_rate in zip(stage_list, dilation_list):
            utils.replace_strides_with_dilation(module=(stages[stage_indx]),
              dilation_rate=dilation_rate)

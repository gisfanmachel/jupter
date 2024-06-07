# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_torch_models\deeplabv3p\model.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 3560 bytes
import torch.nn as nn
from typing import Optional
from ..base import SegmentationHead, ClassificationHead, SegmentationModel
from .decoder import DeepLabV3PlusDecoder
from ..encoders import get_encoder

class DeepLabV3Plus(SegmentationModel):
    __doc__ = 'DeepLabV3_ implemetation from "Rethinking Atrous Convolution for Semantic Image Segmentation"\n    Args:\n        encoder_name: name of classification model (without last dense layers) used as feature\n                extractor to build segmentation model.\n        encoder_depth: number of stages used in decoder, larger depth - more features are generated.\n            e.g. for depth=3 encoder will generate list of features with following spatial shapes\n            [(H,W), (H/2, W/2), (H/4, W/4), (H/8, W/8)], so in general the deepest feature will have\n            spatial resolution (H/(2^depth), W/(2^depth)]\n        encoder_weights: one of ``None`` (random initialization), ``imagenet`` (pre-training on ImageNet).\n        decoder_channels: a number of convolution filters in ASPP module (default 256).\n        in_channels: number of input channels for model, default is 3.\n        classes: a number of classes for output (output shape - ``(batch, classes, h, w)``).\n        activation (str, callable): activation function used in ``.predict(x)`` method for inference.\n            One of [``sigmoid``, ``softmax2d``, callable, None]\n        upsampling: optional, final upsampling factor\n            (default is 8 to preserve input -> output spatial shape identity)\n        aux_params: if specified model will have additional classification auxiliary output\n            build on top of encoder, supported params:\n                - classes (int): number of classes\n                - pooling (str): one of \'max\', \'avg\'. Default is \'avg\'.\n                - dropout (float): dropout factor in [0, 1)\n                - activation (str): activation function to apply "sigmoid"/"softmax" (could be None to return logits)\n    Returns:\n        ``torch.nn.Module``: **DeepLabV3**\n    .. _DeeplabV3:\n        https://arxiv.org/abs/1706.05587\n    '

    def __init__(self, encoder_name='xception_atrous', encoder_depth=5, encoder_weights='imagenet', decoder_channels=256, in_channels=3, classes=1, activation=None, upsampling=4, aux_params=None):
        super().__init__()
        self.encoder = get_encoder(encoder_name,
          in_channels=in_channels,
          depth=encoder_depth,
          weights=encoder_weights)
        self.decoder = DeepLabV3PlusDecoder(in_channels=(self.encoder.out_channels[-1]),
          out_channels=decoder_channels)
        self.segmentation_head = SegmentationHead(in_channels=(self.decoder.out_channels),
          out_channels=classes,
          activation=activation,
          kernel_size=1,
          upsampling=upsampling)
        if aux_params is not None:
            self.classification_head = ClassificationHead(in_channels=self.encoder.out_channels[-1], **aux_params)
        else:
            self.classification_head = None
        self.name = "deeplabv3plus-{}".format(encoder_name)
        self.initialize()

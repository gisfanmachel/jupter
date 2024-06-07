# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_torch_models\geo_api\model_builder.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 961 bytes
from ..deeplabv3p import DeepLabV3Plus
from ..fpn import FPN

def build_torch_seg_model(in_channels, classes, backbone_name='vgg19', encoder_weights='imagenet', net_type='unet', activation=None, freeze_encoder=False):
    """
    :param in_channels: 输入图像通道数
    :param classes: 类别数量
    :param backbone_name: 主干网络 vgg19 resnet50 resnext50
    :param encoder_weights:  str imagenet
    :param net_type:  暂时只支持fpn,deeplabv3plus
    :return: keras.model
    """
    if net_type == "fpn":
        model = FPN(encoder_name=backbone_name, in_channels=in_channels, classes=classes, encoder_weights=encoder_weights,
          activation=activation)
    else:
        if net_type == "deeplabv3plus":
            model = DeepLabV3Plus(encoder_name=backbone_name, encoder_weights=encoder_weights, in_channels=in_channels, classes=classes,
              activation=activation)
    return model

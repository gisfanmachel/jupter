# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_seg_models\model_builder.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 1731 bytes
"""
@author: YangRuijie
@license: 
@contact: yangruijie@supermap.com
@software: 
@file: unet_api.py
@time: 5/10/19 1:54 AM
@desc:
"""
from keras import Input
from . import Unet, ChangUNet

def build_model(width, height, depth, classes, backbone_name='vgg19', encoder_weights='imagenet', net_type='unet', freeze_encoder=False):
    """

    :param width: 输入图像宽
    :param height: 输入图像高
    :param depth: 输入图像通道数
    :param classes: 类别数量
    :param backbone_name: 主干网络 vgg19 resnet50 resnext50
    :param encoder_weights:  str imagenet
    :param net_type:  暂时只支持unet, 其他 pspnet,linknet,fpn,unetregression 随后支持
    :return: keras.model
    """
    input_tensor = Input(shape=(width, height, depth))
    input_shape = (width, height, depth)
    if net_type == "unet":
        model = Unet(input_shape=input_shape, input_tensor=input_tensor, backbone_name=backbone_name, encoder_weights=encoder_weights,
          classes=classes)
    else:
        if net_type == "change_unet":
            model = ChangUNet(input_shape=input_shape, input_tensor=input_tensor, backbone_name=backbone_name, encoder_weights=encoder_weights,
              classes=classes,
              freeze_encoder=freeze_encoder)
    return model

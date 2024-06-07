# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_seg_models\change_net\model.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 3002 bytes
"""
@author: YangRuijie
@license: 
@contact: yangruijie@supermap.com
@software: 
@file: model.py
@time: 7/23/19 6:35 AM
@desc:
"""
from keras import Model
from ..utils import freeze_model
from ..._seg_models import Unet
from .builder import build_change_unet
from ..utils import get_layer_number

def ChangUNet(backbone_name='vgg16', input_shape=(None, None, 3), input_tensor=None, encoder_weights='imagenet', freeze_encoder=False, skip_connections='default', decoder_block_type='upsampling', decoder_filters=(256, 128, 64, 32, 16), decoder_use_batchnorm=True, n_upsample_blocks=5, upsample_rates=(2, 2, 2, 2, 2), classes=1, activation='sigmoid'):
    """

    Args:
        backbone_name: (str) look at list of available backbones.
        input_shape:  (tuple) dimensions of input data (H, W, C)
        input_tensor: keras tensor
        encoder_weights: one of `None` (random initialization), 'imagenet' (pre-training on ImageNet)
        freeze_encoder: (bool) Set encoder layers weights as non-trainable. Useful for fine-tuning
        skip_connections: if 'default' is used take default skip connections,
            else provide a list of layer numbers or names starting from top of model
        decoder_block_type: (str) one of 'upsampling' and 'transpose' (look at blocks.py)
        decoder_filters: (int) number of convolution layer filters in decoder blocks
        decoder_use_batchnorm: (bool) if True add batch normalisation layer between `Conv2D` ad `Activation` layers
        n_upsample_blocks: (int) a number of upsampling blocks
        upsample_rates: (tuple of int) upsampling rates decoder blocks
        classes: (int) a number of classes for output
        activation: (str) one of keras activations for last model layer

    Returns:
        keras.models.Model instance

    """
    base_model = Unet(backbone_name=backbone_name, input_shape=input_shape,
      input_tensor=input_tensor,
      encoder_weights=encoder_weights,
      freeze_encoder=freeze_encoder,
      skip_connections=skip_connections,
      decoder_block_type=decoder_block_type,
      decoder_filters=decoder_filters,
      decoder_use_batchnorm=decoder_use_batchnorm,
      n_upsample_blocks=n_upsample_blocks,
      upsample_rates=upsample_rates,
      classes=classes,
      activation=activation)
    model_extract = Model(base_model.input, base_model.layers[get_layer_number(base_model, "final_conv")].input)
    model = build_change_unet(model_extract, input_shape, classes, activation)
    if freeze_encoder:
        freeze_model(model_extract)
    model.name = "change-u-{}".format(backbone_name)
    return model

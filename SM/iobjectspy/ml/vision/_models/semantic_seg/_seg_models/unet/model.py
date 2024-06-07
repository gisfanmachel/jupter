# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_seg_models\unet\model.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 4479 bytes
from .builder import build_unet
from ..utils import freeze_model
from ..encs import get_backbone
DEFAULT_SKIP_CONNECTIONS = {
 'vgg16': (17, 13, 9, 5, 2), 
 'vgg19': (20, 15, 10, 5, 2), 
 'resnet18': (66, 47, 28, 5), 
 'resnet34': (129, 74, 37, 5), 
 'resnet50': (155, 88, 43, 5), 
 'resnet101': (342, 88, 43, 5), 
 'resnet152': (529, 132, 43, 5), 
 'resnext50': (991, 539, 237, 5), 
 'resnext101': (2266, 539, 237, 5), 
 'inceptionv3': (228, 86, 16, 9), 
 'inceptionresnetv2': (594, 260, 16, 9), 
 'densenet121': (311, 139, 51, 4), 
 'densenet169': (367, 139, 51, 4), 
 'densenet201': (479, 139, 51, 4), 
 'efficientnetb2': ('swish_48', 'swish_24', 'swish_15', 'swish_6'), 
 'efficientnetb3': (278, 122, 76, 30)}

def Unet(backbone_name='vgg16', input_shape=(None, None, 3), input_tensor=None, encoder_weights='imagenet', freeze_encoder=False, skip_connections='default', decoder_block_type='upsampling', decoder_filters=(256, 128, 64, 32, 16), decoder_use_batchnorm=True, n_upsample_blocks=5, upsample_rates=(2, 2, 2, 2, 2), classes=1, activation='sigmoid'):
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
    backbone = get_backbone(backbone_name, input_shape=input_shape,
      input_tensor=input_tensor,
      weights=encoder_weights,
      include_top=False)
    if skip_connections == "default":
        skip_connections = DEFAULT_SKIP_CONNECTIONS[backbone_name]
    model = build_unet(backbone, classes,
      skip_connections,
      decoder_filters=decoder_filters,
      block_type=decoder_block_type,
      activation=activation,
      n_upsample_blocks=n_upsample_blocks,
      upsample_rates=upsample_rates,
      use_batchnorm=decoder_use_batchnorm)
    if freeze_encoder:
        freeze_model(backbone)
    model.name = "u-{}".format(backbone_name)
    return model

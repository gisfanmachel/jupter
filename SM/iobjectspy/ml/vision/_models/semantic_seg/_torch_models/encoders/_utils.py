# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_torch_models\encoders\_utils.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 1515 bytes
import torch
import torch.nn as nn

def patch_first_conv(model, in_channels):
    """Change first convolution layer input channels.
    In case:
        in_channels == 1 or in_channels == 2 -> reuse original weights
        in_channels > 3 -> make random kaiming normal initialization
    """
    for module in model.modules():
        if isinstance(module, nn.Conv2d):
            break

    module.in_channels = in_channels
    weight = module.weight.detach()
    reset = False
    if in_channels == 1:
        weight = weight.sum(1, keepdim=True)
    else:
        if in_channels == 2:
            weight = weight[(None[:None], None[:2])] * 1.5
        else:
            reset = True
            weight = (torch.Tensor)(module.out_channels, module.in_channels // module.groups, *module.kernel_size)
    module.weight = nn.parameter.Parameter(weight)
    if reset:
        module.reset_parameters()


def replace_strides_with_dilation(module, dilation_rate):
    """Patch Conv2d modules replacing strides with dilation"""
    for mod in module.modules():
        if isinstance(mod, nn.Conv2d):
            mod.stride = (1, 1)
            mod.dilation = (dilation_rate, dilation_rate)
            kh, kw = mod.kernel_size
            mod.padding = (kh // 2 * dilation_rate, kh // 2 * dilation_rate)
            if hasattr(mod, "static_padding"):
                mod.static_padding = nn.Identity()

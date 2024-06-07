# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_torch_models\encoders\xception_atrous.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 11351 bytes
""" 
Ported to pytorch thanks to [tstandley](https://github.com/tstandley/Xception-PyTorch)
@author: tstandley
Adapted by cadene
Creates an Xception Model as defined in:
Francois Chollet
Xception: Deep Learning with Depthwise Separable Convolutions
https://arxiv.org/pdf/1610.02357.pdf
This weights ported from the Keras implementation. Achieves the following performance on the validation set:
Loss:0.9173 Prec@1:78.892 Prec@5:94.292
REMEMBER to set your image size to 3x299x299 for both test and validation
normalize = transforms.Normalize(mean=[0.5, 0.5, 0.5],
                                  std=[0.5, 0.5, 0.5])
The resize parameter of the validation transform should be 333, and make sure to center crop at 299x299
"""
import math, torch
import torch.nn as nn
from pretrainedmodels.models.xception import pretrained_settings, Xception
from torch.nn import init
from torch.nn import BatchNorm2d
from iobjectspy.ml.vision._models.semantic_seg._torch_models.encoders._base import EncoderMixin
bn_mom = 0.0003
__all__ = ["xception"]
model_urls = {"xception": "http://data.lip6.fr/cadene/pretrainedmodels/xception-b5690688.pth"}

class SeparableConv2d(nn.Module):

    def __init__(self, in_channels, out_channels, kernel_size=1, stride=1, padding=0, dilation=1, bias=False, activate_first=True, inplace=True):
        super(SeparableConv2d, self).__init__()
        self.relu0 = nn.ReLU(inplace=inplace)
        self.depthwise = nn.Conv2d(in_channels, in_channels, kernel_size, stride, padding, dilation, groups=in_channels, bias=bias)
        self.bn1 = BatchNorm2d(in_channels, momentum=bn_mom)
        self.relu1 = nn.ReLU(inplace=True)
        self.pointwise = nn.Conv2d(in_channels, out_channels, 1, 1, 0, 1, 1, bias=bias)
        self.bn2 = BatchNorm2d(out_channels, momentum=bn_mom)
        self.relu2 = nn.ReLU(inplace=True)
        self.activate_first = activate_first

    def forward(self, x):
        if self.activate_first:
            x = self.relu0(x)
        else:
            x = self.depthwise(x)
            x = self.bn1(x)
            if not self.activate_first:
                x = self.relu1(x)
            x = self.pointwise(x)
            x = self.bn2(x)
            x = self.activate_first or self.relu2(x)
        return x


class Block(nn.Module):

    def __init__(self, in_filters, out_filters, strides=1, atrous=None, grow_first=True, activate_first=True, inplace=True):
        super(Block, self).__init__()
        if atrous == None:
            atrous = [
             1] * 3
        else:
            if isinstance(atrous, int):
                atrous_list = [
                 atrous] * 3
                atrous = atrous_list
            else:
                idx = 0
                self.head_relu = True
                if out_filters != in_filters or strides != 1:
                    self.skip = nn.Conv2d(in_filters, out_filters, 1, stride=strides, bias=False)
                    self.skipbn = BatchNorm2d(out_filters, momentum=bn_mom)
                    self.head_relu = False
                else:
                    self.skip = None
                self.hook_layer = None
                if grow_first:
                    filters = out_filters
                else:
                    filters = in_filters
            self.sepconv1 = SeparableConv2d(in_filters, filters, 3, stride=1, padding=(1 * atrous[0]), dilation=(atrous[0]), bias=False,
              activate_first=activate_first,
              inplace=(self.head_relu))
            self.sepconv2 = SeparableConv2d(filters, out_filters, 3, stride=1, padding=(1 * atrous[1]), dilation=(atrous[1]), bias=False,
              activate_first=activate_first)
            self.sepconv3 = SeparableConv2d(out_filters, out_filters, 3, stride=strides, padding=(1 * atrous[2]), dilation=(atrous[2]),
              bias=False,
              activate_first=activate_first,
              inplace=inplace)

    def forward(self, inp):
        if self.skip is not None:
            skip = self.skip(inp)
            skip = self.skipbn(skip)
        else:
            skip = inp
        x = self.sepconv1(inp)
        x = self.sepconv2(x)
        self.hook_layer = x
        x = self.sepconv3(x)
        x += skip
        return x


class Xception(nn.Module):
    __doc__ = "\n    Xception optimized for the ImageNet dataset, as specified in\n    https://arxiv.org/pdf/1610.02357.pdf\n    "

    def __init__(self, os=16):
        """ Constructor
        Args:
            num_classes: number of classes
        """
        super(Xception, self).__init__()
        stride_list = None
        if os == 8:
            stride_list = [
             2, 1, 1]
        else:
            if os == 16:
                stride_list = [
                 2, 2, 1]
            else:
                raise ValueError("xception.py: output stride=%d is not supported." % os)
        self.conv1 = nn.Conv2d(3, 32, 3, 2, 1, bias=False)
        self.bn1 = BatchNorm2d(32, momentum=bn_mom)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv2d(32, 64, 3, 1, 1, bias=False)
        self.bn2 = BatchNorm2d(64, momentum=bn_mom)
        self.block1 = Block(64, 128, 2)
        self.block2 = Block(128, 256, (stride_list[0]), inplace=False)
        self.block3 = Block(256, 728, stride_list[1])
        rate = 16 // os
        self.block4 = Block(728, 728, 1, atrous=rate)
        self.block5 = Block(728, 728, 1, atrous=rate)
        self.block6 = Block(728, 728, 1, atrous=rate)
        self.block7 = Block(728, 728, 1, atrous=rate)
        self.block8 = Block(728, 728, 1, atrous=rate)
        self.block9 = Block(728, 728, 1, atrous=rate)
        self.block10 = Block(728, 728, 1, atrous=rate)
        self.block11 = Block(728, 728, 1, atrous=rate)
        self.block12 = Block(728, 728, 1, atrous=rate)
        self.block13 = Block(728, 728, 1, atrous=rate)
        self.block14 = Block(728, 728, 1, atrous=rate)
        self.block15 = Block(728, 728, 1, atrous=rate)
        self.block16 = Block(728, 728, 1, atrous=[1 * rate, 1 * rate, 1 * rate])
        self.block17 = Block(728, 728, 1, atrous=[1 * rate, 1 * rate, 1 * rate])
        self.block18 = Block(728, 728, 1, atrous=[1 * rate, 1 * rate, 1 * rate])
        self.block19 = Block(728, 728, 1, atrous=[1 * rate, 1 * rate, 1 * rate])
        self.block20 = Block(728, 1024, (stride_list[2]), atrous=rate, grow_first=False)
        self.conv3 = SeparableConv2d(1024, 1536, 3, 1, (1 * rate), dilation=rate, activate_first=False)
        self.conv5 = SeparableConv2d(1536, 2048, 3, 1, (1 * rate), dilation=rate, activate_first=False)
        self.layers = []
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
                m.weight.data.normal_(0, math.sqrt(2.0 / n))

    def forward(self, input):
        self.layers = []
        x = self.conv1(input)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.conv2(x)
        x = self.bn2(x)
        x = self.relu(x)
        x = self.block1(x)
        x = self.block2(x)
        self.layers.append(self.block2.hook_layer)
        x = self.block3(x)
        x = self.block4(x)
        x = self.block5(x)
        x = self.block6(x)
        x = self.block7(x)
        x = self.block8(x)
        x = self.block9(x)
        x = self.block10(x)
        x = self.block11(x)
        x = self.block12(x)
        x = self.block13(x)
        x = self.block14(x)
        x = self.block15(x)
        x = self.block16(x)
        x = self.block17(x)
        x = self.block18(x)
        x = self.block19(x)
        x = self.block20(x)
        x = self.conv3(x)
        x = self.conv5(x)
        self.layers.append(x)
        return x

    def get_layers(self):
        return self.layers


def xception(pretrained=True, os=16):
    model = Xception(os=os)
    if pretrained:
        old_dict = torch.load(model_urls["xception"])
        model_dict = model.state_dict()
        old_dict = {k: v for k, v in old_dict.items() if "track" not in k}
        model_dict.update(old_dict)
        model.load_state_dict(model_dict)
    return model


class XceptionAtrousEncoder(Xception, EncoderMixin):

    def __init__(self, out_channels, *args, depth=5, **kwargs):
        (super().__init__)(*args, **kwargs)
        self._out_channels = out_channels
        self._depth = depth
        self._in_channels = 3
        self.conv1.padding = (1, 1)
        self.conv2.padding = (1, 1)

    def get_stages(self):
        return [
         nn.Identity(),
         nn.Sequential(self.conv1, self.bn1, self.relu, self.conv2, self.bn2, self.relu),
         self.block1,
         self.block2,
         nn.Sequential(self.block3, self.block4, self.block5, self.block6, self.block7, self.block8, self.block9, self.block10, self.block11, self.block12, self.block13, self.block14, self.block15, self.block16, self.block17, self.block18, self.block19),
         nn.Sequential(self.block20),
         nn.Sequential(self.conv3),
         nn.Sequential(self.conv5)]

    def forward(self, x):
        stages = self.get_stages()
        features = []
        for i in range(self._depth + 1):
            x = stages[i](x)
            features.append(x)

        return features

    def load_state_dict(self, state_dict):
        state_dict.pop("fc.bias")
        state_dict.pop("fc.weight")
        super().load_state_dict(state_dict, strict=False)


pretrained_settings = {"xception": {"imagenet": {'url':"http://data.lip6.fr/cadene/pretrainedmodels/xception-43020ad28.pth", 
                           'input_space':"RGB", 
                           'input_size':[
                            3, 299, 299], 
                           'input_range':[
                            0, 1], 
                           'mean':[
                            0.5, 0.5, 0.5], 
                           'std':[
                            0.5, 0.5, 0.5], 
                           'num_classes':1000, 
                           'scale':0.8975}}}

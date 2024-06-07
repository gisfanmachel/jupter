# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_torch_models\deeplabv3p\decoder.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 4581 bytes
import torch
from torch import nn
from torch.nn import functional as F
from torch.nn import BatchNorm2d
__all__ = ["DeepLabV3PlusDecoder"]

class ASPP(nn.Module):

    def __init__(self, dim_in, dim_out, rate=1, bn_mom=0.1):
        super(ASPP, self).__init__()
        self.branch1 = nn.Sequential(nn.Conv2d(dim_in, dim_out, 1, 1, padding=0, dilation=rate, bias=True), BatchNorm2d(dim_out, momentum=bn_mom), nn.ReLU(inplace=True))
        self.branch2 = nn.Sequential(nn.Conv2d(dim_in, dim_out, 3, 1, padding=(6 * rate), dilation=(6 * rate), bias=True), BatchNorm2d(dim_out, momentum=bn_mom), nn.ReLU(inplace=True))
        self.branch3 = nn.Sequential(nn.Conv2d(dim_in, dim_out, 3, 1, padding=(12 * rate), dilation=(12 * rate), bias=True), BatchNorm2d(dim_out, momentum=bn_mom), nn.ReLU(inplace=True))
        self.branch4 = nn.Sequential(nn.Conv2d(dim_in, dim_out, 3, 1, padding=(18 * rate), dilation=(18 * rate), bias=True), BatchNorm2d(dim_out, momentum=bn_mom), nn.ReLU(inplace=True))
        self.assp_pooling = ASPPPooling(dim_in, dim_out)
        self.conv_cat = nn.Sequential(nn.Conv2d((dim_out * 5), dim_out, 1, 1, padding=0, bias=True), BatchNorm2d(dim_out, momentum=bn_mom), nn.ReLU(inplace=True))

    def forward(self, x):
        b, c, row, col = x.size()
        conv1x1 = self.branch1(x)
        conv3x3_1 = self.branch2(x)
        conv3x3_2 = self.branch3(x)
        conv3x3_3 = self.branch4(x)
        global_feature = self.assp_pooling(x)
        feature_cat = torch.cat([conv1x1, conv3x3_1, conv3x3_2, conv3x3_3, global_feature], dim=1)
        result = self.conv_cat(feature_cat)
        return result


class ASPPPooling(nn.Sequential):

    def __init__(self, in_channels, out_channels):
        super(ASPPPooling, self).__init__(nn.AdaptiveAvgPool2d(1), nn.Conv2d(in_channels, out_channels, 1, bias=False), nn.ReLU())

    def forward(self, x):
        size = x.shape[(-2)[:None]]
        for mod in self:
            x = mod(x)

        return F.interpolate(x, size=size, mode="bilinear", align_corners=False)


class DeepLabV3PlusDecoder(nn.Sequential):

    def __init__(self, in_channels, out_channels=256, atrous_rates=(12, 24, 36)):
        super(DeepLabV3PlusDecoder, self).__init__()
        self.out_channels = out_channels
        self.aspp = ASPP(dim_in=in_channels, dim_out=out_channels,
          rate=1,
          bn_mom=0.1)
        self.dropout1 = nn.Dropout(0.5)
        self.upsample4 = nn.UpsamplingBilinear2d(scale_factor=4)
        self.upsample_sub = nn.UpsamplingBilinear2d(scale_factor=4)
        indim = 128
        self.shortcut_conv = nn.Sequential(nn.Conv2d(indim, 48, 1, 1, padding=0,
          bias=True), BatchNorm2d(48, momentum=0.1), nn.ReLU(inplace=True))
        self.cat_conv = nn.Sequential(nn.Conv2d((out_channels + 48), out_channels, 3, 1, padding=1, bias=True), BatchNorm2d(out_channels, momentum=0.1), nn.ReLU(inplace=True), nn.Dropout(0.5), nn.Conv2d(out_channels, out_channels, 3, 1, padding=1, bias=True), BatchNorm2d(out_channels, momentum=0.1), nn.ReLU(inplace=True), nn.Dropout(0.1))
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_((m.weight), mode="fan_out", nonlinearity="relu")

    def forward(self, *features):
        layers = features
        feature_aspp = self.aspp(layers[-1])
        feature_aspp = self.dropout1(feature_aspp)
        feature_aspp = self.upsample_sub(feature_aspp)
        feature_shallow = self.shortcut_conv(layers[2])
        feature_cat = torch.cat([feature_aspp, feature_shallow], 1)
        result = self.cat_conv(feature_cat)
        return result

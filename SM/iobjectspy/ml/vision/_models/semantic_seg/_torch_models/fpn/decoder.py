# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_torch_models\fpn\decoder.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 3760 bytes
import torch
import torch.nn as nn
import torch.nn.functional as F

class Conv3x3GNReLU(nn.Module):

    def __init__(self, in_channels, out_channels, upsample=False):
        super().__init__()
        self.upsample = upsample
        self.block = nn.Sequential(nn.Conv2d(in_channels,
          out_channels, (3, 3), stride=1, padding=1, bias=False), nn.GroupNorm(32, out_channels), nn.ReLU(inplace=True))

    def forward(self, x):
        x = self.block(x)
        if self.upsample:
            x = F.interpolate(x, scale_factor=2, mode="bilinear", align_corners=True)
        return x


class FPNBlock(nn.Module):

    def __init__(self, pyramid_channels, skip_channels):
        super().__init__()
        self.skip_conv = nn.Conv2d(skip_channels, pyramid_channels, kernel_size=1)

    def forward(self, x, skip=None):
        x = F.interpolate(x, scale_factor=2, mode="nearest")
        skip = self.skip_conv(skip)
        x = x + skip
        return x


class SegmentationBlock(nn.Module):

    def __init__(self, in_channels, out_channels, n_upsamples=0):
        super().__init__()
        blocks = [
         Conv3x3GNReLU(in_channels, out_channels, upsample=(bool(n_upsamples)))]
        if n_upsamples > 1:
            for _ in range(1, n_upsamples):
                blocks.append(Conv3x3GNReLU(out_channels, out_channels, upsample=True))

        self.block = (nn.Sequential)(*blocks)

    def forward(self, x):
        return self.block(x)


class MergeBlock(nn.Module):

    def __init__(self, policy):
        super().__init__()
        if policy not in ('add', 'cat'):
            raise ValueError("`merge_policy` must be one of: ['add', 'cat'], got {}".format(policy))
        self.policy = policy

    def forward(self, x):
        if self.policy == "add":
            return sum(x)
        if self.policy == "cat":
            return torch.cat(x, dim=1)
        raise ValueError("`merge_policy` must be one of: ['add', 'cat'], got {}".format(self.policy))


class FPNDecoder(nn.Module):

    def __init__(self, encoder_channels, encoder_depth=5, pyramid_channels=256, segmentation_channels=128, dropout=0.2, merge_policy='add'):
        super().__init__()
        self.out_channels = segmentation_channels if merge_policy == "add" else segmentation_channels * 4
        if encoder_depth < 3:
            raise ValueError("Encoder depth for FPN decoder cannot be less than 3, got {}.".format(encoder_depth))
        encoder_channels = encoder_channels[None[None:-1]]
        encoder_channels = encoder_channels[None[:encoder_depth + 1]]
        self.p5 = nn.Conv2d((encoder_channels[0]), pyramid_channels, kernel_size=1)
        self.p4 = FPNBlock(pyramid_channels, encoder_channels[1])
        self.p3 = FPNBlock(pyramid_channels, encoder_channels[2])
        self.p2 = FPNBlock(pyramid_channels, encoder_channels[3])
        self.seg_blocks = nn.ModuleList([SegmentationBlock(pyramid_channels, segmentation_channels, n_upsamples=n_upsamples) for n_upsamples in (3,
                                                                                                                                                 2,
                                                                                                                                                 1,
                                                                                                                                                 0)])
        self.merge = MergeBlock(merge_policy)
        self.dropout = nn.Dropout2d(p=dropout, inplace=True)

    def forward(self, *features):
        c2, c3, c4, c5 = features[(-4)[:None]]
        p5 = self.p5(c5)
        p4 = self.p4(p5, c4)
        p3 = self.p3(p4, c3)
        p2 = self.p2(p3, c2)
        feature_pyramid = [seg_block(p) for seg_block, p in zip(self.seg_blocks, [p5, p4, p3, p2])]
        x = self.merge(feature_pyramid)
        x = self.dropout(x)
        return x

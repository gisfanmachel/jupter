# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_torch_models\base\modules.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 3104 bytes
import torch.nn as nn
try:
    from inplace_abn import InPlaceABN
except ImportError:
    InPlaceABN = None

class Conv2dReLU(nn.Sequential):

    def __init__(self, in_channels, out_channels, kernel_size, padding=0, stride=1, use_batchnorm=True):
        if use_batchnorm == "inplace":
            if InPlaceABN is None:
                raise RuntimeError("In order to use `use_batchnorm='inplace'` inplace_abn package must be installed. To install see: https://github.com/mapillary/inplace_abn")
        else:
            super().__init__()
            conv = nn.Conv2d(in_channels,
              out_channels,
              kernel_size,
              stride=stride,
              padding=padding,
              bias=(not use_batchnorm))
            relu = nn.ReLU(inplace=True)
            if use_batchnorm == "inplace":
                bn = InPlaceABN(out_channels, activation="leaky_relu", activation_param=0.0)
                relu = nn.Identity()
            else:
                if use_batchnorm and use_batchnorm != "inplace":
                    bn = nn.BatchNorm2d(out_channels)
                else:
                    bn = nn.Identity()
        super(Conv2dReLU, self).__init__(conv, bn, relu)


class SCSEModule(nn.Module):

    def __init__(self, in_channels, reduction=16):
        super().__init__()
        self.cSE = nn.Sequential(nn.AdaptiveAvgPool2d(1), nn.Conv2d(in_channels, in_channels // reduction, 1), nn.ReLU(inplace=True), nn.Conv2d(in_channels // reduction, in_channels, 1), nn.Sigmoid())
        self.sSE = nn.Sequential(nn.Conv2d(in_channels, 1, 1), nn.Sigmoid())

    def forward(self, x):
        return x * self.cSE(x) + x * self.sSE(x)


class Activation(nn.Module):

    def __init__(self, name, **params):
        super().__init__()
        if name is None or name == "identity":
            self.activation = (nn.Identity)(**params)
        else:
            if name == "sigmoid":
                self.activation = nn.Sigmoid()
            else:
                if name == "softmax2d":
                    self.activation = (nn.Softmax)(dim=1, **params)
                else:
                    if name == "softmax":
                        self.activation = (nn.Softmax)(**params)
                    else:
                        if name == "logsoftmax":
                            self.activation = (nn.LogSoftmax)(**params)
                        else:
                            if callable(name):
                                self.activation = name(**params)
                            else:
                                raise ValueError("Activation should be callable/sigmoid/softmax/logsoftmax/None; got {}".format(name))

    def forward(self, x):
        return self.activation(x)


class Attention(nn.Module):

    def __init__(self, name, **params):
        super().__init__()
        if name is None:
            self.attention = (nn.Identity)(**params)
        else:
            if name == "scse":
                self.attention = SCSEModule(**params)
            else:
                raise ValueError("Attention {} is not implemented".format(name))

    def forward(self, x):
        return self.attention(x)


class Flatten(nn.Module):

    def forward(self, x):
        return x.view(x.shape[0], -1)

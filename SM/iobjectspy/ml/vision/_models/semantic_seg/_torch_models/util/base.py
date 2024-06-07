# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_torch_models\util\base.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 2422 bytes
import re, functools, torch
import torch.nn as nn

class Activation(nn.Module):

    def __init__(self, activation):
        super().__init__()
        if activation == None or activation == "identity":
            self.activation = nn.Identity()
        else:
            if activation == "sigmoid":
                self.activation = torch.sigmoid
            else:
                if activation == "softmax2d":
                    self.activation = functools.partial((torch.softmax), dim=1)
                else:
                    if callable(activation):
                        self.activation = activation
                    else:
                        raise ValueError

    def forward(self, x):
        return self.activation(x)


class BaseObject(nn.Module):

    def __init__(self, name=None):
        super().__init__()
        self._name = name

    @property
    def __name__(self):
        if self._name is None:
            name = self.__class__.__name__
            s1 = re.sub("(.)([A-Z][a-z]+)", "\\1_\\2", name)
            return re.sub("([a-z0-9])([A-Z])", "\\1_\\2", s1).lower()
        return self._name


class Metric(BaseObject):
    pass


class Loss(BaseObject):

    def __add__(self, other):
        if isinstance(other, Loss):
            return SumOfLosses(self, other)
        raise ValueError("Loss should be inherited from `Loss` class")

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, value):
        if isinstance(value, (int, float)):
            return MultipliedLoss(self, value)
        raise ValueError("Loss should be inherited from `BaseLoss` class")

    def __rmul__(self, other):
        return self.__mul__(other)


class SumOfLosses(Loss):

    def __init__(self, l1, l2):
        name = "{} + {}".format(l1.__name__, l2.__name__)
        super().__init__(name=name)
        self.l1 = l1
        self.l2 = l2

    def __call__(self, *inputs):
        return (self.l1.forward)(*inputs) + (self.l2.forward)(*inputs)


class MultipliedLoss(Loss):

    def __init__(self, loss, multiplier):
        if len(loss.__name__.split("+")) > 1:
            name = "{} * ({})".format(multiplier, loss.__name__)
        else:
            name = "{} * {}".format(multiplier, loss.__name__)
        super().__init__(name=name)
        self.loss = loss
        self.multiplier = multiplier

    def __call__(self, *inputs):
        return self.multiplier * (self.loss.forward)(*inputs)

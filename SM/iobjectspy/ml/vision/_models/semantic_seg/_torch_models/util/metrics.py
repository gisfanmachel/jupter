# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_torch_models\util\metrics.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 2927 bytes
from . import base
from . import functional as F
from .base import Activation

class IoU(base.Metric):
    __name__ = "iou_score"

    def __init__(self, eps=1e-07, threshold=0.5, activation=None, ignore_channels=None, **kwargs):
        (super().__init__)(**kwargs)
        self.eps = eps
        self.threshold = threshold
        self.activation = Activation(activation)
        self.ignore_channels = ignore_channels

    def forward(self, y_pr, y_gt):
        y_pr = self.activation(y_pr)
        return F.iou(y_pr,
          y_gt, eps=(self.eps),
          threshold=(self.threshold),
          ignore_channels=(self.ignore_channels))


class Fscore(base.Metric):

    def __init__(self, beta=1, eps=1e-07, threshold=0.5, activation=None, ignore_channels=None, **kwargs):
        (super().__init__)(**kwargs)
        self.eps = eps
        self.beta = beta
        self.threshold = threshold
        self.activation = Activation(activation)
        self.ignore_channels = ignore_channels

    def forward(self, y_pr, y_gt):
        y_pr = self.activation(y_pr)
        return F.f_score(y_pr,
          y_gt, eps=(self.eps),
          beta=(self.beta),
          threshold=(self.threshold),
          ignore_channels=(self.ignore_channels))


class Accuracy(base.Metric):

    def __init__(self, threshold=0.5, activation=None, ignore_channels=None, **kwargs):
        (super().__init__)(**kwargs)
        self.threshold = threshold
        self.activation = Activation(activation)
        self.ignore_channels = ignore_channels

    def forward(self, y_pr, y_gt):
        y_pr = self.activation(y_pr)
        return F.accuracy(y_pr,
          y_gt, threshold=(self.threshold),
          ignore_channels=(self.ignore_channels))


class Recall(base.Metric):

    def __init__(self, eps=1e-07, threshold=0.5, activation=None, ignore_channels=None, **kwargs):
        (super().__init__)(**kwargs)
        self.eps = eps
        self.threshold = threshold
        self.activation = Activation(activation)
        self.ignore_channels = ignore_channels

    def forward(self, y_pr, y_gt):
        y_pr = self.activation(y_pr)
        return F.recall(y_pr,
          y_gt, eps=(self.eps),
          threshold=(self.threshold),
          ignore_channels=(self.ignore_channels))


class Precision(base.Metric):

    def __init__(self, eps=1e-07, threshold=0.5, activation=None, ignore_channels=None, **kwargs):
        (super().__init__)(**kwargs)
        self.eps = eps
        self.threshold = threshold
        self.activation = Activation(activation)
        self.ignore_channels = ignore_channels

    def forward(self, y_pr, y_gt):
        y_pr = self.activation(y_pr)
        return F.precision(y_pr,
          y_gt, eps=(self.eps),
          threshold=(self.threshold),
          ignore_channels=(self.ignore_channels))

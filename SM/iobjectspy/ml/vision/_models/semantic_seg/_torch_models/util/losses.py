# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_torch_models\util\losses.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 6952 bytes
import torch
import torch.nn as nn
from . import base
from . import functional as F
from .base import Activation

class JaccardLoss(base.Loss):

    def __init__(self, eps=1.0, activation=None, ignore_channels=None, **kwargs):
        (super().__init__)(**kwargs)
        self.eps = eps
        self.activation = Activation(activation)
        self.ignore_channels = ignore_channels

    def forward(self, y_pr, y_gt):
        y_pr = self.activation(y_pr)
        return 1 - F.jaccard(y_pr,
          y_gt, eps=(self.eps),
          threshold=None,
          ignore_channels=(self.ignore_channels))


class DiceLoss(base.Loss):

    def __init__(self, eps=1.0, beta=1.0, activation=None, ignore_channels=None, **kwargs):
        (super().__init__)(**kwargs)
        self.eps = eps
        self.beta = beta
        self.activation = Activation(activation)
        self.ignore_channels = ignore_channels

    def forward(self, y_pr, y_gt):
        return 1 - F.f_score(y_pr,
          y_gt, beta=(self.beta),
          eps=(self.eps),
          threshold=None,
          ignore_channels=(self.ignore_channels))


class CrossEntropyLoss(base.Loss):

    def __init__(self, weight=None, size_average=True):
        super(CrossEntropyLoss, self).__init__()
        self.crossentropyloss = nn.CrossEntropyLoss(weight, size_average)

    def forward(self, inputs, targets):
        logits_2d = inputs.view(inputs.size()[0], inputs.size()[1], -1)
        targets = torch.argmax(targets, dim=1)
        labels_2d = targets.view(targets.size()[0], -1)
        return self.crossentropyloss(logits_2d, labels_2d.long())


class L1Loss(nn.L1Loss, base.Loss):
    pass


class MSELoss(nn.MSELoss, base.Loss):
    pass


class BCELoss(nn.BCELoss, base.Loss):
    pass


class BCEWithLogitsLoss(nn.BCEWithLogitsLoss, base.Loss):
    pass


class HrnetCrossEntropy(base.Loss):

    def __init__(self, ignore_label=-1, weight=None):
        super(HrnetCrossEntropy, self).__init__()
        self.ignore_label = ignore_label
        self.criterion = nn.CrossEntropyLoss(weight=weight, ignore_index=ignore_label)

    def forward(self, score, target):
        ph, pw = score.size(2), score.size(3)
        h, w = target.size(1), target.size(2)
        if ph != h or pw != w:
            score = nn.functional.upsample(input=score,
              size=(h, w),
              mode="bilinear")
        loss = self.criterion(score, target)
        return loss


class HrnetOhemCrossEntropy(base.Loss):

    def __init__(self, ignore_label=-1, thres=0.7, min_kept=100000, weight=None):
        super(HrnetOhemCrossEntropy, self).__init__()
        self.thresh = thres
        self.min_kept = max(1, min_kept)
        self.ignore_label = ignore_label
        self.criterion = nn.CrossEntropyLoss(weight=weight, ignore_index=ignore_label,
          reduction="none")

    def forward(self, score, target, **kwargs):
        ph, pw = score.size(2), score.size(3)
        h, w = target.size(1), target.size(2)
        if ph != h or pw != w:
            score = nn.functional.upsample(input=score, size=(h, w), mode="bilinear")
        pred = F.softmax(score, dim=1)
        pixel_losses = self.criterion(score, target).contiguous().view(-1)
        mask = target.contiguous().view(-1) != self.ignore_label
        tmp_target = target.clone()
        tmp_target[tmp_target == self.ignore_label] = 0
        pred = pred.gather(1, tmp_target.unsqueeze(1))
        pred, ind = pred.contiguous().view(-1)[mask].contiguous().sort()
        min_value = pred[min(self.min_kept, pred.numel() - 1)]
        threshold = max(min_value, self.thresh)
        pixel_losses = pixel_losses[mask][ind]
        pixel_losses = pixel_losses[pred < threshold]
        return pixel_losses.mean()


class DiceJaccardLoss(base.Loss):

    def __init__(self, eps=1.0, beta=1.0, activation=None, ignore_channels=None, **kwargs):
        (super().__init__)(**kwargs)
        self.eps = eps
        self.beta = beta
        self.activation = Activation(activation)
        self.ignore_channels = ignore_channels

    def forward(self, y_pr, y_gt):
        return 1 - F.f_score(y_pr, y_gt, beta=(self.beta), eps=(self.eps), threshold=None, ignore_channels=(self.ignore_channels)) + 1 - F.jaccard(y_pr,
          y_gt, eps=(self.eps),
          threshold=None,
          ignore_channels=(self.ignore_channels))


def get_loss(loss_type, **kwargs):
    loss_list = loss_type.split("+")
    loss_list = [l.lower().replace("_", "") for l in loss_list]
    loss_fs = []
    for l in loss_list:
        if l == "diceloss":
            loss_fs.append(DiceLoss)
        elif l == "jaccardloss":
            loss_fs.append(JaccardLoss)
        elif l == "l1loss":
            loss_fs.append(L1Loss)
        elif l == "bceloss":
            loss_fs.append(BCELoss)
        elif l == "crossentropyloss":
            loss_fs.append(CrossEntropyLoss)
        else:
            if l == "bcewithlogitsloss":
                loss_fs.append(BCEWithLogitsLoss)

    all_loss = None
    for l in loss_fs:
        if all_loss is not None:
            all_loss = all_loss + l(**kwargs)
        else:
            all_loss = l(**kwargs)

    return all_loss

"""Metrics for segmentation.
"""

import torch
import math
import numpy as np

class Metrics:
    """Tracking mean metrics
    """

    def __init__(self, labels):
        """Creates an new `Metrics` instance.

        Args:
          labels: the labels for all classes.
        """

        self.labels = labels

        self.tn = 0
        self.fn = 0
        self.fp = 0
        self.tp = 0
        self.inf = 1e-6

    def add(self, actual, predicted):
        """Adds an observation to the tracker.

        Args:
          actual: the ground truth labels.
          predicted: the predicted labels.
        """

        confusion = predicted.view(-1).float() / actual.view(-1).float()

        self.tn += torch.sum(torch.isnan(confusion)).item()
        self.fn += torch.sum(confusion == float("inf")).item()
        self.fp += torch.sum(confusion == 0).item()
        self.tp += torch.sum(confusion == 1).item()


    def get_precision(self):
        try:
            val = self.tp / (self.tp + self.fp)
        except ZeroDivisionError:
            val = self.inf
        return val

    def get_recall(self):
        try:
            val = self.tp / (self.tp + self.fn)
        except ZeroDivisionError:
            val = self.inf
        return val

    def get_f_score(self):

        pr = 2 * (self.tp / (self.tp + self.fp + self.inf)) * (self.tp / (self.tp + self.fn + self.inf))
        p_r = (self.tp / (self.tp + self.fp + self.inf)) + (self.tp / (self.tp + self.fn + self.inf))
        return pr / (p_r + self.inf)

    def get_oa(self):

        t_pn = self.tp + self.tn
        t_tpn = self.tp + self.tn + self.fp + self.fn + self.inf
        return t_pn / (t_tpn + self.inf)

    def get_miou(self):
        """Retrieves the mean Intersection over Union score.

        Returns:
          The mean Intersection over Union score for all observations seen so far.
        """
        return np.nanmean([self.tn / (self.tn + self.fn + self.fp), self.tp / (self.tp + self.fn + self.fp)])

    def get_fg_iou(self):
        """Retrieves the foreground Intersection over Union score.

        Returns:
          The foreground Intersection over Union score for all observations seen so far.
        """

        try:
            iou = self.tp / (self.tp + self.fn + self.fp)
        except ZeroDivisionError:
            iou = self.inf

        return iou

    def get_mcc(self):
        """Retrieves the Matthew's Coefficient Correlation score.

        Returns:
          The Matthew's Coefficient Correlation score for all observations seen so far.
        """

        try:
            mcc = (self.tp * self.tn - self.fp * self.fn) / math.sqrt(
                (self.tp + self.fp) * (self.tp + self.fn) * (self.tn + self.fp) * (self.tn + self.fn)
            )
        except ZeroDivisionError:
            mcc = self.inf

        return mcc

# Todo:
# - Rewrite mIoU to handle N classes (and not only binary SemSeg)


class Metrics_multi:
    """Tracking mean metrics
    """

    def __init__(self, labels):
        """Creates an new `Metrics` instance.

        Args:
          labels: the labels for all classes.
        """

        self.labels = labels

        self.tn = [0]*self.labels
        self.fn = [0]*self.labels
        self.fp = [0]*self.labels
        self.tp = [0]*self.labels
        self.inf = [1e-6]*self.labels

    def add_(self, actual, predicted):
        """Adds an observation to the tracker.

        Args:
          actual: the ground truth labels.
          predicted: the predicted labels.
        """

        confusion = predicted.view(-1).float() / actual.view(-1).float()

        self.tn += torch.sum(torch.isnan(confusion)).item()
        self.fn += torch.sum(confusion == float("inf")).item()
        self.fp += torch.sum(confusion == 0).item()
        self.tp += torch.sum(confusion == 1).item()

    def add(self, actual, predicted):
        """Adds an observation to the tracker.

        Args:
          actual: the ground truth labels.
          predicted: the predicted labels.
        """
        mask_unique = np.unique(actual)
        # self.mask_unique = mask_unique
        for mask_unique_label in mask_unique:
            mask1 = np.where(actual == mask_unique_label, 1, 0)
            pred1 = np.where(predicted == mask_unique_label, 1, 0)

            # confusion = predicted.view(-1).float() / actual.view(-1).float()
            confusion = torch.from_numpy(pred1.reshape(-1)/mask1.reshape(-1))
            # confusion = pred1.reshape(-1) / mask1.reshape(-1)
            mask_unique_label=int(mask_unique_label)
            self.tn[mask_unique_label] += torch.sum(torch.isnan(confusion)).item()
            self.fn[mask_unique_label] += torch.sum(confusion == float("inf")).item()
            self.fp[mask_unique_label] += torch.sum(confusion == 0).item()
            self.tp[mask_unique_label] += torch.sum(confusion == 1).item()

    def get_precision(self):
        val = [0]*self.labels
        for i in range(self.labels):
            try:
                val[i] = self.tp[i] / (self.tp[i] + self.fp[i])
            except ZeroDivisionError:
                val[i] = self.inf[i]
        return val

    def get_recall(self):
        val = [0]*self.labels
        for i in range(self.labels):
            try:
                val[i] = self.tp[i] / (self.tp[i] + self.fn[i])
            except ZeroDivisionError:
                val[i] = self.inf[i]
        return val

    def get_f_score(self):
        f1 = [0]*self.labels
        for i in range(self.labels):
            pr = 2 * (self.tp[i] / (self.tp[i] + self.fp[i] + self.inf[i])) * (self.tp[i] / (self.tp[i] + self.fn[i] + self.inf[i]))
            p_r = (self.tp[i] / (self.tp[i] + self.fp[i] + self.inf[i])) + (self.tp[i] / (self.tp[i] + self.fn[i] + self.inf[i]))
            f1[i] =  pr / (p_r + self.inf[0])

        return f1

    def get_oa(self):

        t_pn = self.tp + self.tn
        t_tpn = self.tp + self.tn + self.fp + self.fn + self.inf
        return t_pn / (t_tpn + self.inf)

    def get_miou(self):
        """Retrieves the mean Intersection over Union score.

        Returns:
          The mean Intersection over Union score for all observations seen so far.
        """
        # return np.nanmean([self.tn / (self.tn + self.fn + self.fp), self.tp / (self.tp + self.fn + self.fp)])
        return np.nanmean([
            np.array(self.tn) / (np.array(self.tn) + np.array(self.fn) + np.array(self.fp)),
            np.array(self.tp) / (np.array(self.tp) + np.array(self.fn) + np.array(self.fp))
        ])

    def get_fg_iou(self):
        """Retrieves the foreground Intersection over Union score.

        Returns:
          The foreground Intersection over Union score for all observations seen so far.
        """
        iou = [0]*self.labels
        for i in range(self.labels):

            try:
                iou[i] = self.tp[i] / (self.tp[i] + self.fn[i] + self.fp[i])
            except ZeroDivisionError:
                iou[i] = self.inf[i]

        return iou

    def get_mcc(self):
        """Retrieves the Matthew's Coefficient Correlation score.

        Returns:
          The Matthew's Coefficient Correlation score for all observations seen so far.
        """
        mcc = [0]*self.labels
        for i in self.mask_unique:
            if i==0:
                continue
            try:
                mcc[i] = (self.tp[i] * self.tn[i] - self.fp[i] * self.fn[i]) / math.sqrt(
                    (self.tp[i] + self.fp[i]) * (self.tp[i] + self.fn[i]) * (self.tn[i] + self.fp[i]) * (self.tn[i] + self.fn[i])
                )
            except ZeroDivisionError:
                mcc[i] = self.inf

        return mcc

# 获取单张图片对应的评价指标
def precision_recall_mean_image(mask, predicted,num_classes,name='precision'):

    stn = [0]* num_classes
    sfn = [0]* num_classes
    sfp = [0]* num_classes
    stp = [0]* num_classes
    sinf = [1e-6]* num_classes

    mask_unique = np.unique(mask)

    for mask_unique_label in mask_unique:
        mask1 = np.where(mask == mask_unique_label, 1, 0)
        pred1 = np.where(predicted == mask_unique_label, 1, 0)

        # confusion = predicted.view(-1).float() / actual.view(-1).float()
        confusion = torch.from_numpy(pred1.reshape(-1) / mask1.reshape(-1))
        mask_unique_label=int(mask_unique_label)

        stn[mask_unique_label] += torch.sum(torch.isnan(confusion)).item()
        sfn[mask_unique_label] += torch.sum(confusion == float("inf")).item()
        sfp[mask_unique_label] += torch.sum(confusion == 0).item()
        stp[mask_unique_label] += torch.sum(confusion == 1).item()

    mean_metrics = None
    if name == 'each_epoch_error':
        precision = [0] * num_classes
        for i in range(num_classes):
            try:
                precision[i] = stp[i] / (stp[i] + sfp[i])
            except ZeroDivisionError:
                precision[i] = sinf[i]
        mean_prec = sum(precision)/len(precision)
        mean_metrics = 1 - mean_prec
    elif name == 'each_epoch_error':
        recall = [0] * num_classes
        for i in range(num_classes):
            try:
                recall[i] = stp[i] / (stp[i] + sfn[i])
            except ZeroDivisionError:
                recall[i] = sinf[i]
        mean_recall = sum(recall)/len(recall)
        mean_metrics = 1- mean_recall

    return mean_metrics
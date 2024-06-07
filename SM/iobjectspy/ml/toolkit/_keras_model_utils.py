# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\toolkit\_keras_model_utils.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 16930 bytes
"""
@author: YangRuijie
@license: 
@contact: yangruijie@supermap.com
@software: 
@file: _keras_model_utils.py
@time: 5/24/19 6:46 AM
@desc: 主要实现一些keras 模型的自定义损失函数和自定义操作等
"""
import os, re, time, tensorflow as tf, numpy as np
from keras.callbacks import Callback, ModelCheckpoint
from keras.losses import binary_crossentropy
from keras import backend as K

def mean_iou(y_true, y_pred):
    prec = []
    for t in np.arange(0.5, 1.0, 0.05):
        y_pred_ = tf.to_int32(y_pred > t)
        score, up_opt = tf.metrics.mean_iou(y_true, y_pred_, 2)
        K.get_session().run(tf.local_variables_initializer())
        with tf.control_dependencies([up_opt]):
            score = tf.identity(score)
        prec.append(score)

    return K.mean((K.stack(prec)), axis=0)


def dice_coef(y_true, y_pred):
    smooth = 1e-10
    y_true_f = K.flatten(y_true)
    y_pred_f = K.flatten(y_pred)
    intersection = K.sum(y_true_f * y_pred_f)
    return (2.0 * intersection + smooth) / (K.sum(y_true_f) + K.sum(y_pred_f) + smooth)


def bce_dice_loss(y_true, y_pred):
    return 0.5 * binary_crossentropy(y_true, y_pred) + 0.5 * (1.0 - dice_coef(y_true, y_pred))


def find_last(log_dir, model_name, best=True):
    """Finds the last checkpoint file of the last trained model in the
    model directory.
    Returns:
        The path of the last checkpoint file
    """
    if not os.path.exists(log_dir):
        return
    dir_names = next(os.walk(log_dir))[1]
    dir_names = filter((lambda f: re.match("^(?:(?!0000)[0-9]{4}-(?:(?:0[1-9]|1[0-2])-(?:0[1-9]|1[0-9]|2[0-8])|(?:0[13-9]|1[0-2])-(?:29|30)|(?:0[13578]|1[02])-31)|(?:[0-9]{2}(?:0[48]|[2468][048]|[13579][26])|(?:0[48]|[2468][048]|[13579][26])00)-02-29)$", f)), dir_names)
    dir_names = sorted(dir_names, reverse=True)
    for dir in dir_names:
        checkpoints_dir = os.path.join(log_dir, dir, model_name, "checkpoints")
        if os.path.exists(checkpoints_dir):
            if not best:
                if os.path.exists(os.path.join(checkpoints_dir, "latest.h5")):
                    return os.path.join(checkpoints_dir, "latest.h5")
            file_names = next(os.walk(checkpoints_dir))[2]
            match_str = "^" + model_name + "-[0-9]*[1-9][0-9]*-([0-9]{1,}[.][0-9]*).hdf5$"
            file_names = list(filter((lambda f: re.match(match_str, f)), file_names))
            file_modify = []
            for file in file_names:
                mtime = os.stat(os.path.join(checkpoints_dir, file)).st_mtime
                file_modify_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mtime))
                file_modify.append((file, file_modify_time))

            file_modify = sorted(file_modify, key=(lambda x: x[1]))
            if len(file_names) > 0:
                return os.path.join(checkpoints_dir, file_modify[-1][0])


SMOOTH = 1e-05

def _gather_channels(x, indexes, **kwargs):
    """Slice tensor along channels axis by given indexes"""
    backend = kwargs["backend"]
    if backend.image_data_format() == "channels_last":
        x = backend.permute_dimensions(x, (3, 0, 1, 2))
        x = backend.gather(x, indexes)
        x = backend.permute_dimensions(x, (1, 2, 3, 0))
    else:
        x = backend.permute_dimensions(x, (1, 0, 2, 3))
        x = backend.gather(x.indexes)
        x = backend.permute_dimensions(x, (1, 0, 2, 3))
    return x


def get_reduce_axes(per_image, **kwargs):
    backend = kwargs["backend"]
    axes = [1, 2] if backend.image_data_format() == "channels_last" else [2, 3]
    if not per_image:
        axes.insert(0, 0)
    return axes


def gather_channels(*xs, indexes=None, **kwargs):
    """Slice tensors along channels axis by given indexes"""
    if indexes is None:
        return xs
    if isinstance(indexes, int):
        indexes = [
         indexes]
    xs = [_gather_channels(x, indexes=indexes, **kwargs) for x in xs]
    return xs


def round_if_needed(x, threshold, **kwargs):
    backend = kwargs["backend"]
    if threshold is not None:
        x = backend.greater(x, threshold)
        x = backend.cast(x, backend.floatx())
    return x


def average(x, per_image=False, class_weights=None, **kwargs):
    backend = kwargs["backend"]
    if per_image:
        x = backend.mean(x, axis=0)
    if class_weights is not None:
        x = x * class_weights
    return backend.mean(x)


def iou_score(gt, pr, class_weights=1.0, class_indexes=None, smooth=SMOOTH, per_image=False, threshold=None, **kwargs):
    r""" The `Jaccard index`_, also known as Intersection over Union and the Jaccard similarity coefficient
    (originally coined coefficient de communaut¨¦ by Paul Jaccard), is a statistic used for comparing the
    similarity and diversity of sample sets. The Jaccard coefficient measures similarity between finite sample sets,
    and is defined as the size of the intersection divided by the size of the union of the sample sets:

    .. math:: J(A, B) = \frac{A \cap B}{A \cup B}

    Args:
        gt: ground truth 4D keras tensor (B, H, W, C) or (B, C, H, W)
        pr: prediction 4D keras tensor (B, H, W, C) or (B, C, H, W)
        class_weights: 1. or list of class weights, len(weights) = C
        class_indexes: Optional integer or list of integers, classes to consider, if ``None`` all classes are used.
        smooth: value to avoid division by zero
        per_image: if ``True``, metric is calculated as mean over images in batch (B),
            else over whole batch
        threshold: value to round predictions (use ``>`` comparison), if ``None`` prediction will not be round

    Returns:
        IoU/Jaccard score in range [0, 1]

    .. _`Jaccard index`: https://en.wikipedia.org/wiki/Jaccard_index

    """
    backend = kwargs["backend"]
    gt, pr = gather_channels(gt, pr, indexes=class_indexes, **kwargs)
    pr = round_if_needed(pr, threshold, **kwargs)
    axes = get_reduce_axes(per_image, **kwargs)
    intersection = backend.sum((gt * pr), axis=axes)
    union = backend.sum((gt + pr), axis=axes) - intersection
    score = (intersection + smooth) / (union + smooth)
    score = average(score, per_image, class_weights, **kwargs)
    return score


def f_score(gt, pr, beta=1, class_weights=1, class_indexes=None, smooth=SMOOTH, per_image=False, threshold=None, **kwargs):
    r"""The F-score (Dice coefficient) can be interpreted as a weighted average of the precision and recall,
    where an F-score reaches its best value at 1 and worst score at 0.
    The relative contribution of ``precision`` and ``recall`` to the F1-score are equal.
    The formula for the F score is:

    .. math:: F_\beta(precision, recall) = (1 + \beta^2) \frac{precision \cdot recall}
        {\beta^2 \cdot precision + recall}

    The formula in terms of *Type I* and *Type II* errors:

    .. math:: F_\beta(A, B) = \frac{(1 + \beta^2) TP} {(1 + \beta^2) TP + \beta^2 FN + FP}

    where:
        TP - true positive;
        FP - false positive;
        FN - false negative;

    Args:
        gt: ground truth 4D keras tensor (B, H, W, C) or (B, C, H, W)
        pr: prediction 4D keras tensor (B, H, W, C) or (B, C, H, W)
        class_weights: 1. or list of class weights, len(weights) = C
        class_indexes: Optional integer or list of integers, classes to consider, if ``None`` all classes are used.
        beta: f-score coefficient
        smooth: value to avoid division by zero
        per_image: if ``True``, metric is calculated as mean over images in batch (B),
            else over whole batch
        threshold: value to round predictions (use ``>`` comparison), if ``None`` prediction will not be round

    Returns:
        F-score in range [0, 1]

    """
    backend = kwargs["backend"]
    gt, pr = gather_channels(gt, pr, indexes=class_indexes, **kwargs)
    pr = round_if_needed(pr, threshold, **kwargs)
    axes = get_reduce_axes(per_image, **kwargs)
    tp = backend.sum((gt * pr), axis=axes)
    fp = backend.sum(pr, axis=axes) - tp
    fn = backend.sum(gt, axis=axes) - tp
    score = ((1 + beta ** 2) * tp + smooth) / ((1 + beta ** 2) * tp + beta ** 2 * fn + fp + smooth)
    score = average(score, per_image, class_weights, **kwargs)
    return score


def precision(gt, pr, class_weights=1, class_indexes=None, smooth=SMOOTH, per_image=False, threshold=None, **kwargs):
    r"""Calculate precision between the ground truth (gt) and the prediction (pr).

    .. math:: F_\beta(tp, fp) = \frac{tp} {(tp + fp)}

    where:
         - tp - true positives;
         - fp - false positives;

    Args:
        gt: ground truth 4D keras tensor (B, H, W, C) or (B, C, H, W)
        pr: prediction 4D keras tensor (B, H, W, C) or (B, C, H, W)
        class_weights: 1. or ``np.array`` of class weights (``len(weights) = num_classes``)
        class_indexes: Optional integer or list of integers, classes to consider, if ``None`` all classes are used.
        smooth: Float value to avoid division by zero.
        per_image: If ``True``, metric is calculated as mean over images in batch (B),
            else over whole batch.
        threshold: Float value to round predictions (use ``>`` comparison), if ``None`` prediction will not be round.
        name: Optional string, if ``None`` default ``precision`` name is used.

    Returns:
        float: precision score
    """
    backend = kwargs["backend"]
    gt, pr = gather_channels(gt, pr, indexes=class_indexes, **kwargs)
    pr = round_if_needed(pr, threshold, **kwargs)
    axes = get_reduce_axes(per_image, **kwargs)
    tp = backend.sum((gt * pr), axis=axes)
    fn = backend.sum(gt, axis=axes) - tp
    score = (tp + smooth) / (tp + fn + smooth)
    score = average(score, per_image, class_weights, **kwargs)
    return score


def recall(gt, pr, class_weights=1, class_indexes=None, smooth=SMOOTH, per_image=False, threshold=None, **kwargs):
    r"""Calculate recall between the ground truth (gt) and the prediction (pr).

    .. math:: F_\beta(tp, fn) = \frac{tp} {(tp + fn)}

    where:
         - tp - true positives;
         - fp - false positives;

    Args:
        gt: ground truth 4D keras tensor (B, H, W, C) or (B, C, H, W)
        pr: prediction 4D keras tensor (B, H, W, C) or (B, C, H, W)
        class_weights: 1. or ``np.array`` of class weights (``len(weights) = num_classes``)
        class_indexes: Optional integer or list of integers, classes to consider, if ``None`` all classes are used.
        smooth: Float value to avoid division by zero.
        per_image: If ``True``, metric is calculated as mean over images in batch (B),
            else over whole batch.
        threshold: Float value to round predictions (use ``>`` comparison), if ``None`` prediction will not be round.
        name: Optional string, if ``None`` default ``precision`` name is used.

    Returns:
        float: recall score
    """
    backend = kwargs["backend"]
    gt, pr = gather_channels(gt, pr, indexes=class_indexes, **kwargs)
    pr = round_if_needed(pr, threshold, **kwargs)
    axes = get_reduce_axes(per_image, **kwargs)
    tp = backend.sum((gt * pr), axis=axes)
    fp = backend.sum(pr, axis=axes) - tp
    score = (tp + smooth) / (tp + fp + smooth)
    score = average(score, per_image, class_weights, **kwargs)
    return score


def categorical_crossentropy(gt, pr, class_weights=1.0, class_indexes=None, **kwargs):
    backend = kwargs["backend"]
    gt, pr = gather_channels(gt, pr, indexes=class_indexes, **kwargs)
    axis = 3 if backend.image_data_format() == "channels_last" else 1
    pr /= backend.sum(pr, axis=axis, keepdims=True)
    pr = backend.clip(pr, backend.epsilon(), 1 - backend.epsilon())
    output = gt * backend.log(pr) * class_weights
    return -backend.sum(output, axis=axis)


def bianary_crossentropy(gt, pr, **kwargs):
    backend = kwargs["backend"]
    return backend.mean(backend.binary_crossentropy(gt, pr))


def categorical_focal_loss(gt, pr, gamma=2.0, alpha=0.25, class_indexes=None, **kwargs):
    """Implementation of Focal Loss from the paper in multiclass classification

    Formula:
        loss = - gt * alpha * ((1 - pr)^gamma) * log(pr)

    Args:
        gt: ground truth 4D keras tensor (B, H, W, C) or (B, C, H, W)
        pr: prediction 4D keras tensor (B, H, W, C) or (B, C, H, W)
        alpha: the same as weighting factor in balanced cross entropy, default 0.25
        gamma: focusing parameter for modulating factor (1-p), default 2.0
        class_indexes: Optional integer or list of integers, classes to consider, if ``None`` all classes are used.

    """
    backend = kwargs["backend"]
    gt, pr = gather_channels(gt, pr, indexes=class_indexes, **kwargs)
    pr = backend.clip(pr, backend.epsilon(), 1.0 - backend.epsilon())
    loss = -gt * (alpha * backend.pow(1 - pr, gamma) * backend.log(pr))
    return backend.sum(loss)


def binary_focal_loss(gt, pr, gamma=2.0, alpha=0.25, **kwargs):
    r"""Implementation of Focal Loss from the paper in binary classification

    Formula:
        loss = - gt * alpha * ((1 - pr)^gamma) * log(pr) \
               - (1 - gt) * alpha * (pr^gamma) * log(1 - pr)

    Args:
        gt: ground truth 4D keras tensor (B, H, W, C) or (B, C, H, W)
        pr: prediction 4D keras tensor (B, H, W, C) or (B, C, H, W)
        alpha: the same as weighting factor in balanced cross entropy, default 0.25
        gamma: focusing parameter for modulating factor (1-p), default 2.0

    """
    backend = kwargs["backend"]
    pr = backend.clip(pr, backend.epsilon(), 1.0 - backend.epsilon())
    loss_1 = -gt * (alpha * backend.pow(1 - pr, gamma) * backend.log(pr))
    loss_0 = -(1 - gt) * (alpha * backend.pow(pr, gamma) * backend.log(1 - pr))
    loss = backend.mean(loss_0 + loss_1)
    return loss


class ModelCheckpointLatest(Callback):
    __doc__ = "\n    save latest checkpoint\n    :param filepath:  save dir\n    :param name: file name ,default 'latest.h5'\n    :param verbose: print out ,0 not out ,other out\n    "

    def __init__(self, filepath, name='latest.h5', verbose=0):
        super(ModelCheckpointLatest, self).__init__()
        self.verbose = verbose
        self.filepath = os.path.join(filepath, name)
        self.epochs_since_last_save = 0

    def on_epoch_end(self, epoch, logs=None):
        self.model.save_weights((self.filepath), overwrite=True)
        self.epochs_since_last_save += 1
        if self.verbose > 0:
            print("\nEpoch %05d: saving model to %s" % (epoch + 1, self.filepath))


class ParallelModelCheckpoint(ModelCheckpoint):

    def __init__(self, model, filepath, monitor='val_loss', verbose=0, save_best_only=False, save_weights_only=False, mode='auto', period=1):
        self.single_model = model
        super(ParallelModelCheckpoint, self).__init__(filepath, monitor, verbose, save_best_only, save_weights_only, mode, period)

    def set_model(self, model):
        super(ParallelModelCheckpoint, self).set_model(self.single_model)


class ParallelModelCheckpointLatest(Callback):
    __doc__ = "\n    Parallel train\n    save latest checkpoint\n    :param filepath:  save dir\n    :param name: file name ,default 'latest.h5'\n    :param verbose: print out ,0 not out ,other out\n    "

    def __init__(self, model, filepath, name='latest.h5', verbose=0):
        super(ParallelModelCheckpointLatest, self).__init__()
        self.verbose = verbose
        self.filepath = os.path.join(filepath, name)
        self.epochs_since_last_save = 0
        self.single_model = model

    def set_model(self, model):
        super(ParallelModelCheckpointLatest, self).set_model(self.single_model)

    def on_epoch_end(self, epoch, logs=None):
        self.model.save_weights((self.filepath), overwrite=True)
        self.epochs_since_last_save += 1
        if self.verbose > 0:
            print("\nEpoch %05d: saving model to %s" % (epoch + 1, self.filepath))

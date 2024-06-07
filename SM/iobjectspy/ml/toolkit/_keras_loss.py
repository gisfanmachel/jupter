# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\toolkit\_keras_loss.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 20438 bytes
"""
@author: YangRuijie
@license: 
@contact: yangruijie@supermap.com
@software: 
@file: _keras_loss.py
@time: 8/16/19 2:18 PM
@desc:
"""
from . import _keras_model_utils as F
from keras import backend as K
import tensorflow as tf
SMOOTH = 1e-05

class KerasObject:
    _backend = None
    _models = None
    _layers = None
    _utils = None

    def __init__(self, name=None):
        self._name = name

    @property
    def __name__(self):
        if self._name is None:
            return self.__class__.__name__
        return self._name

    @property
    def name(self):
        return self.__name__

    @name.setter
    def name(self, name):
        self._name = name

    @classmethod
    def set_submodules(cls, backend, layers, models, utils):
        cls._backend = backend
        cls._layers = layers
        cls._models = models
        cls._utils = utils

    @property
    def submodules(self):
        return {'backend':self.backend, 
         'layers':self.layers, 
         'models':self.models, 
         'utils':self.utils}

    @property
    def backend(self):
        return self._backend

    @property
    def layers(self):
        return self._layers

    @property
    def models(self):
        return self._models

    @property
    def utils(self):
        return self._utils


KerasObject.set_submodules(K, None, None, None)

class Metric(KerasObject):
    pass


class IOUScore(Metric):
    __doc__ = " The `Jaccard index`_, also known as Intersection over Union and the Jaccard similarity coefficient\n    (originally coined coefficient de communaut¨¦ by Paul Jaccard), is a statistic used for comparing the\n    similarity and diversity of sample sets. The Jaccard coefficient measures similarity between finite sample sets,\n    and is defined as the size of the intersection divided by the size of the union of the sample sets:\n    .. math:: J(A, B) = \\frac{A \\cap B}{A \\cup B}\n    Args:\n        class_weights: 1. or ``np.array`` of class weights (``len(weights) = num_classes``).\n        class_indexes: Optional integer or list of integers, classes to consider, if ``None`` all classes are used.\n        smooth: value to avoid division by zero\n        per_image: if ``True``, metric is calculated as mean over images in batch (B),\n            else over whole batch\n        threshold: value to round predictions (use ``>`` comparison), if ``None`` prediction will not be round\n    Returns:\n       A callable ``iou_score`` instance. Can be used in ``model.compile(...)`` function.\n    .. _`Jaccard index`: https://en.wikipedia.org/wiki/Jaccard_index\n    Example:\n    .. code:: python\n        metric = IOUScore()\n        model.compile('SGD', loss=loss, metrics=[metric])\n    "

    def __init__(self, class_weights=None, class_indexes=None, threshold=None, per_image=False, smooth=SMOOTH, name=None):
        name = name or "iou_score"
        super().__init__(name=name)
        self.class_weights = class_weights if class_weights is not None else 1
        self.class_indexes = class_indexes
        self.threshold = threshold
        self.per_image = per_image
        self.smooth = smooth

    def __call__(self, gt, pr):
        return (F.iou_score)(
 gt,
 pr, class_weights=self.class_weights, 
         class_indexes=self.class_indexes, 
         smooth=self.smooth, 
         per_image=self.per_image, 
         threshold=self.threshold, **self.submodules)


class FScore(Metric):
    __doc__ = "The F-score (Dice coefficient) can be interpreted as a weighted average of the precision and recall,\n    where an F-score reaches its best value at 1 and worst score at 0.\n    The relative contribution of ``precision`` and ``recall`` to the F1-score are equal.\n    The formula for the F score is:\n    .. math:: F_\\beta(precision, recall) = (1 + \\beta^2) \\frac{precision \\cdot recall}\n        {\\beta^2 \\cdot precision + recall}\n    The formula in terms of *Type I* and *Type II* errors:\n    .. math:: L(tp, fp, fn) = \\frac{(1 + \\beta^2) \\cdot tp} {(1 + \\beta^2) \\cdot fp + \\beta^2 \\cdot fn + fp}\n    where:\n         - tp - true positives;\n         - fp - false positives;\n         - fn - false negatives;\n    Args:\n        beta: Integer of float f-score coefficient to balance precision and recall.\n        class_weights: 1. or ``np.array`` of class weights (``len(weights) = num_classes``)\n        class_indexes: Optional integer or list of integers, classes to consider, if ``None`` all classes are used.\n        smooth: Float value to avoid division by zero.\n        per_image: If ``True``, metric is calculated as mean over images in batch (B),\n            else over whole batch.\n        threshold: Float value to round predictions (use ``>`` comparison), if ``None`` prediction will not be round.\n        name: Optional string, if ``None`` default ``f{beta}-score`` name is used.\n    Returns:\n        A callable ``f_score`` instance. Can be used in ``model.compile(...)`` function.\n    Example:\n    .. code:: python\n        metric = FScore()\n        model.compile('SGD', loss=loss, metrics=[metric])\n    "

    def __init__(self, beta=1, class_weights=None, class_indexes=None, threshold=None, per_image=False, smooth=SMOOTH, name=None):
        name = name or "f{}-score".format(beta)
        super().__init__(name=name)
        self.beta = beta
        self.class_weights = class_weights if class_weights is not None else 1
        self.class_indexes = class_indexes
        self.threshold = threshold
        self.per_image = per_image
        self.smooth = smooth

    def __call__(self, gt, pr):
        return (F.f_score)(
 gt,
 pr, beta=self.beta, 
         class_weights=self.class_weights, 
         class_indexes=self.class_indexes, 
         smooth=self.smooth, 
         per_image=self.per_image, 
         threshold=self.threshold, **self.submodules)


class Precision(Metric):
    __doc__ = "Creates a criterion that measures the Precision between the\n    ground truth (gt) and the prediction (pr).\n    .. math:: F_\\beta(tp, fp) = \\frac{tp} {(tp + fp)}\n    where:\n         - tp - true positives;\n         - fp - false positives;\n    Args:\n        class_weights: 1. or ``np.array`` of class weights (``len(weights) = num_classes``).\n        class_indexes: Optional integer or list of integers, classes to consider, if ``None`` all classes are used.\n        smooth: Float value to avoid division by zero.\n        per_image: If ``True``, metric is calculated as mean over images in batch (B),\n            else over whole batch.\n        threshold: Float value to round predictions (use ``>`` comparison), if ``None`` prediction will not be round.\n        name: Optional string, if ``None`` default ``precision`` name is used.\n    Returns:\n        A callable ``precision`` instance. Can be used in ``model.compile(...)`` function.\n    Example:\n    .. code:: python\n        metric = Precision()\n        model.compile('SGD', loss=loss, metrics=[metric])\n    "

    def __init__(self, class_weights=None, class_indexes=None, threshold=None, per_image=False, smooth=SMOOTH, name=None):
        name = name or "precision"
        super().__init__(name=name)
        self.class_weights = class_weights if class_weights is not None else 1
        self.class_indexes = class_indexes
        self.threshold = threshold
        self.per_image = per_image
        self.smooth = smooth

    def __call__(self, gt, pr):
        return (F.precision)(
 gt,
 pr, class_weights=self.class_weights, 
         class_indexes=self.class_indexes, 
         smooth=self.smooth, 
         per_image=self.per_image, 
         threshold=self.threshold, **self.submodules)


class Recall(Metric):
    __doc__ = "Creates a criterion that measures the Precision between the\n    ground truth (gt) and the prediction (pr).\n    .. math:: F_\\beta(tp, fn) = \\frac{tp} {(tp + fn)}\n    where:\n         - tp - true positives;\n         - fn - false negatives;\n    Args:\n        class_weights: 1. or ``np.array`` of class weights (``len(weights) = num_classes``).\n        class_indexes: Optional integer or list of integers, classes to consider, if ``None`` all classes are used.\n        smooth: Float value to avoid division by zero.\n        per_image: If ``True``, metric is calculated as mean over images in batch (B),\n            else over whole batch.\n        threshold: Float value to round predictions (use ``>`` comparison), if ``None`` prediction will not be round.\n        name: Optional string, if ``None`` default ``recall`` name is used.\n    Returns:\n        A callable ``recall`` instance. Can be used in ``model.compile(...)`` function.\n    Example:\n    .. code:: python\n        metric = Precision()\n        model.compile('SGD', loss=loss, metrics=[metric])\n    "

    def __init__(self, class_weights=None, class_indexes=None, threshold=None, per_image=False, smooth=SMOOTH, name=None):
        name = name or "recall"
        super().__init__(name=name)
        self.class_weights = class_weights if class_weights is not None else 1
        self.class_indexes = class_indexes
        self.threshold = threshold
        self.per_image = per_image
        self.smooth = smooth

    def __call__(self, gt, pr):
        return (F.recall)(
 gt,
 pr, class_weights=self.class_weights, 
         class_indexes=self.class_indexes, 
         smooth=self.smooth, 
         per_image=self.per_image, 
         threshold=self.threshold, **self.submodules)


class Loss(KerasObject):

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


class MultipliedLoss(Loss):

    def __init__(self, loss, multiplier):
        if len(loss.__name__.split("+")) > 1:
            name = "{} * ({})".format(multiplier, loss.__name__)
        else:
            name = "{} * {}".format(multiplier, loss.__name__)
        super().__init__(name=name)
        self.loss = loss
        self.multiplier = multiplier

    def __call__(self, gt, pr):
        return self.multiplier * self.loss(gt, pr)


class SumOfLosses(Loss):

    def __init__(self, l1, l2):
        name = "{}_p_{}".format(l1.__name__, l2.__name__)
        super().__init__(name=name)
        self.l1 = l1
        self.l2 = l2

    def __call__(self, gt, pr):
        return self.l1(gt, pr) + self.l2(gt, pr)


class JaccardLoss(Loss):
    __doc__ = "Creates a criterion to measure Jaccard loss:\n\n    .. math:: L(A, B) = 1 - \\frac{A \\cap B}{A \\cup B}\n\n    Args:\n        class_weights: Array (``np.array``) of class weights (``len(weights) = num_classes``).\n        class_indexes: Optional integer or list of integers, classes to consider, if ``None`` all classes are used.\n        per_image: If ``True`` loss is calculated for each image in batch and then averaged,\n            else loss is calculated for the whole batch.\n        smooth: Value to avoid division by zero.\n\n    Returns:\n         A callable ``jaccard_loss`` instance. Can be used in ``model.compile(...)`` function\n         or combined with other losses.\n\n    Example:\n\n    .. code:: python\n\n        loss = JaccardLoss()\n        model.compile('SGD', loss=loss)\n    "

    def __init__(self, class_weights=None, class_indexes=None, per_image=False, smooth=SMOOTH):
        super().__init__(name="jaccard_loss")
        self.class_weights = class_weights if class_weights is not None else 1
        self.class_indexes = class_indexes
        self.per_image = per_image
        self.smooth = smooth

    def __call__(self, gt, pr):
        return 1 - (F.iou_score)(
 gt,
 pr, class_weights=self.class_weights, 
         class_indexes=self.class_indexes, 
         smooth=self.smooth, 
         per_image=self.per_image, 
         threshold=None, **self.submodules)


class DiceLoss(Loss):
    __doc__ = "Creates a criterion to measure Dice loss:\n\n    .. math:: L(precision, recall) = 1 - (1 + \\beta^2) \\frac{precision \\cdot recall}\n        {\\beta^2 \\cdot precision + recall}\n\n    The formula in terms of *Type I* and *Type II* errors:\n\n    .. math:: L(tp, fp, fn) = \\frac{(1 + \\beta^2) \\cdot tp} {(1 + \\beta^2) \\cdot fp + \\beta^2 \\cdot fn + fp}\n\n    where:\n         - tp - true positives;\n         - fp - false positives;\n         - fn - false negatives;\n\n    Args:\n        beta: Float or integer coefficient for precision and recall balance.\n        class_weights: Array (``np.array``) of class weights (``len(weights) = num_classes``).\n        class_indexes: Optional integer or list of integers, classes to consider, if ``None`` all classes are used.\n        per_image: If ``True`` loss is calculated for each image in batch and then averaged,\n        else loss is calculated for the whole batch.\n        smooth: Value to avoid division by zero.\n\n    Returns:\n        A callable ``dice_loss`` instance. Can be used in ``model.compile(...)`` function`\n        or combined with other losses.\n\n    Example:\n\n    .. code:: python\n\n        loss = DiceLoss()\n        model.compile('SGD', loss=loss)\n    "

    def __init__(self, beta=1, class_weights=None, class_indexes=None, per_image=False, smooth=SMOOTH):
        super().__init__(name="dice_loss")
        self.beta = beta
        self.class_weights = class_weights if class_weights is not None else 1
        self.class_indexes = class_indexes
        self.per_image = per_image
        self.smooth = smooth

    def __call__(self, gt, pr):
        return 1 - (F.f_score)(
 gt,
 pr, beta=self.beta, 
         class_weights=self.class_weights, 
         class_indexes=self.class_indexes, 
         smooth=self.smooth, 
         per_image=self.per_image, 
         threshold=None, **self.submodules)


class BinaryCELoss(Loss):
    __doc__ = "Creates a criterion that measures the Binary Cross Entropy between the\n    ground truth (gt) and the prediction (pr).\n\n    .. math:: L(gt, pr) = - gt \\cdot \\log(pr) - (1 - gt) \\cdot \\log(1 - pr)\n\n    Returns:\n        A callable ``binary_crossentropy`` instance. Can be used in ``model.compile(...)`` function\n        or combined with other losses.\n\n    Example:\n\n    .. code:: python\n\n        loss = BinaryCELoss()\n        model.compile('SGD', loss=loss)\n    "

    def __init__(self):
        super().__init__(name="binary_crossentropy")

    def __call__(self, gt, pr):
        return (F.bianary_crossentropy)(gt, pr, **self.submodules)


class CategoricalCELoss(Loss):
    __doc__ = "Creates a criterion that measures the Categorical Cross Entropy between the\n    ground truth (gt) and the prediction (pr).\n\n    .. math:: L(gt, pr) = - gt \\cdot \\log(pr)\n\n    Args:\n        class_weights: Array (``np.array``) of class weights (``len(weights) = num_classes``).\n        class_indexes: Optional integer or list of integers, classes to consider, if ``None`` all classes are used.\n\n    Returns:\n        A callable ``categorical_crossentropy`` instance. Can be used in ``model.compile(...)`` function\n        or combined with other losses.\n\n    Example:\n\n    .. code:: python\n\n        loss = CategoricalCELoss()\n        model.compile('SGD', loss=loss)\n    "

    def __init__(self, class_weights=None, class_indexes=None):
        super().__init__(name="categorical_crossentropy")
        self.class_weights = class_weights if class_weights is not None else 1
        self.class_indexes = class_indexes

    def __call__(self, gt, pr):
        return (F.categorical_crossentropy)(
 gt,
 pr, class_weights=self.class_weights, 
         class_indexes=self.class_indexes, **self.submodules)


class CategoricalFocalLoss(Loss):
    __doc__ = "Creates a criterion that measures the Categorical Focal Loss between the\n    ground truth (gt) and the prediction (pr).\n\n    .. math:: L(gt, pr) = - gt \\cdot \\alpha \\cdot (1 - pr)^\\gamma \\cdot \\log(pr)\n\n    Args:\n        alpha: Float or integer, the same as weighting factor in balanced cross entropy, default 0.25.\n        gamma: Float or integer, focusing parameter for modulating factor (1 - p), default 2.0.\n        class_indexes: Optional integer or list of integers, classes to consider, if ``None`` all classes are used.\n\n    Returns:\n        A callable ``categorical_focal_loss`` instance. Can be used in ``model.compile(...)`` function\n        or combined with other losses.\n\n    Example:\n\n        .. code:: python\n\n            loss = CategoricalFocalLoss()\n            model.compile('SGD', loss=loss)\n    "

    def __init__(self, alpha=0.25, gamma=2.0, class_indexes=None):
        super().__init__(name="focal_loss")
        self.alpha = alpha
        self.gamma = gamma
        self.class_indexes = class_indexes

    def __call__(self, gt, pr):
        return (F.categorical_focal_loss)(
 gt,
 pr,
 self.alpha,
 self.gamma, class_indexes=self.class_indexes, **self.submodules)


class BinaryFocalLoss(Loss):
    __doc__ = "Creates a criterion that measures the Binary Focal Loss between the\n    ground truth (gt) and the prediction (pr).\n\n    .. math:: L(gt, pr) = - gt \\alpha (1 - pr)^\\gamma \\log(pr) - (1 - gt) \\alpha pr^\\gamma \\log(1 - pr)\n\n    Args:\n        alpha: Float or integer, the same as weighting factor in balanced cross entropy, default 0.25.\n        gamma: Float or integer, focusing parameter for modulating factor (1 - p), default 2.0.\n\n    Returns:\n        A callable ``binary_focal_loss`` instance. Can be used in ``model.compile(...)`` function\n        or combined with other losses.\n\n    Example:\n\n    .. code:: python\n\n        loss = BinaryFocalLoss()\n        model.compile('SGD', loss=loss)\n    "

    def __init__(self, alpha=0.25, gamma=2.0):
        super().__init__(name="binary_focal_loss")
        self.alpha = alpha
        self.gamma = gamma

    def __call__(self, gt, pr):
        return (F.binary_focal_loss)(gt, pr, (self.alpha), (self.gamma), **self.submodules)


def focal_loss(alpha=0.25, gamma=2):

    def focal_loss_with_logits(logits, targets, alpha, gamma, y_pred):
        weight_a = alpha * (1 - y_pred) ** gamma * targets
        weight_b = (1 - alpha) * y_pred ** gamma * (1 - targets)
        return (tf.log1p(tf.exp(-tf.abs(logits))) + tf.nn.relu(-logits)) * (weight_a + weight_b) + logits * weight_b

    def loss(y_true, y_pred):
        y_pred = tf.clip_by_value(y_pred, tf.keras.backend.epsilon(), 1 - tf.keras.backend.epsilon())
        logits = tf.log(y_pred / (1 - y_pred))
        loss = focal_loss_with_logits(logits=logits, targets=y_true, alpha=alpha, gamma=gamma, y_pred=y_pred)
        return tf.reduce_mean(loss)

    return loss


jaccard_loss = JaccardLoss()
dice_loss = DiceLoss()
binary_focal_loss = BinaryFocalLoss()
categorical_focal_loss = CategoricalFocalLoss()
binary_crossentropy = BinaryCELoss()
categorical_crossentropy = CategoricalCELoss()
bce_dice_loss = binary_crossentropy + dice_loss
bce_jaccard_loss = binary_crossentropy + jaccard_loss
cce_dice_loss = categorical_crossentropy + dice_loss
cce_jaccard_loss = categorical_crossentropy + jaccard_loss
binary_focal_dice_loss = binary_focal_loss + dice_loss
binary_focal_jaccard_loss = binary_focal_loss + jaccard_loss
categorical_focal_dice_loss = categorical_focal_loss + dice_loss
categorical_focal_jaccard_loss = categorical_focal_loss + jaccard_loss

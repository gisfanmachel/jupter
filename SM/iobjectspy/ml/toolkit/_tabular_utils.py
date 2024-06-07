# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\toolkit\_tabular_utils.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 1748 bytes
"""
@author: YangRuijie
@license: 
@contact: yangruijie@supermap.com
@software: 
@file: tabular_utils.py
@time: 6/22/20 7:37 AM
@desc:
"""
import numpy as np

def f1_score(truth_y, predict_y, average='micro'):
    """
    计算预测结果f1 score
    :param truth_y: 真值
    :param predict_y: 预测值
    :param average: 计算方法，参考sklearn，支持传入 'micro' 或者 'macro'
    :return: f1 值
    """
    max_c = max(np.max(truth_y), np.max(predict_y))
    classes = [i for i in range(max_c)]
    truth_y_onehot = to_onehot_cls(truth_y, classes)
    predict_y_onehot = to_onehot_cls(truth_y, classes)
    if average == "micro":
        truth_pos = np.sum(truth_y_onehot * predict_y_onehot)
        real_pos = np.sum(truth_y_onehot)
        predict_pos = np.sum(predict_y_onehot)
        pre = truth_pos / predict_pos
        recall = truth_pos / real_pos
        f1 = 2 * pre * recall / (pre + recall)
    else:
        if average == "macro":
            truth_pos = np.sum((truth_y_onehot * predict_y_onehot), axis=(-1))
            real_pos = np.sum(truth_y_onehot, axis=(-1))
            predict_pos = np.sum(predict_y_onehot, axis=(-1))
            pre = truth_pos / predict_pos
            recall = truth_pos / real_pos
            f1 = np.mean(2 * pre * recall / (pre + recall))
        else:
            raise NotImplementedError
    return f1


def to_onehot_cls(y, classes):
    """
    :param y: 标签
    :param classes: 类别列表
    :return: one_hot标签
    """
    y_shape = list(y.shape)
    y_shape.append(len(classes))
    y_shape = tuple(y_shape)
    y_out = np.zeros(y_shape, dtype=(np.uint16))
    for i in range(len(classes)):
        y_out[(..., i)][y == classes[i]] = 1

    return np.squeeze(y_out)

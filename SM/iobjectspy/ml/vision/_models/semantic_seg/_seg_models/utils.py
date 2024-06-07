# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_seg_models\utils.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 2175 bytes
""" Utility functions for segmentation models """
from functools import wraps
import numpy as np

def get_layer_number(model, layer_name):
    """
    Help find layer in Keras model by name
    Args:
        model: Keras `Model`
        layer_name: str, name of layer

    Returns:
        index of layer

    Raises:
        ValueError: if model does not contains layer with such name
    """
    for i, l in enumerate(model.layers):
        if l.name == layer_name:
            return i

    raise ValueError("No layer with name {} in  model {}.".format(layer_name, model.name))


def extract_outputs(model, layers, include_top=False):
    """
    Help extract intermediate layer outputs from model
    Args:
        model: Keras `Model`
        layer: list of integers/str, list of layers indexes or names to extract output
        include_top: bool, include final model layer output

    Returns:
        list of tensors (outputs)
    """
    layers_indexes = [get_layer_number(model, l) if isinstance(l, str) else l for l in layers]
    outputs = [model.layers[i].output for i in layers_indexes]
    if include_top:
        outputs.insert(0, model.output)
    return outputs


def reverse(l):
    """Reverse list"""
    return list(reversed(l))


def add_docstring(doc_string=None):

    def decorator(fn):
        if fn.__doc__:
            fn.__doc__ += doc_string
        else:
            fn.__doc__ = doc_string

        @wraps(fn)
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)

        return wrapper

    return decorator


def recompile(model):
    model.compile(model.optimizer, model.loss, model.metrics)


def freeze_model(model):
    for layer in model.layers:
        layer.trainable = False


def set_trainable(model):
    for layer in model.layers:
        layer.trainable = True

    recompile(model)


def to_tuple(x):
    if isinstance(x, tuple):
        if len(x) == 2:
            return x
    elif np.isscalar(x):
        return (
         x, x)
    raise ValueError('Value should be tuple of length 2 or int value, got "{}"'.format(x))

# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_seg_models\encs\cls_models\cls_models\utils.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 6082 bytes
import os, shutil, warnings
from keras.utils import get_file
from _jsuperpy._logger import log_info, log_warning

def find_weights(weights_collection, model_name, dataset, include_top):
    w = list(filter((lambda x: x["model"] == model_name), weights_collection))
    w = list(filter((lambda x: x["dataset"] == dataset), w))
    w = list(filter((lambda x: x["include_top"] == include_top), w))
    return w


def load_model_weights(weights_collection, model, dataset, classes, include_top):
    weights = find_weights(weights_collection, model.name, dataset, include_top)
    if weights:
        weights = weights[0]
        if include_top:
            if weights["classes"] != classes:
                raise ValueError("If using `weights` and `include_top` as true, `classes` should be {}".format(weights["classes"]))
        datadir_base = os.path.expanduser(os.path.join(os.path.expanduser("~"), ".keras"))
        if not os.access(datadir_base, os.W_OK):
            datadir_base = os.path.join("/tmp", ".keras")
        else:
            model_dir = os.path.join(datadir_base, "models")
            if not os.path.exists(model_dir):
                os.makedirs(model_dir)
            else:
                keras_cache_file = os.path.join(model_dir, weights["name"])
                _, cache_file = get_weights_default_path(weights_collection, model.name, dataset, include_top)
                weights_path = None
                if os.path.exists(keras_cache_file):
                    weights_path = keras_cache_file
                    if not os.path.exists(cache_file):
                        shutil.copyfile(keras_cache_file, cache_file)
                else:
                    if os.path.exists(cache_file):
                        weights_path = cache_file
                        shutil.copyfile(cache_file, keras_cache_file)
                    else:
                        warnings.warn("预训练模型不存在,请检查预训练模型")
                        log_warning("预训练模型不存在,将只使用自有训练数据,请检查预训练模型,复制到 {} 或 {} 目录下".format(os.path.abspath(model_dir), os.path.abspath(cache_file)))
        if weights_path:
            log_info("load backbone weight from: {}".format(weights_path))
            model.load_weights(weights_path, by_name=True, skip_mismatch=True)
    else:
        raise ValueError("There is no weights for such configuration: " + "model = {}, dataset = {}, ".format(model.name, dataset) + "classes = {}, include_top = {}.".format(classes, include_top))


def load_efficient_model_weights(weights, model, load_from_internet=False):
    if weights:
        datadir_base = os.path.expanduser(os.path.join(os.path.expanduser("~"), ".keras"))
        if not os.access(datadir_base, os.W_OK):
            datadir_base = os.path.join("/tmp", ".keras")
        else:
            model_dir = os.path.join(datadir_base, "models")
            if not os.path.exists(model_dir):
                os.makedirs(model_dir)
            else:
                keras_cache_file = os.path.join(model_dir, weights["name"])
                cache_file = os.path.abspath(os.path.join("..", "..", "resources_ml", "backbone", weights["name"]))
                weights_path = None
                if os.path.exists(keras_cache_file):
                    weights_path = keras_cache_file
                    if not os.path.exists(cache_file):
                        shutil.copyfile(keras_cache_file, cache_file)
                else:
                    if os.path.exists(cache_file):
                        weights_path = cache_file
                        shutil.copyfile(cache_file, keras_cache_file)
                    else:
                        if load_from_internet:
                            weights_path = get_file((weights["name"]),
                              (weights["url"]),
                              cache_subdir="models",
                              md5_hash=(weights["md5"]))
                        else:
                            warnings.warn("预训练模型不存在,请检查预训练模型")
                            log_warning("预训练模型不存在,将只使用自有训练数据,请检查预训练模型,复制到 {} 或 {} 目录下".format(os.path.abspath(model_dir), os.path.abspath(cache_file)))
        if weights_path:
            log_info("load backbone weight from: {}".format(weights_path))
            model.load_weights(weights_path, by_name=True, skip_mismatch=True)
    else:
        raise ValueError("There is no weights for such configuration: " + "model = {}, dataset = {}, ".format(model.name))


def get_weights_default_path(weights_collection, model_name, dataset, include_top):
    """

    :param weights_collection:
    :param model_name:
    :param dataset:
    :param include_top:
    :return:
    """
    if model_name.find("efficientnet") != -1:
        return (None, None)
    weights = find_weights(weights_collection, model_name, dataset, include_top)
    if weights:
        weights = weights[0]
        datadir_base = os.path.expanduser(os.path.join(os.path.expanduser("~"), ".keras"))
        if not os.access(datadir_base, os.W_OK):
            datadir_base = os.path.join("/tmp", ".keras")
        model_dir = os.path.join(datadir_base, "models")
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
        keras_cache_file = os.path.join(model_dir, weights["name"])
        cache_file = os.path.join("..", "..", "resources_ml", "backbone", weights["name"])
        return (keras_cache_file, cache_file)
    raise ValueError("There is no weights for such configuration: " + "model = {}, dataset = {}, ".format(model_name, dataset) + " include_top = {}.".format(include_top))

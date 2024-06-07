# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_torch_models\encoders\__init__.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 3076 bytes
import functools, os, torch
from urllib.parse import urlparse
import torch.utils.model_zoo as model_zoo
from torch.hub import _get_torch_home
from .resnet import resnet_encoders
from .dpn import dpn_encoders
from .vgg import vgg_encoders
from .senet import senet_encoders
from .densenet import densenet_encoders
from .inceptionresnetv2 import inceptionresnetv2_encoders
from .inceptionv4 import inceptionv4_encoders
from .efficientnet import efficient_net_encoders
from .mobilenet import mobilenet_encoders
from .xception import xception_encoders
from ._preprocessing import preprocess_input
encoders = {}
encoders.update(resnet_encoders)
encoders.update(dpn_encoders)
encoders.update(vgg_encoders)
encoders.update(senet_encoders)
encoders.update(densenet_encoders)
encoders.update(inceptionresnetv2_encoders)
encoders.update(inceptionv4_encoders)
encoders.update(efficient_net_encoders)
encoders.update(mobilenet_encoders)
encoders.update(xception_encoders)

def get_encoder(name, in_channels=3, depth=5, weights=None):
    Encoder = encoders[name]["encoder"]
    params = encoders[name]["params"]
    params.update(depth=depth)
    encoder = Encoder(**params)
    if weights is not None:
        settings = encoders[name]["pretrained_settings"][weights]
        encoder.load_state_dict(load_weighs_url(settings["url"]))
    encoder.set_in_channels(in_channels)
    return encoder


def load_weighs_url(url):
    parts = urlparse(url)
    filename = os.path.basename(parts.path)
    torch_home = _get_torch_home()
    model_dir = os.path.join(torch_home, "checkpoints")
    torch_cached_file = os.path.join(model_dir, filename)
    cached_dir = os.path.abspath(os.path.join("..", "..", "resources_ml", "backbone"))
    cached_file = os.path.join(cached_dir, filename)
    if os.path.exists(cached_file):
        print("backbone 预训练权重从{} 加载".format(cached_file))
        return torch.load(cached_file)
    print("backbone 预训练权重如果下载失败，请从下面网址手动下载，并保存到 “{}” 或 “{}”目录，下载网址为： {}".format(cached_dir, model_dir, url))
    return model_zoo.load_url(url)


def get_encoder_names():
    return list(encoders.keys())


def get_preprocessing_params(encoder_name, pretrained='imagenet'):
    settings = encoders[encoder_name]["pretrained_settings"]
    if pretrained not in settings.keys():
        raise ValueError("Avaliable pretrained options {}".format(settings.keys()))
    formatted_settings = {}
    formatted_settings["input_space"] = settings[pretrained].get("input_space")
    formatted_settings["input_range"] = settings[pretrained].get("input_range")
    formatted_settings["mean"] = settings[pretrained].get("mean")
    formatted_settings["std"] = settings[pretrained].get("std")
    return formatted_settings


def get_preprocessing_fn(encoder_name, pretrained='imagenet'):
    params = get_preprocessing_params(encoder_name, pretrained=(pretrained if pretrained else "imagenet"))
    return (functools.partial)(preprocess_input, **params)

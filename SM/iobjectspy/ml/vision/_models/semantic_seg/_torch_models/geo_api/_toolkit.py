# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_torch_models\geo_api\_toolkit.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 5491 bytes
"""
@author: YangRuijie
@license: 
@contact: yangruijie@supermap.com
@software: 
@file: _toolkit.py
@time: 12/24/19 12:32 AM
@desc:
"""
import glob, os, numpy as np, yaml
from dotmap import DotMap
import albumentations as albu
from matplotlib import pyplot as plt

def list_file(folder, pattern='*', ext='tif'):
    """
    列出指定文件夹下的文件目录
    :param folder: 指定的文件夹
    :param pattern: 文件名过滤
    :param ext: 后缀名过滤
    :return: 符合要求的文件路径list
    """
    folder_dirs = [x[0] for x in os.walk(folder)]
    filenames = []
    new_filenames = []
    for folderdir in folder_dirs:
        filenames.extend(sorted(glob.glob(folderdir + "/" + pattern + "." + ext)))

    for filename in filenames:
        new_filenames.append(filename.replace("\\", "/"))

    return new_filenames


def list_xy_file_fromtxt(txt_path):
    """
    通过txt文件列出image，mask所有文件完整路径
    :param txt_path: 文件名字txt路径
    :return:
    """
    x_filenames = []
    y_filenames = []
    with open(txt_path, "r") as f:
        for line in f:
            files = line.strip().split(",")
            x_filenames.append(files[0])
            y_filenames.append(files[1])

    return (
     x_filenames, y_filenames)


def to_onehot(y, classes):
    """
    最多支持256类
    :param y:
    :param classes: 最多支持256类
    :return:
    """
    y_shape = list(y.shape)
    y_shape.append(len(classes))
    y_shape = tuple(y_shape)
    y_out = np.zeros(y_shape, dtype=(np.uint8))
    for i in range(len(classes)):
        y_out[(..., i)][y == classes[i]] = 1

    return y_out


def get_config_from_yaml(yaml_file, encoding='utf8'):
    """
    Get the config from a yml or yaml file
    :param yaml_file: 文件路径
    :param encoding: encoding default: utf8
    :return: config(namespace) or config(dictionary)
    """
    with open(yaml_file, encoding=encoding) as f:
        config_dict = yaml.load(f, Loader=(yaml.FullLoader))
    config = DotMap(config_dict)
    return config


def get_training_augmentation(size):
    train_transform = [
     albu.Compose([
      albu.VerticalFlip(p=0.5),
      albu.RandomRotate90(p=0.5),
      albu.Transpose(p=0.2),
      albu.Downscale(scale_min=0.2, scale_max=0.8, p=0.2),
      albu.OneOf([albu.RandomCrop(height=(size // 2), width=(size // 2), p=1),
       albu.CropNonEmptyMaskIfExists(height=(size // 2), width=(size // 2), p=1)],
        p=0.5),
      albu.OneOf([
       albu.MedianBlur(blur_limit=3, p=1),
       albu.Blur(blur_limit=3, p=1),
       albu.MotionBlur(blur_limit=3, p=1)],
        p=0.2),
      albu.ShiftScaleRotate(scale_limit=0.5, rotate_limit=0, shift_limit=0.1, p=0.2, border_mode=0),
      albu.IAAPerspective(p=0.5),
      albu.IAAAdditiveGaussianNoise(p=0.2),
      albu.RandomScale(scale_limit=[0.25, 2], p=0.5),
      albu.GridDistortion(p=0.2),
      albu.Solarize(p=0.2),
      albu.RandomBrightnessContrast(p=0.2)],
       p=0.4),
     albu.Resize(size, size)]
    return albu.Compose(train_transform)


def get_validation_augmentation(size):
    """Add paddings to make image shape divisible by 32"""
    test_transform = [
     albu.Resize(size, size)]
    return albu.Compose(test_transform)


def to_tensor(x, **kwargs):
    return x.transpose(2, 0, 1).astype("float32")


def get_preprocessing(preprocessing_fn):
    """Construct preprocessing transform

    Args:
        preprocessing_fn (callbale): data normalization function
            (can be specific for each pretrained neural network)
    Return:
        transform: albumentations.Compose

    """
    _transform = [
     albu.Lambda(image=preprocessing_fn),
     albu.Lambda(image=to_tensor, mask=to_tensor)]
    return albu.Compose(_transform)


def vis_image_mask(title, *args):
    l = len(args)
    plt.figure(figsize=(20, 20))
    plt.suptitle(title)
    for i in range(l):
        cur_plt = (
         1, l, i + 1)
        (plt.subplot)(*cur_plt)
        plt.imshow(list(args[i].values())[0])
        plt.title(list(args[i].keys())[0])

    plt.show()


def preprocess_input(x, mean=None, std=None, input_space='RGB', input_range=None, input_min=None, input_max=None, **kwargs):
    if input_space == "BGR":
        x = x[(..., None[None:-1])].copy()
    elif input_range is not None:
        if x.max() > 1:
            if input_range[1] == 1:
                x = x / 255.0
    elif input_range is None:
        if input_min is not None and input_max is not None:
            input_min = np.array(input_min)
            input_max = np.array(input_max)
            x = (x - input_min) / (input_max - input_min)
            if mean is not None:
                mean = np.array(mean)
                mean = (mean - input_min) / (input_max - input_min)
            if std is not None:
                std = np.array(std)
                std = std / (input_max - input_min)
    if mean is not None:
        mean = np.array(mean)
        x = x - mean
    if std is not None:
        std = np.array(std)
        x = x / std
    return x

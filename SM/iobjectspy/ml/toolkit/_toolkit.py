# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\toolkit\_toolkit.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 36110 bytes
"""
@author: 杨瑞杰
@license: (C) Copyright 2013-2018, Supermap Corporation Limited.
@contact: yangruijie@supermap.com
@software: 
@file: _toolkit.py
@time: 18-9-20 上午8:41
@desc:
"""
import glob, json, os, random, shutil, sys
from collections import OrderedDict
import numpy as np, rasterio, yaml
from PIL import Image
from albumentations import Compose, VerticalFlip, RandomRotate90, OneOf, ElasticTransform, GridDistortion, CLAHE, OpticalDistortion, RandomBrightnessContrast, RandomGamma, RandomCrop, Resize, HueSaturationValue, IAAAdditiveGaussianNoise, IAAPerspective, IAASharpen, Blur, MotionBlur, ImageCompression, JpegCompression
from dotmap import DotMap
from ..._logger import log_info
from ... import Dataset, Workspace, EngineType, Datasource, DatasourceConnectionInfo, DatasourceOpenedFailedError

def find_element_in_list(element, list_element):
    """列表判断定位元素

    :param element: 需要定位的元素
    :param list_element: 被查找的列表
    :return: 是否能找到元素
    """
    try:
        list_element.index(element)
        return True
    except ValueError:
        return False


def getStr_InList_ByKey(key, list_i, list_v=None):
    """ 列表搜索字符串元素
    函数分为两种使用模式
        - list_v 为None时，直接根据key去查找list_i
        - list_v不为None时，根据key去查找list_v元素位置的值，作为搜索键值，查找list_i

    :param key: 待搜索的字符串键值
    :param list_i: 待搜索的列表
    :param list_v: 用于匹配搜索的列表，默认为None
    :return: 返回list_i中的字符元素
    """
    try:
        idx = list_i.index(key)
        if list_v is None:
            list_v = list_i
        return list_v[idx]
    except ValueError:
        return ""


def check_module(modulename=None):
    """检测模块是否存在

    :param modulename: 模块名称
    :return: 是否存在
    """
    if modulename is None:
        return True
    import importlib
    lib_spec = importlib.util.find_spec(modulename)
    found = lib_spec is not None
    return found


def checkpath(strpath, type=None):
    """ 检测路径文件是否有效

    :param strpath: 被检测的文件路径
    :param type: 是否指定文件后缀名
    :return: 文件是否存在; 当文件路径存在时，且type不为None，返回是否是指定文件类型
    """
    if not isinstance(strpath, str):
        return False
    from pathlib import Path
    my_file = Path(strpath)
    if my_file.is_file():
        if type is None:
            return True
        if type is not None:
            if strpath.endswith(type):
                return True
    return False


def merge_number(rawss):
    """
    合并数字,CRFPP中需要将前后相邻的数字字符元素合并成一个元素
    比如路号，楼栋编号等等

    :param rawss: 原始待合并的字符串列表
    :return: 合并数字后的字符串列表
    """
    ss = list(rawss)
    isdigit = [y.isdigit() for y in [i for i in ss]]
    sy = [y for y in [i for i in ss]]
    i = 0
    while i < len(isdigit):
        if isdigit[i]:
            for j in range(i, len(isdigit)):
                if isdigit[j] is not True:
                    break

            if j == len(isdigit) - 1:
                if isdigit[j]:
                    j = j + 1
            sy[i] = "".join(ss[i[:j]])
            for ii in range(i + 1, j):
                sy[ii] = ""

            i = j
        i += 1

    return list(filter(None, sy))


def stretch_n(bands, lower_percent=2, higher_percent=98):
    """
    将影像数据标准化到0到1之间

    :param bands:  输入影像
    :param lower_percent:   最小值比率
    :param higher_percent:  最大值比率
    :return:  标准化后的影像
    """
    out = np.zeros_like(bands, dtype=(np.float))
    n = bands.shape[2]
    for i in range(n):
        a = 0
        b = 1
        c = np.percentile(bands[(None[:None], None[:None], i)], lower_percent)
        d = np.percentile(bands[(None[:None], None[:None], i)], higher_percent)
        t = a + (bands[(None[:None], None[:None], i)] - c) * (b - a) / (d - c)
        t[t < a] = a
        t[t > b] = b
        out[(None[:None], None[:None], i)] = t

    return out


def stretch_min_max(bands, min, max):
    """
        将影像数据各个波段分别标准化到0到1之间

        :param bands:  输入影像
        :param min:   最小值数组
        :param max:  最大值数组
        :return:  标准化后的影像
        """
    out = np.zeros_like(bands, dtype=(np.float))
    n = bands.shape[2]
    for i in range(n):
        a = 0
        b = 1
        c = min[i]
        d = max[i]
        t = a + (bands[(None[:None], None[:None], i)] - c) * (b - a) / (d - c)
        t[t < a] = a
        t[t > b] = b
        out[(None[:None], None[:None], i)] = t

    return out


def stretch_minmax(bands, max_value=256, min_value=0):
    """
    将影像数据标准化到0到1之间
    :param bands: 输入影像
    :param max_value: 最小值
    :param min_value: 最大值
    :return: 标准化后的影像
    """
    out = np.zeros_like(bands, dtype=(np.float))
    n = bands.shape[2]
    for i in range(n):
        a = 0
        b = 1
        c = min_value
        d = max_value
        t = a + (bands[(None[:None], None[:None], i)] - c) * (b - a) / (d - c)
        t[t < a] = a
        t[t > b] = b
        out[(None[:None], None[:None], i)] = t

    return out


def get_percentclip_min_max(image_path, lower_percent=2, higher_percent=98):
    import gdal
    src_ds = gdal.Open(image_path)
    band_xsize, band_ysize, band_count = src_ds.RasterXSize, src_ds.RasterYSize, src_ds.RasterCount
    band_percent_min, band_percent_max = [], []
    for i in range(band_count):
        band = src_ds.GetRasterBand(i + 1)
        band_min, band_max = band.ComputeRasterMinMax()
        hist = band.GetHistogram(min=(-0.5 + band_min), max=(band_max + 0.5), buckets=(int(band_max - band_min + 1)))
        band_pixel_count = sum(hist)
        band_pixel_min_count, band_pixel_max_count = band_pixel_count * lower_percent / 100, band_pixel_count * (100 - higher_percent) / 100
        count_pixel = 0
        for min_i in range(len(hist)):
            count_pixel += hist[min_i]
            if count_pixel > band_pixel_min_count:
                band_percent_min.append(band_min + min_i)
                break

        count_pixel = 0
        for max_i in range(len(hist) - 1, -1, -1):
            count_pixel += hist[max_i]
            if count_pixel > band_pixel_max_count:
                band_percent_max.append(band_max + max_i - len(hist))
                break

    return (
     band_percent_min, band_percent_max)


def read_short_json_file(file_path, encoding='utf8'):
    """
    读取小的json文件，转换为dict

    :param file_path:  文件路径
    :param encoding:  文件编码
    :return:  json字符对应的dict对象
    """
    with open(file_path, "r", encoding=encoding) as json_f:
        json_str = ""
        for line in json_f:
            json_str += line

    return json.loads(json_str)


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


def get_image_from_csv(csv_path, is_aug=False, input_bands=3, output_bands=1, image_size=None, generate=False, batch_size=None):
    """
    从csv文件中的路径读取训练数据
    :param csv_path: csv未见路径
    :return: 读取的数据 （X,Y）
    """
    import rasterio
    from rasterio._base import NotGeoreferencedWarning
    from warnings import filterwarnings
    filterwarnings("ignore", category=NotGeoreferencedWarning)
    log_info("ignore  NotGeoreferencedWarning")
    x_files, y_files = list_xy_file_fromtxt(csv_path)
    if len(x_files) < 1:
        raise Exception("Data load error,Image file is not enough")
    if len(y_files) < 1:
        raise Exception("Data load error,Mask file is not enough")

    def read_xy(x_file, y_file):
        x_image, y = rasterio.open(x_file).read()[(None[:input_bands], ...)], np.array(Image.open(y_file)) if y_file.strip().endswith("png") else rasterio.open(y_file).read(1)
        x_image = np.transpose(x_image, (1, 2, 0))
        if is_aug:
            aug_list = [
             VerticalFlip(p=0.5),
             RandomRotate90(p=0.5),
             OneOf([
              ElasticTransform(p=0.5, alpha=120, sigma=6.0, alpha_affine=3.5999999999999996),
              GridDistortion(p=0.5),
              OpticalDistortion(p=1, distort_limit=2, shift_limit=0.5)],
               p=0.1),
             ImageCompression(quality_lower=50, quality_upper=90, p=0.5),
             IAAAdditiveGaussianNoise(p=0.2),
             IAAPerspective(p=0.5),
             OneOf([
              CLAHE(p=1),
              RandomBrightnessContrast(p=1),
              RandomGamma(p=1)],
               p=0.9),
             OneOf([
              IAASharpen(p=1),
              Blur(blur_limit=3, p=1),
              MotionBlur(blur_limit=3, p=1)],
               p=0.9),
             OneOf([
              RandomBrightnessContrast(p=1),
              HueSaturationValue(p=1)],
               p=0.9)]
            if image_size is not None:
                if image_size < x_image.shape[1]:
                    aug_list.append(Resize(image_size, image_size))
                else:
                    aug_list.append(RandomCrop(image_size, image_size, p=1))
            aug = Compose(aug_list)
            augmented = aug(image=x_image, mask=y)
            x_image = augmented["image"]
            y = augmented["mask"]
        else:
            if image_size is not None:
                aug = Compose([
                 RandomCrop(image_size, image_size, p=1)])
                augmented = aug(image=x_image, mask=y)
                x_image = augmented["image"]
                y = augmented["mask"]
            if output_bands > 1:
                y = to_onehot(y, [num for num in range(output_bands)])
            return (
             x_image, y)

    if generate:

        def gen_f():
            X = []
            Y = []
            count = 0
            while 1:
                for x_file, y_file in zip(x_files, y_files):
                    x_image, y = read_xy(x_file, y_file)
                    X.append(x_image)
                    if len(y.shape) < 3:
                        Y.append(y[(None[:None], None[:None], np.newaxis)])
                    else:
                        Y.append(y)
                    count += 1
                    if count >= batch_size:
                        yield (
                         np.array(X), np.array(Y))
                        X = []
                        Y = []
                        count = 0

        return gen_f
    X = []
    Y = []
    for x_file, y_file in zip(x_files, y_files):
        x_image, y = read_xy(x_file, y_file)
        X.append(x_image)
        if len(y.shape) < 3:
            Y.append(y[(None[:None], None[:None], np.newaxis)])
        else:
            Y.append(y)

    return (
     np.array(X), np.array(Y))


def get_changedet_image_from_csv(csv_path, is_aug=False, band_num=1, image_size=None):
    """
    从csv文件中的路径读取训练数据
    :param csv_path: csv未见路径
    :return: 读取的数据 （X,Y）
    """
    import rasterio
    pre_x_files, next_x_files, y_files = [], [], []
    with open(csv_path, "r", encoding="utf8") as f:
        for line in f:
            pre_x_file, next_x_file, y_file = line.strip().split(",")
            pre_x_files.append(pre_x_file)
            next_x_files.append(next_x_file)
            y_files.append(y_file)

    PX = []
    NX = []
    Y = []
    for x_file, next_x_file, y_file in zip(pre_x_files, next_x_files, y_files):
        x_image, latest_x_image, y = rasterio.open(x_file).read()[(None[:3], ...)], rasterio.open(next_x_file).read()[(None[:3],
         ...)], np.array(Image.open(y_file)) if os.path.splitext(y_file)[-1] is "png" else rasterio.open(y_file).read(1)
        x_image = np.transpose(x_image, (1, 2, 0))
        latest_x_image = np.transpose(latest_x_image, (1, 2, 0))
        if band_num > 1:
            y = to_onehot(y, [num for num in range(band_num)])
        PX.append(x_image)
        NX.append(latest_x_image)
        if len(y.shape) < 3:
            Y.append(y[(None[:None], None[:None], np.newaxis)])
        else:
            Y.append(y)

    return (
     np.array(PX), np.array(NX), np.array(Y))


def get_scene_image_from_csv(csv_path, label_dict, input_bands=3, is_aug=False, image_size=None, generate=False, batch_size=None):
    """
    从csv文件中的路径读取训练数据
    :param csv_path: csv未见路径
    :return: 读取的数据 （X,Y）
    """
    import rasterio

    def read_xy(x_file, label_id):
        x_image = rasterio.open(x_file).read()[(None[:input_bands], ...)]
        x_image = np.transpose(x_image, (1, 2, 0))
        if is_aug:
            aug_list = [
             VerticalFlip(p=0.5),
             RandomRotate90(p=0.5),
             OneOf([
              ElasticTransform(p=0.5, alpha=120, sigma=6.0, alpha_affine=3.5999999999999996),
              GridDistortion(p=0.5),
              OpticalDistortion(p=1, distort_limit=2, shift_limit=0.5)],
               p=0.1),
             JpegCompression(quality_lower=50, quality_upper=80, p=0.5),
             CLAHE(p=0.8),
             RandomBrightnessContrast(p=0.8),
             RandomGamma(p=0.8)]
            if image_size is not None:
                if image_size < x_image.shape[1]:
                    aug_list.append(RandomCrop(image_size, image_size, p=1))
                else:
                    aug_list.append(Resize(image_size, image_size, p=1))
            aug = Compose(aug_list)
            augmented = aug(image=x_image)
            x_image = augmented["image"]
        else:
            if image_size is not None:
                if image_size < x_image.shape[1]:
                    aug = Compose([
                     RandomCrop(image_size, image_size, p=1)])
                else:
                    aug = Compose([
                     Resize(image_size, image_size, p=1)])
                augmented = aug(image=x_image)
                x_image = augmented["image"]
            y = np.array([int(label_id)])
            y = to_onehot_image_cls(y, [num for num in range(len(label_dict))])
            return (x_image, y)

    x_files, label_ids = [], []
    with open(csv_path, "r", encoding="utf8") as f:
        for line in f:
            x_file, label_name, label_value = line.strip().split(",")
            label_id = label_dict[label_name.strip()]
            assert label_id == int(label_value), "标签数据有错误，label data has error "
            x_files.append(x_file)
            label_ids.append(label_id)

    if generate:

        def gen_f():
            X = []
            Y = []
            count = 0
            while 1:
                for x_file, label_id in zip(x_files, label_ids):
                    x_image, y = read_xy(x_file, label_id)
                    X.append(x_image)
                    Y.append(y)
                    count += 1
                    if count >= batch_size:
                        yield (
                         np.array(X), np.array(Y))
                        X = []
                        Y = []
                        count = 0

        return gen_f
    X = []
    Y = []
    for x_file, label_id in zip(x_files, label_ids):
        x_image, y = read_xy(x_file, label_id)
        X.append(x_image)
        Y.append(y)

    return (np.array(X), np.array(Y))


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


def to_onehot_image_cls(y, classes):
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

    return np.squeeze(y_out)


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


def split_train_val_withdirs(image_dirs, mask_dirs, train_txt_path, val_scale=0.3, x_ext='tif', y_ext='tif'):
    """
    多份分割数据放在一起划分训练集和验证集,shuffle
    :param image_dirs: 多个影像目录
    :type image_dirs: list
    :param mask_dirs:  多个mask目录，与影像目录顺序对应
    :type mask_dirs: list
    :param train_txt_path: 训练文件记录的txt文件路径
    :type train_txt_path: str
    :param val_scale: 验证集比例
    :type val_scale: float
    :param x_ext: 影像后缀名
    :type x_ext: str
    :param y_ext: mask后缀名
    :type y_ext: str
    :return: train_num,val_num,train_val_num
    """
    if os.path.exists(train_txt_path) is not True:
        os.makedirs(train_txt_path)
    train_file = open((os.path.join(train_txt_path, "train.csv")), "w", encoding="utf8")
    trainval_file = open((os.path.join(train_txt_path, "trainval.csv")), "w", encoding="utf8")
    val_file = open((os.path.join(train_txt_path, "val.csv")), "w", encoding="utf8")
    image_files = []
    mask_files = []
    for image_dir, mask_dir in zip(image_dirs, mask_dirs):
        files = list_file(image_dir, "*", x_ext)
        for file in files:
            filename = os.path.splitext(os.path.basename(file))[0]
            mask_file = os.path.join(mask_dir, filename + "." + y_ext)
            if os.path.exists(mask_file):
                mask_files.append(mask_file)
                image_files.append(file)

    merge_files = list(zip(image_files, mask_files))
    random.shuffle(merge_files)
    train_val_num = len(merge_files)
    val_num = int(train_val_num * val_scale)
    train_num = train_val_num - val_num
    i = 0
    for image_file, mask_file in merge_files:
        if i < train_num:
            train_file.write(image_file + "," + mask_file + "\n")
            trainval_file.write(image_file + "," + mask_file + "\n")
        else:
            if i < train_val_num:
                val_file.write(image_file + "," + mask_file + "\n")
                trainval_file.write(image_file + "," + mask_file + "\n")
            i += 1

    return (
     train_num, val_num, train_val_num)


def split_train_val_change_det(pre_image_dirs, next_image_dirs, mask_dirs, train_txt_path, val_scale=0.3, x_ext='tif', y_ext='tif'):
    """
    多份分割数据放在一起划分训练集和验证集
    :param pre_image_dirs: 前一时相影像目录
    :type pre_image_dirs: list
    :param next_image_dirs: 后一时相影像目录
    :type next_image_dirs: list
    :param mask_dirs:  多个mask目录，与影像目录顺序对应
    :type mask_dirs: list
    :param train_txt_path: 训练文件记录的txt文件路径
    :type train_txt_path: str
    :param val_scale: 验证集比例
    :type val_scale: float
    :param x_ext: 影像后缀名
    :type x_ext: str
    :param y_ext: mask后缀名
    :type y_ext: str
    :return: None
    """
    if os.path.exists(train_txt_path) is not True:
        os.makedirs(train_txt_path)
    train_file = open((os.path.join(train_txt_path, "train.csv")), "w", encoding="utf8")
    trainval_file = open((os.path.join(train_txt_path, "trainval.csv")), "w", encoding="utf8")
    val_file = open((os.path.join(train_txt_path, "val.csv")), "w", encoding="utf8")
    pre_image_files = []
    next_image_files = []
    mask_files = []
    for image_dir, latest_image_dir, mask_dir in zip(pre_image_dirs, next_image_dirs, mask_dirs):
        files = list_file(image_dir, "*", x_ext)
        for file in files:
            filename = os.path.splitext(os.path.basename(file))[0]
            mask_file = os.path.join(mask_dir, filename + "." + y_ext)
            latest_image_file = os.path.join(latest_image_dir, filename + "." + x_ext)
            if os.path.exists(mask_file) and os.path.exists(latest_image_file):
                mask_files.append(mask_file)
                pre_image_files.append(file)
                next_image_files.append(latest_image_file)

    merge_files = list(zip(pre_image_files, next_image_files, mask_files))
    random.shuffle(merge_files)
    train_val_num = len(merge_files)
    val_num = int(train_val_num * val_scale)
    train_num = train_val_num - val_num
    i = 0
    for image_file, latest_image_file, mask_file in merge_files:
        if i < train_num:
            train_file.write(image_file + "," + latest_image_file + "," + mask_file + "\n")
            trainval_file.write(image_file + "," + latest_image_file + "," + mask_file + "\n")
        else:
            if i < train_val_num:
                val_file.write(image_file + "," + latest_image_file + "," + mask_file + "\n")
                trainval_file.write(image_file + "," + latest_image_file + "," + mask_file + "\n")
            i += 1


def split_train_val_scene_classification(image_dirs, train_txt_path, val_scale=0.3):
    """
    场景分类数据集划分验证测试集
    :param image_dirs:
    :param train_txt_path:
    :param val_scale:
    :return:
    """
    if os.path.exists(train_txt_path) is not True:
        os.makedirs(train_txt_path)
    train_file = open((os.path.join(train_txt_path, "train.csv")), "w", encoding="utf8")
    trainval_file = open((os.path.join(train_txt_path, "trainval.csv")), "w", encoding="utf8")
    val_file = open((os.path.join(train_txt_path, "val.csv")), "w", encoding="utf8")
    all_files = []
    for image_dir in image_dirs:
        with open((os.path.join(image_dir, "scene_classification.csv")), "r", encoding="utf8") as f:
            for line in f:
                line = line.strip().split(",")
                line[0] = os.path.join(image_dir, line[0])
                all_files.append(line)

    random.shuffle(all_files)
    train_val_num = len(all_files)
    val_num = int(train_val_num * val_scale)
    train_num = train_val_num - val_num
    i = 0
    for file in all_files:
        if i < train_num:
            train_file.write(",".join(file) + "\n")
            trainval_file.write(",".join(file) + "\n")
        else:
            if i < train_val_num:
                val_file.write(",".join(file) + "\n")
                trainval_file.write(",".join(file) + "\n")
            i += 1

    train_file.close()
    val_file.close()
    trainval_file.close()
    return (train_num, val_num, train_val_num)


def split_train_val_image_classification(image_dirs, train_txt_path, val_scale=0.3):
    """
    场景分类数据集划分验证测试集
    :param image_dirs:
    :param train_txt_path:
    :param val_scale:
    :return:
    """
    if os.path.exists(train_txt_path) is not True:
        os.makedirs(train_txt_path)
    train_file = open((os.path.join(train_txt_path, "train.csv")), "w", encoding="utf8")
    trainval_file = open((os.path.join(train_txt_path, "trainval.csv")), "w", encoding="utf8")
    val_file = open((os.path.join(train_txt_path, "val.csv")), "w", encoding="utf8")
    all_files = []
    for image_dir in image_dirs:
        with open((os.path.join(image_dir, "image_classification.csv")), "r", encoding="utf8") as f:
            for line in f:
                line = line.strip().split(",")
                line[0] = os.path.join(image_dir, line[0])
                all_files.append(line)

    random.shuffle(all_files)
    train_val_num = len(all_files)
    val_num = int(train_val_num * val_scale)
    train_num = train_val_num - val_num
    i = 0
    for file in all_files:
        if i < train_num:
            train_file.write(",".join(file) + "\n")
            trainval_file.write(",".join(file) + "\n")
        else:
            if i < train_val_num:
                val_file.write(",".join(file) + "\n")
                trainval_file.write(",".join(file) + "\n")
            i += 1

    train_file.close()
    val_file.close()
    trainval_file.close()
    return (train_num, val_num, train_val_num)


def get_input_dataset(value):
    if value is None:
        return
        if isinstance(value, str):
            _value = value.replace("\\", "/")
            try:
                _index = _value.rindex("|")
            except:
                try:
                    _index = _value.rindex("/")
                except:
                    _index = -1

            if _index < 0:
                return value
        else:
            _ds_info = _value[None[:_index]]
            if _ds_info.find("\\") >= 0 or _ds_info.find("/") >= 0 or _ds_info.find(":") >= 0:
                ds = Workspace().open_datasource(_ds_info, True)
                if ds is not None:
                    return ds[_value[(_index + 1)[:None]]]
                    return
                else:
                    pass
            alias = _value[None[:_index]]
            ds = Workspace().get_datasource(alias)
            if ds is not None:
                dt_name = value[(_index + 1)[:None]]
                return ds[dt_name]
            return
    else:
        if isinstance(value, Dataset):
            return value
        return value


def _get_dataset_readonly(value):
    if value is None:
        return
        if isinstance(value, str):
            _value = value.replace("\\", "/")
            try:
                _index = _value.rindex("|")
            except:
                try:
                    _index = _value.rindex("/")
                except:
                    _index = -1

            if _index < 0:
                return value
        else:
            _ds_info = _value[None[:_index]]
            if _ds_info.find("\\") >= 0 or _ds_info.find("/") >= 0 or _ds_info.find(":") >= 0:
                conn = DatasourceConnectionInfo(_ds_info)
                conn.set_readonly(True)
                ds = Workspace().open_datasource(conn, True)
                if ds is not None:
                    return ds[_value[(_index + 1)[:None]]]
                    return
                else:
                    pass
            alias = _value[None[:_index]]
            ds = Workspace().get_datasource(alias)
            if ds is not None:
                dt_name = value[(_index + 1)[:None]]
                return ds[dt_name]
            return
    else:
        if isinstance(value, Dataset):
            return value
        return value


def view_bar(num, total):
    """
    进度条
    :param num: 当前进度
    :param total: 任务总量
    :return:
    """
    rate = float(num) / float(total)
    rate_num = int(rate * 100)
    r = "\r[%s%s]%d%%,%d" % (">" * rate_num, "-" * (100 - rate_num), rate_num, num)
    sys.stdout.write(r)
    sys.stdout.flush()


def ordered_yaml_dump(data, stream=None, Dumper=yaml.SafeDumper, **kwds):

    class OrderedDumper(Dumper):
        pass

    def _dict_representer(dumper, data):
        return dumper.represent_mapping(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, data.items())

    OrderedDumper.add_representer(OrderedDict, _dict_representer)
    return (yaml.dump)(data, stream, OrderedDumper, **kwds)


def save_config_to_yaml(config: OrderedDict, yaml_file: str, encoding='utf8') -> None:
    """
    save the config to a yaml format file
    :param config:
    :param yaml_file:
    :param encoding:
    :return:
    """
    with open(yaml_file, "w", encoding=encoding) as f:
        ordered_yaml_dump(config, f, encoding="utf8", allow_unicode=True)


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


def _is_image_file(input_data):
    """
    输入数据是否为影像文件
    通过后缀名判断
    """
    try:
        with rasterio.open(input_data) as ds:
            data_is_image = True
    except Exception as e:
        try:
            data_is_image = False
        finally:
            e = None
            del e

    return data_is_image


def save_pattle_png(image, color_codes, out_file):
    if out_file.endswith("png"):
        r = sorted((color_codes.items()), key=(lambda d: d[1]))
        palette = [color_value for class_color in r for color_value in iter((class_color[0]))]
        out = Image.fromarray((np.squeeze(image)), mode="P")
        out.putpalette(palette)
        out.save(out_file, optimize=True)
    else:
        raise Exception("out_file should end with png")


def del_dir(path, is_del_dir=True):
    """
       删除文件夹
    """
    if is_del_dir is True:
        if os.path.exists(path):
            shutil.rmtree(path)


def compute_bbox_iou(box, boxes, box_area, boxes_area):
    """Calculates IoU of the given box with the array of the given boxes.
    # 使用给定框的数组计算给定框的IoU。即计算一个bbox和一组bbox的iou
    box: 1D vector [y1, x1, y2, x2], equal to [ymin,xmin,ymax,xmax]
    boxes: [boxes_count, (y1, x1, y2, x2)]
    box_area: float. the area of 'box'  'box'的面积
    boxes_area: array of length boxes_count.  长度数组box_count
    Note: the areas are passed in rather than calculated here for
          efficency. Calculate once in the caller to avoid duplicate work.
    :return: 一维数组
    """
    y1 = np.maximum(box[0], boxes[(None[:None], 0)])
    y2 = np.minimum(box[2], boxes[(None[:None], 2)])
    x1 = np.maximum(box[1], boxes[(None[:None], 1)])
    x2 = np.minimum(box[3], boxes[(None[:None], 3)])
    intersection = np.maximum(x2 - x1, 0) * np.maximum(y2 - y1, 0)
    union = box_area + boxes_area[None[:None]] - intersection[None[:None]]
    iou = intersection / union
    return iou


def non_max_suppression(boxes, scores, threshold):
    """Performs non-maximum supression and returns indicies of kept boxes.
    执行非最大抑制并返回保留框的索引。
    boxes: [N, (y1, x1, y2, x2)]. Notice that (y2, x2) lays outside the box. 注意（y2，x2）在框外。
    scores: 1-D array of box scores.
    threshold: Float. IoU threshold to use for filtering. 用于过滤的IoU阈值
    """
    assert boxes.shape[0] > 0
    if boxes.dtype.kind != "f":
        boxes = boxes.astype(np.float32)
    y1 = boxes[(None[:None], 0)]
    x1 = boxes[(None[:None], 1)]
    y2 = boxes[(None[:None], 2)]
    x2 = boxes[(None[:None], 3)]
    area = (y2 - y1) * (x2 - x1)
    ixs = scores.argsort()[None[None:-1]]
    pick = []
    while len(ixs) > 0:
        i = ixs[0]
        pick.append(i)
        iou = compute_bbox_iou(boxes[i], boxes[ixs[1[:None]]], area[i], area[ixs[1[:None]]])
        remove_ixs = np.where(iou > threshold)[0] + 1
        ixs = np.delete(ixs, remove_ixs)
        ixs = np.delete(ixs, 0)

    return np.array(pick, dtype=(np.int32))


def get_pic_path_from_dir(input_dir, get_all_dir, suffix):
    """
    从给定的文件目录下获取指定后缀图片的完整路径
    :param input_dir: 输入文件目录的路径
    :type input_dir: str
    :param get_all_dir: 是否获取输入路径下所有子目录内图片
    :type get_all_dir: bool
    :param suffix: 指定获取图片的后缀
    :type suffix: list

    :return image_path_list: 所获图片的完整路径
    :type image_path_list: list [image_path1,image_path2,...]
    """
    image_path_list = []
    if get_all_dir:
        for root, dir, files in os.walk(input_dir):
            for file in files:
                file_suffix = file.split(".")[-1]
                if file_suffix in suffix:
                    image_path = os.path.join(root, file)
                    image_path_list.append(image_path)

    else:
        files = os.listdir(input_dir)
        for file in files:
            file_suffix = file.split(".")[-1]
            if file_suffix in suffix:
                image_path = os.path.join(input_dir, file)
                image_path_list.append(image_path)

    return image_path_list


def mkdir_not_exist(path_list):
    """
    创建单个或者多个不存在的文件路径
    path_list[path1, path2, path3]
    :param path1:某个需要被创建的文件路径
    type path1: str
    """
    for _path in path_list:
        if not os.path.exists(_path):
            os.makedirs(_path)

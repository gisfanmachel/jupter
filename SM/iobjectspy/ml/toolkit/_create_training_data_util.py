# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\toolkit\_create_training_data_util.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 4003 bytes
import os, warnings, rasterio, yaml
from dotmap import DotMap
from rasterio.windows import Window
from iobjectspy import Dataset

def _save_img(ds, tile_format, block_xmin, block_ymin, tile_size_x, tile_size_y, output_path_images, transf, input_data=None):
    """
    保存tile
    :param ds: rasterio读取影像文件
    :param tile_format: 保存的影像文件格式
    :param block_xmin: tile左上方像素坐标(x方向)
    :param block_ymin: tile左上方像素坐标(y方向)
    :param tile_size_x: tile的宽
    :param tile_size_y: tile的高
    :param output_path_images: 输出tile的路径
    :param transf: 每个tile的transf
    :param input_data: 原始影像文件路径
    """
    img = ds.read(window=(Window(block_xmin, block_ymin, tile_size_x, tile_size_y)))
    if tile_format == "jpg":
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            dst = rasterio.open((output_path_images + "." + tile_format), "w", driver="JPEG",
              width=tile_size_x,
              height=tile_size_y,
              count=3,
              dtype=(ds.dtypes[0]))
            dst.write(img[(None[:3], None[:None], None[:None])])
    else:
        if tile_format == "png":
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                dst = rasterio.open((output_path_images + "." + tile_format), "w", driver="PNG",
                  width=tile_size_x,
                  height=tile_size_y,
                  count=3,
                  dtype=(ds.dtypes[0]))
                dst.write(img[(None[:3], None[:None], None[:None])])
        else:
            if tile_format == "tif":
                dst = rasterio.open((output_path_images + "." + tile_format), "w", driver="GTiff",
                  width=tile_size_x,
                  height=tile_size_y,
                  count=(ds.count),
                  bounds=(ds.bounds),
                  crs=(ds.crs),
                  transform=transf,
                  dtype=(ds.dtypes[0]))
                dst.write(img)
            else:
                if tile_format == "origin":
                    dst = rasterio.open((output_path_images + os.path.splitext(input_data)[-1]), "w", driver=(ds.driver),
                      width=tile_size_x,
                      height=tile_size_y,
                      count=(ds.count),
                      bounds=(ds.bounds),
                      crs=(ds.crs),
                      transform=transf,
                      dtype=(ds.dtypes[0]))
                    dst.write(img)
                dst.close()


def get_key(dict, value):
    """
    字典通过value查找key
    :param dict: 字典
    :param value: 值
    :return: key : 键
    """
    return [k for k, v in dict.items() if v == value]


def _get_input_feature(input_label):
    """
    :param input_label: 矢量数据集
    :return: features
    """
    if isinstance(input_label, Dataset):
        input_label = input_label.get_features()
    else:
        if isinstance(input_label, str):
            with open(input_label, "r") as f:
                pass
    return input_label


def get_tile_start_index(tile_start_index, tile_count_yml):
    """
    获取训练数据生成的文件索引
   :param tile_start_index: 文件索引数
   :param tile_count_yml: 训练数据配置文件(.sda)
   :return: tile_start_index
   """
    if tile_start_index == -1:
        try:
            with open(tile_count_yml) as f:
                config_dict = yaml.load(f, Loader=(yaml.FullLoader))
            voc_config = DotMap(config_dict)
            tile_start_index = voc_config.dataset.get("image_count")
        except:
            tile_start_index = 0

    else:
        tile_start_index = tile_start_index
    return tile_start_index


def _rgb(v):
    """
    获取RGB颜色
   :param v: 十六进制颜色码
   :return: RGB颜色值
       """
    r, g, b = v[1[:3]], v[3[:5]], v[5[:7]]
    return (int(r, 16), int(g, 16), int(b, 16))


def get_image_transf(input_data):
    with rasterio.open(input_data) as ds:
        transf = ds.transform
    return transf


def get_image_crs(input_data):
    with rasterio.open(input_data) as ds:
        crs = ds.crs
    return crs

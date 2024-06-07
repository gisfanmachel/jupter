# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\unet.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 55118 bytes
"""
@author: YangRuijie
@license: 
@contact: yangruijie@supermap.com
@software: 
@file: unet.py.py
@time: 4/4/19 3:33 AM
@desc:
"""
import os, keras
from keras.utils import multi_gpu_model
from iobjectspy._jsuperpy.data._util import get_output_datasource, get_input_dataset
from toolkit._keras_loss import IOUScore
from ....._logger import log_error, log_warning, log_info
os.environ["KERAS_BACKEND"] = "tensorflow"
import shutil, tempfile
from iobjectspy import Dataset, raster_to_vector, DatasourceConnectionInfo, Datasource, import_tif, DatasetType, datasetraster_to_numpy_array, numpy_array_to_datasetraster, EngineType
from toolkit._toolkit import view_bar, stretch_n, get_percentclip_min_max, stretch_min_max, get_image_from_csv, split_train_val_withdirs, get_config_from_yaml
from toolkit._keras_model_utils import bce_dice_loss, dice_coef, find_last
from .base_keras_models import Trainer
from _seg_models.model_builder import build_model
from _seg_models.encs.cls_models.cls_models.utils import get_weights_default_path
from _seg_models.encs.cls_models.cls_models.weights import weights_collection
import numpy as np, rasterio, tensorflow as tf
from rasterio.plot import reshape_as_image, reshape_as_raster
from rasterio.windows import Window
from keras import backend as K
K.set_image_data_format("channels_last")
from keras.losses import binary_crossentropy, categorical_crossentropy
from keras.optimizers import Adam

class UnetEstimation:

    def __init__(self, model_path, config):
        if not isinstance(model_path, str):
            raise TypeError("model_path data type inappropriate ，should be str ")
        if not os.path.exists(model_path):
            raise Exception("model_path  path not exists")
        self.model_input = config.model_input[0]
        self.model_output = config.model_output[0]
        if np.argmin(self.model_input.shape) == 0:
            self.band_order = "first"
            self.seg_size = self.model_input.shape[1]
            self.input_bands = self.model_input.shape[0]
            self.out_width_height = [self.model_output.shape[1], self.model_output.shape[2]]
            self.output_msk_num = self.model_output.shape[0]
            if self.model_input.shape[1] != self.model_input.shape[2]:
                raise ValueError("Model input width and height should be equal!")
        else:
            self.band_order = "last"
            self.seg_size = self.model_input.shape[1]
            self.input_bands = self.model_input.shape[-1]
            self.out_width_height = [self.model_output.shape[0], self.model_output.shape[1]]
            self.output_msk_num = self.model_output.shape[-1]
            if self.model_input.shape[1] != self.model_input.shape[0]:
                raise ValueError("Model input width and height should be equal!")
            self.class_type = config.class_type
            self.color_map = {c.class_value: tuple(c.class_color) for c in self.class_type}
            self.is_stretch = config.is_stretch
            self.model_path = model_path
            self.sess = None
            self.tf_inputs = None
            self.tf_outputs = None
            self.load_model(model_path)

    def augment_data(self, input_tile):
        img90 = np.array(np.rot90(input_tile))
        img1 = np.concatenate([input_tile[None], img90[None]])
        img2 = np.array(img1)[(None[:None], None[None:-1])]
        img3 = np.concatenate([img1, img2])
        img4 = np.array(img3)[(None[:None], None[:None], None[None:-1])]
        img5 = img3.transpose(0, 3, 1, 2)
        img_augment1 = np.array(img5, np.float32) / 255.0 * 3.2 - 1.6
        img6 = img4.transpose(0, 3, 1, 2)
        img_augment2 = np.array(img6, np.float32) / 255.0 * 3.2 - 1.6
        return (
         img_augment1, img_augment2)

    def estimate_img(self, input_img, coversize, out_path, out_dataset_name, result_type, **kwargs):
        """

        :param input_img:
        :param coversize:
        :param out_path:
        :param out_dataset_name:
        :param result_type: region or grid
        :param kwargs:
        :return:
        """
        self.half_oversize = coversize
        dsm_dataset = kwargs.get("dsm_dataset")
        if not result_type in ('grid', 'region'):
            raise AssertionError("result_type should be grid or region")
        else:
            if self.output_msk_num > 1:
                self.back_or_no_value = -9999
            else:
                self.back_or_no_value = 0
            dom_is_udb = False
            try:
                rasterio.open(input_img)
            except Exception as e:
                try:
                    dom_is_udb = True
                finally:
                    e = None
                    del e

            if dom_is_udb:
                if isinstance(input_img, str):
                    input_img = get_input_dataset(input_img)
                else:
                    if not isinstance(input_img, Dataset):
                        raise TypeError("image_dataset data type inappropriate ，should be  str or Dataset")
                    else:
                        dom_bounds = input_img.bounds
                        x_pixel_res = (dom_bounds.right - dom_bounds.left) / input_img.width
                        y_pixel_res = (dom_bounds.top - dom_bounds.bottom) / input_img.height
                        coord_array = [
                         x_pixel_res,
                         0,
                         0,
                         y_pixel_res,
                         dom_bounds.left,
                         dom_bounds.bottom]
                        if not dsm_dataset is None:
                            input_martix = dsm_dataset or datasetraster_to_numpy_array(input_img)
                        else:
                            pass
                        dom = datasetraster_to_numpy_array(input_img)
                        dsm = datasetraster_to_numpy_array(dsm_dataset)
                        input_martix = np.concatenate((dom, dsm[(np.newaxis, None[:None], None[:None])]))
                    result_int, result_dataset = self._predict_with_matix(input_martix,
                      out_path, out_dataset_name, coord_array=coord_array, band_order="first", result_type=result_type)
            else:
                result_dataset = self.predict_with_rasterio(input_img, dsm_dataset, out_path, out_dataset_name,
                  result_type=result_type)
        return result_dataset

    def estimate_numpy(self, input_img, coversize, **kwargs):
        self.half_oversize = coversize
        result_numpy = self._predict_with_numpy(input_img, self.band_order)
        return result_numpy

    def estimate_tile(self, input_img, single_thresold=0.5):
        if self.band_order == "first":
            assert input_img.shape[0] == self.model_input.shape[0], "channel first channel顺序不对或channel数量不对"
            assert input_img.shape[1] <= self.seg_size, "输入图像长宽应小于等于{}".format(self.seg_size)
            assert input_img.shape[2] <= self.seg_size, "输入图像长宽应小于等于{}".format(self.seg_size)
            input_width_height = [input_img.shape[1], input_img.shape[2]]
            process_img = np.pad(input_img, (
             (0, 0), (0, self.seg_size - input_img.shape[1]), (0, self.seg_size - input_img.shape[2])), "constant")
        else:
            assert input_img.shape[2] == self.model_input.shape[2], "channel last channel顺序不对或channel数量不对"
            assert input_img.shape[0] <= self.seg_size, "输入图像长宽应小于等于{}".format(self.seg_size)
            assert input_img.shape[1] <= self.seg_size, "输入图像长宽应小于等于{}".format(self.seg_size)
            input_width_height = [input_img.shape[0], input_img.shape[1]]
            process_img = np.pad(input_img, (
             (
              0, self.seg_size - input_img.shape[0]), (0, self.seg_size - input_img.shape[1]), (0, 0)), "constant")
        output_img_shape = (
         self.out_width_height[0], self.out_width_height[1], self.output_msk_num)
        result_tile = self._predict_tile_local(process_img[(np.newaxis, ...)], output_img_shape)
        if self.output_msk_num > 1:
            result_tile = np.argmax(result_tile, 0 if self.band_order == "first" else -1).astype(input_img.dtype)
        else:
            predict_msk = result_tile[(0, None[:None], None[:None])] if self.band_order == "first" else result_tile[(None[:None], None[:None], 0)]
            result_tile = (predict_msk > single_thresold).astype(input_img.dtype)
        return result_tile[(None[:input_width_height[0]], None[:input_width_height[1]])]

    def _predict_with_numpy(self, image_matix, band_order='last', single_thresold=0.5):
        if self.band_order is not band_order:
            if band_order is "first":
                image_matix = np.transpose(image_matix, (1, 2, 0))
            else:
                if band_order is "last":
                    image_matix = np.transpose(image_matix, (2, 0, 1))
                else:
                    raise Exception("band_order参数错误")
        else:
            predict_msk = self._UnetEstimation__predict_with_preload(image_matix)
            if self.output_msk_num > 1:
                predict_int = np.argmax(predict_msk, 0 if self.band_order == "first" else -1)
            else:
                predict_msk = predict_msk[(0, None[:None], None[:None])] if self.band_order == "first" else predict_msk[(None[:None], None[:None], 0)]
            predict_int = predict_msk > single_thresold
        return predict_int

    def _predict_with_matix(self, image_matix, out_ds, dst_name, band_order="last", coord_array=[1, 0, 0, 1, 0, 0], single_thresold=0.5, result_type="grid"):
        """
        基于输入的图像矩阵，得到的预测结果二值图和矢量数据

        :param image_matix: ndarray输入的原始图像矩阵
        :param out_ds: 输出矢量数据要存储的数据源
        :param dst_name: 输出矢量数据集的名字
        :param band_order: 输入数据集的band所在维度 'last' or 'first'
        :param coord_array: array 数组，依次为 0——X方向上的象素分辨素， 1——X方向的旋转系数，2——Y方向的旋转系数，
            3——Y方向上的象素分辨率，4——栅格地图左下角象素中心X坐标，5——栅格地图左下角象素中心Y坐标
        :param single_thresold:  概率阈值，概率超过该值的像素则会输出为矢量
        :param result_type: grid or region
        :type result_type: str
        :return: （predict_int,result） predict_int——ndarray 二值或多值二维矩阵,result——矢量数据集
        """
        if self.band_order is not band_order:
            if band_order is "first":
                image_matix = np.transpose(image_matix, (1, 2, 0))
            else:
                if band_order is "last":
                    image_matix = np.transpose(image_matix, (2, 0, 1))
                else:
                    raise Exception("band_order参数错误")
        else:
            predict_msk = self._UnetEstimation__predict(image_matix)
            if self.output_msk_num > 1:
                predict_int = np.argmax(predict_msk, 0 if self.band_order == "first" else -1)
            else:
                predict_msk = predict_msk[(0, None[:None], None[:None])] if self.band_order == "first" else predict_msk[(None[:None], None[:None], 0)]
                predict_int = predict_msk > single_thresold
            predict_int = predict_int.astype(np.int)
            tmp_dsc = DatasourceConnectionInfo(server=":memory:", engine_type=(EngineType.MEMORY))
            tmp_ds = Datasource().create(tmp_dsc)
            result_dst = numpy_array_to_datasetraster(predict_int, (coord_array[0]), (coord_array[3]), tmp_ds, (coord_array[4]),
              (coord_array[5]), "tmp", as_grid=True)
            if result_type.strip() == "grid":
                out_ds = get_output_datasource(out_ds)
                result = out_ds.copy_dataset(result_dst, dst_name)
            else:
                if result_type.strip() == "region":
                    result = raster_to_vector(result_dst, "class_type", out_dataset_type=(DatasetType.REGION), back_or_no_value=(self.back_or_no_value),
                      is_thin_raster=True,
                      out_data=out_ds,
                      out_dataset_name=dst_name)
                else:
                    raise Exception("result_type error ,result_type should be region or grid")
        tmp_ds.delete_all()
        tmp_ds.close()
        return (
         predict_int, result)

    def predict_with_rasterioParse error at or near `COME_FROM' instruction at offset 1858_0

    def __predict(self, input_image):
        """
        输入numpy的影像数据，进行预测

        :param input_image: numpy输入影像
        :type input_image: ndarray
        :return:
        """
        if self.is_stretch:
            input_image = stretch_n(input_image)
        else:
            predict_merge = np.zeros((input_image.shape[0], input_image.shape[1], self.output_msk_num), dtype=(np.float))
            seg_size = self.seg_size
            half_oversize = self.half_oversize
            if self.band_order == "last":
                predict_tile = self._UnetEstimation__make_predict_tile(input_image, seg_size=seg_size, half_oversize=half_oversize, band_order="last")
                out_shape = (predict_tile.shape[0], self.out_width_height[0], self.out_width_height[1], self.output_msk_num)
                predict_y = self._predict_tile_local(predict_tile, out_shape)
                self.close_model()
                predict_merge = self._UnetEstimation__make_predict_merage(predict_y, predict_merge, seg_size=seg_size, half_oversize=half_oversize,
                  band_order="last")
            else:
                predict_tile = self._UnetEstimation__make_predict_tile(input_image, seg_size=seg_size, half_oversize=half_oversize, band_order="first")
                out_shape = (predict_tile.shape[0], self.output_msk_num, self.out_width_height[0], self.out_width_height[1])
                predict_y = self._predict_tile_local(predict_tile, out_shape)
                self.close_model()
            predict_merge = self._UnetEstimation__make_predict_merage(predict_y, predict_merge, seg_size=seg_size, half_oversize=half_oversize,
              band_order="first")
        return predict_merge

    def __predict_with_preload(self, input_image):
        """
        输入numpy的影像数据，进行预测

        :param input_image: numpy输入影像
        :type input_image: ndarray
        :return:
        """
        if self.is_stretch:
            input_image = stretch_n(input_image)
        else:
            predict_merge = np.zeros((input_image.shape[0], input_image.shape[1], self.output_msk_num), dtype=(np.float))
            seg_size = self.seg_size
            half_oversize = self.half_oversize
            if self.band_order == "last":
                predict_tile = self._UnetEstimation__make_predict_tile(input_image, seg_size=seg_size, half_oversize=half_oversize, band_order="last")
                out_shape = (predict_tile.shape[0], self.out_width_height[0], self.out_width_height[1], self.output_msk_num)
                predict_y = self._predict_tile_local(predict_tile, out_shape)
                predict_merge = self._UnetEstimation__make_predict_merage(predict_y, predict_merge, seg_size=seg_size, half_oversize=half_oversize,
                  band_order="last")
            else:
                predict_tile = self._UnetEstimation__make_predict_tile(input_image, seg_size=seg_size, half_oversize=half_oversize, band_order="first")
            out_shape = (
             predict_tile.shape[0], self.output_msk_num, self.out_width_height[0], self.out_width_height[1])
            predict_y = self._predict_tile_local(predict_tile, out_shape)
            predict_merge = self._UnetEstimation__make_predict_merage(predict_y, predict_merge, seg_size=seg_size, half_oversize=half_oversize,
              band_order="first")
        return predict_merge

    def __make_predict_tile(self, image, seg_size, half_oversize, band_order='last'):
        """
        to divided the image to be predicted a specified size

        :param image:   input predicted image
        :param seg_size: specified divide size
        :param oversize: each patch overlapping size
        :return: divided image list
        """
        if band_order == "first":
            image = np.transpose(image, (1, 2, 0))
        x = []
        oversize = 2 * half_oversize
        count_x = int((image.shape[0] - oversize) / (seg_size - oversize)) + 1
        count_y = int((image.shape[1] - oversize) / (seg_size - oversize)) + 1
        realsize = seg_size - oversize
        if count_x == 1 and count_y == 1:
            im = np.zeros((seg_size, seg_size, image.shape[2]), dtype=(np.float))
            im[(0[:image.shape[0]], 0[:image.shape[1]], None[:None])] = image
            x.append(im)
        else:
            if count_x == 1 and count_y is not 1:
                im = np.zeros((seg_size, seg_size, image.shape[2]), dtype=(np.float))
                for i in range(0, count_y):
                    if i == 0:
                        im[(0[:image.shape[0]], None[:None])] = image[(None[:None], 0[:seg_size], None[:None])]
                        x.append(im)
                    elif i == count_y - 1:
                        im[(0[:image.shape[0]], 0[:image.shape[1] - realsize * (count_y - 1)])] = image[(None[:None],
                         (realsize * i)[:image.shape[1]], None[:None])]
                        x.append(im)
                    else:
                        im[(0[:image.shape[0]], None[:None])] = image[(None[:None], (realsize * i)[:realsize * i + seg_size], None[:None])]
                        x.append(im)

            else:
                if count_y == 1 and count_x is not 1:
                    im = np.zeros((seg_size, seg_size, image.shape[2]), dtype=(np.float))
                    for i in range(0, count_x):
                        if i == 0:
                            im[(None[:None], 0[:image.shape[1]])] = image[(0[:seg_size], None[:None], None[:None])]
                            x.append(im)
                        elif i == count_x - 1:
                            im[(0[:image.shape[0] - realsize * (count_x - 1)], 0[:image.shape[1]])] = image[(
                             (realsize * i)[:image.shape[0]], None[:None], None[:None])]
                            x.append(im)
                        else:
                            im[(None[:None], 0[:image.shape[1]])] = image[((realsize * i)[:realsize * i + seg_size], None[:None], None[:None])]
                            x.append(im)

                else:
                    for i in range(0, count_x):
                        for j in range(0, count_y):
                            im = np.zeros((seg_size, seg_size, image.shape[2]), dtype=(np.float))
                            if i == 0:
                                if j == 0:
                                    im = image[(0[:seg_size], 0[:seg_size])]
                                    x.append(im)
                            if i == 0:
                                if j is not 0:
                                    if j == count_y - 1:
                                        im[(None[:None], 0[:image.shape[1] - realsize * (count_y - 1)])] = image[(0[:seg_size],
                                         (realsize * j)[:image.shape[1]], None[:None])]
                                        x.append(im)
                                    else:
                                        im = image[(0[:seg_size], (realsize * j)[:realsize * j + seg_size], None[:None])]
                                        x.append(im)
                            if j == 0:
                                if i is not 0:
                                    if i == count_x - 1:
                                        im[(0[:image.shape[0] - realsize * (count_x - 1)], None[:None])] = image[((realsize * i)[:image.shape[0]],
                                         0[:seg_size], None[:None])]
                                        x.append(im)
                                    else:
                                        im = image[((realsize * i)[:realsize * i + seg_size], 0[:seg_size], None[:None])]
                                        x.append(im)
                            if i == count_x - 1:
                                if j == count_y - 1:
                                    im[(0[:image.shape[0] - realsize * (count_x - 1)], 0[:image.shape[1] - realsize * (count_y - 1)])] = image[((realsize * i)[:image.shape[0]],
                                     (realsize * j)[:image.shape[1]], None[:None])]
                                    x.append(im)
                            if i == count_x - 1 and j is not count_y - 1:
                                im[(0[:image.shape[0] - realsize * (count_x - 1)], None[:None])] = image[((realsize * i)[:image.shape[0]],
                                 (realsize * j)[:realsize * j + seg_size], None[:None])]
                                x.append(im)
                            elif i is not count_x - 1 and j == count_y - 1:
                                im[(None[:None], 0[:image.shape[1] - realsize * (count_y - 1)])] = image[(
                                 (realsize * i)[:realsize * i + seg_size],
                                 (realsize * j)[:image.shape[1]], None[:None])]
                                x.append(im)
                            else:
                                im = image[((realsize * i)[:realsize * i + seg_size], (realsize * j)[:realsize * j + seg_size], None[:None])]
                                x.append(im)

        if band_order == "first":
            x = np.transpose(x, (0, 3, 1, 2))
        return np.array(x)

    def __make_predict_merage(self, predict_y, predict_merge, seg_size, half_oversize, band_order='last'):
        """
        merage the predicted tiles, only channels last
        maybe have a bug ,the axis x maybe have a data lose,but the reason isn't found

        :param predict_y: predict tiles
        :param predict_merge: merage
        :param seg_size: divided size
        :param half_oversize: half overlap size
        :return: meraged image
        """
        if band_order == "first":
            predict_y = np.transpose(predict_y, (0, 2, 3, 1))
        oversize = 2 * half_oversize
        count_x = int((predict_merge.shape[0] - oversize) / (seg_size - oversize)) + 1
        count_y = int((predict_merge.shape[1] - oversize) / (seg_size - oversize)) + 1
        realsize = seg_size - oversize
        if count_x == 1 and count_y == 1:
            predict_merge = predict_y[0][(0[:predict_merge.shape[0]], 0[:predict_merge.shape[1]])]
        else:
            if count_x == 1 and count_y is not 1:
                for i in range(0, count_y):
                    if i == 0:
                        predict_merge[(None[:None], 0[:seg_size - half_oversize], None[:None])] = predict_y[i][(0[:predict_merge.shape[0]],
                         0[:seg_size - half_oversize])]
                    elif i == count_y - 1:
                        predict_merge[(None[:None], (realsize * i + half_oversize)[:None], None[:None])] = predict_y[i][(0[:predict_merge.shape[0]],
                         half_oversize[:predict_merge.shape[1] - realsize * (count_y - 1)])]
                    else:
                        predict_merge[(None[:None], (realsize * i + half_oversize)[:realsize * i + seg_size - half_oversize], None[:None])] = predict_y[i][(0[:predict_merge.shape[0]], half_oversize[:seg_size - half_oversize])]

            else:
                if count_y == 1 and count_x is not 1:
                    for i in range(0, count_x):
                        if i == 0:
                            predict_merge[(0[:seg_size - half_oversize], None[:None], None[:None])] = predict_y[i][(0[:seg_size - half_oversize],
                             0[:predict_merge.shape[1]])]
                        elif i == count_x - 1:
                            predict_merge[((realsize * i + half_oversize)[:None], None[:None], None[:None])] = predict_y[i][(
                             half_oversize[:predict_merge.shape[0] - realsize * (count_y - 1)],
                             0[:predict_merge.shape[1]])]
                        else:
                            predict_merge[((realsize * i + half_oversize)[:realsize * i + seg_size - half_oversize], None[:None], None[:None])] = predict_y[i][(half_oversize[:seg_size - half_oversize], 0[:predict_merge.shape[1]])]

                else:
                    for i in range(0, count_x):
                        for j in range(0, count_y):
                            if i == 0 and j == 0:
                                predict_merge[(0[:seg_size - half_oversize], 0[:seg_size - half_oversize])] = predict_y[i * count_y + j][(
                                 0[:seg_size - half_oversize],
                                 0[:seg_size - half_oversize])]
                            elif i == 0:
                                if j is not 0:
                                    if j == count_y - 1:
                                        predict_merge[(0[:seg_size - half_oversize], (realsize * j + half_oversize)[:None], None[:None])] = predict_y[i * count_y + j][(
                                         0[:seg_size - half_oversize],
                                         half_oversize[:predict_merge.shape[1] - realsize * (count_y - 1)])]
                                else:
                                    predict_merge[(0[:seg_size - half_oversize], (realsize * j + half_oversize)[:realsize * j + seg_size - half_oversize], None[:None])] = predict_y[i * count_y + j][(
                                     0[:seg_size - half_oversize],
                                     half_oversize[:seg_size - half_oversize])]
                            elif j == 0:
                                if i is not 0:
                                    if i == count_x - 1:
                                        predict_merge[((realsize * i + half_oversize)[:None], 0[:seg_size - half_oversize], None[:None])] = predict_y[i * count_y + j][(
                                         half_oversize[:predict_merge.shape[0] - realsize * (count_x - 1)],
                                         0[:seg_size - half_oversize])]
                                else:
                                    predict_merge[((realsize * i + half_oversize)[:realsize * i + seg_size - half_oversize], 0[:seg_size - half_oversize], None[:None])] = predict_y[i * count_y + j][(
                                     half_oversize[:seg_size - half_oversize],
                                     0[:seg_size - half_oversize], None[:None])]
                            elif i == count_x - 1 and j == count_y - 1:
                                predict_merge[((realsize * i + half_oversize)[:None], (realsize * j + half_oversize)[:None], None[:None])] = predict_y[i * count_y + j][(
                                 half_oversize[:predict_merge.shape[0] - realsize * i],
                                 half_oversize[:predict_merge.shape[1] - realsize * j])]
                            elif i == count_x - 1 and j is not count_y - 1:
                                predict_merge[((realsize * i + half_oversize)[:None], (realsize * j + half_oversize)[:realsize * j + seg_size - half_oversize], None[:None])] = predict_y[i * count_y + j][(
                                 half_oversize[:predict_merge.shape[0] - realsize * i],
                                 half_oversize[:seg_size - half_oversize], None[:None])]
                            elif i is not count_x - 1 and j == count_y - 1:
                                predict_merge[((realsize * i + half_oversize)[:realsize * i + seg_size - half_oversize], (realsize * j + half_oversize)[:None], None[:None])] = predict_y[i * count_y + j][(
                                 half_oversize[:seg_size - half_oversize],
                                 half_oversize[:predict_merge.shape[1] - realsize * j], None[:None])]
                            else:
                                predict_merge[((realsize * i + half_oversize)[:realsize * i + seg_size - half_oversize], (realsize * j + half_oversize)[:realsize * j + seg_size - half_oversize], None[:None])] = predict_y[i * count_y + j][(
                                 half_oversize[:seg_size - half_oversize],
                                 half_oversize[:seg_size - half_oversize], None[:None])]

        if band_order == "first":
            predict_merge = np.transpose(predict_merge, (1, 2, 0))
        return predict_merge

    def _predict_tile_local(self, predict_tile, out_shape):
        """
        利用给定的模型使用tensorflow推断得到模型预测结果
        :param predict_tile:  ndarray 需要预测的数组片 形状为 （tile_nums,:） 即第一列为图片的数量
        :param out_shape: tuple 输出结果的形状  如（100,320,320,1）
        :return:  ndarray 返回预测的结果
        """
        x_tensor_name = self.signature["predict"].inputs["images"].name
        y_tensor_name = self.signature["predict"].outputs["scores"].name
        x = self.sess.graph.get_tensor_by_name(x_tensor_name)
        y = self.sess.graph.get_tensor_by_name(y_tensor_name)
        self.sess.graph.finalize()
        batch_size = 1
        total_batch = int(predict_tile.shape[0] / batch_size)
        for i in range(total_batch):
            out = self.sess.run(y, feed_dict={x: (predict_tile[((i * batch_size)[:(i + 1) * batch_size], None[:None])])})
            if i == 0:
                y_all = out
            else:
                y_all = np.concatenate((y_all, out), 0)

        y_out = np.expand_dims(y_all, axis=0)
        y_out.resize(out_shape)
        return y_out

    def load_model(self, model_path):
        self.model_path = model_path
        self.sess = tf.Session()
        self.meta_graph_def = tf.saved_model.loader.load(self.sess, ["serve"], model_path)
        self.signature = self.meta_graph_def.signature_def
        self.sess.graph.finalize()

    def close_model(self):
        """
        关闭模型
        :return:
        """
        self.sess.close()
        tf.reset_default_graph()


class UnetTrainer(Trainer):

    def __init__(self):
        super().__init__()
        self.callbacks = []
        self.loss = []
        self.acc = []
        self.val_loss = []
        self.val_acc = []
        self.model_architecture = "unet"
        self.single_model = None

    def train(self, train_data_path, config, epoch=1, batch_size=1, lr=0.001, output_model_path='./', output_model_name='unet', log_path=None, backbone_name='resnext50', backbone_weight_path=None, reload_model=False, pretrained_model_path=None, **kwargs):
        K.clear_session()
        self.gpus = kwargs.get("gpus")
        os.environ["CUDA_VISIBLE_DEVICES"] = ",".join(map(str, kwargs.get("gpus"))) if kwargs.get("gpus") else "0"
        self.config = config
        self.train_data_path = train_data_path
        self.data_config = get_config_from_yaml(os.path.join(self.train_data_path, os.path.basename(self.train_data_path) + ".sda"))
        self.data_type = self.data_config.dataset.data_type
        if not self.data_type in ('multi_classification', 'binary_classifition'):
            raise AssertionError("data_type should be multi_classification or binary_classifition ")
        else:
            self.class_type = self.data_config.dataset.class_type
            self.tile_size = self.data_config.dataset.tile_size
            self.x_type = self.data_config.dataset.x_type
            if self.x_type == "uint8":
                self.is_aug = True
            else:
                self.is_aug = False
            pixel_counts = np.array([c.pixel_count for c in self.class_type])
            self.class_weight = list(pixel_counts.sum(dtype=(np.float64)) / pixel_counts.shape[0] / (pixel_counts + 1.0))
            if self.data_type.strip() == "multi_classification":
                self.output_bands = len(self.class_type)
            else:
                if self.data_type.strip() == "binary_classifition":
                    self.output_bands = 1
                else:
                    log_error("data_type should be multi_classification or binary_classifition")
                    raise Exception("data_type should be multi_classification or binary_classifition")
        self.model_type = self.data_type
        self.input_bands = self.data_config.dataset.x_bandnum
        assert self.input_bands >= 1, "输入波段数应大于等于1"
        assert self.output_bands >= 1, "输出波段数应大于等于1"
        self.backbone_name = backbone_name
        if self.backbone_name is None or self.backbone_name.strip() == "":
            self.backbone_name = self.config.model.backbone_name
            log_warning("backbone_name 为空,将使用默认 backbone_name : {}".format(self.backbone_name))
        self.config = config
        self.epoch = epoch
        self.batch_size = batch_size
        self.lr = lr
        self.output_model_path = output_model_path
        self.output_model_name = output_model_name
        self.backbone_weight_path = backbone_weight_path
        self.pretrained_model_path = pretrained_model_path
        self.log_path = log_path
        self.reload_model = reload_model
        self.config.trainer.num_epochs = epoch
        self.config.trainer.batch_size = batch_size
        self.config.trainer.learning_rate = lr
        if self.pretrained_model_path is not None:
            self.model = build_model((self.tile_size), (self.tile_size), (self.input_bands), (self.output_bands), backbone_name=(self.backbone_name),
              encoder_weights=None,
              net_type="unet")
            checkpoint = find_last(self.pretrained_model_path, self.config.application.name)
            if checkpoint and os.path.exists(checkpoint):
                log_info("从 {} 下加载预训练模型".format(checkpoint))
                self.model.load_weights(checkpoint)
            else:
                log_error("{} 中没有预训练模型".format(self.pretrained_model_path))
        else:
            if self.backbone_weight_path is not None:
                if os.path.isfile(self.backbone_weight_path) and os.path.exists(self.backbone_weight_path):
                    self.model = build_model((self.tile_size), (self.tile_size), (self.input_bands), (self.output_bands), backbone_name=(self.backbone_name),
                      encoder_weights=None,
                      net_type="unet")
                    log_info("从 {} 下加载backbone模型".format(self.backbone_weight_path))
                    self.model.load_weights((self.backbone_weight_path), by_name=True, skip_mismatch=True)
                else:
                    self.model = build_model((self.tile_size), (self.tile_size), (self.input_bands), (self.output_bands), backbone_name=(self.backbone_name),
                      encoder_weights="imagenet",
                      net_type="unet")
            else:
                self.single_model = self.model
                self.init_callbacks(log_path)
                if self.gpus is not None and len(self.gpus) > 1:
                    self.model = multi_gpu_model((self.model), gpus=(len(self.gpus)))
            if self.output_bands == 1:
                self.model.compile(loss=bce_dice_loss, optimizer=Adam(lr=(self.lr)),
                  metrics=[
                 "acc", dice_coef, IOUScore(threshold=0.5)])
            else:
                self.class_index = [i for i in range(len(self.class_type))]
                loss = categorical_crossentropy
                self.model.compile(loss=loss, optimizer=Adam(lr=(self.lr)),
                  metrics=[
                 "acc", IOUScore(threshold=0.5, class_indexes=(self.class_index))])
            if self.config.trainer.num_epochs > 0:
                try:
                    import psutil
                    free_memory = psutil.virtual_memory().total
                except Exception as e:
                    try:
                        free_memory = 4294967296L
                    finally:
                        e = None
                        del e

                train_num, val_num, train_val_num = self._init_data()
                train_path = os.path.join(self.train_data_path, "csv_path", "train.csv")
                val_path = os.path.join(self.train_data_path, "csv_path", "val.csv")
                image_memory = train_val_num * (self.input_bands + self.output_bands) * self.tile_size ** 2
                if image_memory * 2.0 < free_memory:
                    x, y = self._get_data_from_csv(train_path, (self.is_aug), image_size=(self.tile_size))
                    history = self.model.fit(x=x,
                      y=y,
                      validation_data=self._get_data_from_csv(val_path, False, image_size=(self.tile_size)),
                      epochs=(self.config.trainer.num_epochs),
                      verbose=(self.config.trainer.verbose_training),
                      batch_size=(self.config.trainer.batch_size),
                      callbacks=(self.callbacks))
                else:
                    history = self.model.fit_generator((self._get_data_from_csv(train_path, (self.is_aug), image_size=(self.tile_size), generate=True, batch_size=(self.config.trainer.batch_size))()),
                      steps_per_epoch=(int(train_val_num / self.config.trainer.batch_size)),
                      epochs=(self.config.trainer.num_epochs),
                      validation_data=(self._get_data_from_csv(val_path, False, image_size=(self.tile_size), generate=True, batch_size=(self.config.trainer.batch_size))()),
                      validation_steps=(int(val_num / self.config.trainer.batch_size)),
                      verbose=(self.config.trainer.verbose_training),
                      callbacks=(self.callbacks))
                self.loss.extend(history.history["loss"])
                self.acc.extend(history.history["acc"])
                self.val_loss.extend(history.history["val_loss"])
                self.val_acc.extend(history.history["val_acc"])
                checkpoint = find_last(self.log_path, self.config.application.name)
            else:
                checkpoint = find_last((self.pretrained_model_path), (self.config.application.name), best=False)
            K.clear_session()
            K.set_learning_phase(0)
            export_model = build_model((self.tile_size), (self.tile_size), (self.input_bands), (self.output_bands), backbone_name=(self.backbone_name),
              encoder_weights=None,
              net_type="unet")
            export_model.load_weights(checkpoint)
            log_info("export model load from {}".format(checkpoint))
            self._save_tfserving_model(export_model, os.path.join(output_model_path, output_model_name))

    def _init_data(self):
        return split_train_val_withdirs([os.path.join(self.train_data_path, "Images")], [
         os.path.join(self.train_data_path, "Masks")],
          (os.path.join(self.train_data_path, "csv_path")),
          x_ext=(self.data_config.dataset.x_ext),
          y_ext=(self.data_config.dataset.y_ext),
          val_scale=(self.config.trainer.validation_split))

    def _get_data_from_csv(self, data_path, is_aug=False, image_size=None, generate=False, batch_size=None):
        if self.output_bands > 1:
            if data_path.endswith(".csv"):
                if generate:
                    return get_image_from_csv(data_path, is_aug,
                      input_bands=(self.input_bands),
                      output_bands=(self.output_bands),
                      image_size=image_size,
                      generate=generate,
                      batch_size=batch_size)
                return get_image_from_csv(data_path, is_aug,
                  input_bands=(self.input_bands),
                  output_bands=(self.output_bands),
                  image_size=image_size)
            else:
                raise Exception("Data load error,You should input a *.csv file")
        elif data_path.endswith(".csv"):
            if generate:
                return get_image_from_csv(data_path, is_aug,
                  input_bands=(self.input_bands),
                  output_bands=(self.output_bands),
                  image_size=image_size,
                  generate=generate,
                  batch_size=batch_size)
            return get_image_from_csv(data_path, is_aug,
              input_bands=(self.input_bands),
              output_bands=(self.output_bands),
              image_size=image_size)
        else:
            raise Exception("Data load error,You should input a *.csv file")
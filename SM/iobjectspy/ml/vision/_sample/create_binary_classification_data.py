# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_sample\create_binary_classification_data.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 19966 bytes
import json, os
from collections import OrderedDict
import numpy as np, rasterio
from iobjectspy._logger import log_info, log_error
from rasterio import features
from iobjectspy import Rectangle, clip
from iobjectspy.ml.toolkit._create_training_data_util import get_tile_start_index, _get_input_feature, _save_img
from iobjectspy.ml.toolkit._toolkit import save_pattle_png, save_config_to_yaml

class CreateBinaryClassificationData(object):

    def __init__(self, input_data, input_label, label_class_field, output_path, output_name, training_data_format, tile_format='jpg', tile_size_x=1024, tile_size_y=1024, tile_offset_x=512, tile_offset_y=512, tile_start_index=0, save_nolabel_tiles=False, **kwargs):
        self.input_data = input_data
        self.input_label = input_label
        self.label_class_field = label_class_field
        self.output_path = output_path
        self.output_name = output_name
        self.training_data_format = training_data_format
        self.tile_format = tile_format
        self.tile_size_x = tile_size_x
        self.tile_size_y = tile_size_y
        self.tile_offset_x = tile_offset_x
        self.tile_offset_y = tile_offset_y
        self.tile_start_index = tile_start_index
        self.save_nolabel_tiles = save_nolabel_tiles
        self.kwargs = kwargs

    def create_binary_classification(self):
        out_binary_sda = os.path.join(self.output_path, self.output_name, self.output_name + ".sda")
        output_path_images = os.path.join(self.output_path, self.output_name, "Images")
        output_path_masks = os.path.join(self.output_path, self.output_name, "Masks")
        if not os.path.exists(output_path_images):
            os.makedirs(output_path_images)
        if not os.path.exists(output_path_masks):
            os.makedirs(output_path_masks)
        temp_tile_index = get_tile_start_index(self.tile_start_index, out_binary_sda)
        temp_input_label = _get_input_feature(self.input_label)
        categorys = [
         "background"]
        if self.label_class_field is None:
            categorys.append("unspecified")
        else:
            try:
                for dlmc in temp_input_label:
                    category = dlmc.get_value(self.label_class_field)
                    if category not in categorys:
                        categorys.append(category)

            except:
                log_error("The category field is set and information cannot be queried from the\u3000category field，KeyError：{} ".format(self.label_class_field))

            for category in categorys:
                if category != "background":
                    positive_e_category = category

            categorys_dict = {}
            categorys_dict[positive_e_category] = 0
            categorys_count = {}
            categorys_count["background"] = 0
            categorys_count[positive_e_category] = 0
            with rasterio.open(self.input_data) as ds:
                transf = ds.transform
                rectangle = self.kwargs.get("rectangle")
                if rectangle is None:
                    rectangle = Rectangle(max(self.input_label.bounds.left, ds.bounds.left), max(self.input_label.bounds.bottom, ds.bounds.bottom), min(self.input_label.bounds.right, ds.bounds.right), min(self.input_label.bounds.top, ds.bounds.top))
                log_info("Training data boundary：".format(rectangle))
                rectangle_ymin, rectangle_xmin = rasterio.transform.rowcol(transf, rectangle.left, rectangle.top)
                rectangle_ymax, rectangle_xmax = rasterio.transform.rowcol(transf, rectangle.right, rectangle.bottom)
                width_block_num = int((rectangle_xmax - rectangle_xmin) // self.tile_size_x)
                height_block_num = int((rectangle_ymax - rectangle_ymin) // self.tile_size_y)
                for i in range(height_block_num):
                    for j in range(width_block_num):
                        block_xmin = rectangle_xmin + j * self.tile_size_x
                        block_ymin = rectangle_ymin + i * self.tile_size_y
                        coord_min = rasterio.transform.xy(transf, int(block_ymin), int(block_xmin))
                        coord_max = rasterio.transform.xy(transf, int(block_ymin + self.tile_size_y), int(block_xmin + self.tile_size_x))
                        coord_offset_min = rasterio.transform.xy(transf, int(block_ymin + self.tile_offset_y), int(block_xmin + self.tile_offset_x))
                        coord_offset_max = rasterio.transform.xy(transf, int(block_ymin + self.tile_offset_y + self.tile_size_y), int(block_xmin + self.tile_offset_x + self.tile_size_x))
                        tile_box = Rectangle(coord_min[0], coord_min[1], coord_max[0], coord_max[1])
                        recordset = self.input_label.query_with_bounds(tile_box, cursor_type="STATIC")
                        transf_tile = rasterio.transform.from_bounds(coord_min[0], coord_max[1], coord_max[0], coord_min[1], self.tile_size_x, self.tile_size_y)
                        feature_list = []
                        for feature in recordset.get_features():
                            clip_geometry = clip(feature.geometry, tile_box)
                            if clip_geometry is not None:
                                feature_geojson = json.loads(clip_geometry.to_geojson())
                                feature_list.append((feature_geojson, 1))

                        temp_tile_index, positive_e_pixel_count, negative_e_pixel_count = self._save_images_labels(ds, feature_list, transf_tile, block_xmin, block_ymin, temp_tile_index)
                        recordset.close()
                        if self.tile_offset_x != 0:
                            if j != width_block_num - 1:
                                tile_box = Rectangle(coord_offset_min[0], coord_min[1], coord_offset_max[0], coord_max[1])
                                recordset = self.input_label.query_with_bounds(tile_box, cursor_type="STATIC")
                                feature_list = []
                                for feature in recordset.get_features():
                                    clip_geometry = clip(feature.geometry, tile_box)
                                    if clip_geometry is not None:
                                        feature_geojson = json.loads(clip_geometry.to_geojson())
                                        feature_list.append((feature_geojson, 1))

                                transf_tile = rasterio.transform.from_bounds(coord_offset_min[0], coord_max[1], coord_offset_max[0], coord_min[1], self.tile_size_x, self.tile_size_y)
                                temp_tile_index, positive_e_pixel_count, negative_e_pixel_count = self._save_images_labels(ds, feature_list, transf_tile, block_xmin + self.tile_offset_x, block_ymin, temp_tile_index)
                                recordset.close()
                        if self.tile_offset_y != 0:
                            if i != height_block_num - 1:
                                tile_box = Rectangle(coord_min[0], coord_offset_min[1], coord_max[0], coord_offset_max[1])
                                recordset = self.input_label.query_with_bounds(tile_box, cursor_type="STATIC")
                                feature_list = []
                                for feature in recordset.get_features():
                                    clip_geometry = clip(feature.geometry, tile_box)
                                    if clip_geometry is not None:
                                        feature_geojson = json.loads(clip_geometry.to_geojson())
                                        feature_list.append((feature_geojson, 1))

                                transf_tile = rasterio.transform.from_bounds(coord_min[0], coord_offset_max[1], coord_max[0], coord_offset_min[1], self.tile_size_x, self.tile_size_y)
                                temp_tile_index, positive_e_pixel_count, negative_e_pixel_count = self._save_images_labels(ds, feature_list, transf_tile, block_xmin, block_ymin + self.tile_offset_y, temp_tile_index)
                                recordset.close()
                        if self.tile_offset_x != 0 and self.tile_offset_y != 0:
                            if (i != height_block_num - 1) & (j != width_block_num - 1):
                                tile_box = Rectangle(coord_offset_min[0], coord_offset_min[1], coord_offset_max[0], coord_offset_max[1])
                                recordset = self.input_label.query_with_bounds(tile_box, cursor_type="STATIC")
                                feature_list = []
                                for feature in recordset.get_features():
                                    clip_geometry = clip(feature.geometry, tile_box)
                                    if clip_geometry is not None:
                                        feature_geojson = json.loads(clip_geometry.to_geojson())
                                        feature_list.append((feature_geojson, 1))

                                transf_tile = rasterio.transform.from_bounds(coord_offset_min[0], coord_offset_max[1], coord_offset_max[0], coord_offset_min[1], self.tile_size_x, self.tile_size_y)
                                temp_tile_index, positive_e_pixel_count, negative_e_pixel_count = self._save_images_labels(ds, feature_list, transf_tile, block_xmin + self.tile_offset_x, block_ymin + self.tile_offset_y, temp_tile_index)
                                recordset.close()
                        categorys_count["background"] = categorys_count["background"] + negative_e_pixel_count
                        categorys_count[positive_e_category] = categorys_count[positive_e_category] + positive_e_pixel_count

                list_class_type = []
                negative_e_count = int(categorys_count["background"])
                positive_e_count = int(categorys_count[positive_e_category])
                positive_e_dict = OrderedDict({'class_name': '"background"', 
                 'class_value': 0, 'pixel_count': negative_e_count, 
                 'class_color': (0, 0, 0)})
                negative_e_dict = OrderedDict({'class_name': positive_e_category, 
                 'class_value': 1, 'pixel_count': positive_e_count, 
                 'class_color': (255, 0, 0)})
                list_class_type.append(positive_e_dict)
                list_class_type.append(negative_e_dict)
                if self.tile_format == "jpg":
                    x_ext = self.tile_format
                else:
                    if self.tile_format == "png":
                        x_ext = self.tile_format
                    else:
                        if self.tile_format == "tif":
                            x_ext = self.tile_format
                        else:
                            if self.tile_format == "origin":
                                x_ext = os.path.splitext(self.input_data)[-1][1[:None]]
                            dic_binary_sda = OrderedDict({"dataset": (OrderedDict({'name':"example_bc",  'data_type':"binary_classifition", 
                                         'x_bandnum':ds.count, 
                                         'x_ext':x_ext,  'x_type':ds.dtypes[0], 
                                         'y_bandnum':1,  'y_ext':"png",  'y_type':rasterio.uint8, 
                                         'tile_size':self.tile_size_x,  'image_mean':[
                                          115.6545965, 117.62014299, 106.01483799], 
                                         'image_std':[
                                          56.82521775, 53.46318049, 56.07113724], 
                                         'image_count':temp_tile_index, 
                                         'class_type':list_class_type}))})
                            save_config_to_yaml(dic_binary_sda, out_binary_sda)

    def _save_images_labels(self, ds, feature_list, transf_tile, block_xmin, block_ymin, temp_tile_index):
        """
        保存影像切片与标签

        :param DataSource ds  image数据源
        :param list feature_list  存储矢量对象的数组
        :param transf_tile tile的仿射变换值
        :param int block_xmin  tile左上方向x坐标
        :param int block_ymin  tile左上方向y坐标
        :param int temp_tile_index  记录tile的数量
        :return: temp_tile_index 记录tile的数量
        :rtype: int
        :return: positive_e_pixel_count 记录正例子像素数
        :rtype: int
        :return: negative_e_pixel_count 记录反例的像素数
        :rtype: int
        """
        start_index_string = str(temp_tile_index).zfill(8)
        output_path_images = os.path.join(self.output_path, self.output_name, "Images", start_index_string)
        output_path_masks = os.path.join(self.output_path, self.output_name, "Masks", start_index_string) + "." + "png"
        temp_tile_index = temp_tile_index
        positive_e_pixel_count = 0
        negative_e_pixel_count = 0
        if self.save_nolabel_tiles == False:
            if len(feature_list) > 0:
                _save_img(ds, self.tile_format, block_xmin, block_ymin, self.tile_size_x, self.tile_size_y, output_path_images, transf_tile, self.input_data)
                positive_e_pixel_count, negative_e_pixel_count = self._save_masks(feature_list, transf_tile, self.tile_size_x, self.tile_size_y, output_path_masks)
                temp_tile_index = temp_tile_index + 1
        else:
            _save_img(ds, self.tile_format, block_xmin, block_ymin, self.tile_size_x, self.tile_size_y, output_path_images, transf_tile, self.input_data)
            if len(feature_list) > 0:
                positive_e_pixel_count, negative_e_pixel_count = self._save_masks(feature_list, transf_tile, self.tile_size_x, self.tile_size_y, output_path_masks)
            else:
                positive_e_pixel_count, negative_e_pixel_count = self._save_nolabel_masks(self.tile_size_x, self.tile_size_y, output_path_masks)
            temp_tile_index = temp_tile_index + 1
        return (temp_tile_index, positive_e_pixel_count, negative_e_pixel_count)

    def _save_masks(self, feature_list, transf_tile, tile_size_x, tile_size_y, output_path_masks):
        """
        保存影像mask标签，feature_list需要有值

        :param list feature_list  存储矢量对象的数组
        :param transf_tile tile的仿射变换值
        :param str output_path_masks  输出mask的路径
        :return: positive_e_pixel_count 记录正例子像素数
        :rtype: int
        :return: negative_e_pixel_count 记录反例的像素数
        :rtype: int
        """
        image = features.rasterize(((g, 1) for g, v in feature_list), out_shape=(tile_size_y, tile_size_x), transform=transf_tile)
        positive_e_pixel_count = np.sum(image == 1)
        negative_e_pixel_count = np.sum(image == 0)
        color_codes = {(0, 0, 0):0, 
         (255, 0, 0):1}
        save_pattle_png(image, color_codes, output_path_masks)
        return (
         positive_e_pixel_count, negative_e_pixel_count)

    def _save_nolabel_masks(self, tile_size_x, tile_size_y, output_path_masks):
        """
        保存影像mask标签，标签中全是反例

        :param str output_path_masks  输出mask的路径
        :return: positive_e_pixel_count 记录正例子像素数
        :rtype: int
        :return: negative_e_pixel_count 记录反例的像素数
        :rtype: int
        """
        image = np.zeros((tile_size_x, tile_size_y))
        positive_e_pixel_count = np.sum(image == 1)
        negative_e_pixel_count = np.sum(image == 0)
        color_codes = {(0, 0, 0): 0}
        save_pattle_png(image, color_codes, output_path_masks)
        return (
         positive_e_pixel_count, negative_e_pixel_count)

# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_sample\create_secne_classification_data.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 17778 bytes
import csv, os
from collections import OrderedDict
import rasterio
from iobjectspy import Rectangle, clip
from iobjectspy._logger import log_info
from iobjectspy.ml.toolkit._create_training_data_util import get_tile_start_index, _get_input_feature, _save_img
from iobjectspy.ml.toolkit._toolkit import save_config_to_yaml, get_config_from_yaml

class CreateSceneClassificationData(object):

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

    def create_scene_classification(self):
        out_secne_sda = os.path.join(self.output_path, self.output_name, self.output_name + ".sda")
        out_scene_csv = os.path.join(self.output_path, self.output_name, "scene_classification.csv")
        temp_tile_index = get_tile_start_index(self.tile_start_index, out_secne_sda)
        temp_input_label = _get_input_feature(self.input_label)
        categorys = []
        try:
            config = get_config_from_yaml(out_secne_sda)
            for temp_class_type in config.get("dataset").get("class_type"):
                categorys.append(temp_class_type.get("class_name"))

            log_info("Get {} from sda file ".format(categorys))
        except:
            log_info("Initialization category")

        for dlmc in temp_input_label:
            category = dlmc.get_value(self.label_class_field)
            if category not in categorys:
                categorys.append(category)

        categorys_dict = {}
        id_category = 0
        try:
            config = get_config_from_yaml(out_secne_sda)
            for temp_class_type in config.get("dataset").get("class_type"):
                categorys_dict[temp_class_type.get("class_name")] = temp_class_type.get("class_id")

            log_info("Get {} from sda file ".format(categorys_dict))
        except:
            log_info("Initialization categorys_dict")

        for category in categorys:
            if category not in categorys_dict.keys():
                categorys_dict[category] = id_category
            id_category = id_category + 1

        categorys_count = {}
        try:
            config = get_config_from_yaml(out_secne_sda)
            for temp_class_type in config.get("dataset").get("class_type"):
                categorys_count[temp_class_type.get("class_name")] = temp_class_type.get("image_count")

            log_info("Get {} from sda file ".format(categorys_dict))
        except:
            log_info("Initialization categorys_dict")

        for category in categorys:
            if category not in categorys_count.keys():
                categorys_count[category] = 0

        for category in categorys:
            output_path = os.path.join(self.output_path, self.output_name, str(categorys_dict[category]))
            if not os.path.exists(output_path):
                os.makedirs(output_path)

        with rasterio.open(self.input_data) as ds:
            transf = ds.transform
            rectangle = self.kwargs.get("rectangle")
            if rectangle is None:
                rectangle = Rectangle(max(self.input_label.bounds.left, ds.bounds.left), max(self.input_label.bounds.bottom, ds.bounds.bottom), min(self.input_label.bounds.right, ds.bounds.right), min(self.input_label.bounds.top, ds.bounds.top))
            log_info("Training data boundary：".format(rectangle))
            rectangle_ymin, rectangle_xmin = rasterio.transform.rowcol(transf, rectangle.left, rectangle.top)
            rectangle_ymax, rectangle_xmax = rasterio.transform.rowcol(transf, rectangle.right, rectangle.bottom)
            with open(out_scene_csv, "a", newline="", encoding="utf8") as f:
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
                        if recordset.get_geometry() is not None:
                            temp_tile_index = self._save_images_labels(ds, recordset, tile_box, block_xmin, block_ymin, categorys_dict, transf_tile, categorys_count, temp_tile_index, f)
                        recordset.close()
                        if self.tile_offset_x != 0:
                            if j != width_block_num - 1:
                                tile_box = Rectangle(coord_offset_min[0], coord_min[1], coord_offset_max[0], coord_max[1])
                                recordset = self.input_label.query_with_bounds(tile_box, cursor_type="STATIC")
                                transf_tile = rasterio.transform.from_bounds(coord_offset_min[0], coord_max[1], coord_offset_max[0], coord_min[1], self.tile_size_x, self.tile_size_y)
                                if recordset.get_geometry() is not None:
                                    temp_tile_index = self._save_images_labels(ds, recordset, tile_box, block_xmin + self.tile_offset_x, block_ymin, categorys_dict, transf_tile, categorys_count, temp_tile_index, f)
                                recordset.close()
                        if self.tile_offset_y != 0 and i != height_block_num - 1:
                            tile_box = Rectangle(coord_min[0], coord_offset_min[1], coord_max[0], coord_offset_max[1])
                            recordset = self.input_label.query_with_bounds(tile_box, cursor_type="STATIC")
                            transf_tile = rasterio.transform.from_bounds(coord_min[0], coord_offset_max[1], coord_max[0], coord_offset_min[1], self.tile_size_x, self.tile_size_y)
                            if recordset.get_geometry() is not None:
                                temp_tile_index = self._save_images_labels(ds, recordset, tile_box, block_xmin, block_ymin + self.tile_offset_y, categorys_dict, transf_tile, categorys_count, temp_tile_index, f)
                                recordset.close()
                            if self.tile_offset_x != 0:
                                if self.tile_offset_y != 0 and (i != height_block_num - 1) & (j != width_block_num - 1):
                                    tile_box = Rectangle(coord_offset_min[0], coord_offset_min[1], coord_offset_max[0], coord_offset_max[1])
                                    recordset = self.input_label.query_with_bounds(tile_box, cursor_type="STATIC")
                                    transf_tile = rasterio.transform.from_bounds(coord_offset_min[0], coord_offset_max[1], coord_offset_max[0], coord_offset_min[1], self.tile_size_x, self.tile_size_y)
                                    if recordset.get_geometry() is not None:
                                        temp_tile_index = self._save_images_labels(ds, recordset, tile_box, block_xmin + self.tile_offset_x, block_ymin + self.tile_offset_y, categorys_dict, transf_tile, categorys_count, temp_tile_index, f)
                                recordset.close()

            list = []
            image_count = temp_tile_index
            for key in categorys_count:
                list.append({'class_name':key,  'class_id':categorys_dict[key], 
                 'image_count':categorys_count[key]})
                image_count = image_count + categorys_count[key]

            dic_scene_sda = OrderedDict({"dataset": (OrderedDict({'name':"example_scene",  'data_type':"scene_classification", 
                         'x_bandnum':ds.count, 
                         'x_ext':self.input_data.split(".")[-1],  'x_type':ds.dtypes[0], 
                         'image_count':temp_tile_index,  'tile_size':self.tile_size_y, 
                         'image_mean':[
                          115.6545965, 117.62014299, 106.01483799], 
                         'image_std':[
                          56.82521775, 53.46318049, 56.07113724], 
                         'image_list':"scene_classification.csv", 
                         'class_type':list}))})
            save_config_to_yaml(dic_scene_sda, out_secne_sda)

    def _save_images_labels(self, ds, recordset, tile_box, block_xmin, block_ymin, categorys_dict, transf_tile, categorys_count, temp_tile_index, f):
        """
       保存影像切片与标签

       :param DataSource ds  image数据源
       :param RecordSet recordset  基于tile_box查询出的矢量记录集
       :param Rectangle tile_box  tile的矩形边界框
       :param int block_xmin  tile左上方向x坐标
       :param int block_ymin  tile左上方向y坐标
       :param dict categorys_dict 字典，保存类别与数字编号对应关系
       :param transf_tile tile的仿射变换值
       :param dict categorys_count  构建类别计数字典，记录每个类别tile数量
       :param int temp_tile_index  记录tile的数量
       :param f  csv文件
       :return: temp_tile_index 记录tile的数量
       :rtype: int
       """
        dict_categorys = {}
        for feature in recordset.get_features():
            if clip(feature.geometry, tile_box) is not None:
                category = feature.get_value(self.label_class_field)
                try:
                    dict_categorys[category] = dict_categorys[category] + clip(tile_box, feature.geometry).area
                except:
                    dict_categorys.update({category: (clip(tile_box, feature.geometry).area)})

        for dict_category in dict_categorys:
            if dict_categorys[dict_category] > 0.5 * (tile_box.height * tile_box.width):
                category = dict_category
                start_index_string = str(temp_tile_index).zfill(8)
                temp_tile_index = temp_tile_index + 1
                output_path = os.path.join(self.output_path, self.output_name, str(categorys_dict[category]), start_index_string)
                _save_img(ds, self.tile_format, block_xmin, block_ymin, self.tile_size_x, self.tile_size_y, output_path, transf_tile, self.input_data)
                categorys_count[category] = categorys_count[category] + 1
                if self.tile_format == "origin":
                    relative_output_path = "./" + str(categorys_dict[category]) + "/" + start_index_string + os.path.splitext(self.input_data)[-1]
                else:
                    relative_output_path = "./" + str(categorys_dict[category]) + "/" + start_index_string + "." + self.tile_format
                list = []
                list.append(relative_output_path)
                list.append(category)
                list.append(categorys_dict[category])
                f_csv = csv.writer(f)
                f_csv.writerow(list)

        return temp_tile_index

# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_sample\create_object_detection_data.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 23409 bytes
import os
from collections import OrderedDict
import rasterio
from iobjectspy import Rectangle
from iobjectspy._logger import log_info, log_error
from iobjectspy.ml.toolkit._create_training_data_util import _save_img, get_tile_start_index, _get_input_feature
from iobjectspy.ml.toolkit._toolkit import save_config_to_yaml, get_config_from_yaml

class CreateObjectDetectionData(object):

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

    def create_voc(self):
        output_path_img = os.path.join(self.output_path, self.output_name, "Images")
        output_path_label = os.path.join(self.output_path, self.output_name, "Annotations")
        output_path_main = os.path.join(self.output_path, self.output_name, "ImageSets", "Main")
        output_voc_sda = os.path.join(self.output_path, self.output_name, self.output_name + ".sda")
        if not os.path.exists(output_path_img):
            os.makedirs(output_path_img)
        if not os.path.exists(output_path_label):
            os.makedirs(output_path_label)
        if not os.path.exists(output_path_main):
            os.makedirs(output_path_main)
        temp_tile_index = get_tile_start_index(self.tile_start_index, output_voc_sda)
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
                    temp_input_label = recordset.get_features()
                    transf_tile = rasterio.transform.from_bounds(coord_min[0], coord_max[1], coord_max[0], coord_min[1], self.tile_size_x, self.tile_size_y)
                    temp_tile_index = self._save_images_labels(temp_input_label, ds, block_xmin, block_ymin, transf_tile, temp_tile_index)
                    recordset.close()
                    if self.tile_offset_x != 0:
                        if j != width_block_num - 1:
                            tile_box = Rectangle(coord_offset_min[0], coord_min[1], coord_offset_max[0], coord_max[1])
                            recordset = self.input_label.query_with_bounds(tile_box, cursor_type="STATIC")
                            temp_input_label = recordset.get_features()
                            transf_tile = rasterio.transform.from_bounds(coord_offset_min[0], coord_max[1], coord_offset_max[0], coord_min[1], self.tile_size_x, self.tile_size_y)
                            temp_tile_index = self._save_images_labels(temp_input_label, ds, block_xmin + self.tile_offset_x, block_ymin, transf_tile, temp_tile_index)
                            recordset.close()
                    if self.tile_offset_y != 0:
                        if i != height_block_num - 1:
                            tile_box = Rectangle(coord_min[0], coord_offset_min[1], coord_max[0], coord_offset_max[1])
                            recordset = self.input_label.query_with_bounds(tile_box, cursor_type="STATIC")
                            temp_input_label = recordset.get_features()
                            transf_tile = rasterio.transform.from_bounds(coord_min[0], coord_offset_max[1], coord_max[0], coord_offset_min[1], self.tile_size_x, self.tile_size_y)
                            temp_tile_index = self._save_images_labels(temp_input_label, ds, block_xmin, block_ymin + self.tile_offset_y, transf_tile, temp_tile_index)
                            recordset.close()
                        if self.tile_offset_x != 0 and self.tile_offset_y != 0 and (i != height_block_num - 1) & (j != width_block_num - 1):
                            tile_box = Rectangle(coord_offset_min[0], coord_offset_min[1], coord_offset_max[0], coord_offset_max[1])
                            recordset = self.input_label.query_with_bounds(tile_box, cursor_type="STATIC")
                            temp_input_label = recordset.get_features()
                            transf_tile = rasterio.transform.from_bounds(coord_offset_min[0], coord_offset_max[1], coord_offset_max[0], coord_offset_min[1], self.tile_size_x, self.tile_size_y)
                            temp_tile_index = self._save_images_labels(temp_input_label, ds, block_xmin + self.tile_offset_x, block_ymin + self.tile_offset_y, transf_tile, temp_tile_index)
                            recordset.close()

            temp_input_label = _get_input_feature(self.input_label)
            try:
                config = get_config_from_yaml(output_voc_sda)
                log_info("Get the number of pixels of each category and color table information from  {} ".format(output_voc_sda))
                categorys = config.dataset.get("classes")
                for i in temp_input_label:
                    category = i.get_value(self.label_class_field)
                    if category not in categorys:
                        categorys.append(category)

            except:
                categorys = [
                 "__background__"]
                if self.label_class_field is None:
                    categorys.append("unspecified")
                else:
                    try:
                        for i in temp_input_label:
                            category = i.get_value(self.label_class_field)
                            if category not in categorys:
                                categorys.append(category)

                    except:
                        log_error("The category field is set and information cannot be queried from the\u3000category field，KeyError：{} ".format(self.label_class_field))

            dic_voc_yml = OrderedDict({"dataset": (OrderedDict({'name':"example_voc",  'classes':categorys, 
                         'image_count':temp_tile_index, 
                         'data_type':"voc", 
                         'input_bandnum':ds.count, 
                         'input_ext':ds.dtypes[0],  'x_ext':self.input_data.split(".")[-1], 
                         'tile_size_x':self.tile_size_x, 
                         'tile_size_y':self.tile_size_y, 
                         'tile_offset_x':self.tile_offset_x, 
                         'tile_offset_y':self.tile_offset_y, 
                         'image_mean':[
                          115.6545965, 117.62014299, 106.01483799], 
                         'image_std':[
                          56.82521775, 53.46318049, 56.07113724]}))})
            save_config_to_yaml(dic_voc_yml, output_voc_sda)
            self._save_index_file()
            print("train data saved to `{:s}`".format(os.path.join(self.output_path, self.output_name)))

    def _get_features_box(self, temp_input_label, block_xmin, block_ymin, transf):
        """
        计算 features_box ,存储像素坐标以及类别信息

        """
        features_box = []
        block_xmax = block_xmin + self.tile_size_x
        block_ymax = block_ymin + self.tile_size_y
        for feature_index in temp_input_label:
            if self.label_class_field is None:
                category = "unspecified"
            else:
                try:
                    category = feature_index.get_value(self.label_class_field)
                except:
                    log_error("The category field is set and information cannot be queried from the category\u3000field，KeyError：{} ".format(self.label_class_field))

                feature_xmin_geo = feature_index.geometry.bounds.left
                feature_xmax_geo = feature_index.geometry.bounds.right
                feature_ymin_geo = feature_index.geometry.bounds.bottom
                feature_ymax_geo = feature_index.geometry.bounds.top
                feature_ymax, feature_xmin = rasterio.transform.rowcol(transf, feature_xmin_geo, feature_ymin_geo)
                feature_ymin, feature_xmax = rasterio.transform.rowcol(transf, feature_xmax_geo, feature_ymax_geo)
                feature_half_length_x = abs(feature_xmax - feature_xmin) / 2
                feature_half_length_y = abs(feature_ymax - feature_ymin) / 2
                list_bbox = []
            if (feature_xmin >= block_xmin - feature_half_length_x) & (feature_xmax <= block_xmax + feature_half_length_x) & (feature_ymin >= block_ymin - feature_half_length_y) & (feature_ymax <= block_ymax + feature_half_length_y):
                if feature_xmin - block_xmin < 0:
                    xmin = 0
                else:
                    xmin = round(feature_xmin - block_xmin, 2)
                if feature_ymin - block_ymin < 0:
                    ymin = 0
                else:
                    ymin = round(feature_ymin - block_ymin, 2)
                if block_xmax - feature_xmax < 0:
                    xmax = block_xmax - block_xmin
                else:
                    xmax = round(feature_xmax - block_xmin, 2)
                if block_ymax - feature_ymax < 0:
                    ymax = block_ymax - block_ymin
                else:
                    ymax = round(feature_ymax - block_ymin, 2)
                if xmin < xmax - 2 and ymin < ymax - 2:
                    list_bbox.append(xmin)
                    list_bbox.append(ymin)
                    list_bbox.append(xmax)
                    list_bbox.append(ymax)
                    list_bbox.append(category)
                    list_bbox.append(0)
                    features_box.append(list_bbox)

        return features_box

    def _save_images_labels(self, temp_input_label, ds, block_xmin, block_ymin, transf_tile, temp_tile_index):
        """
        计算 features_box ,存储像素坐标以及类别信息

        """
        block_xmax = block_xmin + self.tile_size_x
        block_ymax = block_ymin + self.tile_size_y
        height = ds.height
        width = ds.width
        tile_size_x = self.tile_size_x
        tile_size_y = self.tile_size_y
        if height <= block_ymax:
            tile_size_y = height - block_ymin
        elif width <= block_xmax:
            tile_size_x = width - block_xmin
        else:
            start_index_string = str(temp_tile_index).zfill(8)
            transf = ds.transform
            output_path_img = os.path.join(self.output_path, self.output_name, "Images", start_index_string)
            output_path_label = os.path.join(self.output_path, self.output_name, "Annotations")
            features_box = self._get_features_box(temp_input_label, block_xmin, block_ymin, transf)
            if self.save_nolabel_tiles == False:
                if features_box:
                    _save_img(ds, self.tile_format, block_xmin, block_ymin, tile_size_x, tile_size_y, output_path_img, transf_tile, self.input_data)
                    if self.tile_format == "origin":
                        self._save_xml(output_path_label, features_box, tile_size_x, tile_size_y, start_index_string + "." + self.input_data.split(".")[-1], ds.count)
                    else:
                        self._save_xml(output_path_label, features_box, tile_size_x, tile_size_y, start_index_string + "." + self.tile_format, ds.count)
                    temp_tile_index = temp_tile_index + 1
            else:
                _save_img(ds, self.tile_format, block_xmin, block_ymin, tile_size_x, tile_size_y, output_path_img, transf_tile, self.input_data)
                if self.tile_format == "origin":
                    self._save_xml(output_path_label, features_box, tile_size_x, tile_size_y, start_index_string + "." + self.input_data.split(".")[-1], ds.count)
                else:
                    self._save_xml(output_path_label, features_box, tile_size_x, tile_size_y, start_index_string + "." + self.tile_format, ds.count)
            temp_tile_index = temp_tile_index + 1
        return temp_tile_index

    def _save_xml(self, output_path_label, lists, width, height, pic_name, depth):
        """
        生成xml描述文件

        :param output_path_label: 输入标签文件存储路径
        :type output_path_label: str
        :param lists: 包含bbox，category，difficult信息
        :type lists: list
        :param width: 图像宽度
        :type width: Long
        :param height: 图像高度
        :type height: Long
        :param pic_name: 对应标签文件的图片名称
        :type pic_name: str
        :param tile_format: 切片的图像格式:TIFF,PNG,JPG
        :type tile_format: str

        """
        if self.tile_format == "jpg" or self.tile_format == "png":
            depth = 3
        from lxml.etree import Element, SubElement, tostring
        node_root = Element("annotation")
        node_folder = SubElement(node_root, "folder")
        node_folder.text = "VOC"
        node_filename = SubElement(node_root, "filename")
        node_filename.text = pic_name
        node_size = SubElement(node_root, "size")
        node_width = SubElement(node_size, "width")
        node_width.text = "%s" % width
        node_height = SubElement(node_size, "height")
        node_height.text = "%s" % height
        node_depth = SubElement(node_size, "depth")
        node_depth.text = "%s" % depth
        node_segmented = SubElement(node_root, "segmented")
        node_segmented.text = "%s" % 0
        for list in lists:
            node_object = SubElement(node_root, "object")
            node_name = SubElement(node_object, "name")
            node_name.text = str(list[4])
            node_difficult = SubElement(node_object, "difficult")
            node_difficult.text = str(list[5])
            node_truncated = SubElement(node_object, "truncated")
            node_truncated.text = str(0)
            node_bndbox = SubElement(node_object, "bndbox")
            node_xmin = SubElement(node_bndbox, "xmin")
            node_xmin.text = "%s" % list[0]
            node_ymin = SubElement(node_bndbox, "ymin")
            node_ymin.text = "%s" % list[1]
            node_xmax = SubElement(node_bndbox, "xmax")
            node_xmax.text = "%s" % list[2]
            node_ymax = SubElement(node_bndbox, "ymax")
            node_ymax.text = "%s" % list[3]

        xml = tostring(node_root, pretty_print=True, encoding="UTF-8")
        save_xml = os.path.join(output_path_label, pic_name.split(".")[0] + ".xml")
        with open(save_xml, "wb") as f:
            f.write(xml)

    def _save_index_file(self):
        """
        将数据划分为训练集、测试集、验证集

        """
        output_path_img = os.path.join(self.output_path, self.output_name, "Images")
        output_path_main = os.path.join(self.output_path, self.output_name, "ImageSets", "Main")
        pic_names = os.listdir(output_path_img)
        train_length = int(len(pic_names) / 5 * 4)
        val_length = int(len(pic_names) / 10)
        list_train = pic_names[0[:train_length]]
        list_val = pic_names[train_length[:train_length + val_length]]
        list_test = pic_names[(train_length + val_length)[:None]]
        list_trainval = list_train + list_val
        train_txt = open(os.path.join(output_path_main, "train.txt"), "w")
        val_txt = open(os.path.join(output_path_main, "val.txt"), "w")
        test_txt = open(os.path.join(output_path_main, "test.txt"), "w")
        trainval_txt = open(os.path.join(output_path_main, "trainval.txt"), "w")
        for pic_name in list_train:
            label_name = pic_name.split(".")[0]
            train_txt.write(label_name + "\n")

        for pic_name in list_val:
            label_name = pic_name.split(".")[0]
            val_txt.write(label_name + "\n")

        for pic_name in list_test:
            label_name = pic_name.split(".")[0]
            test_txt.write(label_name + "\n")

        for pic_name in list_trainval:
            label_name = pic_name.split(".")[0]
            trainval_txt.write(label_name + "\n")

        train_txt.close()
        val_txt.close()
        test_txt.close()
        trainval_txt.close()

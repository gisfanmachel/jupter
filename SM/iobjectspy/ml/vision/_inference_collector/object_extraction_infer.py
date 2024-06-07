# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_inference_collector\object_extraction_infer.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 2988 bytes
import os
from _models.instance_segmentation.prediction_instance_seg import Mask_Rcnn_Prediction
from toolkit._toolkit import get_config_from_yaml

class ObjectExtraction:

    def __init__(self, model_path):
        self.config = get_config_from_yaml(model_path)
        self.model_path = os.path.abspath(os.path.join(model_path, os.path.pardir))
        self.model = None
        self.load_model()

    def load_model(self):
        func_str = "self." + self.config.model_architecture + "_" + self.config.framework + "_load_model"
        result = eval(func_str)()

    def close_model(self):
        self.model.close_model()

    def maskrcnn_keras_load_model(self):
        self.model = Mask_Rcnn_Prediction(self.model_path)

    def infer(self, input_data, out_data, out_dataset_name, score_thresh, nms_thresh, return_bbox):
        """
        根据func_str拼接字符串自动执行各个网络的函数
        :return:
        """
        if out_dataset_name is None:
            out_dataset_name = self.config.model_type + "_" + self.config.model_categorys
        func_str = "self." + self.config.model_architecture + "_" + self.config.framework
        result = eval(func_str)(input_data, out_data, out_dataset_name, score_thresh, nms_thresh, return_bbox)
        print("The Object Extraction have done!")
        return result

    def infer_pic(self, input_data, image_path_list, output_data_path, out_dataset_name, score_thresh, nms_thresh):
        """
        根据func_str拼接字符串自动执行各个网络的函数
        :return:
        """
        if out_dataset_name is None:
            out_dataset_name = self.config.model_type + "_" + self.config.model_categorys
        func_str = "self." + self.config.model_architecture + "_" + self.config.framework + "_pic"
        result = eval(func_str)(input_data, image_path_list, output_data_path, out_dataset_name, score_thresh, nms_thresh)
        print("The Object Extraction have done!")
        return result

    def maskrcnn_keras(self, *args):
        input_data, output_data_path, out_dataset_name, score_thresh, nms_thresh, return_bbox = args
        return self.model.infer_geo_image(input_data, self.config, output_data_path, out_dataset_name, score_thresh, nms_thresh, return_bbox)

    def maskrcnn_keras_pic(self, *args):
        input_data, image_path_list, output_data_path, out_dataset_name, score_thresh, nms_thresh = args
        return self.model.infer_pic_dir(image_path_list, input_data, self.config, output_data_path, out_dataset_name, score_thresh, nms_thresh)

# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_inference_collector\multi_classification_infer.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 4507 bytes
"""
@author: YangRuijie
@license: 
@contact: yangruijie@supermap.com
@software: 
@file: multi_classidication.py
@time: 8/19/19 5:48 AM
@desc:
"""
import os
from iobjectspy.ml.vision._models.semantic_seg.fpn_torch import FpnEstimation
from _models.semantic_seg.deeplabv3plus_torch import Deeplabv3PlusEstimation
from _models.semantic_seg.unet import UnetEstimation
from toolkit._toolkit import get_config_from_yaml

class MultiClassification:

    def __init__(self, input_data, model_path, out_data, out_dataset_name, offset, result_type, **kwargs):
        self.model_path = os.path.abspath(os.path.join(model_path, os.path.pardir))
        self.config = get_config_from_yaml(model_path)
        self.input_data = input_data
        self.out_data = out_data
        self.out_dataset_name = out_dataset_name
        self.offset = offset
        self.result_type = result_type
        self.kwargs = kwargs

    def infer(self):
        """
        根据func_str拼接字符串自动执行各个网络的函数
        :return:
        """
        if self.out_dataset_name is None:
            self.out_dataset_name = self.config.model_type + "_" + self.config.model_categorys
        func_str = "self." + self.config.model_architecture + "_" + self.config.framework + "_" + self.result_type
        result = eval(func_str)()
        print("The multi classification have done!")
        return result

    def deeplabv3plus_pytorch_grid(self):
        return (Deeplabv3PlusEstimation(self.model_path, self.config).estimate_img)((self.input_data), (self.offset), 
         (self.out_data), 
         (self.out_dataset_name), 
         (self.result_type), **self.kwargs)

    def fpn_pytorch_grid(self):
        return (FpnEstimation(self.model_path, self.config).estimate_img)((self.input_data), (self.offset), 
         (self.out_data), 
         (self.out_dataset_name), 
         (self.result_type), **self.kwargs)

    def unet_keras_region(self):
        return (UnetEstimation(self.model_path, self.config).estimate_img)((self.input_data), (self.offset), (self.out_data), 
         (self.out_dataset_name), (self.result_type), **self.kwargs)

    def unet_keras_grid(self):
        return (UnetEstimation(self.model_path, self.config).estimate_img)((self.input_data), (self.offset), (self.out_data), 
         (self.out_dataset_name), (self.result_type), **self.kwargs)


class MultiClassificationWithTile:

    def __init__(self, model_path, **kwargs):
        """
        使用numpy进行地物提取,输入和输出都为图像数组
        :param model_path: 模型路径
        :param config: 配置文件路径
        :param kwargs:
        """
        self.model_path = os.path.abspath(os.path.join(model_path, os.path.pardir))
        self.config = get_config_from_yaml(model_path)
        self.kwargs = kwargs
        self.estimation = None
        self.load_model()

    def load_model(self):
        func_str = "self." + self.config.model_architecture + "_" + self.config.framework + "_load_model"
        return eval(func_str)()

    def infer_tile(self, image_data):
        func_str = "self." + self.config.model_architecture + "_" + self.config.framework + "_tile"
        return eval(func_str)(image_data)

    def unet_keras_tile(self, image_data):
        return (self.estimation.estimate_tile)(image_data, **self.kwargs)

    def unet_keras_load_model(self):
        self.estimation = UnetEstimation(self.model_path, self.config)

    def close_model(self):
        self.estimation.close_model()

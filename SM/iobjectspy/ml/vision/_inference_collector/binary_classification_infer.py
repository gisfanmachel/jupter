# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_inference_collector\binary_classification_infer.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 5098 bytes
import os
from _models.semantic_seg.deeplabv3plus_torch import Deeplabv3PlusEstimation
from _models.semantic_seg.fpn_torch import FpnEstimation
from _models.dlinknet import DlinknetEstimationTf
from _models.semantic_seg.unet import UnetEstimation
from toolkit._toolkit import get_config_from_yaml

class BinaryClassification:

    def __init__(self, model_path, **kwargs):
        self.model_path = os.path.abspath(os.path.join(model_path, os.path.pardir))
        self.config = get_config_from_yaml(model_path)
        self.estimation = None
        self.model_kwargs = kwargs
        self.load_model()

    def load_model(self):
        """
        根据func_str拼接字符串自动执行各个网络的模型加载函数
        :return:
        """
        func_str = "self._" + self.config.model_architecture + "_" + self.config.framework + "_load_model"
        return eval(func_str)()

    def infer(self, input_data, out_data, out_dataset_name, offset, result_type, **kwargs):
        """
        根据self.estimation执行对应的影像预测函数estimate_img
        :return:
        """
        if out_dataset_name is None:
            out_dataset_name = self.config.model_type + "_" + self.config.model_categorys
        result = (self.estimation.estimate_img)(input_data, offset, out_data, 
         out_dataset_name, result_type, **kwargs)
        print("The binary classification have done!")
        return result

    def _dlinknet_tensorflow_load_model(self):
        self.estimation = DlinknetEstimationTf(self.model_path, self.config)

    def _unet_keras_load_model(self):
        self.estimation = UnetEstimation(self.model_path, self.config)

    def _fpn_pytorch_load_model(self):
        self.estimation = FpnEstimation((self.model_path), (self.config), **self.model_kwargs)

    def _deeplabv3plus_pytorch_load_model(self):
        self.estimation = Deeplabv3PlusEstimation((self.model_path), (self.config), **self.model_kwargs)

    def close_model(self):
        self.estimation.close_model()


class BinaryClassificationWithTile:

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


class BinaryClassificationWithNumpy:

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
        self.estimation = UnetEstimation(self.model_path, self.config)

    def infer(self, image_data, offset):
        """
        根据func_str拼接字符串自动执行各个网络的函数
        :return:
        """
        func_str = "self." + self.config.model_architecture + "_" + self.config.framework + "_numpy"
        return eval(func_str)(image_data, offset)

    def infer_tile(self, image_data):
        """
        根据func_str拼接字符串自动执行各个网络的函数
        :return:
        """
        func_str = "self." + self.config.model_architecture + "_" + self.config.framework + "_tile"
        return eval(func_str)(image_data)

    def unet_keras_numpy(self, image_data, offset):
        """
        使用numpy进行地物提取,输入和输出都为图像数组
        :return:
        """
        return (self.estimation.estimate_numpy)(image_data, offset, **self.kwargs)

    def unet_keras_tile(self, image_data):
        """
        使用numpy进行地物提取,输入和输出都为图像数组
        :return:
        """
        return (self.estimation.estimate_tile)(image_data, **self.kwargs)

    def close_model(self):
        self.estimation.close_model()

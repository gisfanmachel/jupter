# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_inference_collector\image_classification_infer.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 1949 bytes
import os
from _models.image_classification import ClassificationEstimation
from toolkit._toolkit import get_config_from_yaml

class ImageClassification:

    def __init__(self, input_data, model_path, out_data, out_dataset_name, **kwargs):
        self.model_path = os.path.abspath(os.path.join(model_path, os.path.pardir))
        self.config = get_config_from_yaml(model_path)
        self.input_data = input_data
        self.out_data = out_data
        self.out_dataset_name = out_dataset_name
        self.kwargs = kwargs

    def infer(self):
        """
        根据func_str拼接字符串自动执行各个网络的函数
        :return:
        """
        func_str = "self." + self.config.model_architecture + "_" + self.config.framework
        result = eval(func_str)()
        print("The image classification have done!")
        return result

    def cnn_keras(self):
        return ClassificationEstimation(self.model_path, self.config).estimate_img(self.input_data, self.out_data, self.out_dataset_name)


class ImageClassificationSingle:

    def __init__(self, model_path, **kwargs):
        self.model_path = os.path.abspath(os.path.join(model_path, os.path.pardir))
        self.config = get_config_from_yaml(model_path)
        self.kwargs = kwargs
        self.load_model()

    def infer(self, input_data):
        """
        根据func_str拼接字符串自动执行各个网络的函数
        :return:
        """
        func_str = "self." + self.config.model_architecture + "_" + self.config.framework
        eval(func_str)(input_data)

    def cnn_keras(self, input_data):
        pass

    def load_model(self):
        """
        根据func_str拼接字符串自动加载各个网络的模型
        :return:
        """
        func_str = "self." + self.config.model_architecture + "_" + self.config.framework + "_load_model"
        eval(func_str)()

    def cnn_keras_load_model(self):
        pass

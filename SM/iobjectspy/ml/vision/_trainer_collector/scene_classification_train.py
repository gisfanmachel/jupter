# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_trainer_collector\scene_classification_train.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 2021 bytes
"""
@author: YangRuijie
@license: 
@contact: yangruijie@supermap.com
@software: 
@file: scene_classification_train.py
@time: 7/16/19 9:03 AM
@desc:
"""
from _models.scene_classification import ClassificationTrainer
from toolkit._toolkit import get_config_from_yaml

class SceneClassification:

    def __init__(self, train_data_path, config, epoch, batch_size, lr, output_model_path, output_model_name, log_path, backbone_name, backbone_weight_path, reload_model, pretrained_model_path):
        self.train_data_path = train_data_path
        self.config = get_config_from_yaml(config)
        self.epoch = epoch
        self.batch_size = batch_size
        self.lr = lr
        self.output_model_path = output_model_path
        self.output_model_name = output_model_name
        self.log_path = log_path
        self.backbone_name = backbone_name
        self.backbone_weight_path = backbone_weight_path
        self.reload_model = reload_model
        self.pretrained_model_path = pretrained_model_path

    def train(self):
        """
        根据func_str拼接字符串自动执行各个网络的函数
        :return:
        """
        func_str = "self." + self.config.model.name + "_" + self.config.framework.name
        eval(func_str)()

    def image_classification_keras(self):
        ClassificationTrainer().train((self.train_data_path), (self.config), epoch=(self.epoch), batch_size=(self.batch_size), lr=(self.lr),
          output_model_path=(self.output_model_path),
          output_model_name=(self.output_model_name),
          log_path=(self.log_path),
          backbone_name=(self.backbone_name),
          backbone_weight_path=(self.backbone_weight_path),
          reload_model=(self.reload_model),
          pretrained_model_path=(self.pretrained_model_path))

# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\spacetime\_trainer_collector\graph_st_regression_train.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 1490 bytes
import os
from _models.torch_st_regression import GraphSTRegressionTrainer
from _models.dcrnn.lib.utils import read_yaml, write_yaml
from pathlib import Path

class GraphSTRegression:

    def __init__(self, train_data_path, config, epoch=5, batch_size=1, lr=0.01, output_model_path=None, checkpoint_filename=None):
        self.train_data_path = train_data_path
        self.out_model_path = output_model_path
        self.checkpoint_filename = checkpoint_filename
        self.config = config
        self.epoch = epoch
        self.batch_size = batch_size
        self.lr = lr
        self._config = read_yaml(Path(config))

    def train(self):
        """train.
        根据func_str拼接字符串自动执行各个网络的函数
        :return:
        """
        func_str = "self." + self._config.model.name + "_" + self._config.framework.name
        eval(func_str)()

    def dcrnn_pytorch(self):
        trainer = GraphSTRegressionTrainer(self.train_data_path, self.config, self.out_model_path, self.epoch, self.batch_size, self.lr, self.checkpoint_filename)
        trainer.train()

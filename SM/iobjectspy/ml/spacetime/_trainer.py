# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\spacetime\_trainer.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 1932 bytes
from iobjectspy._jsuperpy._utils import check_lic
from ._trainer_collector import GraphSTRegression

class Trainer:

    def __init__(self, train_data_path, config, epochs=5, batch_size=1, lr=0.01, output_model_path=None, checkpoint_filename=None, **kwargs):
        """
        图时空深度学习训练功能入口

        :param train_data_path: 训练数据路径
        :type train_data_path: str
        :param config: 配置文件路径
        :type config: str
        """
        self.train_data_path = train_data_path
        self.config = config
        if epochs is not None and isinstance(epochs, int):
            self.epochs = epochs
        else:
            self.epochs = 5
            print("[WARNING] {epochs} is not valid for parameter epochs".format(epochs))
        if batch_size is not None and isinstance(batch_size, int):
            self.batch_size = batch_size
        else:
            self.batch_size = 1
            print("[WARNING] {batch_size} is not valid for parameter for batch_size".format(batch_size))
        if lr is not None:
            self.lr = lr
        else:
            self.lr = 0.01
            print("[WARNING] {lr} is not valid for parameter for learning rate".format(lr))
        self.output_model_path = output_model_path
        self.checkpoint_filename = checkpoint_filename
        self.kwargs = kwargs
        check_lic()

    def graphst_regression_train(self):
        """
        图时空深度学习训练功能

        生成模型将存储在输入的 ‘output_model_path’ 路径下

        :return: None
        """
        GraphSTRegression(self.train_data_path, self.config, self.epochs, self.batch_size, self.lr, self.output_model_path, self.checkpoint_filename).train()

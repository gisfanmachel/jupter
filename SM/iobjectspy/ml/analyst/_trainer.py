# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\analyst\_trainer.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 1294 bytes
from iobjectspy._jsuperpy._utils import check_lic
from _tabular.classification import ClsTrainer

class Trainer:

    def __init__(self, train_data_path, config, lr, output_model_path, output_model_name, model_kwargs=None, **kwargs):
        """
        表格数据训练入口

        :param train_data_path: 训练数据路径
        :param config: 训练配置文件
        :param lr: 学习率
        :param output_model_path: 输出模型路径
        :param output_model_name: 输出模型名字
        :param model_kwargs: 模型附加参数
        :param kwargs: 其他参数
        """
        self.train_data_path = train_data_path
        self.config = config
        self.lr = lr
        self.output_model_path = output_model_path
        self.output_model_name = output_model_name
        self.model_kwargs = model_kwargs
        self.kwargs = kwargs
        check_lic()

    def tabular_cls_train(self):
        """
        表格数据分类模型训练功能

        生成模型将存储在输入的 ‘output_model_path’ 路径下

        :return: None
        """
        (ClsTrainer().train)((self.train_data_path), (self.config), (self.lr), (self.output_model_path), (self.output_model_name), 
         (self.model_kwargs), **self.kwargs)

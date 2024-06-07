# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_trainer.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 13291 bytes
import sys, warnings
from iobjectspy._jsuperpy._utils import check_lic
from ._trainer_collector import BinaryClassification, ObjectDetection, SceneClassification, ImageClassification, ObjectExtraction

class Trainer:

    def __init__(self, train_data_path, config, epoch, batch_size, lr, output_model_path, output_model_name, backbone_name, backbone_weight_path=None, log_path='./', reload_model=False, pretrained_model_path=None, **kwargs):
        """
        图像数据模型训练功能入口，

        :param train_data_path: 训练数据路径
        :type train_data_path: str
        :param config: 配置文件路径
        :type config: str
        :param epoch: 迭代次数
        :type epoch: int
        :param batch_size: 批数据大小
        :type batch_size: int
        :param lr: 学习率
        :type lr: float
        :param output_model_path: 输出模型文件路径
        :type output_model_path: str
        :param output_model_name: 输出模型的文件名
        :type output_model_name: str
        :param backbone_name: 主干网络名
        :type backbone_name: str
        :param backbone_weight_path: 主干网络模型文件路径，若为None则随机初始化模型权重
        :type backbone_weight_path: str or None
        :param log_path: 日志及checkpoint输出路径
        :type log_path: str
        :param reload_model: 是否重载之前训练的checkpoint模型
        :type  reload_model: bool
        :param pretrained_model_path: 预训练模型路径（可选）
        :type pretrained_model_path: str or None
        """
        self.train_data_path = train_data_path
        self.config = config
        self.epoch = epoch
        self.batch_size = batch_size
        self.lr = lr
        self.output_model_path = output_model_path
        self.output_model_name = output_model_name
        self.backbone_name = backbone_name
        self.backbone_weight_path = backbone_weight_path
        self.log_path = log_path
        self.reload_model = reload_model
        self.pretrained_model_path = pretrained_model_path
        self.kwargs = kwargs
        check_lic()

    def object_detect_train(self):
        """
        目标检测模型训练功能

        生成模型将存储在输入的 ‘output_model_path’ 路径下

        :return: None
        """
        ObjectDetection(self.train_data_path, self.config, self.epoch, self.batch_size, self.lr, self.output_model_path, self.output_model_name, self.log_path, self.backbone_name, self.backbone_weight_path, self.reload_model, self.pretrained_model_path).train()

    def binary_classify_train(self):
        """
        二元分类模型训练功能

        生成模型将存储在输入的 ‘output_model_path’ 路径下

        :return: None
        """
        BinaryClassification((self.train_data_path), (self.config), (self.epoch), (self.batch_size), (self.lr), 
         (self.output_model_path), (self.output_model_name), (self.log_path), (self.backbone_name), 
         (self.backbone_weight_path), (self.reload_model), (self.pretrained_model_path), **self.kwargs).train()

    def multi_classify_train(self):
        """
        地物分类训练功能

        生成模型将存储在输入的 ‘output_model_path’ 路径下

        :return: None
        """
        BinaryClassification((self.train_data_path), (self.config), (self.epoch), (self.batch_size), (self.lr), 
         (self.output_model_path), (self.output_model_name), (self.log_path), (self.backbone_name), 
         (self.backbone_weight_path), (self.reload_model), (self.pretrained_model_path), **self.kwargs).train()

    def scene_classify_train(self):
        """
        场景分类训练功能

        生成模型将存储在输入的 ‘output_model_path’ 路径下

        :return: None
        """
        SceneClassification(self.train_data_path, self.config, self.epoch, self.batch_size, self.lr, self.output_model_path, self.output_model_name, self.log_path, self.backbone_name, self.backbone_weight_path, self.reload_model, self.pretrained_model_path).train()

    def image_classify_train(self):
        """
        图片分类训练功能

        生成模型将存储在输入的 ‘output_model_path’ 路径下

        :return: None
        """
        ImageClassification(self.train_data_path, self.config, self.epoch, self.batch_size, self.lr, self.output_model_path, self.output_model_name, self.log_path, self.backbone_name, self.backbone_weight_path, self.reload_model, self.pretrained_model_path).train()

    def object_extract_train(self):
        """
        对象提取训练功能

        生成模型将存储在输入的 ‘output_model_path’ 路径下

        :return: None
        """
        ObjectExtraction(self.train_data_path, self.config, self.epoch, self.batch_size, self.lr, self.output_model_path, self.output_model_name, self.log_path, self.backbone_name, self.backbone_weight_path, self.reload_model, self.pretrained_model_path).train()


class _ImageryTrainer:

    def __init__(self, train_data_path, config, epoch, batch_size, lr, output_model_path, output_model_name, backbone_name, backbone_weight_path=None, log_path='./', reload_model=False, pretrained_model_path=None, **kwargs):
        """
        影像数据模型训练功能入口，

        :param train_data_path: 训练数据路径
        :type train_data_path: str
        :param config: 配置文件路径
        :type config: str
        :param epoch: 迭代次数
        :type epoch: int
        :param batch_size: 批数据大小
        :type batch_size: int
        :param lr: 学习率
        :type lr: float
        :param output_model_path: 输出模型文件路径
        :type output_model_path: str
        :param output_model_name: 输出模型的文件名
        :type output_model_name: str
        :param backbone_name: 主干网络名
        :type backbone_name: str
        :param backbone_weight_path: 主干网络模型文件路径，若为None则随机初始化模型权重
        :type backbone_weight_path: str or None
        :param log_path: 日志及checkpoint输出路径
        :type log_path: str
        :param reload_model: 是否重载之前训练的checkpoint模型
        :type  reload_model: bool
        :param pretrained_model_path: 预训练模型路径（可选）
        :type pretrained_model_path: str or None
        """
        check_lic()
        self.train_data_path = train_data_path
        self.config = config
        self.epoch = epoch
        self.batch_size = batch_size
        self.lr = lr
        self.output_model_path = output_model_path
        self.output_model_name = output_model_name
        self.backbone_name = backbone_name
        self.backbone_weight_path = backbone_weight_path
        self.log_path = log_path
        self.reload_model = reload_model
        self.pretrained_model_path = pretrained_model_path
        self.kwargs = kwargs

    def object_detect_train(self):
        """
        目标检测模型训练功能

        生成模型将存储在输入的 ‘output_model_path’ 路径下

        :return: None
        """
        ObjectDetection(self.train_data_path, self.config, self.epoch, self.batch_size, self.lr, self.output_model_path, self.output_model_name, self.log_path, self.backbone_name, self.backbone_weight_path, self.reload_model, self.pretrained_model_path).train()

    def binary_classify_train(self):
        """
        二元分类模型训练功能

        生成模型将存储在输入的 ‘output_model_path’ 路径下

        :return: None
        """
        BinaryClassification((self.train_data_path), (self.config), (self.epoch), (self.batch_size), (self.lr), 
         (self.output_model_path), (self.output_model_name), (self.log_path), (self.backbone_name), 
         (self.backbone_weight_path), (self.reload_model), (self.pretrained_model_path), **self.kwargs).train()

    def multi_classify_train(self):
        """
        地物分类训练功能

        生成模型将存储在输入的 ‘output_model_path’ 路径下

        :return: None
        """
        BinaryClassification(self.train_data_path, self.config, self.epoch, self.batch_size, self.lr, self.output_model_path, self.output_model_name, self.log_path, self.backbone_name, self.backbone_weight_path, self.reload_model, self.pretrained_model_path).train()

    def scene_classify_train(self):
        """
        场景分类训练功能

        生成模型将存储在输入的 ‘output_model_path’ 路径下

        :return: None
        """
        SceneClassification(self.train_data_path, self.config, self.epoch, self.batch_size, self.lr, self.output_model_path, self.output_model_name, self.log_path, self.backbone_name, self.backbone_weight_path, self.reload_model, self.pretrained_model_path).train()

    def object_extract_train(self):
        """
        对象提取训练功能

        生成模型将存储在输入的 ‘output_model_path’ 路径下

        :return: None
        """
        ObjectExtraction(self.train_data_path, self.config, self.epoch, self.batch_size, self.lr, self.output_model_path, self.output_model_name, self.log_path, self.backbone_name, self.backbone_weight_path, self.reload_model, self.pretrained_model_path).train()


class _PictureTrainer:

    def __init__(self, train_data_path, config, epoch, batch_size, lr, output_model_path, output_model_name, backbone_name, backbone_weight_path=None, log_path='./', reload_model=False, pretrained_model_path=None, **kwargs):
        """
        图片数据模型训练功能入口，

        :param train_data_path: 训练数据路径
        :type train_data_path: str
        :param config: 配置文件路径
        :type config: str
        :param epoch: 迭代次数
        :type epoch: int
        :param batch_size: 批数据大小
        :type batch_size: int
        :param lr: 学习率
        :type lr: float
        :param output_model_path: 输出模型文件路径
        :type output_model_path: str
        :param output_model_name: 输出模型的文件名
        :type output_model_name: str
        :param backbone_name: 主干网络名
        :type backbone_name: str
        :param backbone_weight_path: 主干网络模型文件路径，若为None则随机初始化模型权重
        :type backbone_weight_path: str or None
        :param log_path: 日志及checkpoint输出路径
        :type log_path: str
        :param reload_model: 是否重载之前训练的checkpoint模型
        :type  reload_model: bool
        :param pretrained_model_path: 预训练模型路径（可选）
        :type pretrained_model_path: str or None
        """
        check_lic()
        self.train_data_path = train_data_path
        self.config = config
        self.epoch = epoch
        self.batch_size = batch_size
        self.lr = lr
        self.output_model_path = output_model_path
        self.output_model_name = output_model_name
        self.backbone_name = backbone_name
        self.backbone_weight_path = backbone_weight_path
        self.log_path = log_path
        self.reload_model = reload_model
        self.pretrained_model_path = pretrained_model_path
        self.kwargs = kwargs

    def object_detect_train(self):
        """
        目标检测模型训练功能

        生成模型将存储在输入的 ‘output_model_path’ 路径下

        :return: None
        """
        ObjectDetection(self.train_data_path, self.config, self.epoch, self.batch_size, self.lr, self.output_model_path, self.output_model_name, self.log_path, self.backbone_name, self.backbone_weight_path, self.reload_model, self.pretrained_model_path).train()

    def picture_classify_train(self):
        """
        图片分类训练功能

        生成模型将存储在输入的 ‘output_model_path’ 路径下

        :return: None
        """
        ImageClassification(self.train_data_path, self.config, self.epoch, self.batch_size, self.lr, self.output_model_path, self.output_model_name, self.log_path, self.backbone_name, self.backbone_weight_path, self.reload_model, self.pretrained_model_path).train()

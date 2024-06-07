# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_torch_models\geo_api\train_api.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 13221 bytes
"""
@author: YangRuijie
@license: 
@contact: yangruijie@supermap.com
@software: 
@file: train_api.py
@time: 12/23/19 2:07 PM
@desc:
"""
import copy, os
import os.path as osp
import platform, warnings
from collections import OrderedDict
import torch, numpy as np
from ..encoders import get_preprocessing_fn
from ._toolkit import get_training_augmentation, get_preprocessing, get_validation_augmentation
from .cus_dataloader import FastDataLoader
from .dataset import SdaDataset
from util.losses import get_loss
from util.metrics import IoU
from util.ranger import Ranger, RangerVA, RangerQH
from util.train import TrainEpoch, ValidEpoch
from ......._logger import log_error, log_warning, log_info
from toolkit._toolkit import get_config_from_yaml, save_config_to_yaml, split_train_val_withdirs
from .base import BaseTorchTrainer

class SegTorchTrainer(BaseTorchTrainer):

    def __init__(self):
        super().__init__()

    def train(self, train_data_path, config, epoch=1, batch_size=1, lr=0.001, output_model_path='./', output_model_name='fpn', log_path=None, backbone_name='resnext50', backbone_weight_path=None, reload_model=False, pretrained_model_path=None, **kwargs):
        """

        :param train_data_path:
        :param config:
        :param epoch:
        :param batch_size:
        :param lr:
        :param output_model_path:
        :param output_model_name:
        :param log_path:
        :param backbone_name:
        :param backbone_weight_path:
        :param reload_model:
        :param pretrained_model_path:
        :param kwargs:
        :return:
        """
        self.config = config
        self.train_data_path = train_data_path
        self.sda_path = os.path.join(self.train_data_path, os.path.basename(self.train_data_path) + ".sda")
        self.data_config = get_config_from_yaml(self.sda_path)
        self.data_type = self.data_config.dataset.data_type
        if not self.data_type in ('multi_classification', 'binary_classifition'):
            raise AssertionError("data_type should be multi_classification or binary_classifition ")
        else:
            self.class_type = self.data_config.dataset.class_type
            self.tile_size = self.data_config.dataset.tile_size
            pixel_counts = np.array([c.pixel_count for c in self.class_type])
            self.class_weight = list(pixel_counts.sum(dtype=(np.float64)) / pixel_counts.shape[0] / (pixel_counts + 1.0))
            if self.data_type.strip() == "multi_classification":
                self.output_bands = len(self.class_type)
            else:
                if self.data_type.strip() == "binary_classifition":
                    self.output_bands = 1
                else:
                    log_error("data_type should be multi_classification or binary_classifition")
                    raise Exception("data_type should be multi_classification or binary_classifition")
            self.model_type = self.data_type
            self.input_bands = self.data_config.dataset.x_bandnum
            if not self.input_bands >= 1:
                raise AssertionError("输入波段数应大于等于1")
            else:
                if not self.output_bands >= 1:
                    raise AssertionError("输出波段数应大于等于1")
                else:
                    self.backbone_name = backbone_name
                    if self.backbone_name is None or self.backbone_name.strip() == "":
                        self.backbone_name = self.config.model.backbone_name
                        log_warning("backbone_name 为空,将使用默认 backbone_name : {}".format(self.backbone_name))
                    else:
                        self.config = config
                        self.epoch = epoch
                        self.batch_size = batch_size
                        self.lr = lr
                        self.output_model_path = output_model_path
                        self.output_model_name = output_model_name
                        self.backbone_weight_path = backbone_weight_path
                        self.pretrained_model_path = pretrained_model_path
                        self.log_path = log_path
                        self.reload_model = reload_model
                        self.optimizer = kwargs.get("optimizer") if kwargs.get("optimizer") is not None else self.config.trainer.optimizer
                        self.init_callbacks(log_path)
                        self.config.trainer.num_epochs = epoch
                        self.config.trainer.batch_size = batch_size
                        self.config.trainer.learning_rate = lr
                        os.environ["CUDA_VISIBLE_DEVICES"] = ",".join(map(str, kwargs.get("gpus"))) if kwargs.get("gpus") else "0"
                        if kwargs.get("device") is None:
                            device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
                        else:
                            device = torch.device(kwargs.get("device"))
                    self.output_model_path = osp.join(self.output_model_path, self.output_model_name)
                    file_num = 1
                    origin_output_model_path = self.output_model_path
                    while os.path.exists(self.output_model_path):
                        self.output_model_path = origin_output_model_path + ("_" + str(file_num))
                        file_num += 1

                    osp.exists(self.output_model_path) or os.makedirs(self.output_model_path)
                self.model_base_name = osp.basename(self.output_model_path.rstrip(osp.sep))
                self.torch_model_path = osp.join(self.output_model_path, self.model_base_name + ".pth")
                self.sdm_path = osp.join(self.output_model_path, self.model_base_name + ".sdm")
                data_config = self.data_config
                self.model_type = data_config.dataset.data_type
                self.class_type = data_config.dataset.class_type
                self.tile_size = data_config.dataset.tile_size
                self.model_input = [
                 (
                  data_config.dataset.x_bandnum, self.tile_size, self.tile_size)]
                self.model_output = [(len(self.class_type) if len(self.class_type) > 2 else 1, self.tile_size, self.tile_size)]
                self.encoder = backbone_name
                self.encoder_weights = kwargs.get("encoder_weights") if kwargs.get("encoder_weights") is not None else "imagenet"
                if not backbone_weight_path is not None:
                    if pretrained_model_path is not None:
                        self.encoder_weights = None
                    self.activation = "sigmoid" if kwargs.get("activation") is None else kwargs.get("activation")
                    self.cuda_count = torch.cuda.device_count()
                    self.data_works = self.cuda_count * 2 + 1 if kwargs.get("data_works") is None else kwargs.get("data_works")
                    if kwargs.get("loss_type") is not None:
                        self.loss_type = kwargs.get("loss_type")
                elif len(self.class_type) > 2:
                    self.loss_type = "crossentropyloss"
                else:
                    self.loss_type = "dice_loss+bce_loss"
        model = self.get_model()
        model_clone = copy.deepcopy(model)
        if backbone_weight_path is not None:
            model.encoder.load_state_dict(torch.load(backbone_weight_path))
        elif pretrained_model_path:
            model.load_state_dict(torch.load(pretrained_model_path.replace(".sdm", ".pth")).state_dict())
        elif torch.cuda.device_count() > 1 and kwargs.get("gpus") is not None:
            if len(kwargs.get("gpus")) > 1:
                model = torch.nn.DataParallel(model)
            else:
                model_params = model.parameters()
                self._init_data()
                if self.encoder_weights is None:
                    warnings.warn("encoder_weights 为None，将使用imagenet权重对数据的预处理方式处理数据")
                    preprocessing_fn = get_preprocessing_fn(self.encoder, "imagenet")
                else:
                    preprocessing_fn = get_preprocessing_fn(self.encoder, self.encoder_weights)
            train_dataset = SdaDataset((self.sda_path),
              "train",
              augmentation=(get_training_augmentation(self.tile_size)),
              preprocessing=(get_preprocessing(preprocessing_fn)),
              mix_up=True)
            valid_dataset = SdaDataset((self.sda_path),
              "val",
              augmentation=(get_validation_augmentation(self.tile_size)),
              preprocessing=(get_preprocessing(preprocessing_fn)))
            syst = platform.system()
            if syst == "Windows":
                train_loader = FastDataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0)
                valid_loader = FastDataLoader(valid_dataset, batch_size=batch_size, shuffle=False, num_workers=0)
            else:
                train_loader = FastDataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=(self.data_works))
                valid_loader = FastDataLoader(valid_dataset, batch_size=batch_size, shuffle=False, num_workers=(self.data_works))
            loss = get_loss(self.loss_type)
            metrics = [
             IoU(threshold=0.5, ignore_channels=[])]
            if self.optimizer == "adam":
                optimizer = torch.optim.Adam([
                 dict(params=(model.parameters()), lr=lr)])
        elif self.optimizer == "sgd":
            optimizer = torch.optim.SGD([{'params':model_params,  'lr':lr}], lr=lr,
              momentum=0.9,
              weight_decay=0.0005,
              nesterov=False)
        else:
            if self.optimizer == "ranger":
                optimizer = Ranger(params=model_params, lr=lr)
            else:
                if self.optimizer == "rangerva":
                    optimizer = RangerVA(params=model_params, lr=lr)
                else:
                    if self.optimizer == "rangerqh":
                        optimizer = RangerQH(params=model_params, lr=lr)
                    else:
                        raise Exception("optimizer do not support {}".format(self.optimizer))
        train_epoch = TrainEpoch(model,
          loss=loss,
          metrics=metrics,
          optimizer=optimizer,
          device=device,
          verbose=True)
        valid_epoch = ValidEpoch(model,
          loss=loss,
          metrics=metrics,
          device=device,
          verbose=True)
        max_score = 0
        for i in range(epoch):
            train_logs, valid_logs = (None, None)
            try:
                print("\nEpoch: {}/{}".format(i + 1, epoch))
                if kwargs.get("data_aug_change"):
                    train_dataset.augmentation[0].p = i / epoch * 0.35
                train_logs = train_epoch.run(train_loader)
                valid_logs = valid_epoch.run(valid_loader)
                if max_score < valid_logs["iou_score"]:
                    max_score = valid_logs["iou_score"]
                    (self._save_model_pth)(i, model, model_clone, replace=True, **kwargs)
                    print("Model saved!")
                if lr < 1e-05:
                    break
            finally:
                del train_logs
                del valid_logs

        return (
         self._saving_model(), max_score)

    def get_model(self):
        raise NotImplementedError

    def _init_data(self):
        return split_train_val_withdirs([os.path.join(self.train_data_path, "Images")], [
         os.path.join(self.train_data_path, "Masks")],
          (os.path.join(self.train_data_path, "csv_path")),
          x_ext=(self.data_config.dataset.x_ext),
          y_ext=(self.data_config.dataset.y_ext),
          val_scale=(self.config.trainer.validation_split))

    def _saving_model(self):
        config = OrderedDict({'model_type':self.model_type, 
         'framework':"pytorch", 
         'model_architecture':self.model_architecture, 
         'model_categorys':self.model_base_name, 
         'tile_size':self.tile_size, 
         'model_tag':"standard", 
         'signature_name':"predict", 
         'model_input':[{'shape':input,  'type':"float",  'inputs':"images" + (str(i))} for i, input in enumerate(self.model_input)], 
         'model_output':[{'shape':output,  'type':"float",  'outputs':"scores" + (str(i))} for i, output in enumerate(self.model_output)], 
         'class_type':[OrderedDict(l.toDict()) for l in list(self.class_type)], 
         'is_stretch':0, 
         'batch_size':1, 
         'encoder':self.encoder, 
         'encoder_weights':self.encoder_weights})
        save_config_to_yaml(config, self.sdm_path)
        log_info("model saved in dir : {}".format(self.sdm_path))
        print("model saved in dir : {}".format(self.sdm_path))
        return self.sdm_path

# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\change_unet.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 20606 bytes
"""
@author: YangRuijie
@license: 
@contact: yangruijie@supermap.com
@software: 
@file: change_unet.py
@time: 7/26/19 8:25 AM
@desc: 基于特征相减的变化检测unet网络
"""
import os, shutil, tempfile, numpy as np, rasterio
from keras import backend as K
from keras.losses import categorical_crossentropy
from keras.optimizers import Adam
from rasterio.plot import reshape_as_image, reshape_as_raster
from rasterio.windows import Window
from ..... import import_tif, raster_to_vector, DatasetType
from _jsuperpy.data._util import get_output_datasource, check_output_datasource, get_input_dataset
from ....._logger import log_warning, log_info, log_error
from toolkit._keras_model_utils import find_last, bce_dice_loss, dice_coef
from toolkit._toolkit import stretch_n, view_bar, split_train_val_withdirs, split_train_val_change_det, get_image_from_csv, get_changedet_image_from_csv
from _seg_models.encs.cls_models.cls_models.utils import get_weights_default_path
from _seg_models.encs.cls_models.cls_models.weights import weights_collection
from _seg_models.model_builder import build_model
from .base_keras_models import Estimation, Trainer

class ChangUNetEstimation(Estimation):

    def __init__(self, model_path, config):
        super().__init__(model_path, config)
        self.model_input1 = config.ModelInput[0]
        self.model_input2 = config.ModelInput[1]
        self.model_output = config.ModelOutput[0]
        if np.argmin(self.model_input1.Shape) == 0:
            self.band_order = "first"
            self.seg_size = self.model_input1.Shape[1]
            self.out_width_height = [self.model_output.Shape[1], self.model_output.Shape[2]]
            self.output_msk_num = self.model_output.Shape[0]
            if self.model_input1.Shape[1] != self.model_input1.Shape[2]:
                raise ValueError("Model input width and height should be equal!")
        else:
            self.band_order = "last"
            self.seg_size = self.model_input1.Shape[1]
            self.out_width_height = [self.model_output.Shape[0], self.model_output.Shape[1]]
            self.output_msk_num = self.model_output.Shape[-1]
            if self.model_input1.Shape[1] != self.model_input1.Shape[0]:
                raise ValueError("Model input width and height should be equal!")
        self.is_stretch = config.IsStretch
        self.model_path = model_path

    def estimate_img(self, before_img, after_image, coversize, out_ds, out_dataset_name, **kwargs):
        self.half_oversize = coversize
        self._predict_with_rasterio(before_img, after_image, out_ds, out_dataset_name)

    def _predict_with_rasterioParse error at or near `COME_FROM' instruction at offset 1672_0

    def _predict_tile_local(self, pre_tile, next_tile, out_shape):
        """
        利用给定的模型使用tensorflow推断得到模型预测结果
        :param predict_tile:  ndarray 需要预测的数组片 形状为 （tile_nums,:） 即第一列为图片的数量
        :param out_shape: tuple 输出结果的形状  如（100,320,320,1）
        :return:  ndarray 返回预测的结果
        """
        x1_tensor_name = self.signature["predict"].inputs["images0"].name
        x2_tensor_name = self.signature["predict"].inputs["images1"].name
        y_tensor_name = self.signature["predict"].outputs["scores"].name
        x1 = self.sess.graph.get_tensor_by_name(x1_tensor_name)
        x2 = self.sess.graph.get_tensor_by_name(x2_tensor_name)
        y = self.sess.graph.get_tensor_by_name(y_tensor_name)
        self.sess.graph.finalize()
        batch_size = 1
        assert pre_tile.shape[0] == next_tile.shape[0], "before after image shape should be same"
        total_batch = int(pre_tile.shape[0] / batch_size)
        for i in range(total_batch):
            out = self.sess.run(y, feed_dict={x1: (pre_tile[((i * batch_size)[:(i + 1) * batch_size], None[:None])]), 
             x2: (pre_tile[((i * batch_size)[:(i + 1) * batch_size], None[:None])])})
            if i == 0:
                y_all = out
            else:
                y_all = np.concatenate((y_all, out), 0)

        y_out = np.expand_dims(y_all, axis=0)
        y_out.resize(out_shape)
        return y_out


class ChangeUNetTrainer(Trainer):

    def __init__(self):
        super().__init__()
        self.model_type = "change"
        self.model_architecture = "change_unet"

    def train(self, train_data_path, config, epoch=1, batch_size=1, lr=0.001, output_model_path='./', output_model_name='change_unet', log_path=None, backbone_name='resnext50', backbone_weight_path=None, reload_model=False, pretrained_model_path=None):
        K.clear_session()
        self.train_data_path = train_data_path
        self.config = config
        self.epoch = epoch
        self.batch_size = batch_size
        self.lr = lr
        self.output_model_path = output_model_path
        self.output_model_name = output_model_name
        self.backbone_name = backbone_name
        if self.backbone_name is None or self.backbone_name.strip() == "":
            log_warning("backbone_name 为空,将使用默认 backbone_name")
            self.backbone_name = "resnext50"
        else:
            if self.backbone_name != "resnext50":
                log_warning("backbone_name 不支持 {} ,将使用默认 backbone_name".format(backbone_name))
                self.backbone_name = "resnext50"
        self.backbone_weight_path = backbone_weight_path
        self.pretrained_model_path = pretrained_model_path
        self.log_path = log_path
        self.reload_model = reload_model
        self.init_callbacks(log_path)
        self.config.trainer.num_epochs = epoch
        self.config.trainer.batch_size = batch_size
        self.config.model.learning_rate = lr
        self.input_bands = self.config.model.input_bands
        if len(self.input_bands) > 0:
            tmp_num = self.input_bands[0]
            for i in self.input_bands:
                assert i >= 1, "输入波段数应大于等于1"
                assert tmp_num == i, "各个输入波段数应相等"

        self.output_bands = self.config.model.output_bands
        assert self.output_bands >= 1, "输出波段数应大于等于1"
        self.split_size = self.config.data.split_size
        self.class_type = self.config.model.ClassType
        if self.pretrained_model_path is not None:
            self.model = build_model((self.split_size), (self.split_size), (self.input_bands[0]), (self.output_bands), backbone_name=(self.backbone_name),
              encoder_weights=None,
              net_type="change_unet")
            checkpoint = find_last(self.pretrained_model_path, self.config.exp.name)
            if checkpoint and os.path.exists(checkpoint):
                log_info("从 {} 下加载预训练模型".format(checkpoint))
                self.model.load_weights(checkpoint, by_name=True)
            else:
                log_error("{} 中没有预训练模型".format(self.pretrained_model_path))
        else:
            if self.backbone_weight_path is not None and os.path.isfile(self.backbone_weight_path):
                if os.path.exists(self.backbone_weight_path):
                    keras_cache_file, cache_file = get_weights_default_pathweights_collectionself.backbone_name"imagenet"False
                    if os.path.exists(cache_file) is not True:
                        log_info("从 {} 下加载主干网络模型".format(self.backbone_weight_path))
                        if os.path.exists(os.path.dirname(keras_cache_file)) is not True:
                            os.makedirs(os.path.dirname(keras_cache_file))
                        shutil.copy2(self.backbone_weight_path, keras_cache_file)
                    else:
                        log_info("缓存模型已存在")
                self.model = build_model((self.split_size), (self.split_size), (self.input_bands[0]), (self.output_bands), backbone_name=(self.backbone_name),
                  encoder_weights="imagenet",
                  net_type="change_unet")
            elif self.output_bands == 1:
                self.model.compile(loss=bce_dice_loss, optimizer=Adam(lr=(self.lr)),
                  metrics=[
                 "acc", dice_coef])
            else:
                self.model.compile(loss=categorical_crossentropy, optimizer=Adam(lr=(self.lr)),
                  metrics={
                 "acc", categorical_crossentropy, dice_coef})
            self._init_data()
            train_path = os.path.join(self.train_data_path, "csv_path", "train.csv")
            val_path = os.path.join(self.train_data_path, "csv_path", "val.csv")
            x, y = self._get_data_from_csv(train_path, False, image_size=(self.split_size))
            history = self.model.fit(x=x,
              y=y,
              validation_data=self._get_data_from_csv(val_path, False, image_size=(self.split_size)),
              epochs=(self.config.trainer.num_epochs),
              verbose=(self.config.trainer.verbose_training),
              batch_size=(self.config.trainer.batch_size),
              callbacks=(self.callbacks))
            self.loss.extend(history.history["loss"])
            self.acc.extend(history.history["acc"])
            self.val_loss.extend(history.history["val_loss"])
            self.val_acc.extend(history.history["val_acc"])
            checkpoint = os.path.join(tempfile.gettempdir(), "checkpoint")
            self.model.save_weights(checkpoint)
            K.clear_session()
            K.set_learning_phase(0)
            export_model = build_model((self.config.data.split_size), (self.config.data.split_size), (self.input_bands[0]), (self.output_bands),
              backbone_name=(self.backbone_name),
              encoder_weights=None,
              net_type="change_unet")
            export_model.load_weights(checkpoint)
            self._save_tfserving_model(export_model, os.path.join(output_model_path, output_model_name))
            K.clear_session()

    def _init_data(self):
        split_train_val_change_det([os.path.join(self.train_data_path, "PreImages")], [
         os.path.join(self.train_data_path, "NextImages")],
          [
         os.path.join(self.train_data_path, "Masks")],
          (os.path.join(self.train_data_path, "csv_path")),
          x_ext=(self.config.data.x_ext),
          y_ext=(self.config.data.y_ext),
          val_scale=(self.config.data.val_scale))

    def _get_data_from_csv(self, data_path, is_aug=False, image_size=None):
        if self.output_bands > 1:
            if data_path.endswith(".csv"):
                x1, x2, y = get_changedet_image_from_csv(data_path, is_aug, band_num=(self.output_bands), image_size=image_size)
            else:
                raise Exception("You should input a *.csv file")
        else:
            return (
             [
              x1, x2], y)
            if data_path.endswith(".csv"):
                x1, x2, y = get_changedet_image_from_csv(data_path, is_aug, image_size=image_size)
            else:
                raise Exception("You should input a *.csv file")
        return (
         [
          x1, x2], y)
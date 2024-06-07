# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\base_keras_models.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 10419 bytes
"""
@author: YangRuijie
@license: 
@contact: yangruijie@supermap.com
@software: 
@file: base_models.py
@time: 7/23/19 6:49 AM
@desc:
"""
import os, time
from collections import OrderedDict
import numpy as np, tensorflow as tf
from keras.callbacks import TensorBoard, ModelCheckpoint
from tensorflow import Tensor
from tensorflow.python.saved_model import tag_constants
from tensorflow.python.saved_model.signature_def_utils_impl import predict_signature_def
from tensorflow.python.saved_model import builder as saved_model_builder
from keras import backend as K
from toolkit._keras_model_utils import ModelCheckpointLatest, ParallelModelCheckpoint, ParallelModelCheckpointLatest
from ....._logger import log_warning, log_info
from toolkit._toolkit import save_config_to_yaml

class Estimation:

    def __init__(self, model_path, config):
        if not isinstance(model_path, str):
            raise TypeError("model_path data type inappropriate ，should be str ")
        if not os.path.exists(model_path):
            raise Exception("model_path  path not exists")
        self.model_path = model_path
        self.sess = None
        self.tf_inputs = None
        self.tf_outputs = None
        self.load_model(model_path)

    def estimate_img(self):
        pass

    def estimate_tile(self):
        pass

    def load_model(self, model_path):
        self.model_path = model_path
        self.sess = tf.Session()
        self.meta_graph_def = tf.saved_model.loader.load(self.sess, ["serve"], model_path)
        self.signature = self.meta_graph_def.signature_def
        self.sess.graph.finalize()

    def close_model(self):
        """
        关闭模型
        :return:
        """
        self.sess.close()
        tf.reset_default_graph()

    def _predict_tile_local(self, predict_tile, out_shape):
        """
        利用给定的模型使用tensorflow推断得到模型预测结果
        :param predict_tile:  ndarray 需要预测的数组片 形状为 （tile_nums,:） 即第一列为图片的数量
        :param out_shape: tuple 输出结果的形状  如（100,320,320,1）
        :return:  ndarray 返回预测的结果
        """
        x_tensor_name = self.signature["predict"].inputs["images"].name
        y_tensor_name = self.signature["predict"].outputs["scores"].name
        x = self.sess.graph.get_tensor_by_name(x_tensor_name)
        y = self.sess.graph.get_tensor_by_name(y_tensor_name)
        self.sess.graph.finalize()
        batch_size = 1
        total_batch = int(predict_tile.shape[0] / batch_size)
        for i in range(total_batch):
            out = self.sess.run(y, feed_dict={x: (predict_tile[((i * batch_size)[:(i + 1) * batch_size], None[:None])])})
            if i == 0:
                y_all = out
            else:
                y_all = np.concatenate((y_all, out), 0)

        y_out = np.expand_dims(y_all, axis=0)
        y_out.resize(out_shape)
        return y_out


class Trainer:

    def __init__(self):
        self.callbacks = []
        self.loss = []
        self.acc = []
        self.val_loss = []
        self.val_acc = []
        self.model_type = ""
        self.model_architecture = ""
        self.single_model = None

    def init_callbacks(self, log_path=None):
        if log_path:
            self.config.trainer.callbacks.tensorboard_log_dir = os.path.join(log_path, time.strftime("%Y-%m-%d", time.localtime()), self.config.application.name, "logs")
            self.config.trainer.callbacks.checkpoint_dir = os.path.join(log_path, time.strftime("%Y-%m-%d", time.localtime()), self.config.application.name, "checkpoints")
        else:
            self.log_path = "experiments"
            self.config.trainer.callbacks.tensorboard_log_dir = os.path.join("experiments", time.strftime("%Y-%m-%d", time.localtime()), self.config.application.name, "logs")
            self.config.trainer.callbacks.checkpoint_dir = os.path.join("experiments", time.strftime("%Y-%m-%d", time.localtime()), self.config.application.name, "checkpoints")
        if os.path.exists(self.config.trainer.callbacks.tensorboard_log_dir) is not True:
            os.makedirs(self.config.trainer.callbacks.tensorboard_log_dir)
        elif os.path.exists(self.config.trainer.callbacks.checkpoint_dir) is not True:
            os.makedirs(self.config.trainer.callbacks.checkpoint_dir)
        if self.single_model is None:
            self.callbacks.append(ModelCheckpoint(filepath=(os.path.join(self.config.trainer.callbacks.checkpoint_dir, "%s-{epoch:04d}-{val_loss:.4f}.hdf5" % self.config.application.name)),
              monitor=(self.config.trainer.callbacks.checkpoint_monitor),
              mode=(self.config.trainer.callbacks.checkpoint_mode),
              save_best_only=(self.config.trainer.callbacks.checkpoint_save_best_only),
              save_weights_only=(self.config.trainer.callbacks.checkpoint_save_weights_only),
              verbose=(self.config.trainer.callbacks.checkpoint_verbose)))
            self.callbacks.append(ModelCheckpointLatest(self.config.trainer.callbacks.checkpoint_dir))
        else:
            self.callbacks.append(ParallelModelCheckpoint((self.single_model),
              filepath=(os.path.join(self.config.trainer.callbacks.checkpoint_dir, "%s-{epoch:04d}-{val_loss:.4f}.hdf5" % self.config.application.name)),
              monitor=(self.config.trainer.callbacks.checkpoint_monitor),
              mode=(self.config.trainer.callbacks.checkpoint_mode),
              save_best_only=(self.config.trainer.callbacks.checkpoint_save_best_only),
              save_weights_only=(self.config.trainer.callbacks.checkpoint_save_weights_only),
              verbose=(self.config.trainer.callbacks.checkpoint_verbose)))
            self.callbacks.append(ParallelModelCheckpointLatest(self.single_model, self.config.trainer.callbacks.checkpoint_dir))
        self.callbacks.append(TensorBoard(log_dir=(self.config.trainer.callbacks.tensorboard_log_dir),
          write_graph=(self.config.trainer.callbacks.tensorboard_write_graph)))

    def train(self):
        pass

    def _save_tfserving_model(self, model, out_path, export_version=None):
        """
        save tfserving model
        :param model: keras model
        :param out_path:
        :param export_version:
        :return:
        """
        K.set_learning_phase(0)
        with tf.device("/cpu:0"):
            new_model = model
            export_base_path = out_path
            if export_version is None:
                export_path = export_base_path
            else:
                export_path = os.path.join(export_base_path, str(export_version))
            while os.path.exists(export_path):
                export_path += "_1"

            builder = saved_model_builder.SavedModelBuilder(export_path)
            if not isinstance(new_model.input, Tensor):
                signature = predict_signature_def(inputs={"images" + str(i): input for i, input in enumerate(new_model.input)}, outputs={"scores": (new_model.output)})
                ModelinputputJson = [{'shape':input.shape.as_list()[1[:None]],  'type':(input.dtype).name,  'inputs':"images" + (str(i))} for i, input in enumerate(new_model.input)]
            else:
                ModelinputputJson = [{'shape':new_model.input.shape.as_list()[1[:None]], 
                  'type':(new_model.input.dtype).name,  'inputs':"images"}]
                signature = predict_signature_def(inputs={"images": (new_model.input)}, outputs={"scores": (new_model.output)})
            with K.get_session() as sess:
                builder.add_meta_graph_and_variables(sess=sess, tags=[
                 tag_constants.SERVING],
                  signature_def_map={"predict": signature})
                builder.save()
        base_name = os.path.basename(export_path)
        config = OrderedDict({'model_type':self.model_type, 
         'framework':"keras", 
         'model_architecture':self.model_architecture, 
         'model_categorys':base_name, 
         'tile_size':self.tile_size, 
         'model_tag':"standard", 
         'signature_name':"predict", 
         'model_input':ModelinputputJson, 
         'model_output':[
          {'shape':new_model.output.shape.as_list()[1[:None]], 
           'type':(new_model.output.dtype).name,  'outputs':"scores"}], 
         'class_type':[OrderedDict(l.toDict()) for l in list(self.class_type)], 
         'is_stretch':0, 
         'batch_size':1, 
         'input_node_names':(model.input.op).name, 
         'output_node_names':(model.output.op).name})
        model_path = os.path.join(export_path, str(base_name) + ".sdm")
        save_config_to_yaml(config, model_path)
        log_info("model saved in dir : {}".format(model_path))
        print("model saved in dir : {}".format(model_path))

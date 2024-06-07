# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\dlinknet\estimation_tf.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 10545 bytes
import os, sys, tempfile, cv2, numpy as np, rasterio, tensorflow as tf
from rasterio.plot import reshape_as_image
from rasterio.windows import Window
from tensorflow.python.platform import gfile
from iobjectspy import raster_to_vector, DatasourceConnectionInfo, Datasource, import_tif, DatasetType, EngineType
from iobjectspy._jsuperpy.data._util import get_output_datasource
from iobjectspy.ml.toolkit._toolkit import view_bar

class DlinknetEstimationTf:

    def __init__(self, model_path, config):
        self.model_path = model_path
        self.config = config
        self.model_input = self.config.model_input[0]
        self.model_output = self.config.model_output[0]
        self.in_bands_num = self.model_input.shape[-1]
        self.out_bands_num = self.model_output.shape[-1]
        self.sess = None
        self.tf_inputs = None
        self.tf_outputs = None
        self.load_model(self.model_path)

    def augment_data(self, input_tile):
        img90 = np.array(np.rot90(input_tile))
        img1 = np.concatenate([input_tile[None], img90[None]])
        img2 = np.array(img1)[(None[:None], None[None:-1])]
        img3 = np.concatenate([img1, img2])
        img4 = np.array(img3)[(None[:None], None[:None], None[None:-1])]
        img5 = img3.transpose(0, 3, 1, 2)
        img_augment1 = np.array(img5, np.float32) / 255.0 * 3.2 - 1.6
        img6 = img4.transpose(0, 3, 1, 2)
        img_augment2 = np.array(img6, np.float32) / 255.0 * 3.2 - 1.6
        return (
         img_augment1, img_augment2)

    def estimate_tile(self, tile_augment1, tile_augment2):
        maska = self.sess.run((self.tf_outputs), feed_dict={(self.tf_inputs): tile_augment1})
        maskb = self.sess.run((self.tf_outputs), feed_dict={(self.tf_inputs): tile_augment2})
        maska = maska.reshape(4, 1024, 1024)
        maskb = maskb.reshape(4, 1024, 1024)
        mask1 = maska + maskb[(None[:None], None[:None], None[None:-1])]
        mask2 = mask1[None[:2]] + mask1[(2[:None], None[None:-1])]
        mask3 = mask2[0] + np.rot90(mask2[1])[(None[None:-1], None[None:-1])]
        result_threshold = self.config.result_threshold
        mask3[mask3 < result_threshold] = 0
        mask3[mask3 >= result_threshold] = 1
        mask3 = mask3.reshape(1, mask3.shape[0], mask3.shape[1])
        return mask3

    def estimate_imgParse error at or near `COME_FROM' instruction at offset 1330_0

    def load_model(self, model_path):
        model_path = os.path.join(model_path, "saved_model.pb")
        self.sess = tf.Session
        with gfile.FastGFile(model_path, "rb") as f:
            graph_def = tf.GraphDef
            graph_def.ParseFromString(f.read)
            self.sess.graph.as_default
            tf.import_graph_def(graph_def, name="")
        self.sess.graph.finalize
        self.tf_inputs = self.sess.graph.get_tensor_by_name("input:0")
        self.tf_outputs = self.sess.graph.get_tensor_by_name("Sigmoid:0")

    def close_model(self):
        self.sess.close
        tf.reset_default_graph
# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\instance_segmentation\mask_segmentation.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 50627 bytes
import glob, math, os, platform, random, shutil, sys
from collections import OrderedDict
import cv2
import matplotlib.pyplot as plt
import numpy as np, scipy.misc, scipy.ndimage, tensorflow as tf
from keras import backend as K
from albumentations import Resize, HorizontalFlip, VerticalFlip, RandomSizedCrop, ShiftScaleRotate, ISONoise
import warnings
from . import model as modellib
from . import utils
from .utils import show_two_image
from .config import Config
from toolkit._toolkit import get_config_from_yaml
from toolkit._toolkit import save_config_to_yaml

def export_savedmodel(model, model_out_path, out_name):
    export_path = os.path.join(model_out_path, out_name)
    while True:
        if os.path.exists(export_path):
            export_path = export_path + "_1"
        else:
            break

    model_signature = tf.saved_model.signature_def_utils.build_signature_def(inputs={'input_image':(tf.saved_model.utils.build_tensor_info)(model.inputs[0]), 
     'input_image_meta':(tf.saved_model.utils.build_tensor_info)(model.inputs[1])},
      outputs={'detections':(tf.saved_model.utils.build_tensor_info)(model.outputs[0]), 
     'mrcnn_class':(tf.saved_model.utils.build_tensor_info)(model.outputs[1]), 
     'mrcnn_bbox':(tf.saved_model.utils.build_tensor_info)(model.outputs[2]), 
     'mrcnn_mask':(tf.saved_model.utils.build_tensor_info)(model.outputs[3]), 
     'roi':(tf.saved_model.utils.build_tensor_info)(model.outputs[4]), 
     'rpn_class':(tf.saved_model.utils.build_tensor_info)(model.outputs[5]), 
     'rpn_bbox':(tf.saved_model.utils.build_tensor_info)(model.outputs[6])},
      method_name=(tf.saved_model.signature_constants.CLASSIFY_METHOD_NAME))
    builder = tf.saved_model.builder.SavedModelBuilder(export_path)
    builder.add_meta_graph_and_variables(sess=(K.get_session()),
      tags=[
     tf.saved_model.tag_constants.SERVING],
      clear_devices=True,
      signature_def_map={"predict": model_signature})
    builder.save()
    print("model saved in dir :{}".format(export_path))
    return export_path


def conver_config(feed_config, yaml_config):
    feed_config.NAME = yaml_config.application.name
    feed_config.FRAMEWORK = yaml_config.framework.name
    feed_config.GPU_COUNT = yaml_config.trainer.gpu_count
    feed_config.IMAGES_PER_GPU = yaml_config.trainer.image_per_gpu
    feed_config.STEPS_PER_EPOCH = yaml_config.trainer.steps_per_epoch
    feed_config.VALIDATION_STEPS = yaml_config.trainer.validation_steps
    feed_config.BACKBONE_STRIDES = yaml_config.trainer.backbone_strides
    feed_config.RPN_ANCHOR_SCALES = yaml_config.trainer.rpn_anchor_scales
    feed_config.RPN_ANCHOR_RATIOS = yaml_config.trainer.rpn_anchor_ratios
    feed_config.RPN_ANCHOR_STRIDE = yaml_config.trainer.rpn_anchor_stride
    feed_config.RPN_NMS_THRESHOLD = yaml_config.trainer.rpn_nms_threshold
    feed_config.VALIDATION_SPLIT = yaml_config.trainer.validation_split
    feed_config.RPN_TRAIN_ANCHORS_PER_IMAGE = yaml_config.trainer.rpn_train_anchors_per_image
    feed_config.POST_NMS_ROIS_TRAINING = yaml_config.trainer.post_nms_rois_training
    feed_config.POST_NMS_ROIS_INFERENCE = yaml_config.trainer.post_nms_rois_inference
    feed_config.USE_MINI_MASK = yaml_config.trainer.use_mini_mask
    feed_config.MINI_MASK_SHAPE = yaml_config.trainer.mini_mask_shape
    feed_config.IMAGE_MIN_DIM = yaml_config.trainer.image_min_dim
    feed_config.IMAGE_MAX_DIM = yaml_config.trainer.image_max_dim
    feed_config.IMAGE_PADDING = yaml_config.trainer.image_padding
    feed_config.MEAN_PIXEL = np.array(yaml_config.trainer.mean_pixel)
    feed_config.TRAIN_ROIS_PER_IMAGE = yaml_config.trainer.train_rois_per_image
    feed_config.ROI_POSITIVE_RATIO = yaml_config.trainer.roi_positive_ratio
    feed_config.POOL_SIZE = yaml_config.trainer.pool_size
    feed_config.MASK_POOL_SIZE = yaml_config.trainer.mask_pool_size
    feed_config.MASK_SHAPE = yaml_config.trainer.mask_shape
    feed_config.MAX_GT_INSTANCES = yaml_config.trainer.max_gt_instances
    feed_config.RPN_BBOX_STD_DEV = np.array(yaml_config.trainer.rpn_bbox_std_dev)
    feed_config.BBOX_STD_DEV = np.array(yaml_config.trainer.bbox_std_dev)
    feed_config.DETECTION_MAX_INSTANCES = yaml_config.trainer.detection_max_instances
    feed_config.DETECTION_MIN_CONFIDENCE = yaml_config.trainer.detection_min_confidence
    feed_config.DETECTION_NMS_THRESHOLD = yaml_config.trainer.detection_nms_threshold
    feed_config.LEARNING_RATE = yaml_config.trainer.learning_rate
    feed_config.LEARNING_MOMENTUM = yaml_config.trainer.learning_momentum
    feed_config.WEIGHT_DECAY = yaml_config.trainer.weight_decay
    feed_config.USE_RPN_ROIS = yaml_config.trainer.use_rpn_rois
    feed_config.EPOCHS = yaml_config.trainer.epochs
    return feed_config


class ShapesDataset(utils.Object_Extract_Dataset):

    def __init__(self, data, class_map=None):
        super(ShapesDataset, self).__init__(class_map)
        self.data = data

    def load_shapes(self, count, height, width):
        data = self.data
        class_dict = self.data[0][0]
        class_name_dict = dict(zip(class_dict.values(), class_dict.keys()))
        [self.add_class("shapes", i, class_name_dict[i]) for i in range(1, len(class_dict) + 1)]
        for i in range(1, len(data)):
            comb_image = data[i][0]
            mask = data[i][1]
            class_ids = data[i][2]
            self.add_image("shapes", image_id=(i - 1), path=None, width=height,
              height=width,
              image=comb_image,
              mask=mask,
              class_ids=class_ids)

    def load_image(self, image_id):
        info = self.image_info[image_id]
        image = info["image"]
        return image

    def image_reference(self, image_id):
        """Return the shapes data of the image."""
        info = self.image_info[image_id]
        if info["source"] == "shapes":
            return info["shapes"]
        super(self.__class__).image_reference(self, image_id)

    def load_mask(self, image_id):
        info = self.image_info[image_id]
        mask = info["mask"]
        class_ids = info["class_ids"]
        return (mask, class_ids.astype(np.int32))


def saved_config_sdm(config, model, class_names, export_path, output_model_name):
    pixel = str(list(config.MEAN_PIXEL))
    saved_config = OrderedDict({'model_type':config.NAME, 
     'framework':config.FRAMEWORK, 
     'model_architecture':"maskrcnn", 
     'model_categorys':class_names, 
     'signature_name':"predict", 
     'model_input':[
      {'inputs':"images", 
       'shape':model.inputs[0].shape.as_list()[1[:None]],  'type':(model.inputs[0].dtype).name}], 
     'mean_pixel':pixel})
    model_path = os.path.join(export_path, output_model_name + ".sdm")
    save_config_to_yaml(saved_config, model_path)


class MaskRcnnTrainer:

    def __init__(self):
        self.dataset_train = None
        self.dataset_val = None
        self.config = None
        self.epoch_stages = None
        self.layers = None
        self.warmup_epoch = None
        self.log_path = None
        self.backbone_name = None

    def train(self, train_data_path, yml_config, epochs, batch_size, lr, output_model_path, output_model_name, log_path, reload_model, pretrained_model_path, backbone_weight_path=None, backbone_name=None, load_optimizer_state=False, mlflow_add=False, only_export_pb=False, pickle_file=None):
        self.config = Config()
        self.config = conver_config(self.config, yml_config)
        train_data_path = os.path.abspath(train_data_path)
        sda_file = os.path.basename(train_data_path) + ".sda"
        sda_file_path = os.path.join(train_data_path, sda_file)
        if not os.path.exists(sda_file_path):
            raise ValueError("sda file can't be found in this path  {}".format(sda_file_path))
        else:
            _sda = get_config_from_yaml(sda_file_path)
            self.config.MEAN_PIXEL = _sda.dataset.image_mean
            image_suffix = str(".") + _sda.dataset.suffix
            self.config.IMAGE_MAX_DIM = max(int(_sda.dataset.tile_size_x), int(_sda.dataset.tile_size_y))
            self.set_model_input_size()
            self.config.do_init()
            self.config.EPOCHS = epochs
            self.config.BATCH_SIZE = batch_size
            self.config.LEARNING_RATE = lr
            self.config.IMAGES_PER_GPU = round(batch_size // self.config.GPU_COUNT)
            self.config.MINI_MASK_SHAPE = tuple(self.config.MINI_MASK_SHAPE)
            self.config.RPN_ANCHOR_SCALES = tuple(self.config.RPN_ANCHOR_SCALES)
            self.Mlflow_record(use=mlflow_add)
            self.dataset_train, self.dataset_val, train_images = self.data_to_train(train_data_path, self.config, image_suffix)
            self.config.STEPS_PER_EPOCH = round(train_images / self.config.BATCH_SIZE)
            self.config.VALIDATION_STEPS = self.config.STEPS_PER_EPOCH // 20
            self.layers = ["heads", "4+", "all"]
            self.epoch_stages = [round(self.config.EPOCHS // 3), 2 * round(self.config.EPOCHS // 3), self.config.EPOCHS]
            self.warmup_epoch = 5
            self.log_path = log_path
            if backbone_name == None:
                self.backbone_name = yml_config.model.backbone_name
            else:
                self.backbone_name = backbone_name
            if not only_export_pb:
                model, pickle_file = self.model_initiate(reload_model, pretrained_model_path, backbone_weight_path, load_optimizer_state)
                if self.config.EPOCHS > self.warmup_epoch:
                    if not reload_model:
                        self.warmup_train(model)
                    self.stages_train(model, load_optimizer_state, pickle_file)
                else:
                    model.train((self.dataset_train), (self.dataset_val), learning_rate=(self.config.LEARNING_RATE),
                      epochs=(self.epoch_stages[2]),
                      layers=(self.layers[2]))
                try:
                    checkpoint = model.find_last()
                    self.save_pb(checkpoint, output_model_path, output_model_name)
                except Exception as e:
                    try:
                        if not os.path.exists(checkpoint):
                            raise ValueError("The model can't be found in the path {}".format(checkpoint))
                        else:
                            raise ValueError(e)
                    finally:
                        e = None
                        del e

            else:
                h5_path = ""
                self.save_pb(h5_path, output_model_path, output_model_name)

    def set_model_input_size(self):
        """
        根据切出图片的行列数,取最近的64的倍数作为模型输入
        """
        image_size = self.config.IMAGE_MAX_DIM
        larger_size = math.ceil(image_size / 64) * 64
        small_size = math.floor(image_size / 64) * 64
        pixel_l = larger_size - image_size
        pixel_s = image_size - small_size
        if pixel_l > pixel_s:
            self.config.IMAGE_MAX_DIM = small_size
        else:
            self.config.IMAGE_MAX_DIM = larger_size
        self.config.IMAGE_MIN_DIM = self.config.IMAGE_MAX_DIM

    def model_initiate(self, reload_model, pretrained_model_path, backbone_weight_path, load_optimizer_state):
        if platform.system() == "Windows":
            sp = "\\"
        else:
            sp = "/"
        pickle_file = None
        model = modellib.MaskRCNN(mode="training", config=(self.config), model_dir=(self.log_path),
          backbone_name=(self.backbone_name))
        if reload_model:
            try:
                model_path = model.find_last(pretrained_model_path=pretrained_model_path)
            except Exception as e:
                try:
                    print(e)
                    raise ValueError("Find pretrained model failed, please check the directory saved pretrained model  \n {} ".format(pretrained_model_path))
                finally:
                    e = None
                    del e

            try:
                model.load_weights(model_path, by_name=True)
            except Exception as e:
                try:
                    print(e)
                    raise ValueError("Reload pretrained model failed, please check the pretrained model path {} ".format(model_path))
                finally:
                    e = None
                    del e

            if load_optimizer_state:
                pickle_file = model_path.replace(".h5", ".pkl")
        else:
            if backbone_weight_path is not None:
                if os.path.exists(backbone_weight_path) and os.path.isfile(backbone_weight_path):
                    backbone_file = backbone_weight_path.split(sp)[-1]
                    if "maskrcnn" in backbone_file:
                        model.load_weights(backbone_weight_path, by_name=True, exclude=[
                         "mrcnn_class_logits", "mrcnn_bbox_fc",
                         "mrcnn_bbox", "mrcnn_mask"])
                else:
                    model.load_weights(backbone_weight_path, by_name=True)
            else:
                warnings.warn("Load backbone failed , init weights randomly", RuntimeWarning)
                print("please check backbone path  {}".format(backbone_weight_path))
                model.set_log_dir()
        return (
         model, pickle_file)

    def save_pb(self, checkpoint, output_model_path, output_model_name):
        """
               # Save weights
               # Typically not needed because callbacks save after every epoch
               # Uncomment to save manually
               保存重量
               ＃通常不需要，因为回调在每个epoch后都会保存
               ＃取消注释以手动保存
               """
        K.clear_session()
        self.config.BATCH_SIZE = 1
        self.config.IMAGES_PER_GPU = 1
        self.config.GPU_COUNT = 1
        self.config.DETECTION_MIN_CONFIDENCE = 0.2
        self.config.DETECTION_NMS_THRESHOLD = 1.0
        model_ex = modellib.MaskRCNN(mode="inference", config=(self.config), model_dir=(self.log_path),
          backbone_name=(self.backbone_name))
        model_ex.load_weights(checkpoint, by_name=True)
        config_path = export_savedmodel(model_ex.keras_model, output_model_path, output_model_name)
        saved_config_sdm(self.config, model_ex.keras_model, self.dataset_train.class_names, config_path, output_model_name)

    def warmup_train(self, model):
        model.train((self.dataset_train), (self.dataset_val), learning_rate=(self.config.LEARNING_RATE / 10),
          epochs=(self.warmup_epoch),
          layers=(self.layers[0]))

    def stages_train(self, model, load_optimizer_state, pickle_file):
        model.train((self.dataset_train), (self.dataset_val), learning_rate=(self.config.LEARNING_RATE),
          epochs=(self.epoch_stages[0]),
          steps_per_epoch=(self.config.STEPS_PER_EPOCH),
          warmup=False,
          layers=(self.layers[0]),
          weight_decay=(self.config.WEIGHT_DECAY),
          load_optimizer_state=load_optimizer_state,
          pkl_path=pickle_file)
        model.train((self.dataset_train), (self.dataset_val), learning_rate=(self.config.LEARNING_RATE),
          epochs=(self.epoch_stages[1]),
          layers=(self.layers[1]))
        model.train((self.dataset_train), (self.dataset_val), learning_rate=(self.config.LEARNING_RATE / 10),
          epochs=(self.epoch_stages[2]),
          layers=(self.layers[2]))

    def Mlflow_record(self, use=False):
        if use:
            import mlflow
            mlflow.log_param("MEAN_PIXEL", self.config.MEAN_PIXEL)
            mlflow.log_param("mask_shape", self.config.MASK_SHAPE)
            mlflow.log_param("weight_decay", self.config.WEIGHT_DECAY)
            mlflow.log_param("learning_rate", self.config.LEARNING_RATE)
            mlflow.log_param("learning_momentum", self.config.LEARNING_MOMENTUM)
            mlflow.log_param("detection_min_confidence", self.config.DETECTION_MIN_CONFIDENCE)
            mlflow.log_param("nms_threshold", self.config.DETECTION_NMS_THRESHOLD)
            mlflow.log_param("epoch", self.config.EPOCHS)
            mlflow.log_param("learning-rate", self.config.LEARNING_RATE)
            mlflow.log_param("batch_size", self.config.BATCH_SIZE)

    def mAP_cal(self, dataset_val, inference_config, model):
        image_ids = np.random.choice(dataset_val.image_ids, 60)
        APs = []
        for image_id in image_ids:
            image, image_meta, gt_class_id, gt_bbox, gt_mask = modellib.load_image_gt(dataset_val, inference_config, image_id,
              use_mini_mask=False)
            molded_images = np.expand_dims(modellib.mold_image(image, inference_config), 0)
            results = model.detect([image], verbose=0)
            r = results[0]
            AP, precisions, recalls, overlaps = utils.compute_ap(gt_bbox, gt_class_id, gt_mask, r["rois"], r["class_ids"], r["scores"], r["masks"])
            APs.append(AP)

        print("mAP: ", np.mean(APs))

    def _save_index_file(self, data_path, Img_path, train_portion=0.8):
        """
        将训练数据以4:1划分训练集和验证集,并将对应图片名称写入文件夹ImageSets/Main 的txt文件
        """
        output_path_main = os.path.join(data_path, "ImageSets/Main")
        if not os.path.exists(output_path_main):
            os.makedirs(output_path_main)
        else:
            pic_names = next(os.walk(Img_path))[-1]
            pic_names.sort()
            class_split = [
             0]
            if len(class_split) > 1:
                list_train, list_val = [], []
                for num in range(len(class_split) - 1):
                    data_class = pic_names[class_split[num][:class_split[num + 1]]]
                    random.shuffle(data_class)
                    list_train = list_train + data_class[0[:int(len(data_class) * train_portion)]]
                    list_val = list_val + data_class[int(len(data_class) * train_portion)[:None]]

                data_class = pic_names[class_split[-1][:None]]
                random.shuffle(data_class)
                list_train = list_train + data_class[0[:int(len(data_class) * train_portion)]]
                list_val = list_val + data_class[int(len(data_class) * train_portion)[:None]]
                random.shuffle(list_train)
                random.shuffle(list_val)
            else:
                random.shuffle(pic_names)
            train_length = int(len(pic_names) * train_portion)
            list_train = pic_names[0[:train_length]]
            list_val = pic_names[train_length[:None]]
        train_txt = open(os.path.join(output_path_main, "train.txt"), "w")
        val_txt = open(os.path.join(output_path_main, "val.txt"), "w")
        for pic_name in list_train:
            label_name = pic_name.split(".")[0]
            train_txt.write(label_name + "\n")

        for pic_name in list_val:
            label_name = pic_name.split(".")[0]
            val_txt.write(label_name + "\n")

        train_txt.close()
        val_txt.close()

    def data_to_train(self, data_path, config, image_suffix):
        """
        加载并返回训练数据
        """
        data_path = os.path.abspath(data_path)
        Image_path = os.path.join(data_path, "Images")
        Annotations_path = os.path.join(data_path, "Annotations")
        Object_path = os.path.join(data_path, "SegmentationObject")
        Main_path = os.path.join(data_path, "ImageSets/Main")
        if os.path.exists(Main_path):
            shutil.rmtree(Main_path)
            self._save_index_file(data_path, Image_path)
        else:
            self._save_index_file(data_path, Image_path)
        if not os.path.exists(Object_path):
            raise ValueError(" SegObjection_path error")
        if not os.path.exists(Image_path):
            raise ValueError("Train Image_path error")
        if not os.path.exists(Annotations_path):
            raise ValueError("Train Annotations_path error")
        if not os.path.exists(Main_path):
            raise ValueError("txt path error")
        train_path_data = self.func_data_1(Object_path, Image_path, Annotations_path, (config.IMAGE_MIN_DIM), (config.IMAGE_MAX_DIM),
          image_suffix, txt_for_train_val="train")
        config.NUM_CLASSES = len(train_path_data[0][0]) + 1
        train_images = len(train_path_data) - 1
        val_data = self.func_data_1(Object_path, Image_path, Annotations_path, (config.IMAGE_MIN_DIM), (config.IMAGE_MAX_DIM),
          image_suffix, txt_for_train_val="val")
        dataset_train = ShapesDataset(train_path_data)
        dataset_train.load_shapes(train_images, config.IMAGE_SHAPE[0], config.IMAGE_SHAPE[1])
        dataset_train.prepare()
        dataset_val = ShapesDataset(val_data)
        dataset_val.load_shapes(50, config.IMAGE_SHAPE[0], config.IMAGE_SHAPE[1])
        dataset_val.prepare()
        return (dataset_train, dataset_val, train_images)

    def get_ax(self, rows=1, cols=1, size=8):
        """Return a Matplotlib Axes array to be used in
        all visualizations in the notebook. Provide a
        central point to control graph sizes.

        Change the default size attribute to control the size
        of rendered images
        返回要用于的Matplotlib轴数组
         笔记本中的所有可视化。 提供一个
         控制图形大小的中心点。

         更改默认大小属性以控制大小
         的渲染图像
        """
        _, ax = plt.subplots(rows, cols, figsize=(size * cols, size * rows))
        return ax

    def analyze_xml(self, file_name):
        """
        从xml文件中解析class，对象位置
        :param file_name: xml文件位置
        :return: class，每个类别的矩形位置
        """
        fp = open(file_name)
        class_name = []
        rectangle_position = []
        for p in fp:
            if "<object>" in p:
                class_name.append(next(fp).split(">")[1].split("<")[0])
            if "<bndbox>" in p:
                rectangle = []
                [rectangle.append(round(eval(next(fp).split(">")[1].split("<")[0]))) for _ in range(4)]
                rectangle_position.append(rectangle)

        fp.close()
        return (
         class_name, rectangle_position)

    def analyze_xml_class(self, file_names, class_name=[]):
        """解析xml的所有类别"""
        for file_name in file_names:
            with open(file_name) as fp:
                for p in fp:
                    if "<object>" in p:
                        class_name.append(next(fp).split(">")[1].split("<")[0])

    def resize_image(self, image, min_dim=None, max_dim=None, padding=False):
        """
        Resizes an image keeping the aspect ratio.
        min_dim: if provided, resizes the image such that it's smaller
            dimension == min_dim
        max_dim: if provided, ensures that the image longest side doesn't
            exceed this value.
        padding: If true, pads image with zeros so it's size is max_dim x max_dim
        Returns:
        image: the resized image
        window: (y1, x1, y2, x2). If max_dim is provided, padding might
            be inserted in the returned image. If so, this window is the
            coordinates of the image part of the full image (excluding
            the padding). The x2, y2 pixels are not included.
        scale: The scale factor used to resize the image
        padding: Padding added to the image [(top, bottom), (left, right), (0, 0)]
        """
        h, w = image.shape[None[:2]]
        window = (0, 0, h, w)
        scale = 1
        if min_dim:
            scale = max(1, min_dim / min(h, w))
        if max_dim:
            image_max = max(h, w)
            if round(image_max * scale) > max_dim:
                scale = max_dim / image_max
        if scale != 1:
            image = scipy.misc.imresize(image, (round(h * scale), round(w * scale)))
        if padding:
            h, w = image.shape[None[:2]]
            top_pad = (max_dim - h) // 2
            bottom_pad = max_dim - h - top_pad
            left_pad = (max_dim - w) // 2
            right_pad = max_dim - w - left_pad
            padding = [(top_pad, bottom_pad), (left_pad, right_pad), (0, 0)]
            image = np.pad(image, padding, mode="constant", constant_values=0)
            window = (top_pad, left_pad, h + top_pad, w + left_pad)
        return (
         image, window, scale, padding)

    def resize_mask(self, mask, scale, padding):
        """Resizes a mask using the given scale and padding.
        Typically, you get the scale and padding from resize_image() to
        ensure both, the image and the mask, are resized consistently.
        scale: mask scaling factor
        padding: Padding to add to the mask in the form
                [(top, bottom), (left, right), (0, 0)]
        """
        h, w = mask.shape[None[:2]]
        mask = scipy.ndimage.zoom(mask, zoom=[scale, scale, 1], order=0)
        mask = np.pad(mask, padding, mode="constant", constant_values=0)
        return mask

    def func_data_1(self, SegObject_path, Image_path, Annotations_path, IMAGE_MIN_DIM, IMAGE_MAX_DIM, image_suffix, txt_for_train_val=None):
        txt_path = None
        Object_path = []
        xml_path = []
        if txt_for_train_val == "train":
            txt_path = os.path.join(Image_path, "..", "ImageSets/Main", "train.txt")
        else:
            if txt_for_train_val == "val":
                txt_path = os.path.join(Image_path, "..", "ImageSets/Main", "val.txt")
            else:
                raise ValueError("没有找到划分训练集和验证集的txt文件")
        with open(txt_path, "r") as txt:
            lines = txt.readlines()
            for line in lines:
                line = line.strip("\n")
                line_p = os.path.join(SegObject_path, line + ".png")
                line_x = os.path.join(Annotations_path, line + ".xml")
                Object_path.append(line_p)
                xml_path.append(line_x)

        class_all_name = []
        self.analyze_xml_class(xml_path, class_all_name)
        class_set = set(class_all_name)
        if "" in class_set:
            class_set.remove("")
        elif "" in class_set:
            class_set.remove("")
        class_list = sorted(list(class_set))
        class_dict = dict(zip(class_list, range(1, len(class_list) + 1)))
        object_data = []
        object_data.append([class_dict])
        sp = None
        if platform.system() == "Windows":
            sp = "\\"
        else:
            sp = "/"
        if platform.system() == "Linux":
            process_num = 50
            loop_i = 0
            loop_num = len(Object_path) // 50
            all_result_processed = []
            from functools import partial
            fun_param = partial((self.load_train_data1), Image_path=Image_path, Annotations_path=Annotations_path, class_dict=class_dict,
              image_suffix=image_suffix,
              IMAGE_MIN_DIM=IMAGE_MIN_DIM,
              IMAGE_MAX_DIM=IMAGE_MAX_DIM,
              sp=sp)
            while loop_i < loop_num:
                _Object_path = Object_path[(loop_i * process_num)[:(loop_i + 1) * process_num]]
                result_process = self.batch_multiprocess(_Object_path, fun_param)
                all_result_processed = all_result_processed + result_process
                loop_i += 1

            if loop_num == 0:
                _Object_path = Object_path
            else:
                _Object_path = Object_path[(loop_i * process_num)[:None]]
            result_process = self.batch_multiprocess(_Object_path, fun_param)
            all_result_processed = all_result_processed + result_process
            random.shuffle(all_result_processed)
            all_result_processed.insert(0, [class_dict])
            return all_result_processed
        object_data = self.load_train_data(Image_path, Object_path, Annotations_path, object_data, class_dict, image_suffix, IMAGE_MIN_DIM, IMAGE_MAX_DIM, sp)
        return object_data

    def batch_multiprocess(self, _Object_path, fun_param):
        from multiprocessing import Pool
        process_number = max(self.config.BATCH_SIZE // 2, 2)
        pool = Pool(process_number)
        path_iter = self.iter_object_path(_Object_path)
        _result_process = pool.map(fun_param, path_iter)
        pool.close()
        pool.join()
        _result_process = list(filter(None, _result_process))
        result_process = _result_process[0]
        for iobj in range(1, len(_result_process)):
            result_process = result_process + _result_process[iobj]

        return result_process

    def iter_object_path(self, object_path):
        for i in object_path:
            yield i

    def load_train_data(self, Image_path, Object_path, Annotations_path, object_data, class_dict, image_suffix, IMAGE_MIN_DIM, IMAGE_MAX_DIM, sp):
        for num, path in enumerate(Object_path):
            sys.stdout.write("\r>> Converting image %d/%d" % (
             num + 1, len(Object_path)))
            sys.stdout.flush()
            file_name = path.split(sp)[-1].split(".")[0]
            Annotations_path_ = os.path.join(Annotations_path, file_name + ".xml")
            class_name, rectangle_position = self.analyze_xml(Annotations_path_)
            mask_1 = cv2.imread(path, 0)
            masks = []
            for rectangle in rectangle_position:
                xmin, ymin, xmax, ymax = (
                 rectangle[0], rectangle[1], rectangle[2], rectangle[3])
                if not xmin >= xmax:
                    if ymin >= ymax:
                        continue
                    mask = np.zeros_like(mask_1, np.uint8)
                    mask[(rectangle[1][:rectangle[3]], rectangle[0][:rectangle[2]])] = mask_1[(rectangle[1][:rectangle[3]],
                     rectangle[0][:rectangle[2]])]
                    mean_x = (rectangle[0] + rectangle[2]) // 2
                    mean_y = (rectangle[1] + rectangle[3]) // 2
                    end = min((mask.shape[1], round(rectangle[2]) + 1))
                    start = max((0, round(rectangle[0]) - 1))
                    flag = True
                    for i in range(mean_x, end):
                        x_ = i
                        y_ = mean_y
                        pixels = mask_1[(y_, x_)]
                        if pixels != 0 and pixels != 220:
                            mask = (mask == pixels).astype(np.uint8)
                            flag = False
                            break

                    if flag:
                        for i in range(mean_x, start, -1):
                            x_ = i
                            y_ = mean_y
                            pixels = mask_1[(y_, x_)]
                            if pixels != 0 and pixels != 220:
                                mask = (mask == pixels).astype(np.uint8)
                                break

                    masks.append(mask)

            try:
                masks = np.asarray(masks, np.uint8).transpose([1, 2, 0])
            except Exception as e:
                try:
                    if len(rectangle_position) == 0 or len(masks) == 0:
                        continue
                    else:
                        print("error file name {}".format(file_name))
                        raise ValueError(e)
                finally:
                    e = None
                    del e

            class_id = []
            [class_id.append(class_dict[i]) for i in class_name]
            class_id = np.asarray(class_id, np.uint8)
            image = cv2.imread(os.path.join(Image_path, file_name + image_suffix))
            object_data.append([image, masks, class_id])
            object_data = self.flip_augmentation(image, masks, class_id, object_data)

        return object_data

    def load_train_data1(self, path, Image_path, Annotations_path, class_dict, image_suffix, IMAGE_MIN_DIM, IMAGE_MAX_DIM, sp):
        """根据xml文件内的bbox,提取相应对象的mask"""
        object_list = []
        for i in range(1):
            file_name = path.split(sp)[-1].split(".")[0]
            Annotations_path_ = os.path.join(Annotations_path, file_name + ".xml")
            class_name, rectangle_position = self.analyze_xml(Annotations_path_)
            mask_1 = cv2.imread(path, 0)
            masks = []
            for rectangle in rectangle_position:
                xmin, ymin, xmax, ymax = (
                 rectangle[0], rectangle[1], rectangle[2], rectangle[3])
                if not xmin >= xmax:
                    if ymin >= ymax:
                        continue
                    mask = np.zeros_like(mask_1, np.uint8)
                    mask[(rectangle[1][:rectangle[3]], rectangle[0][:rectangle[2]])] = mask_1[(rectangle[1][:rectangle[3]],
                     rectangle[0][:rectangle[2]])]
                    mean_x = (rectangle[0] + rectangle[2]) // 2
                    mean_y = (rectangle[1] + rectangle[3]) // 2
                    end = min((mask.shape[1], round(rectangle[2]) + 1))
                    start = max((0, round(rectangle[0]) - 1))
                    flag = True
                    for i in range(mean_x, end):
                        x_ = i
                        y_ = mean_y
                        pixels = mask_1[(y_, x_)]
                        if pixels != 0 and pixels != 220:
                            mask = (mask == pixels).astype(np.uint8)
                            flag = False
                            break

                    if flag:
                        for i in range(mean_x, start, -1):
                            x_ = i
                            y_ = mean_y
                            pixels = mask_1[(y_, x_)]
                            if pixels != 0 and pixels != 220:
                                mask = (mask == pixels).astype(np.uint8)
                                break

                    masks.append(mask)

            try:
                masks = np.asarray(masks, np.uint8).transpose([1, 2, 0])
            except Exception as e:
                try:
                    if len(rectangle_position) == 0 or len(masks) == 0:
                        continue
                    else:
                        print("error file name {}".format(file_name))
                        raise ValueError(e)
                finally:
                    e = None
                    del e

            class_id = []
            [class_id.append(class_dict[i]) for i in class_name]
            class_id = np.asarray(class_id, np.uint8)
            image = cv2.imread(os.path.join(Image_path, file_name + image_suffix))
            object_list.append([image, masks, class_id])
            object_list = self.flip_augmentation(image, masks, class_id, object_list)
            return object_list

    def multiscale(self, image, masks, class_id, image_dim, object_data):
        scale = [
         384, 576, 768, 1024, 1216]
        for iscal in scale:
            if iscal != image_dim:
                image_scal = Resize(p=1, height=iscal, width=iscal)(image=image)["image"]
                masks_scal = Resize(p=1, height=iscal, width=iscal)(image=masks)["image"]
                object_data.append([image_scal, masks_scal, class_id])

        return object_data

    def flip_augmentation(self, image, masks, class_id, object_data):
        """简单的增强数据,避免反作用"""
        image_Ho = HorizontalFlip(p=1)(image=image)["image"]
        masks_Ho = HorizontalFlip(p=1)(image=masks)["image"]
        object_data.append([image_Ho, masks_Ho, class_id])
        image_Ve = VerticalFlip(p=1)(image=image)["image"]
        masks_Ve = VerticalFlip(p=1)(image=masks)["image"]
        object_data.append([image_Ve, masks_Ve, class_id])
        return object_data

    def check_mask_little(self, mask_resized, masks):
        delete_ind = []
        iq = mask_resized.shape[-1]
        for ia in range(mask_resized.shape[-1]):
            pp = mask_resized[(None[:None], None[:None], ia)].max()
            if pp < 1:
                delete_ind.append(ia)

        if len(delete_ind) > 0:
            mask_resized = np.delete(mask_resized, delete_ind, axis=2)
            masks = np.delete(masks, delete_ind, axis=2)
        iq1 = mask_resized.shape[-1]
        if iq - iq1 != len(delete_ind):
            raise ValueError("delete not equal")
        return (
         mask_resized, masks)

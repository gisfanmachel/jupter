# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\instance_segmentation\prediction_instance_seg.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 63488 bytes
import json, math, os, shutil, tempfile, cv2, numpy as np, rasterio, scipy, shutil, tensorflow as tf
from rasterio import features
from rasterio import transform as rio_transform
from rasterio.plot import reshape_as_image
from rasterio.windows import Window
from affine import Affine
import copy
from iobjectspy import DatasetType, FieldInfo, FieldType, Feature, Geometry
from iobjectspy.analyst import dissolve, compute_features_envelope, raster_to_vector
from iobjectspy.data import Dataset
from iobjectspy.conversion import import_tif
from . import utils
from toolkit._toolkit import view_bar, mkdir_not_exist, get_config_from_yaml
from _jsuperpy.data._util import check_output_datasource, get_output_datasource
from _jsuperpy.data.geo import GeoRegion
from .utils import compute_iou, compute_overlaps_masks, non_max_suppression, _save_xml, _save_segobject, create_sda_voc_mask, show_two_image

def cover_config(config, sdm_config):
    shape = sdm_config.model_input[0].shape
    config.IMAGE_MIN_DIM = shape[0]
    config.IMAGE_MAX_DIM = shape[1]
    config.NAME = sdm_config.name
    config.SIGNATURE_NAME = sdm_config.signature_name
    config.CATEGORYS = sdm_config.model_categorys
    config.NUM_CLASSES = len(config.CATEGORYS)
    MEAN_PIXEL = eval(sdm_config.mean_pixel)
    config.MEAN_PIXEL = MEAN_PIXEL


def mold_image(images, config):
    """Takes RGB images with 0-255 values and subtraces
    the mean pixel and converts it to float. Expects image
    colors in RGB order.
    """
    return images.astype(np.float32) - config.MEAN_PIXEL


def compose_image_meta(image_id, image_shape, window, active_class_ids):
    """Takes attributes of an image and puts them in one 1D array.
    image_id: An int ID of the image. Useful for debugging.
    image_shape: [height, width, channels]
    window: (y1, x1, y2, x2) in pixels. The area of the image where the real
            image is (excluding the padding)
    active_class_ids: List of class_ids available in the dataset from which
        the image came. Useful if training on images from multiple datasets
        where not all classes are present in all datasets.
    """
    meta = np.array([
     image_id] + list(image_shape) + list(window) + list(active_class_ids))
    return meta


def mold_inputs(config, images):
    """Takes a list of images and modifies them to the format expected
    as an input to the neural network.
    images: List of image matricies [height,width,depth]. Images can have
        different sizes.
    Returns 3 Numpy matricies:
    molded_images: [N, h, w, 3]. Images resized and normalized.
    image_metas: [N, length of meta data]. Details about each image.
    windows: [N, (y1, x1, y2, x2)]. The portion of the image that has the
        original image (padding excluded).
    """
    molded_images = []
    image_metas = []
    windows = []
    for image in images:
        molded_image, window, scale, padding = utils.resize_image(image,
          min_dim=(config.IMAGE_MIN_DIM),
          max_dim=(config.IMAGE_MAX_DIM),
          padding=(config.IMAGE_PADDING))
        molded_image = mold_image(molded_image, config)
        image_meta = compose_image_meta(0, image.shape, window, np.zeros([config.NUM_CLASSES], dtype=(np.int32)))
        molded_images.append(molded_image)
        windows.append(window)
        image_metas.append(image_meta)

    molded_images = np.stack(molded_images)
    image_metas = np.stack(image_metas)
    windows = np.stack(windows)
    return (molded_images, image_metas, windows)


def cal_config(config):
    scale = 1024 // config.IMAGE_MAX_DIM
    config.RPN_ANCHOR_SCALES = (
     32 // scale, 64 // scale, 128 // scale, 256 // scale, 512 // scale)
    config.RPN_TRAIN_ANCHORS_PER_IMAGE = 256 // scale
    config.MINI_MASK_SHAPE = (
     56 // scale, 56 // scale)
    config.TRAIN_ROIS_PER_IMAGE = 200 // scale
    config.DETECTION_MAX_INSTANCES = 100 * scale * 2 // 3


def unmold_detections(detections, mrcnn_mask, image_shape, window):
    """Reformats the detections of one image from the format of the neural
    network output to a format suitable for use in the rest of the
    application.
    detections: [N, (y1, x1, y2, x2, class_id, score)]
    mrcnn_mask: [N, height, width, num_classes]
    image_shape: [height, width, depth] Original size of the image before resizing
    window: [y1, x1, y2, x2] Box in the image where the real image is
            excluding the padding.
    Returns:
    boxes: [N, (y1, x1, y2, x2)] Bounding boxes in pixels
    class_ids: [N] Integer class IDs for each bounding box
    scores: [N] Float probability scores of the class_id
    masks: [height, width, num_instances] Instance masks
    """
    zero_ix = np.where(detections[(None[:None], 4)] == 0)[0]
    N = zero_ix[0] if zero_ix.shape[0] > 0 else detections.shape[0]
    boxes = detections[(None[:N], None[:4])]
    class_ids = detections[(None[:N], 4)].astype(np.int32)
    scores = detections[(None[:N], 5)]
    masks = mrcnn_mask[(np.arange(N), None[:None], None[:None], class_ids)]
    h_scale = image_shape[0] / (window[2] - window[0])
    w_scale = image_shape[1] / (window[3] - window[1])
    scale = min(h_scale, w_scale)
    shift = window[None[:2]]
    scales = np.array([scale, scale, scale, scale])
    shifts = np.array([shift[0], shift[1], shift[0], shift[1]])
    boxes = np.multiply(boxes - shifts, scales).astype(np.int32)
    exclude_ix = np.where((boxes[(None[:None], 2)] - boxes[(None[:None], 0)]) * (boxes[(None[:None], 3)] - boxes[(None[:None], 1)]) <= 0)[0]
    if exclude_ix.shape[0] > 0:
        boxes = np.delete(boxes, exclude_ix, axis=0)
        class_ids = np.delete(class_ids, exclude_ix, axis=0)
        scores = np.delete(scores, exclude_ix, axis=0)
        masks = np.delete(masks, exclude_ix, axis=0)
        N = class_ids.shape[0]
    full_masks = []
    for i in range(N):
        full_mask = utils.unmold_mask(masks[i], boxes[i], image_shape)
        full_masks.append(full_mask)

    full_masks = np.stack(full_masks, axis=(-1)) if full_masks else np.empty((0, ) + masks.shape[1[:3]])
    return (
     boxes, class_ids, scores, full_masks)


class infer_config:
    IMAGE_MIN_DIM = 512
    IMAGE_MAX_DIM = 512
    IMAGE_PADDING = True
    NUM_CLASSES = 2
    MEAN_PIXEL = [81.8, 91.3, 86]
    CATEGORYS = ["UU", "building"]

    def display(self):
        """Display Configuration values."""
        print("\nConfigurations:")
        for a in dir(self):
            if not a.startswith("__"):
                callable(getattr(self, a)) or print("{:30} {}".format(a, getattr(self, a)))

        print("\n")


class Mask_Rcnn_Prediction:

    def __init__(self, model_path):
        self.config = None
        self.score_thresh = None
        self.input_data = None
        self.output_data_path = None
        self.out_dataset_name = None
        self.return_bbox = False
        self.model_path = model_path
        self.load_model()

    def infer_geo_image(self, input_img, sdm_config, out_data, out_dataset_name, score_thresh, nms_thresh, return_bbox=False):
        self.init_input_params(input_img, sdm_config, out_data, out_dataset_name, score_thresh, nms_thresh, return_bbox=return_bbox)
        geo_image_output = self.do_prediction(image_path=input_img)
        return geo_image_output

    def init_input_params(self, input_data, sdm_config, out_data, out_dataset_name, score_thresh, nms_thresh, return_bbox=False):
        self.input_data = input_data
        self.config = infer_config()
        cover_config(self.config, sdm_config)
        self.output_data_path = out_data
        self.out_dataset_name = out_dataset_name
        self.score_thresh = score_thresh
        self.nms_thresh = nms_thresh
        self.return_bbox = return_bbox

    def load_model(self):
        """
        加载模型，这一步只跟model_path有关，与其他参数无关
        """
        if not os.path.isdir(self.model_path):
            raise ValueError("there is no file in the path {}".format(self.model_path))
        tf_config = tf.ConfigProto()
        tf_config.gpu_options.allow_growth = True
        self.sess = tf.Session(config=tf_config)
        signature_key = "predict"
        self.meta_graph_def = tf.saved_model.loader.load(self.sess, [tf.saved_model.tag_constants.SERVING], self.model_path)
        self.signature = self.meta_graph_def.signature_def
        input_image_name = self.signature[signature_key].inputs["input_image"].name
        input_image_meta_name = self.signature[signature_key].inputs["input_image_meta"].name
        detections_name = self.signature[signature_key].outputs["detections"].name
        mrcnn_class_name = self.signature[signature_key].outputs["mrcnn_class"].name
        mrcnn_bbox_name = self.signature[signature_key].outputs["mrcnn_bbox"].name
        mrcnn_mask_name = self.signature[signature_key].outputs["mrcnn_mask"].name
        roi_name = self.signature[signature_key].outputs["roi"].name
        rpn_class_name = self.signature[signature_key].outputs["rpn_class"].name
        rpn_bbox_name = self.signature[signature_key].outputs["rpn_bbox"].name
        self.input_image = self.sess.graph.get_tensor_by_name(input_image_name)
        self.input_image_meta = self.sess.graph.get_tensor_by_name(input_image_meta_name)
        self.detections = self.sess.graph.get_tensor_by_name(detections_name)
        self.rpn_class = self.sess.graph.get_tensor_by_name(rpn_class_name)
        self.rpn_bbox = self.sess.graph.get_tensor_by_name(rpn_bbox_name)
        self.roi = self.sess.graph.get_tensor_by_name(roi_name)
        self.mrcnn_class = self.sess.graph.get_tensor_by_name(mrcnn_class_name)
        self.mrcnn_bbox = self.sess.graph.get_tensor_by_name(mrcnn_bbox_name)
        self.mrcnn_mask = self.sess.graph.get_tensor_by_name(mrcnn_mask_name)

    def close_model(self):
        """
        关闭模型
        :return:
        """
        self.sess.close()
        tf.reset_default_graph()

    def infer_smallsize(self, ds, pic_path=None, is_geo_image=True, application='train'):
        """
        预测小幅影像或图片
        is_geo_image: bool；是否为带地理坐标的数据
        """
        if is_geo_image:
            view_bar(0, 1)
        else:
            img = ds.read(window=(Window(0, 0, ds.width, ds.height)))
            block = np.zeros([3, ds.height, ds.width], dtype=(np.uint8))
            block[(None[:None], None[:img.shape[1]], None[:img.shape[2]])] = img[(None[:3], None[:None], None[:None])]
            image = reshape_as_image(block)
            transform = ds.transform
            class_names = self.config.CATEGORYS
            alclass_ids = []
            alleups = []
            all_rois = []
            all_scores = []
            final_masks, final_class_ids, final_scores, final_rois = self.get_model_output(image)
            if is_geo_image:
                view_bar(1, 1)
            if len(final_rois) > 0:
                alleups.append(np.array([[0, 0]] * len(final_scores)))
                almasks = final_masks.transpose([2, 0, 1])
                alclass_ids.append(final_class_ids)
                all_rois.append(final_rois)
                all_scores.append(final_scores)
                if is_geo_image:
                    output_dataset_name = nms_all_output(all_rois, almasks, all_scores, alclass_ids, alleups, transform, class_names,
                      (self.output_data_path), (self.out_dataset_name), (self.nms_thresh),
                      return_bbox=(self.return_bbox))
                    return output_dataset_name
                extra_rois, extra_class_ids, whole_mask = self.process_large_output(all_rois, almasks, all_scores, alclass_ids,
                  alleups,
                  (self.nms_thresh), (ds.height), (ds.width),
                  small_size=True)
                result_path = self.save_pic_out(extra_rois, extra_class_ids, whole_mask, pic_path, application)
                self.tile_size_x.append(ds.width)
                self.tile_size_y.append(ds.height)
                self.get_image_mean_pixel(image)
                return result_path
            else:
                print("There is no object in the image")

    def infer_large(self, ds, is_geo_image=True, overlap_offset=0):
        transform = ds.transform
        if ds.crs is None:
            transform = Affine(transform[0], transform[1], transform[2], transform[3], -transform[4], ds.height)
        IMAGE_MIN_DIM = self.config.IMAGE_MIN_DIM
        IMAGE_MAX_DIM = self.config.IMAGE_MAX_DIM
        block_hh = IMAGE_MIN_DIM
        block_ww = IMAGE_MIN_DIM
        overlap_offset = self.config.IMAGE_MIN_DIM // 2
        next_w = block_ww - overlap_offset
        next_h = block_hh - overlap_offset
        width_block = math.ceil((ds.width - block_ww) / next_w) + 1
        height_block = math.ceil((ds.height - block_hh) / next_h) + 1
        almasks = []
        alclass_ids = []
        alleups = []
        al_rois = []
        al_scores = []
        block_now = 0
        block_all = height_block * width_block
        for ph in range(height_block):
            start_h = ph * next_h
            if start_h + block_hh > ds.height:
                if ds.height <= block_hh:
                    start_h = 0
                    block_hh = ds.height
                else:
                    start_h = ds.height - block_hh
            for pw in range(width_block):
                start_le_up = (
                 pw * next_w, start_h)
                if pw * next_w + block_ww > ds.width:
                    if ds.width <= block_ww:
                        start_le_up = (
                         0, start_h)
                        block_ww = ds.width
                    else:
                        start_le_up = (
                         ds.width - block_ww, start_h)
                block_now += 1
                if is_geo_image:
                    view_bar(block_now, block_all)
                img = ds.read(window=(Window(start_le_up[0], start_le_up[1], block_ww, block_hh)))
                block = np.zeros([3, block_hh, block_ww], dtype=(np.uint8))
                block[(None[:None], None[:img.shape[1]], None[:img.shape[2]])] = img[(None[:3], None[:None], None[:None])]
                image = reshape_as_image(block)
                final_masks, final_class_ids, final_scores, final_rois = self.get_model_output(image)
                if len(final_rois) > 0:
                    final_rois[(None[:None], [0, 2])] = final_rois[(None[:None], [0, 2])] + start_le_up[1]
                    final_rois[(None[:None], [1, 3])] = final_rois[(None[:None], [1, 3])] + start_le_up[0]
                    alclass_ids.append(final_class_ids)
                    al_rois.append(final_rois)
                    al_scores.append(final_scores)
                    alleups.append(np.array([[start_le_up[0], start_le_up[1]]] * len(final_scores)))
                    for imm in range(len(final_scores)):
                        almasks.append(final_masks[(None[:None], None[:None], imm)])

        return (
         al_rois, almasks, al_scores, alclass_ids, alleups, transform)

    def infer_large_smooth(self, ds, pic_path=None, is_geo_image=True, application='train', overlap_offset=0):
        """
        推理大幅的影像或者图片
        is_geo_image: bool；是否为带地理坐标的数据
        """
        al_rois, almasks, al_scores, alclass_ids, alleups, transform = self.infer_large(ds, is_geo_image=is_geo_image)
        class_names = self.config.CATEGORYS
        if len(alleups) != 0:
            if is_geo_image:
                output_dataset_name = nms_all_output(al_rois, almasks, al_scores, alclass_ids, alleups, transform, class_names,
                  (self.output_data_path), (self.out_dataset_name), (self.nms_thresh),
                  return_bbox=(self.return_bbox))
                return output_dataset_name
            extra_rois, extra_class_ids, whole_mask = self.process_large_output(al_rois, almasks, al_scores, alclass_ids, alleups, self.nms_thresh, ds.height, ds.width)
            result_path = self.save_pic_out(extra_rois, extra_class_ids, whole_mask, pic_path, application)
            img = ds.read(window=(Window(0, 0, ds.width, ds.height)))
            self.tile_size_x.append(ds.width)
            self.tile_size_y.append(ds.height)
            block = np.zeros([3, ds.height, ds.width], dtype=(np.uint8))
            block[(None[:None], None[:img.shape[1]], None[:img.shape[2]])] = img[(None[:3], None[:None], None[:None])]
            image = reshape_as_image(block)
            self.get_image_mean_pixel(image)
            return result_path
        else:
            print("There is no object in the image")

    def process_large_output(self, all_rois, all_masks, all_scores, all_class_ids, all_leups, nms_thresh, raw_height, raw_width, small_size=False):
        """
                对预测结果进行nms,将推理结果处理，bbox去重，mask映射到原图上。对于大图和小图都适用
                        all_rois：一维列表，列表内每个单元存储每个block预测结果的最小外接矩形
                        all_masks：一维列表，列表内每个单元存储单个对象的mask，与all_rois内bbox的顺序一致
                        all_scores：一维列表，列表内每个单元存储每个block预测结果的所有分数值
                        all_class_ids：一维列表，列表内每个单元存储每个block预测结果的所有类别代码
                        all_leups：一维列表，列表内每个单元存储所预测block在原图上的左上角点像素坐标（多个相同的点）
        """
        infer_block_size = self.config.IMAGE_MIN_DIM
        extra_rois, extra_masks, extra_class_ids, extra_scores, extra_leups = nms_large_output(all_rois, all_masks, all_scores, all_class_ids, all_leups, nms_thresh)
        whole_mask = np.zeros(shape=(raw_height, raw_width), dtype=(np.uint8))
        if small_size:
            for num_mask in range(len(extra_leups)):
                whole_mask += extra_masks[num_mask] * (num_mask + 1)

            return (extra_rois, extra_class_ids, whole_mask)
        for num_mask in range(len(extra_leups)):
            col, raw = extra_leups[num_mask]
            try:
                whole_mask[(raw[:raw + infer_block_size], col[:col + infer_block_size])] += extra_masks[num_mask] * (num_mask + 1)
            except:
                if raw + infer_block_size == whole_mask.shape[0] and col + infer_block_size == whole_mask.shape[1]:
                    whole_mask[(raw[:None], col[:None])] += extra_masks[num_mask] * (num_mask + 1)
                else:
                    if raw + infer_block_size == whole_mask.shape[0]:
                        whole_mask[(raw[:None], col[:col + infer_block_size])] += extra_masks[num_mask] * (num_mask + 1)
                    else:
                        if col + infer_block_size == whole_mask.shape[1]:
                            whole_mask[(raw + infer_block_size, col[:None])] += extra_masks[num_mask] * (num_mask + 1)

        return (
         extra_rois, extra_class_ids, whole_mask)

    def save_pic_out(self, rois, class_ids, whole_mask, pic_path, application='train'):
        """
        rois: [[], [], []]
        class_ids: [ , , ,]
        whole_mask: 二维的array
        applicaton: train时，所有推理结果都在指定路径下的Annotation和SegmentationObject下；display时，只保存按输入目录的文件结构只保存mask
        仅处理一张图片的推理结果，将处理后的bbox和mask存入Annotations下的xml文件和SegmentationObject下的png文件
        """
        if application == "train":
            img_shape = whole_mask.shape
            difficult_value = np.zeros(shape=(len(rois)))
            xml_array = np.insert(rois, 4, class_ids, axis=1)
            xml_array = np.insert(xml_array, 5, difficult_value, axis=1)
            xml_list = xml_array.tolist()
            xml_path = os.path.join(self.output_data_path, "Annotations")
            _save_xml(output_path_label=xml_path, pic_name=(self.out_dataset_name), lists=xml_list, width=(img_shape[1]),
              height=(img_shape[0]),
              depth=3,
              class_names=(self.config.CATEGORYS))
            seg_path = os.path.join(self.output_data_path, "SegmentationObject")
            seg_name = self.out_dataset_name + ".png"
            seg_path = os.path.join(seg_path, seg_name)
            _save_segobject(image=whole_mask, output_segobject=seg_path, num_color_id=(len(rois)))
            out_image_name = self.out_dataset_name + ".jpg"
            out_image_path = os.path.join(self.output_data_path, "Images", out_image_name)
            shutil.copy(pic_path, out_image_path)
        else:
            if application == "display":
                seg_name = self.out_dataset_name.split(".")[0] + ".png"
                seg_path = os.path.join(self.output_data_path, seg_name)
                _save_segobject(image=whole_mask, output_segobject=seg_path, num_color_id=(len(rois)))
            return self.output_data_path

    def get_model_output(self, image):
        """
        输入带推理的array
        返回置信区间之上的推理结果：掩码，类别id,可信度，掩码的最小外接矩形
        """
        molded_images, image_metas, windows = mold_inputs(self.config, [image])
        detections, mrcnn_class, mrcnn_bbox, mrcnn_mask, rois, rpn_class, rpn_bbox = self.sess.run((self.detections, self.mrcnn_class, self.mrcnn_bbox, self.mrcnn_mask,
         self.roi, self.rpn_class, self.rpn_bbox),
          feed_dict={(self.input_image): molded_images, (self.input_image_meta): image_metas})
        final_rois, final_class_ids, final_scores, final_masks = unmold_detections(detections[0], mrcnn_mask[0], image.shape, windows[0])
        low_score_inds = np.where(final_scores < self.score_thresh)[0]
        final_scores = np.delete(final_scores, low_score_inds, axis=0)
        final_rois = np.delete(final_rois, low_score_inds, axis=0)
        final_class_ids = np.delete(final_class_ids, low_score_inds, axis=0)
        final_masks = np.delete(final_masks, low_score_inds, axis=2)
        return (
         final_masks, final_class_ids, final_scores, final_rois)

    def infer_pic_only(self, pic_path):
        """
        仅推理单张图片，大小图片皆适用
        """
        drop_offset = 50
        IMAGE_MIN_DIM = self.config.IMAGE_MIN_DIM
        IMAGE_MAX_DIM = self.config.IMAGE_MAX_DIM
        try:
            ds = rasterio.open(pic_path)
        except:
            print("the picture path {} can't be opended by rasterio".format(pic_path))
            return
            if ds.width >= IMAGE_MIN_DIM * 1.2 or ds.height >= IMAGE_MIN_DIM * 1.2:
                result_path = self.infer_large_smooth(ds, pic_path=pic_path, is_geo_image=False)
            else:
                result_path = self.infer_smallsize(ds, pic_path=pic_path, is_geo_image=False)
            return result_path

    def infer_pic_dir(self, image_path_list, input_data, sdm_config, output_data_path, out_dataset_name, score_thresh, nms_thresh, return_bbox=False, application='train'):
        """
        推理单张图片或者整个文件夹内图片
        """
        self.init_input_params(input_data, sdm_config, output_data_path, out_dataset_name, score_thresh, nms_thresh,
          return_bbox=return_bbox)
        all_num = len(image_path_list)
        self.per_image_Rmean = []
        self.per_image_Gmean = []
        self.per_image_Bmean = []
        self.tile_size_x = []
        self.tile_size_y = []
        if os.path.isdir(input_data):
            result_path = None
            if application == "train":
                Annotations_path = os.path.join(output_data_path, "Annotations")
                SegmentationObject_path = os.path.join(output_data_path, "SegmentationObject")
                Images_path = os.path.join(output_data_path, "Images")
                mkdir_not_exist([Annotations_path, SegmentationObject_path, Images_path])
                sda_name = os.path.basename(output_data_path) + ".sda"
                sda_path = os.path.join(output_data_path, sda_name)
                if os.path.isfile(sda_path):
                    sda_last = get_config_from_yaml(sda_path)
                    index_last = sda_last.dataset.image_count
                else:
                    index_last = 0
            else:
                for num in range(len(image_path_list)):
                    view_bar(num + 1, all_num)
                    pic_path = image_path_list[num]
                    index_now = index_last + num
                    index_now = "%08d" % index_now
                    self.out_dataset_name = index_now
                    result_path = self.infer_pic_only(pic_path)

                image_count = len(self.per_image_Rmean)
                R_mean, G_mean, B_mean = self.get_mean_pixel()
                image_mean = [R_mean, G_mean, B_mean]
                tile_x, tile_y = int(np.mean(self.tile_size_x)), int(np.mean(self.tile_size_y))
                if os.path.isfile(sda_path):
                    image_mean = np.array([R_mean, G_mean, B_mean])
                    image_last_RGB_mean_pixel = np.array(sda_last.dataset.image_mean)
                    image_mean = (index_last * image_last_RGB_mean_pixel + image_count * image_mean) / (index_last + image_count)
                    image_mean = np.round(image_mean, decimals=6).tolist()
                    image_count = index_last + image_count
                    last_category = sda_last.dataset.classes
                    for class_name in self.config.CATEGORYS:
                        if class_name not in last_category:
                            last_category.append(class_name)

                    create_sda_voc_mask(last_category, image_count, tile_x, tile_y, image_mean, tile_format="jpg", output_path=sda_path)
                else:
                    create_sda_voc_mask((self.config.CATEGORYS), image_count, tile_x, tile_y, image_mean, tile_format="jpg",
                      output_path=sda_path)
        else:
            if application == "display":
                SegmentationObject_path = os.path.join(output_data_path, "SegmentationObject")
                mkdir_not_exist([SegmentationObject_path])
                for num in range(len(image_path_list)):
                    view_bar(num, all_num)
                    pic_path = image_path_list[num]
                    image_name = os.path.basename(pic_path)
                    self.output_data_path = self.output_data_path.replace(self.input_data, self.output_data_path)
                    self.out_dataset_name = image_name
                    result_path = self.infer_pic_only(pic_path)

            return result_path
            view_bar(0, 1)
            Annotations_path = os.path.join(output_data_path, "Annotations")
            SegmentationObject_path = os.path.join(output_data_path, "SegmentationObject")
            mkdir_not_exist([Annotations_path, SegmentationObject_path])
            if self.out_dataset_name is None:
                self.out_dataset_name = os.path.basename(input_data)
            result_path = self.infer_pic_only(image_path_list[0])
            view_bar(1, 1)
            return result_path

    def infer_large_smooth_mask(self, ds, overlap_offset=0):
        transform = ds.transform
        output_dataset_name = None
        class_names = self.config.CATEGORYS
        IMAGE_MIN_DIM = self.config.IMAGE_MIN_DIM
        IMAGE_MAX_DIM = self.config.IMAGE_MAX_DIM
        block_hh = IMAGE_MIN_DIM
        block_ww = IMAGE_MIN_DIM
        overlap_offset = self.config.IMAGE_MIN_DIM // 2
        next_w = block_ww - overlap_offset
        next_h = block_hh - overlap_offset
        width_block = math.ceil((ds.width - block_ww) / next_w) + 1
        height_block = math.ceil((ds.height - block_hh) / next_h) + 1
        almasks = []
        alclass_ids = []
        alleups = []
        block_now = 0
        block_all = height_block * width_block
        for ph in range(height_block):
            start_h = ph * next_h
            if start_h + block_hh > ds.height:
                if ds.height <= block_hh:
                    start_h = 0
                    block_hh = ds.height
                else:
                    start_h = ds.height - block_hh
            for pw in range(width_block):
                start_le_up = (
                 pw * next_w, start_h)
                if pw * next_w + block_ww > ds.width:
                    if ds.width <= block_ww:
                        start_le_up = (
                         0, start_h)
                        block_ww = ds.width
                    else:
                        start_le_up = (
                         ds.width - block_ww, start_h)
                block_now += 1
                view_bar(block_now, block_all)
                img = ds.read(window=(Window(start_le_up[0], start_le_up[1], block_ww, block_hh)))
                block = np.zeros([3, block_hh, block_ww], dtype=(np.uint8))
                block[(None[:None], None[:img.shape[1]], None[:img.shape[2]])] = img[(None[:3], None[:None], None[:None])]
                image = reshape_as_image(block)
                final_masks, final_class_ids, final_scores, final_rois = self.get_model_output(image)
                if len(final_rois) > 0:
                    final_rois[(None[:None], [0, 2])] = final_rois[(None[:None], [0, 2])] + start_le_up[1]
                    final_rois[(None[:None], [1, 3])] = final_rois[(None[:None], [1, 3])] + start_le_up[0]
                    alleups.append([start_le_up[0], start_le_up[1]])
                    almasks.append(final_masks)
                    alclass_ids.append(final_class_ids)

        if len(alleups) != 0:
            output_dataset_name = self.merge_mask(almasks, alleups, alclass_ids, class_names, transform, (self.output_data_path),
              (self.out_dataset_name),
              ds,
              block_hh, block_ww, return_bbox=(self.return_bbox))
        else:
            print("There is no object in the image")
        return output_dataset_name

    def merge_block_mask_class(self, final_masks, final_class_ids, class_id, block_shape):
        class_mask = np.zeros(shape=block_shape)
        cls_inds = np.where(final_class_ids == class_id)[0]
        if len(cls_inds) > 0:
            cls_masks = final_masks[(None[:None], None[:None], cls_inds)]
            for ia in range(len(cls_masks[(0, 0, None[:None])])):
                class_mask = class_mask + cls_masks[(None[:None], None[:None], ia)]

            return class_mask
        return

    def merge_mask(self, almasks, alleups, alclass_ids, class_names, transform, out_data, out_dataset_name, ds, block_h, block_w, return_bbox):
        """
        将预测结果按类投射到不同的二维数组上，重叠处的最终结果会是每次重叠像素相加的累加结果之和，
        所以最后会对这个二维数组上像素值非零且与这个类别分配到的像素值不同的区域都改成分配到的像素值（即[0,k,l1,l2,l3],会最终变为[0,k]）
        最后多个二维数组在投射到一张全为0的二维数组上，执行上述逻辑，
        最后由此生成临时数据tif转成矢量，对矢量结果融合，根据return_bbox值决定是否生成最小外接矩形

        almasks：一维列表，列表内每个单元存储每个block预测结果的masks
        alleups：一维列表，列表内每个单元存储所预测block在原图上的左上角点像素坐标（一个block共用一个点）
        alclass_ids：一维列表，列表内每个单元存储每个block预测结果的所有类别代码

        """
        all_tifs = []
        for it in range(len(class_names)):
            all_tifs.append(np.zeros(shape=(ds.height, ds.width)))

        tif_dtype = str(all_tifs[0].dtype)
        for ia in range(len(alleups)):
            blo_masks = almasks[ia]
            leup = alleups[ia]
            cls_ids = list(set(alclass_ids[ia]))
            cls_ids.sort()
            left_end = leup[0] + block_w
            up_end = leup[1] + block_h
            for ic in range(len(cls_ids)):
                id = cls_ids[ic]
                mask0 = self.merge_block_mask_class(blo_masks, alclass_ids[ia], id, (block_h, block_w))
                all_tifs[id][(leup[1][:up_end], leup[0][:left_end])] = all_tifs[id][(leup[1][:up_end], leup[0][:left_end])] + mask0

        whole_mask = all_tifs[0]
        for ie in range(1, len(class_names)):
            all_tifs[ie][all_tifs[ie] > 0] = ie
            whole_mask = whole_mask + all_tifs[ie]

        whole_mask[whole_mask >= len(class_names)] = 0
        tif_path = tempfile.mkdtemp()
        tif_name = os.path.join(tif_path, "mask1.tif")
        speci_value = tuple([ig for ig in range(1, len(class_names))])
        img_f = rasterio.open(tif_name, "w", driver="GTiff", height=(whole_mask.shape[0]), width=(whole_mask.shape[1]),
          count=1,
          dtype=tif_dtype,
          transform=transform)
        img_f.write(whole_mask, 1)
        img_f.close()
        ds = get_output_datasource(out_data)
        check_output_datasource(ds)
        tif_dataset = import_tif(tif_name, output=ds, out_dataset_name="mask_tif", is_import_as_grid=True)
        vector = raster_to_vector((ds[tif_dataset[0]]), back_or_no_value=0, out_data=ds, out_dataset_type=(DatasetType.REGION),
          out_dataset_name="mask_vector",
          value_field="mask_value")
        dissolve_mask = dissolve(vector, dissolve_type="SINGLE", dissolve_fields="SmUserID", out_dataset_name=out_dataset_name)
        ds.delete(tif_dataset[0])
        ds.delete("mask_vector")
        shutil.rmtree(tif_path)
        if return_bbox:
            nb = compute_features_envelope(dissolve_mask, out_data=ds, out_dataset_name=(out_dataset_name + str("_bbox")))
        return out_dataset_name

    def do_prediction(self, image_path):
        drop_offset = 50
        IMAGE_MIN_DIM = self.config.IMAGE_MIN_DIM
        IMAGE_MAX_DIM = self.config.IMAGE_MAX_DIM
        try:
            ds = rasterio.open(image_path)
        except:
            raise ValueError("rasterio can't open this file")

        if ds.width >= IMAGE_MIN_DIM * 1.2 or ds.height >= IMAGE_MIN_DIM * 1.2:
            output_dataset_name = self.infer_large_smooth(ds)
        else:
            output_dataset_name = self.infer_smallsize(ds)
        return output_dataset_name

    def get_image_mean_pixel(self, image):
        self.per_image_Rmean.append(np.mean(image[(None[:None], None[:None], 0)]))
        self.per_image_Gmean.append(np.mean(image[(None[:None], None[:None], 1)]))
        self.per_image_Bmean.append(np.mean(image[(None[:None], None[:None], 2)]))

    def get_mean_pixel(self):
        R_mean = eval(format(np.mean(self.per_image_Rmean), ".6f"))
        G_mean = eval(format(np.mean(self.per_image_Gmean), ".6f"))
        B_mean = eval(format(np.mean(self.per_image_Bmean), ".6f"))
        return (
         R_mean, G_mean, B_mean)


def nms_large_output(all_rois, all_masks, all_scores, all_class_ids, all_leups, nms_thresh):
    """
        对预测结果进行nms,相关的结果除mask是列表中顺序存储多个对象mask，其他都与模型的直接输出形式无异
                all_rois：一维列表，列表内每个单元存储每个block预测结果的最小外接矩形
                all_masks：一维列表，列表内每个单元存储单个对象的mask，与all_rois内bbox的顺序一致
                all_scores：一维列表，列表内每个单元存储每个block预测结果的所有分数值
                all_class_ids：一维列表，列表内每个单元存储每个block预测结果的所有类别代码
                all_leups：一维列表，列表内每个单元存储所预测block在原图上的左上角点像素坐标（多个相同的点）
    """
    rois = all_rois[0]
    class_ids = all_class_ids[0]
    scores = all_scores[0]
    leups = all_leups[0]
    for ia in range(1, len(all_scores)):
        rois = np.append(rois, (all_rois[ia]), axis=0)
        class_ids = np.append(class_ids, (all_class_ids[ia]), axis=0)
        scores = np.append(scores, (all_scores[ia]), axis=0)
        leups = np.append(leups, (all_leups[ia]), axis=0)

    pick_inds = non_max_suppression(rois, scores, threshold=nms_thresh)
    pick_inds.sort()
    extra_rois = rois[pick_inds]
    extra_rois = extra_rois.astype(np.float64)
    extra_scores = scores[pick_inds]
    extra_class_ids = class_ids[pick_inds]
    extra_leups = leups[pick_inds]
    extra_masks = [all_masks[i_m] for i_m in pick_inds]
    return (
     extra_rois, extra_masks, extra_class_ids, extra_scores, extra_leups)


def nms_all_output(all_rois, all_masks, all_scores, all_class_ids, all_leups, transform, class_names, out_data_location, out_dataset_name, nms_thresh, return_bbox=False):
    """
    对预测结果进行nms后转为georegion对象存入udbx中
            all_rois：一维列表，列表内每个单元存储每个block预测结果的最小外接矩形
            all_masks：一维列表，列表内每个单元存储单个对象的mask，与all_rois内bbox的顺序一致
            all_scores：一维列表，列表内每个单元存储每个block预测结果的所有分数值
            all_class_ids：一维列表，列表内每个单元存储每个block预测结果的所有类别代码
            all_leups：一维列表，列表内每个单元存储所预测block在原图上的左上角点像素坐标（多个相同的点）
    """
    extra_rois, extra_masks, extra_class_ids, extra_scores, extra_leups = nms_large_output(all_rois, all_masks, all_scores, all_class_ids, all_leups, nms_thresh)
    extra_rois, extra_scores, extra_class_ids, masks_processed = geo_process_masks_smooth_no_pinjie(extra_rois, extra_masks, extra_scores, extra_class_ids, transform, extra_leups)
    output_dataset_name = save_udb(transform, extra_rois, masks_processed, extra_scores, extra_class_ids, class_names, out_data_location,
      out_dataset_name, return_bbox=return_bbox)
    return output_dataset_name


def geo_process_masks_smooth_no_pinjie(rois, masks, scores, class_ids, transform, leups):
    mask_num = len(leups)
    masks_process = [None] * mask_num
    problem_mk = []
    for mnum in range(mask_num):
        mask_c = masks[mnum]
        leup = leups[mnum]
        x, y = rio_transform.xy(transform, leup[1], leup[0])
        tile_transform = rio_transform.from_origin(x, y, transform[0], -transform[4])
        con_ck = features.shapes(mask_c, mask=(mask_c.astype(np.bool)), transform=tile_transform)
        point_num = 0
        con_c = None
        select_ind = 0
        try:
            _con_c = next(con_ck)[0]
            ind_cal = 0
            while True:
                if len(_con_c["coordinates"][0]) > point_num:
                    point_num = len(_con_c["coordinates"][0])
                    con_c = copy.deepcopy(_con_c)
                    select_ind = ind_cal
                else:
                    try:
                        _con_c = next(con_ck)[0]
                        ind_cal += 1
                    except Exception as e:
                        try:
                            break
                        finally:
                            e = None
                            del e

            if con_c == None:
                raise ValueError("there is no closed polygon in the mask")
            json_shp = json.dumps(con_c)
            region_shp = Geometry.from_geojson(json_shp)
            masks_process[mnum] = region_shp
        except Exception as e:
            try:
                raise ValueError(e)
            finally:
                e = None
                del e

    all_inds = np.array([x for x in range(len(scores))])
    all_inds = np.delete(all_inds, problem_mk, axis=0)
    rois = rois[all_inds]
    scores = scores[all_inds]
    class_ids = class_ids[all_inds]
    masks_process = [masks_process[i_m] for i_m in range(len(masks_process)) if i_m in all_inds]
    return (rois, scores, class_ids, masks_process)


def geo_process_masks_smooth_save(masks, class_ids, class_names, transform, leups, out_data_location, out_dataset_name, return_bbox=False):
    """

    :param masks: 存了每个block的预测总结果
    :param class_ids: 类别相关目前没用，后续给对象加入类别字段时使用
    :param class_names:
    :param transform:
    :param leups: 存了每个block的左上角点
    :param out_data_location: udbx的路径
    :param out_dataset_name: 数据集名称
    :param return_bbox: 是否生成对象的外接矩形
    :return:
    """
    ds = get_output_datasource(out_data_location)
    check_output_datasource(ds)
    if out_dataset_name is None:
        out_dataset_name = "NewDataset"
    mask_name = out_dataset_name + str("_mask_drop")
    mask_dataset = ds.create_vector_dataset(mask_name, (DatasetType.REGION), adjust_name=True)
    region_list = []
    feature_mask_list = []
    for num in range(len(leups)):
        leup = leups[num]
        if len(masks[num].shape) == 3:
            for mnum in range(len(masks[num][(0, 0, None[:None])])):
                mask_c = masks[num][(None[:None], None[:None], mnum)]
                x, y = rio_transform.xy(transform, leup[1], leup[0])
                tile_transform = rio_transform.from_origin(x, y, transform[0], -transform[4])
                con_ck = features.shapes(mask_c, mask=(mask_c.astype(np.bool)), transform=tile_transform)
                try:
                    con_c = next(con_ck)[0]
                    while True:
                        if len(con_c["coordinates"][0]) > 100:
                            break
                        else:
                            try:
                                con_c = next(con_ck)[0]
                            except Exception as e:
                                try:
                                    print(e)
                                    break
                                finally:
                                    e = None
                                    del e

                    json_shp = json.dumps(con_c)
                    region_shp = Geometry.from_geojson(json_shp)
                    region_list.append(region_shp)
                except Exception as e:
                    try:
                        if not math.ceil(mask_c.max()) == 0:
                            raise ValueError(e)
                    finally:
                        e = None
                        del e

        elif len(masks[num].shape) == 2:
            mask_c = masks[num]
            x, y = rio_transform.xy(transform, leup[1], leup[0])
            tile_transform = rio_transform.from_origin(x, y, transform[0], -transform[4])
            con_ck = features.shapes(mask_c, mask=(mask_c.astype(np.bool)), transform=tile_transform)
            try:
                con_c = next(con_ck)[0]
                while True:
                    if len(con_c["coordinates"][0]) > 100:
                        break
                    else:
                        try:
                            con_c = next(con_ck)[0]
                        except Exception as e:
                            try:
                                print(e)
                                break
                            finally:
                                e = None
                                del e

                json_shp = json.dumps(con_c)
                region_shp = Geometry.from_geojson(json_shp)
                region_list.append(region_shp)
            except Exception as e:
                try:
                    if not math.ceil(mask_c.max()) == 0:
                        raise ValueError(e)
                finally:
                    e = None
                    del e

        else:
            raise ValueError("please check mask result channels")

    for i_re in range(len(region_list)):
        feature_mask = Feature(region_list[i_re])
        feature_mask_list.append(feature_mask)

    mask_dataset.append(feature_mask_list)
    dissolve_mask = dissolve(mask_dataset, dissolve_type="SINGLE", dissolve_fields="SmUserID", out_dataset_name=out_dataset_name)
    if return_bbox:
        nb = compute_features_envelope(dissolve_mask, out_data=ds, out_dataset_name=(out_dataset_name + str("_bbox")))
    mask_dataset.close()
    ds.delete(mask_name)
    return out_dataset_name


def core_contours(mask):
    """Extracts contours and the relationship between them from a binary mask.
    Args:
      mask: the binary mask to find contours in.
    Returns:
      The detected contours as a list of points and the contour hierarchy.
    Note: the hierarchy can be used to re-construct polygons with holes as one entity.
    """
    k1 = cv2.RETR_TREE
    k2 = cv2.CHAIN_APPROX_SIMPLE
    contours, hierarchy = cv2.findContours(mask, k1, k2)
    return (contours, hierarchy)


def get_mask_poly(mask_t):
    all_con_points = []
    contours, _ = core_contours(mask_t)
    for i in range(len(contours)):
        if len(contours[i]) > 2:
            con_points = []
            for i1 in contours[i]:
                con_points.append(i1[0].tolist())

            all_con_points.append(con_points)

    all_poly = []
    for k in range(len(all_con_points)):
        poly = GeoRegion(all_con_points[k])
        all_poly.append(poly)

    return all_poly


def save_udb(transform, rois, masks, scores, class_ids, class_name, out_dir, out_name, return_bbox=False):
    """

    :param rois: [h_min,w_min,h_max,w_max]
    :param masks:
    :param scores: scores of result
    :param class_ids: class names correspond ids
    :param class_name: class_ids corresponding class names
    :param out_dir: existing or creating udb location
    :param out_name: dataset name,just for one
    :return:
    """
    ds = get_output_datasource(out_dir)
    check_output_datasource(ds)
    if out_name is None:
        out_name = "NewDataset"
    mask_dataset = ds.create_vector_dataset(out_name, (DatasetType.REGION), adjust_name=True)
    type_class = FieldInfo("class_type", (FieldType.TEXT), max_length=50)
    type_score = FieldInfo("scores", (FieldType.DOUBLE), max_length=50)
    type_object = FieldInfo("object_num", (FieldType.INT64), max_length=50)
    mask_dataset.create_field(type_class)
    mask_dataset.create_field(type_score)
    mask_dataset.create_field(type_object)
    feature_mask_list = []
    if len(scores) != 0:
        for ie in range(len(scores)):
            _rois = rois[ie]
            _mask = masks[ie]
            _score = scores[ie]
            _class = class_name[class_ids[ie]]
            feature_mask = Feature(_mask, {'class_type':_class,  'scores':_score,  'object_num':ie}, field_infos=[
             type_class, type_score, type_object])
            feature_mask_list.append(feature_mask)

        mask_dataset.append(feature_mask_list)
        mask_dataset.close()
        if return_bbox:
            bbox_name = out_name + str("_bbox")
            bbox_dataset = ds.create_vector_dataset(bbox_name, (DatasetType.REGION), adjust_name=True)
            type_class = FieldInfo("class_type", (FieldType.TEXT), max_length=50)
            type_score = FieldInfo("scores", (FieldType.DOUBLE), max_length=50)
            bbox_dataset.create_field(type_class)
            bbox_dataset.create_field(type_score)
            bbox_li = []
            if len(scores) != 0:
                for ie in range(len(scores)):
                    _rois = rois[ie]
                    _score = scores[ie]
                    _class = class_name[class_ids[ie]]
                    x1, y1 = rio_transform.xy(transform, _rois[0], _rois[1])
                    x2, y2 = rio_transform.xy(transform, _rois[2], _rois[3])
                    point = [
                     (
                      x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1)]
                    region = GeoRegion(point)
                    feature_roi = Feature(region, {'class_type':_class,  'scores':_score}, field_infos=[
                     type_class, type_score])
                    bbox_li.append(feature_roi)

                bbox_dataset.append(bbox_li)
                bbox_dataset.close()
    return out_name


def resize_image(image, min_dim=None, max_dim=None, padding=False):
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


def extract_image_from_dir(image_path, config):
    all_images = []
    if "." in image_path.split("\\")[-1]:
        image = cv2.imdecode(np.fromfile(image_path, dtype=(np.uint8)), -1)
        resized_image = resize_image(image, (config.IMAGE_MIN_DIM), (config.IMAGE_MAX_DIM), padding=True)
        resized_image_get = resized_image[0]
        all_images.append(resized_image_get)
    else:
        all_images_name = os.walk(image_path)[-1]
        for image_name in all_images_name:
            image = cv2.imread(image_name)
            resized_image = resize_image(image, (config.IMAGE_MIN_DIM), (config.IMAGE_MAX_DIM), padding=True)
            all_images.append(resized_image)

    return all_images

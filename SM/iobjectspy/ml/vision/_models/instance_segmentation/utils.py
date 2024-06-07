# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\instance_segmentation\utils.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 38354 bytes
"""
Mask R-CNN
Common utility functions and classes.
Copyright (c) 2017 Matterport, Inc.
Licensed under the MIT License (see LICENSE for details)
Written by Waleed Abdulla
"""
import numpy as np, scipy.misc, skimage.color, skimage.io, tensorflow as tf, PIL
from PIL import Image
import os, colorsys, cv2 as cv
from iobjectspy.ml.toolkit._toolkit import save_pattle_png, save_config_to_yaml
from collections import OrderedDict

def extract_bboxes(mask):
    """Compute bounding boxes from masks.
    计算mask的边界框。
    mask: [height, width, num_instances]. Mask pixels are either 1 or 0.
    Returns: bbox array [num_instances, (y1, x1, y2, x2)].
    """
    boxes = np.zeros([mask.shape[-1], 4], dtype=(np.int32))
    delete_inds = []
    for i in range(mask.shape[-1]):
        m = mask[(None[:None], None[:None], i)]
        horizontal_indicies = np.where(np.any(m, axis=0))[0]
        vertical_indicies = np.where(np.any(m, axis=1))[0]
        if horizontal_indicies.shape[0]:
            x1, x2 = horizontal_indicies[[0, -1]]
            y1, y2 = vertical_indicies[[0, -1]]
            x2 += 1
            y2 += 1
            boxes[i] = np.array([y1, x1, y2, x2])
        else:
            delete_inds.append(i)

    return (
     boxes.astype(np.int32), delete_inds)


def compute_iou(box, boxes, box_area, boxes_area):
    """Calculates IoU of the given box with the array of the given boxes.
    # 使用给定框的数组计算给定框的IoU。
    box: 1D vector [y1, x1, y2, x2]
    boxes: [boxes_count, (y1, x1, y2, x2)]
    box_area: float. the area of 'box'  'box'的面积
    boxes_area: array of length boxes_count.  长度数组box_count
    Note: the areas are passed in rather than calculated here for
          efficency. Calculate once in the caller to avoid duplicate work.
    """
    y1 = np.maximum(box[0], boxes[(None[:None], 0)])
    y2 = np.minimum(box[2], boxes[(None[:None], 2)])
    x1 = np.maximum(box[1], boxes[(None[:None], 1)])
    x2 = np.minimum(box[3], boxes[(None[:None], 3)])
    intersection = np.maximum(x2 - x1, 0) * np.maximum(y2 - y1, 0)
    union = box_area + boxes_area[None[:None]] - intersection[None[:None]]
    iou = intersection / union
    return iou


def compute_overlaps(boxes1, boxes2):
    """Computes IoU overlaps between two sets of boxes.
    计算两组框之间的IoU重叠。
    boxes1, boxes2: [N, (y1, x1, y2, x2)].
    For better performance, pass the largest set first and the smaller second.
    为了获得更好的性能，请先传递最大集合，再传递更小的第二个。
    """
    area1 = (boxes1[(None[:None], 2)] - boxes1[(None[:None], 0)]) * (boxes1[(None[:None], 3)] - boxes1[(None[:None], 1)])
    area2 = (boxes2[(None[:None], 2)] - boxes2[(None[:None], 0)]) * (boxes2[(None[:None], 3)] - boxes2[(None[:None], 1)])
    overlaps = np.zeros((boxes1.shape[0], boxes2.shape[0]))
    for i in range(overlaps.shape[1]):
        box2 = boxes2[i]
        overlaps[(None[:None], i)] = compute_iou(box2, boxes1, area2[i], area1)

    return overlaps


def compute_overlaps_masks(masks1, masks2):
    """Computes IoU overlaps between two sets of masks.
    计算两组掩码之间的IoU重叠。
    masks1, masks2: [Height, Width, instances]
    """
    masks1 = np.reshape(masks1 > 0.5, (-1, masks1.shape[-1])).astype(np.float32)
    masks2 = np.reshape(masks2 > 0.5, (-1, masks2.shape[-1])).astype(np.float32)
    area1 = np.sum(masks1, axis=0)
    area2 = np.sum(masks2, axis=0)
    intersections = np.dot(masks1.T, masks2)
    union = area1[(None[:None], None)] + area2[(None, None[:None])] - intersections
    overlaps = intersections / union
    return overlaps


def non_max_suppression(boxes, scores, threshold):
    """Performs non-maximum supression and returns indicies of kept boxes.
    执行非最大抑制并返回保留框的索引
    boxes: [N, (y1, x1, y2, x2)]. Notice that (y2, x2) lays outside the box. 注意（y2，x2）在框外。
    scores: 1-D array of box scores.
    threshold: Float. IoU threshold to use for filtering. 用于过滤的IoU阈值
    """
    assert boxes.shape[0] > 0
    if boxes.dtype.kind != "f":
        boxes = boxes.astype(np.float32)
    y1 = boxes[(None[:None], 0)]
    x1 = boxes[(None[:None], 1)]
    y2 = boxes[(None[:None], 2)]
    x2 = boxes[(None[:None], 3)]
    area = (y2 - y1) * (x2 - x1)
    ixs = scores.argsort()[None[None:-1]]
    pick = []
    while len(ixs) > 0:
        i = ixs[0]
        pick.append(i)
        iou = compute_iou(boxes[i], boxes[ixs[1[:None]]], area[i], area[ixs[1[:None]]])
        remove_ixs = np.where(iou > threshold)[0] + 1
        ixs = np.delete(ixs, remove_ixs)
        ixs = np.delete(ixs, 0)

    return np.array(pick, dtype=(np.int32))


def apply_box_deltas(boxes, deltas):
    """Applies the given deltas to the given boxes.
    将给定的deltas应用于给定的框。
    boxes: [N, (y1, x1, y2, x2)]. Note that (y2, x2) is outside the box.
    deltas: [N, (dy, dx, log(dh), log(dw))]
    """
    boxes = boxes.astype(np.float32)
    height = boxes[(None[:None], 2)] - boxes[(None[:None], 0)]
    width = boxes[(None[:None], 3)] - boxes[(None[:None], 1)]
    center_y = boxes[(None[:None], 0)] + 0.5 * height
    center_x = boxes[(None[:None], 1)] + 0.5 * width
    center_y += deltas[(None[:None], 0)] * height
    center_x += deltas[(None[:None], 1)] * width
    height *= np.exp(deltas[(None[:None], 2)])
    width *= np.exp(deltas[(None[:None], 3)])
    y1 = center_y - 0.5 * height
    x1 = center_x - 0.5 * width
    y2 = y1 + height
    x2 = x1 + width
    return np.stack([y1, x1, y2, x2], axis=1)


def box_refinement_graph(box, gt_box):
    """Compute refinement needed to transform box to gt_box.
    将框转换为gt_box所需的计算细化。
    box and gt_box are [N, (y1, x1, y2, x2)]
    """
    box = tf.cast(box, tf.float32)
    gt_box = tf.cast(gt_box, tf.float32)
    height = box[(None[:None], 2)] - box[(None[:None], 0)]
    width = box[(None[:None], 3)] - box[(None[:None], 1)]
    center_y = box[(None[:None], 0)] + 0.5 * height
    center_x = box[(None[:None], 1)] + 0.5 * width
    gt_height = gt_box[(None[:None], 2)] - gt_box[(None[:None], 0)]
    gt_width = gt_box[(None[:None], 3)] - gt_box[(None[:None], 1)]
    gt_center_y = gt_box[(None[:None], 0)] + 0.5 * gt_height
    gt_center_x = gt_box[(None[:None], 1)] + 0.5 * gt_width
    dy = (gt_center_y - center_y) / height
    dx = (gt_center_x - center_x) / width
    dh = tf.log(gt_height / height)
    dw = tf.log(gt_width / width)
    result = tf.stack([dy, dx, dh, dw], axis=1)
    return result


def box_refinement(box, gt_box):
    """Compute refinement needed to transform box to gt_box.
    将框转换为gt_box所需的计算细化。
    box and gt_box are [N, (y1, x1, y2, x2)]. (y2, x2) is
    assumed to be outside the box.
    """
    box = box.astype(np.float32)
    gt_box = gt_box.astype(np.float32)
    height = box[(None[:None], 2)] - box[(None[:None], 0)]
    width = box[(None[:None], 3)] - box[(None[:None], 1)]
    center_y = box[(None[:None], 0)] + 0.5 * height
    center_x = box[(None[:None], 1)] + 0.5 * width
    gt_height = gt_box[(None[:None], 2)] - gt_box[(None[:None], 0)]
    gt_width = gt_box[(None[:None], 3)] - gt_box[(None[:None], 1)]
    gt_center_y = gt_box[(None[:None], 0)] + 0.5 * gt_height
    gt_center_x = gt_box[(None[:None], 1)] + 0.5 * gt_width
    dy = (gt_center_y - center_y) / height
    dx = (gt_center_x - center_x) / width
    dh = np.log(gt_height / height)
    dw = np.log(gt_width / width)
    return np.stack([dy, dx, dh, dw], axis=1)


class Object_Extract_Dataset(object):
    __doc__ = "The base class for dataset classes.\n    To use it, create a new class that adds functions specific to the dataset\n    you want to use. For example:\n    数据集类的基类。\n\xa0\xa0\xa0\xa0要使用它，请创建一个新类，添加特定于数据集的函数\n\xa0\xa0\xa0\xa0你想用。例如\n    class CatsAndDogsDataset(Dataset):\n        def load_cats_and_dogs(self):\n            ...\n        def load_mask(self, image_id):\n            ...\n        def image_reference(self, image_id):\n            ...\n    See COCODataset and ShapesDataset as examples.\n    "

    def __init__(self, class_map=None):
        self._image_ids = []
        self.image_info = []
        self.class_info = [
         {'source':"", 
          'id':0,  'name':"BG"}]
        self.source_class_ids = {}

    def add_class(self, source, class_id, class_name):
        assert "." not in source, "Source name cannot contain a dot"
        for info in self.class_info:
            if info["source"] == source and info["id"] == class_id:
                return

        self.class_info.append({'source':source, 
         'id':class_id, 
         'name':class_name})

    def add_image(self, source, image_id, path, **kwargs):
        image_info = {'id':image_id, 
         'source':source, 
         'path':path}
        image_info.update(kwargs)
        self.image_info.append(image_info)

    def image_reference(self, image_id):
        """Return a link to the image in its source Website or details about
        the image that help looking it up or debugging it.
        Override for your dataset, but pass to this function
        if you encounter images not in your dataset.
        返回源网站中图片的链接或有关详情
\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0 帮助查看或调试它的图像。
\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0 覆盖您的数据集，但传递给此函数
\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0 如果您遇到不在数据集中的图像。
        """
        return ""

    def prepare(self, class_map=None):
        """Prepares the Dataset class for use.
        TODO: class map is not supported yet. When done, it should handle mapping
              classes from different datasets to the same class ID.

        准备Dataset类以供使用。
\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0 TODO：class map尚未得到支持。 完成后，它应该处理映射
\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0 从不同数据集到同一个类ID的类。
        """

        def clean_name(name):
            """Returns a shorter version of object names for cleaner display.
            返回更简洁的对象名称，以便更清晰地显示"""
            return ",".join(name.split(",")[None[:1]])

        self.num_classes = len(self.class_info)
        self.class_ids = np.arange(self.num_classes)
        self.class_names = [clean_name(c["name"]) for c in self.class_info]
        self.num_images = len(self.image_info)
        self._image_ids = np.arange(self.num_images)
        self.class_from_source_map = {"{}.{}".format(info["source"], info["id"]): id for info, id in zip(self.class_info, self.class_ids)}
        self.sources = list(set([i["source"] for i in self.class_info]))
        self.source_class_ids = {}
        for source in self.sources:
            self.source_class_ids[source] = []
            for i, info in enumerate(self.class_info):
                if i == 0 or source == info["source"]:
                    self.source_class_ids[source].append(i)

    def map_source_class_id(self, source_class_id):
        """Takes a source class ID and returns the int class ID assigned to it.
        For example:
        dataset.map_source_class_id("coco.12") -> 23
        """
        return self.class_from_source_map[source_class_id]

    def get_source_class_id(self, class_id, source):
        """Map an internal class ID to the corresponding class ID in the source dataset."""
        info = self.class_info[class_id]
        assert info["source"] == source
        return info["id"]

    def append_data(self, class_info, image_info):
        self.external_to_class_id = {}
        for i, c in enumerate(self.class_info):
            for ds, id in c["map"]:
                self.external_to_class_id[ds + str(id)] = i

        self.external_to_image_id = {}
        for i, info in enumerate(self.image_info):
            self.external_to_image_id[info["ds"] + str(info["id"])] = i

    @property
    def image_ids(self):
        return self._image_ids

    def source_image_link(self, image_id):
        """Returns the path or URL to the image.
        Override this to return a URL to the image if it's availble online for easy
        debugging.
        """
        return self.image_info[image_id]["path"]

    def load_image(self, image_id):
        """Load the specified image and return a [H,W,3] Numpy array.
        """
        image = skimage.io.imread(self.image_info[image_id]["path"])
        if image.ndim != 3:
            image = skimage.color.gray2rgb(image)
        return image

    def load_mask(self, image_id):
        """Load instance masks for the given image.
        Different datasets use different ways to store masks. Override this
        method to load instance masks and return them in the form of am
        array of binary masks of shape [height, width, instances].
        Returns:
            masks: A bool array of shape [height, width, instance count] with
                a binary mask per instance.
            class_ids: a 1D array of class IDs of the instance masks.
        """
        mask = np.empty([0, 0, 0])
        class_ids = np.empty([0], np.int32)
        return (mask, class_ids)


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
        image = np.array(Image.fromarray(image).resize(size=(round(h * scale), round(w * scale))))
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


def resize_mask(mask, scale, padding):
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


def minimize_mask(bbox, mask, mini_shape):
    """Resize masks to a smaller version to cut memory load.
    Mini-masks can then resized back to image scale using expand_masks()
    See inspect_data.ipynb notebook for more details.
    """
    mini_mask = np.zeros((mini_shape + (mask.shape[-1],)), dtype=bool)
    for i in range(mask.shape[-1]):
        m = mask[(None[:None], None[:None], i)]
        y1, x1, y2, x2 = bbox[i][None[:4]]
        m = m[(y1[:y2], x1[:x2])]
        if m.size == 0:
            raise Exception("Invalid bounding box with area of zero")
        m = np.array(Image.fromarray(m.astype(float)).resize(size=mini_shape, resample=(PIL.Image.BILINEAR))) * 255
        mini_mask[(None[:None], None[:None], i)] = np.where(m >= 128, 1, 0)

    return mini_mask


def expand_mask(bbox, mini_mask, image_shape):
    """Resizes mini masks back to image size. Reverses the change
    of minimize_mask().
    See inspect_data.ipynb notebook for more details.
    """
    mask = np.zeros((image_shape[None[:2]] + (mini_mask.shape[-1],)), dtype=bool)
    for i in range(mask.shape[-1]):
        m = mini_mask[(None[:None], None[:None], i)]
        y1, x1, y2, x2 = bbox[i][None[:4]]
        h = y2 - y1
        w = x2 - x1
        m = scipy.misc.imresize((m.astype(float)), (h, w), interp="bilinear")
        mask[(y1[:y2], x1[:x2], i)] = np.where(m >= 128, 1, 0)

    return mask


def mold_mask(mask, config):
    pass


def unmold_mask(mask, bbox, image_shape):
    """Converts a mask generated by the neural network into a format similar
    to it's original shape.
    mask: [height, width] of type float. A small, typically 28x28 mask.
    bbox: [y1, x1, y2, x2]. The box to fit the mask in.
    Returns a binary mask with the same size as the original image.
    """
    threshold = 0.5
    y1, x1, y2, x2 = bbox
    mask = scipy.misc.imresize(mask,
      (y2 - y1, x2 - x1), interp="bilinear").astype(np.float32) / 255.0
    mask = np.where(mask >= threshold, 1, 0).astype(np.uint8)
    full_mask = np.zeros((image_shape[None[:2]]), dtype=(np.uint8))
    full_mask[(y1[:y2], x1[:x2])] = mask
    return full_mask


def generate_anchors(scales, ratios, shape, feature_stride, anchor_stride):
    """
    scales: 1D array of anchor sizes in pixels. Example: [32, 64, 128]
    ratios: 1D array of anchor ratios of width/height. Example: [0.5, 1, 2]
    shape: [height, width] spatial shape of the feature map over which
            to generate anchors.
    feature_stride: Stride of the feature map relative to the image in pixels.
    anchor_stride: Stride of anchors on the feature map. For example, if the
        value is 2 then generate anchors for every other feature map pixel.
    """
    scales, ratios = np.meshgrid(np.array(scales), np.array(ratios))
    scales = scales.flatten()
    ratios = ratios.flatten()
    heights = scales / np.sqrt(ratios)
    widths = scales * np.sqrt(ratios)
    shifts_y = np.arange(0, shape[0], anchor_stride) * feature_stride
    shifts_x = np.arange(0, shape[1], anchor_stride) * feature_stride
    shifts_x, shifts_y = np.meshgrid(shifts_x, shifts_y)
    box_widths, box_centers_x = np.meshgrid(widths, shifts_x)
    box_heights, box_centers_y = np.meshgrid(heights, shifts_y)
    box_centers = np.stack([
     box_centers_y, box_centers_x],
      axis=2).reshape([-1, 2])
    box_sizes = np.stack([box_heights, box_widths], axis=2).reshape([-1, 2])
    boxes = np.concatenate([box_centers - 0.5 * box_sizes,
     box_centers + 0.5 * box_sizes],
      axis=1)
    return boxes


def generate_pyramid_anchors(scales, ratios, feature_shapes, feature_strides, anchor_stride):
    """Generate anchors at different levels of a feature pyramid. Each scale
    is associated with a level of the pyramid, but each ratio is used in
    all levels of the pyramid.
    Returns:
    anchors: [N, (y1, x1, y2, x2)]. All generated anchors in one array. Sorted
        with the same order of the given scales. So, anchors of scale[0] come
        first, then anchors of scale[1], and so on.
    """
    anchors = []
    for i in range(len(scales)):
        anchors.append(generate_anchors(scales[i], ratios, feature_shapes[i], feature_strides[i], anchor_stride))

    return np.concatenate(anchors, axis=0)


def trim_zeros(x):
    """It's common to have tensors larger than the available data and
    pad with zeros. This function removes rows that are all zeros.
    x: [rows, columns].
    """
    assert len(x.shape) == 2
    return x[~np.all((x == 0), axis=1)]


def compute_matches(gt_boxes, gt_class_ids, gt_masks, pred_boxes, pred_class_ids, pred_scores, pred_masks, iou_threshold=0.5, score_threshold=0.0):
    """Finds matches between prediction and ground truth instances.

    Returns:
        gt_match: 1-D array. For each GT box it has the index of the matched
                  predicted box.
        pred_match: 1-D array. For each predicted box, it has the index of
                    the matched ground truth box.
        overlaps: [pred_boxes, gt_boxes] IoU overlaps.
    """
    gt_boxes = trim_zeros(gt_boxes)
    gt_masks = gt_masks[(..., None[:gt_boxes.shape[0]])]
    pred_boxes = trim_zeros(pred_boxes)
    pred_scores = pred_scores[None[:pred_boxes.shape[0]]]
    indices = np.argsort(pred_scores)[None[None:-1]]
    pred_boxes = pred_boxes[indices]
    pred_class_ids = pred_class_ids[indices]
    pred_scores = pred_scores[indices]
    pred_masks = pred_masks[(..., indices)]
    overlaps = compute_overlaps_masks(pred_masks, gt_masks)
    match_count = 0
    pred_match = -1 * np.ones([pred_boxes.shape[0]])
    gt_match = -1 * np.ones([gt_boxes.shape[0]])
    for i in range(len(pred_boxes)):
        sorted_ixs = np.argsort(overlaps[i])[None[None:-1]]
        low_score_idx = np.where(overlaps[(i, sorted_ixs)] < score_threshold)[0]
        if low_score_idx.size > 0:
            sorted_ixs = sorted_ixs[None[:low_score_idx[0]]]
        for j in sorted_ixs:
            if gt_match[j] > -1:
                continue
            iou = overlaps[(i, j)]
            if iou < iou_threshold:
                break
            if pred_class_ids[i] == gt_class_ids[j]:
                match_count += 1
                gt_match[j] = i
                pred_match[i] = j
                break

    return (
     gt_match, pred_match, overlaps)


def compute_ap1(gt_boxes, gt_class_ids, gt_masks, pred_boxes, pred_class_ids, pred_scores, pred_masks, iou_threshold=0.5):
    """Compute Average Precision at a set IoU threshold (default 0.5).
    Returns:
    mAP: Mean Average Precision
    precisions: List of precisions at different class score thresholds.
    recalls: List of recall values at different class score thresholds.
    overlaps: [pred_boxes, gt_boxes] IoU overlaps.
    """
    gt_boxes = trim_zeros(gt_boxes)
    gt_masks = gt_masks[(..., None[:gt_boxes.shape[0]])]
    pred_boxes = trim_zeros(pred_boxes)
    pred_scores = pred_scores[None[:pred_boxes.shape[0]]]
    indices = np.argsort(pred_scores)[None[None:-1]]
    pred_boxes = pred_boxes[indices]
    pred_class_ids = pred_class_ids[indices]
    pred_scores = pred_scores[indices]
    pred_masks = pred_masks[(..., indices)]
    overlaps = compute_overlaps_masks(pred_masks, gt_masks)
    match_count = 0
    pred_match = np.zeros([pred_boxes.shape[0]])
    gt_match = np.zeros([gt_boxes.shape[0]])
    for i in range(len(pred_boxes)):
        sorted_ixs = np.argsort(overlaps[i])[None[None:-1]]
        for j in sorted_ixs:
            if gt_match[j] == 1:
                continue
            iou = overlaps[(i, j)]
            if iou < iou_threshold:
                break
            if pred_class_ids[i] == gt_class_ids[j]:
                match_count += 1
                gt_match[j] = 1
                pred_match[i] = 1
                break

    precisions = np.cumsum(pred_match) / (np.arange(len(pred_match)) + 1)
    recalls = np.cumsum(pred_match).astype(np.float32) / len(gt_match)
    precisions = np.concatenate([[0], precisions, [0]])
    recalls = np.concatenate([[0], recalls, [1]])
    for i in range(len(precisions) - 2, -1, -1):
        precisions[i] = np.maximum(precisions[i], precisions[i + 1])

    indices = np.where(recalls[None[:-1]] != recalls[1[:None]])[0] + 1
    mAP = np.sum((recalls[indices] - recalls[indices - 1]) * precisions[indices])
    return (
     mAP, precisions, recalls, overlaps)


def compute_ap(gt_boxes, gt_class_ids, gt_masks, pred_boxes, pred_class_ids, pred_scores, pred_masks, iou_threshold=0.5):
    """Compute Average Precision at a set IoU threshold (default 0.5).

    Returns:
    mAP: Mean Average Precision
    precisions: List of precisions at different class score thresholds.
    recalls: List of recall values at different class score thresholds.
    overlaps: [pred_boxes, gt_boxes] IoU overlaps.
    """
    gt_match, pred_match, overlaps = compute_matches(gt_boxes, gt_class_ids, gt_masks, pred_boxes, pred_class_ids, pred_scores, pred_masks, iou_threshold)
    precisions = np.cumsum(pred_match > -1) / (np.arange(len(pred_match)) + 1)
    recalls = np.cumsum(pred_match > -1).astype(np.float32) / len(gt_match)
    precisions = np.concatenate([[0], precisions, [0]])
    recalls = np.concatenate([[0], recalls, [1]])
    for i in range(len(precisions) - 2, -1, -1):
        precisions[i] = np.maximum(precisions[i], precisions[i + 1])

    indices = np.where(recalls[None[:-1]] != recalls[1[:None]])[0] + 1
    mAP = np.sum((recalls[indices] - recalls[indices - 1]) * precisions[indices])
    return (
     mAP, precisions, recalls, overlaps)


def compute_recall(pred_boxes, gt_boxes, iou):
    """Compute the recall at the given IoU threshold. It's an indication
    of how many GT boxes were found by the given prediction boxes.
    pred_boxes: [N, (y1, x1, y2, x2)] in image coordinates
    gt_boxes: [N, (y1, x1, y2, x2)] in image coordinates
    """
    overlaps = compute_overlaps(pred_boxes, gt_boxes)
    iou_max = np.max(overlaps, axis=1)
    iou_argmax = np.argmax(overlaps, axis=1)
    positive_ids = np.where(iou_max >= iou)[0]
    matched_gt_boxes = iou_argmax[positive_ids]
    recall = len(set(matched_gt_boxes)) / gt_boxes.shape[0]
    return (recall, positive_ids)


def batch_slice(inputs, graph_fn, batch_size, names=None):
    """Splits inputs into slices and feeds each slice to a copy of the given
    computation graph and then combines the results. It allows you to run a
    graph on a batch of inputs even if the graph is written to support one
    instance only.
    inputs: list of tensors. All must have the same first dimension length
    graph_fn: A function that returns a TF tensor that's part of a graph.
    batch_size: number of slices to divide the data into.
    names: If provided, assigns names to the resulting tensors.
    """
    if not isinstance(inputs, list):
        inputs = [
         inputs]
    outputs = []
    for i in range(batch_size):
        inputs_slice = [x[i] for x in inputs]
        output_slice = graph_fn(*inputs_slice)
        if not isinstance(output_slice, (tuple, list)):
            output_slice = [
             output_slice]
        outputs.append(output_slice)

    outputs = list(zip(*outputs))
    if names is None:
        names = [
         None] * len(outputs)
    result = [tf.stack(o, axis=0, name=n) for o, n in zip(outputs, names)]
    if len(result) == 1:
        result = result[0]
    return result


def _save_xml(output_path_label, lists, width, height, pic_name, depth, class_names):
    """
        传入lists包含bbox，category，difficult信息，将其转换为xml格式

        :param output_path_label: 输入标签文件存储路径
        :type output_path_label: str
        :param lists: 包含bbox，category，difficult信息
        :type lists: list
        :param width: 图像宽度
        :type width: Long
        :param height: 图像高度
        :type height: Long
        :param pic_name: 对应标签文件的图片名称
        :type pic_name: str
        """
    tile_format = (
     pic_name.split(".")[-1],)
    if tile_format == "jpg" or tile_format == "png":
        depth = 3
    from lxml.etree import Element, SubElement, tostring
    node_root = Element("annotation")
    node_folder = SubElement(node_root, "folder")
    node_folder.text = "VOC"
    node_filename = SubElement(node_root, "filename")
    node_filename.text = pic_name
    node_size = SubElement(node_root, "size")
    node_width = SubElement(node_size, "width")
    node_width.text = "%s" % width
    node_height = SubElement(node_size, "height")
    node_height.text = "%s" % height
    node_depth = SubElement(node_size, "depth")
    node_depth.text = "%s" % depth
    node_segmented = SubElement(node_root, "segmented")
    node_segmented.text = "%s" % 0
    for list in lists:
        node_object = SubElement(node_root, "object")
        node_name = SubElement(node_object, "name")
        node_name.text = class_names[int(list[4])]
        node_difficult = SubElement(node_object, "difficult")
        node_difficult.text = str(list[5])
        node_bndbox = SubElement(node_object, "bndbox")
        node_xmin = SubElement(node_bndbox, "xmin")
        node_xmin.text = "%s" % list[1]
        node_ymin = SubElement(node_bndbox, "ymin")
        node_ymin.text = "%s" % list[0]
        node_xmax = SubElement(node_bndbox, "xmax")
        node_xmax.text = "%s" % list[3]
        node_ymax = SubElement(node_bndbox, "ymax")
        node_ymax.text = "%s" % list[2]

    del lists[None[:None]]
    xml = tostring(node_root, pretty_print=True)
    save_xml = os.path.join(output_path_label, pic_name + ".xml")
    with open(save_xml, "wb") as f:
        f.write(xml)


def _get_continuous_codes_list(num_color=256):
    """
    动态获取颜色表列表

    :param int num_color: 颜色表数量
    :return: color_continuous_codes_list 颜色表列表
    :type: list[tuple]

    """
    r, g, b = [v / 255 for v in get_rgb("#ffffff")]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    color_continuous_codes_list = []
    for i in range(num_color):
        ns = 1 / num_color * (i + 1)
        color_continuous_codes_list.append(tuple([int(v * 255) for v in colorsys.hsv_to_rgb(h, ns, v)]))

    return list(set(color_continuous_codes_list))


def get_rgb(v):
    """
    获取RGB颜色
   :param v: 十六进制颜色码
   :return: RGB颜色值
       """
    r, g, b = v[1[:3]], v[3[:5]], v[5[:7]]
    return (int(r, 16), int(g, 16), int(b, 16))


def _save_segobject(image, output_segobject, num_color_id):
    """
    保存按照object分割的mask标签
    """
    color_continuous_codes_list = _get_continuous_codes_list(num_color_id)
    color_codes_segobject = {}
    color_codes_segobject[(0, 0, 0)] = 0
    for color_codes_id in range(num_color_id):
        color_codes_segobject[color_continuous_codes_list[color_codes_id]] = color_codes_id

    image = image.astype(np.uint8)
    save_pattle_png(image, color_codes_segobject, output_segobject)


def show_two_image(image1, image2):
    from matplotlib import pyplot as plt
    fig = plt.figure(figsize=(10, 10))
    ax1 = plt.subplot(1, 2, 1)
    ax2 = plt.subplot(1, 2, 2)
    plt.sca(ax1)
    plt.imshow(image1)
    plt.sca(ax2)
    plt.imshow(image2)
    plt.show()


def create_sda_voc_mask(categorys, image_count, tile_size_x, tile_size_y, image_mean, tile_format, output_path):
    dic_voc_yml = OrderedDict({"dataset": (OrderedDict({'name': '"example_voc"', 
                 'classes': categorys, 
                 'image_count': image_count, 
                 'data_type': '"voc_mask"', 
                 'tile_size_x': tile_size_x, 
                 'tile_size_y': tile_size_y, 
                 'image_mean': image_mean, 
                 'suffix': tile_format}))})
    save_config_to_yaml(dic_voc_yml, output_path)

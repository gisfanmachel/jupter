import json
import os

import torch
import torch.nn as nn
import numpy as np

from pie.get_platform_arguments import parse_platform_arguments
from pie.network.models.pytorch.detection.yolo_decode import DecodeBox
from pie.train_center.pytorch.utils_obj import non_max_suppression, yolo_correct_boxes


def load_arguments(mode='eval'):
    '''
        加载参数
    :param is_input: 是否有参数输入 智能解译时为True，模型评估及模型发布中为False
    :return:
    '''

    init = parse_platform_arguments(mode=mode)

    # 输入的参数
    estimate_id = None
    image_path = None
    device_ids = None
    if mode=='eval':
        estimate_id = init.estimate_id
        image_path = init.image_path
        device_ids = init.device_ids

        # estimate_id = '121'
        # image_path = '/home/0w.jpg'
        # device_ids = 1
    # platform_arguments = {
    #     'estimate_id': estimate_id,  # 任务ID
    #     'image_path': image_path,  # 训练图片路径
    #     'device_ids': device_ids,  # gpu device id 数
    #     'result_path': init.result_path,  # 输出结果文件 output
    #     'network_type': 2,  # 预测的类别 （必填）
    #     'load_size': init.load_size,  # 图片加载大小
    #     'value_name_map': init.trainval_class_mapping,  # 训练value对应英文名称
    #     'value_title_map': init.trainval_title_mapping,  # 训练value对应类别中文名称
    #     'name_title_map': init.class_title_mapping,  # 类别英文名称 对应类别中文名称
    #     'value_color': init.trainval_rgb_mapping,  # 训练value对应 rgb()颜色
    #     'background_value': init.background_value,  # 背景对应的训练value
    #     'class_name_list': init.class_name_list,  # 除背景外的类别列表
    #     'nms': 0.3,  # 目标识别
    #     'init': init,
    #     'anchors': init.anchors
    # }

    platform_arguments = {
        'estimate_id': estimate_id,  # 任务ID
        'image_path': image_path,  # 训练图片路径
        'device_ids': device_ids,  # gpu device id 数
        'result_path': init.result_path,  # 输出结果文件 output
        'network_type': 2,  # 预测的类别 （必填）
        'load_size': init.load_size,  # 图片加载大小
        'value_name_map': init.trainval_class_mapping,  # 训练value对应英文名称
        'value_title_map': init.trainval_title_mapping,  # 训练value对应类别中文名称
        'name_title_map': init.class_title_mapping,  # 类别英文名称 对应类别中文名称
        'value_color': init.trainval_rgb_mapping,  # 训练value对应 rgb()颜色
        'background_value': init.background_value,  # 背景对应的训练value
        'class_name_list': init.class_name_list,  # 除背景外的类别列表
        'load_model': load_model,  # 模型加载方法
        'data_preprocessing': preprocess,  # 处理进入到模型里面的数据方法
        'data_post_processing': postprocess,  # 处理模型预测后的结果方法
        'trans_pipelines': init.trans_pipelines,  # 处理模型预测后的结果方法
        'nms': 0.3,  # 目标识别
        'init': init,
        'anchors': init.anchors
    }
    return platform_arguments


# 加载权重文件
def load_model(**kwargs):
    '''
        加载模型
    Returns:
    '''
    init = None
    if kwargs.get('init'):
        init = kwargs.get('init')

    # weights_file = init.weight_path
    weights_file ='/home/weight/YOLOv3.th'

    # 内置的网络结构
    model = init.model_loader_build_in(model_dir=weights_file)
    model = model.eval()

    return model


def preprocess(image, **kwargs):
    '''
    获取得到（H,W,C）ndarray数组，进行处理，可以直接输入模型进行预测
    Args:
        img:

    Returns:

    '''

    image = image/255.0
    # image /= 255.0
    img = np.transpose(image, (2, 0, 1))
    photo = img.astype(np.float32)

    photo = photo[0:3, :, :]

    images = []
    images.append(photo)
    images = np.asarray(images)

    images = torch.from_numpy(images)
    if True:
        images = images.cuda()

    return images


def postprocess(pred_image, **kwargs):
    '''
        处理输出后结果
        语义分割、变化检测：单波段（h,w）数组
        目标识别：结果数组 [[classId,score,xmin,xmax,ymin,ymax]]
        Args:
            outputs: 模型输出结果

        Returns:

        '''
    print('pred_image---------')
    if kwargs.get('anchors').all():
        anchors = kwargs.get('anchors')
    if kwargs.get('class_name_list'):
        class_names = kwargs.get('class_name_list')
    if kwargs.get('load_size'):
        load_size = kwargs.get('load_size')

    image_shape = np.array(load_size)

    yolo_decodes = []
    for i in range(3):
        yolo_decodes.append(
            DecodeBox(anchors[i], len(class_names), (image_shape[1], image_shape[0])))

    output_list = []
    for i in range(3):
        output_list.append(yolo_decodes[i](pred_image[i]))

    output = torch.cat(output_list, 1)
    batch_detections = non_max_suppression(output, len(class_names), conf_thres=0.4, nms_thres=0.3)
    boxes_mc = []
    if batch_detections[0] is None:
        return None
    else:
        batch_detections = batch_detections[0].cpu().numpy()
        top_index = batch_detections[:, 4] * batch_detections[:, 5] > 0.4
        top_conf = batch_detections[top_index, 4] * batch_detections[top_index, 5]
        top_label = np.array(batch_detections[top_index, -1], np.int32)
        top_bboxes = np.array(batch_detections[top_index, :4])
        top_xmin, top_ymin, top_xmax, top_ymax = np.expand_dims(top_bboxes[:, 0], -1), np.expand_dims(
            top_bboxes[:, 1],
            -1), np.expand_dims(
            top_bboxes[:, 2], -1), np.expand_dims(top_bboxes[:, 3], -1)

        # 去掉灰条
        boxes = yolo_correct_boxes(top_ymin, top_xmin, top_ymax, top_xmax,
                                   np.array([image_shape[0], image_shape[1]]),
                                   image_shape)

        for i, c in enumerate(top_label):
            score = top_conf[i]

            top, left, bottom, right = boxes[i]
            top = top - 5
            left = left - 5
            bottom = bottom + 5
            right = right + 5
            patch_box = [int(c), score, left, top, right, bottom]
            boxes_mc.append(patch_box)

    return boxes_mc

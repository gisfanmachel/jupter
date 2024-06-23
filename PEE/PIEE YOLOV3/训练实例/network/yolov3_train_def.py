# yolov3 pytorch 中训练过程中的方法

import torch
import numpy as np

from nets.utils import DecodeBox
from nets.yolo_loss import YOLOLoss
from metrics_yolov3 import get_batch_statistics
from nets.utils import non_max_suppression



# from pie.network.models.pytorch.detection.yolo_decode import DecodeBox
# from pie.train_center.common.loss_yolo import YOLOLoss
# from pie.train_center.common.metrics_obj import get_batch_statistics
# from pie.train_center.pytorch.utils_obj import non_max_suppression
# from pie.utils.registry import Registry



# 初始化loss
def create_loss(anchors,num_classes,input_shape):
    yolo_losses = []
    for i in range(3):
        yolo_losses.append(YOLOLoss(np.reshape(anchors, [-1, 2]), num_classes,
                                    (input_shape[1], input_shape[0]), True , False))
    return yolo_losses



def create_decode(anchors,num_classes,input_shape):
    yolo_decodes = []
    for i in range(3):
        yolo_decodes.append(
            DecodeBox(anchors[i], num_classes, (input_shape[1], input_shape[0])))
    return yolo_decodes


# 使用loss (输入 output,target 输出loss值)
def epoch_loss_train(outputs, targets, **kwargs):
    loss = None
    if kwargs.get('yolo_losses'):
        loss_name = kwargs['yolo_losses']
        losses = []
        for i in range(3):
            loss_item = loss_name[i](outputs[i], targets)
            losses.append(loss_item[0])
        loss = sum(losses)
    return loss

# 评价指标 （输入 outputs,targets）
# yolo_decodes num_classes input_shape,nms_outputs,targets,conf_thres=0.4, iou_threshold=0.3
def metrics_yolo_train(outputs, targets,**kwargs):

    input_shape = kwargs.get("input_shape")
    if not input_shape:
        print('metrics is must input_shape... ')
        exit(1)
    conf_thres = kwargs.get("conf_thres")
    if not conf_thres:
        conf_thres = 0.4
    iou_threshold = kwargs.get("iou_threshold")
    if not iou_threshold:
        iou_threshold = 0.4

    batch_metrics = get_batch_statistics(input_shape, outputs, targets, conf_thres, iou_threshold)
    return batch_metrics

def yolo_post_processing(outputs,**kwargs):

    if kwargs.get('yolo_decodes'):
        yolo_decodes = kwargs.get('yolo_decodes')

    num_classes = kwargs.get("num_classes")
    if not num_classes:
        print('metrics is must num_classes ... ')
        exit(1)

    nms_thres = kwargs.get("nms_thres")
    if not nms_thres:
        nms_thres = 0.4
    conf_thres = kwargs.get("conf_thres")
    if not conf_thres:
        conf_thres = 0.4

    # 处理
    output_list = []
    for i in range(3):
        output_list.append(yolo_decodes[i](outputs[i]))

    cat_outputs = torch.cat(output_list, 1)
    nms_outputs = non_max_suppression(cat_outputs, num_classes, conf_thres, nms_thres)

    return nms_outputs
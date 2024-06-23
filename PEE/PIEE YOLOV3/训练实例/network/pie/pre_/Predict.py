import json
import os

import torch
import torch.nn as nn
from nets.yolo4 import YoloBody
import numpy as np

from Predict_utils import prediction_image
basedir = os.path.abspath(os.path.dirname(__file__))
weights_root_path = basedir + '/weight/'

load_size = [1024,1024]
gpu_num = 1

# 类别
classes_path = basedir + '/classes.txt'
with open(classes_path) as f:
    class_names = f.readlines()
class_names = [c.strip() for c in class_names]

# 锚
anchors_path = basedir + "/oiltank_anchors.txt"
with open(anchors_path) as f:
    anchors = f.readline()
anchors = [float(x) for x in anchors.split(',')]
anchors = np.array(anchors).reshape([-1, 3, 2])[::-1, :, :]

weights_file = weights_root_path + "model.pth"

# 设置参数
def parse_platform_arguments():
    conf = input()
    params_estimate = json.loads(conf)
    estimate_id = params_estimate['estimate_id']
    image_path = params_estimate["image_path"]

    device_ids = []
    gpu_num = int(params_estimate["gpu_num"])
    if gpu_num != 0:
        for i in range(0, gpu_num):
            device_ids.append(i)

    platform_arguments = {
        'estimate_id': estimate_id,  # 任务ID
        'image_path': image_path,  # 训练图片路径
        'device_ids': device_ids,  # gpu device id 数
        'network_type': 2,  # 预测的类别  1.语义分割，2目标识别 ，3 变化检测
        'load_size': [1024, 1024],  # 图片加载大小
        'value_name_map': {0:'oiltank'},  # 训练value对应英文名称
        'value_title_map': {0: '油罐'},  # 训练value对应类别中文名称
        'name_title_map': {'oiltank': '油罐'},  # 类别英文名称 对应类别中文名称
        'value_color': {0: 'rgb(255,0,0)'},  # 训练value对应 rgb()颜色
        'background_value': 0,  # 背景对应的训练value
        'class_name_list': ['oiltank'],  # 除背景外的类别列表
        'load_model': load_model,  # 模型加载方法
        'deal_data_img': deal_data_img,  # 处理进入到模型里面的数据方法
        'deal_pred_result': deal_pred_result,  # 处理模型预测后的结果方法
        'nms': 0.3,  # 目标识别
    }
    return platform_arguments

def get_def_user():
    platform_arguments = {
        'load_model': load_model,  # 模型加载方法
        'deal_data_img': deal_data_img,  # 处理进入到模型里面的数据方法
        'deal_pred_result': deal_pred_result  # 处理模型预测后的结果方法
    }
    return platform_arguments

# 加载权重文件
def load_model():
    '''
        加载模型
    Returns:

    '''
    net = YoloBody(len(anchors[0]), len(class_names)).eval()
    cuda = torch.cuda.is_available()

    # 加快模型训练的效率
    print('Loading weights into state dict...')
    device = torch.device('cuda' if cuda else 'cpu')
    state_dict = torch.load(weights_file, map_location=device)
    net.load_state_dict(state_dict)

    if cuda:
        net = nn.DataParallel(net)
        net = net.cuda()

    return net


class DecodeBox(nn.Module):
    def __init__(self, anchors, num_classes, img_size):
        super(DecodeBox, self).__init__()
        self.anchors = anchors
        self.num_anchors = len(anchors)
        self.num_classes = num_classes
        self.bbox_attrs = 5 + num_classes
        self.img_size = img_size

    def forward(self, input):
        # input为bs,3*(1+4+num_classes),13,13

        # 一共多少张图片
        batch_size = input.size(0)
        # 13，13
        input_height = input.size(2)
        input_width = input.size(3)

        # 计算步长
        # 每一个特征点对应原来的图片上多少个像素点
        # 如果特征层为13x13的话，一个特征点就对应原来的图片上的32个像素点
        # 416/13 = 32
        stride_h = self.img_size[1] / input_height
        stride_w = self.img_size[0] / input_width

        # 把先验框的尺寸调整成特征层大小的形式
        # 计算出先验框在特征层上对应的宽高
        scaled_anchors = [(anchor_width / stride_w, anchor_height / stride_h) for anchor_width, anchor_height in
                          self.anchors]

        # bs,3*(5+num_classes),13,13 -> bs,3,13,13,(5+num_classes)
        prediction = input.view(batch_size, self.num_anchors,
                                self.bbox_attrs, input_height, input_width).permute(0, 1, 3, 4, 2).contiguous()

        # 先验框的中心位置的调整参数
        x = torch.sigmoid(prediction[..., 0])
        y = torch.sigmoid(prediction[..., 1])
        # 先验框的宽高调整参数
        w = prediction[..., 2]  # Width
        h = prediction[..., 3]  # Height

        # 获得置信度，是否有物体
        conf = torch.sigmoid(prediction[..., 4])
        # 种类置信度
        pred_cls = torch.sigmoid(prediction[..., 5:])  # Cls pred.

        FloatTensor = torch.cuda.FloatTensor if x.is_cuda else torch.FloatTensor
        LongTensor = torch.cuda.LongTensor if x.is_cuda else torch.LongTensor

        # 生成网格，先验框中心，网格左上角 batch_size,3,13,13
        grid_x = torch.linspace(0, input_width - 1, input_width).repeat(input_width, 1).repeat(
            batch_size * self.num_anchors, 1, 1).view(x.shape).type(FloatTensor)
        grid_y = torch.linspace(0, input_height - 1, input_height).repeat(input_height, 1).t().repeat(
            batch_size * self.num_anchors, 1, 1).view(y.shape).type(FloatTensor)

        # 生成先验框的宽高
        anchor_w = FloatTensor(scaled_anchors).index_select(1, LongTensor([0]))
        anchor_h = FloatTensor(scaled_anchors).index_select(1, LongTensor([1]))
        anchor_w = anchor_w.repeat(batch_size, 1).repeat(1, 1, input_height * input_width).view(w.shape)
        anchor_h = anchor_h.repeat(batch_size, 1).repeat(1, 1, input_height * input_width).view(h.shape)

        # 计算调整后的先验框中心与宽高
        pred_boxes = FloatTensor(prediction[..., :4].shape)
        pred_boxes[..., 0] = x.data + grid_x
        pred_boxes[..., 1] = y.data + grid_y
        pred_boxes[..., 2] = torch.exp(w.data) * anchor_w
        pred_boxes[..., 3] = torch.exp(h.data) * anchor_h

        # plt.show()
        # 用于将输出调整为相对于416x416的大小
        _scale = torch.Tensor([stride_w, stride_h] * 2).type(FloatTensor)
        output = torch.cat((pred_boxes.view(batch_size, -1, 4) * _scale,
                            conf.view(batch_size, -1, 1), pred_cls.view(batch_size, -1, self.num_classes)), -1)
        return output.data

# 去除灰度条
def yolo_correct_boxes( top, left, bottom, right, input_shape, image_shape):
    new_shape = image_shape * np.min(input_shape / image_shape)

    offset = (input_shape - new_shape) / 2. / input_shape
    scale = input_shape / new_shape

    box_yx = np.concatenate(((top + bottom) / 2, (left + right) / 2), axis=-1) / input_shape
    box_hw = np.concatenate((bottom - top, right - left), axis=-1) / input_shape

    box_yx = (box_yx - offset) * scale
    box_hw *= scale

    box_mins = box_yx - (box_hw / 2.)
    box_maxes = box_yx + (box_hw / 2.)
    boxes = np.concatenate([
        box_mins[:, 0:1],
        box_mins[:, 1:2],
        box_maxes[:, 0:1],
        box_maxes[:, 1:2]
    ], axis=-1)
    # print(np.shape(boxes))
    boxes *= np.concatenate([image_shape, image_shape], axis=-1)
    return boxes

def non_max_suppression( prediction, num_classes, conf_thres=0.5, nms_thres=0.4):
    # 求左上角和右下角
    box_corner = prediction.new(prediction.shape)
    box_corner[:, :, 0] = prediction[:, :, 0] - prediction[:, :, 2] / 2
    box_corner[:, :, 1] = prediction[:, :, 1] - prediction[:, :, 3] / 2
    box_corner[:, :, 2] = prediction[:, :, 0] + prediction[:, :, 2] / 2
    box_corner[:, :, 3] = prediction[:, :, 1] + prediction[:, :, 3] / 2
    prediction[:, :, :4] = box_corner[:, :, :4]

    output = [None for _ in range(len(prediction))]
    for image_i, image_pred in enumerate(prediction):
        conf_mask = (image_pred[:, 4] >= conf_thres).squeeze()
        image_pred = image_pred[conf_mask]

        if not image_pred.size(0):
            continue

        class_conf, class_pred = torch.max(image_pred[:, 5:5 + num_classes], 1, keepdim=True)
        detections = torch.cat((image_pred[:, :5], class_conf.float(), class_pred.float()), 1)
        unique_labels = detections[:, -1].cpu().unique()

        if prediction.is_cuda:
            unique_labels = unique_labels.cuda()

        for c in unique_labels:

            detections_class = detections[detections[:, -1] == c]
            _, conf_sort_index = torch.sort(detections_class[:, 4], descending=True)
            detections_class = detections_class[conf_sort_index]
            max_detections = []
            while detections_class.size(0):

                max_detections.append(detections_class[0].unsqueeze(0))
                if len(detections_class) == 1:
                    break
                ious = bbox_iou(max_detections[-1], detections_class[1:])
                detections_class = detections_class[1:][ious < nms_thres]
            max_detections = torch.cat(max_detections).data
            # Add max detections to outputs
            output[image_i] = max_detections if output[image_i] is None else torch.cat(
                (output[image_i], max_detections))

    return output

def bbox_iou(box1, box2, x1y1x2y2=True):
    """
        计算IOU
    """
    if not x1y1x2y2:
        b1_x1, b1_x2 = box1[:, 0] - box1[:, 2] / 2, box1[:, 0] + box1[:, 2] / 2
        b1_y1, b1_y2 = box1[:, 1] - box1[:, 3] / 2, box1[:, 1] + box1[:, 3] / 2
        b2_x1, b2_x2 = box2[:, 0] - box2[:, 2] / 2, box2[:, 0] + box2[:, 2] / 2
        b2_y1, b2_y2 = box2[:, 1] - box2[:, 3] / 2, box2[:, 1] + box2[:, 3] / 2
    else:
        b1_x1, b1_y1, b1_x2, b1_y2 = box1[:, 0], box1[:, 1], box1[:, 2], box1[:, 3]
        b2_x1, b2_y1, b2_x2, b2_y2 = box2[:, 0], box2[:, 1], box2[:, 2], box2[:, 3]

    inter_rect_x1 = torch.max(b1_x1, b2_x1)
    inter_rect_y1 = torch.max(b1_y1, b2_y1)
    inter_rect_x2 = torch.min(b1_x2, b2_x2)
    inter_rect_y2 = torch.min(b1_y2, b2_y2)

    inter_area = torch.clamp(inter_rect_x2 - inter_rect_x1 + 1, min=0) * \
                 torch.clamp(inter_rect_y2 - inter_rect_y1 + 1, min=0)

    b1_area = (b1_x2 - b1_x1 + 1) * (b1_y2 - b1_y1 + 1)
    b2_area = (b2_x2 - b2_x1 + 1) * (b2_y2 - b2_y1 + 1)

    iou = inter_area / (b1_area + b2_area - inter_area + 1e-16)

    return iou

def deal_data_img(image):
    '''
    获取得到（H,W,C）ndarray数组，进行处理，可以直接输入模型进行预测
    Args:
        img:

    Returns:

    '''
    image /= 255.0
    img = np.transpose(image, (2, 0, 1))
    photo = img.astype(np.float32)
    images = []
    images.append(photo)
    images = np.asarray(images)

    return images

def deal_pred_result(pred_image):
    '''
        处理输出后结果
        语义分割、变化检测：单波段（h,w）数组
        目标识别：结果数组 [[classId,score,xmin,xmax,ymin,ymax]]
        Args:
            outputs: 模型输出结果

        Returns:

        '''
    image_shape = np.array([1024, 1024])
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

if __name__ == '__main__':
    platform_arguments = parse_platform_arguments()
    prediction_image(**platform_arguments)
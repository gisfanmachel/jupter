# -------------------------------------#
#       创建YOLO类
# -------------------------------------#
import json
import geojson
import torch
import torch.nn as nn
from nets.yolo4 import YoloBody
from utils.utils import non_max_suppression, DecodeBox, yolo_correct_boxes
import warnings
import colorsys
import os
from geojson import Point, Feature, FeatureCollection, Polygon
import numpy as np
from typing import List, Iterable, Dict, Union
import cv2

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
# os.environ["CUDA_VISIBLE_DEVICES"] = "0"
warnings.filterwarnings('ignore')

basedir = os.path.abspath(os.path.dirname(__file__))

# 图片大小
load_size = [1024,1024]

classes_path = basedir + "/classes.txt"
anchors_path=basedir + "/oiltank_anchors.txt"
nms= "0.2"
score_threshold = 0.4
weights_file = basedir + "/weight/" +"model.pth"

# gpu 子进程
import multiprocessing
def gpu_process():
    # os.system('nvidia-smi -l 60 -f ' + outputSaveDir + '/gpu_nvidia-smi.log')
    os.system('nvidia-smi -l 1 ')

# --------------------------------------------#
#   使用自己训练好的模型预测需要修改2个参数
#   model_path和classes_path都需要修改！
# --------------------------------------------#
class YOLO(object):
    _defaults = {
        "model_image_size": (int(load_size[0]), int(load_size[1]),3),
        "cuda": True,
    }

    @classmethod
    def get_defaults(cls, n):
        if n in cls._defaults:
            return cls._defaults[n]
        else:
            return "Unrecognized attribute name '" + n + "'"

    # ---------------------------------------------------#
    #   初始化YOLO
    # ---------------------------------------------------#
    def __init__(self, **kwargs):
        self.__dict__.update(self._defaults)
        self.class_names = self._get_class()
        self.anchors = self._get_anchors()
        self.generate()

    # ---------------------------------------------------#
    #   获得所有的分类
    # ---------------------------------------------------#
    def _get_class(self):
        with open(classes_path) as f:
            class_names = f.readlines()
        class_names = [c.strip() for c in class_names]
        return class_names

    # ---------------------------------------------------#
    #   获得所有的先验框
    # ---------------------------------------------------#
    def _get_anchors(self):
        with open(anchors_path) as f:
            anchors = f.readline()
        anchors = [float(x) for x in anchors.split(',')]
        return np.array(anchors).reshape([-1, 3, 2])[::-1, :, :]

    # ---------------------------------------------------#
    #   获得所有的分类
    # ---------------------------------------------------#
    def generate(self):

        self.net = YoloBody(len(self.anchors[0]), len(self.class_names)).eval()

        # 加快模型训练的效率
        print('Loading weights into state dict...')
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        state_dict = torch.load(weights_file, map_location=device)
        self.net.load_state_dict(state_dict)

        if self.cuda:
            self.net = nn.DataParallel(self.net)
            self.net = self.net.cuda()


        self.yolo_decodes = []
        for i in range(3):
            self.yolo_decodes.append(
                DecodeBox(self.anchors[i], len(self.class_names), (self.model_image_size[1], self.model_image_size[0])))

        print('{} model, anchors, and classes loaded.'.format(weights_file))
        # 画框设置不同的颜色
        hsv_tuples = [(x / len(self.class_names), 1., 1.)
                      for x in range(len(self.class_names))]
        self.colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
        self.colors = list(
            map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)),
                self.colors))

    # ---------------------py-gpu-nms---------------------------#
    # 非极大值抑制的实现
    def py_cpu_nms(self, dets, thresh):

        if len(dets) == 0:
            return []
        """Pure Python NMS baseline."""
        dets = np.array(dets)
        # print(dets)
        x1 = dets[:, 2]
        y1 = dets[:, 3]
        x2 = dets[:, 4]
        y2 = dets[:, 5]
        scores = dets[:, 1]  # bbox打分
        boxes = []
        areas = (x2 - x1 + 1) * (y2 - y1 + 1)
        # 打分从大到小排列，取index
        order = scores.argsort()[::-1]
        # keep为最后保留的边框
        keep = []
        while order.size > 0:
            # order[0]是当前分数最大的窗口，肯定保留
            i = order[0]
            boxes.append(dets[i])
            keep.append(i)
            # 计算窗口i与其他所有窗口的交叠部分的面积
            xx1 = np.maximum(x1[i], x1[order[1:]])
            yy1 = np.maximum(y1[i], y1[order[1:]])
            xx2 = np.minimum(x2[i], x2[order[1:]])
            yy2 = np.minimum(y2[i], y2[order[1:]])

            w = np.maximum(0.0, xx2 - xx1 + 1)
            h = np.maximum(0.0, yy2 - yy1 + 1)
            inter = w * h
            # 交/并得到iou值
            ovr = inter / (areas[i] + areas[order[1:]] - inter)
            # inds为所有与窗口i的iou值小于threshold值的窗口的index，其他窗口此次都被窗口i吸收
            inds = np.where(ovr <= thresh)[0]
            # order里面只保留与窗口i交叠面积小于threshold的那些窗口，由于ovr长度比order长度少1(不包含i)，所以inds+1对应到保留的窗口
            order = order[inds + 1]

        return boxes
        # ----------------------------------#

    # -------------------------------nums2nums  overlap ----------------------------------------
    def mat_inter(self, dets, area_th_ratio):

        # 判断两个矩形是否相交
        # box=(xA,yA,xB,yB)
        boxes_no = []
        boxes_over = []
        if len(dets) <= 1:
            return dets
        # 判断两个矩形是否相交
        else:
            for i in range(len(dets) - 1):

                x01 = dets[i][2]
                y01 = dets[i][3]
                x02 = dets[i][4]
                y02 = dets[i][5]

                for j in range(i + 1, len(dets)):

                    x11 = dets[j][2]  # 取所有行第一列的数据
                    y11 = dets[j][3]
                    x12 = dets[j][4]
                    y12 = dets[j][5]

                    lx = abs((x01 + x02) / 2 - (x11 + x12) / 2)
                    ly = abs((y01 + y02) / 2 - (y11 + y12) / 2)
                    sax = abs(x01 - x02)
                    sbx = abs(x11 - x12)
                    say = abs(y01 - y02)
                    sby = abs(y11 - y12)
                    # --------------------相交--------------------------
                    if lx <= (sax + sbx) / 2 and ly <= (say + sby) / 2:

                        col = min(x02, x12) - max(x01, x11)
                        row = min(y02, y12) - max(y01, y11)
                        intersection = col * row
                        area1 = (x02 - x01) * (y02 - y01)
                        area2 = (x12 - x11) * (y12 - y11)

                        area1_ratio = intersection / area1
                        area2_ratio = intersection / area2
                        if area1_ratio > area_th_ratio:
                            boxes_over.append(list(dets[i]))
                            # else:
                            # boxes_no.append(list(dets[i]))
                            continue

                        if area2_ratio > area_th_ratio:
                            boxes_over.append(list(dets[j]))

                    else:  # 不相交
                        continue

            a1 = np.asarray(dets)
            a2 = np.asarray(boxes_over)

            a1_rows = a1.view([('', a1.dtype)] * a1.shape[1])
            a2_rows = a2.view([('', a2.dtype)] * a2.shape[1])

            return np.setdiff1d(a1_rows, a2_rows).view(a1.dtype).reshape(-1, a1.shape[1])

    def uint16to8(self, bands, lower_percent=0.001, higher_percent=99.999):
        out = np.zeros_like(bands).astype(np.uint8)  # .astype(np.float)
        n = bands.shape[2]
        for i in range(n):
            a = 0  # np.min(band)
            b = 255  # np.max(band)
            c = np.percentile(bands[:, :, i], lower_percent)
            d = np.percentile(bands[:, :, i], higher_percent)
            t = a + (bands[:, :, i] - c) * (b - a) / (d - c)
            t[t < a] = a
            t[t > b] = b
            out[:, :, i] = t

        return out

    # ----------------------------------------------------------#

    def get_region_boxes(self, patch_box, x_start, y_start):
        xmin = x_start + patch_box[2]
        ymin = y_start + patch_box[3]
        xmax = x_start + patch_box[4]
        ymax = y_start + patch_box[5]

        image_box = [patch_box[0], patch_box[1], xmin, ymin, xmax, ymax]
        return image_box

    def detect_tile(self, image):

        band_count = 3
        temp = int(load_size[1])
        mask_temp = np.zeros((temp, temp, band_count), dtype=np.uint8)
        mask_temp[0:image.shape[0], 0:image.shape[1], :] = image[:, :, :]
        x_start = 0
        y_start = 0

        out_boxes = []
        all_boxes = []

        image_shape = np.array(np.shape(mask_temp)[0:2])
        photo = np.array(mask_temp, dtype=np.float64)

        photo /= 255.0
        photo = np.transpose(photo, (2, 0, 1))
        photo = photo.astype(np.float32)
        images = []
        images.append(photo)
        images = np.asarray(images)

        with torch.no_grad():
            images = torch.from_numpy(images)
            if self.cuda:
                images = images.cuda()
            outputs = self.net(images)

        output_list = []
        for i in range(3):
            output_list.append(self.yolo_decodes[i](outputs[i]))
        output = torch.cat(output_list, 1)
        batch_detections = non_max_suppression(output, len(self.class_names),
                                                conf_thres=score_threshold,
                                                nms_thres=0.1)
        if batch_detections[0] is None:
            return None

        else:
            batch_detections = batch_detections[0].cpu().numpy()
            top_index = batch_detections[:, 4] * batch_detections[:, 5] > score_threshold
            top_conf = batch_detections[top_index, 4] * batch_detections[top_index, 5]
            top_label = np.array(batch_detections[top_index, -1], np.int32)
            top_bboxes = np.array(batch_detections[top_index, :4])
            top_xmin, top_ymin, top_xmax, top_ymax = np.expand_dims(top_bboxes[:, 0], -1), np.expand_dims(
                top_bboxes[:, 1],
                -1), np.expand_dims(
                top_bboxes[:, 2], -1), np.expand_dims(top_bboxes[:, 3], -1)

            # 去掉灰条
            boxes = yolo_correct_boxes(top_ymin, top_xmin, top_ymax, top_xmax,
                                        np.array([self.model_image_size[0], self.model_image_size[1]]),
                                        image_shape)
            for i, c in enumerate(top_label):
                score = top_conf[i]

                top, left, bottom, right = boxes[i]
                top = top - 1
                left = left - 1

                patch_box = [int(c), score, left, top, right, bottom]
                boxes_mc = self.get_region_boxes(patch_box, x_start, y_start)

                all_boxes.append(boxes_mc)

            out_boxes = self.py_cpu_nms(np.array(all_boxes), float(nms))

        features = []
        # f = open(basedir + '/result.txt', "w")
        for k, out_box in enumerate(out_boxes):
            cls_name = self.class_names[int(out_boxes[k][0])]
            score = out_boxes[k][1]

            #polgon 是闭合的，首尾要相同
            polygon = Polygon([[(int(out_boxes[k][2]), int(out_boxes[k][3])), (int(out_boxes[k][4]), int(out_boxes[k][3])),(int(out_boxes[k][4]), int(out_boxes[k][5])), (int(out_boxes[k][2]), int(out_boxes[k][5])), (int(out_boxes[k][2]), int(out_boxes[k][3]))]])
            feature = Feature(geometry=polygon, properties={"className":cls_name, "score": round(score, 4)})
            features.append(feature)
            # f.write("%s %s %s %s %s %s %s %s %s %s\n" % (
            #     cls_name, str(round(score, 4)), int(out_boxes[k][2]), int(out_boxes[k][3]), int(out_boxes[k][4]), int(out_boxes[k][3]),
            #     int(out_boxes[k][4]), int(out_boxes[k][5]), int(out_boxes[k][2]), int(out_boxes[k][5])))
        feature_collection = FeatureCollection(features)
        return geojson.dumps(feature_collection)


    def get_anchors(self,anchors_path):
        '''loads the anchors from a file'''
        with open(anchors_path) as f:
            anchors = f.readline()
        anchors = [float(x) for x in anchors.split(',')]
        return np.array(anchors).reshape([-1, 3, 2])[::-1, :, :]


    def yolo_decodes2(self):
        num_classes = len(self.class_names)
        anchors = self.get_anchors(basedir + '/oiltank_anchors.txt')

        yolo_decodes = []
        for i in range(3):
            yolo_decodes.append(
                DecodeBox(anchors[i], num_classes, (int(load_size[0]), int(load_size[1]))))
        return yolo_decodes

    def get_image_num(self,image):
        # gpu 监控
        # p = multiprocessing.Process(target=gpu_process)
        # p.daemen=True
        # p.start()
        
        band_count = 3
        temp = int(load_size[1])
        mask_temp = np.zeros((temp, temp, band_count), dtype=np.uint8)
        mask_temp[0:int(load_size[0]), 0:int(load_size[1]), :] = image[:, :, :]

        photo = np.array(mask_temp, dtype=np.float64)

        photo /= 255.0
        photo = np.transpose(photo, (2, 0, 1))
        photo = photo.astype(np.float32)
        images = []
        images.append(photo)
        images = np.asarray(images)

        with torch.no_grad():
            images = torch.from_numpy(images)
            if self.cuda:
                images = images.cuda()
            outputs = self.net(images)

        output_list = []
        for i in range(3):
            yolo_decodes = self.yolo_decodes2()
            output_list.append(yolo_decodes[i](outputs[i]))

        val_cat_outputs = torch.cat(output_list, 1)
        val_nms_outputs = non_max_suppression(val_cat_outputs, len(self.class_names), conf_thres=0.1, nms_thres=0.1)
        input_shape = (int(load_size[0]), int(load_size[1]))
        feature_collection = self.get_target_py( self.class_names, images, val_nms_outputs, input_shape,
                                    conf_thres=0.3, nms_thres=nms)
        return geojson.dumps(feature_collection)

    def get_target_py(self, class_names, images, batch_detections, \
                        input_shape, conf_thres, nms_thres):

        # class_names = ",".join([str(x) for x in class_names])
        # f = open(path + '/' + str(epoch) + str(iteration) + '.txt', "w")
        image = images[0, :, :, :].cpu().numpy().transpose((1, 2, 0)) * 255
        image_shape = np.array(np.shape(image)[0:2])
        all_boxes = []
        count = 0
        if batch_detections[0] is not None:

            batch_detections = batch_detections[0].cpu().numpy()
            top_index = batch_detections[:, 4] * batch_detections[:, 5] > conf_thres
            top_conf = batch_detections[top_index, 4] * batch_detections[top_index, 5]
            top_label = np.array(batch_detections[top_index, -1], np.int32)
            top_bboxes = np.array(batch_detections[top_index, :4])
            top_xmin, top_ymin, top_xmax, top_ymax = np.expand_dims(top_bboxes[:, 0], -1), np.expand_dims(
                top_bboxes[:, 1],
                -1), np.expand_dims(
                top_bboxes[:, 2], -1), np.expand_dims(top_bboxes[:, 3], -1)

            boxes = yolo_correct_boxes(top_ymin, top_xmin, top_ymax, top_xmax,
                                       np.array([input_shape[0], input_shape[1]]),
                                       image_shape)
            for i, c in enumerate(top_label):
                predicted_class = class_names
                score = top_conf[i]

                top, left, bottom, right = boxes[i]
                top = top - 5
                left = left - 5
                bottom = bottom + 5
                right = right + 5
                top = max(0, np.floor(top + 0.5).astype('int32'))
                left = max(0, np.floor(left + 0.5).astype('int32'))
                bottom = min(np.shape(image)[0], np.floor(bottom + 0.5).astype('int32'))
                right = min(np.shape(image)[1], np.floor(right + 0.5).astype('int32'))

                patch_box = [int(c), score, left, top, right, bottom]
                # boxes_mc = self.get_region_boxes(patch_box, x_start, y_start)

                all_boxes.append(patch_box)
            count += 1

        out_boxes = self.py_cpu_nms(np.array(all_boxes), float(nms_thres))


        features = []
        for i, out_box in enumerate(out_boxes):
            predicted_class = class_names[int(out_boxes[i][0])]
            score = out_boxes[i][1]

            left, top, right, bottom = out_boxes[i][2], out_boxes[i][3], out_boxes[i][4], out_boxes[i][5]
            top = top - 5
            left = left - 5
            bottom = bottom + 5
            right = right + 5

            top = max(0, np.floor(top + 0.5).astype('int32'))
            left = max(0, np.floor(left + 0.5).astype('int32'))
            bottom = min(np.shape(image)[0], np.floor(bottom + 0.5).astype('int32'))
            right = min(np.shape(image)[1], np.floor(right + 0.5).astype('int32'))

            polygon = Polygon([[(int(left), int(top)),(int(right), int(top)),(int(right), int(bottom)),(int(left), int(bottom)),(int(left), int(top))]])
            feature = Feature(geometry=polygon, properties={"className": predicted_class, "score": round(score, 4)})
            features.append(feature)

        feature_collection = FeatureCollection(features)
        print('feature_collection========================')
        print(feature_collection)
        return feature_collection



class PredictModel:
    def __init__(self):
        self.yolo = YOLO()
    #names和meta为可选参数，预留参数。函数返回类型是ndarray
    def predict(self, X: np.ndarray, names: Iterable[str] = None, meta: Dict = None) -> Union[np.ndarray, List, str, bytes]:
        # return self.yolo.detect_tile(X)
        if X.shape[0] < int(load_size[0]) or X.shape[1] < int(load_size[0]):
            img = np.zeros((int(load_size[0]),int(load_size[1]),X.shape[2]))
            img[0:X.shape[0],0:X.shape[1],:] = X
            X = img

        return np.frombuffer(str.encode(self.yolo.get_image_num(X)), dtype=np.uint8)

#调用示例，测试
if __name__ == '__main__':
    # p = multiprocessing.Process(target=gpu_process)
    # p.daemen=True
    # p.start()
    image = cv2.imread("./oil.png")
    #model对象在http服务中会一直存在
    model = PredictModel()
    model.predict(image)

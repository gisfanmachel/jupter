import json
import time

import cv2
import numpy as np
import shutil

from pie.train_center.pytorch.utils_obj import yolo_correct_boxes, py_cpu_nms
from pie.utils.registry import Registry

ImageFont_path = 'pie/utils/voc_weight/simhei.ttf'

# 根据保存中间图片的策略，进行输出中间图片宿主列表
def middle_image_array(middle_metrics_list, middle_results_count,image_list, mean_metric):
    middle_metrics_parmas_dict, middle_image_dict = middle_metrics_list[0],middle_metrics_list[1]
    i = len(middle_metrics_parmas_dict)

    if mean_metric:
        if len(middle_metrics_parmas_dict.keys()) < middle_results_count:
            middle_image_dict[i + 1] = mean_metric
            middle_metrics_parmas_dict[i + 1] = image_list
        else:
            min_pre = min(middle_image_dict.values())
            min_index = 0
            for key, value in middle_image_dict.items():
                if value == min_pre:
                    min_index = key
            for key, value in middle_metrics_parmas_dict.items():

                if key == min_index and mean_metric < min_pre:
                    middle_metrics_parmas_dict[key] = image_list

    return [middle_metrics_parmas_dict, middle_image_dict]


# 数组生成中间图片
def save_picture(epoch,middle_results_dict, network_type,root_path, trainval_color_mapping,class_names,input_shape):
    epoch = epoch+1
    for index_, image_array in middle_results_dict.items():

        if len(image_array) == 4:
            img = image_array[0]
            img2 = image_array[1]
            mask = image_array[2]
            pred = image_array[3]
        else:
            img2 = None
            img = image_array[0]
            mask = image_array[1]
            pred = image_array[2]

        img_bands, height, width = img.shape

        if network_type != 2:
            mask = classToRGB(mask, height, width, trainval_color_mapping)
            pred = classToRGB(pred, height, width, trainval_color_mapping)
            if img_bands > 3:
                img = img[:3, :, :]

            # imge处理
            img = stre_to_8(img)

            if not img2 is None:
                img2 = img2[:3, :, :]
                img2 = stre_to_8(img2)

                cv2.imwrite(root_path + str(epoch) + '_' + str(index_) + "_A" + '.png', img.transpose((1, 2, 0)))
                cv2.imwrite(root_path + str(epoch) + '_' + str(index_) + "_B" + '.png', img2.transpose((1, 2, 0)))
            else:
                cv2.imwrite(root_path + str(epoch) + '_' + str(index_) + "_image" + '.png', img.transpose((1, 2, 0)))

            cv2.imwrite(root_path + str(epoch) + '_' + str(index_) + "_label" + '.png', mask)
            cv2.imwrite(root_path + str(epoch) + '_' + str(index_) + "_pred" + '.png', pred)
        else:
            save_val_images(class_names, img, pred,
                    input_shape, root_path + str(epoch) + '_' + str(index_) + '_', trainval_color_mapping)


from PIL import Image, ImageDraw, ImageFont
def save_val_images(class_names, images, batch_detections, \
                    input_shape, path, trainval_color_mapping,conf_thres=0.3, nms_thres=0.3):
    # colors = color_array
    image = images.transpose((1, 2, 0)) * 255
    image_shape = np.array(np.shape(image)[0:2])
    all_boxes = []
    count = 0

    if batch_detections is not None:

        # batch_detections = batch_detections[0].cpu().numpy()
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
        font = ImageFont.truetype(font=ImageFont_path,
                                  size=np.floor(3e-2 * np.shape(image)[1] + 0.5).astype('int32'))

        thickness = (np.shape(image)[0] + np.shape(image)[1]) // input_shape[0]
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

    out_boxes = py_cpu_nms(np.array(all_boxes), float(nms_thres))

    img = image
    if len(out_boxes) > 0:
        for i, out_box in enumerate(out_boxes):
            predict_value = int(out_boxes[i][0])

            predicted_class = class_names[predict_value]
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

            label = '{} {:.2f}'.format(predicted_class, score)
            image = np.array(np.uint8(image))
            image = Image.fromarray(image)
            draw = ImageDraw.Draw(image)

            label_size = draw.textsize(label, font)
            label = label.encode('utf-8')
            if top - label_size[1] >= 0:
                text_origin = np.array([left, top - label_size[1]])
            else:
                text_origin = np.array([left, top + 1])
            for i in range(thickness):
                draw.rectangle(
                    [left + i, top + i, right - i, bottom - i],
                    outline=trainval_color_mapping[predict_value])
            draw.rectangle(
                [tuple(text_origin), tuple(text_origin + label_size)],
                fill=trainval_color_mapping[predict_value])
            draw.text(text_origin, str(label, 'UTF-8'), fill=(0, 0, 0), font=font)
            image.save(path + "pred_" + '.png')
            del draw
    else:
        cv2.imwrite(path + "pred_" + '.png', img)

def classToRGB(mask, height, width, trainval_color_mapping):
    colmap = np.zeros(shape=(height, width, 3)).astype(np.uint8)
    for trainval in trainval_color_mapping.keys():
        indices = np.where(mask == trainval)
        colmap[indices[0].tolist(),
        indices[1].tolist(), :] = np.array(trainval_color_mapping[trainval])
    return colmap


#拉伸图像 统一拉到8位
def stre_to_8(bands):
    out = np.zeros_like(bands, dtype=np.uint8)
    n = bands.shape[0]
    for i in range(n):
        n = Registry['stretching']
        t = n(bands[i, :, :], [0, 255])
        out[i, :, :] = t
    return out



def trainlog_json_epoch(best_,log_init, epoch, epoch_all, loss, epoch_metrics_dict_list, class_name_list, result_path,
                        log_train=True):
    '''
    记录日志信息
    :param log_init:
    :param epoch_log: {"epoch":str(epoch+1),"train":[],"valid":[]}
    :param train_loss:
    :param valid_loss:
    :param train_epoch_metrics_dict_list:
    :param valid_epoch_metrics_dict_list:
    :return:
    '''

    # log_init["best"] = {"train": {}, "valid": {}}
    if log_train:
        epoch_log = {'epoch': int(epoch + 1), "train": [],"valid": []}
    else:
        log_count = len(log_init["epochs"])
        epoch_log = log_init["epochs"][log_count-1]

    epoch_dict_all = {"class": "all", "values": {}}
    best_log={}
    epoch_log_list_dict = {}
    one_class = False

    if len(epoch_metrics_dict_list) > 0:

        # for index, class_name in enumerate(class_name_list):
        #     epoch_log_list_dict[class_name] = {}

        for i, metrics_dict in enumerate(epoch_metrics_dict_list):
            for key, value in metrics_dict.items():
                params = key.split('_')[0]
                value_type = key.split('_')[1]
                if value_type == "all":
                    epoch_dict_all['values'][params] = value
                if value_type == "part":
                    if len(value) > 2:
                        one_class = True
                        for class_index in range(len(value)):
                            if value[class_index] != "background":
                                epoch_log_list_dict[class_name_list[class_index]][params] = value[class_index]
                    # one_class = True
                    # for class_index in range(len(value)):
                    #     epoch_log_list_dict[class_name_list[class_index]][params] = value[class_index]

        if one_class:
            for classname, metrics in epoch_log_list_dict.items():
                epoch_dict_mean = {"class": classname, "values": metrics}
                if log_train:
                    epoch_log['train'].append(epoch_dict_mean)
                else:
                    epoch_log['valid'].append(epoch_dict_mean)
        if loss:
            epoch_dict_all['values']['loss'] = loss
        if log_train:
            epoch_log['train'].append(epoch_dict_all)
            log_init["best"] = best_
        else:
            epoch_log['valid'].append(epoch_dict_all)
    else:
        if log_train:
            epoch_log['train'].append([])
        else:
            epoch_log['valid'].append([])
    if log_train:
        log_init["epochs"].append(epoch_log)

    if epoch == epoch_all - 1:
        end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        log_init["end_time"] = end_time
        # shutil.rmtree('/tempdataset')

    trainlog = json.dumps(log_init, indent=4)
    with open(result_path, 'w',
              encoding='utf-8') as log_file:
        log_file.write(trainlog)
    print("[Process: {process}]".format(process=str(epoch + 1) + '/' + str(epoch_all)))

    return log_init

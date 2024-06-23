# from sample_access_interface import sample_access_interface
import glob
import os
import torch
import torch.utils.data as data
import skimage.io
import io
# from PIL import Image
import cv2
# from shutil import copyfile
import numpy as np
# from osgeo import gdal
# from torch.utils.data import DataLoader
import pie.dataset.ehance
# from registry import Registry
from pie.utils import aiUtils
import xml.etree.ElementTree as ET

s3Client = aiUtils.s3GetImg()
gdal = s3Client.gdal
keyFormatDict = {"png": "PNG",
                 "tif": "GTiff",
                 "tiff": "GTiff",
                 "jpg": "JPEG",
                 "jpeg": "JPEG",
                 "TIF": "GTiff",
                 "bmp": "BMP"}

networkTypeFileDict = {
    1: ['images', 'labels'],
    3: ['A', 'labels', 'B'],
    2: ['images', 'labels']
}


def get_dataset_samples_path(set_path, network_type,class_name_list):
    file_list = networkTypeFileDict[network_type]

    if set_path.split('/')[0] == 's3:':
        data_path = "/".join(set_path.split("/")[3:])
        files = s3Client.getImages(data_path + file_list[0])

        if network_type == 2:
            label_key = 'xml'
        else:
            label_key = s3Client.getImages(data_path + file_list[1])[0].split('.')[-1]
        s3KeyPre = "/".join(set_path.split("/")[:3]) + "/"
    else:
        files = glob.glob(set_path + file_list[0] + '/*.jpg') + glob.glob(set_path + file_list[0] + '/*.tif') + \
                glob.glob(set_path + file_list[0] + '/*.tiff') + glob.glob(set_path + file_list[0] + '/*.bmp') + \
                glob.glob(set_path + file_list[0] + '/*.png')
        label_key = glob.glob(set_path + file_list[1] + '/*.jpg') + glob.glob(set_path + file_list[1] + '/*.tif') + \
                    glob.glob(set_path + file_list[1] + '/*.tiff') + glob.glob(set_path + file_list[1] + '/*.bmp') + \
                    glob.glob(set_path + file_list[1] + '/*.png') + glob.glob(set_path + file_list[1] + '/*.xml')
        label_key = label_key[0].split('.')[-1]
        s3KeyPre = ""
    files_key = files[0].split('.')[-1]
    imagelist = []
    image2list = []
    labellist = []
    for imgFile in files:
        if network_type == 1:
            labelfile = imgFile.replace(file_list[0], file_list[1]).replace(files_key, label_key)
            labellist.append(s3KeyPre + labelfile)
        if network_type == 2:
            labelfile = imgFile.replace(file_list[0], file_list[1]).replace(files_key, label_key)
            labelfilex=load_xml(labelfile,class_name_list)
            labellist.append(labelfilex)
        elif network_type == 3:
            files2 = imgFile.replace(file_list[0], file_list[2])
            labelfile = imgFile.replace(file_list[0], file_list[1]).replace(files_key, label_key)
            labellist.append(s3KeyPre + labelfile)
            image2list.append(s3KeyPre + files2)
        imagelist.append(s3KeyPre + imgFile)
        # labellist.append(s3KeyPre + labelfile)
    return imagelist, image2list, labellist

def load_xml(xmlPath,classes):
    if xmlPath.split('/')[0] == 's3:':
        xmlPath = "/".join(xmlPath.split("/")[3:])
        dataBody = s3Client.getImgXmlArray(xmlPath)
        root = ET.fromstring(dataBody)
    else:
        in_file = open(xmlPath)
        tree = ET.parse(in_file)
        root = tree.getroot()

    labels = ""
    height = int(tree.findtext('./size/height'))
    width = int(tree.findtext('./size/width'))
    for obj in root.iter('object'):

        cls = obj.find('name').text
        if cls not in classes:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        len_ = len(list(xmlbox))
        if len_ == 4:
            b = (int(round(float(xmlbox.find('xmin').text))), int(round(float(xmlbox.find('ymin').text))),
                 int(round(float(xmlbox.find('xmax').text))),
                 int(round(float(xmlbox.find('ymax').text))))
        elif len_ > 4:
            i = 1
            xvalue = []
            yvalue = []
            for ele in list(xmlbox):
                value = int(round(float(ele.text)))
                if i % 2 == 0:
                    yvalue.append(value)
                else:
                    xvalue.append(value)
                i += 1
            xmin = min(xvalue)
            xmax = max(xvalue)
            ymin = min(yvalue)
            ymax = max(yvalue)
            b = (xmin, ymin, xmax, ymax)
        else:
            raise Exception(" bndbox not element in xml !")
        labels += " " + ",".join([str(a) for a in b]) + ',' + str(cls_id)
    labels += ' ' + str(height) + ',' + str(width)
    # print(labels)
    return labels

def load_img(line='', newline=''):
    #######TODO gdal读取图片#######################
    '''random preprocessing for real-time data augmentation'''
    if os.path.exists(newline):
        imagepath = newline
        try:
            image = gdal.Open(imagepath)
            image = image.ReadAsArray()
        except:
            print('wrong')
            return load_img(line, '')
    else:
        imagepath = line.replace("s3://", "")
        imagepath = f"/vsis3/{imagepath}"
        image = gdal.Open(imagepath)
        driverName = keyFormatDict[line.split('.')[-1]]
        outputDirver = gdal.GetDriverByName(driverName)
        outputDirver.CreateCopy(newline, image)
        image = image.ReadAsArray()
    if len(image.shape) == 3:
        image = image.transpose(1, 2, 0)
        # print(image.shape, np.max(image))
    return image



# 将类别信息转换为颜色值
def convert_to_color(arr_2d, palette):
    arr_3d = np.zeros((arr_2d.shape[0], arr_2d.shape[1], 3),
                      dtype=np.uint8)

    for c, i in palette.items():
        m = arr_2d == c
        arr_3d[m] = i

    return arr_3d


# 将颜色值转换为类别
def convert_from_color(arr_3d, palette):
    arr_2d = np.zeros((arr_3d.shape[0], arr_3d.shape[1]),
                      dtype=np.uint8)
    for c, i in palette.items():
        m = np.all(arr_3d == np.array(c).reshape(1, 1, 3),
                   axis=2)
        arr_2d[m] = i
    return arr_2d


# 将类别值转换成训练的像素值，按序号进行递增
def convert_train_and_class_value(arr_2d, palette):
    train_arr = np.zeros((arr_2d.shape[0], arr_2d.shape[1]),
                         dtype=np.uint8)
    for c, i in palette.items():
        m = arr_2d == c
        train_arr[m] = i
    return train_arr


def str_to_label(label):
    labels = eval(label)
    invert_palette = {}
    train_value_palette = {}
    for i, val in enumerate(labels):
        color_tuple = None
        value = -1
        name = ''
        for key in val.keys():
            if key == "class_color":
                color_ = val[key]
                color_tuple = tuple(np.array(color_.split(',')).astype(int))
            elif key == "class_value":
                value = int(val[key])
                train_value = int(i)
            elif key == 'class_name':
                name = val[key]
            else:
                continue
        if name and color_tuple and value >= 0:
            invert_palette[color_tuple] = value
            train_value_palette[value] = train_value
    return invert_palette, train_value_palette


##################################################

def cas_iou(box, cluster):
    x = np.minimum(cluster[:, 0], box[0])
    y = np.minimum(cluster[:, 1], box[1])

    intersection = x * y
    area1 = box[0] * box[1]

    area2 = cluster[:, 0] * cluster[:, 1]
    # print((area1 + area2 - intersection))
    iou = intersection / (area1 + area2 - intersection)

    return iou


def avg_iou(box, cluster):
    return np.mean([np.max(cas_iou(box[i], cluster)) for i in range(box.shape[0])])


def kmeans(box, k):
    # 取出一共有多少框
    row = box.shape[0]

    # 每个框各个点的位置
    distance = np.empty((row, k))

    # 最后的聚类位置
    last_clu = np.zeros((row,))

    np.random.seed()

    # 随机选5个当聚类中心
    cluster = box[np.random.choice(row, k, replace=False)]
    # cluster = random.sample(row, k)
    while True:
        # 计算每一行距离五个点的iou情况。
        for i in range(row):
            distance[i] = 1 - cas_iou(box[i], cluster)
        # 取出最小点
        near = np.argmin(distance, axis=1)

        if (last_clu == near).all():
            break
        # 求每一个类的中位点
        for j in range(k):
            d = box[near == j]
            if len(d)==0:
                continue
            cluster[j] = np.median(d, axis=0)

        last_clu = near

    return cluster

def load_data(data):
    data1=[]
    for i in data:
        # print(data,'\n\n\n\n')
        x=i.split()[:-1]
        height,width=eval(i.split()[-1])
        for j in x:
            xmin = int(float(j.split(',')[0])) / width
            ymin = int(float(j.split(',')[1])) / height
            xmax = int(float(j.split(',')[2])) / width
            ymax = int(float(j.split(',')[3])) / height

            xmin = np.float64(xmin)
            ymin = np.float64(ymin)
            xmax = np.float64(xmax)
            ymax = np.float64(ymax)

            # 得到宽高
            data1.append([xmax - xmin, ymax - ymin])
    return np.array(data1)

def GetAnchors(images_size, label_list,outputfile):
    SIZE = images_size[0]
    anchors_num = 9
    # label_list_1=[i for i in label_list]
    data = load_data(label_list)
    # print(data)
    # print('cccccc')
    # 使用k聚类算法
    out = kmeans(data, anchors_num)
    # print('bbbbbbb')
    out = out[np.argsort(out[:, 0])]
    # print('acc:{:.2f}%'.format(avg_iou(data, out) * 100))
    data = out * SIZE
    f = open(outputfile + "pre_anchors.txt", 'w')
    row = np.shape(data)[0]
    # print('aaaaaaa')
    for i in range(row):
        if i == 0:
            x_y = "%d,%d" % (data[i][0], data[i][1])
        else:
            x_y = ", %d,%d" % (data[i][0], data[i][1])
        f.write(x_y)
    return data
# from sample_access_interface import sample_access_interface
import torch
import torch.utils.data as data
import skimage.io
import io
from PIL import Image
import cv2
import numpy as np
# from osgeo import gdal
from torch.utils.data import DataLoader
import pie.dataset.ehance
from pie.utils.registry import Registry
from pie.dataset.dataset_utils import get_dataset_samples_path,load_img,convert_to_color,convert_from_color,convert_train_and_class_value,str_to_label,GetAnchors
from pie.utils import aiUtils
from pie.utils import dist_utils
import os
import random
import shutil
# from pie.dataset.kmeans_for_anchors import GetAnchors
import subprocess
import shlex
# import os
import time
from PIL import Image

s3Client = aiUtils.s3GetImg()
gdal = s3Client.gdal


class torch_dataset:
    def __init__(self, data_path,
               ehance=None,
               type='train/',
               network_type = 1,
               palette=None,
               train_value_palette=None,
               class_name_list=None,
               mosaic=False,
               image_size=None):
        # self.dataset_path=s3Client.path
        self.dataset_path = data_path
        self.network_type=network_type
        self.palette = palette
        self.train_value_palette = train_value_palette
        self.class_name_list = class_name_list
        self.mosaic=mosaic
        self.image_size=image_size

        # self.dataset_path = './data/tempdataset/'
        # self.dataset_path ="s3://pie-engine-ai/devel/system/dataset/segmentation/test_train/"

        self.type=type
        # self.dataset_path = self.dataset_path + self.type
        # self.temppicDir = os.path.abspath(os.path.dirname("train.py")) + '/data/tempdataset/' + self.type
        self.temppicDir = os.path.join(self.dataset_path, self.type)
        self.image_file_list, self.image2_file_list,self.label_file_list = get_dataset_samples_path(self.temppicDir,self.network_type,self.class_name_list)
        if self.network_type==2:
            self.lines = list(zip(self.image_file_list, self.label_file_list))
        self.image_file_list_org=[a for a in self.image_file_list]
        self.label_file_list_org=[a for a in self.label_file_list]
        if self.network_type == 3:
            self.image2_file_list_org = [a for a in self.image2_file_list]

        if ehance == None:
            self.ehance = [  # 流程， 由之前创建的 train_pipeline 传递进来。
                dict(name='randomShiftScaleRotate'),
                dict(name='randomHorizontalFlip'),
                dict(name='randomVerticleFlip'),
                dict(name='randomRotate90'),
                dict(name='Normalization')]
        else:
            self.ehance = eval(ehance)

    def __getitem__(self, index):
        if self.network_type == 1 or self.network_type == 3:
            image2_file = None
            # print(self.image_file_list_org[index])
            image_file = self.image_file_list_org[index]
            label_file = self.label_file_list_org[index]
            if len(self.image2_file_list) > 0:
                image2_file = self.image2_file_list[index]
            # print(image_file)
            img2 = None
            if image_file.split('/')[0] == "s3:":
                self.image_file_list[index] = self.temppicDir + image_file.split(self.type)[-1]
                self.label_file_list[index] = self.temppicDir + label_file.split(self.type)[-1]
                img = load_img(line=image_file, newline=self.image_file_list[index])
                mask = load_img(line=label_file, newline=self.label_file_list[index])
                if len(self.image2_file_list) > 0:
                    self.image2_file_list[index] = self.temppicDir + image2_file.split(self.type)[-1]
                    img2 = load_img(image_file, self.image2_file_list[index])
            else:
                img = load_img(newline=image_file)
                mask = load_img(newline=label_file)
                if image2_file:
                    img2 = load_img(newline=image2_file)
            for i in self.ehance:
                u = i.get('random')
                if u == None:
                    i['random'] = 0.5
                # if i.get('name') == 'LambdaDef':
                #     try:
                #         exec('import ' + i.get('path').replace('./', '').replace('.py', '').replace('/', '.'))
                #         ehancefun = Registry[i.get('name')]
                #         if np.random.random() < i['random']:
                #             img, img2, mask = ehancefun(img, img2, mask)
                #     except:
                #         print(i.get('type'), '出错！')
                # else:
                try:
                    ehancefun = Registry[i.get('name')]
                    img, img2, mask = ehancefun(img, img2, mask, i)
                except:
                    print(i.get('name'), '出错！')
            img = np.array(img.transpose(2, 0, 1), np.float32)
            if not img2 is None:
                img2 = np.array(img2.transpose(2, 0, 1), np.float32)
            ######################################################################################################
            if mask.ndim == 3:
                if not self.palette:
                    raise RuntimeError("No rgb color to class value palette!")
                mask = convert_from_color(mask, self.palette)
                # 将样本标注mask转换成train_value
            if self.train_value_palette:
                mask = convert_train_and_class_value(mask, self.train_value_palette)
            mask = mask
            mask = np.array(mask, np.int64)
            img = torch.Tensor(img)
            mask = torch.Tensor(mask).long()
            if not img2 is None:
                img2 = torch.Tensor(img2)
                return img, img2, mask
            # print(img.shape)
            return img, mask

        elif self.network_type==2:
            if index == 0:
                self.lines = list(zip(self.image_file_list, self.label_file_list))
                random.shuffle(self.lines)
            lines = self.lines
            n = len(self.lines)
            index = index % n
            if self.mosaic:
                if self.flag and (index + 4) < n:
                    img, y = self.get_random_data_with_Mosaic(lines[index:index + 4], self.image_size[0:2])
                else:
                    img, y = self.get_random_data(lines[index], self.image_size[0:2])
                self.flag = bool(1 - self.flag)
            else:
                img, y = self.get_random_data(lines[index], self.image_size[0:2])
            if len(y) != 0:
                boxes = np.array(y[:, :4], dtype=np.float32)
                boxes[:, 0] = boxes[:, 0] / self.image_size[1]
                boxes[:, 1] = boxes[:, 1] / self.image_size[0]
                boxes[:, 2] = boxes[:, 2] / self.image_size[1]
                boxes[:, 3] = boxes[:, 3] / self.image_size[0]

                boxes = np.maximum(np.minimum(boxes, 1), 0)
                boxes[:, 2] = boxes[:, 2] - boxes[:, 0]
                boxes[:, 3] = boxes[:, 3] - boxes[:, 1]

                boxes[:, 0] = boxes[:, 0] + boxes[:, 2] / 2
                boxes[:, 1] = boxes[:, 1] + boxes[:, 3] / 2
                y = np.concatenate([boxes, y[:, -1:]], axis=-1)

            img = np.array(img, dtype=np.float32)
            tmp_inp = np.transpose(img / 255.0, (2, 0, 1))
            tmp_targets = np.array(y, dtype=np.float32)
            return tmp_inp, tmp_targets
        else:
            print('wrong network type!')
            return None

    def __len__(self):
        return len(self.image_file_list)

    def get_random_data(self, annotation_line, input_shape, jitter=.3, hue=.1, sat=1.5, val=1.5):
        """实时数据增强的随机预处理"""
        line = annotation_line

        # if self.s3Utils.path.split('/')[0] == 's3:':
        #     xmlbody = self.s3Utils.getImgXmlArray(line[0])
        #     image = Image.open(io.BytesIO(xmlbody))
        # else:
        #     image = Image.open(line[0])
        image = Image.open(line[0])
        # image=load_img(newline=line[0])
        iw, ih = image.size
        h, w = input_shape
        label_line=line[1].split()[:-1]
        box = np.array([np.array(list(map(int, box.split(',')))) for box in label_line])

        # 调整图片大小
        new_ar = w / h * self.rand(1 - jitter, 1 + jitter) / self.rand(1 - jitter, 1 + jitter)
        scale = 1
        #scale = self.rand(.25, 2)
        if new_ar < 1:
            nh = int(scale * h)
            nw = int(nh * new_ar)
        else:
            nw = int(scale * w)
            nh = int(nw / new_ar)
        image = image.resize((nw, nh), Image.BICUBIC)

        # 放置图片
        dx = int(self.rand(0, w - nw))
        dy = int(self.rand(0, h - nh))
        new_image = Image.new('RGB', (w, h),
                              (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255)))
        new_image.paste(image, (dx, dy))
        image = new_image

        # 是否翻转图片
        flip = self.rand() < .5
        if flip:
            image = image.transpose(Image.FLIP_LEFT_RIGHT)

        # 色域变换
        hue = self.rand(-hue, hue)
        sat = self.rand(1, sat) if self.rand() < .5 else 1 / self.rand(1, sat)
        val = self.rand(1, val) if self.rand() < .5 else 1 / self.rand(1, val)
        x = cv2.cvtColor(np.array(image,np.float32)/255, cv2.COLOR_RGB2HSV)
        x[..., 0] += hue*360
        x[..., 0][x[..., 0]>1] -= 1
        x[..., 0][x[..., 0]<0] += 1
        x[..., 1] *= sat
        x[..., 2] *= val
        x[x[:,:, 0]>360, 0] = 360
        x[:, :, 1:][x[:, :, 1:]>1] = 1
        x[x<0] = 0
        image_data = cv2.cvtColor(x, cv2.COLOR_HSV2RGB)*255

        # 调整目标框坐标
        box_data = np.zeros((len(box), 5))
        if len(box) > 0:
            np.random.shuffle(box)
            box[:, [0, 2]] = box[:, [0, 2]] * nw / iw + dx
            box[:, [1, 3]] = box[:, [1, 3]] * nh / ih + dy
            if flip:
                box[:, [0, 2]] = w - box[:, [2, 0]]
            box[:, 0:2][box[:, 0:2] < 0] = 0
            box[:, 2][box[:, 2] > w] = w
            box[:, 3][box[:, 3] > h] = h
            box_w = box[:, 2] - box[:, 0]
            box_h = box[:, 3] - box[:, 1]
            box = box[np.logical_and(box_w > 1, box_h > 1)]  # 保留有效框
            box_data = np.zeros((len(box), 5))
            box_data[:len(box)] = box
        if len(box) == 0:
            return image_data, []

        if (box_data[:, :4] > 0).any():
            return image_data, box_data
        else:
            return image_data, []

    def get_random_data_with_Mosaic(self, annotation_line, input_shape, hue=.1, sat=1.5, val=1.5):
        h, w = input_shape
        min_offset_x = 0.3
        min_offset_y = 0.3
        scale_low = 1 - min(min_offset_x, min_offset_y)
        scale_high = scale_low + 0.2

        image_datas = []
        box_datas = []
        index = 0

        place_x = [0, 0, int(w * min_offset_x), int(w * min_offset_x)]
        place_y = [0, int(h * min_offset_y), int(w * min_offset_y), 0]
        for line in annotation_line:

            image = Image.open(line[0])
            image = image.convert("RGB")
            # 图片的大小
            iw, ih = image.size
            # 保存框的位置
            label_line = line[1].split()[:-1]
            box = np.array([np.array(list(map(int, box.split(',')))) for box in label_line])

            # 是否翻转图片
            flip = self.rand() < .5
            if flip and len(box) > 0:
                image = image.transpose(Image.FLIP_LEFT_RIGHT)
                box[:, [0, 2]] = iw - box[:, [2, 0]]

            # 对输入进来的图片进行缩放
            new_ar = w / h
            scale = self.rand(scale_low, scale_high)
            if new_ar < 1:
                nh = int(scale * h)
                nw = int(nh * new_ar)
            else:
                nw = int(scale * w)
                nh = int(nw / new_ar)
            image = image.resize((nw, nh), Image.BICUBIC)

            # 进行色域变换
            hue = self.rand(-hue, hue)
            sat = self.rand(1, sat) if self.rand() < .5 else 1 / self.rand(1, sat)
            val = self.rand(1, val) if self.rand() < .5 else 1 / self.rand(1, val)
            x = cv2.cvtColor(np.array(image,np.float32)/255, cv2.COLOR_RGB2HSV)
            x[..., 0] += hue*360
            x[..., 0][x[..., 0]>1] -= 1
            x[..., 0][x[..., 0]<0] += 1
            x[..., 1] *= sat
            x[..., 2] *= val
            x[x[:,:, 0]>360, 0] = 360
            x[:, :, 1:][x[:, :, 1:]>1] = 1
            x[x<0] = 0
            image = cv2.cvtColor(x, cv2.COLOR_HSV2RGB) # numpy array, 0 to 1

            image = Image.fromarray((image * 255).astype(np.uint8))
            # 将图片进行放置，分别对应四张分割图片的位置
            dx = place_x[index]
            dy = place_y[index]
            new_image = Image.new('RGB', (w, h),
                                  (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255)))
            new_image.paste(image, (dx, dy))
            image_data = np.array(new_image)

            index = index + 1
            box_data = []
            # 对box进行重新处理
            if len(box) > 0:
                np.random.shuffle(box)
                box[:, [0, 2]] = box[:, [0, 2]] * nw / iw + dx
                box[:, [1, 3]] = box[:, [1, 3]] * nh / ih + dy
                box[:, 0:2][box[:, 0:2] < 0] = 0
                box[:, 2][box[:, 2] > w] = w
                box[:, 3][box[:, 3] > h] = h
                box_w = box[:, 2] - box[:, 0]
                box_h = box[:, 3] - box[:, 1]
                box = box[np.logical_and(box_w > 1, box_h > 1)]
                box_data = np.zeros((len(box), 5))
                box_data[:len(box)] = box

            image_datas.append(image_data)
            box_datas.append(box_data)

        # 将图片分割，放在一起
        cutx = np.random.randint(int(w * min_offset_x), int(w * (1 - min_offset_x)))
        cuty = np.random.randint(int(h * min_offset_y), int(h * (1 - min_offset_y)))

        new_image = np.zeros([h, w, 3])
        new_image[:cuty, :cutx, :] = image_datas[0][:cuty, :cutx, :]
        new_image[cuty:, :cutx, :] = image_datas[1][cuty:, :cutx, :]
        new_image[cuty:, cutx:, :] = image_datas[2][cuty:, cutx:, :]
        new_image[:cuty, cutx:, :] = image_datas[3][:cuty, cutx:, :]

        # 对框进行进一步的处理
        new_boxes = np.array(merge_bboxes(box_datas, cutx, cuty))

        if len(new_boxes) == 0:
            return new_image, []
        if (new_boxes[:, :4] > 0).any():
            return new_image, new_boxes
        else:
            return new_image, []

    def rand(self, a=0, b=1):
        return np.random.rand() * (b - a) + a

    # 获取样本数据原始影像的波段数，主要用于初始化网络结构
    def get_dataset_img_bandcount(self):
        first_image_file = self.image_file_list[0].strip('\n')
        image_body = self.data_interface.get_data_content(first_image_file)
        pil_image = Image.open(io.BytesIO(image_body))
        img = np.asarray(pil_image)
        band_count = 1
        if int(len(img.shape)) == 3:
            band_count = int(img.shape[2])
        return band_count

    def save_pre_anchors(self,path):
        return GetAnchors(self.image_size, self.label_file_list_org,path)



class load_dataset:
    def __init__(self,dataset_id,network_type, root_path,
                 batch_size, node_num, invert_palette=None,
                 train_value_palette=None,
                 class_name_list=None,
                 trans_pipelines=None,
                 mosaic=False,
                 image_size=None):
        self.dataroot = os.path.join(root_path, "data", "tempdataset")
        # if os.path.exists(self.dataroot):
        #     shutil.rmtree(self.dataroot)

        # 单机训练或分布式训练的rank0进程创建数据目录
        if dist_utils.CURRENT_RANK == 0:
            self.create_data_dir(network_type, 'train')
            self.create_data_dir(network_type, 'valid')

        s3Client = aiUtils.s3GetImg(dataset_id)
        print("start to pull image in root path")
        s3Client.pullImage(self.dataroot)
        print("sucess!")
        # 启动监视器，当进程结束，删除缓存数据集。
        # self.monitor()
        self.train_torchdataset=torch_dataset(data_path=self.dataroot, ehance=trans_pipelines,
                            type='train/',
                            network_type=network_type,
                            palette=invert_palette,
                            train_value_palette=train_value_palette,
                            class_name_list=class_name_list,
                            mosaic=mosaic,
                            image_size=image_size)
        self.valid_torchdataset=torch_dataset(data_path=self.dataroot, ehance=trans_pipelines,
                            type='valid/',
                            network_type=network_type,
                            palette=invert_palette,
                            train_value_palette=train_value_palette,
                            class_name_list=class_name_list,
                            mosaic=mosaic,
                            image_size=image_size)
        train_sampler = None
        val_sampler = None
        if dist_utils.should_distribute(node_num):
            train_sampler = torch.utils.data.distributed.DistributedSampler(self.train_torchdataset)
            val_sampler = torch.utils.data.distributed.DistributedSampler(self.valid_torchdataset)
        if network_type==2:
            self.train_loader = DataLoader(self.train_torchdataset, batch_size=batch_size,
                                           num_workers=0, pin_memory=True,
                                           shuffle=(train_sampler is None), sampler=train_sampler,
                                           drop_last=True, collate_fn=self.yolo_dataset_collate)
            self.valid_loader = DataLoader(self.valid_torchdataset, batch_size=batch_size,
                                           num_workers=0, pin_memory=True,
                                           shuffle=(val_sampler is None), sampler=val_sampler,
                                           drop_last=True, collate_fn=self.yolo_dataset_collate)
        else:
            self.train_loader = DataLoader(self.train_torchdataset, batch_size=batch_size,
                                           shuffle=True, num_workers=0)
            self.valid_loader = DataLoader(self.valid_torchdataset, batch_size=1,
                                           shuffle=True, num_workers=0)

    def __len__(self):
        return len(self.train_torchdataset)+len(self.valid_torchdataset)
    def list(self):
        return self.train_torchdataset.image_file_list_org,self.train_torchdataset.label_file_list_org,self.valid_torchdataset.image_file_list_org,self.valid_torchdataset.label_file_list_org
    def img_band(self):
        bands = 3
        if len(self.train_torchdataset[1]) == 2:
            img,_=self.train_torchdataset[1]
            bands = img.shape[0]
        elif len(self.train_torchdataset[1]) == 3:
            img,_,_=self.train_torchdataset[1]
            bands = img.shape[0]
        return bands
    def read_one(self,path):
        try:
            if 's3' in path:
                if 'train' in path:
                    a = self.train_torchdataset[self.train_torchdataset.image_file_list_org.index(path)]
                if "valid" in path:
                    a = self.valid_torchdataset[self.valid_torchdataset.image_file_list_org.index(path)]
            else:
                if 'train' in path:
                    a = self.train_torchdataset[self.train_torchdataset.image_file_list.index(path)]
                if "valid" in path:
                    a = self.valid_torchdataset[self.valid_torchdataset.image_file_list.index(path)]
        except:
            print('获取列表失败！')
            a = []
        return a
    def del_temp(self):
        shutil.rmtree(self.dataroot)

    def yolo_dataset_collate(self,batch):
        images = []
        bboxes = []
        for img, box in batch:
            images.append(img)
            bboxes.append(box)
        images = np.array(images)
        bboxes = np.array(bboxes, dtype=object)
        return images, bboxes

    def monitor(self):
        pid = os.getpid()
        a = shlex.split('python pie/dataset/monitor.py ' + str(pid))
        subprocess.Popen(a)
        # time.sleep(20)
    def save_pre_anchors(self,path='./'):
        return self.train_torchdataset.save_pre_anchors(path).reshape([-1, 3, 2])[::-1, :, :]

    def create_data_dir(self, network_type, dir_type):
        """
        创建临时下载s3数据的目录
        :param network_type: 网络结构类型
        :param dir_type: 目录类型： train or valid
        :return:
        """
        temppicDir = os.path.join(self.dataroot, dir_type)
        dir_path = os.path.join(temppicDir, 'A')
        if network_type == 3:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            dir_path = os.path.join(temppicDir, 'B')
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
        else:
            dir_path = os.path.join(temppicDir, 'images')
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
        dir_path = os.path.join(temppicDir, 'labels')
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)


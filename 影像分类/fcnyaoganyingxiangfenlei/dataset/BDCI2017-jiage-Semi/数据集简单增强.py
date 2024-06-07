'''
    @author: yuchende
    @built date: 2020-6-10
    @function:
        将具有5张图片对应5张label的数据集，通过裁剪，旋转这2种方式，增强到5688张图片 和 5688张标签

    @Args:
        参数需要
            input_size  裁剪后每张图片的大小
            img_root_path, label_root_path 原始图像以及标签的路径
            labels_save_root_path, imgs_save_root_path 剪切后图像以及标签保存的路径

'''
import os
import cv2 as cv
import imutils as Image
import numpy as np

label_root_path = r'./training/labels'
img_root_path = r'./training/src'

labels_save_root_path = r'./training/train_labels'
imgs_save_root_path = r'./training/train'

input_size = (352, 352)  # h,w



class DataIncrease:

    def __init__(self, label_path, labels_path, img_path, imgs_path):
        self.labels_list = [os.path.join(label_path, item) for item in os.listdir(label_path)]
        self.imgs_list = [os.path.join(img_path, item) for item in os.listdir(img_path)]
        self.labels_path = labels_path
        self.imgs_path = imgs_path

        self.labels_list.sort()
        self.imgs_list.sort()

    def Rotation(self, img, label, rotat):
        ''' Rotate '''
        ''' img,label 均为 cv读出的对象 '''
        return Image.rotate(img, rotat), Image.rotate(label, rotat)

    def cutImage(self, originPicImage, originPicLabel, x0, y0, x1, y1):
        ''' originPic 是cv读出的图片, (x0,y0) 左上角坐标，另一个是右下角坐标 '''
        return originPicImage[y0:y1, x0:x1], originPicLabel[y0:y1, x0:x1]

    def saveImgAndLabel(self, img, img_name, label, label_name):
        ''' save path = self.labels_path and  self.imgs_path '''
        cv.imwrite(os.path.join(self.imgs_path, img_name), img)
        cv.imwrite(os.path.join(self.labels_path, label_name), label)


di = DataIncrease(label_root_path, labels_save_root_path, img_root_path, imgs_save_root_path)

totle = 0
imgn = len(di.imgs_list)
for item in range(0, imgn):
    train_img = cv.imread(di.imgs_list[item])
    train_label = cv.imread(di.labels_list[item])
    h, w, _ = train_img.shape
    ch, cw = input_size[0], input_size[1]
    hn, wn = h // ch, w // cw
    count = 0
    print('*' * 30)
    for i in range(0, hn):
        for j in range(0, wn):
            cutImage, cutLabel = di.cutImage(train_img, train_label, j * cw, i * ch, j * cw + cw, i * ch + ch)
            for k in range(0, 4):
                name = str(+i * wn * 4 + j * 4 + k) + '_' + str(item) + '.png'
                print(name)
                roateImage, roateLabels = di.Rotation(cutImage, cutLabel, k * 90)
                di.saveImgAndLabel(roateImage, name, roateLabels, name)
                count += 1
                totle += 1
    print('h : ', h, ' w : ', w, ' hn = ', hn, ' wn = ', wn, ' count = ', count)

print('totle = ', totle)
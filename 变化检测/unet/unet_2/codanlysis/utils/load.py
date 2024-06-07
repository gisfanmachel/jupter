#
# load.py : utils on generators / lists of ids to transform from strings to
#           cropped images and masks

import os

import numpy as np
from PIL import Image

from .utils import resize_and_crop, get_square, normalize, hwc_to_chw


def get_ids(dir):
    """返回目录中的id列表"""
    return (f[:-4] for f in os.listdir(dir))  # 图片名字的后4位为数字，能作为图片id


def split_ids(ids, n=2):
    """将每个id拆分为n个，为每个id创建n个元组(id, k)"""
    # 等价于for id in ids:
    #       for i in range(n):
    #           (id, i)
    # 得到元祖列表[(id1,0),(id1,1),(id2,0),(id2,1),...,(idn,0),(idn,1)]
    # 这样的作用是后面会通过后面的0,1作为utils.py中get_square函数的pos参数，pos=0的取左边的部分，pos=1的取右边的部分
    return ((id, i) for id in ids for i in range(n))


def to_cropped_imgs(ids, dir, suffix, scale):
    """从元组列表中返回经过剪裁的正确img"""
    for id, pos in ids:
        im = resize_and_crop(Image.open(dir + id + suffix), scale=scale)  # 重新设置图片大小为原来的scale倍
        yield get_square(im, pos)  # 然后根据pos选择图片的左边或右边


def get_imgs_and_masks(ids, dir_img, dir_mask, scale):
    """返回所有组(img, mask)"""

    imgs = to_cropped_imgs(ids, dir_img, '.jpg', scale)

    # need to transform from HWC to CHW
    imgs_switched = map(hwc_to_chw, imgs)  # 对图像进行转置，将(H, W, C)变为(C, H, W)
    imgs_normalized = map(normalize, imgs_switched)  # 对像素值进行归一化，由[0,255]变为[0,1]

    masks = to_cropped_imgs(ids, dir_mask, '_mask.gif', scale)  # 对图像的结果也进行相同的处理

    return zip(imgs_normalized, masks)  # 并将两个结果打包在一起


def get_full_img_and_mask(id, dir_img, dir_mask):
    im = Image.open(dir_img + id + '.jpg')
    mask = Image.open(dir_mask + id + '_mask.gif')
    return np.array(im), np.array(mask)

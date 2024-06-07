#
# load.py : utils on generators / lists of ids to transform from strings to
#           cropped images and masks

import os

import numpy as np
from PIL import Image

from .utils import resize_and_crop, get_square, normalize, hwc_to_chw


def get_ids(dir):
    """����Ŀ¼�е�id�б�"""
    return (f[:-4] for f in os.listdir(dir))  # ͼƬ���ֵĺ�4λΪ���֣�����ΪͼƬid


def split_ids(ids, n=2):
    """��ÿ��id���Ϊn����Ϊÿ��id����n��Ԫ��(id, k)"""
    # �ȼ���for id in ids:
    #       for i in range(n):
    #           (id, i)
    # �õ�Ԫ���б�[(id1,0),(id1,1),(id2,0),(id2,1),...,(idn,0),(idn,1)]
    # �����������Ǻ����ͨ�������0,1��Ϊutils.py��get_square������pos������pos=0��ȡ��ߵĲ��֣�pos=1��ȡ�ұߵĲ���
    return ((id, i) for id in ids for i in range(n))


def to_cropped_imgs(ids, dir, suffix, scale):
    """��Ԫ���б��з��ؾ������õ���ȷimg"""
    for id, pos in ids:
        im = resize_and_crop(Image.open(dir + id + suffix), scale=scale)  # ��������ͼƬ��СΪԭ����scale��
        yield get_square(im, pos)  # Ȼ�����posѡ��ͼƬ����߻��ұ�


def get_imgs_and_masks(ids, dir_img, dir_mask, scale):
    """����������(img, mask)"""

    imgs = to_cropped_imgs(ids, dir_img, '.jpg', scale)

    # need to transform from HWC to CHW
    imgs_switched = map(hwc_to_chw, imgs)  # ��ͼ�����ת�ã���(H, W, C)��Ϊ(C, H, W)
    imgs_normalized = map(normalize, imgs_switched)  # ������ֵ���й�һ������[0,255]��Ϊ[0,1]

    masks = to_cropped_imgs(ids, dir_mask, '_mask.gif', scale)  # ��ͼ��Ľ��Ҳ������ͬ�Ĵ���

    return zip(imgs_normalized, masks)  # ����������������һ��


def get_full_img_and_mask(id, dir_img, dir_mask):
    im = Image.open(dir_img + id + '.jpg')
    mask = Image.open(dir_mask + id + '_mask.gif')
    return np.array(im), np.array(mask)

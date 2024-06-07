import random
import numpy as np


# ��ͼ��ֳ���������
def get_square(img, pos):
    """Extract a left or a right square from ndarray shape : (H, W, C))"""
    h = img.shape[0]
    if pos == 0:
        return img[:, :h]
    else:
        return img[:, -h:]


def split_img_into_squares(img):
    return get_square(img, 0), get_square(img, 1)


# ��ͼ�����ת�ã���(H, W, C)��Ϊ(C, H, W)
def hwc_to_chw(img):
    return np.transpose(img, axes=[2, 0, 1])


def resize_and_crop(pilimg, scale=0.5, final_height=None):
    w = pilimg.size[0]  # �õ�ͼƬ�Ŀ�
    h = pilimg.size[1]  # �õ�ͼƬ�ĸ�
    # Ĭ��scaleΪ0.5,�����ߺͿ���Сһ��
    newW = int(w * scale)
    newH = int(h * scale)

    # ���û��ָ��ϣ���õ������ո߶�
    if not final_height:
        diff = 0
    else:
        diff = newH - final_height
    # �����趨ͼƬ�Ĵ�С
    img = pilimg.resize((newW, newH))
    # crop((left,upper,right,lower))����,��ͼ������ȡ��ĳ�����δ�С��ͼ��������һ����Ԫ�ص�Ԫ����Ϊ��������Ԫ��Ϊ��left, upper, right, lower��������ϵͳ��ԭ�㣨0, 0�������Ͻ�
    # ���û������final_height����ʵ����ȡ����ͼƬ
    # ���������final_height������ȡһ�������е�diff // 2�����߶�Ϊfinal_height��ͼƬ
    img = img.crop((0, diff // 2, newW, newH - diff // 2))
    return np.array(img, dtype=np.float32)


def batch(iterable, batch_size):
    """���������б�"""
    b = []
    for i, t in enumerate(iterable):
        b.append(t)
        if (i + 1) % batch_size == 0:
            yield b
            b = []

    if len(b) > 0:
        yield b


# Ȼ�����ݷ�Ϊѵ��������֤������
def split_train_val(dataset, val_percent=0.05):
    dataset = list(dataset)
    length = len(dataset)  # �õ����ݼ���С
    n = int(length * val_percent)  # ��֤��������
    random.shuffle(dataset)  # �����ݴ���
    return {'train': dataset[:-n], 'val': dataset[-n:]}


# ������ֵ���й�һ������[0,255]��Ϊ[0,1]
def normalize(x):
    return x / 255


# ������ͼƬ�ϲ�����
def merge_masks(img1, img2, full_w):
    h = img1.shape[0]

    new = np.zeros((h, full_w), np.float32)
    new[:, :full_w // 2 + 1] = img1[:, :full_w // 2 + 1]
    new[:, full_w // 2 + 1:] = img2[:, -(full_w // 2 - 1):]

    return new


# credits to https://stackoverflow.com/users/6076729/manuel-lagunas
def rle_encode(mask_image):
    pixels = mask_image.flatten()
    # We avoid issues with '1' at the start or end (at the corners of
    # the original image) by setting those pixels to '0' explicitly.
    # We do not expect these to be non-zero for an accurate mask,
    # so this should not harm the score.
    pixels[0] = 0
    pixels[-1] = 0
    runs = np.where(pixels[1:] != pixels[:-1])[0] + 2
    runs[1::2] = runs[1::2] - runs[:-1:2]
    return runs

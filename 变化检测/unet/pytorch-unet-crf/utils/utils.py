import random
import numpy as np


# 将图像分成左右两块
def get_square(img, pos):
    """Extract a left or a right square from ndarray shape : (H, W, C))"""
    h = img.shape[0]
    if pos == 0:
        return img[:, :h]
    else:
        return img[:, -h:]


def split_img_into_squares(img):
    return get_square(img, 0), get_square(img, 1)


# 对图像进行转置，将(H, W, C)变为(C, H, W)
def hwc_to_chw(img):
    return np.transpose(img, axes=[2, 0, 1])


def resize_and_crop(pilimg, scale=0.5, final_height=None):
    w = pilimg.size[0]  # 得到图片的宽
    h = pilimg.size[1]  # 得到图片的高
    # 默认scale为0.5,即将高和宽都缩小一半
    newW = int(w * scale)
    newH = int(h * scale)

    # 如果没有指明希望得到的最终高度
    if not final_height:
        diff = 0
    else:
        diff = newH - final_height
    # 重新设定图片的大小
    img = pilimg.resize((newW, newH))
    # crop((left,upper,right,lower))函数,从图像中提取出某个矩形大小的图像。它接收一个四元素的元组作为参数，各元素为（left, upper, right, lower），坐标系统的原点（0, 0）是左上角
    # 如果没有设置final_height，其实就是取整个图片
    # 如果设置了final_height，就是取一个上下切掉diff // 2，最后高度为final_height的图片
    img = img.crop((0, diff // 2, newW, newH - diff // 2))
    return np.array(img, dtype=np.float32)


def batch(iterable, batch_size):
    """批量处理列表"""
    b = []
    for i, t in enumerate(iterable):
        b.append(t)
        if (i + 1) % batch_size == 0:
            yield b
            b = []

    if len(b) > 0:
        yield b


# 然后将数据分为训练集和验证集两份
def split_train_val(dataset, val_percent=0.05):
    dataset = list(dataset)
    length = len(dataset)  # 得到数据集大小
    n = int(length * val_percent)  # 验证集的数量
    random.shuffle(dataset)  # 将数据打乱
    return {'train': dataset[:-n], 'val': dataset[-n:]}


# 对像素值进行归一化，由[0,255]变为[0,1]
def normalize(x):
    return x / 255


# 将两个图片合并起来
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

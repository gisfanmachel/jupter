

import cv2
from os import path


# --------------用于读取原始数据，填充、分割成256*256---------------

# 影像裁剪到256*256

def crop_image(img):
    # m是图像height，行数，y方向
    # n是图像width，列数，X方向
    m, n = img.shape[0], img.shape[1]

    # a1 是 裁剪的行数（边缘不够尺寸的也要裁剪算行数），Y方向
    a1 = (m // 256) + 1
    # a1 是 裁剪的列数（边缘不够尺寸的也要裁剪算列数），X方向
    b1 = (n // 256) + 1

    # a 是 Y 方向不够的像素
    a = a1 * 256 - m
    # b 是 X 方向不够的像素
    b = b1 * 256 - n

    # 将原影像填充,满足（256，256）的倍数，填充部分为黑色
    # 原来的Y 为13659 ，现在变成了13824，增加了a=165
    # 原来的X 为15632，现在变成了15772，增加了b=240
    img_padding = cv2.copyMakeBorder(img, 0, a, 0, b, cv2.BORDER_CONSTANT, value=(0, 0, 0))

    img_crops = []
    # Y方向
    for i in range(a1):
        # X 方向
        for j in range(b1):
            img_c = img_padding[i * 256:(i + 1) * 256, j * 256:(j + 1) * 256]
            img_crops.append(img_c)
    return img_crops


# 读取影像名对应图像
def segmentation(img_before_dir, img_after_dir, logger):
    img_before = cv2.imread(img_before_dir, 1)
    img_after = cv2.imread(img_after_dir, 1)

    img_before_seg = crop_image(img_before)
    img_after_seg = crop_image(img_after)

    img_before_save_dir = './Data/test/A'
    img_after_save_dir = './Data/test/B'

    for j in range(len(img_before_seg)):
        cv2.imwrite(path.join(img_before_save_dir, 'Test_' + str(j) + '.png'), img_before_seg[j])
    for q in range(len(img_after_seg)):
        cv2.imwrite(path.join(img_after_save_dir, 'Test_' + str(q) + '.png'), img_after_seg[q])

    logger.info("裁剪256*256已保存")

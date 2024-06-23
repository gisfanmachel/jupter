import skimage.io
import io
from PIL import Image
import cv2
import numpy as np
# from osgeo import gdal
from pie.utils.registry import Registry




# 使用opencv的函数对图像进行增强，对比度变换，图像的HSV颜色空间，改变H,S和V亮度分量，增加光照变化
@Registry.divfun
def randomHueSaturationValue(image, image2,mask,i):
    u = i.get('random')
    hue_shift_limit = (-180, 180)
    sat_shift_limit = (-255, 255)
    val_shift_limit = (-255, 255)
    if np.random.random() < u:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(image)
        hue_shift = np.random.randint(hue_shift_limit[0], hue_shift_limit[1] + 1)
        hue_shift = np.uint8(hue_shift)
        h += hue_shift
        sat_shift = np.random.uniform(sat_shift_limit[0], sat_shift_limit[1])
        s = cv2.add(s, sat_shift)
        val_shift = np.random.uniform(val_shift_limit[0], val_shift_limit[1])
        v = cv2.add(v, val_shift)
        image = cv2.merge((h, s, v))
        image = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
        if image2 is not None:
            image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(image2)
            h += hue_shift
            s = cv2.add(s, sat_shift)
            v = cv2.add(v, val_shift)
            image2 = cv2.merge((h, s, v))
            image2 = cv2.cvtColor(image2, cv2.COLOR_HSV2BGR)
    return image, image2,mask


# 随机应用仿射变换：平移，缩放和旋转输入。
@Registry.divfun
def randomShiftScaleRotate(image, image2, mask, i):
    u = i.get('random')
    shift_limit = (-0.0, 0.0)
    scale_limit = (-0.0, 0.0)
    rotate_limit = (-0.0, 0.0)
    aspect_limit = (-0.0, 0.0)
    borderMode = cv2.BORDER_CONSTANT
    if np.random.random() < u:
        height, width, channel = image.shape
        angle = np.random.uniform(rotate_limit[0], rotate_limit[1])
        scale = np.random.uniform(1 + scale_limit[0], 1 + scale_limit[1])
        aspect = np.random.uniform(1 + aspect_limit[0], 1 + aspect_limit[1])
        sx = scale * aspect / (aspect ** 0.5)
        sy = scale / (aspect ** 0.5)
        dx = round(np.random.uniform(shift_limit[0], shift_limit[1]) * width)
        dy = round(np.random.uniform(shift_limit[0], shift_limit[1]) * height)

        cc = np.math.cos(angle / 180 * np.math.pi) * sx
        ss = np.math.sin(angle / 180 * np.math.pi) * sy
        rotate_matrix = np.array([[cc, -ss], [ss, cc]])

        box0 = np.array([[0, 0], [width, 0], [width, height], [0, height], ])
        box1 = box0 - np.array([width / 2, height / 2])
        box1 = np.dot(box1, rotate_matrix.T) + np.array([width / 2 + dx, height / 2 + dy])

        box0 = box0.astype(np.float32)
        box1 = box1.astype(np.float32)
        mat = cv2.getPerspectiveTransform(box0, box1)
        image = cv2.warpPerspective(image, mat, (width, height),
                                    flags=cv2.INTER_LINEAR, borderMode=borderMode,
                                    borderValue=(
                                        0, 0, 0,))
        mask = cv2.warpPerspective(mask, mat, (width, height),
                                   flags=cv2.INTER_LINEAR, borderMode=borderMode,
                                   borderValue=(
                                       0, 0, 0,))

        if image2 is not None:
            image2 = cv2.warpPerspective(image2, mat, (width, height),
                                         flags=cv2.INTER_LINEAR, borderMode=borderMode,
                                         borderValue=(
                                             0, 0, 0,))

    return image, image2, mask

@Registry.divfun
def randomHorizontalFlip(image, image2, mask, i):
    u = i.get('random')
    if np.random.random() < u:
        image = cv2.flip(image, 1)
        mask = cv2.flip(mask, 1)

        if image2 is not None:
            image2 = cv2.flip(image2, 1)

    return image, image2, mask

@Registry.divfun
def randomVerticleFlip(image, image2, mask, i):
    u = i.get('random')
    if np.random.random() < u:
        image = cv2.flip(image, 0)
        mask = cv2.flip(mask, 0)

        if image2 is not None:
            image2 = cv2.flip(image2, 0)

    return image, image2, mask

@Registry.divfun
def randomRotate90(image, image2, mask, i):
    u=i.get('random')
    if np.random.random() < u:
        image = np.rot90(image)
        mask = np.rot90(mask)
        if image2 is not None:
            image2 = np.rot90(image2)
    return image, image2, mask


@Registry.divfun
def Normalization(image, image2, mask, i):
    region = i.get('region')
    stretching=Registry['stretching']
    image=stretching(image,region)
    if image2 is not None:
        image2 = stretching(image2, region)
    return image, image2, mask

@Registry.divfun
def stretching(img,region):
    img = np.array(img, np.float32)
    max=np.percentile(img, 99.999)
    min=np.percentile(img, 0.001)
    img = ((img - min) / (max - min)) * (np.max(region) - np.min(region))
    img[img > np.max(region)] = np.max(region)
    img[img < np.min(region)] = np.min(region)
    return img
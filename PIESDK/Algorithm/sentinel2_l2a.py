# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   sentinel2_l2a.py
@Time    :   2020/8/6 下午5:19
@Author  :   liuxiaodong
@Version :   1.0
@Contact :   2152550864@qq.com
@License :   (C)Copyright 2019-2020, liuxiaodong
@Desc    :   哨兵2处理算法
"""
from pie.number import PIENumber
from pie.object import PIEObject
from pie.reducer import PIEReducer
from pie.utils.error import ArgsIsNull

class PIESentinel2_L2A(PIEObject):
    def __init__(self):
        super(PIESentinel2_L2A, self).__init__()
        self.pre = None
        self.statement = None

    @staticmethod
    def name():
        return "PIESentinel2_L2A"

    @classmethod
    def cloudMask(cls, image):
        """
        哨兵2去云
        :param image:
        :return:
        """
        if image is None:
            raise ArgsIsNull("image")

        qaBand = image.select("QA60")
        cloudBitMask = 1 << 10
        cirrusBitMask = 1 << 11
        mask = qaBand.bitwiseAnd(cloudBitMask).Or(qaBand.bitwiseAnd(cirrusBitMask))
        return mask

    @classmethod
    def NDVI(cls, input):
        """
        计算NDVI植被指数
        :param input:
        :return:
        """
        if input is None:
            raise ArgsIsNull("input")
        imageRed = input.select("B4")
        imageNir = input.select("B8")

        if imageRed is None or imageNir is None:
            return None
        imageNDVI = imageNir.subtract(imageRed).divide(imageNir.add(imageRed))
        return imageNDVI.rename("NDVI")

    @classmethod
    def NDWI(cls, input):
        """
        计算NDWI水体指数
        :param input:
        :return:
        """
        if input is None:
            raise ArgsIsNull("input")
        imageGreen = input.select("B3")
        imageNir = input.select("B8")

        if imageGreen is None or imageNir is None:
            return None
        imageNDWI = imageGreen.subtract(imageNir).divide(imageGreen.add(imageNir))
        return imageNDWI.rename("NDWI")

    @classmethod
    def MNDWI(cls, input):
        """
        计算MNDWI增强型水体指数
        :param input:
        :return:
        """
        if input is None:
            raise ArgsIsNull("input")
        imageGreen = input.select("B3")
        imageMir = input.select("B11")

        if imageGreen is None or imageMir is None:
            return None
        imageMNDWI = imageGreen.subtract(imageMir).divide(imageGreen.add(imageMir))
        return imageMNDWI.rename("MNDWI")

    @classmethod
    def NDBI(cls, input):
        """
        计算NDBI建筑指数
        :param input:
        :return:
        """
        if input is None:
            raise ArgsIsNull("input")
        imageMIR = input.select("B11")
        imageNir = input.select("B8")

        if imageMIR is None or imageNir is None:
            return None
        imageNDBI = imageMIR.subtract(imageNir).divide(imageMIR.add(imageNir))
        return imageNDBI.rename("NDBI")

    @classmethod
    def EVI(cls, input):
        """
        计算EVI增强型植被指数
        :param input:
        :return:
        """
        if input is None:
            raise ArgsIsNull("input")
        imageRed = input.select("B4")
        imageNir = input.select("B8")
        imageBlue = input.select("B2")

        if imageRed is None or imageNir is None or imageBlue is None:
            return None

        imageEVI = imageNir.subtract(imageRed).divide(
            imageNir.add(imageRed.multiply(6)).add(imageBlue.multiply(7.5)).add(10000))
        imageEVI = imageEVI.multiply(2.5)
        return imageEVI.rename("EVI")

    @classmethod
    def FVC(cls, input, scale):
        red = input.select("B4")
        nir = input.select("B5")
        if red is None or nir is None:
            return None
        region = input.geometry()
        if not scale:
            scale = 30

        ndvi = (nir.subtract(red)).divide(nir.add(red)).rename("ndvi")
        reducer = PIEReducer()
        obj = ndvi.reduceRegion(reducer.minMax(), region, scale)
        max = obj.get("ndvi_max")
        min = obj.get("ndvi_min")
        max = PIENumber(max)
        min = PIENumber(min)
        fvc = (ndvi.subtract(min)).divide(max.subtract(min))
        return fvc.rename('FVC')

    @classmethod
    def LSWI(cls, input):
        swir = input.select("B11")
        nir = input.select("B8")
        if swir is None or nir is None:
            return None

        imageLswi = (nir.subtract(swir)).divide(nir.add(swir))
        return imageLswi.rename("LSWI")

    @classmethod
    def RVI(cls, input):
        red = input.select("B4")
        nir = input.select("B8")
        if red is None or nir is None:
            return None

        imageRvi = nir.divide(red)
        return imageRvi.rename("RVI")

    @classmethod
    def BSI(cls, input):
        blue = input.select("B2")
        red = input.select("B4")
        nir = input.select("B8")
        swir = input.select("B11")
        if blue is None or red is None or swir is None or nir is None:
            return None

        imageBsi = ((swir.add(red)).subtract(nir.add(blue))).divide((swir.add(red)).add(nir.add(blue)))
        return imageBsi.rename("BSI")

    @classmethod
    def NBR(cls, input):
        nir = input.select("B12")
        swir = input.select("B8")
        if swir is None or nir is None:
            return None

        nbr = (nir.subtract(swir)).divide(nir.add(swir))
        return nbr.rename("BSI")

    @classmethod
    def SAVI(cls, input):
        nir = input.select("B8")
        red = input.select("B4")
        if red is None or nir is None:
            return None
        savi = ((nir.subtract(red)).multiply(1.5)).divide(nir.add(red).add(5000))
        return savi.rename("SAVI")

    @classmethod
    def NDSI(cls, input):
        green = input.select("B3")
        swir = input.select("B11")
        if swir is None or green is None:
            return None

        ndsi = (green.subtract(swir)).divide(green.add(swir))
        return ndsi.rename("NDSI")


Sentinel2_L2A = PIESentinel2_L2A()
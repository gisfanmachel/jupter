# -*- coding:utf-8 -*-

from pie.object import PIEObject
from pie.utils.error import ArgsIsNull
from pie.number import PIENumber
from pie.reducer import PIEReducer

class PIELandsat9C2_SR(PIEObject):
    def __init__(self):
        super(PIELandsat9C2_SR, self).__init__()
        self.pre = None
        self.statement = None

    @staticmethod
    def name():
        return "PIELandsat9C2_SR"

    @classmethod
    def cloudMask(cls, input):
        """
        云掩膜
        :param input:
        :return:
        """
        if input is None:
            raise ArgsIsNull("input")

        # 选择QA波段
        image_QA_PIXEL = input.select("QA_PIXEL")
        # 云比特位
        cloudsBitMask = 1 << 3
        # 云阴影
        cloudShadowBitMask = 1 << 4
        # 云掩膜 云1，其他0
        mask1 = image_QA_PIXEL.bitwiseAnd(cloudsBitMask)
        # 云阴影 云1，其他0
        mask2 = image_QA_PIXEL.bitwiseAnd(cloudShadowBitMask)
        # 与运算
        mask = mask1.Or(mask2)
        return mask.rename("cloud")

    @classmethod
    def NDVI(cls, input):
        """
        计算NDVI植被指数
        :param input:
        :return:
        """
        if input is None:
            raise ArgsIsNull("input")
        imageRed = input.select("B4").multiply(0.0000275).add(-0.2)
        imageNir = input.select("B5").multiply(0.0000275).add(-0.2)

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
        imageGreen = input.select("B3").multiply(0.0000275).add(-0.2)
        imageNir = input.select("B5").multiply(0.0000275).add(-0.2)

        if imageGreen is None or imageNir is None:
            return None
        imageNDWI = imageGreen.subtract(imageNir).divide(imageGreen.add(imageNir))
        return imageNDWI.rename("NDWI")

    @classmethod
    def MNDWI(cls, input):
        """
        计算MNDWI增强型植被指数
        :param input:
        :return:
        """
        if input is None:
            raise ArgsIsNull("input")
        imageGreen = input.select("B3").multiply(0.0000275).add(-0.2)
        imageMir = input.select("B6").multiply(0.0000275).add(-0.2)

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
        imageMIR = input.select("B6").multiply(0.0000275).add(-0.2)
        imageNir = input.select("B5").multiply(0.0000275).add(-0.2)

        if imageMIR is None or imageNir is None:
            return None
        imageNDBI = imageMIR.subtract(imageNir).divide(imageMIR.add(imageNir))
        return imageNDBI.rename("NDBI")

    @classmethod
    def EVI(cls, input):
        """
        计算EVI增强植被指数
        :param input:
        :return:
        """
        if input is None:
            raise ArgsIsNull("input")
        imageRed = input.select("B4").multiply(0.0000275).add(-0.2)
        imageNir = input.select("B5").multiply(0.0000275).add(-0.2)
        imageBlue = input.select("B2").multiply(0.0000275).add(-0.2)

        if imageRed is None or imageNir is None or imageBlue is None:
            return None

        imageEVI = imageNir.subtract(imageRed).divide(
            imageNir.add(imageRed.multiply(6)).add(imageBlue.multiply(7.5)).add(10000))
        imageEVI = imageEVI.multiply(2.5)
        return imageEVI.rename("EVI")

    @classmethod
    def FVC(cls, input, scale):
        imageRed = input.select("B4")
        imageNir = input.select("B5")
        if imageRed is None or imageNir is None:
            return None
        region = input.geometry()
        if not scale:
            scale = 30

        red = imageRed.multiply(0.0000275).add(-0.2)
        nir = imageNir.multiply(0.0000275).add(-0.2)
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
        imageSwir = input.select("B6")
        imageNir = input.select("B5")
        if imageSwir is None or imageNir is None:
            return None
        swir = imageSwir.multiply(0.0000275).add(-0.2)
        nir = imageNir.multiply(0.0000275).add(-0.2)
        imageLswi = (nir.subtract(swir)).divide(nir.add(swir))
        return imageLswi.rename("LSWI")

    @classmethod
    def RVI(cls, input):
        imageRed = input.select("B4")
        imageNir = input.select("B5")
        if imageRed is None or imageNir is None:
            return None
        red = imageRed.multiply(0.0000275).add(-0.2)
        nir = imageNir.multiply(0.0000275).add(-0.2)
        imageRvi = nir.divide(red)
        return imageRvi.rename("RVI")

    @classmethod
    def BSI(cls, input):
        imageBlue = input.select("B2")
        imageRed = input.select("B4")
        imageNir = input.select("B5")
        imageSwir = input.select("B6")
        if imageBlue is None or imageRed is None or imageNir is None or imageSwir is None:
            return None
        blue = imageBlue.multiply(0.0000275).add(-0.2)
        red = imageRed.multiply(0.0000275).add(-0.2)
        swir = imageSwir.multiply(0.0000275).add(-0.2)
        nir = imageNir.multiply(0.0000275).add(-0.2)
        imageBsi = ((swir.add(red)).subtract(nir.add(blue))).divide((swir.add(red)).add(nir.add(blue)))
        return imageBsi.rename("BSI")

    @classmethod
    def NBR(cls, input):
        imageNir = input.select("B5")
        imageSwir = input.select("B7")
        if imageSwir is None or imageNir is None:
            return None
        swir = imageSwir.multiply(0.0000275).add(-0.2)
        nir = imageNir.multiply(0.0000275).add(-0.2)
        nbr = (nir.subtract(swir)).divide(nir.add(swir))
        return nbr.rename("BSI")

    @classmethod
    def SAVI(cls, input):
        imageNir = input.select("B5")
        imageRed = input.select("B4")
        if imageRed is None or imageNir is None:
            return None
        red = imageRed.multiply(0.0000275).add(-0.2)
        nir = imageNir.multiply(0.0000275).add(-0.2)
        savi = ((nir.subtract(red)).multiply(1.5)).divide(nir.add(red).add(0.5))
        return savi.rename("SAVI")

    @classmethod
    def NDSI(cls, input):
        imageGreen = input.select("B3")
        imageSwir = input.select("B6")
        if imageSwir is None or imageGreen is None:
            return None
        swir = imageSwir.multiply(0.0000275).add(-0.2)
        green = imageGreen.multiply(0.0000275).add(-0.2)
        ndsi = (green.subtract(swir)).divide(green.add(swir))
        return ndsi.rename("NDSI")

Landsat9C2_SR = PIELandsat9C2_SR()

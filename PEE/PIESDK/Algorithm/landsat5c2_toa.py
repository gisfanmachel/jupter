# -*- coding:utf-8 -*-

from pie.array import PIEArray
from pie.number import PIENumber
from pie.object import PIEObject
from pie.reducer import PIEReducer
from pie.utils.error import ArgsIsNull

class PIELandsat5C2_TOA(PIEObject):
    def __init__(self):
        super(PIELandsat5C2_TOA, self).__init__()
        self.pre = None
        self.statement = None

    @staticmethod
    def name():
        return "PIELandsat5C2_TOA"

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
        imageRed = input.select("B3")
        imageNir = input.select("B4")

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
        imageGreen = input.select("B2")
        imageNir = input.select("B4")

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
        imageGreen = input.select("B2")
        imageMir = input.select("B5")

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
        imageMIR = input.select("B5")
        imageNir = input.select("B4")

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
        imageRed = input.select("B3")
        imageNir = input.select("B4")
        imageBlue = input.select("B1")

        if imageRed is None or imageNir is None or imageBlue is None:
            return None

        imageEVI = imageNir.subtract(imageRed).divide(
            imageNir.add(imageRed.multiply(6)).add(imageBlue.multiply(7.5)).add(10000))
        imageEVI = imageEVI.multiply(2.5)
        return imageEVI.rename("EVI")

    @classmethod
    def FVC(cls, input, scale):
        red = input.select("B3")
        nir = input.select("B4")
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
        swir = input.select("B5")
        nir = input.select("B4")
        if swir is None or nir is None:
            return None

        imageLswi = (nir.subtract(swir)).divide(nir.add(swir))
        return imageLswi.rename("LSWI")

    @classmethod
    def RVI(cls, input):
        red = input.select("B3")
        nir = input.select("B4")
        if red is None or nir is None:
            return None

        imageRvi = nir.divide(red)
        return imageRvi.rename("RVI")

    @classmethod
    def BSI(cls, input):
        blue = input.select("B1")
        red = input.select("B3")
        nir = input.select("B4")
        swir = input.select("B5")
        if blue is None or red is None or swir is None or nir is None:
            return None

        imageBsi = ((swir.add(red)).subtract(nir.add(blue))).divide((swir.add(red)).add(nir.add(blue)))
        return imageBsi.rename("BSI")

    @classmethod
    def NBR(cls, input):
        nir = input.select("B4")
        swir = input.select("B7")
        if swir is None or nir is None:
            return None

        nbr = (nir.subtract(swir)).divide(nir.add(swir))
        return nbr.rename("BSI")

    @classmethod
    def SAVI(cls, input):
        nir = input.select("B4")
        red = input.select("B3")
        if red is None or nir is None:
            return None
        savi = ((nir.subtract(red)).multiply(1.5)).divide(nir.add(red).add(5000))
        return savi.rename("SAVI")

    @classmethod
    def NDSI(cls, input):
        green = input.select("B2")
        swir = input.select("B5")
        if swir is None or green is None:
            return None

        ndsi = (green.subtract(swir)).divide(green.add(swir))
        return ndsi.rename("NDSI")

    @classmethod
    def KT(cls, input):
        """
        缨帽变换（K-T变换）的结果，计算公式为：U = Cx + r
        :param input:
        :return:
        """
        _image = input.select(["B1","B2","B3","B4","B5","B7"])
        _params = PIEArray([
            [ 0.2909, 0.2493, 0.4806, 0.5568, 0.4438, 0.1706,10.3695],
            [-0.2728,-0.2174,-0.5508, 0.7220, 0.0733,-0.1648,-0.7310],
            [ 0.1446, 0.1761, 0.3322, 0.3396,-0.6210, 0.4186,-3.3828],
            [ 0.8461,-0.0731,-0.4640,-0.0032,-0.0492, 0.0119, 0.7879],
            [ 0.0549,-0.0232, 0.0339,-0.1937, 0.4162,-0.7823,-2.4750],
            [ 0.1186,-0.8069, 0.4094, 0.0571,-0.0228, 0.0220,-0.0336]
        ])
        _bandNames = ["Brightness", "Greenness", "Wetness", "Fourth", "Fifth", "Sixth"]
        return _image.pca(_params).rename(_bandNames)

Landsat5C2_TOA = PIELandsat5C2_TOA()

# -*- coding:utf-8 -*-

from pie.array import PIEArray
from pie.number import PIENumber
from pie.object import PIEObject
from pie.reducer import PIEReducer
from pie.utils.error import ArgsIsNull

class PIELandsat7C2_TOA(PIEObject):
    def __init__(self):
        super(PIELandsat7C2_TOA, self).__init__()
        self.pre = None
        self.statement = None

    @staticmethod
    def name():
        return "PIELandsat7C2_TOA"

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
        image_BQA = input.select("BQA")
        # 云比特位
        cloudsBitMask = 1 << 4
        # 云置信度比特位
        cloudConfidenceBitMask = 1 << 6
        # 云掩膜 云1，其他0
        mask1 = image_BQA.bitwiseAnd(cloudsBitMask)
        # 云置信度掩膜 云1，其他0
        mask2 = image_BQA.bitwiseAnd(cloudConfidenceBitMask)
        # 与运算
        mask = mask1.Or(mask2)
        return mask.rename("cloud")

    @classmethod
    def NDVI(cls, input):
        if input is None:
            raise ArgsIsNull("input")
        imageRed = input.select("B3")
        imageNir = input.select("B4")

        if (imageRed is None) or (imageNir is None):
            return None
        imageNDVI = imageNir.subtract(imageRed).divide(imageNir.add(imageRed))
        return imageNDVI.rename("NDVI")

    @classmethod
    def NDWI(cls, input):
        if input is None:
            raise ArgsIsNull("input")
        imageGreen = input.select("B2")
        imageNir = input.select("B4")

        if (imageGreen is None) or (imageNir is None):
            return None
        imageNDWI = imageGreen.subtract(imageNir).divide(imageGreen.add(imageNir))
        return imageNDWI.rename("NDWI")

    @classmethod
    def MNDWI(cls, input):
        if input is None:
            raise ArgsIsNull("input")
        imageGreen = input.select("B2")
        imageMir = input.select("B5")

        if (imageGreen is None) or (imageMir is None):
            return None
        imageMNDWI = imageGreen.subtract(imageMir).divide(imageGreen.add(imageMir))
        return imageMNDWI.rename("MNDWI")

    @classmethod
    def NDBI(cls, input):
        if input is None:
            raise ArgsIsNull("input")
        imageMIR = input.select("B5")
        imageNir = input.select("B4")

        if (imageMIR is None) or (imageNir is None):
            return None
        imageNDBI = imageMIR.subtract(imageNir).divide(imageMIR.add(imageNir))
        return imageNDBI.rename("NDBI")

    @classmethod
    def EVI(cls, input):
        if input is None:
            raise ArgsIsNull("input")
        imageRed = input.select("B3")
        imageNir = input.select("B4")
        imageBlue = input.select("B1")

        if (imageRed is None) or (imageNir is None) or (imageBlue is None):
            return None

        imageEVI = imageNir.subtract(imageRed).divide(
            imageNir.add(imageRed.multiply(6)).add(imageBlue.multiply(7.5)).add(10000))
        imageEVI = imageEVI.multiply(2.5)
        return imageEVI.rename("EVI")

    @classmethod
    def KT(cls, input):
        """
        缨帽变换（K-T变换）的结果，计算公式为：U = Cx + r
        :param input:
        :return:
        """
        lc7Image = input.select(["B1", "B2", "B3", "B4", "B5", "B7"])
        lc7KTParams = PIEArray([
            [0.3561, 0.3972, 0.3904, 0.6966, 0.2286, 0.1596],
            [-0.3344, -0.3544, -0.4556, 0.6966, -0.0242, -0.2630],
            [0.2626, 0.2141, 0.0926, 0.0656, -0.7629, -0.5388],
            [0.0805, -0.0498, 0.1950, -0.1327, 0.5752, -0.7775],
            [-0.7252, -0.0202, 0.6683, 0.0631, -0.1494, -0.0274],
            [0.4000, -0.8172, 0.3832, 0.0602, -0.1095, 0.0985]
        ])
        return lc7Image.pca(lc7KTParams).rename(["Brightness", "Greenness", "Wetness", "Fourth", "Fifth", "Sixth"])

    @classmethod
    def FVC(cls, input, scale):
        """
        计算FVC
        :param input:
        :param scale:
        :return:
        """
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

Landsat7C2_TOA = PIELandsat7C2_TOA()

# -*- coding:utf-8 -*-

from pie.number import PIENumber
from pie.object import PIEObject
from pie.reducer import PIEReducer
from pie.utils.error import ArgsIsNull

class PIEPlugin_Modis_SR(PIEObject):
    def __init__(self):
        super(PIEPlugin_Modis_SR, self).__init__()
        self.pre = None
        self.statement = None

    @staticmethod
    def name():
        return "PIEPlugin_Modis_SR"

    @classmethod
    def NDVI(cls, input):
        if input is None:
            raise ArgsIsNull("input")

        imageRed = input.select("sur_refl_b01")
        imageNir = input.select("sur_refl_b02")
        if imageRed is None or imageNir is None:
            return None

        imageNDVI = imageNir.subtract(imageRed).divide(imageNir.add(imageRed))
        return imageNDVI.rename("NDVI")

    @classmethod
    def NDWI(cls, input):
        if input is None:
            raise ArgsIsNull("input")
        imageGreen = input.select("sur_refl_b04")
        imageNir = input.select("sur_refl_b02")
        if imageGreen is None or imageNir is None:
            return None
        imageNDWI = imageGreen.subtract(imageNir).divide(imageGreen.add(imageNir))
        return imageNDWI.rename("NDWI")

    @classmethod
    def MNDWI(cls, input):
        if input is None:
            raise ArgsIsNull("input")
        imageGreen = input.select("sur_refl_b04")
        imageMir = input.select("sur_refl_b06")
        if imageGreen is None or imageMir is None:
            return None
        imageMNDWI = imageGreen.subtract(imageMir).divide(imageGreen.add(imageMir))
        return imageMNDWI.rename("MNDWI")

    @classmethod
    def NDBI(cls, input):
        if input is None:
            raise ArgsIsNull("input")
        imageMIR = input.select("sur_refl_b06")
        imageNir = input.select("sur_refl_b06")

        if imageMIR is None or imageNir is None:
            return None
        imageNDBI = imageMIR.subtract(imageNir).divide(imageMIR.add(imageNir))
        return imageNDBI.rename("NDBI")

    @classmethod
    def EVI(cls, input):
        if input is None:
            raise ArgsIsNull("input")
        imageRed = input.select("sur_refl_b02")
        imageNir = input.select("sur_refl_b01")
        imageBlue = input.select("sur_refl_b03")

        if imageRed is None or imageNir is None or imageBlue is None:
            return None

        imageEVI = imageNir.subtract(imageRed).divide(
            imageNir.add(imageRed.multiply(6)).add(imageBlue.multiply(7.5)).add(10000))
        imageEVI = imageEVI.multiply(2.5)
        return imageEVI.rename("EVI")

    @classmethod
    def FVC(cls, input, scale):
        red = input.select("sur_refl_b01")
        nir = input.select("sur_refl_b02")
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
        swir = input.select("sur_refl_b06")
        nir = input.select("sur_refl_b02")
        if swir is None or nir is None:
            return None

        imageLswi = (nir.subtract(swir)).divide(nir.add(swir))
        return imageLswi.rename("LSWI")

    @classmethod
    def RVI(cls, input):
        red = input.select("sur_refl_b01")
        nir = input.select("sur_refl_b02")
        if red is None or nir is None:
            return None
        imageRvi = nir.divide(red)
        return imageRvi.rename("RVI")

    @classmethod
    def BSI(cls, input):
        blue = input.select("sur_refl_b03")
        red = input.select("sur_refl_b01")
        nir = input.select("sur_refl_b02")
        swir = input.select("sur_refl_b06")
        if blue is None or red is None or swir is None or nir is None:
            return None

        imageBsi = ((swir.add(red)).subtract(nir.add(blue))).divide((swir.add(red)).add(nir.add(blue)))
        return imageBsi.rename("BSI")

    @classmethod
    def NBR(cls, input):
        swir = input.select("sur_refl_b07")
        nir = input.select("sur_refl_b02")
        if swir is None or nir is None:
            return None
        nbr = (nir.subtract(swir)).divide(nir.add(swir))
        return nbr.rename("BSI")

    @classmethod
    def SAVI(cls, input):
        nir = input.select("sur_refl_b02")
        red = input.select("sur_refl_b01")
        if red is None or nir is None:
            return None

        savi = ((nir.subtract(red)).multiply(1.5)).divide(nir.add(red).add(5000))
        return savi.rename("SAVI")

    @classmethod
    def NDSI(cls, input):
        green = input.select("sur_refl_b04")
        swir = input.select("sur_refl_b06")
        if green is None or swir is None:
            return None

        ndsi = (green.subtract(swir)).divide(green.add(swir))
        return ndsi.rename("NDSI")

Modis_SR = PIEPlugin_Modis_SR()

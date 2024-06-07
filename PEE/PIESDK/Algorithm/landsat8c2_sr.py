# -*- coding:utf-8 -*-

from pie.image.image import PIEImage
from pie.number import PIENumber
from pie.object import PIEObject
from pie.reducer import PIEReducer
from pie.utils.error import ArgsIsNull

def coefficient2Img(listCoefficient):
    resImg = PIEImage(listCoefficient[0])
    for i in range(1, len(listCoefficient)):
        resImg = resImg.addBands(PIEImage(listCoefficient[i]))
    return resImg

def HVL_index (image,region):
    image = image.rename('B1')
    reducer = PIEReducer()
    obj = image.reduceRegion(reducer.minMax(), region, 30)
    max = obj.get("B1_max")
    min = obj.get("B1_min")
    max = PIENumber(max)
    min = PIENumber(min)
    resImg = image.subtract(min).divide(max.subtract(min))
    return resImg

class PIELandsat8C2_SR(PIEObject):
    def __init__(self):
        super(PIELandsat8C2_SR, self).__init__()
        self.pre = None
        self.statement = None

    @staticmethod
    def name():
        return "PIELandsat8C2_SR"

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
        计算MNDWI增强型水体指数
        :param input:
        :return:
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
    def imperviousSurface(cls, input, region, threshold=0):
        """
        不透水层算法
        :param input:
        :param region:
        :param threshold:
        :return:
        """
        # 1.研究区域设定
        if not region:
            region = input.geometry()
        else:
            input = input.clip(region)

        # 2.进行辐射校正
        bandsname = ['B2', 'B3', 'B4', 'B5', 'B6', 'B7']
        outbandsname = ['Blue', 'Green', 'Red', 'Nir', 'Swir1', 'Swir2']
        ref_img = input.select(bandsname).multiply(0.0000275).add(-0.2).rename(outbandsname)

        # 3.进行缨帽变换
        coe_TC1_brightness = [0.3029, 0.2786, 0.4733, 0.5599, 0.5080, 0.1872]
        coe_TC2_green = [-0.2941, -0.2430, -0.5424, 0.7276, 0.0713, -0.1608]
        coe_TC3_wet = [0.1511, 0.1973, 0.3283, 0.3407, -0.7117, -0.4559]
        redu = PIEReducer()
        img_TC1 = ref_img.multiply(coefficient2Img(coe_TC1_brightness)).reduce(redu.sum()).rename('TC1')
        img_TC2 = ref_img.multiply(coefficient2Img(coe_TC2_green)).reduce(redu.sum()).rename('TC2')
        img_TC3 = ref_img.multiply(coefficient2Img(coe_TC3_wet)).reduce(redu.sum()).rename('TC3')

        # 4.计算绿度、亮度、湿度
        img_H = HVL_index(img_TC1, region)
        img_V = HVL_index(img_TC2, region)
        img_L = HVL_index(img_TC3, region)

        # 5.计算BCI指数
        img1 = img_H.add(img_L).multiply(0.5)
        img_BCI = img1.subtract(img_V).divide(img1.add(img_V)).rename('BCI')

        # 6.水体掩膜
        imgG = ref_img.select('Green')
        imgIR = ref_img.select('Swir1')
        img_mndwi = imgG.subtract(imgIR).divide(imgG.add(imgIR)).rename('MNDWI')
        mask_water = img_mndwi.lt(0.2)

        # 7.得到不透水面
        img_imperviousSurface = img_BCI.gt(threshold).multiply(mask_water).clip(region)
        return img_imperviousSurface.rename("surface")

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

Landsat8C2_SR = PIELandsat8C2_SR()

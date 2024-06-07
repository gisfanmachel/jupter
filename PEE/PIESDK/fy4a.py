# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   fy4a.py
@Time    :   2020/8/6 下午5:19
@Author  :   liuxiaodong
@Version :   1.0
@Contact :   2152550864@qq.com
@License :   (C)Copyright 2019-2020, liuxiaodong
@Desc    :   None
"""
from .object import PIEObject
from .image import PIEImage
from .utils.error import ArgsIsNull

def _generatePIEImage(pre, statement):
    """
    生成 PIEImage 对象
    :param pre:
    :param statement:
    :return:
    """
    _object = PIEImage()
    _object.pre = pre
    _object.statement = statement
    return _object

class PIEPlugin_FY4a(PIEObject):
    def __init__(self):
        super(PIEPlugin_FY4a, self).__init__()
        self.pre = None
        self.statement = None

    @staticmethod
    def name():
        return "PIEPlugin_FY4a"

    @staticmethod
    def AOT(input, water_mask=None):
        ImageA = input.select(["B1","B2","B3","B4","B5","B6","B8","B12","B15","B16","B17","B18"])
        if water_mask is None:
            imageWater = PIEImage("user/101/public/SeaLand").select("B1")
            # water_mask_statement = imageWater.statement
            water_mask_statement = PIEPlugin_FY4a.formatValue(imageWater)
        else:
            # water_mask_statement = water_mask.statement
            water_mask_statement = PIEPlugin_FY4a.formatValue(water_mask)
        _obj = PIEPlugin_FY4a().getStatement(functionName="PluginFY4A.AOT",
                                             arguments={
                                                 "input": PIEPlugin_FY4a.formatValue(ImageA),
                                                 "water_mask": water_mask_statement
                                             })
        # _obj = {
        #     "type": "Invocation",
        #     "arguments": {
        #         "input": ImageA.statement,
        #         "water_mask": water_mask_statement
        #     },
        #       "functionName": "PluginFY4A.AOT",
        # }
        return _generatePIEImage(ImageA, _obj)

    @staticmethod
    def PM25(input, water_mask=None):
        ImageA = input.select(["B1", "B2", "B3", "B4", "B5", "B6", "B8", "B12", "B15", "B16", "B17", "B18"])
        if water_mask is None:
            imageWater = PIEImage("user/101/public/SeaLand").select("B1")
            water_mask_statement = PIEPlugin_FY4a.formatValue(imageWater)
        else:
            water_mask_statement = PIEPlugin_FY4a.formatValue(water_mask)

        _obj = PIEPlugin_FY4a().getStatement(functionName="PluginFY4A.PM25",
                                             arguments={
                                                 "input": PIEPlugin_FY4a.formatValue(ImageA),
                                                 "water_mask": water_mask_statement,
                                             })
        return _generatePIEImage(ImageA, _obj)

    @staticmethod
    def PM100(input, water_mask=None):
        ImageA = input.select(["B1", "B2", "B3", "B4", "B5", "B6", "B8", "B12", "B15", "B16", "B17", "B18"])
        if water_mask is None:
            imageWater = PIEImage("user/101/public/SeaLand").select("B1")
            water_mask_statement = PIEPlugin_FY4a.formatValue(imageWater)
        else:
            water_mask_statement = PIEPlugin_FY4a.formatValue(water_mask)

        _obj = PIEPlugin_FY4a().getStatement(functionName="PluginFY4A.PM100",
                                             arguments={
                                                 "input": PIEPlugin_FY4a.formatValue(ImageA),
                                                 "water_mask": water_mask_statement
                                             })
        return _generatePIEImage(ImageA, _obj)

    @staticmethod
    def rgb(input, type="Airmass"):
        if input is None: return None
        if type == "Airmass":
            image9 = input.select("B9")
            image10 = input.select("B10")
            image11 = input.select("B11")
            image12 = input.select("B12")
            imageR = image9.subtract(image10).divide(100).subtract(-20).divide(20).multiply(255)
            imageG = image11.subtract(image12).divide(100).subtract(-8).divide(14).multiply(255)
            imageB = image9.divide(100).subtract(248).divide(-40).multiply(255)
            imageRGB = imageR.addBands(imageG).addBands(imageB).rename(["R", "G", "B"])
            return imageRGB
        elif type == "Day_Convective_Storms":
            image2 = input.select("B2")
            image5 = input.select("B5")
            image7 = input.select("B7")
            image9 = input.select("B9")
            image10 = input.select("B10")
            image12 = input.select("B12")

            imageR = image9.subtract(image10).divide(100).subtract(-35).divide(40).multiply(255)
            imageG = image7.subtract(image12).divide(100).subtract(-5).divide(65).power(1 / 0.3).multiply(255)
            imageB = image5.subtract(image2).divide(10000).subtract(-0.75).divide(1.05).multiply(255)
            imageRGB = imageR.addBands(imageG).addBands(imageB).rename(["R", "G", "B"])
            return imageRGB
        elif type == "Night_Microphysics":
            image7 = input.select("B7")
            image13 = input.select("B13")
            image12 = input.select("B12")

            imageR = image13.subtract(image12).divide(100).subtract(-4).divide(6).multiply(255)
            imageG = image12.subtract(image7).divide(100).subtract(-2).divide(7).multiply(255)
            imageB = image12.divide(100).subtract(243).divide(40).multiply(255)
            imageRGB = imageR.addBands(imageG).addBands(imageB).rename(["R", "G", "B"])
            return imageRGB
        elif type == "Day_Microphysics":
            image3 = input.select("B3")
            image7 = input.select("B7")
            image12 = input.select("B12")

            imageR = image3.divide(10000).multiply(255)
            imageG = image7.divide(100).divide(0.3).power(1 / 1.8).multiply(255)
            imageB = image12.divide(100).subtract(203).divide(120).multiply(255)
            imageRGB = imageR.addBands(imageG).addBands(imageB).rename(["R", "G", "B"])
            return imageRGB
        elif type == "Dust":
            image12 = input.select("B12")
            image11 = input.select("B11")
            image13 = input.select("B13")

            imageR = image13.subtract(image12).divide(100).subtract(-4).divide(6).multiply(255)
            imageG = image12.subtract(image11).divide(100).divide(15).power(0.4).multiply(255)
            imageB = image12.divide(100).subtract(261).divide(28).multiply(255)
            imageRGB = imageR.addBands(imageG).addBands(imageB).rename(["R", "G", "B"])
            return imageRGB
        elif type == "Clouds_Convection":
            image3 = input.select("B3")
            image12 = input.select("B12")

            imageR = image3.divide(10000).multiply(255)
            imageG = image3.divide(10000).multiply(255)
            imageB = image12.divide(100).subtract(323).divide(-120).multiply(255)
            imageRGB = imageR.addBands(imageG).addBands(imageB).rename(["R", "G", "B"])
            return imageRGB
        elif type == "Severe_Storm":
            image3 = input.select("B3")
            image12 = input.select("B12")
            image7 = input.select("B7")

            imageR = image3.divide(10000).multiply(255)
            imageG = image3.divide(10000).multiply(255)
            imageB = image12.subtract(image7).divide(100).subtract(-60).divide(100).power(0.5).multiply(255)
            imageRGB = imageR.addBands(imageG).addBands(imageB).rename(["R", "G", "B"])
            return imageRGB
        elif type == "Ash":
            image12 = input.select("B12")
            image13 = input.select("B13")
            image11 = input.select("B11")

            imageR = image13.subtract(image12).divide(100).subtract(-4).divide(7).multiply(255)
            imageG = image12.subtract(image11).divide(100).subtract(-4).divide(9).multiply(255)
            imageB = image12.divide(100).subtract(240).divide(63).multiply(255)
            imageRGB = imageR.addBands(imageG).addBands(imageB).rename(["R", "G", "B"])
            return imageRGB
        elif type == "Snow_Fog":
            image3 = input.select("B3")
            image5 = input.select("B5")
            image7 = input.select("B7")

            imageR = image3.divide(10000).power(1 / 1.7).multiply(255)
            imageG = image5.divide(10000).divide(0.7).power(1 / 1.7).multiply(255)
            imageB = image7.divide(100).divide(0.25).power(1 / 1.7).multiply(255)
            imageRGB = imageR.addBands(imageG).addBands(imageB).rename(["R", "G", "B"])
            return imageRGB
        elif type == "Natural":
            image2 = input.select("B2")
            image5 = input.select("B5")
            image3 = input.select("B3")

            imageR = image5.divide(10000).power(1 / 1.2).multiply(255)
            imageG = image3.divide(10000).power(1 / 1.2).multiply(255)
            imageB = image2.divide(10000).power(1 / 1.5).multiply(255)
            imageRGB = imageR.addBands(imageG).addBands(imageB).rename(["R", "G", "B"])
            return imageRGB

    @staticmethod
    def cloudMask(input):
        soz = input.select("B18").divide(100)
        image_day = soz.lte(90)
        image_night = soz.gt(90)
        b2 = input.select("B2").divide(10000)
        b3 = input.select("B3").divide(10000)
        b12 = input.select("B12").divide(100)
        b13 = input.select("B13").divide(100)
        cloud_day = image_day.And(((b2.add(b3)).gt(0.3)).Or(b13.lt(225)).Or(((b2.add(b3)).gt(0.25)).And(b13.lt(275))))
        cloud_night = image_night.And(b12.lt(245))
        cloud = cloud_day.Or(cloud_night)
        return cloud

    @staticmethod
    def snowPercent(input, landuseFile, cloudMask=None):
        ImageA = input.select(["B2", "B3", "B4", "B5", "B6", "B11", "B12", "B13", "B18"])
        ImageLu = landuseFile.select(["B1"])

        _obj = PIEPlugin_FY4a().getStatement(functionName="PluginFY4A.SnowPercent",
                                             arguments={
                                                 "input": PIEPlugin_FY4a.formatValue(ImageA),
                                                 "landuseFile": PIEPlugin_FY4a.formatValue(ImageLu),
                                             })
        image = _generatePIEImage(ImageA, _obj)
        if cloudMask is not None:
            image = image.updateMask(cloudMask.eq(0))
        return image


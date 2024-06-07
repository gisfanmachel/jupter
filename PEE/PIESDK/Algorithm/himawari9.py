# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   himawari8.py
@Time    :   2020/10/9 下午3:20
@Author  :   lsw
@Version :   1.0
@Contact :   shi_weihappy@126.com
@License :   (C)Copyright 2019-2020, lsw
@Desc    :   None
葵花八数据方法
"""
from pie.object import PIEObject
from pie.image.image import PIEImage
from pie.utils.error import ArgsIsNull

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

class PIEHimawari9(PIEObject):
    def __init__(self):
        super(PIEHimawari8, self).__init__()
        self.pre = None
        self.statement = None

    @staticmethod
    def name():
        return "PIEHimawari8"

    def rgb(self, input, type="Airmass"):
        """
        葵花8数据RGB合成
        :param input:
        :param type:
        合成模型
        Airmass表示气团
        Day_Convective_Storms表示白天对流风暴
        Night_Microphysics表示夜间云微物理
        Day_Microphysics表示白天云微物理
        :return:
        """
        if input is None or type is None:
            raise ArgsIsNull("input, type")
        if type == "Airmass":
            image8 = input.select("B8")
            image10 = input.select("B10")
            image12 = input.select("B12")
            image13 = input.select("B13")
            imageR = image8.subtract(image10).divide(100).subtract(-25).divide(25).multiply(255)
            imageG = image12.subtract(image13).divide(100).subtract(-40).divide(45).multiply(255)
            imageB = image8.divide(100).subtract(243).divide(-35).multiply(255)
            imageRGB = imageR.addBands(imageG).addBands(imageB).rename(["R", "G", "B"])
            return imageRGB
        elif type == "Day_Convective_Storms":
            image3 = input.select("B3")
            image5 = input.select("B5")
            image7 = input.select("B7")
            image8 = input.select("B8")
            image10 = input.select("B10")
            image13 = input.select("B13")
            imageR = image8.subtract(image10).divide(100).subtract(-35).divide(40).multiply(255)
            imageG = image7.subtract(image13).divide(100).subtract(-5).divide(65).power(2).multiply(255)
            imageB = image5.subtract(image3).divide(10000).subtract(-0.75).multiply(255)
            imageRGB = imageR.addBands(imageG).addBands(imageB).rename(["R", "G", "B"])
            return imageRGB
        elif type == "Night_Microphysics":
            image7 = input.select("B7")
            image13 = input.select("B13")
            image15 = input.select("B15")
            imageR = image15.subtract(image13).divide(100).subtract(-4).divide(6).multiply(255)
            imageG = image13.subtract(image7).divide(100).divide(10).multiply(255)
            imageB = image13.divide(100).subtract(243).divide(50).multiply(255)
            imageRGB = imageR.addBands(imageG).addBands(imageB).rename(["R", "G", "B"])
            return imageRGB
        elif type == "Day_Microphysics":
            image4 = input.select("B4")
            image7 = input.select("B7")
            image13 = input.select("B13")
            imageR = image4.divide(10000).subtract(0).multiply(255)
            imageG = image7.divide(100).divide(0.6).power(0.4).multiply(255)
            imageB = image13.divide(100).subtract(203).divide(120).multiply(255)
            imageRGB = imageR.addBands(imageG).addBands(imageB).rename(["R", "G", "B"])
            return imageRGB
        elif type == "Dust":
            image15 = input.select("B15")
            image11 = input.select("B11")
            image13 = input.select("B13")
            imageR = image15.subtract(image13).divide(100).subtract(-4).divide(6).multiply(255)
            imageG = image13.subtract(image11).divide(100).divide(15).power(0.4).multiply(255)
            imageB = image13.divide(100).subtract(261).divide(28).multiply(255)
            imageRGB = imageR.addBands(imageG).addBands(imageB).rename(["R", "G", "B"])
            return imageRGB
        elif type == "Clouds_Convection":
            image4 = input.select("B4")
            image13 = input.select("B13")
            imageR = image4.divide(10000).multiply(255)
            imageG = image4.divide(10000).multiply(255)
            imageB = image13.divide(100).subtract(323).divide(-120).multiply(255)
            imageRGB = imageR.addBands(imageG).addBands(imageB).rename(["R", "G", "B"])
            return imageRGB
        elif type == "Severe_Storm":
            image4 = input.select("B4")
            image13 = input.select("B13")
            image7 = input.select("B7")
            imageR = image4.divide(10000).multiply(255)
            imageG = image4.divide(10000).multiply(255)
            imageB = image13.subtract(image7).divide(100).\
                subtract(-60).divide(100).power(0.5).multiply(255)
            imageRGB = imageR.addBands(imageG).addBands(imageB).rename(["R", "G", "B"])
            return imageRGB
        elif type == "Ash":
            image15 = input.select("B15")
            image13 = input.select("B13")
            image11 = input.select("B11")

            imageR = image15.subtract(image13).divide(100).subtract(-4).divide(6).multiply(255)
            imageG = image13.subtract(image11).divide(100).subtract(-4).divide(9).multiply(255)
            imageB = image13.divide(100).subtract(243).divide(60).multiply(255)
            imageRGB = imageR.addBands(imageG).addBands(imageB).rename(["R", "G", "B"])
            return imageRGB
        elif type == "Snow_Fog":
            image4 = input.select("B4")
            image5 = input.select("B5")
            image7 = input.select("B7")

            imageR = image4.divide(10000).power(1 / 1.7).multiply(255)
            imageG = image5.divide(10000).divide(0.7).power(1 / 1.7).multiply(255)
            imageB = image7.divide(100).divide(0.3).power(1 / 1.7).multiply(255)
            imageRGB = imageR.addBands(imageG).addBands(imageB).rename(["R", "G", "B"])
            return imageRGB
        elif type == "Natural":
            image4 = input.select("B4")
            image5 = input.select("B5")
            image3 = input.select("B3")
            imageR = image5.divide(10000).multiply(255)
            imageG = image4.divide(10000).multiply(255)
            imageB = image3.divide(10000).multiply(255)
            imageRGB = imageR.addBands(imageG).addBands(imageB).rename(["R", "G", "B"])
            return imageRGB
        elif type == "TrueColor":
            return self.rgbTC(input)
        else:
            raise ArgsIsNull("录入的类型不存在")

    def rgbTC(self, input):
        """
        计算RGB
        :param input:
        :return:
        """
        if input is None:
            raise ArgsIsNull("input")
        #todo 修改部分
        image19 = PIEImage('user/101/public/H08/sateAzimuth').select("B1").rename("B19")
        image20 = PIEImage('user/101/public/H08/sateZenith').select("B1").rename("B20")
        image21 = PIEImage('user/101/public/H08/DEM').select("B1").rename("B21")
        imageA = input.addBands(image19).addBands(image20).addBands(image21)
        imageA = imageA.select(["B1", "B2", "B3", "B4", "B7", "B13", "B17", "B18", "B19", "B20", "B21"])

        obj = self.getStatement(
            arguments={
                "input": self.formatValue(imageA),
            },
            functionName="PluginAtmospheric.rgbTC"
        )
        image = _generatePIEImage(imageA, obj)
        return image

    def sst(self, input):
        """
        计算sst
        :param input:
        :return:
        """
        if input is None:
            raise ArgsIsNull("input")
        image20 = PIEImage('user/101/public/H08/sateZenith').select("B1").rename("B20")
        imageA = input.addBands(image20)
        imageA = imageA.select(["B3", "B13", "B14", "B18", "B20"])
        _obj = self.getStatement(
            functionName="PluginAtmospheric.sst",
            arguments={
                "input": self.formatValue(imageA)
        })
        image = _generatePIEImage(imageA, _obj)
        image = image.divide(100)
        imageMask = PIEImage("user/101/public/SeaLand").select("B1")
        image = image.updateMask(imageMask.eq(0))
        return image

    def legend(self, type="Airmass"):
        """
        生成图例
        :param type:
        :return:
        """
        if type is None:
            raise ArgsIsNull("type")
        colors = []
        labels = []
        infos = []
        title = ""
        if type == "Airmass":
            title = "气团"
            colors = ["#ffffff", "#efbea2", "#494772", "#820b12", "#3a127c", "#207125", "#727113"]
            labels = ["厚高层云", "厚中层云", "高纬度厚低云", "高空急流", "冷气团", "对流层上部高湿度暖气团", "对流层上部低湿度暖气团"]
            infos = ["R=WV(6.2)-W3(7.3)", "G=O3(9.7)-IR(10.8)", "B=WV(6.2)"]
        elif type == "Day_Convective_Storms":
            title = "白天对流风暴"
            colors = ["#df291e", "#fffe70", "#a82b5b", "#b51dbb", "#3c14a7", "#5726fb"]
            labels = ["深对流层云", "强烈上升积雨云", "大冰粒卷云", "小冰粒卷云", "海洋", "陆地"]
            infos = ["R=WV(6.2)-W3(7.3)", "G=I4(3.9)-IR(10.8)", "B=NIR(1.6)-VIS(0.6)"]
        elif type == "Night_Microphysics":
            title = "夜间云微物理"
            colors = ["#810308", "#15153b", "#a6feee", "#3024fa", "#cccdfe", "#ba8846", "#bf66a4", "#80070a", "#97ec75"]
            labels = ["冷厚高层云", "卷云", "雾", "海洋", "暖低云", "厚中层云", "陆地", "过冷高层云", "冷低云"]
            infos = ["R=I2(12.0)-IR(10.4)", "G=IR(10.4)-I4(3.9)", "B=IR(10.4)"]
        elif type == "Day_Microphysics":
            title = "白天云微物理"
            colors = ["#f33371", "#cc9532", "#b5c2a3", "#539530", "#0726b4", "#e6f86f", "#e41918", "#d7a29f"]
            labels = ["雪", "上升积雨云（大粒径冰云）", "雾", "薄卷云（小粒径冰云）", "海洋", "过冷厚水云", "深积云（小粒径冰云）", "暖水云"]
            infos = ["R=N1(0.86)", "G=I4(3.9)", "B=IR(10.4)"]
        return {
            "title": title,
            "labels": labels,
            "colors": colors,
            "infos": infos
        }

    @classmethod
    def cloudMask(cls, input):
        """
        计算云掩膜
        :param input:
        :return:
        """
        if input is None:
            raise ArgsIsNull("input")
        image90 = PIEImage.constant(90)
        imageSunZ = image90.subtract(input.select("B18").divide(100))
        imageSunZMask = imageSunZ.lte(90)
        imageRef0064 = input.select("B3").divide(10000)
        imageTb112 = input.select("B14").divide(100)
        imageCloudDay = imageRef0064.gt(0.05).And(imageRef0064.lt(1)).And(imageTb112.lt(275))
        imageCloudNight = imageTb112.lt(270)
        imageCloud = imageCloudNight.where(imageSunZMask, imageCloudDay)
        return imageCloud

    def AOT(self, input, water_mask=None):
        """
        计算AOT
        :param input:
        :param water_mask:
        :return:
        """
        if input is None:
            raise ArgsIsNull("input")
        image_SatA = PIEImage('user/101/public/H08/sateAzimuth').select("B1").rename("B19") # 卫星方位角
        image_SatZ = PIEImage('user/101/public/H08/sateZenith').select("B1").rename("B20") # 卫星天顶角
        input = input.addBands(image_SatA).addBands(image_SatZ)

        ImageA = input.select(["B1", "B2", "B3", "B4", "B6", "B14", "B17", "B18", "B19", "B20"])
        imageWaterMask = water_mask
        if water_mask is None:
            imageWaterMask = PIEImage("user/101/public/SeaLand").select("B1")
        imageDem = PIEImage("user/101/public/H08/DEM").select("B1")
        imageCloudMask = self.cloudMask(input).rename("B1")
        _obj = self.getStatement(
            functionName="PluginAtmospheric.AOT",
            arguments={
                "input": self.formatValue(ImageA),
                "cloud_mask": self.formatValue(imageCloudMask),
                "dem_mask": self.formatValue(imageDem),
                "water_mask": self.formatValue(imageWaterMask)
            }
        )
        return _generatePIEImage(ImageA, _obj)

    def PM25(self, input, water_mask=None):
        """
        计算PM2.5
        :param input:
        :param water_mask:
        :return:
        """
        if input is None:
            raise ArgsIsNull("input")

        image_SatA = PIEImage('user/101/public/H08/sateAzimuth').select("B1").rename("B19")  # 卫星方位角
        image_SatZ = PIEImage('user/101/public/H08/sateZenith').select("B1").rename("B20")  # 卫星天顶角
        input = input.addBands(image_SatA).addBands(image_SatZ)

        ImageA = input.select(["B1", "B2", "B3", "B4", "B6", "B14", "B17", "B18", "B19", "B20"])
        imageWaterMask = water_mask
        if water_mask is None:
            imageWaterMask = PIEImage("user/101/public/SeaLand").select("B1")
        imageDem = PIEImage("user/101/public/H08/DEM").select("B1")
        imageCloudMask = self.cloudMask(input).rename("B1")

        _obj = self.getStatement(
            functionName="PluginAtmospheric.PM25",
            arguments={
                "input": self.formatValue(ImageA),
                "cloud_mask": self.formatValue(imageCloudMask),
                "dem_mask": self.formatValue(imageDem),
                "water_mask": self.formatValue(imageWaterMask)
            }
        )
        return _generatePIEImage(ImageA, _obj)

    def PM100(self, input, water_mask=None):
        """
        计算PM10
        :param input:
        :param water_mask:
        :return:
        """
        if input is None:
            raise ArgsIsNull("input")

        image_SatA = PIEImage('user/101/public/H08/sateAzimuth').select("B1").rename("B19")  # 卫星方位角
        image_SatZ = PIEImage('user/101/public/H08/sateZenith').select("B1").rename("B20")  # 卫星天顶角
        input = input.addBands(image_SatA).addBands(image_SatZ)

        ImageA = input.select(["B1", "B2", "B3", "B4", "B6", "B14", "B17", "B18", "B19", "B20"])
        imageWaterMask = water_mask
        if water_mask is None:
            imageWaterMask = PIEImage("user/101/public/SeaLand").select("B1")
        imageDem = PIEImage("user/101/public/H08/DEM").select("B1")
        imageCloudMask = self.cloudMask(input).rename("B1")

        _obj = self.getStatement(
            functionName="PluginAtmospheric.PM100",
            arguments={
                "input": self.formatValue(ImageA),
                "cloud_mask": self.formatValue(imageCloudMask),
                "dem_mask": self.formatValue(imageDem),
                "water_mask": self.formatValue(imageWaterMask)
            }
        )
        return _generatePIEImage(ImageA, _obj)

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
        imageMir = input.select("B16")

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
        imageMIR = input.select("B16")
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

Himawari9 = PIEHimawari9()


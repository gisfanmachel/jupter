# -*- coding:utf-8 -*-

from pie.object import PIEObject
from pie.utils.error import ArgsIsNull


def _generatePIEImage(pre, statement):
    """
    生成 PIEImage 对象
    :param pre:
    :param statement:
    :return:
    """
    from pie.image.image import PIEImage
    _object = PIEImage()
    _object.pre = pre
    _object.statement = statement
    return _object


class PIEGF1(PIEObject):
    def __init__(self):
        super(PIEGF1, self).__init__()
        self.pre = None
        self.statement = None

    @staticmethod
    def name():
        return "PIEGF1"

    def coastlineExtract(self, input):
        """
        识别海岸线
        :param input:
        :return:
        """
        if input is None:
            raise ArgsIsNull("input")
        _obj = self.getStatement(
            arguments={
                "image1": self.formatValue(input)
            },
            functionName="Image.coastlineExtract"
        )
        return _generatePIEImage(self, _obj)


    def shipDetection(self,input) :
        """
        船体识别
        :param input:
        :return:
        """
        if not input:
            raise ArgsIsNull("input")
        _obj = self.getStatement(
            arguments={
                "image1": self.formatValue(input)
            },
            functionName="Image.shipDetection"
        )

        return _generatePIEImage(self, _obj)

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
    def EVI(cls, input):
        """
        计算EVI植被指数
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


GF1 = PIEGF1()
# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   projection.py
@Time    :   2020/8/5 下午3:42
@Author  :   lsw
@Version :   1.0
@Contact :   shi_weihappy@126.com
@License :   (C)Copyright 2019-2020, lsw
@Desc    :   None
"""
from pie.object import PIEObject
import math

class PIEProjection(PIEObject):
    def __init__(self, crs=None, transform=None, wkt=None):
        """
        初始化投影信息类
        :param crs:
        :param transform:
        :param wkt:
        """
        super(PIEProjection, self).__init__()
        self._crs = crs
        self._transform = transform
        self._wkt = wkt
        if crs and type(crs).__name__ == self.name():
            self.pre = crs.pre
            self.statement = crs.statement
        else:
            self.pre = None
            self.statement = self.getStatement(
                functionName="Projection",
                arguments={"crs": crs}
            )

    @staticmethod
    def name():
        return "PIEProjection"

    def crs(self, image):
        """
        获取投影信息
        :param image:
        :return:
        """
        coords = list()
        wkt = image.getInfo()
        band_info = wkt.get("bands")
        for id in band_info:
            wkt = id.get("wkt")
            crs = wkt[id.get("wkt").index("SPHEROID"):107]
            spheroid = crs.split("[")[0]
            coord = crs.split("[")[1]
            coords.append(coord)
        return coords

    def wkt(self, image):
        """
        获取wkt字符串
        :param image:
        :return:
        """
        img_wkt = list()
        wkt = image.getInfo()
        band_info = wkt.get("bands")
        for id in band_info:
            img_wkt.append(id.get("wkt"))
        return img_wkt

    def transform(self, image):
        """
        转投影
        :param image:
        :return:
        """
        img_extent = list()
        wkt = image.getInfo()
        band_info = wkt.get("bands")
        for id in band_info:
            img_extent.append(id.get("extent"))
        return img_extent

    @staticmethod
    def WebMercatorToWGS84(point):
        """
        web墨卡托转为84投影
        :param point:
        :return:
        """
        if not isinstance(point, dict):
            print("The point is not dict genre")
            raise AttributeError
        lnglat = {"lng": point.get("x") / 20037508.34 * 180, "lat": 0}
        mmy = point.get("y") /  20037508.34 * 180
        lnglat["lat"] = 180 / math.pi * (2 * math.atan(math.exp(mmy * math.pi / 180.0)) - math.pi / 2.0)
        return lnglat

    @staticmethod
    def WGS84ToWebMercator(point):
        """
        84投影转为web墨卡托
        :param point:
        :return:
        """
        if not isinstance(point, dict):
            print("The point is not dict genre")
            raise AttributeError
        mercator = {"x":0, "y": 0}
        earthRad = 6378137.0
        mercator["x"] = point.get("lng") * math.pi / 180 * earthRad
        a = point.get("lat") * math.pi / 180
        mercator["y"] = earthRad / 2 * math.log((1.0 + math.sin(a)) / (1.0 - math.sin(a)))
        return mercator


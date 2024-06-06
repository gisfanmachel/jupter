# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   geometry.py
@Time    :   2020/8/2 上午11:10
@Author  :   lsw
@Version :   1.0
@Contact :   shi_weihappy@126.com
@License :   (C)Copyright 2019-2020, lsw
@Desc    :   None
"""
from pie.object import PIEObject
from pie.utils.error import ArgsIsNull, ArgsTypeIsWrong
from pie.utils.common import encodeJSON
import numpy as np

def _generatePIENumber(pre, statement):
    """
    生成 PIENumber 对象
    :param pre:
    :param statement:
    :return:
    """
    from pie.number import PIENumber
    _object = PIENumber()
    _object.pre = pre
    _object.statement = statement
    return _object

def _generatePIEGeometry(pre, statement):
    """
    生成 PIEGeometry 的对象
    :param pre:
    :param statement:
    :return:
    """
    _object = PIEGeometry()
    _object.pre = pre
    _object.statement = statement
    return _object

class PIEGeometry(PIEObject):
    def __init__(self, geoJson=None, proj=None, geodesic=True, evenOdd=True):
        """
        :param geoJson:描述几何图形的GeoJSON对象
        :param proj:坐标系，默认的是WGS84
        :param geodesic:
        :param evenOdd:
        """
        super(PIEGeometry, self).__init__()
        self._geoJson = None
        self.geoJson = geoJson
        self.pre = None
        self.statement = None
        if geoJson is None:
            return

        if type(geoJson).__name__ == self.name():
            self.pre = geoJson.pre
            self.statement = geoJson.statement
        elif type(geoJson).__name__ == PIEObject.name():
            self.statement = self.getStatement(
                functionName="Geometry.constructors",
                arguments={
                    "geometry": self.formatValue(geoJson),
                    "proj": self.formatValue(proj),
                    "geodesic": geodesic,
                    "evenOdd": evenOdd
                },
                compress="polyline"
            )
        else:
            self.statement = self.getStatement(
                functionName="Geometry.constructors",
                arguments={
                    "geometry": geoJson,
                    "proj": self.formatValue(proj),
                    "geodesic": geodesic,
                    "evenOdd": evenOdd
                },
                compress="polyline"
            )

    @property
    def geoJson(self):
        return self._geoJson

    @geoJson.setter
    def geoJson(self, value):
        self._geoJson = value

    def getGeometryType(self):
        """
        获取矢量数据的类型
        :return:
        """
        if self.geoJson:
            return self.geoJson.get("type", PIEGeometry.name())
        return PIEGeometry.name()

    def getGeometryCoordinates(self):
        """
        获取矢量数据的坐标列表
        :return:
        """
        if self.geoJson:
            return self.geoJson.get("coordinates", None)
        return None

    @staticmethod
    def name():
        return "PIEGeometry"

    @staticmethod
    def Point(coords, proj=None):
        """
        构造点对象
        :param coords: 给定坐标系下xy坐标的List
        :param proj:坐标系，默认的是WGS84
        :return:
        """
        geojson = {
            "type": "Point",
            "coordinates": coords
        }
        return PIEGeometry(
            geoJson=geojson,
            proj=proj,
            geodesic=True,
            evenOdd=True
        )

    @staticmethod
    def MultiPoint(coords, proj=None):
        """
        构造复合点对象
        :param coords: 给定坐标系下xy坐标的List
        :param proj:坐标系，默认的是WGS84
        :return:
        """
        if coords is None:
            raise ArgsIsNull("coords")
        coords = np.array(coords)
        if not isinstance(coords, np.ndarray):
            raise ArgsTypeIsWrong("coords必须是数组")
        if not isinstance(coords[0], np.ndarray):
            raise ArgsTypeIsWrong()
        if len(coords) < 2:
            raise ArgsTypeIsWrong()
        if len(coords[0]) != 2:
            raise ArgsTypeIsWrong()
        coords = coords.tolist()

        geojson = {
            "type": "MultiPoint",
            "coordinates": coords
        }
        return PIEGeometry(
            geoJson=geojson,
            proj=proj,
            geodesic=True,
            evenOdd=True
        )

    @staticmethod
    def LineString(coords, proj=None, geodesic=True, maxError=None):
        """

        :param coords:
        :param proj:
        :param geodesic:
        :param maxError:
        :return:
        """
        if coords is None: raise ArgsIsNull("coords")
        coords = np.array(coords)
        if not isinstance(coords, np.ndarray): raise ArgsTypeIsWrong('coords类型不对')
        if not isinstance(coords[0], np.ndarray): raise ArgsIsNull()
        if len(coords) < 2: raise ArgsIsNull()
        if len(coords[0]) != 2: raise ArgsIsNull()
        coords = coords.tolist()

        geojson = {
            "type": "LineString",
            "coordinates": coords
        }
        return PIEGeometry(
            geoJson=geojson,
            proj=proj,
            geodesic=geodesic,
            evenOdd=True
        )

    @staticmethod
    def MultiLineString(coords, proj=None, geodesic=True, maxError=None):
        """

        :param coords:
        :param proj:
        :param geodesic:
        :param maxError:
        :return:
        """
        if coords is None: raise ArgsIsNull("coords")
        coords = np.array(coords)
        if not isinstance(coords, np.ndarray): raise ArgsTypeIsWrong('coords类型不对')
        if not isinstance(coords[0], np.ndarray): raise ArgsIsNull()
        if not isinstance(coords[0][0], np.ndarray): raise ArgsIsNull()
        coords = coords.tolist()

        geojson = {
            "type": "MultiLineString",
            "coordinates": coords
        }
        return PIEGeometry(
            geoJson=geojson,
            proj=proj,
            geodesic=geodesic,
            evenOdd=True
        )

    @staticmethod
    def LinearRing(coords, proj=None, geodesic=True, maxError=None):
        """

        :param coords:
        :param proj:
        :param geodesic:
        :param maxError:
        :return:
        """
        if coords is None: raise ArgsIsNull("coords")
        coords = np.array(coords)
        if not isinstance(coords, np.ndarray): raise ArgsTypeIsWrong('coords类型不对')
        if not isinstance(coords[0], np.ndarray): raise ArgsIsNull()
        if len(coords) < 2: raise ArgsIsNull()
        if len(coords[0]) != 2: raise ArgsIsNull()
        length = len(coords)
        if coords[0][0] != coords[length - 1][0] \
            or coords[0][1] != coords[length - 1][1]:
            coords[length] = coords[0]

        coords = coords.tolist()
        geojson = {
            "type": "LineString",
            "coordinates": coords
        }
        return PIEGeometry(
            geoJson=geojson,
            proj=proj,
            geodesic=geodesic,
            evenOdd=True
        )

    @staticmethod
    def Polygon(coords, proj=None, geodesic=True, maxError=None, evenOdd=True):
        """

        :param coords:
        :param proj:
        :param geodesic:
        :param maxError:
        :param evenOdd:
        :return:
        """
        coords = np.array(coords)
        if coords is None:
            raise ArgsIsNull("coords")
        if not isinstance(coords, np.ndarray):
            raise ArgsIsNull("coords")

        for c1 in coords:
            if not isinstance(c1, np.ndarray):
                return None
            for c2 in c1:
                if not isinstance(c2, np.ndarray) or (len(c2) != 2):
                    return None

        coords = coords.tolist()
        geojson = {
            "type": "Polygon",
            "coordinates": coords
        }
        return PIEGeometry(
            geoJson=geojson,
            proj=proj,
            geodesic=geodesic,
            evenOdd=evenOdd
        )

    @staticmethod
    def MultiPolygon(coords, proj=None, geodesic=True, maxError=None, evenOdd=True):
        """

        :param coords:
        :param proj:
        :param geodesic:
        :param maxError:
        :param evenOdd:
        :return:
        """
        if coords is None: raise ArgsIsNull("coords")
        coords = np.array(coords)
        if not isinstance(coords, np.ndarray): raise ArgsTypeIsWrong('coords类型不对')
        if not isinstance(coords[0], np.ndarray): raise ArgsIsNull()
        for c1 in coords:
            if not isinstance(c1, np.ndarray):
                return None
            for c2 in c1:
                if not isinstance(c2, np.ndarray):
                    return None
                for c3 in c2:
                    if not isinstance(c3, np.ndarray) or len(c3) != 2:
                        return None
        coords = coords.tolist()
        geojson = {
            "type": "MultiPolygon",
            "coordinates": coords
        }
        return PIEGeometry(
            geoJson=geojson,
            proj=proj,
            geodesic=geodesic,
            evenOdd=evenOdd
        )

    @staticmethod
    def Rectangle(coords, proj=None, geodesic=True, evenOdd=True):
        """

        :param coords:
        :param proj:
        :param geodesic:
        :param evenOdd:
        :return:
        """
        if coords is None: raise ArgsIsNull("coords")
        coords = np.array(coords)
        if not isinstance(coords, np.ndarray): raise ArgsTypeIsWrong('coords类型不对')
        if not isinstance(coords[0], np.ndarray): raise ArgsIsNull()
        if len(coords) < 2: raise ArgsIsNull()
        if len(coords[0]) != 2: raise ArgsIsNull()

        length = len(coords)
        minX = maxX = coords[0][0]
        minY = maxY = coords[0][1]

        for i in range(1, length):
            minX = minX if minX<coords[i][0] else coords[i][0]
            maxX = maxX if maxX>coords[i][0] else coords[i][0]
            minY = minY if minY<coords[i][1] else coords[i][1]
            maxY = maxY if maxY>coords[i][1] else coords[i][1]
        coords = list()
        coords.append([[minX, minY], [maxX, minY], [maxX, maxY], [minX, maxY], [minX, minY]])

        geojson = {
            "type": "Polygon",
            "coordinates": coords
        }
        return PIEGeometry(
            geoJson=geojson,
            proj=proj,
            geodesic=geodesic,
            evenOdd=evenOdd
        )

    def bounds(self, maxError=None, proj=None):
        """
        获得外接矩形
        :param maxError:
        :param proj:
        :return:
        """
        _geometry = self.statement
        _obj = self.getStatement(
            functionName="Geometry.bounds",
            arguments={
                "geometry": _geometry,
                "maxError": maxError,
                "proj": self.formatValue(proj)
            },
            compress="polyline"
        )
        return _generatePIEGeometry(self, _obj)

    def centroid(self, maxError=None, proj=None):
        """
        获得中心点
        :param maxError:
        :param proj:
        :return:
        """
        _geometry = self.statement
        _obj = self.getStatement(
            functionName="Geometry.centroid",
            arguments={
                "geometry": _geometry,
                "maxError": maxError,
                "proj": self.formatValue(proj)
            },
            compress="polyline"
        )
        return _generatePIEGeometry(self, _obj)

    def coordinates(self):
        """
        获得坐标点
        :return:
        """
        if self.geoJson:
            return self.geoJson.get("coordinates", None)
        return None

    def containedIn(self, right, proj=None):
        """
        判断是否被第二个矢量数据包含
        :param right:
        :param proj:
        :return:
        """
        if right is None:
            raise ArgsIsNull('right')
        _obj = self.getStatement(
            functionName="Geometry.containedIn",
            arguments={
                "geometry": self.statement,
                "right": self.formatValue(right),
                "proj": self.formatValue(proj)
            },
            compute=True
        )
        return _generatePIENumber(self, _obj)

    def contains(self, right, proj=None):
        """
        判断是包含否第二个矢量数据
        :param right:
        :param proj:
        :return:
        """
        if right is None:
            raise ArgsIsNull('right')
        _obj = self.getStatement(
            functionName="Geometry.contains",
            arguments={
                "geometry": self.statement,
                "right": self.formatValue(right),
                "proj": self.formatValue(proj)
            },
            compute=True
        )
        return _generatePIENumber(self, _obj)

    def difference(self, right, proj=None):
        """
        获取两个矢量数据的差集
        :param right:
        :param proj:
        :return:
        """
        if right is None:
            raise ArgsIsNull('right')
        _obj = self.getStatement(
            functionName="Geometry.difference",
            arguments={
                "geometry": self.statement,
                "right": self.formatValue(right),
                "proj": self.formatValue(proj)
            },
            compress="polyline"
        )
        return _generatePIEGeometry(self, _obj)

    def disjoint(self, right, proj=None):
        """
        判断两个Geometry是否具有共同点
        :param right:
        :param proj:
        :return:
        """
        if right is None:
            raise ArgsIsNull('right')
        _obj = self.getStatement(
            functionName="Geometry.disjoint",
            arguments={
                "geometry": self.statement,
                "right": self.formatValue(right),
                "proj": self.formatValue(proj)
            },
            compute=True
        )
        return _generatePIENumber(self, _obj)

    def intersects(self, right, proj=None):
        """
        判断两个Geometry是否相交
        :param right:
        :param proj:
        :return:
        """
        if right is None:
            raise ArgsIsNull('right')
        _obj = self.getStatement(
            functionName="Geometry.intersects",
            arguments={
                "geometry": self.statement,
                "right": self.formatValue(right),
                "proj": self.formatValue(proj)
            },
            compute=True
        )
        return _generatePIENumber(self, _obj)

    def intersection(self, right, proj=None):
        """
        获取两个Geometry的交集
        :param right:
        :param proj:
        :return:
        """
        if right is None:
            raise ArgsIsNull('right')
        _obj = self.getStatement(
            functionName="Geometry.intersection",
            arguments={
                "geometry": self.statement,
                "right": self.formatValue(right),
                "proj": self.formatValue(proj)
            },
            compress="polyline"
        )
        return _generatePIEGeometry(self, _obj)

    def union(self, right, proj=None):
        """
        获取两个Geometry的并集
        :param right:
        :param proj:
        :return:
        """
        if right is None:
            raise ArgsIsNull('right')
        _obj = self.getStatement(
            functionName="Geometry.union",
            arguments={
                "geometry": self.statement,
                "right": self.formatValue(right),
                "proj": self.formatValue(proj)
            },
            compress="polyline"
        )
        return _generatePIEGeometry(self, _obj)

    def withinDistance(self, right, distance=1, proj=None):
        """
        判断两个Geometry是否相交
        :param right:
        :param distance:
        :param proj:
        :return:
        """
        if right is None:
            raise ArgsIsNull('right')
        if distance is None:
            distance = 1
        _obj = self.getStatement(
            functionName="Geometry.withinDistance",
            arguments={
                "geometry": self.statement,
                "right": self.formatValue(right),
                "distance": self.formatValue(distance),
                "proj": self.formatValue(proj)
            },
            compute=True
        )
        return _generatePIENumber(self, _obj)

    def simplify(self, proj=None):
        """
        简化Geometry
        :param proj:
        :return:
        """
        _obj = self.getStatement(
            functionName="Geometry.simplify",
            arguments={
                "geometry": self.statement,
                "proj": self.formatValue(proj)
            },
            compress="polyline"
        )
        return _generatePIEGeometry(self, _obj)

    def dissolve(self, proj=None):
        """
        将所有的Geometry融合
        :param proj:
        :return:
        """
        _obj = self.getStatement(
            functionName="Geometry.dissolve",
            arguments={
                "geometry": self.statement,
                "proj": self.formatValue(proj)
            },
            compress="polyline"
        )
        return _generatePIEGeometry(self, _obj)

    def buffer(self, distance, proj=None):
        """
        为Geometry做缓冲
        :param distance:
        :param proj:
        :return:
        """
        if distance is None:
            distance = 10
        _obj = self.getStatement(
            functionName="Geometry.buffer",
            arguments={
                "geometry": self.statement,
                "distance": self.formatValue(distance),
                "proj": self.formatValue(proj)
            },
            compress="polyline"
        )
        return _generatePIEGeometry(self, _obj)

    def area(self, proj=None):
        """
        计算Geometry的面积
        :param proj:
        :return:
        """
        _obj = self.getStatement(
            functionName="Geometry.area",
            arguments={
                "geometry": self.statement,
                "proj": self.formatValue(proj)
            },
        )
        return _generatePIENumber(self, _obj)

    def length(self, proj=None):
        """
        计算Geometry的线段长度
        :param proj:
        :return:
        """
        _obj = self.getStatement(
            functionName="Geometry.length",
            arguments={
                "geometry": self.statement,
                "proj": self.formatValue(proj)
            }

        )
        return _generatePIENumber(self, _obj)

    def perimeter(self, proj=None):
        """
        计算周长-只对线面有效，单位和Proj的单位相同
        """
        _geometry = self.statement
        _obj = self.getStatement(
            functionName="Geometry.perimeter",
            arguments={
                "geometry": _geometry,
                "proj": self.formatValue(proj)
            }
        )
        return _generatePIENumber(self, _obj)

    def toGeoJSON(self):
        """

        :return:
        """
        return self.geoJson

    def toGeoJSONString(self):
        """

        :return:
        """
        if self.geoJson:
            return encodeJSON(self.geoJson)
        return ""


geometry = PIEGeometry()

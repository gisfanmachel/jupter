# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   ai.py
@Time    :   2020/8/6 下午5:19
@Author  :   lsw
@Version :   1.0
@Contact :   shi_weihappy@126.com
@License :   (C)Copyright 2019-2020, lsw
@Desc    :   None
"""

from .object import PIEObject
from .utils.common import uuid1
from .utils.http import getUserInfo, POST

AI_DETECT_TYPE = {
    "AIR_PLANE": "PLANE",
    "DDZD": "DDZD",
    "WATER": "WATER",
    "SOLAR": "SOLAR",
    "GREENHOUSE": "GREENHOUSE",
    "ROADS_BJ": "ROADS_BJ",
    "BUILD":"BUILD"
}

def _detectAlgorithm(param, errorMsg, style, coordinates, pieMap=None):
    """

    :param param:
    :param errorMsg:
    :param style:
    :param coordinates:
    :param pieMap:
    :return:
    """
    layerName = param.get("layerName")
    val = {
        "pageCount":0,
        "queryResultList":[],
        "queryConditionList":[],
        "orderColName":"",
        "pageNum":0,
        "collectionName":param.get("collectionName")
    }
    url = "https://cloud.piesat.cn/api/v2/dataEngine/featureCollection/queryFeatureByQueryParameter"
    response = POST(url, val)
    if response:
        _data = response.get("data", {}).get("data", [])
        if pieMap:
            fCol = {
                'type': 'FeatureCollection',
                'features': _data
            }
            pieMap.addGeoJsonLayer(fCol, style=style, name=layerName)
    else:
        print(errorMsg)


# def _detectAlgorithm(param, errorMsg, style, coordinates):
#     layerName = param.layerName
#     response = POST(config.getAIDetectURL(), param)
#     if response:
#         _data = response.get("data", {}).get("data", {})
#         _param = _data.get("param", None)
#         _url = _data.get("url", None)
#         _response = POST(_url, _param)
#         if _response:
#             _data = response.get("data", {}).get("data", {})

class PIEAI(PIEObject):
    def __init__(self):
        super(PIEAI, self).__init__()
        self.pre = None
        self.statement = None

    @staticmethod
    def name():
        return "PIEAI"

    @staticmethod
    def roadRecognitionAlgorithm(datasetName, layerName, geometry, style=None, pieMap=None):
        """
        道路识别
        :param datasetName:
        :param layerName:
        :param geometry:
        :param style:
        :param pieMap:
        :return:
        """
        uuid = uuid1()
        _coordinates = None
        if geometry.name() == "PIEGeometry":
            _coordinates = geometry.get("geoJson", {}).get("coordinates", [])
            if len(_coordinates) > 0:
                _coordinates = _coordinates[0]
        elif geometry.name() == "PIEFeature":
            pass
        elif geometry.name() == "PIEFeatureCollection":
            pass
        else:
            _coordinates = geometry
        #TODO:使用固定的区域范围
        polygon = [
            [116.3860, 39.9200],
            [116.3860, 39.9143],
            [116.3956, 39.9143],
            [116.3956, 39.9200],
            [116.3860, 39.9200]
        ]
        param = {
            "datasetName": uuid,
            "detectType": AI_DETECT_TYPE.get("ROADS_BJ", None),
            "layerName": layerName,
            "polygon": polygon,
            "userId": getUserInfo().get("teamId", None),
            "collection": "test_road_ggshp"
        }
        _detectAlgorithm(param, "道路识别失败！", style, _coordinates, pieMap)

    @staticmethod
    def airplaneDetectAlgorithm(datasetName, layerName, geometry, style=None, pieMap=None):
        """
        飞机识别
        :param datasetName:
        :param layerName:
        :param geometry:
        :param style:
        :param pieMap:
        :return:
        """
        uuid = uuid1()
        _coordinates = None
        if geometry.name() == "PIEGeometry":
            _coordinates = geometry.get("geoJson", {}).get("coordinates", [])
            if len(_coordinates) > 0:
                _coordinates = _coordinates[0]
        elif geometry.name() == "PIEFeature":
            pass
        elif geometry.name() == "PIEFeatureCollection":
            pass
        else:
            _coordinates = geometry
        # TODO:使用固定的区域范围
        polygon = [
            [127.7394131, 26.3740513],
            [127.7394131, 26.3369724],
            [127.7929714, 26.3369724],
            [127.7929714, 26.3740513],
            [127.7394131, 26.3740513]
        ]
        param = {
            "datasetName": uuid,
            "detectType": AI_DETECT_TYPE.get("AIR_PLANE", None),
            "layerName": layerName,
            "polygon": polygon,
            "userId": getUserInfo().get("teamId", None),
            "collection": "5c478a1aa49043e58d773869bb2ecac5"
        }
        _detectAlgorithm(param, "飞机识别失败！", style, _coordinates, pieMap)

    @staticmethod
    def ddzdDetectAlgorithm(datasetName, layerName, geometry, style=None, pieMap=None):
        """
        导弹阵地识别
        :param datasetName:
        :param layerName:
        :param geometry:
        :param style:
        :return:
        """
        uuid = uuid1()
        _coordinates = None
        if geometry.name() == "PIEGeometry":
            _coordinates = geometry.get("geoJson", {}).get("coordinates", [])
            if len(_coordinates) > 0:
                _coordinates = _coordinates[0]
        elif geometry.name() == "PIEFeature":
            pass
        elif geometry.name() == "PIEFeatureCollection":
            pass
        else:
            _coordinates = geometry
        # TODO:使用固定的区域范围
        polygon = [
            [135.9983826, 35.3746033],
            [135.9983826, 35.3649902],
            [136.0134888, 35.3649902],
            [136.0134888, 35.3746033],
            [135.9983826, 35.3746033]
        ]
        param = {
            "datasetName": uuid,
            "detectType": AI_DETECT_TYPE.get("DDZD", None),
            "layerName": layerName,
            "polygon": polygon,
            "userId": getUserInfo().get("teamId", None),
            "collection": "d43ec9549cb040f696f746c56b2c9aec"
        }
        _detectAlgorithm(param, "导弹识别失败！", style, _coordinates, pieMap)

    @staticmethod
    def buildDetectAlgorithm(datasetName, layerName, geometry, style=None, pieMap=None):
        """
        建筑识别
        :param datasetName:
        :param layerName:
        :param geometry:
        :param style:
        :return:
        """
        uuid = uuid1()
        _coordinates = None
        if geometry.name() == "PIEGeometry":
            _coordinates = geometry.get("geoJson", {}).get("coordinates", [])
            if len(_coordinates) > 0:
                _coordinates = _coordinates[0]
        elif geometry.name() == "PIEFeature":
            pass
        elif geometry.name() == "PIEFeatureCollection":
            pass
        else:
            _coordinates = geometry
        # TODO:使用固定的区域范围
        polygon = [
            [172.7135930299957, -43.50071905485671],
            [172.7135930299957, -43.50208094724615],
            [172.71600701812136, -43.50208094724615],
            [172.71600701812136, -43.50071905485671],
            [172.7135930299957, -43.50071905485671]
        ]
        param = {
            "datasetName": uuid,
            "detectType": AI_DETECT_TYPE.get("BUILD", None),
            "layerName": layerName,
            "polygon": polygon,
            "userId": getUserInfo().get("teamId", None)
        }
        _detectAlgorithm(param, "建筑识别失败！", style, _coordinates, pieMap)

    @staticmethod
    def greenHouseDetectAlgorithm(datasetName, layerName, geometry, style=None, pieMap=None):
        """
        大棚识别
        :param datasetName:
        :param layerName:
        :param geometry:
        :param style:
        :return:
        """
        uuid = uuid1()
        _coordinates = None
        if geometry.name() == "PIEGeometry":
            _coordinates = geometry.get("geoJson", {}).get("coordinates", [])
            if len(_coordinates) > 0:
                _coordinates = _coordinates[0]
        elif geometry.name() == "PIEFeature":
            pass
        elif geometry.name() == "PIEFeatureCollection":
            pass
        else:
            _coordinates = geometry
        # TODO:使用固定的区域范围
        polygon = [

        ]
        param = {
            "datasetName": uuid,
            "detectType": AI_DETECT_TYPE.get("GREENHOUSE", None),
            "layerName": layerName,
            "polygon": polygon,
            "userId": getUserInfo().get("teamId", None)
        }
        _detectAlgorithm(param, "大棚识别失败！", style, _coordinates, pieMap)

    @staticmethod
    def waterDetectAlgorithm(datasetName, layerName, geometry, style=None, pieMap=None):
        """
        水体识别
        :param datasetName:
        :param layerName:
        :param geometry:
        :param style:
        :return:
        """
        uuid = uuid1()
        _coordinates = None
        if geometry.name() == "PIEGeometry":
            _coordinates = geometry.get("geoJson", {}).get("coordinates", [])
            if len(_coordinates) > 0:
                _coordinates = _coordinates[0]
        elif geometry.name() == "PIEFeature":
            pass
        elif geometry.name() == "PIEFeatureCollection":
            pass
        else:
            _coordinates = geometry
        # TODO:使用固定的区域范围
        polygon = [

        ]
        param = {
            "datasetName": uuid,
            "detectType": AI_DETECT_TYPE.get("WATER", None),
            "layerName": layerName,
            "polygon": polygon,
            "userId": getUserInfo().get("teamId", None)
        }
        _detectAlgorithm(param, "水体识别失败！", style, _coordinates, pieMap)

    @staticmethod
    def solarDetectAlgorithm(datasetName, layerName, geometry, style=None, pieMap=None):
        """
        光伏识别
        :param datasetName:
        :param layerName:
        :param geometry:
        :param style:
        :return:
        """
        uuid = uuid1()
        _coordinates = None
        if geometry.name() == "PIEGeometry":
            _coordinates = geometry.get("geoJson", {}).get("coordinates", [])
            if len(_coordinates) > 0:
                _coordinates = _coordinates[0]
        elif geometry.name() == "PIEFeature":
            pass
        elif geometry.name() == "PIEFeatureCollection":
            pass
        else:
            _coordinates = geometry
        # TODO:使用固定的区域范围
        polygon = [

        ]
        param = {
            "datasetName": uuid,
            "detectType": AI_DETECT_TYPE.get("SOLAR", None),
            "layerName": layerName,
            "polygon": polygon,
            "userId": getUserInfo().get("teamId", None)
        }
        _detectAlgorithm(param, "光伏识别失败！", style, _coordinates, pieMap)


# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   config.py
@Time    :   2020/8/4 下午5:39
@Author  :   lsw
@Version :   1.0
@Contact :   shi_weihappy@126.com
@License :   (C)Copyright 2019-2020, lsw
@Desc    :   None
"""
import os
from configparser import ConfigParser

class Config(object):
    def __init__(self):
        super(Config, self).__init__()
        # 加载配置文件
        cfg = ConfigParser()
        config_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config/config.ini")
        try:
            cfg.read(config_file, encoding="utf-8")
            self._login_url = cfg.get("URL", "login")
            self._print_url = cfg.get("URL", "print")
            self._compute_url = cfg.get("URL", "compute")
            self._wmts_tiles_url = cfg.get("URL", "wmts_tiles")
            self._image_tiles_url = cfg.get("URL", "image_tiles")
            self._vector_tiles_url = cfg.get("URL", "vector_tiles")
            self._check_url = cfg.get("URL", "check")
            self._refresh_url = cfg.get("URL", "refresh")
            self._layer_url = cfg.get("URL", "layer")
            self._map_url = cfg.get("URL", "map")
            self._export_image_url = cfg.get("URL", "export_image")
            self._export_vector_url = cfg.get("URL", "export_vector")
            self._ai_detect_url = cfg.get("URL", "ai_detect")
            self._geo_url = cfg.get("URL", "tdt_geo")
            self._regeo_url = cfg.get("URL", "tdt_regeo")
            self.fuzzy_query_url = cfg.get("URL", "fuzzy_query")
            self.query_catalog_url = cfg.get("URL", "query_catalog")
            self.insert_catalog_url = cfg.get("URL", "insert_catalog")
            self.save_share_code_url = cfg.get("URL", "save_share_code")
            self.user_resource_storage_url = cfg.get("URL", "user_resource_storage")
            self.user_resource_uri_url = cfg.get("URL", "user_resource_uri")
            self.task_list_url = cfg.get("URL", "task_list")
            self.task_detail_url = cfg.get("URL", "task_detail")
            self.cancel_task_url = cfg.get("URL", "cancel_task")
            self.clear_task_url = cfg.get("URL", "clear_task")

            self._login_x_api = cfg.get("X-API", "login")
            self._print_x_api = cfg.get("X-API", "print")
            self._compute_x_api = cfg.get("X-API", "compute")
            self._wmts_tiles_x_api = cfg.get("X-API", "wmts_tiles")
            self._image_tiles_x_api = cfg.get("X-API", "image_tiles")
            self._vector_tiles_x_api = cfg.get("X-API", "vector_tiles")
            self._check_x_api = cfg.get("X-API", "check")
            self._refresh_x_api = cfg.get("X-API", "refresh")
            self._layer_x_api = cfg.get("X-API", "layer")
            self._map_x_api = cfg.get("X-API", "map")
            self._export_image_x_api = cfg.get("X-API", "export_image")
            self._export_vector_x_api = cfg.get("X-API", "export_vector")
            self._geo_x_api = cfg.get("X-API", "tdt_geo")
            self._regeo_x_api = cfg.get("X-API", "tdt_regeo")
            self.fuzzy_query_x_api = cfg.get("X-API", "fuzzy_query")
            self.query_catalog_x_api = cfg.get("X-API", "query_catalog")
            self.insert_catalog_x_api = cfg.get("X-API", "insert_catalog")
            self.save_share_code_x_api = cfg.get("X-API", "save_share_code")
            self.user_resource_storage_api = cfg.get("X-API", "user_resource_storage")
            self.user_resource_uri_api = cfg.get("X-API", "user_resource_uri")
            self.task_list_api = cfg.get("X-API", "task_list")
            self.task_detail_api = cfg.get("X-API", "task_detail")
            self.cancel_task_api = cfg.get("X-API", "cancel_task")
            self.clear_task_api = cfg.get("X-API", "clear_task")

            _home_path = os.path.expanduser('~')
            _pie_path = os.path.join(_home_path, ".pie")
            self._credentials_file = os.path.join(_pie_path, cfg.get("LOGIN", "credentials")) # HOME
            self._user_file = os.path.join(_pie_path, cfg.get("LOGIN", "user"))
        except Exception as e:
            print("load config file fail! error is: {}".format(e))

    def getGeoURL(self):
        return {
            "url": self._geo_url,
            "x-api": self._geo_x_api
        }

    def getReGeoUrl(self):
        return {
            "url": self._regeo_url,
            "x-api": self._regeo_x_api
        }

    def getLoginURL(self):
        return {
            "url": self._login_url,
            "x-api": self._login_x_api
        }

    def getCheckURL(self):
        return {
            "url": self._check_url,
            "x-api": self._check_x_api
        }

    def getRefreshURL(self):
        return {
            "url": self._refresh_url,
            "x-api": self._refresh_x_api
        }

    def getPrintURL(self):
        return {
            "url": self._print_url,
            "x-api": self._print_x_api
        }

    def getComputeURL(self):
        return {
            "url": self._compute_url,
            "x-api": self._compute_x_api
        }

    def getLayerURL(self):
        return {
            "url": self._layer_url,
            "x-api": self._layer_x_api
        }

    def getMapURL(self):
        return {
            "url": self._map_url,
            "x-api": self._map_x_api
        }

    def getWMTSTilesURL(self, tiles):
        return {
            "url": self._wmts_tiles_url.format(tiles=tiles, x="{x}", y="{y}", z="{z}"),
            "x-api": self._wmts_tiles_x_api
        }

    def getImageTilesURL(self, tiles):
        return {
            "url": self._image_tiles_url.format(tiles=tiles, x="{x}", y="{y}", z="{z}"),
            "x-api": self._image_tiles_x_api
        }

    def getVectorTilesURL(self, tiles):
        return {
            "url": self._vector_tiles_url.format(tiles=tiles, x="{x}", y="{y}", z="{z}"),
            "x-api": self._vector_tiles_x_api
        }
    # def getVectorTilesURL(self, tiles, token):
    #     return {
    #         "url": self._vector_tiles_url.format(tiles=tiles, token=token,x="{x}", y="{y}", z="{z}"),
    #         "x-api": self._vector_tiles_x_api
    #     }

    def getCredentialsFile(self):
        return self._credentials_file

    def getUserFile(self):
        return self._user_file

    def getExportImageURL(self):
        return {
            "url": self._export_image_url,
            "x-api": self._export_image_x_api
        }

    def getExportVectorURL(self):
        return {
            "url": self._export_vector_url,
            "x-api": self._export_vector_x_api
        }

    def getFuzzyQuery(self):
        return {
            "url": self.fuzzy_query_url,
            "x-api": self.fuzzy_query_x_api
        }

    def getQueryCatalogURL(self):
        return {
            "url": self.query_catalog_url,
            "x-api": self.query_catalog_x_api
        }

    def insertCatalogURL(self):
        return {
            "url": self.insert_catalog_url,
            "x-api": self.insert_catalog_x_api
        }

    def getSaveShareCode(self):
        return {
            "url": self.save_share_code_url,
            "x-api": self.save_share_code_x_api
        }

    def getUserResourceStorageURL(self):
        return {
            "url": self.user_resource_storage_url,
            "x-api": self.user_resource_storage_api
        }

    def getUserResourceUriURL(self):
        return {
            "url": self.user_resource_uri_url,
            "x-api": self.user_resource_uri_api
        }

    def getTaskListURL(self):
        return {
            "url": self.task_list_url,
            "x-api": self.task_list_api
        }

    def getTaskDetailURL(self):
        return {
            "url": self.task_detail_url,
            "x-api": self.task_detail_api
        }

    def getCancelTaskURL(self):
        return {
            "url": self.cancel_task_url,
            "x-api": self.cancel_task_api
        }

    def getClearTaskURL(self):
        return {
            "url": self.clear_task_url,
            "x-api": self.clear_task_api
        }

config = Config()
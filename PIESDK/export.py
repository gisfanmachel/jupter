# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   export.py
@Time    :   2020/8/6 下午2:57
@Author  :   lsw
@Version :   1.0
@Contact :   shi_weihappy@126.com
@License :   (C)Copyright 2019-2020, lsw
@Desc    :   None
"""

from pie.object import PIEObject
from pie.utils.config import config
from pie.utils.common import encodeURIComponent, encodeJSON
from pie.utils.pieHttp import POST
from pie.utils.resourceTools import insertNewFolder, checkStorageFileIsExist
from pie.utils.error import ArgsIsNull, FileIsExist

class PIEExport(PIEObject):
    def __init__(self):
        super(PIEExport, self).__init__()
        self.pre = None
        self.statement = None

    @staticmethod
    def name():
        return "PIEExport"

    def _imageToAsset(self, **kwargs):
        """
        导出影像
        :param kwargs:
            image,
            description,
            assetId,
            pyramidingPolicy,
            dimensions,
            region,
            scale,
            crs,
            crsTransform,
            maxPixels
        :return:
        """
        image = kwargs.get("image", None)
        description = kwargs.get("description", "")
        assetId = kwargs.get("assetId", "")
        pyramidingPolicy = kwargs.get("pyramidingPolicy", "")
        dimensions = kwargs.get("dimensions", [1024, 1024])
        region = kwargs.get("region", "")
        scale = kwargs.get("scale", 1000)
        crs = kwargs.get("crs", "")
        crsTransform = kwargs.get("crsTransform", "")
        maxPixels = kwargs.get("maxPixels", 1e13)
        if not image:
            raise ArgsIsNull("image")
        if not region:
            raise ArgsIsNull("region")
        if not assetId:
            raise ArgsIsNull("assetId")
        if not description:
            raise ArgsIsNull("description")

        if checkStorageFileIsExist(assetId):
            raise FileIsExist(assetId)

        asset_paths = assetId.split("/")
        asset_name = asset_paths[len(asset_paths) - 1]
        parentId = "0"
        if len(asset_paths) > 1:
            asset_paths = asset_paths[:len(asset_paths) - 1]
            parentId = insertNewFolder("/".join(asset_paths))
        self.statement = self.getStatement(
            functionName="Export.image",
            arguments={
                "image": self.formatValue(image),
                "description": description,
                "assetId": assetId,
                "pyramidingPolicy": pyramidingPolicy,
                "dimensions": dimensions,
                "region": self.formatValue(region),
                "scale": scale,
                "crs": crs,
                "crsTransform": crsTransform,
                "maxPixels": maxPixels
            },
        )
        _url = config.getExportImageURL()
        statement = encodeJSON(self.statement)
        statement = encodeURIComponent(statement)
        _params = {
            "parentId": parentId,
            "name": asset_name,
            "description": description,
            "statement": statement,
            "suffixName": "geojson",
            "code": "",
            "isDownload": False
        }
        response = POST(urlInfo=_url, params=_params)
        return response

    def _imageToCloud(self, **kwargs):
        """
        导出影像
        :param kwargs:
            image,
            description,
            assetId,
            pyramidingPolicy,
            dimensions,
            region,
            scale,
            crs,
            crsTransform,
            maxPixels
        :return:
        """
        image = kwargs.get("image", None)
        description = kwargs.get("description", "")
        assetId = kwargs.get("assetId", "")
        pyramidingPolicy = kwargs.get("pyramidingPolicy", "")
        dimensions = kwargs.get("dimensions", [1024, 1024])
        region = kwargs.get("region", "")
        scale = kwargs.get("scale", 1000)
        crs = kwargs.get("crs", "")
        crsTransform = kwargs.get("crsTransform", "")
        maxPixels = kwargs.get("maxPixels", 1e13)
        if not image:
            raise ArgsIsNull("image")
        if not region:
            raise ArgsIsNull("region")
        if not assetId:
            raise ArgsIsNull("assetId")
        if not description:
            raise ArgsIsNull("description")

        if checkStorageFileIsExist(assetId):
            raise FileIsExist(assetId)

        asset_paths = assetId.split("/")
        asset_name = asset_paths[len(asset_paths) - 1]
        parentId = "0"
        if len(asset_paths) > 1:
            asset_paths = asset_paths[:len(asset_paths) - 1]
            parentId = insertNewFolder("/".join(asset_paths))

        self.statement = self.getStatement(
            functionName="Export.image",
            arguments={
                "image": self.formatValue(image),
                "description": description,
                "assetId": assetId,
                "pyramidingPolicy": pyramidingPolicy,
                "dimensions": dimensions,
                "region": self.formatValue(region),
                "scale": scale,
                "crs": crs,
                "crsTransform": crsTransform,
                "maxPixels": maxPixels
            },
        )
        _url = config.getExportImageURL()
        statement = encodeJSON(self.statement)
        statement = encodeURIComponent(statement)
        _params = {
            "parentId": parentId,
            "name": asset_name,
            "description": description,
            "statement": statement,
            "suffixName": "geojson",
            "code": "",
            "isDownload": True
        }
        response = POST(urlInfo=_url, params=_params)
        return response

    def table(self, **kwargs):
        """
        导出矢量数据
        :param kwargs:
        :return:
        """
        collection = kwargs.get("collection", None)
        description = kwargs.get("description", None)
        assetId = kwargs.get("assetId", None)
        params = kwargs.get("params", None)
        if not collection:
            raise ArgsIsNull("collection")
        if not assetId:
            raise ArgsIsNull("assetId")
        if not description:
            raise ArgsIsNull("description")

        if checkStorageFileIsExist(assetId):
            raise FileIsExist(assetId)

        asset_paths = assetId.split("/")
        asset_name = asset_paths[len(asset_paths) - 1]
        parentId = "0"
        if len(asset_paths) > 1:
            asset_paths = asset_paths[:len(asset_paths) - 1]
            parentId = insertNewFolder("/".join(asset_paths))

        self.statement = self.getStatement(
            functionName="Export.table",
            arguments={
                "collection": self.formatValue(collection),
                "description": description,
                "assetId": assetId,
                "params": params,
            },
        )
        _url = config.getExportVectorURL()
        statement = encodeJSON(self.statement)
        statement = encodeURIComponent(statement)
        _params = {
            "parentId": parentId,
            "name": asset_name,
            "description":description,
            "statement":statement,
            "suffixName":"geojson",
            "code": "",
            "isDownload": False
        }
        response = POST(urlInfo=_url, params=_params)
        return response

    @staticmethod
    def Table(**kwargs):
        return PIEExport().table(**kwargs)

    @staticmethod
    def Image(**kwargs):
        return PIEExport()._imageToAsset(**kwargs)

    @staticmethod
    def imageToAssets(**kwargs):
        return PIEExport()._imageToAsset(**kwargs)

    @staticmethod
    def imageToCloud(**kwargs):
        return PIEExport()._imageToCloud(**kwargs)



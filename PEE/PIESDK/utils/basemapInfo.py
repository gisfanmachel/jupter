# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   basemapInfo.py
@Time    :   2022/7/27 17:03
@Author  :   lishiwei
@Version :   1.0
@Contact :   shi_weihappy@126.com
@License :   (C)Copyright 2021-2022, lishiwei
@Desc    :   None
"""
import ipyleaflet
import folium

xyz_tiles = {
    "GaodeVec": {
        "url": "https://webrd01.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}",
        "attribution": "高德地图",
        "name": "高德地图",
    },
    "GaodeImg": {
        "url": "https://webst04.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}",
        "attribution": "高德影像",
        "name": "高德影像",
    }
}

def leaflet_basemap(url=None, name="自定义地图", attribution="自定义地图"):
    if url is None:
        leaflet_dict = {}
        for key, tile in xyz_tiles.items():
            name = tile["name"]
            url = tile["url"]
            attribution = tile["attribution"]
            leaflet_dict[key] = ipyleaflet.TileLayer(
                url=url,
                name=name,
                attribution=attribution,
                max_zoom=22
            )
        return leaflet_dict
    else:
        if not name:
            name = "自定义地图"
        if not attribution:
            attribution = "自定义地图"
        return ipyleaflet.TileLayer(
            url=url,
            name=name,
            attribution=attribution,
            max_zoom=22
        )

def folium_basemap(url=None, name="自定义地图", attribution="自定义地图"):
    if url is None:
        folium_dict = {}
        for key, tile in xyz_tiles.items():
            name = tile["name"]
            url = tile["url"]
            attribution = tile["attribution"]
            folium_dict[key] = folium.TileLayer(
                tiles=url,
                name=name,
                attr=attribution,
                max_zoom=22
            )
        return folium_dict
    else:
        if not name:
            name = "自定义地图"
        if not attribution:
            attribution = "自定义地图"
        return folium.TileLayer(
            tiles=url,
            name=name,
            attr=attribution,
            max_zoom=22
        )

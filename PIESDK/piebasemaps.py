# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   piebasemaps.py
@Time    :   2020/8/6 下午5:19
@Author  :   liuxiaodong
@Version :   1.0
@Contact :   2152550864@qq.com
@License :   (C)Copyright 2019-2020, liuxiaodong
@Desc    :   None
"""
from ipyleaflet import TileLayer, WMSLayer, basemaps, basemap_to_tiles

pie_basemaps = {
    'Gaode': TileLayer(
        url="https://webst04.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}",
        attribution='高德地图',
        name='GaoDe Maps'
    ),
    'TDT': TileLayer(
        url="http://t1.tianditu.gov.cn/img_w/wmts?tk=1e5a8aeb87fbf336c3d7780f91b7fdfc&SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=img&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}",
        attribution='天地图',
        name='TianDiTu Maps'
    ),
    'TDT_ibo': TileLayer(
        url='http://t0.tianditu.gov.cn/ibo_w/wmts?tk=1e5a8aeb87fbf336c3d7780f91b7fdfc&SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=ibo&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}',
        attribution='天地图边界',
        name='TianDiTu Bounds'

    ),
    'TDT_cia': TileLayer(
        url='http://t0.tianditu.gov.cn/cia_w/wmts?tk=1e5a8aeb87fbf336c3d7780f91b7fdfc&SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=cia&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}',
        attribution='天地图路网',
        name='TianDiTu Road'
    )

}


# Adds ipyleaflet basemaps
for item in basemaps.values():
    try:
        name = item['name']
        basemap = 'basemaps.{}'.format(name)
        pie_basemaps[name] = basemap_to_tiles(eval(basemap))
    except:
        for sub_item in item:
            name = item[sub_item]['name']
            basemap = 'basemaps.{}'.format(name)
            basemap = basemap.replace('Mids', 'Modis')
            pie_basemaps[name] = basemap_to_tiles(eval(basemap))

# -*- coding:utf-8 -*-
"""
@Project :   PyCharm
@File    :   foliumTileLayer.py
@Time    :   2021/4/18 18:28 下午
@Author  :   lsw
@Version :   1.0
@Contact :   shi_weihappy@126.com
@License :   (C)Copyright 2019-2020, lsw
@Desc    :   None
"""
from folium import GeoJson

from pie.utils.common import encodeJSON, encodeURIComponent
from pie.utils.config import config
from pie.utils.pieHttp import POST, getCredentials, getHeaders
from pie.vector.featureCollection import PIEFeatureCollection
from pie.vector.geometry import PIEGeometry
from pie.image.image import PIEImage
from pie.vector.feature import PIEFeature
from pie.image.imageCollection import PIEImageCollection
from pie.map.foliumPIERasterTileLayer import PIERasterTileLayer
from pie.map.foliumPIEVectorTileLayer import PIEVectorTileLayer

def generateVectorTileLayer(pieObject, style, name, visible, opacity):
    """
    生成矢量瓦片
    :param pieObject:
    :param style:
    :param name:
    :param visible:
    :param opacity:
    :return:
    """
    _opacity = opacity
    if style:
        if "opacity" in style:
            _opacity = style.get("opacity")
    else:
        style = {}
    style['opacity'] = _opacity
    statement = encodeURIComponent(encodeJSON(pieObject.statement))
    render_style = encodeURIComponent(encodeJSON(style))
    params = {
        "statement": statement,
        "style": render_style,
        "type": "vector"
    }
    _mapUrl = config.getMapURL()
    response = POST(_mapUrl, params)
    if response:
        _data = response.get("data", {})
        _id = _data.get("id")
        _url = _data.get("url")
        kwargs = {
            "url": config.getVectorTilesURL(_url).get("url"),
            "name": name
        }
        _color = style.get("color", "blue")
        _fillColor = style.get("fillColor", "blue")
        point_style = dict(
            weight=2,
            color=_color,
            opacity=_opacity,
            fillColor= _fillColor,
            fill=True,
            radius= 4,
            fillOpacity= _opacity
        )
        line_style = dict(
            weight=1,
            opacity=_opacity,
            color= _color,
            fillColor= _fillColor,
            fillOpacity= 0
        )
        polygon_style = dict(
            weight= 1,
            fillColor= _fillColor,
            color= _color,
            fill= True,
            fillOpacity= 0.2,
            opacity= _opacity
        )
        # vector_tile_layer_styles = dict(
        #     point=point_style,
        #     line=line_style,
        #     polygon=polygon_style
        # )
        layer_name = kwargs.get("name")
        vector_tile_layer_styles = dict(
            interactive = True,
            maxNativeZoom = 6,
            vectorTileLayerStyles = {layer_name: polygon_style}
        )
        tilelayer = PIEVectorTileLayer(
            url=kwargs.get("url"),
            name=kwargs.get("name"),
            show=visible,
            options=vector_tile_layer_styles
        )
        return tilelayer
    else:
        return None

def generateImageLayer(pieObject, style, name, visible, opacity):
    """
    生成image
    @param pieObject:the PIEImage or PIEImageCollection
    @param style:the style of show in the map
    @param name:layer name
    @param visible:True or False
    @param opacity
    @return:
    """
    _opacity = opacity
    if style:
        if "opacity" in style:
            _opacity = style.get("opacity")
    else:
        style = {}
    style['opacity'] = _opacity
    statement = encodeURIComponent(encodeJSON(pieObject.statement))
    render_style = encodeURIComponent(encodeJSON(style))
    params = {
        "statement": statement,
        "style": render_style,
        "type": "raster"
    }
    _mapUrl = config.getMapURL()
    response = POST(_mapUrl, params)
    if response:
        _data = response.get("data", {})
        _id = _data.get("id")
        _url = _data.get("url")
        url = config.getImageTilesURL(_url).get("url")
        headers = getHeaders(config.getImageTilesURL(_url).get("x-api"), getCredentials())
        tilelayer = PIERasterTileLayer(
            url=url,
            name=name,
            show=visible,
            options={
                "headers": headers
            }
        )
        return tilelayer
    else:
        return None

def generateImageCollectionLayer(pieObject, style, name, visible, opacity):
    """
    生成imageCollection的图层
    :param pieObject:
    :param style:
    :param name:
    :param visible:
    :param opacity:
    :return:
    """
    image = pieObject.mosaic()
    return generateImageLayer(image, style, name, visible, opacity)

def generateGeometryLayer(pieObject, style, name, visible, opacity):
    """
    生成geometry对应的图层
    :param pieObject:
    :param style:
    :param name:
    :param visible:
    :param opacity:
    :return:
    """
    geom = pieObject.getInfo()
    fCol = {
        "type": 'FeatureCollection',
        "features": [{
            "type": "Feature",
            "geometry": geom
        }]
    }
    return generateGeoJSONLayer(fCol, style, name, visible, opacity)

def generateFeatureLayer(pieObject, style, name, visible, opacity):
    """
    生成feature对应的图层
    :param pieObject:
    :param style:
    :param name:
    :param visible:
    :param opacity:
    :return:
    """
    properties = pieObject.getInfo().get("properties")
    geom = pieObject.geometry().getInfo()
    fCol = {
        "type": 'FeatureCollection',
        "features": [{
            "type": "Feature",
            "geometry": geom,
            "properties": properties
        }]
    }
    return generateGeoJSONLayer(fCol, style, name, visible, opacity)

def generateFeatureCollectionLayer(pieObject, style, name, visible, opacity):
    """
    生成featureCollection对应的图层
    :param pieObject:
    :param style:
    :param name:
    :param visible:
    :param opacity:
    :return:
    """
    elements = pieObject.getInfo().get("elements", [])
    geometries = pieObject.geometries().getInfo()
    features = []
    for i in range(len(geometries)):
        if i < len(elements):
            properties = elements[i].get("properties")
        else:
            properties = {}

        obj = {
            "type": "Feature",
            "geometry": geometries[i],
            "properties": properties
        }
        features.append(obj)
    fCol = {
        "type": 'FeatureCollection',
        "features": features
    }
    return generateGeoJSONLayer(fCol, style, name, visible, opacity)

def generateGeoJSONLayer(data, style, name, visible, opacity=1):
    """
    生成GeoJSON图层
    :param data:
    :param style:
    :param name:
    :param visible:
    :param opacity:
    :return:
    """
    _color = style.get("color", "blue")
    _fillColor = style.get("fillColor", "orange")
    geo_json = GeoJson(
        data=data,
        style_function=lambda feature: {
            'opacity': opacity,
            'fillOpacity': 0.8,
            'weight': 1,
            'color': _color,
            'fillColor': _fillColor
        },
        highlight_function=lambda feature: {
            'color': 'red',
            'fillOpacity': 0.5
        },
        name=name,
        show=visible
    )
    return geo_json

def generateTileLayer(pieObject, style, name, visible, opacity):
    if isinstance(pieObject, PIEImage):
        _mapTypeId = style.get("type", 1)
        if _mapTypeId == 1:
            tileLayer = generateImageLayer(
                pieObject=pieObject,
                style=style,
                name=name,
                visible=visible,
                opacity=opacity
            )
        elif _mapTypeId == 2:
            tileLayer = generateVectorTileLayer(
                pieObject=pieObject,
                style=style,
                name=name,
                visible=visible,
                opacity=opacity
            )
        else:
            tileLayer = generateImageLayer(
                pieObject=pieObject,
                style=style,
                name=name,
                visible=visible,
                opacity=opacity
            )
    elif isinstance(pieObject, PIEImageCollection):
        tileLayer = generateImageCollectionLayer(
            pieObject=pieObject,
            style=style,
            name=name,
            visible=visible,
            opacity=opacity
        )
    elif isinstance(pieObject, PIEGeometry):
        tileLayer = generateGeometryLayer(
            pieObject=pieObject,
            style=style,
            name=name,
            visible=visible,
            opacity=opacity
        )
    elif isinstance(pieObject, PIEFeature):
        tileLayer = generateFeatureLayer(
            pieObject=pieObject,
            style=style,
            name=name,
            visible=visible,
            opacity=opacity
        )
    elif isinstance(pieObject, PIEFeatureCollection):
        tileLayer = generateFeatureCollectionLayer(
            pieObject=pieObject,
            style=style,
            name=name,
            visible=visible,
            opacity=opacity
        )
    else:
        print("The pieObject must be the follows object: PIEImage, PIEImageCollection, PIEGeometry, PIEFeature, PIEFeatureCollection")
        tileLayer = None
    return tileLayer
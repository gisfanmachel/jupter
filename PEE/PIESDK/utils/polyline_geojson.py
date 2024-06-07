# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   polyline_geojson.py
@Time    :   2021/1/28 下午4:24
@Author  :   lsw
@Version :   1.0
@Contact :   shi_weihappy@126.com
@License :   (C)Copyright 2019-2020, lsw
@Desc    :   None
解析
"""
from itertools import chain
from math import floor, ceil
from operator import sub

DEFAULT_PRECISION = 1e6

def polyline_round(number):
    """
    Return the given number rounded to nearest integer.
    >>> polyline_round(0.5)
    1
    >>> polyline_round(-0.5)
    -1
    Note:
        The rounding behaviour is "always round up 0.5". This is not
        generally considered the standard way of rounding numbers now
        (Python 3 does it differently, for example). But it is what
        Python 2 does by default and it is, not coincidentally, what the
        Encoded Polyline Algorithm requires.

    Args:
        number (float): value to round to nearest integer

    Returns:
        int
    """
    if number > 0:
        return floor(number + 0.5)
    else:
        return ceil(number - 0.5)

def encode_coord(coord, precision):
    coord = polyline_round(coord * precision) << 1  # Steps 1–4.
    if coord < 0:
        coord = ~coord  # Step 5.
    encoded_coord = ""
    while coord >= 0x20:
        encoded_coord += chr((0x20 | (coord & 0x1F)) + 63)  # Steps 8–10.
        coord >>= 5
    encoded_coord += chr(coord + 63)  # Steps 9–10.
    return encoded_coord

def encode(locations, precision=None):
    if precision is None:
        precision = DEFAULT_PRECISION
    else:
        precision = 10 ** precision
    encoded_coords = []
    prev_location = (0, 0)
    for location in locations:
        encoded_coords.append(
            encode_coord(p, precision)
            for p in map(sub, location, prev_location)
        )
        prev_location = location
    return "".join(chain(*encoded_coords))

def decode_coords(polyline):
    coord = 0
    shift = 0
    for char in map(ord, polyline):
        char -= 63
        coord |= (char & 0x1F) << shift
        shift += 5
        if char < 0x20:
            if coord & 1:
                yield ~coord >> 1
            else:
                yield coord >> 1
            coord = 0
            shift = 0

def decode(polyline, precision=None):
    if precision is None:
        precision = DEFAULT_PRECISION
    else:
        precision = 10 ** precision
    prev_location = [0, 0]
    i = decode_coords(polyline)
    for coord in i:
        location = [coord + prev_location[0], next(i) + prev_location[1]]
        # 将经纬度翻转
        result = [p/ precision for p in location]
        result.reverse()
        yield result
        prev_location = location

def decodeGeoJSON(geojson, options=None):
    if options is None:
        options = {}
    precision = options.get("precision", 6)
    _type = geojson.get("type")
    if _type == "Point":
        _coordinates = geojson.get("coordinates")
        if not isinstance(_coordinates, str):
            return geojson
        return {
            "coordinates": list(decode(_coordinates, precision))[0],
            "type": _type
        }
    elif _type == "MultiPoint" or _type == "LineString":
        _coordinates = geojson.get("coordinates")
        if not isinstance(_coordinates, str):
            return geojson
        return {
            "coordinates": list(decode(_coordinates, precision)),
            "type": _type
        }
    elif _type == "MultiLineString" or _type == "Polygon":
        _coordinates = geojson.get("coordinates")
        for d in _coordinates:
            if not isinstance(d, str):
                return geojson
        return {
            "coordinates": list(map(lambda _coord:list(decode(_coord, precision)), _coordinates)),
            "type": _type
        }
    elif _type == "MultiPolygon":
        _coordinates = geojson.get("coordinates")
        for polygons in _coordinates:
            for d in polygons:
                if not isinstance(d, str):
                    return geojson
        return {
            "coordinates": list(map(lambda p: list(map(lambda coords: list(decode(coords, precision)), p)), _coordinates)),
            "type": _type
        }
    elif _type == "feature":
        return {
            "geometry": decodeGeoJSON(geojson.get("geometry"), options)
        }
    elif _type == "FeatureCollection":
        _features = geojson.get("features", [])
        return {
            "features": list(map(lambda feature: decodeGeoJSON(feature, options), _features))
        }
    elif _type == "GeometryCollection":
        _geometries = geojson.get("geometries", [])
        return {
            "geometries": list(map(lambda geometry: decodeGeoJSON(geometry, options), _geometries))
        }
    else:
        return geojson

def encodeGeoJSON(geojson, options=None):
    if options is None:
        options = {}
    precision = options.get("precision", 6)
    _type = geojson.get("type")
    if _type == "Point":
        _coordinates = geojson.get("coordinates")
        return {
            "coordinates": encode([_coordinates], precision),
            "type": _type
        }
    elif _type == "MultiPoint" or _type == "LineString":
        _coordinates = geojson.get("coordinates")
        return {
            "coordinates": encode(_coordinates, precision),
            "type": _type
        }
    elif _type == "MultiLineString" or _type == "Polygon":
        _coordinates = geojson.get("coordinates")
        return {
            "coordinates": list(map(lambda _coord: encode(_coord, precision), _coordinates)),
            "type": _type
        }
    elif _type == "MultiPolygon":
        _coordinates = geojson.get("coordinates")
        return {
            "coordinates": list(map(lambda p: list(map(lambda coords: encode(coords, precision), p)), _coordinates)),
            "type": _type
        }
    elif _type == "feature":
        return {
            "geometry": encodeGeoJSON(geojson.get("geometry"), options)
        }
    elif _type == "FeatureCollection":
        _features = geojson.get("features", [])
        return {
            "features": list(map(lambda feature: encodeGeoJSON(feature, options), _features))
        }
    elif _type == "GeometryCollection":
        _geometries = geojson.get("geometries", [])
        return {
            "geometries": list(map(lambda geometry: encodeGeoJSON(geometry, options), _geometries))
        }
    else:
        return geojson


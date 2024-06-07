# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/threeddesigner.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 707 bytes
try:
    from . import _jsuperpy as supermap
except ImportError as e:
    try:
        from . import _csuperpy as supermap
    finally:
        e = None
        del e

Material3D = supermap.Material3D
linear_extrude = supermap.linear_extrude
build_house = supermap.build_house
compose_models = supermap.compose_models
building_height_check = supermap.building_height_check
BoolOperation3D = supermap.BoolOperation3D
ModelBuilder3D = supermap.ModelBuilder3D
ClassificationOperator = supermap.ClassificationOperator
ClassificationInfos = supermap.ClassificationInfos
__all__ = [
 'linear_extrude', 'build_house', 'compose_models', 'Material3D', 'building_height_check', 
 'BoolOperation3D', 
 'ModelBuilder3D', 'ClassificationOperator', 'ClassificationInfos']

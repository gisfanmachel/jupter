# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/mapping.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 2908 bytes
try:
    from . import _jsuperpy as supermap
except ImportError as e:
    try:
        from . import _csuperpy as supermap
    finally:
        e = None
        del e

Map = supermap.Map
LayerSetting = supermap.LayerSetting
LayerSettingImage = supermap.LayerSettingImage
LayerSettingVector = supermap.LayerSettingVector
LayerSettingGrid = supermap.LayerSettingGrid
Layer = supermap.Layer
TrackingLayer = supermap.TrackingLayer
LayerHeatmap = supermap.LayerHeatmap
LayerGridAggregation = supermap.LayerGridAggregation
ThemeType = supermap.ThemeType
Theme = supermap.Theme
ThemeUniqueItem = supermap.ThemeUniqueItem
ThemeUnique = supermap.ThemeUnique
ThemeRangeItem = supermap.ThemeRangeItem
RangeMode = supermap.RangeMode
ThemeRange = supermap.ThemeRange
MixedTextStyle = supermap.MixedTextStyle
LabelMatrix = supermap.LabelMatrix
LabelMatrixImageCell = supermap.LabelMatrixImageCell
LabelMatrixSymbolCell = supermap.LabelMatrixSymbolCell
LabelBackShape = supermap.LabelBackShape
AvoidMode = supermap.LabelBackShape
AlongLineCulture = supermap.AlongLineCulture
AlongLineDirection = supermap.AlongLineDirection
AlongLineDrawingMode = supermap.AlongLineDrawingMode
OverLengthLabelMode = supermap.OverLengthLabelMode
ThemeLabelRangeItem = supermap.ThemeLabelRangeItem
ThemeLabelRangeItems = supermap.ThemeLabelRangeItems
ThemeLabelUniqueItem = supermap.ThemeLabelUniqueItem
ThemeLabelUniqueItems = supermap.ThemeLabelUniqueItems
ThemeLabel = supermap.ThemeLabel
ThemeGraphItem = supermap.ThemeGraphItem
ThemeGraphType = supermap.ThemeGraphType
ThemeGraphTextFormat = supermap.ThemeGraphTextFormat
GraphAxesTextDisplayMode = supermap.GraphAxesTextDisplayMode
ThemeGraph = supermap.ThemeGraph
GraduatedMode = supermap.GraduatedMode
ThemeGraduatedSymbol = supermap.ThemeGraduatedSymbol
ThemeDotDensity = supermap.ThemeDotDensity
ThemeGridUniqueItem = supermap.ThemeGridUniqueItem
ThemeGridUnique = supermap.ThemeGridUnique
ThemeGridRangeItem = supermap.ThemeGridRangeItem
ThemeGridRange = supermap.ThemeGridRange
ThemeCustom = supermap.ThemeCustom
__all__ = [
 'Map', 'LayerSetting', 'LayerSettingImage', 'LayerSettingVector', 'LayerSettingGrid', 
 'TrackingLayer', 
 'Layer', 'LayerHeatmap', 'LayerGridAggregation', 'ThemeType', 
 'Theme', 'ThemeUniqueItem', 'ThemeUnique', 
 'ThemeRangeItem', 'RangeMode', 
 'ThemeRange', 
 'MixedTextStyle', 'LabelMatrix', 'LabelMatrixImageCell', 
 'LabelMatrixSymbolCell', 'LabelBackShape', 
 'AvoidMode', 'AlongLineCulture', 
 'AlongLineDirection', 'AlongLineDrawingMode', 
 'OverLengthLabelMode', 'ThemeLabelRangeItem', 
 'ThemeLabelRangeItems', 'ThemeLabelUniqueItem', 
 'ThemeLabelUniqueItems', 
 'ThemeLabel', 'ThemeGraphItem', 'ThemeGraphType', 'ThemeGraphTextFormat', 
 'GraphAxesTextDisplayMode', 
 'ThemeGraph', 'GraduatedMode', 'ThemeGraduatedSymbol', 'ThemeDotDensity', 
 'ThemeGridUniqueItem', 
 'ThemeGridUnique', 'ThemeGridRangeItem', 'ThemeGridRange', 'ThemeCustom']

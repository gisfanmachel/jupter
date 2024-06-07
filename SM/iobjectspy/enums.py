# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/enums.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 6167 bytes
try:
    from . import _jsuperpy as supermap
except ImportError as e:
    try:
        from . import _csuperpy as supermap
    finally:
        e = None
        del e

PixelFormat = supermap.PixelFormat
BlockSizeOption = supermap.BlockSizeOption
AreaUnit = supermap.AreaUnit
Unit = supermap.Unit
EngineType = supermap.EngineType
DatasetType = supermap.DatasetType
FieldType = supermap.FieldType
GeometryType = supermap.GeometryType
WorkspaceType = supermap.WorkspaceType
WorkspaceVersion = supermap.WorkspaceVersion
EncodeType = supermap.EncodeType
CursorType = supermap.CursorType
Charset = supermap.Charset
OverlayMode = supermap.OverlayMode
SpatialIndexType = supermap.SpatialIndexType
DissolveType = supermap.DissolveType
TextAlignment = supermap.TextAlignment
StringAlignment = supermap.StringAlignment
ColorGradientType = supermap.ColorGradientType
SpatialQueryMode = supermap.SpatialQueryMode
StatisticsType = supermap.StatisticsType
JoinType = supermap.JoinType
BufferEndType = supermap.BufferEndType
BufferRadiusUnit = supermap.BufferRadiusUnit
StatisticMode = supermap.StatisticMode
PrjCoordSysType = supermap.PrjCoordSysType
ImportMode = supermap.ImportMode
IgnoreMode = supermap.IgnoreMode
MultiBandImportMode = supermap.MultiBandImportMode
CADVersion = supermap.CADVersion
TopologyRule = supermap.TopologyRule
GeoSpatialRefType = supermap.GeoSpatialRefType
GeoCoordSysType = supermap.GeoCoordSysType
ProjectionType = supermap.ProjectionType
GeoPrimeMeridianType = supermap.GeoPrimeMeridianType
GeoSpheroidType = supermap.GeoSpheroidType
GeoDatumType = supermap.GeoDatumType
CoordSysTransMethod = supermap.CoordSysTransMethod
StatisticsFieldType = supermap.StatisticsFieldType
VectorResampleType = supermap.VectorResampleType
ArcAndVertexFilterMode = supermap.ArcAndVertexFilterMode
RasterResampleMode = supermap.RasterResampleMode
ResamplingMethod = supermap.ResamplingMethod
AggregationType = supermap.AggregationType
ReclassPixelFormat = supermap.ReclassPixelFormat
ReclassSegmentType = supermap.ReclassSegmentType
ReclassType = supermap.ReclassType
NeighbourShapeType = supermap.NeighbourShapeType
SearchMode = supermap.SearchMode
Exponent = supermap.Exponent
VariogramMode = supermap.VariogramMode
ComputeType = supermap.ComputeType
SmoothMethod = supermap.SmoothMethod
ShadowMode = supermap.ShadowMode
SlopeType = supermap.SlopeType
NeighbourUnitType = supermap.NeighbourUnitType
InterpolationAlgorithmType = supermap.InterpolationAlgorithmType
GriddingLevel = supermap.GriddingLevel
RegionToPointMode = supermap.RegionToPointMode
LineToPointMode = supermap.LineToPointMode
EllipseSize = supermap.EllipseSize
SpatialStatisticsType = supermap.SpatialStatisticsType
DistanceMethod = supermap.DistanceMethod
KernelFunction = supermap.KernelFunction
KernelType = supermap.KernelType
BandWidthType = supermap.BandWidthType
AggregationMethod = supermap.AggregationMethod
StreamOrderType = supermap.StreamOrderType
TerrainInterpolateType = supermap.TerrainInterpolateType
TerrainStatisticType = supermap.TerrainStatisticType
EdgeMatchMode = supermap.EdgeMatchMode
FunctionType = supermap.FunctionType
StatisticsCompareType = supermap.StatisticsCompareType
GridStatisticsMode = supermap.GridStatisticsMode
ConceptualizationModel = supermap.ConceptualizationModel
AttributeStatisticsMode = supermap.AttributeStatisticsMode
VCTVersion = supermap.VCTVersion
RasterJoinType = supermap.RasterJoinType
RasterJoinPixelFormat = supermap.RasterJoinPixelFormat
PlaneType = supermap.PlaneType
ChamferStyle = supermap.ChamferStyle
Buffer3DJoinType = supermap.Buffer3DJoinType
ViewShedType = supermap.ViewShedType
ImageType = supermap.ImageType
FillGradientMode = supermap.FillGradientMode
ColorSpaceType = supermap.ColorSpaceType
ImageInterpolationMode = supermap.ImageInterpolationMode
ImageDisplayMode = supermap.ImageDisplayMode
MapColorMode = supermap.MapColorMode
LayerGridAggregationType = supermap.LayerGridAggregationType
NeighbourNumber = supermap.NeighbourNumber
MajorityDefinition = supermap.MajorityDefinition
BoundaryCleanSortType = supermap.BoundaryCleanSortType
OverlayAnalystOutputType = supermap.OverlayAnalystOutputType
FieldSign = supermap.FieldSign
PyramidResampleType = supermap.PyramidResampleType
__all__ = [
 'PixelFormat', 'BlockSizeOption', 'AreaUnit', 'Unit', 'EngineType', 'DatasetType', 
 'FieldType', 
 'GeometryType', 'WorkspaceType', 'WorkspaceVersion', 'EncodeType', 
 'CursorType', 'Charset', 
 'OverlayMode', 'SpatialIndexType', 'DissolveType', 
 'TextAlignment', 'StringAlignment', 
 'ColorGradientType', 'Buffer3DJoinType', 
 'SpatialQueryMode', 
 'StatisticsType', 'JoinType', 'BufferEndType', 'BufferRadiusUnit', 
 'StatisticMode', 
 'PrjCoordSysType', 'ImportMode', 'IgnoreMode', 'MultiBandImportMode', 
 'CADVersion', 
 'TopologyRule', 'GeoSpatialRefType', 'GeoCoordSysType', 'ProjectionType', 
 'GeoPrimeMeridianType', 
 'GeoSpheroidType', 'GeoDatumType', 'CoordSysTransMethod', 'StatisticsFieldType', 
 'VectorResampleType', 
 'ArcAndVertexFilterMode', 'RasterResampleMode', 'ResamplingMethod', 
 'AggregationType', 
 'ReclassPixelFormat', 'ReclassSegmentType', 'ReclassType', 'NeighbourShapeType', 
 'SearchMode', 
 'Exponent', 'VariogramMode', 'ComputeType', 'SmoothMethod', 'ShadowMode', 
 'SlopeType', 
 'NeighbourUnitType', 'InterpolationAlgorithmType', 'GriddingLevel', 
 'RegionToPointMode', 
 'LineToPointMode', 'EllipseSize', 'SpatialStatisticsType', 
 'DistanceMethod', 'KernelFunction', 
 'KernelType', 'BandWidthType', 'AggregationMethod', 
 'StreamOrderType', 'TerrainInterpolateType', 
 'TerrainStatisticType', 'EdgeMatchMode', 
 'FunctionType', 'StatisticsCompareType', 'GridStatisticsMode', 
 'ConceptualizationModel', 
 'AttributeStatisticsMode', 'VCTVersion', 'RasterJoinType', 'RasterJoinPixelFormat', 
 'PlaneType', 
 'ChamferStyle', 'ViewShedType', 'ImageType', 'FillGradientMode', 'ColorSpaceType', 
 'ImageInterpolationMode', 
 'ImageDisplayMode', 'MapColorMode', 'LayerGridAggregationType', 
 'NeighbourNumber', 
 'MajorityDefinition', 'BoundaryCleanSortType', 'OverlayAnalystOutputType', 
 'FieldSign', 
 'PyramidResampleType']

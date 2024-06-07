# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/data.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 8243 bytes
try:
    from . import _jsuperpy as supermap
except ImportError as e:
    try:
        from . import _csuperpy as supermap
    finally:
        e = None
        del e

FieldInfo = supermap.FieldInfo
Point2D = supermap.Point2D
Point3D = supermap.Point3D
Rectangle = supermap.Rectangle
Geometry = supermap.Geometry
GeoPoint = supermap.GeoPoint
GeoPoint3D = supermap.GeoPoint3D
GeoLine = supermap.GeoLine
GeoLineM = supermap.GeoLineM
GeoRegion = supermap.GeoRegion
GeoBox = supermap.GeoBox
GeoCylinder = supermap.GeoCylinder
GeoCircle3D = supermap.GeoCircle3D
GeoRegion3D = supermap.GeoRegion3D
GeoModel3D = supermap.GeoModel3D
GeoLine3D = supermap.GeoLine3D
TextPart = supermap.TextPart
GeoText = supermap.GeoText
TextStyle = supermap.TextStyle
GeoStyle3D = supermap.GeoStyle3D
Feature = supermap.Feature
StepEvent = supermap.StepEvent
Plane = supermap.Plane
Matrix = supermap.Matrix
Datasource = supermap.Datasource
DatasourceConnectionInfo = supermap.DatasourceConnectionInfo
Dataset = supermap.Dataset
DatasetVector = supermap.DatasetVector
DatasetVectorInfo = supermap.DatasetVectorInfo
DatasetImageInfo = supermap.DatasetImageInfo
DatasetGridInfo = supermap.DatasetGridInfo
DatasetImage = supermap.DatasetImage
DatasetGrid = supermap.DatasetGrid
DatasetTopology = supermap.DatasetTopology
DatasetVolume = supermap.DatasetVolume
DatasetMosaic = supermap.DatasetMosaic
Colors = supermap.Colors
JoinItem = supermap.JoinItem
LinkItem = supermap.LinkItem
SpatialIndexInfo = supermap.SpatialIndexInfo
QueryParameter = supermap.QueryParameter
TimeCondition = supermap.TimeCondition
combine_band = supermap.combine_band
Recordset = supermap.Recordset
DatasourceReadOnlyError = supermap.DatasourceReadOnlyError
DatasourceOpenedFailedError = supermap.DatasourceOpenedFailedError
ObjectDisposedError = supermap.ObjectDisposedError
DatasourceCreatedFailedError = supermap.DatasourceCreatedFailedError
PrjCoordSys = supermap.PrjCoordSys
GeoCoordSys = supermap.GeoCoordSys
GeoDatum = supermap.GeoDatum
GeoSpheroid = supermap.GeoSpheroid
GeoPrimeMeridian = supermap.GeoPrimeMeridian
Projection = supermap.Projection
PrjParameter = supermap.PrjParameter
CoordSysTransParameter = supermap.CoordSysTransParameter
CoordSysTranslator = supermap.CoordSysTranslator
WorkspaceConnectionInfo = supermap.WorkspaceConnectionInfo
Workspace = supermap.Workspace
open_datasource = supermap.open_datasource
get_datasource = supermap.get_datasource
close_datasource = supermap.close_datasource
list_datasources = supermap.list_datasources
create_datasource = supermap.create_datasource
GeometriesRelation = supermap.GeometriesRelation
aggregate_points_geo = supermap.aggregate_points_geo
can_contain = supermap.can_contain
has_intersection = supermap.has_intersection
has_area_intersection = supermap.has_area_intersection
has_cross = supermap.has_cross
has_overlap = supermap.has_overlap
has_touch = supermap.has_touch
has_common_point = supermap.has_common_point
has_common_line = supermap.has_common_line
has_hollow = supermap.has_hollow
is_disjointed = supermap.is_disjointed
is_identical = supermap.is_identical
is_within = supermap.is_within
is_left = supermap.is_left
is_right = supermap.is_right
is_on_same_side = supermap.is_on_same_side
is_parallel = supermap.is_parallel
is_point_on_line = supermap.is_point_on_line
is_project_on_line_segment = supermap.is_project_on_line_segment
is_perpendicular = supermap.is_perpendicular
nearest_point_to_vertex = supermap.nearest_point_to_vertex
clip = supermap.clip
erase = supermap.erase
identity = supermap.identity
intersect = supermap.intersect
intersect_line = supermap.intersect_line
intersect_polyline = supermap.intersect_polyline
union = supermap.union
update = supermap.update
xor = supermap.xor
compute_concave_hull = supermap.compute_concave_hull
compute_convex_hull = supermap.compute_convex_hull
compute_geodesic_area = supermap.compute_geodesic_area
compute_geodesic_distance = supermap.compute_geodesic_distance
compute_geodesic_line = supermap.compute_geodesic_line
compute_geodesic_line2 = supermap.compute_geodesic_line2
compute_parallel = supermap.compute_parallel
compute_parallel2 = supermap.compute_parallel2
compute_perpendicular = supermap.compute_perpendicular
compute_perpendicular_position = supermap.compute_perpendicular_position
compute_distance = supermap.compute_distance
point_to_segment_distance = supermap.point_to_segment_distance
resample = supermap.resample
smooth = supermap.smooth
compute_default_tolerance = supermap.compute_default_tolerance
split_line = supermap.split_line
split_region = supermap.split_region
georegion_to_center_line = supermap.georegion_to_center_line
orthogonal_polygon_fitting = supermap.orthogonal_polygon_fitting
dataset_dim2_to_dim3 = supermap.dataset_dim2_to_dim3
dataset_dim3_to_dim2 = supermap.dataset_dim3_to_dim2
dataset_point_to_line = supermap.dataset_point_to_line
dataset_line_to_point = supermap.dataset_line_to_point
dataset_line_to_region = supermap.dataset_line_to_region
dataset_region_to_line = supermap.dataset_region_to_line
dataset_region_to_point = supermap.dataset_region_to_point
dataset_field_to_text = supermap.dataset_field_to_text
dataset_text_to_field = supermap.dataset_text_to_field
dataset_text_to_point = supermap.dataset_text_to_point
dataset_field_to_point = supermap.dataset_field_to_point
dataset_network_to_line = supermap.dataset_network_to_line
dataset_network_to_point = supermap.dataset_network_to_point
Color = supermap.Color
GeoStyle = supermap.GeoStyle
list_maps = supermap.list_maps
get_map = supermap.get_map
remove_map = supermap.remove_map
add_map = supermap.add_map
__all__ = [
 'DatasourceConnectionInfo', 'Datasource', 'Dataset', 'DatasetVector', 'DatasetVectorInfo', 
 'DatasetImageInfo', 
 'DatasetGridInfo', 
 'DatasetImage', 'DatasetGrid', 'DatasetTopology', 'DatasetMosaic', 
 'DatasetVolume', 
 'Colors', 'JoinItem', 'LinkItem', 'SpatialIndexInfo', 
 'QueryParameter', 
 'TimeCondition', 'combine_band', 'Recordset', 'DatasourceReadOnlyError', 
 'DatasourceOpenedFailedError', 
 'ObjectDisposedError', 'DatasourceCreatedFailedError', 
 'FieldInfo', 'Point2D', 'Point3D', 'Rectangle', 
 'Geometry', 'GeoPoint', 
 'GeoPoint3D', 'GeoLine', 'GeoLineM', 'GeoRegion', 'TextPart', 'GeoText', 
 'TextStyle', 
 'GeoRegion3D', 'GeoModel3D', 'GeoBox', 'GeoLine3D', 'GeoCylinder', 
 'GeoCircle3D', 'GeoStyle3D', 'Plane', 
 'Matrix', 'Feature', 'GeometriesRelation', 
 'aggregate_points_geo', 'can_contain', 'has_intersection', 
 'has_area_intersection', 
 'has_cross', 
 'has_overlap', 'has_touch', 'has_common_point', 'has_common_line', 'has_hollow', 
 'is_disjointed', 
 'is_identical', 'is_within', 'is_left', 'is_right', 'is_on_same_side', 'is_parallel', 
 'is_point_on_line', 
 'is_project_on_line_segment', 'is_perpendicular', 'nearest_point_to_vertex', 
 'clip', 
 'erase', 'identity', 
 'intersect', 'intersect_line', 'intersect_polyline', 
 'union', 'update', 'xor', 'compute_concave_hull', 
 'compute_convex_hull', 
 'compute_geodesic_area', 'compute_geodesic_distance', 'compute_geodesic_line', 
 'compute_geodesic_line2', 
 'compute_parallel', 'compute_parallel2', 'compute_perpendicular', 
 'compute_perpendicular_position', 
 'compute_distance', 'point_to_segment_distance', 'resample', 'smooth', 
 'compute_default_tolerance', 
 'split_line', 'split_region', 'georegion_to_center_line', 
 'orthogonal_polygon_fitting', 
 'PrjCoordSys', 
 'GeoCoordSys', 'GeoDatum', 'GeoSpheroid', 'GeoPrimeMeridian', 
 'Projection', 'PrjParameter', 
 'CoordSysTransParameter', 'CoordSysTranslator', 
 'StepEvent', 
 'WorkspaceConnectionInfo', 'Workspace', 'open_datasource', 'get_datasource', 
 'close_datasource', 
 'list_datasources', 'create_datasource', 'dataset_dim2_to_dim3', 'dataset_dim3_to_dim2', 
 'dataset_point_to_line', 
 'dataset_line_to_point', 
 'dataset_line_to_region', 'dataset_region_to_line', 
 'dataset_region_to_point', 'dataset_field_to_text', 
 'dataset_text_to_field', 
 'dataset_text_to_point', 'dataset_field_to_point', 'dataset_network_to_line', 
 'dataset_network_to_point', 
 'Color', 'GeoStyle', 'list_maps', 'remove_map', 'add_map', 'get_map']

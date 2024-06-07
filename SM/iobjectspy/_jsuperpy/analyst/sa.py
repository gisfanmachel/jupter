# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/_jsuperpy\analyst\sa.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 643857 bytes
"""空间分析模块"""
from iobjectspy._jsuperpy._gateway import get_gateway, get_jvm, safe_start_callback_server, close_callback_server
from iobjectspy._jsuperpy.data import Datasource, Colors, DatasetVector, Recordset, Point2D, Geometry, DatasetImage, DatasetGrid, Rectangle, GeoRegion, GeoLine, GeoRegion3D, Point3D, GeoLine3D
from iobjectspy._jsuperpy.data._listener import ProgressListener
from iobjectspy._jsuperpy.data._util import to_java_point2d_array, get_input_dataset, get_output_datasource, check_output_datasource, try_close_output_datasource, create_result_datasaet, to_java_stattype_array, to_java_geometry_array, to_java_point3ds, to_java_datasetgrid_array, to_java_datasetvector_array, to_java_dataset_array
from iobjectspy._jsuperpy.enums import *
from iobjectspy._jsuperpy._utils import *
from iobjectspy._jsuperpy._logger import *
from iobjectspy._jsuperpy.data._jvm import JVMBase
from iobjectspy._jsuperpy.data._listener import PythonListenerBase
from enum import unique
__all__ = [
 'create_buffer', 'overlay', 'dissolve', 'aggregate_points', 'smooth_vector', 
 'resample_vector', 
 'create_thiessen_polygons', 'summary_points', 'clip_vector', 
 'update_attributes', 'simplify_building', 
 'resample_raster', 'ReclassSegment', 
 'ReclassMappingTable', 
 'reclass_grid', 'aggregate_grid', 'slice_grid', 
 'compute_range_raster', 'compute_range_vector', 
 'NeighbourShape', 'NeighbourShapeRectangle', 
 'NeighbourShapeCircle', 
 'NeighbourShapeAnnulus', 'NeighbourShapeWedge', 
 'kernel_density', 'point_density', 'clip_raster', 
 'InterpolationDensityParameter', 
 'InterpolationIDWParameter', 'InterpolationKrigingParameter', 
 'InterpolationRBFParameter', 
 'interpolate', 'interpolate_points', 'idw_interpolate', 'density_interpolate', 
 'kriging_interpolate', 
 'rbf_interpolate', 'vector_to_raster', 'raster_to_vector', 'cost_distance', 
 'cost_path', 
 'cost_path_line', 'path_line', 'straight_distance', 'surface_distance', 'surface_path_line', 
 'calculate_hill_shade', 
 'calculate_slope', 'calculate_aspect', 'compute_point_aspect', 'compute_point_slope', 
 'calculate_ortho_image', 
 'compute_surface_area', 'compute_surface_distance', 'compute_surface_volume', 
 'divide_math_analyst', 
 'plus_math_analyst', 'minus_math_analyst', 'multiply_math_analyst', 
 'to_float_math_analyst', 
 'to_int_math_analyst', 'expression_math_analyst', 'StatisticsField', 
 'create_line_one_side_multi_buffer', 
 'create_multi_buffer', 'compute_min_distance', 
 'compute_range_distance', 
 'integrate', 'eliminate', 'eliminate_specified_regions', 'edge_match', 
 'region_to_center_line', 
 'dual_line_to_center_line', 
 'grid_extract_isoline', 'grid_extract_isoregion', 'point_extract_isoline', 
 'points_extract_isoregion', 
 'point3ds_extract_isoline', 'point3ds_extract_isoregion', 
 'grid_basic_statistics', 
 'BasicStatisticsAnalystResult', 'grid_common_statistics', 
 'grid_neighbour_statistics', 
 'altitude_statistics', 
 'GridHistogram', 'thin_raster', 'build_lake', 'build_terrain', 
 'area_solar_radiation_days', 
 'area_solar_radiation_hours', 'raster_mosaic', 
 'zonal_statistics_on_raster_value', 
 'calculate_profile', 'CutFillResult', 'inverse_cut_fill', 
 'cut_fill_grid', 
 'cut_fill_oblique', 'cut_fill_region', 'cut_fill_region3d', 'flood', 'thin_raster_bit', 
 'ViewShedType', 
 'NDVI', 'NDWI', 'compute_features_envelope', 'calculate_view_shed', 'calculate_view_sheds', 
 'VisibleResult', 
 'is_point_visible', 'are_points_visible', 'line_of_sight', 'radar_shield_angle', 
 'majority_filter', 
 'expand', 'shrink', 'nibble', 'region_group', 'boundary_clean', 
 'CellularAutomataParameter', 
 'PCACellularAutomataParameter', 'PCAEigenValue', 
 'PCAEigenResult', 'PCACellularAutomata', 
 'CellularAutomataFlushedEvent', 
 'ANNTrainResult', 'ANNCellularAutomataParameter', 
 'ANNCellularAutomata', 'ANNCellularAutomataResult', 
 'ANNParameter']

class StatisticsField(object):
    __doc__ = "\n    对字段进行统计的信息。主要用于 :py:meth:`summary_points`\n    "

    def __init__(self, source_field=None, stat_type=None, result_field=None):
        """
        初始化对象

        :param str source_field: 被统计的字段名称
        :param stat_type: 统计类型
        :type stat_type: StatisticsFieldType or str
        :param str result_field: 结果字段名称
        """
        self._source_field = None
        self._stat_type = None
        self._result_field = None
        self.set_source_field(source_field).set_stat_type(stat_type).set_result_field(result_field)

    @property
    def source_field(self):
        """str: 被统计的字段名称"""
        return self._source_field

    @property
    def stat_type(self):
        """StatisticsFieldType: 字段统计类型"""
        return self._stat_type

    @property
    def result_field(self):
        """str: 结果字段名称"""
        return self._result_field

    def set_source_field(self, value):
        """
        设置被统计的字段名称

        :param str value: 字段名称
        :return: self
        :rtype: StatisticsField
        """
        if value is not None:
            self._source_field = value
        return self

    def set_stat_type(self, value):
        """
        设置字段统计类型

        :param value: 字段统计类型
        :type value: StatisticsFieldType or str
        :return: self
        :rtype: StatisticsField
        """
        if value is not None:
            self._stat_type = StatisticsFieldType._make(value)
        return self

    def set_result_field(self, value):
        """
        设置结果字段名称

        :param str value: 结果字段名称
        :return: self
        :rtype: StatisticsField
        """
        if value is not None:
            self._result_field = value
        return self

    @property
    def _jobject(self):
        """Py4J 映射的 Java 对象"""
        jvm = get_jvm()
        java_statField = jvm.com.supermap.analyst.spatialanalyst.StatisticsField()
        java_statField.setSourceField(self.source_field)
        java_statField.setMode(self.stat_type._jobject)
        java_statField.setResultField(self.result_field)
        return java_statField


def _throw_un_supported():
    raise Exception("Unsupported")


def create_buffer(input_data, distance_left, distance_right=None, unit=None, end_type=None, segment=24, is_save_attributes=True, is_union_result=False, out_data=None, out_dataset_name='BufferResult', progress=None):
    """
    创建矢量数据集或记录集的缓冲。

    缓冲区分析是围绕空间对象，使用一个或多个与这些对象的距离值（称为缓冲半径）作为半径，生成一个或多个区域的过程。缓冲区也可以理解为空间对象的一种影响或服务范围。

    缓冲区分析的基本作用对象是点、线、面。SuperMap 支持对二维点、线、面数据集（或记录集）和网络数据集进行缓冲区分析。其中，对网络数据集进行缓冲区分析时，是对其中的弧段作缓冲区。缓冲区的类型可以分析单重缓冲区（或称简单缓冲区）和多重缓冲区。下面以简单缓冲区为例分别介绍点、线、面的缓冲区。

    * 点缓冲区
      点的缓冲区是以点对象为圆心，以给定的缓冲距离为半径生成的圆形区域。当缓冲距离足够大时，两个或多个点对象的缓冲区可能有重叠。选择合并缓冲区时，重叠部分将被合并，最终得到的缓冲区是一个复杂面对象。

      .. image:: ../image/PointBuffer.png

    * 线缓冲区
      线的缓冲区是沿线对象的法线方向，分别向线对象的两侧平移一定的距离而得到两条线，并与在线端点处形成的光滑曲线（也可以形成平头）接合形成的封闭区域。同样，当缓冲距离足够大时，两个或多个线对象的缓冲区可能有重叠。合并缓冲区的效果与点的合并缓冲区相同。

      .. image:: ../image/LineBuffer.png

      线对象两侧的缓冲宽度可以不一致，从而生成左右不等缓冲区；也可以只在线对象的一侧创建单边缓冲区。此时只能生成平头缓冲区。

      .. image:: ../image/LineBuffer_1.png

    * 面缓冲区

      面的缓冲区生成方式与线的缓冲区类似，区别是面的缓冲区仅在面边界的一侧延展或收缩。当缓冲半径为正值时，缓冲区向面对象边界的外侧扩展；为负值时，向边界内收缩。同样，当缓冲距离足够大时，两个或多个线对象的缓冲区可能有重叠。也可以选择合并缓冲区，其效果与点的合并缓冲区相同。

      .. image:: ../image/RegionBuffer.png

    * 多重缓冲区是指在几何对象的周围，根据给定的若干缓冲区半径，建立相应数据量的缓冲区。对于线对象，还可以建立单边多重缓冲区，但注意不支持对网络数据集创建。

      .. image:: ../image/MultiBuffer.png

    缓冲区分析在 GIS 空间分析中经常用到，且往往结合叠加分析来共同解决实际问题。缓冲区分析在农业、城市规划、生态保护、防洪抗灾、军事、地质、环境等诸多领域都有应用。

    例如扩建道路时，可根据道路扩宽宽度对道路创建缓冲区，然后将缓冲区图层与建筑图层叠加，通过叠加分析查找落入缓冲区而需要被拆除的建筑；又如，为了保护环境和耕地，可对湿地、森林、草地和耕地进行缓冲区分析，在缓冲区内不允许进行工业建设。

    说明：

    *  对于面对象，在做缓冲区分析前最好先经过拓扑检查，排除面内相交的情况，所谓面内相交，指的是面对象自身相交，如图所示，图中数字代表面对象的节点顺序。

    .. image:: ../image/buffer_regioninter.png

    * 对“负半径”的说明

        * 如果缓冲区半径为数值型，则仅面数据支持负半径；
        * 如果缓冲区半径为字段或字段表达式，如果字段或字段表达式的值为负值，对于点、线数据取其绝对值；对于面数据，若合并缓冲区，则取其绝对值，若不合并，则按照负半径处理。

    :param input_data: 指定的创建缓冲区的源矢量记录集是数据集。支持点、线、面数据集和记录集。
    :type input_data: Recordset or DatasetVector or str
    :param distance_left: （左）缓冲区的距离。如果为字符串，则表示（左）缓冲距离所在的字段，即每个几何对象创建缓冲区时使用字段中存储的值作为缓冲半径。对于线对象，表示左缓冲区半径，对于点和面对象，表示缓冲区半径。
    :type distance_left: float or str
    :param distance_right: 右缓冲区的距离，如果为字符串，则表示右缓冲距离所在的字段，即每个线几何对象创建缓冲区时使用字段中存储的值作为右缓冲半径。该参数只对线对象有效。
    :type distance_right: float or str
    :param unit: 缓冲区距离半径单位，只支持距离单位，不支持角度和弧度单位。
    :type unit: Unit or str
    :param end_type: 缓冲区端点类型。用以区分线对象缓冲区分析时的端点是圆头缓冲还是平头缓冲。对于点或面对象，只支持圆头缓冲
    :type end_type: BufferEndType or str
    :param int segment: 半圆弧线段个数，即用多少个线段来模拟一个半圆，必须大于等于4。
    :param  bool is_save_attributes: 是否保留进行缓冲区分析的对象的字段属性。当合并结果面数据集时，该参数无效。即当 isUnion 参数为 false 时有效。
    :param bool is_union_result: 是否合并缓冲区，即是否将源数据各对象生成的所有缓冲区域进行合并运算后返回。对于面对象而言，要求源数据集中的面对象不相交。
    :param out_data: 存储结果数据的数据源
    :type out_data: Datasource
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector or str
    """
    check_lic()
    _input = get_input_dataset(input_data)
    if _input is None:
        raise ValueError("input_data is None")
    else:
        if not isinstance(_input, (DatasetVector, Recordset)):
            raise ValueError("input_data required DatasetVector or Recordset, but now is " + str(type(_input)))
        else:
            end_type = BufferEndType._make(end_type, BufferEndType.ROUND)
            if end_type is None:
                raise ValueError("invalid buffer end type object")
            else:
                _jvm = get_jvm()
                if unit is not None:
                    if isinstance(unit, Unit):
                        unit = unit.name
                    dist_unit = BufferRadiusUnit._make(unit, BufferRadiusUnit.METER)
                else:
                    dist_unit = BufferRadiusUnit.METER
            buffer_param = _jvm.com.supermap.analyst.spatialanalyst.BufferAnalystParameter()
            buffer_param.setEndType(end_type._jobject)
            buffer_param.setRadiusUnit(dist_unit._jobject)
            buffer_param.setSemicircleLineSegment(segment)
            buffer_param.setLeftDistance(distance_left)
            buffer_param.setRightDistance(distance_right)
            if out_data is not None:
                out_datasource = get_output_datasource(out_data)
                _ds = out_datasource
            else:
                _ds = _input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = "buffer_result"
        else:
            _outDatasetName = out_dataset_name
    result_dt = create_result_datasaet(_ds, _outDatasetName, "REGION")
    if isinstance(_input, DatasetVector):
        result_dt.set_prj_coordsys(_input.prj_coordsys)
    else:
        if isinstance(_input, Recordset):
            result_dt.set_prj_coordsys(_input.dataset.prj_coordsys)
        listener = None
        if progress is not None:
            if safe_start_callback_server():
                try:
                    listener = ProgressListener(progress, "create_buffer")
                    _jvm.com.supermap.analyst.spatialanalyst.BufferAnalyst.addSteppedListener(listener)
                except Exception as e:
                    try:
                        close_callback_server()
                        log_error(e)
                        listener = None
                    finally:
                        e = None
                        del e

        try:
            try:
                result = _jvm.com.supermap.analyst.spatialanalyst.BufferAnalyst.createBuffer(_input._jobject, result_dt._jobject, buffer_param, is_union_result, is_save_attributes)
            except Exception as e:
                try:
                    log_error(e)
                    result = False
                finally:
                    e = None
                    del e

        finally:
            if listener is not None:
                try:
                    _jvm.com.supermap.analyst.spatialanalyst.BufferAnalyst.removeSteppedListener(listener)
                except Exception as e1:
                    try:
                        log_error(e1)
                    finally:
                        e1 = None
                        del e1

                close_callback_server()
            if not result:
                out_datasource.delete(result_dt.name)
                result_dt = None
            if out_data is not None:
                return try_close_output_datasource(result_dt, out_datasource)
            return result_dt


def create_line_one_side_multi_bufferParse error at or near `COME_FROM_LOOP' instruction at offset 204_3


def create_multi_bufferParse error at or near `COME_FROM_LOOP' instruction at offset 198_3


def overlayParse error at or near `COME_FROM' instruction at offset 990_0


def _overlay_geometrys(source_geos, overlay_geos, overlay_mode, ds, out_name, tolerance, progress):
    _overlayMode = OverlayMode._make(overlay_mode)
    _jvm = get_jvm()
    overlay_funs = {(OverlayMode.CLIP): (_jvm.com.supermap.analyst.spatialanalyst.OverlayAnalyst.clip), 
     (OverlayMode.ERASE): (_jvm.com.supermap.analyst.spatialanalyst.OverlayAnalyst.erase), 
     (OverlayMode.INTERSECT): (_jvm.com.supermap.analyst.spatialanalyst.OverlayAnalyst.intersect), 
     (OverlayMode.IDENTITY): (_jvm.com.supermap.analyst.spatialanalyst.OverlayAnalyst.identity), 
     (OverlayMode.XOR): (_jvm.com.supermap.analyst.spatialanalyst.OverlayAnalyst.xOR), 
     (OverlayMode.UPDATE): (_jvm.com.supermap.analyst.spatialanalyst.OverlayAnalyst.update), 
     (OverlayMode.UNION): (_jvm.com.supermap.analyst.spatialanalyst.OverlayAnalyst.union)}
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, "overlay")
                _jvm.com.supermap.analyst.spatialanalyst.OverlayAnalyst.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            result = overlay_funs[_overlayMode](to_java_geometry_array(source_geos), to_java_geometry_array(overlay_geos), tolerance)
        except:
            import traceback
            log_error(traceback.format_exc())
            result = None

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.OverlayAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if result is None:
            return try_close_output_datasource(None, ds)
        from ..data import FieldInfo, Feature
        field_infos = [FieldInfo("SourceIndex", "INT32"), FieldInfo("OverlayIndex", "INT32")]
        features = []
        for r in result:
            feature = Feature((Geometry._from_java_object(r.getGeometry())), [
             r.getSourceIndex(), r.getTargetIndex()],
              field_infos=field_infos)
            features.append(feature)

        dt = ds.write_features(features, out_name)
        return try_close_output_datasource(dt, ds)


class _DissolveParameter:
    __doc__ = "\n    融合是指将融合字段值相同的对象合并为一个简单对象或复杂对象。适用于线对象和面对象。简单对象是指只有一个子对象（即简单对象本身）的对象，与复杂对象对应。\n    复杂对象是指具有两个或多个子对象的对象，这些子对象类型相同。子对象是构成简单对象和复杂对象的基本对象。简单对象由一个子对象组成，即简单对象本身；复杂对象由两个或两个以上相同类型的子对象组成\n    "

    def __init__(self, dissolve_type=None, fields=None, stats_fields=None, stats_types=None, attr_filter=None, tolerance=1e-10, is_null_value_able=True, is_preprocess=True):
        """
        初始化融合参数对象
        :param dissolve_type: 融合类型
        :type dissolve_type: DissolveType or str
        :param fields: 融合字段，融合字段的字段值相同的记录才会融合。当 fields 为 str 时，支持设置 ',' 分隔多个字段，例如 "field1,field2,field3"
        :type fields: list[str] or str
        :param stats_fields:  统计字段的名称的集合。当 stats_fields 为 str 时，支持设置 ',' 分隔多个字段，例如 "field1,field2,field3"
        :type stats_fields: list[str] or str
        :param stats_types: 统计字段的类型的集合。必须与 stats_fields 数目相同。如果 stats_types 为 str 时，支持设置 ',' 分隔多个统计字段类型名称，比如'MAX,MIN,SUM'
        :type stats_types: list[StatisticsType] or str
        :param str attr_filter: 数据集融合时对象的过滤表达式
        :param float tolerance: 融合容限
        :param bool is_null_value_able: 是否处理融合字段值为空的对象
        :param bool is_preprocess: 是否进行拓扑预处理
        """
        self._dissolveType = None
        self._fields = None
        self._statsFields = None
        self._statsType = None
        self._filter = None
        self._tolerance = 1e-10
        self._isNullValue = True
        self._isPreprocess = True
        self.set_dissolve_type(dissolve_type)
        self.set_dissolve_fields(fields)
        self.set_statistics_field_names(stats_fields)
        self.set_statistics_types(stats_types)
        self.set_filter_string(attr_filter)
        self.set_tolerance(tolerance)
        self.set_null_value_able(is_null_value_able)
        self.set_preprocess(is_preprocess)

    def set_dissolve_type(self, value):
        """
        设置融合类型

        :param value:  融合类型
        :type value: DissolveType or str
        :return: self
        :rtype: _DissolveParameter
        """
        self._dissolveType = DissolveType._make(value)
        return self

    @property
    def dissolve_type(self):
        """DissolveType: 返回融合类型"""
        return self._dissolveType

    def set_dissolve_fields(self, value):
        """
        设置融合字段

        :param value: 融合字段的字段值相同的记录才会融合。当 value 为 str 时，支持设置 ',' 分隔多个字段，例如 "field1,field2,field3"
        :type value: list[str] or str
        :return: self
        :rtype: _DissolveParameter
        """
        if value is not None:
            self._fields = split_input_list_from_str(value)
        return self

    @property
    def dissolve_fields(self):
        """list[str]: 融合字段"""
        return self._fields

    def set_statistics_field_names(self, value):
        """
        设置属性统计字段名称
        :param value: 属性统计字段名称。如果 value 为 str 时，支持设置 ',' 分隔多个统计字段类型名称，比如'field1,field2,field3'
        :type value: list[str] or str
        :return: self
        :rtype: _DissolveParameter
        """
        if value is not None:
            self._statsFields = split_input_list_from_str(value)
        return self

    @property
    def statistics_field_names(self):
        """list[str]: 属性统计字段名称"""
        return self._statsFields

    def set_statistics_types(self, value):
        """
        设置属性统计类型，数目必须与 statistics_field_names 数目相同

        :param value: 属性统计类型。如果 value 为 str 时，支持设置 ',' 分隔多个统计字段类型名称，比如'MAX,MIN,SUM'
        :type value: list[StatisticsType] or str
        :return: self
        :rtype: _DissolveParameter
        """
        if value is not None:
            items = split_input_list_from_str(value)
            if items is not None:
                self._statsType = []
                for item in items:
                    self._statsType.append(StatisticsType._make(item))

        return self

    @property
    def statistics_types(self):
        """list[StatisticsType]: 属性统计类型列表"""
        return self._statsType

    def set_filter_string(self, value):
        """
        设置数据集融合时对象的过滤表达式

        :param str value: 数据集融合时对象的过滤表达式
        :return: self
        :rtype: _DissolveParameter
        """
        self._filter = value
        return self

    @property
    def filter_string(self):
        """str: 数据集融合时对象的过滤表达式 """
        return self._filter

    def set_tolerance(self, value):
        """
        设置融合过程中使用的节点容限

        :param float value: 节点容限
        :return: self
        :rtype: _DissolveParameter
        """
        if value is not None:
            self._tolerance = float(value)
        return self

    @property
    def tolerance(self):
        """float: 融合过程使用的节点容限"""
        return self._tolerance

    def set_null_value_able(self, value):
        """
        设置是否处理空字段对象

        :param bool value: 是否处理空字段对象
        :return: self
        :rtype: _DissolveParameter
        """
        if value is not None:
            self._isNullValue = bool(value)
        return self

    @property
    def is_null_value_able(self):
        """bool: 是否处理空字段的对象 """
        return self._isNullValue

    def set_preprocess(self, value):
        """
        设置是否进行拓扑预处理

        :param bool value: 是否进行拓扑预处理
        :return: self
        :rtype: _DissolveParameter
        """
        if value is not None:
            self._isPreprocess = bool(value)
        return self

    @property
    def is_preprocess(self):
        """bool: 是否进行拓扑预处理"""
        return self._isPreprocess

    @property
    def _jobject(self):
        """Py4J 映射的 Java 对象"""
        java_parameter = get_jvm().com.supermap.analyst.spatialanalyst.DissolveParameter()
        java_parameter.setDissolveType(self.dissolve_type._jobject)
        java_parameter.setFieldNames(to_java_string_array(self.dissolve_fields))
        java_parameter.setFilterString(self.filter_string)
        java_parameter.setNullValue(self.is_null_value_able)
        java_parameter.setPreProcess(self.is_preprocess)
        if self.statistics_field_names is not None:
            java_parameter.setStatisticsFieldNames(to_java_string_array(self.statistics_field_names))
        if self.statistics_types is not None:
            java_parameter.setStatisticsTypes(to_java_stattype_array(self.statistics_types))
        java_parameter.setTolerance(self.tolerance)
        return java_parameter


def dissolve(input_data, dissolve_type, dissolve_fields, field_stats=None, attr_filter=None, is_null_value_able=True, is_preprocess=True, tolerance=1e-10, out_data=None, out_dataset_name='DissolveResult', progress=None):
    """
    融合是指将融合字段值相同的对象合并为一个简单对象或复杂对象。适用于线对象和面对象。子对象是构成简单对象和复杂对象的基本对象。简单对象由一个子对象组成，
    即简单对象本身；复杂对象由两个或两个以上相同类型的子对象组成。

    :param input_data: 待融合的矢量数据集。必须为线数据集或面数据集。
    :type input_data: DatasetVector or str
    :param dissolve_type: 融合类型
    :type dissolve_type: DissolveType or str
    :param dissolve_fields: 融合字段，融合字段的字段值相同的记录才会融合。当 dissolve_fields 为 str 时，支持设置 ',' 分隔多个字段，例如 "field1,field2,field3"
    :type dissolve_fields: list[str] or str
    :param field_stats:  统计字段名称和对应的统计类型。stats_fields 为 list，list中每个元素为一个tuple，tuple的第一个元素为被统计的字段，第二个元素为统计类型。
                         当 stats_fields 为 str 时，支持设置 ',' 分隔多个字段，例如 "field1:SUM, field2:MAX, field3:MIN"
    :type field_stats: list[tuple[str,StatisticsType]] or list[tuple[str,str]] or str
    :param str attr_filter: 数据集融合时对象的过滤表达式
    :param float tolerance: 融合容限
    :param bool is_null_value_able: 是否处理融合字段值为空的对象
    :param bool is_preprocess: 是否进行拓扑预处理
    :param out_data: 结果数据保存的数据源。如果为空，则结果数据集保存到输入数据集所在的数据源。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector or str

    >>> result = dissolve('E:/data.udb/zones', 'SINGLE', 'SmUserID', 'Area:SUM', tolerance=0.000001, out_data='E:/dissolve_out.udb')

    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    else:
        if not isinstance(_source_input, DatasetVector):
            raise ValueError("source input_data must be DatasetVector")
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + "_Dissolve"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    stats_fields = []
    stats_types = []
    if field_stats is not None:
        field_stats = split_input_list_tuple_item_from_str(field_stats)
        if isinstance(field_stats, list):
            for name, stat_type in field_stats:
                stats_fields.append(name)
                stats_types.append(StatisticsType._make(stat_type))

    parameter = _DissolveParameter().set_dissolve_type(dissolve_type).set_dissolve_fields(dissolve_fields).set_statistics_field_names(stats_fields).set_statistics_types(stats_types).set_filter_string(attr_filter).set_tolerance(tolerance).set_null_value_able(is_null_value_able).set_preprocess(is_preprocess)
    _java_parameter = parameter._jobject
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, "dissolve")
                _jvm.com.supermap.analyst.spatialanalyst.Generalization.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.Generalization.dissolve(_source_input._jobject, _ds._jobject, _outDatasetName, _java_parameter)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.OverlayAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def aggregate_points(input_data, min_pile_point, distance, unit=None, class_field=None, out_data=None, out_dataset_name='AggregateResult', progress=None):
    """
    对点数据集进行聚类，使用密度聚类算法，返回聚类后的类别或同一簇构成的多边形。
    对点集合进行空间位置的聚类，使用密度聚类方法 DBSCAN，它能将具有足够高密度的区域划分为簇，并可以在带有噪声的空间数据中发现任意形状的聚类。它定义
    簇为密度相连的点的最大集合。DBSCAN 使用阈值 e 和 MinPts 来控制簇的生成。其中，给定对象半径 e 内的区域称为该对象的 e一邻域。如果一个对象的
    e一邻域至少包含最小数目 MinPtS 个对象，则称该对象为核心对象。给定一个对象集合 D，如果 P 是在 Q 的 e一邻域内，而 Q 是一个核心对象，我们说对象
    P 从对象 Q 出发是直接密度可达的。DBSCAN 通过检查数据里中每个点的 e-领域来寻找聚类，如果一个点 P 的 e-领域包含多于 MinPts 个点，则创建一个
    以 P 作为核心对象的新簇，然后，DBSCAN反复地寻找从这些核心对象直接密度可达的对象并加入该簇，直到没有新的点可以被添加。

    :param input_data: 输入的点数据集
    :type input_data: DatasetVector or str
    :param int min_pile_point:  密度聚类点数目阈值，必须大于等于2。阈值越大表示能聚类为一簇的条件越苛刻。
    :param float distance: 密度聚类半径。
    :param unit:  密度聚类半径的单位。
    :type unit: Unit or str
    :param str class_field: 输入的点数据集中用于保存密度聚类的结果聚类类别的字段，如果不为空，则必须是点数据集中合法的字段名称。
                            要求字段类型为INT16, INT32 或 INT64，如果字段名有效但不存在，将会创建一个 INT32 的字段。
                            参数有效，则会将聚类类别保存在此字段中。
    :param out_data: 结果数据源信息，结果数据源信息不能与 class_field同时为空，如果结果数据源有效时，将会生成结果面对象。
    :type out_data: Datasource or DatasourceConnectionInfo or st
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称，如果输入的结果数据源为空，将会返回一个布尔值，True 表示聚类成功，False 表示聚类失败。
    :rtype: DatasetVector or str or bool

    >>> result = aggregate_points('E:/data.udb/point', 4, 100, 'Meter', 'SmUserID', out_data='E:/aggregate_out.udb')

    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    elif not isinstance(_source_input, DatasetVector):
        raise ValueError("source input_data must be DatasetVector")
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
            check_output_datasource(_ds)
            if out_dataset_name is None:
                _outDatasetName = _source_input.name + "_Agge"
            else:
                _outDatasetName = out_dataset_name
            _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
        else:
            _ds = None
            _outDatasetName = None
        _jvm = get_jvm()
        if class_field is not None:
            field_info = _source_input.get_field_info(str(class_field))
            if field_info is not None:
                if field_info.type not in (FieldType.INT16, FieldType.INT32, FieldType.INT64):
                    raise ValueError("invalid class field type, required int16, int32 and int64, but is " + str(field_info.type.name))
            else:
                from ..data import FieldInfo
                _source_input.create_field(FieldInfo(class_field, FieldType.INT32))
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, "aggregate_points")
                _jvm.com.supermap.analyst.spatialanalyst.Generalization.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            is_success = _jvm.com.supermap.analyst.spatialanalyst.Generalization.aggregatePoints(oj(_source_input), float(distance), oj(Unit._make(unit)), min_pile_point, oj(_ds), _outDatasetName, class_field)
        except Exception as e:
            try:
                log_error(e)
                is_success = False
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.Generalization.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif is_success:
            if _outDatasetName is not None:
                return try_close_output_datasource(_ds[_outDatasetName], _ds)
            return is_success
        else:
            if _outDatasetName is not None:
                return try_close_output_datasource(None, _ds)
            return False


def smooth_vector(input_data, smoothness, out_data=None, out_dataset_name=None, progress=None, is_save_topology=False):
    """
    对矢量数据集进行光滑，支持线数据集、面数据集和网络数据集

    * 光滑的目的

        当折线或多边形的边界的线段过多时，就可能影响对原始特征的描述，不利用进一步的处理或分析，或显示和打印效果不够理想，因此需要对数据简化。简化的方法
        一般有重采样（:py:meth:`resample_vector`）和光滑。光滑是通过增加节点的方式使用曲线或直线段来代替原始折线的方法。需要注意，对折线进行光滑后，
        其长度通常会变短，折线上线段的方向也会发生明显改变，但两个端点的相对位置不会变化；面对象经过光滑后，其面积通常会变小。

    * 光滑方法与光滑系数的设置

        该方法采用 B 样条法对矢量数据集进行光滑。有关 B 样条法的介绍可参见 SmoothMethod 类。光滑系数（方法中对应 smoothness 参数）影响着光滑的程度，
        光滑系数越大，结果数据越光滑。光滑系数的建议取值范围为[2,10]。该方法支持对线数据集、面数据集和网络数据集进行光滑。

        * 对线数据集设置不同光滑系数的光滑效果：

        .. image:: ../image/Smooth_1.png

        * 对面数据集设置不同光滑系数的光滑效果：

        .. image:: ../image/Smooth_2.png

    :param input_data: 需要进行光滑处理的数据集，支持线数据集、面数据集和网络数据集
    :type input_data: DatasetVector or str
    :param int smoothness: 指定的光滑系数。取大于等于 2 的值有效，该值越大，线对象或面对象边界的节点数越多，也就越光滑。建议取值范围为[2,10]。
    :param out_data: 结果数据源所在半径，如果此参数为空，将直接对原始数据做光滑，也就是会改变原始数据。如果此参数不为空，将会先复制原始数据到此数据源中，
                     再对复制得到的数据集进行光滑处理。out_data 所指向数据源可以与源数据集所在的数据源相同。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称，当 out_data 不为空时才有效。
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :param bool is_save_topology: 是否保存对象拓扑关系
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector or str
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    if not isinstance(_source_input, DatasetVector):
        raise ValueError("source input_data must be DatasetVector")
    if out_data is not None:
        out_datasource = get_output_datasource(out_data)
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + "_Smooth"
        else:
            _outDatasetName = out_dataset_name
        _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
        result = out_datasource.copy_dataset(_source_input, _outDatasetName, None, progress=progress)
        if result is None:
            raise RuntimeError("Failed to copy dataset " + _source_input.name)
        _source_input = result
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, "smooth_vector")
                _source_input._jobject.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            is_success = _source_input._jobject.smooth(int(smoothness), bool(is_save_topology), listener is not None)
        except Exception as e:
            try:
                log_error(e)
                is_success = False
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _source_input._jobject.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if not is_success:
            _source_input = None
        if out_data is not None:
            return try_close_output_datasource(_source_input, out_datasource)
        return _source_input


def resample_vector(input_data, distance, resample_type=VectorResampleType.RTBEND, is_preprocess=True, tolerance=1e-10, is_save_small_geometry=False, out_data=None, out_dataset_name=None, progress=None, is_save_topology=False):
    """
    对矢量数据集进行重采样，支持线数据集、面数据集和网络数据集。 矢量数据重采样是按照一定规则剔除一些节点，以达到对数据进行简化的目的（如下图所示），
    其结果可能由于使用不同的重采样方法而不同。SuperMap 提供了两种重采样方法，具体参考 :py:class:`.VectorResampleType`

    .. image:: ../image/VectorResample.png

    该方法可以对线数据集、面数据集和网络数据集进行重采样。对面数据集重采样时，实质是对面对象的边界进行重采样。对于多个面对象的公共边界，如果进行了
    拓扑预处理只对其中一个多边形的该公共边界重采样一次，其他多边形的该公共边界会依据该多边形重采样的结果进行调整使之贴合，因此不会出现缝隙。

    注意: 重采样容限过大时，可能影响数据正确性，如出现两多边形的公共边界处出现相交的情况。

    :param input_data: 需要进行重采样的矢量数据集，支持线数据集、面数据集和网络数据集
    :type input_data: DatasetVector or str
    :param float distance: 设置重采样距离。单位与数据集坐标系单位相同。重采样距离可设置为大于 0 的浮点型数值。但如果设置的值小于默认值，将使用默认值。设置的重采样容限值越大，采样结果数据越简化
    :param resample_type: 重采样方法。重采样支持光栏采样算法和道格拉斯算法。具体参考 :py:class:`.VectorResampleType` 。默认使用光栏采样。
    :type resample_type: VectorResampleType or str
    :param bool is_preprocess: 是否进行拓扑预处理。只对面数据集有效，如果数据集不进行拓扑预处理，可能会导致缝隙，除非能确保数据中两个相邻面公共线部分的节点坐标完全一致。
    :param float tolerance: 进行拓扑预处理时的节点捕捉容限，单位与数据集单位相同。
    :param bool is_save_small_geometry: 是否保留小对象。小对象是指面积为0的对象，重采样过程有可能产生小对象。true 表示保留小对象，false 表示不保留。
    :param out_data: 结果数据源所在半径，如果此参数为空，将直接对原始数据做采样，也就是会改变原始数据。如果此参数不为空，将会先复制原始数据到此数据源中，
                     再对复制得到的数据集进行采样处理。out_data 所指向数据源可以与源数据集所在的数据源相同。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称，当 out_data 不为空时才有效。
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :param bool is_save_topology: 是否保存对象拓扑关系
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector or str
    """
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    if not isinstance(_source_input, DatasetVector):
        raise ValueError("source input_data must be DatasetVector")
    if out_data is not None:
        out_datasource = get_output_datasource(out_data)
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + "_resample"
        else:
            _outDatasetName = out_dataset_name
        _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
        result = out_datasource.copy_dataset(_source_input, _outDatasetName, None, progress=progress)
        if result is None:
            raise RuntimeError("Failed to copy dataset " + _source_input.name)
        _source_input = result
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, "resample_vector")
                _source_input._jobject.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            resample_parameter = get_jvm().com.supermap.data.ResampleInformation()
            resample_parameter.setResampleType(VectorResampleType._make(resample_type, VectorResampleType.RTBEND)._jobject)
            resample_parameter.setTolerance(float(distance))
            resample_parameter.setTopologyPreprocess(bool(is_preprocess))
            resample_parameter.setVertexInterval(float(tolerance))
            resample_parameter.setSaveTopology(bool(is_save_topology))
            is_success = _source_input._jobject.resample(resample_parameter, listener is not None, bool(is_save_small_geometry))
            resample_parameter.dispose()
        except Exception as e:
            try:
                log_error(e)
                is_success = False
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _source_input._jobject.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if not is_success:
            _source_input = None
        if out_data is not None:
            return try_close_output_datasource(_source_input, out_datasource)
        return _source_input


def create_thiessen_polygons(input_data, clip_region, field_stats=None, out_data=None, out_dataset_name=None, progress=None):
    """
    创建泰森多边形。
    荷兰气候学家 A.H.Thiessen 提出了一种根据离散分布的气象站的降雨量来计算平均降雨量的方法，即将所有相邻气象站连成三角形，作这些三角形各边的垂直平分线，
    于是每个气象站周围的若干垂直平分线便围成一个多边形。用这个多边形内所包含的一个唯一气象站的降雨强度来表示这个多边形区域内的降雨强度，并称这个多边形为泰森多边形。

    泰森多边形的特性:

        - 每个泰森多边形内仅含有一个离散点数据；
        - 泰森多边形内的点到相应离散点的距离最近；
        - 位于泰森多边形边上的点到其两边的离散点的距离相等。
        - 泰森多边形可用于定性分析、统计分析、邻近分析等。例如，可以用离散点的性质来描述泰森多边形区域的性质；可用离散点的数据来计算泰森多边形区域的数据
        - 判断一个离散点与其它哪些离散点相邻时，可根据泰森多边形直接得出，且若泰森多边形是n边形，则就与n个离散点相邻；当某一数据点落入某一泰森多边形中时，它与相应的离散点最邻近，无需计算距离。

    邻近分析是 GIS 领域里又一个最为基础的分析功能之一，邻近分析是用来发现事物之间的某种邻近关系。邻近分析类所提供的进行邻近分析的方法都是实现泰森多边形的建立，
    就是根据所提供的点数据建立泰森多边形，从而获得点之间的邻近关系。泰森多边形用于将点集合中的点的周围区域分配给相应的点，使位于这个点所拥有的区域（即该点所关联的泰森多边形）
    内的任何地点离这个点的距离都要比离其他点的距离要小，同时，所建立的泰森多边形还满足上述所有的泰森多边形法的理论。

    泰森多边形是如何创建的？利用下面的图示来理解泰森多边形建立的过程：

        - 对待建立泰森多边形的点数据进行由左向右，由上到下的扫描，如果某个点距离之前刚刚扫描过的点的距离小于给定的邻近容限值，那么分析时将忽略该点；
        - 基于扫描检查后符合要求的所有点建立不规则三角网，即构建 Delaunay 三角网；
        - 画出每个三角形边的中垂线，由这些中垂线构成泰森多边形的边，而中垂线的交点是相应的泰森多边形的顶点；
        - 用于建立泰森多边形的点的点位将成为相应的泰森多边形的锚点。

    :param input_data: 输入的点数据，可以为点数据集、点记录集或 :py:class:`.Point2D` 的列表
    :type input_data: DatasetVector or Recordset or list[Point2D]
    :param GeoRegion clip_region:  指定的裁剪结果数据的裁剪区域。该参数可以为空，如果为空，结果数据集将不进行裁剪
    :param field_stats:  统计字段名称和对应的统计类型，输入为一个list，list中存储的每个元素为tuple，tuple的大小为2，第一个元素为被统计的字段名称，第二个元素为统计类型。
                         当 stats_fields 为 str 时，支持设置 ',' 分隔多个字段，例如 "field1:SUM, field2:MAX, field3:MIN"
    :type field_stats: list[str,StatisticsType] or list[str,str] or str
    :param out_data: 结果面对象所在的数据源。如果 out_data 为空，则会将生成的泰森多边形面几何对象直接返回
    :type out_data:  Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称，当 out_data 不为空时才有效。
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 如果 out_data 为空，将返回 list[GeoRegion]，否则返回结果数据集或数据集名称。
    :rtype: DatasetVector or str or list[GeoRegion]
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    _jvm = get_jvm()
    points = None
    if isinstance(_source_input, (list, set, tuple)):
        points = _jvm.com.supermap.data.Point2Ds()
        for p in _source_input:
            p = Point2D.make(p)
            if isinstance(p, Point2D):
                points.add(p._jobject)

    else:
        if isinstance(_source_input, (DatasetVector, Recordset)):
            pass
        else:
            raise ValueError("Create thiessen polygon only support DatasetVector, Recordset and list points for input_data")
        fields = None
        statTypes = None
        if field_stats is not None:
            field_stats = split_input_list_tuple_item_from_str(field_stats)
            if isinstance(field_stats, list):
                fields = []
                statTypes = []
                for name, stat_type in field_stats:
                    fields.append(name)
                    statTypes.append(StatisticsType._make(stat_type))

        listener = None
        if progress is not None and safe_start_callback_server():
            try:
                listener = ProgressListener(progress, "create_thiessen_polygons")
                _jvm.com.supermap.analyst.spatialanalyst.ProximityAnalyst.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

            if clip_region is not None:
                java_clip_region = clip_region._jobject
            else:
                java_clip_region = None
            if out_data is not None:
                out_datasource = get_output_datasource(out_data)
                check_output_datasource(out_datasource)
                _jvm = get_jvm()
                if out_dataset_name is None:
                    _outDatasetName = "ThiessenPolygon"
        else:
            _outDatasetName = out_dataset_name
        _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
        try:
            try:
                if points is not None:
                    java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.ProximityAnalyst.createThiessenPolygon(points, out_datasource._jobject, _outDatasetName, java_clip_region)
                else:
                    if fields is None or statTypes is None:
                        java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.ProximityAnalyst.createThiessenPolygon(_source_input._jobject, out_datasource._jobject, _outDatasetName, java_clip_region)
                    else:
                        java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.ProximityAnalyst.createThiessenPolygon(_source_input._jobject, out_datasource._jobject, _outDatasetName, java_clip_region, to_java_string_array(fields), to_java_stattype_array(statTypes))
            except Exception as e:
                try:
                    log_error(e)
                    java_result_dt = None
                finally:
                    e = None
                    del e

        finally:
            if listener is not None:
                try:
                    _jvm.com.supermap.analyst.spatialanalyst.ProximityAnalyst.removeSteppedListener(listener)
                except Exception as e1:
                    try:
                        log_error(e1)
                    finally:
                        e1 = None
                        del e1

                close_callback_server()
            elif java_result_dt is not None:
                result_dt = out_datasource[java_result_dt.getName()]
            else:
                result_dt = None
            return try_close_output_datasource(result_dt, out_datasource)
            try:
                try:
                    if points is not None:
                        regions = _jvm.com.supermap.analyst.spatialanalyst.ProximityAnalyst.createThiessenPolygon(points, java_clip_region)
                    else:
                        regions = _jvm.com.supermap.analyst.spatialanalyst.ProximityAnalyst.createThiessenPolygon(_source_input._jobject, java_clip_region)
                except Exception as e:
                    try:
                        log_error(e)
                        regions = None
                    finally:
                        e = None
                        del e

            finally:
                return

            if listener is not None:
                try:
                    _jvm.com.supermap.analyst.spatialanalyst.ProximityAnalyst.removeSteppedListener(listener)
                except Exception as e1:
                    try:
                        log_error(e1)
                    finally:
                        e1 = None
                        del e1

                close_callback_server()
            if regions is not None:
                return list(map((lambda geo: Geometry._from_java_object(geo)), regions))
            return


def summary_points(input_data, radius, unit=None, stats=None, is_random_save_point=False, is_save_attrs=False, out_data=None, out_dataset_name=None, progress=None):
    """
    根据指定的距离抽稀点数据集，即用一个点表示指定距离范围内的所有点。 该方法支持不同的单位，并且可以选择点抽稀的方式，还可以对抽稀点原始点集做统计。
    在结果数据集 resultDatasetName 中，会新建SourceObjID 和 StatisticsObjNum 两个字段。SourceObjID 字段存储抽稀后得到的点对象在原始数据集
    中的 SmID, StatisticsObjNum 表示当前点所代表的所有点数目，包括被抽稀的点和其自身。

    :param input_data: 待抽稀的点数据集
    :type input_data: DatasetVector or str or Recordset
    :param float radius:  抽稀点的半径。任取一个坐标点，在此坐标点半径内的所有点坐标通过此点表示。需注意选择抽稀点的半径的单位。
    :param unit: 抽稀点半径的单位。
    :type unit: Unit or str
    :param stats: 对抽稀点原始点集做统计。需要设置统计的字段名，统计结果的字段名和统计模式。当该数组为空表示不做统计。当 stats 为 str 时，支持设置以 ';'
                  分隔多个 StatisticsField，每个 StatisticsField 使用 ',' 分隔 'source_field,stat_type,result_name'，例如：
                  'field1,AVERAGE,field1_avg; field2,MINVALUE,field2_min'
    :type stats: list[StatisticsField] or str
    :param bool is_random_save_point:  是否随机保存抽稀点。True表示从抽稀半径范围内的点集中随机取一个点保存，False表示取抽稀半径范围内点集中距点集内所有点的距离之和最小的点。
    :param bool is_save_attrs: 是否保留属性字段
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector or str
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    else:
        if not isinstance(_source_input, (DatasetVector, Recordset)):
            raise ValueError("source input_data must be DatasetVector or Recordset")
        elif radius < 0:
            raise ValueError("radius must be greater 0")
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            if isinstance(_source_input, Recordset):
                _outDatasetName = _source_input.dataset.name + "_summary"
            else:
                _outDatasetName = _source_input.name + "_summary"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, "summary_points")
                _jvm.com.supermap.analyst.spatialanalyst.ProximityAnalyst.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            statFields = []
            if stats is not None:
                if isinstance(stats, StatisticsField):
                    statFields.append(stats._jobject)
                else:
                    if isinstance(stats, (list, tuple, set)):
                        for item in stats:
                            if isinstance(item, StatisticsField):
                                statFields.append(item._jobject)

                    else:
                        if isinstance(stats, str):
                            tokens = stats.split(";")
                            for token in tokens:
                                keys = token.split(",")
                                if len(keys) == 3:
                                    statFields.append(StatisticsField(str(keys[0]), str(keys[1]), str(keys[2]))._jobject)

                        else:
                            raise ValueError("invalid stats type, required StatisticsField, (list,tuple,set of StatisticsField) or str")
            java_statFields = get_gateway().new_array(_jvm.com.supermap.analyst.spatialanalyst.StatisticsField, len(statFields))
            i = 0
            for item in statFields:
                java_statFields[i] = item
                i += 1

            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.ProximityAnalyst.summaryPoints_source_input._jobjectfloat(radius)Unit._make(unit, Unit.METER)._jobjectjava_statFields_ds._jobject_outDatasetNamebool(is_random_save_point)bool(is_save_attrs)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.ProximityAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def clip_vector(input_data, clip_region, is_clip_in_region=True, is_erase_source=False, out_data=None, out_dataset_name=None, progress=None):
    """
    对矢量数据集进行裁剪，结果存储为一个新的矢量数据集。

    :param input_data: 指定的要进行裁剪的矢量数据集，支持点、线、面、文本、CAD 数据集。
    :type input_data: DatasetVector or str
    :param GeoRegion  clip_region: 指定的裁剪区域
    :param bool is_clip_in_region: 指定是否对裁剪区内的数据集进行裁剪。若为 True，则对裁剪区域内的数据集进行裁剪，若为 False ，则对裁剪区域外的数据集进行裁剪。
    :param bool is_erase_source: 指定是否擦除裁剪区域，若为 True，表示对裁剪区域进行擦除，若为 False，则不对裁剪区域进行擦除。
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector or str
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    else:
        if not isinstance(_source_input, DatasetVector):
            raise ValueError("source input_data must be DatasetVector")
        elif clip_region is None:
            raise ValueError("clip_region is None")
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = input_data.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + "_clip"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, "clip_datasetvector")
                _jvm.com.supermap.analyst.spatialanalyst.VectorClip.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.VectorClip.clipDatasetVector(_source_input._jobject, clip_region._jobject, bool(is_clip_in_region), bool(is_erase_source), _ds._jobject, _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.VectorClip.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def simplify_building(source_data, width_threshold, height_threshold, save_failed=False, out_data=None, out_dataset_name=None):
    """
    面对象的直角多边形拟合
    如果一串连续的节点到最小面积外接矩形的下界的距离大于 height_threshold，且节点的总宽度大于 width_threshold，则对连续节点进行拟合。

    :param source_data: 需要处理的面数据集
    :type source_data: DatasetVector or str
    :param float width_threshold: 点到最小面积外接矩形的左右边界的阈值
    :param float height_threshold: 点到最小面积外接矩形的上下边界的阈值
    :param bool save_failed: 面对象进行直角化失败时，是否保存源面对象，如果为 False，则结果数据集中不含失败的面对象。
    :param out_data: 用于存储结果数据集的数据源。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :return: 结果数据集或数据集名称
    :rtype:  DatasetVector or str
    """
    check_lic()
    _source_input = get_input_dataset(source_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    if not isinstance(_source_input, DatasetVector):
        raise ValueError("source input_data must be DatasetVector")
    if not width_threshold > 0:
        raise ValueError("width_threshold must be greater than 0")
    else:
        if not height_threshold > 0:
            raise ValueError("height_threshold must be greater than 0")
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = source_data.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + "_simplify"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    try:
        try:
            java_result_dt = get_jvm().com.supermap.jsuperpy.Utils.simplifyBuilding(oj(_source_input), oj(_ds), _outDatasetName, float(width_threshold), float(height_threshold), not save_failed)
        except Exception as e:
            try:
                import traceback
                log_error(traceback.format_exc())
                java_result_dt = False
            finally:
                e = None
                del e

    finally:
        if java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def update_attributes(source_data, target_data, spatial_relation, update_fields, interval=1e-06):
    """
    矢量数据集属性更新，将 source_data 中的属性，根据 spatial_relation 指定的空间关系，更新到 target_data 数据集中。
    例如，有一份点数据和面数据，需要将点数据集中的属性值取平均值，然后将值写到包含点的面对象中，可以通过以下代码实现::

    >>> result = update_attributes('ds/points', 'ds/zones', 'WITHIN', [('trip_distance', 'mean'), ('', 'count')])

    spatial_relation 参数是指源数据集（ source_data）对目标被更新数据集（target_data）的空间关系。

    :param source_data: 源数据集。源数据集提供属性数据，将源数据集中的属性值根据空间关系更新到目标数据集中。
    :type source_data:  DatasetVector or str
    :param target_data: 目标数据集。被写入属性数据的数据集。
    :type target_data: DatasetVector or str
    :param spatial_relation: 空间关系类型，源数据（查询对象）对目标数据（被查询对象）的空间关系，具体参考 :py:class:`SpatialQueryMode`
    :type spatial_relation: SpatialQueryMode or str
    :param update_fields: 字段统计信息，可能有多个源数据中对象与目标数据对象满足空间关系，需要对源数据的属性字段值进行汇总统计，将统计的结果写入到目标数据集中
                          为一个list，list中每个元素为一个 tuple，tuple的大小为2，tuple的第一个元素为被统计的字段名称，tuple的第二个元素为统计类型。
    :type update_fields: list[tuple(str,AttributeStatisticsMode)] or list[tuple(str,str)] or str
    :param interval: 节点容限
    :type interval: float
    :return: 是否属性更新成功。更新成功返回 True，否则返回 False。
    :rtype: bool
    """
    check_lic()
    _updated_input = get_input_dataset(target_data)
    if not isinstance(_updated_input, DatasetVector):
        raise ValueError("target_data must be DatasetVector, but is " + str(type(target_data)))
    _attribute_input = get_input_dataset(source_data)
    if not isinstance(_attribute_input, DatasetVector):
        raise ValueError("source_data must be DatasetVector, but is " + str(type(source_data)))
    spatial_relation = SpatialQueryMode._make(spatial_relation)
    stat_fields = None
    stat_modes = None
    if update_fields is not None:
        stats = split_input_list_tuple_item_from_str(update_fields)
        if isinstance(stats, list):
            stat_fields = []
            stat_modes = []
            for name, stat_mode in stats:
                stat_mode = AttributeStatisticsMode._make(stat_mode)
                if stat_mode is not None and stat_mode is not AttributeStatisticsMode.MAXINTERSECTAREA:
                    stat_fields.append(name)
                    stat_modes.append(oj(stat_mode))

    try:
        try:
            result = get_jvm().com.supermap.jsuperpy.UpdateAttributes.updateAttributes(oj(_attribute_input), oj(_updated_input), oj(spatial_relation), stat_fields, stat_modes, interval)
        except Exception as e:
            try:
                import traceback
                log_error(traceback.format_exc())
                result = False
            finally:
                e = None
                del e

    finally:
        return

    return result


def resample_raster(input_data, new_cell_size, resample_mode, out_data=None, out_dataset_name=None, progress=None):
    """
    栅格数据重采样，返回结果数据集。

    栅格数据经过了配准或纠正、投影等几何操作后，栅格的像元中心位置通常会发生变化，其在输入栅格中的位置不一定是整数的行列号，因此需要根据输出栅格上每个格子在输入栅格中的位置，对输入栅格按一定规则进行重采样，进行栅格值的插值计算，建立新的栅格矩阵。不同分辨率的栅格数据之间进行代数运算时，需要将栅格大小统一到一个指定的分辨率上，此时也需要对栅格进行重采样。

    栅格重采样有三种常用方法：最邻近法、双线性内插法和三次卷积法。有关这三种重采样方法较为详细的介绍，请参见 ResampleMode 类。

    :param input_data:  指定的用于栅格重采样的数据集。支持影像数据集，包括多波段影像
    :type input_data: DatasetImage or DatasetGrid or str
    :param float new_cell_size: 指定的结果栅格的单元格大小
    :param resample_mode: 重采样计算方法
    :type resample_mode: ResampleMode or str
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetImage or DatasetGrid or str
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    else:
        if not isinstance(_source_input, (DatasetGrid, DatasetImage)):
            raise ValueError("source input_data required DatasetGrid or DatasetImage")
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + "_resample"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, "resample_raster")
                _jvm.com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.resample(_source_input._jobject, float(new_cell_size), RasterResampleMode._make(resample_mode)._jobject, _ds._jobject, _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


class ReclassSegment(object):
    __doc__ = "\n    栅格重分级区间类。该类主要用于重分级区间信息的相关设置，包括区间的起始值、终止值等。\n\n    该类用于设置在进行重分级时，重分级映射表中每个重分级区间的参数，重分级类型不同，需要设置的属性也有所不同。\n\n    - 当重分级类型为单值重分级时，需要通过 :py:meth:`set_start_value` 方法指定需要被重新赋值的源栅格的单值，并通过 :py:meth:`set_new_value` 方法设置该值对应的新值。\n    - 当重分级类型为范围重分级时，需要通过 :py:meth:`set_start_value` 方法指定需要重新赋值的源栅格值区间的起始值，通过 :py:meth:`set_end_value` 方法设置区间的终止值，\n      并通过 :py:meth:`set_new_value` 方法设置该区间对应的新值，还可以由 :py:meth:`set_segment_type` 方法设置区间类型是“左开右闭”还是“左闭右开”。\n\n    "

    def __init__(self, start_value=None, end_value=None, new_value=None, segment_type=None):
        """
        构造栅格重分级区间对象

        :param float start_value:  栅格重分级区间的起始值
        :param float end_value: 栅格重分级区间的终止值
        :param float new_value: 栅格重分级的区间值或旧值对应的新值
        :param segment_type:  栅格重分级区间类型
        :type segment_type: ReclassSegmentType or str
        """
        self._endValue = None
        self._startValue = None
        self._newValue = None
        self._segmentType = None
        self.set_start_value(start_value).set_end_value(end_value).set_new_value(new_value).set_segment_type(segment_type)

    def set_segment_type(self, value):
        """
        设置栅格重分级区间类型

        :param value: 栅格重分级区间类型
        :type value: ReclassSegmentType or str
        :return: self
        :rtype: ReclassSegment
        """
        self._segmentType = ReclassSegmentType._make(value)
        return self

    @property
    def end_value(self):
        """float: 栅格重分级区间的终止值"""
        return self._endValue

    def set_start_value(self, value):
        """
        设置栅格重分级区间的起始值

        :param float value: 栅格重分级区间的起始值
        :return: self
        :rtype: ReclassSegment
        """
        if value is not None:
            self._startValue = float(value)
        return self

    def set_new_value(self, value):
        """
        栅格重分级的区间值或旧值对应的新值

        :param float value: 栅格重分级的区间值或旧值对应的新值
        :return: self
        :rtype: ReclassSegment
        """
        if value is not None:
            self._newValue = float(value)
        return self

    @property
    def start_value(self):
        """float: 栅格重分级区间的起始值"""
        return self._startValue

    def set_end_value(self, value):
        """
        栅格重分级区间的终止值

        :param float value: 栅格重分级区间的终止值
        :return: self
        :rtype: ReclassSegment
        """
        if value is not None:
            self._endValue = float(value)
        return self

    @property
    def new_value(self):
        """float: 栅格重分级的区间值或旧值对应的新值"""
        return self._newValue

    @property
    def segment_type(self):
        """ReclassSegmentType: 栅格重分级区间类型"""
        return self._segmentType

    @property
    def _jobject(self):
        """Py4J 映射的 Java 对象"""
        java_obj = get_jvm().com.supermap.analyst.spatialanalyst.ReclassSegment()
        if self.segment_type is not None:
            java_obj.setSegmentType(self.segment_type._jobject)
        if self.start_value is not None:
            java_obj.setStartValue(self.start_value)
        if self.new_value is not None:
            java_obj.setNewValue(self.new_value)
        if self.end_value is not None:
            java_obj.setEndValue(self.end_value)
        return java_obj

    def to_dict(self):
        """
        将当前对象信息输出到 dict

        :return: 包含当前对象信息的 dict 对象
        :rtype: dict
        """
        d = dict()
        if self.end_value is not None:
            d["end_value"] = self.end_value
        if self.start_value is not None:
            d["start_value"] = self.start_value
        if self.new_value is not None:
            d["new_value"] = self.new_value
        if self.segment_type is not None:
            d["segment_type"] = self.segment_type.name
        return d

    @staticmethod
    def make_from_dict(values):
        """
        从dict中读取信息构造 ReclassSegment 对象

        :param values: 包含 ReclassSegment 信息的 dict
        :type values: dict
        :return: 栅格重分级区间对象
        :rtype: ReclassSegment
        """
        return ReclassSegment().from_dict(values)

    def from_dict(self, values):
        """
        从dict中读取信息

        :param values: 包含 ReclassSegment 信息的 dict
        :type values: dict
        :return: self
        :rtype: ReclassSegment
        """
        if "end_value" in values.keys():
            self.set_end_value(values["end_value"])
        if "start_value" in values.keys():
            self.set_start_value(values["start_value"])
        if "new_value" in values.keys():
            self.set_new_value(values["new_value"])
        if "segment_type" in values.keys():
            self.set_segment_type(values["segment_type"])
        return self


def _to_java_reclass_segment_array(values):
    if values is None:
        return
    if isinstance(values, ReclassSegment):
        java_array = get_gateway().new_array(get_jvm().com.supermap.analyst.spatialanalyst.ReclassSegment, 1)
        java_array[0] = values._jobject
        return java_array
    if isinstance(values, (list, tuple, set)):
        _size = len(values)
        java_array = get_gateway().new_array(get_jvm().com.supermap.analyst.spatialanalyst.ReclassSegment, _size)
        i = 0
        for value in values:
            java_array[i] = value._jobject
            i += 1

        return java_array
    return


class ReclassMappingTable(object):
    __doc__ = "\n    栅格重分级映射表类。提供对源栅格数据集进行单值或范围的重分级，且包含对无值数据和未分级单元格的处理。\n\n    重分级映射表，用于说明源数据和结果数据值之间的对应关系。这种对应关系由这几部分内容表达：重分级类型、重分级区间集合、无值和未分级数据的处理。\n\n    - 重分级的类型\n      重分级有两种类型，单值重分级和范围重分级。单值重分级是对指定的某些单值进行重新赋值，如将源栅格中值为100的单元格，赋值为1输出到结果\n      栅格中；范围重分级将一个区间内的值重新赋值为一个值，如将源栅格中栅格值在[100,500)范围内的单元格，重新赋值为200输出到结果栅格中。通过该类的 :py:meth:`set_reclass_type` 方法来设置重分级类型。\n\n    - 重分级区间集合\n      重分级的区间集合规定了源栅格某个栅格值或者一定区间内的栅格值与重分级后的新值的对应关系，通过该类的  :py:meth:`set_segments` 方法设置。\n      该集合由若干重分级区间（ReclassSegment）对象构成。该对象用于设置每个重分级区间的信息，包括要重新赋值的源栅格单值或区间的起始值、终止值，重分级区间的类型，\n      以及栅格重分级的区间值或源栅格单值对应的新值等，详见 :py:class:`.ReclassSegment` 类。\n\n    - 无值和未分级数据的处理\n      对源栅格数据中的无值，可以通过该类的 :py:meth:`set_retain_no_value` 方法来设置是否保持无值，如果为 False，即不保持为无值，则可通过 :py:meth:`set_change_no_value_to` 方法为无值数据指定一个值。\n\n      对在重分级映射表中未涉及的栅格值，可以通过该类的 :py:meth:`set_retain_missing_value` 方法来设置是否保持其原值，如果为 False，即不保持原值，则可通过 :py:meth:`set_change_missing_valueT_to` 方法为其指定一个值。\n\n    此外，该类还提供了将重分级映射表数据导出为 XML 字符串及 XML 文件的方法和导入 XML 字符串或文件的方法。当多个输入的栅格数据需要应用相同的分级范围时，可以将其导出为重分级映射表文件，\n    当对后续数据进行分级时，直接导入该重分级映射表文件，进而可以批量处理导入的栅格数据。有关栅格重分级映射表文件的格式和标签含义请参见 to_xml 方法。\n\n\n    "

    def __init__(self):
        self._retainMissingValue = None
        self._changeNoValueTo = None
        self._changeMissingValueTo = None
        self._segments = []
        self._retainNoValue = None
        self._reclassType = None

    @property
    def is_retain_missing_value(self):
        """bool: 源数据集中不在指定区间或单值之外的数据是否保留原值"""
        return self._retainMissingValue

    def set_change_missing_value_to(self, value):
        """
        设置不在指定区间或单值内的栅格的指定值。如果 :py:meth:`is_retain_no_value` 为 True 时，则该设置无效。

        :param float value: 不在指定区间或单值内的栅格的指定值
        :return: self
        :rtype: ReclassMappingTable
        """
        self._changeMissingValueTo = float(value)
        return self

    def set_retain_missing_value(self, value):
        """
        设置源数据集中不在指定区间或单值之外的数据是否保留原值。

        :param bool value:  源数据集中不在指定区间或单值之外的数据是否保留原值。
        :return: self
        :rtype: ReclassMappingTable
        """
        self._retainMissingValue = value
        return self

    @property
    def change_no_value_to(self):
        """float: 返回无值数据的指定值"""
        return self._changeNoValueTo

    @property
    def change_missing_value_to(self):
        """float: 返回不在指定区间或单值内的栅格的指定值。"""
        if self._changeMissingValueTo is not None:
            return float(self._changeMissingValueTo)

    def set_change_no_value_to(self, value):
        """
        设置无值数据的指定值。:py:meth:`is_retain_no_value` 为 True 时，该设置无效。

        :param float value: 无值数据的指定值
        :return: self
        :rtype: ReclassMappingTable
        """
        if value is not None:
            self._changeNoValueTo = float(value)
        return self

    @property
    def segments(self):
        """list[ReclassSegment]: 返回重分级区间集合。 每一个 ReclassSegment 就是一个区间范围或者是一个旧值和一个新值的对应关系。"""
        return self._segments

    @property
    def is_retain_no_value(self):
        """bool: 返回是否将源数据集中的无值数据保持为无值。 """
        return self._retainNoValue

    def set_segments(self, value):
        """
        设置重分级区间集合

        :param value: 重分级区间集合。当 value 为 str 时，支持使用 ';' 分隔多个ReclassSegment，每个 ReclassSegment使用 ','分隔 起始值、终止值、新值和分区类型。例如:
                        '0,100,50,CLOSEOPEN; 100,200,150,CLOSEOPEN'
        :type value: list[ReclassSegment] or str
        :return: self
        :rtype: ReclassMappingTable
        """
        if value is not None:
            if isinstance(value, (list, tuple)):
                self._segments = list(value)
            else:
                if isinstance(value, str):
                    segs = value.split(";")
                    self._segments = []
                    for seg in segs:
                        items = seg.split(",")
                        if len(items) == 4:
                            self._segments.append(ReclassSegment(float(items[0]), float(items[1]), float(items[2]), str(items[3])))
                        else:
                            items = seg.split(" ")
                        if len(items) == 4:
                            self._segments.append(ReclassSegment(float(items[0]), float(items[1]), float(items[2]), str(items[3])))

        return self

    @property
    def reclass_type(self):
        """ReclassType: 返回栅格重分级类型"""
        return self._reclassType

    def set_reclass_type(self, value):
        """
        设置栅格重分级类型

        :param value: 栅格重分级类型，默认值为 UNIQUE
        :type value: ReclassType or str
        :return: self
        :rtype: ReclassMappingTable
        """
        self._reclassType = ReclassType._make(value)
        return self

    def set_retain_no_value(self, value):
        """
        设置是否将源数据集中的无值数据保持为无值。设置是否将源数据集中的无值数据保持为无值。
        - 当 set_retain_no_value 方法设置为 True 时，表示保持源数据集中的无值数据为无值；
        - 当 set_retain_no_value 方法设置为 False 时，表示将源数据集中的无值数据设置为指定的值（ :py:meth:`set_change_no_value_to` ）

        :param bool value:
        :return: self
        :rtype: ReclassMappingTable
        """
        self._retainNoValue = value
        return self

    @property
    def _jobject(self):
        """Py4J 映射的 Java 对象"""
        java_obj = get_jvm().com.supermap.analyst.spatialanalyst.ReclassMappingTable()
        if self.change_missing_value_to is not None:
            java_obj.setChangeMissingValueTo(float(self.change_missing_value_to))
        if self.is_retain_missing_value is not None:
            java_obj.setRetainMissingValue(self.is_retain_missing_value)
        if self.change_no_value_to is not None:
            java_obj.setChangeNoValueTo(self.change_no_value_to)
        if self.segments is not None:
            java_obj.setSegments(_to_java_reclass_segment_array(self.segments))
        if self.reclass_type is not None:
            java_obj.setReclassType(self.reclass_type._jobject)
        if self.is_retain_no_value is not None:
            java_obj.setRetainNoValue(self.is_retain_no_value)
        return java_obj

    @staticmethod
    def _from_java_object(java_obj):
        rel = ReclassMappingTable()
        rel.set_retain_no_value(java_obj.isRetainNoValue())
        rel.set_retain_missing_value(java_obj.isRetainMissingValue())
        rel.set_reclass_type(java_obj.getReclassType().name())
        rel.set_change_no_value_to(java_obj.getChangeNoValueTo())
        rel.set_change_missing_value_to(java_obj.getChangeMissingValueTo())
        java_segments = java_obj.getSegments()
        if java_segments is not None:
            segments = []
            for java_seg in java_segments:
                segments.append(ReclassSegment(java_seg.getStartValue(), java_seg.getEndValue(), java_seg.getNewValue(), java_seg.getSegmentType().name()))

            rel.set_segments(segments)
        return rel

    def to_dict(self):
        """
        将当前信息输出到 dict 中

        :return: 包含当前信息的字典对象
        :rtype: dict
        """
        d = dict()
        if self.is_retain_missing_value is not None:
            d["is_retain_missing_value"] = self.is_retain_missing_value
        if self.change_no_value_to is not None:
            d["change_no_value_to"] = self.change_no_value_to
        if self.change_missing_value_to is not None:
            d["change_missing_value_to"] = self.change_missing_value_to
        if self.segments is not None:
            d["segments"] = self.segments
        if self.is_retain_no_value is not None:
            d["is_retain_no_value"] = self.is_retain_no_value
        if self.reclass_type is not None:
            d["reclass_type"] = self.reclass_type
        return d

    @staticmethod
    def make_from_dict(values):
        """
        从 dict 对象中读取重分级映射表信息构造新的对象

        :param dict values: 包含重分级映射表信息的 dict 对象
        :return: 重分级映射表对象
        :rtype: ReclassMappingTable
        """
        return ReclassMappingTable().from_dict(values)

    def from_dict(self, values):
        """
        从 dict 对象中读取重分级映射表信息

        :param dict values: 包含重分级映射表信息的 dict 对象
        :return: self
        :rtype: ReclassMappingTable
        """
        if "is_retain_missing_value" in values.keys():
            self.set_retain_missing_value(values["is_retain_missing_value"])
        if "change_no_value_to" in values.keys():
            self.set_change_no_value_to(values["change_no_value_to"])
        if "change_missing_value_to" in values.keys():
            self.set_change_missing_value_to(values["change_missing_value_to"])
        if "segments" in values.keys():
            self.set_segments(values["segments"])
        if "is_retain_no_value" in values.keys():
            self.set_retain_no_value(values["is_retain_no_value"])
        if "reclass_type" in values.keys():
            self.set_reclass_type(values["reclass_type"])
        return self

    def to_xml(self):
        """
        将当前对象信息输出为 xml 字符串

        :return: xml 字符串
        :rtype: str
        """
        return self._jobject.toXml()

    def to_xml_file(self, xml_file):
        """
        该方法用于将对重分级映射表对象的参数设置写入一个 XML 文件，称为栅格重分级映射表文件，其后缀名为 .xml，下面是一个栅格重分级映射表文件的例子：

        重分级映射表文件中各标签的含义如下：

        - <SmXml:ReclassType></SmXml:ReclassType> 标签：重分级类型。1表示单值重分级，2表示范围重分级。
        - <SmXml:SegmentCount></SmXml:SegmentCount> 标签：重分级区间集合，count 参数表示重分级的级数。
        - <SmXml:Range></SmXml:Range> 标签：重分级区间，重分级类型为单值重分级，格式为：区间起始值--区间终止值：新值-区间类型。对于区间类型，0表示左开右闭，1表示左闭右开。
        - <SmXml:Unique></SmXml:Unique> 标签：重分级区间，重分级类型为范围重分级，格式为：原值：新值。
        - <SmXml:RetainMissingValue></SmXml:RetainMissingValue> 标签：未分级单元格是否保留原值。0表示不保留，1表示保留。
        - <SmXml:RetainNoValue></SmXml:RetainNoValue> 标签：无值数据是否保持无值。0表示不保持，0表示不保持。
        - <SmXml:ChangeMissingValueTo></SmXml:ChangeMissingValueTo> 标签：为未分级单元格的指定的值。
        - <SmXml:ChangeNoValueTo></SmXml:ChangeNoValueTo> 标签：为无值数据的指定的值。

        :param str xml_file: xml 文件路径
        :type xml_file:
        :return: 导出成功返回 True，否则返回 False
        :rtype: bool
        """
        return self._jobject.toXmlFile(xml_file)

    @staticmethod
    def from_xml(xml):
        """
        从存储在XML格式字符串中的参数值导入到映射表数据中，并返回一个新的对象。

        :param str xml: XML格式字符串
        :return:  栅格重分级映射表对象
        :rtype: ReclassMappingTable
        """
        java_obj = get_jvm().com.supermap.analyst.spatialanalyst.ReclassMappingTable()
        if java_obj.fromXml(xml):
            return ReclassMappingTable._from_java_object(java_obj)
        return

    @staticmethod
    def from_xml_file(xml_file):
        """
        从已保存的XML格式的映射表文件中导入映射表数据，并返回一个新的对象。

        :param str xml_file: XML文件
        :return:  栅格重分级映射表对象
        :rtype: ReclassMappingTable
        """
        java_obj = get_jvm().com.supermap.analyst.spatialanalyst.ReclassMappingTable()
        if java_obj.fromXmlFile(xml_file):
            return ReclassMappingTable._from_java_object(java_obj)
        return


def reclass_grid(input_data, re_pixel_format, segments=None, reclass_type='UNIQUE', is_retain_no_value=True, change_no_value_to=None, is_retain_missing_value=False, change_missing_value_to=None, reclass_map=None, out_data=None, out_dataset_name=None, progress=None):
    """
    栅格数据重分级，返回结果栅格数据集。
    栅格重分级就是对源栅格数据的栅格值进行重新分类和按照新的分类标准赋值，其结果是用新的值取代了栅格数据的原栅格值。对于已知的栅格数据，有时为了便于看清趋势，找出栅格值的规律，或者为了方便进一步的分析，重分级是很必要的：

        - 通过重分级，可以使用新值来替代单元格的旧值，以达到更新数据的目的。例如，在处理土地类型变更时，将已经开垦为耕地的荒地赋予新的栅格值；
        - 通过重分级，可以对大量的栅格值进行分组归类，同组的单元格赋予相同的值来简化数据。例如，将旱地、水浇地、水田等都归为农业用地；
        - 通过重分级，可以对多种栅格数据按照统一的标准进行分类。例如，某个建筑物的选址的影响因素包括土壤和坡度，则对输入的土壤类型和坡度的栅格数据，可以按照 1-10 的等级标准来进行重分级，便于进一步的选址分析；
        - 通过重分级，可以将某些不希望参与分析的单元格设为无值，也可以为原先为无值的单元格补充新测定的值，便于进一步的分析处理。

    例如，常常需要对栅格表面进行坡度分析得到坡度数据，来辅助与地形有关的分析。但我们可能需要知道坡度属于哪个等级而不是具体的坡度数值，来帮助我们了解地形的陡峭程度，从而辅助进一步的分析，如选址、分析道路铺设线路等。此时可以使用重分级，将不同的坡度划分到对应的等级中。

    :param input_data:  指定的用于栅格重采样的数据集。支持影像数据集，包括多波段影像
    :type input_data: DatasetImage or DatasetGrid or str
    :param re_pixel_format: 结果数据集的栅格值的存储类型
    :type re_pixel_format: ReclassPixelFormat
    :param segments: 重分级区间集合。重分级区间集合。当 segments 为 str 时，支持使用 ';' 分隔多个ReclassSegment，每个 ReclassSegment使用 ','分隔 起始值、终止值、新值和分区类型。例如: '0,100,50,CLOSEOPEN; 100,200,150,CLOSEOPEN'
    :type segments: list[ReclassSegment] or str
    :param reclass_type: 栅格重分级类型
    :type reclass_type: ReclassType or str
    :param bool is_retain_no_value: 是否将源数据集中的无值数据保持为无值
    :param float change_no_value_to: 无值数据的指定值。 is_retain_no_value 设置为 False 时，该设置有效，否则无效。
    :param bool is_retain_missing_value: 源数据集中不在指定区间或单值之外的数据是否保留原值
    :param float change_missing_value_to: 不在指定区间或单值内的栅格的指定值，is_retain_no_value 设置为 False 时，该设置有效，否则无效。
    :param ReclassMappingTable reclass_map: 栅格重分级映射表类。如果该对象不为空，使用该对象设置的值进行栅格重分级。
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetGrid or DatasetImage or str
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    else:
        if not isinstance(_source_input, (DatasetGrid, DatasetImage)):
            raise ValueError("source input_data required DatasetGrid or DatasetImage")
        else:
            if out_data is not None:
                out_datasource = get_output_datasource(out_data)
                _ds = out_datasource
            else:
                _ds = _source_input.datasource
            check_output_datasource(_ds)
            if out_dataset_name is None:
                _outDatasetName = _source_input.name + "_reclass"
            else:
                _outDatasetName = out_dataset_name
        _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
        _jvm = get_jvm()
        if reclass_map is not None:
            java_reclassMap = reclass_map._jobject
        else:
            java_reclassMap = ReclassMappingTable().set_change_missing_value_to(change_missing_value_to).set_change_no_value_to(change_no_value_to).set_reclass_type(reclass_type).set_retain_missing_value(is_retain_missing_value).set_retain_no_value(is_retain_no_value).set_segments(segments)._jobject
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, "reclass_grid")
                _jvm.com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.reclass(_source_input._jobject, java_reclassMap, ReclassPixelFormat._make(re_pixel_format)._jobject, _ds._jobject, _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def aggregate_grid(input_data, scale, aggregation_type, is_expanded, is_ignore_no_value, out_data=None, out_dataset_name=None, progress=None):
    """

    栅格数据聚合，返回结果栅格数据集。
    栅格聚合操作是以整数倍缩小栅格分辨率，生成一个新的分辨率较粗的栅格的过程。此时，每个像元由原栅格数据的一组像元聚合而成，其值由其包含的原栅格的值共
    同决定，可以取包含栅格的和、最大值、最小值、平均值、中位数。如缩小n（n为大于1的整数）倍，则聚合后栅格的行、列的数目均为原栅格的1/n，也就是单元格
    大小是原来的n倍。聚合可以通过对数据进行概化，达到清除不需要的信息或者删除微小错误的目的。

    注意：如果原栅格数据的行列数不是 scale 的整数倍，使用 is_expanded 参数来处理零头。

    - is_expanded 为 true，则在零头加上一个数，使之成为一个整数倍，扩大的范围其栅格值均为无值，因此，结果数据集的范围会比原始的大一些。

    - is_expanded 为 false，去掉零头，结果数据集的范围会比原始的小一些。

    :param input_data: 指定的进行聚合操作的栅格数据集。
    :type input_data: DatasetGrid or str
    :param int scale: 指定的结果栅格与输入栅格之间栅格大小的比例。取值为大于 1 的整型数值。
    :param aggregation_type: 聚合操作类型
    :type aggregation_type: AggregationType
    :param bool is_expanded: 指定是否处理零头。当原栅格数据的行列数不是 scale 的整数倍时，栅格边界处则会出现零头。
    :param bool is_ignore_no_value:  在聚合范围内含有无值数据时聚合操作的计算方式。如果为 True，使用聚合范围内除无值外的其余栅格值来计算；如果为 False，则聚合结果为无值。
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetGrid or str
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    else:
        if not isinstance(_source_input, DatasetGrid):
            raise ValueError("source input_data must be DatasetGrid")
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + "_aggregate"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, "aggregate_grid")
                _jvm.com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.aggregate(_source_input._jobject, int(scale), AggregationType._make(aggregation_type)._jobject, bool(is_expanded), bool(is_ignore_no_value), _ds._jobject, _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def slice_grid(input_data, number_zones, base_output_zones, out_data=None, out_dataset_name=None, progress=None):
    """
    自然分割重分级，适用于分布不均匀的数据。

    Jenks自然间断法:

    该重分级方法利用的是Jenks自然间断法。Jenks自然间断法基于数据中固有的自然分组，这是方差最小化分级的形式，间断通常不均匀，且间断 选择在值出现剧
    烈变动的地方，所以该方法能对相似值进行恰当分组并可使各分级间差异最大化。Jenks间断点分级法会将相似值（聚类值）放置在同一类中，所以该方法适用于
    分布不均匀的数据值。

    :param input_data: 指定的进行重分级操作的栅格数据集。
    :type input_data: DatasetGrid or str
    :param int number_zones: 将栅格数据集重分级的区域数量。
    :param int base_output_zones:  结果栅格数据集中最低区域的值
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetGrid or str

    设置分级区域数为9,将待分级栅格数据的最小值到最大值自然分割为9份。最低区域值设为1，重分级后的值以1为起始值每级递增。

    >>> slice_grid('E:/data.udb/DEM', 9, 1, 'E:/Slice_out.udb')

    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    else:
        if not isinstance(_source_input, DatasetGrid):
            raise ValueError("source input_data must be DatasetGrid")
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + "_Slice"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, "slice_grid")
                _jvm.com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.slice(_source_input._jobject, _ds._jobject, _outDatasetName, int(number_zones), int(base_output_zones))
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def compute_range_raster(input_data, count, progress=None):
    """
    计算栅格像元值的自然断点中断值

    :param input_data: 栅格数据集
    :type input_data: DatasetGrid or str
    :param count: 自然分段的个数
    :type count: int
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 自然分段的中断值（包括像元的最大和最小值）
    :rtype: Array
    """
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    if not isinstance(_source_input, DatasetGrid):
        raise ValueError("source input_data must be DatasetGrid")
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, "compute_range_raster")
                _jvm.com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            java_result_arr = _jvm.com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.ComputeRange(_source_input._jobject, int(count))
        except Exception as e:
            try:
                log_error(e)
                java_result_arr = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if java_result_arr is not None:
            result_arr = java_result_arr
            return result_arr
        return


def compute_range_vector(input_data, value_field, count, progress=None):
    """
    计算矢量自然断点中断值

    :param input_data: 矢量数据集
    :type input_data: DatasetVector or str
    :param value_field: 分段的标准字段
    :type value_field: str
    :param count: 自然分段的个数
    :type count: int
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 自然分段的中断值（包括属性的最大和最小值）
    :rtype: Array
    """
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    if not isinstance(_source_input, DatasetVector):
        raise ValueError("source input_data must be DatasetVector")
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, "compute_range_vector")
                _jvm.com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            java_result_arr = _jvm.com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.ComputeRange(_source_input._jobject, str(value_field), int(count))
        except Exception as e:
            try:
                log_error(e)
                java_result_arr = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if java_result_arr is not None:
            result_arr = java_result_arr
            return result_arr
        return


class NeighbourShape:
    __doc__ = "邻域形状基类。邻域按照形状可分为：矩形邻域、圆形邻域、环形邻域和扇形邻域。邻域形状的相关参数设置"

    def __init__(self):
        self._shape_type = None

    @property
    def shape_type(self):
        """NeighbourShapeType: 域分析的邻域形状类型"""
        return self._shape_type


class NeighbourShapeRectangle(NeighbourShape):
    __doc__ = "矩形邻域形状类"

    def __init__(self, width, height):
        """
        构造矩形邻域形状类对象

        :param float width: 矩形邻域的宽
        :param float height: 矩形邻域的高
        """
        NeighbourShape.__init__(self)
        self._width = 0.0
        self._height = 0.0
        self.set_width(width).set_height(height)
        self._shape_type = NeighbourShapeType.RECTANGLE

    @property
    def width(self):
        """float: 矩形邻域的宽"""
        return self._width

    def set_width(self, value):
        """
        设置矩形邻域的宽

        :param float value: 矩形邻域的宽
        :return: self
        :rtype:  NeighbourShapeRectangle
        """
        self._width = float(value)
        return self

    @property
    def height(self):
        """float: 矩形邻域的高"""
        return self._height

    def set_height(self, value):
        """
        设置矩形邻域的高

        :param float value:  矩形邻域的高
        :return: self
        :rtype:  NeighbourShapeRectangle
        """
        self._height = float(value)
        return self

    @property
    def _jobject(self):
        """Py4J 映射的 Java 对象"""
        java_obj = get_jvm().com.supermap.analyst.spatialanalyst.NeighbourShapeRectangle()
        java_obj.setWidth(self.width)
        java_obj.setHeight(self.height)
        return java_obj


class NeighbourShapeCircle(NeighbourShape):
    __doc__ = "圆形邻域形状类"

    def __init__(self, radius):
        """
        构造圆形邻域形状类对象

        :param float radius: 圆形邻域的半径
        """
        NeighbourShape.__init__(self)
        self._radius = None
        self.set_radius(radius)
        self._shape_type = NeighbourShapeType.CIRCLE

    @property
    def radius(self):
        """float: 圆形邻域的半径"""
        return self._radius

    def set_radius(self, value):
        """
        设置圆形邻域的半径

        :param float value: 圆形邻域的半径
        :return: self
        :rtype: NeighbourShapeCircle
        """
        self._radius = float(value)
        return self

    @property
    def _jobject(self):
        """Py4J 映射的 Java 对象"""
        java_obj = get_jvm().com.supermap.analyst.spatialanalyst.NeighbourShapeCircle()
        java_obj.setRadius(self.radius)
        return java_obj


class NeighbourShapeAnnulus(NeighbourShape):
    __doc__ = "环形邻域形状类"

    def __init__(self, inner_radius, outer_radius):
        """
        构造环形邻域形状类对象

        :param float inner_radius: 内环半径
        :param float outer_radius: 外环半径
        """
        NeighbourShape.__init__(self)
        self._inner_radius = None
        self._outer_radius = None
        self.set_inner_radius(inner_radius).set_outer_radius(outer_radius)
        self._shape_type = NeighbourShapeType.ANNULUS

    @property
    def inner_radius(self):
        """float: 内环半径"""
        return self._inner_radius

    def set_inner_radius(self, value):
        """
        设置内环半径

        :param float value: 内环半径
        :return: self
        :rtype: NeighbourShapeAnnulus
        """
        self._inner_radius = float(value)
        return self

    @property
    def outer_radius(self):
        """float: 外环半径"""
        return float(self._out_radius)

    def set_outer_radius(self, value):
        """
        设置外环半径

        :param float value: 外环半径
        :return: self
        :rtype: NeighbourShapeAnnulus
        """
        self._out_radius = float(value)
        return self

    @property
    def _jobject(self):
        """Py4J 映射的 Java 对象"""
        java_obj = get_jvm().com.supermap.analyst.spatialanalyst.NeighbourShapeAnnulus()
        java_obj.setInnerRadius(self.inner_radius)
        java_obj.setOuterRadius(self.outer_radius)
        return java_obj


class NeighbourShapeWedge(NeighbourShape):
    __doc__ = "扇形邻域形状类"

    def __init__(self, radius, start_angle, end_angle):
        """
        构造扇形邻域形状类对象

        :param float radius: 形邻域的半径
        :param float start_angle: 扇形邻域的起始角度。单位为度。规定水平向右为 0 度，顺时针旋转计算角度。
        :param float end_angle: 扇形邻域的终止角度。单位为度。规定水平向右为 0 度，顺时针旋转计算角度。
        """
        NeighbourShape.__init__(self)
        self._radius = 0.0
        self._start_angle = 0.0
        self._end_angle = 0.0
        self.set_radius(radius).set_start_angle(start_angle).set_end_angle(end_angle)
        self._shape_type = NeighbourShapeType.WEDGE

    @property
    def radius(self):
        """float: 扇形邻域的半径"""
        return self._radius

    @property
    def start_angle(self):
        """float: 扇形邻域的起始角度。单位为度。规定水平向右为 0 度，顺时针旋转计算角度。 """
        return self._start_angle

    @property
    def end_angle(self):
        """float: 扇形邻域的终止角度。单位为度。规定水平向右为 0 度，顺时针旋转计算角度。 """
        return self._end_angle

    def set_radius(self, value):
        """
        设置扇形邻域的半径

        :param float value: 扇形邻域的半径
        :return: self
        :rtype: NeighbourShapeWedge
        """
        self._radius = float(value)
        return self

    def set_start_angle(self, value):
        """
        设置扇形邻域的起始角度。单位为度。规定水平向右为 0 度，顺时针旋转计算角度。

        :param float value: 扇形邻域的起始角度。单位为度。规定水平向右为 0 度，顺时针旋转计算角度。
        :return: self
        :rtype: NeighbourShapeWedge
        """
        self._start_angle = float(value)
        return self

    def set_end_angle(self, value):
        """
        设置扇形邻域的终止角度。单位为度。规定水平向右为 0 度，顺时针旋转计算角度。

        :param float value:
        :return: self
        :rtype: NeighbourShapeWedge
        """
        self._end_angle = float(value)
        return self

    @property
    def _jobject(self):
        """Py4J 映射的 Java 对象"""
        java_obj = get_jvm().com.supermap.analyst.spatialanalyst.NeighbourShapeWedge()
        java_obj.setRadius(self.radius)
        java_obj.setStartAngle(self.start_angle)
        java_obj.setEndAngle(self.end_angle)
        return java_obj


def kernel_density(input_data, value_field, search_radius, resolution, bounds=None, out_data=None, out_dataset_name=None, progress=None):
    """
    对点数据集或线数据集进行核密度分析，并返回分析结果。
    核密度分析，即使用核函数，来计算点或线邻域范围内的每单位面积量值。其结果是中间值大周边值小的光滑曲面，在邻域边界处降为0。

    :param input_data: 需要进行核密度分析的点数据集或线数据集。
    :type input_data: DatasetVector or str
    :param str value_field: 存储用于进行密度分析的测量值的字段名称。若传 None 则所有几何对象都按值为1处理。不支持文本类型的字段。
    :param float search_radius: 栅格邻域内用于计算密度的查找半径。单位与用于分析的数据集的单位相同。当计算某个栅格位置的未知数值时，会以该位置
                                为圆心，以该属性设置的值为半径，落在这个范围内的采样对象都将参与运算，即该位置的预测值由该范围内采样对象的测量
                                值决定。查找半径越大，生成的密度栅格越平滑且概化程度越高。值越小，生成的栅格所显示的信息越详细。

    :param float resolution: 密度分析结果栅格数据的分辨率
    :param Rectangle bounds: 密度分析的范围，用于确定运行结果所得到的栅格数据集的范围
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetGrid or str

    >>> kernel_density(data_dir + 'example_data.udb/taxi', 'passenger_count', 0.01, 0.001, out_data=out_dir + 'density_result.udb'

    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    else:
        if not isinstance(_source_input, DatasetVector):
            raise ValueError("source input_data must be DatasetVector")
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + "_density"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, "KernelDensity")
                _jvm.com.supermap.analyst.spatialanalyst.DensityAnalyst.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            param = _jvm.com.supermap.analyst.spatialanalyst.DensityAnalystParameter()
            if bounds is not None:
                param.setBounds(bounds._jobject)
            else:
                param.setBounds(_source_input.bounds._jobject)
            param.setResolution(float(resolution))
            param.setSearchRadius(float(search_radius))
            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.DensityAnalyst.kernelDensity(param, _source_input._jobject, value_field, _ds._jobject, _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.DensityAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def point_density(input_data, value_field, resolution, neighbour_shape, neighbour_unit='CELL', bounds=None, out_data=None, out_dataset_name=None, progress=None):
    """
    对点数据集进行点密度分析，并返回分析结果。
    简单点密度分析，即计算每个点的指定邻域形状内的每单位面积量值。计算方法为指定测量值除以邻域面积。点的邻域叠加处，其密度值也相加。
    每个输出栅格的密度均为叠加在栅格上的所有邻域密度值之和。结果栅格值的单位为原数据集单位的平方的倒数，即若原数据集单位为米，则结果栅格值的单位
    为每平方米。注意对于地理坐标数据集，结果栅格值的单位为“每平方度”，是没有实际意义的。

    :param input_data: 需要进行核密度分析的点数据集或线数据集。
    :type input_data: DatasetVector or str
    :param str value_field: 存储用于进行密度分析的测量值的字段名称。若传 None 则所有几何对象都按值为1处理。不支持文本类型的字段。
    :param float resolution: 密度分析结果栅格数据的分辨率
    :param neighbour_shape: 计算密度的查找邻域形状。如果输入值为 str，则要求格式为:
                            - 'CIRCLE,radius', 例如 'CIRCLE, 10'
                            - 'RECTANGLE,width,height'，例如 'RECTANGLE,5.0,10.0'
                            - 'ANNULUS,inner_radius,outer_radius'，例如 'ANNULUS,5.0,10.0'
                            - 'WEDGE,radius,start_angle,end_angle'，例如 'WEDGE,10.0,0,45'
    :type neighbour_shape: NeighbourShape or str
    :param neighbour_unit: 邻域统计的单位类型。可以使用栅格坐标或地理坐标。
    :type neighbour_unit: NeighbourUnitType or str
    :param Rectangle bounds: 密度分析的范围，用于确定运行结果所得到的栅格数据集的范围
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetGrid or str

    >>> point_density(data_dir + 'example_data.udb/taxi', 'passenger_count', 0.0001, 'CIRCLE,0.001', 'MAP', out_data=out_dir + 'density_result.udb')

    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    else:
        if not isinstance(_source_input, DatasetVector):
            raise ValueError("source input_data must be DatasetVector")
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + "_density"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, "PointDensity")
                _jvm.com.supermap.analyst.spatialanalyst.DensityAnalyst.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            param = _jvm.com.supermap.analyst.spatialanalyst.DensityAnalystParameter()
            if bounds is not None:
                param.setBounds(bounds._jobject)
            else:
                param.setBounds(_source_input.bounds._jobject)
            param.setResolution(float(resolution))
            java_neighbourShape = None
            if neighbour_shape is not None:
                if isinstance(neighbour_shape, NeighbourShape):
                    java_neighbourShape = neighbour_shape._jobject
                else:
                    if isinstance(neighbour_shape, str):
                        tokens = neighbour_shape.split(",")
                        if len(tokens) > 1:
                            shapeType = NeighbourShapeType._make(tokens[0])
                            if shapeType is NeighbourShapeType.RECTANGLE:
                                if len(tokens) >= 3:
                                    java_neighbourShape = NeighbourShapeRectangle(float(tokens[1]), float(tokens[2]))._jobject
                            elif shapeType is NeighbourShapeType.CIRCLE:
                                if len(tokens) >= 2:
                                    java_neighbourShape = NeighbourShapeCircle(float(tokens[1]))._jobject
                            elif shapeType is NeighbourShapeType.WEDGE:
                                if len(tokens) >= 4:
                                    java_neighbourShape = NeighbourShapeWedge(float(tokens[1]), float(tokens[2]), float(tokens[3]))._jobject
                            elif shapeType is NeighbourShapeType.ANNULUS:
                                if len(tokens) >= 3:
                                    java_neighbourShape = NeighbourShapeAnnulus(float(tokens[1]), float(tokens[2]))._jobject
            if java_neighbourShape is None:
                raise ValueError("neighbourShape is invalid")
            java_neighbourShape.setUnitType(NeighbourUnitType._make(neighbour_unit)._jobject)
            param.setSearchNeighbourhood(java_neighbourShape)
            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.DensityAnalyst.pointDensity(param, _source_input._jobject, value_field, _ds._jobject, _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.DensityAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


class _RasterClipFileType(JEnum):
    TIF = 103
    IMG = 101
    SIT = 204
    BMP = 121
    JPG = 122
    PNG = 123
    GIF = 124

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialanalyst.RasterClipFileType"


def clip_raster(input_data, clip_region, is_clip_in_region=True, is_exact_clip=False, out_data=None, out_dataset_name=None, progress=None):
    """
    对栅格或影像数据集进行裁剪，结果存储为一个新的栅格或影像数据集。有时，我们的研究范围或者感兴趣区域较小，仅涉及当前栅格数据
    的一部分，这时可以对栅格数据进行裁剪，即通过一个 GeoRegion 对象作为裁剪区域对栅格数据进行裁剪，提取该区域内（外）的栅格数
    据生成一个新的数据集，此外，还可以选择进行精确裁剪或显示裁剪。

    :param input_data:  指定的要进行裁剪的数据集，支持栅格数据集和影像数据集。
    :type input_data: DatasetGrid or DatasetImage or str
    :param clip_region: 裁剪区域
    :type clip_region: GeoRegion or Rectangle
    :param bool is_clip_in_region: 是否对裁剪区内的数据集进行裁剪。若为 True，则对裁剪区域内的数据集进行裁剪，若为 False，则对裁剪区域外的数据集进行裁剪。
    :param bool is_exact_clip: 是否使用精确裁剪。若为 True，表示使用精确裁剪对栅格或影像数据集进行裁剪，False 表示使用显示裁剪:

                                - 采用显示裁剪时，系统会按照像素分块（详见 DatasetGrid.block_size_option、DatasetImage.block_size_option 方法）的大小,
                                  对栅格或影像数据集进行裁剪。此时只有裁剪区域内的数据被保留，即如果裁剪区的边界没有恰好与单元格的边界重合，那么单元格将被分割，
                                  位于裁剪区的部分会保留下来；位于裁剪区域外，且在被裁剪的那部分栅格所在块的总范围内的栅格仍有栅格值，但不显示。此种方式适用于大数据的裁剪。

                                - 采用精确裁剪时，系统在裁剪区域边界，会根据裁剪区域压盖的单元格的中心点的位置确定是否保留该单元格。如果使用区域内裁剪方式，单元格的中心点位于裁剪区内则保留，反之不保留。

    :param out_data: 结果数据集所在的数据源或直接生成 tif 文件
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称。如果设置直接生成 tif 文件，则此参数无效。
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称或第三方影像文件路径。
    :rtype: DatasetGrid or DatasetImage or str

    >>> clip_region = Rectangle(875.5, 861.2, 1172.6, 520.9)
    >>> result = clip_raster(data_dir + 'example_data.udb/seaport', clip_region, True, False, out_data=out_dir + 'clip_seaport.tif')
    >>> result = clip_raster(data_dir + 'example_data.udb/seaport', clip_region, True, False, out_data=out_dir + 'clip_out.udb')

    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    if not isinstance(_source_input, (DatasetGrid, DatasetImage)):
        raise ValueError("source input_data must be DatasetGrid or DatasetImage")
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, "clip_raster")
                _jvm.com.supermap.analyst.spatialanalyst.RasterClip.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    if isinstance(clip_region, Rectangle):
        clip_region = clip_region.to_region()
    else:
        import os
        try:
            ext_name = os.path.basename(out_data).split(".")[-1]
        except:
            ext_name = None

        if ext_name is not None and ext_name.lower() in set(["tif", "tiff"]):
            try:
                if not isinstance(_source_input, DatasetImage):
                    raise ValueError("input_data must be DatasetImage")
                targetFileName = out_data
                ext_type = ext_name
                if ext_type == "tiff":
                    ext_type = "tif"
                targetFileType = _RasterClipFileType._make("TIF")
                java_result = _jvm.com.supermap.analyst.spatialanalyst.RasterClip.clip(_source_input._jobject, clip_region._jobject, bool(is_clip_in_region), targetFileName, targetFileType._jobject)
            except Exception as e:
                try:
                    log_error(e)
                    java_result = False
                finally:
                    e = None
                    del e

            if java_result:
                return targetFileName
            return
        else:
            if out_data is not None:
                out_datasource = get_output_datasource(out_data)
                _ds = out_datasource
            else:
                _ds = _source_input.datasource
            check_output_datasource(_ds)
            if out_dataset_name is None:
                _outDatasetName = _source_input.name + "_clip"
            else:
                _outDatasetName = out_dataset_name
            _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
            try:
                try:
                    java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.RasterClip.clip(_source_input._jobject, clip_region._jobject, bool(is_clip_in_region), bool(is_exact_clip), _ds._jobject, _outDatasetName)
                except Exception as e:
                    try:
                        log_error(e)
                        java_result_dt = None
                    finally:
                        e = None
                        del e

            finally:
                if listener is not None:
                    try:
                        _jvm.com.supermap.analyst.spatialanalyst.RasterClip.removeSteppedListener(listener)
                    except Exception as e1:
                        try:
                            log_error(e1)
                        finally:
                            e1 = None
                            del e1

                    close_callback_server()
                elif java_result_dt is not None:
                    result_dt = _ds[java_result_dt.getName()]
                else:
                    result_dt = None
                if out_data is not None:
                    return try_close_output_datasource(result_dt, out_datasource)
                return result_dt


class InterpolationParameter(object):

    def __init__(self, bounds, resolution):
        self._type = None
        self._bounds = None
        self._resolution = None
        self.set_bounds(bounds).set_resolution(resolution)

    @property
    def type(self):
        """InterpolationAlgorithmType: 插值分支所支持的算法的类型 """
        return self._type

    @property
    def bounds(self):
        """Rectangle: 插值分析的范围，用于确定运行结果的范围"""
        return self._bounds

    def set_bounds(self, value):
        """
        设置插值分析的范围，用于确定运行结果的范围

        :param Rectangle value: 插值分析的范围，用于确定运行结果的范围
        :return: self
        :rtype: InterpolationParameter
        """
        self._bounds = value
        return self

    @property
    def resolution(self):
        """float: 插值运算时使用的分辨率"""
        return self._resolution

    def set_resolution(self, value):
        """
        设置插值运算时使用的分辨率。

        :param float value: 插值运算时使用的分辨率
        :return: self
        :rtype: InterpolationParameter
        """
        self._resolution = float(value)
        return self


class InterpolationDensityParameter(InterpolationParameter):
    __doc__ = "\n    点密度差值（Density）插值参数类。点密度插值方法，用于表达采样点的密度分布情况。\n    点密度插值的结果栅格的分辨率设置需要结合点数据集范围大小来取值，一般结果栅格行列值（即结果栅格数据集范围除以分辨率）在 500\n    以内即可以较好的体现出密度走势。由于点密度插值暂时只支持定长搜索模式，因此搜索半径（search_radius）值设置较为重要，此值需要用户根据待插值点数据分布状况和点数据集范围进行设置。\n    "

    def __init__(self, resolution, search_radius=0.0, expected_count=12, bounds=None):
        """
        构造点密度差值插值参数类对象

        :param float resolution: 插值运算时使用的分辨率
        :param float search_radius: 查找参与运算点的查找半径
        :param int expected_count: 期望参与插值运算的点数
        :param Rectangle bounds: 插值分析的范围，用于确定运行结果的范围
        """
        InterpolationParameter.__init__(self, bounds, resolution)
        self._search_mode = SearchMode.KDTREE_FIXED_RADIUS
        self._search_radius = None
        self._expected_count = None
        self._type = InterpolationAlgorithmType.DENSITY
        self.set_search_radius(search_radius).set_expected_count(expected_count)

    @property
    def search_mode(self):
        """SearchMode: 在插值运算时，查找参与运算点的方式，只支持定长查找（KDTREE_FIXED_RADIUS）方式"""
        return self._search_mode

    @property
    def search_radius(self):
        """float: 查找参与运算点的查找半径"""
        return self._search_radius

    def set_search_radius(self, value):
        """
        设置查找参与运算点的查找半径。单位与用于插值的点数据集（或记录集所属的数据集）的单位相同。查找半径决定了参与运算点的查找范围，当计算某个位置
        的未知数值时，会以该位置为圆心，以search_radius为半径，落在这个范围内的采样点都将参与运算，即该位置的预测值由该范围内采样点的数值决定。

        :param float value: 查找参与运算点的查找半径
        :return: self
        :rtype: InterpolationDensityParameter
        """
        if value is not None:
            self._search_radius = float(value)
        return self

    @property
    def expected_count(self):
        """int: 返回期望参与插值运算的点数，表示期望参与运算的最少样点数"""
        return self._expected_count

    def set_expected_count(self, value):
        """
        设置期望参与插值运算的点数

        :param int value: 表示期望参与运算的最少样点数
        :return: self
        :rtype: InterpolationDensityParameter
        """
        self._expected_count = value
        return self

    @property
    def _jobject(self):
        """Py4J 映射的 Java 对象"""
        java_obj = get_jvm().com.supermap.analyst.spatialanalyst.InterpolationDensityParameter()
        if self.bounds is not None:
            java_obj.setBounds(self.bounds._jobject)
        if self.expected_count is not None:
            java_obj.setExpectedCount(self.expected_count)
        if self.resolution is not None:
            java_obj.setResolution(self.resolution)
        if self.search_mode is not None:
            java_obj.setSearchMode(self.search_mode._jobject)
        if self.search_radius is not None:
            java_obj.setSearchRadius(self.search_radius)
        return java_obj


class InterpolationIDWParameter(InterpolationParameter):
    __doc__ = "\n    距离反比权值插值（Inverse Distance Weighted）参数类，\n    "

    def __init__(self, resolution, search_mode=SearchMode.KDTREE_FIXED_COUNT, search_radius=0.0, expected_count=12, power=1, bounds=None):
        """
        构造 IDW 插值参数类。

        :param float resolution: 插值运算时使用的分辨率
        :param search_mode: 查找方式，不支持 QUADTREE
        :type search_mode: SearchMode or str
        :param float search_radius: 查找参与运算点的查找半径
        :param int expected_count: 期望参与插值运算的点数
        :param int power: 距离权重计算的幂次，幂次值越低，内插结果越平滑，幂次值越高，内插结果细节越详细。此参数应为一个大于0的值。如果不指定此参数，方法缺省将其设置为1
        :param Rectangle bounds: 插值分析的范围，用于确定运行结果的范围
        """
        InterpolationParameter.__init__(self, bounds, resolution)
        self._search_mode = SearchMode.KDTREE_FIXED_RADIUS
        self._search_radius = None
        self._expected_count = None
        self._power = 1
        self._type = InterpolationAlgorithmType.IDW
        self.set_search_mode(search_mode)
        self.set_search_radius(search_radius)
        self.set_expected_count(expected_count)
        self.set_power(power)

    @property
    def search_mode(self):
        """SearchMode: 在插值运算时，查找参与运算点的方式，不支持 QUADTREE"""
        return self._search_mode

    def set_search_mode(self, value):
        """
        设置在插值运算时，查找参与运算点的方式。不支持 QUADTREE

        :param value: 在插值运算时，查找参与运算点的方式
        :type value:  SearchMode or str
        :return: self
        :rtype: InterpolationIDWParameter
        """
        self._search_mode = SearchMode._make(value)
        return self

    @property
    def search_radius(self):
        """float: 查找参与运算点的查找半径"""
        return self._search_radius

    def set_search_radius(self, value):
        """
        设置查找参与运算点的查找半径。单位与用于插值的点数据集（或记录集所属的数据集）的单位相同。查找半径决定了参与运算点的查找范围，当计算某个位置
        的未知数值时，会以该位置为圆心，以search_radius为半径，落在这个范围内的采样点都将参与运算，即该位置的预测值由该范围内采样点的数值决定。

        如果设置 search_mode 为KDTREE_FIXED_COUNT，同时指定查找参与运算点的范围，当查找范围内的点数小于指定的点数时赋为空值，当查找范围内的点数
        大于指定的点数时，则返回距离插值点最近的指定个数的点进行插值。

        :param float value: 查找参与运算点的查找半径
        :return: self
        :rtype: InterpolationIDWParameter
        """
        self._search_radius = float(value)
        return self

    @property
    def expected_count(self):
        """int: 期望参与插值运算的点数，如果设置 search_mode 为 KDTREE_FIXED_RADIUS ，同时指定参与插值运算点的个数，当查找范围内的点数小于指定的点数时赋为空值。 """
        return self._expected_count

    def set_expected_count(self, value):
        """
        设置期望参与插值运算的点数。如果设置 search_mode 为 KDTREE_FIXED_RADIUS ，同时指定参与插值运算点的个数，当查找范围内的点数小于指定的点数时赋为空值。

        :param int value: 表示期望参与运算的最少样点数
        :return: self
        :rtype: InterpolationIDWParameter
        """
        self._expected_count = value
        return self

    @property
    def power(self):
        """int: 距离权重计算的幂次"""
        return self._power

    def set_power(self, value):
        """
        设置距离权重计算的幂次。幂次值越低，内插结果越平滑，幂次值越高，内插结果细节越详细。此参数应为一个大于0的值。如果不指定此参数，方法缺省
        将其设置为1。

        :param int value: 距离权重计算的幂次
        :return: self
        :rtype: InterpolationIDWParameter
        """
        self._power = int(value)
        return self

    @property
    def _jobject(self):
        """ Py4J 映射的 Java 对象"""
        java_obj = get_jvm().com.supermap.analyst.spatialanalyst.InterpolationIDWParameter()
        if self.bounds is not None:
            java_obj.setBounds(self.bounds._jobject)
        if self.expected_count:
            java_obj.setExpectedCount(self.expected_count)
        if self.resolution:
            java_obj.setResolution(self.resolution)
        if self.search_mode:
            java_obj.setSearchMode(self.search_mode._jobject)
        if self.search_radius:
            java_obj.setSearchRadius(self.search_radius)
        if self.power:
            java_obj.setPower(self.power)
        return java_obj


class InterpolationKrigingParameter(InterpolationParameter):
    __doc__ = "\n    克吕金（Kriging）内插法参数。\n\n    Kriging 法为地质统计学上一种空间资料内插处理方法，主要的目的是利用各数据点间变异数（variance）的大小来推求某一未知点与各已知点的权重关系，再\n    由各数据点的值和其与未知点的权重关系推求未知点的值。Kriging 法最大的特色不仅是提供一个最小估计误差的预测值，并且可明确的指出误差值的大小。一般\n    而言，许多地质参数，如地形面本身即具有连续的性质，故在一短距离内的任两点必有空间上的关系。反之，在一不规则面上的两点若相距甚远，则在统计意义上可\n    视为互为独立 (stastically indepedent)，这种随距离而改变的空间上连续性，可用半变异图 (semivariogram) 来表现。因此，若想由已知的散乱点来\n    推求某一未知点的值，则可利用半变异图推求各已知点及欲求值点的空间关系。再由此空间参数推求半变异数，由各数据点间的半变异数可推求未知点与已知点间的\n    权重关系，进而推求出未知点的值。克吕金法的优点是以空间统计学作为其坚实的理论基础。物理含义明确；不但能估计测定参数的空间变异分布，而且还可以估算\n    参数的方差分布。克吕金法的缺点是计算步骤较烦琐，计算量大，且变异函数有时需要根据经验人为选定。\n\n    克吕金插值法可以采用两种方式来获取参与插值的采样点，进而获得相应位置点的预测值，一个是在待计算预测值位置点周围一定范围内，获取该范围内的所有采样\n    点，通过特定的插值计算公式获得该位置点的预测值；另一个是在待计算预测值位置点周围获取一定数目的采样点，通过特定的插值计算公式获得该位置点的预测值。\n\n    克吕金插值过程是一个多步骤的处理过程，包括:\n        - 创建变异图和协方差函数来估计统计相关（也称为空间自相关）的值；\n        - 预测待计算位置点的未知值。\n\n    半变异函数与半变异图:\n        - 计算所有采样点中相距 h 个单位的任意两点的半变异函数值，那么任意两点的距离 h 一般是唯一的，将所有的点对的距离与相应的半变函数值快速显示在以 h\n          为 X 坐标轴和以半变函数值为 Y 坐标轴的坐标空间内，就得到了半变异图。相距距离愈小的点其半变异数愈小，而随着距离的增加，任两点间的空间相依关系愈\n          小，使得半变异函数值趋向于一稳定值。此稳定值我们称之为基台值（Sill）；而达到基台值时的最小 h 值称之为自相关阈值（Range）。\n\n    块金效应:\n        - 当点间距离为 0（比如，步长=0）时，半变函数值为 0。然而，在一个无限小的距离内，半变函数通常显示出块金效应，这是一个大于 0 的值。如果半变函数\n          在Y周上的截距式 2 ，则块金效应值为 2。\n        - 块金效应属于测量误差，或者是小于采样步长的小距离上的空间变化，或者两者兼而有之。测量误差主要是由于观测仪器的内在误差引起的。自然现象的空间变异\n          范围很大（可以在很小的尺度上，也可以在很大的尺度上）。小于步长尺度上的变化就表现为块金的一部分。\n\n    半变异图的获得是进行空间插值预测的关键步骤之一，克吕金法的主要应用之一就是预测非采样点的属性值，半变异图提供了采样点的空间自相关信息，根据半变\n    异图，选择合适的半变异模型，即拟合半变异图的曲线模型。\n\n    不同的模型将会影响所获得的预测结果，如果接近原点处的半变异函数曲线越陡，则较近领域对该预测值的影响就越大。因此输出表面就会越不光滑。\n\n    SuperMap 支持的半变函数模型有指数型、球型和高斯型。详细信息参见 VariogramMode 类\n\n    "

    def __init__(self, resolution, krighing_type=InterpolationAlgorithmType.KRIGING, search_mode=SearchMode.KDTREE_FIXED_COUNT, search_radius=0.0, expected_count=12, max_point_count_in_node=50, max_point_count_for_interpolation=200, variogram=VariogramMode.SPHERICAL, angle=0.0, mean=0.0, exponent=Exponent.EXP1, nugget=0.0, range_value=0.0, sill=0.0, bounds=None):
        """
        构造 克吕金插值参数对象。

        :param float resolution: 插值运算时使用的分辨率
        :param krighing_type: 插值分析的算法类型。支持设置 KRIGING, SimpleKRIGING, UniversalKRIGING 三种，默认使用 KRIGING。
        :type krighing_type: InterpolationAlgorithmType or str
        :param search_mode: 查找模式。
        :type search_mode: SearchMode or str
        :param float search_radius:  查找参与运算点的查找半径。单位与用于插值的点数据集（或记录集所属的数据集）的单位相同。查找半径决定了参与
                                     运算点的查找范围，当计算某个位置的未知数值时，会以该位置为圆心，search_radius 为半径，落在这个范围内的
                                     采样点都将参与运算，即该位置的预测值由该范围内采样点的数值决定。
        :param int expected_count:  期望参与插值运算的点数，当查找方式为变长查找时，表示期望参与运算的最多样点数。
        :param int max_point_count_in_node: 单个块内最多查找点数。当用QuadTree的查找插值点时，才可以设置块内最多点数。
        :param int max_point_count_for_interpolation: 设置块查找时，最多参与插值的点数。注意，该值必须大于零。当用QuadTree的查找插值点时，才可以设置最多参与插值的点数
        :param variogram:  克吕金（Kriging）插值时的半变函数类型。默认值为 VariogramMode.SPHERICAL
        :type variogram: VariogramMode or str
        :param float angle:  克吕金算法中旋转角度值
        :param float mean: 插值字段的平均值，即采样点插值字段值总和除以采样点数目。
        :param exponent: 用于插值的样点数据中趋势面方程的阶数
        :type exponent: Exponent or str
        :param float nugget: 块金效应值。
        :param float range_value: 自相关阈值。
        :param float sill: 基台值
        :param Rectangle bounds: 插值分析的范围，用于确定运行结果的范围
        """
        InterpolationParameter.__init__(self, bounds, resolution)
        self._search_mode = None
        self._search_radius = None
        self._expected_count = None
        self._max_point_count_in_node = None
        self._max_point_count_for_interpolation = None
        self._variogram_mode = None
        self._angle = None
        self._mean = None
        self._exponent = None
        self._nugget = None
        self._range = None
        self._sill = None
        self._type = InterpolationAlgorithmType._make(krighing_type)
        if self._type not in (InterpolationAlgorithmType.KRIGING,
         InterpolationAlgorithmType.SIMPLEKRIGING,
         InterpolationAlgorithmType.UNIVERSALKRIGING):
            raise ValueError("Only Support KRIGING, SimpleKRIGING and UniversalKRIGING, but now is " + str(self._type))
        self.set_search_mode(search_mode)
        self.set_search_radius(search_radius)
        self.set_expected_count(expected_count)
        self.set_max_point_count_in_node(max_point_count_in_node)
        self.set_max_point_count_for_interpolation(max_point_count_for_interpolation)
        self.set_variogram_mode(variogram)
        self.set_angle(angle)
        self.set_mean(mean)
        self.set_exponent(exponent)
        self.set_nugget(nugget)
        self.set_range(range_value)
        self.set_sill(sill)

    @property
    def max_point_count_in_node(self):
        """int:  单个块内最多查找点数"""
        return self._max_point_count_in_node

    def set_max_point_count_in_node(self, value):
        """
        设置单个块内最多查找点数。当用QuadTree的查找插值点时，才可以设置块内最多点数。

        :param int value: 单个块内最多查找点数。当用QuadTree的查找插值点时，才可以设置块内最多点数
        :return: self
        :rtype: InterpolationKrigingParameter
        """
        self._max_point_count_in_node = int(value)
        return self

    @property
    def max_point_count_for_interpolation(self):
        """int:块查找时，最多参与插值的点数 """
        return self._max_point_count_for_interpolation

    def set_max_point_count_for_interpolation(self, value):
        """
        设置块查找时，最多参与插值的点数。注意，该值必须大于零。当用QuadTree的查找插值点时，才可以设置最多参与插值的点数

        :param int value: 块查找时，最多参与插值的点数
        :return: self
        :rtype: InterpolationKrigingParameter
        """
        self._max_point_count_for_interpolation = int(value)
        return self

    @property
    def variogram_mode(self):
        """VariogramMode: 克吕金（Kriging）插值时的半变函数类型。默认值为 VariogramMode.SPHERICAL"""
        return self._variogram_mode

    def set_variogram_mode(self, value):
        """
        设置克吕金（Kriging）插值时的半变函数类型。默认值为 VariogramMode.SPHERICAL

        :param value: 克吕金（Kriging）插值时的半变函数类型
        :type value: VariogramMode or
        :return: self
        :rtype: InterpolationKrigingParameter
        """
        self._variogram_mode = VariogramMode._make(value)
        return self

    @property
    def angle(self):
        """float: 克吕金算法中旋转角度值"""
        return self._angle

    def set_angle(self, value):
        """
        设置克吕金算法中旋转角度值

        :param float value: 克吕金算法中旋转角度值
        :return: self
        :rtype: InterpolationKrigingParameter
        """
        self._angle = float(value)
        return self

    @property
    def mean(self):
        """float: 插值字段的平均值，即采样点插值字段值总和除以采样点数目。"""
        return self._mean

    def set_mean(self, value):
        """
        设置插值字段的平均值，即采样点插值字段值总和除以采样点数目。

        :param float value: 插值字段的平均值，即采样点插值字段值总和除以采样点数目。
        :return: self
        :rtype: InterpolationKrigingParameter
        """
        self._mean = float(value)
        return self

    @property
    def exponent(self):
        """Exponent: 用于插值的样点数据中趋势面方程的阶数"""
        return self._exponent

    def set_exponent(self, value):
        """
        设置用于插值的样点数据中趋势面方程的阶数

        :param value: 用于插值的样点数据中趋势面方程的阶数
        :type value: Exponent or str
        :return: self
        :rtype: InterpolationKrigingParameter
        """
        self._exponent = Exponent._make(value)
        return self

    @property
    def nugget(self):
        """float:  块金效应值。"""
        return self._nugget

    def set_nugget(self, value):
        """
        设置块金效应值。

        :param float value: 块金效应值。
        :return: self
        :rtype: InterpolationKrigingParameter
        """
        self._nugget = float(value)
        return self

    @property
    def range(self):
        """float: 自相关阈值"""
        return self._range

    def set_range(self, value):
        """
        设置自相关阈值

        :param float value: 自相关阈值
        :return: self
        :rtype: InterpolationKrigingParameter
        """
        self._range = float(value)
        return self

    @property
    def sill(self):
        """float: 基台值"""
        return self._sill

    def set_sill(self, value):
        """
        设置基台值

        :param float value: 基台值
        :return: self
        :rtype: InterpolationKrigingParameter
        """
        self._sill = float(value)
        return self

    @property
    def search_mode(self):
        """SearchMode: 在插值运算时，查找参与运算点的方式"""
        return self._search_mode

    def set_search_mode(self, value):
        """
        设置在插值运算时，查找参与运算点的方式

        :param value: 在插值运算时，查找参与运算点的方式
        :type value:  SearchMode or str
        :return: self
        :rtype: InterpolationIDWParameter
        """
        self._search_mode = SearchMode._make(value)
        return self

    @property
    def search_radius(self):
        """float: 查找参与运算点的查找半径"""
        return self._search_radius

    def set_search_radius(self, value):
        """
        设置查找参与运算点的查找半径。单位与用于插值的点数据集（或记录集所属的数据集）的单位相同。查找半径决定了参与运算点的查找范围，当计算某个位置
        的未知数值时，会以该位置为圆心，以 search_radius为半径，落在这个范围内的采样点都将参与运算，即该位置的预测值由该范围内采样点的数值决定。

        查找模式设置为“变长查找”（KDTREE_FIXED_COUNT），将使用最大查找半径范围内的固定数目的样点值进行插值，最大查找半径为点数据集的区域范围对
        应的矩形的对角线长度的 0.2 倍。

        :param float value: 查找参与运算点的查找半径
        :return: self
        :rtype: InterpolationIDWParameter
        """
        self._search_radius = float(value)
        return self

    @property
    def expected_count(self):
        """int: 期望参与插值运算的点数 """
        return self._expected_count

    def set_expected_count(self, value):
        """
        设置期望参与插值运算的点数

        :param int value: 表示期望参与运算的最少样点数
        :return: self
        :rtype: InterpolationIDWParameter
        """
        self._expected_count = int(value)
        return self

    @property
    def _jobject(self):
        """Py4J 映射的 Java 对象"""
        java_obj = get_jvm().com.supermap.analyst.spatialanalyst.InterpolationKrigingParameter(self.type._jobject)
        if self.bounds is not None:
            java_obj.setBounds(self.bounds._jobject)
        if self.expected_count:
            java_obj.setExpectedCount(self.expected_count)
        if self.resolution:
            java_obj.setResolution(self.resolution)
        if self.search_mode:
            java_obj.setSearchMode(self.search_mode._jobject)
        if self.search_radius:
            java_obj.setSearchRadius(self.search_radius)
        if self.search_mode == SearchMode.QUADTREE:
            if self.max_point_count_in_node:
                java_obj.setMaxPointCountInNode(self.max_point_count_in_node)
            if self.max_point_count_for_interpolation:
                java_obj.setMaxPointCountForInterpolation(self.max_point_count_for_interpolation)
        if self.variogram_mode:
            java_obj.setVariogramMode(self.variogram_mode._jobject)
        if self.angle:
            if self.search_mode != SearchMode.QUADTREE:
                java_obj.setAngle(self.angle)
        if self.type == InterpolationAlgorithmType.SIMPLEKRIGING:
            if self.mean:
                java_obj.setMean(self.mean)
        if self.type == InterpolationAlgorithmType.UNIVERSALKRIGING:
            if self.exponent:
                java_obj.setExponent(self.exponent._jobject)
        if self.nugget:
            java_obj.setNugget(self.nugget)
        if self.range:
            java_obj.setRange(self.range)
        if self.sill:
            java_obj.setSill(self.sill)
        if self.bounds:
            java_obj.setBounds(self.bounds._jobject)
        return java_obj


class InterpolationRBFParameter(InterpolationParameter):
    __doc__ = "\n    径向基函数 RBF（Radial Basis Function）插值法参数类\n    "

    def __init__(self, resolution, search_mode=SearchMode.KDTREE_FIXED_COUNT, search_radius=0.0, expected_count=12, max_point_count_in_node=50, max_point_count_for_interpolation=200, smooth=0.100000001490116, tension=40, bounds=None):
        """
        构造径向基函数插值法参数类对象。

        :param float resolution: 插值运算时使用的分辨率
        :param search_mode: 查找模式。
        :type search_mode: SearchMode or str
        :param float search_radius:  查找参与运算点的查找半径。单位与用于插值的点数据集（或记录集所属的数据集）的单位相同。查找半径决定了参与
                                     运算点的查找范围，当计算某个位置的未知数值时，会以该位置为圆心，search_radius 为半径，落在这个范围内的
                                     采样点都将参与运算，即该位置的预测值由该范围内采样点的数值决定。
        :param int expected_count:  期望参与插值运算的点数，当查找方式为变长查找时，表示期望参与运算的最多样点数。
        :param int max_point_count_in_node: 单个块内最多查找点数。当用QuadTree的查找插值点时，才可以设置块内最多点数。
        :param int max_point_count_for_interpolation: 设置块查找时，最多参与插值的点数。注意，该值必须大于零。当用QuadTree的查找插值点时，才可以设置最多参与插值的点数
        :param float smooth: 光滑系数，值域为 [0,1]
        :param float tension: 张力系数
        :param Rectangle bounds: 插值分析的范围，用于确定运行结果的范围
        """
        InterpolationParameter.__init__(self, bounds, resolution)
        self._search_mode = None
        self._search_radius = None
        self._expected_count = None
        self._max_point_count_in_node = None
        self._max_point_count_for_interpolation = None
        self._smooth = None
        self._tension = None
        self._type = InterpolationAlgorithmType.RBF
        self.set_search_mode(search_mode)
        self.set_search_radius(search_radius)
        self.set_expected_count(expected_count)
        self.set_max_point_count_in_node(max_point_count_in_node)
        self.set_max_point_count_for_interpolation(max_point_count_for_interpolation)
        self.set_smooth(smooth)
        self.set_tension(tension)

    @property
    def smooth(self):
        """float: 光滑系数"""
        return self._smooth

    def set_smooth(self, value):
        """
        设置光滑系数

        :param float value: 光滑系数
        :return: self
        :rtype: InterpolationRBFParameter
        """
        if value is not None:
            self._smooth = float(value)
        return self

    @property
    def tension(self):
        """float: 张力系数"""
        return self._tension

    def set_tension(self, value):
        """
        设置张力系数

        :param float value: 张力系数
        :return: self
        :rtype: InterpolationRBFParameter
        """
        self._tension = float(value)
        return self

    @property
    def max_point_count_in_node(self):
        """int:  单个块内最多查找点数"""
        return self._max_point_count_in_node

    def set_max_point_count_in_node(self, value):
        """
        设置单个块内最多查找点数。当用QuadTree的查找插值点时，才可以设置块内最多点数。

        :param int value: 单个块内最多查找点数。当用QuadTree的查找插值点时，才可以设置块内最多点数
        :return: self
        :rtype: InterpolationRBFParameter
        """
        self._max_point_count_in_node = int(value)
        return self

    @property
    def max_point_count_for_interpolation(self):
        """int:块查找时，最多参与插值的点数 """
        return self._max_point_count_for_interpolation

    def set_max_point_count_for_interpolation(self, value):
        """
        设置块查找时，最多参与插值的点数。注意，该值必须大于零。当用QuadTree的查找插值点时，才可以设置最多参与插值的点数

        :param int value: 块查找时，最多参与插值的点数
        :return: self
        :rtype: InterpolationRBFParameter
        """
        self._max_point_count_for_interpolation = int(value)
        return self

    @property
    def search_mode(self):
        """SearchMode: 在插值运算时，查找参与运算点的方式，不支持 KDTREE_FIXED_RADIUS """
        return self._search_mode

    def set_search_mode(self, value):
        """
        设置在插值运算时，查找参与运算点的方式。

        :param value: 在插值运算时，查找参与运算点的方式
        :type value:  SearchMode or str
        :return: self
        :rtype: InterpolationRBFParameter
        """
        self._search_mode = SearchMode._make(value)
        return self

    @property
    def search_radius(self):
        """float: 查找参与运算点的查找半径"""
        return self._search_radius

    def set_search_radius(self, value):
        """
        设置查找参与运算点的查找半径。单位与用于插值的点数据集（或记录集所属的数据集）的单位相同。查找半径决定了参与运算点的查找范围，当计算某个位置
        的未知数值时，会以该位置为圆心，以 search_radiu s为半径，落在这个范围内的采样点都将参与运算，即该位置的预测值由该范围内采样点的数值决定。

        查找模式设置为“变长查找”（KDTREE_FIXED_COUNT），将使用最大查找半径范围内的固定数目的样点值进行插值，最大查找半径为点数据集的区域范围对
        应的矩形的对角线长度的 0.2 倍。

        :param float value: 查找参与运算点的查找半径
        :return: self
        :rtype: InterpolationRBFParameter
        """
        self._search_radius = float(value)
        return self

    @property
    def expected_count(self):
        """int: 期望参与插值运算的点数 """
        return self._expected_count

    def set_expected_count(self, value):
        """
        设置期望参与插值运算的点数

        :param int value: 表示期望参与运算的最少样点数
        :return: self
        :rtype: InterpolationRBFParameter
        """
        self._expected_count = int(value)
        return self

    @property
    def _jobject(self):
        """Py4J 映射的 Java 对象"""
        java_obj = get_jvm().com.supermap.analyst.spatialanalyst.InterpolationRBFParameter()
        if self.bounds is not None:
            java_obj.setBounds(self.bounds._jobject)
        if self.expected_count:
            java_obj.setExpectedCount(self.expected_count)
        if self.resolution:
            java_obj.setResolution(self.resolution)
        if self.search_mode:
            java_obj.setSearchMode(self.search_mode._jobject)
        if self.search_radius:
            java_obj.setSearchRadius(self.search_radius)
        if self.search_mode == SearchMode.QUADTREE:
            if self.max_point_count_in_node:
                java_obj.setMaxPointCountInNode(self.max_point_count_in_node)
            if self.max_point_count_for_interpolation:
                java_obj.setMaxPointCountForInterpolation(self.max_point_count_for_interpolation)
        if self.smooth:
            java_obj.setSmooth(self.smooth)
        if self.tension:
            java_obj.setTension(self.tension)
        return java_obj


def interpolate(input_data, parameter, z_value_field, pixel_format, z_value_scale=1.0, out_data=None, out_dataset_name=None, progress=None):
    """
    插值分析类。该类提供插值分析功能，用于对离散的点数据进行插值得到栅格数据集。插值分析可以将有限的采样点数据，通过插值对采样点周围的数值情况进行预测，
    从而掌握研究区域内数据的总体分布状况，而使采样的离散点不仅仅反映其所在位置的数值情况，而且可以反映区域的数值分布。

    为什么要进行插值？

    由于地理空间要素之间存在着空间关联性，即相互邻近的事物总是趋于同质，也就是具有相同或者相似的特征，举个例子，街道的一边下雨了，那么街道的另一边在大
    多数情况下也一定在下雨，如果在更大的区域范围，一个乡镇的气候应当与其接壤的另一的乡镇的气候相同，等等，基于这样的推理，我们就可以利用已知地点的信息
    来间接获取与其相邻的其他地点的信息，而插值分析就是基于这样的思想产生的，也是插值重要的应用价值之一。

    将某个区域的采样点数据插值生成栅格数据，实际上是将研究区域按照给定的格网尺寸（分辨率）进行栅格化，栅格数据中每一个栅格单元对应一块区域，栅格单元的
    值由其邻近的采样点的数值通过某种插值方法计算得到，因此，就可以预测采样点周围的数值情况，进而了解整个区域的数值分布情况。其中，插值方法主要有距离反
    比权值插值法、克吕金（Kriging）内插法、径向基函数RBF（Radial Basis Function）插值。
    利用插值分析功能能够预测任何地理点数据的未知值，如高程、降雨量、化学物浓度、噪声级等等。

    :param input_data:  需要进行插值分析的点数据集或点记录集
    :type input_data: DatasetVector or str or Recordset
    :param InterpolationParameter parameter: 插值方法需要的参数信息
    :param str z_value_field: 存储用于进行插值分析的值的字段名称。插值分析不支持文本类型的字段。
    :param pixel_format: 指定结果栅格数据集存储的像素，不支持 BIT64
    :type pixel_format: PixelFormat or str
    :param float z_value_scale: 插值分析值的缩放比率
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetGrid or str
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    else:
        if not isinstance(_source_input, (DatasetVector, Recordset)):
            raise ValueError("source input_data must be DatasetVector or Recordset")
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            if isinstance(_source_input, DatasetVector):
                _outDatasetName = _source_input.name + "_interpolate"
            else:
                _outDatasetName = _source_input.dataset.name + "_interpolate"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, "Interpolate")
                _jvm.com.supermap.analyst.spatialanalyst.Interpolator.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.Interpolator.interpolate(parameter._jobject, _source_input._jobject, str(z_value_field), float(z_value_scale), _ds._jobject, _outDatasetName, PixelFormat._make(pixel_format)._jobject)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.Interpolator.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def interpolate_points(points, values, parameter, pixel_format, prj, out_data, z_value_scale=1.0, out_dataset_name=None, progress=None):
    """
    对点数组进行插值分析，并返回分析结果

    :param points: 需要进行插值分析的点数据
    :type points: list[Point2D]
    :param values:  点数组对应的用于插值分析的值。
    :type values: list[float]
    :param InterpolationParameter parameter:  插值方法需要的参数信息
    :param  pixel_format: 指定结果栅格数据集存储的像素，不支持 BIT64
    :type pixel_format: PixelFormat or str
    :param PrjCoordSys prj: 点数组的坐标系统。生成的结果数据集也参照该坐标系统。
    :param out_data:  结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param float z_value_scale: 插值分析值的缩放比率
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    """
    check_lic()
    if not isinstance(points, (list, tuple)):
        raise ValueError("source input_data must be list or tuple")
    if len(points) != len(values):
        raise ValueError("The count of points or values must be equal.")
    if out_data is None:
        raise ValueError("out_data cannot be None")
    if prj is None:
        raise ValueError("prj cannot be None")
    else:
        out_datasource = get_output_datasource(out_data)
        check_output_datasource(out_datasource)
        _ds = out_datasource
        if out_dataset_name is None:
            _outDatasetName = "point_interpolate"
        else:
            _outDatasetName = out_dataset_name
        _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
        _jvm = get_jvm()
        listener = None
        if progress is not None and safe_start_callback_server():
            try:
                listener = ProgressListener(progress, "interpolate_points")
                _jvm.com.supermap.analyst.spatialanalyst.Interpolator.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

            try:
                try:
                    _points = to_java_point2d_array(points)
                    _values = to_java_double_array(values)
                    if prj is not None:
                        java_prj = prj._jobject
                    else:
                        java_prj = None
                    java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.Interpolator.interpolateparameter._jobject_points_valuesjava_prjfloat(z_value_scale)_ds._jobject_outDatasetNamePixelFormat._make(pixel_format)._jobject
                except Exception as e:
                    try:
                        log_error(e)
                        java_result_dt = None
                    finally:
                        e = None
                        del e

            finally:
                return

            if listener is not None:
                try:
                    _jvm.com.supermap.analyst.spatialanalyst.Interpolator.removeSteppedListener(listener)
                except Exception as e1:
                    try:
                        log_error(e1)
                    finally:
                        e1 = None
                        del e1

                close_callback_server()
            if java_result_dt is not None:
                result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
    return try_close_output_datasource(result_dt, out_datasource)


def idw_interpolate(input_data, z_value_field, pixel_format, resolution, search_mode=SearchMode.KDTREE_FIXED_COUNT, search_radius=0.0, expected_count=12, power=1, bounds=None, z_value_scale=1.0, out_data=None, out_dataset_name=None, progress=None):
    """
    使用 IDW 插值方法对点数据集或记录集进行插值。具体参考 :py:meth:`interpolate` 和 :py:class:`.InterpolationIDWParameter`

    :param input_data:  需要进行插值分析的点数据集或点记录集
    :type input_data: DatasetVector or str or Recordset
    :param str z_value_field: 存储用于进行插值分析的值的字段名称。插值分析不支持文本类型的字段。
    :param pixel_format: 指定结果栅格数据集存储的像素，不支持 BIT64
    :type pixel_format: PixelFormat or str
    :param float resolution: 插值运算时使用的分辨率
    :param search_mode: 插值运算时，查找参与运算点的方式。不支持 QUADTREE
    :type search_mode: SearchMode or str
    :param float search_radius: 查找参与运算点的查找半径。单位与用于插值的点数据集（或记录集所属的数据集）的单位相同。查找半径决定了参与运算点的查找范围，当计算某个位置的未知数值时，会以该位置为圆心，以search_radius为半径，落在这个范围内的采样点都将参与运算，即该位置的预测值由该范围内采样点的数值决定。
                                如果设置 search_mode 为KDTREE_FIXED_COUNT，同时指定查找参与运算点的范围，当查找范围内的点数小于指定的点数时赋为空值，当查找范围内的点数大于指定的点数时，则返回距离插值点最近的指定个数的点进行插值。
    :param int expected_count: 期望参与插值运算的点数。如果设置 search_mode 为 KDTREE_FIXED_RADIUS ，同时指定参与插值运算点的个数，当查找范围内的点数小于指定的点数时赋为空值。
    :param int power: 距离权重计算的幂次。幂次值越低，内插结果越平滑，幂次值越高，内插结果细节越详细。此参数应为一个大于0的值。如果不指定此参数，方法缺省将其设置为1。
    :param Rectangle bounds: 插值分析的范围，用于确定运行结果的范围
    :param float z_value_scale: 插值分析值的缩放比率
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetGrid or str
    """
    parameter = InterpolationIDWParameter(resolution, search_mode, search_radius, expected_count, power, bounds)
    return interpolate(input_data, parameter, z_value_field, pixel_format, z_value_scale, out_data, out_dataset_name, progress)


def density_interpolate(input_data, z_value_field, pixel_format, resolution, search_radius=0.0, expected_count=12, bounds=None, z_value_scale=1.0, out_data=None, out_dataset_name=None, progress=None):
    """
    使用点密度插值方法对点数据集或记录集进行插值。具体参考 :py:meth:`interpolate` 和 :py:class:`.InterpolationDensityParameter`

    :param input_data:  需要进行插值分析的点数据集或点记录集
    :type input_data: DatasetVector or str or Recordset
    :param str z_value_field: 存储用于进行插值分析的值的字段名称。插值分析不支持文本类型的字段。
    :param pixel_format: 指定结果栅格数据集存储的像素，不支持 BIT64
    :type pixel_format: PixelFormat or str
    :param float resolution: 插值运算时使用的分辨率
    :param float search_radius: 查找参与运算点的查找半径。单位与用于插值的点数据集（或记录集所属的数据集）的单位相同。查找半径决定了参与运算点的查找范围，当计算某个位置的未知数值时，会以该位置为圆心，以search_radius为半径，落在这个范围内的采样点都将参与运算，即该位置的预测值由该范围内采样点的数值决定。
    :param int expected_count: 期望参与插值运算的点数
    :param Rectangle bounds: 插值分析的范围，用于确定运行结果的范围
    :param float z_value_scale:  插值分析值的缩放比率
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetGrid or str
    """
    parameter = InterpolationDensityParameter(resolution, search_radius, expected_count, bounds)
    return interpolate(input_data, parameter, z_value_field, pixel_format, z_value_scale, out_data, out_dataset_name, progress)


def kriging_interpolate(input_data, z_value_field, pixel_format, resolution, krighing_type="KRIGING", search_mode=SearchMode.KDTREE_FIXED_COUNT, search_radius=0.0, expected_count=12, max_point_count_in_node=50, max_point_count_for_interpolation=200, variogram_mode=VariogramMode.SPHERICAL, angle=0.0, mean=0.0, exponent=Exponent.EXP1, nugget=0.0, range_value=0.0, sill=0.0, bounds=None, z_value_scale=1.0, out_data=None, out_dataset_name=None, progress=None):
    """
    使用克吕金插值方法对点数据集或记录集进行插值。具体参考 :py:meth:`interpolate` 和 :py:class:`.InterpolationKrigingParameter`

    :param input_data:  需要进行插值分析的点数据集或点记录集
    :type input_data: DatasetVector or str or Recordset
    :param str z_value_field: 存储用于进行插值分析的值的字段名称。插值分析不支持文本类型的字段。
    :param pixel_format: 指定结果栅格数据集存储的像素，不支持 BIT64
    :type pixel_format: PixelFormat or str
    :param float resolution: 插值运算时使用的分辨率
    :param krighing_type: 插值分析的算法类型。支持设置 KRIGING, SimpleKRIGING, UniversalKRIGING 三种，默认使用 KRIGING。
    :type krighing_type: InterpolationAlgorithmType or str
    :param search_mode: 查找模式。
    :type search_mode: SearchMode or str
    :param float search_radius:  查找参与运算点的查找半径。单位与用于插值的点数据集（或记录集所属的数据集）的单位相同。查找半径决定了参与
                                     运算点的查找范围，当计算某个位置的未知数值时，会以该位置为圆心，search_radius 为半径，落在这个范围内的
                                     采样点都将参与运算，即该位置的预测值由该范围内采样点的数值决定。
    :param int expected_count:  期望参与插值运算的点数，当查找方式为变长查找时，表示期望参与运算的最多样点数。
    :param int max_point_count_in_node: 单个块内最多查找点数。当用QuadTree的查找插值点时，才可以设置块内最多点数。
    :param int max_point_count_for_interpolation: 设置块查找时，最多参与插值的点数。注意，该值必须大于零。当用QuadTree的查找插值点时，才可以设置最多参与插值的点数
    :param variogram:  克吕金（Kriging）插值时的半变函数类型。默认值为 VariogramMode.SPHERICAL
    :type variogram: VariogramMode or str
    :param float angle:  克吕金算法中旋转角度值
    :param float mean: 插值字段的平均值，即采样点插值字段值总和除以采样点数目。
    :param exponent: 用于插值的样点数据中趋势面方程的阶数
    :type exponent: Exponent or str
    :param float nugget: 块金效应值。
    :param float range_value: 自相关阈值。
    :param float sill: 基台值
    :param Rectangle bounds: 插值分析的范围，用于确定运行结果的范围
    :param float z_value_scale: 插值分析值的缩放比率
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetGrid or str
    """
    parameter = InterpolationKrigingParameter(resolution, krighing_type, search_mode, search_radius, expected_count, max_point_count_in_node, max_point_count_for_interpolation, variogram_mode, angle, mean, exponent, nugget, range_value, sill, bounds)
    return interpolate(input_data, parameter, z_value_field, pixel_format, z_value_scale, out_data, out_dataset_name, progress)


def rbf_interpolate(input_data, z_value_field, pixel_format, resolution, search_mode=SearchMode.KDTREE_FIXED_COUNT, search_radius=0.0, expected_count=12, max_point_count_in_node=50, max_point_count_for_interpolation=200, smooth=0.100000001490116, tension=40, bounds=None, z_value_scale=1.0, out_data=None, out_dataset_name=None, progress=None):
    """
    使用径向基函数（RBF） 插值方法对点数据集或记录集进行插值。具体参考 :py:meth:`interpolate` 和 :py:class:`.InterpolationRBFParameter`

    :param input_data:  需要进行插值分析的点数据集或点记录集
    :type input_data: DatasetVector or str or Recordset
    :param str z_value_field: 存储用于进行插值分析的值的字段名称。插值分析不支持文本类型的字段。
    :param pixel_format: 指定结果栅格数据集存储的像素，不支持 BIT64
    :type pixel_format: PixelFormat or str
    :param float resolution: 插值运算时使用的分辨率
    :param search_mode: 查找模式。
    :type search_mode: SearchMode or str
    :param float search_radius: 查找参与运算点的查找半径。单位与用于插值的点数据集（或记录集所属的数据集）的单位相同。查找半径决定了参与运算点的查找范围，当计算某个位置的未知数值时，会以该位置为圆心，search_radius 为半径，落在这个范围内的采样点都将参与运算，即该位置的预测值由该范围内采样点的数值决定。
    :param int expected_count: 期望参与插值运算的点数，当查找方式为变长查找时，表示期望参与运算的最多样点数。
    :param int max_point_count_in_node: 单个块内最多查找点数。当用QuadTree的查找插值点时，才可以设置块内最多点数。
    :param int max_point_count_for_interpolation: 设置块查找时，最多参与插值的点数。注意，该值必须大于零。当用QuadTree的查找插值点时，才可以设置最多参与插值的点数
    :param float smooth: 光滑系数，值域为 [0,1]
    :param float tension: 张力系数
    :param Rectangle bounds: 插值分析的范围，用于确定运行结果的范围
    :param float z_value_scale: 插值分析值的缩放比率
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetGrid or str

    """
    parameter = InterpolationRBFParameter(resolution, search_mode, search_radius, expected_count, max_point_count_in_node, max_point_count_for_interpolation, smooth, tension, bounds)
    return interpolate(input_data, parameter, z_value_field, pixel_format, z_value_scale, out_data, out_dataset_name, progress)


def vector_to_raster(input_data, value_field, clip_region=None, cell_size=None, pixel_format=PixelFormat.SINGLE, out_data=None, out_dataset_name=None, progress=None):
    """
    通过指定转换参数设置将矢量数据集转换为栅格数据集。

    :param input_data: 待转换的矢量数据集。支持点、线和面数据集
    :type input_data: DatasetVector or str
    :param str value_field: 矢量数据集中存储栅格值的字段
    :param clip_region: 转换的有效区域
    :type clip_region: GeoRegion or Rectangle
    :param float cell_size: 结果栅格数据集的单元格大小
    :param pixel_format: 如果将矢量数据转为像素格式 为 UBIT1、UBIT4 和 UBIT8 的栅格数据集，矢量数据中值为 0 的对象在结果栅格中会丢失。
    :type pixel_format: PixelFormat or str
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetGrid or str
    """
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    else:
        if not isinstance(_source_input, DatasetVector):
            raise ValueError("source input_data must be DatasetVector")
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + "_raster"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    try:
        try:
            parameter = _jvm.com.supermap.analyst.spatialanalyst.ConversionAnalystParameter()
            parameter.setSourceDataset(_source_input._jobject)
            parameter.setValueFieldName(value_field)
            if clip_region is not None:
                if isinstance(clip_region, Rectangle):
                    clip_region = clip_region.to_region()
                if isinstance(clip_region, GeoRegion):
                    parameter.setClipRegion(clip_region._jobject)
            if cell_size is not None:
                parameter.setCellSize(float(cell_size))
            if pixel_format is not None:
                parameter.setPixelFormat(PixelFormat._make(pixel_format)._jobject)
            parameter.setTargetDatasource(_ds._jobject)
            parameter.setTargetDatasetName(_outDatasetName)
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "VectorToRaster")
                        _jvm.com.supermap.analyst.spatialanalyst.ConversionAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.ConversionAnalyst.vectorToRaster(parameter)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.ConversionAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def raster_to_vector(input_data, value_field, out_dataset_type=DatasetType.POINT, back_or_no_value=-9999, back_or_no_value_tolerance=0.0, specifiedvalue=None, specifiedvalue_tolerance=0.0, valid_region=None, is_thin_raster=True, smooth_method=None, smooth_degree=0.0, out_data=None, out_dataset_name=None, progress=None):
    """
    通过指定转换参数设置将栅格数据集转换为矢量数据集。

    :param input_data: 待转换的栅格数据集或影像数据集
    :type input_data: DatasetGrid or DatasetImage or str
    :param str value_field:  结果矢量数据集中存储值的字段
    :param out_dataset_type: 结果数据集类型，支持点、线和面数据集。当结果数据集类型为线数据聚集时，is_thin_raster, smooth_method, smooth_degree 才有效。
    :type out_dataset_type: DatasetType or str
    :param back_or_no_value: 设置栅格的背景色或表示无值的值，只在栅格转矢量时有效。 允许用户指定一个值来标识那些不需要转换的单元格:

                              - 当被转换的栅格数据为栅格数据集时，栅格值为指定的值的单元格被视为无值，这些单元格不会被转换，而栅格的原无值将作为有效值来参与转换。
                              - 当被转化的栅格数据为影像数据集时，栅格值为指定的值的单元格被视为背景色，从而不参与转换。

                             需要注意，影像数据集中栅格值代表的是一个颜色或颜色的索引值，与其像素格式（PixelFormat）有关。对于 BIT32、UBIT32、RGBA、RGB 和 BIT16

                             格式的影像数据集，其栅格值对应为 RGB 颜色，可以使用一个 tuple 或 int 来表示 RGB 值 或 RGBA 值

                             对于 UBIT8 和 UBIT4 格式的影像数据集，其栅格值对应的是颜色的索引值，因此，应为该属性设置的值为被视为背景色的颜色对应的索引值。
    :type back_or_no_value: int or tuple
    :param back_or_no_value_tolerance: 栅格背景色的容限或无值的容限，只在栅格转矢量时有效。用于配合 back_or_no_value 方法（指定栅格无值或者背景色）来共同确定栅格数据中哪些值不被转换:

                                        - 当被转换的栅格数据为栅格数据集时，如果指定为无值的值为 a，指定的无值的容限为 b，则栅格值在[a-b,a+b]范围内的单元格均被视为无值。需要注意，无值的容限是用户指定的无值的值的容限，与栅格中原无值无关。
                                        - 当被转化的栅格数据为影像数据集时，该容限值为一个32位整型值或tuple，tuple用于表示 RGB值或RGBA值。
                                        - 该值代表的意义与影像数据集的像素格式有关：对于栅格值对应 RGB 颜色的影像数据集，该值在系统内部被转为分别对应 R、G、B 的三个容限值，
                                          例如，指定为背景色的颜色为(100,200,60)，指定的容限值为329738，该值对应的 RGB 值为(10,8,5)，则值在 (90,192,55) 和 (110,208,65)
                                          之间的颜色均为背景色；对于栅格值为颜色索引值的影像数据集，该容限值为颜色索引值的容限，在该容限范围内的栅格值均视为背景色。

    :type back_or_no_value_tolerance: int or float or tuple
    :param specifiedvalue: 栅格按值转矢量时指定的栅格值。只将具有该值的栅格转为矢量。
    :type specifiedvalue: int or float or tuple
    :param specifiedvalue_tolerance: 栅格按值转矢量时指定的栅格值的容限
    :type specifiedvalue_tolerance: int or float or tuple
    :param valid_region: 转换的有效区域
    :type valid_region: GeoRegion or Rectangle
    :param bool is_thin_raster: 转换之前是否进行栅格细化。
    :param smooth_method: 光滑方法，只在栅格转为矢量线数据时有效
    :type smooth_method: SmoothMethod or str
    :param int smooth_degree: 光滑度。光滑度的值越大，光滑度的值越大，则结果矢量线的光滑度越高。当 smooth_method 不为 NONE 时有效。光滑度的有效取值与光滑方法有关，光滑方法有 B 样条法和磨角法:

                                - 光滑方法为 B 样条法时，光滑度的有效取值为大于等于2的整数，建议取值范围为[2,10]。
                                - 光滑方法为磨角法时，光滑度代表一次光滑过程中磨角的次数，设置为大于等于1的整数时有效

    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector or str

    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    else:
        if not isinstance(_source_input, (DatasetGrid, DatasetImage)):
            raise ValueError("source input_data must be DatasetGrid or DatasetImage")
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + "_vector"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    try:
        try:
            parameter = _jvm.com.supermap.analyst.spatialanalyst.ConversionAnalystParameter()
            parameter.setSourceDataset(_source_input._jobject)
            parameter.setValueFieldName(value_field)
            if out_dataset_type is not None:
                parameter.setTargetDatasetType(DatasetType._make(out_dataset_type)._jobject)
            if back_or_no_value is not None:
                if isinstance(back_or_no_value, tuple):
                    back_or_no_value = tuple_to_color(back_or_no_value)
                parameter.setBackOrNoValue(int(back_or_no_value))
            if back_or_no_value_tolerance is not None:
                if isinstance(back_or_no_value_tolerance, tuple):
                    back_or_no_value_tolerance = tuple_to_color(back_or_no_value_tolerance)
                parameter.setBackOrNoValueTolerance(float(back_or_no_value_tolerance))
            if specifiedvalue is not None:
                if isinstance(specifiedvalue, tuple):
                    specifiedvalue = tuple_to_color(specifiedvalue)
                parameter.setSpecifiedValue(int(specifiedvalue))
            if specifiedvalue_tolerance is not None:
                if isinstance(specifiedvalue_tolerance, tuple):
                    specifiedvalue_tolerance = tuple_to_color(specifiedvalue_tolerance)
                parameter.setSpecifiedValueTolerance(float(specifiedvalue_tolerance))
            if is_thin_raster is not None:
                parameter.setThinRaster(bool(is_thin_raster))
            if smooth_method is not None:
                parameter.setSmoothMethod(SmoothMethod._make(smooth_method)._jobject)
            if smooth_degree is not None:
                parameter.setSmoothDegree(int(smooth_degree))
            parameter.setTargetDatasource(_ds._jobject)
            parameter.setTargetDatasetName(_outDatasetName)
            if valid_region is not None:
                if isinstance(valid_region, Rectangle):
                    valid_region = valid_region.to_region()
            if isinstance(valid_region, GeoRegion):
                parameter.setClipRegion(oj(valid_region))
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "RasterToVector")
                        _jvm.com.supermap.analyst.spatialanalyst.ConversionAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.ConversionAnalyst.rasterToVector(parameter)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.ConversionAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def cost_distance(input_data, cost_grid, max_distance=-1.0, cell_size=None, out_data=None, out_distance_grid_name=None, out_direction_grid_name=None, out_allocation_grid_name=None, progress=None):
    """
    根据给定的参数，生成耗费距离栅格，以及耗费方向栅格和耗费分配栅格。

    实际应用中，直线距离往往不能满足要求。例如，从 B 到最近源 A 的直线距离与从 C 到最近源 A 的直线距离相同，若 BA 路段交通拥堵，而 CA 路段交通畅
    通，则其时间耗费必然不同；此外，通过直线距离对应的路径到达最近源时常常是不可行的，例如，遇到河流、高山等障碍物就需要绕行，这时就需要考虑其耗费距离。

    该方法根据源数据集和耗费栅格生成相应的耗费距离栅格、耗费方向栅格（可选）和耗费分配栅格（可选）。源数据可以是矢量数据（点、线、面），也可以是栅格数据。
    对于栅格数据，要求除标识源以外的单元格为无值。

     * 耗费距离栅格的值表示该单元格到最近源的最小耗费值（可以是各种类型的耗费因子，也可以是各感兴趣的耗费因子的加权）。最近源
       是当前单元格到达所有的源中耗费最小的一个源。耗费栅格中为无值的单元格在输出的耗费距离栅格中仍为无值。

       单元格到达源的耗费的计算方法是，从待计算单元格的中心出发，到达最近源的最小耗费路径在每个单元格上经过的距离乘以耗费栅格
       上对应单元格的值，将这些值累加即为单元格到源的耗费值。因此，耗费距离的计算与单元格大小和耗费栅格有关。在下面的示意图中，
       源栅格和耗费栅格的单元格大小（cell_size）均为2，单元格（2,1）到达源（0,0）的最小耗费路线如右图中红线所示：

       .. image:: ../image/CostDistance_1.png

       那么单元格（2,1）到达源的最小耗费（即耗费距离）为：

       .. image:: ../image/CostDistance_2.png

     * 耗费方向栅格的值表达的是从该单元格到达最近的源的最小耗费路径的行进方向。在耗费方向栅格中，可能的行进方向共有八个（正北、
       正南、正西、正东、西北、西南、东南、东北），使用1到8八个整数对这八个方向进行编码，如下图所示。注意，源所在的单元格在耗费
       方向栅格中的值为0，耗费栅格中为无值的单元格在输出的耗费方向栅格中将被赋值为15。

       .. image:: ../image/CostDistance_3.png

     * 耗费分配栅格的值为单元格的最近源的值（源为栅格时，为最近源的栅格值；源为矢量对象时，为最近源的 SMID），单元格到达最近的
       源具有最小耗费距离。耗费栅格中为无值的单元格在输出的耗费分配栅格中仍为无值。

       下图为生成耗费距离的示意图。其中，在耗费栅格上，使用蓝色箭头标识了单元格到达最近源的行进路线，耗费方向栅格的值即标示了
       当前单元格到达最近源的最小耗费路线的行进方向。

       .. image:: ../image/CostDistance_4.png

    下图为生成耗费距离栅格的一个实例，其中源数据集为点数据集，耗费栅格为对应区域的坡度栅格的重分级结果，生成了耗费距离栅格、耗费方向栅格和耗费分配栅格。

    .. image:: ../image/CostDistance.png

    :param input_data: 生成距离栅格的源数据集。源是指感兴趣的研究对象或地物，如学校、道路或消防栓等。包含源的数据集，即为源数据集。源数据集可以为
                        点、线、面数据集，也可以为栅格数据集，栅格数据集中具有有效值的栅格为源，对于无值则视为该位置没有源。
    :type input_data: DatasetVector or DatasetGrid or str
    :param DatasetGrid cost_grid:  耗费栅格。其栅格值不能为负值。该数据集为一个栅格数据集，每个单元格的值表示经过此单元格时的单位耗费。
    :param float max_distance: 生成距离栅格的最大距离，大于该距离的栅格其计算结果取无值。若某个栅格单元格 A 到最近源之间的最短距离大于该值，则结果数据集中该栅格的值取无值。
    :param float cell_size: 结果数据集的分辨率，是生成距离栅格的可选参数
    :param out_data: 结果数据集所在的数据源
    :type out_data:  Datasource or DatasourceConnectionInfo or str
    :param str out_distance_grid_name: 结果距离栅格数据集的名称。如果名称为空，将自动获取有效的数据集名称。
    :param str out_direction_grid_name: 方向栅格数据集的名称，如果为空，将不生成方向栅格数据集
    :param str out_allocation_grid_name:  分配栅格数据集的名称，如果为空，将不生成 分配栅格数据集
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 如果生成成功，返回结果数据集或数据集名称的元组，其中第一个为距离栅格数据集，第二个为方向栅格数据集，第三个为分配栅格数据集，如果没有设置方向栅格数据集名称和
             分配栅格数据集名称，对应的值为 None
    :rtype: tuple[DataetGrid] or tuple[str]
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    if not isinstance(_source_input, (DatasetVector, DatasetGrid)):
        raise ValueError("source input_data must be DatasetVector,  DatasetGrid")
    _source_cost_grid = get_input_dataset(cost_grid)
    if _source_cost_grid is None:
        raise ValueError("cost grid dataset is None")
    else:
        if not isinstance(_source_cost_grid, DatasetGrid):
            raise ValueError("cost input_data must be DatasetGrid")
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_distance_grid_name is None:
            _outDistanceGridName = _source_input.name + "_distance"
        else:
            _outDistanceGridName = out_distance_grid_name
    _outDistanceGridName = _ds.get_available_dataset_name(_outDistanceGridName)
    _jvm = get_jvm()
    try:
        try:
            parameter = _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalystParameter()
            parameter.setSourceDataset(_source_input._jobject)
            parameter.setCostGrid(_source_cost_grid._jobject)
            parameter.setTargetDatasource(_ds._jobject)
            parameter.setDistanceGridName(_outDistanceGridName)
            if max_distance is not None:
                parameter.setMaxDistance(float(max_distance))
            if cell_size is not None:
                parameter.setCellSize(float(cell_size))
            if out_direction_grid_name is not None:
                parameter.setDirectionGridName(out_direction_grid_name)
            if out_allocation_grid_name is not None:
                parameter.setAllocationGridName(out_allocation_grid_name)
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "CostDistance")
                        _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            distance_analyst_result = _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalyst.costDistance(parameter)
        except Exception as e:
            try:
                log_error(e)
                distance_analyst_result = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif distance_analyst_result is not None:
            results = []
            dt = distance_analyst_result.getDistanceDatasetGrid()
            if dt is not None:
                results.append(_ds[dt.getName()])
            else:
                results.append(None)
            dt = distance_analyst_result.getDirectionDatasetGrid()
            if dt is not None:
                results.append(_ds[dt.getName()])
            else:
                results.append(None)
            dt = distance_analyst_result.getAllocationDatasetGrid()
            if dt is not None:
                results.append(_ds[dt.getName()])
            else:
                results.append(None)
            if out_data is not None:
                return try_close_output_datasource(results, out_datasource)
            return results
        else:
            if out_data is not None:
                try_close_output_datasource(None, out_datasource)
            return


def cost_path(input_data, distance_dataset, direction_dataset, compute_type, out_data=None, out_dataset_name=None, progress=None):
    """
    根据耗费距离栅格和耗费方向栅格，分析从目标出发到达最近源的最短路径栅格。
    该方法根据给定的目标数据集，以及通过“生成耗费距离栅格”功能得到的耗费距离栅格和耗费方向栅格，来计算每个目标对象到达最近的源的最短路径，也就是最小
    耗费路径。该方法不需要指定源所在的数据集，因为源的位置在距离栅格和方向栅格中能够体现出来，即栅格值为 0 的单元格。生成的最短路径栅格是一个二值栅
    格，值为 1 的单元格表示路径，其他单元格的值为 0。

    例如，将购物商场（一个点数据集）作为源，各居民小区（一个面数据集）作为目标，分析从各居民小区出发，如何到达距其最近的购物商场。实现的过程是，首先
    针对源（购物商场）生成距离栅格和方向栅格，然后将居民小区作为目标区域，通过最短路径分析，得到各居民小区（目标）到最近购物商场（源）的最短路径。该
    最短路径包含两种含义：通过直线距离栅格与直线方向栅格，将得到最小直线距离路径；通过耗费距离栅格与耗费方向栅格，则得到最小耗费路径。

    注意，该方法中要求输入的耗费距离栅格和耗费方向栅格必须是匹配的，也就是说二者应是同一次使用“生成耗费距离栅格”功能生成的。此外，有三种计算最短路径
    的方式：像元路径、区域路径和单一路径，具体含义请参见 :py:class:`.ComputeType` 类。

    :param input_data: 目标所在的数据集。可以为点、线、面或栅格数据集。如果是栅格数据，要求除标识目标以外的单元格为无值。
    :type input_data: DatasetVector or DatasetGrid or DatasetImage or str
    :param distance_dataset: 耗费距离栅格数据集。
    :type distance_dataset: DatasetGrid or str
    :param direction_dataset:  耗费方向栅格数据集
    :type direction_dataset: DatasetGrid or str
    :param compute_type: 栅格距离最短路径分析的计算方式
    :type compute_type: ComputeType or str
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector or str
    """
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    if not isinstance(_source_input, (DatasetVector, DatasetGrid)):
        raise ValueError("source input_data must be DatasetGrid")
    _source_distance = get_input_dataset(distance_dataset)
    if _source_distance is None:
        raise ValueError("source distance dataset is None")
    if not isinstance(_source_distance, DatasetGrid):
        raise ValueError("source distance dataset must be DatasetGrid")
    _source_direction = get_input_dataset(direction_dataset)
    if _source_direction is None:
        raise ValueError("source direction dataset is None")
    else:
        if not isinstance(_source_direction, DatasetGrid):
            raise ValueError("source direction dataset must be DatasetGrid")
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + "_costpath"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    try:
        try:
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "CostPath")
                        _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalyst.costPath(_source_input._jobject, _source_distance._jobject, _source_direction._jobject, ComputeType._make(compute_type)._jobject, _ds._jobject, _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def cost_path_line(source_point, target_point, cost_grid, smooth_method=None, smooth_degree=0, progress=None):
    """
    根据给定的参数，计算源点和目标点之间的最小耗费路径（一个二维矢量线对象）。该方法用于根据给定的源点、目标点和耗费栅格，计算源点与目标点之间的最小耗费路径

    下图为计算两点间最小耗费路径的实例。该例以 DEM 栅格的坡度的重分级结果作为耗费栅格，分析给定的源点和目标点之间的最小耗费路径。

    .. image:: ../image/CostPathLine.png

    :param Point2D source_point: 指定的源点
    :param Point2D target_point: 指定的目标点
    :param DatasetGrid cost_grid:  耗费栅格。其栅格值不能为负值。该数据集为一个栅格数据集，每个单元格的值表示经过此单元格时的单位耗费。
    :param smooth_method: 计算两点（源和目标）间最短路径时对结果路线进行光滑的方法
    :type smooth_method: SmoothMethod or str
    :param int smooth_degree: 计算两点（源和目标）间最短路径时对结果路线进行光滑的光滑度。
                                光滑度的值越大，光滑度的值越大，则结果矢量线的光滑度越高。当 smooth_method 不为 NONE 时有效。光滑度的有效取值与光滑方法有关，光滑方法有 B 样条法和磨角法:
                                - 光滑方法为 B 样条法时，光滑度的有效取值为大于等于2的整数，建议取值范围为[2,10]。
                                - 光滑方法为磨角法时，光滑度代表一次光滑过程中磨角的次数，设置为大于等于1的整数时有效
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 返回表示最短路径的线对象和最短路径的花费
    :rtype: tuple[GeoLine,float]
    """
    _source_grid = get_input_dataset(cost_grid)
    if _source_grid is None:
        raise ValueError("source Grid dataset is None")
    if not isinstance(_source_grid, DatasetGrid):
        raise ValueError("source Grid dataset must be DatasetGrid")
    _jvm = get_jvm()
    try:
        try:
            parameter = _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalystParameter()
            parameter.setCostGrid(_source_grid._jobject)
            if smooth_method is not None:
                parameter.setPathLineSmoothMethod(SmoothMethod._make(smooth_method)._jobject)
            if smooth_degree is not None:
                parameter.setPathLineSmoothDegree(int(smooth_degree))
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "CostPathLine")
                        _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_result = _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalyst.costPathLine(source_point._jobject, target_point._jobject, parameter)
        except Exception as e:
            try:
                log_error(e)
                java_result = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if java_result is not None:
            return (
             Geometry._from_java_object(java_result.getPathLine()), java_result.getCost())
        return


def path_line(target_point, distance_dataset, direction_dataset, smooth_method=None, smooth_degree=0):
    """
    根据距离栅格和方向栅格，分析从目标点出发到达最近源的最短路径（一个二维矢量线对象）。 该方法根据距离栅格和方向栅格，分析给定的目标点到达最近源的最短路径。其中距离栅格和方向栅格可以是耗费距离栅格和耗费方向栅格，也可以是表面距离栅格和表面方向栅格。

        - 当距离栅格为耗费距离栅格，方向栅格为耗费方向栅格时，该方法计算得出的是最小耗费路径。耗费距离栅格和耗费方向栅格可以通过 costDistance 方法生成。注意，此方法要求二者是同一次生成的结果。
        - 当距离栅格为表面距离栅格，方向栅格为表面方向栅格时，该方法计算得出的是最短表面距离路径。表面距离栅格和表面方向栅格可以通过 surfaceDistance 方法生成。同样，此方法要求二者是同一次生成的结果。

    源的位置在距离栅格和方向栅格中能够体现出来，即栅格值为 0 的单元格。源可以是一个，也可以有多个。当有多个源时，最短路径是目标点到达其最近的源的路径。

    下图为源、表面栅格、耗费栅格和目标点，其中耗费栅格是对表面栅格计算坡度后重分级的结果。

    .. image:: ../image/PathLine_2.png

    使用如上图所示的源和表面栅格生成表面距离栅格和表面方向栅格，然后计算目标点到最近源的最短表面距离路径；使用源和耗费栅格生成耗费距离栅格和耗费方向栅格，然后计算目标点到最近源的最小耗费路径。得到的结果路径如下图所示：

    .. image:: ../image/PathLine_3.png
    

    :param Point2D target_point: 指定的目标点。
    :param DatasetGrid distance_dataset: 指定的距离栅格。可以是耗费距离栅格或表面距离栅格。
    :param DatasetGrid direction_dataset: 指定的方向栅格。与距离栅格对应，可以是耗费方向栅格或表面方向栅格。
    :param smooth_method: 计算两点（源和目标）间最短路径时对结果路线进行光滑的方法
    :type smooth_method: SmoothMethod or str
    :param int smooth_degree: 计算两点（源和目标）间最短路径时对结果路线进行光滑的光滑度。
                                光滑度的值越大，光滑度的值越大，则结果矢量线的光滑度越高。当 smooth_method 不为 NONE 时有效。光滑度的有效取值与光滑方法有关，光滑方法有 B 样条法和磨角法:
                                - 光滑方法为 B 样条法时，光滑度的有效取值为大于等于2的整数，建议取值范围为[2,10]。
                                - 光滑方法为磨角法时，光滑度代表一次光滑过程中磨角的次数，设置为大于等于1的整数时有效
    :return: 返回表示最短路径的线对象和最短路径的花费
    :rtype: tuple[GeoLine,float]
    """
    check_lic()
    _source_distance = get_input_dataset(distance_dataset)
    if _source_distance is None:
        raise ValueError("source distance dataset is None")
    if not isinstance(_source_distance, DatasetGrid):
        raise ValueError("source distance dataset must be DatasetGrid")
    _source_direction = get_input_dataset(direction_dataset)
    if _source_direction is None:
        raise ValueError("source direction dataset is None")
    if not isinstance(_source_direction, DatasetGrid):
        raise ValueError("source direction dataset must be DatasetGrid")
    _jvm = get_jvm()
    try:
        try:
            java_result = _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalyst.pathLine(target_point._jobject, _source_distance._jobject, _source_direction._jobject, SmoothMethod._make(smooth_method)._jobject, int(smooth_degree))
        except Exception as e:
            try:
                log_error(e)
                java_result = None
            finally:
                e = None
                del e

    finally:
        if java_result is not None:
            return (
             Geometry._from_java_object(java_result.getPathLine()), java_result.getCost())
        return


def straight_distance(input_data, max_distance=-1.0, cell_size=None, out_data=None, out_distance_grid_name=None, out_direction_grid_name=None, out_allocation_grid_name=None, progress=None):
    """
    根据给定的参数，生成直线距离栅格，以及直线方向栅格和直线分配栅格。

    该方法用于对源数据集生成相应的直线距离栅格、直线方向栅格（可选）和直线分配栅格（可选），三个结果数据集的区域范围与源数据集的范围一致。生成直线距
    离栅格的源数据可以是矢量数据（点、线、面），也可以是栅格数据。对于栅格数据，要求除标识源以外的单元格为无值。

    * 直线距离栅格的值代表该单元格到最近的源的欧氏距离（即直线距离）。最近源是当前单元格到达所有源中直线距离最短的一个源。对于每个
      单元格，它的中心与源的中心相连的直线即为单元格到源的距离，计算的方法是通过二者形成的直角三角形的两条直角边来计算，因此直线
      距离的计算只与单元格大小（即分辨率）有关。下图为直线距离计算的示意图，其中源栅格的单元格大小（cell_size）为10。

      .. image:: ../image/StraightDistance_1.png

      那么第三行第三列的单元格到源的距离L为：

      .. image:: ../image/StraightDistance_2.png

    * 直线方向栅格的值表示该单元格到最近的源的方位角，单位为度。以正东方向为90度，正南为180度，正西为270度，正北为360度，顺时针方向旋转，范围为0-360度，并规定对应源的栅格值为0度。

    * 直线分配栅格的值为单元格的最近源的值（源为栅格时，为最近源的栅格值；源为矢量对象时，为最近源的 SMID），因此从直线分配栅格中可以得知每个单元格的最近的源是哪个。

    下图为生成直线距离的示意图。单元格大小均为2。

    .. image:: ../image/StraightDistance_3.png

    直线距离栅格通常用于分析经过的路线没有障碍或等同耗费的情况，例如，救援飞机飞往最近的医院时，空中没有障碍物，因此采用哪条路线的耗费均相同，此时通过直线距离栅格就可以确定从救援飞机所在地点到周围各医院的距离；根据直线分配栅格可以获知离救援飞机所在地点最近的医院；由直线方向栅格可以确定最近的医院在救援飞机所在地点的方位。

    然而，在救援汽车开往最近医院的实例中，因为地表有各种类型的障碍物，采用不同的路线的耗费不尽相同，这时，就需要使用耗费距离栅格来进行分析。有关耗费距离栅格请参见 CostDistance 方法。

    下图为生成直线距离栅格的一个实例，其中源数据集为点数据集，生成了直线距离栅格、直线方向栅格和直线分配栅格。

    .. image:: ../image/StraightDistance.png

    注意：当数据集的最小外接矩形（bounds）为某些特殊情形时，结果数据集的 Bounds 按以下规则取值：

    * 当源数据集的 Bounds 的高和宽均为 0 （如只有一个矢量点）时，结果数据集的 Bounds 的高和宽，均取源数据集 Bounds 的左边界值（Left）和下边界值（Right）二者绝对值较小的一个。
    * 当源数据集的 Bounds 的高为 0 而宽不为 0 （如只有一条水平线）时，结果数据集的 Bounds 的高和宽，均等于源数据集 Bounds 的宽。
    * 当源数据集的 Bounds 的宽为 0 而高不为 0 （如只有一条竖直线）时，结果数据集的 Bounds 的高和宽，均等于源数据集 Bounds 的高。

    :param input_data: 生成距离栅格的源数据集。源是指感兴趣的研究对象或地物，如学校、道路或消防栓等。包含源的数据集，即为源数据集。源数据集可以为
                        点、线、面数据集，也可以为栅格数据集，栅格数据集中具有有效值的栅格为源，对于无值则视为该位置没有源。
    :type input_data: DatasetVector or DatasetGrid or DatasetImage or str
    :param float max_distance: 生成距离栅格的最大距离，大于该距离的栅格其计算结果取无值。若某个栅格单元格 A 到最近源之间的最短距离大于该值，则结果数据集中该栅格的值取无值。
    :param float cell_size: 结果数据集的分辨率，是生成距离栅格的可选参数
    :param out_data: 结果数据集所在的数据源
    :type out_data:  Datasource or DatasourceConnectionInfo or str
    :param str out_distance_grid_name: 结果距离栅格数据集的名称。如果名称为空，将自动获取有效的数据集名称。
    :param str out_direction_grid_name: 方向栅格数据集的名称，如果为空，将不生成方向栅格数据集
    :param str out_allocation_grid_name:  分配栅格数据集的名称，如果为空，将不生成 分配栅格数据集
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 如果生成成功，返回结果数据集或数据集名称的元组，其中第一个为距离栅格数据集，第二个为方向栅格数据集，第三个为分配栅格数据集，如果没有设置方向栅格数据集名称和
             分配栅格数据集名称，对应的值为 None
    :rtype: tuple[DataetGrid] or tuple[str]
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    else:
        if not isinstance(_source_input, (DatasetVector, DatasetGrid)):
            raise ValueError("source input_data must be DatasetVector or DatasetGrid")
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_distance_grid_name is None:
            _outDistanceGridName = _source_input.name + "_distance"
        else:
            _outDistanceGridName = out_distance_grid_name
    _outDistanceGridName = _ds.get_available_dataset_name(_outDistanceGridName)
    _jvm = get_jvm()
    try:
        try:
            parameter = _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalystParameter()
            parameter.setSourceDataset(_source_input._jobject)
            parameter.setTargetDatasource(_ds._jobject)
            parameter.setDistanceGridName(_outDistanceGridName)
            if max_distance is not None:
                parameter.setMaxDistance(float(max_distance))
            if cell_size is not None:
                parameter.setCellSize(float(cell_size))
            if out_direction_grid_name is not None:
                parameter.setDirectionGridName(out_direction_grid_name)
            if out_allocation_grid_name is not None:
                parameter.setAllocationGridName(out_allocation_grid_name)
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "StraightDistance")
                        _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            distance_analyst_result = _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalyst.straightDistance(parameter)
        except Exception as e:
            try:
                log_error(e)
                distance_analyst_result = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif distance_analyst_result is not None:
            results = []
            dt = distance_analyst_result.getDistanceDatasetGrid()
            if dt is not None:
                results.append(_ds[dt.getName()])
            else:
                results.append(None)
            dt = distance_analyst_result.getDirectionDatasetGrid()
            if dt is not None:
                results.append(_ds[dt.getName()])
            else:
                results.append(None)
            dt = distance_analyst_result.getAllocationDatasetGrid()
            if dt is not None:
                results.append(_ds[dt.getName()])
            else:
                results.append(None)
            if out_data is not None:
                return try_close_output_datasource(results, out_datasource)
            return results
        else:
            if out_data is not None:
                try_close_output_datasource(None, out_datasource)
            return


def surface_distance(input_data, surface_grid_dataset, max_distance=-1.0, cell_size=None, max_upslope_degrees=90.0, max_downslope_degree=90.0, out_data=None, out_distance_grid_name=None, out_direction_grid_name=None, out_allocation_grid_name=None, progress=None):
    """
    根据给定的参数，生成表面距离栅格，以及表面方向栅格和表面分配栅格。 该方法根据源数据集和表面栅格生成相应的表面距离栅格、表面方向栅格（可选）和表面
    分配栅格（可选）。源数据可以是矢量数据（点、线、面），也可以是栅格数据。对于栅格数据，要求除标识源以外的单元格为无值。

    * 表面距离栅格的值表示表面栅格上该单元格到最近源的表面最短距离。最近源是指当前单元格到达所有的源中表面距离最短的一个源。表面栅格中为无值的单元格在输出的表面距离栅格中仍为无值。
      从当前单元格（设为 g1）到达下一个单元格（设为 g2）的表面距离 d 的计算方法为：

      .. image:: ../image/SurfaceDistance_1.png

      其中，b 为 g1 的栅格值（即高程）与 g2 的栅格值的差；a 为 g1 与 g2 的中心点之间的直线距离，其值考虑两种情况，当 g2 是与
      g1 相邻的上、下、左、右四个单元格之一时，a 的值等于单元格大小；当 g2 是与 g1 对角相邻的四个单元格之一时，a 的值为单元格大小乘以根号 2。

      当前单元格到达最近源的距离值就是沿着最短路径的表面距离值。在下面的示意图中，源栅格和表面栅格的单元格大小（CellSize）均为
      1，单元格（2,1）到达源（0,0）的表面最短路径如右图中红线所示：

      .. image:: ../image/SurfaceDistance_2.png

      那么单元格（2,1）到达源的最短表面距离为：

      .. image:: ../image/SurfaceDistance_3.png

    * 表面方向栅格的值表达的是从该单元格到达最近源的最短表面距离路径的行进方向。在表面方向栅格中，可能的行进方向共有八个（正北、
      正南、正西、正东、西北、西南、东南、东北），使用 1 到 8 八个整数对这八个方向进行编码，如下图所示。注意，源所在的单元格在表面方向栅格中的值为 0，表面栅格中为无值的单元格在输出的表面方向栅格中将被赋值为 15。

      .. image:: ../image/CostDistance_3.png

    * 表面分配栅格的值为单元格的最近源的值（源为栅格时，为最近源的栅格值；源为矢量对象时，为最近源的 SMID），单元格到达最近的源具有最短表面距离。表面栅格中为无值的单元格在输出的表面分配栅格中仍为无值。
      下图为生成表面距离的示意图。其中，在表面栅格上，根据结果表面方向栅格，使用蓝色箭头标识了单元格到达最近源的行进方向。

      SurfaceDistance_4.png

    通过上面的介绍，可以了解到，结合表面距离栅格及对应的方向、分配栅格，可以知道表面栅格上每个单元格最近的源是哪个，表面距离是多少以及如何到达该最近源。

    注意，生成表面距离时可以指定最大上坡角度（max_upslope_degrees）和最大下坡角度（max_downslope_degree），从而在寻找最近源时
    避免经过上下坡角度超过指定值的单元格。从当前单元格行进到下一个高程更高的单元格为上坡，上坡角度即上坡方向与水平面的夹角，如果
    上坡角度大于给定值，则不会考虑此行进方向；从当前单元格行进到下一个高程小于当前高程的单元格为下坡，下坡角度即下坡方向与水平面
    的夹角，同样的，如果下坡角度大于给定值，则不会考虑此行进方向。如果由于上下坡角度限制，使得当前单元格没能找到最近源，那么在
    表面距离栅格中该单元格的值为无值，在方向栅格和分配栅格中也为无值。

    下图为生成表面距离栅格的一个实例，其中源数据集为点数据集，表面栅格为对应区域的 DEM 栅格，生成了表面距离栅格、表面方向栅格和表面分配栅格。

    .. image:: ../image/SurfaceDistance.png

    :param input_data: 生成距离栅格的源数据集。源是指感兴趣的研究对象或地物，如学校、道路或消防栓等。包含源的数据集，即为源数据集。源数据集可以为
                        点、线、面数据集，也可以为栅格数据集，栅格数据集中具有有效值的栅格为源，对于无值则视为该位置没有源。
    :type input_data: DatasetVector or DatasetGrid or DatasetImage or str
    :param surface_grid_dataset: 表面栅格
    :type surface_grid_dataset: DatasetGrid or str
    :param float max_distance: 生成距离栅格的最大距离，大于该距离的栅格其计算结果取无值。若某个栅格单元格 A 到最近源之间的最短距离大于该值，则结果数据集中该栅格的值取无值。
    :param float cell_size: 结果数据集的分辨率，是生成距离栅格的可选参数
    :param float max_upslope_degrees: 最大上坡角度。单位为度，取值范围为大于或等于0。默认值为 90 度，即不考虑上坡角度。
                                      如果指定了最大上坡角度，则选择路线的时候会考虑地形的上坡的角度。从当前单元格行进到下一个高程更高的单元格
                                      为上坡，上坡角度即上坡方向与水平面的夹角。如果上坡角度大于给定值，则不会考虑此行进方向，即给出的路线不会
                                      经过上坡角度大于该值的区域。可想而知，可能会因为该值的设置而导致没有符合条件的路线。此外，由于坡度的表示
                                      范围为0到90度，因此，虽然可以指定为一个大于90度的值，但产生的效果与指定为90度相同，即不考虑上坡角度。
    :param float max_downslope_degree: 设置最大下坡角度。单位为度，取值范围为大于或等于0。
                                      如果指定了最大下坡角度，则选择路线的时候会考虑地形的下坡的角度。从当前单元格行进到下一个高程小于当前高
                                      程的单元格为下坡，下坡角度即下坡方向与水平面的夹角。如果下坡角度大于给定值，则不会考虑此行进方向，即给
                                      出的路线不会经过下坡角度大于该值的区域。可想而知，可能会因为该值的设置而导致没有符合条件的路线。此外，
                                      由于坡度的表示范围为0到90度，因此，虽然可以指定为一个大于90度的值，但产生的效果与指定为90度相同，即不
                                      考虑下坡角度。
    :param out_data: 结果数据集所在的数据源
    :type out_data:  Datasource or DatasourceConnectionInfo or str
    :param str out_distance_grid_name: 结果距离栅格数据集的名称。如果名称为空，将自动获取有效的数据集名称。
    :param str out_direction_grid_name: 方向栅格数据集的名称，如果为空，将不生成方向栅格数据集
    :param str out_allocation_grid_name:  分配栅格数据集的名称，如果为空，将不生成 分配栅格数据集
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 如果生成成功，返回结果数据集或数据集名称的元组，其中第一个为距离栅格数据集，第二个为方向栅格数据集，第三个为分配栅格数据集，如果没有设置方向栅格数据集名称和
             分配栅格数据集名称，对应的值为 None
    :rtype: tuple[DataetGrid] or tuple[str]
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    if not isinstance(_source_input, (DatasetVector, DatasetGrid)):
        raise ValueError("source input_data must be DatasetVector or DatasetGrid")
    _source_surface = get_input_dataset(surface_grid_dataset)
    if _source_surface is None:
        raise ValueError("surface grid dataset is None")
    else:
        if not isinstance(_source_surface, DatasetGrid):
            raise ValueError("surface grid dataset must be DatasetGrid")
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_distance_grid_name is None:
            _outDistanceGridName = _source_input.name + "_distance"
        else:
            _outDistanceGridName = out_distance_grid_name
    _outDistanceGridName = _ds.get_available_dataset_name(_outDistanceGridName)
    _jvm = get_jvm()
    try:
        try:
            parameter = _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalystParameter()
            parameter.setSourceDataset(_source_input._jobject)
            parameter.setTargetDatasource(_ds._jobject)
            parameter.setDistanceGridName(_outDistanceGridName)
            if max_distance is not None:
                parameter.setMaxDistance(float(max_distance))
            if cell_size is not None:
                parameter.setCellSize(float(cell_size))
            if out_direction_grid_name is not None:
                parameter.setDirectionGridName(out_direction_grid_name)
            if out_allocation_grid_name is not None:
                parameter.setAllocationGridName(out_allocation_grid_name)
            if max_upslope_degrees is not None:
                parameter.setMaxUpslopeDegree(float(max_upslope_degrees))
            if max_downslope_degree is not None:
                parameter.setMaxDownslopeDegree(float(max_downslope_degree))
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "StraightDistance")
                        _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            distance_analyst_result = _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalyst.straightDistance(parameter)
        except Exception as e:
            try:
                log_error(e)
                distance_analyst_result = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif distance_analyst_result is not None:
            results = []
            dt = distance_analyst_result.getDistanceDatasetGrid()
            if dt is not None:
                results.append(_ds[dt.getName()])
            else:
                results.append(None)
            dt = distance_analyst_result.getDirectionDatasetGrid()
            if dt is not None:
                results.append(_ds[dt.getName()])
            else:
                results.append(None)
            dt = distance_analyst_result.getAllocationDatasetGrid()
            if dt is not None:
                results.append(_ds[dt.getName()])
            else:
                results.append(None)
            if out_data is not None:
                return try_close_output_datasource(results, out_datasource)
            return results
        else:
            if out_data is not None:
                try_close_output_datasource(None, out_datasource)
            return


def surface_path_line(source_point, target_point, surface_grid_dataset, max_upslope_degrees=90.0, max_downslope_degree=90.0, smooth_method=None, smooth_degree=0, progress=None):
    """
    根据给定的参数，计算源点和目标点之间的最短表面距离路径（一个二维矢量线对象）。该方法用于根据给定的源点、目标点和表面栅格，计算源点与目标点之间的最短表面距离路径。

    设置最大上坡角度（max_upslope_degrees）和最大下坡角度（max_downslope_degree）可以使分析得出的路线不经过过于陡峭的地形。
    但注意，如果指定了上下坡角度限制，也可能得不到分析结果，这与最大上下坡角度的值和表面栅格所表达的地形有关。下图展示了将最
    大上坡角度和最大下坡角度分别均设置为 5 度、10 度和 90 度（即不限制上下坡角度）时的表面距离最短路径，由于对上下坡角度做出
    了限制，因此表面距离最短路径是以不超过最大上下坡角度为前提而得出的。

    .. image:: ../image/SurfacePathLine.png

    :param Point2D source_point: 指定的源点。
    :param Point2D target_point:  指定的目标点。
    :param surface_grid_dataset: 表面栅格
    :type surface_grid_dataset: DatasetGrid or str
    :param float max_upslope_degrees: 最大上坡角度。单位为度，取值范围为大于或等于0。默认值为 90 度，即不考虑上坡角度。
                                      如果指定了最大上坡角度，则选择路线的时候会考虑地形的上坡的角度。从当前单元格行进到下一个高程更高的单元格
                                      为上坡，上坡角度即上坡方向与水平面的夹角。如果上坡角度大于给定值，则不会考虑此行进方向，即给出的路线不会
                                      经过上坡角度大于该值的区域。可想而知，可能会因为该值的设置而导致没有符合条件的路线。此外，由于坡度的表示
                                      范围为0到90度，因此，虽然可以指定为一个大于90度的值，但产生的效果与指定为90度相同，即不考虑上坡角度。
    :param float max_downslope_degree: 设置最大下坡角度。单位为度，取值范围为大于或等于0。
                                      如果指定了最大下坡角度，则选择路线的时候会考虑地形的下坡的角度。从当前单元格行进到下一个高程小于当前高
                                      程的单元格为下坡，下坡角度即下坡方向与水平面的夹角。如果下坡角度大于给定值，则不会考虑此行进方向，即给
                                      出的路线不会经过下坡角度大于该值的区域。可想而知，可能会因为该值的设置而导致没有符合条件的路线。此外，
                                      由于坡度的表示范围为0到90度，因此，虽然可以指定为一个大于90度的值，但产生的效果与指定为90度相同，即不
                                      考虑下坡角度。
    :param smooth_method: 计算两点（源和目标）间最短路径时对结果路线进行光滑的方法
    :type smooth_method: SmoothMethod or str
    :param int smooth_degree: 计算两点（源和目标）间最短路径时对结果路线进行光滑的光滑度。
                                光滑度的值越大，光滑度的值越大，则结果矢量线的光滑度越高。当 smooth_method 不为 NONE 时有效。光滑度的有效取值与光滑方法有关，光滑方法有 B 样条法和磨角法:
                                - 光滑方法为 B 样条法时，光滑度的有效取值为大于等于2的整数，建议取值范围为[2,10]。
                                - 光滑方法为磨角法时，光滑度代表一次光滑过程中磨角的次数，设置为大于等于1的整数时有效
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 返回表示最短路径的线对象和最短路径的花费
    :rtype: tuple[GeoLine,float]
    """
    _source_grid = get_input_dataset(surface_grid_dataset)
    if _source_grid is None:
        raise ValueError("source Grid dataset is None")
    if not isinstance(_source_grid, DatasetGrid):
        raise ValueError("source Grid dataset must be DatasetGrid")
    _jvm = get_jvm()
    try:
        try:
            parameter = _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalystParameter()
            parameter.setSurfaceGrid(_source_grid._jobject)
            if smooth_method is not None:
                parameter.setPathLineSmoothMethod(SmoothMethod._make(smooth_method)._jobject)
            if smooth_degree is not None:
                parameter.setPathLineSmoothDegree(int(smooth_degree))
            if max_upslope_degrees is not None:
                parameter.setMaxUpslopeDegree(float(max_upslope_degrees))
            if max_downslope_degree is not None:
                parameter.setMaxDownslopeDegree(float(max_downslope_degree))
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "CostPathLine")
                        _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_result = _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalyst.surfacePathLine(source_point._jobject, target_point._jobject, parameter)
        except Exception as e:
            try:
                log_error(e)
                java_result = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.DistanceAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if java_result is not None:
            return (
             Geometry._from_java_object(java_result.getPathLine()), java_result.getCost())
        return


def calculate_hill_shade(input_data, shadow_mode, azimuth, altitude_angle, z_factor, out_data=None, out_dataset_name=None, progress=None):
    """
    三维晕渲图是指通过模拟实际地表的本影与落影的方式反映地形起伏状况的栅格图。通过采用假想的光源照射地表，结合栅格数据得到的坡度坡向信息， 得到各像元
    的灰度值，面向光源的斜坡的灰度值较高，背向光源的灰度值较低，即为阴影区，从而形象表现出实际地表的地貌和地势。 由栅格数据计算得出的这种山体阴影图
    往往具有非常逼真的立体效果，因而称其为三维晕渲图。

    .. image:: ../image/CalculateHillShade.png

    三维晕渲图在描述地表三维状况和地形分析中都具有比较重要的价值，当将其他专题信息叠加在三维晕渲图之上时，将会更加提高三维晕渲图的应用价值和直观效果。

    在生成三维晕渲图时，需要指定假想光源的位置，该位置由光源的方位角和高度角确定。方位角确定光源的方向，高度角是光源照射时倾斜角度。例如，当光源的方位角
    为 315 度，高度角为 45 度时，其与地表的相对位置如下图所示。

    .. image:: ../image/CalculateHillShade_1.png

    三维晕渲图有三种类型：渲染阴影效果、渲染效果和阴影效果，通过 :py:class:`ShadowMode` 类来指定。

    :param input_data: 指定的待生成三维晕渲图的栅格数据集
    :type input_data: DatasetGrid or str
    :param shadow_mode: 三维晕渲图的渲染类型
    :type shadow_mode: ShadowMode or str
    :param float azimuth: 指定的光源方位角。用于确定光源的方向，是从光源所在位置的正北方向线起，依顺时针方向到光源与目标方向线
                          的夹角，范围为 0-360 度，以正北方向为 0 度，依顺时针方向递增。

                          .. image:: ../image/Azimuth.png

    :param float altitude_angle: 指定的光源高度角。用于确定光源照射的倾斜角度，是光源与目标的方向线与水平面间的夹角，范围为
                                 0-90 度。当光源高度角为 90 度时，光源正射地表。

                                 .. image:: ../image/AltitudeAngle.png

    :param float z_factor:  指定的高程缩放系数。该值是指在栅格中，栅格值（Z 坐标，即高程值）相对于 X 和 Y 坐标的单位变换系数。通常有 X，Y，Z 都参加的计算中，需要将高程值乘以一个高程缩放系数，使得三者单位一致。例如，X、Y 方向上的单位是米，而 Z 方向的单位是英尺，由于 1 英尺等于 0.3048 米，则需要指定缩放系数为 0.3048。如果设置为 1.0，表示不缩放。
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetGrid or str
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    else:
        if not isinstance(_source_input, DatasetGrid):
            raise ValueError("source input_data must be DatasetGrid")
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + "_hill"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    try:
        try:
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "CalculateHillShade")
                        _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.calculateHillShade(_source_input._jobject, ShadowMode._make(shadow_mode)._jobject, float(azimuth), float(altitude_angle), float(z_factor), _ds._jobject, _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def calculate_slope(input_data, slope_type, z_factor, out_data=None, out_dataset_name=None, progress=None):
    """
    计算坡度，并返回坡度栅格数据集，即坡度图。 坡度是地表面上某一点的切面和水平面所成的夹角。坡度值越大，表示地势越陡峭

    注意：
        计算坡度时，要求待计算的栅格值（即高程）的单位与 x，y 坐标的单位相同。如果不一致，可通过高程缩放系数（方法中对应 zFactor 参数）来调整。
        但注意，当高程值单位与坐标单位间的换算无法通过固定值来调节时，则需要通过其他途径对数据进行处理。最常见的情况之一是 DEM 栅格采用地理坐标系时，
        单位为度，而高程值单位为米，此时建议对 DEM 栅格进行投影转换，将 x，y 坐标转换为平面坐标。

    :param input_data: 指定的的待计算坡度的栅格数据集
    :type input_data: DatasetGrid or str
    :param slope_type: 坡度的单位类型
    :type slope_type: SlopeType or str
    :param float z_factor: 指定的高程缩放系数。该值是指在栅格中，栅格值（Z 坐标，即高程值）相对于 X 和 Y 坐标的单位变换系数。通常有 X，Y，Z 都参加的计算中，需要将高程值乘以一个高程缩放系数，使得三者单位一致。例如，X、Y 方向上的单位是米，而 Z 方向的单位是 英尺，由于 1 英尺等于 0.3048 米，则需要指定缩放系数为 0.3048。如果设置为 1.0，表示不缩放。
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetGrid or str

    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    else:
        if not isinstance(_source_input, DatasetGrid):
            raise ValueError("source input_data must be DatasetGrid")
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + "_slope"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    try:
        try:
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "calculate_slope")
                        _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.calculateSlope(_source_input._jobject, SlopeType._make(slope_type)._jobject, float(z_factor), _ds._jobject, _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def calculate_aspect(input_data, out_data=None, out_dataset_name=None, progress=None):
    """
    计算坡向，并返回坡向栅格数据集，即坡向图。
    坡向是指坡面的朝向，它表示地形表面某处最陡的下坡方向。坡向反映了斜坡所面对的方向，任意斜坡的倾斜方向可取 0～360 度中的任意方向，所以坡向计算的
    结果范围为 0～360 度。从正北方向（0 度）开始顺时针计算

    :param input_data: 指定的待计算坡向的栅格数据集
    :type input_data: DatasetGrid or str
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetGrid or str
    """
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    else:
        if not isinstance(_source_input, DatasetGrid):
            raise ValueError("source input_data must be DatasetGrid")
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + "_aspect"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    try:
        try:
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "calculate_aspect")
                        _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.calculateAspect(_source_input._jobject, _ds._jobject, _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def compute_point_aspect(input_data, specified_point):
    """
    计算 DEM 栅格上指定点处的坡向。 DEM 栅格上指定点处的坡向，与坡向图（calculate_aspect 方法）的计算方法相同，是将该点所在单元格与其周围的相
    邻的八个单元格所形成的 3 × 3 平面作为计算单元，通过三阶反距离平方权差分法计算水平高程变化率和垂直高程变化率从而得出坡向。更多介绍，请参阅 :py:meth:`calculate_aspect` 方法。

    注意：
        当指定点所在的单元格为无值时，计算结果为 -1，这与生成坡向图不同；当指定的点位于 DEM 栅格的数据集范围之外时，计算结果为 -1。

    :param input_data: 指定的待计算坡向的栅格数据集
    :type input_data: DatasetGrid or str
    :param Point2D specified_point:  指定的地理坐标点。
    :return: 指定点处的坡向。单位为度。
    :rtype: float
    """
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    if not isinstance(_source_input, DatasetGrid):
        raise ValueError("source input_data must be DatasetGrid")
    _jvm = get_jvm()
    try:
        return _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.computePointAspect(_source_input._jobject, specified_point._jobject)
    except Exception as e:
        try:
            log_error(e)
        finally:
            e = None
            del e


def compute_point_slope(input_data, specified_point, slope_type, z_factor):
    """
    计算 DEM 栅格上指定点处的坡度。
    DEM 栅格上指定点处的坡度，与坡度图（calculate_slope 方法）的计算方法相同，是将该点所在单元格与其周围的相邻的八个单元格所形成的 3 × 3 平面作
    为计算单元，通过三阶反距离平方权差分法计算水平高程变化率和垂直高程变化率从而得出坡度。更多介绍，请参阅 calculate_slope 方法。

    注意：
        当指定点所在的单元格为无值时，计算结果为 -1，这与生成坡度图不同；当指定的点位于 DEM 栅格的数据集范围之外时，计算结果为 -1。

    :param input_data: 指定的待计算坡向的栅格数据集
    :type input_data: DatasetGrid or str
    :param Point2D specified_point: 指定的地理坐标点。
    :param slope_type: 指定的坡度单位类型。可以用角度、弧度或百分数来表示。以使用角度为例，坡度计算的结果范围为 0～90 度。
    :type slope_type: SlopeType or str
    :param float z_factor: 指定的高程缩放系数。该值是指在 DEM 栅格中，栅格值（Z 坐标，即高程值）相对于 X 和 Y 坐标的单位变换系数。通常有 X，Y，Z 都参加的计算中，需要将高程值乘以一个高程缩放系数，使得三者单位一致。例如，X、Y 方向上的单位是米，而 Z 方向的单位是英尺，由于 1 英尺等于 0.3048 米，则需要指定缩放系数为 0.3048。如果设置为 1.0，表示不缩放。
    :return: 指定点处的坡度。单位为 type 参数指定的类型。
    :rtype: float
    """
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    if not isinstance(_source_input, DatasetGrid):
        raise ValueError("source input_data must be DatasetGrid")
    _jvm = get_jvm()
    try:
        return _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.computePointSlope(_source_input._jobject, specified_point._jobject, SlopeType._make(slope_type)._jobject, float(z_factor))
    except Exception as e:
        try:
            import traceback
            log_error(traceback.format_exc())
        finally:
            e = None
            del e


def calculate_ortho_image(input_data, colors, no_value_color, out_data=None, out_dataset_name=None, progress=None):
    """
    根据给定的颜色集合生成正射三维影像。

    正射影像是采用数字微分纠正技术，通过周边邻近栅格的高程得到当前点的合理日照强度，进行正射影像纠正。

    :param input_data: 指定的待计算三维正射影像的 DEM 栅格。
    :type input_data: DatasetGrid or str
    :param colors: 三维投影后的颜色集合。输入如果为 dict，则表示高程值与颜色值的对应关系。
                可以不必在高程颜色对照表中列出待计算栅格的所有栅格值（高程值）及其对应颜色，未在高程颜色对照表中列出的高程值，其在结果影像中的颜色将通过插值得出。
    :type colors: Colors or dict[float,tuple]
    :param no_value_color: 无值栅格的颜色
    :type no_value_color: tuple or int
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetGrid or str
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    else:
        if not isinstance(_source_input, DatasetGrid):
            raise ValueError("source input_data must be DatasetGrid")
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + "_orthoImage"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    try:
        try:
            if isinstance(colors, dict):
                java_color = _jvm.com.supermap.data.ColorDictionary()
                for key, value in colors.items():
                    java_color.setColor(float(key), to_java_color(value))

            else:
                if isinstance(colors, Colors):
                    java_color = colors._jobject
                else:
                    raise ValueError("valid colors type, required dict or Colors, but now is " + str(type(colors)))
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "CalculateOrthoImage")
                        _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.calculateOrthoImage(oj(_source_input), java_color, to_java_color(no_value_color), oj(_ds), _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def compute_surface_area(input_data, region):
    """
    计算表面面积，即计算所选多边形区域内的 DEM 栅格拟合的三维曲面的总的表面面积。

    :param input_data: 指定的待计算表面面积的 DEM 栅格。
    :type input_data: DatasetGrid or str
    :param GeoRegion region: 指定的用于计算表面面积的多边形
    :return: 表面面积的值。单位为平方米。返回 -1 表示计算失败。
    :rtype: float
    """
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    if not isinstance(_source_input, DatasetGrid):
        raise ValueError("source input_data must be DatasetGrid")
    _jvm = get_jvm()
    try:
        return _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.computeSurfaceArea(oj(_source_input), oj(region))
    except Exception as e:
        try:
            log_error(e)
        finally:
            e = None
            del e

    return -1.0


def compute_surface_distance(input_data, line):
    """
    计算栅格表面距离，即计算在 DEM 栅格拟合的三维曲面上沿指定的线段或折线段的曲面距离。

    注意：
        - 表面量算所量算的距离是曲面上的，因而比平面上的值要大。
        - 当用于量算的线超出了 DEM 栅格的范围时，会先按数据集范围对线对象进行裁剪，按照位于数据集范围内的那部分线来计算表面距离。

    :param input_data:  指定的待计算表面距离的 DEM 栅格。
    :type input_data: DatasetGrid or str
    :param GeoLine line: 用于计算表面距离的二维线。
    :return: 表面距离的值。单位为米。
    :rtype: float
    """
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    if not isinstance(_source_input, DatasetGrid):
        raise ValueError("source input_data must be DatasetGrid")
    _jvm = get_jvm()
    try:
        return _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.computeSurfaceDistance(oj(_source_input), oj(line))
    except Exception as e:
        try:
            log_error(e)
        finally:
            e = None
            del e

    return -1.0


def compute_surface_volume(input_data, region, base_value):
    """
    计算表面体积，即计算所选多边形区域内的 DEM 栅格拟合的三维曲面与一个基准平面之间的空间上的体积。

    :param input_data: 待计算体积的 DEM 栅格。
    :type input_data: DatasetGrid or str
    :param GeoRegion region: 用于计算体积的多边形。
    :param float base_value: 基准平面的值。单位与待计算的 DEM 栅格的栅格值单位相同。
    :return: 指定的基准平面的值。单位与待计算的 DEM 栅格的栅格值单位相同。
    :rtype: float
    """
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    if not isinstance(_source_input, DatasetGrid):
        raise ValueError("source input_data must be DatasetGrid")
    _jvm = get_jvm()
    try:
        return _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.computeSurfaceVolume(oj(_source_input), oj(region), float(base_value))
    except Exception as e:
        try:
            log_error(e)
        finally:
            e = None
            del e


def calculate_profile(input_data, line):
    """
    剖面分析，根据给定线路查看 DEM 栅格沿该线路的剖面，返回剖面线和采样点坐标。
    给定一条直线或者折线，查看 DEM 栅格沿此线的纵截面，称为剖面分析。剖面分析的结果包含两部分：剖面线和采样点集合。

    * 采样点

    剖面分析需要沿给定线路选取一些点，通过这些点所在位置的高程和坐标信息，来展现剖面效果，这些点称为采样点。采样点的选取依照以下规则，
    可结合下图来了解。

        - 给定路线途经的每个单元格内只选取一个采样点；
        - 给定路线的节点都被作为采样点；
        - 如果路线经过且节点不在该单元格内，则将线路与该单元格两条中心线中交角较大的一条的交点作为采样点。

    .. image:: ../image/CalculateProfile_1.png

    * 剖面线和采样点坐标集合

    剖面线是剖面分析的结果之一，是一条二维线（ :py:class:`GeoLine` ），它的节点与采样点一一对应，节点的 X 值表示当前采样点到给定线
    路的起点（也是第一个采样点）的直线距离，Y 值为当前采样点所在位置的高程。而采样点集合给出了所有采样点的位置，使用一个二维集合线对
    象来存储这些点。剖面线与采样点集合的点是一一对应的，结合剖面线和采样点集合可以知道在某位置的高程以及距离分析的起点的距离。

    下图展示了以剖面线的 X 值为横轴，Y 值为纵轴绘制二维坐标系下的剖面线示意图，通过剖面线可以直观的了解沿着给定的线路，地形的高程和地势。

    .. image:: ../image/CalculateProfile_2.png

    注意：指定的线路必须在 DEM 栅格的数据集范围内，否则可能分析失败。如果采样点位于无值栅格上，则剖面线上对应的点的高程为0。

    :param input_data:  指定的待进行剖面分析的 DEM 栅格。
    :type input_data: DatasetGrid or str
    :param line: 指定的线路，为一条线段或折线。剖面分析给出沿该线路的剖面。
    :type line: GeoLine
    :return: 剖面分析结果，剖面线和采样点集合。
    :rtype: tuple[GeoLine, GeoLine]
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    if not isinstance(_source_input, DatasetGrid):
        raise ValueError("source input_data must be DatasetGrid")
    if not isinstance(line, GeoLine):
        raise ValueError("line must be GeoLine")
    _jvm = get_jvm()
    try:
        profile_result = _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.calculateProfile(oj(_source_input), oj(line))
        if profile_result:
            return (
             Geometry._from_java_object(profile_result.getProfile()),
             Geometry._from_java_object(profile_result.getXYCoordinate()))
    except Exception:
        import traceback
        log_error(traceback.format_exc())


class CutFillResult:
    __doc__ = "\n    填挖方结果信息类。该对象用于获取对栅格数据集进行填方和挖方计算的结果，例如需要填方、挖方的面积、填方和挖方的体积数等。\n\n    关于填挖方结果面积和体积单位的说明：\n\n    填挖的面积单位为平方米，体积的单位为平方米乘以高程（即进行填挖的栅格值）的单位。但需注意，如果进行填挖方计算的栅格是地理坐标系，面积的值是一个近似转换到平方米单位的值。\n    "

    def __init__(self, cut_area, cut_volume, fill_area, fill_volume, remainder_area, cut_fill_grid_result):
        """
        内部构造函数，用户不需要使用

        :param float cut_area: 填挖方分析结果挖掘面积。单位为平方米。当进行填挖方的栅格为地理坐标系时，该值为近似转换
        :param float cut_volume: 填挖方分析结果挖掘体积。单位为平方米乘以填挖栅格的栅格值（即高程值）的单位
        :param float fill_area: 填挖方分析结果填充面积。单位为平方米。当进行填挖方的栅格为地理坐标系时，该值为近似转换。
        :param float fill_volume: 填挖方分析结果填充体积。单位为平方米乘以填挖栅格的栅格值（即高程值）的单位。
        :param float remainder_area: 填挖方分析中未进行填挖方的面积。单位为平方米。当进行填挖方的栅格为地理坐标系时，该值为近似转换。
        :param cut_fill_grid_result: 填挖方分析的结果数据集。 单元格值大于0表示要挖的深度，小于0表要填的深度。
        :type cut_fill_grid_result: DatasetGrid or str
        """
        self.cut_area = cut_area
        self.cut_fill_grid_result = cut_fill_grid_result
        self.cut_volume = cut_volume
        self.fill_area = fill_area
        self.fill_volume = fill_volume
        self.remainder = remainder_area

    @staticmethod
    def _from_java_object(java_object, grid_result):
        return CutFillResult(java_object.getCutArea(), java_object.getCutVolume(), java_object.getFillArea(), java_object.getFillVolume(), java_object.getRemainderArea(), grid_result)


def inverse_cut_fill(input_data, volume, is_fill, region=None, progress=None):
    """
    反算填挖方，即根据给定的填方或挖方的体积计算填挖后的高程
    反算填挖方用于解决这样一类实际问题：已知填挖前的栅格数据和该数据范围内要填或挖的体积，来推求填方或挖方后的高程值。例如，某建筑施
    工地的一片区域需要填方，现得知某地可提供体积为 V 的土方，此时使用反算填挖方就可以计算出将这批土填到施工区域后，施工区域的高程是
    多少。然后可判断是否达到施工需求，是否需要继续填方。

    :param input_data: 指定的待填挖的栅格数据。
    :type input_data: DatasetGrid or str
    :param float volume: 指定的填或挖的体积。该值为一个大于0的值，如果设置为小于或等于0会抛出异常。单位为平方米乘以待填挖栅格的栅格值单位。
    :param bool is_fill: 指定是否进行填方计算。如果为 true 表示进行填方计算，false 表示进行挖方计算。
    :param region: 指定的填挖方区域。如果为 None 则填挖计算应用于整个栅格区域。
    :type region: GeoRegion or Rectangle
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 填挖后的高程值。单位与待填挖栅格的栅格值单位一致。
    :rtype: float
    """
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    if not isinstance(_source_input, DatasetGrid):
        raise ValueError("source input_data must be DatasetGrid")
    if isinstance(region, Rectangle):
        region = region.to_region()
    _jvm = get_jvm()
    listener = None
    try:
        try:
            if progress is not None and safe_start_callback_server():
                try:
                    listener = ProgressListener(progress, "inverse_cut_fill")
                    _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.addSteppedListener(listener)
                except Exception as e:
                    try:
                        close_callback_server()
                        log_error(e)
                        listener = None
                    finally:
                        e = None
                        del e

            elif isinstance(region, GeoRegion):
                result = _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.cutFill(oj(_source_input), float(volume), bool(is_fill), oj(region))
            else:
                result = _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.cutFill(oj(_source_input), float(volume), bool(is_fill))
        except Exception:
            import traceback
            log_error(traceback.format_exc())
            result = None

    finally:
        return

    if listener is not None:
        try:
            _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.removeSteppedListener(listener)
        except Exception as e1:
            try:
                log_error(e1)
            finally:
                e1 = None
                del e1

        close_callback_server()
    return result


def cut_fill_grid(before_cut_fill_grid, after_cut_full_grid, out_data=None, out_dataset_name=None, progress=None):
    """
    栅格填挖方计算，即对填挖方前、后两个栅格数据集对应像元的计算。
    地表经常由于沉积和侵蚀等作用引起表面物质的迁移，表现为地表某些区域的表面物质增加，某些区域的表面物质减少。在工程中，通常将表面物质的减少称为“挖方”，而将表面物质的增加称为“填方”。

    栅格填挖方计算要求输入两个栅格数据集：填挖方前的栅格数据集和填挖方后的栅格数据集，生成的结果数据集的每个像元值为其两个输入数据集对应像元值的变化值。如果像元值为正，表示该像元处的表面物质减少；如果像元值为负，表示该像元处的表面物质增加。填挖方的计算方法如下图所示：

    .. image:: ../image/CalculationTerrain_CutFill.png

    通过该图可以发现，结果数据集=填挖方前栅格数据集-填挖方后栅格数据集。

    对于输入的两个栅格数据集及结果数据集有几点内容需要注意：

    - 要求两个输入的栅格数据集有相同的坐标和投影系统，以保证同一个地点有相同的坐标，如果两个输入的栅格数据集的坐标系统不一致，则很有可能产生错误的结果。

    - 理论上，要求输入的两个栅格数据集的空间范围也是一致的。对于空间范围不一致的两个栅格数据集，只计算其重叠区域的表面填挖方的结果。

    - 在其中一个栅格数据集的像元为空值处，计算结果数据集该像元值也为空值。

    :param before_cut_fill_grid: 指定的填挖方前的栅格数据集
    :type before_cut_fill_grid: DatasetGrid or str
    :param after_cut_full_grid: 指定的填挖方后的栅格数据集。
    :type after_cut_full_grid: DatasetGrid or str
    :param out_data: 指定的存放结果数据集的数据源。
    :type out_data: Datasource or str
    :param out_dataset_name: 指定的结果数据集的名称。
    :type out_dataset_name: str
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 填挖方结果信息
    :rtype: CutFillResult
    """
    check_lic()
    _before_source_input = get_input_dataset(before_cut_fill_grid)
    if _before_source_input is None:
        raise ValueError("before cut fill grid is None")
    if not isinstance(_before_source_input, DatasetGrid):
        raise ValueError("before cut fill grid must be DatasetGrid")
    _after_source_input = get_input_dataset(after_cut_full_grid)
    if _after_source_input is None:
        raise ValueError("after cut fill grid is None")
    else:
        if not isinstance(_after_source_input, DatasetGrid):
            raise ValueError("after cut fill grid must be DatasetGrid")
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _before_source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _before_source_input.name + "_CutFill"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "cut_fill_grid")
                        _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            cut_fill_result = _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.cutFill(oj(_before_source_input), oj(_after_source_input), oj(_ds), _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                cut_fill_result = None
            finally:
                e = None
                del e

    finally:
        return

    if listener is not None:
        try:
            _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.removeSteppedListener(listener)
        except Exception as e1:
            try:
                log_error(e1)
            finally:
                e1 = None
                del e1

        close_callback_server()
    result_dt = None
    if cut_fill_result is not None:
        java_cut_fill_grid_result = cut_fill_result.getCutFillGridResult()
        if java_cut_fill_grid_result:
            result_dt = _ds[java_cut_fill_grid_result.getName()]
    if out_data is not None:
        result_dt = try_close_output_datasource(result_dt, out_datasource)
    return CutFillResult._from_java_object(cut_fill_result, result_dt)


def cut_fill_oblique(input_data, line3d, buffer_radius, is_round_head, out_data=None, out_dataset_name=None, progress=None):
    """
    斜面填挖方计算。
    斜面填挖方功能是统计在一个地形表面创建一个斜面所需要的填挖量。其原理与选面填挖方相似。

    :param input_data: 指定的待填挖方的栅格数据集。
    :type input_data: DatasetGrid or str
    :param line3d: 指定的填挖方路线
    :type line3d: GeoLine3D
    :param buffer_radius: 指定的填挖方线路的缓冲区半径。单位与待填挖的栅格数据集的坐标系单位相同。
    :type buffer_radius: float
    :param is_round_head: 指定是否使用圆头缓冲为填挖方路线创建缓冲区。
    :type is_round_head: bool
    :param out_data: 指定的存放结果数据集的数据源
    :type out_data: Datasource or str
    :param out_dataset_name: 指定的结果数据集的名称。
    :type out_dataset_name: str
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 填挖方结果信息
    :rtype: CutFillResult
    """
    source_input = get_input_dataset(input_data)
    if source_input is None:
        raise ValueError("source input_data grid is None")
    if not isinstance(source_input, DatasetGrid):
        raise ValueError("source input_data grid must be DatasetGrid")
    else:
        if not isinstance(line3d, GeoLine3D):
            raise ValueError("line3d must GeoLine3D")
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = source_input.name + "_CutFill"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "cut_fill_oblique")
                        _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            cut_fill_result = _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.cutFill(oj(source_input), oj(line3d), float(buffer_radius), bool(is_round_head), oj(_ds), _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                cut_fill_result = None
            finally:
                e = None
                del e

    finally:
        return

    if listener is not None:
        try:
            _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.removeSteppedListener(listener)
        except Exception as e1:
            try:
                log_error(e1)
            finally:
                e1 = None
                del e1

        close_callback_server()
    result_dt = None
    if cut_fill_result is not None:
        java_cut_fill_grid_result = cut_fill_result.getCutFillGridResult()
        if java_cut_fill_grid_result:
            result_dt = _ds[java_cut_fill_grid_result.getName()]
    if out_data is not None:
        result_dt = try_close_output_datasource(result_dt, out_datasource)
    return CutFillResult._from_java_object(cut_fill_result, result_dt)


def cut_fill_region(input_data, region, base_altitude, out_data=None, out_dataset_name=None, progress=None):
    """
    选面填挖方计算。
    当需要将一个高低起伏的区域夷为平地时，用户可以通过指定高低起伏的区域以及夷为平地的高程，利用该方法进行选面填挖方计算，计算出填方
    面积，挖方面积、 填方量以及挖方量。

    :param input_data:  指定的待填挖的栅格数据集。
    :type input_data: DatasetGrid or str
    :param region: 指定的填挖方区域。
    :type region: GeoRegion or Rectangle
    :param base_altitude:  指定的填挖方区域的结果高程。单位与待填挖的栅格数据集的栅格值单位相同。
    :type base_altitude: float
    :param out_data: 指定的存放结果数据集的数据源。
    :type out_data: Datasource or str
    :param out_dataset_name: 指定的结果数据集的名称。
    :type out_dataset_name: str
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 填挖方结果信息
    :rtype: CutFillResult
    """
    check_lic()
    source_input = get_input_dataset(input_data)
    if source_input is None:
        raise ValueError("source input_data grid is None")
    else:
        if not isinstance(source_input, DatasetGrid):
            raise ValueError("source input_data grid must be DatasetGrid")
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = source_input.name + "_CutFill"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    if isinstance(region, Rectangle):
        region = region.to_region()
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "cut_fill_region")
                        _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            cut_fill_result = _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.cutFill(oj(source_input), oj(region), float(base_altitude), oj(_ds), _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                cut_fill_result = None
            finally:
                e = None
                del e

    finally:
        return

    if listener is not None:
        try:
            _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.removeSteppedListener(listener)
        except Exception as e1:
            try:
                log_error(e1)
            finally:
                e1 = None
                del e1

        close_callback_server()
    result_dt = None
    if cut_fill_result is not None:
        java_cut_fill_grid_result = cut_fill_result.getCutFillGridResult()
        if java_cut_fill_grid_result:
            result_dt = _ds[java_cut_fill_grid_result.getName()]
    if out_data is not None:
        result_dt = try_close_output_datasource(result_dt, out_datasource)
    return CutFillResult._from_java_object(cut_fill_result, result_dt)


def cut_fill_region3d(input_data, region, out_data=None, out_dataset_name=None, progress=None):
    """
    三维面填挖方计算。
    一个高低起伏的区域，可以根据这个区域填挖方后的三维面，利用三维面填挖方计算出需要填方的面积，挖方的面积、填方量以及挖方量。

    :param input_data:  指定的待填挖的栅格数据集。
    :type input_data: DatasetGrid or str
    :param region: 指定的填挖方区域。
    :type region: GeoRegion3D
    :param out_data: 指定的存放结果数据集的数据源。
    :type out_data: Datasource or str
    :param out_dataset_name: 指定的结果数据集的名称。
    :type out_dataset_name: str
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 填挖方结果信息
    :rtype: CutFillResult
    """
    source_input = get_input_dataset(input_data)
    if source_input is None:
        raise ValueError("source input_data grid is None")
    else:
        if not isinstance(source_input, DatasetGrid):
            raise ValueError("source input_data grid must be DatasetGrid")
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = source_input.name + "_CutFill"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "cut_fill_region3d")
                        _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            cut_fill_result = _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.cutFill(oj(source_input), oj(region), oj(_ds), _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                cut_fill_result = None
            finally:
                e = None
                del e

    finally:
        return

    if listener is not None:
        try:
            _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.removeSteppedListener(listener)
        except Exception as e1:
            try:
                log_error(e1)
            finally:
                e1 = None
                del e1

        close_callback_server()
    result_dt = None
    if cut_fill_result is not None:
        java_cut_fill_grid_result = cut_fill_result.getCutFillGridResult()
        if java_cut_fill_grid_result:
            result_dt = _ds[java_cut_fill_grid_result.getName()]
    if out_data is not None:
        result_dt = try_close_output_datasource(result_dt, out_datasource)
    return CutFillResult._from_java_object(cut_fill_result, result_dt)


def flood(input_data, height, region=None, progress=None):
    """
    根据指定的高程计算 DEM 栅格的淹没区域。
    淹没区域的计算基于 DEM 栅格数据，根据给定的一个淹没后的水位高程（由参数 height 指定），与 DEM 栅格的值（即高程值）进行比较，凡是高程值低于或等于给定水位的单元格均被划入淹没区域，然后将淹没区域转为矢量面输出，源 DEM 数据并不会被改变。通过淹没区域面对象，很容易统计出被淹没的范围、面积等。
    下图是计算水位达到 200 时的淹没区域的一个实例，由原始 DEM 数据和淹没区域的矢量面数据集（紫色区域）叠加而成

    .. image:: ../image/Flood.png

    注意：该方法返回的面对象是将所有淹没区域进行合并后的结果。

    :param input_data: 指定的需要计算淹没区域的 DEM 数据。
    :type input_data: DatasetGrid or str
    :param height: 指定的淹没后水位的高程值，DEM 数据中小于或等于该值的单元格会划入淹没区域。单位与待分析的 DEM 栅格的栅格值单位相同。
    :type height: float
    :param region: 指定的有效计算区域。指定该区域后，只在该区域内计算淹没区域。
    :type region: GeoRegion or Rectangle
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 将所有淹没区域合并后的面对象
    :rtype: GeoRegion
    """
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    if not isinstance(_source_input, DatasetGrid):
        raise ValueError("source input_data must be DatasetGrid")
    if isinstance(region, Rectangle):
        region = region.to_region()
    _jvm = get_jvm()
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "flood")
                        _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_result = _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.flood(oj(_source_input), float(height), oj(region))
        except Exception as e:
            try:
                log_error(e)
                java_result = None
            finally:
                e = None
                del e

    finally:
        return

    if listener is not None:
        try:
            _jvm.com.supermap.analyst.spatialanalyst.CalculationTerrain.removeSteppedListener(listener)
        except Exception as e1:
            try:
                log_error(e1)
            finally:
                e1 = None
                del e1

        close_callback_server()
    if java_result:
        return Geometry._from_java_object(java_result)


def divide_math_analyst(first_operand, second_operand, user_region=None, out_data=None, out_dataset_name=None, progress=None):
    """
    栅格除法运算。将输入的两个栅格数据集的栅格值逐个像元地相除。栅格代数运算的具体使用，参考 :py:meth:`expression_math_analyst`

    如果输入两个像素类型（PixelFormat）均为整数类型的栅格数据集，则输出整数类型的结果数据集；否则，输出浮点型的结果数据集。如果输入的两个栅格数据集
    的像素类型精度不同，则运算的结果数据集的像素类型与二者中精度较高者保持一致。

    :param first_operand: 指定的第一栅格数据集。
    :type first_operand: DatasetGrid or str
    :param second_operand:  指定的第二栅格数据集。
    :type second_operand: DatasetGrid or str
    :param GeoRegion user_region: 用户指定的有效计算区域。如果为 None，则表示计算全部区域，如果参与运算的数据集范围不一致，将使用所有数据集的范围的交集作为计算区域。
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetGrid or str
    """
    _first_input = get_input_dataset(first_operand)
    if _first_input is None:
        raise ValueError("first operand data is None")
    if not isinstance(_first_input, DatasetGrid):
        raise ValueError("first operand data must be DatasetGrid")
    _second_input = get_input_dataset(second_operand)
    if _second_input is None:
        raise ValueError("second operand data is None")
    else:
        if not isinstance(_second_input, DatasetGrid):
            raise ValueError("second operand data must be DatasetGrid")
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _first_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _first_input.name + "_divide"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    try:
        try:
            listener = None
            if progress is not None and safe_start_callback_server():
                try:
                    listener = ProgressListener(progress, "divide_math_analyst")
                    _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.addSteppedListener(listener)
                except Exception as e:
                    try:
                        close_callback_server()
                        log_error(e)
                        listener = None
                    finally:
                        e = None
                        del e

            elif user_region is not None:
                javaRegion = user_region._jobject
            else:
                javaRegion = None
            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.divide(_first_input._jobject, _second_input._jobject, javaRegion, _ds._jobject, _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def plus_math_analyst(first_operand, second_operand, user_region=None, out_data=None, out_dataset_name=None, progress=None):
    """
    栅格加法运算。将输入的两个栅格数据集的栅格值逐个像元地相加。 栅格代数运算的具体使用，参考 :py:meth:`expression_math_analyst`

    如果输入两个像素类型（PixelFormat）均为整数类型的栅格数据集，则输出整数类型的结果数据集；否则，输出浮点型的结果数据集。如果输入的两个栅格数据集
    的像素类型精度不同，则运算的结果数据集的像素类型与二者中精度较高者保持一致。

    :param first_operand: 指定的第一栅格数据集。
    :type first_operand: DatasetGrid or str
    :param second_operand:  指定的第二栅格数据集。
    :type second_operand: DatasetGrid or str
    :param GeoRegion user_region: 用户指定的有效计算区域。如果为 None，则表示计算全部区域，如果参与运算的数据集范围不一致，将使用所有数据集的范围的交集作为计算区域。
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetGrid or str
    """
    check_lic()
    _first_input = get_input_dataset(first_operand)
    if _first_input is None:
        raise ValueError("first operand data is None")
    if not isinstance(_first_input, DatasetGrid):
        raise ValueError("first operand data must be DatasetGrid")
    _second_input = get_input_dataset(second_operand)
    if _second_input is None:
        raise ValueError("second operand data is None")
    else:
        if not isinstance(_second_input, DatasetGrid):
            raise ValueError("second operand data must be DatasetGrid")
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _first_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _first_input.name + "_plus"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    try:
        try:
            listener = None
            if progress is not None and safe_start_callback_server():
                try:
                    listener = ProgressListener(progress, "plus_math_analyst")
                    _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.addSteppedListener(listener)
                except Exception as e:
                    try:
                        close_callback_server()
                        log_error(e)
                        listener = None
                    finally:
                        e = None
                        del e

            elif user_region is not None:
                javaRegion = user_region._jobject
            else:
                javaRegion = None
            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.plus(_first_input._jobject, _second_input._jobject, javaRegion, _ds._jobject, _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def minus_math_analyst(first_operand, second_operand, user_region=None, out_data=None, out_dataset_name=None, progress=None):
    """
    栅格减法运算。逐个像元地从第一个栅格数据集的栅格值中减去第二个数据集的栅格值。进行此运算时，输入栅格数据集的顺序很重要，顺序不同，结果通常也是不相同的。栅格代数运算的具体使用，参考 :py:meth:`expression_math_analyst`

    如果输入两个像素类型（PixelFormat）均为整数类型的栅格数据集，则输出整数类型的结果数据集；否则，输出浮点型的结果数据集。如果输入的两个栅格数据集
    的像素类型精度不同，则运算的结果数据集的像素类型与二者中精度较高者保持一致。

    :param first_operand: 指定的第一栅格数据集。
    :type first_operand: DatasetGrid or str
    :param second_operand:  指定的第二栅格数据集。
    :type second_operand: DatasetGrid or str
    :param GeoRegion user_region: 用户指定的有效计算区域。如果为 None，则表示计算全部区域，如果参与运算的数据集范围不一致，将使用所有数据集的范围的交集作为计算区域。
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetGrid or str

    """
    _first_input = get_input_dataset(first_operand)
    if _first_input is None:
        raise ValueError("first operand data is None")
    if not isinstance(_first_input, DatasetGrid):
        raise ValueError("first operand data must be DatasetGrid")
    _second_input = get_input_dataset(second_operand)
    if _second_input is None:
        raise ValueError("second operand data is None")
    else:
        if not isinstance(_second_input, DatasetGrid):
            raise ValueError("second operand data must be DatasetGrid")
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _first_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _first_input.name + "_minus"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    try:
        try:
            listener = None
            if progress is not None and safe_start_callback_server():
                try:
                    listener = ProgressListener(progress, "minus_math_analyst")
                    _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.addSteppedListener(listener)
                except Exception as e:
                    try:
                        close_callback_server()
                        log_error(e)
                        listener = None
                    finally:
                        e = None
                        del e

            elif user_region is not None:
                javaRegion = user_region._jobject
            else:
                javaRegion = None
            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.minus(_first_input._jobject, _second_input._jobject, javaRegion, _ds._jobject, _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def multiply_math_analyst(first_operand, second_operand, user_region=None, out_data=None, out_dataset_name=None, progress=None):
    """
    栅格乘法运算。将输入的两个栅格数据集的栅格值逐个像元地相乘。栅格代数运算的具体使用，参考 :py:meth:`expression_math_analyst`

    如果输入两个像素类型（PixelFormat）均为整数类型的栅格数据集，则输出整数类型的结果数据集；否则，输出浮点型的结果数据集。如果输入的两个栅格数据集
    的像素类型精度不同，则运算的结果数据集的像素类型与二者中精度较高者保持一致。

    :param first_operand: 指定的第一栅格数据集。
    :type first_operand: DatasetGrid or str
    :param second_operand:  指定的第二栅格数据集。
    :type second_operand: DatasetGrid or str
    :param GeoRegion user_region: 用户指定的有效计算区域。如果为 None，则表示计算全部区域，如果参与运算的数据集范围不一致，将使用所有数据集的范围的交集作为计算区域。
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetGrid or str

    """
    _first_input = get_input_dataset(first_operand)
    if _first_input is None:
        raise ValueError("first operand data is None")
    if not isinstance(_first_input, DatasetGrid):
        raise ValueError("first operand data must be DatasetGrid")
    _second_input = get_input_dataset(second_operand)
    if _second_input is None:
        raise ValueError("second operand data is None")
    else:
        if not isinstance(_second_input, DatasetGrid):
            raise ValueError("second operand data must be DatasetGrid")
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _first_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _first_input.name + "_multiply"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    try:
        try:
            listener = None
            if progress is not None and safe_start_callback_server():
                try:
                    listener = ProgressListener(progress, "multiply_math_analyst")
                    _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.addSteppedListener(listener)
                except Exception as e:
                    try:
                        close_callback_server()
                        log_error(e)
                        listener = None
                    finally:
                        e = None
                        del e

            elif user_region is not None:
                javaRegion = user_region._jobject
            else:
                javaRegion = None
            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.multiply(_first_input._jobject, _second_input._jobject, javaRegion, _ds._jobject, _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def to_float_math_analyst(input_data, user_region=None, out_data=None, out_dataset_name=None, progress=None):
    """
      栅格浮点运算。将输入的栅格数据集的栅格值转换成浮点型。 如果输入的栅格值为双精度浮点型，进行浮点运算后的结果栅格值也转换为单精度浮点型。

      :param input_data: 指定的第一栅格数据集。
      :type input_data: DatasetGrid or str
      :param GeoRegion user_region: 用户指定的有效计算区域。如果为 None，则表示计算全部区域，如果参与运算的数据集范围不一致，将使用所有数据集的范围的交集作为计算区域。
      :param out_data: 结果数据集所在的数据源
      :type out_data: Datasource or DatasourceConnectionInfo or str
      :param str out_dataset_name: 结果数据集名称
      :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
      :return: 结果数据集或数据集名称
      :rtype: DatasetGrid or str

    """
    _first_input = get_input_dataset(input_data)
    if _first_input is None:
        raise ValueError("source input_data is None")
    else:
        if not isinstance(_first_input, DatasetGrid):
            raise ValueError("source input_data must be DatasetGrid")
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _first_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _first_input.name + "_float"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    try:
        try:
            listener = None
            if progress is not None and safe_start_callback_server():
                try:
                    listener = ProgressListener(progress, "to_float_math_analyst")
                    _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.addSteppedListener(listener)
                except Exception as e:
                    try:
                        close_callback_server()
                        log_error(e)
                        listener = None
                    finally:
                        e = None
                        del e

            elif user_region is not None:
                javaRegion = user_region._jobject
            else:
                javaRegion = None
            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.toFloat(_first_input._jobject, javaRegion, _ds._jobject, _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def to_int_math_analyst(input_data, user_region=None, out_data=None, out_dataset_name=None, progress=None):
    """
      栅格取整运算。提供对输入的栅格数据集的栅格值进行取整运算。取整运算的结果是去除栅格值的小数部分，只保留栅格值的整数。如果输入栅格值为整数类型，进行取整运算后的结果与输入栅格值相同。

      :param input_data: 指定的第一栅格数据集。
      :type input_data: DatasetGrid or str
      :param GeoRegion user_region: 用户指定的有效计算区域。如果为 None，则表示计算全部区域，如果参与运算的数据集范围不一致，将使用所有数据集的范围的交集作为计算区域。
      :param out_data: 结果数据集所在的数据源
      :type out_data: Datasource or DatasourceConnectionInfo or str
      :param str out_dataset_name: 结果数据集名称
      :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
      :return: 结果数据集或数据集名称
      :rtype: DatasetGrid or str

    """
    _first_input = get_input_dataset(input_data)
    if _first_input is None:
        raise ValueError("source input_data is None")
    else:
        if not isinstance(_first_input, DatasetGrid):
            raise ValueError("source input_data must be DatasetGrid")
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _first_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _first_input.name + "_int"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    try:
        try:
            listener = None
            if progress is not None and safe_start_callback_server():
                try:
                    listener = ProgressListener(progress, "to_int_math_analyst")
                    _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.addSteppedListener(listener)
                except Exception as e:
                    try:
                        close_callback_server()
                        log_error(e)
                        listener = None
                    finally:
                        e = None
                        del e

            elif user_region is not None:
                javaRegion = user_region._jobject
            else:
                javaRegion = None
            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.toInt(_first_input._jobject, javaRegion, _ds._jobject, _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def expression_math_analyst(expression, pixel_format, out_data, is_ingore_no_value=True, user_region=None, out_dataset_name=None, progress=None):
    """
    栅格代数运算类。用于提供对一个或多个栅格数据集的数学运算及函数运算。

    栅格代数运算的思想是运用代数学的观点对地理特征和现象进行空间分析。实质上，是对多个栅格数据集（DatasetGrid）进行数学运算以及函数运算。运算结果
    栅格的像元值是由输入的一个或多个栅格同一位置的像元的值通过代数规则运算得到的。

    栅格分析中很多功能都是基于栅格代数运算的，作为栅格分析的核心内容，栅格代数运算用途十分广泛，能够帮助我们解决各种类型的实际问题。如建筑工程中的计
    算填挖方量，将工程实施前的DEM栅格与实施后的DEM栅格相减，就能够从结果栅格中得到施工前后的高程差，将结果栅格的像元值与像元所代表的实际面积相乘，
    就可以得知工程的填方量与挖方量；又如，想要提取2000年全国范围内平均降雨量介于20毫米和50毫米的地区，可以通过“20<年平均降雨量<50”关系运算表达式，
    对年平均降雨量栅格数据进行运算而获得。

    通过该类的方法进行栅格代数运算主要有以下两种途径:

        - 使用该类提供的基础运算方法。该类提供了六个用于进行基础运算的方法，包括 plus（加法运算）、minus（减法运算）、multiply（乘法运算）、
          divide（除法运算）、to_int（取整运算）和 to_float（浮点运算）。使用这几个方法可以完成一个或多个栅格数据对应栅格值的算术运算。对于相
          对简单的运算，可以通过多次调用这几个方法来实现，如 (A/B)-(A/C)。
        - 执行运算表达式。使用表达式不仅可以对一个或多个栅格数据集实现运算符运算，还能够进行函数运算。运算符包括算术运算符、关系运算符和布尔运算符，
          算术运算主要包括加法（+）、减法（-）、乘法（*）、除法（/）；布尔运算主要包括和（And）、或（Or）、异或（Xor）、非（Not）；关系运算主要包括
          =、<、>、<>、>=、<=。注意，对于布尔运算和关系运算均有三种可能的输出结果：真＝1、假=0及无值（只要有一个输入值为无值，结果即为无值）。

    此外，还支持 21 种常用的函数运算，如下图所示:

    .. image:: ../image/MathAnalyst_Function.png

    执行栅格代数运算表达式，支持自定义表达式栅格运算，通过自定义表达式可以进行算术运算、条件运算、逻辑运算、函数运算（常用函数、三角函数）以及复合运算。
    栅格代数运算表达式的组成需要遵循以下规则:

        - 运算表达式应为一个形如下式的字符串:

            [DatasourceAlias1.Raster1] + [DatasourceAlias2.Raster2]
            使用“ [数据源别名.数据集名] ”来指定参加运算的栅格数据集；注意要使用方括号把名字括起来。

        - 栅格代数运算支持四则运算符（"+" 、"-" 、"*" 、"/" ）、条件运算符（">" 、">=" 、"<" 、"<=" 、"<>" 、"==" ）、逻辑运算符（"|" 、"&" 、"Not()" 、"^" ）和一些常用数学函数（"abs()" 、"acos()" 、"asin()" 、"atan()" 、"acot()" 、"cos()" 、"cosh()" 、"cot()" 、"exp()" 、"floor()" 、"mod(,)" 、"ln()" 、"log()" 、"pow(,)" 、"sin()" 、"sinh()" 、"sqrt()" 、"tan()" 、"tanh()" 、"Isnull()" 、"Con(,,)" 、"Pick(,,,..)" ）。
        - 代数运算的表达式中各个函数之间可以嵌套使用，直接用条件运算符计算的栅格结果都为二值（如大于、小于等），即满足条件的用1代替，不满足的用0代替，若想使用其他值来表示满足条件和不满足条件的取值，可以使用条件提取函数Con(,,)。例如："Con(IsNull([SURFACE_ANALYST.Dem3] ) ,100,Con([SURFACE_ANALYST.Dem3] > 100,[SURFACE_ANALYST.Dem3] ,-9999) ) " ，该表达式的含义是：栅格数据集 Dem3 在别名为 SURFACE_ANALYST 的数据源中，将其中无值栅格变为 100，剩余栅格中，大于100 的，值保持不变，小于等于 100 的，值改成 -9999。
        - 如果栅格计算中有小于零的负值，注意要加小括号，如：[DatasourceAlias1.Raster1] - ([DatasourceAlias2.Raster2])。
        - 表达式中，运算符连接的操作数可以是一个栅格数据集，也可以是数字或者数学函数。
        - 数学函数的自变量可以为一个数值，也可以为某个数据集，或者是一个数据集或多个数据集的运算表达式。
        - 表达式必须是没有回车的单行表达式。
        - 表达式中必须至少含有一个输入栅格数据集。

    注意:

        - 参与运算的两个数据集，如果其像素类型（PixelFormat）不同，则运算的结果数据集的像素类型与二者中精度较高者保持一致。例如，一个为32位整型，一个为单精度浮点型，那么进行加法运算后，结果数据集的像素类型将为单精度浮点型。
        - 对于栅格数据集中的无值数据，如果忽略无值，则无论何种运算，结果仍为无值；如果不忽略无值，意味着无值将参与运算。例如，两栅格数据集 A 和 B 相加，A 某单元格为无值，值为-9999，B 对应单元格值为3000，如果不忽略无值，则运算结果该单元格值为-6999。

    :param str expression:  自定义的栅格运算表达式。
    :param pixel_format: 指定的结果数据集的像素格式。注意，如果指定的像素类型的精度低于参与运算的栅格数据集像素类型的精度，运算结果可能不正确。
    :type pixel_format: PixelFormat or str
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param bool is_ingore_no_value:  是否忽略无值栅格数据。true 表示忽略无值数据，即无值栅格不参与运算。
    :param GeoRegion user_region: 用户指定的有效计算区域。如果为 None，则表示计算全部区域，如果参与运算的数据集范围不一致，将使用所有数据集
                                 的范围的交集作为计算区域。
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetGrid or str

    """
    check_lic()
    _jvm = get_jvm()
    try:
        try:
            out_datasource = get_output_datasource(out_data)
            check_output_datasource(out_datasource)
            if out_dataset_name is None:
                _outDatasetName = "MathExpression"
            else:
                _outDatasetName = out_dataset_name
            _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
            print("outdatasetName: " + _outDatasetName + "\r\n")
            listener = None
            if progress is not None and safe_start_callback_server():
                try:
                    listener = ProgressListener(progress, "expression_math_analyst")
                    _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.addSteppedListener(listener)
                except Exception as e:
                    try:
                        close_callback_server()
                        log_error(e)
                        listener = None
                    finally:
                        e = None
                        del e

            elif user_region is not None:
                javaRegion = user_region._jobject
            else:
                javaRegion = None
            java_result_dt = _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.execute(expression, javaRegion, oj(PixelFormat._make(pixel_format)), False, is_ingore_no_value, oj(out_datasource), _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        return

    if listener is not None:
        try:
            _jvm.com.supermap.analyst.spatialanalyst.MathAnalyst.removeSteppedListener(listener)
        except Exception as e1:
            try:
                log_error(e1)
            finally:
                e1 = None
                del e1

        close_callback_server()
    elif java_result_dt is not None:
        result_dt = out_datasource[java_result_dt.getName()]
    else:
        result_dt = None
    return try_close_output_datasource(result_dt, out_datasource)


def compute_min_distance(source, reference, min_distance, max_distance, out_data=None, out_dataset_name=None, progress=None):
    """
    最近距离计算。求算“被计算记录集”中每一个对象到“参考记录集”中在查询范围内的所有对象的距离中的最小值（即最近距离），并将最近距离信息保存到一个新的属性表数据集中。
    最近距离计算功能用于计算“被计算记录集”中每一个对象（称为“被计算对象”）到“参考记录集”中在查询范围内的所有对象（称为“参考对象”）的距离中的最小值，也就是最近距离，计算的结果为一个纯属性表数据集，记录了“被计算对象”到最近的“参考对象”的距离信息，使用三个属性字段存储，分别为：Source_ID（“被计算对象”的 SMID）、根据参考对象的类型可能为 Point_ID、Line_ID、Region_ID（“参考对象”的 SMID）以及 Distance（前面二者的距离值）。如果被计算对象与多个参考对象具有最近距离，则属性表中相应的添加多条记录。

    * 支持的数据类型

      “被计算记录集”仅支持二维点记录集，“参考记录集”可以是为从二维点、线、面数据集以及二维网络数据集获得的记录集。从二维网络数据集可以获得存有弧段的记录集，或存有结点的记录集（从网络数据集的子集获取），将这两种记录集作为“参考记录集”，可用于查找最近的弧段或最近的结点。

      “被计算记录集”和“参考记录集”可以是同一个记录集，也可以是从同一个数据集查询出的不同记录集，这两种情况下，不会计算对象到自身的距离。

    * 查询范围

      查询范围由用户指定的一个最小距离和一个最大距离构成，用于过滤不参与计算的“参考对象”，即从“被计算对象”出发，只有与其距离介于最小距离和最大距离之间（包括等于）的“参考对象”参与计算。如果将查询范围设置为从“0”到“-1”，则表示计算到“参考记录集”中所有对象的最近距离。

      如下图所示，红色圆点来自“被计算记录集”，方块来自“参考记录集”，粉色区域表示查询范围，则只有位于查询范围内的蓝色方块参与最近距离计算，也就是说本例的计算的结果只包含红色圆点与距其最近的蓝色方块的 SMID 和距离值

      .. image:: ../image/ComputeDistance.png

    * 注意事项：

      * “被计算记录集”和“参考记录集”所属的数据集的必须具有相同的坐标系。

      * 如下图所示，点到线对象的距离，是计算点到整个线对象的最小距离，即在线上找到一点与被计算点的距离最短；同样的，点到面对象的距离，是计算点到面对象的整个边界的最小距离。

        .. image:: ../image/ComputeDistance_1.png

      * 计算两个对象间距离时，出现包含或（部分）重叠的情况时，距离均为 0。例如点对象在线对象上，二者间距离为 0。

    :param source:  指定的被计算记录集。只支持二维点记录集和数据集
    :type source: DatasetVector or Recordset or str
    :param reference: 指定的参考记录集。支持二维点、线、面记录集和数据集
    :type reference: DatasetVector or Recordset or str
    :param min_distance: 指定的查询范围的最小距离。取值范围为大于或等于 0。单位与被计算记录集所属数据集的单位相同。
    :type min_distance: float
    :param max_distance:  指定的查询范围的最大距离。取值范围为大于 0 的值及 -1。当设置为 -1 时，表示不限制最大距离。单位与被计算记录集所属数据集的单位相同。
    :type max_distance: float
    :param out_data: 指定的用于存储结果属性表数据集的数据源。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param out_dataset_name:  指定的结果属性表数据集的名称。
    :type out_dataset_name: str
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return:  结果数据集或数据集名称
    :rtype: DatasetVector
    """
    if isinstance(source, DatasetVector):
        source_rd = source.get_recordset(False, "STATIC", list())
    else:
        if isinstance(source, Recordset):
            source_rd = source
        else:
            if isinstance(source, str):
                source_info = source
                source = get_input_dataset(source)
                if source is not None:
                    source_rd = source.get_recordset(False, "STATIC", list())
                else:
                    raise ValueError("Failed to get source recordset from " + source_info)
            else:
                assert isinstance(source_rd, Recordset), "source required DatasetVector or Recordset, but now is " + str(type(source))
            if isinstance(reference, DatasetVector):
                reference_rd = reference.get_recordset(False, "STATIC", list())
            else:
                if isinstance(reference, Recordset):
                    reference_rd = reference
                else:
                    if isinstance(reference, str):
                        reference_info = reference
                        reference = get_input_dataset(reference)
                        if reference is not None:
                            reference_rd = reference.get_recordset(False, "STATIC", list())
                        else:
                            if not isinstance(source, Recordset):
                                source_rd.close()
                                del source_rd
                            raise ValueError("Failed to get reference recordset from " + reference_info)
                    else:
                        if not isinstance(reference_rd, Recordset):
                            if not isinstance(source, Recordset):
                                source_rd.close()
                                del source_rd
                            raise ValueError("reference required DatasetVector or Recordset, but now is " + str(type(source)))
                        elif out_data is not None:
                            out_datasource = get_output_datasource(out_data)
                        else:
                            out_datasource = source.datasource
                        check_output_datasource(out_datasource)
                        if out_dataset_name is None:
                            _outDatasetName = "MinDistance"
                        else:
                            _outDatasetName = out_dataset_name
                    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
                    try:
                        try:
                            if min_distance is None:
                                min_distance = 0
                            elif max_distance is None:
                                max_distance = -1.0
                            listener = None
                            if progress is not None:
                                if safe_start_callback_server():
                                    try:
                                        listener = ProgressListener(progress, "compute_min_distance")
                                        get_jvm().com.supermap.analyst.spatialanalyst.ProximityAnalyst.addSteppedListener(listener)
                                    except Exception as e:
                                        try:
                                            close_callback_server()
                                            log_error(e)
                                            listener = None
                                        finally:
                                            e = None
                                            del e

                            computeMinDistance = get_jvm().com.supermap.analyst.spatialanalyst.ProximityAnalyst.computeMinDistance
                            success = computeMinDistance(oj(source_rd), oj(reference_rd), float(min_distance), float(max_distance), oj(out_datasource), _outDatasetName)
                        except:
                            import traceback
                            log_error(traceback.format_exc())
                            success = False

                    finally:
                        if listener is not None:
                            try:
                                get_jvm().com.supermap.analyst.spatialanalyst.ProximityAnalyst.removeSteppedListener(listener)
                            except Exception as e1:
                                try:
                                    log_error(e1)
                                finally:
                                    e1 = None
                                    del e1

                            close_callback_server()
                        elif not isinstance(source, Recordset):
                            source_rd.close()
                            del source_rd
                        if not isinstance(reference, Recordset):
                            reference_rd.close()
                            del reference_rd
                        if success:
                            result_dt = out_datasource[_outDatasetName]
                        else:
                            result_dt = None
                        if out_data is not None:
                            return try_close_output_datasource(result_dt, out_datasource)
                        return result_dt


def compute_range_distance(source, reference, min_distance, max_distance, out_data=None, out_dataset_name=None, progress=None):
    """
    范围距离计算。求算“被计算记录集”中每一个对象到“参考记录集”中在查询范围内的每一个对象的距离，并将距离信息保存到一个新的属性表数据集中。

    该功能用于计算记录集 A 中每一个对象到记录集 B 中在查询范围内的每一个对象的距离，记录集 A 称为“被计算记录集”，当中的对象称作“被计算对象”，记录集 B 称为“参考记录集”，当中的对象称作“参考对象”。“被计算记录集”和“参考记录集”可以是同一个记录集，也可以是从同一个数据集查询出的不同记录集，这两种情况下，不会计算对象到自身的距离。

    查询范围由一个最小距离和一个最大距离构成，用于过滤不参与计算的“参考对象”，即从“被计算对象”出发，只有与其距离介于最小距离和最大距离之间（包括等于）的“参考对象”参与计算。

    如下图所示，红色圆点为“被计算对象”，方块为“参考对象”，粉色区域表示查询范围，则只有位于查询范围内的蓝色方块参与距离计算，也就是说本例的计算的结果只包含红色圆点与粉色区域内的蓝色方块的 SMID 和距离值。

    .. image:: ../image/ComputeDistance.png

    范围距离计算的结果为一个纯属性表数据集，记录了“被计算对象”到“参考对象”的距离信息，使用三个属性字段存储，分别为：Source_ID（“被计算对象”的 SMID）、根据参考对象的类型可能为 Point_ID、Line_ID、Region_ID（“参考对象”的 SMID）以及 Distance（前面二者的距离值）。

    注意事项：

     * “被计算记录集”和“参考记录集”所属的数据集的必须具有相同的坐标系。

     * 如下图所示，点到线对象的距离，是计算点到整个线对象的最小距离，即在线上找到一点与被计算点的距离最短；同样的，点到面对象的距离，是计算点到面对象的整个边界的最小距离。

       .. image:: ../image/ComputeDistance_1.png

     * 计算两个对象间距离时，出现包含或（部分）重叠的情况时，距离均为 0。例如点对象在线对象上，二者间距离为 0。

    :param source: 指定的被计算记录集。只支持二维点记录集或数据集
    :type source: DatasetVector or Recordset or str
    :param reference: 指定的参考记录集。只支持二维点、线、面记录集或数据集
    :type reference: DatasetVector or Recordset or str
    :param min_distance: 指定的查询范围的最小距离。取值范围为大于或等于 0。 单位与被计算记录集所属数据集的单位相同。
    :type min_distance: float
    :param max_distance: 指定的查询范围的最大距离。取值范围为大于或等于 0，且必须大于或等于最小距离。单位与被计算记录集所属数据集的单位相同。
    :type max_distance: float
    :param out_data: 指定的用于存储结果属性表数据集的数据源。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param out_dataset_name: 指定的结果属性表数据集的名称。
    :type out_dataset_name: str
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector
    """
    if isinstance(source, DatasetVector):
        source_rd = source.get_recordset(False, "STATIC", list())
    else:
        if isinstance(source, Recordset):
            source_rd = source
        else:
            if isinstance(source, str):
                source_info = source
                source = get_input_dataset(source)
                if source is not None:
                    source_rd = source.get_recordset(False, "STATIC", list())
                else:
                    raise ValueError("Failed to get source recordset from " + source_info)
            else:
                assert isinstance(source_rd, Recordset), "source required DatasetVector or Recordset, but now is " + str(type(source))
            if isinstance(reference, DatasetVector):
                reference_rd = reference.get_recordset(False, "STATIC", list())
            else:
                if isinstance(reference, Recordset):
                    reference_rd = reference
                else:
                    if isinstance(reference, str):
                        reference_info = reference
                        reference = get_input_dataset(reference)
                        if reference is not None:
                            reference_rd = reference.get_recordset(False, "STATIC", list())
                        else:
                            if not isinstance(source, Recordset):
                                source_rd.close()
                                del source_rd
                            raise ValueError("Failed to get reference recordset from " + reference_info)
                    else:
                        if not isinstance(reference_rd, Recordset):
                            if not isinstance(source, Recordset):
                                source_rd.close()
                                del source_rd
                            raise ValueError("reference required DatasetVector or Recordset, but now is " + str(type(source)))
                        elif out_data is not None:
                            out_datasource = get_output_datasource(out_data)
                        else:
                            out_datasource = source.datasource
                        check_output_datasource(out_datasource)
                        if out_dataset_name is None:
                            _outDatasetName = "RangeDistance"
                        else:
                            _outDatasetName = out_dataset_name
                    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
                    try:
                        try:
                            if min_distance is None:
                                min_distance = 0
                            elif max_distance is None or float(max_distance) <= float(min_distance):
                                raise ValueError("max_distance cannot be None or zero, must be greater than min_distance")
                            listener = None
                            if progress is not None:
                                if safe_start_callback_server():
                                    try:
                                        listener = ProgressListener(progress, "compute_range_distance")
                                        get_jvm().com.supermap.analyst.spatialanalyst.ProximityAnalyst.addSteppedListener(listener)
                                    except Exception as e:
                                        try:
                                            close_callback_server()
                                            log_error(e)
                                            listener = None
                                        finally:
                                            e = None
                                            del e

                            computeRangeDistance = get_jvm().com.supermap.analyst.spatialanalyst.ProximityAnalyst.computeRangeDistance
                            success = computeRangeDistance(oj(source_rd), oj(reference_rd), float(min_distance), float(max_distance), oj(out_datasource), _outDatasetName)
                        except:
                            import traceback
                            log_error(traceback.format_exc())
                            success = False

                    finally:
                        if listener is not None:
                            try:
                                get_jvm().com.supermap.analyst.spatialanalyst.ProximityAnalyst.removeSteppedListener(listener)
                            except Exception as e1:
                                try:
                                    log_error(e1)
                                finally:
                                    e1 = None
                                    del e1

                            close_callback_server()
                        elif isinstance(source, DatasetVector):
                            if source_rd is not None:
                                source_rd.close()
                                del source_rd
                            if isinstance(reference, DatasetVector):
                                if reference_rd is not None:
                                    reference_rd.close()
                                    del reference_rd
                            if success:
                                result_dt = out_datasource[_outDatasetName]
                        else:
                            result_dt = None
                        if out_data is not None:
                            return try_close_output_datasource(result_dt, out_datasource)
                        return result_dt


def integrate(source, tolerance, unit=None, progress=None):
    """
    整合, 将容限范围内的节点捕捉在一起。节点容限较大会导致要素重叠或导致面和线对象被删除，还可能导致不被期望移动的节点发生移动。
    所以，选取容限值时应当根据实际情形设置合理的容限值。

    注意：整合功能将直接修改源数据集。

    :param source: 指定的待整合的数据集。可以为点、线、面数据集。
    :type source: DatasetVector or str
    :param tolerance: 指定的节点容限。
    :type tolerance: float
    :param unit:  指定的节点容限单位。
    :type unit: Unit or str
    :param progress:
    :type progress: function
    :return: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :rtype: bool
    """
    try:
        try:
            source_dt = get_input_dataset(source)
            if not isinstance(source_dt, DatasetVector):
                raise ValueError("source required DatasetVector, but now is " + str(type(source_dt)))
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "integrate")
                        get_jvm().com.supermap.analyst.spatialanalyst.Generalization.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            unit = Unit._make(unit)
            if unit is None:
                unit = source_dt.prj_coordsys.coord_unit
            integrate = get_jvm().com.supermap.analyst.spatialanalyst.Generalization.integrate
            success = integrate(oj(source_dt), float(tolerance), oj(unit))
        except:
            import traceback
            log_error(traceback.format_exc())
            success = False

    finally:
        return

    if listener is not None:
        try:
            get_jvm().com.supermap.analyst.spatialanalyst.Generalization.removeSteppedListener(listener)
        except Exception as e1:
            try:
                log_error(e1)
            finally:
                e1 = None
                del e1

        close_callback_server()
    return success


@unique
class _EliminateMode(JEnum):
    ELIMINATE_BY_AREA = 1
    ELIMINATE_BY_BORDER = 2

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialanalyst.EliminateMode"

    @classmethod
    def _externals(cls):
        return {'AREA':_EliminateMode.ELIMINATE_BY_AREA,  'BORDER':_EliminateMode.ELIMINATE_BY_BORDER}


def eliminate(source, region_tolerance, vertex_tolerance, is_delete_single_region=False, progress=None, group_fields=None, priority_fields=None):
    """
    碎多边形合并，即将数据集中小于指定面积的多边形合并到相邻的多边形中。目前仅支持将碎多边形合并到与其相邻的具有最大面积的多边形中。

    在数据制作和处理过程中，或对不精确的数据进行叠加后，都可能产生一些细碎而无用的多边形，称为碎多边形。可以通过“碎多边形合并”
    功能将这些细碎多边形合并到相邻的多边形中，或删除孤立的碎多边形（没有与其他多边形相交或者相切的多边形），以达到简化数据的目的。

    一般面积远远小于数据集中其他对象的多边形才被认为是“碎多边形”，通常是同一数据集中最大面积的百万分之一到万分之一间，但可以依
    据实际研究的需求来设置最小多边形容限。如下图所示的数据中，在较大的多边形的边界上，有很多无用的碎多边形。

    .. image:: ../image/Eliminate_1.png

    下图是对该数据进行“碎多边形合并”处理后的结果，与上图对比可以看出，碎多边形都被合并到了相邻的较大的多边形中。

    .. image:: ../image/Eliminate_2.png

    注意：

        * 该方法适用于两个面具有公共边界的情况，处理后会把公共边界去除。
        * 进行碎多边形合并处理后，数据集内的对象数量可能减少。

    :param source: 指定的待进行碎多边形合并的数据集。只支持矢量二维面数据集，指定其他类型的数据集会抛出异常。
    :type source: DatasetVector or str
    :param region_tolerance: 指定的最小多边形容限。单位与系统计算的面积（SMAREA 字段）的单位一致。将 SMAREA 字段的值与该容限值对比，小于该值的多边形将被消除。取值范围为大于等于0，指定为小于0的值会抛出异常。
    :type region_tolerance: float
    :param vertex_tolerance: 指定的节点容限。单位与进行碎多边形合并的数据集单位相同。若两个节点之间的距离小于此容限值，则合并过程中会自动将这两个节点合并为一个节点。取值范围大于等于0，指定为小于0的值会抛出异常。
    :type vertex_tolerance: float
    :param is_delete_single_region: 指定是否删除孤立的小多边形。如果为 true 会删除孤立的小多边形，否则不删除。
    :type is_delete_single_region: bool
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :param group_fields: 分组字段，字段值相同的多边形才可能进行合并
    :type group_fields: list[str] or tuple[str] or str
    :param priority_fields: 合并对象的优先级字段，当分组字段不为空时有效。用户可以指定多个优先级字段或不指定，如果指定优先级字段，则按照字段的顺序，
                            当被合并的多边形的属性字段值等于相邻多边形的属性字段值，则合并到对应的多边形上，如果不相等，则比较下一个优先级字段的字段值，
                            如果所有的优先级字段值都不相等，则默认会合并到相邻的面积最大的多边形上。

                            例如用户指定了 A、B、C 三个优先级字段
                             - 当被合并的多边形 F1 中 A 字段值等于相邻对象 F2 的 A 字段值，则 F1 被合并到 F2 中
                             - 如果 A 字段不相等，则比较 B 字段值的值，如果 F1 的 B字段值等于相邻对象 F2 的 B 字段值，但 F1 的A 字段值又同时等于 F3 的 A 字段值，则将 F1 合并到 F3，因为靠前的字段具有较高的优先级。
                             - 如果有 F2 和 F3 两个对象的 A 字段值都等于 F1 的 A 字段值，则默认使用面积最大的多边形，即，如果 Area(F2) > Area(F3)，则 F1 合并到 F2，否则合并到 F3中。

                            当优先级字段为空时，使用面积最大原则，即小多边形（被合并的多边形）将会合并到面积最大的多边形上。
    :type priority_fields: list[str] or tuple[str] or str
    :return: 整合成功返回 True，失败返回 False
    :rtype: bool
    """
    listener = None
    try:
        try:
            source_dt = get_input_dataset(source)
            if not isinstance(source_dt, DatasetVector):
                raise ValueError("source required DatasetVector, but now is " + str(type(source_dt)))
            elif progress is not None and safe_start_callback_server():
                try:
                    listener = ProgressListener(progress, "eliminate")
                    get_jvm().com.supermap.analyst.spatialanalyst.Generalization.addSteppedListener(listener)
                except Exception as e:
                    try:
                        close_callback_server()
                        log_error(e)
                        listener = None
                    finally:
                        e = None
                        del e

                eliminate_mode = _EliminateMode._make("ELIMINATE_BY_AREA")
                eliminate = get_jvm().com.supermap.analyst.spatialanalyst.Generalization.eliminate
                group_fields = split_input_list_from_str(group_fields)
                priority_fields = split_input_list_from_str(priority_fields)
                if group_fields:
                    success = eliminateoj(source_dt)to_java_string_array(group_fields)to_java_string_array(priority_fields)float(region_tolerance)float(vertex_tolerance)oj(eliminate_mode)bool(is_delete_single_region)
            else:
                success = eliminate(oj(source_dt), float(region_tolerance), float(vertex_tolerance), oj(eliminate_mode), bool(is_delete_single_region))
        except:
            import traceback
            log_error(traceback.format_exc())
            success = False

    finally:
        return

    if listener is not None:
        try:
            get_jvm().com.supermap.analyst.spatialanalyst.Generalization.removeSteppedListener(listener)
        except Exception as e1:
            try:
                log_error(e1)
            finally:
                e1 = None
                del e1

        close_callback_server()
    return success


def eliminate_specified_regions(source, small_region_ids, vertex_tolerance, exclude_region_ids=None, group_fields=None, priority_fields=None, is_max_border=False, progress=None):
    """
    指定要被合并的多边形ID，进行碎多边形合并操作，关于碎多边形合并的相关介绍，具体参考 :py:meth:`.eliminate` .

    :param source: 指定的待进行碎多边形合并的数据集。只支持矢量二维面数据集，指定其他类型的数据集会抛出异常。
    :type source: DatasetVector or str
    :param small_region_ids: 指定被合并的小多边形的 ID，指定的对象如果找到符合要求临近对象，则会被合并到临近对象中，小多边形则会被删除。
    :type small_region_ids: int or list[int] or tuple[int]
    :param float vertex_tolerance: 指定的节点容限。单位与进行碎多边形合并的数据集单位相同。若两个节点之间的距离小于此容限值，则合并过程中会自
                                   动将这两个节点合并为一个节点。取值范围大于等于0，指定为小于0的值会抛出异常。
    :param exclude_region_ids: 指定要排除的多边形的 ID，即不参与运算的的对象 ID。
    :type exclude_region_ids: int or list[int] or tuple[int]
    :param group_fields: 分组字段，字段值相同的多边形才可能进行合并
    :type group_fields: list[str] or tuple[str] or str
    :param priority_fields: 合并对象的优先级字段，当分组字段不为空时有效。用户可以指定多个优先级字段或不指定，如果指定优先级字段，则按照字段的顺序，
                            当被合并的多边形的属性字段值等于相邻多边形的属性字段值，则合并到对应的多边形上，如果不相等，则比较下一个优先级字段的字段值，
                            如果所有的优先级字段值都不相等，等默认会合并到相邻的面积最大的多边形上或公共边界最大的多边形上。

                            例如用户指定了 A、B、C 三个优先级字段
                             - 当被合并的多边形 F1 中 A 字段值等于相邻对象 F2 的 A 字段值，则 F1 被合并到 F2 中
                             - 如果 A 字段不相等，则比较 B 字段值的值，如果 F1 的 B字段值等于相邻对象 F2 的 B 字段值，但 F1 的A 字段值又同时等于 F3 的 A 字段值，则将 F1 合并到 F3，因为靠前的字段具有较高的优先级。
                             - 如果有 F2 和 F3 两个对象的 A 字段值都等于 F1 的 A 字段值，则默认使用面积最大的多边形或公共边界最大的多边形。

                            当优先级字段为空时，使用面积最大原则，即小多边形（被合并的多边形）将会合并到面积最大的多边形上或公共边界最大的多边形上。
    :type priority_fields: list[str] or tuple[str] or str
    :param bool is_max_border: 设置合并对象时是否以最大边界方式合并：
                               - 如果为True，则指定的小多边形会被合并到临近的公共边界最长的多边形上
                               - 如果为False，则指定的小多边形会被合并到临近的面积最大的多边形上。
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 整合成功返回 True，失败返回 False
    :rtype: bool
    """
    listener = None
    try:
        try:
            source_dt = get_input_dataset(source)
            if not isinstance(source_dt, DatasetVector):
                raise ValueError("source required DatasetVector, but now is " + str(type(source_dt)))
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "eliminate")
                        get_jvm().com.supermap.analyst.spatialanalyst.Generalization.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            small_region_ids = split_input_int_list_from_str(small_region_ids)
            exclude_region_ids = split_input_int_list_from_str(exclude_region_ids)
            eliminateSpecifiedRegions = get_jvm().com.supermap.analyst.spatialanalyst.Generalization.eliminateSpecifiedRegions
            group_fields = split_input_list_from_str(group_fields)
            priority_fields = split_input_list_from_str(priority_fields)
            success = eliminateSpecifiedRegionsoj(source_dt)to_java_int_array(small_region_ids)to_java_int_array(exclude_region_ids)to_java_string_array(group_fields)to_java_string_array(priority_fields)parse_bool(is_max_border)float(vertex_tolerance)
        except:
            import traceback
            log_error(traceback.format_exc())
            success = False

    finally:
        return

    if listener is not None:
        try:
            get_jvm().com.supermap.analyst.spatialanalyst.Generalization.removeSteppedListener(listener)
        except Exception as e1:
            try:
                log_error(e1)
            finally:
                e1 = None
                del e1

        close_callback_server()
    return success


def edge_match(source, target, edge_match_mode, tolerance=None, is_union=False, edge_match_line=None, out_data=None, out_dataset_name=None, progress=None):
    """
    图幅接边，对两个二维线数据集进行自动接边。

    :param source: 接边源数据集。只能是二维线数据集。
    :type source: DatasetVector
    :param target: 接边目标数据。只能是二维线数据集，与接边源数据有相同的坐标系。
    :type target: DatasetVector
    :param edge_match_mode: 接边模式。
    :type edge_match_mode: EdgeMatchMode or str
    :param tolerance: 接边容限。单位与进行接边的数据集的单位相同。
    :type tolerance: float
    :param is_union: 是否进行接边融合。
    :type is_union: bool
    :param edge_match_line: 数据接边的接边线。在接边方式为交点位置接边 EdgeMatchMode.THE_INTERSECTION 的时候用来计算交点，
                            不设置将按照数据集范围自动计算接边线来计算交点。
                            设置接边线后，发生接边关联的对象的端点将尽可能的靠到接边线上。
    :type edge_match_line: GeoLine
    :param out_data: 接边关联数据所在的数据源。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param out_dataset_name: 接边关联数据的数据集名称。
    :type out_dataset_name: str
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 如果设置了接边关联数据集且接边成功，则返回接边关联数据集对象或数据集名称。如果没有设置接边关联数据集，将不会生成
             接边关联数据集，则返回是否进行接边成功。
    :rtype: DatasetVector or str or bool
    """
    source_dt = get_input_dataset(source)
    if not isinstance(source_dt, DatasetVector):
        raise ValueError("source required DatasetVector, but now is " + str(type(source_dt)))
    else:
        target_dt = get_input_dataset(target)
        if not isinstance(target_dt, DatasetVector):
            raise ValueError("target required DatasetVector, but now is " + str(type(target_dt)))
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            check_output_datasource(out_datasource)
        else:
            out_datasource = None
        if out_datasource is not None:
            if out_dataset_name is None:
                _outDatasetName = source_dt.name + "_edge_link"
            else:
                _outDatasetName = out_dataset_name
            _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
        else:
            _outDatasetName = None
    try:
        try:
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "edge_match")
                        get_jvm().com.supermap.analyst.spatialanalyst.Generalization.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_edge_param = get_jvm().com.supermap.analyst.spatialanalyst.EdgeMatchParameter()
            if edge_match_line is not None:
                java_edge_param.setEdgeMatchLine(oj(edge_match_line))
            java_edge_param.setEdgeMatchMode(oj(EdgeMatchMode._make(edge_match_mode)))
            if is_union is not None:
                java_edge_param.setUnion(bool(is_union))
            if tolerance is not None:
                java_edge_param.setTolerance(float(tolerance))
            if out_datasource is not None:
                java_edge_param.setOutputDatasource(oj(out_datasource))
                java_edge_param.setOutputDatasetLinkName(_outDatasetName)
            edgeMatch = get_jvm().com.supermap.analyst.spatialanalyst.Generalization.edgeMatch
            success = edgeMatch(oj(source_dt), oj(target_dt), java_edge_param)
            del java_edge_param
        except:
            import traceback
            log_error(traceback.format_exc())
            success = False

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialanalyst.Generalization.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if out_datasource is not None:
            if success:
                result_dt = out_datasource[_outDatasetName]
            else:
                result_dt = None
            return try_close_output_datasource(result_dt, out_datasource)
        return success


def region_to_center_line(region_data, out_data=None, out_dataset_name=None, progress=None):
    """
    提取面数据集或记录集的中心线，一般用于提取河流的中心线。

    该方法用于提取面对象的中心线。如果面包含岛洞，提取时会绕过岛洞，采用最短路径绕过。如下图。

    .. image:: ../image/RegionToCenterLine_1.png

    如果面对象不是简单的长条形，而是具有分叉结构，则提取的中心线是最长的一段。如下图所示。

    .. image:: ../image/RegionToCenterLine_2.png

    :param region_data: 指定的待提取中心线的面记录集或面数据集
    :type region_data: Recordset or DatasetVector
    :param out_data: 结果数据源信息或数据源对象
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param out_dataset_name: 结果中心线数据集名称
    :type out_dataset_name: str
    :param progress:  进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 结果数据集对象或结果数据集名称
    :rtype: DatasetVector or str
    """
    check_lic()
    if isinstance(region_data, Recordset):
        source_rd = region_data
    else:
        if isinstance(region_data, DatasetVector):
            source_rd = region_data.get_recordset(False, "STATIC")
        else:
            if isinstance(region_data, str):
                region_data = get_input_dataset(region_data)
                if region_data is not None:
                    source_rd = region_data.get_recordset(False, "STATIC")
            else:
                if not isinstance(source_rd, Recordset):
                    raise ValueError("region_data required region Recordset or Dataset")
                elif source_rd.dataset.type is not DatasetType.REGION:
                    if not isinstance(region_data, Recordset):
                        source_rd.close()
                        del source_rd
                    raise ValueError("region_data required region Recordset or Dataset")
                if out_data is not None:
                    out_datasource = get_output_datasource(out_data)
                else:
                    out_datasource = source_rd.datasource
                check_output_datasource(out_datasource)
                if out_dataset_name is None:
                    _outDatasetName = source_rd.dataset.name + "_center"
                else:
                    _outDatasetName = out_dataset_name
            _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
            try:
                try:
                    listener = None
                    if progress is not None:
                        if safe_start_callback_server():
                            try:
                                listener = ProgressListener(progress, "region_to_center_line")
                                get_jvm().com.supermap.analyst.spatialanalyst.Generalization.addSteppedListener(listener)
                            except Exception as e:
                                try:
                                    close_callback_server()
                                    log_error(e)
                                    listener = None
                                finally:
                                    e = None
                                    del e

                    regionToCenterLine = get_jvm().com.supermap.analyst.spatialanalyst.Generalization.regionToCenterLine
                    java_result_dt = regionToCenterLine(oj(source_rd), oj(out_datasource), _outDatasetName)
                except:
                    import traceback
                    log_error(traceback.format_exc())
                    java_result_dt = None

            finally:
                if listener is not None:
                    try:
                        get_jvm().com.supermap.analyst.spatialanalyst.Generalization.removeSteppedListener(listener)
                    except Exception as e1:
                        try:
                            log_error(e1)
                        finally:
                            e1 = None
                            del e1

                    close_callback_server()
                elif not isinstance(region_data, Recordset):
                    source_rd.close()
                    del source_rd
                if java_result_dt is not None:
                    result_dt = out_datasource[java_result_dt.getName()]
                else:
                    result_dt = None
                if out_data is not None:
                    return try_close_output_datasource(result_dt, out_datasource)
                return result_dt


def dual_line_to_center_line(source_line, max_width, min_width, out_data=None, out_dataset_name=None, progress=None):
    """

    根据给定的宽度从双线记录集或数据集中提取中心线。
    该功能一般用于提取双线道路或河流的中心线。双线要求连续且平行或基本平行，提取效果如下图。

    .. image:: ../image/DualLineToCenterLine.png

    注意：

     * 双线一般为双线道路或双线河流，可以是线数据，也可以是面数据。
     * max_width 和 min_width 参数用于指定记录集中双线的最大宽度和最小宽度,用于提取最小和最大宽度之间的双线的中心线。小于最小宽度、大于最大宽度部分的双线不提取中心线，且大于最大宽度的双线保留，小于最小宽度的双线丢弃。
     * 对于双线道路或双线河流中比较复杂的交叉口，如五叉六叉，或者双线的最大宽度和最小宽度相差较大的情形，提取的结果可能不理想。

    :param source_line: 指定的双线记录集或数据集。要求为面类型的数据集或记录集。
    :type source_line: DatasetVector or Recordset or str
    :param max_width: 指定的双线的最大宽度。要求为大于 0 的值。单位与双线记录集所属的数据集相同。
    :type max_width: float
    :param min_width: 指定的双线的最小宽度。要求为大于或等于 0 的值。单位与双线记录集所属的数据集相同。
    :type min_width: float
    :param out_data: 指定的用于存储结果中心线数据集的数据源。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param out_dataset_name: 指定的结果中心线数据集的名称。
    :type out_dataset_name: str
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 结果数据集对象或结果数据集名称
    :rtype: DatasetVector or str
    """
    if isinstance(source_line, Recordset):
        source_rd = source_line
    else:
        if isinstance(source_line, DatasetVector):
            source_rd = source_line.get_recordset(False, "STATIC")
        else:
            if isinstance(source_line, str):
                source_line = get_input_dataset(source_line)
                if source_line is not None:
                    source_rd = source_line.get_recordset(False, "STATIC")
            else:
                if not isinstance(source_rd, Recordset):
                    raise ValueError("region_data required line or region Recordset or Dataset")
                elif source_rd.dataset.type not in (DatasetType.LINE, DatasetType.REGION):
                    if not isinstance(source_line, Recordset):
                        source_rd.close()
                        del source_rd
                    raise ValueError("region_data required line or region Recordset or Dataset")
                if out_data is not None:
                    out_datasource = get_output_datasource(out_data)
                else:
                    out_datasource = source_rd.datasource
                check_output_datasource(out_datasource)
                if out_dataset_name is None:
                    _outDatasetName = source_rd.dataset.name + "_centerline"
                else:
                    _outDatasetName = out_dataset_name
            _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
            try:
                try:
                    listener = None
                    if progress is not None:
                        if safe_start_callback_server():
                            try:
                                listener = ProgressListener(progress, "dual_line_to_center_line")
                                get_jvm().com.supermap.analyst.spatialanalyst.Generalization.addSteppedListener(listener)
                            except Exception as e:
                                try:
                                    close_callback_server()
                                    log_error(e)
                                    listener = None
                                finally:
                                    e = None
                                    del e

                    dualLineToCenterLine = get_jvm().com.supermap.analyst.spatialanalyst.Generalization.dualLineToCenterLine
                    java_result_dt = dualLineToCenterLine(oj(source_rd), float(max_width), float(min_width), oj(out_datasource), _outDatasetName)
                except:
                    import traceback
                    log_error(traceback.format_exc())
                    java_result_dt = None

            finally:
                if listener is not None:
                    try:
                        get_jvm().com.supermap.analyst.spatialanalyst.Generalization.removeSteppedListener(listener)
                    except Exception as e1:
                        try:
                            log_error(e1)
                        finally:
                            e1 = None
                            del e1

                    close_callback_server()
                elif not isinstance(source_line, Recordset):
                    source_rd.close()
                    del source_rd
                if java_result_dt is not None:
                    result_dt = out_datasource[java_result_dt.getName()]
                else:
                    result_dt = None
                if out_data is not None:
                    return try_close_output_datasource(result_dt, out_datasource)
                return result_dt


def _get_surface_extract_parameter(datum_value=0.0, interval=0.0, resample_tolerance=0.0, smooth_method='BSPLINE', smoothness=0, expected_z_values=None):
    java_param = get_jvm().com.supermap.analyst.spatialanalyst.SurfaceExtractParameter()
    java_param.setDatumValue(float(datum_value))
    if interval <= 0:
        raise ValueError("interval must be greater than 0, now is " + str(interval))
    java_param.setInterval(float(interval))
    java_param.setResampleTolerance(float(resample_tolerance))
    if smooth_method is not None:
        java_param.setSmoothMethod(oj(SmoothMethod._make(smooth_method)))
    java_param.setSmoothness(int(smoothness))
    if expected_z_values is not None:
        java_param.setExpectedZValues(to_java_double_array(split_input_list_from_str(expected_z_values)))
    return java_param


def grid_extract_isoline(extracted_grid, interval, datum_value=0.0, expected_z_values=None, resample_tolerance=0.0, smooth_method='BSPLINE', smoothness=0, clip_region=None, out_data=None, out_dataset_name=None, progress=None):
    """
    用于从栅格数据集中提取等值线，并将结果保存为数据集。

    等值线是由一系列具有相同值的点连接而成的光滑曲线或折线，如等高线、等温线。等值线的分布反映了栅格表面上值的变化，等值线分布越密集的地方， 表示栅格表面值的变化比较剧烈，例如，如果为等高线，则越密集，坡度越陡峭，反之坡度越平缓。通过提取等值线，可以找到高程、温度、降水等的值相同的位置， 同时等值线的分布状况也可以显示出变化的陡峭和平缓区。

    如下所示，上图为某个区域的 DEM 栅格数据，下图是从上图中提取的等高线。DEM 栅格数据的高程信息是存储在每一个栅格单元中的，栅格是有大小的，栅格的大小取决于栅格数据的分辨率 ，即每一个栅格单元代表实际地面上的相应地块的大小，因此，栅格数据不能很精确的反应每一位置上的高程信息 ，而矢量数据在这方面相对具有很大的优势，因此，从栅格数据中提取等高线 ，把栅格数据变成矢量数据，就可以突出显示数据的细节部分，便于分析，例如，从等高线数据中可以明显的区分地势的陡峭与舒缓的部位，可以区分出山脊山谷

    .. image:: ../image/SurfaceAnalyst_1.png

    .. image:: ../image/SurfaceAnalyst_2.png

    SuperMap 提供两种方法来提取等值线：

        * 通过设置基准值（datum_value）和等值距（interval）来提取等间距的等值线。该方法是以等值距为间隔向基准值的前后两个方向
          计算提取哪些高程的等值线。例如，高程范围为15-165的 DEM 栅格数据，设置基准值为50，等值距为20，则提取等值线的高程分别
          为：30、50、70、90、110、130和150。
        * 通过 expected_z_values 方法指定一个 Z 值的集合，则只提取高程为集合中值的等值线/面。例如，高程范围为0-1000的 DEM 栅
          格数据，指定 Z 值集合为[20,300,800]，那么提取的结果就只有 20、300、800 三条等值线或三者构成的等值面。

    注意：
        * 如果同时调用了上面两种方法所需设置的属性，那么只有 expected_z_values 方法有效，即只提取指定的值的等值线。因此，想要
          提取等间距的等值线，就不能调用 expected_z_values 方法。

    :param extracted_grid: 指定的提取操作需要的参数。
    :type extracted_grid: DatasetGrid or str
    :param  float interval:  等值距，等值距是两条等值线之间的间隔值，必须大于0.
    :param datum_value: 设置等值线的基准值。基准值与等值距（interval）共同决定提取哪些高程上的等值线。基准值作为一个生成等值
                        线的初始起算值，以等值距为间隔向其前后两个方向计算，因此并不一定是最小等值线的值。例如，高程范围为
                        220-1550 的 DEM 栅格数据，如果设基准值为 500，等值距为 50，则提取等值线的结果是：最小等值线值为 250，
                        最大等值线值为 1550。

                        当同时设置 expected_z_values 时，只会考虑 expected_z_values 设置的值，即只提取高程为这些值的等值线。
    :type datum_value: float

    :param expected_z_values: 期望分析结果的 Z 值集合。Z 值集合存储一系列数值，该数值为待提取等值线的值。即，仅高程值在Z值集
                              合中的等值线会被提取。
                              当同时设置 datum_value 时，只会考虑 expected_z_values 设置的值，即只提取高程为这些值的等值线。
    :type expected_z_values: list[float] or str
    :param resample_tolerance: 重采样的距离容限系数。通过对提取出的等值线行重采样，可以简化最终提取的等值线数据。SuperMap 在
                               提取等值线/面时使用的重采样方法为光栏法（VectorResampleType.RTBEND），该方法需要一个重采样
                               距离容限进行采样控制。它的值由重采样的距离容限系数乘以源栅格分辨率得出，一般取值为源栅格分辨率
                               的 0～1 倍。

                               重采样的距离容限系数默认为 0，即不进行任何采样，保证结果正确，但通过设置合理的参数，可以加快执
                               行速度。容限值越大，等值线边界的控制点越少，此时可能出现等值线相交的情况。因此，推荐用户先使
                               用默认值来提取等值线。
    :type resample_tolerance: float
    :param smooth_method: 滑处理所使用的方法
    :type smooth_method: SmoothMethod or str
    :param smoothness: 设置等值线或等值面的光滑度。 光滑度为 0 或 1表示不进行光滑处理，值越大则光滑度越高。等值线提取时，光滑度可自由设置
    :type smoothness: int
    :param clip_region: 指定的裁剪面对象。如果不需要对操作结果进行裁剪，可以使用 None 值取代该参数。
    :type clip_region: GeoRegion
    :param out_data: 用于存放结果数据集的数据源。如果为空，则会直接返回等值线对象的列表。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param out_dataset_name:  指定的提取结果数据集的名称。
    :type out_dataset_name: str
    :param progress: function
    :type progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 提取等值线得到的数据集或数据集名称，或等值线对象列表。
    :rtype: DatasetVector or str or list[GeoLine]
    """
    check_lic()
    source_dt = get_input_dataset(extracted_grid)
    if not isinstance(source_dt, DatasetGrid):
        raise ValueError("extracted_grid required DatasetGrid, but is " + str(type(extracted_grid)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
            check_output_datasource(out_datasource)
            if out_dataset_name is None:
                _outDatasetName = source_dt.name + "_isoline"
            else:
                _outDatasetName = out_dataset_name
            _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
        else:
            out_datasource = None
            _outDatasetName = None
        if clip_region is not None:
            java_clip_region = oj(clip_region)
        else:
            java_clip_region = None
    try:
        try:
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "grid_extract_isoline")
                        get_jvm().com.supermap.analyst.spatialanalyst.SurfaceAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_param = _get_surface_extract_parameter(datum_value, interval, resample_tolerance, smooth_method, smoothness, expected_z_values)
            extractIsoline = get_jvm().com.supermap.analyst.spatialanalyst.SurfaceAnalyst.extractIsoline
            if out_datasource is not None:
                if java_clip_region is not None:
                    java_result = extractIsoline(java_param, oj(source_dt), oj(out_datasource), _outDatasetName, java_clip_region)
                else:
                    java_result = extractIsoline(java_param, oj(source_dt), oj(out_datasource), _outDatasetName)
            else:
                java_result = extractIsoline(java_param, oj(source_dt), java_clip_region)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialanalyst.SurfaceAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if java_clip_region is not None:
            java_clip_region.dispose()
        del java_clip_region
        if java_result is None:
            if out_datasource is not None:
                try_close_output_datasource(None, out_datasource)
            return
        if out_datasource is not None:
            return try_close_output_datasource(out_datasource[java_result.getName()], out_datasource)
        return list((Geometry._from_java_object(geo) for geo in java_result))


def point_extract_isoline(extracted_point, z_value_field, resolution, interval, terrain_interpolate_type=None, datum_value=0.0, expected_z_values=None, resample_tolerance=0.0, smooth_method='BSPLINE', smoothness=0, clip_region=None, out_data=None, out_dataset_name=None, progress=None):
    """
    用于从点数据集中提取等值线，并将结果保存为数据集。方法的实现原理类似“从点数据集中提取等值线”的方法，不同之处在于，
    这里的操作对象是点数据集，因此， 实现的过程是先对点数据集中的点数据使用 IDW 插值法（'InterpolationAlgorithmType.IDW` ）
    进行插值分析，得到栅格数据集（方法实现的中间结果，栅格值为单精度浮点型），然后从栅格数据集中提取等值线。

    点数据中的点是分散分布，点数据能够很好的表现位置信息，但对于点本身的其他属性信息却表现不出来，例如，已经获取了某个研究区域的
    大量采样点的高程信息，如下所示 （上图），从图上并不能看出地势高低起伏的趋势，看不出哪里地势陡峭、哪里地形平坦，如果我们运用
    等值线的原理，将这些点数据所蕴含的信息以等值线的形式表现出来， 即将相邻的具有相同高程值的点连接起来 ，形成下面下图所示的等
    高线图，那么关于这个区域的地形信息就明显的表现出来了。不同的点数据提取的等值线具有不同的含义，主要依据点数据多代表的信息而定，
    如果点的值代表温度，那么提取的等值线就是等温线；如果点的值代表雨量，那么提取的等值线就是等降水量线，等等。

    .. image:: ../image/SurfaceAnalyst_3.png

    .. image:: ../image/SurfaceAnalyst_4.png

    注意：

     * 从点数据（点数据集/记录集/三维点集合）中提取等值线（面）时，插值得出的中间结果栅格的分辨率如果太小，会导致提取等值线（面）
       失败。这里提供一个判断方法：使用点数据的 Bounds 的长和宽分别除以设置的分辨率，也就是中间结果栅格的行列数，如果行列数任何一
       个大于10000，即认为分辨率设置的过小了，此时系统会抛出异常

    :param extracted_point: 指定的待提取的点数据集或记录集
    :type extracted_point: DatasetVector or str or Recordset
    :param z_value_field: 指定的用于提取操作的字段名称。提取等值线时，将使用该字段中的值，对点数据集进行插值分析。
    :type z_value_field: str
    :param resolution: 指定的中间结果（栅格数据集）的分辨率。
    :type resolution: float
    :param float interval:  等值距，等值距是两条等值线之间的间隔值，必须大于0
    :param terrain_interpolate_type: 地形插值类型。
    :type terrain_interpolate_type: TerrainInterpolateType or str
    :param datum_value: 设置等值线的基准值。基准值与等值距（interval）共同决定提取哪些高程上的等值线。基准值作为一个生成等值
                        线的初始起算值，以等值距为间隔向其前后两个方向计算，因此并不一定是最小等值线的值。例如，高程范围为
                        220-1550 的 DEM 栅格数据，如果设基准值为 500，等值距为 50，则提取等值线的结果是：最小等值线值为 250，
                        最大等值线值为 1550。

                        当同时设置 expected_z_values 时，只会考虑 expected_z_values 设置的值，即只提取高程为这些值的等值线。
    :type datum_value: float
    :param expected_z_values: 期望分析结果的 Z 值集合。Z 值集合存储一系列数值，该数值为待提取等值线的值。即，仅高程值在Z值集
                              合中的等值线会被提取。
                              当同时设置 datum_value 时，只会考虑 expected_z_values 设置的值，即只提取高程为这些值的等值线。
    :type expected_z_values: list[float] or str
    :param resample_tolerance: 重采样的距离容限系数。通过对提取出的等值线行重采样，可以简化最终提取的等值线数据。SuperMap 在
                               提取等值线/面时使用的重采样方法为光栏法（VectorResampleType.RTBEND），该方法需要一个重采样
                               距离容限进行采样控制。它的值由重采样的距离容限系数乘以源栅格分辨率得出，一般取值为源栅格分辨率
                               的 0～1 倍。

                               重采样的距离容限系数默认为 0，即不进行任何采样，保证结果正确，但通过设置合理的参数，可以加快执
                               行速度。容限值越大，等值线边界的控制点越少，此时可能出现等值线相交的情况。因此，推荐用户先使
                               用默认值来提取等值线。
    :type resample_tolerance: float
    :param smooth_method: 滑处理所使用的方法
    :type smooth_method: SmoothMethod or str
    :param smoothness: 设置等值线或等值面的光滑度。 光滑度为 0 或 1表示不进行光滑处理，值越大则光滑度越高。等值线提取时，光滑度可自由设置
    :type smoothness: int
    :param clip_region: 指定的裁剪面对象。
    :type clip_region: GeoRegion
    :param out_data: 用于存放结果数据集的数据源。 如果为空，则会直接返回等值线对象的列表。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param out_dataset_name:  指定的提取结果数据集的名称。
    :type out_dataset_name: str
    :param progress: function
    :type progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 提取等值线得到的数据集或数据集名称，或等值线对象列表
    :rtype: DatasetVector or str or list[GeoLine]
    """
    check_lic()
    source_dt = get_input_dataset(extracted_point)
    if not isinstance(source_dt, (DatasetVector, Recordset)):
        raise ValueError("extracted_point required DatasetVector or Recordset, but is " + str(type(extracted_point)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
            check_output_datasource(out_datasource)
            if out_dataset_name is None:
                _outDatasetName = source_dt.name + "_isoline"
            else:
                _outDatasetName = out_dataset_name
            _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
        else:
            out_datasource = None
            _outDatasetName = None
        if clip_region is not None:
            java_clip_region = oj(GeoRegion(clip_region))
        else:
            java_clip_region = None
    try:
        try:
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "point_extract_isoline")
                        get_jvm().com.supermap.analyst.spatialanalyst.SurfaceAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_param = _get_surface_extract_parameter(datum_value, interval, resample_tolerance, smooth_method, smoothness, expected_z_values)
            extractIsoline = get_jvm().com.supermap.analyst.spatialanalyst.SurfaceAnalyst.extractIsoline
            if out_datasource is not None:
                if terrain_interpolate_type is not None:
                    terrain_interpolate_type = TerrainInterpolateType._make(terrain_interpolate_type)
                    java_result = extractIsoline(java_param, oj(source_dt), str(z_value_field), oj(terrain_interpolate_type), oj(out_datasource), _outDatasetName, float(resolution), java_clip_region)
                else:
                    java_result = extractIsolinejava_paramoj(source_dt)str(z_value_field)oj(out_datasource)_outDatasetNamefloat(resolution)java_clip_region
            else:
                if terrain_interpolate_type is not None:
                    terrain_interpolate_type = TerrainInterpolateType._make(terrain_interpolate_type)
                    java_result = extractIsoline(java_param, oj(source_dt), str(z_value_field), oj(terrain_interpolate_type), float(resolution), java_clip_region)
                else:
                    java_result = extractIsoline(java_param, oj(source_dt), str(z_value_field), float(resolution), java_clip_region)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialanalyst.SurfaceAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if java_result is None:
            if out_datasource is not None:
                try_close_output_datasource(None, out_datasource)
            return
        if out_datasource is not None:
            return try_close_output_datasource(out_datasource[java_result.getName()], out_datasource)
        return list((Geometry._from_java_object(geo) for geo in java_result))


def point3ds_extract_isoline(extracted_points, resolution, interval, terrain_interpolate_type=None, datum_value=0.0, expected_z_values=None, resample_tolerance=0.0, smooth_method='BSPLINE', smoothness=0, clip_region=None, out_data=None, out_dataset_name=None, progress=None):
    """
    用于从三维点集合中提取等值线，并将结果保存为数据集。方法的实现原理是先利用点集合中存储的三维信息（高程或者温度等），也就是
    除了点的坐标信息的数据， 对点数据进行插值分析，得到栅格数据集（方法实现的中间结果，栅格值为单精度浮点型），然后从栅格数据集
    中提取等值线。

    点数据提取等值线介绍参考 :py:meth:`point_extract_isoline`

    注意：

     * 从点数据（点数据集/记录集/三维点集合）中提取等值线（面）时，插值得出的中间结果栅格的分辨率如果太小，会导致提取等值线（面）
       失败。这里提供一个判断方法：使用点数据的 Bounds 的长和宽分别除以设置的分辨率，也就是中间结果栅格的行列数，如果行列数任何一
       个大于10000，即认为分辨率设置的过小了，此时系统会抛出异常

    :param extracted_points: 指定的待提取等值线的点串，该点串中的点是三维点，每一个点存储了 X，Y 坐标信息和只有一个三维度的信息（例如：高程信息等）。
    :type extracted_points: list[Point3D]
    :param resolution: 指定的中间结果（栅格数据集）的分辨率。
    :type resolution: float
    :param float interval:  等值距，等值距是两条等值线之间的间隔值，必须大于0
    :param terrain_interpolate_type: 地形插值类型。
    :type terrain_interpolate_type: TerrainInterpolateType or str
    :param datum_value: 设置等值线的基准值。基准值与等值距（interval）共同决定提取哪些高程上的等值线。基准值作为一个生成等值
                        线的初始起算值，以等值距为间隔向其前后两个方向计算，因此并不一定是最小等值线的值。例如，高程范围为
                        220-1550 的 DEM 栅格数据，如果设基准值为 500，等值距为 50，则提取等值线的结果是：最小等值线值为 250，
                        最大等值线值为 1550。

                        当同时设置 expected_z_values 时，只会考虑 expected_z_values 设置的值，即只提取高程为这些值的等值线。
    :type datum_value: float
    :param expected_z_values: 期望分析结果的 Z 值集合。Z 值集合存储一系列数值，该数值为待提取等值线的值。即，仅高程值在Z值集
                              合中的等值线会被提取。
                              当同时设置 datum_value 时，只会考虑 expected_z_values 设置的值，即只提取高程为这些值的等值线。
    :type expected_z_values: list[float] or str
    :param resample_tolerance: 重采样的距离容限系数。通过对提取出的等值线行重采样，可以简化最终提取的等值线数据。SuperMap 在
                               提取等值线/面时使用的重采样方法为光栏法（VectorResampleType.RTBEND），该方法需要一个重采样
                               距离容限进行采样控制。它的值由重采样的距离容限系数乘以源栅格分辨率得出，一般取值为源栅格分辨率
                               的 0～1 倍。
                               重采样的距离容限系数默认为 0，即不进行任何采样，保证结果正确，但通过设置合理的参数，可以加快执
                               行速度。容限值越大，等值线边界的控制点越少，此时可能出现等值线相交的情况。因此，推荐用户先使
                               用默认值来提取等值线。
    :type resample_tolerance: float
    :param smooth_method: 滑处理所使用的方法
    :type smooth_method: SmoothMethod or str
    :param smoothness: 设置等值线或等值面的光滑度。 光滑度为 0 或 1表示不进行光滑处理，值越大则光滑度越高。等值线提取时，光滑度可自由设置;
    :type smoothness: int
    :param clip_region: 指定的裁剪面对象。
    :type clip_region: GeoRegion
    :param out_data: 用于存放结果数据集的数据源。如果为空，则直接返回等值线对象列表
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param out_dataset_name:  指定的提取结果数据集的名称。
    :type out_dataset_name: str
    :param progress: function
    :type progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 提取等值线得到的数据集或数据集名称，或等值线对象列表
    :rtype: DatasetVector or str or list[GeoLine]
    """
    check_lic()
    if out_data is not None:
        out_datasource = get_output_datasource(out_data)
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = "isoline"
        else:
            _outDatasetName = out_dataset_name
        _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    else:
        out_datasource = None
        _outDatasetName = None
    if clip_region is not None:
        java_clip_region = oj(GeoRegion(clip_region))
    else:
        java_clip_region = None
    java_point_3ds = to_java_point3ds(extracted_points)
    try:
        try:
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "point3ds_extract_isoline")
                        get_jvm().com.supermap.analyst.spatialanalyst.SurfaceAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_param = _get_surface_extract_parameter(datum_value, interval, resample_tolerance, smooth_method, smoothness, expected_z_values)
            extractIsoline = get_jvm().com.supermap.analyst.spatialanalyst.SurfaceAnalyst.extractIsoline
            if out_datasource is not None:
                if terrain_interpolate_type is not None:
                    terrain_interpolate_type = TerrainInterpolateType._make(terrain_interpolate_type)
                    java_result = extractIsolinejava_paramjava_point_3dsoj(terrain_interpolate_type)oj(out_datasource)_outDatasetNamefloat(resolution)java_clip_region
                else:
                    java_result = extractIsoline(java_param, java_point_3ds, oj(out_datasource), _outDatasetName, float(resolution), java_clip_region)
            else:
                if terrain_interpolate_type is not None:
                    terrain_interpolate_type = TerrainInterpolateType._make(terrain_interpolate_type)
                    java_result = extractIsoline(java_param, java_point_3ds, oj(terrain_interpolate_type), float(resolution), java_clip_region)
                else:
                    java_result = extractIsoline(java_param, java_point_3ds, float(resolution), java_clip_region)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialanalyst.SurfaceAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if java_result is None:
            if out_datasource is not None:
                try_close_output_datasource(None, out_datasource)
            return
        if out_datasource is not None:
            return try_close_output_datasource(out_datasource[java_result.getName()], out_datasource)
        return list((Geometry._from_java_object(geo) for geo in java_result))


def grid_extract_isoregion(extracted_grid, interval, datum_value=0.0, expected_z_values=None, resample_tolerance=0.0, smooth_method='BSPLINE', smoothness=0, clip_region=None, out_data=None, out_dataset_name=None, progress=None):
    """
    用于从栅格数据集中提取等值面。

    SuperMap 提供两种方法来提取等值面：

    * 通过设置基准值（datum_value）和等值距（interval）来提取等间距的等值面。该方法是以等值距为间隔向基准值的前后两个方向计算
      提取哪些高程的等值线。例如，高程范围为15-165的 DEM 栅格数据，设置基准值为50，等值距为20，则提取等值线的高程分别为：
      30、50、70、90、110、130和150。
    * 通过 expected_z_values 方法指定一个 Z 值的集合，则只提取高程为集合中值的等值面。例如，高程范围为0-1000的 DEM 栅格数据，
      指定 Z 值集合为[20,300,800]，那么提取的结果就只有20、300、800三者构成的等值面。

    注意：

     * 如果同时调用了上面两种方法所需设置的属性，那么只有 setExpectedZValues 方法有效，即只提取指定的值的等值面。
       因此，想要提取等间距的等值面，就不能调用 expected_z_values 方法。

    :param extracted_grid: DatasetGrid or str
    :type extracted_grid:  指定的待提取的栅格数据集。
    :param float interval:  等值距，等值距是两条等值线之间的间隔值，必须大于0
    :param datum_value: 设置等值线的基准值。基准值与等值距（interval）共同决定提取哪些高程上的等值面。基准值作为一个生成等值
                        线的初始起算值，以等值距为间隔向其前后两个方向计算，因此并不一定是最小等值面的值。例如，高程范围为
                        220-1550 的 DEM 栅格数据，如果设基准值为 500，等值距为 50，则提取等值线的结果是：最小等值线值为 250，
                        最大等值线值为 1550。

                        当同时设置 expected_z_values 时，只会考虑 expected_z_values 设置的值，即只提取高程为这些值的等值线。
    :type datum_value: float
    :param expected_z_values: 期望分析结果的 Z 值集合。Z 值集合存储一系列数值，该数值为待提取等值线的值。即，仅高程值在Z值集
                              合中的等值线会被提取。
                              当同时设置 datum_value 时，只会考虑 expected_z_values 设置的值，即只提取高程为这些值的等值线。
    :type expected_z_values: list[float] or str
    :param resample_tolerance: 重采样的距离容限系数。通过对提取出的等值线行重采样，可以简化最终提取的等值线数据。SuperMap 在
                               提取等值线/面时使用的重采样方法为光栏法（VectorResampleType.RTBEND），该方法需要一个重采样
                               距离容限进行采样控制。它的值由重采样的距离容限系数乘以源栅格分辨率得出，一般取值为源栅格分辨率
                               的 0～1 倍。
                               重采样的距离容限系数默认为 0，即不进行任何采样，保证结果正确，但通过设置合理的参数，可以加快执
                               行速度。容限值越大，等值线边界的控制点越少，此时可能出现等值线相交的情况。因此，推荐用户先使
                               用默认值来提取等值线。
    :type resample_tolerance: float
    :param smooth_method: 滑处理所使用的方法
    :type smooth_method: SmoothMethod or str
    :param smoothness: 设置等值面的光滑度。 光滑度为 0 或 1表示不进行光滑处理，值越大则光滑度越高。
                       对于等值面的提取，采用先提取等值线然后生成等值面的方式，若将光滑度设置为2，
                       则中间结果数据集，即等值线对象的点数将为原始数据集点数的2倍，当光滑度设定值不断增大时，点数将成2的指数倍
                       增长，这将大大降低等值面提取的效率甚至可能导致提取失败。
    :type smoothness: int
    :param clip_region: 指定的裁剪面对象。
    :type clip_region: GeoRegion
    :param out_data: 用于存放结果数据集的数据源。如果为空，则直接返回等值面对象列表
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param out_dataset_name:  指定的提取结果数据集的名称。
    :type out_dataset_name: str
    :param progress: function
    :type progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 提取等值面得到的数据集或数据集名称，或等值面对象列表
    :rtype: DatasetVector or str or list[GeoRegion]
    """
    check_lic()
    source_dt = get_input_dataset(extracted_grid)
    if not isinstance(source_dt, DatasetGrid):
        raise ValueError("extracted_grid required DatasetGrid, but is " + str(type(extracted_grid)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
            check_output_datasource(out_datasource)
            if out_dataset_name is None:
                _outDatasetName = source_dt.name + "_isoregion"
            else:
                _outDatasetName = out_dataset_name
            _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
        else:
            out_datasource = None
            _outDatasetName = None
        if clip_region is not None:
            java_clip_region = oj(GeoRegion(clip_region))
        else:
            java_clip_region = None
    try:
        try:
            listener = None
            if progress is not None and safe_start_callback_server():
                try:
                    listener = ProgressListener(progress, "grid_extract_isoregion")
                    get_jvm().com.supermap.analyst.spatialanalyst.SurfaceAnalyst.addSteppedListener(listener)
                except Exception as e:
                    try:
                        close_callback_server()
                        log_error(e)
                        listener = None
                    finally:
                        e = None
                        del e

            else:
                java_param = _get_surface_extract_parameter(datum_value, interval, resample_tolerance, smooth_method, smoothness, expected_z_values)
                extractIsoregion = get_jvm().com.supermap.analyst.spatialanalyst.SurfaceAnalyst.extractIsoregion
                if out_datasource is not None:
                    java_result = extractIsoregion(java_param, oj(source_dt), oj(out_datasource), _outDatasetName, java_clip_region)
                else:
                    java_result = extractIsoregion(java_param, oj(source_dt), java_clip_region)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialanalyst.SurfaceAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if java_result is None:
            if out_datasource is not None:
                return try_close_output_datasource(None, out_datasource)
            return
        if out_datasource is not None:
            return try_close_output_datasource(out_datasource[java_result.getName()], out_datasource)
        return list((Geometry._from_java_object(geo) for geo in java_result))


def points_extract_isoregion(extracted_point, z_value_field, interval, resolution=None, terrain_interpolate_type=None, datum_value=0.0, expected_z_values=None, resample_tolerance=0.0, smooth_method='BSPLINE', smoothness=0, clip_region=None, out_data=None, out_dataset_name=None, progress=None):
    """
    用于从点数据集中提取等值面。方法的实现原理是先对点数据集使用 IDW 插值法（InterpolationAlgorithmType.IDW）进行插值分析，
    得到栅格数据集（方法实现的中间结果，栅格值为单精度浮点型），接着从栅格数据集中提取等值线， 最终由等值线构成等值面。

    等值面是由相邻的等值线封闭组成的面。等值面的变化可以很直观的表示出相邻等值线之间的变化，诸如高程、温度、降水、污染或大气压
    力等用等值面来表示是非常直观、 有效的。等值面分布的效果与等值线的分布相同，也是反映了栅格表面上的变化，等值面分布越密集的地
    方，表示栅格表面值有较大的变化，反之则表示栅格表面值变化较少； 等值面越窄的地方，表示栅格表面值有较大的变化，反之则表示栅格
    表面值变化较少。

    如下所示，上图为存储了高程信息的点数据集，下图为从上图点数据集中提取的等值面，从等值面数据中可以明显的分析出地形的起伏变化，
    等值面越密集， 越狭窄的地方表示地势越陡峭，反之，等值面越稀疏，较宽的地方表示地势较舒缓，变化较小。

    .. image:: ../image/SurfaceAnalyst_5.png

    .. image:: ../image/SurfaceAnalyst_6.png

    注意：

     * 从点数据（点数据集/记录集/三维点集合）中提取等值面时，插值得出的中间结果栅格的分辨率如果太小，会导致提取等值面
       失败。这里提供一个判断方法：使用点数据的 Bounds 的长和宽分别除以设置的分辨率，也就是中间结果栅格的行列数，如果行列数任何一个
       大于10000，即认为分辨率设置的过小了，此时系统会抛出异常。

    :param extracted_point: 指定的待提取的点数据集或记录集
    :type extracted_point: DatasetVector or str or Recordset
    :param z_value_field: 指定的用于提取操作的字段名称。提取等值面时，将使用该字段中的值，对点数据集进行插值分析。
    :type z_value_field: str
    :param float interval:  等值距，等值距是两条等值线之间的间隔值，必须大于0
    :param resolution: 指定的中间结果（栅格数据集）的分辨率。
    :type resolution: float
    :param terrain_interpolate_type: 指定的地形插值类型。
    :type terrain_interpolate_type: TerrainStatisticType
    :param datum_value: 设置等值线的基准值。基准值与等值距（interval）共同决定提取哪些高程上的等值面。基准值作为一个生成等值
                        线的初始起算值，以等值距为间隔向其前后两个方向计算，因此并不一定是最小等值面的值。例如，高程范围为
                        220-1550 的 DEM 栅格数据，如果设基准值为 500，等值距为 50，则提取等值线的结果是：最小等值线值为 250，
                        最大等值线值为 1550。

                        当同时设置 expected_z_values 时，只会考虑 expected_z_values 设置的值，即只提取高程为这些值的等值线。
    :type datum_value: float
    :param expected_z_values: 期望分析结果的 Z 值集合。Z 值集合存储一系列数值，该数值为待提取等值线的值。即，仅高程值在Z值集
                              合中的等值线会被提取。
                              当同时设置 datum_value 时，只会考虑 expected_z_values 设置的值，即只提取高程为这些值的等值线。
    :type expected_z_values: list[float] or str
    :param resample_tolerance: 重采样的距离容限系数。通过对提取出的等值线行重采样，可以简化最终提取的等值线数据。SuperMap 在
                               提取等值线/面时使用的重采样方法为光栏法（VectorResampleType.RTBEND），该方法需要一个重采样
                               距离容限进行采样控制。它的值由重采样的距离容限系数乘以源栅格分辨率得出，一般取值为源栅格分辨率
                               的 0～1 倍。
                               重采样的距离容限系数默认为 0，即不进行任何采样，保证结果正确，但通过设置合理的参数，可以加快执
                               行速度。容限值越大，等值线边界的控制点越少，此时可能出现等值线相交的情况。因此，推荐用户先使
                               用默认值来提取等值线。
    :type resample_tolerance: float
    :param smooth_method: 滑处理所使用的方法
    :type smooth_method: SmoothMethod or str
    :param smoothness: 设置等值面的光滑度。 光滑度为 0 或 1表示不进行光滑处理，值越大则光滑度越高。
                       对于等值面的提取，采用先提取等值线然后生成等值面的方式，若将光滑度设置为2，
                       则中间结果数据集，即等值线对象的点数将为原始数据集点数的2倍，当光滑度设定值不断增大时，点数将成2的指数倍
                       增长，这将大大降低等值面提取的效率甚至可能导致提取失败。
    :type smoothness: int
    :param clip_region: 指定的裁剪面对象。
    :type clip_region: GeoRegion
    :param out_data: 用于存放结果数据集的数据源。如果为空，则直接返回等值面对象列表
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param out_dataset_name:  指定的提取结果数据集的名称。
    :type out_dataset_name: str
    :param progress: function
    :type progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 提取等值面得到的数据集或数据集名称，或等值面对象列表
    :rtype: DatasetVector or str or list[GeoRegion]
    """
    source_dt = get_input_dataset(extracted_point)
    if not isinstance(source_dt, (DatasetVector, Recordset)):
        raise ValueError("extracted_point required DatasetVector or Recordset, but is " + str(type(extracted_point)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
            check_output_datasource(out_datasource)
            if out_dataset_name is None:
                _outDatasetName = source_dt.name + "_isoregion"
            else:
                _outDatasetName = out_dataset_name
            _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
        else:
            out_datasource = None
            _outDatasetName = None
        if clip_region is not None:
            java_clip_region = oj(GeoRegion(clip_region))
        else:
            java_clip_region = None
    try:
        try:
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "points_extract_isoregion")
                        get_jvm().com.supermap.analyst.spatialanalyst.SurfaceAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_param = _get_surface_extract_parameter(datum_value, interval, resample_tolerance, smooth_method, smoothness, expected_z_values)
            extractIsoregion = get_jvm().com.supermap.analyst.spatialanalyst.SurfaceAnalyst.extractIsoregion
            if out_datasource is not None:
                if terrain_interpolate_type is not None:
                    terrain_interpolate_type = TerrainInterpolateType._make(terrain_interpolate_type)
                    java_result = extractIsoregion(java_param, oj(source_dt), str(z_value_field), oj(terrain_interpolate_type), oj(out_datasource), _outDatasetName, float(resolution), java_clip_region)
                else:
                    java_result = extractIsoregionjava_paramoj(source_dt)str(z_value_field)oj(out_datasource)_outDatasetNamefloat(resolution)java_clip_region
            else:
                if terrain_interpolate_type is not None:
                    terrain_interpolate_type = TerrainInterpolateType._make(terrain_interpolate_type)
                    java_result = extractIsoregion(java_param, oj(source_dt), str(z_value_field), oj(terrain_interpolate_type), float(resolution), java_clip_region)
                else:
                    java_result = extractIsoregion(java_param, oj(source_dt), str(z_value_field), float(resolution), java_clip_region)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialanalyst.SurfaceAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if java_result is None:
            if out_datasource is not None:
                return try_close_output_datasource(None, out_datasource)
            return
        if out_datasource is not None:
            return try_close_output_datasource(out_datasource[java_result.getName()], out_datasource)
        return list((Geometry._from_java_object(geo) for geo in java_result))


def point3ds_extract_isoregion(extracted_points, resolution, interval, terrain_interpolate_type=None, datum_value=0.0, expected_z_values=None, resample_tolerance=0.0, smooth_method='BSPLINE', smoothness=0, clip_region=None, out_data=None, out_dataset_name=None, progress=None):
    """
    用于从三维点集合中提取等值面，并将结果保存为数据集。方法的实现原理是先利用点集合中存储的第三维信息（高程或者温度等），也就
    是除了点的坐标信息的数据， 对点数据使用 IDW 插值法（InterpolationAlgorithmType.IDW）进行插值分析，得到栅格数据集（方法实现
    的中间结果，栅格值为单精度浮点型），接着从栅格数据集中提取等值面。

    点数据提取等值面介绍，参考 :py:meth:`points_extract_isoregion`

    :param extracted_points: 指定的待提取等值面的点串，该点串中的点是三维点，每一个点存储了 X，Y 坐标信息和只有一个第三维度的信息（例如：高程信息等）。
    :type extracted_points: list[Point3D]
    :param resolution: 指定的中间结果（栅格数据集）的分辨率
    :type resolution: float
    :param float interval:  等值距，等值距是两条等值线之间的间隔值，必须大于0
    :param terrain_interpolate_type: 指定的地形插值类型。
    :type terrain_interpolate_type: TerrainInterpolateType or str
    :param datum_value: 设置等值线的基准值。基准值与等值距（interval）共同决定提取哪些高程上的等值面。基准值作为一个生成等值
                        线的初始起算值，以等值距为间隔向其前后两个方向计算，因此并不一定是最小等值面的值。例如，高程范围为
                        220-1550 的 DEM 栅格数据，如果设基准值为 500，等值距为 50，则提取等值线的结果是：最小等值线值为 250，
                        最大等值线值为 1550。

                        当同时设置 expected_z_values 时，只会考虑 expected_z_values 设置的值，即只提取高程为这些值的等值线。
    :type datum_value: float
    :param expected_z_values: 期望分析结果的 Z 值集合。Z 值集合存储一系列数值，该数值为待提取等值线的值。即，仅高程值在Z值集
                              合中的等值线会被提取。
                              当同时设置 datum_value 时，只会考虑 expected_z_values 设置的值，即只提取高程为这些值的等值线。
    :type expected_z_values: list[float] or str
    :param resample_tolerance: 重采样的距离容限系数。通过对提取出的等值线行重采样，可以简化最终提取的等值线数据。SuperMap 在
                               提取等值线/面时使用的重采样方法为光栏法（VectorResampleType.RTBEND），该方法需要一个重采样
                               距离容限进行采样控制。它的值由重采样的距离容限系数乘以源栅格分辨率得出，一般取值为源栅格分辨率
                               的 0～1 倍。
                               重采样的距离容限系数默认为 0，即不进行任何采样，保证结果正确，但通过设置合理的参数，可以加快执
                               行速度。容限值越大，等值线边界的控制点越少，此时可能出现等值线相交的情况。因此，推荐用户先使
                               用默认值来提取等值线。
    :type resample_tolerance: float
    :param smooth_method: 滑处理所使用的方法
    :type smooth_method: SmoothMethod or str
    :param smoothness: 设置等值面的光滑度。 光滑度为 0 或 1表示不进行光滑处理，值越大则光滑度越高。
                       对于等值面的提取，采用先提取等值线然后生成等值面的方式，若将光滑度设置为2，
                       则中间结果数据集，即等值线对象的点数将为原始数据集点数的2倍，当光滑度设定值不断增大时，点数将成2的指数倍
                       增长，这将大大降低等值面提取的效率甚至可能导致提取失败。
    :type smoothness: int
    :param clip_region: 指定的裁剪面对象。
    :type clip_region: GeoRegion
    :param out_data: 用于存放结果数据集的数据源。如果为空，则直接返回等值面对象列表
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param out_dataset_name:  指定的提取结果数据集的名称。
    :type out_dataset_name: str
    :param progress: function
    :type progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 提取等值面得到的数据集或数据集名称，或等值面对象列表
    :rtype: DatasetVector or str or list[GeoRegion]
    """
    check_lic()
    if out_data is not None:
        out_datasource = get_output_datasource(out_data)
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = "isoregion"
        else:
            _outDatasetName = out_dataset_name
        _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    else:
        out_datasource = None
        _outDatasetName = None
    if clip_region is not None:
        java_clip_region = oj(clip_region)
    else:
        java_clip_region = None
    java_point_3ds = to_java_point3ds(extracted_points)
    try:
        try:
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "point3ds_extract_isoregion")
                        get_jvm().com.supermap.analyst.spatialanalyst.SurfaceAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_param = _get_surface_extract_parameter(datum_value, interval, resample_tolerance, smooth_method, smoothness, expected_z_values)
            extractIsoRegion = get_jvm().com.supermap.analyst.spatialanalyst.SurfaceAnalyst.extractIsoregion
            if out_datasource is not None:
                if terrain_interpolate_type is not None:
                    terrain_interpolate_type = TerrainInterpolateType._make(terrain_interpolate_type)
                    java_result = extractIsoRegionjava_paramjava_point_3dsoj(terrain_interpolate_type)oj(out_datasource)_outDatasetNamefloat(resolution)java_clip_region
                else:
                    java_result = extractIsoRegion(java_param, java_point_3ds, oj(out_datasource), _outDatasetName, float(resolution), java_clip_region)
            else:
                if terrain_interpolate_type is not None:
                    terrain_interpolate_type = TerrainInterpolateType._make(terrain_interpolate_type)
                    java_result = extractIsoRegion(java_param, java_point_3ds, oj(terrain_interpolate_type), float(resolution), java_clip_region)
                else:
                    java_result = extractIsoRegion(java_param, java_point_3ds, float(resolution), java_clip_region)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialanalyst.SurfaceAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if java_result is None:
            if out_datasource is not None:
                try_close_output_datasource(None, out_datasource)
            return
        if out_datasource is not None:
            return try_close_output_datasource(out_datasource[java_result.getName()], out_datasource)
        return list((Geometry._from_java_object(geo) for geo in java_result))


class BasicStatisticsAnalystResult:
    __doc__ = "\n    栅格基本统计分析结果类\n\n    "

    def __init__(self):
        self._first_quartile = None
        self._kurtosis = None
        self._max = None
        self._mean = None
        self._median = None
        self._min = None
        self._skewness = None
        self._std = None
        self._thd_quartile = None

    @staticmethod
    def _from_java_object(java_obj):
        if java_obj is None:
            return
        obj = BasicStatisticsAnalystResult()
        obj._first_quartile = java_obj.getFirstQuartile()
        obj._kurtosis = java_obj.getKurtosis()
        obj._max = java_obj.getMax()
        obj._min = java_obj.getMin()
        obj._mean = java_obj.getMean()
        obj._median = java_obj.getMedian()
        obj._skewness = java_obj.getSkewness()
        obj._std = java_obj.getStandardDeviation()
        obj._thd_quartile = java_obj.getThirdQuartile()
        return obj

    def __str__(self):
        return "\n".join(["Basic statistics analyst result: ",
         "first_quartile: " + str(self.first_quartile),
         "kurtosis:       " + str(self.kurtosis),
         "max:            " + str(self.max),
         "min:            " + str(self.min),
         "mean:           " + str(self.mean),
         "median:         " + str(self.median),
         "skewness:       " + str(self.skewness),
         "std:            " + str(self.std),
         "third_quartile: " + str(self.third_quartile)])

    @property
    def first_quartile(self):
        """float: 栅格基本统计分析计算所得的第一四分值"""
        return self._first_quartile

    @property
    def kurtosis(self):
        """float: 栅格基本统计分析计算所得的峰度"""
        return self._kurtosis

    @property
    def max(self):
        """float: 栅格基本统计分析计算所得的最大值"""
        return self._max

    @property
    def min(self):
        """float: """
        return self._min

    @property
    def mean(self):
        """float: 栅格基本统计分析计算所得的最小值"""
        return self._mean

    @property
    def median(self):
        """float: 栅格基本统计分析计算所得的中位数"""
        return self._median

    @property
    def skewness(self):
        """float: 栅格基本统计分析计算所得的偏度"""
        return self._skewness

    @property
    def std(self):
        """float: 栅格基本统计分析计算所得的均方差（标准差）"""
        return self._std

    @property
    def third_quartile(self):
        """float: 栅格基本统计分析计算所得的第三四分值"""
        return self._thd_quartile

    def to_dict(self):
        """
        输出为 dict 对象

        :rtype: dict
        """
        return {'first_quartile':self.first_quartile, 
         'kurtosis':self.kurtosis, 
         'max':self.max, 
         'min':self.min, 
         'mean':self.mean, 
         'median':self.median, 
         'skewness':self.skewness, 
         'std':self.std, 
         'third_quartile':self.third_quartile}


def grid_basic_statistics(grid_data, function_type=None, progress=None):
    """
    栅格基本统计分析，可指定变换函数类型。用于对栅格数据集进行基本的统计分析，包括最大值、最小值、平均值和标准差等。

    指定变换函数时，用来统计的数据是原始栅格值经过函数变换后得到的值。

    :param grid_data: 待统计的栅格数据
    :type grid_data: DatasetGrid or str
    :param function_type: 变换函数类型
    :type function_type: FunctionType or str
    :param progress: function
    :type progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 基本统计分析结果
    :rtype: BasicStatisticsAnalystResult
    """
    source_dt = get_input_dataset(grid_data)
    if not isinstance(source_dt, DatasetGrid):
        raise ValueError("extracted_point required DatasetGrid, but is " + str(type(grid_data)))
    listener = None
    try:
        try:
            if progress is not None and safe_start_callback_server():
                try:
                    listener = ProgressListener(progress, "grid_basic_statistics")
                    get_jvm().com.supermap.analyst.spatialanalyst.SurfaceAnalyst.addSteppedListener(listener)
                except Exception as e:
                    try:
                        close_callback_server()
                        log_error(e)
                        listener = None
                    finally:
                        e = None
                        del e

            else:
                basicStatistics = get_jvm().com.supermap.analyst.spatialanalyst.StatisticsAnalyst.basicStatistics
                if function_type is not None:
                    function_type = FunctionType._make(function_type)
                    java_result = basicStatistics(oj(source_dt), oj(function_type))
                else:
                    java_result = basicStatistics(oj(source_dt))
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialanalyst.StatisticsAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if java_result is None:
            return
        return BasicStatisticsAnalystResult._from_java_object(java_result)


def grid_common_statistics(grid_data, compare_datasets_or_value, compare_type, is_ignore_no_value, out_data=None, out_dataset_name=None, progress=None):
    """
    栅格常用统计分析，将一个栅格数据集逐行逐列按照某种比较方式与一个（或多个）栅格数据集，或一个固定值进行比较，比较结果为“真”的像元值为 1，为“假”的像元值为 0。

    关于无值的说明：

     * 当待统计源数据集的栅格有无值时，如果忽略无值，则统计结果栅格也为无值，否则使用该无值参与统计；当各比较数据集的栅格有无值时，
       如果忽略无值，则此次统计（待统计栅格与该比较数据集的计算）不计入结果，否则使用该无值进行比较。
     * 当无值不参与运算（即忽略无值）时，统计结果数据集中无值的值，由结果栅格的像素格式决定，为最大像元值，例如，结果栅格数据集像素
       格式为 PixelFormat.UBIT8，即每个像元使用 8 个比特表示，则无值的值为 255。在此方法中，结果栅格的像素格式是由比较栅格数据集
       的数量来决定的。比较数据集得个数、结果栅格的像素格式和结果栅格中无值的值三者的对应关系如下所示：

    .. image:: ../image/CommonStatistics.png

    :param grid_data:  指定的待统计的栅格数据。
    :type grid_data: DatasetGrid or str
    :param compare_datasets_or_value: 指定的比较的数据集集合或固定值。指定固定值时，固定值的单位与待统计的栅格数据集的栅格值单位相同。
    :type compare_datasets_or_value: list[DatasetGrid] or list[str] or float
    :param compare_type: 指定的比较类型
    :type compare_type: StatisticsCompareType or str
    :param is_ignore_no_value: 指定是否忽略无值。如果为 true，即忽略无值，则计算区域内的无值不参与计算，结果栅格值仍为无值；若为 false，则计算区域内的无值参与计算。
    :type is_ignore_no_value: bool
    :param out_data: 用于存储结果数据的数据源。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param out_dataset_name: 结果数据集的名称
    :type out_dataset_name: str
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 统计结果栅格数据集或数据集名称
    :rtype: DatasetGrid or str
    """
    source_dt = get_input_dataset(grid_data)
    if not isinstance(source_dt, DatasetGrid):
        raise ValueError("extracted_point required DatasetGrid, but is " + str(type(grid_data)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name + "_stats"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None and safe_start_callback_server():
                try:
                    listener = ProgressListener(progress, "grid_common_statistics")
                    get_jvm().com.supermap.analyst.spatialanalyst.SurfaceAnalyst.addSteppedListener(listener)
                except Exception as e:
                    try:
                        close_callback_server()
                        log_error(e)
                        listener = None
                    finally:
                        e = None
                        del e

            else:
                func_commonStatistics = get_jvm().com.supermap.analyst.spatialanalyst.StatisticsAnalyst.commonStatistics
                compare_value = None
                if isinstance(compare_datasets_or_value, (float, int)):
                    compare_value = float(compare_datasets_or_value)
                else:
                    if isinstance(compare_datasets_or_value, DatasetGrid):
                        compare_value = [
                         compare_datasets_or_value]
                    else:
                        if isinstance(compare_datasets_or_value, str):
                            compare_value = []
                            for t in split_input_list_from_str(compare_datasets_or_value):
                                dt = get_input_dataset(t)
                                if isinstance(dt, DatasetGrid):
                                    compare_value.append(dt)

                        else:
                            if isinstance(compare_datasets_or_value, list):
                                compare_value = []
                                for t in compare_datasets_or_value:
                                    dt = get_input_dataset(t)
                                    if isinstance(dt, DatasetGrid):
                                        compare_value.append(dt)

            if compare_value is None:
                raise ValueError("have no valid compare value or compare dataset")
            if isinstance(compare_value, float):
                java_result = func_commonStatistics(oj(source_dt), compare_value, oj(StatisticsCompareType._make(compare_type)), bool(is_ignore_no_value), oj(out_datasource), _outDatasetName)
            else:
                java_dts = to_java_datasetgrid_array(compare_value)
                java_result = func_commonStatistics(oj(source_dt), java_dts, oj(StatisticsCompareType._make(compare_type)), bool(is_ignore_no_value), oj(out_datasource), _outDatasetName)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialanalyst.StatisticsAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def grid_neighbour_statistics(grid_data, neighbour_shape, is_ignore_no_value=True, grid_stat_mode='SUM', unit_type='CELL', out_data=None, out_dataset_name=None, progress=None):
    """
    栅格邻域统计分析。

    邻域统计分析，是对输入数据集中的每个像元的指定扩展区域中的像元进行统计，将运算结果作为像元的值。统计的方法包括：总和、
    最大值、最小值、众数、少数、中位数等，请参见 GridStatisticsMode 枚举类型。目前提供的邻域范围类型（请参见 NeighbourShapeType
    枚举类型）有：矩形、圆形、圆环和扇形。

    下图为邻域统计的原理示意，假设使用“总和”作为统计方法做矩形邻域统计，邻域大小为 3×3，那么对于图中位于第二行第三列的单元格，
    它的值则由以其为中心向周围扩散得到的一个 3×3 的矩形内所有像元值的和来决定。

    .. image:: ../image/NeighbourStatistics.png

    邻域统计的应用十分广泛。例如：

    * 对表示物种种类分布的栅格计算每个邻域内的生物种类（统计方法：种类），从而观察该地区的物种丰度；
    * 对坡度栅格统计邻域内的坡度差（统计方法：值域），从而评估该区域的地形起伏状况；
    
      .. image:: ../image/NeighbourStatistics_1.png

    * 邻域统计还用于图像处理，如统计邻域内的平均值（称为均值滤波）或中位数（称为中值滤波）可以达到平滑的效果，从而去除噪声或过多的细节，等等。

      .. image:: ../image/NeighbourStatistics_2.png

    :param grid_data: 指定的待统计的栅格数据。
    :type grid_data: DatasetGrid or str
    :param neighbour_shape: 邻域形状
    :type neighbour_shape: NeighbourShape
    :param is_ignore_no_value: 指定是否忽略无值。如果为 true，即忽略无值，则计算区域内的无值不参与计算，结果栅格值仍为无值；若为 false，则计算区域内的无值参与计算。
    :type is_ignore_no_value: bool
    :param grid_stat_mode: 邻域分析的统计方法
    :type grid_stat_mode: GridStatisticsMode or str
    :param unit_type: 邻域统计的单位类型
    :type unit_type: NeighbourUnitType or str
    :param out_data: 用于存储结果数据的数据源。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param out_dataset_name: 结果数据集的名称
    :type out_dataset_name: str
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 统计结果栅格数据集或数据集名称
    :rtype: DatasetGrid or str
    """
    check_lic()
    source_dt = get_input_dataset(grid_data)
    if not isinstance(source_dt, DatasetGrid):
        raise ValueError("extracted_point required DatasetGrid, but is " + str(type(grid_data)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name + "_stats"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None and safe_start_callback_server():
                try:
                    listener = ProgressListener(progress, "grid_neighbour_statistics")
                    get_jvm().com.supermap.analyst.spatialanalyst.StatisticsAnalyst.addSteppedListener(listener)
                except Exception as e:
                    try:
                        close_callback_server()
                        log_error(e)
                        listener = None
                    finally:
                        e = None
                        del e

            else:
                neighbourStatistics = get_jvm().com.supermap.analyst.spatialanalyst.StatisticsAnalyst.neighbourStatistics
                if neighbour_shape.shape_type is NeighbourShapeType.RECTANGLE:
                    java_param = get_jvm().com.supermap.analyst.spatialanalyst.NeighbourStatisticsRectangleParameter()
                    java_param.setWidth(neighbour_shape.width)
                    java_param.setHeight(neighbour_shape.height)
                else:
                    if neighbour_shape.shape_type is NeighbourShapeType.ANNULUS:
                        java_param = get_jvm().com.supermap.analyst.spatialanalyst.NeighbourStatisticsAnnulusParameter()
                        java_param.setInnerRadius(neighbour_shape.inner_radius)
                        java_param.setOuterRadius(neighbour_shape.outer_radius)
                    else:
                        if neighbour_shape.shape_type is NeighbourShapeType.CIRCLE:
                            java_param = get_jvm().com.supermap.analyst.spatialanalyst.NeighbourStatisticsCircleParameter()
                            java_param.setRadius(neighbour_shape.radius)
                        else:
                            if neighbour_shape.shape_type is NeighbourShapeType.WEDGE:
                                java_param = get_jvm().com.supermap.analyst.spatialanalyst.NeighbourStatisticsWedgeParameter()
                                java_param.setRadius(neighbour_shape.radius)
                                java_param.setStartAngle(neighbour_shape.start_angle)
                                java_param.setEndAngle(neighbour_shape.end_angle)
                            else:
                                raise ValueError("invalid shape type")
            java_param.setIgnoreNoValue(bool(is_ignore_no_value))
            java_param.setSourceDataset(oj(source_dt))
            java_param.setStatisticsMode(oj(GridStatisticsMode._make(grid_stat_mode)))
            java_param.setTargetDatasource(oj(out_datasource))
            java_param.setTargetDatasetName(_outDatasetName)
            java_param.setUnitType(oj(NeighbourUnitType._make(unit_type)))
            java_result = neighbourStatistics(java_param)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialanalyst.StatisticsAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def altitude_statistics(point_data, grid_data, out_data=None, out_dataset_name=None):
    """
    高程统计，统计二维点数据集中每个点对应的栅格值，并生成一个三维点数据集，三维点对象的 Z 值即为被统计的栅格像素的高程值。

    :param point_data: 二维点数据集
    :type point_data: DatasetVector or str
    :param grid_data: 被统计的栅格数据集
    :type grid_data: DatasetGrid or str
    :param out_data: 用于存储结果数据的数据源。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param out_dataset_name: 结果数据集的名称
    :type out_dataset_name: str
    :return: 统计三维数据集或数据集名称
    :rtype: DatasetGrid or str
    """
    check_lic()
    source_dt = get_input_dataset(grid_data)
    if not isinstance(source_dt, DatasetGrid):
        raise ValueError("grid_data required DatasetGrid, but is " + str(type(grid_data)))
    else:
        point_dt = get_input_dataset(point_data)
        if isinstance(point_dt, DatasetVector):
            if point_dt.type is not DatasetType.POINT:
                raise ValueError("point_data required Point DatasetVector, but is " + str(type(point_data)))
            if out_data is not None:
                out_datasource = get_output_datasource(out_data)
            else:
                out_datasource = point_dt.datasource
            check_output_datasource(out_datasource)
            if out_dataset_name is None:
                _outDatasetName = source_dt.name + "_stats"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    try:
        try:
            java_result = get_jvm().com.supermap.jsuperpy.Utils.AltitudeStatistics(oj(point_dt), oj(grid_data), oj(out_datasource), _outDatasetName)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def zonal_statistics_on_raster_value(value_data, zonal_data, zonal_field, is_ignore_no_value=True, grid_stat_mode='SUM', out_data=None, out_dataset_name=None, out_table_name=None, progress=None):
    """
    栅格分带统计，方法中值数据为栅格的数据集，带数据可以是矢量或栅格数据。

    栅格分带统计，是以某种统计方法对区域内的单元格的值进行统计，将每个区域内的统计值赋给该区域所覆盖的所有单元格，从而得到结果栅格。栅格分带统计涉及两种数据，值数据和带数据。值数据即被统计的栅格数据，带数据为标识统计区域的数据，可以为栅格或矢量面数据。下图为使用栅格带数据进行分带统计的算法示意，其中灰色单元格代表无值数据。

    .. image:: ../image/ZonalStatisticsOnRasterValue_1.png

    当带数据为栅格数据集时，连续的栅格值相同的单元格作为一个带（区域）；当带数据为矢量面数据集时，要求其属性表中有一个标识带的字段，以数值来区分不同的带，如果两个及以上的面对象（可以相邻，也可以不相邻）的标识值相同，则进行分带统计时，它们将作为一个带进行统计，即在结果栅格中，这些面对象对应位置的栅格值都是这些面对象范围内的所有单元格的栅格值的统计值。

    分带统计的结果包含两部分：一是分带统计结果栅格，每个带内的栅格值相同，即按照统计方法计算所得的值；二是一个记录了每个分带内统计信息的属性表，包含 ZONALID（带的标识）、PIXELCOUNT（带内单元格数）、MININUM（最小值）、MAXIMUM（最大值）、RANGE_VALUE（值域）、SUM_VALUE（和）、MEAN（平均值）、STD（标准差）、VARIETY（种类）、MAJORITY（众数）、MINORITY（少数）、MEDIAN（中位数）等字段。

    下面通过一个实例来了解分带统计的应用。

      1. 如下图所示，左图是 DEM 栅格值，将其作为值数据，右图为对应区域的行政区划，将其作为带数据，进行分带统计；

      .. image:: ../image/ZonalStatisticsOnRasterValue_2.png

      2. 使用上面的数据，将最大值作为统计方法，进行分带统计。结果包括如下图所示的结果栅格，以及对应的统计信息属性表（略）。结果栅格中，每个带内的栅格值均相等，即在该带范围内的值栅格中最大的栅格值，也就是高程值。该例统计了该地区每个行政区内最高的高程。

      .. image:: ../image/ZonalStatisticsOnRasterValue_3.png

    注意，分带统计的结果栅格的像素类型（PixelFormat）与指定的分带统计类型（通过 ZonalStatisticsAnalystParameter 类的 setStatisticsMode 方法设置）有关：

    \u3000*\u3000当统计类型为种类（VARIETY）时，结果栅格像素类型为 BIT32；
    \u3000*\u3000当统计类型为最大值（MAX）、最小值（MIN）、值域（RANGE）时，结果栅格的像素类型与源栅格保持一致；
    \u3000*\u3000当统计类型为平均值（MEAN）、标准差（STDEV）、总和（SUM）、众数（MAJORITY）、最少数（MINORITY）、中位数（MEDIAN）时，结果栅格的像素类型为 DOUBLE。

    :param value_data: 需要被统计的值数据
    :type value_data: DatasetGrid or str
    :param zonal_data: 待统计的分带数据集。仅支持像素格式（PixelFormat）为 UBIT1、UBIT4、UBIT8 和 UBIT16 的栅格数据集或矢量面数据集。
    :type zonal_data: DatasetGrid or DatasetVector or str
    :param str zonal_field: 矢量分带数据中用于标识带的字段。字段类型只支持32位整型。
    :param bool is_ignore_no_value: 统计时是否忽略无值数据。 如果为 True，表示无值栅格不参与运算；若为 False，表示有无值参与的运算，结果仍为无值
    :param grid_stat_mode: 分带统计类型
    :type grid_stat_mode:  GridStatisticsMode or str
    :param out_data: 用于存储结果数据的数据源。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param out_dataset_name: 结果数据集的名称
    :type out_dataset_name: str
    :param out_table_name: 分析结果属性表的名称
    :type out_table_name: str
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 返回一个 tuple，tuple 有两个元素，第一个为结果数据集或名称，第二个为结果属性表数据集或名称
    :rtype: tuple[DatasetGrid, DatasetGrid] or tuple[str,str]
    """
    check_lic()
    source_dt = get_input_dataset(value_data)
    if not isinstance(source_dt, DatasetGrid):
        raise ValueError("value_data required DatasetGrid, but is " + str(type(value_data)))
    else:
        zonal_dt = get_input_dataset(zonal_data)
        if not isinstance(zonal_dt, (DatasetGrid, DatasetVector)):
            raise ValueError("zonal_data required DatasetGrid or DatasetVector, but is " + str(type(zonal_data)))
        else:
            if out_data is not None:
                out_datasource = get_output_datasource(out_data)
            else:
                out_datasource = source_dt.datasource
            check_output_datasource(out_datasource)
            if out_dataset_name is None:
                _outDatasetName = source_dt.name + "_zonal_stats"
            else:
                _outDatasetName = out_dataset_name
        _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
        if out_table_name is None:
            _outTableName = source_dt.name + "_zonal_tabular"
        else:
            _outTableName = out_table_name
    _outTableName = out_datasource.get_available_dataset_name(_outTableName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "zonal_statistics_on_raster_value")
                        get_jvm().com.supermap.analyst.spatialanalyst.StatisticsAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            zonalStatisticsOnRasterValue = get_jvm().com.supermap.analyst.spatialanalyst.StatisticsAnalyst.zonalStatisticsOnRasterValue
            java_param = get_jvm().com.supermap.analyst.spatialanalyst.ZonalStatisticsAnalystParameter()
            java_param.setIgnoreNoValue(bool(is_ignore_no_value))
            java_param.setValueDataset(oj(source_dt))
            java_param.setZonalDataset(oj(zonal_dt))
            java_param.setZonalFieldName(str(zonal_field))
            java_param.setStatisticsMode(oj(GridStatisticsMode._make(grid_stat_mode)))
            java_param.setTargetDatasource(oj(out_datasource))
            java_param.setTargetDatasetName(_outDatasetName)
            java_param.setTargetTableName(_outTableName)
            java_result = zonalStatisticsOnRasterValue(java_param)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialanalyst.StatisticsAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if java_result is None:
            if out_data is not None:
                try_close_output_datasource(None, out_datasource)
            return
        result_dt = out_datasource[_outDatasetName]
        result_table = out_datasource[_outTableName]
        if out_data is not None:
            return try_close_output_datasource((result_dt, result_table), out_datasource)
        return (result_dt, result_table)


class GridHistogram:
    __doc__ = "\n    创建给定栅格数据集的直方图。\n\n    直方图，又称柱状图，由一系列高度不等的矩形块来表示一份数据的分布情况。一般横轴表示类别，纵轴表示分布情况。\n\n    栅格直方图的横轴表示栅格值的分组，栅格值将被划分到这 N（默认为 100）个组中，即每个组对应着一个栅格值范围；纵轴表示频数，即\n    栅格值在每组的值范围内的单元格的个数。\n\n    下图是栅格直方图的示意图。该栅格数据的最小值和最大值分别为 0 和 100，取组数为 10，得出每组的频数，绘制如下的直方图。矩形块\n    上方标注了该组的频数，例如，第 6 组的栅格值范围为 [50,60)，栅格数据中值在此范围内的单元格共有 3 个，因此该组的频数为 3。\n\n    .. image:: ../image/BuildHistogram.png\n\n    注：直方图分组的最后一组的值范围为前闭后闭，其余均为前闭后开。\n\n    在通过此方法获得栅格数据集的直方图（GridHistogram）对象后，可以通过该对象的 get_frequencies 方法返回每个组的频数，还可以通过\n    get_group_count 方法重新指定栅格直方图的组数，然后再通过 get_frequencies 方法返回每组的频数。\n\n    下图为创建栅格直方图的一个实例。本例中，最小栅格值为 250，最大栅格值为 1243，组数为 500，获取各组的频数，绘制出如右侧所示的\n    栅格直方图。从右侧的栅格直方图，可以非常直观的了解栅格数据集栅格值的分布情况。\n\n    .. image:: ../image/BuildHistogram_1.png\n\n    "

    def __init__(self, source_data, group_count, function_type=None, progress=None):
        """
        构造栅格直方图对象

        :param source_data:  指定的栅格数据集
        :type source_data: DatasetGrid or str
        :param group_count:  指定的直方图的组数。必须大于 0。
        :type group_count: int
        :param function_type: FunctionType
        :type function_type: 指定的变换函数类型。
        :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
        :type progress: function
        """
        self._source_data = get_input_dataset(source_data)
        self._group_count = int(group_count)
        if function_type is not None:
            self._function_type = FunctionType._make(function_type)
        else:
            self._function_type = None
        self._progress = progress
        self._jobject = None

    def get_frequencies(self):
        """
        返回栅格直方图每个组的频数。直方图的每个组都对应了一个栅格值范围，值在这个范围内的所有单元格的个数即为该组的频数。

        :return:  返回栅格直方图每个组的频数。
        :rtype: list[int]
        """
        self._create_histogram()
        return self._jobject.getFrequencies()

    def get_group_count(self):
        """
        返回栅格直方图横轴上的组数。

        :return: 返回栅格直方图横轴上的组数。
        :rtype: int
        """
        self._create_histogram()
        return self._jobject.getGroupCount()

    def set_group_count(self, count):
        """
        设置栅格直方图横轴上的组数。

        :param int count: 栅格直方图横轴上的组数。必须大于 0。
        :rtype: self
        """
        self._jobject.setGroupCount(int(count))
        return self

    class HistogramSegmentInfo:
        __doc__ = "\n        栅格直方图每个分段区间的信息类。\n        "

        def __init__(self, count, max_value, min_value, range_max, range_min):
            self._count = count
            self._max = max_value
            self._min = min_value
            self._range_max = range_max
            self._range_min = range_min

        def __str__(self):
            s = []
            s.append("HistogramSegmentInfo:")
            s.append("count:           " + str(self.count))
            s.append("max value:       " + str(self.max))
            s.append("min value:       " + str(self.min))
            s.append("range max value: " + str(self.range_max))
            s.append("range min value: " + str(self.range_min))
            return "\n".join(s)

        @property
        def count(self):
            """int: 分段区间内容值的个数"""
            return self._count

        @property
        def max(self):
            """float: 分段区间内容值的最大值"""
            return self._max

        @property
        def min(self):
            """float: 分段区间内容值的最小值"""
            return self._min

        @property
        def range_max(self):
            """float: 分段区间的最大值"""
            return self._range_max

        @property
        def range_min(self):
            """float: 分段区间的最小值"""
            return self._range_min

    def get_segments(self):
        """
        返回栅格直方图每个组的区间信息。

        :return:  栅格直方图每个组的区间信息。
        :rtype: list[GridHistogram.HistogramSegmentInfo]
        """
        self._create_histogram()
        segments = self._jobject.getSegmentInfos()
        result = []
        for seg in segments:
            result.append(GridHistogram.HistogramSegmentInfo(seg.getCount(), seg.getMaxValue(), seg.getMinValue(), seg.getRangeMaxValue(), seg.getRangeMinValue()))

        del segments
        return result

    def _create_histogram(self):
        if self._jobject is not None:
            return self._jobject
        listener = None
        try:
            try:
                if self._progress is not None and safe_start_callback_server():
                    try:
                        listener = ProgressListener(self._progress, "GridHistogram")
                        get_jvm().com.supermap.analyst.spatialanalyst.StatisticsAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

                else:
                    createHistogram = get_jvm().com.supermap.analyst.spatialanalyst.StatisticsAnalyst.createHistogram
                    if self._function_type is not None:
                        java_result = createHistogram(oj(self._source_data), int(self._group_count), oj(self._function_type))
                    else:
                        java_result = createHistogram(oj(self._source_data), int(self._group_count))
            except:
                import traceback
                log_error(traceback.format_exc())
                java_result = None

        finally:
            if listener is not None:
                try:
                    get_jvm().com.supermap.analyst.spatialanalyst.StatisticsAnalyst.removeSteppedListener(listener)
                except Exception as e1:
                    try:
                        log_error(e1)
                    finally:
                        e1 = None
                        del e1

                close_callback_server()
            self._jobject = java_result


def thin_raster(source, back_or_no_value, back_or_no_value_tolerance, out_data=None, out_dataset_name=None, progress=None):
    """
    栅格细化，通常在将栅格转换为矢量线数据前使用。

    栅格数据细化处理可以减少栅格数据中用于标识线状地物的单元格的数量，从而提高矢量化的速度和精度。一般作为栅格转线矢量数据之
    前的预处理，使转换的效果更好。例如一幅扫描的等高线图上可能使用 5、6 个单元格来显示一条等高线的宽度，细化处理后，等高线的
    宽度就只用一个单元格来显示了，有利于更好地进行矢量化。

    .. image:: ../image/ThinRaster.png

    关于无值/背景色及其容限的说明：

    进行栅格细化时，允许用户标识那些不需要细化的单元格。对于栅格数据集，通过无值及其容限来确定这些值，对于影像数据集，则通过背景色及其容限来确定。

    * 当对栅格数据集进行细化时，栅格值为 back_or_no_value 参数指定的值的单元格被视为无值，不参与细化，而栅格的原无值将作为有效值来参与细化；
      同时，在 back_or_no_value_tolerance 参数指定的无值的容限范围内的单元格也不参与细化。例如，指定无值的值为 a，指定的无值的容限为 b，
      则栅格值在 [a-b,a+b] 范围内的单元格均不参与细化。

    * 当对影像数据集进行细化时，栅格值为指定的值的单元格被视为背景色，不参与细化；同时，在 back_or_no_value_tolerance 参数指
      定的背景色的容限范围内的单元格也不参与细化。

    需要注意，影像数据集中栅格值代表的是一个颜色值，因此，如果想要将某种颜色设为背景色，为 back_or_no_value 参数指定的值应为
    将该颜色（RGB 值）转为 32 位整型之后的值，系统内部会根据像素格式再进行相应的转换。背景色的容限同样为一个 32 位整型值。该
    值在系统内部被转为分别对应 R、G、B 的三个容限值，例如，指定为背景色的颜色为 (100,200,60)，指定的容限值为 329738，该值对应
    的 RGB 值为 (10,8,5)，则值在 (90,192,55) 和 (110,208,65) 之间的颜色均不参与细化。

    注意：对于栅格数据集，如果指定的无值的值，在待细化的栅格数据集的值域范围外，会分析失败，返回 None。

    :param source: 指定的待细化的栅格数据集。支持影像数据集。
    :type source: DatasetImage or DatasetGrid or str
    :param back_or_no_value: 指定栅格的背景色或表示无值的值。可以使用一个 int 或 tuple 来表示一个 RGB 或 RGBA 值。
    :type back_or_no_value: int or tuple
    :param back_or_no_value_tolerance: 栅格背景色的容限或无值的容限。可以使用一个 float 或 tuple 来表示一个 RGB 或 RGBA 值。
    :type back_or_no_value_tolerance: float or tuple
    :param out_data: 用于存储结果数据的数据源。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param out_dataset_name: 结果数据集的名称
    :type out_dataset_name: str
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 结果数据集或数据集名称
    :rtype: Dataset or str
    """
    check_lic()
    source_dt = get_input_dataset(source)
    if not isinstance(source_dt, (DatasetGrid, DatasetImage)):
        raise ValueError("source required DatasetGrid or DatasetImage, but is " + str(type(source)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name + "_thin_raster"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    if back_or_no_value is not None:
        if isinstance(back_or_no_value, tuple):
            back_or_no_value = tuple_to_color(back_or_no_value)
    if back_or_no_value_tolerance is not None:
        if isinstance(back_or_no_value_tolerance, tuple):
            back_or_no_value_tolerance = tuple_to_color(back_or_no_value_tolerance)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "thin_raster")
                        get_jvm().com.supermap.analyst.spatialanalyst.ConversionAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            thinRaster = get_jvm().com.supermap.analyst.spatialanalyst.ConversionAnalyst.thinRaster
            java_result = thinRaster(oj(source_dt), int(back_or_no_value), float(back_or_no_value_tolerance), oj(out_datasource), _outDatasetName)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialanalyst.ConversionAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def thin_raster_bit(input_data, back_or_no_value, is_save_as_grid=True, out_data=None, out_dataset_name=None, progress=None):
    """
    通过减少要素宽度的像元来对栅格化的线状要素进行细化，该方法是处理二值图像的细化方法，如果不是二值图像会先处理为二值图像，只需指定背景色的值，背景色以外的值都是需要细化的值。该方法的效率最快。

    :param input_data: 指定的待细化的栅格数据集。支持影像数据集。
    :type input_data: DatasetImage or DatasetGrid or str
    :param back_or_no_value: 指定栅格的背景色或表示无值的值。可以使用一个 int 或 tuple 来表示一个 RGB 或 RGBA 值。
    :type back_or_no_value: int or tuple
    :param bool is_save_as_grid: 是否保存为栅格数据集，Ture 表示保存为栅格数据集，False保存为原数据类型（栅格或影像）。保存为栅格数据集便于栅格矢量化时指定值矢量化，方便快速获取线数据。
    :param out_data: 用于存储结果数据的数据源。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param out_dataset_name: 结果数据集的名称
    :type out_dataset_name: str
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 结果数据集或数据集名称
    :rtype: Dataset or str
    """
    source_dt = get_input_dataset(input_data)
    if not isinstance(source_dt, (DatasetGrid, DatasetImage)):
        raise ValueError("source required DatasetGrid or DatasetImage, but is " + str(type(input_data)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name + "_thin_raster"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    if back_or_no_value is not None:
        if isinstance(back_or_no_value, tuple):
            back_or_no_value = tuple_to_color(back_or_no_value)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "thin_raster_bit")
                        get_jvm().com.supermap.analyst.spatialanalyst.ConversionAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            thinRaster = get_jvm().com.supermap.analyst.spatialanalyst.ConversionAnalyst.thinRaster
            java_result = thinRaster(oj(source_dt), oj(out_datasource), _outDatasetName, int(back_or_no_value), parse_bool(is_save_as_grid))
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialanalyst.ConversionAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def build_lake(dem_grid, lake_data, elevation, progress=None):
    """
    挖湖，即修改面数据集区域范围内的 DEM 数据集的高程值为指定的数值。
    挖湖是指根据已有的湖泊面数据，在 DEM 数据集上显示湖泊信息。如下图所示，挖湖之后，DEM 在湖泊面数据对应位置的栅格值变成指定的高程值，且整个湖泊区域栅格值相同。

    .. image:: ../image/BuildLake.png

    :param dem_grid:  指定的待挖湖的 DEM 栅格数据集。
    :type dem_grid: DatasetGrid or str
    :param lake_data:  指定的湖区域，为面数据集。
    :type lake_data: DatasetVector or str
    :param elevation: 指定的湖区域的高程字段或指定的高程值。如果为 str，则要求字段类型为数值型。如果指定为 None 或空字符串，或湖区域数据集中不存在指定的
                      字段，则按照湖区域边界对应 DEM 栅格上的最小高程进行挖湖。高程值的单位与 DEM 栅格数据集的栅格值单位相同。
    :type elevation: str or float
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 成功返回 True，否则返回 False
    :rtype: bool
    """
    check_lic()
    source_dt = get_input_dataset(dem_grid)
    if not isinstance(source_dt, DatasetGrid):
        raise ValueError("dem_grid required DatasetGrid, but is " + str(type(dem_grid)))
    lake_dt = get_input_dataset(lake_data)
    if not isinstance(lake_dt, DatasetVector):
        raise ValueError("lake_data required DatasetVector, but is " + str(type(lake_dt)))
    listener = None
    try:
        try:
            if progress is not None and safe_start_callback_server():
                try:
                    listener = ProgressListener(progress, "build_lake")
                    get_jvm().com.supermap.analyst.spatialanalyst.TerrainBuilder.addSteppedListener(listener)
                except Exception as e:
                    try:
                        close_callback_server()
                        log_error(e)
                        listener = None
                    finally:
                        e = None
                        del e

            else:
                buildLake = get_jvm().com.supermap.analyst.spatialanalyst.TerrainBuilder.buildLake
                if isinstance(elevation, (float, int)):
                    elevation = float(elevation)
                else:
                    elevation = str(elevation)
            java_result = buildLake(oj(source_dt), oj(lake_dt), elevation)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = False

    finally:
        return

    if listener is not None:
        try:
            get_jvm().com.supermap.analyst.spatialanalyst.TerrainBuilder.removeSteppedListener(listener)
        except Exception as e1:
            try:
                log_error(e1)
            finally:
                e1 = None
                del e1

        close_callback_server()
    return java_result


def build_terrain(source_datas, lake_dataset=None, lake_altitude_field=None, clip_data=None, erase_data=None, interpolate_type='IDW', resample_len=0.0, z_factor=1.0, is_process_flat_area=False, encode_type='NONE', pixel_format='SINGLE', cell_size=0.0, out_data=None, out_dataset_name=None, progress=None):
    """
    根据指定的地形构建参数信息创建地形。
    DEM（Digital Elevation Model，数字高程模型）主要用于描述区域地貌形态的空间分布，是地面特性为高程和海拔高程的数字地面模型（DTM），
    通常通过高程测量点（或从等高线中进行采样提取高程点）进行数据内插而成。此方法用于构建地形，即对具有高程信息的点或线数据集通过插值生成 DEM 栅格。

    .. image:: ../image/BuildTerrain_1.png

    可以通过 source_datas 参数指定用于构建地形的数据集，支持仅高程点、仅等高线以及支持高程点和等高线共同构建。

    :param source_datas: 用于构建的点数据集和线数据集，以及数据集的高程字段。要求数据集的坐标系相同。
    :type source_datas: dict[DatasetVector,str] or dict[str,str]
    :param lake_dataset:  湖泊面数据集。在结果数据集中，湖泊面数据集区域范围内的高程值小于周边相邻的高程值。
    :type lake_dataset: DatasetVector or str
    :param str lake_altitude_field: 湖泊面数据集的高程字段
    :param clip_data: 设置用于裁剪的数据集。构建地形时，仅位于裁剪区域内的 DEM 结果被保留，区域外的部分被赋予无值。

                      .. image:: ../image/BuildTerrainParameter_1.png

    :type clip_data: DatasetVector or str
    :param erase_data: 用于擦除的数据集。构建地形时，位于擦除区域内的结果 DEM 栅格值为无值。仅在 interpolate_type 设置为 TIN 时有效。

                       .. image:: ../image/BuildTerrainParameter_2.png

    :type erase_data: DatasetVector or str
    :param interpolate_type: 地形插值类型。默认值为 IDW。
    :type interpolate_type: TerrainInterpolateType  or str
    :param float resample_len: 采样距离。只对线数据集有效。单位与用于构建地形的线数据集单位一致。仅在 interpolate_type 设置为TIN时有效。
                         首先对线数据集进行重采样过滤掉一些比较密集的节点，然后再生成 TIN 模型，提高生成速度。
    :param float z_factor: 高程缩放系数
    :param bool is_process_flat_area: 是否处理平坦区域。等值线生成DEM能较好地处理山顶山谷，点生成DEM也可以处理平坦区域，但效
                                      果没有等值线生成DEM处理的好，主要原因是根据点判断平坦区域结果较为粗糙。
    :param encode_type: 编码方式。对于栅格数据集，目前支持的编码方式有未编码、SGL、LZW 三种方式
    :type encode_type: EncodeType or str
    :param pixel_format: 结果数据集的像素格式
    :type pixel_format: PixelFormat or str
    :param float cell_size: 结果数据集的栅格单元的大小，如果指定为 0 或负数，则系统会使用 L/500（L 是指源数据集的区域范围对应的矩形的对角线长度）作为单元格大小。
    :param out_data: 用于存储结果数据的数据源。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param out_dataset_name: 结果数据集的名称
    :type out_dataset_name: str
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 结果数据集或数据集名称
    :rtype: Dataset or str
    """
    check_lic()
    point_datasets = []
    point_altitude_fields = []
    line_datasets = []
    line_altitude_fields = []
    if isinstance(source_datas, dict):
        for dt, field in source_datas.items():
            dt = get_input_dataset(dt)
            if isinstance(dt, DatasetVector) and dt.index_of_field(field) != -1:
                if dt.type is DatasetType.POINT:
                    point_datasets.append(dt)
                    point_altitude_fields.append(field)
                elif dt.type is DatasetType.LINE:
                    line_datasets.append(dt)
                    line_altitude_fields.append(field)

    if len(point_datasets) + len(line_datasets) == 0:
        raise ValueError("have no valid source  datasets")
    elif lake_dataset is not None:
        if lake_altitude_field is not None:
            lake_dataset = get_input_dataset(lake_dataset)
            lake_altitude_field = str(lake_altitude_field)
        else:
            lake_dataset = None
            lake_altitude_field = None
        clip_data = get_input_dataset(clip_data)
        if clip_data is not None:
            java_clip_data = oj(clip_data)
        else:
            java_clip_data = None
        erase_data = get_input_dataset(erase_data)
        if erase_data is not None:
            java_erase_data = oj(erase_data)
        else:
            java_erase_data = None
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            if len(point_datasets) > 0:
                out_datasource = point_datasets[0].datasource
            else:
                out_datasource = line_datasets[0].datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            if len(point_datasets) > 0:
                _outDatasetName = point_datasets[0].name + "_terrain"
        else:
            _outDatasetName = line_datasets[0].name + "_terrain"
    else:
        _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "build_terrain")
                        get_jvm().com.supermap.analyst.spatialanalyst.TerrainBuilder.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_param = get_jvm().com.supermap.analyst.spatialanalyst.TerrainBuilderParameter()
            if len(point_datasets) > 0:
                java_param.setPointDatasets(to_java_datasetvector_array(point_datasets))
                java_param.setPointAltitudeFileds(to_java_string_array(point_altitude_fields))
            else:
                java_param.setLineDatasets(to_java_datasetvector_array(line_datasets))
                java_param.setLineAltitudeFileds(to_java_string_array(line_altitude_fields))
            if lake_dataset is not None:
                java_param.setLakeDataset(oj(lake_dataset))
                java_param.setLakeAltitudeFiled(lake_altitude_field)
            if cell_size is not None:
                java_param.setCellSize(float(cell_size))
            if java_clip_data is not None:
                java_param.setClipDataset(java_clip_data)
            if encode_type is not None:
                java_param.setEncodeType(oj(EncodeType._make(encode_type)))
            if java_erase_data is not None:
                java_param.setEraseDataset(java_erase_data)
            if interpolate_type is not None:
                java_param.setInterpolateType(oj(TerrainInterpolateType._make(interpolate_type)))
            if pixel_format is not None:
                java_param.setPixelFormat(oj(PixelFormat._make(pixel_format)))
            if is_process_flat_area is not None:
                java_param.setProcessFlatArea(parse_bool(is_process_flat_area))
            if resample_len is not None:
                java_param.setResampleLen(float(resample_len))
            if z_factor is not None:
                java_param.setZFactor(float(z_factor))
            java_result = get_jvm().com.supermap.analyst.spatialanalyst.TerrainBuilder.buildTerrain(java_param, oj(out_datasource), _outDatasetName)
            del java_param
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialanalyst.TerrainBuilder.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def area_solar_radiation_days(grid_data, latitude, start_day, end_day=160, hour_start=0, hour_end=24, day_interval=5, hour_interval=0.5, transmittance=0.5, z_factor=1.0, out_data=None, out_total_grid_name='TotalGrid', out_direct_grid_name=None, out_diffuse_grid_name=None, out_duration_grid_name=None, progress=None):
    """
    计算多天的区域太阳辐射总量，即整个DEM范围内每个栅格的太阳辐射情况。需要指定每天的开始时点、结束时点和开始日期、结束日期。

    :param grid_data: 待计算太阳辐射的DEM栅格数据
    :type grid_data: DatasetGrid or str
    :param latitude: 待计算区域的平均纬度
    :type latitude: float
    :param start_day: 起始日期，可以是 "%Y-%m-%d" 格式的字符串，如果为 int，则表示一年中的第几天
    :type start_day: datetime.date or str or int
    :param end_day: 终止日期，可以是 "%Y-%m-%d" 格式的字符串，如果为 int，则表示一年中的第几天
    :type end_day: datetime.date or str or int
    :param hour_start: 起始时点，如果输入float 时，可以输入一个 [0,24]范围内的数值，表示一天中的第几个小时。也可以输入一个 datetime.datatime 或 "%H:%M:%S" 格式的字符串
    :type hour_start: float or str or datetime.datetime
    :param hour_end: 终止时点，如果输入float 时，可以输入一个 [0,24]范围内的数值，表示一天中的第几个小时。也可以输入一个 datetime.datatime 或 "%H:%M:%S" 格式的字符串
    :type hour_end:  float or str or datetime.datetime
    :param int day_interval: 天数间隔，单位为天
    :param float hour_interval: 小时间隔，单位为小时。
    :param float transmittance: 太阳辐射穿过大气的透射率，值域为[0,1]。
    :param float z_factor: 高程缩放系数
    :param out_data: 用于存储结果数据的数据源。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_total_grid_name: 总辐射量结果数据集名称，数据集名称必须合法
    :param str out_direct_grid_name: 直射辐射量结果数据集名称，数据集名称必须合法，且接口内不会自动获取有效的数据集名称
    :param str out_diffuse_grid_name: 散射辐射量结果数据集名称，数据集名称必须合法，且接口内不会自动获取有效的数据集名称
    :param str out_duration_grid_name: 太阳直射持续时间结果数据集名称，数据集名称必须合法，且接口内不会自动获取有效的数据集名称
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 返回一个四个元素的 tuple：

               * 第一个为总辐射量结果数据集，
               * 如果设置了直射辐射量结果数据集名称，第二个为直射辐射量结果数据集，否则为 None，
               * 如果设置散射辐射量结果数据集的名称，第三个为散射辐射量结果数据集，否则为 None
               * 如果设置太阳直射持续时间结果数据集的名称，第四个为太阳直射持续时间结果数据集，否则为 None

    :rtype: tuple[DatasetGrid] or tuple[str]
    """
    source_dt = get_input_dataset(grid_data)
    if not isinstance(source_dt, DatasetGrid):
        raise ValueError("grid_data required DatasetGrid, but is " + str(type(grid_data)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_total_grid_name is None:
            _out_total_grid_name = source_dt.name + "_solar"
        else:
            _out_total_grid_name = out_total_grid_name
    _out_total_grid_name = out_datasource.get_available_dataset_name(_out_total_grid_name)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "area_solar_radiation_days")
                        get_jvm().com.supermap.analyst.spatialanalyst.SolarRadiation.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_param = get_jvm().com.supermap.analyst.spatialanalyst.SolarRadiationParameter()
            n_start_day = 0
            if start_day is not None:
                if isinstance(start_day, int):
                    n_start_day = start_day
                else:
                    start_day = get_struct_time(start_day)
                    if start_day is not None:
                        n_start_day = start_day.tm_yday
                    n_end_day = 0
                if end_day is not None:
                    if isinstance(end_day, int):
                        n_end_day = end_day
            else:
                end_day = get_struct_time(end_day)
            if end_day is not None:
                n_end_day = end_day.tm_yday
            java_param.setTimeMode(get_jvm().com.supermap.analyst.spatialanalyst.SolarTimeMode.MULTIDAYS)
            java_param.setDayStart(n_start_day)
            java_param.setDayEnd(n_end_day)
            if hour_start is not None:
                java_param.setHourStart(get_day_hour(hour_start))
            if hour_end is not None:
                java_param.setHourEnd(get_day_hour(hour_end))
            java_param.setLatitude(float(latitude))
            java_param.setTransmittance(float(transmittance))
            if z_factor is not None:
                java_param.setZFactor(float(z_factor))
            java_param.setDayInterval(int(day_interval))
            java_param.setHourInterval(float(hour_interval))
            areaSolarRadiation = get_jvm().com.supermap.analyst.spatialanalyst.SolarRadiation.areaSolarRadiation
            java_result = areaSolarRadiationoj(source_dt)java_paramoj(out_datasource)_out_total_grid_nameout_direct_grid_nameout_diffuse_grid_nameout_duration_grid_name
            del java_param
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialanalyst.SolarRadiation.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is None:
            if out_data is not None:
                try_close_output_datasource(None, out_datasource)
            else:
                return
                total_grid_dt = out_datasource[_out_total_grid_name]
                if out_direct_grid_name is not None:
                    direct_grid_dt = out_datasource[out_direct_grid_name]
                else:
                    direct_grid_dt = None
                if out_diffuse_grid_name is not None:
                    diffuse_grid_dt = out_datasource[out_diffuse_grid_name]
                else:
                    diffuse_grid_dt = None
            if out_duration_grid_name is not None:
                duration_grid_dt = out_datasource[out_duration_grid_name]
        else:
            duration_grid_dt = None
        if out_data is not None:
            return try_close_output_datasource((total_grid_dt, direct_grid_dt, diffuse_grid_dt, duration_grid_dt), out_datasource)
        return (
         total_grid_dt, direct_grid_dt, diffuse_grid_dt, duration_grid_dt)


def area_solar_radiation_hours(grid_data, latitude, day, hour_start=0, hour_end=24, hour_interval=0.5, transmittance=0.5, z_factor=1.0, out_data=None, out_total_grid_name='TotalGrid', out_direct_grid_name=None, out_diffuse_grid_name=None, out_duration_grid_name=None, progress=None):
    """
    计算一天内的太阳辐射，需要指定开始时点、结束时点及开始日期作为要计算的日期

    :param grid_data: 待计算太阳辐射的DEM栅格数据
    :type grid_data: DatasetGrid or str
    :param latitude: 待计算区域的平均纬度
    :type latitude: float
    :param day: 待计算的指定日期。可以是 "%Y-%m-%d" 格式的字符串，如果为 int，则表示一年中的第几天。
    :type day:  datetime.date or str or int
    :param hour_start: 起始时点，如果输入float 时，可以输入一个 [0,24]范围内的数值，表示一天中的第几个小时。也可以输入一个 datetime.datatime 或 "%H:%M:%S" 格式的字符串
    :type hour_start: float or str or datetime.datetime
    :param hour_end: 终止时点，如果输入float 时，可以输入一个 [0,24]范围内的数值，表示一天中的第几个小时。也可以输入一个 datetime.datatime 或 "%H:%M:%S" 格式的字符串
    :type hour_end:  float or str or datetime.datetime
    :param float hour_interval: 小时间隔，单位为小时。
    :param float transmittance: 太阳辐射穿过大气的透射率，值域为[0,1]。
    :param float z_factor: 高程缩放系数
    :param out_data: 用于存储结果数据的数据源。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_total_grid_name: 总辐射量结果数据集名称，数据集名称必须合法
    :param str out_direct_grid_name: 直射辐射量结果数据集名称，数据集名称必须合法，且接口内不会自动获取有效的数据集名称
    :param str out_diffuse_grid_name: 散射辐射量结果数据集名称，数据集名称必须合法，且接口内不会自动获取有效的数据集名称
    :param str out_duration_grid_name: 太阳直射持续时间结果数据集名称，数据集名称必须合法，且接口内不会自动获取有效的数据集名称
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 返回一个四个元素的 tuple：

               * 第一个为总辐射量结果数据集，
               * 如果设置了直射辐射量结果数据集名称，第二个为直射辐射量结果数据集，否则为 None，
               * 如果设置散射辐射量结果数据集的名称，第三个为散射辐射量结果数据集，否则为 None
               * 如果设置太阳直射持续时间结果数据集的名称，第四个为太阳直射持续时间结果数据集，否则为 None

    :rtype: tuple[DatasetGrid] or tuple[str]
    """
    check_lic()
    source_dt = get_input_dataset(grid_data)
    if not isinstance(source_dt, DatasetGrid):
        raise ValueError("grid_data required DatasetGrid, but is " + str(type(grid_data)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_total_grid_name is None:
            _out_total_grid_name = source_dt.name + "_solar"
        else:
            _out_total_grid_name = out_total_grid_name
    _out_total_grid_name = out_datasource.get_available_dataset_name(_out_total_grid_name)
    listener = None
    try:
        try:
            if progress is not None and safe_start_callback_server():
                try:
                    listener = ProgressListener(progress, "area_solar_radiation_hours")
                    get_jvm().com.supermap.analyst.spatialanalyst.SolarRadiation.addSteppedListener(listener)
                except Exception as e:
                    try:
                        close_callback_server()
                        log_error(e)
                        listener = None
                    finally:
                        e = None
                        del e

                java_param = get_jvm().com.supermap.analyst.spatialanalyst.SolarRadiationParameter()
                n_start_day = 0
                if day is not None:
                    if isinstance(day, int):
                        n_start_day = day
            else:
                start_day = get_struct_time(day)
            if start_day is not None:
                n_start_day = start_day.tm_yday
            java_param.setTimeMode(get_jvm().com.supermap.analyst.spatialanalyst.SolarTimeMode.WITHINDAY)
            java_param.setDayStart(n_start_day)
            if hour_start is not None:
                java_param.setHourStart(get_day_hour(hour_start))
            if hour_end is not None:
                java_param.setHourEnd(get_day_hour(hour_end))
            java_param.setLatitude(float(latitude))
            java_param.setTransmittance(float(transmittance))
            if z_factor is not None:
                java_param.setZFactor(float(z_factor))
            java_param.setHourInterval(float(hour_interval))
            areaSolarRadiation = get_jvm().com.supermap.analyst.spatialanalyst.SolarRadiation.areaSolarRadiation
            java_result = areaSolarRadiationoj(source_dt)java_paramoj(out_datasource)_out_total_grid_nameout_direct_grid_nameout_diffuse_grid_nameout_duration_grid_name
            del java_param
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialanalyst.TerrainBuilder.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is None:
            if out_data is not None:
                try_close_output_datasource(None, out_datasource)
            else:
                return
                total_grid_dt = out_datasource[_out_total_grid_name]
                if out_direct_grid_name is not None:
                    direct_grid_dt = out_datasource[out_direct_grid_name]
                else:
                    direct_grid_dt = None
                if out_diffuse_grid_name is not None:
                    diffuse_grid_dt = out_datasource[out_diffuse_grid_name]
                else:
                    diffuse_grid_dt = None
            if out_duration_grid_name is not None:
                duration_grid_dt = out_datasource[out_duration_grid_name]
        else:
            duration_grid_dt = None
        if out_data is not None:
            return try_close_output_datasource((total_grid_dt, direct_grid_dt, diffuse_grid_dt, duration_grid_dt), out_datasource)
        return (
         total_grid_dt, direct_grid_dt, diffuse_grid_dt, duration_grid_dt)


def raster_mosaic(inputs, back_or_no_value, back_tolerance, join_method, join_pixel_format, cell_size, encode_type='NONE', valid_rect=None, out_data=None, out_dataset_name=None, progress=None):
    """
    栅格数据集镶嵌。支持栅格数据集和影像数据集。

    栅格数据的镶嵌是指将两个或两个以上栅格数据按照地理坐标组成一个栅格数据。有时由于待研究分析的区域很大，或者感兴趣的目标对象
    分布很广，涉及到多个栅格数据集或者多幅影像，就需要进行镶嵌。下图展示了六幅相邻的栅格数据镶嵌为一幅数据。

    .. image:: ../image/Mosaic_1.png

    进行栅格数据镶嵌时，需要注意以下要点：

     * 待镶嵌栅格必须具有相同的坐标系
       镶嵌要求所有栅格数据集或影像数据集具有相同的坐标系，否则镶嵌结果可能出错。可以在镶嵌前通过投影转换统一所有带镶嵌栅格的
       坐标系。

     * 重叠区域的处理
       镶嵌时，经常会出现两幅或多幅栅格数据之间有重叠区域的情况（如下图，两幅影像在红色框内的区域是重叠的），此时需要指定对重
       叠区域栅格的取值方式。SuperMap 提供了五种重叠区域取值方式，使用者可根据实际需求选择适当的方式，详见 :py:class:`.RasterJoinType` 类。

       .. image:: ../image/Mosaic_2.png

     * 关于无值和背景色及其容限的说明
       待镶嵌的栅格数据有两种：栅格数据集和影像数据集。对于栅格数据集，该方法可以指定无值及无值的容限，对于影像数据集，该方法
       可以指定背景色及其容限。

       * 待镶嵌数据为栅格数据集:

          * 当待镶嵌的数据为栅格数据集时，栅格值为 back_or_no_value 参数所指定的值的单元格，以及在 back_tolerance 参数指定的容限范
            围内的单元格被视为无值，这些单元格不会参与镶嵌时的计算（叠加区域的计算），而栅格的原无值单元格则不再是无值数据从而参与运算。

          * 需要注意，无值的容限是用户指定的无值的值的容限，与栅格中原无值无关。

       * 待镶嵌数据为影像数据集

          * 当待镶嵌的数据为影像数据集时，栅格值为 back_or_no_value 参数所指定的值的单元格，以及在 back_tolerance 参数指定的容限
            范围内单元格被视为背景色，这些单元格不参与镶嵌时的计算。例如，指定无值的值为 a，指定的无值的容限为 b，则栅格值在
            [a-b,a+b] 范围内的单元格均不参与计算。

          * 注意，影像数据集中栅格值代表的是一个颜色。影像数据集的栅格值对应为 RGB 颜色，因此，如果想要将某种颜色设为背景色，
            为 back_or_no_value 参数指定的值应为将该颜色（RGB 值）转为 32 位整型之后的值，系统内部会根据像素格式再进行相应的转换。

          * 对于背景色的容限值的设置，与背景色的值的指定方式相同：该容限值为一个 32 位整型值，在系统内部被转换为对应背景色
            R、G、B 的三个容限值，例如，指定为背景色的颜色为 (100,200,60)，指定的容限值为 329738，该值对应的 RGB 值为
            (10,8,5)，则值在 (90,192,55) 和 (110,208,65) 之间的颜色均被视为背景色，不参与计算。

    注意：

    将两个或以上高像素格式的栅格镶嵌成低像素格式的栅格时，结果栅格值可能超出值域，导致错误，因此不建议进行此种操作。

    :param inputs: 指定的待镶嵌的数据集的集合。
    :type inputs: list[DatasetGrid] or list[DatasetImage] list[str] or str
    :param back_or_no_value: 指定的栅格背景颜色或无值的值。可以使用一个 float 或 tuple 表示一个 RGB 或 RGBA 值
    :type back_or_no_value: float or tuple
    :param back_tolerance: 指定的栅格背景颜色或无值的容限。可以使用一个 float 或 tuple 表示一个 RGB 或 RGBA 值
    :type back_tolerance: float or tuple
    :param join_method: 指定的镶嵌方法，即镶嵌时重叠区域的取值方式。
    :type join_method: RasterJoinType or str
    :param join_pixel_format: 指定的镶嵌结果栅格数据的像素格式。
    :type join_pixel_format: RasterJoinPixelFormat or str
    :param float cell_size: 指定的镶嵌结果数据集的单元格大小。
    :param encode_type: 指定的镶嵌结果数据集的编码方式。
    :type encode_type: EncodeType or str
    :param valid_rect: 指定的镶嵌结果数据集的有效范围。
    :type valid_rect: Rectangle
    :param out_data: 指定的用于存储镶嵌结果数据集的数据源信息
    :type out_data:  Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 指定的镶嵌结果数据集的名称。
    :param progress: 进度信息，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 镶嵌结果数据集
    :rtype: Dataset
    """
    check_lic()
    datasets = []
    if isinstance(inputs, (list, tuple)):
        for i in range(len(inputs)):
            item = inputs[i]
            temp = get_input_dataset(item)
            if temp is not None:
                if isinstance(temp, (DatasetGrid, DatasetImage)):
                    datasets.append(temp)
                else:
                    raise ValueError("Only support DatasetGrid or DatasetImage")
            else:
                raise ValueError("input_data item is None" + str(item))

    else:
        temp = get_input_dataset(inputs)
        if temp is not None:
            if isinstance(temp, (DatasetGrid, DatasetImage)):
                datasets.append(temp)
            else:
                raise ValueError("Only support DatasetGrid or DatasetImage")
        else:
            raise ValueError("input_data item is None" + str(inputs))
    if len(datasets) == 0:
        raise ValueError("hava no valid source datasets")
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = datasets[0].datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = datasets[0].name + "_mosaic"
        else:
            _outDatasetName = out_dataset_name
        _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
        if join_method is not None:
            java_join_method = oj(RasterJoinType._make(join_method))
        else:
            java_join_method = oj(RasterJoinType.RJMFIRST)
        if join_pixel_format is not None:
            java_join_pixel_format = oj(RasterJoinPixelFormat._make(join_pixel_format))
        else:
            java_join_pixel_format = oj(RasterJoinPixelFormat.RJPMAX)
        if encode_type is not None:
            java_encode_type = oj(EncodeType._make(encode_type))
        else:
            java_encode_type = oj(EncodeType.NONE)
        if valid_rect is None:
            valid_rect = Rectangle.make((0, 0, 0, 0))
        elif back_or_no_value is not None:
            if isinstance(back_or_no_value, tuple):
                back_or_no_value = tuple_to_color(back_or_no_value)
            else:
                back_or_no_value = -9999
            if back_tolerance is not None:
                if isinstance(back_tolerance, tuple):
                    back_tolerance = tuple_to_color(back_tolerance)
        else:
            back_tolerance = 0.0
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "raster_mosaic")
                        get_jvm().com.supermap.analyst.spatialanalyst.RasterMosaic.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_result = get_jvm().com.supermap.analyst.spatialanalyst.RasterMosaic.mosaic(to_java_dataset_array(datasets), float(back_or_no_value), float(back_tolerance), java_join_method, java_join_pixel_format, float(cell_size), java_encode_type, oj(valid_rect), oj(out_datasource), _outDatasetName)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialanalyst.RasterMosaic.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[java_result.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def NDVI(input_data, nir_index, red_index, out_data=None, out_dataset_name=None):
    """
    归一化植被指数，也叫做归一化差分植被指数或者标准差异植被指数或生物量指标变化。可使植被从水和土中分离出来。

    :param input_data: 多波段影像数据集。
    :type input_data: DatasetImage or str
    :param int nir_index: 近红外波段的索引
    :param int red_index: 红波段的索引
    :param out_data: 结果数据源
    :type out_data: Datasource or str
    :param str out_dataset_name: 结果数据集名称
    :return: 结果数据集，用于保存NDVI值。NDVI值的范围在-1到1之间。
    :rtype: DatasetGrid or str
    """
    check_lic()
    source_dt = get_input_dataset(input_data)
    if not isinstance(source_dt, DatasetImage):
        raise ValueError("source required DatasetImage, but is " + str(type(input_data)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name + "_NDVI"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    try:
        try:
            NDVI = get_jvm().com.supermap.analyst.spatialanalyst.ImageAnalyst.NDVI
            java_result = NDVI(oj(source_dt), int(nir_index), int(red_index), _outDatasetName, oj(out_datasource))
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if java_result is not None:
            result_dt = out_datasource[java_result.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def NDWI(input_data, nir_index, green_index, out_data=None, out_dataset_name=None):
    """
    归一化水指数。NDWI一般用来提取影像中的水体信息，效果较好.

    :param input_data: 多波段影像数据集。
    :type input_data: DatasetImage or str
    :param int nir_index: 近红外波段的索引
    :param int green_index: 绿波段的索引
    :param out_data: 结果数据源
    :type out_data: Datasource or str
    :param str out_dataset_name: 结果数据集名称
    :return: 结果数据集，用于保存NDWI值。
    :rtype: DatasetGrid or str
    """
    check_lic()
    source_dt = get_input_dataset(input_data)
    if not isinstance(source_dt, DatasetImage):
        raise ValueError("source required DatasetImage, but is " + str(type(input_data)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name + "_NDWI"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    try:
        try:
            NDWI = get_jvm().com.supermap.analyst.spatialanalyst.ImageAnalyst.NDWI
            java_result = NDWI(oj(source_dt), int(nir_index), int(green_index), _outDatasetName, oj(out_datasource))
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if java_result is not None:
            result_dt = out_datasource[java_result.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def compute_features_envelope(input_data, is_single_part=True, out_data=None, out_dataset_name=None, progress=None):
    """
    计算几何对象的矩形范围面

    :param input_data: 待分析的数据集，仅支持线数据集和面数据集。
    :type input_data: DatasetVector or str
    :param bool is_single_part: 有组合线或者组合面时，是否拆分子对象。默认为 True，拆分子对象。
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or str
    :param str out_dataset_name: 结果数据集名称
    :param progress: 进度信息，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 结果数据集，返回每个对象的范围面。结果数据集中新增了字段"ORIG_FID"用于保存输入对象的ID值。
    :rtype: DatasetVector or str
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    else:
        if not isinstance(_source_input, DatasetVector):
            raise ValueError("source input_data must be DatasetVector")
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = _source_input.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + "_envelope"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, "compute_features_envelope")
                _jvm.com.supermap.analyst.spatialanalyst.Generalization.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            java_result = _jvm.com.supermap.analyst.spatialanalyst.Generalization.featureEnvelope(oj(_source_input), _outDatasetName, oj(out_datasource), bool(is_single_part))
        except Exception:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.Generalization.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[java_result.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def calculate_view_shed(input_data, view_point, start_angle, view_angle, view_radius, out_data=None, out_dataset_name=None, progress=None):
    """
    单点可视域分析，即分析单个观察点的可视范围。
    单点可视域分析是在栅格表面数据集上，对于给定的一个观察点，查找其在给定的范围内（由观察半径、观察角度决定）所能观察到的区域，也就是给定点的通视区域范围。分析的结果为一个栅格数据集，其中可视区域保持原始栅格表面的栅格值，其他区域为无值。

    如下图所示，图中绿色的点为观察点，叠加在原始栅格表面上的蓝色区域即为对其进行可视域分析的结果。

    .. image:: ../image/CalculateViewShed.png

    注意：如果指定的观察点的高程小于当前栅格表面对应位置的高程值，则观察点的高程值将被自动设置为当前栅格表面的对应位置的高程。

    :param input_data: 指定的用于可视域分析的栅格表面数据集。
    :type input_data: DatasetGrid or str
    :param Point3D view_point: 指定的观察点位置。
    :param float start_angle: 指定的起始观察角度，单位为度，以正北方向为 0 度，顺时针方向旋转。指定为负值或大于 360 度，将自动换算到 0 到 360 度范围内。
    :param float view_angle:  指定的观察角度，单位为度，最大值为 360 度。观察角度基于起始角度，即观察角度范围为 [起始角度，起始角度+观察角度]。例如起始角度为 90 度，观察角度为 90 度，那么实际观察的角度范围是从 90 度到 180 度。但注意，当指定为 0 或负值时，无论起始角度为何值，观察角度范围都为 0 到 360 度
    :param float view_radius: 指定的观察半径。该值限制了视野范围的大小，若观测半径小于等于 0 时，表示无限制。单位为米
    :param out_data: 指定的用于存储结果数据集的数据源
    :type out_data: Datasource or str
    :param str out_dataset_name: 指定的结果数据集的名称
    :param progress: 进度信息，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 单点可视域分析结果数据集
    :rtype: DatasetGrid or str
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    if not isinstance(_source_input, DatasetGrid):
        raise ValueError("source input_data must be DatasetGrid")
    else:
        view_point = Point3D.make(view_point)
        if not isinstance(view_point, Point3D):
            raise ValueError("view_point must be Point3D")
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = _source_input.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + "_ViewShed"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, "calculate_view_shed")
                _jvm.com.supermap.analyst.spatialanalyst.VisibilityAnalyst.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            java_result = _jvm.com.supermap.analyst.spatialanalyst.VisibilityAnalyst.calculateViewShed(oj(_source_input), oj(view_point), float(start_angle), float(view_angle), float(view_radius), oj(out_datasource), _outDatasetName)
        except Exception:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.VisibilityAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[java_result.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def calculate_view_sheds(input_data, view_points, start_angles, view_angles, view_radiuses, view_shed_type, out_data=None, out_dataset_name=None, progress=None):
    """
    多点可视域分析，即分析多个观察点的可视范围，可以为共同可视域或非共同可视域。
    多点可视域分析，是根据栅格表面，对给定的观察点集合中每一个观察点进行可视域分析，然后根据指定的可视域类型，计算所有观察点的可视域的交集（称为“共同可视域”）或者并集（称为“非共同可视域”），并将结果输出到一个栅格数据集中，其中可视区域保持原始栅格表面的栅格值，其他区域为无值。

    如下图所示，图中绿色的点为观察点，叠加在原始栅格表面上的蓝色区域即为对其进行可视域分析的结果。左图展示了三个观察点的共同可视域，右图则是三个观察点的非共同可视域。

    .. image:: ../image/CalculateViewShed_1.png

    注意：如果指定的观察点的高程小于当前栅格表面对应位置的高程值，则观察点的高程值将被自动设置为当前栅格表面的对应位置的高程。

    :param input_data: 指定的用于可视域分析的栅格表面数据集。
    :type input_data: DatasetGrid or str
    :param view_points: 指定的观察点集合。
    :type view_points: list[Point3D]
    :param start_angles:  指定的起始观察角度集合，与观察点一一对应。单位为度，以正北方向为 0 度，顺时针方向旋转。指定为负值或大于 360 度，将自动换算到 0 到 360 度范围内。
    :type start_angles: list[float]
    :param view_angles: 指定的观察角度集合，与观察点和起始观察角度一一对应，单位为度，最大值为 360 度。观察角度基于起始角度，即观察角度范围为 [起始角度，起始角度+观察角度]。例如起始角度为 90 度，观察角度为 90 度，那么实际观察的角度范围是从 90 度到 180 度。    :type view_angles: list[float]
    :param view_radiuses: 指定的观察半径集合，与观察点一一对应。该值限制了视野范围的大小，若观测半径小于等于 0 时，表示无限制。单位为米。
    :type view_radiuses: list[float]
    :param view_shed_type: 指定的可视域的类型，可以是多个观察点的可视域的交集，也可以是多个观察点可视域的并集。
    :type view_shed_type: ViewShedType or str
    :param out_data: 指定的用于存储结果数据集的数据源
    :type out_data: Datasource or str
    :param str out_dataset_name: 指定的结果数据集的名称
    :param progress: 进度信息，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 多点可视域分析结果数据集。
    :rtype: DatasetGrid
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    if not isinstance(_source_input, DatasetGrid):
        raise ValueError("source input_data must be DatasetGrid")
    elif not isinstance(view_points, (list, tuple)):
        raise ValueError("view_points must be list or tuple")
    view_points = [Point3D.make(p) for p in view_points]
    if not len(view_points) != len(start_angles):
        if len(view_points) != len(view_angles) or len(view_points) != len(view_radiuses):
            raise ValueError("The length of view_points, start_angles, view_angles and view_radius must be equal.")
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = _source_input.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + "_ViewShed"
    else:
        _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    view_shed_type = ViewShedType._make(view_shed_type)
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, "calculate_view_sheds")
                _jvm.com.supermap.analyst.spatialanalyst.VisibilityAnalyst.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            java_result = _jvm.com.supermap.analyst.spatialanalyst.VisibilityAnalyst.calculateViewShedoj(_source_input)to_java_point3ds(view_points)to_java_double_array(start_angles)to_java_double_array(view_angles)to_java_double_array(view_radiuses)oj(out_datasource)_outDatasetNameoj(view_shed_type)
        except Exception:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.VisibilityAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[java_result.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


class VisibleResult:
    __doc__ = "\n    可视性分析结果类。\n\n    该类给出了观察点与被观察点之间可视分析的结果，如果不可视的话，还会给出障碍点的相关信息。\n    "

    def __init__(self, java_object):
        self._java_object = java_object

    @property
    def barrier_alter_height(self):
        """float: 障碍点建议修改的最大高度值。若将障碍点所在栅格表面的单元格的栅格值（即高程）修改为小于或等于该值，则该点不再阻碍
        视线，但注意，并不表示该点之后不存在其他障碍点。可通过 DatasetGrid 类的 set_value() 方法修改栅格值"""
        return self._java_object.getBarrierAlterHeight()

    @property
    def barrier_point(self):
        """Point3D: 障碍点的坐标值。如果观察点与被观察点之间不可视，则该方法的返回值为观察点与被观察点之间的第一个障碍点。如果观察
        点与被观察点之间可视时，障碍点坐标取默认值。 """
        return Point3D._from_java_object(self._java_object.getBarrierPoint())

    @property
    def from_point_index(self):
        """int: 观察点的索引值。如果是两点之间进行可视性分析，则观察点的索引值为 0。"""
        return self._java_object.getFromPointIndex()

    @property
    def to_point_index(self):
        """int: 被观察点的索引值。如果是两点之间进行可视性分析，则被观察点的索引值为 0。 """
        return self._java_object.getToPointIndex()

    @property
    def visible(self):
        """bool: 观察点与被观察点对之间是否可视"""
        return self._java_object.getVisible()


def is_point_visible(input_data, from_point, to_point):
    """
    两点可视性分析，即判断两点之间是否相互可见。
    基于栅格表面，判断给定的观察点与被观察点之间是否可见，称为两点间可视性分析。两点间可视性分析的结果有两种：可视与不可视。该方法返
    回一个 VisibleResult 对象，该对象用于返回两点间可视性分析的结果，即两点是否可视，如果不可视，会返回第一个阻碍视线的障碍点，还会
    给出该障碍点的建议高程值以使该点不再阻碍视线。

    :param input_data: 指定的用于可视性分析的栅格表面数据集。
    :type input_data: DatasetGrid or str
    :param from_point: 指定的用于可视性分析的起始点，即观察点
    :type from_point: Point3D
    :param to_point: 指定的用于可视性分析的终止点，即被观察点。
    :type to_point: Point3D
    :return: 可视性分析的结果
    :rtype: VisibleResult
    """
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    if not isinstance(_source_input, DatasetGrid):
        raise ValueError("source input_data must be DatasetGrid")
    _jvm = get_jvm()
    from_point = Point3D.make(from_point)
    to_point = Point3D.make(to_point)
    try:
        try:
            java_result = _jvm.com.supermap.analyst.spatialanalyst.VisibilityAnalyst.isVisible(oj(_source_input), oj(from_point), oj(to_point))
        except Exception:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        return

    if java_result is not None:
        return VisibleResult(java_result)


def are_points_visible(input_data, from_points, to_points):
    """
    多点可视性分析，即判断多点之间是否可两两通视。
    多点可视性分析，是根据栅格表面，计算观察点与被观察点之间是否两两通视。两点间可视性分析请参阅另一重载方法 isVisible 方法的介绍。

    如果有 m 个观测点和 n 个被观测点，将有 m * n 种观测组合。分析的结果通过一个 VisibleResult 对象数组返回，每个 VisibleResult
    对象包括对应的两点是否可视，如果不可视，会给出第一个障碍点，以及该点的建议高程值以使该点不再阻碍视线。

    注意：如果指定的观察点的高程小于当前栅格表面对应位置的高程值，则观察点的高程值将被自动设置为当前栅格表面的对应位置的高程。

    :param input_data: 指定的用于可视性分析的栅格表面数据集。
    :type input_data: DatasetGrid or str
    :param from_points: 指定的用于可视性分析的起始点，即观察点
    :type from_points: list[Point3D]
    :param to_points: 指定的用于可视性分析的终止点，即被观察点。
    :type to_points: list[Point3D]
    :return: 可视性分析的结果
    :rtype: list[VisibleResult]
    """
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    if not isinstance(_source_input, DatasetGrid):
        raise ValueError("source input_data must be DatasetGrid")
    _jvm = get_jvm()
    from_points = to_java_point3ds([Point3D.make(p) for p in from_points])
    to_points = to_java_point3ds([Point3D.make(p) for p in to_points])
    try:
        try:
            java_result = _jvm.com.supermap.analyst.spatialanalyst.VisibilityAnalyst.isVisible(oj(_source_input), from_points, to_points)
        except Exception:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        return

    if java_result is not None:
        return [VisibleResult(item) for item in java_result]


def line_of_sight(input_data, from_point, to_point):
    """
    计算两点间的通视线，即根据地形计算观察点到目标点的视线上的可视部分和不可视部分。
    依据地形的起伏，计算从观察点看向目标点的视线上哪些段可视或不可视，称为计算两点间的通视线。观察点与目标点间的这条线称为通视线。
    通视线可以帮助了解在给定点能够看到哪些位置，可服务于旅游线路规划、雷达站或信号发射站的选址，以及布设阵地、观察哨所设置等军事活动。

    .. image:: ../image/LineOfSight.png

    观察点和目标点的高程由其 Z 值确定。当观察点或目标点的 Z 值小于栅格表面上对应单元格的高程值时，则使用该单元格的栅格值作为观察点或
    目标点的高程来计算通视线。

    计算两点间通视线的结果为一个二维线对象数组，该数组的第 0 个元素为可视线对象，第 1 个元素为不可视线对象。该数组的长度可能为 1 或
     2，这是因为不可视线对象有可能不存在，此时结果数组只包含一个对象，即可视线对象。由于可视线（或不可视线）可能不连续，因此可视线或
     不可视线对象有可能是复杂线对象。

    :param input_data: 指定的栅格表面数据集。
    :type input_data: DatasetGrid or str
    :param from_point: 指定的观察点，是一个三维点对象。
    :type from_point: Point3D
    :param to_point: 指定的目标点，是一个三维点对象。
    :type to_point: Point3D
    :return: 结果通视线，是一个二维线数组
    :rtype: list[GeoLine]
    """
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    if not isinstance(_source_input, DatasetGrid):
        raise ValueError("source input_data must be DatasetGrid")
    _jvm = get_jvm()
    from_point = Point3D.make(from_point)
    to_point = Point3D.make(to_point)
    try:
        try:
            java_result = _jvm.com.supermap.analyst.spatialanalyst.VisibilityAnalyst.lineOfSight(oj(_source_input), oj(from_point), oj(to_point))
        except Exception:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        return

    if java_result is not None:
        return [Geometry._from_java_object(item) for item in java_result]


def radar_shield_angle(input_data, view_point, start_angle, end_angle, view_radius, interval, out_data=None, out_dataset_name=None, progress=None):
    """
    根据地形图和雷达中心点，返回各方位上最大的雷达遮蔽角的点数据集。方位角是顺时针与正北方向的夹角。

    :param input_data:  删格数据集或DEM
    :type input_data: DatasetGrid or str or list[DatasetGrid] or list[str]
    :param view_point: 三维点对象，表示雷达中心点的坐标和雷达中心与地面的高度。
    :type view_point: Point3D
    :param float start_angle: 雷达方位起始角度,单位为度,以正北方向为 0 度,顺时针方向旋转。范围为0到360度。如果设置为小于0，默认值
                              为0；如果该值大于360，默认为360。
    :param float end_angle: 雷达方位终止角度，单位为度，最大值为 360 度。观察角度基于起始角度，即观察角度范围为 [起始角度，终止角度)。
                            该值必须大于起始角度。如果该值小于等于0,表示[0,360)。
    :param float view_radius: 观察范围，单位为米。如果设置为小于0，表示整个地形图范围。
    :param float interval: 方位角的间隔，即每隔多少度返回一个雷达遮蔽点。该值必须大于0且小于360。
    :param out_data: 目标数据源。
    :type out_data: Datasource or str
    :param str out_dataset_name: 结果数据集名称
    :param progress:  进度信息，具体参考 :py:class:`.StepEvent`
    :type progress: funtion
    :return: 返回的三维点数据集,Z代表该点所在位置的地形高度。该数据集记录了每个方位上雷达遮蔽角最大的点,并增加了字段"ShieldAngle"、
             "ShieldPosition"和"RadarDistance"分别记录了雷达遮蔽角、该点与正北方向的夹角和点与雷达中心的距离。
    :rtype: DatasetVector or str
    """
    check_lic()
    inputs = []
    if isinstance(input_data, (list, tuple)):
        for item in input_data:
            inputs.append(get_input_dataset(item))

    else:
        inputs.append(get_input_dataset(input_data))
    inputs = list(filter((lambda x: isinstance(x, DatasetGrid)), inputs))
    if len(inputs) == 0:
        raise ValueError("source input_data must be DatasetGrid or list[DatasetGrid]")
    else:
        view_point = Point3D.make(view_point)
        if not isinstance(view_point, Point3D):
            raise ValueError("view_point must be Point3D")
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = inputs[0].datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = inputs[0].name + "_radarShield"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, "radar_shield_angle")
                _jvm.com.supermap.analyst.spatialanalyst.VisibilityAnalyst.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            if len(inputs) == 1:
                java_dt = oj(inputs[0])
            else:
                java_dt = to_java_datasetgrid_array(inputs)
            java_result = _jvm.com.supermap.analyst.spatialanalyst.VisibilityAnalyst.radarShieldAnglejava_dtoj(view_point)float(start_angle)float(end_angle)float(view_radius)oj(out_datasource)_outDatasetNamefloat(interval)
        except Exception:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialanalyst.VisibilityAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[java_result.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def majority_filter(source_grid, neighbour_number_method, majority_definition, out_data=None, out_dataset_name=None, progress=None):
    """
    众数滤波，返回结果栅格数据集。
    根据相邻像元值的众数替换栅格像元值。众数滤波工具必须满足两个条件才能执行替换。具有相同值的相邻像元数必须足够多（达到所有像元的半
    数及以上），并且这些像元在滤波器内核周围必须是连续的。第二个条件与像元的空间连通性有关，目的是将像元的空间模式的破坏程度降到最低。

    特殊情况:

    - 角像元：4邻域情况下相邻像元2个，8邻域情况下相邻像元3个，此时必须连续两个及以上相同值才能发生替换；
    - 边像元：4邻域情况下相邻像元3个，此时必须连续2个及以上相同值才能替换；8邻域情况下相邻像元5个，此时必须3个及以上并且至少一个像
      元在边上才能发生替换。
    - 半数相等：有两种值都为半数时其中一种和该像元相同时不替换，不同时随意替换。

    下图为众数滤波的示意图。

    .. image:: ../image/majorityFilter.png

    :param source_grid: 指定的待处理的数据集。输入栅格必须为整型。
    :type source_grid: DatasetGrid or str
    :param neighbour_number_method: 邻域像元数。有上下左右4个像元作为邻近像元（FOUR），和相邻8个像元作为邻近像元（EIGHT）两种选
                                    择方法。
    :type neighbour_number_method: str or NeighbourNumber
    :param majority_definition: 众数定义，即在进行替换之前指定必须具有相同值的相邻（空间连接）像元数，具体参考 :py:class:`.MajorityDefinition` .
    :type majority_definition: str or MajorityDefinition
    :param out_data:  指定的存储结果数据集的数据源。
    :type out_data:  DatasourceConnectionInfo or Datasource or str
    :param out_dataset_name: 指定的结果数据集的名称。
    :type out_dataset_name: str
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集
    :rtype: DatasetGrid
    """
    check_lic()
    source_dt = get_input_dataset(source_grid)
    if not isinstance(source_dt, DatasetGrid):
        raise ValueError("source required DatasetGrid, but is " + str(type(source_grid)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name + "_majority"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "majority_filter")
                        get_jvm().com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            neighbour_number_method = NeighbourNumber._make(neighbour_number_method)
            majority_definition = MajorityDefinition._make(majority_definition)
            majorityFilter = get_jvm().com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.majorityFilter
            java_result = majorityFilter(oj(source_dt), oj(out_datasource), _outDatasetName, oj(neighbour_number_method), oj(majority_definition))
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def expand(source_grid, neighbour_number_method, cell_number, zone_values, out_data=None, out_dataset_name=None, progress=None):
    """
    扩展，返回结果栅格数据集。
    按指定的像元数目展开指定的栅格区域。将指定的区域值视为前景区域，其余的区域值视为背景区域。通过此方法可使前景区域扩展到背景区域。
    无值像元将始终被视为背景像元，因此任何值的相邻像元都可以扩展到无值像元，无值像元不会扩展到相邻像元。

    注意：

    - 只有一种类型区域值时，则扩展该值；
    - 多种类型区域值时，首先扩展距离最近的；
    - 距离相等的情况下，计算每个区域值的贡献值，扩展总贡献值最大的值（4邻域法和8邻域法的贡献值计算方式不同）；
    - 距离和贡献值相等，则扩展像元值最小的。

    下图为扩展的示意图:

    .. image:: ../image/expand.png

    :param source_grid: 指定的待处理的数据集。输入栅格必须为整型。
    :type source_grid: DatasetGrid or str
    :param neighbour_number_method: 邻域像元数，在这里指用于扩展所选区域的方法。有基于距离的方法，即上下左右4个像元作为邻近像
                                    元（FOUR），和基于数学形态学的方法，即相邻8个像元作为邻近像元（EIGHT）两种扩展方法。
    :type neighbour_number_method: NeighbourNumber or str
    :param cell_number: 概化量。每个指定区域要扩展的像元数，类似于指定运行次数，其中上一次运行的结果是后续迭代的输入，该值必须为大
                        于1的整数。
    :type cell_number: int
    :param zone_values: 区域值。要进行扩展的像元区域值。
    :type zone_values: list[int]
    :param out_data: 指定的存储结果数据集的数据源
    :type out_data:  DatasourceConnectionInfo or Datasource or str
    :param out_dataset_name: 指定的结果数据集的名称。
    :type out_dataset_name: str
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果栅格数据集
    :rtype: DatasetGrid
    """
    check_lic()
    source_dt = get_input_dataset(source_grid)
    if not isinstance(source_dt, DatasetGrid):
        raise ValueError("source required DatasetGrid, but is " + str(type(source_grid)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name + "_expand"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "expand")
                        get_jvm().com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            neighbour_number_method = NeighbourNumber._make(neighbour_number_method)
            expand = get_jvm().com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.expand
            java_result = expand(oj(source_dt), oj(out_datasource), _outDatasetName, oj(neighbour_number_method), int(cell_number), to_java_int_array(split_input_int_list_from_str(zone_values)))
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def shrink(source_grid, neighbour_number_method, cell_number, zone_values, out_data=None, out_dataset_name=None, progress=None):
    """
    收缩，返回结果栅格数据集。
    按指定的像元数目收缩所选区域，方法是用邻域中出现最频繁的像元值替换该区域的值。将指定的区域值视为前景区域，其余的区域值视为背景区
    域。通过此方法可用背景区域中的像元来替换前景区域中的像元。

    注意：

    - 收缩有多个值时，取出现最频繁的，如果多个值个数相同则取随机值；
    - 两个相邻区域都是要收缩的像元，则在边界上没有任何变化；
    - 无值为有效值，即与无值数据相邻的像元有可能被替换为无值。

    下图为收缩的示意图:

    .. image:: ../image/shrink.png

    :param source_grid: 指定的待处理的数据集。输入栅格必须为整型。
    :type source_grid: DatasetGrid or str
    :param neighbour_number_method: 邻域像元数，在这里指用于收缩所选区域的方法。有基于距离的方法，即上下左右4个像元作为邻近像
                                    元（FOUR），和基于数学形态学的方法，即相邻8个像元作为邻近像元（EIGHT）两种收缩方法。
    :type neighbour_number_method: NeighbourNumber or str
    :param cell_number: 概化量。要收缩的像元数，类似于指定运行次数，其中上一次运行的结果是后续迭代的输入，该值必须为大于0的整数。
    :type cell_number: int
    :param zone_values: 区域值。要进行收缩的像元区域值。
    :type zone_values: list[int]
    :param out_data: 指定的存储结果数据集的数据源。
    :type out_data: DatasourceConnectionInfo or Datasource or str
    :param out_dataset_name: 指定的结果数据集的名称。
    :type out_dataset_name: str
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果栅格数据集
    :rtype: DatasetGrid
    """
    check_lic()
    source_dt = get_input_dataset(source_grid)
    if not isinstance(source_dt, DatasetGrid):
        raise ValueError("source required DatasetGrid, but is " + str(type(source_grid)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name + "_shrink"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "shrink")
                        get_jvm().com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            neighbour_number_method = NeighbourNumber._make(neighbour_number_method)
            shrink = get_jvm().com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.shrink
            java_result = shrink(oj(source_dt), oj(out_datasource), _outDatasetName, oj(neighbour_number_method), int(cell_number), to_java_int_array(split_input_list_from_str(zone_values)))
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def region_group(source_grid, neighbour_number_method, is_save_link_value, is_link_by_neighbour=False, exclude_value=None, out_data=None, out_dataset_name=None, progress=None):
    """
    区域分组。
    记录输出中每个像元所属的连接区域的标识，系统为每个区域分配唯一编号，简单来说就是将连通的具有相同值的像元组成一个区域并编号。扫描
    的第一个区域赋值为1，第二个区域赋值为2，依此类推，直到所有的区域均已赋值。扫描将按从左至右、从上至下的顺序进行。

    下图为区域分组的示意图:

    .. image:: ../image/regionGroup.png

    :param source_grid: 指定的待处理的数据集。输入栅格必须为整型。
    :type source_grid: DatasetGird or str
    :param neighbour_number_method: 邻域像元数。有上下左右4个像元作为邻近像元（FOUR），和相邻8个像元作为邻近像元（EIGHT）两种选择方法。
    :type neighbour_number_method: str or NeighbourNumber
    :param bool is_save_link_value: 是否保留对应的栅格原始值。设置为true,属性表增加SourceValue项，连接输入栅格的每个像元的原始
                                    值；如果不再需要每个区域的原始值，可以设置为false，会加速处理过程。
    :param bool is_link_by_neighbour: 是否根据邻域连通。设置为true时，根据4邻域或8邻域法连通像元构成区域；设置为false时，必须设
                                      置排除值excludedValue，此时除了排除值的连通区域都可以构成一个区域
    :param int exclude_value: 排除值。排除的栅格值不参与计数，在输出栅格上，包含排除值的像元位置赋值为0。如果设置了排除值，结果属
                              性表中就没有连接信息。
    :param out_data: 指定的存储结果数据集的数据源
    :type out_data: DatasourceConnectionInfo or Datasource or str
    :param out_dataset_name: 指定的结果数据集的名称
    :type out_dataset_name: str
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果栅格数据集和属性表
    :rtype: tuple[DatasetGrid, DatasetVector]
    """
    check_lic()
    source_dt = get_input_dataset(source_grid)
    if not isinstance(source_dt, DatasetGrid):
        raise ValueError("source required DatasetGrid, but is " + str(type(source_grid)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name + "_regionGroup"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None and safe_start_callback_server():
                try:
                    listener = ProgressListener(progress, "regionGroup")
                    get_jvm().com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.addSteppedListener(listener)
                except Exception as e:
                    try:
                        close_callback_server()
                        log_error(e)
                        listener = None
                    finally:
                        e = None
                        del e

            else:
                neighbour_number_method = NeighbourNumber._make(neighbour_number_method)
                regionGroup = get_jvm().com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.regionGroup
                if exclude_value is None:
                    java_result = regionGroup(oj(source_dt), oj(out_datasource), _outDatasetName, oj(neighbour_number_method), bool(is_save_link_value))
                else:
                    java_result = regionGroupoj(source_dt)oj(out_datasource)_outDatasetNameoj(neighbour_number_method)bool(is_save_link_value)bool(is_link_by_neighbour)int(exclude_value)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_grid_dt = out_datasource[java_result.getResultGrid()]
            result_vector_dt = out_datasource[java_result.getResultTable()]
            result_dts = (result_grid_dt, result_vector_dt)
        else:
            result_dts = None
        if out_data is not None:
            return try_close_output_datasource(result_dts, out_datasource)
        return result_dts


def nibble(source_grid, mask_grid, zone_grid, is_mask_no_value, is_nibble_no_value, out_data=None, out_dataset_name=None, progress=None):
    """
    蚕食，返回结果栅格数据集。

    用最邻近点的值替换掩膜范围内的栅格像元值。蚕食可将最近邻域的值分配给栅格中的所选区域，可用于编辑某栅格中已知数据存在错误的区域。

    一般来说掩膜栅格中值为无值的像元定义哪些像元被蚕食。输入栅格中任何不在掩膜范围内的位置均不会被蚕食。

    下图为蚕食的示意图:

    .. image:: ../image/nibble.png

    :param source_grid: 指定的待处理的数据集。输入栅格可以为整型，也可以为浮点型。
    :type source_grid: DatasetGrid or str
    :param mask_grid: 指定的作为掩膜的栅格数据集。
    :type mask_grid: DatasetGrid or str
    :param zone_grid: 区域栅格。如果有区域栅格，掩膜内的像元只会被区域栅格中同一区域的最近像元（非掩膜的值）替换。区域是指栅格中具
                      有相同值
    :type zone_grid: DatasetGrid or str
    :param bool is_mask_no_value: 是否选择掩膜中无值像元被蚕食。True 表示选择无值像元被蚕食，即把掩膜中为无值的对应原栅格值替换为
                                  最邻近区域的值，有值像元在原栅格中保持不变；False 表示选择有值像元被蚕食，即把掩膜中为有值的对应
                                  原栅格值替换为最邻近区域的值，无值像元在原栅格中保持不变。一般使用第一种情况较多。
    :param bool is_nibble_no_value: 是否修改原栅格中的无值数据。True表示输入栅格中的无值像元在输出中仍为无值；False表示输入栅格。
                                    中处于掩膜内的无值像元可以被蚕食为有效的输出像元值
    :param out_data: 指定的存储结果数据集的数据源
    :type out_data: DatasourceConnectionInfo or Datasource or str
    :param out_dataset_name: 指定的结果数据集的名称。
    :type out_dataset_name: str
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return:
    :rtype: DatasetGrid
    """
    check_lic()
    source_dt = get_input_dataset(source_grid)
    if not isinstance(source_dt, DatasetGrid):
        raise ValueError("source required DatasetGrid, but is " + str(type(source_grid)))
    else:
        mask_dt = get_input_dataset(mask_grid)
        if mask_dt is not None:
            if not isinstance(mask_dt, DatasetGrid):
                raise ValueError("source required DatasetGrid, but is " + str(type(mask_grid)))
        zone_dt = get_input_dataset(zone_grid)
        if zone_dt is not None:
            if not isinstance(zone_dt, DatasetGrid):
                raise ValueError("source required DatasetGrid, but is " + str(type(zone_grid)))
            elif out_data is not None:
                out_datasource = get_output_datasource(out_data)
            else:
                out_datasource = source_dt.datasource
            check_output_datasource(out_datasource)
            if out_dataset_name is None:
                _outDatasetName = source_dt.name + "_nibble"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "nibble")
                        get_jvm().com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            nibble = get_jvm().com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.nibble
            java_result = nibbleoj(source_dt)oj(mask_dt)oj(zone_dt)oj(out_datasource)_outDatasetNamebool(is_mask_no_value)bool(is_nibble_no_value)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def boundary_clean(source_grid, sort_type, is_run_two_times, out_data=None, out_dataset_name=None, progress=None):
    """
    边界清理，返回结果栅格数据集。
    通过扩展和收缩来平滑区域间的边界。将更改x和y方向上所有少于三个像元的区域。

    下图为边界清理的示意图:

    .. image:: ../image/BoundaryClean.png

    :param source_grid: 指定的待处理的数据集。输入栅格必须为整型。
    :type source_grid: DatasetGrid or str
    :param sort_type: 排序方法。指定要在平滑处理中使用的排序类型。包括NOSORT、DESCEND、ASCEND三种方法。
    :type sort_type: BoundaryCleanSortType or str
    :param is_run_two_times: 发生平滑处理过程的次数是否为两次。True表示执行两次扩展-收缩过程，根据排序类型执行扩展和收缩，然后使
                             用相反的优先级多执行一次收缩和扩展；False表示根据排序类型执行一次扩展和收缩。
    :type is_run_two_times: bool
    :param out_data: 指定的存储结果数据集的数据源。
    :type out_data: DatasourceConnectionInfo or Datasource or str
    :param out_dataset_name: 结果数据集的名称
    :type out_dataset_name: str
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果栅格数据集
    :rtype: DatasetGrid
    """
    check_lic()
    source_dt = get_input_dataset(source_grid)
    if not isinstance(source_dt, DatasetGrid):
        raise ValueError("source required DatasetGrid, but is " + str(type(source_grid)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name + "_boundaryClean"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "boundary_clean")
                        get_jvm().com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            boundaryClean = get_jvm().com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.boundaryClean
            sort_type = BoundaryCleanSortType._make(sort_type)
            java_result = boundaryClean(oj(source_dt), oj(out_datasource), _outDatasetName, oj(sort_type), bool(is_run_two_times))
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialanalyst.GeneralizeAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


class CellularAutomataParameter:
    __doc__ = "\n    元胞自动机参数设置类。包括设置起始栅格和空间变量栅格数据，及模拟过程的显示与输出配置（模拟结果迭代刷新、模拟结果输出）等\n    "

    def __init__(self):
        self._cell_grid = None
        self._spatial_variable_grids = None
        self._is_save = False
        self._save_frequency = 10
        self._flush_frequency = 10
        self._simulation_count = 0
        self._flush_file_path = None
        self._output_ds = None
        self._output_dt_name = None
        self._iterations = 10

    def set_cell_grid(self, cell_grid):
        """
        设置起始数据栅格。

        :param cell_grid:  起始数据栅格
        :type cell_grid: DatasetGrid or str
        :return: self
        :rtype: CellularAutomataParameter
        """
        self._cell_grid = get_input_dataset(cell_grid)
        return self

    @property
    def cell_grid(self):
        """DatasetGrid:  起始数据栅格"""
        return self._cell_grid

    def set_spatial_variable_grids(self, spatial_variable_grids):
        """
        设置空间变量数据栅格数组。

        :param spatial_variable_grids: 空间变量数据栅格数组
        :type spatial_variable_grids: DatasetGrid or list[DatasetGrid] or tuple[DatasetGrid]
        :return: self
        :rtype: CellularAutomataParameter
        """
        if isinstance(spatial_variable_grids, (list, tuple)):
            self._spatial_variable_grids = [get_input_dataset(grid) for grid in spatial_variable_grids]
        else:
            if isinstance(self.spatial_variable_grids, (DatasetGrid, str)):
                self._spatial_variable_grids = [
                 get_input_dataset(spatial_variable_grids)]
        return self

    @property
    def spatial_variable_grids(self):
        """list[DatasetGrid]: 空间变量数据栅格数组"""
        return self._spatial_variable_grids

    def set_save(self, save):
        """
        设置是否保存中间迭代结果。即模拟过程中是否输出结果。

        :param bool save: 是否保存中间迭代结果
        :return: self
        :rtype: CellularAutomataParameter
        """
        if save:
            self._is_save = bool(save)
        return self

    @property
    def is_save(self):
        """bool: 是否保存中间迭代结果"""
        return self._is_save

    def set_save_frequency(self, save_frequency):
        """
        设置中间迭代结果保存频率。即每隔多少次迭代输出一次结果。

        :param int save_frequency: 中间迭代结果保存频率
        :return: self
        :rtype: CellularAutomataParameter
        """
        if save_frequency:
            self._save_frequency = int(save_frequency)
        return self

    @property
    def save_frequency(self):
        """int: 中间迭代结果保存频率"""
        return self._save_frequency

    def set_flush_frequency(self, flush_frequency):
        """
        设置迭代结果刷新频率。即每隔多少次迭代刷新一次输出信息和图表。

        :param int flush_frequency: 迭代结果刷新频率
        :return: self
        :rtype: CellularAutomataParameter
        """
        if flush_frequency:
            self._flush_frequency = int(flush_frequency)
        return self

    @property
    def flush_frequency(self):
        """int: 迭代结果刷新频率"""
        return self._flush_frequency

    def set_simulation_count(self, simulation_count):
        """
        设置转换数目。模拟转换数目是模拟过程所需参数，是指两个不同时段之间的城市增加的个数。

        :param int simulation_count:  转换数目
        :return: self
        :rtype: CellularAutomataParameter
        """
        if simulation_count:
            self._simulation_count = int(simulation_count)
        return self

    @property
    def simulation_count(self):
        """int:  转换数目"""
        return self._simulation_count

    def set_output_datasource(self, datasource):
        """
        设置中间迭代结果保存数据源。

        :param datasource: 中间迭代结果保存数据源。
        :type datasource: Datasource or str or DatasourceConnectionInfo
        :return: self
        :rtype: CellularAutomataParameter
        """
        self._output_ds = get_output_datasource(datasource)
        return self

    @property
    def output_datasource(self):
        """Datasource:  中间迭代结果保存数据源。"""
        return self._output_ds

    def set_output_dataset_name(self, dataset_name):
        """
        设置中间迭代结果保存数据集名称

        :param str dataset_name: 中间迭代结果保存数据集名称
        :return: self
        :rtype: CellularAutomataParameter
        """
        self._output_dt_name = dataset_name
        return self

    @property
    def output_dataset_name(self):
        """str: """
        return self._output_dt_name

    def set_flush_file_path(self, value):
        """
        设置用于界面刷新的文件路径

        :param str value: 用于界面刷新的文件路径
        :return: self
        :rtype: CellularAutomataParameter
        """
        self._flush_file_path = value
        return self

    @property
    def flush_file_path(self):
        """str: 用于界面刷新的文件路径"""
        return self._flush_file_path

    @property
    def iterations(self):
        """int: 迭代次数"""
        return self._iterations

    def set_iterations(self, value):
        """
        设置迭代次数

        :param int value: 迭代次数
        :return: self
        :rtype: CellularAutomataParameter
        """
        if value:
            self._iterations = int(value)
        return self

    @property
    def _jobject(self):
        jvm = get_jvm()
        java_object = jvm.com.supermap.analyst.spatialanalyst.CellularAutomataParameter()
        java_object.setCellGrid(oj(self.cell_grid))
        java_object.setSpatialVariableGrids(to_java_datasetgrid_array(self.spatial_variable_grids))
        java_object.setSave(bool(self.is_save))
        java_object.setSaveFrequency(int(self.save_frequency))
        java_object.setFlushFrequency(int(self.flush_frequency))
        java_object.setSimulationCount(int(self.simulation_count))
        if self._output_ds is not None:
            out_ds = get_output_datasource(self._output_ds)
        else:
            out_ds = self._cell_grid.datasource
        check_output_datasource(out_ds)
        if self._output_dt_name is None:
            _dest_name = self._cell_grid.name + "_CA"
        else:
            _dest_name = self._output_dt_name
        _dest_name = out_ds.get_available_dataset_name(_dest_name)
        if out_ds:
            java_object.setOutputDataSource(oj(out_ds))
        if _dest_name:
            java_object.setOutputDatasetName(_dest_name)
        if self.flush_file_path:
            java_object.setFlushFilePathName(str(self.flush_file_path))
        java_object.setIterations(int(self.iterations))
        return java_object


class PCAEigenValue:
    __doc__ = "\n    主成分分析特征值结果类。\n    "

    def __init__(self):
        self._eigen_value = None
        self._contribution_rate = None
        self._cumulative = None
        self._spatial_raster_name = None

    @property
    def eigen_value(self):
        """float: 特征值"""
        return self._eigen_value

    @property
    def contribution_rate(self):
        """float: 贡献率"""
        return self._contribution_rate

    @property
    def cumulative(self):
        """float: 累积贡献率"""
        return self._cumulative

    @property
    def spatial_dataset_raster_name(self):
        """str: 空间变量数据名称"""
        return self._spatial_raster_name

    @staticmethod
    def _make_from_java_object(java_object):
        event_value = PCAEigenValue()
        event_value._eigen_value = java_object.getEigenValue()
        event_value._contribution_rate = java_object.getContributionRate()
        event_value._cumulative = java_object.getCumulative()
        event_value._spatial_raster_name = java_object.getSpatialDatasetRasterName()
        return event_value


class PCAEigenResult:
    __doc__ = "\n    主成分分析结果类。主成分分析由于不同的抽样数目和主成分比例，导致得到的主成分数目不同，所以需要在主成分分析之后根据得到的结\n    果（主成分和贡献率等）进行权重设置，设置好权重之后就能利用元胞自动机进行模拟。\n\n    "

    def __init__(self):
        self._component_count = None
        self._spatial_dataset_raster_names = None
        self._pca_eigen_values = None
        self._pca_loadings = None

    @property
    def component_count(self):
        """int: 主成分数目"""
        return self._component_count

    @property
    def spatial_dataset_raster_names(self):
        """list[str]: 空间变量数据名称"""
        return self._spatial_dataset_raster_names

    @property
    def pca_eigen_values(self):
        """list[PCAEigenValue]: 主成分分析特征值结果数组"""
        return self._pca_eigen_values

    @property
    def pca_loadings(self):
        """list[float]: 主成分贡献率"""
        return self._pca_loadings

    @staticmethod
    def _make_from_java_object(java_object):
        result = PCAEigenResult()
        result._component_count = java_object.getComponentCount()
        result._spatial_dataset_raster_names = java_object.getSpatialDatasetRasterNames()
        eigen_values = java_object.getPCAEigenValues()
        if eigen_values is not None:
            result._pca_eigen_values = [PCAEigenValue._make_from_java_object(item) for item in eigen_values]
        result._primary_component_loadings = java_object.getPCALoadings()
        return result


class PCACellularAutomataParameter:
    __doc__ = "\n    基于主成分分析的元胞自动机参数类。在进行基于主成分分析的元胞自动机过程时，需要生成主成分分析，这一过程需要设置主成分权重值、模拟\n    过程所需参数（非线性指数变换值、扩散指数）等。\n    "

    def __init__(self):
        self._component_weights = None
        self._alpha = 2
        self._index_k = 4.0
        self._conversion_rules = None
        self._conversion_target = None
        self._ca_parameter = None

    @property
    def cellular_automata_parameter(self):
        """CellularAutomataParameter: 元胞自动机参数"""
        return self._ca_parameter

    def set_cellular_automata_parameter(self, value):
        """
        设置元胞自动机参数。

        :param value: 元胞自动机参数
        :type value: CellularAutomataParameter
        :return: self
        :rtype: PCACAParameter
        """
        if isinstance(value, CellularAutomataParameter):
            self._ca_parameter = value
        return self

    def set_component_weights(self, value):
        """
        设置主成分权重数组。

        :param value: 主成分权重数组
        :type value: list[float] or tuple[float]
        :return: self
        :rtype: PCACAParameter
        """
        if value is not None:
            self._component_weights = split_input_list_from_str(value)
        return self

    @property
    def component_weights(self):
        """list[float]: 主成分权重数组"""
        return self._component_weights

    def set_alpha(self, value):
        """
        设置扩散参数。一般1-10。

        :param int value: 扩散参数。
        :return: self
        :rtype: PCACAParameter
        """
        if value is not None:
            self._alpha = int(value)
        return self

    @property
    def alpha(self):
        """int: 扩散参数"""
        return self._alpha

    def set_index_k(self, value):
        """
        设置非线性指数变换值。本系统为4。

        :param float value: 非线性指数变换值。
        :return: self
        :rtype: PCACAParameter
        """
        if value is not None:
            self._index_k = float(value)
        return self

    @property
    def index_k(self):
        """float:  非线性指数变换值。"""
        return self._index_k

    def set_conversion_rules(self, value):
        """
        设置转换规则。例如在土地利用的变化中，水域为不可转变用地，农田为可转变用地。

        :param value: 转换规则
        :type value: dict[int,bool]
        :return: self
        :rtype: PCACAParameter
        """
        if value is not None:
            self._conversion_rules = split_input_dict_from_str(value)
        return self

    @property
    def conversion_rules(self):
        """dict[int,bool]: 转换规则"""
        return self._conversion_rules

    def set_conversion_target(self, value):
        """
        设置转换目标。例如农田转换为城市用地中，城市用地为转换目标。

        :param int value: 转换目标
        :return: self
        :rtype: PCACAParameter
        """
        if value is not None:
            self._conversion_target = float(value)
        return self

    @property
    def conversion_target(self):
        """int: 转换目标"""
        return self._conversion_target

    @property
    def _jobject(self):
        java_object = get_jvm().com.supermap.analyst.spatialanalyst.PCACellularAutomataParameter()
        if self.cellular_automata_parameter:
            java_object.setCellularAutomataParameter(oj(self.cellular_automata_parameter))
        if self._component_weights:
            java_object.setComponentWeights(to_java_double_array(self._component_weights))
        if self._index_k:
            java_object.setIndexK(float(self._index_k))
        if self.alpha:
            java_object.setAlpha(int(self.alpha))
        if self.conversion_target:
            java_object.setConversionTarget(int(self.conversion_target))
        if self._conversion_rules:
            rules = {}
            for item in self._conversion_rules.keys():
                rules[int(item)] = bool(self._conversion_rules[item])

            java_object.setConversionRules(rules)
        return java_object


class CellularAutomataFlushedEvent(object):
    __doc__ = "\n    元胞自动机刷新事务类。\n    "

    def __init__(self, flush_file_path=None):
        """
        :param str flush_file_path: 用于刷新的tif文件路径
        """
        self._flush_file_path = flush_file_path

    def __repr__(self):
        return self._flush_file_path

    @property
    def flush_file_path(self):
        """str: 用于刷新的tif文件路径"""
        return self._flush_file_path


class CellularAutomataFlushedListener(PythonListenerBase):
    __doc__ = "\n    元胞自动机刷新信息的监听器，内部调用，外部用户不要调用。\n    "

    def __init__(self, progress_fun, name):
        """

        :param progress_fun: 元胞自动机刷新信息处理函数
        :type progress_fun: function
        :param name: 唯一标识名称。
        :type name: str
        """
        self._flush_event = CellularAutomataFlushedEvent()
        PythonListenerBase.__init__(self, "CellularAutomataFlushed:" + name, progress_fun)

    def CAFlushed(self, event):
        if self.func is not None:
            self._flush_event._flush_file_path = event.getFlushFilePathName()
            self.func(self._flush_event)

    class Java:
        implements = [
         "com.supermap.analyst.spatialanalyst.CAFlushedListener"]


class PCACellularAutomata(JVMBase):
    __doc__ = "\n    基于主成分分析的元胞自动机。\n\n    元胞自动机（cellular automata, CA）是一种时间、空间、状态都离散，空间相互作用和时间因果关系为局部的网络动力学模型，具有模拟复杂\n    系统时空演化过程的能力。\n\n    当地理模拟需要使用许多空间变量，这些空间变量往往是相关的，有必要采用主成分分析，可以有效地将多个空间变量压缩到少数的主成分中，减\n    少设置权重的难度，可以将基于主成分分析的元胞自动机应用在城市发展的空间模拟中。\n    "

    def __init__(self):
        JVMBase.__init__(self)

    def _make_java_object(self):
        self._java_object = get_jvm().com.supermap.analyst.spatialanalyst.PCACellularAutomata()
        return self._java_object

    def pca(self, spatial_variable_grids, sample_count, component_radio, progress_func=None):
        """
        对元胞数据集进行抽样和主成分分析。

        该方法用于在进行基于主成分分析的元胞自动机分析之前，利用得到的主成分个数设置对应的权重值。

        :param spatial_variable_grids: 空间变量栅格数据集。
        :type spatial_variable_grids: list[DatasetGrid] or tuple[DatasetGird]
        :param int sample_count: 抽样个数。在整个栅格数据中随机抽取样本指定的样本个数
        :param float component_radio: 主成分比例，取值范围 [0,1]，例如取值为0.8时，表示选取前n个累计贡献率达到80%的主成分。
        :param function progress_func: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
        :return: 主成分分析结果，包含主成分个数、贡献率、特征值和特征向量
        :rtype: PCAEigenResult
        """
        if isinstance(spatial_variable_grids, (DatasetGrid, str)):
            spatial_variable_grids = [
             spatial_variable_grids]
        if isinstance(spatial_variable_grids, (list, tuple)):
            spatial_variable_grids = [get_input_dataset(grid) for grid in spatial_variable_grids]
        listener = None
        try:
            try:
                if progress_func is not None:
                    if safe_start_callback_server():
                        try:
                            listener = ProgressListener(progress_func, "principal_component_analysis")
                            self._jobject.addSteppedListener(listener)
                        except Exception as e:
                            try:
                                close_callback_server()
                                log_error(e)
                                listener = None
                            finally:
                                e = None
                                del e

                java_result = self._jobject.pca(to_java_datasetgrid_array(spatial_variable_grids), int(sample_count), float(component_radio))
            except:
                import traceback
                log_error(traceback.format_exc())
                java_result = None

        finally:
            return

        if listener is not None:
            try:
                self._jobject.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if java_result:
            return PCAEigenResult._make_from_java_object(java_result)

    def pca_cellular_automata(self, parameter, out_data=None, out_dataset_name=None, progress_func=None, flush_func=None):
        """
        基于主成分分析的元胞自动机。

        :param parameter:  基于主成分分析的元胞自动机的参数。
        :type parameter: PCACellularAutomataParameter
        :param out_data: 输出结果数据集所在数据源。
        :type out_data: Datasource or str
        :param out_dataset_name: 输出结果数据集的名称。
        :type out_dataset_name: str
        :param progress_func: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
        :type progress_func: function
        :param flush_func: 元胞自动机刷新信息处理函数，具体参考 :py:class:`.CellularAutomataFlushedEvent`
        :type flush_func: function
        :return: 结果栅格数据集
        :rtype: DatasetGrid
        """
        if not isinstance(parameter, PCACellularAutomataParameter):
            raise ValueError("parameter must be PCACellularAutomataParameter")
        else:
            source_cell_grid = parameter.cellular_automata_parameter.cell_grid
            if out_data is not None:
                out_datasource = get_output_datasource(out_data)
            else:
                out_datasource = source_cell_grid.datasource
            check_output_datasource(out_datasource)
            if out_dataset_name is None:
                _dest_name = source_cell_grid.name + "_pca_ca"
            else:
                _dest_name = out_dataset_name
        _dest_name = out_datasource.get_available_dataset_name(_dest_name)
        flushed_listener = None
        listener = None
        try:
            try:
                if progress_func is not None or flush_func is not None:
                    if safe_start_callback_server():
                        if progress_func is not None:
                            try:
                                listener = ProgressListener(progress_func, "PCACA")
                                self._jobject.addSteppedListener(listener)
                            except Exception as e:
                                try:
                                    close_callback_server()
                                    log_error(e)
                                    listener = None
                                finally:
                                    e = None
                                    del e

                        if flush_func is not None:
                            try:
                                flushed_listener = CellularAutomataFlushedListener(flush_func, "PCACA")
                                self._jobject.addCAFlushedListener(flushed_listener)
                            except Exception as e:
                                try:
                                    close_callback_server()
                                    log_error(e)
                                    flushed_listener = None
                                finally:
                                    e = None
                                    del e

                java_result = self._jobject.pcaCellularAutomata(oj(out_datasource), _dest_name, oj(parameter))
            except:
                import traceback
                log_error(traceback.format_exc())
                java_result = None

        finally:
            if listener is not None:
                try:
                    self._jobject.removeSteppedListener(listener)
                except Exception as e1:
                    try:
                        log_error(e1)
                    finally:
                        e1 = None
                        del e1

            elif flushed_listener is not None:
                try:
                    self._jobject.removeCAFlushedListener(flushed_listener)
                except Exception as e1:
                    try:
                        log_error(e1)
                    finally:
                        e1 = None
                        del e1

                if listener or flushed_listener:
                    close_callback_server()
                if java_result is not None:
                    result_dt = out_datasource[_dest_name]
            else:
                result_dt = None
            if out_data is not None:
                return try_close_output_datasource(result_dt, out_datasource)
            return result_dt


class ANNParameter:
    __doc__ = "\n    人工神经网络参数设置。\n    "

    def __init__(self, is_custom_neighborhood=False, neighborhood_number=7, custom_neighborhoods=None, learning_rate=0.2, sample_count=1000):
        """
        初始化对象

        :param bool is_custom_neighborhood: 是否自定义邻域范围
        :param int neighborhood_number: 邻域范围
        :param list[list[bool]] custom_neighborhoods: 自定义邻域范围。
        :param float learning_rate: 学习速率
        :param int sample_count: 抽样数目
        """
        self._is_custom_neighborhood = False
        self._neighborhood_number = 7
        self._custom_neighborhoods = None
        self._learning_rate = 0.2
        self._sample_count = 1000
        self.set_custom_neighborhood(is_custom_neighborhood).set_neighborhood_number(neighborhood_number).set_custom_neighborhoods(custom_neighborhoods).set_learning_rate(learning_rate).set_sample_count(sample_count)

    @property
    def is_custom_neighborhood(self):
        """bool: 是否自定义邻域范围"""
        return self._is_custom_neighborhood

    def set_custom_neighborhood(self, value):
        """
        设置是否自定义邻域范围

        :param bool value: 是否自定义邻域范围
        :return: self
        :rtype: ANNParameter
        """
        self._is_custom_neighborhood = parse_bool(value)
        return self

    @property
    def neighborhood_number(self):
        """int: 邻域范围"""
        return self._neighborhood_number

    def set_neighborhood_number(self, value):
        """
        设置邻域范围

        :param int value: 邻域范围
        :return: self
        :rtype: ANNParameter
        """
        self._neighborhood_number = int(value)
        return self

    @property
    def custom_neighborhoods(self):
        """list[list[bool]]: 自定义领域范围"""
        return self._custom_neighborhoods

    def set_custom_neighborhoods(self, value):
        """
        设置自定义领域范围

        :param value: 自定义领域范围
        :type value: list[list[bool]]
        :return: self
        :rtype: ANNParameter
        """
        self._custom_neighborhoods = value
        return self

    @property
    def learning_rate(self):
        """float: 学习速率"""
        return self._learning_rate

    def set_learning_rate(self, value):
        """
        设置学习速率

        :param float value: 学习速率
        :return: self
        :rtype: ANNParameter
        """
        self._learning_rate = float(value)
        return self

    @property
    def sample_count(self):
        """int: 抽样数目"""
        return self._sample_count

    def set_sample_count(self, value):
        """
        设置抽样数目

        :param int value: 抽样数目
        :return: self
        :rtype: ANNParameter
        """
        self._sample_count = int(value)
        return self

    @property
    def _jobject(self):
        java_object = get_jvm().com.supermap.analyst.spatialanalyst.ANNParameter()
        java_object.setCustomNeighborhood(parse_bool(self.is_custom_neighborhood))
        if self.custom_neighborhoods:
            java_object.setCustomNeighborhoods(to_java_2d_array(self.custom_neighborhoods, get_jvm().boolean))
        java_object.setLearningRate(float(self.learning_rate))
        java_object.setNeighborhoodNumber(int(self.neighborhood_number))
        java_object.setSampleCount(int(self.sample_count))
        return java_object


class ANNTrainResult:
    __doc__ = "\n    人工神经网络（ANN）训练结果\n    "

    def __init__(self, java_object):
        self._accuracy = java_object.getAccuracy()
        java_iterator_result = java_object.getIterationResults()
        self._convert_values = {}
        if java_iterator_result:
            for result in java_iterator_result:
                self._convert_values[result.getIterations()] = result.getError()

    @property
    def accuracy(self):
        """float: 训练正确率"""
        return self._accuracy

    @property
    def convert_values(self):
        """dict[int, error]: 训练迭代结果, key 为迭代次数，value 为错误率"""
        return self._convert_values


class ANNCellularAutomataParameter:
    __doc__ = "\n    基于人工神经网络的元胞自动机参数设置。\n    "

    def __init__(self):
        self._ca_parameter = None
        self._is_check_result = True
        self._end_cell_grid = None
        self._threshold = 0.75
        self._alpha = 2
        self._conversion_rules = None
        self._conversion_class_ids = None

    @property
    def end_cell_grid(self):
        """DatasetGrid: 终止栅格数据集"""
        return self._end_cell_grid

    def set_end_cell_grid(self, value):
        """
        设置终止栅格数据集。当 :py:attr:`.is_check_result` 为 True 时必须设置

        :param value: 终止栅格数据集
        :type value: DatasetGrid or str
        :return: self
        :rtype: ANNCellularAutomataParameter
        """
        self._end_cell_grid = get_input_dataset(value)
        return self

    @property
    def threshold(self):
        """float: 元胞转变概率阈值"""
        return self._threshold

    def set_threshold(self, value):
        """
        设置元胞转变概率阈值

        :param float value: 元胞转变概率阈值
        :return: self
        :rtype: ANNCellularAutomataParameter
        """
        self._threshold = float(value)
        return self

    @property
    def alpha(self):
        """int: 扩散参数"""
        return self._alpha

    def set_alpha(self, value):
        """
        设置扩散参数

        :param int value: 扩散参数。一般1-10。
        :return: self
        :rtype: ANNCellularAutomataParameter
        """
        self._alpha = int(value)
        return self

    @property
    def conversion_rules(self):
        """list[list[bool]]: 元胞自动机转换规则"""
        return self._conversion_rules

    def set_conversion_rules(self, value):
        """
        设置元胞自动机转换规则。

        :param value: 设置元胞自动机转换规则
        :type value: list[list[bool]]
        :return: self
        :rtype: ANNCellularAutomataParameter
        """
        self._conversion_rules = value
        return self

    @property
    def conversion_class_ids(self):
        """list[int]: 元胞自动机转换规则的分类ID（即栅格值）数组"""
        return self._conversion_class_ids

    def set_conversion_class_ids(self, value):
        """
        设置元胞自动机转换规则的分类 ID（即栅格值）数组

        :param value: 元胞自动机转换规则的分类ID（即栅格值）数组
        :type value: list[int] or tuple[int]
        :return: self
        :rtype: ANNCellularAutomataParameter
        """
        self._conversion_class_ids = split_input_int_list_from_str(value)
        return self

    @property
    def is_check_result(self):
        """bool: 是否检测结果"""
        return self._is_check_result

    def set_check_result(self, value):
        """
        设置是否检测结果

        :param bool value: 是否检测结果
        :return: self
        :rtype: ANNCellularAutomataParameter
        """
        self._is_check_result = parse_bool(value)
        return self

    @property
    def cellular_automata_parameter(self):
        """CellularAutomataParameter: 元胞自动机的参数"""
        return self._ca_parameter

    def set_cellular_automata_parameter(self, value):
        """
        设置元胞自动机的参数

        :param value: 元胞自动机的参数
        :type value: CellularAutomataParameter
        :return: self
        :rtype: ANNCellularAutomataParameter
        """
        if isinstance(value, CellularAutomataParameter):
            self._ca_parameter = value
        return self

    @property
    def _jobject(self):
        java_object = get_jvm().com.supermap.analyst.spatialanalyst.ANNCellularAutomataParameter()
        if self.cellular_automata_parameter:
            java_object.setCellularAutomataParameter(oj(self.cellular_automata_parameter))
        java_object.setCheckResult(parse_bool(self.is_check_result))
        if self.end_cell_grid:
            java_object.setEndCellGrid(oj(self.end_cell_grid))
        java_object.setThreshold(float(self.threshold))
        java_object.setAlpha(int(self.alpha))
        if self.conversion_class_ids:
            java_object.setConversionClassIDs(to_java_int_array(self.conversion_class_ids))
        if self.conversion_rules:
            java_object.setConversionRules(to_java_2d_array(self.conversion_rules, get_jvm().boolean))
        return java_object


class ANNCellularAutomataResult:
    __doc__ = "基于人工神经网络的元胞自动机结果"

    def __init__(self, convert_values, accuracies, result_dataset):
        self._convert_values = convert_values
        self._accuracies = accuracies
        self._result_dataset = result_dataset

    @property
    def convert_values(self):
        """list[float]: 转换值数组，为转换规则的栅格类型"""
        return self._convert_values

    @property
    def accuracies(self):
        """list[float]: 正确率"""
        return self._accuracies

    @property
    def result_dataset(self):
        """DatasetGrid: 元胞自动机的栅格结果数据集"""
        return self._result_dataset


class ANNCellularAutomata(JVMBase):
    __doc__ = "\n    基于人工神经网络的元胞自动机。\n    "

    def __init__(self):
        JVMBase.__init__(self)

    def _make_java_object(self):
        return get_jvm().com.supermap.analyst.spatialanalyst.ANNCellularAutomata()

    def initialize_ann(self, train_start_cell_grid, train_end_cell_grid, ann_train_values, spatial_variable_grids, ann_parameter):
        """
        初始化基于人工神经网络的元胞自动机

        :param train_start_cell_grid: 训练起始栅格数据集
        :type train_start_cell_grid: DatasetGrid or str
        :param train_end_cell_grid: 训练终止栅格数据集
        :type train_end_cell_grid: DatasetGrid or str
        :param ann_train_values:
        :type ann_train_values: list[int] or tuple[int]
        :param spatial_variable_grids: 空间变量栅格数据集
        :type spatial_variable_grids: list[DatasetGrid] or list[str]
        :param ann_parameter: 人工神经网络训练参数设置。
        :type ann_parameter: ANNParameter
        :return: 是否初始化成功
        :rtype: bool
        """
        train_start_cell_grid = get_input_dataset(train_start_cell_grid)
        train_end_cell_grid = get_input_dataset(train_end_cell_grid)
        ann_train_values = split_input_int_list_from_str(ann_train_values)
        if spatial_variable_grids:
            if not isinstance(spatial_variable_grids, (list, tuple)):
                spatial_variable_grids = [
                 spatial_variable_grids]
            for i, grid in enumerate(spatial_variable_grids):
                spatial_variable_grids[i] = get_input_dataset(grid)

        else:
            spatial_variable_grids = []
        spatial_variable_grids = list(filter((lambda dt: isinstance(dt, DatasetGrid)), spatial_variable_grids))
        return self._jobject.initializeAnn(oj(train_start_cell_grid), oj(train_end_cell_grid), to_java_int_array(ann_train_values), to_java_datasetgrid_array(spatial_variable_grids), oj(ann_parameter))

    def ann_train(self, error_rate, max_times):
        """
        人工神经网络训练。

        :param float error_rate: 人工神经网络训练终止条件，误差期望值。
        :param int max_times: 人工神经网络训练终止条件，迭代最大次数。
        :return: 人工神经网络训练结果
        :rtype: ANNTrainResult
        """
        java_result = self._jobject.annTrain(float(error_rate), int(max_times))
        if java_result is not None:
            return ANNTrainResult(java_result)
        return

    def ann_cellular_automata(self, parameter, out_data=None, out_dataset_name=None, progress_func=None, flush_func=None):
        """
        基于人工神经网络的元胞自动机。

        :param parameter: 基于人工神经网络的元胞自动机参数。
        :type parameter: ANNCellularAutomataParameter
        :param out_data: 输出数据集所在数据源。
        :type out_data: Datasource or DatasourceConnectionInfo or str
        :param str out_dataset_name: 输出数据集的名称。
        :param progress_func: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
        :type progress_func: function
        :param flush_func: 胞自动机刷新信息处理函数，具体参考 :py:class:`.CellularAutomataFlushedEvent`
        :type flush_func: function
        :return: 基于人工神经网络的元胞自动机的结果，包括土地类型（如果有）、准确率(如果有)、结果栅格数据集。
        :rtype: ANNCellularAutomataResult
        """
        if not isinstance(parameter, ANNCellularAutomataParameter):
            raise ValueError("parameter must be ANNCellularAutomataParameter")
        else:
            source_cell_grid = parameter.cellular_automata_parameter.cell_grid
            if out_data is not None:
                out_datasource = get_output_datasource(out_data)
            else:
                out_datasource = source_cell_grid.datasource
            check_output_datasource(out_datasource)
            if out_dataset_name is None:
                _dest_name = source_cell_grid.name + "_ann_ca"
            else:
                _dest_name = out_dataset_name
            _dest_name = out_datasource.get_available_dataset_name(_dest_name)
            flushed_listener = None
            listener = None
            try:
                try:
                    if progress_func is not None or flush_func is not None:
                        if safe_start_callback_server():
                            if progress_func is not None:
                                try:
                                    listener = ProgressListener(progress_func, "ANNCA")
                                    self._jobject.addSteppedListener(listener)
                                except Exception as e:
                                    try:
                                        close_callback_server()
                                        log_error(e)
                                        listener = None
                                    finally:
                                        e = None
                                        del e

                            if flush_func is not None:
                                try:
                                    flushed_listener = CellularAutomataFlushedListener(flush_func, "ANNCA")
                                    self._jobject.addCAFlushedListener(flushed_listener)
                                except Exception as e:
                                    try:
                                        close_callback_server()
                                        log_error(e)
                                        flushed_listener = None
                                    finally:
                                        e = None
                                        del e

                    java_result = self._jobject.annCellularAutomata(oj(out_datasource), _dest_name, oj(parameter))
                except:
                    import traceback
                    log_error(traceback.format_exc())
                    java_result = None

            finally:
                return

            if listener is not None:
                try:
                    self._jobject.removeSteppedListener(listener)
                except Exception as e1:
                    try:
                        log_error(e1)
                    finally:
                        e1 = None
                        del e1

            if flushed_listener is not None:
                try:
                    self._jobject.removeCAFlushedListener(flushed_listener)
                except Exception as e1:
                    try:
                        log_error(e1)
                    finally:
                        e1 = None
                        del e1

            if not listener:
                if flushed_listener:
                    close_callback_server()
                if java_result is not None:
                    result_dt = out_datasource[_dest_name]
            else:
                result_dt = None
        if out_data is not None:
            result_dt = try_close_output_datasource(result_dt, out_datasource)
        if java_result:
            return ANNCellularAutomataResult(java_array_to_list(java_result.getConvertValues()), java_array_to_list(java_result.getAccuracys()), result_dt)
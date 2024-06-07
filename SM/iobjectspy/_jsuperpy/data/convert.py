# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/_jsuperpy\data\convert.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 33255 bytes
from ..enums import LineToPointMode, RegionToPointMode, AttributeStatisticsMode
from .dt import DatasetVector
from ._util import check_output_datasource, get_input_dataset, get_output_datasource, try_close_output_datasource
from .._gateway import get_jvm
from .._logger import log_error
from .._utils import oj, split_input_list_from_str, split_input_list_tuple_item_from_str
__all__ = [
 'dataset_dim2_to_dim3', 'dataset_dim3_to_dim2', 'dataset_point_to_line', 'dataset_line_to_point', 
 'dataset_line_to_region', 
 'dataset_region_to_line', 'dataset_region_to_point', 'dataset_field_to_text', 
 'dataset_text_to_field', 
 'dataset_text_to_point', 'dataset_field_to_point', 'dataset_network_to_line', 
 'dataset_network_to_point']

def dataset_dim2_to_dim3(source, z_field_or_value, line_to_z_field=None, saved_fields=None, out_data=None, out_dataset_name=None):
    """
    将二维数据集转换为三维数据集，二维的点、线和面数据集将会分别转换为三维的点、线和面数据集。

    :param source: 二维数据集，支持点、线和面数据集
    :type source: DatasetVector or str
    :param z_field_or_value: z 值的来源字段名称或指定的 z 值，如果为字段，则必须是数值型字段。
    :type z_field_or_value: str or float
    :param line_to_z_field: 当输入的是二维线数据集时，用于指定终止 z 值的字段名称，则 z_field_or_value 则作为起始 z 值的字段的名称。
                            line_to_z_field 必须为字段名称，不支持指定的 z 值。
    :type line_to_z_field: str
    :param saved_fields:  将要保留的字段名称
    :type saved_fields: list[str] or str
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :return: 结果三数据集或数据集名称
    :rtype: DatasetVector or str
    """
    source_dt = get_input_dataset(source)
    if not isinstance(source_dt, DatasetVector):
        raise ValueError("source required DatasetVector, but is " + str(type(source)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    saved_fields = split_input_list_from_str(saved_fields)
    try:
        try:
            if isinstance(z_field_or_value, (int, float)):
                z_field_or_value = float(z_field_or_value)
                java_result = get_jvm().com.supermap.jsuperpy.Converts.convertDatasetDim2To3(oj(source_dt), z_field_or_value, saved_fields, oj(out_datasource), _outDatasetName)
            else:
                z_field_or_value = str(z_field_or_value)
                java_result = get_jvm().com.supermap.jsuperpy.Converts.convertDatasetDim2To3(oj(source_dt), z_field_or_value, line_to_z_field, saved_fields, oj(out_datasource), _outDatasetName)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if java_result is None:
            result_dt = None
        else:
            result_dt = out_datasource[_outDatasetName]
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def dataset_dim3_to_dim2(source, out_z_field='Z', saved_fields=None, out_data=None, out_dataset_name=None):
    """
    将三维的点、线和面数据集转换为二维的点、线和面数据集。

    :param source: 三维数据集，支持三维点、线和面数据集
    :type source: DatasetVector or str
    :param out_z_field: 保留 Z 值的字段，如果为 None 或不合法，将会获取到一个有效的字段用于存储对象的 Z 值
    :type out_z_field: str
    :param saved_fields: 需要保留的字段名称
    :type saved_fields: list[str] or str
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :return: 结果二维数据集或数据集名称
    :rtype: DatasetVector or str
    """
    source_dt = get_input_dataset(source)
    if not isinstance(source_dt, DatasetVector):
        raise ValueError("source required DatasetVector, but is " + str(type(source)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    saved_fields = split_input_list_from_str(saved_fields)
    try:
        try:
            java_result = get_jvm().com.supermap.jsuperpy.Converts.convertDatasetDim3To2(oj(source_dt), out_z_field, saved_fields, oj(out_datasource), _outDatasetName)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if java_result is None:
            result_dt = None
        else:
            result_dt = out_datasource[_outDatasetName]
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def dataset_point_to_line(source, group_fields=None, order_fields=None, field_stats=None, out_data=None, out_dataset_name=None):
    """
    将二维点数据集中点对象，根据分组字段进行分组构造线对象，返回一个二维线数据集

    :param source: 二维点数据集
    :type source: DatasetVector or str
    :param group_fields: 二维点数据集中用于分组的字段名称，只有分组字段名称的字段值都相等时才会将点连接成线。
    :type group_fields: list[str]
    :param order_fields: 排序字段，同一分组内的点，按照排序字段的字段值的升序进行排序，再连接成线。如果为 None，则默认使用 SmID 字段进行排序。
    :type order_fields: list[str] or str
    :param field_stats: 字段统计信息，同一分组内的点属性进行字段统计。为一个list，list中每个元素为一个 tuple，tuple的大小为2，tuple的第一个元素为被统计的字段名称，tuple的第二个元素为统计类型。
                        注意，不支持 :py:attr:`AttributeStatisticsMode.MAXINTERSECTAREA`
    :type field_stats: list[tuple(str,AttributeStatisticsMode)] or list[tuple(str,str)] or str
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :return: 二维点数据集或数据集名称
    :rtype: DatasetVector or str
    """
    source_dt = get_input_dataset(source)
    if not isinstance(source_dt, DatasetVector):
        raise ValueError("source required DatasetVector, but is " + str(type(source)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    group_fields = split_input_list_from_str(group_fields)
    order_fields = split_input_list_from_str(order_fields)
    stat_fields = None
    stat_modes = None
    if field_stats is not None:
        stats = split_input_list_tuple_item_from_str(field_stats)
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
            java_result = get_jvm().com.supermap.jsuperpy.Converts.convertDatasetPointToLine(oj(source_dt), group_fields, order_fields, stat_fields, stat_modes, oj(out_datasource), _outDatasetName)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if java_result is None:
            result_dt = None
        else:
            result_dt = out_datasource[_outDatasetName]
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def dataset_line_to_point(source, mode='VERTEX', saved_fields=None, out_data=None, out_dataset_name=None):
    """
    将线数据集转换为点数据集

    :param source: 二维线数据集
    :type source: DatasetVector or str
    :param mode: 线对象转换为点对象的方式
    :type mode: LineToPointMode or str
    :param saved_fields: 需要保留的字段名称
    :type saved_fields: list[str] or str
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :return: 结果二维点数据集或数据集名称
    :rtype: DatasetVector or str
    """
    source_dt = get_input_dataset(source)
    if not isinstance(source_dt, DatasetVector):
        raise ValueError("source required DatasetVector, but is " + str(type(source)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    saved_fields = split_input_list_from_str(saved_fields)
    try:
        try:
            java_result = get_jvm().com.supermap.jsuperpy.Converts.convertDatasetLineToPoint(oj(source_dt), oj(LineToPointMode._make(mode, "VERTEX")), saved_fields, oj(out_datasource), _outDatasetName)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if java_result is None:
            result_dt = None
        else:
            result_dt = out_datasource[_outDatasetName]
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def dataset_line_to_region(source, saved_fields=None, out_data=None, out_dataset_name=None):
    """
    将线数据集转换为面数据集。此方法将线对象直接转换为面对象，如果线对象不是首位相接，可能会转换失败。如果要将线数据集转换为面数据集，更
    可靠的方式的是拓扑构面 :py:func:`.topology_build_regions`

    :param source: 二维线数据集
    :type source: DatasetVector or str
    :param saved_fields: 需要保留的字段名称
    :type saved_fields: list[str] or str
    :param out_data: 结果数据集所在的数据源信息
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :return: 结果二维面数据集或数据集名称
    :rtype: DatasetVector or str
    """
    source_dt = get_input_dataset(source)
    if not isinstance(source_dt, DatasetVector):
        raise ValueError("source required DatasetVector, but is " + str(type(source)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    saved_fields = split_input_list_from_str(saved_fields)
    try:
        try:
            java_result = get_jvm().com.supermap.jsuperpy.Converts.convertDatasetLineToRegion(oj(source_dt), saved_fields, oj(out_datasource), _outDatasetName)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if java_result is None:
            result_dt = None
        else:
            result_dt = out_datasource[_outDatasetName]
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def dataset_region_to_line(source, saved_fields=None, out_data=None, out_dataset_name=None):
    """
    将二维面对象转换为线数据集。此方法会将每个点对象直接转换为线对象，如果需要提取不包含重复线的线数据集，可以使用 :py:func:`.pickup_border`

    :param source: 二维面数据集
    :type source: DatasetVector or str
    :param saved_fields: 需要保留的字段名称
    :type saved_fields: list[str] or str
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :return: 结果线数据集或数据集名称
    :rtype: DatasetVector or str
    """
    source_dt = get_input_dataset(source)
    if not isinstance(source_dt, DatasetVector):
        raise ValueError("source required DatasetVector, but is " + str(type(source)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    saved_fields = split_input_list_from_str(saved_fields)
    try:
        try:
            java_result = get_jvm().com.supermap.jsuperpy.Converts.convertDatasetRegionToLine(oj(source_dt), saved_fields, oj(out_datasource), _outDatasetName)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if java_result is None:
            result_dt = None
        else:
            result_dt = out_datasource[_outDatasetName]
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def dataset_region_to_point(source, mode='INNER_POINT', saved_fields=None, out_data=None, out_dataset_name=None):
    """
    将二维面数据集转换为点数据集

    :param source: 二维面数据集
    :type source: DatasetVector or str
    :param mode: 面对象转换为点对象的方式
    :type mode: RegionToPointMode or str
    :param saved_fields: 需要保留的字段名称
    :type saved_fields: list[str] or str
    :param out_data: 结果数据集所在的数据源信息
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :return: 结果二维点数据集或数据集名称
    :rtype: DatasetVector or str
    """
    source_dt = get_input_dataset(source)
    if not isinstance(source_dt, DatasetVector):
        raise ValueError("source required DatasetVector, but is " + str(type(source)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    saved_fields = split_input_list_from_str(saved_fields)
    mode = RegionToPointMode._make(mode, "INNER_POINT")
    try:
        try:
            java_result = get_jvm().com.supermap.jsuperpy.Converts.convertDatasetRegionToPoint(oj(source_dt), oj(mode), saved_fields, oj(out_datasource), _outDatasetName)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if java_result is None:
            result_dt = None
        else:
            result_dt = out_datasource[_outDatasetName]
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def dataset_field_to_text(source, field, saved_fields=None, out_data=None, out_dataset_name=None):
    """
    将点数据集转换为文本数据集

    :param source: 输入的二维点数据集
    :type source: DatasetVector or str
    :param str field: 包含文本信息的字段，用于构造文本几何对象的文本信息。
    :param saved_fields: 需要保留的字段名称
    :type saved_fields: list[str] or str
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :return: 结果文本数据集或数据集名称
    :rtype: DatasetVector or str
    """
    source_dt = get_input_dataset(source)
    if not isinstance(source_dt, DatasetVector):
        raise ValueError("source required DatasetVector, but is " + str(type(source)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    saved_fields = split_input_list_from_str(saved_fields)
    try:
        try:
            java_result = get_jvm().com.supermap.jsuperpy.Converts.convertDatasetFieldToText(oj(source_dt), field, saved_fields, oj(out_datasource), _outDatasetName)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if java_result is None:
            result_dt = None
        else:
            result_dt = out_datasource[_outDatasetName]
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def dataset_text_to_field(source, out_field='Text'):
    """
    将二维文本数据集的文本信息存储到字段中。文本对象的文本信息将会存储在指定的 out_field 字段中。

    :param source: 输入的二维文本数据集。
    :type source: DatasetVector or str
    :param out_field: 存储文本信息的字段名称。如果 out_field 指定的字段名称已经存在，必须为文本型字段。如果不存在，将会新建一个文本型字段。
    :type out_field: str
    :return: 成功返回 True，否则返回  False。
    :rtype: bool
    """
    source_dt = get_input_dataset(source)
    if not isinstance(source_dt, DatasetVector):
        raise ValueError("source required DatasetVector, but is " + str(type(source)))
    try:
        try:
            java_result = get_jvm().com.supermap.jsuperpy.Converts.convertDatasetTextToField(oj(source_dt), out_field)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = False

    finally:
        return

    return java_result


def dataset_text_to_point(source, out_field='Text', saved_fields=None, out_data=None, out_dataset_name=None):
    """
    将二维文本数据集转换为点数据集，文本对象的文本信息将会存储在指定的 out_field 字段中

    :param source: 输入的二维文本数据集
    :type source: DatasetVector or str
    :param str out_field: 存储文本信息的字段名称。如果 out_field 指定的字段名称已经存在，必须为文本型字段。如果不存在，将会新建一个文本型字段。
    :param saved_fields:  需要保留的字段名称。
    :type saved_fields: list[str] or str
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :return: 二维点数据集或数据集名称
    :rtype: DatasetVector or str
    """
    source_dt = get_input_dataset(source)
    if not isinstance(source_dt, DatasetVector):
        raise ValueError("source required DatasetVector, but is " + str(type(source)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    saved_fields = split_input_list_from_str(saved_fields)
    try:
        try:
            java_result = get_jvm().com.supermap.jsuperpy.Converts.convertDatasetTextToPoint(oj(source_dt), out_field, saved_fields, oj(out_datasource), _outDatasetName)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if java_result is None:
            result_dt = None
        else:
            result_dt = out_datasource[_outDatasetName]
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def dataset_field_to_point(source, x_field, y_field, z_field=None, saved_fields=None, out_data=None, out_dataset_name=None):
    """
    根据数据集中字段，构造二维点数据集或三维点数据集。如果指定了有效的 z_field将会得到三维点数据集，否则将会得到二维点数据集

    :param source: 提供数据的数据集，可以为属性表或点、线、面等数据集
    :type source: DatasetVector or str
    :param x_field: x 坐标值的来源字段，必须有效。
    :type x_field: str
    :param y_field: y 坐标值的来源字段，必须有效。
    :type y_field: str
    :param z_field: z 坐标值的来源字段，可选。
    :type z_field: str
    :param saved_fields: 需要保留的字段名称。
    :type saved_fields: list[str] or str
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :return: 二维点或三维点数据集或数据集名称
    :rtype: DatasetVector or str
    """
    source_dt = get_input_dataset(source)
    if not isinstance(source_dt, DatasetVector):
        raise ValueError("source required DatasetVector, but is " + str(type(source)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    saved_fields = split_input_list_from_str(saved_fields)
    try:
        try:
            java_result = get_jvm().com.supermap.jsuperpy.Converts.convertDatasetFieldToPoint(oj(source_dt), x_field, y_field, z_field, saved_fields, oj(out_datasource), _outDatasetName)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if java_result is None:
            result_dt = None
        else:
            result_dt = out_datasource[_outDatasetName]
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def dataset_network_to_line(source, saved_fields=None, out_data=None, out_dataset_name=None):
    """
    将二维网络数据集的转换为线数据集，网络数据集的 SmEdgeID、SmFNode和SmTNode 字段值将会存储在结果数据集的 EdgeID、FNode和TNode 字段
    中，如果  EdgeID、FNode 或 TNode 已被占用，会获取到一个有效的字段。

    :param source: 被转换的二维网络数据集
    :type source: DatasetVector or str
    :param saved_fields: 需要保存的字段名称。
    :type saved_fields: list[str] or str
    :param out_data: 结果数据集所在的数据源信息
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :return: 结果二维线数据集或数据集名称
    :rtype: DatasetVector or str
    """
    source_dt = get_input_dataset(source)
    if not isinstance(source_dt, DatasetVector):
        raise ValueError("source required DatasetVector, but is " + str(type(source)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    saved_fields = split_input_list_from_str(saved_fields)
    try:
        try:
            java_result = get_jvm().com.supermap.jsuperpy.Converts.convertDatasetNetworkToLine(oj(source_dt), saved_fields, oj(out_datasource), _outDatasetName)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if java_result is None:
            result_dt = None
        else:
            result_dt = out_datasource[_outDatasetName]
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def dataset_network_to_point(source, saved_fields=None, out_data=None, out_dataset_name=None):
    """
    将二维网络数据集的点子数据集转换为点数据集，网络数据集的 SmNodeID 字段值将会存储在结果数据集的 NodeID 字段中，如果 NodeID 已被占用，会获取到一个有效的字段。

    :param source: 被转换的二维网络数据集
    :type source: DatasetVector or str
    :param saved_fields: 需要保存的字段名称。
    :type saved_fields: list[str] or str
    :param out_data: 结果数据集所在的数据源信息
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :return: 结果二维点数据集或数据集名称
    :rtype: DatasetVector or str
    """
    source_dt = get_input_dataset(source)
    if not isinstance(source_dt, DatasetVector):
        raise ValueError("source required DatasetVector, but is " + str(type(source)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    saved_fields = split_input_list_from_str(saved_fields)
    try:
        try:
            java_result = get_jvm().com.supermap.jsuperpy.Converts.convertDatasetNetworkToPoint(oj(source_dt), saved_fields, oj(out_datasource), _outDatasetName)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if java_result is None:
            result_dt = None
        else:
            result_dt = out_datasource[_outDatasetName]
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt

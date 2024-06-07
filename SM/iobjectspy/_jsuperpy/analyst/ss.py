# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/_jsuperpy\analyst\ss.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 157847 bytes
"""
空间统计模块
"""
from iobjectspy._jsuperpy._gateway import get_gateway, get_jvm, safe_start_callback_server, close_callback_server
from iobjectspy._jsuperpy.data import Datasource, DatasetVector
from iobjectspy._jsuperpy.data._listener import ProgressListener
from iobjectspy._jsuperpy.data._util import get_input_dataset, get_output_datasource, check_output_datasource, try_close_output_datasource
from iobjectspy._jsuperpy.enums import *
from iobjectspy._jsuperpy._utils import *
from iobjectspy._jsuperpy._logger import *
from enum import unique
__all__ = [
 'measure_central_element', 'measure_directional', 'measure_linear_directional_mean', 
 'measure_mean_center', 
 'measure_median_center', 'measure_standard_distance', 
 'AnalyzingPatternsResult', 'auto_correlation', 
 'high_or_low_clustering', 
 'average_nearest_neighbor', 'incremental_auto_correlation', 'IncrementalResult', 
 'cluster_outlier_analyst', 
 'hot_spot_analyst', 'optimized_hot_spot_analyst', 'collect_events', 
 'build_weight_matrix', 
 'weight_matrix_file_to_table', 'GWR', 'GWRSummary', 'OLSSummary', 
 'ordinary_least_squares', 
 'InteractionDetectorResult', 'RiskDetectorMean', 'RiskDetectorResult', 
 'GeographicalDetectorResult', 
 'geographical_detector', 
 'density_based_clustering', 'hierarchical_density_based_clustering', 
 'ordering_density_based_clustering', 
 'spa_estimation', 'bshade_estimation', 
 'bshade_sampling', 'BShadeSamplingResult', 'BShadeEstimationResult', 
 'BShadeSampleNumberMethod', 
 'BShadeEstimateMethod', 'BShadeSamplingParameter']

def _to_java_spatial_stat_type_array(values):
    if values is None:
        return
        jvm = get_jvm()
        if isinstance(values, SpatialStatisticsType):
            java_array = get_gateway().new_array(jvm.com.supermap.analyst.spatialstatistics.StatisticsType, 1)
            java_array[0] = oj(values)
            return java_array
        if isinstance(values, (list, tuple, set)):
            _size = len(values)
            java_array = get_gateway().new_array(jvm.com.supermap.analyst.spatialstatistics.StatisticsType, _size)
            i = 0
            for value in values:
                if isinstance(value, SpatialStatisticsType):
                    java_array[i] = oj(value)
                else:
                    if isinstance(value, (str, int)):
                        v = SpatialStatisticsType._make(value)
                        if v is not None:
                            java_array[i] = oj(v)
                    else:
                        java_array[i] = value
                i += 1

            return java_array
        java_array = get_gateway().new_array(jvm.com.supermap.analyst.spatialstatistics.StatisticsType, 1)
        if isinstance(values, (str, int)):
            v = SpatialStatisticsType._make(values)
            if v is not None:
                java_array[0] = oj(v)
    else:
        java_array[0] = values
    return java_array


def _measure_param(group_field=None, weight_field=None, self_weight_field=None, distance_method='EUCLIDEAN', stats_fields=None, ellipse_size=None, is_orientation=None):
    java_param = get_jvm().com.supermap.analyst.spatialstatistics.MeasureParameter()
    java_param.setGroupFieldName(group_field)
    if weight_field is not None:
        java_param.setWeightFieldName(weight_field)
    elif self_weight_field is not None:
        java_param.setSelfWeightFieldName(self_weight_field)
    if distance_method is not None:
        java_param.setDistanceMethod(oj(DistanceMethod._make(distance_method)))
    if isinstance(stats_fields, (list, str)):
        fields = []
        stat_types = []
        stats_fields = split_input_list_tuple_item_from_str(stats_fields)
        if isinstance(stats_fields, list):
            for f, t in stats_fields:
                t = SpatialStatisticsType._make(t)
                if t is not None:
                    fields.append(str(f))
                    stat_types.append(oj(t))

    else:
        fields = None
        stat_types = None
    if fields is not None:
        if len(fields) > 0:
            java_param.setStatisticsFieldNames(to_java_string_array(fields))
            java_param.setStatisticsTypes(_to_java_spatial_stat_type_array(stat_types))
    if ellipse_size is not None:
        java_param.setEllipseSize(oj(EllipseSize._make(ellipse_size)))
    if is_orientation is not None:
        java_param.setOrientation(parse_bool(is_orientation))
    return java_param


def measure_central_element(source, group_field=None, weight_field=None, self_weight_field=None, distance_method='EUCLIDEAN', stats_fields=None, out_data=None, out_dataset_name=None, progress=None):
    """
    关于空间度量：

        空间度量用来计算的数据可以是点、线、面。对于点、线和面对象，在距离计算中会使用对象的质心。对象的质心为所有子对象的加权
        平均中心。点对象的加权项为1（即质心为自身），线对象的加权项是长度，而面对象的加权项是面积。

        用户可以通过空间度量计算来解决以下问题：

            1. 数据的中心在哪里？

            2. 数据的分布呈什么形状和方向？

            3. 数据是如何分散布局？

        空间度量包括中心要素（ :py:func:`measure_central_element` ）、方向分布（ :py:func:`measure_directional` ）、
        标准距离（ :py:func:`measure_standard_distance` ）、方向平均值（ :py:func:`measure_linear_directional_mean` ）、
        平均中心（ :py:func:`measure_mean_center` ）、中位数中心（ :py:func:`measure_median_center` ）等。

    计算矢量数据的中心要素，返回结果矢量数据集。

     * 中心要素是与其他所有对象质心的累积距离最小，位于最中心的对象。

     * 如果设置了分组字段，则结果矢量数据集将包含 “分组字段名_Group” 字段。

     * 实际上，距其他所有对象质心的累积距离最小的中心要素可能会有多个，但中心要素方法只会输出SmID 字段值最小的对象。

    :param source: 待计算的数据集。可以为点、线、面数据集。
    :type source: DatasetVector or str
    :param str group_field: 分组字段的名称
    :param str weight_field: 权重字段的名称
    :param str self_weight_field: 自身权重字段的名称
    :param distance_method: 距离计算方法类型
    :type distance_method: DistanceMethod or str
    :param stats_fields: 统计字段的类型，为一个字典类型，字典类型的 key 为字段名，value 为统计类型。
    :type stats_fields: list[tuple[str,SpatialStatisticsType]] or list[tuple[str,str]] or str
    :param out_data: 用于存储结果数据集的数据源
    :type out_data: DatasourceConnectionInfo or Datasource or str
    :param str out_dataset_name: 结果数据集名称
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 结果矢量数据集或数据集名称
    :rtype: DatasetVector or str
    """
    check_lic()
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
            _outDatasetName = source_dt.name + "_measure"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "measure_central_element")
                        get_jvm().com.supermap.analyst.spatialstatistics.SpatialMeasure.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_param = _measure_param(group_field, weight_field, self_weight_field, distance_method, stats_fields)
            measureCentralElement = get_jvm().com.supermap.analyst.spatialstatistics.SpatialMeasure.measureCentralElement
            java_result = measureCentralElement(oj(source_dt), oj(out_datasource), _outDatasetName, java_param)
            del java_param
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialstatistics.SpatialMeasure.removeSteppedListener(listener)
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


def measure_directional(source, group_field=None, ellipse_size='SINGLE', stats_fields=None, out_data=None, out_dataset_name=None, progress=None):
    """
    计算矢量数据的方向分布，返回结果矢量数据集。

     * 方向分布是根据所有对象质心的平均中心（有权重，为加权）为圆点，计算x和y坐标的标准差为轴得到的标准差椭圆。

     * 标准差椭圆的圆心x和y坐标、两个标准距离（长半轴和短半轴）、椭圆的方向，分别储存在结果矢量数据集中的CircleCenterX、
       CircleCenterY、SemiMajorAxis、SemiMinorAxis、RotationAngle字段中。如果设置了分组字段，则结果矢量数据集将包含
       “分组字段名_Group” 字段。

     * 椭圆的方向RotationAngle字段中的正值表示正椭圆（长半轴的方向为X轴方向, 短半轴的方向为Y轴方向)）按逆时针旋转，负值表示
       正椭圆按顺时针旋转。

     * 输出的椭圆大小有三个级别：Single（一个标准差）、Twice（二个标准差）和Triple（三个标准差），详细介绍请参见 :py:class:`.EllipseSize` 类。

     * 用于计算方向分布的标准差椭圆算法是由D. Welty Lefever在1926年提出，用来度量数据的方向和分布。首先确定椭圆的圆心，即平均
       中心（有权重，为加权）；然后确定椭圆的方向；最后确定长轴和短轴的长度。

     .. image:: ../image/MeasureDirection.png

    关于空间度量介绍，请参考 :py:func:`measure_central_element`

    :param source: 待计算的数据集。可以为点、线、面数据集。
    :type source: DatasetVector or str
    :param str group_field: 分组字段名称
    :param ellipse_size: 椭圆大小类型
    :type ellipse_size: EllipseSize or str
    :param stats_fields: 统计字段的类型，为一个list类型，list 中存储2个元素的tuple，tuple的第一个元素为被统计的字段，第二个元素为统计类型
    :type stats_fields: list[tuple[str,SpatialStatisticsType]] or list[tuple[str,str]] or str
    :param out_data: 用于存储结果数据集的数据源
    :type out_data: DatasourceConnectionInfo or Datasource or str
    :param str out_dataset_name: 结果数据集名称
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 结果矢量数据集
    :rtype: DatasetVector or str
    """
    check_lic()
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
            _outDatasetName = source_dt.name + "_measure"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "measure_direction_element")
                        get_jvm().com.supermap.analyst.spatialstatistics.SpatialMeasure.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_param = _measure_param(group_field, None, None, None, stats_fields, ellipse_size)
            measureDirectional = get_jvm().com.supermap.analyst.spatialstatistics.SpatialMeasure.measureDirectional
            java_result = measureDirectional(oj(source_dt), oj(out_datasource), _outDatasetName, java_param)
            del java_param
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialstatistics.SpatialMeasure.removeSteppedListener(listener)
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


def measure_linear_directional_mean(source, group_field=None, weight_field=None, is_orientation=False, stats_fields=None, out_data=None, out_dataset_name=None, progress=None):
    """

    计算线数据集的方向平均值，并返回结果矢量数据集。

     * 线性方向平均值是根据所有线对象的质心的平均中心点为其中心、长度等于所有输入线对象的平均长度、方位或方向为由所有输入线对象
       的起点和终点（每个线对象都只会使用起点和终点来确定方向）计算得到的平均方位或平均方向创建的线对象。

     * 线对象的平均中心x和y坐标、平均长度、罗盘角、方向平均值、圆方差，分别储存在结果矢量数据集中的AverageX、AverageY、
       AverageLength、CompassAngle、DirectionalMean、CircleVariance字段中。如果设置了分组字段，则结果矢量数据集将包含
       “分组字段名_Group” 字段。

     * 线对象的罗盘角（CompassAngle）字段表示以正北方为基准方向按顺时针旋转;方向平均值（DirectionalMean）字段表示以正东方为
       基准方向按逆时针旋转;圆方差（CircleVariance）表示方向或方位偏离方向平均值的程度,如果输入线对象具有非常相似（或完全相同）
       的方向则该值会非常小，反之则相反。

     .. image:: ../image/MeasureLinearDirectionalMean.png

    关于空间度量介绍，请参考 :py:func:`measure_central_element`

    :param source: 待计算的数据集。为线数据集。
    :type source: DatasetVector or str
    :param str group_field: 分组字段名称
    :param str weight_field: 权重字段名称
    :param bool is_orientation: 是否忽略起点和终点的方向。为 False 时，将在计算方向平均值时使用起始点和终止点的顺序；为 True 时，将忽略起始点和终止点的顺序。
    :param stats_fields:  统计字段的类型，为一个list类型，list 中存储2个元素的tuple，tuple的第一个元素为被统计的字段，第二个元素为统计类型
    :type stats_fields: list[tuple[str,SpatialStatisticsType]] or list[tuple[str,str]] or str
    :param out_data: 用于存储结果数据集的数据源
    :type out_data: DatasourceConnectionInfo or Datasource or str
    :param str out_dataset_name: 结果数据集名称
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector or str
    """
    check_lic()
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
            _outDatasetName = source_dt.name + "_measure"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "measure_linear_directional_mean")
                        get_jvm().com.supermap.analyst.spatialstatistics.SpatialMeasure.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_param = _measure_param(group_field, weight_field, None, None, stats_fields, None, is_orientation)
            measureLinearDirectionalMean = get_jvm().com.supermap.analyst.spatialstatistics.SpatialMeasure.measureLinearDirectionalMean
            java_result = measureLinearDirectionalMean(oj(source_dt), oj(out_datasource), _outDatasetName, java_param)
            del java_param
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialstatistics.SpatialMeasure.removeSteppedListener(listener)
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


def measure_mean_center(source, group_field=None, weight_field=None, stats_fields=None, out_data=None, out_dataset_name=None, progress=None):
    """
    计算矢量数据的平均中心，返回结果矢量数据集。

     * 平均中心是根据输入的所有对象质心的平均x和y坐标构造的点。

     * 平均中心的x和y坐标分别储存在结果矢量数据集中的SmX和SmY字段中。如果设置了分组字段，则结果矢量数据集将包含 “分组字段名_Group” 字段。

     .. image:: ../image/MeasureMeanCenter.png

    关于空间度量介绍，请参考 :py:func:`measure_central_element`

    :param source: 待计算的数据集。可以为点、线、面数据集。
    :type source: DatasetVector or str
    :param str group_field: 分组字段
    :param str weight_field: 权重字段
    :param stats_fields: 统计字段的类型，为一个list类型，list 中存储2个元素的tuple，tuple的第一个元素为被统计的字段，第二个元素为统计类型
    :type stats_fields: list[tuple[str,SpatialStatisticsType]] or list[tuple[str,str]] or str
    :param out_data: 用于存储结果数据集的数据源
    :type out_data: DatasourceConnectionInfo or Datasource or str
    :param str out_dataset_name: 结果数据集名称
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 结果数据集或数据集名称
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
            _outDatasetName = source_dt.name + "_measure"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "measure_mean_center")
                        get_jvm().com.supermap.analyst.spatialstatistics.SpatialMeasure.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_param = _measure_param(group_field, weight_field, None, None, stats_fields)
            measureMeanCenter = get_jvm().com.supermap.analyst.spatialstatistics.SpatialMeasure.measureMeanCenter
            java_result = measureMeanCenter(oj(source_dt), oj(out_datasource), _outDatasetName, java_param)
            del java_param
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialstatistics.SpatialMeasure.removeSteppedListener(listener)
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


def measure_median_center(source, group_field, weight_field, stats_fields=None, out_data=None, out_dataset_name=None, progress=None):
    """

    计算矢量数据的中位数中心，返回结果矢量数据集。

     * 中位数中心是根据输入的所有对象质心，使用迭代算法找出到所有对象质心的欧式距离最小的点。

     * 中位数中心的x和y坐标分别储存在结果矢量数据集中的SmX和SmY字段中。如果设置了分组字段，则结果矢量数据集将包含
       “分组字段名_Group” 字段。

     * 实际上，距所有对象质心的距离最小的点可能有多个，但中位数中心方法只会返回一个点。

     * 用于计算中位数中心的算法是由Kuhn,Harold W.和Robert E. Kuenne在1962年提出的迭代加权最小二乘法（Weiszfeld算法），之后由
       James E. Burt和Gerald M. Barber进一步概括。首先以平均中心（有权重，为加权）作为起算点，利用加权最小二乘法得到候选点，将
       候选点重新作为起算点代入计算得到新的候选点，迭代计算直到候选点到所有对象质心的欧式距离最小为止。

     .. image:: ../image/MeasureMedianCenter.png

    关于空间度量介绍，请参考 :py:func:`measure_central_element`

    :param source: 待计算的数据集。可以为点、线、面数据集。
    :type source: DatasetVector or str
    :param str group_field: 分组字段
    :param str weight_field: 权重字段
    :param stats_fields: 统计字段的类型，为一个list类型，list 中存储2个元素的tuple，tuple的第一个元素为被统计的字段，第二个元素为统计类型
    :type stats_fields: list[tuple[str,SpatialStatisticsType]] or list[tuple[str,str]] or str
    :param out_data: 用于存储结果数据集的数据源
    :type out_data: DatasourceConnectionInfo or Datasource or str
    :param str out_dataset_name: 结果数据集名称
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector or str
    """
    check_lic()
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
            _outDatasetName = source_dt.name + "_measure"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "measure_median_center")
                        get_jvm().com.supermap.analyst.spatialstatistics.SpatialMeasure.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_param = _measure_param(group_field, weight_field, None, None, stats_fields)
            measureMedianCenter = get_jvm().com.supermap.analyst.spatialstatistics.SpatialMeasure.measureMedianCenter
            java_result = measureMedianCenter(oj(source_dt), oj(out_datasource), _outDatasetName, java_param)
            del java_param
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialstatistics.SpatialMeasure.removeSteppedListener(listener)
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


def measure_standard_distance(source, group_field, weight_field, ellipse_size='SINGLE', stats_fields=None, out_data=None, out_dataset_name=None, progress=None):
    """

    计算矢量数据的标准距离，返回结果矢量数据集。

     * 标准距离是根据所有对象质心的平均中心（有权重，为加权）为圆心，计算x和y坐标的标准距离为半径得到的圆。

     * 圆的圆心x和y坐标、标准距离（圆的半径），分别储存在结果矢量数据集中的CircleCenterX、CircleCenterY、StandardDistance字
       段中。如果设置了分组字段，则结果矢量数据集将包含 “分组字段名_Group” 字段。

     * 输出的圆大小有三个级别：Single（一个标准差）、Twice（二个标准差）和Triple（三个标准差），详细介绍请参见 :py:class:`.EllipseSize` 枚举类型。

     .. image:: ../image/MeasureStandardDistance.png

    关于空间度量介绍，请参考 :py:func:`measure_central_element`

    :param source: 待计算的数据集。为线数据集
    :type source: DatasetVector or str
    :param str group_field: 分组字段
    :param str weight_field: 权重字段
    :param ellipse_size: 椭圆大小类型
    :type ellipse_size: EllipseSize or str
    :param stats_fields: 统计字段的类型，为一个list类型，list 中存储2个元素的tuple，tuple的第一个元素为被统计的字段，第二个元素为统计类型
    :type stats_fields: list[tuple[str,SpatialStatisticsType]] or list[tuple[str,str]] or str
    :param out_data: 用于存储结果数据集的数据源
    :type out_data: DatasourceConnectionInfo or Datasource or str
    :param str out_dataset_name: 结果数据集名称
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector or str
    """
    check_lic()
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
            _outDatasetName = source_dt.name + "_measure"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "measure_standard_distance")
                        get_jvm().com.supermap.analyst.spatialstatistics.SpatialMeasure.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_param = _measure_param(group_field, weight_field, None, None, stats_fields, ellipse_size)
            measureStandardDistance = get_jvm().com.supermap.analyst.spatialstatistics.SpatialMeasure.measureStandardDistance
            java_result = measureStandardDistance(oj(source_dt), oj(out_datasource), _outDatasetName, java_param)
            del java_param
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialstatistics.SpatialMeasure.removeSteppedListener(listener)
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


def _patterns_param(assessment_field=None, concept_model='INVERSEDISTANCE', distance_method='EUCLIDEAN', distance_tolerance=-1.0, exponent=1.0, weight_file_path=None, k_neighbors=1, is_standardization=False, is_FDR_adj=False, self_weight_field=None):
    java_param = get_jvm().com.supermap.analyst.spatialstatistics.PatternsParameter()
    if assessment_field is not None:
        java_param.setAssessmentFieldName(str(assessment_field))
    if concept_model is not None:
        java_param.setConceptModel(oj(ConceptualizationModel._make(concept_model)))
    if distance_method is not None:
        java_param.setDistanceMethod(oj(DistanceMethod._make(distance_method)))
    if distance_tolerance is not None:
        java_param.setDistanceTolerance(float(distance_tolerance))
    if exponent is not None:
        java_param.setExponent(float(exponent))
    if weight_file_path is not None:
        java_param.setFilePath(str(weight_file_path))
    if k_neighbors is not None:
        java_param.setKNeighbors(int(k_neighbors))
    if is_standardization is not None:
        java_param.setStandardization(parse_bool(is_standardization))
    if is_FDR_adj is not None:
        java_param.setFDRAdjusted(bool(is_FDR_adj))
    if self_weight_field is not None:
        java_param.setSelfWeightFieldName(str(self_weight_field))
    return java_param


class AnalyzingPatternsResult:
    __doc__ = "\n    分析模式结果类。该类用于获取分析模式计算的结果，包括结果指数、期望、方差、Z得分和P值等。\n    "

    def __init__(self):
        self._expectation = None
        self._index = None
        self._p_value = None
        self._variance = None
        self._z_score = None

    def __str__(self):
        s = []
        s.append("AnalyzingPatternsResult: ")
        s.append("expectation: " + str(self.expectation))
        s.append("index:       " + str(self.index))
        s.append("variance:    " + str(self.variance))
        s.append("P value:     " + str(self.p_value))
        s.append("Z score:     " + str(self.z_score))
        return "\n".join(s)

    @staticmethod
    def _from_java_object(java_obj):
        if java_obj is None:
            return
        result = AnalyzingPatternsResult()
        result._expectation = java_obj.getExpectation()
        result._index = java_obj.getIndex()
        result._p_value = java_obj.getPValue()
        result._variance = java_obj.getVariance()
        result._z_score = java_obj.getZScore()
        return result

    @property
    def expectation(self):
        """float: 分析模式结果中的期望值"""
        return self._expectation

    @property
    def index(self):
        """float: 分析模式结果中的莫兰指数或GeneralG指数"""
        return self._index

    @property
    def p_value(self):
        """float: 分析模式结果中的P值"""
        return self._p_value

    @property
    def z_score(self):
        """float: 分析模式结果中的Z得分"""
        return self._z_score

    @property
    def variance(self):
        """float: 分析模式结果中的方差值"""
        return self._variance


def auto_correlation(source, assessment_field, concept_model='INVERSEDISTANCE', distance_method='EUCLIDEAN', distance_tolerance=-1.0, exponent=1.0, k_neighbors=1, is_standardization=False, weight_file_path=None, progress=None):
    """
    分析模式介绍：

        分析模式可评估一组数据是形成离散空间模式、聚类空间模式或者随机空间模式。

        * 分析模式用来计算的数据可以是点、线、面。对于点、线和面对象，在距离计算中会使用对象的质心。对象的质心为所有子对象的加权平均中心。点对象的加权项为1（即质心为自身），线对象的加权项是长度，而面对象的加权项是面积。
        * 分析模式类采用推论式统计,会在进行统计检验时预先建立"零假设",假设要素或要素之间相关的值都表现为随机空间模式。
        * 分析结果计算中会给出一个P值用来表示"零假设"的正确概率,用以判定是接受"零假设"还是拒绝"零假设"。
        * 分析结果计算中会给出一个Z得分用来表示标准差的倍数,用以判定数据是呈聚类、离散或随机。
        * 要拒绝"零假设",就必须要承担可能做出错误选择（即错误的拒绝"零假设"）的风险。

          下表显示了不同置信度下未经校正的临界P值和临界Z得分:

          .. image:: ../image/AnalyzingPatterns.png

        * 用户可以通过分析模式来解决以下问题：

            * 数据集中的要素或数据集中要素关联的值是否发生空间聚类？
            * 数据集的聚类程度是否会随时间变化？

        分析模式包括空间自相关分析（ :py:func:`auto_correlation` ）、平均最近邻分析（ :py:func:`average_nearest_neighbor` ）、
        高低值聚类分析（ :py:func:`high_or_low_clustering` ）、增量空间自相关分析（ :py:func:`incremental_auto_correlation` ）等。

    对矢量数据集进行空间自相关分析，并返回空间自相关分析结果。空间自相关返回的结果包括莫兰指数、期望、方差、z得分、P值,
    请参阅 :py:class:`.AnalyzingPatternsResult` 类。

    .. image:: ../image/AnalyzingPatterns_autoCorrelation.png

    :param source: 待计算的数据集。可以为点、线、面数据集。
    :type source: DatasetVector or str
    :param str assessment_field: 评估字段的名称。仅数值字段有效。
    :param concept_model: 空间关系概念化模型。默认值 :py:attr:`.ConceptualizationModel.INVERSEDISTANCE`。
    :type concept_model: ConceptualizationModel or str
    :param distance_method: 距离计算方法类型
    :type distance_method: DistanceMethod or str
    :param float distance_tolerance: 中断距离容限。仅对概念化模型设置为 :py:attr:`.ConceptualizationModel.INVERSEDISTANCE` 、
                                     :py:attr:`.ConceptualizationModel.INVERSEDISTANCESQUARED` 、
                                     :py:attr:`.ConceptualizationModel.FIXEDDISTANCEBAND` 、
                                     :py:attr:`.ConceptualizationModel.ZONEOFINDIFFERENCE` 时有效。

                                     为"反距离"和"固定距离"模型指定中断距离。"-1"表示计算并应用默认距离，此默认值为保证每个要
                                     素至少有一个相邻的要素;"0"表示为未应用任何距离，则每个要素都是相邻要素。

    :param float exponent: 反距离幂指数。仅对概念化模型设置为 :py:attr:`.ConceptualizationModel.INVERSEDISTANCE` 、
                                     :py:attr:`.ConceptualizationModel.INVERSEDISTANCESQUARED` 、
                                     :py:attr:`.ConceptualizationModel.ZONEOFINDIFFERENCE` 时有效。
    :param int k_neighbors:  相邻数目，目标要素周围最近的K个要素为相邻要素。仅对概念化模型设置为 :py:attr:`.ConceptualizationModel.KNEARESTNEIGHBORS` 时有效。
    :param bool is_standardization: 是否对空间权重矩阵进行标准化。若进行标准化,则每个权重都会除以该行的和。
    :param str weight_file_path: 空间权重矩阵文件路径
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 空间自相关结果
    :rtype: AnalyzingPatternsResult
    """
    check_lic()
    source_dt = get_input_dataset(source)
    if not isinstance(source_dt, DatasetVector):
        raise ValueError("source required DatasetVector, but is " + str(type(source)))
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "auto_correlation")
                        get_jvm().com.supermap.analyst.spatialstatistics.AnalyzingPatterns.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            autoCorrelation = get_jvm().com.supermap.analyst.spatialstatistics.AnalyzingPatterns.autoCorrelation
            java_param = _patterns_param(assessment_field, concept_model, distance_method, distance_tolerance, exponent, weight_file_path, k_neighbors, is_standardization)
            java_result = autoCorrelation(oj(source_dt), java_param)
            del java_param
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialstatistics.AnalyzingPatterns.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if java_result is None:
            return
        return AnalyzingPatternsResult._from_java_object(java_result)


def high_or_low_clustering(source, assessment_field, concept_model='INVERSEDISTANCE', distance_method='EUCLIDEAN', distance_tolerance=-1.0, exponent=1.0, k_neighbors=1, is_standardization=False, weight_file_path=None, progress=None):
    """
    对矢量数据集进行高低值聚类分析,并返回高低值聚类分析结果。 高低值聚类返回的结果包括GeneralG指数、期望、方差、z得分、P值,
    请参阅 :py:class:`.AnalyzingPatternsResult` 类。

    .. image:: ../image/AnalyzingPatterns_highOrLowClustering.png

    关于分析模式介绍，请参考 :py:func:`auto_correlation`

    :param source: 待计算的数据集。可以为点、线、面数据集。
    :type source: DatasetVector or str
    :param str assessment_field: 评估字段的名称。仅数值字段有效。
    :param concept_model: 空间关系概念化模型。默认值 :py:attr:`.ConceptualizationModel.INVERSEDISTANCE`。
    :type concept_model: ConceptualizationModel or str
    :param distance_method: 距离计算方法类型
    :type distance_method: DistanceMethod or str
    :param float distance_tolerance: 中断距离容限。仅对概念化模型设置为 :py:attr:`.ConceptualizationModel.INVERSEDISTANCE` 、
                                     :py:attr:`.ConceptualizationModel.INVERSEDISTANCESQUARED` 、
                                     :py:attr:`.ConceptualizationModel.FIXEDDISTANCEBAND` 、
                                     :py:attr:`.ConceptualizationModel.ZONEOFINDIFFERENCE` 时有效。

                                     为"反距离"和"固定距离"模型指定中断距离。"-1"表示计算并应用默认距离，此默认值为保证每个要
                                     素至少有一个相邻的要素;"0"表示为未应用任何距离，则每个要素都是相邻要素。

    :param float exponent: 反距离幂指数。仅对概念化模型设置为 :py:attr:`.ConceptualizationModel.INVERSEDISTANCE` 、
                                     :py:attr:`.ConceptualizationModel.INVERSEDISTANCESQUARED` 、
                                     :py:attr:`.ConceptualizationModel.ZONEOFINDIFFERENCE` 时有效。
    :param int k_neighbors:  相邻数目，目标要素周围最近的K个要素为相邻要素。仅对概念化模型设置为 :py:attr:`.ConceptualizationModel.KNEARESTNEIGHBORS` 时有效。
    :param bool is_standardization: 是否对空间权重矩阵进行标准化。若进行标准化,则每个权重都会除以该行的和。
    :param str weight_file_path: 空间权重矩阵文件路径
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 高低值聚类结果
    :rtype: AnalyzingPatternsResult
    """
    check_lic()
    source_dt = get_input_dataset(source)
    if not isinstance(source_dt, DatasetVector):
        raise ValueError("source required DatasetVector, but is " + str(type(source)))
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "high_or_low_clustering")
                        get_jvm().com.supermap.analyst.spatialstatistics.AnalyzingPatterns.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            highOrLowClustering = get_jvm().com.supermap.analyst.spatialstatistics.AnalyzingPatterns.highOrLowClustering
            java_param = _patterns_param(assessment_field, concept_model, distance_method, distance_tolerance, exponent, weight_file_path, k_neighbors, is_standardization)
            java_result = highOrLowClustering(oj(source_dt), java_param)
            del java_param
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialstatistics.AnalyzingPatterns.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if java_result is None:
            return
        return AnalyzingPatternsResult._from_java_object(java_result)


def average_nearest_neighbor(source, study_area, distance_method='EUCLIDEAN', progress=None):
    """

    对矢量数据集进行平均最近邻分析，并返回平均最近邻分析结果数组。

    * 平均最近邻返回的结果包括最近邻指数、预期平均距离、平均观测距离、z得分、P值,请参阅 :py:class:`.AnalyzingPatternsResult` 类。

    * 给定的研究区域面积大小必须大于等于0;如果研究区域面积等于0,则会自动生成输入数据集的最小面积外接矩形,用该矩形的面积来进行计算。
      该默认值为: 0 。

    * 距离计算方法类型可以指定相邻要素之间的距离计算方式(参阅 :py:class:`.DistanceMethod` )。如果输入数据集为地理坐标系，则会采用弦测量方法来
      计算距离。地球表面上的任意两点,两点之间的弦距离为穿过地球体连接两点的直线长度。

    .. image:: ../image/AnalyzingPatterns_AverageNearestNeighbor.png

    关于分析模式介绍，请参考 :py:func:`auto_correlation`

    :param source: 待计算的数据集。可以为点、线、面数据集。
    :type source: DatasetVector or str
    :param float study_area: 研究区域面积
    :param distance_method: 距离计算方法
    :type distance_method: DistanceMethod or str
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 平均最近邻分析结果
    :rtype: AnalyzingPatternsResult
    """
    source_dt = get_input_dataset(source)
    if not isinstance(source_dt, DatasetVector):
        raise ValueError("source required DatasetVector, but is " + str(type(source)))
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "average_nearest_neighbor")
                        get_jvm().com.supermap.analyst.spatialstatistics.AnalyzingPatterns.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            averageNearestNeighbor = get_jvm().com.supermap.analyst.spatialstatistics.AnalyzingPatterns.averageNearestNeighbor
            java_result = averageNearestNeighbor(oj(source_dt), float(study_area), oj(DistanceMethod._make(distance_method, "EUCLIDEAN")))
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialstatistics.AnalyzingPatterns.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if java_result is None:
            return
        return AnalyzingPatternsResult._from_java_object(java_result)


class IncrementalResult(AnalyzingPatternsResult):
    __doc__ = "\n    增量空间自相关结果类。该类用于获取增量空间自相关计算的结果，包括结果增量距离、莫兰指数、期望、方差、Z得分和P值等。\n    "

    def __init__(self):
        AnalyzingPatternsResult.__init__(self)
        self._distance = None

    def __str__(self):
        s = []
        s.append("IncrementalResult: ")
        s.append("expectation: " + str(self.expectation))
        s.append("index:       " + str(self.index))
        s.append("variance:    " + str(self.variance))
        s.append("P value:     " + str(self.p_value))
        s.append("Z score:     " + str(self.z_score))
        s.append("distance:      " + str(self.distance))
        return "\n".join(s)

    @staticmethod
    def _from_java_object(java_obj):
        if java_obj is None:
            return
        result = IncrementalResult()
        result._expectation = java_obj.getExpectation()
        result._index = java_obj.getIndex()
        result._p_value = java_obj.getPValue()
        result._variance = java_obj.getVariance()
        result._z_score = java_obj.getZScore()
        result._distance = java_obj.getDistance()
        return result

    @property
    def distance(self):
        """float: 增量空间自相关结果中的增量距离"""
        return self._distance


def incremental_auto_correlation(source, assessment_field, begin_distance=0.0, distance_method='EUCLIDEAN', incremental_distance=0.0, incremental_number=10, is_standardization=False, progress=None):
    """
    对矢量数据集进行增量空间自相关分析，并返回增量空间自相关分析结果数组。增量空间自相关返回的结果包括增量距离、莫兰指数、期望、方差、z得分、P值,
    请参阅 :py:class:`.IncrementalResult` 类。

    增量空间自相关会为一系列的增量距离运行空间自相关方法（参考 :py:func:`auto_correlation` ）,空间关系概念化模型默认为固定距离
    模型(参阅 :py:attr:`.ConceptualizationModel.FIXEDDISTANCEBAND` ）

    关于分析模式介绍，请参考 :py:func:`auto_correlation`

    :param source: 待计算的数据集。可以为点、线、面数据集。
    :type source: DatasetVector or str
    :param str assessment_field: 评估字段的名称。仅数值字段有效。
    :param float begin_distance: 增量空间自相关开始分析的起始距离。
    :param distance_method: 距离计算方法类型
    :type distance_method: DistanceMethod or str
    :param float incremental_distance: 距离增量，增量空间自相关每次分析的间隔距离。
    :param int incremental_number: 递增的距离段数目。为增量空间自相关指定分析数据集的次数，该值的范围为：2 ~ 30。
    :param bool is_standardization: 是否对空间权重矩阵进行标准化。若进行标准化,则每个权重都会除以该行的和。
    :param progress: 进度信息，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 增量空间自相关分析结果列表。
    :rtype: list[IncrementalResult]
    """
    check_lic()
    source_dt = get_input_dataset(source)
    if not isinstance(source_dt, DatasetVector):
        raise ValueError("source required DatasetVector, but is " + str(type(source)))
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "incremental_auto_correlation")
                        get_jvm().com.supermap.analyst.spatialstatistics.AnalyzingPatterns.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_param = get_jvm().com.supermap.analyst.spatialstatistics.IncrementalParameter()
            if assessment_field is not None:
                java_param.setAssessmentFieldName(str(assessment_field))
            if begin_distance is not None:
                java_param.setBeginDistance(float(begin_distance))
            if distance_method is not None:
                java_param.setDistanceMethod(oj(DistanceMethod._make(distance_method, "EUCLIDEAN")))
            if incremental_distance is not None:
                java_param.setIncrementalDistance(float(incremental_distance))
            if incremental_number is not None:
                java_param.setIncrementalNumber(int(incremental_number))
            if is_standardization is not None:
                java_param.setStandardization(parse_bool(is_standardization))
            incrementalAutoCorrelation = get_jvm().com.supermap.analyst.spatialstatistics.AnalyzingPatterns.incrementalAutoCorrelation
            java_result = incrementalAutoCorrelation(oj(source_dt), java_param)
            del java_param
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialstatistics.AnalyzingPatterns.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if java_result is None:
            return
        return list((IncrementalResult._from_java_object(item) for item in java_result))


def cluster_outlier_analyst(source, assessment_field, concept_model='INVERSEDISTANCE', distance_method='EUCLIDEAN', distance_tolerance=-1.0, exponent=1.0, is_FDR_adjusted=False, k_neighbors=1, is_standardization=False, weight_file_path=None, out_data=None, out_dataset_name=None, progress=None):
    """
    聚类分布介绍：

        聚类分布可识别一组数据具有统计显著性的热点、冷点或者空间异常值。

        聚类分布用来计算的数据可以是点、线、面。对于点、线和面对象，在距离计算中会使用对象的质心。对象的质心为所有子对象的加权
        平均中心。点对象的加权项为1（即质心为自身），线对象的加权项是长度，而面对象的加权项是面积。

        用户可以通过聚类分布计算来解决以下问题：

            1. 聚类或冷点和热点出现在哪里？
            2. 空间异常值的出现位置在哪里？
            3. 哪些要素十分相似？

        聚类分布包括聚类和异常值分析（:py:func:`cluster_outlier_analyst`）、热点分析（:py:func:`hot_spot_analyst`）、
        优化热点分析（:py:func:`optimized_hot_spot_analyst`）等

    聚类和异常值分析，返回结果矢量数据集。

     * 结果数据集中包括局部莫兰指数（ALMI_MoranI）、z得分（ALMI_Zscore）、P值（ALMI_Pvalue）和聚类和异常值类型（ALMI_Type）。
     * z得分和P值都是统计显著性的度量,用于逐要素的判断是否拒绝"零假设"。置信区间字段会识别具有统计显著性的聚类和异常值。如果,
       要素的Z得分是一个较高的正值,则表示周围的要素拥有相似值（高值或低值）,聚类和异常值类型字段将具有统计显著性的高值聚类表示
       为"HH"，将具有统计显著性的低值聚类表示为"LL";如果,要素的Z得分是一个较低的负值值,则表示有一个具有统计显著性的空间数据异常
       值,聚类和异常值类型字段将指出低值要素围绕高值要素表示为"HL"，将高值要素围绕低值要素表示为"LH"。
     * 在没有设置 is_FDR_adjusted,统计显著性以P值和Z字段为基础,否则,确定置信度的关键P值会降低以兼顾多重测试和空间依赖性。

     .. image:: ../image/ClusteringDistributions_clusterOutlierAnalyst.png

    :param source: 待计算的数据集。可以为点、线、面数据集。
    :type source: DatasetVector or str
    :param str assessment_field: 评估字段的名称。仅数值字段有效。
    :param concept_model: 空间关系概念化模型。默认值 :py:attr:`.ConceptualizationModel.INVERSEDISTANCE`。
    :type concept_model: ConceptualizationModel or str
    :param distance_method: 距离计算方法类型
    :type distance_method: DistanceMethod or str
    :param float distance_tolerance: 中断距离容限。仅对概念化模型设置为 :py:attr:`.ConceptualizationModel.INVERSEDISTANCE` 、
                                     :py:attr:`.ConceptualizationModel.INVERSEDISTANCESQUARED` 、
                                     :py:attr:`.ConceptualizationModel.FIXEDDISTANCEBAND` 、
                                     :py:attr:`.ConceptualizationModel.ZONEOFINDIFFERENCE` 时有效。

                                     为"反距离"和"固定距离"模型指定中断距离。"-1"表示计算并应用默认距离，此默认值为保证每个要
                                     素至少有一个相邻的要素;"0"表示为未应用任何距离，则每个要素都是相邻要素。

    :param float exponent: 反距离幂指数。仅对概念化模型设置为 :py:attr:`.ConceptualizationModel.INVERSEDISTANCE` 、
                                     :py:attr:`.ConceptualizationModel.INVERSEDISTANCESQUARED` 、
                                     :py:attr:`.ConceptualizationModel.ZONEOFINDIFFERENCE` 时有效。
    :param bool is_FDR_adjusted: 是否进行FDR（错误发现率）校正。若进行FDR（错误发现率）校正,则统计显著性将以错误发现率校正为基础,否则,统计显著性将以P值和z得分字段为基础。
    :param int k_neighbors:  相邻数目，目标要素周围最近的K个要素为相邻要素。仅对概念化模型设置为 :py:attr:`.ConceptualizationModel.KNEARESTNEIGHBORS` 时有效。
    :param bool is_standardization: 是否对空间权重矩阵进行标准化。若进行标准化,则每个权重都会除以该行的和。
    :param str weight_file_path: 空间权重矩阵文件路径
    :param out_data: 结果数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param progress: 进度信息，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector or str
    """
    check_lic()
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
            _outDatasetName = source_dt.name + "_outlier"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "cluster_outlier_analyst")
                        get_jvm().com.supermap.analyst.spatialstatistics.ClusteringDistributions.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            clusterOutlierAnalyst = get_jvm().com.supermap.analyst.spatialstatistics.ClusteringDistributions.clusterOutlierAnalyst
            java_param = _patterns_param(assessment_field, concept_model, distance_method, distance_tolerance, exponent, weight_file_path, k_neighbors, is_standardization, is_FDR_adjusted)
            java_result = clusterOutlierAnalyst(oj(source_dt), oj(out_datasource), _outDatasetName, java_param)
            del java_param
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialstatistics.ClusteringDistributions.removeSteppedListener(listener)
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


def hot_spot_analyst(source, assessment_field, concept_model='INVERSEDISTANCE', distance_method='EUCLIDEAN', distance_tolerance=-1.0, exponent=1.0, is_FDR_adjusted=False, k_neighbors=1, is_standardization=False, self_weight_field=None, weight_file_path=None, out_data=None, out_dataset_name=None, progress=None):
    """
    热点分析，返回结果矢量数据集。

     * 结果数据集中包括z得分（Gi_Zscore）、P值（Gi_Pvalue）和置信区间（Gi_ConfInvl）。

     * z得分和P值都是统计显著性的度量,用于逐要素的判断是否拒绝"零假设"。置信区间字段会识别具有统计显著性的热点和冷点。置信区间
       为+3和-3的要素反映置信度为99%的统计显著性,置信区间为+2和-2的要素反映置信度为95%的统计显著性,置信区间为+1和-1的要素反映置
       信度为90%的统计显著性,而置信区间为0的要素的聚类则没有统计意义。

     * 在没有设置 is_FDR_adjusted 方法的情况下,统计显著性以P值和Z字段为基础,否则,确定置信度的关键P值会降低以兼顾多重测试和空间依赖性。

    .. image:: ../image/ClusteringDistributions_hotSpotAnalyst.png

    关于聚类分布介绍，参考 :py:func:`cluster_outlier_analyst`

    :param source: 待计算的数据集。可以为点、线、面数据集。
    :type source: DatasetVector or str
    :param str assessment_field: 评估字段的名称。仅数值字段有效。
    :param concept_model: 空间关系概念化模型。默认值 :py:attr:`.ConceptualizationModel.INVERSEDISTANCE`。
    :type concept_model: ConceptualizationModel or str
    :param distance_method: 距离计算方法类型
    :type distance_method: DistanceMethod or str
    :param float distance_tolerance: 中断距离容限。仅对概念化模型设置为 :py:attr:`.ConceptualizationModel.INVERSEDISTANCE` 、
                                     :py:attr:`.ConceptualizationModel.INVERSEDISTANCESQUARED` 、
                                     :py:attr:`.ConceptualizationModel.FIXEDDISTANCEBAND` 、
                                     :py:attr:`.ConceptualizationModel.ZONEOFINDIFFERENCE` 时有效。

                                     为"反距离"和"固定距离"模型指定中断距离。"-1"表示计算并应用默认距离，此默认值为保证每个要
                                     素至少有一个相邻的要素;"0"表示为未应用任何距离，则每个要素都是相邻要素。

    :param float exponent: 反距离幂指数。仅对概念化模型设置为 :py:attr:`.ConceptualizationModel.INVERSEDISTANCE` 、
                           :py:attr:`.ConceptualizationModel.INVERSEDISTANCESQUARED` 、
                           :py:attr:`.ConceptualizationModel.ZONEOFINDIFFERENCE` 时有效。
    :param bool is_FDR_adjusted: 是否进行 FDR（错误发现率）校正。若进行FDR（错误发现率）校正,则统计显著性将以错误发现率校正为基础,否则,统计显著性将以P值和z得分字段为基础。
    :param int k_neighbors:  相邻数目，目标要素周围最近的K个要素为相邻要素。仅对概念化模型设置为 :py:attr:`.ConceptualizationModel.KNEARESTNEIGHBORS` 时有效。
    :param bool is_standardization: 是否对空间权重矩阵进行标准化。若进行标准化,则每个权重都会除以该行的和。
    :param str self_weight_field: 自身权重字段的名称，仅数值字段有效。
    :param str weight_file_path: 空间权重矩阵文件路径
    :param out_data: 结果数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param progress: 进度信息，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector or str
    """
    check_lic()
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
            _outDatasetName = source_dt.name + "_hotspot"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "hot_spot_analyst")
                        get_jvm().com.supermap.analyst.spatialstatistics.ClusteringDistributions.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            hotSpotAnalyst = get_jvm().com.supermap.analyst.spatialstatistics.ClusteringDistributions.hotSpotAnalyst
            java_param = _patterns_param(assessment_field, concept_model, distance_method, distance_tolerance, exponent, weight_file_path, k_neighbors, is_standardization, is_FDR_adjusted, self_weight_field)
            java_result = hotSpotAnalyst(oj(source_dt), oj(out_datasource), _outDatasetName, java_param)
            del java_param
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialstatistics.ClusteringDistributions.removeSteppedListener(listener)
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


def optimized_hot_spot_analyst(source, assessment_field=None, aggregation_method='NETWORKPOLYGONS', aggregating_polygons=None, bounding_polygons=None, out_data=None, out_dataset_name=None, progress=None):
    """
    优化的热点分析，返回结果矢量数据集。

     * 结果数据集中包括z得分（Gi_Zscore）、P值（Gi_Pvalue）和置信区间（Gi_ConfInvl）,详细介绍请参阅 :py:func:`hot_spot_analyst` 方法结果。

     * z得分和P值都是统计显著性的度量,用于逐要素的判断是否拒绝"零假设"。置信区间字段会识别具有统计显著性的热点和冷点。置信区间
       为+3和-3的要素反映置信度为99%的统计显著性,置信区间为+2和-2的要素反映置信度为95%的统计显著性,置信区间为+1和-1的要素反映
       置信度为90%的统计显著性,而置信区间为0的要素的聚类则没有统计意义。

     * 如果提供分析字段，则会直接执行热点分析; 如果未提供分析字段，则会利用提供的聚合方法（参阅 :py:class:`AggregationMethod`）聚
       合所有输入事件点以获得计数，从而作为分析字段执行热点分析。

     * 执行热点分析时，默认概念化模型为 :py:attr:`.ConceptualizationModel.FIXEDDISTANCEBAND` 、错误发现率（FDR）为 True ,
       统计显著性将使用错误发现率（FDR）校正法自动兼顾多重测试和空间依赖性。

     .. image:: ../image/ClusteringDistributions_OptimizedHotSpotAnalyst.png

    关于聚类分布介绍，参考 :py:func:`cluster_outlier_analyst`

    :param source: 待计算的数据集。如果设置了评估字段，可以为点、线、面数据集，否则，则必须为点数据集。
    :type source: DatasetVector or str
    :param str assessment_field: 评估字段的名称。
    :param aggregation_method: 聚合方法。如果未设置提供分析字段，则需要为优化的热点分析提供的聚合方法。

                               * 如果设置为 :py:attr:`.AggregationMethod.AGGREGATIONPOLYGONS` ，则必须设置 aggregating_polygons
                               * 如果设置为 :py:attr:`.AggregationMethod.NETWORKPOLYGONS` ，如果设置了 bounding_polygons，则使用
                                 bounding_polygons 进行聚合，如果没有设置 bounding_polygons， 则使用点数据集的地理范围进行聚合。
                               * 如果设置为 :py:attr:`.AggregationMethod.SNAPNEARBYPOINTS` , aggregating_polygons 和 bounding_polygons 都无效。

    :type aggregation_method: AggregationMethod or str
    :param aggregating_polygons: 聚合事件点以获得事件计数的面数据集。如果未提供分析字段(assessment_field） 且 aggregation_method
                                 设置为 :py:attr:`.AggregationMethod.AGGREGATIONPOLYGONS` 时，提供聚合事件点以获得事件计数的面数据集。
                                 如果设置了评估字段，此参数无效。
    :type aggregating_polygons: DatasetVector or str
    :param bounding_polygons: 事件点发生区域的边界面数据集。必须为面数据集。如果未提供分析字段(assessment_field)且 aggregation_method
                              设置为 :py:attr:`.AggregationMethod.NETWORKPOLYGONS` 时，提供事件点发生区域的边界面数据集。
    :type bounding_polygons: DatasetVector or str
    :param out_data: 结果数据源信息
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param progress: 进度信息，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector or str
    """
    check_lic()
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
            _outDatasetName = source_dt.name + "_hotspot"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "optimized_hot_spot_analyst")
                        get_jvm().com.supermap.analyst.spatialstatistics.ClusteringDistributions.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            optimizedHotSpotAnalyst = get_jvm().com.supermap.analyst.spatialstatistics.ClusteringDistributions.optimizedHotSpotAnalyst
            java_param = get_jvm().com.supermap.analyst.spatialstatistics.OptimizedParameter()
            if assessment_field is not None:
                java_param.setAssessmentFieldName(str(assessment_field))
            if aggregating_polygons is not None:
                java_param.setAggregatingPolygons(oj(get_input_dataset(aggregating_polygons)))
            if aggregation_method is not None:
                java_param.setAggregationMethod(oj(AggregationMethod._make(aggregation_method)))
            if bounding_polygons is not None:
                java_param.setBoundingPolygons(oj(get_input_dataset(bounding_polygons)))
            java_result = optimizedHotSpotAnalyst(oj(source_dt), oj(out_datasource), _outDatasetName, java_param)
            del java_param
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialstatistics.ClusteringDistributions.removeSteppedListener(listener)
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


def collect_events(source, out_data=None, out_dataset_name=None, progress=None):
    """

    收集事件,将事件数据转换成加权数据。

     * 结果点数据集中包含一个 Counts 字段,该字段会保存每个唯一位置所有质心的总和。

     * 收集事件只会处理质心坐标完全相同的对象,并且只会保留一个质心,去除其余的重复点。

     * 对于点、线和面对象，在距离计算中会使用对象的质心。对象的质心为所有子对象的加权平均中心。点对象的加权项为1（即质心为自身），
       线对象的加权项是长度，而面对象的加权项是面积。

    :param source: 待收集的数据集。可以为点、线、面数据集。
    :type source: DatasetVector or str
    :param out_data: 用于存储结果点数据集的数据源。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果点数据集名称。
    :param progress: 进度信息，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector or str
    """
    check_lic()
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
            _outDatasetName = source_dt.name + "_events"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "collect_events")
                        get_jvm().com.supermap.analyst.spatialstatistics.StatisticsUtilities.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            collectEvents = get_jvm().com.supermap.analyst.spatialstatistics.StatisticsUtilities.collectEvents
            java_result = collectEvents(oj(source_dt), oj(out_datasource), _outDatasetName)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialstatistics.StatisticsUtilities.removeSteppedListener(listener)
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


def build_weight_matrix(source, unique_id_field, file_path, concept_model='INVERSEDISTANCE', distance_method='EUCLIDEAN', distance_tolerance=-1.0, exponent=1.0, k_neighbors=1, is_standardization=False, progress=None):
    """
    构建空间权重矩阵。

     * 空间权重矩阵文件旨在生成、存储、重用和共享一组要素之间关系的空间关系概念化模型。文件采用的是二进制文件格式创建,要素关系
       存储为稀疏矩阵。

     * 该方法会生成一个空间权重矩阵文件，文件格式为 ‘*.swmb’。生成的空间权重矩阵文件可用来进行分析，只要将空间关系概念化模型设
       置为 :py:attr:`.ConceptualizationModel.SPATIALWEIGHTMATRIXFILE` 并且通过 weight_file_path 参数指定创建的空间权重矩阵
       文件的完整路径。

    :param source: 待构建空间权重矩阵的数据集，支持点线面。
    :type source: DatasetVector or str
    :param str unique_id_field: 唯一ID字段名，必须是数值型字段。
    :param str file_path: 空间权重矩阵文件保存路径。
    :param concept_model: 概念化模型
    :type concept_model: ConceptualizationModel or str
    :param distance_method: 距离计算方法类型
    :type distance_method: DistanceMethod or str
    :param float distance_tolerance: 中断距离容限。仅对概念化模型设置为 :py:attr:`.ConceptualizationModel.INVERSEDISTANCE` 、
                                     :py:attr:`.ConceptualizationModel.INVERSEDISTANCESQUARED` 、
                                     :py:attr:`.ConceptualizationModel.FIXEDDISTANCEBAND` 、
                                     :py:attr:`.ConceptualizationModel.ZONEOFINDIFFERENCE` 时有效。

                                     为"反距离"和"固定距离"模型指定中断距离。"-1"表示计算并应用默认距离，此默认值为保证每个要
                                     素至少有一个相邻的要素;"0"表示为未应用任何距离，则每个要素都是相邻要素。

    :param float exponent: 反距离幂指数。仅对概念化模型设置为 :py:attr:`.ConceptualizationModel.INVERSEDISTANCE` 、
                           :py:attr:`.ConceptualizationModel.INVERSEDISTANCESQUARED` 、
                           :py:attr:`.ConceptualizationModel.ZONEOFINDIFFERENCE` 时有效。

    :param int k_neighbors: 相邻数目。仅对概念化模型设置为 :py:attr:`.ConceptualizationModel.KNEARESTNEIGHBORS` 时有效。
    :param bool is_standardization: 是否对空间权重矩阵进行标准化。若进行标准化,则每个权重都会除以该行的和。
    :param progress: 进度信息，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 如果构建空间权重矩阵，返回 True，否则返回 False
    :rtype: bool
    """
    source_dt = get_input_dataset(source)
    if not isinstance(source_dt, DatasetVector):
        raise ValueError("source required DatasetVector, but is " + str(type(source)))
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "build_weight_matrix")
                        get_jvm().com.supermap.analyst.spatialstatistics.WeightsUtilities.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            if not file_path.lower().endswith(".swmb"):
                file_path = file_path + ".swmb"
            buildWeightMatrix = get_jvm().com.supermap.analyst.spatialstatistics.WeightsUtilities.buildWeightMatrix
            java_param = _patterns_param(None, concept_model, distance_method, distance_tolerance, exponent, None, k_neighbors, is_standardization, None, None)
            java_result = buildWeightMatrix(oj(source_dt), str(unique_id_field), str(file_path), java_param)
            del java_param
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = False

    finally:
        return

    if listener is not None:
        try:
            get_jvm().com.supermap.analyst.spatialstatistics.WeightsUtilities.removeSteppedListener(listener)
        except Exception as e1:
            try:
                log_error(e1)
            finally:
                e1 = None
                del e1

        close_callback_server()
    return java_result


def weight_matrix_file_to_table(file_path, out_data, out_dataset_name=None, progress=None):
    """
    空间权重矩阵文件转换成属性表。

    结果属性表包含源唯一ID字段（UniqueID）、相邻要素唯一ID字段（NeighborsID）、权重字段（Weight）。

    :param str file_path: 空间权重矩阵文件路径。
    :param out_data: 用于存储结果属性表的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果属性表名称
    :param progress: 进度信息，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 结果属性表数据集或数据集名称。
    :rtype: DatasetVector or str
    """
    if out_data is not None:
        out_datasource = get_output_datasource(out_data)
        check_output_datasource(out_datasource)
    else:
        raise ValueError("out_data cannot be None")
    if out_dataset_name is None:
        _outDatasetName = "NewDataset"
    else:
        _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "weight_matrix_file_to_table")
                        get_jvm().com.supermap.analyst.spatialstatistics.WeightsUtilities.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_result = get_jvm().com.supermap.analyst.spatialstatistics.WeightsUtilities.converToTableDataset(str(file_path), oj(out_datasource), _outDatasetName)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialstatistics.WeightsUtilities.removeSteppedListener(listener)
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


class GWRSummary:
    __doc__ = "\n    地理加权回归结果汇总类。该类给出了地理加权回归分析的结果汇总，例如带宽、相邻数、残差平方和、AICc和判定系数等。\n    "

    def __init__(self):
        self._AIC = None
        self._AICc = None
        self._band_width = None
        self._edf = None
        self._effective_number = None
        self._neighbours = None
        self._r2 = None
        self._r2_adjusted = None
        self._residual_squares = None
        self._sigma = None

    def __str__(self):
        s = []
        s.append("GWRSummary: ")
        s.append("AIC:              " + str(self.AIC))
        s.append("AICc:             " + str(self.AICc))
        s.append("Band Width:       " + str(self.band_width))
        s.append("Edf:              " + str(self.Edf))
        s.append("Effective Number: " + str(self.effective_number))
        s.append("Neighbours:       " + str(self.neighbours))
        s.append("R2:               " + str(self.R2))
        s.append("R2 Adjusted:      " + str(self.R2_adjusted))
        s.append("Residual Squares: " + str(self.residual_squares))
        s.append("Sigma:            " + str(self.sigma))
        return "\n".join(s)

    @staticmethod
    def _from_java_object(java_obj):
        if java_obj is None:
            return
        result = GWRSummary()
        result._AIC = java_obj.getAIC()
        result._AICc = java_obj.getAICc()
        result._band_width = java_obj.getBandwidth()
        result._edf = java_obj.getEdf()
        result._effective_number = java_obj.getEffectiveNumber()
        result._neighbours = java_obj.getNeighbors()
        result._r2 = java_obj.getR2()
        result._r2_adjusted = java_obj.getR2Adjusted()
        result._residual_squares = java_obj.getResidualSquares()
        result._sigma = java_obj.getSigma()
        return result

    @property
    def AIC(self):
        """float: 地理加权回归结果汇总中的AIC。与AICc类似，是衡量模型拟合优良性的一种标准，可以权衡所估计模型的复杂度和模型拟
                  合数据的优良性，在评价模型时是兼顾了简洁性和精确性。表明增加自由参数的数目提高了拟合的优良性，AIC鼓励数据的
                  拟合性，但是应尽量避免出现过度拟合的情况。所以优先考虑AIC值较小的，是寻找可以最好的解释数据但包含最少自由参
                  数的模型。"""
        return self._AIC

    @property
    def AICc(self):
        """float: 地理加权回归结果汇总中的AICc。当数据增加时，AICc收敛为AIC，也是模型性能的一种度量，有助与比较不同的回归模型。
                  考虑到模型复杂性，具有较低AICc值的模型将更好的拟合观测数据。AICc不是拟合度的绝对度量，但对于比较用于同一因变
                  量且具有不同解释变量的模型非常有用。如果两个模型的AICc值相差大于3，具有较低AICc值的模型将视为更佳的模型。"""
        return self._AICc

    @property
    def band_width(self):
        """float: 地理加权回归结果汇总中的带宽范围。

                   * 用于各个局部估计的带宽范围，它控制模型中的平滑程度。通常，你可以选择默认的带宽范围，方法是：设置带宽确定
                     方式(kernel_type)方法选择 :py:attr:`.BandWidthType.AICC` 或 :py:attr:`.BandWidthType.CV`，这两个选项都将尝试识别最佳带宽范围。

                   * 由于"最佳"条件对于 AIC 和 CV 并不相同，都会得到相对的最优 AICc 值和 CV 值，因而通常会获得不同的最佳值。

                   * 可以通过设置带宽类型（kernel_type）方法提供精确的带宽范围。
        """
        return self._band_width

    @property
    def Edf(self):
        """float: 地理加权回归结果汇总中的有效自由度。数据的数目与有效的参数数量（EffectiveNumber）的差值，不一定是整数，可用
                  来计算多个诊断测量值。自由度较大的模型拟合度会较差，能够较好的反应数据的真实情况，统计量会变得比较可靠；反之，
                  拟合效果会较好，但是不能较好的反应数据的真实情况，模型数据的独立性被削弱，关联度增加。"""
        return self._edf

    @property
    def effective_number(self):
        """float: 地理加权回归结果汇总中的有效的参数数量。反映了估计值的方差与系数估计值的偏差之间的折衷，该值与带宽的选择有关，
                  可用来计算多个诊断测量值。对于较大的带宽，系数的有效数量将接近实际参数数量，局部系数估计值将具有较小的方差，
                  但是偏差将会非常大;对于较小的带宽，系数的有效数量将接近观测值的数量，局部系数估计值将具有较大的方差，但是偏
                  差将会变小。"""
        return self._effective_number

    @property
    def neighbours(self):
        """int: 地理加权回归结果汇总中的相邻数目。

                 * 用于各个局部估计的相邻数目，它控制模型中的平滑程度。通常，你可以选择默认的相邻点值，方法是：设置带宽确定方式(kernel_type)
                   方法选择 :py:attr:`.BandWidthType.AICC` 或 :py:attr:`.BandWidthType.CV`，这两个选项都将尝试识别最佳自适应相邻点数目。

                 * 由于"最佳"条件对于 AIC 和 CV 并不相同，都会得到相对的最优 AICc 值和 CV 值，因而通常会获得不同的最佳值。

                 * 可以通过设置带宽类型（kernel_type）方法提供精确的自适应相邻点数目。

                """
        return self._neighbours

    @property
    def R2(self):
        """float: 地理加权回归结果汇总中的判定系数（R2）。判定系数是拟合度的一种度量，其值在0.0和1.0范围内变化，值越大模型越好。
                 此值可解释为回归模型所涵盖的因变量方差的比例。R2计算的分母为因变量值的平方和，添加一个解释变量不会更改分母但是
                 会更改分子，这将出现改善模型拟合的情况，但是也可能假象。"""
        return self._r2

    @property
    def R2_adjusted(self):
        """float: 地理加权回归结果汇总中的校正的判定系数。校正的判定系数的计算将按分子和分母的自由度对它们进行正规化。这具有对
                  模型中变量数进行补偿的效果，由于校正的R2值通常小于R2值。但是，执行校正时，无法将该值的解释作为所解释方差的比例。
                  自由度的有效值是带宽的函数，因此，AICc是对模型进行比较的首选方式。"""
        return self._r2_adjusted

    @property
    def residual_squares(self):
        """float: 地理加权回归结果汇总中的残差平方和。残差平方和为实际值与估计值（或拟合值）的平方之和。此测量值越小，模型越
                  拟合观测数据，即拟合程度越好。"""
        return self._residual_squares

    @property
    def sigma(self):
        """float: 地理加权回归结果汇总中的残差估计标准差。残差的估计标准差，为剩余平方和除以残差的有效自由度的平方根。此统计值
                  越小，模型拟合效果越好。"""
        return self._sigma


def GWR(source, explanatory_fields, model_field, kernel_function='GAUSSIAN', band_width_type='AICC', distance_tolerance=0.0, kernel_type='FIXED', neighbors=2, out_data=None, out_dataset_name=None, progress=None):
    """
    空间关系建模介绍：

     * 用户可以通过空间关系建模来解决以下问题：

       * 为什么某一现象会持续的发生,是什么因素导致了这种情况？
       * 导致某一事故发生率比预期的要高的因素有那些？有没有什么方法来减少整个城市或特定区域内的事故发生率？
       * 对某种现象建模以预测其他地点或者其他时间的数值？

     * 通过回归分析，你可以对空间关系进行建模、检查和研究，可以帮助你解释所观测到的空间模型后的诸多因素。比如线性关系是正或者
       是负；对于正向关系，即存在正相关性，某一变量随着另一个变量增加而增加；反之，某一变量随着另一个变量增加而减小；或者两个变量无关系。

    地理加权回归分析。

    * 地理加权回归分析结果信息包含一个结果数据集和地理加权回归结果汇总（请参阅 GWRSummary 类）。
    * 结果数据集包含交叉验证（CVScore）、预测值（Predicted）、回归系数（Intercept、C1_解释字段名）、残差（Residual）、标准误
      （StdError)、系数标准误(SE_Intercept、SE1_解释字段名）、伪t值（TV_Intercept、TV1_解释字段名）和Studentised残差（StdResidual）等。

    说明：

      * 地理加权回归分析是一种用于空间变化关系的线性回归的局部形式,可用来在空间变化依赖和独立变量之间的关系研究。对地理要素所
        关联的数据变量之间的关系进行建模，从而可以对未知值进行预测或者更好地理解可对要建模的变量产生影响的关键因素。回归方法使
        你可以对空间关系进行验证并衡量空间关系的稳固性。
      * 交叉验证（CVScore）：交叉验证在回归系数估计时不包括回归点本身即只根据回归点周围的数据点进行回归计算。该值就是每个回归
        点在交叉验证中得到的估计值与实际值之差，它们的平方和为CV值。作为一个模型性能指标。
      * 预测值（Predicted）：这些值是地理加权回归得到的估计值（或拟合值）。
      * 回归系数（Intercept）：它是地理加权回归模型的回归系数，为回归模型的回归截距，表示所有解释变量均为零时因变量的预测值。
      * 回归系数（C1_解释字段名）：它是解释字段的回归系数，表示解释变量与因变量之间的关系强度和类型。如果回归系数为正，则解释
        变量与因变量之间的关系为正向的；反之，则存在负向关系。如果关系很强，则回归系数也相对较大；关系较弱时，则回归系数接近于0。
      * 残差(Residual)：这些是因变量无法解释的部分，是估计值和实际值之差，标准化残差的平均值为0，标准差为1。残差可用于确定模
        型的拟合程度，残差较小表明模型拟合效果较好，可以解释大部分预测值，说明这个回归方程是有效的。
      * 标准误(StdError)：估计值的标准误差，用于衡量每个估计值的可靠性。较小的标准误表明拟合值与实际值的差异程度越小，模型拟合效果越好。
      * 系数标准误（SE_Intercept、SE1_解释字段名）:这些值用于衡量每个回归系数估计值的可靠性。系数的标准误差与实际系数相比较小
        时，估计值的可信度会更高。较大的标准误差可能表示存在局部多重共线性问题。
      * 伪t值(TV_Intercept、TV1_解释字段名)：是对各个回归系数的显著性检验。当T值大于临界值时，拒绝零假设，回归系数显著即回归系
        估计值是可靠的；当T值小于临界值时，则接受零假设，回归系数不显著。
      * Studentised残差（StdResidual）：残差和标准误的比值，该值可用来判断数据是否异常，若数据都在（-2，2）区间内，表明数据具
        有正态性和方差齐性；若数据超出（-2，2）区间，表明该数据为异常数据，无方差齐性和正态性。

    :param source: 待计算的数据集。可以为点、线、面数据集。
    :type source: DatasetVector or str
    :param explanatory_fields: 解释字段的名称的集合
    :type explanatory_fields: list[str] or str
    :param str model_field: 建模字段的名称
    :param kernel_function: 核函数类型
    :type kernel_function: KernelFunction or str
    :param band_width_type: 带宽确定方式
    :type band_width_type: BandWidthType or str
    :param float distance_tolerance: 带宽范围
    :param kernel_type: 带宽类型
    :type kernel_type: KernelType or str
    :param int neighbors: 相邻数目。只有当带宽类型设置为 :py:attr:`.KernelType.ADAPTIVE` 且宽确定方式设置为 :py:attr:`.BandWidthType.BANDWIDTH` 时有效。
    :param out_data: 用于存储结果数据集的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param progress: 进度信息，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 返回一个两个元素的 tuple，tuple 的第一个元素为 :py:class:`.GWRSummary` ，第二个元素为地理加权回归结果数据集。
    :rtype: tuple[GWRSummary, DatasetVector]
    """
    check_lic()
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
            _outDatasetName = source_dt.name + "_gwr"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "geographic_weighted_regression")
                        get_jvm().com.supermap.analyst.spatialstatistics.SpatialRelModeling.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_param = get_jvm().com.supermap.analyst.spatialstatistics.GWRParameter()
            if explanatory_fields is not None:
                explanatory_fields = split_input_list_from_str(explanatory_fields)
                java_param.setExplanatoryFeilds(to_java_string_array(explanatory_fields))
            if model_field is not None:
                java_param.setModelFeild(str(model_field))
            if kernel_function is not None:
                java_param.setKernelFunction(oj(KernelFunction._make(kernel_function)))
            if kernel_type is not None:
                java_param.setKernelType(oj(KernelType._make(kernel_type)))
            if band_width_type is not None:
                java_param.setBandWidthType(oj(BandWidthType._make(band_width_type)))
            if distance_tolerance is not None:
                java_param.setDistanceTolerance(float(distance_tolerance))
            if neighbors is not None:
                java_param.setNeighbors(int(neighbors))
            gwr = get_jvm().com.supermap.analyst.spatialstatistics.SpatialRelModeling.geographicWeightedRegression
            java_result = gwr(oj(source_dt), oj(out_datasource), _outDatasetName, java_param)
            del java_param
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        return

    if listener is not None:
        try:
            get_jvm().com.supermap.analyst.spatialstatistics.SpatialRelModeling.removeSteppedListener(listener)
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
    gwr_dt = out_datasource[java_result.getResultDataset().getName()]
    if out_data is not None:
        gwr_dt = try_close_output_datasource(gwr_dt, out_datasource)
    gwr_summary = GWRSummary._from_java_object(java_result.getGWRSummary())
    return (gwr_summary, gwr_dt)


class OLSSummary:
    __doc__ = "\n    普通最小二乘法结果汇总类。该类给出了普通最小二乘法分析的结果汇总，例如分布统计量、统计量概率、AICc和判定系数等。\n    "

    def __init__(self, java_object):
        self._java_object = java_object

    @property
    def AIC(self):
        """float: 普通最小二乘法结果汇总中的AIC。与AICc类似，是衡量模型拟合优良性的一种标准，可以权衡所估计模型的复杂度和模型拟合数
        据的优良性，在评价模型时是兼顾了简洁性和精确性。表明增加自由参数的数目提高了拟合的优良性，AIC鼓励数据的拟合性，但是应尽量避
        免出现过度拟合的情况。所以优先考虑AIC值较小的，是寻找可以最好的解释数据但包含最少自由参数的模型"""
        return self._java_object.getAIC()

    @property
    def AICc(self):
        """float: 普通最小二乘法结果汇总中的AICc。当数据增加时，AICc收敛为AIC，也是模型性能的一种度量，有助与比较不同的回归模型。
        考虑到模型复杂性，具有较低AICc值的模型将更好的拟合观测数据。AICc不是拟合度的绝对度量，但对于比较用于同一因变量且具有不同解
        释变量的模型非常有用。如果两个模型的AICc值相差大于3，具有较低AICc值的模型将视为更佳的模型。"""
        return self._java_object.getAICc()

    @property
    def coefficient(self):
        """list[float]: 普通最小二乘法结果汇总中的系数。 系数表示解释变量和因变量之间的关系和类型。"""
        return self._java_object.getCoefficient()

    @property
    def coefficient_std(self):
        """list[float]: 普通最小二乘法结果汇总中的系数标准差"""
        return self._java_object.getCoefficientStd()

    @property
    def F_dof(self):
        """int: 普通最小二乘法结果汇总中的联合F统计量自由度。 """
        return self._java_object.getFDof()

    @property
    def F_probability(self):
        """float: 普通最小二乘法结果汇总中的联合F统计量的概率。 """
        return self._java_object.getFProbability()

    @property
    def f_statistic(self):
        """float: 普通最小二乘法结果汇总中的联合F统计量。联合F统计量用于检验整个模型的统计显著性。只有在Koenker（Breusch-Pagan）
        统计量不具有统计显著性时,联合F统计量才可信。检验的零假设为模型中的解释变量不起作用。对于大小为95%的置信度,联合F统计量概率小
        于0.05表示模型具有统计显著性。"""
        return self._java_object.getFStatistic()

    @property
    def JB_dof(self):
        """int: 普通最小二乘法结果汇总中的Jarque-Bera统计量自由度。 """
        return self._java_object.getJBDof()

    @property
    def JB_probability(self):
        """float: 普通最小二乘法结果汇总中的Jarque-Bera统计量的概率"""
        return self._java_object.getJBProbability()

    @property
    def JB_statistic(self):
        """float: 普通最小二乘法结果汇总中的Jarque-Bera统计量。Jarque-Bera统计量能评估模型的偏差，用于指示残差是否呈正态分布。检
        验的零假设为残差呈正态分布。对于大小为95%的置信度,联合F统计量概率小于0.05表示模型具有统计显著性,回归不会呈正态分布,模型有
        偏差。"""
        return self._java_object.getJBStatistic()

    @property
    def KBP_dof(self):
        """int: 普通最小二乘法结果汇总中的Koenker（Breusch-Pagan）统计量自由度。 """
        return self._java_object.getKBPDof()

    @property
    def KBP_probability(self):
        """float: 普通最小二乘法结果汇总中的Koenker（Breusch-Pagan）统计量的概率"""
        return self._java_object.getKBPProbability()

    @property
    def KBP_statistic(self):
        """float: 普通最小二乘法结果汇总中的Koenker（Breusch-Pagan）统计量。Koenker（Breusch-Pagan）统计量能评估模型的稳态，用
        于确定模型的解释变量是否在地理空间和数据空间中都与因变量具有一致的关系。检验的零假设为检验的模型是稳态的。对于大小为95%的
        置信度,联合F统计量概率小于0.05表示模型具有统计显著异方差性或非稳态。当检验结果具有显著性时，则需要参考稳健系数标准差和
        概率来评估每个解释变量的效果。"""
        return self._java_object.getKBPStatistic()

    @property
    def probability(self):
        """list[float]: 普通最小二乘法结果汇总中的t分布统计量概率"""
        return self._java_object.getProbability()

    @property
    def R2(self):
        """float: 普通最小二乘法结果汇总中的判定系数（R2）。"""
        return self._java_object.getR2()

    @property
    def R2_adjusted(self):
        """float: 普通最小二乘法结果汇总中的校正的判定系数"""
        return self._java_object.getR2Adjusted()

    @property
    def robust_Pr(self):
        """list[float]: 普通最小二乘法结果汇总中的稳健系数概率。"""
        return self._java_object.getRobust_Pr()

    @property
    def robust_SE(self):
        """list[float]: 获取普通最小二乘法结果汇总中的稳健系数标准差。"""
        return self._java_object.getRobust_SE()

    @property
    def robust_t(self):
        """list[float]: 普通最小二乘法结果汇总中的稳健系数t分布统计量。"""
        return self._java_object.getRobust_t()

    @property
    def sigma2(self):
        """float: 普通最小二乘法结果汇总中的残差方差。"""
        return self._java_object.getSigma2()

    @property
    def std_error(self):
        """list[float]: 普通最小二乘法结果汇总中的标准误差。"""
        return self._java_object.getStdError()

    @property
    def t_statistic(self):
        """list[float]: 普通最小二乘法结果汇总中的t分布统计量。"""
        return self._java_object.gett_Statistic()

    @property
    def variable(self):
        """list[float]: 普通最小二乘法结果汇总中的变量数组"""
        return self._java_object.getVariable()

    @property
    def VIF(self):
        """list[float]: 普通最小二乘法结果汇总中的方差膨胀因子"""
        return self._java_object.getVIF()

    @property
    def wald_dof(self):
        """int: 普通最小二乘法结果汇总中的联合卡方统计量自由度"""
        return self._java_object.getWaldDof()

    @property
    def wald_probability(self):
        """float: 普通最小二乘法结果汇总中的联合卡方统计量的概率"""
        return self._java_object.getWaldProbability()

    @property
    def wald_statistic(self):
        """float: 普通最小二乘法结果汇总中的联合卡方统计量。联合卡方统计量用于检验整个模型的统计显著性。只有在
         Koenker（Breusch-Pagan）统计量具有统计显著性时,联合F统计量才可信。检验的零假设为模型中的解释变量不起作用。对于大小为
         95%的置信度,联合F统计量概率小于0.05表示模型具有统计显著性。 """
        return self._java_object.getWaldStatistic()


def ordinary_least_squares(input_data, explanatory_fields, model_field, out_data=None, out_dataset_name=None, progress=None):
    """
    普通最小二乘法。
    普通最小二乘法分析结果信息包含一个结果数据集和普通最小二乘法结果汇总。
    结果数据集包含预测值（Estimated）、残差（Residual）、标准化残差（StdResid）等。

    说明：

    - 预测值（Estimated）：这些值是普通最小二乘法得到的估计值（或拟合值）。
    - 残差（Residual）：这些是因变量无法解释的部分，是估计值和实际值之差，标准化残差的平均值为0，标准差为1。残差可用于确定模型的拟合程度，残差较小表明模型拟合效果较好，可以解释大部分预测值，说明这个回归方程是有效的。
    - 标准化残差（StdResid）：残差和标准误的比值，该值可用来判断数据是否异常，若数据都在（-2，2）区间内，表明数据具有正态性和方差齐性；若数据超出（-2，2）区间，表明该数据为异常数据，无方差齐性和正态性。

    :param input_data: 指定的待计算的数据集。可以为点、线、面数据集。
    :type input_data: DatasetVector or str
    :param explanatory_fields: 解释字段的名称的集合
    :type explanatory_fields: list[str] or str
    :param model_field: 建模字段的名称
    :type model_field: str
    :param out_data: 指定的用于存储结果数据集的数据源。
    :type out_data: Datasource or str
    :param out_dataset_name: 指定的结果数据集名称
    :type out_dataset_name: str
    :param progress: 进度信息，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 返回一个元组，元组的第一个元素为最小二乘法结果数据集或数据集名称，第二个元素为最小二乘法结果汇总
    :rtype: tuple[DatasetVector, OLSSummary] or tuple[str, OLSSummary]
    """
    check_lic()
    source_dt = get_input_dataset(input_data)
    if not isinstance(source_dt, DatasetVector):
        raise ValueError("source required DatasetVector, but is " + str(type(input_data)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name + "_OLS"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    _jvm = get_jvm()
    ols_parameter = _jvm.com.supermap.analyst.spatialstatistics.OLSParameter()
    ols_parameter.setExplanatoryFields(to_java_string_array(split_input_list_from_str(explanatory_fields)))
    ols_parameter.setModelField(model_field)
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "ordinary_least_squares")
                        _jvm.com.supermap.analyst.spatialstatistics.SpatialRelModeling.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            ordinaryLeastSquares = _jvm.com.supermap.analyst.spatialstatistics.SpatialRelModeling.ordinaryLeastSquares
            java_result = ordinaryLeastSquares(oj(source_dt), oj(out_datasource), _outDatasetName, ols_parameter)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.analyst.spatialstatistics.SpatialRelModeling.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[java_result.getResultDataset().getName()]
        else:
            result_dt = None
        if out_data is not None:
            result_dt = try_close_output_datasource(result_dt, out_datasource)
        if java_result is not None:
            return (
             result_dt, OLSSummary(java_result.getOLSSummary()))
        return


def geographical_detector(input_data, model_field, explanatory_fields, is_factor_detector=True, is_ecological_detector=True, is_interaction_detector=True, is_risk_detector=True, progress=None):
    """
    对数据进行地理探测器分析，并返回地理探测器的结果。
    地理探测器返回的结果包括因子探测器，生态探测器，交互探测器，风险探测器的分析结果

    地理探测器是探测空间分异性，以及揭示其背后驱动力的一组统计学方法。其核心思想是基于这样的假设：如果某个自变量对某个因变量有重要影
    响,那么自变量和因变量的空间分布应该具有相似性。地理分异既可以用分类算法来表达，例如环境遥感分类，也可以根据经验确定，例如胡焕庸线。
    地理探测器擅长分析类型量,而对于顺序量、比值量或间隔量,只要进行适当的离散化,也可以利用地理探测器对其进行统计分析。
    因此,地理探测器既可以探测数值型数据，也可以探测定性数据，这正是地理探测器的一大优势。地理探测器的另一个独特优势是探测两因子交互
    作用于因变量。交互作用一般的识别方法是在回归模型中增加两因子的乘积项，检验其统计显著性。然而,两因子交互作用不一定就是相乘关系。
    地理探测器通过分别计算和比较各单因子 q 值及两因子叠加后的 q 值，可以判断两因子是否存在交互作用，以及交互作用的强弱、方向、线性还是
    非线性等。两因子叠加既包括相乘关系，也包括其他关系，只要有关系，就能检验出来。

    :param input_data: 待计算的矢量数据集
    :type input_data: DatasetVector or str
    :param str model_field: 建模字段
    :param explanatory_fields: 解释变量数组
    :type explanatory_fields: list[str] or str
    :param bool is_factor_detector: 是否计算因子探测器
    :param bool is_ecological_detector: 是否计算生态探测器
    :param bool  is_interaction_detector: 是否计算交互探测器
    :param bool is_risk_detector: 是否进行风险探测器
    :param progress: 进度信息，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 地理探测器结果
    :rtype: GeographicalDetectorResult
    """
    check_lic()
    source_dt = get_input_dataset(input_data)
    if not isinstance(source_dt, DatasetVector):
        raise ValueError("source required DatasetVector, but is " + str(type(input_data)))
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "geographical_detector")
                        get_jvm().com.supermap.analyst.spatialstatistics.AnalyzingPatterns.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            geographicalDetector = get_jvm().com.supermap.analyst.spatialstatistics.AnalyzingPatterns.geographicalDetector
            java_result = geographicalDetector(oj(source_dt), str(model_field), to_java_string_array(split_input_list_from_str(explanatory_fields)), bool(is_factor_detector), bool(is_ecological_detector), bool(is_interaction_detector), bool(is_risk_detector), None)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.spatialstatistics.AnalyzingPatterns.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if java_result is None:
            return
        result = GeographicalDetectorResult(java_result)
        del java_result
        return result


class InteractionDetectorResult:
    __doc__ = "\n    交互作用探测器分析结果，用于获取对数据进行交互作用探测器得到的分析结果，包括不同解释变量之间交互作用的描述以及分析结果矩阵。\n    用户不能创建此对象。\n    "

    def __init__(self, java_object):
        if java_object is None:
            self._descriptions = None
            self._interaction_values = None
        else:
            self._descriptions = java_object.getInteractionDescriptions()
            self._interaction_values = InteractionDetectorResult._get_interaction_detector_values(java_object)

    @staticmethod
    def _get_interaction_detector_values(java_object):
        detector_values = java_object.getInteractionDetectorValues()
        values = []
        for i in range(len(detector_values)):
            result_item = detector_values[i]
            values.append([
             result_item.getVariableRow(), result_item.getVariableCol(), result_item.getInteractionValue()])

        import pandas as pd
        return pd.DataFrame(values, columns=["VariableRow", "VariableCol", "InteractionValues"])

    @property
    def descriptions(self):
        """list[str]: 交互作用探测器结果描述。评估不同解释变量共同作用时是否会增加或减弱对因变量的解释力，或这些因子对因变量的影响
        是否相互独立，两个解释变量对因变量交互作用的类型包括：非线性减弱、单因子非线性减弱、双因子增强、独立及非线性增强。"""
        return self._descriptions

    @property
    def interaction_values(self):
        """pandas.DataFrame: 交互作用探测器分析结果值。"""
        return self._interaction_values


class RiskDetectorMean:
    __doc__ = "\n    风险探测器结果均值类，用于获取对数据进行风险区域探测器得到的不同解释变量字段的结果均值。\n    "

    def __init__(self, java_object):
        self._variable = java_object.getVariable()
        self._unique_values = java_object.getVariableUniqueValues()
        self._means = java_object.getMeans()

    @property
    def variable(self):
        """str: 风险探测器解释变量名称"""
        return self._variable

    @property
    def unique_values(self):
        """list[str]: 风险探测器解释变量字段唯一值"""
        return self._unique_values

    @property
    def means(self):
        """list[float]: 风险探测器分析结果均值"""
        return self._means


class RiskDetectorResult:
    __doc__ = "风险区探测器分析结果类，用于获取对数据进行风险区探测器得到的分析结果，包括结果均值、结果矩阵"

    def __init__(self, java_object):
        if java_object is None:
            self._means = None
            self._values = None
        else:
            self._means = [RiskDetectorMean(item) for item in java_object.getRiskDetectorMeans()]
            self._values = [RiskDetectorResult._get_risk_detector_values(values) for values in java_object.getRiskDetectorValues()]

    @staticmethod
    def _get_risk_detector_values(detector_values):
        values = []
        for i in range(len(detector_values)):
            result_item = detector_values[i]
            values.append([
             result_item.getVariableRow(), result_item.getVariableCol(), result_item.getSig()])

        import pandas as pd
        return pd.DataFrame(values, columns=["VariableRow", "VariableCol", "Sig"])

    @property
    def means(self):
        """list[iobjectspy.RiskDetectorMean]: 风险区探测器结果均值"""
        return self._means

    @property
    def values(self):
        """list[pandas.DataFrame]: 风险探测器分析结果值"""
        return self._values


class GeographicalDetectorResult:
    __doc__ = "\n    地理探测器结果类，用于获取地理探测器计算的结果，包括因子探测器、生态探测器、交互作用探测器、风险探测器分析结果。\n    "

    def __init__(self, java_object):
        self._variables = java_object.getVariables()
        self._factor_detector_result = GeographicalDetectorResult._get_java_factor_detector_results(java_object)
        self._risk_detector_result = RiskDetectorResult(java_object.getRiskDetectorResult())
        self._interaction_detector_result = InteractionDetectorResult(java_object.getInteractionDetectorResult())
        self._ecological_detector_result = GeographicalDetectorResult._get_java_ecological_detector_result(java_object)

    @property
    def variables(self):
        """list[str]: 地理探测器解释变量"""
        return self._variables

    @property
    def factor_detector_result(self):
        """pandas.DataFrame: 因子探测器分析结果。探测Y的空间分异性，以及探测某因子 X 多大程度上解释了属性Y的空间分异。用 q 值度量.

                             .. image:: ../image/GeographicalDetectorQformula.png

                             q 的值域为[0,1]，值越大，说明 y 的空间分异越明显，如果分层是由自变量 X 生成的，则 q 值越大，表示 X 和 Y 的空间分布越一致，
                             自变量 X 对属性 Y 的解释力越强，反之则越弱。极端情况下，q 值为1表明在 X 的层内，Y的方差为0，即因子 X 完全控制了 Y 的空间分布，
                             q 值为0 则表明 Y 按照 X 分层后的方差和与 Y 不分层的方差相等，Y 没有按照 X 进行分异，即因子 X 与 Y 没有任何关系。q 值 表示 X 解释了 100q% 的 Y。
        """
        return self._factor_detector_result

    @property
    def risk_detector_result(self):
        """RiskDetectorResult: 风险区探测器分析结果。用于判断两个子区域间的属性均值是否有显著的差别,用 t 统计量来检验。

                               .. image:: ../image/GeographicalDetectorTformula.png

        """
        return self._risk_detector_result

    @property
    def interaction_detector_result(self):
        """InteractionDetectorResult: 交互作用探测器分析结果。识别不同风险因子 Xs 之间的交互作用,即评估因子 X1 和 X2 共同作用时
                                      是否会增加或减弱对因变量Y的解释力，或这些因子对 Y 的影响是相互独立的？评估的方法是首先分别
                                      计算两种因子 X1 和 X2 对 Y 的 q 值: q(Y|X1) 和 q(Y|X2)。然后叠加变量 X1 和 X2 两个图层相切所形成的新的层，计算 X1∩X2 对 Y 的 q 值： q(Y|X1∩X2)。最后，对
                                      q(Y|X1)、q(Y|X2) 与 q(Y|X1∩X2) 的数值进行比较，判断交互作用。

                                       - q(X1∩X2) < Min(q(X1),q(X2))                     非线性减弱
                                       - Min(q(X1),q(X2)) < q(X1∩X2) < Max(q(X1),q(X2))  单因子非线性减弱
                                       - q(X1∩X2) > Max(q(X1),q(X2))                     双因子增强
                                       - q(X1∩X2) = q(X1) + q(X2)                        独立
                                       - q(X1∩X2) > q(X1) + q(X2)                        非线性增强
        """
        return self._interaction_detector_result

    @property
    def ecological_detector_result(self):
        """pandas.DataFrame: 生态探测器分析结果。生态探测器用于比较两因子X1和X2对属性Y的空间分布的影响是否有显著的差异，以 F 统计量来衡量。

                             .. image:: ../image/GeographicalDetectorFformula.png

                             """
        return self._ecological_detector_result

    @staticmethod
    def _get_java_factor_detector_results(java_object):
        results = java_object.getFactorDetectorResults()
        if results is None:
            return
        values = []
        for i in range(len(results)):
            result_item = results[i]
            values.append([result_item.getVariable(), result_item.getQValue(), result_item.getPValue()])

        del results
        import pandas as pd
        return pd.DataFrame(values, columns=["Variable", "Q", "P"])

    @staticmethod
    def _get_java_ecological_detector_result(java_object):
        results = java_object.getEcologicalDetectorResult()
        if results is None:
            return
        detector_values = results.getEcologicalDetectorValues()
        values = []
        for i in range(len(detector_values)):
            result_item = detector_values[i]
            values.append([
             result_item.getVariableRow(), result_item.getVariableCol(), result_item.getSig()])

        del results
        import pandas as pd
        return pd.DataFrame(values, columns=["VariableRow", "VariableCol", "Sig"])


def density_based_clustering(input_data, min_pile_point_count, search_distance, unit, out_data=None, out_dataset_name=None, progress=None):
    """
    密度聚类的DBSCAN实现

    该方法根据给定的搜索半径（search_distance）和该范围内需包含的最少点数（min_pile_point_count）将空间点数据中密度足够大且空间相近的区域相连，并消除噪声的干扰，以达到较好的聚类效果。

    :param input_data: 指定的要聚类的矢量数据集，支持点数据集。
    :type input_data: DatasetVector or str
    :param min_pile_point_count: 每类包含的最少点数
    :type min_pile_point_count: int
    :param search_distance: 搜索邻域的距离
    :type search_distance: int
    :param unit: 搜索距离的单位
    :type unit: Unit
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
    if not isinstance(_source_input, DatasetVector):
        raise ValueError("source input_data must be DatasetVector")
    if min_pile_point_count is None:
        raise ValueError("min pile point count is None")
    if search_distance is None:
        raise ValueError("search distance is None")
    else:
        if not isinstance(unit, Unit):
            raise ValueError("unit is illegal")
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + "_dbscan"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, "density_based_clustering")
                _jvm.com.supermap.analyst.spatialstatistics.ClusteringDistributions.addSteppedListener(listener)
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
            java_result_dt = _jvm.com.supermap.analyst.spatialstatistics.ClusteringDistributions.densityBasedClustering(_source_input._jobject, _ds._jobject, _outDatasetName, int(min_pile_point_count), float(search_distance), Unit._make(unit)._jobject)
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
                _jvm.com.supermap.analyst.spatialstatistics.ClusteringDistributions.removeSteppedListener(listener)
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


def hierarchical_density_based_clustering(input_data, min_pile_point_count, out_data=None, out_dataset_name=None, progress=None):
    """
    密度聚类的HDBSCAN实现

    该方法是对DBSCAN方法的改进，只需给定空间邻域范围内的最少点数（min_pile_point_count）。在DBSCAN的基础上，计算不同的搜索半径选择最稳定的空间聚类分布作为密度聚类结果。

    :param input_data: 指定的要聚类的矢量数据集，支持点数据集。
    :type input_data: DatasetVector or str
    :param min_pile_point_count: 每类包含的最少点数
    :type min_pile_point_count: int
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
        elif min_pile_point_count is None:
            raise ValueError("min pile point count is None")
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + "_hdbscan"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, "hierarchical_density_based_clustering")
                _jvm.com.supermap.analyst.spatialstatistics.ClusteringDistributions.addSteppedListener(listener)
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
            java_result_dt = _jvm.com.supermap.analyst.spatialstatistics.ClusteringDistributions.hierarchicalDensityBasedClustering(_source_input._jobject, _ds._jobject, _outDatasetName, int(min_pile_point_count))
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
                _jvm.com.supermap.analyst.spatialstatistics.ClusteringDistributions.removeSteppedListener(listener)
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


def ordering_density_based_clustering(input_data, min_pile_point_count, search_distance, unit, cluster_sensitivity, out_data=None, out_dataset_name=None, progress=None):
    """
    密度聚类的OPTICS实现

    该方法在DBSCAN的基础上，额外计算了每个点的可达距离，并基于排序信息和聚类系数（cluster_sensitivity）得到聚类结果。该方法对于搜索半径（search_distance）和该范围内需包含的最少点数（min_pile_point_count）不是很敏感，主要决定结果的是聚类系数（cluster_sensitivity）

    概念定义：
    - 可达距离：取核心点的核心距离和其到周围临近点距离的最大值。
    - 核心点：某个点在搜索半径内，存在点的个数不小于每类包含的最少点数（min_pile_point_count）。
    - 核心距离：某个点成为核心点的最小距离。
    - 聚类系数：为1~100的整数，是对聚类类别多少的标准量化，系数为1时聚类类别最少、100最多。

    :param input_data: 指定的要聚类的矢量数据集，支持点数据集。
    :type input_data: DatasetVector or str
    :param min_pile_point_count: 每类包含的最少点数
    :type min_pile_point_count: int
    :param search_distance: 搜索邻域的距离
    :type search_distance: int
    :param unit: 搜索距离的单位
    :type unit: Unit
    :param cluster_sensitivity: 聚类系数
    :type cluster_sensitivity: int
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
    if not isinstance(_source_input, DatasetVector):
        raise ValueError("source input_data must be DatasetVector")
    if min_pile_point_count is None:
        raise ValueError("min pile point count is None")
    if search_distance is None:
        raise ValueError("search distance is None")
    if cluster_sensitivity is None:
        raise ValueError("cluster sensitivity is None")
    else:
        if not isinstance(unit, Unit):
            raise ValueError("unit is illegal")
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + "_optics"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, "ordering_density_based_clustering")
                _jvm.com.supermap.analyst.spatialstatistics.ClusteringDistributions.addSteppedListener(listener)
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
            java_result_dt = _jvm.com.supermap.analyst.spatialstatistics.ClusteringDistributions.orderingDensityBasedClustering(_source_input._jobject, _ds._jobject, _outDatasetName, int(min_pile_point_count), float(search_distance), Unit._make(unit)._jobject, int(cluster_sensitivity))
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
                _jvm.com.supermap.analyst.spatialstatistics.ClusteringDistributions.removeSteppedListener(listener)
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


def spa_estimation(source_dataset, reference_dataset, source_unique_id_field, source_data_field, reference_unique_id_field, reference_data_fields, out_data=None, out_dataset_name=None, progress=None):
    """
    单点地域估计(SPA)

    :param source_dataset: 源数据集
    :type source_dataset: DataetVector or str
    :param reference_dataset: 参考数据集
    :type reference_dataset: DataetVector or str
    :param str source_unique_id_field: 源数据集唯一 ID 字段名称
    :param str source_data_field: 源数据集数据字段名称
    :param str reference_unique_id_field: 参考数据集唯一字段名称
    :param reference_data_fields: 参考数据集数据字段名称集合
    :type reference_data_fields: list[str] or tuple[str] or str
    :param out_data: 结果数据集所在数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 输出数据集的名称。
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 结果数据集
    :rtype: DatasetVector
    """
    _source_input = get_input_dataset(source_dataset)
    if not isinstance(_source_input, DatasetVector):
        raise ValueError("source_dataset must be DatasetVector")
    else:
        _ref_input = get_input_dataset(reference_dataset)
        if not isinstance(_ref_input, DatasetVector):
            raise ValueError("reference_dataset must be DatasetVector")
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _dest_dt_name = _source_input.name + "_spa"
        else:
            _dest_dt_name = out_dataset_name
    _dest_dt_name = _ds.get_available_dataset_name(_dest_dt_name)
    _jvm = get_jvm()
    reference_data_fields = split_input_list_from_str(reference_data_fields)
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, "spa_estimation")
                _jvm.com.supermap.analyst.spatialstatistics.SamplingInference.addSteppedListener(listener)
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
            java_result_dt = _jvm.com.supermap.analyst.spatialstatistics.SamplingInference.SPA(oj(_source_input), oj(_ref_input), str(source_unique_id_field), str(source_data_field), str(reference_unique_id_field), to_java_string_array(reference_data_fields), oj(_ds), str(_dest_dt_name))
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
                _jvm.com.supermap.analyst.spatialstatistics.SamplingInference.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


@unique
class BShadeEstimateMethod(JEnum):
    __doc__ = "\n    :var BShadeEstimateMethod.TOTAL: 总量方法，即按照样本与总体之比值。\n    :var BShadeEstimateMethod.MEAN: 均值方法，即按照样本均值与总体均值的比值。\n    "
    TOTAL = 1
    MEAN = 2

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialstatistics.BShadeEstimateMethod"


@unique
class BShadeSampleNumberMethod(JEnum):
    __doc__ = "\n    :var BShadeEstimateMethod.FIXED: 使用固定字段数目。\n    :var BShadeEstimateMethod.RANGE: 使用范围字段抽样数目。\n    "
    FIXED = 1
    RANGE = 2

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialstatistics.BShadeSampleNumberMethod"


class BShadeEstimationResult:
    __doc__ = "BShade估计结果"

    def __init__(self):
        self._dataset = None
        self._variance = None
        self._weights = None

    @property
    def dataset(self):
        """DatasetVector: BShade估计结果数据集"""
        return self._dataset

    @property
    def variance(self):
        """float: 估计方差"""
        return self._variance

    @property
    def weights(self):
        """list[float]: 权重数组"""
        return self._weights

    def _from_result(self, dataset, variance, weights):
        self._dataset = dataset
        self._variance = variance
        self._weights = weights
        return self

    def to_dict(self):
        """
        转成 dict。

        :return: 用于描述 BShade 估计结果的字典对象。
        :rtype: dict[str, object]
        """
        return {'dataset':self.dataset, 
         'variance':self.variance,  'weights':self.weights}


def bshade_estimation(source_dataset, historical_dataset, source_data_fields, historical_fields, estimate_method='TOTAL', out_data=None, out_dataset_name=None, progress=None):
    """

    BShade预测

    :param source_dataset: 源数据集
    :type source_dataset: DatasetVector or str
    :param historical_dataset: 历史数据集
    :type historical_dataset: DatasetVector or str
    :param source_data_fields: 源数据集数据字段名称集合
    :type source_data_fields: list[str] or tuple[str] or str
    :param historical_fields: 历史数据集数据字段名称集合
    :type historical_fields:  list[str] or tuple[str] or str
    :param estimate_method: 估计方法。包括总量和均值两种方法。
    :type estimate_method: BShadeEstimateMethod or str
    :param out_data: 结果数据集所在数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 输出数据集的名称。
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 分析结果
    :rtype: BShadeEstimationResult
    """
    _source_input = get_input_dataset(source_dataset)
    if not isinstance(_source_input, DatasetVector):
        raise ValueError("source_dataset must be DatasetVector")
    else:
        _historical_input = get_input_dataset(historical_dataset)
        if not isinstance(_historical_input, DatasetVector):
            raise ValueError("historical_dataset must be DatasetVector")
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = _source_input.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _dest_dt_name = _source_input.name + "_bshade"
        else:
            _dest_dt_name = out_dataset_name
    _dest_dt_name = _ds.get_available_dataset_name(_dest_dt_name)
    _jvm = get_jvm()
    source_data_fields = split_input_list_from_str(source_data_fields)
    historical_fields = split_input_list_from_str(historical_fields)
    estimate_method = BShadeEstimateMethod._make(estimate_method, "TOTAL")
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, "bshade_estimation")
                _jvm.com.supermap.analyst.spatialstatistics.SamplingInference.addSteppedListener(listener)
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
            java_result = _jvm.com.supermap.analyst.spatialstatistics.SamplingInference.BShadeEstimation(oj(_source_input), oj(_historical_input), to_java_string_array(source_data_fields), to_java_string_array(historical_fields), oj(estimate_method), oj(_ds), str(_dest_dt_name))
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
            _jvm.com.supermap.analyst.spatialstatistics.SamplingInference.removeSteppedListener(listener)
        except Exception as e1:
            try:
                log_error(e1)
            finally:
                e1 = None
                del e1

    if java_result is not None:
        result_dt = _ds[java_result.getResultDataset().getName()]
        return BShadeEstimationResult()._from_result(result_dt, java_result.getEstimatedVariance(), java_array_to_list(java_result.getWeights()))


class BShadeSamplingResult:
    __doc__ = "BShade抽样结果"

    def __init__(self):
        self._sample_number = None
        self._variance = None
        self._weights = None
        self._solution_names = None

    @property
    def sample_number(self):
        """int: 抽样字段数目"""
        return self._sample_number

    @property
    def estimate_variance(self):
        """float: 估计方差"""
        return self._variance

    @property
    def weights(self):
        """list[float]: 权重数组"""
        return self._weights

    @property
    def solution_names(self):
        """list[str]: 字段名称数组"""
        return self._solution_names

    def _from_result(self, sample_number, variance, weights, solution_names):
        self._sample_number = sample_number
        self._variance = variance
        self._weights = weights
        self._solution_names = solution_names
        return self

    def to_dict(self):
        """
        转成 dict。

        :return: 用于描述 BShade 抽样结果的字典对象
        :rtype: dict[str, object]
        """
        return {'sample_number':self.sample_number, 
         'estimate_variance':self.estimate_variance,  'weights':self.weights,  'solution_names':self.solution_names}


class BShadeSamplingParameter:
    __doc__ = "\n    BShade抽样参数。\n\n    在抽样过程中会用到模拟退火算法，该方法中将包含模拟退火算法的多个参数。模拟退火算法是用来求解函数最小值的。\n    "

    def __init__(self):
        self._sample_number_method = BShadeSampleNumberMethod.FIXED
        self._estimate_method = BShadeEstimateMethod.TOTAL
        self._select_sample_num = 5
        self._select_sample_rangel = 3
        self._select_sample_rangeu = 5
        self._select_sample_range_step = 2
        self._init_temperature = 1.0
        self._min_temperature = 1e-08
        self._min_energy = -1e+38
        self._cool_rate = 0.9
        self._max_cons_rej = 1000
        self._max_try = 300
        self._max_success = 20
        self._max_full_combination = 5000

    @property
    def bshade_sample_number_method(self):
        """BShadeSampleNumberMethod: BShade抽样数目方法"""
        return self._sample_number_method

    def set_bshade_sample_number_method(self, value):
        """
        设置BShade抽样数目方法。默认值为 FIXED

        :param value: BShade抽样数目方法
        :type value: BShadeSampleNumberMethod or str
        :return: self
        :rtype: BShadeSamplingParameter
        """
        value = BShadeSampleNumberMethod._make(value, "FIXED")
        if value is not None:
            self._sample_number_method = value
        return self

    @property
    def bshade_estimate_method(self):
        """BShadeEstimateMethod: BShade估计方法"""
        return self._estimate_method

    def set_bshade_estimate_method(self, value):
        """
        设置BShade估计方法。即按照总量或者均值计算样本

        :param value: BShade估计方法，默认值为 TOTAL
        :type value: BShadeEstimateMethod or str
        :return: self
        :rtype: BShadeSamplingParameter
        """
        value = BShadeEstimateMethod._make(value, "total")
        if value is not None:
            self._estimate_method = value
        return self

    @property
    def select_sample_number(self):
        """int: 选择样本数目"""
        return self._select_sample_num

    def set_select_sample_number(self, value):
        """
        设置选择样本数目

        :param int value: 选择样本数目
        :return: self
        :rtype: BShadeSamplingParameter
        """
        if value is not None:
            self._select_sample_num = int(value)
        return self

    @property
    def select_sample_range_lower(self):
        """int: 范围抽样数目下限"""
        return self._select_sample_rangel

    def set_select_sample_range_l(self, value):
        """
        设置范围抽样数目下限

        :param int value: 范围抽样数目下限
        :return: self
        :rtype: BShadeSamplingParameter
        """
        if value is not None:
            self._select_sample_rangel = int(value)
        return self

    @property
    def select_sample_range_upper(self):
        """int: 范围抽样数目上限"""
        return self._select_sample_rangeu

    def set_select_sample_range_u(self, value):
        """
        设置范围抽样数目上限

        :param int value: 范围抽样数目上限
        :return: self
        :rtype: BShadeSamplingParameter
        """
        if value is not None:
            self._select_sample_rangeu = int(value)
        return self

    @property
    def select_sample_range_step(self):
        """int: 范围抽样步长"""
        return self._select_sample_range_step

    def set_select_sample_range_step(self, value):
        """
        设置范围抽样步长

        :param int value: 范围抽样步长
        :return: self
        :rtype: BShadeSamplingParameter
        """
        if value is not None:
            self._select_sample_range_step = int(value)
        return self

    @property
    def initial_temperature(self):
        """float: 起始温度"""
        return self._init_temperature

    def set_initial_temperature(self, value):
        """
        设置起始温度

        :param float value: 起始温度
        :return: self
        :rtype: BShadeSamplingParameter
        """
        if value is not None:
            self._init_temperature = float(value)
        return self

    @property
    def min_temperature(self):
        """float: 最小温度，即停止温度"""
        return self._min_temperature

    def set_min_temperature(self, value):
        """
        设置最小温度，即停止温度

        :param float value: 最小温度，即停止温度
        :return: self
        :rtype: BShadeSamplingParameter
        """
        if value is not None:
            self._min_temperature = float(value)
        return self

    @property
    def min_energy(self):
        """float: 最小能量，即停止能量"""
        return self._min_energy

    def set_min_energy(self, value):
        """
        设置最小能量，即停止能量

        :param float value: 最小能量，即停止能量
        :return: self
        :rtype: BShadeSamplingParameter
        """
        if value is not None:
            self._min_energy = float(value)
        return self

    @property
    def cool_rate(self):
        """float: """
        return self._cool_rate

    def set_cool_rate(self, value):
        """
        设置退火速率

        :param float value: 退火速率
        :return: self
        :rtype: BShadeSamplingParameter
        """
        if value is not None:
            self._cool_rate = float(value)
        return self

    @property
    def max_consecutive_rejection(self):
        """int: 最大连续拒绝数目"""
        return self._max_cons_rej

    def set_max_consecutive_rejection(self, value):
        """
        设置最大连续拒绝数目

        :param int value: 最大连续拒绝数目
        :return: self
        :rtype: BShadeSamplingParameter
        """
        if value is not None:
            self._max_cons_rej = int(value)
        return self

    @property
    def max_try(self):
        """int: 最大尝试数目"""
        return self._max_try

    def set_max_try(self, value):
        """
        设置最大尝试数目

        :param int value: 最大尝试数目
        :return: self
        :rtype: BShadeSamplingParameter
        """
        if value is not None:
            self._max_try = int(value)
        return self

    @property
    def max_success(self):
        """int: 在一个温度内的最大成功数目"""
        return self._max_success

    def set_max_success(self, value):
        """
        设置在一个温度内的最大成功数目

        :param int value: 最大成功数目
        :return: self
        :rtype: BShadeSamplingParameter
        """
        if value is not None:
            self._max_success = int(value)
        return self

    @property
    def max_full_combination(self):
        """int: 最大字段组合数目"""
        return self._max_full_combination

    def set_max_full_combination(self, value):
        """
        设置最大字段组合数目

        :param int value: 最大字段组合数目
        :return: self
        :rtype: BShadeSamplingParameter
        """
        if value is not None:
            self._max_full_combination = int(value)
        return self

    @property
    def _jobject(self):
        java_object = get_jvm().com.supermap.analyst.spatialstatistics.BShadeSamplingParameter()
        if self.bshade_sample_number_method is not None:
            java_object.setBShadeSampleNumberMethod(oj(self.bshade_sample_number_method))
        if self.bshade_estimate_method is not None:
            java_object.setBShadeEstimateMethod(oj(self.bshade_estimate_method))
        if self.select_sample_number is not None:
            java_object.setSelectSampleNumber(int(self.select_sample_number))
        if self.select_sample_range_lower is not None:
            java_object.setSelectSampleRangeL(int(self.select_sample_range_lower))
        if self.select_sample_range_upper is not None:
            java_object.setSelectSampleRangeU(int(self.select_sample_range_upper))
        if self.select_sample_range_step is not None:
            java_object.setSelectSampleRangeStep(int(self.select_sample_range_step))
        if self.initial_temperature is not None:
            java_object.setInitialTemperature(float(self.initial_temperature))
        if self.min_temperature is not None:
            java_object.setMinTemperature(float(self.min_temperature))
        if self.min_energy is not None:
            java_object.setMinEnergy(float(self.min_energy))
        if self.cool_rate is not None:
            java_object.setCoolRate(float(self.cool_rate))
        if self.max_consecutive_rejection is not None:
            java_object.setMaxConsecutiveRejection(int(self.max_consecutive_rejection))
        if self.max_try is not None:
            java_object.setMaxTry(int(self.max_try))
        if self.max_success is not None:
            java_object.setMaxSuccess(int(self.max_success))
        if self.max_full_combination is not None:
            java_object.setMaxFullCombination(int(self.max_full_combination))
        return java_object


def bshade_sampling(historical_dataset, historical_fields, parameter, progress=None):
    """
    BShade抽样。

    :param historical_dataset: 历史数据集。
    :type historical_dataset: DatasetVector or str
    :param historical_fields: 历史数据集数据字段名称集合。
    :type historical_fields: list[str] or tuple[str] or str
    :param BShadeSamplingParameter parameter: 参数设置。
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 分析结果。
    :rtype: list[BShadeSamplingResult]
    """
    _historical_input = get_input_dataset(historical_dataset)
    if not isinstance(_historical_input, DatasetVector):
        raise ValueError("historical_dataset must be DatasetVector")
    if not isinstance(parameter, BShadeSamplingParameter):
        raise ValueError("parameter required BShadeSamplingParameter ")
    _jvm = get_jvm()
    historical_fields = split_input_list_from_str(historical_fields)
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, "bshade_simpling")
                _jvm.com.supermap.analyst.spatialstatistics.SamplingInference.addSteppedListener(listener)
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
            java_result = _jvm.com.supermap.analyst.spatialstatistics.SamplingInference.BShadeSampling(oj(_historical_input), to_java_string_array(historical_fields), oj(parameter))
        except Exception as e:
            try:
                import traceback
                log_error(traceback.format_exc())
                java_result = None
            finally:
                e = None
                del e

    finally:
        return

    if listener is not None:
        try:
            _jvm.com.supermap.analyst.spatialstatistics.SamplingInference.removeSteppedListener(listener)
        except Exception as e1:
            try:
                log_error(e1)
            finally:
                e1 = None
                del e1

    if java_result is not None:
        results = []
        for item in java_result:
            result = BShadeSamplingResult()._from_result(item.getSampleNumber(), item.getEstimatedVariance(), java_array_to_list(item.getWeights()), java_array_to_list(item.getSolutionNames()))
            results.append(result)

        return results

# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/_jsuperpy\_numpy.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 43530 bytes
r"""

_numpy 模块用于 SuperMap 数据与 `numpy`_ 的 ndarray 数据交换，通过使用 _numpy 可以将SuperMap 中的矢量数据集、影像数据集和栅格数据集
导出为 numpy 的 ndarray，同时也支持将 ndarray 写入到 SuperMap 中的矢量数据集或栅格数据集中：

.. _numpy: http://www.numpy.org/

    - :py:meth:`recordset_to_numpy_array` 和 :py:meth:`datasetvector_to_numpy_array` 用于将矢量数据写出为 ndarray。写出的 ndarray 为一维数组，数组的每
      项元素均含有多个子元素，可以直接使用列名称获取子项所在的列，例如，通过下面的代码可以直接读取矢量数据：

        >>> narray = datasetvector_to_numpy_array(data_dir + 'example_data.udb/Town_P', export_spatial=True)
        >>> print('ndarray.ndim : ' + str(narray.ndim))
        ndarray.ndim : 1
        >>> print('ndarray.dtype : ' + str(narray.dtype))
        ndarray.dtype : [('NAME', '<U9'), ('SmX', '<f8'), ('SmY', '<f8')]
        >>> print(narray[:10])
        [('百尺竿乡', 115.917748, 39.53525099) ('什刹海', 116.380351, 39.93393099)
         ('月坛', 116.344828, 39.91476099) ('广安门内', 116.365305, 39.89622499)
         ('牛街', 116.36388 , 39.88680299) ('崇文门外', 116.427342, 39.89467499)
         ('永定门外', 116.402249, 39.86559299) ('崔各庄', 116.515447, 39.99966499)
         ('小关', 116.411727, 39.97737199) ('潘家园', 116.467911, 39.87179299)]
        >>> print(narray['SmX'][:10])
        [115.917748 116.380351 116.344828 116.365305 116.36388  116.427342
         116.402249 116.515447 116.411727 116.467911]
        >>> xy_array = np.c_[narray['SmX'], narray['SmY']][:10]
        >>> print(xy_array.ndim)
        2
        >>> print(xy_array.dtype)
        float64
        >>> print(xy_array)
        [[115.917748    39.53525099]
         [116.380351    39.93393099]
         [116.344828    39.91476099]
         [116.365305    39.89622499]
         [116.36388     39.88680299]
         [116.427342    39.89467499]
         [116.402249    39.86559299]
         [116.515447    39.99966499]
         [116.411727    39.97737199]
         [116.467911    39.87179299]]

      写出矢量数据时，可以选择是否写出空间信息，对于点对象，将写出点的 X 和 Y 值到 SmX 列和 SmY 列中，对线对象，将写出线的内点 :py:meth:`GeoLine.get_inner_point` 到 SmX 列和 SmY列，并将线
      的长度字段值 `SmLength` 写出为 `SmLength` 列。对于面对象，将写出面的内点 :py:meth:`GeoRegion.get_inner_point` 到 SmX 列和 SmY列，并将面的周长字段值 `SmPerimeter` 写出为 `SmPerimeter` 列，
      面的面积字段值 `SmArea` 写出为 `SmArea` 列。

        >>> narray = datasetvector_to_numpy_array(data_dir + 'example_data.udb/Landuse_R', export_spatial=True)
        >>> print(narray.dtype)
        [('LANDTYPE', '<U4'), ('Area', '<f4'), ('Area_1', '<i2'), ('SmX', '<f8'), ('SmY', '<f8'), ('SmPerimeter', '<f8'), ('SmArea', '<f8')]
        >>> print(narray[:10])
        [('用材林', 132., 132, 116.47779337, 40.87251703, 0.75917921, 1.40894401e-02)
         ('用材林',  97.,  97, 116.6540059 , 40.94696274, 0.4945153 , 1.03534475e-02)
         ('灌丛',  36.,  36, 116.58451795, 40.98712283, 0.25655489, 3.89923745e-03)
         ('灌丛',  36.,  36, 116.89611418, 40.76792703, 0.59237713, 3.81791878e-03)
         ('用材林',   1.,   1, 116.37943683, 40.91435429, 0.03874328, 7.08450886e-05)
         ('灌丛', 126., 126, 116.49117083, 40.78302383, 0.53664074, 1.34577856e-02)
         ('用材林',  83.,  83, 116.69943237, 40.74456848, 0.39696365, 8.83225363e-03)
         ('用材林', 128., 128, 116.8129727 , 40.69116153, 0.56949408, 1.35877743e-02)
         ('用材林',  29.,  29, 116.24543769, 40.71076092, 0.30082509, 3.07221559e-03)
         ('灌丛', 467., 467, 116.43290772, 40.50875567, 1.91745792, 4.95537433e-02)]

    - :py:meth:`datasetraster_to_numpy_array` 支持将影像数据集和栅格数据集写出到 numpy 的 ndarray，影像数据集支持多波段影像。在写出影像数据集时:

        - 如果是 RGB 或 RGBA 像素格式的影像数据集，将会写出为为维度为3的数组，地中第一个维度的大小为3（RGB）或4（RGBA），第二维度为为行，第三维度为列；
        - 如果是单波段数据集，将会写出为一个维度为2的数组第一维度为行，第二维度为列；
        - 如果波段数目大于1，将会写出一个维度为3的数组，其中第一维度为波段，第二维度为为行，第三维度为列；

        如果写出为栅格数据集，因为栅格数据集不支持多波段，所以将会写出为一个维度为2的数组。

        写出一个 RGB 影像数据集::

            >>> datasetraster_to_numpy_array(data_dir + 'example_data.udb/seaport')
            >>> print(k_array.ndim)
            3
            >>> print(k_array.shape)
            (3, 1537, 1728)
            >>> print(k_array.dtype)
            uint8
            >>> print(k_array)
            [[[ 21  21  21 ... 192 194 191]
              [ 21  21  21 ... 191 192 190]
              [ 21  21  21 ... 190 192 193]
              ...
              [ 98  94  91 ...  31  31  29]
              [101  97  94 ...  30  30  29]
              [116 114 110 ...  24  24  24]]

             [[ 56  56  56 ... 196 198 195]
              [ 56  56  56 ... 195 196 194]
              [ 56  56  56 ... 194 196 197]
              ...
              [119 115 111 ...  25  25  26]
              [125 121 114 ...  24  24  26]
              [116 114 110 ...  24  24  24]]

             [[ 75  75  75 ... 179 181 181]
              [ 75  75  75 ... 178 179 180]
              [ 75  75  75 ... 177 179 183]
              ...
              [110 106 102 ...  35  35  33]
              [112 108 105 ...  34  34  33]
              [116 114 110 ...  24  24  24]]]

        写出一个像素格式为 BIT16 的栅格数据集::

            >>> datasetraster_to_numpy_array(data_dir + 'example_data.udb/DEM')
            >>> print(k_array.ndim)
            2
            >>> print(k_array.shape)
            (4849, 5892)
            >>> print(k_array.dtype)
            int16
            >>> print(k_array)
            [[-32768 -32768 -32768 ... -32768 -32768 -32768]
             [-32768 -32768 -32768 ... -32768 -32768 -32768]
             [-32768 -32768 -32768 ... -32768 -32768 -32768]
             ...
             [-32768 -32768 -32768 ... -32768 -32768 -32768]
             [-32768 -32768 -32768 ... -32768 -32768 -32768]
             [-32768 -32768 -32768 ... -32768 -32768 -32768]]

        另外，需要注意的是 origin_is_left 可以指定生成的数组原点（第0行第0列）对应在 SuperMap 栅格数据集或影像数据集中的左上角还是左下角。在SuperMap的栅格数据集和影像数据集中
        第0行和第0列位于左上角，往下则行递增，往右则列递增 ::

            [[(0,0),       (0,1),        (0,2), ...        (0, width-2),       (0, width-1)]
            [(1,0),        (1,1),        (1,2), ...        (1, width-2),       (1, width-1)]
            [(2,0),        (2,1),        (0,2), ...        (2, width-2),       (2, width-1)]
            ...                                 ...                             ...
            [(height-2,0), (height-2,1), (height-2,2), ... (height-2, width-2), (height-2, width-1)]
            [(height-1,0), (height-1,1), (height-1,2), ... (height-1, width-2), (height-1, width-1)]]

        但在其他软件中可能第0行和第0列位于左下角，往上则行递增，往右则列递增 ::

            [(height-1,0), (height-1,1), (height-1,2), ... (height-1, width-2), (height-1, width-1)]]
            [(height-2,0), (height-2,1), (height-2,2), ... (height-2, width-2), (height-2, width-1)]
            ...                                 ...                            ...
            [(2,0),        (2,1),        (0,2), ...        (2, width-2),       (2, width-1)]
            [(1,0),        (1,1),        (1,2), ...        (1, width-2),       (1, width-1)]
            [(0,0),       (0,1),         (0,2), ...        (0, width-2),       (0, width-1)]

        所以用户可以根据具体使用情况，选择将左上角还是左下角作为数组的原点。

    - :py:meth:`numpy_array_to_datasetvector` 支持将一个含有 dtype 信息和列名称的 ndarray 数组写入到 SuperMap 的矢量数据集中，如果指定了 X 和 Y 字段值的列名称，将会写入为
      点数据集，否则，将写入为属性表数据集。注意的是，ndarray 必须含有列名称才可能写入::

            >>> narray = np.empty(10, dtype=[('ID', 'int32'), ('X', 'float64'), ('Y', 'float64'), ('NAME', 'U10'), ('COUNT', 'int32')])
            >>> narray[0] = 1, 116.380351, 39.93393099, '什刹海', 1023
            >>> narray[1] = 2, 116.365305, 39.89622499, '广安门内', 10
            >>> narray[2] = 3, 116.427342, 39.89467499, '崇文门外', 238
            >>> narray[3] = 4, 116.490881, 39.96567299, '酒仙桥', 1788
            >>> narray[4] = 5, 116.447486, 39.93767799, '三里屯', 8902
            >>> narray[5] = 6, 116.347435, 40.08078599, '回龙观', 903
            >>> narray[6] = 7, 116.407196, 39.83895899, '大红门', 88
            >>> narray[7] = 8, 116.396915, 39.88371499, '天桥', 5
            >>> narray[8] = 9, 116.334522, 40.03594199, '清河', 77
            >>> narray[9] = 10, 116.03008, 39.87852799, '潭柘寺', 1
            >>> result = numpy_array_to_datasetvector(narray, out_dir + 'narray_out.udb', x_col='X', y_col='Y')

    - :py:meth:`numpy_array_to_datasetraster` 支持将一个二维数组或三维数组写入到影像数据集或栅格数据集中，如果选择写入到栅格数据集，则只能是二维数组，如果
      写入到影像数据集，数组为三维数组时，第一个维度必须为波段信息，同时第二维度和第三维度必须为行和列::

            >>> d = numpy.empty((100, 100), dtype='float32')
            >>> for i in range(100):
            ...     for j in range(100):
            ...     d[i][j] = i * j + i
            >>> iobjects.numpy_array_to_datasetraster(d, 0.1, 0.1, out_dir + 'narray_out.udb', as_grid=True)

需要注意:
    - :py:meth:`datasetvector_to_numpy_array` 和 :py:meth:`datasetraster_to_numpy_array` 两个接口中，被写数据集对象的 source 参数接受输入一个数据集对象）
      或数据源别名与数据集名称的组合（例如，'alias/dataset_name', 'alias\dataset_name'),，也支持数据源连接信息与数据集名称的组合（例如， 'E:/data.udb/dataset_name')
      ，值得注意的是，当输入的是数据源信息时，程序会自动打开数据源，但是不会自动关闭数据源，也就是打开后的数据源会存在当前工作空间中

    - :py:meth:`numpy_array_to_datasetvector` 和 :py:meth:`numpy_array_to_datasetraster` 两个接口中，结果数据源对象的 output 参数输入结果数据集的数据源信息，
      可以为 Datasource 对象，也可以为 DatasourceConnectionInfo 对象，同时，也支持当前工作空间下数据源的别名，也支持 UDB 文件路基，DCF 文件路径等。

"""
import numpy
from data._util import get_input_dataset, get_output_datasource, check_output_datasource, try_close_output_datasource
from .data import DatasetVector, DatasetGridInfo, Rectangle, DatasetImageInfo, DatasetGrid, DatasetImage, FieldInfo, DatasetVectorInfo, GeoPoint
from .enums import FieldType, PixelFormat, DatasetType
from ._utils import read_float, read_int, write_float, write_int, oj
from ._gateway import get_jvm
from ._logger import *
import io, datetime, threading
from iobjectspy.rpc._utils import decode_tile
import tempfile, os
__all__ = [
 'recordset_to_numpy_array', 'datasetvector_to_numpy_array', 'numpy_array_to_datasetvector', 
 'datasetraster_to_numpy_array', 
 'numpy_array_to_datasetraster']

def _to_numpy_type(fieldInfo):
    _field_to_numpy = {(FieldType.BOOLEAN): "?", 
     (FieldType.BYTE): "B", 
     (FieldType.INT16): "int16", 
     (FieldType.INT32): "int32", 
     (FieldType.INT64): "int64", 
     (FieldType.SINGLE): "float32", 
     (FieldType.DOUBLE): "float64", 
     (FieldType.DATETIME): "datetime64[s]", 
     (FieldType.LONGBINARY): "S", 
     (FieldType.TEXT): "U", 
     (FieldType.WTEXT): "U", 
     (FieldType.CHAR): "U", 
     (FieldType.JSONB): "U"}
    return _field_to_numpy[fieldInfo.type]


def _get_default_null_value(fieldInfo):
    _default_null = {(FieldType.BOOLEAN): None, 
     (FieldType.BYTE): (-128), 
     (FieldType.INT16): (-32768), 
     (FieldType.INT32): (-2147483648), 
     (FieldType.INT64): (-9223372036854775808L), 
     (FieldType.SINGLE): (numpy.nan), 
     (FieldType.DOUBLE): (numpy.nan), 
     (FieldType.DATETIME): None, 
     (FieldType.LONGBINARY): None, 
     (FieldType.TEXT): "", 
     (FieldType.WTEXT): "", 
     (FieldType.CHAR): "", 
     (FieldType.JSONB): ""}
    return _default_null[fieldInfo.type]


def recordset_to_numpy_array(recordset, fields=None, export_spatial=False, skip_null_value=True, null_values=None):
    """
    将一个记录集写出到 numpy.ndarray 中，支持将点数据集、线数据集、面数据集和属性表数据集的记录集写出。

    :param Recordset recordset: 被写出数据集的记录集
    :param fields: 需要写出的字段名称，如果为 None，则将全部非系统字段都写出
    :type fields: list[str]
    :param bool export_spatial: 是否写出空间几何信息，对点对象，将直接写出点的 X 和 Y 值到 ‘SmX’ 和 ‘SmY’ 列中。对于线面对象，将写出线和面对象的内点，并输出到 ‘SmX’ 和 ‘SmY’ 列中，同时，线将写出 ‘SmLength’字段，面将写出 ‘SmPerimeter’ 和 ‘SmArea 字段。
    :param is skip_null_value: 是否跳过含有空值的记录。numpy数组中，不支持整型类型的值为空值，如果列的类型为整型类型但又是空值，可能会写出失败。所以，如果数据集中字段含有空值，需要填入一个空值。对于浮点型的字段，空值为 numpy.nan，对于文本型（TEXT，WTEXT，CHAR，JSONB）为空字符串，布尔类型、二进制类型和时间类型字段的空值为 None。
    :param null_values: 指定的字段对应的空值，key 值为字段名称或字段序号，value 为指定的空值，value 的值的类型需要与字段的类型匹配。例如，需要指定字段整型字段 ID 的空值为 -9999，则 null_values = {'ID': -9999}
    :type null_values: dict
    :return: numpy 数组，将返回一个维度为1的数组。
    :rtype: numpy.ndarray
    """
    if recordset is None:
        raise ValueError("recordset is None")
    elif recordset.get_record_count() is 0:
        return
        datasetType = recordset.dataset.type
        if datasetType not in [DatasetType.POINT, DatasetType.LINE, DatasetType.REGION, DatasetType.TABULAR]:
            raise ValueError("invalid dataset type, support point, line, region and tabular dataset, but now is " + str(datasetType))
        if fields is not None:
            if not isinstance(fields, (tuple, list)):
                raise ValueError("fields must be tuple or list")
            fieldIndexes = []
            dataTypes = []
            for field in fields:
                index = recordset.index_of_field(field)
                if index is not None:
                    fieldIndexes.append(index)
                    fieldInfo = recordset.get_field_info(index)
                    dataTypes.append((fieldInfo.name, _to_numpy_type(fieldInfo)))

        else:
            fieldIndexes = []
            fieldCount = recordset.get_field_count()
            dataTypes = []
            for i in range(fieldCount):
                fieldInfo = recordset.get_field_info(i)
                if fieldInfo is not None:
                    fieldInfo.is_system_field() or fieldIndexes.append(i)
                    dataTypes.append((fieldInfo.name, _to_numpy_type(fieldInfo)))

        if export_spatial and datasetType is not DatasetType.TABULAR:
            dataTypes.append(('SmX', 'float64'))
            dataTypes.append(('SmY', 'float64'))
            if datasetType is DatasetType.LINE:
                dataTypes.append(('SmLength', 'float64'))
            else:
                if datasetType is DatasetType.REGION:
                    dataTypes.append(('SmPerimeter', 'float64'))
                    dataTypes.append(('SmArea', 'float64'))
            export_spatial = True
    else:
        export_spatial = False
    valuesMaxSize = None
    fieldValues = []
    fieldInfos = list((recordset.get_field_info(k) for k in range(recordset.get_field_count())))
    i = 0
    values = []
    record_count = recordset.get_record_count()
    while i < record_count:
        i += 1
        values.clear()
        is_break = False
        for fieldIndex in fieldIndexes:
            value = recordset.get_value(fieldIndex)
            if value is not None:
                if isinstance(value, datetime.datetime):
                    values.append(value.strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    values.append(value)
            elif skip_null_value:
                is_break = True
                break
            else:
                if null_values is not None and fieldInfos[fieldIndex].name in null_values.keys():
                    nullValue = null_values[fieldInfos[fieldIndex].name]
                else:
                    nullValue = _get_default_null_value(fieldInfos[fieldIndex])
                values.append(nullValue)

        if is_break:
            recordset.move_next()
            continue
        elif export_spatial:
            geo = recordset.get_geometry()
            if geo is not None:
                if datasetType is DatasetType.POINT:
                    values.append(geo.get_x())
                    values.append(geo.get_y())
                else:
                    if datasetType is DatasetType.LINE:
                        _point = geo.get_inner_point()
                        values.append(_point.x)
                        values.append(_point.y)
                        values.append(geo.length)
                    else:
                        _point = geo.get_inner_point()
                        values.append(_point.x)
                        values.append(_point.y)
                        values.append(geo.perimeter)
                        values.append(geo.area)
            else:
                recordset.move_next()
                continue
        recordset.move_next()
        if valuesMaxSize is None:
            valuesMaxSize = []
            k = -1
            while k < len(dataTypes) - 1:
                k += 1
                if dataTypes[k][1] in ('U', 'S'):
                    if values[k] is not None:
                        valuesMaxSize.append(len(values[k]))
                    else:
                        valuesMaxSize.append(0)
                else:
                    valuesMaxSize.append(None)

        else:
            k = -1
            while k < len(dataTypes) - 1:
                k += 1
                if dataTypes[k][1] in ('U', 'S'):
                    try:
                        if values[k] is not None:
                            if len(values[k]) > valuesMaxSize[k]:
                                valuesMaxSize[k] = len(values[k])
                    except Exception as e:
                        try:
                            print(recordset.getID())
                            raise e
                        finally:
                            e = None
                            del e

        fieldValues.append(tuple(values))

    reset_size_datatypes = []
    i = -1
    while i < len(dataTypes) - 1:
        i += 1
        if dataTypes[i][1] in ('U', 'S'):
            reset_size_datatypes.append((dataTypes[i][0], dataTypes[i][1] + str(valuesMaxSize[i])))
        else:
            reset_size_datatypes.append(dataTypes[i])

    return numpy.array(fieldValues, dtype=reset_size_datatypes)


def datasetvector_to_numpy_array(source, attr_filter=None, fields=None, export_spatial=False, skip_null_value=True, null_values=None):
    """
    将矢量数据集写出到 numpy 的数组中

    :param source: 被写出的矢量数据集，支持点、线、面和属性表数据集。支持输入数据集对象以及数据源信息和数据集名称的组合形式，例如 ’alias|point'
    :type source: DatasetVector or str
    :param str attr_filter: 属性过滤条件
    :param fields: 需要写出的字段，如果为None，将写出所有的非系统字段
    :type fields: list[str]
    :param bool export_spatial: 是否导出空间几何对象，对点对象，将直接写出点的 X 和 Y 值到 ‘SmX’ 和 ‘SmY’ 列中。对于线面对象，将写出线和面对象的内点，并输出到 ‘SmX’ 和 ‘SmY’ 列中，同时，线将写出 ‘SmLength’字段，面将写出 ‘SmPerimeter’ 和 ‘SmArea 字段。
    :param is skip_null_value: 是否跳过含有空值的记录。numpy数组中，不支持整型类型的值为空值，如果列的类型为整型类型但又是空值，可能会写出失败。所以，如果数据集中字段含有空值，需要填入一个空值。对于浮点型的字段，空值为 numpy.nan，对于文本型（TEXT，WTEXT，CHAR，JSONB）为空字符串，布尔类型、二进制类型和时间类型字段的空值为 None。
    :param null_values: 指定的字段对应的空值，key 值为字段名称或字段序号，value 为指定的空值，value 的值的类型需要与字段的类型匹配。例如，需要指定字段整型字段 ID 的空值为 -9999，则 null_values = {'ID': -9999}
    :type null_values: dict
    :return: numpy 数组，将返回一个维度为1的数组。
    :rtype: numpy.ndarray
    """
    dt = get_input_dataset(source)
    if dt is None:
        raise ValueError("cannot get valid dataset object from source")
    if isinstance(dt, DatasetVector):
        rd = dt.query_with_filter(attr_filter, result_fields=fields, cursor_type="STATIC")
        if rd is None:
            raise RuntimeError("Failed to query recordset with attribute filter: " + attr_filter)
        narray = recordset_to_numpy_array(rd, fields, export_spatial, skip_null_value=skip_null_value, null_values=null_values)
        rd.close()
        return narray
    raise ValueError("Unsupported source type " + str(type(source)))


def _to_supermap_type(dtype):
    field_to_sm = {(numpy.bool_): (FieldType.BOOLEAN), 
     (numpy.byte): (FieldType.BYTE), 
     (numpy.int8): (FieldType.CHAR), 
     (numpy.short): (FieldType.INT16), 
     (numpy.int32): (FieldType.INT32), 
     (numpy.int64): (FieldType.INT64), 
     (numpy.longlong): (FieldType.INT64), 
     (numpy.ubyte): (FieldType.INT16), 
     (numpy.ushort): (FieldType.INT32), 
     (numpy.uint32): (FieldType.INT64), 
     (numpy.uint64): (FieldType.INT64), 
     (numpy.single): (FieldType.SINGLE), 
     (numpy.double): (FieldType.DOUBLE), 
     (numpy.float_): (FieldType.DOUBLE), 
     (numpy.float16): (FieldType.SINGLE), 
     (numpy.float32): (FieldType.DOUBLE), 
     (numpy.float64): (FieldType.DOUBLE), 
     (numpy.datetime64): (FieldType.DATETIME), 
     (numpy.str_): (FieldType.WTEXT), 
     (numpy.unicode_): (FieldType.WTEXT), 
     (numpy.bytes_): (FieldType.LONGBINARY), 
     (numpy.object_): (FieldType.WTEXT)}
    if dtype in field_to_sm.keys():
        return field_to_sm[dtype]
    return


def _to_sm_value(value, dtype):
    if dtype is numpy.datetime64:
        dt = value.astype(datetime.datetime)
        if isinstance(dt, int):
            return int(dt * 1e-09)
        return dt
    return value


def numpy_array_to_datasetvector(narray, output, out_dataset_name=None, x_col=None, y_col=None):
    """
    将 numpy 的数组写入到 SuperMap 的矢量数据集中

    :param numpy.ndarray narray: 被写入的 numpy 数组
    :param output: 结果数据源对象
    :type output: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param str x_col: 写入为点数据集时，点对象 X 值所在的列。如果为空，则写入为属性表数据集。
    :param str y_col: 写入为点数据集时，点对象 Y 值所在的列。如果为空，则写入为属性表数据集。
    :return: 结果数据集对象或数据集名称。
    :rtype: DatasetVector or str
    """
    if narray is None:
        raise ValueError("narray is None")
    elif narray.dtype is None:
        raise ValueError("narray have no dtype")
    ds = get_output_datasource(output)
    check_output_datasource(ds)
    if out_dataset_name is None:
        out_dataset_name = "NewDataset"
    fieldInfos = []
    indexes = {}
    names = narray.dtype.names
    k = 0
    for i in range(len(names)):
        name = names[i]
        if name.lower().startswith("sm"):
            continue
        else:
            field_datatype = narray.dtype[name]
            fieldType = _to_supermap_type(field_datatype.type)
            if fieldType is None:
                raise ValueError("Unsupported data type " + str(field_datatype))
            if fieldType is FieldType.WTEXT:
                strd = field_datatype.str
                try:
                    msize = int(strd[2[:None]])
                except:
                    msize = 255

                fieldInfos.append(FieldInfo(name, fieldType, msize))
            else:
                fieldInfos.append(FieldInfo(name, fieldType))
        indexes[k] = i
        k += 1

    is_point = False
    if x_col in names:
        if narray.dtype[x_col].type in (
         numpy.short, numpy.int32, numpy.int64, numpy.single, numpy.double,
         numpy.ushort, numpy.uint32, numpy.uint64, numpy.float_,
         numpy.float16, numpy.float32, numpy.float64) and y_col in names and narray.dtype[y_col].type in (
         numpy.short, numpy.int32, numpy.int64, numpy.single, numpy.double,
         numpy.ushort, numpy.uint32, numpy.uint64, numpy.float_,
         numpy.float16, numpy.float32, numpy.float64):
            dt = ds.create_dataset(DatasetVectorInfo(out_dataset_name, "POINT"), True)
            is_point = True
            indexOfX = names.index(x_col)
            indexOfY = names.index(y_col)
        else:
            dt = ds.create_dataset(DatasetVectorInfo(out_dataset_name, "TABULAR"), True)
        if dt is None:
            raise RuntimeError("Failed to create result dataset")
        name_pair = {}
        for name in names:
            name_pair[name] = name

        for fieldInfo in fieldInfos:
            available_field_name = dt.get_available_field_name(fieldInfo.name)
            name_pair[available_field_name] = fieldInfo.name
            fieldInfo.set_name(available_field_name)
            if not dt.create_field(fieldInfo):
                raise RuntimeError("Failed to create field " + str(fieldInfo))

        if "SmUserID" in names:
            indexOfUserID = names.index("SmUserID")
    else:
        indexOfUserID = -1
    dt.open()
    rd = dt.get_recordset(True)
    rd.batch_edit()
    for i in range(len(narray)):
        row = narray[i]
        if is_point:
            x = row[indexOfX]
            y = row[indexOfY]
            geoPoint = GeoPoint((x, y))
            rd.add(geoPoint)
        else:
            rd.add(None)
        for fieldIndex, valueIndex in indexes.items():
            value = row[valueIndex]
            array_field_name = name_pair[fieldInfos[fieldIndex].name]
            rd.set_value(fieldInfos[fieldIndex].name, _to_sm_value(value, narray.dtype[array_field_name].type))

        if indexOfUserID is not -1:
            rd.set_value("SmUserID", row[indexOfUserID])

    rd.batch_update()
    rd.close()
    return try_close_output_datasource(dt, ds)


def _pixel_to_numpy_dtype(pixel):
    _pixel_to_numpy = {(PixelFormat.UBIT1): "b", 
     (PixelFormat.UBIT4): "b", 
     (PixelFormat.UBIT8): "B", 
     (PixelFormat.UBIT16): "uint16", 
     (PixelFormat.UBIT32): "uint32", 
     (PixelFormat.BIT8): "b", 
     (PixelFormat.BIT16): "int16", 
     (PixelFormat.BIT32): "int32", 
     (PixelFormat.BIT64): "int64", 
     (PixelFormat.RGB): "int32", 
     (PixelFormat.RGBA): "int32", 
     (PixelFormat.DOUBLE): "float64", 
     (PixelFormat.SINGLE): "float32"}
    return _pixel_to_numpy[pixel]


def _read_floats_from_stream(bys):
    stream = io.BytesIO(bys)
    count = read_int(stream)
    for i in range(count):
        yield read_float(stream)


def _write_floats_to_stream(values, no_value):
    stream = io.BytesIO()
    write_int(len(values), stream)
    for value in values:
        if value is None or value is numpy.nan:
            write_float(no_value, stream)
        else:
            write_float(value, stream)

    return stream.getvalue()


class _ReadDataSingleThread(threading.Thread):

    def __init__(self, socket, out):
        threading.Thread.__init__(self)
        self.server_socket = socket
        self.values = out

    def run(self):
        self.server_socket.listen()
        import select
        try:
            try:
                while 1:
                    readable, _, _ = select.select([self.server_socket], [], [], 1)
                    if self.server_socket in readable:
                        conn = self.server_socket.accept()[0]
                        out_file = conn.makefile("wrb", 65536)
                        length = read_int(out_file)
                        while length > 0:
                            self.values.append(decode_tile(out_file.read(length)).values)
                            length = read_int(out_file)

                        write_int(-1, out_file)
                        conn.close()
                        break

            except:
                import traceback
                log_error(traceback.format_exc())

        finally:
            self.server_socket.close()


def _del_dir_tree(path):
    if os.path.isfile(path):
        try:
            os.remove(path)
        except:
            pass

    else:
        if os.path.isdir(path):
            for item in os.listdir(path):
                itempath = os.path.join(path, item)
                _del_dir_tree(itempath)

            try:
                os.rmdir(path)
            except:
                pass


def datasetraster_to_numpy_array(source, no_value=None, origin_is_left_up=True):
    """
    从栅格数据集 (DatasetGrid) 或影像数据集 (DatasetImage) 中读取数据到 numpy 数组中。数组的列的数目为数据集的宽度(width)，行的数目为数据集的高度(height)。
    如果是单波段数据集，且不是 RGB 和 RGBA 像素格式的数据集，返回一个二维数组，数组的第一维度为行，第二维度为列。如果是 RGB 和 RGBA 的单波段
    数据集，返回一个三维数组，数组的第一维度为波段，第一维度的大小为 3（RGB）或 4（RGBA），数组的第二维度为行，第三维度为列。
    如果是多波段数据集，返回一个三维数组，数组的第一维度为波段。第一维度的大小为波段的数目，数组的第二维度为行，第三维度为列。

    :param source: 需要读取数据的栅格数据集或影像数据集对象。如果输入为 str, 则可以使用数据源信息加数据集名称方式表示数据集，
                   例如，使用数据源别名'alias/imagedataset',也可以使用数据源的连接信息（udb文件路径， dcf文件路径，或者数据
                   源连接信息的xml字符串表示），例如使用udb文件，'/home/data/test.udb/imagedataset'。当使用数据源连接信息时，
                   如果工作空间中已经有相同的数据源信息的数据源存在，则会直接获取已存在的数据源对象，否则会打开一个新的数据源对象。
    :type source: DatasetGrid or DatasetImage or str
    :param float no_value: SuerpMap 的栅格数据集和影像数据集均有无值，用户可以设定一个新的无值来表示数据集的无值，如果 noValue
                           不为 None，在返回的 numpy 数组中会使用用户设定的 noValue 来替换无值的栅格或像素。默认为 None，即返回
                           的数组的无值不改变。
    :param bool origin_is_left_up: 在返回的 numpy 数组中，(0,0) 位置的值是数据集的左上角还是左下角，如果为 True，则表示数组的
                                  （0,0）的值为数据集的左上角的值， ndarray[i][j] 对应数据集中 第i行j列的数值，如果为 False，
                                  则数组的 (0,0) 的值为数据集的左下角的值，即 ndarray[i][j] 对应数据集中 第(height-i)行j列的
                                  数值。在 SuperMap 的栅格数据集或影像数据集中，数据集的 (0,0) 位置为左上角。默认为 True。
    :return: numpy 多维数组
    :rtype: numpy.ndarray
    """
    dt = get_input_dataset(source)
    if dt is None:
        raise ValueError("cannot get valid dataset object from source")
    if not isinstance(dt, (DatasetGrid, DatasetImage)):
        raise ValueError("source must be DatasetGrid, DatasetImage")
    else:
        height = dt.height
        width = dt.width
        is_use_rasterio = True
        try:
            import rasterio
        except ImportError as e:
            try:
                is_use_rasterio = False
            finally:
                e = None
                del e

        if height * width > 25000000 and is_use_rasterio:
            from .conversion import export_to_tif
            import os
            temp_dir = tempfile.mkdtemp()
            result_array = None
            try:
                try:
                    temp_name = os.path.join(temp_dir, "t.tif")
                    export_to_tif(dt, temp_name)
                    rs = rasterio.open(temp_name)
                    result_array = rs.read()
                    rs.close()
                except:
                    import traceback
                    log_error(traceback.format_exc())

            finally:
                _del_dir_tree(temp_dir)

            if result_array is None:
                return
            if not origin_is_left_up:
                rows = list(range(height))
                rows_r = rows.copy()
                rows_r.reverse()
                array_copy = result_array.copy()
                if result_array.ndim == 3:
                    for k in range(result_array.shape[0]):
                        result_array[k][(rows, None[:None])] = array_copy[k][(rows_r, None[:None])]

        else:
            result_array[(rows, None[:None])] = result_array.copy()[(rows_r, None[:None])]
    if no_value is not None:
        from ._utils import tuple_to_color
        no_value = tuple_to_color(no_value)
    if isinstance(dt, DatasetGrid):
        dt_no_value = dt.no_value
        if no_value is not None:
            if dt_no_value != no_value:
                result_array[result_array == dt_no_value] = no_value
        if result_array.ndim == 3:
            result_array = result_array[0]
        return result_array
    bands = dt.band_count
    dt_no_value = dt.get_no_value(0)
    pixel = dt.get_pixel_format(0)
    from ._utils import color_to_tuple
    if bands == 1:
        if pixel is PixelFormat.RGB:
            if no_value is not None:
                rgb = color_to_tuple(dt_no_value)
                _rgb = color_to_tuple(no_value)
                if rgb[0] != _rgb[0]:
                    result_array[result_array == rgb[0]] = _rgb[0]
                if rgb[1] != _rgb[1]:
                    result_array[result_array == rgb[1]] = _rgb[1]
                if rgb[2] != _rgb[2]:
                    result_array[result_array == rgb[2]] = _rgb[2]
            return result_array
    if bands == 1:
        if pixel is PixelFormat.RGBA:
            if no_value is not None:
                rgb = color_to_tuple(dt_no_value)
                _rgb = color_to_tuple(no_value)
                if rgb[0] != _rgb[0]:
                    result_array[result_array == rgb[0]] = _rgb[0]
                if rgb[1] != _rgb[1]:
                    result_array[result_array == rgb[1]] = _rgb[1]
                if rgb[2] != _rgb[2]:
                    result_array[result_array == rgb[2]] = _rgb[2]
                if rgb[3] != _rgb[3]:
                    result_array[result_array == rgb[3]] = _rgb[3]
            return result_array
    if no_value is not None:
        if dt_no_value != no_value:
            result_array[result_array == dt_no_value] = no_value
    if bands == 1:
        if result_array.ndim == 3:
            result_array = result_array[0]
        return result_array
    else:
        res = []
        if no_value is not None:
            from ._utils import tuple_to_color
            _null_value = float(tuple_to_color(no_value))
        else:
            _null_value = None
        import socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('127.0.0.1', 0))
        server_socket.listen(1)
        server_host, server_port = server_socket.getsockname()
        read_thread = _ReadDataSingleThread(server_socket, res)
        read_thread.start()
        get_jvm().com.supermap.jsuperpy.DatasetUtils.ReadDatasetToPb(oj(dt), origin_is_left_up, _null_value, server_host, server_port)
        if len(res) > 0:
            if len(res) == 1:
                result_array = res[0]
            else:
                if res[0].ndim == 2:
                    result_array = numpy.concatenate((tuple(res)), axis=0)
                else:
                    result_array = numpy.concatenate((tuple(res)), axis=1)
        else:
            result_array = None
        return result_array


def numpy_array_to_datasetraster(narray, x_resolution, y_resolution, output, x_start=0, y_start=0, out_dataset_name=None, no_value=None, origin_is_left_up=True, as_grid=False):
    """
    将 numpy 的数组写入到 SuperMap 的栅格或影像数据集中。

    :param numpy.ndarray narray: 被写入的 numpy 数组，支持二维数值型数组或 三维数值型数组。对于三维数组，只能写入为影像数据集。
    :param float x_resolution: 结果数据集的 x 方向的分辨率
    :param float y_resolution: 结果数据集的 y 方向的分辨率
    :param output: 结果数据源对象
    :type output: Datasource or DatasourceConnectionInfo or str
    :param float x_start: 右下角 x 的坐标值
    :param float y_start: 右下角 y 的坐标值
    :param str out_dataset_name: 结果数据集名称
    :param float no_value: 指定的无值。默认情形下，栅格数据集的无值为 -9999.
    :param bool origin_is_left_up: 指定 numpy 数组的第0行第0列为栅格数据集或影像数据集的左上角还是左下角。
    :param bool as_grid: 是否写入为 :py:class:`DatasetGrid` 数据集
    :return: 结果数据集对象或数据集名称。
    :rtype: DatasetGrid or DatasetImage or str
    """
    _numpy_to_pixel = {(numpy.bool_): (PixelFormat.UBIT1), 
     (numpy.byte): (PixelFormat.BIT8), 
     (numpy.int8): (PixelFormat.BIT8), 
     (numpy.short): (PixelFormat.BIT16), 
     (numpy.int32): (PixelFormat.BIT32), 
     (numpy.int64): (PixelFormat.BIT64), 
     (numpy.longlong): (PixelFormat.BIT64), 
     (numpy.ubyte): (PixelFormat.UBIT8), 
     (numpy.uint8): (PixelFormat.UBIT8), 
     (numpy.ushort): (PixelFormat.UBIT16), 
     (numpy.uint32): (PixelFormat.UBIT32), 
     (numpy.single): (PixelFormat.SINGLE), 
     (numpy.double): (PixelFormat.DOUBLE), 
     (numpy.float16): (PixelFormat.SINGLE), 
     (numpy.float32): (PixelFormat.DOUBLE)}
    pixel = _numpy_to_pixel[narray.dtype.type]
    if narray.ndim == 3:
        bands = narray.shape[0]
        rows = narray.shape[1]
        cols = narray.shape[2]
    else:
        if narray.ndim == 2:
            bands = 1
            rows = narray.shape[0]
            cols = narray.shape[1]
        else:
            raise ValueError("Unsupport array, only support 2 or 3 dim array")
    if as_grid:
        if bands > 1:
            log_warning("The NumPy array cannot be written to the grid dataset because the grid dataset does not support Multi-Band.Instead of writing to the image dataset")
            as_grid = False
        else:
            ds = get_output_datasource(output)
            check_output_datasource(ds)
            if out_dataset_name is None:
                out_dataset_name = "NewDataset"
            else:
                bounds = Rectangle(left=x_start, top=(y_start + rows * y_resolution), right=(x_start + cols * x_resolution), bottom=y_start)
                if no_value is None:
                    no_value = -9999
                if as_grid:
                    dtInfo = DatasetGridInfo(out_dataset_name, cols, rows, pixel).set_no_value(no_value).set_bounds(bounds)
                    dt = ds.create_dataset(dtInfo, True)
                    if dt is None:
                        raise RuntimeError("Failed to create result dataset : " + out_dataset_name)
                else:
                    dtInfo = DatasetImageInfo(out_dataset_name, cols, rows, pixel, band_count=bands).set_bounds(bounds)
                    dt = ds.create_dataset(dtInfo, True)
                    if dt is None:
                        raise RuntimeError("Failed to create result dataset : " + out_dataset_name)
                    for band in range(bands):
                        dt.set_no_value(no_value, band)

        dt.open()
        SetRows = get_jvm().com.supermap.jsuperpy.DatasetUtils.SetRows
        if narray.ndim == 2:
            for row in range(rows):
                row_data = _write_floats_to_stream(narray[row][0[:None]], no_value)
                if origin_is_left_up:
                    row_index = row
                else:
                    row_index = rows - row - 1
                if as_grid:
                    SetRows(dt._jobject, row_index, row_data)
                else:
                    SetRows(dt._jobject, row_index, row_data, 0)

    else:
        for band in range(bands):
            for row in range(rows):
                if origin_is_left_up:
                    row_index = row
                else:
                    row_index = rows - row - 1
                row_data = _write_floats_to_stream(narray[band][row][0[:None]], no_value)
                SetRows(dt._jobject, row_index, row_data, band)

    return try_close_output_datasource(dt, ds)

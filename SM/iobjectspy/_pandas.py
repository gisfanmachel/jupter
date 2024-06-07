# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/_pandas.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 11494 bytes
"""
_pandas 模块用于 SuperMap 与 `pandas`_ 的数据交互。因为 `pandas`_ 与 `numpy`_ 之间可以快速的进行数据结构的转换，所以，其实通过
:py:mod:`_numpy` 就可以很方便将数据读出 numpy 的多维数组，然后转换为 pandas 的 DataFrame 对象。_pandas 模块基于 :py:mod:`_numpy` 模块
进行了轻量的封装，以方便用户更加直接的将读取数据和写出数据。

在使用 _pandas 模块之前，请先安装 pandas 包。如果需要读取多波段影像数据集( :py:class:`.DatasetImage` )，包括 RGB 或 RGBA 像素
格式的单波段影像数据集，需要用到 `xarray`_ 包，_pandas 会将多波段影像数据集读出为 xarray 的 DataArray 对象，具体可以参考
:py:func:`datasetraster_to_df_or_xarray`

.. _numpy: http://www.numpy.org/

.. _pandas: http://pandas.pydata.org

.. _xarray: http://xarray.pydata.org

"""
__all__ = [
 'recordset_to_df', 'datasetvector_to_df', 'df_to_datasetvector', 
 'datasetraster_to_df_or_xarray', 
 'df_or_xarray_to_datasetraster']
import numpy, pandas
from ._numpy import *

def _df_to_sarray(df):
    return numpy.array(df.to_records(False))


def recordset_to_df(recordset, fields=None, export_spatial=False, skip_null_value=True, null_values=None):
    """
    将一个记录集写出到 pandas.DataFrame 中，支持将点数据集、线数据集、面数据集和属性表数据集的记录集写出。

    :param Recordset recordset: 被写出数据集的记录集
    :param fields: 需要写出的字段名称，如果为 None，则将全部非系统字段都写出
    :type fields: list[str]
    :param bool export_spatial: 是否写出空间几何信息，对点对象，将直接写出点的 X 和 Y 值到 ‘SmX’ 和 ‘SmY’ 列中。对于线面对象，将写出线和面对象的内点，并输出到 ‘SmX’ 和 ‘SmY’ 列中，同时，线将写出 ‘SmLength’字段，面将写出 ‘SmPerimeter’ 和 ‘SmArea 字段。
    :param is skip_null_value: 是否跳过含有空值的记录。由于 DataFrame 中，不支持整型类型的值为空值，如果列的类型为整型类型但又是空值，会将整型值转为浮点型存储。所以，如果数据集中字段含有空值，需要填入一个空值。对于浮点型的字段，空值为 numpy.nan，对于文本型（TEXT，WTEXT，CHAR，JSONB）为空字符串，布尔类型、二进制类型和时间类型字段的空值为 None。
    :param null_values: 指定的字段对应的空值，key 值为字段名称或字段序号，value 为指定的空值，value 的值的类型需要与字段的类型匹配。例如，需要指定字段整型字段 ID 的空值为 -9999，则 null_values = {'ID': -9999}
    :type null_values: dict
    :return: 返回一个 DataFrame 对象。
    :rtype: pandas.DataFrame
    """
    nr = recordset_to_numpy_array(recordset, fields, export_spatial, skip_null_value, null_values)
    if nr is not None:
        return pandas.DataFrame(nr)
    return


def datasetvector_to_df(source, attr_filter=None, fields=None, export_spatial=False, skip_null_value=True, null_values=None):
    """
    将矢量数据集写出到 pandas.DataFrame 中

    :param source: 被写出的矢量数据集，支持点、线、面和属性表数据集。支持输入数据集对象以及数据源信息和数据集名称的组合形式，例如 ’alias|point'
    :type source: DatasetVector or str
    :param str attr_filter: 属性过滤条件
    :param fields: 需要写出的字段，如果为None，将写出所有的非系统字段
    :type fields: list[str]
    :param is skip_null_value: 是否跳过含有空值的记录。numpy数组中，不支持整型类型的值为空值，如果列的类型为整型类型但又是空值，会将整型值转为浮点型存储。所以，如果数据集中字段含有空值，需要填入一个空值。对于浮点型的字段，空值为 numpy.nan，对于文本型（TEXT，WTEXT，CHAR，JSONB）为空字符串，布尔类型、二进制类型和时间类型字段的空值为 None。
    :param null_values: 指定的字段对应的空值，key 值为字段名称或字段序号，value 为指定的空值，value 的值的类型需要与字段的类型匹配。例如，需要指定字段整型字段 ID 的空值为 -9999，则 null_values = {'ID': -9999}
    :type null_values: dict
    :return: 返回一个 DataFrame 对象。
    :rtype: pandas.DataFrame
    """
    nr = datasetvector_to_numpy_array(source, attr_filter, fields, export_spatial, skip_null_value, null_values)
    if nr is not None:
        return pandas.DataFrame(nr)
    return


def df_to_datasetvector(df, output, out_dataset_name=None, x_col=None, y_col=None):
    """
    将 pandas  DataFrame 对象写入为矢量数据集

    :param df: 待写入的数据集 pandas DataFrame 对象
    :type df: pandas.DataFrame
    :param output: 结果数据源对象
    :type output: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param str x_col: 写入为点数据集时，点对象 X 值所在的列。如果为空，则写入为属性表数据集。
    :param str y_col: 写入为点数据集时，点对象 Y 值所在的列。如果为空，则写入为属性表数据集。
    :return: 结果数据集对象或数据集名称。
    :rtype: DatasetVector or str
    """
    return numpy_array_to_datasetvector(_df_to_sarray(df), output, out_dataset_name, x_col, y_col)


def datasetraster_to_df_or_xarray(source, no_value=None, origin_is_left_up=True):
    """
    从栅格数据集 (DatasetGrid) 或影像数据集 (DatasetImage) 中读取数据到 pandas.DataFrame 或  xarray.DataArray。数组的列的数
    目为数据集的宽度(width)，行的数目为数据集的高度(height)。

     * 如果是单波段数据集，且不是 RGB 和 RGBA 像素格式的数据集，返回一个二维数组，数组的第一维度为行，第二维度为列，即返回一个 DataFrame
     * 如果是 RGB 和 RGBA 的单波段数据集，返回一个三维数组，数组的第一维度为波段，第一维度的大小为 3（RGB）或 4（RGBA），数组的第二维度为行，第三维度为列，即返回 DataArray
     * 如果是多波段数据集，返回一个三维数组，数组的第一维度为波段。第一维度的大小为波段的数目，数组的第二维度为行，第三维度为列。即返回 DataArray

    :param source: 需要读取数据的栅格数据集或影像数据集对象。如果输入为 str, 则可以使用数据源信息加数据集名称方式表示数据集，
                   例如，使用数据源别名'alias/imagedataset',也可以使用数据源的连接信息（udb文件路径， dcf文件路径，或者数据
                   源连接信息的xml字符串表示），例如使用udb文件，'/home/data/test.udb/imagedataset'。当使用数据源连接信息时，
                   如果工作空间中已经有相同的数据源信息的数据源存在，则会直接获取已存在的数据源对象，否则会打开一个新的数据源对象。

    :type source: DatasetGrid or DatasetImage or str
    :param float no_value: SuerpMap 的栅格数据集和影像数据集均有无值，用户可以设定一个新的无值来表示数据集的无值，如果 noValue
                           不为 None，在返回的 DataFrame 中会使用用户设定的 noValue 来替换无值的栅格或像素。默认为 None，即返回
                           的数组的无值不改变。

    :param bool origin_is_left_up: 在返回的 DataFrame 或 DataArray 中，(0,0) 位置的值是数据集的左上角还是左下角，如果为 True，
                                   则表示数组的（0,0）的值为数据集的左上角的值， DataFrame[i][j] 对应数据集中 第i行j列的数值，
                                   如果为 False，则数组的 (0,0) 的值为数据集的左下角的值，即 DataFrame[i][j] 对应数据集中 第(height-i)行j列的
                                   数值。在 SuperMap 的栅格数据集或影像数据集中，数据集的 (0,0) 位置为左上角。默认为 True。

    :return: 但读取数据集为一个二维数组时返回一个 DataFrame，如果读取的数据集是一个三维数组，则返回一个 xarray.DataArray
    :rtype: pandas.DataFrame or xarray.DataArray
    """
    nr = datasetraster_to_numpy_array(source, no_value, origin_is_left_up)
    if nr is not None:
        if nr.ndim == 2:
            return pandas.DataFrame(nr)
            if nr.ndim == 3:
                try:
                    import xarray
                    return xarray.DataArray(nr)
                except ImportError as e:
                    try:
                        print("The source dataset has multiple bands and needs to be output as xarray.DataArray, please install xarray before read data")
                        raise e
                    finally:
                        e = None
                        del e

        else:
            return
    else:
        return


def df_or_xarray_to_datasetraster(data, x_resolution, y_resolution, output, x_start=0, y_start=0, out_dataset_name=None, no_value=None, origin_is_left_up=True, as_grid=False):
    """
    将 pandas.DataFrame， xarray.DataArray 或 xarray.Dataset  写入到 SuperMap 的栅格或影像数据集中。如果是  xarray.DataArray
    或 xarray.Dataset 请先安装 xarray。

    :param DataFrame data: 被写入的 或 xarray.DataArray 或 xarray.Dataset, 支持二维数值型数组或 三维数值型数组。对于三维数组，只能写入为影像数据集。
    :param float x_resolution: 结果数据集的 x 方向的分辨率
    :param float y_resolution: 结果数据集的 y 方向的分辨率
    :param output: 结果数据源对象
    :type output: Datasource or DatasourceConnectionInfo or str
    :param float x_start: 右下角 x 的坐标值
    :param float y_start: 右下角 y 的坐标值
    :param str out_dataset_name: 结果数据集名称
    :param float no_value: 指定的无值。默认情形下，栅格数据集的无值为 -9999.
    :param bool origin_is_left_up: 指定 DataFrame 第0行第0列为栅格数据集或影像数据集的左上角还是左下脚。
    :param bool as_grid: 是否写入为 :py:class:`DatasetGrid` 数据集
    :return: 结果数据集对象或数据集名称。
    :rtype: DatasetGrid or DatasetImage or str

    """
    if isinstance(data, pandas.DataFrame):
        return numpy_array_to_datasetraster(data.values, x_resolution, y_resolution, output, x_start, y_start, out_dataset_name, no_value, origin_is_left_up, as_grid)
    try:
        import xarray
        if isinstance(data, xarray.DataArray):
            values = data.values
        else:
            if isinstance(data, xarray.Dataset):
                values = data.to_array().values
            else:
                raise ValueError("required xarray.DataArray or xarray.Dataset, but is " + str(type(data)))
        return numpy_array_to_datasetraster(values, x_resolution, y_resolution, output, x_start, y_start, out_dataset_name, no_value, origin_is_left_up, as_grid)
    except ImportError as e:
        try:
            print("please install xarray before writing data")
            raise e
        finally:
            e = None
            del e

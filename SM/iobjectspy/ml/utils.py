# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\utils.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 27957 bytes
"""
utils模块负责数据处理中的一些常用小功能
"""
import numpy as np

def recordset_to_numpy_array(recordset, fields=None, export_spatial=False, skip_null_value=True, null_values=None):
    """
    将一个记录集写出到 numpy.ndarray 中，支持将点数据集、线数据集、面数据集和属性表数据集的记录集写出。

    :py:meth:`recordset_to_numpy_array` 和 :py:meth:`datasetvector_to_numpy_array` 用于将矢量数据写出为 ndarray。写出的
    ndarray 为一维数组，数组的每项元素均含有多个子元素，可以直接使用列名称获取子项所在的列，例如，通过下面的代码可以直接读取矢量数据：

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
    from .._numpy import recordset_to_numpy_array
    return recordset_to_numpy_array(recordset, fields, export_spatial, skip_null_value, null_values)


def datasetvector_to_numpy_array(source, attr_filter=None, fields=None, export_spatial=False, skip_null_value=True, null_values=None):
    """
    将矢量数据集写出到 numpy 的数组中

    :param source: 被写出的矢量数据集，支持点、线、面和属性表数据集。支持输入数据集对象以及数据源信息和数据集名称的组合形式，例如 ’alias|point'
    :type source: DatasetVector or str
    :param str attr_filter: 属性过滤条件
    :param fields: 需要写出的字段，如果为None，将写出所有的非系统字段
    :type fields: list[str]
    :param bool export_spatial: 是否导出空间几何对象。对点对象，将直接写出点的 X 和 Y 值到 ‘SmX’ 和 ‘SmY’ 列中。对于线面对象，将写出线和面对象的内点，并输出到 ‘SmX’ 和 ‘SmY’ 列中，同时，线将写出 ‘SmLength’字段，面将写出 ‘SmPerimeter’ 和 ‘SmArea 字段。
    :param is skip_null_value: 是否跳过含有空值的记录。numpy数组中，不支持整型类型的值为空值，如果列的类型为整型类型但又是空值，可能会写出失败。所以，如果数据集中字段含有空值，需要填入一个空值。对于浮点型的字段，空值为 numpy.nan，对于文本型（TEXT，WTEXT，CHAR，JSONB）为空字符串，布尔类型、二进制类型和时间类型字段的空值为 None。
    :param null_values: 指定的字段对应的空值，key 值为字段名称或字段序号，value 为指定的空值，value 的值的类型需要与字段的类型匹配。例如，需要指定字段整型字段 ID 的空值为 -9999，则 null_values = {'ID': -9999}
    :type null_values: dict
    :return: numpy 数组，将返回一个维度为1的数组。
    :rtype: numpy.ndarray
    """
    from .._numpy import datasetvector_to_numpy_array
    return datasetvector_to_numpy_array(source, attr_filter, fields, export_spatial, skip_null_value, null_values)


def numpy_array_to_datasetvector(narray, output, out_dataset_name=None, x_col=None, y_col=None):
    """
    将 numpy 的数组写入到 SuperMap 的矢量数据集中

    支持将一个含有 dtype 信息和列名称的 ndarray 数组写入到 SuperMap 的矢量数据集中，如果指定了 X 和 Y 字段值的列名称，将会写
    入为点数据集，否则，将写入为属性表数据集。注意的是，ndarray 必须含有列名称才可能写入::

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

    :param numpy.ndarray narray: 被写入的 numpy 数组
    :param output: 结果数据源对象
    :type output: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param str x_col: 写入为点数据集时，点对象 X 值所在的列。如果为空，则写入为属性表数据集。
    :param str y_col: 写入为点数据集时，点对象 Y 值所在的列。如果为空，则写入为属性表数据集。
    :return: 结果数据集对象或数据集名称。
    :rtype: DatasetVector or str
    """
    from .._numpy import numpy_array_to_datasetvector
    return numpy_array_to_datasetvector(narray, output, out_dataset_name, x_col, y_col)


def datasetraster_to_numpy_array(source, no_value=None, origin_is_left_up=True):
    """
    从栅格数据集 (DatasetGrid) 或影像数据集 (DatasetImage) 中读取数据到 numpy 数组中。数组的列的数目为数据集的宽度(width)，行的数目为数据集的高度(height)。
    如果是单波段数据集，且不是 RGB 和 RGBA 像素格式的数据集，返回一个二维数组，数组的第一维度为行，第二维度为列。如果是 RGB 和 RGBA 的单波段
    数据集，返回一个三维数组，数组的第一维度为波段，第一维度的大小为 3（RGB）或 4（RGBA），数组的第二维度为行，第三维度为列。
    如果是多波段数据集，返回一个三维数组，数组的第一维度为波段。第一维度的大小为波段的数目，数组的第二维度为行，第三维度为列。

    :py:meth:`datasetraster_to_numpy_array` 支持将影像数据集和栅格数据集写出到 numpy 的 ndarray，影像数据集支持多波段影像。在写出影像数据集时:

     - 如果是 RGB 或 RGBA 像素格式的影像数据集，将会写出为为维度为3的数组，地中第一个维度的大小为3（RGB）或4（RGBA），第二维度为为行，第三维度为列；
     - 如果是单波段数据集，将会写出为一个维度为2的数组第一维度为行，第二维度为列；
     - 如果波段数目大于1，将会写出一个维度为3的数组，其中第一维度为波段，第二维度为为行，第三维度为列；

    如果写出为栅格数据集，因为栅格数据集不支持多波段，所以将会写出为一个维度为2的数组。

     - 写出一个 RGB 影像数据集::

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

     - 写出一个像素格式为 BIT16 的栅格数据集::

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

    - 另外，需要注意的是 origin_is_left 可以指定生成的数组原点（第0行第0列）对应在 SuperMap 栅格数据集或影像数据集中的左上角还是左下角。在SuperMap的栅格数据集和影像数据集中
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
    from .._numpy import datasetraster_to_numpy_array
    return datasetraster_to_numpy_array(source, no_value, origin_is_left_up)


def numpy_array_to_datasetraster(narray, x_resolution, y_resolution, output, x_start=0, y_start=0, out_dataset_name=None, no_value=None, origin_is_left_up=True, as_grid=False):
    """
    将 numpy 的数组写入到 SuperMap 的栅格或影像数据集中。

    支持将一个二维数组或三维数组写入到影像数据集或栅格数据集中，如果选择写入到栅格数据集，则只能是二维数组，如果写入到影像数据
    集，数组为三维数组时，第一个维度必须为波段信息，同时第二维度和第三维度必须为行和列::

        >>> d = numpy.empty((100, 100), dtype='float32')
        >>> for i in range(100):
        ...     for j in range(100):
        ...     d[i][j] = i * j + i
        >>> iobjects.numpy_array_to_datasetraster(d, 0.1, 0.1, out_dir + 'narray_out.udb', as_grid=True)

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
    from .._numpy import numpy_array_to_datasetraster
    return numpy_array_to_datasetraster(narray, x_resolution, y_resolution, output, x_start, y_start, out_dataset_name, no_value, origin_is_left_up, as_grid)


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
    from .._pandas import recordset_to_df
    return recordset_to_df(recordset, fields, export_spatial, skip_null_value, null_values)


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
    from .._pandas import datasetvector_to_df
    return datasetvector_to_df(source, attr_filter, fields, export_spatial, skip_null_value, null_values)


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
    from .._pandas import df_to_datasetvector
    return df_to_datasetvector(df, output, out_dataset_name, x_col, y_col)


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
    from .._pandas import datasetraster_to_df_or_xarray
    return datasetraster_to_df_or_xarray(source, no_value, origin_is_left_up)


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
    :param bool origin_is_left_up: 指定 DataFrame 第0行第0列为栅格数据集或影像数据集的左上角还是左下角。
    :param bool as_grid: 是否写入为 :py:class:`DatasetGrid` 数据集
    :return: 结果数据集对象或数据集名称。
    :rtype: DatasetGrid or DatasetImage or str

    """
    from .._pandas import df_or_xarray_to_datasetraster
    return df_or_xarray_to_datasetraster(data, x_resolution, y_resolution, output, x_start, y_start, out_dataset_name, no_value, origin_is_left_up, as_grid)

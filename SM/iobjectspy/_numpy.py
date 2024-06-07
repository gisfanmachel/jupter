# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/_numpy.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 12216 bytes
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
_s_np = None
try:
    from . import _jsuperpy
    try:
        from ._jsuperpy import _numpy
        _s_np = _numpy
    except ImportError as e:
        try:
            pass
        finally:
            e = None
            del e

except ImportError as e:
    try:
        from . import _csuperpy
        try:
            from ._csuperpy import _numpy
            _s_np = _numpy
        except ImportError as e:
            try:
                pass
            finally:
                e = None
                del e

    finally:
        e = None
        del e

if _s_np is not None:
    recordset_to_numpy_array = _s_np.recordset_to_numpy_array
    datasetvector_to_numpy_array = _s_np.datasetvector_to_numpy_array
    numpy_array_to_datasetvector = _s_np.numpy_array_to_datasetvector
    datasetraster_to_numpy_array = _s_np.datasetraster_to_numpy_array
    numpy_array_to_datasetraster = _s_np.numpy_array_to_datasetraster
    __all__ = [
     'recordset_to_numpy_array', 'datasetvector_to_numpy_array', 'numpy_array_to_datasetvector', 
     'datasetraster_to_numpy_array', 
     'numpy_array_to_datasetraster']
else:
    __all__ = []
del _s_np

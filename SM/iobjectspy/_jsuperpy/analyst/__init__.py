# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/_jsuperpy\analyst\__init__.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 3803 bytes
r"""
ananlyst 模块提供了常用的空间数据处理和分析的功能，用户使用analyst 模块可以进行缓冲区分析( :py:meth:`create_buffer` )、叠加分析( :py:meth:`overlay` )、
创建泰森多边形( :py:meth:`create_thiessen_polygons` )、拓扑构面( :py:meth:`topology_build_regions` )、密度聚类( :py:meth:`kernel_density` )、
插值分析( :py:meth:`interpolate` )，栅格代数运算( :py:meth:`expression_math_analyst` )等功能。

在 analyst 模块的所有接口中，对输入数据参数要求为数据集（ :py:class:`.Dataset` , :py:class:`.DatasetVector` , :py:class:`.DatasetImage` , :py:class:`.DatasetGrid` ）的参数，
都接受直接输入一个数据集对象（Dataset）或数据源别名与数据集名称的组合（例如，'alias/dataset_name', 'alias\\\dataset_name'),也支持数据源连接信息与数据集名称的组合（例如，'E:/data.udb/dataset_name')。

    - 支持设置数据集

        >>> ds = Datasource.open('E:/data.udb')
        >>> create_buffer(ds['point'], 10, 10, unit='Meter', out_data='E:/buffer_out.udb')

    - 支持设置数据集别名和数据集名称组合

        >>> create_buffer(ds.alias + '/point' + , 10, 10, unit='Meter', out_data='E:/buffer_out.udb')
        >>> create_buffer(ds.alias + '\\point', 10, 10, unit='Meter', out_data='E:/buffer_out.udb')
        >>> create_buffer(ds.alias + '|point', 10, 10, unit='Meter', out_data='E:/buffer_out.udb')

    - 支持设置 udb 文件路径和数据集名称组合

        >>> create_buffer('E:/data.udb/point', 10, 10, unit='Meter', out_data='E:/buffer_out.udb')

    - 支持设置数据源连接信息和数据集名称组合，数据源连接信息包括 dcf 文件、xml 字符串等，具体参考 :py:meth:`.DatasourceConnectionInfo.make`

        >>> create_buffer('E:/data_ds.dcf/point', 10, 10, unit='Meter', out_data='E:/buffer_out.udb')

.. Note:: 当输入的是数据源信息时，程序会自动打开数据源，但是接口运行结束时不会自动关闭数据源，也就是打开后的数据源会存在当前工作空间中

在 analyst 模块中所有接口中，对输出数据参数要求为数据源（ :py:class:`.Datasource` ）的，均接受 Datasource 对象，也可以为 :py:class:`.DatasourceConnectionInfo` 对象，
同时，也支持当前工作空间下数据源的别名，也支持 UDB 文件路径，DCF 文件路径等。

    - 支持设置 udb 文件路径

        >>> create_buffer('E:/data.udb/point', 10, 10, unit='Meter', out_data='E:/buffer_out.udb')

    - 支持设置数据源对象

        >>> ds = Datasource.open('E:/buffer_out.udb')
        >>> create_buffer('E:/data.udb/point', 10, 10, unit='Meter', out_data=ds)
        >>> ds.close()

    - 支持设置数据源别名

        >>> ds_conn = DatasourceConnectionInfo('E:/buffer_out.udb', alias='my_datasource')
        >>> create_buffer('E:/data.udb/point', 10, 10, unit='Meter', out_data='my_datasource')

.. Note:: 如果输出数据的参数输入的是数据源连接信息或 UDB 文件路径等，程序会自动打开数据源，如果是 UDB 数据源而本地不存在，还会自动新建一个UDB数据源，但需要确保UDB数据源所在的文件目录存在而且可写。
          在功能完成后，如果数据源是由程序自动打开或创建的，会被自动关闭掉（这里与输入数据为 Dataset 不同，输入数据中被自动打开的数据源不会自动关闭）。所以，对于有些接口
          输出结果为数据集的，就会返回结果数据集的名称，如果传入的是数据源对象，返回的便是结果数据集。

"""
from .na import *
from .sa import *
from .ss import *
from .terrain import *
from .topo import *
from .na3d import *
from .am import *

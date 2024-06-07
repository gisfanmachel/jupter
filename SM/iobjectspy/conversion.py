# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/conversion.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 5462 bytes
r"""
conversion 模块提供基本的数据导入和导出功能，通过使用 conversion 模块可以快速的将第三方的文件导入到 SuperMap 的数据源中，也可以将 SuperMap
数据源 中的数据导出为 第三方文件。

在 conversion 模块中，所有导入数据的接口中，output 参数输入结果数据集的数据源信息，可以为 Datasource 对象，也可以为 DatasourceConnectionInfo 对象，
同时，也支持当前工作空间下数据源的别名，也支持 UDB 文件路径，DCF 文件路径等。

>>> ds = Datasource.create(':memory:')
>>> alias = ds.alias
>>> shape_file = 'E:/Point.shp'
>>> result1 = import_shape(shape_file, ds)
>>> result2 = import_shape(shape_file, alias)
>>> result3 = import_shape(shape_file, 'E:/Point_Out.udb')
>>> result4 = import_shape(shape_file, 'E:/Point_Out_conn.dcf')

而导入数据的结果返回一个 Dataset 或 str 的列表对象。当导入数据只生成一个数据集时，列表的个数为1，当导入数据生成多个数据集时，列表的个数可能大于1。
列表中返回 Dataset 还是 str 是由输入的 output 参数决定的，当输入的 output 参数可以直接在当前工作空间中获取到数据源对象时，将会返回 Dataset 的列表，
如果输入的 output 参数无法直接在当前工作空间中获取到数据源对象时，程序将自动尝试打开数据源或新建数据源（只支持新建 UDB 数据源），此时，返回的结果将是
结果数据集的数据集名称，而完成数据导入后，结果数据源也会被关闭。所以如果用户需要继续基于导入后的结果数据集进行操作，则需要根据结果数据集名称和数据源信息再次开发数据源以获取数据集。

所有导出数据集的接口，data 参数是被导出的数据集信息，data 参数接受输入一个数据集对象（Dataset）或数据源别名与数据集名称的组合（例如，'alias/dataset_name', 'alias\\\dataset_name'),
，也支持数据源连接信息与数据集名称的组合（例如， 'E:/data.udb/dataset_name')，值得注意的是，当输入的是数据源信息时，程序会自动打开数据源，但是不会自动关闭数据源，也就是打开后的数据源
会存在当前工作空间中

>>> export_to_shape('E:/data.udb/Point', 'E:/Point.shp', is_over_write=True)
>>> ds = Datasource.open('E:/data.udb')
>>> export_to_shape(ds['Point'], 'E:/Point.shp', is_over_write=True)
>>> export_to_shape(ds.alias + '|Point', 'E:/Point.shp', is_over_write=True)
>>> ds.close()

"""
try:
    from . import _jsuperpy as supermap
except ImportError as e:
    try:
        from . import _csuperpy as supermap
    finally:
        e = None
        del e

import_shape = supermap.import_shape
import_dbf = supermap.import_dbf
import_csv = supermap.import_csv
import_mapgis = supermap.import_mapgis
import_aibingrid = supermap.import_aibingrid
import_bmp = supermap.import_bmp
import_dgn = supermap.import_dgn
import_dwg = supermap.import_dwg
import_dxf = supermap.import_dxf
import_e00 = supermap.import_e00
import_ecw = supermap.import_ecw
import_geojson = supermap.import_geojson
import_gif = supermap.import_gif
import_grd = supermap.import_grd
import_img = supermap.import_img
import_jp2 = supermap.import_jp2
import_jpg = supermap.import_jpg
import_kml = supermap.import_kml
import_kmz = supermap.import_kmz
import_mif = supermap.import_mif
import_mrsid = supermap.import_mrsid
import_osm = supermap.import_osm
import_png = supermap.import_png
import_simplejson = supermap.import_simplejson
import_sit = supermap.import_sit
import_tab = supermap.import_tab
import_tif = supermap.import_tif
import_usgsdem = supermap.import_usgsdem
import_vct = supermap.import_vct
export_to_bmp = supermap.export_to_bmp
export_to_gif = supermap.export_to_gif
export_to_grd = supermap.export_to_grd
export_to_img = supermap.export_to_img
export_to_jpg = supermap.export_to_jpg
export_to_png = supermap.export_to_png
export_to_sit = supermap.export_to_sit
export_to_tif = supermap.export_to_tif
export_to_csv = supermap.export_to_csv
export_to_dbf = supermap.export_to_dbf
export_to_dwg = supermap.export_to_dwg
export_to_dxf = supermap.export_to_dxf
export_to_e00 = supermap.export_to_e00
export_to_kml = supermap.export_to_kml
export_to_kmz = supermap.export_to_kmz
export_to_geojson = supermap.export_to_geojson
export_to_mif = supermap.export_to_mif
export_to_shape = supermap.export_to_shape
export_to_simplejson = supermap.export_to_simplejson
export_to_tab = supermap.export_to_tab
export_to_vct = supermap.export_to_vct
__all__ = [
 'import_shape', 'import_dbf', 'import_csv', 'import_mapgis', 'import_aibingrid', 
 'import_bmp', 
 'import_dgn', 'import_dwg', 'import_dxf', 'import_e00', 
 'import_ecw', 
 'import_geojson', 'import_gif', 'import_grd', 'import_img', 
 'import_jp2', 
 'import_jpg', 'import_kml', 'import_kmz', 'import_mif', 
 'import_mrsid', 'import_osm', 'import_png', 
 'import_simplejson', 'import_sit', 
 'import_tab', 'import_tif', 'import_usgsdem', 'import_vct', 
 'export_to_bmp', 
 'export_to_gif', 'export_to_grd', 'export_to_img', 'export_to_jpg', 
 'export_to_png', 
 'export_to_sit', 'export_to_tif', 'export_to_csv', 'export_to_dbf', 
 'export_to_dwg', 
 'export_to_dxf', 
 'export_to_e00', 'export_to_kml', 'export_to_kmz', 'export_to_geojson', 
 'export_to_mif', 
 'export_to_shape', 'export_to_simplejson', 'export_to_tab', 
 'export_to_vct']

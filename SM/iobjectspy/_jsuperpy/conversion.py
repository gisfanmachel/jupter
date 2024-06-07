# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/_jsuperpy\conversion.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 104994 bytes
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
from ._gateway import get_jvm, get_gateway, safe_start_callback_server, close_callback_server
from .enums import ImportMode, Charset, IgnoreMode, MultiBandImportMode, _FileType as FileType, CADVersion, VCTVersion
from data._listener import PythonListenerBase
from data._util import get_input_dataset, get_output_datasource, check_output_datasource, try_close_output_datasource
from data.step import StepEvent
from .data import Dataset
from ._utils import *
from ._logger import *
import os
__all__ = [
 'import_shape', 'import_dbf', 'import_csv', 'import_mapgis', 'import_aibingrid', 
 'import_bmp', 
 'import_dgn', 'import_dwg', 'import_dxf', 'import_e00', 
 'import_ecw', 'import_geojson', 
 'import_gif', 'import_grd', 'import_img', 
 'import_jp2', 'import_jpg', 'import_kml', 
 'import_kmz', 'import_mif', 
 'import_mrsid', 'import_osm', 'import_png', 'import_simplejson', 'import_sit', 
 'import_tab', 
 'import_tif', 'import_usgsdem', 'import_vct', 'export_to_bmp', 'export_to_gif', 
 'export_to_grd', 
 'export_to_img', 'export_to_jpg', 'export_to_png', 'export_to_sit', 'export_to_tif', 
 'export_to_csv', 
 'export_to_dbf', 'export_to_dwg', 'export_to_dxf', 'export_to_e00', 'export_to_kml', 
 'export_to_kmz', 
 'export_to_geojson', 'export_to_mif', 'export_to_shape', 'export_to_simplejson', 
 'export_to_tab', 
 'export_to_vct']

def _check_file_exist(source_file):
    if not os.path.exists(source_file):
        raise FileExistsError(source_file)


def _get_file_name(source_file):
    return os.path.basename(source_file).split(".")[0]


def _to_java_object_array(values):
    if values is None:
        return
    elif isinstance(values, Dataset):
        java_array = get_gateway().new_array(get_jvm().java.lang.Object, 1)
        java_array[0] = oj(values)
    else:
        if isinstance(values, (list, tuple, set)):
            _size = len(values)
            java_array = get_gateway().new_array(get_jvm().java.lang.Object, _size)
            i = 0
            for value in values:
                if isinstance(value, Dataset):
                    java_array[i] = oj(value)
                else:
                    java_array[i] = value
                i += 1

        else:
            java_array = get_gateway().new_array(get_jvm().java.lang.Object, 1)
            java_array[0] = values
    return java_array


class _ImportDataProgressListener(PythonListenerBase):

    def __init__(self, progress_fun, name):
        self._stepped = StepEvent()
        PythonListenerBase.__init__(self, "Progress:" + name, progress_fun)

    def stepped(self, event):
        if self.func is not None:
            self._stepped._title = "数据导入"
            total_percent = event.getTotalPercent()
            if total_percent < 100:
                percent = total_percent + int(event.getSubPercent() / event.getCount())
            else:
                percent = 100
            self._stepped._percent = percent
            self._stepped.set_cancel(event.getCancel())
            self._stepped._message = "正在导入 '%s' 文件，已经完成 %d%% " % (
             os.path.basename(event.getCurrentTask().getSourceFilePath()), percent)
            self._stepped._remain_time = 0
            self.func(self._stepped)
            if self._stepped.is_cancel:
                event.setCancle(True)

    class Java:
        implements = ["com.supermap.data.conversion.ImportSteppedListener"]


def _get_import_setting(file_type):
    _file_ImportSettings_ = {'shp':(get_jvm().com.supermap.data.conversion).ImportSettingSHP, 
     'dbf':(get_jvm().com.supermap.data.conversion).ImportSettingDBF, 
     'csv':(get_jvm().com.supermap.data.conversion).ImportSettingCSV, 
     'geojson':(get_jvm().com.supermap.data.conversion).ImportSettingGeoJson, 
     'vct':(get_jvm().com.supermap.data.conversion).ImportSettingVCT, 
     'simplejson':(get_jvm().com.supermap.data.conversion).ImportSettingSimpleJson, 
     'e00':(get_jvm().com.supermap.data.conversion).ImportSettingE00, 
     'osm':(get_jvm().com.supermap.data.conversion).ImportSettingOSM, 
     'coverage':(get_jvm().com.supermap.data.conversion).ImportSettingCoverage, 
     'kml':(get_jvm().com.supermap.data.conversion).ImportSettingKML, 
     'kmz':(get_jvm().com.supermap.data.conversion).ImportSettingKMZ, 
     'gml':(get_jvm().com.supermap.data.conversion).ImportSettingGML, 
     'mapgis':(get_jvm().com.supermap.data.conversion).ImportSettingMAPGIS, 
     'tab':(get_jvm().com.supermap.data.conversion).ImportSettingTAB, 
     'mif':(get_jvm().com.supermap.data.conversion).ImportSettingMIF, 
     'dxf':(get_jvm().com.supermap.data.conversion).ImportSettingDXF, 
     'dwg':(get_jvm().com.supermap.data.conversion).ImportSettingDWG, 
     'dgn':(get_jvm().com.supermap.data.conversion).ImportSettingDGN, 
     'tif':(get_jvm().com.supermap.data.conversion).ImportSettingTIF, 
     'png':(get_jvm().com.supermap.data.conversion).ImportSettingPNG, 
     'bmp':(get_jvm().com.supermap.data.conversion).ImportSettingBMP, 
     'jpg':(get_jvm().com.supermap.data.conversion).ImportSettingJPG, 
     'jp2':(get_jvm().com.supermap.data.conversion).ImportSettingJP2, 
     'aibingrid':(get_jvm().com.supermap.data.conversion).ImportSettingAiBinGrid, 
     'grd':(get_jvm().com.supermap.data.conversion).ImportSettingGRD, 
     'usgsdem':(get_jvm().com.supermap.data.conversion).ImportSettingUSGSDEM, 
     'mrsid':(get_jvm().com.supermap.data.conversion).ImportSettingMrSID, 
     'ecw':(get_jvm().com.supermap.data.conversion).ImportSettingECW, 
     'gif':(get_jvm().com.supermap.data.conversion).ImportSettingGIF, 
     'sit':(get_jvm().com.supermap.data.conversion).ImportSettingSIT, 
     'img':(get_jvm().com.supermap.data.conversion).ImportSettingIMG}
    return _file_ImportSettings_[file_type]()


def _import_vector_data_(file_type, name, source_files, output, out_dataset_name=None, import_mode=None, is_ignore_attrs=None, is_import_empty=None, source_file_charset=None, is_import_as_3d=None, separator=None, is_import_as_cad=None, is_ignore_invisible_object=None, is_import_by_layer=None, style_map_file=None, custom_setting_func=None, progress=None):
    check_lic()
    out_datasource = get_output_datasource(output)
    check_output_datasource(out_datasource)
    _jvm = get_jvm()
    listener = None
    dataImport = _jvm.com.supermap.data.conversion.DataImport()
    settings = dataImport.getImportSettings()
    importSetting = _get_import_setting(file_type)
    if import_mode is not None:
        importSetting.setImportMode(ImportMode._make(import_mode, import_mode.NONE)._jobject)
    else:
        importSetting.setImportMode(ImportMode.NONE._jobject)
    if source_file_charset is not None:
        importSetting.setSourceFileCharset(Charset._make(source_file_charset)._jobject)
    if is_ignore_attrs is not None:
        importSetting.setAttributeIgnored(bool(is_ignore_attrs))
    if is_import_empty is not None:
        importSetting.setImportEmptyDataset(bool(is_import_empty))
    if is_import_as_3d is not None:
        importSetting.setImporttingAs3D(bool(is_import_as_3d))
    if separator is not None:
        importSetting.setSeparator(separator)
    if is_import_as_cad is not None:
        importSetting.setImportingAsCAD(bool(is_import_as_cad))
    if is_ignore_invisible_object is not None:
        importSetting.setUnvisibleObjectIgnored(bool(is_ignore_invisible_object))
    if is_import_by_layer is not None:
        importSetting.setImportingByLayer(bool(is_import_by_layer))
    if style_map_file is not None:
        importSetting.setStyleMappingTableFile(style_map_file)
    if custom_setting_func is not None:
        custom_setting_func(importSetting)
    settings.add(importSetting)
    dataImport.setImportSettings(settings)
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = _ImportDataProgressListener(progress, name)
                dataImport.addImportSteppedListener(listener)
            except Exception as e:
                try:
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    if not isinstance(source_files, (list, tuple, set)):
        source_files = [
         source_files]
    all_results = []
    for source_file in source_files:
        _check_file_exist(source_file)
        if not out_dataset_name is None:
            if len(source_files) > 1:
                out_dataset_name = _get_file_name(source_file)
                out_dataset_name = out_datasource.get_available_dataset_name(out_dataset_name)
            importSetting.setTargetDatasource(out_datasource._jobject)
            importSetting.setSourceFilePath(source_file)
            importSetting.setTargetDatasetName(out_dataset_name)
            try:
                try:
                    import_result = dataImport.run()
                    if import_result is not None:
                        results = java_array_to_list(import_result.getSucceedDatasetNames(importSetting))
                    else:
                        results = None
                except Exception as e:
                    try:
                        import traceback
                        log_error(traceback.format_exc())
                        results = None
                    finally:
                        e = None
                        del e

            finally:
                if results:
                    all_results.extend(results)

    if listener is not None:
        try:
            dataImport.removeImportSteppedListener(listener)
        except Exception as e1:
            try:
                log_error(e1)
            finally:
                e1 = None
                del e1

    if dataImport is not None:
        dataImport.dispose()
    return try_close_output_datasource(all_results, out_datasource)


def import_shape(source_file, output, out_dataset_name=None, import_mode=None, is_ignore_attrs=False, is_import_empty=False, source_file_charset=None, is_import_as_3d=False, progress=None):
    """
    导入 shape 文件到数据源中。支持导入文件目录。

    :param str source_file: 被导入的 shape 文件
    :param output: 结果数据源
    :type output: Datasource or  DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param import_mode: 导入模式类型，可以为 ImportMode 枚举值或名称
    :type import_mode: ImportMode or str
    :param bool is_ignore_attrs: 是否忽略属性信息，默认值为 False
    :param bool is_import_empty: 否导入空的数据集，默认是不导入的。默认为 False
    :param source_file_charset: shape 文件的原始字符集类型
    :type source_file_charset: Charset or str
    :param bool is_import_as_3d: 是否导入为 3D 数据集
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 导入后的结果数据集或结果数据集名称
    :rtype: list[DatasetVector] or list[str]

    >>> result = import_shape( 'E:/point.shp', 'E:/import_shp_out.udb')
    >>> print(len(result) == 1)
    >>> print(result[0])

    """
    source_files = _read_dir(source_file, ["shp"])
    return _import_vector_data_("shp", "import_shape", source_files=source_files, output=output, out_dataset_name=out_dataset_name,
      import_mode=import_mode,
      is_ignore_attrs=is_ignore_attrs,
      is_import_empty=is_import_empty,
      source_file_charset=source_file_charset,
      is_import_as_3d=is_import_as_3d,
      progress=progress)


def import_dbf(source_file, output, out_dataset_name=None, import_mode=None, is_import_empty=False, source_file_charset=None, progress=None):
    """
    导入 dbf 文件到数据源中。支持导入文件目录。

    :param str source_file: 被导入的 dbf 文件
    :param output: 结果数据源
    :type output: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param import_mode: 导入模式类型，可以为 ImportMode 枚举值或名称
    :type import_mode: ImportMode or str
    :param bool is_import_empty: 否导入空的数据集，默认是不导入的。默认为 False
    :param source_file_charset: dbf 文件的原始字符集类型
    :type source_file_charset: Charset or str
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 导入后的结果数据集或结果数据集名称
    :rtype: list[DatasetVector] or list[str]

    >>> result = import_dbf( 'E:/point.dbf', 'E:/import_dbf_out.udb')
    >>> print(len(result) == 1)
    >>> print(result[0])

    """
    source_files = _read_dir(source_file, ["dbf"])
    return _import_vector_data_("dbf", "import_dbf", source_files=source_files, output=output, out_dataset_name=out_dataset_name,
      import_mode=import_mode,
      is_import_empty=is_import_empty,
      source_file_charset=source_file_charset,
      progress=progress)


def import_csv(source_file, output, out_dataset_name=None, import_mode=None, separator=',', head_is_field=True, fields_as_point=None, field_as_geometry=None, is_import_empty=False, source_file_charset=None, progress=None):
    """
    导入 CSV 文件。支持导入文件目录。

    :param str source_file: 被导入的 csv 文件
    :param output: 结果数据源
    :type output: Datasource or  DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param import_mode: 导入模式类型，可以为 ImportMode 枚举值或名称
    :type import_mode: ImportMode or str
    :param str separator: 源 CSV 文件中字段的分隔符。默认以 ',' 作为分隔符
    :param bool head_is_field: CSV 文件的首行是否为字段名称
    :param fields_as_point: 指定字段为X、Y或者X、Y、Z坐标，如果符合条件，则生成点或者三维点数据集
    :type fields_as_point: list[str] or list[int]
    :param int field_as_geometry: 指定WKT串的Geometry索引位置
    :param bool is_import_empty: 是否导入空的数据集，默认为 False，即不导入
    :param source_file_charset: CSV 文件的原始字符集类型
    :type source_file_charset: Charset or str
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 导入后的结果数据集或结果数据集名称
    :rtype: list[DatasetVector] or list[str]
    """

    def func(setting):
        if fields_as_point is not None:
            if isinstance(fields_as_point[0], str):
                setting.setFieldsAsPoint(to_java_string_array(fields_as_point))
            else:
                if isinstance(fields_as_point[0], int):
                    setting.setIndexsAsPoint(to_java_int_array(fields_as_point))
        if field_as_geometry is not None:
            setting.setIndexAsGeometry(field_as_geometry)
        if head_is_field is not None:
            setting.setFirstRowIsField(bool(head_is_field))

    source_files = _read_dir(source_file, ["csv"])
    return _import_vector_data_("csv", "import_csv", import_mode=import_mode, source_files=source_files, output=output, out_dataset_name=out_dataset_name,
      separator=separator,
      is_import_empty=is_import_empty,
      source_file_charset=source_file_charset,
      progress=progress,
      custom_setting_func=func)


def import_geojson(source_file, output, out_dataset_name=None, import_mode=None, is_import_empty=False, is_import_as_cad=False, source_file_charset=None, progress=None):
    """
    导入 GeoJson 文件

    :param str source_file: 被导入的 GeoJson 文件
    :param output: 结果数据源
    :type output: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param import_mode: 导入模式
    :type import_mode: ImportMode or str
    :param bool is_import_empty: 是否导入空的数据集，默认为 False
    :param bool is_import_as_cad: 是否导入为 CAD 数据集
    :param source_file_charset: GeoJson 文件的原始字符集类型
    :type source_file_charset: Charset or str
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 导入后的结果数据集或结果数据集名称
    :rtype: list[DatasetVector] or list[str]
    """
    return _import_vector_data_("geojson", "import_geojson", source_files=source_file, output=output, out_dataset_name=out_dataset_name,
      import_mode=import_mode,
      is_import_empty=is_import_empty,
      source_file_charset=source_file_charset,
      is_import_as_cad=is_import_as_cad,
      progress=progress)


def import_vct(source_file, output, out_dataset_name=None, import_mode=None, is_import_empty=False, source_file_charset=None, layers=None, progress=None):
    """
    导入 VCT 文件。支持导入文件目录。

    :param str source_file: 被导入的 VCT 文件
    :param output: 结果数据源
    :type output: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param import_mode: 数据集导入模式
    :type import_mode: ImportMode or str
    :param bool is_import_empty: 是否导入空数据集
    :param source_file_charset:  VCT 文件的原始字符集
    :type source_file_charset: Charset or str
    :param layers: 需要导入的图层名称，设置为 None 时将全部导入。
    :type layers: str or list[str]
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 导入后的结果数据集或结果数据集名称
    :rtype: list[DatasetVector] or list[str]
    """

    def func(setting):
        if layers is not None:
            setting.setImportLayerName(to_java_string_array(split_input_list_from_str(layers)))

    source_files = _read_dir(source_file, ["vct"])
    return _import_vector_data_("vct", "import_vct", source_files=source_files, output=output, out_dataset_name=out_dataset_name,
      import_mode=import_mode,
      is_import_empty=is_import_empty,
      source_file_charset=source_file_charset,
      progress=progress,
      custom_setting_func=func)


def import_simplejson(source_file, output, out_dataset_name=None, import_mode=None, is_import_empty=False, source_file_charset=None, progress=None):
    """
    导入 SimpleJson 文件

    :param str source_file: 被导入的 SimpleJson 文件
    :param output: 结果数据源
    :type output: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param import_mode: 数据集导入模式
    :type import_mode: ImportMode or str
    :param bool is_import_empty: 是否导入空数据集
    :param source_file_charset:  SimpleJson 文件的原始字符集
    :type source_file_charset: Charset or str
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 导入后的结果数据集或结果数据集名称
    :rtype: list[DatasetVector] or list[str]
    """
    return _import_vector_data_("simplejson", "import_simplejson", source_files=source_file, output=output, out_dataset_name=out_dataset_name,
      import_mode=import_mode,
      is_import_empty=is_import_empty,
      source_file_charset=source_file_charset,
      progress=progress)


def import_e00(source_file, output, out_dataset_name=None, import_mode=None, is_ignore_attrs=True, source_file_charset=None, progress=None):
    """
    导入 E00 文件。支持导入文件目录。

    :param str source_file: 被导入的 E00 文件
    :param output: 结果数据源
    :type output: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param import_mode: 数据集导入模式
    :type import_mode: ImportMode or str
    :param bool is_ignore_attrs: 是否忽略属性信息
    :param source_file_charset:  E00 文件的原始字符集
    :type source_file_charset: Charset or str
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 导入后的结果数据集或结果数据集名称
    :rtype: list[DatasetVector] or list[str]
    """
    source_files = _read_dir(source_file, ["e00"])
    return _import_vector_data_("e00", "import_e00", source_files=source_files, output=output, out_dataset_name=out_dataset_name,
      import_mode=import_mode,
      is_ignore_attrs=is_ignore_attrs,
      source_file_charset=source_file_charset,
      progress=progress)


def import_osm(source_file, output, out_dataset_name=None, import_mode=None, source_file_charset=None, progress=None):
    """
    导入 OSM 矢量数据, Linux 平台不支持 OSM 文件。支持导入文件目录。

    :param str source_file: 被导入的 OSM 文件
    :param output: 结果数据源
    :type output: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param import_mode: 数据集导入模式
    :type import_mode: ImportMode or str
    :param source_file_charset:  OSM 文件的原始字符集
    :type source_file_charset: Charset or str
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 导入后的结果数据集或结果数据集名称
    :rtype: list[DatasetVector] or list[str]
    """
    if is_linux():
        return
    return _import_vector_data_("osm", "import_osm", source_files=(_read_dir(source_file, ["osm"])), output=output, out_dataset_name=out_dataset_name,
      import_mode=import_mode,
      source_file_charset=source_file_charset,
      progress=progress)


def _import_coverage(source_file, output, out_dataset_name=None, import_mode=None, is_ignore_attrs=True, source_file_charset=None, progress=None):
    """
    导入 ArcInfo Coverage 文件

    :param str source_file: 被导入的 ArcInfo Coverage 文件
    :param output: 结果数据源
    :type output: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param import_mode: 数据集导入模式
    :type import_mode: ImportMode or str
    :param bool is_ignore_attrs: 是否忽略属性信息
    :param source_file_charset:  ArcInfo Coverage 文件的原始字符集
    :type source_file_charset: Charset or str
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 导入后的结果数据集或结果数据集名称
    :rtype: list[DatasetVector] or list[str]
    """
    return _import_vector_data_("coverage", "import_coverage", source_files=source_file, output=output, out_dataset_name=out_dataset_name,
      import_mode=import_mode,
      is_ignore_attrs=is_ignore_attrs,
      source_file_charset=source_file_charset,
      progress=progress)


def import_kml(source_file, output, out_dataset_name=None, import_mode=None, is_import_empty=False, is_import_as_cad=False, is_ignore_invisible_object=True, source_file_charset=None, progress=None):
    """
    导入 KML 文件。支持导入文件目录。

    :param str source_file: 被导入的 KML 文件
    :param output: 结果数据源
    :type output: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :type import_mode: ImportMode or str
    :param bool is_import_empty: 是否导入空的数据集
    :param bool is_import_as_cad: 是否以 CAD 数据集方式导入
    :param bool is_ignore_invisible_object: 是否忽略不可见对象
    :param source_file_charset: KML 文件的原始字符集
    :type source_file_charset: Charset or str
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 导入后的结果数据集或结果数据集名称
    :rtype: list[DatasetVector] or list[str]
    """
    source_files = _read_dir(source_file, ["kml"])
    return _import_vector_data_("kml", "import_kml", source_files=source_files, output=output, out_dataset_name=out_dataset_name,
      import_mode=import_mode,
      is_import_empty=is_import_empty,
      source_file_charset=source_file_charset,
      is_import_as_cad=is_import_as_cad,
      is_ignore_invisible_object=is_ignore_invisible_object,
      progress=progress)


def import_kmz(source_file, output, out_dataset_name=None, import_mode=None, is_import_empty=False, is_import_as_cad=False, is_ignore_invisible_object=True, source_file_charset=None, progress=None):
    """
    导入 KMZ 文件。支持导入文件目录。

    :param str source_file: 被导入的 KMZ 文件
    :param output: 结果数据源
    :type output: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param import_mode: 数据集导入模式
    :type import_mode: ImportMode or str
    :param bool is_import_empty: 是否导入空的数据集
    :param bool is_import_as_cad: 是否以 CAD 数据集方式导入
    :param bool is_ignore_invisible_object: 是否忽略不可见对象
    :param source_file_charset: KMZ 文件的原始字符集
    :type source_file_charset: Charset or str
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 导入后的结果数据集或结果数据集名称
    :rtype: list[DatasetVector] or list[str]
    """
    source_files = _read_dir(source_file, ["kmz"])
    return _import_vector_data_("kmz", "import_kmz", source_files=source_files, output=output, out_dataset_name=out_dataset_name,
      import_mode=import_mode,
      is_import_empty=is_import_empty,
      source_file_charset=source_file_charset,
      is_import_as_cad=is_import_as_cad,
      is_ignore_invisible_object=is_ignore_invisible_object,
      progress=progress)


def _import_gml(source_file, output, out_dataset_name=None, import_mode=None, is_import_empty=False, is_ignore_attrs=False, is_import_as_cad=False, is_import_by_layer=False, source_file_charset=None, progress=None):
    """
    导入 GML 文件。支持导入文件目录。

    :param str source_file: 被导入的 GML 文件
    :param output: 结果数据源
    :type output: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param import_mode: 数据集导入模式
    :type import_mode: ImportMode or str
    :param bool is_import_empty: 是否导入空的数据集
    :param bool is_ignore_attrs: 导入 GML 格式数据时是否忽略属性信息。
    :param bool is_import_as_cad: 是否以 CAD 数据集方式导入
    :param bool is_import_by_layer: 导入后的数据中是否合并源数据中的 CAD 图层信息，CAD 是以图层信息来存储的，默认为 false，即所有的图层信息都合并到了一个 CAD 数据集， 否则对应源数据中的每一个图层生成一个 CAD 数据集。
    :param source_file_charset: gml 文件的原始字符集
    :type source_file_charset: Charset or str
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 导入后的结果数据集或结果数据集名称
    :rtype: list[DatasetVector] or list[str]
    """
    source_files = _read_dir(source_file, ["gml"])
    return _import_vector_data_("gml", "ImportGML", source_files=source_files, output=output, out_dataset_name=out_dataset_name,
      import_mode=import_mode,
      is_import_empty=is_import_empty,
      source_file_charset=source_file_charset,
      is_import_as_cad=is_import_as_cad,
      is_ignore_attrs=is_ignore_attrs,
      is_import_by_layer=is_import_by_layer,
      progress=progress)


def import_mapgis(source_file, output, out_dataset_name=None, import_mode=None, is_import_as_cad=True, color_index_file_path=None, import_network_topology=False, source_file_charset=None, progress=None):
    """
    导入 MapGIS 文件，Linux 平台不支持导入 MapGIS 文件。

    :param str source_file: 被导入的 MAPGIS 文件
    :param output: 结果数据源
    :type output: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param import_mode: 数据集导入模式
    :type import_mode: ImportMode or str
    :param bool is_import_as_cad: 是否以 CAD 数据集方式导入
    :param str color_index_file_path: MAPGIS 导入数据时的颜色索引表文件路径，默认文件路径为系统路径下的 MapGISColor.wat
    :param bool import_network_topology: 导入时是否导入网络数据集
    :param source_file_charset: MAPGIS 文件的原始字符集
    :type source_file_charset: Charset or str
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 导入后的结果数据集或结果数据集名称
    :rtype: list[DatasetVector] or list[str]
    """
    if is_linux():
        return

    def func(setting):
        if color_index_file_path is not None:
            setting.setColorIndexFilePath(color_index_file_path)
        if import_network_topology is not None:
            setting.setImportNetworkTopology(bool(import_network_topology))

    return _import_vector_data_("mapgis", "import_mapgis", source_files=source_file, output=output, out_dataset_name=out_dataset_name,
      import_mode=import_mode,
      source_file_charset=source_file_charset,
      is_import_as_cad=is_import_as_cad,
      progress=progress,
      custom_setting_func=func)


def import_tab(source_file, output, out_dataset_name=None, import_mode=None, is_ignore_attrs=True, is_import_empty=False, is_import_as_cad=False, style_map_file=None, source_file_charset=None, progress=None):
    """
    导入 TAB 文件。支持导入文件目录。

    :param str source_file: 被导入的 TAB 文件
    :param output: 结果数据源
    :type output: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param import_mode: 数据集导入模式
    :type import_mode: ImportMode or str
    :param bool is_ignore_attrs: 导入 TAB 格式数据时是否忽略该数据的属性，包括矢量数据的属性信息。
    :param bool is_import_empty: 是否导入空的数据集，默认为 False，即不导入
    :param bool is_import_as_cad: 是否以 CAD 数据集方式导入
    :param source_file_charset: mif 文件的原始字符集
    :type source_file_charset: Charset or str
    :param str style_map_file: 风格对照表的存储路径
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 导入后的结果数据集或结果数据集名称
    :rtype: list[DatasetVector] or list[str]
    """
    source_files = _read_dir(source_file, ["tab"])
    return _import_vector_data_("tab", "import_tab", source_files=source_files, output=output, out_dataset_name=out_dataset_name,
      import_mode=import_mode,
      source_file_charset=source_file_charset,
      is_import_as_cad=is_import_as_cad,
      is_ignore_attrs=is_ignore_attrs,
      is_import_empty=is_import_empty,
      style_map_file=style_map_file,
      progress=progress)


def import_mif(source_file, output, out_dataset_name=None, import_mode=None, is_ignore_attrs=True, is_import_as_cad=False, style_map_file=None, source_file_charset=None, progress=None):
    """
    导入 MIF 文件。支持导入文件目录。

    :param str source_file: 被导入的 mif 文件
    :param output: 结果数据源
    :type output: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param import_mode: 数据集导入模式
    :type import_mode: ImportMode or str
    :param bool is_ignore_attrs: 导入 MIF 格式数据时是否忽略该数据的属性，包括矢量数据的属性信息。
    :param bool is_import_as_cad: 是否以 CAD 数据集方式导入
    :param source_file_charset: mif 文件的原始字符集
    :type source_file_charset: Charset or str
    :param str style_map_file: 风格对照表的存储路径
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 导入后的结果数据集或结果数据集名称
    :rtype: list[DatasetVector] or list[str]
    """
    source_files = _read_dir(source_file, ["mif"])
    return _import_vector_data_("mif", "import_mif", source_files=source_files, output=output, out_dataset_name=out_dataset_name,
      import_mode=import_mode,
      source_file_charset=source_file_charset,
      is_import_as_cad=is_import_as_cad,
      is_ignore_attrs=is_ignore_attrs,
      style_map_file=style_map_file,
      progress=progress)


def import_dxf(source_file, output, out_dataset_name=None, import_mode=None, is_import_empty=False, is_import_as_cad=True, is_import_by_layer=False, ignore_block_attrs=True, block_as_point=False, import_external_data=False, import_xrecord=True, import_invisible_layer=False, keep_parametric_part=False, ignore_lwpline_width=False, shx_paths=None, curve_segment=73, style_map_file=None, progress=None):
    """
    导入 DXF 文件，Linux 平台不支持导入 DXF 文件。支持导入文件目录。

    :param str source_file: 被导入的 dxf 文件
    :param output: 结果数据源
    :type output: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param import_mode: 数据集导入模式
    :type import_mode: ImportMode or str
    :param bool is_import_empty: 是否导入空的数据集，默认为 False，即不导入
    :param bool is_import_as_cad: 是否以 CAD 数据集方式导入
    :param bool is_import_by_layer: 是否在导入后的数据中合并源数据中的 CAD 图层信息，CAD 是以图层信息来存储的，默认为 False，即所有的图层信息都合并到了一个 CAD 数据集， 否则对应源数据中的每一个图层生成一个 CAD 数据集。
    :param bool ignore_block_attrs: 是否数据导入时是否忽略块儿属性。默认为 True
    :param bool block_as_point: 将符号块导入为点对象还是复合对象，默认为 False， 即将原有的符号块作为复合对象导入，否则在符号块的位置用点对象代替。
    :param bool import_external_data: 否导入外部数据，外部数据为 CAD 中类似属性表的数据导入后格式为一些额外的字段，默认为 False，否则将外部数据追加在默认字段后面。
    :param bool import_xrecord: 是否将用户自定义的字段以及属性字段作为扩展记录导入。
    :param bool import_invisible_layer: 是否导入不可见图层
    :param bool keep_parametric_part: 是否保留Acad数据中的参数化部分
    :param bool ignore_lwpline_width: 是否忽略多义线宽度，默认为 False。
    :param shx_paths: shx 字体库的路径
    :type shx_paths: list[str]
    :param int curve_segment: 曲线拟合精度，默认为 73
    :param str style_map_file: 风格对照表的存储路径
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 导入后的结果数据集或结果数据集名称
    :rtype: list[DatasetVector] or list[str]
    """
    if is_linux():
        return

    def func(setting):
        if ignore_block_attrs is not None:
            setting.setBlockAttributeIgnored(bool(ignore_block_attrs))
        elif block_as_point is not None:
            setting.setImportingBlockAsPoint(bool(block_as_point))
        if curve_segment is not None and curve_segment > 0:
            setting.setCurveSegment(int(curve_segment))
        if import_external_data is not None:
            setting.setImportingExternalData(bool(import_external_data))
        if import_xrecord is not None:
            setting.setImportingXRecord(bool(import_xrecord))
        if import_invisible_layer is not None:
            setting.setImportingInvisibleLayer(bool(import_invisible_layer))
        if keep_parametric_part is not None:
            setting.setKeepingParametricPart(bool(keep_parametric_part))
        if ignore_lwpline_width is not None:
            setting.setLWPLineWidthIgnored(bool(ignore_lwpline_width))
        if shx_paths is not None:
            setting.setShxPaths(to_java_string_array(split_input_list_from_str(shx_paths)))

    source_files = _read_dir(source_file, ["dxf"])
    return _import_vector_data_("dxf", "import_dxf", source_files=source_files, output=output, out_dataset_name=out_dataset_name,
      import_mode=import_mode,
      is_import_as_cad=is_import_as_cad,
      is_import_by_layer=is_import_by_layer,
      is_import_empty=is_import_empty,
      style_map_file=style_map_file,
      progress=progress,
      custom_setting_func=func)


def import_dwg(source_file, output, out_dataset_name=None, import_mode=None, is_import_empty=False, is_import_as_cad=True, is_import_by_layer=False, ignore_block_attrs=True, block_as_point=False, import_external_data=False, import_xrecord=True, import_invisible_layer=False, keep_parametric_part=False, ignore_lwpline_width=False, shx_paths=None, curve_segment=73, style_map_file=None, progress=None):
    """
    导入 DWG 文件，Linux 平台不支持导入 DWG 文件。支持导入文件目录。

    :param str source_file: 被导入的 dwg 文件
    :param output: 结果数据源
    :type output: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param import_mode: 数据集导入模式
    :type import_mode: ImportMode or str
    :param bool is_import_empty: 是否导入空的数据集，默认为 False，即不导入
    :param bool is_import_as_cad: 是否以 CAD 数据集方式导入
    :param bool is_import_by_layer: 是否在导入后的数据中合并源数据中的 CAD 图层信息，CAD 是以图层信息来存储的，默认为 False，即所有的图层信息都合并到了一个 CAD 数据集， 否则对应源数据中的每一个图层生成一个 CAD 数据集。
    :param bool ignore_block_attrs: 是否数据导入时是否忽略块儿属性。默认为 True
    :param bool block_as_point: 将符号块导入为点对象还是复合对象，默认为 False， 即将原有的符号块作为复合对象导入，否则在符号块的位置用点对象代替。
    :param bool import_external_data: 否导入外部数据，外部数据为 CAD 中类似属性表的数据导入后格式为一些额外的字段，默认为 False，否则将外部数据追加在默认字段后面。
    :param bool import_xrecord: 是否将用户自定义的字段以及属性字段作为扩展记录导入。
    :param bool import_invisible_layer: 是否导入不可见图层
    :param bool keep_parametric_part: 是否保留Acad数据中的参数化部分
    :param bool ignore_lwpline_width: 是否忽略多义线宽度，默认为 False。
    :param shx_paths: shx 字体库的路径
    :type shx_paths: list[str]
    :param int curve_segment: 曲线拟合精度，默认为 73
    :param str style_map_file: 风格对照表的存储路径
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 导入后的结果数据集或结果数据集名称
    :rtype: list[DatasetVector] or list[str]
    """
    if is_linux():
        return

    def func(setting):
        if ignore_block_attrs is not None:
            setting.setBlockAttributeIgnored(bool(ignore_block_attrs))
        elif block_as_point is not None:
            setting.setImportingBlockAsPoint(bool(block_as_point))
        if curve_segment is not None and curve_segment > 0:
            setting.setCurveSegment(int(curve_segment))
        if import_external_data is not None:
            setting.setImportingExternalData(bool(import_external_data))
        if import_xrecord is not None:
            setting.setImportingXRecord(bool(import_xrecord))
        if import_invisible_layer is not None:
            setting.setImportingInvisibleLayer(bool(import_invisible_layer))
        if keep_parametric_part is not None:
            setting.setKeepingParametricPart(bool(keep_parametric_part))
        if ignore_lwpline_width is not None:
            setting.setLWPLineWidthIgnored(bool(ignore_lwpline_width))
        if shx_paths is not None:
            setting.setShxPaths(to_java_string_array(split_input_list_from_str(shx_paths)))

    source_files = _read_dir(source_file, ["dwg"])
    return _import_vector_data_("dwg", "import_dwg", source_files=source_files, output=output, out_dataset_name=out_dataset_name,
      import_mode=import_mode,
      is_import_as_cad=is_import_as_cad,
      is_import_by_layer=is_import_by_layer,
      is_import_empty=is_import_empty,
      style_map_file=style_map_file,
      progress=progress,
      custom_setting_func=func)


def import_dgn(source_file, output, out_dataset_name=None, import_mode=None, is_import_empty=False, is_import_as_cad=True, style_map_file=None, is_import_by_layer=False, is_cell_as_point=False, progress=None):
    """
    导入 DGN 文件。支持导入文件目录。

    :param str source_file: 被导入的 dgn 文件
    :param output: 结果数据源
    :type output: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param import_mode: 导入模式
    :type import_mode: ImportMode or str
    :param bool is_import_empty: 是否导入空数据集，默认为 False
    :param bool is_import_as_cad: 是否导入为 CAD 数据集，默认为 True
    :param str style_map_file: 设置风格对照表的存储路径。 风格对照表是指 SuperMap 系统与其它系统风格（包括：符号、线型、填充等）的对照文件。风格对照表只对 CAD 类型的数据，如 DXF、DWG、DGN 起作用。在设置风格对照表之前，必须保证数据是以CAD方式导入，且不忽略风格。
    :param bool is_import_by_layer: 是否在导入后的数据中合并源数据中的 CAD 图层信息，CAD 是以图层信息来存储的，默认为 False，即所有 的图层信息都合并到了一个 CAD 数据集， 否则对应源数据中的每一个图层生成一个 CAD 数据集。
    :param bool is_cell_as_point: 是否将 cell（单元）对象导入为点对象(cell header)还是除 cell header 外的所有要素对象。 默认导入为除 cell header 外的所有要素对象。
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 导入后的结果数据集或结果数据集名称
    :rtype: list[DatasetVector] or list[str]
    """

    def func(setting):
        if is_cell_as_point is not None:
            setting.setImportingCellAsPoint(bool(is_cell_as_point))

    source_files = _read_dir(source_file, ["dgn"])
    return _import_vector_data_("dgn", "import_dgn", source_files=source_files, output=output, out_dataset_name=out_dataset_name,
      import_mode=import_mode,
      is_import_as_cad=is_import_as_cad,
      is_import_by_layer=is_import_by_layer,
      is_import_empty=is_import_empty,
      style_map_file=style_map_file,
      progress=progress,
      custom_setting_func=func)


def _import_raster_data_(file_type, name, source_files, output, out_dataset_name=None, ignore_mode=None, ignore_values=None, multi_band_mode=None, world_file_path=None, is_import_as_grid=None, is_build_pyramid=None, custom_setting_func=None, progress=None):
    out_datasource = get_output_datasource(output)
    check_output_datasource(out_datasource)
    _jvm = get_jvm()
    if not isinstance(source_files, (list, tuple, set)):
        source_files = [
         source_files]
    all_results = []
    dataImport = _jvm.com.supermap.data.conversion.DataImport()
    settings = dataImport.getImportSettings()
    importSetting = _get_import_setting(file_type)
    if ignore_mode is not None:
        importSetting.setIgnoreMode(IgnoreMode._make(ignore_mode)._jobject)
    if multi_band_mode is not None:
        importSetting.setMultiBandImportMode(MultiBandImportMode._make(multi_band_mode)._jobject)
    if world_file_path is not None:
        importSetting.setWorldFilePath(str(world_file_path))
    if is_import_as_grid is not None:
        importSetting.setImportingAsGrid(bool(is_import_as_grid))
    if is_build_pyramid is not None:
        importSetting.setPyramidBuilt(bool(is_build_pyramid))
    if ignore_values is not None:
        importSetting.setIgnoreValues(to_java_double_array(ignore_values))
    if custom_setting_func is not None:
        custom_setting_func(importSetting)
    settings.add(importSetting)
    dataImport.setImportSettings(settings)
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = _ImportDataProgressListener(progress, name)
                dataImport.addImportSteppedListener(listener)
            except Exception as e:
                try:
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    for source_file in source_files:
        _check_file_exist(source_file)
        try:
            try:
                if out_dataset_name is None or len(source_files) > 1:
                    out_dataset_name = _get_file_name(source_file)
                    out_dataset_name = out_datasource.get_available_dataset_name(out_dataset_name)
                else:
                    importSetting.setTargetDatasource(oj(out_datasource))
                    importSetting.setSourceFilePath(source_file)
                    importSetting.setTargetDatasetName(out_dataset_name)
                    import_result = dataImport.run()
                    if import_result is not None:
                        results = java_array_to_list(import_result.getSucceedDatasetNames(importSetting))
                    else:
                        results = None
            except Exception as e:
                try:
                    import traceback
                    log_error(traceback.format_exc())
                    results = None
                finally:
                    e = None
                    del e

        finally:
            if results:
                all_results.extend(results)

    if listener is not None:
        try:
            dataImport.removeImportSteppedListener(listener)
        except Exception as e1:
            try:
                log_error(e1)
            finally:
                e1 = None
                del e1

    if dataImport is not None:
        dataImport.dispose()
    return try_close_output_datasource(all_results, out_datasource)


def _read_dir(file_path, file_ext):
    import os
    if not file_path:
        raise ValueError("input file path is None")
    elif not os.path.isdir(file_path):
        return [
         file_path]
        if file_ext is not None:
            if not isinstance(file_ext, (tuple, list, set)):
                file_ext = [
                 file_ext]
            file_ext = set(file_ext)
    else:
        file_ext = set()
    res = []
    for root, dirs, files in os.walk(file_path):
        for name in files:
            if name.split(".")[-1] in file_ext:
                res.append(os.path.join(root, name))

    return res


def import_tif(source_file, output, out_dataset_name=None, ignore_mode='IGNORENONE', ignore_values=None, multi_band_mode=None, world_file_path=None, is_import_as_grid=False, is_build_pyramid=True, progress=None):
    """
    导入 TIF 文件。支持导入文件目录。

    :param str source_file: 被导入的 TIF 文件
    :param output: 结果数据源
    :type output: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param ignore_mode: Tiff/BigTIFF/GeoTIFF 文件的忽略颜色值的模式
    :type ignore_mode: IgnoreMode or str
    :param ignore_values: 要忽略的颜色值
    :type ignore_values: list[float] 要忽略的颜色值
    :param multi_band_mode: 多波段导入模式，可以导入为多个单波段数据集、单个多波段数据集或单个单波段数据集。
    :type multi_band_mode: MultiBandImportMode or str
    :param str world_file_path: 导入的源影像文件的坐标参考文件路径
    :param bool is_import_as_grid: 是否导入为 Grid 数据集
    :param bool is_build_pyramid: 是否自动建立影像金字塔
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 导入后的结果数据集或结果数据集名称
    :rtype: list[DatasetGrid] or list[DatasetImage] or list[str]
    """
    source_files = _read_dir(source_file, ["tiff", "tif"])
    return _import_raster_data_("tif", "import_tif", source_files, output, out_dataset_name, ignore_mode=ignore_mode, ignore_values=ignore_values,
      multi_band_mode=multi_band_mode,
      world_file_path=world_file_path,
      is_import_as_grid=is_import_as_grid,
      is_build_pyramid=is_build_pyramid,
      progress=progress)


def import_img(source_file, output, out_dataset_name=None, ignore_mode='IGNORENONE', ignore_values=None, multi_band_mode=None, is_import_as_grid=False, is_build_pyramid=True, progress=None):
    """
    导入 Erdas Image 文件。支持导入文件目录。

    :param str source_file: 被导入的 IMG 文件
    :param output: 结果数据源
    :type output: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param ignore_mode: Erdas Image 的忽略颜色值的模式
    :type ignore_mode: IgnoreMode or str
    :param ignore_values: 要忽略的颜色值
    :type ignore_values: list[float] 要忽略的颜色值
    :param multi_band_mode: 多波段导入模式，可以导入为多个单波段数据集、单个多波段数据集或单个单波段数据集。
    :type multi_band_mode: MultiBandImportMode or str
    :param bool is_import_as_grid: 是否导入为 Grid 数据集
    :param bool is_build_pyramid: 是否自动建立影像金字塔
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 导入后的结果数据集或结果数据集名称
    :rtype: list[DatasetGrid] or list[DatasetImage] or list[str]
    """
    source_files = _read_dir(source_file, ["img"])
    return _import_raster_data_("img", "import_img", source_files, output, out_dataset_name, ignore_mode=ignore_mode, ignore_values=ignore_values,
      multi_band_mode=multi_band_mode,
      is_import_as_grid=is_import_as_grid,
      is_build_pyramid=is_build_pyramid,
      progress=progress)


def import_png(source_file, output, out_dataset_name=None, ignore_mode='IGNORENONE', ignore_values=None, world_file_path=None, is_import_as_grid=False, is_build_pyramid=True, progress=None):
    """
    导入 Portal Network Graphic (PNG) 文件。支持导入文件目录。

    :param str source_file: 被导入的 PNG 文件
    :param output: 结果数据源
    :type output: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param ignore_mode: PNG 文件的忽略颜色值的模式
    :type ignore_mode: IgnoreMode or str
    :param ignore_values: 要忽略的颜色值
    :type ignore_values: list[float] 要忽略的颜色值
    :param str world_file_path: 导入的源影像文件的坐标参考文件路径
    :param bool is_import_as_grid: 是否导入为 Grid 数据集
    :param bool is_build_pyramid: 是否自动建立影像金字塔
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 导入后的结果数据集或结果数据集名称
    :rtype: list[DatasetGrid] or list[DatasetImage] or list[str]
    """
    source_files = _read_dir(source_file, ["png"])
    return _import_raster_data_("png", "ImportPNG", source_files, output, out_dataset_name, ignore_mode=ignore_mode, ignore_values=ignore_values,
      multi_band_mode="COMPOSITE",
      world_file_path=world_file_path,
      is_import_as_grid=is_import_as_grid,
      is_build_pyramid=is_build_pyramid,
      progress=progress)


def import_jpg(source_file, output, out_dataset_name=None, ignore_mode='IGNORENONE', ignore_values=None, world_file_path=None, is_import_as_grid=False, is_build_pyramid=True, progress=None):
    """
    导入 JPG 文件。支持导入文件目录。

    :param str source_file: 被导入的 JPG 文件
    :param output: 结果数据源
    :type output: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param ignore_mode: 忽略颜色值的模式
    :type ignore_mode: IgnoreMode or str
    :param ignore_values: 要忽略的颜色值
    :type ignore_values: list[float] 要忽略的颜色值
    :param str world_file_path: 导入的源影像文件的坐标参考文件路径
    :param bool is_import_as_grid: 是否导入为 Grid 数据集
    :param bool is_build_pyramid: 是否自动建立影像金字塔
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 导入后的结果数据集或结果数据集名称
    :rtype: list[DatasetGrid] or list[DatasetImage] or list[str]
    """
    source_files = _read_dir(source_file, ["jpg", "jpge"])
    return _import_raster_data_("jpg", "import_jpg", source_files, output, out_dataset_name, ignore_mode=ignore_mode, ignore_values=ignore_values,
      multi_band_mode="COMPOSITE",
      world_file_path=world_file_path,
      is_import_as_grid=is_import_as_grid,
      is_build_pyramid=is_build_pyramid,
      progress=progress)


def import_jp2(source_file, output, out_dataset_name=None, ignore_mode='IGNORENONE', ignore_values=None, is_import_as_grid=False, progress=None):
    """
    导入 JP2 文件。支持导入文件目录。

    :param str source_file: 被导入的 JP2 文件
    :param output: 结果数据源
    :type output: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param ignore_mode: 忽略颜色值的模式
    :type ignore_mode: IgnoreMode or str
    :param ignore_values: 要忽略的颜色值
    :type ignore_values: list[float] 要忽略的颜色值
    :param bool is_import_as_grid: 是否导入为 Grid 数据集
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 导入后的结果数据集或结果数据集名称
    :rtype: list[DatasetGrid] or list[DatasetImage] or list[str]
    """
    return _import_raster_data_("jp2", "import_jp2", (_read_dir(source_file, ["jp2"])), output, out_dataset_name, ignore_mode=ignore_mode,
      ignore_values=ignore_values,
      is_import_as_grid=is_import_as_grid,
      progress=progress)


def import_mrsid(source_file, output, out_dataset_name=None, ignore_mode='IGNORENONE', ignore_values=None, multi_band_mode=None, is_import_as_grid=False, progress=None):
    """
    导入 MrSID 文件, Linux 平台不支持导入 MrSID 文件。

    :param str source_file: 被导入的 MrSID 文件
    :param output: 结果数据源
    :type output: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param ignore_mode: MrSID 文件的忽略颜色值的模式
    :type ignore_mode: IgnoreMode or str
    :param ignore_values: 要忽略的颜色值
    :type ignore_values: list[float] 要忽略的颜色值
    :param multi_band_mode: 多波段导入模式，可以导入为多个单波段数据集、单个多波段数据集或单个单波段数据集。
    :type multi_band_mode: MultiBandImportMode or str
    :param bool is_import_as_grid: 是否导入为 Grid 数据集
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 导入后的结果数据集或结果数据集名称
    :rtype: list[DatasetGrid] or list[DatasetImage] or list[str]
    """
    if is_linux():
        return
    return _import_raster_data_("mrsid", "import_mrsid", source_file, output, out_dataset_name, ignore_mode=ignore_mode, ignore_values=ignore_values,
      multi_band_mode=multi_band_mode,
      is_import_as_grid=is_import_as_grid,
      progress=progress)


def import_gif(source_file, output, out_dataset_name=None, ignore_mode='IGNORENONE', ignore_values=None, world_file_path=None, is_import_as_grid=False, is_build_pyramid=True, progress=None):
    """
    导入 GIF 文件。支持导入文件目录。

    :param str source_file: 被导入的 GIF 文件
    :param output: 结果数据源
    :type output: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param ignore_mode: GIF 文件的忽略颜色值的模式
    :type ignore_mode: IgnoreMode or str
    :param ignore_values: 要忽略的颜色值
    :type ignore_values: list[float] 要忽略的颜色值
    :param str world_file_path: 导入的源影像文件的坐标参考文件路径
    :param bool is_import_as_grid: 是否导入为 Grid 数据集
    :param bool is_build_pyramid: 是否自动建立影像金字塔
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 导入后的结果数据集或结果数据集名称
    :rtype: list[DatasetGrid] or list[DatasetImage] or list[str]
    """
    source_files = _read_dir(source_file, ["gif"])
    return _import_raster_data_("gif", "import_gif", source_files, output, out_dataset_name, ignore_mode=ignore_mode, ignore_values=ignore_values,
      world_file_path=world_file_path,
      is_build_pyramid=is_build_pyramid,
      is_import_as_grid=is_import_as_grid,
      progress=progress)


def import_ecw(source_file, output, out_dataset_name=None, ignore_mode='IGNORENONE', ignore_values=None, multi_band_mode=None, is_import_as_grid=False, progress=None):
    """
    导入 ECW 文件。支持导入文件目录。

    :param str source_file: 被导入的 ECW 文件
    :param output: 结果数据源
    :type output: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param ignore_mode: ECW 文件的忽略颜色值的模式
    :type ignore_mode: IgnoreMode or str
    :param ignore_values: 要忽略的颜色值
    :type ignore_values: list[float] 要忽略的颜色值
    :param multi_band_mode: 多波段导入模式，可以导入为多个单波段数据集、单个多波段数据集或单个单波段数据集。
    :type multi_band_mode: MultiBandImportMode or str
    :param bool is_import_as_grid: 是否导入为 Grid 数据集
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 导入后的结果数据集或结果数据集名称
    :rtype: list[DatasetGrid]  or list[DatasetImage] or list[str]
    """
    source_files = _read_dir(source_file, ["ecw"])
    return _import_raster_data_("ecw", "import_ecw", source_files, output, out_dataset_name, ignore_mode=ignore_mode, ignore_values=ignore_values,
      multi_band_mode=multi_band_mode,
      is_import_as_grid=is_import_as_grid,
      progress=progress)


def import_bmp(source_file, output, out_dataset_name=None, ignore_mode='IGNORENONE', ignore_values=None, world_file_path=None, is_import_as_grid=False, is_build_pyramid=True, progress=None):
    """
    导入 BMP 文件。支持导入文件目录。

    :param str source_file: 被导入的 BMP 文件
    :param output: 结果数据源
    :type output: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param ignore_mode: BMP 文件的忽略颜色值的模式
    :type ignore_mode: IgnoreMode or str
    :param ignore_values: 要忽略的颜色值
    :type ignore_values: list[float] 要忽略的颜色值
    :param str world_file_path: 导入的源影像文件的坐标参考文件路径
    :param bool is_import_as_grid: 是否导入为 Grid 数据集
    :param bool is_build_pyramid: 是否自动建立影像金字塔
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 导入后的结果数据集或结果数据集名称
    :rtype: list[DatasetGrid] or list[DatasetImage] or list[str]
    """
    source_files = _read_dir(source_file, ["bmp"])
    return _import_raster_data_("bmp", "import_bmp", source_files, output, out_dataset_name, ignore_mode=ignore_mode, ignore_values=ignore_values,
      multi_band_mode="COMPOSITE",
      world_file_path=world_file_path,
      is_import_as_grid=is_import_as_grid,
      is_build_pyramid=is_build_pyramid,
      progress=progress)


def import_aibingrid(source_file, output, out_dataset_name=None, ignore_mode='IGNORENONE', ignore_values=None, is_import_as_grid=False, is_build_pyramid=True, progress=None):
    """
    导入 AIBinGrid 文件， Linux 平台不支持导入 AIBinGrid 文件。

    :param str source_file: 被导入的 AIBinGrid 文件
    :param output: 结果数据源
    :type output: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param ignore_mode: 忽略颜色值的模式
    :type ignore_mode: IgnoreMode or str
    :param ignore_values: 要忽略的颜色值
    :type ignore_values: list[float] 要忽略的颜色值
    :param bool is_import_as_grid: 是否导入为 Grid 数据集
    :param bool is_build_pyramid: 是否自动建立影像金字塔
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 导入后的结果数据集或结果数据集名称
    :rtype: list[DatasetGrid] or list[DatasetImage] or list[str]
    """
    if is_linux():
        return
    return _import_raster_data_("aibingrid", "ImportAiBinGrid", source_file, output, out_dataset_name, ignore_mode=ignore_mode,
      ignore_values=ignore_values,
      is_import_as_grid=is_import_as_grid,
      is_build_pyramid=is_build_pyramid,
      progress=progress)


def import_grd(source_file, output, out_dataset_name=None, ignore_mode='IGNORENONE', ignore_values=None, is_build_pyramid=True, progress=None):
    """
    导入 GRD 文件

    :param str source_file: 被导入的 GRD 文件
    :param output: 结果数据源
    :type output: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param ignore_mode: 忽略颜色值的模式
    :type ignore_mode: IgnoreMode or str
    :param ignore_values: 要忽略的颜色值
    :type ignore_values: list[float] 要忽略的颜色值
    :param bool is_build_pyramid: 是否自动建立影像金字塔
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 导入后的结果数据集或结果数据集名称
    :rtype: list[DatasetGrid] or list[str]
    """
    return _import_raster_data_("grd", "import_grd", source_file, output, out_dataset_name, ignore_mode=ignore_mode,
      ignore_values=ignore_values,
      is_build_pyramid=is_build_pyramid,
      progress=progress)


def import_sit(source_file, output, out_dataset_name=None, ignore_mode='IGNORENONE', ignore_values=None, multi_band_mode=None, is_import_as_grid=False, password=None, progress=None):
    """
    导入 SIT 文件。支持导入文件目录。

    :param str source_file: 被导入的 SIT 文件
    :param output: 结果数据源
    :type output: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param ignore_mode: SIT 文件的忽略颜色值的模式
    :type ignore_mode: IgnoreMode or str
    :param ignore_values: 要忽略的颜色值
    :type ignore_values: list[float] 要忽略的颜色值
    :param multi_band_mode: 多波段导入模式，可以导入为多个单波段数据集、单个多波段数据集或单个单波段数据集。
    :type multi_band_mode: MultiBandImportMode or str
    :param bool is_import_as_grid: 是否导入为 Grid 数据集
    :param str password: 密码
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 导入后的结果数据集或结果数据集名称
    :rtype: list[DatasetGrid] or list[DatasetImage] or list[str]
    """

    def func(setting):
        if password is not None:
            setting.setPassword(password)

    source_files = _read_dir(source_file, ["sit"])
    return _import_raster_data_("sit", "import_sit", source_files, output, out_dataset_name, ignore_mode=ignore_mode,
      ignore_values=ignore_values,
      multi_band_mode=multi_band_mode,
      is_import_as_grid=is_import_as_grid,
      custom_setting_func=func,
      progress=progress)


def import_usgsdem(source_file, output, out_dataset_name=None, ignore_mode='IGNORENONE', ignore_values=None, is_build_pyramid=True, progress=None):
    """
    导入 USGSDEM 文件。

    :param str source_file: 被导入的 USGS DEM 文件
    :param output: 结果数据源
    :type output: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param ignore_mode: 忽略颜色值的模式
    :type ignore_mode: IgnoreMode or str
    :param ignore_values: 要忽略的颜色值
    :type ignore_values: list[float] 要忽略的颜色值
    :param bool is_build_pyramid: 是否自动建立影像金字塔
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 导入后的结果数据集或结果数据集名称
    :rtype: list[DatasetGrid] or list[str]
    """
    return _import_raster_data_("usgsdem", "import_usgsdem", (_read_dir(source_file, ["dem"])), output, out_dataset_name, ignore_mode=ignore_mode,
      ignore_values=ignore_values,
      is_build_pyramid=is_build_pyramid,
      progress=progress)


class _ExportDataProgressListener(PythonListenerBase):

    def __init__(self, progress_fun, name):
        from data.step import StepEvent
        self._stepped = StepEvent()
        PythonListenerBase.__init__(self, "Progress:" + name, progress_fun)

    def stepped(self, event):
        if self.func is not None:
            self._stepped._title = "数据导出"
            totalPercent = event.getTotalPercent()
            if totalPercent < 100:
                percent = totalPercent + int(event.getSubPercent() / event.getCount())
            else:
                percent = 100
            self._stepped._percent = percent
            self._stepped.isCancle = event.getCancel()
            self._stepped._message = '正在导出数据到 "%s" 文件中，已经完成 %d%% ' % (
             os.path.basename(event.getCurrentTask().getTargetFilePath()), percent)
            self._stepped._remainTime = 0
            self.func(self._stepped)
            if self._stepped.isCancle:
                event.setCancle(True)

    class Java:
        implements = ["com.supermap.data.conversion.ExportSteppedListener"]


def _get_export_setting(file_type):
    _file_exportSettings_ = {(FileType.SHP): (get_jvm().com.supermap.data.conversion.ExportSetting), 
     (FileType.DBF): (get_jvm().com.supermap.data.conversion.ExportSetting), 
     (FileType.CSV): (get_jvm().com.supermap.data.conversion.ExportSettingCSV), 
     (FileType.GEOJSON): (get_jvm().com.supermap.data.conversion.ExportSettingGeoJson), 
     (FileType.VCT): (get_jvm().com.supermap.data.conversion.ExportSettingVCT), 
     (FileType.SimpleJson): (get_jvm().com.supermap.data.conversion.ExportSettingSimpleJson), 
     (FileType.E00): (get_jvm().com.supermap.data.conversion.ExportSettingE00), 
     (FileType.KML): (get_jvm().com.supermap.data.conversion.ExportSettingKML), 
     (FileType.KMZ): (get_jvm().com.supermap.data.conversion.ExportSettingKMZ), 
     (FileType.TAB): (get_jvm().com.supermap.data.conversion.ExportSettingTAB), 
     (FileType.MIF): (get_jvm().com.supermap.data.conversion.ExportSetting), 
     (FileType.DXF): (get_jvm().com.supermap.data.conversion.ExportSettingDXF), 
     (FileType.DWG): (get_jvm().com.supermap.data.conversion.ExportSettingDWG), 
     (FileType.TIF): (get_jvm().com.supermap.data.conversion.ExportSettingTIF), 
     (FileType.PNG): (get_jvm().com.supermap.data.conversion.ExportSettingPNG), 
     (FileType.BMP): (get_jvm().com.supermap.data.conversion.ExportSettingBMP), 
     (FileType.JPG): (get_jvm().com.supermap.data.conversion.ExportSettingJPG), 
     (FileType.GRD): (get_jvm().com.supermap.data.conversion.ExportSetting), 
     (FileType.GIF): (get_jvm().com.supermap.data.conversion.ExportSettingGIF), 
     (FileType.SIT): (get_jvm().com.supermap.data.conversion.ExportSettingSIT), 
     (FileType.IMG): (get_jvm().com.supermap.data.conversion.ExportSetting)}
    return _file_exportSettings_[file_type]()


def get_input_datasets(value):
    if value is None:
        return
    if isinstance(value, (list, tuple)):
        res = []
        for item in value:
            dts = get_input_datasets(item)
            if dts is not None:
                if isinstance(dts, (list, tuple)):
                    res.extend(dts)
                else:
                    res.append(dts)

        return res
    if isinstance(value, str):
        values = []
        for item in value.split(","):
            for t in item.split(";"):
                d = get_input_dataset(t)
                if d is not None:
                    values.append(d)

        return values
    return [
     get_input_dataset(value)]


def _export_dataset_to_file(file_type, name, data, output, is_over_write=False, attr_filter=None, ignore_fields=None, target_file_charset=None, custom_setting_func=None, is_support_datasets=False, progress=None):
    check_lic()
    _jvm = get_jvm()
    _data = get_input_datasets(data)
    if _data is None:
        raise Exception("input data is None")
    elif isinstance(_data, list):
        if len(_data) == 0:
            raise ValueError("hava no valid input data for export.")
    listener = None
    try:
        try:
            dataExport = _jvm.com.supermap.data.conversion.DataExport()
            settings = dataExport.getExportSettings()
            exportSetting = _get_export_setting(file_type)
            exportSetting.setTargetFileType(file_type._jobject)
            exportSetting.setTargetFilePath(output)
            if target_file_charset is not None:
                exportSetting.setTargetFileCharset(Charset._make(target_file_charset)._jobject)
            if is_over_write is not None:
                exportSetting.setOverwrite(bool(is_over_write))
            if attr_filter is not None:
                exportSetting.setFilter(attr_filter)
            if ignore_fields is not None:
                exportSetting.setIgnoreFieldNames(to_java_string_array(ignore_fields))
            if custom_setting_func is not None:
                custom_setting_func(exportSetting)
            elif progress is not None and safe_start_callback_server():
                try:
                    listener = _ExportDataProgressListener(progress, name)
                    dataExport.addExportSteppedListener(listener)
                except Exception as e:
                    try:
                        close_callback_server()
                        log_error(e)
                        listener = None
                    finally:
                        e = None
                        del e

                if isinstance(_data, Dataset):
                    exportSetting.setSourceData(_data._jobject)
            elif is_support_datasets:
                exportSetting.setSourceDatas(_to_java_object_array(_data))
            else:
                exportSetting.setSourceData(_data[0]._jobject)
            settings.add(exportSetting)
            dataExport.setExportSettings(settings)
            results = dataExport.run()
        except:
            import traceback
            log_error(traceback.format_exc())
            results = None

    finally:
        if listener is not None:
            try:
                dataExport.removeExportSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        dataExport.dispose()

    if results is not None:
        success_count = len(results.getSucceedSettings())
        if success_count == 1:
            return True
        return False
    else:
        return False


def export_to_shape(data, output, is_over_write=False, attr_filter=None, ignore_fields=None, target_file_charset=None, progress=None):
    """
    导出数据集到 Shape 文件中

    :param data: 被导出的数据集
    :type data: DatasetVector or str
    :param str output: 结果文件路径
    :param bool is_over_write: 导出目录中存在同名文件时，是否强制覆盖。默认为 False
    :param str attr_filter: 导出目标文件的过滤信息
    :param ignore_fields:  需要忽略的字段
    :type ignore_fields: list[str]
    :param target_file_charset: 需要导出的文件的字符集类型
    :type target_file_charset: Charset or str
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 是否导出成功
    :rtype: bool
    """
    return _export_dataset_to_file((FileType.SHP), "export_to_shape", data, output, is_over_write=is_over_write, attr_filter=attr_filter,
      ignore_fields=ignore_fields,
      target_file_charset=target_file_charset,
      progress=progress)


def export_to_dbf(data, output, is_over_write=False, attr_filter=None, ignore_fields=None, target_file_charset=None, progress=None):
    """
    导出数据集到 dbf 文件中

    :param data: 被导出的数据集，只支持导出属性表数据集
    :type data: DatasetVector or str
    :param str output: 结果文件路径
    :param bool is_over_write: 导出目录中存在同名文件时，是否强制覆盖。默认为 False
    :param str attr_filter: 导出目标文件的过滤信息
    :param ignore_fields:  需要忽略的字段
    :type ignore_fields: list[str]
    :param target_file_charset: 需要导出的文件的字符集类型
    :type target_file_charset: Charset or str
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 是否导出成功
    :rtype: bool
    """
    return _export_dataset_to_file((FileType.DBF), "export_to_dbf", data, output, is_over_write=is_over_write, attr_filter=attr_filter,
      ignore_fields=ignore_fields,
      target_file_charset=target_file_charset,
      progress=progress)


def export_to_csv(data, output, is_over_write=False, attr_filter=None, ignore_fields=None, target_file_charset=None, is_export_field_names=True, is_export_point_as_wkt=False, progress=None):
    """
    导出数据集到 csv 文件中

    :param data: 被导出的数据集
    :type data: DatasetVector or str
    :param str output: 结果文件路径
    :param bool is_over_write: 导出目录中存在同名文件时，是否强制覆盖。默认为 False
    :param str attr_filter: 导出目标文件的过滤信息
    :param ignore_fields:  需要忽略的字段
    :type ignore_fields: list[str]
    :param target_file_charset: 需要导出的文件的字符集类型
    :type target_file_charset: Charset or str
    :param bool is_export_field_names:  是否写出字段名称。
    :param bool is_export_point_as_wkt: 是否将点以 WKT 方式写出。
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 是否导出成功
    :rtype: bool
    """

    def func(setting):
        if is_export_field_names is not None:
            setting.setIsExportFieldName(bool(is_export_field_names))
        if is_export_point_as_wkt is not None:
            setting.setIsExportPointAsWKT(bool(is_export_point_as_wkt))

    return _export_dataset_to_file((FileType.CSV), "export_to_csv", data, output, is_over_write=is_over_write, attr_filter=attr_filter,
      custom_setting_func=func,
      ignore_fields=ignore_fields,
      target_file_charset=target_file_charset,
      progress=progress)


def export_to_dwg(data, output, is_over_write=False, attr_filter=None, ignore_fields=None, cad_version=CADVersion.CAD2007, is_export_border=False, is_export_xrecord=False, is_export_external_data=False, style_map_file=None, progress=None):
    """
    导出数据集到 DWG 文件中， Linux 平台不支持导出数据集为 DWG 文件。

    :param data: 被导出的数据集
    :type data: DatasetVector or str
    :param str output: 结果文件路径
    :param bool is_over_write: 导出目录中存在同名文件时，是否强制覆盖。默认为 False
    :param str attr_filter: 导出目标文件的过滤信息
    :param ignore_fields:  需要忽略的字段
    :type ignore_fields: list[str]
    :param cad_version: 导出的 DWG 文件的版本。
    :type cad_version: CADVersion or str
    :param bool is_export_border: 导出cad面对像或矩形对象时是否导出边界。
    :param bool is_export_xrecord: 是否将用户自定义的字段以及属性字段作为扩展记录导出
    :param bool is_export_external_data: 是否导出扩展字段
    :param str style_map_file: 风格对照表的路径
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 是否导出成功
    :rtype: bool
    """
    if is_linux():
        return

    def func(setting):
        if cad_version is not None:
            setting.setVersion(CADVersion._make(cad_version)._jobject)
        if is_export_border is not None:
            setting.setExportingBorder(bool(is_export_border))
        if is_export_xrecord is not None:
            setting.setExportingXRecord(bool(is_export_xrecord))
        if is_export_external_data is not None:
            setting.setExportingExternalData(bool(is_export_external_data))
        if style_map_file is not None:
            setting.setStyleMappingTableFile(str(style_map_file))

    return _export_dataset_to_file((FileType.DWG), "export_to_dwg", data, output, is_over_write=is_over_write, attr_filter=attr_filter,
      custom_setting_func=func,
      ignore_fields=ignore_fields,
      progress=progress)


def export_to_dxf(data, output, is_over_write=False, attr_filter=None, ignore_fields=None, cad_version=CADVersion.CAD2007, is_export_border=False, is_export_xrecord=False, is_export_external_data=False, progress=None):
    """
    导出数据集到 DXF 文件中，Linux 平台不支持导出数据集为 DXF 文件

    :param data: 被导出的数据集
    :type data: DatasetVector or str
    :param str output: 结果文件路径
    :param bool is_over_write: 导出目录中存在同名文件时，是否强制覆盖。默认为 False
    :param str attr_filter: 导出目标文件的过滤信息
    :param ignore_fields:  需要忽略的字段
    :type ignore_fields: list[str]
    :param cad_version: 导出的 DWG 文件的版本。
    :type cad_version: CADVersion or str
    :param bool is_export_border: 导出cad面对像或矩形对象时是否导出边界。
    :param bool is_export_xrecord: 是否将用户自定义的字段以及属性字段作为扩展记录导出
    :param bool is_export_external_data: 是否导出扩展字段
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 是否导出成功
    :rtype: bool
    """
    if is_linux():
        return

    def func(setting):
        if cad_version is not None:
            setting.setVersion(CADVersion._make(cad_version)._jobject)
        if is_export_border is not None:
            setting.setExportingBorder(bool(is_export_border))
        if is_export_xrecord is not None:
            setting.setExportingXRecord(bool(is_export_xrecord))
        if is_export_external_data is not None:
            setting.setExportingExternalData(bool(is_export_external_data))

    return _export_dataset_to_file((FileType.DXF), "export_to_dxf", data, output, is_over_write=is_over_write, attr_filter=attr_filter,
      custom_setting_func=func,
      ignore_fields=ignore_fields,
      progress=progress)


def export_to_e00(data, output, is_over_write=False, attr_filter=None, ignore_fields=None, target_file_charset=None, double_precision=False, progress=None):
    """
    导出数据集到 E00 文件中

    :param data: 被导出的数据集
    :type data: DatasetVector or str
    :param str output: 结果文件路径
    :param bool is_over_write: 导出目录中存在同名文件时，是否强制覆盖。默认为 False
    :param str attr_filter: 导出目标文件的过滤信息
    :param ignore_fields:  需要忽略的字段
    :type ignore_fields: list[str]
    :param target_file_charset: 需要导出的文件的字符集类型
    :type target_file_charset: Charset or str
    :param bool double_precision: 是否以双精度方式导出 E00，默认为 False。
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 是否导出成功
    :rtype: bool
    """

    def func(setting):
        if double_precision is not None:
            setting.setExportingAsDoublePrecision(bool(double_precision))

    return _export_dataset_to_file((FileType.E00), "export_to_e00", data, output, is_over_write=is_over_write, attr_filter=attr_filter,
      custom_setting_func=func,
      ignore_fields=ignore_fields,
      target_file_charset=target_file_charset,
      progress=progress)


def export_to_geojson(data, output, is_over_write=False, attr_filter=None, ignore_fields=None, target_file_charset=None, progress=None):
    """
    导出数据集到 GeoJson 文件中

    :param data: 被导出的数据集集合
    :type data: DatasetVector or str or list[DatasetVector] or list[str]
    :param str output: 结果文件路径
    :param bool is_over_write: 导出目录中存在同名文件时，是否强制覆盖。默认为 False
    :param str attr_filter: 导出目标文件的过滤信息
    :param ignore_fields:  需要忽略的字段
    :type ignore_fields: list[str]
    :param target_file_charset: 需要导出的文件的字符集类型
    :type target_file_charset: Charset or str
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 是否导出成功
    :rtype: bool
    """
    return _export_dataset_to_file((FileType.GEOJSON), "export_to_geojson", data, output, is_over_write=is_over_write, attr_filter=attr_filter,
      ignore_fields=ignore_fields,
      target_file_charset=target_file_charset,
      progress=progress,
      is_support_datasets=True)


def export_to_simplejson(data, output, is_over_write=False, attr_filter=None, ignore_fields=None, target_file_charset=None, progress=None):
    """
    导出数据集到 SimpleJson 文件中

    :param data: 被导出的数据集
    :type data: DatasetVector or str
    :param str output: 结果文件路径
    :param bool is_over_write: 导出目录中存在同名文件时，是否强制覆盖。默认为 False
    :param str attr_filter: 导出目标文件的过滤信息
    :param ignore_fields:  需要忽略的字段
    :type ignore_fields: list[str]
    :param target_file_charset: 需要导出的文件的字符集类型
    :type target_file_charset: Charset or str
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 是否导出成功
    :rtype: bool
    """
    return _export_dataset_to_file((FileType.SimpleJson), "export_to_simplejson", data, output, is_over_write=is_over_write,
      attr_filter=attr_filter,
      is_support_datasets=True,
      ignore_fields=ignore_fields,
      target_file_charset=target_file_charset,
      progress=progress)


def export_to_tab(data, output, is_over_write=False, attr_filter=None, ignore_fields=None, target_file_charset=None, style_map_file=None, progress=None):
    """
    导出数据集到 TAB 文件中

    :param data: 被导出的数据集
    :type data: DatasetVector or str
    :param str output: 结果文件路径
    :param bool is_over_write: 导出目录中存在同名文件时，是否强制覆盖。默认为 False
    :param str attr_filter: 导出目标文件的过滤信息
    :param ignore_fields:  需要忽略的字段
    :type ignore_fields: list[str]
    :param target_file_charset: 需要导出的文件的字符集类型
    :type target_file_charset: Charset or str
    :param str style_map_file: 导出的风格对照表路径
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 是否导出成功
    :rtype: bool
    """

    def func(setting):
        if style_map_file is not None:
            setting.setStyleMappingTableFile(str(style_map_file))

    return _export_dataset_to_file((FileType.TAB), "export_to_tab", data, output, is_over_write=is_over_write, attr_filter=attr_filter,
      custom_setting_func=func,
      ignore_fields=ignore_fields,
      target_file_charset=target_file_charset,
      progress=progress)


def export_to_mif(data, output, is_over_write=False, attr_filter=None, ignore_fields=None, target_file_charset=None, progress=None):
    """
    导出数据集到 MIF 文件中

    :param data: 被导出的数据集
    :type data: DatasetVector or str
    :param str output: 结果文件路径
    :param bool is_over_write: 导出目录中存在同名文件时，是否强制覆盖。默认为 False
    :param str attr_filter: 导出目标文件的过滤信息
    :param ignore_fields:  需要忽略的字段
    :type ignore_fields: list[str]
    :param target_file_charset: 需要导出的文件的字符集类型
    :type target_file_charset: Charset or str
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 是否导出成功
    :rtype: bool
    """
    return _export_dataset_to_file((FileType.MIF), "export_to_mif", data, output, is_over_write=is_over_write, attr_filter=attr_filter,
      ignore_fields=ignore_fields,
      target_file_charset=target_file_charset,
      progress=progress)


def export_to_vct(data, config_path, version, output, is_over_write=False, attr_filter=None, ignore_fields=None, target_file_charset=None, progress=None):
    """
    导出数据集到 VCT 文件中

    :param data: 被导出的数据集集合
    :type data: DatasetVector or str or list[DatasetVector] or str
    :param str config_path: VCT 配置文件路径
    :param version: VCT 版本
    :type version: VCTVersion or str
    :param str output: 结果文件路径
    :param bool is_over_write: 导出目录中存在同名文件时，是否强制覆盖。默认为 False
    :param str attr_filter: 导出目标文件的过滤信息
    :param ignore_fields:  需要忽略的字段
    :type ignore_fields: list[str]
    :param target_file_charset: 需要导出的文件的字符集类型
    :type target_file_charset: Charset or str
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 是否导出成功
    :rtype: bool
    """

    def func(setting):
        if config_path is not None:
            setting.setConfigFilePath(str(config_path))
        if version is not None:
            setting.setVersion(oj(VCTVersion._make(version)))

    return _export_dataset_to_file((FileType.VCT), "export_to_vct", data, output, is_over_write=is_over_write, attr_filter=attr_filter,
      is_support_datasets=True,
      ignore_fields=ignore_fields,
      target_file_charset=target_file_charset,
      progress=progress,
      custom_setting_func=func)


def export_to_kml(data, output, is_over_write=False, attr_filter=None, ignore_fields=None, target_file_charset=None, progress=None):
    """
    导出数据集到 KML 文件中

    :param data: 被导出的数据集集合
    :type data: DatasetVector or str or list[DatasetVector] or list[str]
    :param str output: 结果文件路径
    :param bool is_over_write: 导出目录中存在同名文件时，是否强制覆盖。默认为 False
    :param str attr_filter: 导出目标文件的过滤信息
    :param ignore_fields:  需要忽略的字段
    :type ignore_fields: list[str]
    :param target_file_charset: 需要导出的文件的字符集类型
    :type target_file_charset: Charset or str
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 是否导出成功
    :rtype: bool
    """
    return _export_dataset_to_file((FileType.KML), "export_to_kml", data, output, is_over_write=is_over_write, attr_filter=attr_filter,
      is_support_datasets=True,
      ignore_fields=ignore_fields,
      target_file_charset=target_file_charset,
      progress=progress)


def export_to_kmz(data, output, is_over_write=False, attr_filter=None, ignore_fields=None, target_file_charset=None, progress=None):
    """
    导出数据集到 KMZ 文件中

    :param data: 被导出的数据集集合
    :type data: DatasetVector or str or list[DatasetVector] or list[str]
    :param str output: 结果文件路径
    :param bool is_over_write: 导出目录中存在同名文件时，是否强制覆盖。默认为 False
    :param str attr_filter: 导出目标文件的过滤信息
    :param ignore_fields:  需要忽略的字段
    :type ignore_fields: list[str]
    :param target_file_charset: 需要导出的文件的字符集类型
    :type target_file_charset: Charset or str
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 是否导出成功
    :rtype: bool
    """
    return _export_dataset_to_file((FileType.KMZ), "export_to_kmz", data, output, is_over_write=is_over_write, attr_filter=attr_filter,
      is_support_datasets=True,
      ignore_fields=ignore_fields,
      target_file_charset=target_file_charset,
      progress=progress)


def export_to_grd(data, output, is_over_write=False, progress=None):
    """
    导出数据集到 GRD 文件中

    :param data: 被导出的数据集
    :type data: DatasetGrid or str
    :param str output: 结果文件路径
    :param bool is_over_write: 导出目录中存在同名文件时，是否强制覆盖。默认为 False
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 是否导出成功
    :rtype: bool
    """
    return _export_dataset_to_file((FileType.GRD), "export_to_grd", data, output, is_over_write=is_over_write, progress=progress)


def export_to_img(data, output, is_over_write=False, progress=None):
    """
    导出数据集到 IMG 文件中

    :param data: 被导出的数据集
    :type data: DatasetImage or DatasetGrid or str
    :param str output: 结果文件路径
    :param bool is_over_write: 导出目录中存在同名文件时，是否强制覆盖。默认为 False
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 是否导出成功
    :rtype: bool
    """
    return _export_dataset_to_file((FileType.IMG), "export_to_img", data, output, is_over_write=is_over_write, progress=progress)


def export_to_bmp(data, output, is_over_write=False, world_file_path=None, progress=None):
    """
    导出数据集到 BMP 文件中

    :param data: 被导出的数据集
    :type data: DatasetImage or str
    :param str output: 结果文件路径
    :param bool is_over_write: 导出目录中存在同名文件时，是否强制覆盖。默认为 False
    :param str world_file_path: 导出的影像数据的坐标文件路径
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 是否导出成功
    :rtype: bool
    """

    def func(setting):
        if world_file_path is not None:
            setting.setWorldFilePath(str(world_file_path))

    return _export_dataset_to_file((FileType.BMP), "export_to_bmp", data, output, is_over_write=is_over_write, custom_setting_func=func,
      progress=progress)


def export_to_gif(data, output, is_over_write=False, world_file_path=None, progress=None):
    """
    导出数据集到 GIF 文件中

    :param data: 被导出的数据集
    :type data: DatasetImage or str
    :param str output: 结果文件路径
    :param bool is_over_write: 导出目录中存在同名文件时，是否强制覆盖。默认为 False
    :param str world_file_path: 导出的影像数据的坐标文件路径
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 是否导出成功
    :rtype: bool
    """

    def func(setting):
        if world_file_path is not None:
            setting.setWorldFilePath(str(world_file_path))

    return _export_dataset_to_file((FileType.GIF), "export_to_gif", data, output, is_over_write=is_over_write, custom_setting_func=func,
      progress=progress)


def export_to_jpg(data, output, is_over_write=False, world_file_path=None, compression=None, progress=None):
    """
    导出数据集到 JPG 文件中

    :param data: 被导出的数据集
    :type data: DatasetImage or str
    :param str output: 结果文件路径
    :param bool is_over_write: 导出目录中存在同名文件时，是否强制覆盖。默认为 False
    :param str world_file_path: 导出的影像数据的坐标文件路径
    :param int compression: 影像文件的压缩率，单位：百分比
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 是否导出成功
    :rtype: bool
    """

    def func(setting):
        if world_file_path is not None:
            setting.setWorldFilePath(str(world_file_path))
        if compression is not None:
            setting.setCompression(int(compression))

    return _export_dataset_to_file((FileType.JPG), "export_to_jpg", data, output, is_over_write=is_over_write, custom_setting_func=func,
      progress=progress)


def export_to_png(data, output, is_over_write=False, world_file_path=None, progress=None):
    """
    导出数据集到 PNG 文件中

    :param data: 被导出的数据集
    :type data: DatasetImage or str
    :param str output: 结果文件路径
    :param bool is_over_write: 导出目录中存在同名文件时，是否强制覆盖。默认为 False
    :param str world_file_path: 导出的影像数据的坐标文件路径
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 是否导出成功
    :rtype: bool
    """

    def func(setting):
        if world_file_path is not None:
            setting.setWorldFilePath(str(world_file_path))

    return _export_dataset_to_file((FileType.PNG), "export_to_png", data, output, is_over_write=is_over_write, custom_setting_func=func,
      progress=progress)


def export_to_sit(data, output, is_over_write=False, password=None, progress=None):
    """
    导出数据集到 SIT 文件中

    :param data: 被导出的数据集
    :type data: DatasetImage or str
    :param str output: 结果文件路径
    :param bool is_over_write: 导出目录中存在同名文件时，是否强制覆盖。默认为 False
    :param str password: 密码
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 是否导出成功
    :rtype: bool
    """

    def func(setting):
        if password is not None:
            setting.setPassword(str(password))

    return _export_dataset_to_file((FileType.SIT), "export_to_sit", data, output, is_over_write=is_over_write, custom_setting_func=func,
      progress=progress)


def export_to_tif(data, output, is_over_write=False, export_as_tile=False, export_transform_file=True, progress=None):
    """
    导出数据集到 TIF 文件中
    
    :param data: 被导出的数据集
    :type data: DatasetImage or DatasetGrid or str
    :param str output: 结果文件路径
    :param bool is_over_write: 导出目录中存在同名文件时，是否强制覆盖。默认为 False
    :param bool export_as_tile: 是否以块的方式导出，默认为 False
    :param bool export_transform_file: 是否将仿射转换信息导出外部文件，默认为 True，即导出到外部的 tfw 文件中，否则投影信息会导出到 tiff 文件中
    :param function progress: 进度信息处理函数，请参考 :py:class:`.StepEvent`
    :return: 是否导出成功
    :rtype: bool
    """

    def func(setting):
        if export_as_tile is not None:
            setting.setExportAsTile(bool(export_as_tile))
        if export_transform_file is not None:
            setting.setExportingGeoTransformFile(bool(export_transform_file))

    return _export_dataset_to_file((FileType.TIF), "export_to_tif", data, output, is_over_write=is_over_write, custom_setting_func=func,
      progress=progress)

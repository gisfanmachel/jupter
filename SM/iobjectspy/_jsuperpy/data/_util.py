# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/_jsuperpy\data\_util.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 23009 bytes
import datetime, os
from collections import OrderedDict
from .._gateway import get_jvm, get_gateway
from .._utils import java_date_to_datetime, parse_bool, get_datetime_str, datetime_to_java_date
from ..enums import *
from ..env import is_auto_close_output_datasource

def get_input_dataset(value):
    if value is None:
        return
        from .dt import Dataset
        if isinstance(value, str):
            _value = value.replace("\\", "/")
            try:
                _index = _value.rindex("|")
            except:
                try:
                    _index = _value.rindex("/")
                except:
                    _index = -1

            if _index < 0:
                return value
        else:
            from .ws import Workspace
            _ds_info = _value[None[:_index]]
            if _ds_info.find("\\") >= 0 or _ds_info.find("/") >= 0 or _ds_info.find(":") >= 0:
                ds = Workspace().open_datasource(_ds_info, True)
                if ds is not None:
                    return ds[_value[(_index + 1)[:None]]]
                    return
                else:
                    pass
            alias = _value[None[:_index]]
            ds = Workspace().get_datasource(alias)
            if ds is not None:
                dt_name = value[(_index + 1)[:None]]
                return ds[dt_name]
            return
    else:
        if isinstance(value, Dataset):
            return value
        return value


def create_result_datasaet(datasource, name, dataset_type, dataset_from=None):
    if datasource is None:
        raise ValueError("datasource is None")
    elif name is None:
        raise ValueError("name is None")
    from .dt import Dataset, DatasetVectorInfo
    if dataset_type is not None:
        _datasetType = DatasetType._make(dataset_type)
        if _datasetType is None:
            raise ValueError("invalid dataset type")
        return datasource.create_dataset((DatasetVectorInfo(name, _datasetType)), adjust_name=True)
        if dataset_from is None:
            raise ValueError("dataset_from is None")
    else:
        _dt = get_input_dataset(dataset_from)
        if isinstance(_dt, Dataset):
            return datasource.create_dataset_from_template(name, _dt)
    raise ValueError("dataset_from must be Dataset, but now is " + str(type(dataset_from)))


def get_output_datasource(value):
    if value is None:
        return
        from .ds import Datasource, DatasourceConnectionInfo
        if isinstance(value, Datasource):
            value._set_existed()
            return value
            if isinstance(value, str):
                try:
                    if value.lower() == ":memory:":
                        return Datasource.create(":memory:")
                    if value.lower().endswith(".udb") or value.lower().endswith(".udbx"):
                        if not os.path.exists(value):
                            return Datasource.create(value)
                        conninfo = DatasourceConnectionInfo(server=value)
                    else:
                        if value.lower().endswith(".dcf"):
                            conninfo = DatasourceConnectionInfo.load_from_dcf(value)
                        else:
                            conninfo = DatasourceConnectionInfo.load_from_xml(value)
                    return Datasource.open(conninfo)
                except:
                    try:
                        from .ws import Workspace
                        ds = Workspace().get_datasource(value)
                    except:
                        ds = None

                    if ds is not None:
                        ds._set_existed()
                        return ds
                    from .ex import DatasourceOpenedFailedError
                    raise DatasourceOpenedFailedError(value)

                return
            if isinstance(value, DatasourceConnectionInfo):
                if value.type == EngineType.UDB or value.type == EngineType.UDBX:
                    if not os.path.exists(value.server):
                        return Datasource.create(value)
                    return Datasource.open(value)
        else:
            return Datasource.open(value)
    else:
        return


def check_output_datasource(ds):
    from .ds import Datasource
    from .ex import DatasourceReadOnlyError
    if not isinstance(ds, Datasource):
        raise ValueError("Output datasource required Datasource, but is " + str(type(ds)))
    if ds.is_readonly():
        raise DatasourceReadOnlyError(ds.alias)


def try_close_output_datasource(result, out_datasource):
    if not is_auto_close_output_datasource():
        if isinstance(result, (tuple, list)):
            results_new = []
            for it in result:
                if isinstance(it, str):
                    results_new.append(out_datasource[it])
                else:
                    results_new.append(it)

            if isinstance(result, tuple):
                return tuple(results_new)
            return results_new
            if isinstance(result, str):
                return out_datasource[result]
            return result
            if result is not None:
                from .dt import Dataset, Recordset
                if not out_datasource._is_existed():
                    if isinstance(result, (tuple, list)):
                        results_new = []
                        hava_recordset = False
                        for it in result:
                            if isinstance(it, Dataset):
                                results_new.append(it.name)
                            elif isinstance(it, Recordset):
                                hava_recordset = True
                            results_new.append(it)

                        if not hava_recordset:
                            out_datasource.close()
                    elif isinstance(result, tuple):
                        return tuple(results_new)
                    return results_new
                    if isinstance(result, Dataset):
                        name = result.name
                        if is_auto_close_output_datasource():
                            out_datasource.close()
                        return name
                    isinstance(result, Recordset) or out_datasource.close()
                    return result
        else:
            return result
    else:
        if not out_datasource._is_existed():
            out_datasource.close()
        return result


def create_geometry_buffer(geo, distance, prj=None, unit=None):
    buffer_param = get_jvm().com.supermap.analyst.spatialanalyst.BufferAnalystParameter()
    buffer_param.setEndType(BufferEndType.ROUND._jobject)
    buffer_param.setRadiusUnit(BufferRadiusUnit._make(unit, BufferRadiusUnit.METER)._jobject)
    buffer_param.setLeftDistance(float(distance))
    buffer_param.setRightDistance(float(distance))
    javaPrj = prj._jobject if prj is not None else None
    from .geo import Geometry
    return Geometry._from_java_object(get_jvm().com.supermap.analyst.spatialanalyst.BufferAnalystGeometry.createBuffer(geo._jobject, buffer_param, javaPrj))


def get_dataset_type_from_geometry_type(gtype):
    _types = {(GeometryType.GEOPOINT): (DatasetType.POINT), 
     (GeometryType.GEOLINE): (DatasetType.LINE), 
     (GeometryType.GEOREGION): (DatasetType.REGION), 
     (GeometryType.GEOTEXT): (DatasetType.TEXT), 
     (GeometryType.GEOPOINT3D): (DatasetType.POINT3D), 
     (GeometryType.GEOLINE3D): (DatasetType.LINE3D), 
     (GeometryType.GEOREGION3D): (DatasetType.REGION3D)}
    if gtype in _types.keys():
        return _types[gtype]
    return DatasetType.CAD


def from_value_get_field_type(value):
    if value is None:
        return FieldType.WTEXT
    if isinstance(value, bool):
        return FieldType.BOOLEAN
    if isinstance(value, int):
        return FieldType.INT64
    if isinstance(value, str):
        return FieldType.WTEXT
    if isinstance(value, float):
        return FieldType.DOUBLE
    if isinstance(value, bool):
        return FieldType.BOOLEAN
    if isinstance(value, datetime.datetime):
        return FieldType.DATETIME
    if isinstance(value, (bytearray, bytes)):
        return FieldType.LONGBINARY
    return FieldType.WTEXT


def convert_value_to_python(value, field_type):
    if value is None:
        return value
        if field_type is None:
            raise Exception("invalid field_type")
        if field_type == FieldType.DATETIME:
            return java_date_to_datetime(value)
    elif field_type in (FieldType.INT64, FieldType.INT32, FieldType.INT16, FieldType.BYTE):
        try:
            return int(value)
        except:
            return

    else:
        if field_type in (FieldType.SINGLE, FieldType.DOUBLE):
            try:
                return float(value)
            except:
                return

        else:
            if field_type in (FieldType.WTEXT, FieldType.TEXT, FieldType.CHAR, FieldType.JSONB):
                return str(value)
            if field_type is FieldType.LONGBINARY:
                if isinstance(value, str):
                    return bytes((str(value)), encoding="utf-8")
                if isinstance(value, bytes):
                    return value
                if isinstance(value, bytearray):
                    return bytes(value)
                return
            else:
                if field_type is FieldType.BOOLEAN:
                    try:
                        return parse_bool(value)
                    except:
                        return

                else:
                    return


def field_default_value_to_java(value, field_type):
    if value is None:
        return value
        if field_type is None:
            raise Exception("invalid field_type")
        if field_type == FieldType.BOOLEAN:
            return str(bool(value))
        if field_type == FieldType.CHAR:
            return str(value)
        if field_type == FieldType.WTEXT or field_type == FieldType.TEXT:
            return str(value)
        if field_type == FieldType.BYTE:
            return str(int(value))
        if field_type == FieldType.INT16:
            return str(int(value))
        if field_type == FieldType.INT32:
            return str(int(value))
        if field_type == FieldType.INT64:
            return str(int(value))
        if field_type == FieldType.SINGLE:
            return str(float(value))
        if field_type == FieldType.DOUBLE:
            return str(float(value))
        if field_type == FieldType.JSONB:
            return str(value)
        if field_type == FieldType.LONGBINARY and not isinstance(value, bytes):
            if isinstance(value, bytearray):
                return str(value, encoding="utf8")
            return str(value)
    elif field_type == FieldType.DATETIME:
        return get_datetime_str(value)
    return


def convert_value_to_java(value, field_type):
    if value is None:
        return value
        if field_type is None:
            raise Exception("invalid field_type")
        if field_type == FieldType.BOOLEAN:
            return bool(value)
        if field_type == FieldType.CHAR:
            return str(value)
        if field_type == FieldType.WTEXT or field_type == FieldType.TEXT:
            return str(value)
        if field_type == FieldType.BYTE:
            return int(value)
        if field_type == FieldType.INT16:
            return int(value)
        if field_type == FieldType.INT32:
            return int(value)
        if field_type == FieldType.INT64:
            return int(value)
        if field_type == FieldType.SINGLE:
            return float(value)
        if field_type == FieldType.DOUBLE:
            return float(value)
        if field_type == FieldType.JSONB:
            return str(value)
        if field_type == FieldType.LONGBINARY and not isinstance(value, bytes):
            if isinstance(value, bytearray):
                return value
            return bytes((str(value)), encoding="utf-8")
    elif field_type == FieldType.DATETIME:
        return datetime_to_java_date(value)
    return


def to_java_dataset_array(values):
    if values is None:
        return
    else:
        from .dt import Dataset
        if isinstance(values, Dataset):
            java_array = get_gateway().new_array(get_jvm().com.supermap.data.Dataset, 1)
            java_array[0] = values._jobject
        else:
            if isinstance(values, (list, tuple, set)):
                _size = len(values)
                java_array = get_gateway().new_array(get_jvm().com.supermap.data.Dataset, _size)
                i = 0
                for value in values:
                    if isinstance(value, Dataset):
                        java_array[i] = value._jobject
                    else:
                        java_array[i] = value
                    i += 1

            else:
                java_array = get_gateway().new_array(get_jvm().com.supermap.data.Dataset, 1)
                java_array[0] = values
    return java_array


def to_java_datasetvector_array(values):
    if values is None:
        return
    else:
        from .dt import DatasetVector
        if isinstance(values, DatasetVector):
            java_array = get_gateway().new_array(get_jvm().com.supermap.data.DatasetVector, 1)
            java_array[0] = values._jobject
        else:
            if isinstance(values, (list, tuple, set)):
                _size = len(values)
                java_array = get_gateway().new_array(get_jvm().com.supermap.data.DatasetVector, _size)
                i = 0
                for value in values:
                    if isinstance(value, DatasetVector):
                        java_array[i] = value._jobject
                    else:
                        java_array[i] = value
                    i += 1

            else:
                java_array = get_gateway().new_array(get_jvm().com.supermap.data.DatasetVector, 1)
                java_array[0] = values
    return java_array


def to_java_datasetimage_array(values):
    if values is None:
        return
    else:
        from .dt import DatasetImage
        if isinstance(values, DatasetImage):
            java_array = get_gateway().new_array(get_jvm().com.supermap.data.DatasetImage, 1)
            java_array[0] = values._jobject
        else:
            if isinstance(values, (list, tuple, set)):
                _size = len(values)
                java_array = get_gateway().new_array(get_jvm().com.supermap.data.DatasetImage, _size)
                i = 0
                for value in values:
                    if isinstance(value, DatasetImage):
                        java_array[i] = value._jobject
                    else:
                        java_array[i] = value
                    i += 1

            else:
                java_array = get_gateway().new_array(get_jvm().com.supermap.data.DatasetImage, 1)
                java_array[0] = values
    return java_array


def to_java_recordset_array(values):
    if values is None:
        return
    else:
        from .dt import Recordset
        if isinstance(values, Recordset):
            java_array = get_gateway().new_array(get_jvm().com.supermap.data.Recordset, 1)
            java_array[0] = values._jobject
        else:
            if isinstance(values, (list, tuple, set)):
                _size = len(values)
                java_array = get_gateway().new_array(get_jvm().com.supermap.data.Recordset, _size)
                i = 0
                for value in values:
                    if isinstance(value, Recordset):
                        java_array[i] = value._jobject
                    else:
                        java_array[i] = value
                    i += 1

            else:
                java_array = get_gateway().new_array(get_jvm().com.supermap.data.Recordset, 1)
                java_array[0] = values
    return java_array


def to_java_datasetgrid_array(values):
    if values is None:
        return
    else:
        from .dt import DatasetGrid
        if isinstance(values, DatasetGrid):
            java_array = get_gateway().new_array(get_jvm().com.supermap.data.DatasetGrid, 1)
            java_array[0] = values._jobject
        else:
            if isinstance(values, (list, tuple, set)):
                _size = len(values)
                java_array = get_gateway().new_array(get_jvm().com.supermap.data.DatasetGrid, _size)
                i = 0
                for value in values:
                    if isinstance(value, DatasetGrid):
                        java_array[i] = value._jobject
                    else:
                        java_array[i] = value
                    i += 1

            else:
                java_array = get_gateway().new_array(get_jvm().com.supermap.data.DatasetGrid, 1)
                java_array[0] = values
    return java_array


def to_java_datasetvector_array(values):
    if values is None:
        return
    else:
        from .dt import DatasetVector
        if isinstance(values, DatasetVector):
            java_array = get_gateway().new_array(get_jvm().com.supermap.data.DatasetVector, 1)
            java_array[0] = values._jobject
        else:
            if isinstance(values, (list, tuple, set)):
                _size = len(values)
                java_array = get_gateway().new_array(get_jvm().com.supermap.data.DatasetVector, _size)
                i = 0
                for value in values:
                    if isinstance(value, DatasetVector):
                        java_array[i] = value._jobject
                    else:
                        java_array[i] = value
                    i += 1

            else:
                java_array = get_gateway().new_array(get_jvm().com.supermap.data.DatasetVector, 1)
                java_array[0] = values
    return java_array


def to_java_geometry_array(values):
    if values is None:
        return
    else:
        from .geo import Geometry
        if isinstance(values, Geometry):
            java_array = get_gateway().new_array(get_jvm().com.supermap.data.Geometry, 1)
            java_array[0] = values._jobject
        else:
            if isinstance(values, (list, tuple, set)):
                _size = len(values)
                java_array = get_gateway().new_array(get_jvm().com.supermap.data.Geometry, _size)
                i = 0
                for value in values:
                    if isinstance(value, Geometry):
                        java_array[i] = value._jobject
                    i += 1

            else:
                java_array = None
    return java_array


def to_java_geoline_array(values):
    if values is None:
        return
    else:
        from .geo import GeoLine
        if isinstance(values, GeoLine):
            java_array = get_gateway().new_array(get_jvm().com.supermap.data.GeoLine, 1)
            java_array[0] = values._jobject
        else:
            if isinstance(values, (list, tuple, set)):
                _size = len(values)
                java_array = get_gateway().new_array(get_jvm().com.supermap.data.GeoLine, _size)
                i = 0
                for value in values:
                    if isinstance(value, GeoLine):
                        java_array[i] = value._jobject
                    i += 1

            else:
                java_array = None
    return java_array


def to_java_stattype_array(values):
    if values is None:
        return
        jvm = get_jvm()
        if isinstance(values, StatisticsType):
            java_array = get_gateway().new_array(jvm.com.supermap.analyst.spatialanalyst.StatisticsType, 1)
            java_array[0] = values._jobject
            return java_array
        if isinstance(values, (list, tuple, set)):
            _size = len(values)
            java_array = get_gateway().new_array(jvm.com.supermap.analyst.spatialanalyst.StatisticsType, _size)
            i = 0
            for value in values:
                if isinstance(value, StatisticsType):
                    java_array[i] = value._jobject
                else:
                    if isinstance(value, (str, int)):
                        v = StatisticsType._make(value)
                        if v is not None:
                            java_array[i] = v._jobject
                    else:
                        java_array[i] = value
                i += 1

            return java_array
        java_array = get_gateway().new_array(jvm.com.supermap.analyst.spatialanalyst.StatisticsType, 1)
        if isinstance(values, (str, int)):
            v = StatisticsType._make(values)
            if v is not None:
                java_array[0] = v._jobject
    else:
        java_array[0] = values
    return java_array


def to_java_point2ds(values):
    if values is None:
        return
    from .geo import Point2D, GeoPoint
    jvm = get_jvm()
    if isinstance(values, Point2D):
        points = jvm.com.supermap.data.Point2Ds()
        points.add(values._jobject)
        return points
    if isinstance(values, GeoPoint):
        points = jvm.com.supermap.data.Point2Ds()
        points.add(values.point._jobject)
        return points
    if isinstance(values, (list, tuple)):
        points = jvm.com.supermap.data.Point2Ds()
        for p in values:
            if isinstance(p, Point2D):
                points.add(p._jobject)

        return points
    return


def to_java_point3ds(values):
    if values is None:
        return
    from .geo import Point3D, GeoPoint3D
    jvm = get_jvm()
    if isinstance(values, Point3D):
        points = jvm.com.supermap.data.Point3Ds()
        points.add(values._jobject)
        return points
    if isinstance(values, GeoPoint3D):
        points = jvm.com.supermap.data.Point3Ds()
        points.add(values.point._jobject)
        return points
    if isinstance(values, (list, tuple)):
        points = jvm.com.supermap.data.Point3Ds()
        for p in values:
            if isinstance(p, Point3D):
                points.add(p._jobject)

        return points
    return


def to_java_point2d_array(values):
    if values is None:
        return
    from .geo import Point2D, GeoPoint
    if isinstance(values, Point2D):
        java_array = get_gateway().new_array(get_jvm().com.supermap.data.Point2D, 1)
        java_array[0] = values._jobject
        return java_array
    if isinstance(values, (list, tuple, set)):
        _size = len(values)
        java_array = get_gateway().new_array(get_jvm().com.supermap.data.Point2D, _size)
        i = 0
        for value in values:
            java_array[i] = value._jobject
            i += 1

        return java_array
    return


def java_field_infos_to_map(java_fieldinfos):
    from .geo import FieldInfo
    fields = OrderedDict()
    for i in range(java_fieldinfos.getCount()):
        field = FieldInfo._from_java_object(java_fieldinfos.get(i))
        fields[field.name] = field

    return fields


def java_field_infos_to_list(java_fieldinfos):
    from .geo import FieldInfo
    fields = []
    for i in range(java_fieldinfos.getCount()):
        fields.append(FieldInfo._from_java_object(java_fieldinfos.get(i)))

    return fields


def java_point2ds_to_list(java_points):
    from .geo import Point2D
    points = []
    for i in range(java_points.getCount()):
        points.append(Point2D._from_java_object(java_points.getItem(i)))

    return points

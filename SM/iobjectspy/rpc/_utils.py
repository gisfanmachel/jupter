# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/rpc\_utils.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 13126 bytes
from iobjectspy.rpc.protos.tileMessages_pb2 import ProtoTile
from iobjectspy.rpc.protos.rectMessages_pb2 import ProtoRect
from iobjectspy.rpc.protos.featureMessages_pb2 import ProtoFieldInfo, ProtoFeature, ProtoGeometry
from iobjectspy.rpc.protos.processInfoMessage_pb2 import ProtoProcessInfo
import numpy as np
from iobjectspy.enums import FieldType, GeometryType, PixelFormat
from iobjectspy.data import Geometry, Feature, FieldInfo, GeoPoint, GeoLine, GeoRegion, Point2D
import struct
from iobjectspy._logger import *
from .process import Tile, ProcessInfo

def pixel_to_numpy_dtype(pixel):
    _pixel_to_numpy = {
     1: '"b"', 
     4: '"b"', 
     8: '"B"', 
     160: '"uint16"', 
     321: '"uint32"', 
     80: '"b"', 
     16: '"int16"', 
     320: '"int32"', 
     64: '"int64"', 
     24: '"uint8"', 
     32: '"uint8"', 
     6400: '"float64"', 
     3200: '"float32"'}
    return _pixel_to_numpy[pixel]


def get_pixel_from_numpy_dtype(dtype):
    _numpy_to_pixel = {(np.bool_): (PixelFormat.UBIT1), 
     (np.byte): (PixelFormat.BIT8), 
     (np.int8): (PixelFormat.BIT8), 
     (np.short): (PixelFormat.BIT16), 
     (np.int32): (PixelFormat.BIT32), 
     (np.int64): (PixelFormat.BIT64), 
     (np.longlong): (PixelFormat.BIT64), 
     (np.ubyte): (PixelFormat.UBIT8), 
     (np.uint8): (PixelFormat.UBIT8), 
     (np.ushort): (PixelFormat.UBIT16), 
     (np.uint32): (PixelFormat.UBIT32), 
     (np.single): (PixelFormat.SINGLE), 
     (np.double): (PixelFormat.DOUBLE), 
     (np.float16): (PixelFormat.SINGLE), 
     (np.float32): (PixelFormat.DOUBLE)}
    return _numpy_to_pixel[dtype.type]


def decode_tile(bys):
    proto_tile = ProtoTile.FromString(bys)
    no_data_value = proto_tile.noValue
    pixel = proto_tile.pixelFormat
    bands = proto_tile.bands
    cells = np.array(proto_tile.values[None[:None]]).astype(pixel_to_numpy_dtype(pixel))
    if bands > 1:
        return Tile(cells.reshape(bands, proto_tile.rows, proto_tile.cols), no_data_value, bands, pixel)
    return Tile(cells.reshape(proto_tile.rows, proto_tile.cols), no_data_value, 1, pixel)


def encode_tile(obj):
    """

    :param obj: 需要进行序列化的 Tile 对象
    :type obj: Tile
    :return: 序列化的 ProtoBuf 字符串
    :rtype: str
    """
    cells = obj.values
    no_data_value = obj.no_data_value
    bands = obj.bands
    pixel = get_pixel_from_numpy_dtype(cells.dtype)
    if len(cells.shape) > 2:
        _, rows, cols = cells.shape
    else:
        rows, cols = cells.shape
    tile = ProtoTile()
    tile.cols = cols
    tile.rows = rows
    tile.noValue = no_data_value
    tile.pixelFormat = pixel
    tile.bands = bands
    tile.values.extend(cells.flatten().tolist())
    return tile.SerializeToString()


def decode_rect(bys):
    proto_rect = ProtoRect.FromString(bys)
    from iobjectspy.data import Rectangle
    return Rectangle(proto_rect.minx, proto_rect.maxy, proto_rect.maxx, proto_rect.miny)


def encode_rect(rect):
    proto_rect = ProtoRect()
    proto_rect.minx = rect.left
    proto_rect.miny = rect.bottom
    proto_rect.maxx = rect.right
    proto_rect.maxy = rect.top
    return proto_rect.SerializeToString()


def decode_geometry(bys):
    if isinstance(bys, ProtoGeometry):
        from iobjectspy.enums import GeometryType
        geo_type = GeometryType.make(bys.geotype)
        parts = bys.parts
        xys = bys.points
        points = []
        index = 0
        for part in parts:
            part_points = []
            for i in range(abs(part)):
                part_points.append(Point2D(xys[index], xys[index + 1]))
                index += 2

            points.append(part_points)

        if geo_type is GeometryType.GEOPOINT:
            geo = GeoPoint(points[points[0]])
        else:
            if geo_type is GeometryType.GEOLINE:
                geo = GeoLine()
                for part_points in points:
                    geo.add_part(part_points)

            else:
                if geo_type is GeometryType.GEOREGION:
                    geo = GeoRegion()
                    for part_points in points:
                        geo.add_part(part_points)

                else:
                    geo = None
        return geo
    return Geometry._from_pb_bytes(bys)


def encode_geometry(geo):
    if geo is None:
        return
    return geo._to_pb_bytes()


def encode_proto_geometry(geo, proto_geo):
    """

    :param geo:
    :type geo: iobjectspy.Geometry
    :return:
    :rtype:
    """
    if geo is None:
        return
    else:
        proto_geo.geotype = geo.type.value
        if geo.type is GeometryType.GEOPOINT:
            parts = [
             1]
            points = [geo.get_x(), geo.get_y()]
        else:
            if geo.type is GeometryType.GEOLINE or geo.type is GeometryType.GEOREGION:
                all_points = geo.get_parts()
                parts = []
                points = []
                for pts in all_points:
                    parts.append(len(pts))
                    for p in pts:
                        points.append(p.x)
                        points.append(p.y)

            else:
                raise RuntimeError("Unsupported geometry type " + geo.type.name)
    proto_geo.parts.extend(parts)
    proto_geo.points.extend(points)
    return proto_geo


def decode_field_info(bys):
    if isinstance(bys, ProtoFieldInfo):
        proto_field = bys
    else:
        proto_field = ProtoFieldInfo.FromString(bys)
    from iobjectspy.data import FieldInfo
    field_info = FieldInfo()
    field_info.set_name(proto_field.name)
    field_info.set_type(proto_field.fieldType)
    if proto_field.caption is not None:
        field_info.set_caption(proto_field.caption)
    if proto_field.maxLength is not None:
        field_info.set_max_length(proto_field.maxLength)
    if proto_field.isRequired is not None:
        field_info.set_required(proto_field.isRequired)
    if proto_field.isZeroLengthAllowed is not None:
        field_info.set_zero_length_allowed(proto_field.isZeroLengthAllowed)
    if proto_field.defaultValue is not None:
        from _jsuperpy.data._util import convert_value_to_python
        field_info.set_default_value(convert_value_to_python(proto_field.defaultValue, field_info.type))
    return field_info


def encode_field_info(field_info):
    """

    :param field_info:
    :type field_info: FieldInfo
    :return:
    :rtype:
    """
    return encode_proto_field_info(field_info).SerializeToString()


def encode_proto_field_info(field_info):
    proto_field_info = ProtoFieldInfo()
    proto_field_info.name = field_info.name
    proto_field_info.fieldType = field_info.type.value
    proto_field_info.caption = field_info.caption
    proto_field_info.maxLength = field_info.max_length
    proto_field_info.isRequired = field_info.is_required
    proto_field_info.isZeroLengthAllowed = field_info.is_zero_length_allowed
    proto_field_info.defaultValue = encode_field_default_value_to_pb(field_info.default_value, field_info.type)
    return proto_field_info


def decode_feature(bys):
    proto_feature = ProtoFeature.FromString(bys)
    proto_geometry = proto_feature.geometry
    if proto_geometry is not None:
        geo = decode_geometry(proto_geometry)
    else:
        geo = None
    proto_fields = proto_feature.fieldInfos
    fields = []
    for proto_field in proto_fields:
        fields.append(decode_field_info(proto_field))

    proto_values = proto_feature.values
    values = []
    from _jsuperpy.data._util import convert_value_to_python
    if len(proto_values) == len(fields):
        for i in range(len(fields)):
            values.append(convert_value_to_python(proto_values[i], fields[i].type))

    else:
        for i in range(len(fields)):
            values.append(None)

    id = proto_feature.fid
    return Feature(geo, values, field_infos=fields, id_value=id)


def encode_feature(feature):
    """
    :param feature:
    :type feature: iobjectspy.Feature
    :return:
    :rtype:
    """
    proto_feature = ProtoFeature()
    geo = feature.geometry
    if geo is not None:
        encode_proto_geometry(geo, proto_feature.geometry)
    fields = feature.field_infos
    if fields is not None:
        if len(fields) > 0:
            proto_field_infos = []
            proto_values = []
            values = feature.get_values(exclude_system=False)
            for i in range(len(fields)):
                proto_field_infos.append(encode_proto_field_info(fields[i]))
                proto_values.append(encode_field_value_to_pb(values[i], fields[i].type))

            proto_feature.fieldInfos.extend(proto_field_infos)
            proto_feature.values.extend(proto_values)
    proto_feature.fid = feature.feature_id
    return proto_feature.SerializeToString()


def encode_field_default_value_to_pb(value, field_type):
    if value is None:
        return ""
        if field_type is None:
            raise Exception("invalid field_type")
        if field_type is FieldType.BOOLEAN:
            return str(bool(value))
        if field_type is FieldType.CHAR:
            return str(value)
        if field_type is FieldType.WTEXT or field_type == FieldType.TEXT:
            return str(value)
        if field_type is FieldType.BYTE:
            return str(int(value))
        if field_type is FieldType.INT16:
            return str(int(value))
        if field_type is FieldType.INT32:
            return str(int(value))
        if field_type is FieldType.INT64:
            return str(int(value))
        if field_type is FieldType.SINGLE:
            return str(float(value))
        if field_type is FieldType.DOUBLE:
            return str(float(value))
        if field_type is FieldType.JSONB:
            return str(value)
        if field_type is FieldType.LONGBINARY and not isinstance(value, bytes):
            if isinstance(value, bytearray):
                return str(value, encoding="utf8")
            return str(value)
    elif field_type == FieldType.DATETIME:
        from _jsuperpy._utils import get_datetime_str
        return get_datetime_str(value)
    log_warning("invalid field type " + str(field_type))
    return ""


def encode_field_value_to_pb(value, field_type):
    if value is None:
        return b''
        if field_type is None:
            raise Exception("invalid field_type")
        if field_type is FieldType.BOOLEAN:
            if value:
                return "true".encode()
            return "false".encode()
    elif field_type is FieldType.CHAR:
        return str(value).encode()
        if field_type is FieldType.WTEXT or field_type == FieldType.TEXT:
            return str(value).encode()
        if field_type is FieldType.BYTE:
            return struct.pack("!i", int(value))
        if field_type is FieldType.INT16:
            return struct.pack("!h", int(value))
        if field_type is FieldType.INT32:
            return struct.pack("!i", int(value))
        if field_type is FieldType.INT64:
            return struct.pack("!q", int(value))
        if field_type is FieldType.SINGLE:
            return struct.pack("!f", float(value))
        if field_type is FieldType.DOUBLE:
            return struct.pack("!d", float(value))
        if field_type is FieldType.JSONB:
            return str(value).encode()
        if field_type is FieldType.LONGBINARY and not isinstance(value, bytes):
            if isinstance(value, bytearray):
                return bytes(value)
            return bytes((str(value)), encoding="utf-8")
    elif field_type is FieldType.DATETIME:
        from _jsuperpy._utils import get_datetime_str
        return get_datetime_str(value).encode()
    log_warning("invalid field type " + str(field_type))
    return b''


def decode_process_info(bys):
    proto_process_info = ProtoProcessInfo.FromString(bys)
    kvargs = proto_process_info.kvargs
    args = dict()
    from .serializes import DataSerializers
    for name, value_bys in kvargs.items():
        args[name] = DataSerializers.deserialize(value_bys)

    return ProcessInfo(proto_process_info.pyCode, proto_process_info.pyEntryClass, args)


def encode_process_info(process_info):
    proto_process_info = ProtoProcessInfo()
    proto_process_info.pyCode = process_info.py_code
    proto_process_info.pyEntryClass = process_info.entry_class
    from .serializes import DataSerializers
    if process_info.kvargs is not None:
        for name, value in process_info.kvargs.items():
            proto_process_info.kvargs[name] = DataSerializers.serialize(value)

    return proto_process_info.SerializeToString()


def read_int(stream):
    length = stream.read(4)
    if not length:
        raise EOFError
    return struct.unpack("!i", length)[0]


def write_int(value, stream):
    stream.write(struct.pack("!i", value))
    stream.flush()


def read_length_and_bytes(stream):
    return stream.read(read_int(stream))


def write_length_and_bytes(bys, stream):
    if bys is not None:
        write_int(len(bys), stream)
        stream.write(bys)
        stream.flush()

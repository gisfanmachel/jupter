# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/rpc\serializes.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 32890 bytes
import datetime, struct
from io import BytesIO
import iobjectspy
from iobjectspy.rpc.process import Tile, ProcessInfo

class DataSerializer:

    def get_value_class(self):
        pass

    def get_type_name(self):
        pass

    def encode(self, value):
        pass

    def decode(self, bys):
        pass

    @staticmethod
    def serialize_null():
        return bytes("!n;", "utf-8")

    def serialize(self, value):
        if value is None:
            return DataSerializer.serialize_null()
        type_name = self.get_type_name()
        return bytes("!" + type_name + ";", "utf-8") + self.encode(value)

    @classmethod
    def deserialize(cls, bys):
        if bys is None or len(bys) == 0:
            return
        if isinstance(bys, str):
            bys = bytes(bys, "utf-8")
        if isinstance(bys, (bytes, bytearray)):
            try:
                start_pos = bys.index(b'!')
                pos = bys.index(b';')
            except ValueError:
                pos = -1
                start_pos = -1

            if start_pos != 0 or pos == -1:
                raise ValueError("invalid input bytes, cannot find valid type name")
            type_name = str(bys[1[:pos]], "utf-8")
            ser = DataSerializers.find(type_name)
            return ser.decode(bys[(pos + 1)[:len(bys)]])
        return


class NoneSerializer(DataSerializer):

    def get_value_class(self):
        pass

    def get_type_name(self):
        return "n"

    def encode(self, value):
        pass

    def decode(self, bys):
        pass


class BoolSerializer(DataSerializer):

    def get_value_class(self):
        return bool

    def get_type_name(self):
        return "b"

    def encode(self, value):
        if value:
            return bytes("true", "utf-8")
        return bytes("false", "utf-8")

    def decode(self, bys):
        value = str(bys, "utf-8")
        if value == "true":
            return True
        return False


class BoolsSerializer(DataSerializer):

    def get_value_class(self):
        return list

    def get_type_name(self):
        return "bL"

    def encode(self, value):
        if isinstance(value, (list, tuple)):

            def f(item):
                if isinstance(item, bool):
                    return 1
                return 0

            bool_values = list(filter((lambda x: isinstance(x, bool)), value))
            items = [f(item) for item in bool_values]
            return bytes(items)
        return

    def decode(self, bys):
        if isinstance(bys, (bytes, bytearray)):
            return [bool(item) for item in bys]
        return


class ByteSerializer(DataSerializer):

    def get_value_class(self):
        return int

    def get_type_name(self):
        return "B"

    def encode(self, value):
        if isinstance(value, int):
            struct.pack("!i", value)
        else:
            return

    def decode(self, bys):
        if isinstance(bys, (bytes, bytearray)):
            return struct.pack("!i", bys)[0]
        return


class BytesSerializer(DataSerializer):

    def get_value_class(self):
        return bytes

    def get_type_name(self):
        return "BL"

    def encode(self, value):
        if isinstance(value, (bytes, bytearray)):
            return bytes(value)
        if isinstance(value, str):
            return bytes(value, "utf-8")
        return

    def decode(self, bys):
        if isinstance(bys, (bytes, bytearray)):
            return bytes(bys)
        if isinstance(bys, str):
            return bytes(bys, "utf-8")
        return


class IntSerializer(DataSerializer):

    def get_value_class(self):
        return int

    def get_type_name(self):
        return "i"

    def encode(self, value):
        if isinstance(value, int):
            return struct.pack("!i", value)
        return

    def decode(self, bys):
        if isinstance(bys, (bytes, bytearray)):
            return struct.unpack("!i", bys)[0]
        return


class IntsSerializer(DataSerializer):

    def get_value_class(self):
        return list

    def get_type_name(self):
        return "iL"

    def encode(self, value):
        if isinstance(value, (list, tuple)):
            int_values = list(filter((lambda x: isinstance(x, int)), value))
            if len(int_values) > 0:
                stream = BytesIO()
                for v in int_values:
                    stream.write(struct.pack("!i", v))

                return stream.getvalue()
            return
        else:
            return

    def decode(self, bys):
        if isinstance(bys, (bytes, bytearray)):
            stream = BytesIO(bys)
            item = stream.read(4)
            result = []
            while len(item) == 4:
                result.append(struct.unpack("!i", item)[0])
                item = stream.read(4)

            return result
        return


class LongSerializer(DataSerializer):

    def get_value_class(self):
        return int

    def get_type_name(self):
        return "l"

    def encode(self, value):
        if isinstance(value, int):
            return struct.pack("!q", value)
        return

    def decode(self, bys):
        if isinstance(bys, (bytes, bytearray)):
            return struct.unpack("!q", bys)[0]
        return


class LongsSerializer(DataSerializer):

    def get_value_class(self):
        return list

    def get_type_name(self):
        return "lL"

    def encode(self, value):
        if isinstance(value, (list, tuple)):
            int_values = list(filter((lambda x: isinstance(x, int)), value))
            if len(int_values) > 0:
                stream = BytesIO()
                for v in int_values:
                    stream.write(struct.pack("!q", v))

                return stream.getvalue()
            return
        else:
            return

    def decode(self, bys):
        if isinstance(bys, (bytes, bytearray)):
            stream = BytesIO(bys)
            item = stream.read(8)
            result = []
            while len(item) == 8:
                result.append(struct.unpack("!q", item)[0])
                item = stream.read(8)

            return result
        return


class ShortsSerializer(DataSerializer):

    def get_value_class(self):
        return list

    def get_type_name(self):
        return "sL"

    def encode(self, value):
        if isinstance(value, (list, tuple)):
            int_values = list(filter((lambda x: isinstance(x, int)), value))
            if len(int_values) > 0:
                stream = BytesIO()
                for v in int_values:
                    stream.write(struct.pack("!h", v))

                return stream.getvalue()
            return
        else:
            return

    def decode(self, bys):
        if isinstance(bys, (bytes, bytearray)):
            stream = BytesIO(bys)
            item = stream.read(2)
            result = []
            while len(item) == 2:
                result.append(struct.unpack("!h", item)[0])
                item = stream.read(2)

            return result
        return


class ShortSerializer(DataSerializer):

    def get_value_class(self):
        return int

    def get_type_name(self):
        return "s"

    def encode(self, value):
        if isinstance(value, int):
            return struct.pack("!h", value)
        return

    def decode(self, bys):
        if isinstance(bys, (bytes, bytearray)):
            return struct.unpack("!h", bys)[0]
        return


class DoubleSerializer(DataSerializer):

    def get_value_class(self):
        return float

    def get_type_name(self):
        return "d"

    def encode(self, value):
        if isinstance(value, float):
            return struct.pack("!d", value)
        return

    def decode(self, bys):
        if isinstance(bys, (bytes, bytearray)):
            return struct.unpack("!d", bys)[0]
        return


class DoublesSerializer(DataSerializer):

    def get_value_class(self):
        return list

    def get_type_name(self):
        return "dL"

    def encode(self, value):
        if isinstance(value, (list, tuple)):
            double_values = list(filter((lambda x: isinstance(x, float)), value))
            if len(double_values) > 0:
                stream = BytesIO()
                for v in double_values:
                    stream.write(struct.pack("!d", v))

                return stream.getvalue()
            return
        else:
            return

    def decode(self, bys):
        if isinstance(bys, (bytes, bytearray)):
            stream = BytesIO(bys)
            item = stream.read(8)
            result = []
            while len(item) == 8:
                result.append(struct.unpack("!d", item)[0])
                item = stream.read(8)

            return result
        return


class FloatSerializer(DataSerializer):

    def get_value_class(self):
        return float

    def get_type_name(self):
        return "f"

    def encode(self, value):
        if isinstance(value, float):
            return struct.pack("!f", value)
        return

    def decode(self, bys):
        if isinstance(bys, (bytes, bytearray)):
            return struct.unpack("!f", bys)[0]
        return


class FloatsSerializer(DataSerializer):

    def get_value_class(self):
        return list

    def get_type_name(self):
        return "fL"

    def encode(self, value):
        if isinstance(value, (list, tuple)):
            double_values = list(filter((lambda x: isinstance(x, float)), value))
            if len(double_values) > 0:
                stream = BytesIO()
                for v in double_values:
                    stream.write(struct.pack("!f", v))

                return stream.getvalue()
            return
        else:
            return

    def decode(self, bys):
        if isinstance(bys, (bytes, bytearray)):
            stream = BytesIO(bys)
            item = stream.read(4)
            result = []
            while len(item) == 4:
                result.append(struct.unpack("!f", item)[0])
                item = stream.read(8)

            return result
        return


class StrSerializer(DataSerializer):

    def get_value_class(self):
        return str

    def get_type_name(self):
        return "S"

    def encode(self, value):
        if isinstance(value, str):
            return bytes(value, "utf-8")
        if isinstance(value, (bytes, bytearray)):
            return bytes(value)
        return

    def decode(self, bys):
        if isinstance(bys, (bytes, bytearray)):
            return str(bys, "utf-8")
        if isinstance(bys, str):
            return bys
        return


class StrsSerializer(DataSerializer):

    def get_value_class(self):
        return list

    def get_type_name(self):
        return "SL"

    def encode(self, value):
        if isinstance(value, (list, tuple)):
            stream = BytesIO()

            def f(item):
                if isinstance(item, str):
                    bs = bytes(item, "utf-8")
                    c = len(bs)
                    stream.write(struct.pack("!i", c))
                    stream.write(bs)
                else:
                    if isinstance(item, (bytes, bytearray)):
                        bs = bytes(item)
                        c = len(bs)
                        stream.write(struct.pack("!i", c))
                        stream.write(bs)
                    else:
                        return

            for v in value:
                f(v)

            return stream.getvalue()
        return

    def decode(self, bys):
        if isinstance(bys, (bytes, bytearray)):
            stream = BytesIO(bys)
            item_len_bs = stream.read(4)
            result = []
            while len(item_len_bs) == 4:
                item_len = struct.unpack("!i", item_len_bs)[0]
                item_bs = stream.read(item_len)
                result.append(str(item_bs, "utf-8"))
                item_len_bs = stream.read(4)

            return result
        return


class DateSerializer(DataSerializer):

    def get_value_class(self):
        return datetime.datetime

    def get_type_name(self):
        return "D"

    def encode(self, value):
        if isinstance(value, datetime.datetime):
            return bytes(value.strftime("%Y-%m-%d %H:%M:%S"), "utf-8")
        return

    def decode(self, bys):
        if isinstance(bys, (bytes, bytearray)):
            return datetime.datetime.strptime(str(bys, "utf-8"), "%Y-%m-%d %H:%M:%S")
        return


class TimestampSerializer(DataSerializer):

    def get_value_class(self):
        return datetime.datetime

    def get_type_name(self):
        return "T"

    def encode(self, value):
        if isinstance(value, datetime.datetime):
            return struct.pack("!q", value.timestamp())
        return

    def decode(self, bys):
        if isinstance(bys, (bytes, bytearray)):
            return datetime.datetime.fromtimestamp(struct.unpack("!q", bys)[0])
        return


class FieldInfoSerializer(DataSerializer):

    def get_value_class(self):
        return iobjectspy.FieldInfo

    def get_type_name(self):
        return "FI"

    def encode(self, value):
        if isinstance(value, iobjectspy.FieldInfo):
            from iobjectspy.rpc._utils import encode_field_info
            return encode_field_info(value)
        return

    def decode(self, bys):
        if isinstance(bys, (bytes, bytearray)):
            from iobjectspy.rpc._utils import decode_field_info
            return decode_field_info(bytes(bys))
        return


class Point2DSerializer(DataSerializer):

    def get_value_class(self):
        return iobjectspy.Point2D

    def get_type_name(self):
        return "P2"

    def encode(self, value):
        import iobjectspy
        if isinstance(value, iobjectspy.Point2D):
            return struct.pack("!d", value.x) + struct.pack("!d", value.y)
        return

    def decode(self, bys):
        if isinstance(bys, (bytes, bytearray)):
            x = struct.unpack("!d", bys[0[:8]])[0]
            y = struct.unpack("!d", bys[8[:16]])[0]
            import iobjectspy
            return iobjectspy.Point2D(x, y)
        return


class Point2DsSerializer(DataSerializer):

    def get_value_class(self):
        return list

    def get_type_name(self):
        return "P2L"

    def encode(self, value):
        if isinstance(value, (list, tuple)):
            point_values = list(filter((lambda x: isinstance(x, iobjectspy.Point2D)), value))
            if len(point_values) > 0:
                stream = BytesIO()
                for v in point_values:
                    stream.write(struct.pack("!d", v.x) + struct.pack("!d", v.y))

                return stream.getvalue()
            return
        else:
            return

    def decode(self, bys):
        if isinstance(bys, (bytes, bytearray)):
            stream = BytesIO(bys)
            item = stream.read(16)
            result = []
            while len(item) == 16:
                x = struct.unpack("!d", item[0[:8]])[0]
                y = struct.unpack("!d", item[8[:16]])[0]
                import iobjectspy
                result.append(iobjectspy.Point2D(x, y))
                item = stream.read(16)

            return result
        return


class Rect2DSerializer(DataSerializer):

    def get_value_class(self):
        return iobjectspy.Rectangle

    def get_type_name(self):
        return "R"

    def encode(self, value):
        import iobjectspy
        if isinstance(value, iobjectspy.Rectangle):
            from iobjectspy.rpc._utils import encode_rect
            return encode_rect(value)
        return

    def decode(self, bys):
        if isinstance(bys, (bytes, bytearray)):
            from iobjectspy.rpc._utils import decode_rect
            return decode_rect(bys)
        return


class GeometrySerializer(DataSerializer):

    def get_value_class(self):
        return iobjectspy.Geometry

    def get_type_name(self):
        return "G"

    def encode(self, value):
        if isinstance(value, iobjectspy.Geometry):
            from iobjectspy.rpc._utils import encode_geometry
            return encode_geometry(value)
        return

    def decode(self, bys):
        if isinstance(bys, (bytes, bytearray)):
            from iobjectspy.rpc._utils import decode_geometry
            return decode_geometry(bytes(bys))
        return


class FeatureSerializer(DataSerializer):

    def get_value_class(self):
        return iobjectspy.Feature

    def get_type_name(self):
        return "F"

    def encode(self, value):
        if isinstance(value, iobjectspy.Feature):
            from iobjectspy.rpc._utils import encode_feature
            return encode_feature(value)
        return

    def decode(self, bys):
        if isinstance(bys, (bytes, bytearray)):
            from iobjectspy.rpc._utils import decode_feature
            return decode_feature(bytes(bys))
        return


class TileSerializer(DataSerializer):

    def get_value_class(self):
        return Tile

    def get_type_name(self):
        return "TI"

    def encode(self, value):
        if isinstance(value, Tile):
            from iobjectspy.rpc._utils import encode_tile
            return encode_tile(value)
        return

    def decode(self, bys):
        if isinstance(bys, (bytes, bytearray)):
            from iobjectspy.rpc._utils import decode_tile
            return decode_tile(bytes(bys))
        return


class ProcessInfoSerializer(DataSerializer):

    def get_value_class(self):
        return ProcessInfo

    def get_type_name(self):
        return "PI"

    def encode(self, value):
        if isinstance(value, ProcessInfo):
            from iobjectspy.rpc._utils import encode_process_info
            return encode_process_info(value)
        return

    def decode(self, bys):
        if isinstance(bys, (bytes, bytearray)):
            from iobjectspy.rpc._utils import decode_process_info
            return decode_process_info(bytes(bys))
        return


class EnumSerializer(DataSerializer):

    def __init__(self, enum_type):
        self.enum_type = enum_type

    def get_value_class(self):
        return self.enum_type

    def get_type_name(self):
        try:
            return self.enum_type._get_java_class_type()
        except Exception:
            import traceback
            traceback.format_exc()
            return

    def encode(self, value):
        from iobjectspy._jsuperpy.enums import JEnum
        if isinstance(value, JEnum):
            return struct.pack("!i", value.value)
        return

    def decode(self, bys):
        if isinstance(bys, (bytes, bytearray)):
            from iobjectspy._jsuperpy.enums import JEnum
            value = struct.unpack("!i", bys)[0]
            return self.get_value_class()._make(value)
        return


class ListSerializers(DataSerializer):
    _list_sers = {
     'b': BoolsSerializer, 'd': DoublesSerializer, 'f': FloatsSerializer, 
     'i': IntsSerializer, 'l': LongsSerializer, 's': ShortsSerializer, 'P2': Point2DsSerializer}

    def get_value_class(self):
        return list

    def get_type_name(self):
        return "OL"

    @staticmethod
    def _max_subs_same_type(iter, start):
        value = iter[start]
        i = start + 1
        subs = [value]
        value_type = type(value)
        while i < len(iter):
            if isinstance(iter[i], value_type):
                subs.append(iter[i])
                i += 1
            else:
                break

        return (
         subs, i)

    def encode(self, value):
        if isinstance(value, (list, tuple)):
            stream = BytesIO()
            start = 0
            while start < len(value):
                subs, start = ListSerializers._max_subs_same_type(value, start)
                if len(subs) > 0:
                    ser = DataSerializers.find(type(subs[0]))
                    if ser is None:
                        raise ValueError("cannot find serializer for " + type(subs[0]))
                stream.write(struct.pack("!i", len(subs)))
                type_name = ser.get_type_name()
                type_name_bys = bytes("!" + ser.get_type_name() + ";", "utf-8")
                stream.write(type_name_bys)
                if type_name != "n":
                    if type_name in ('b', 'd', 'f', 'i', 'l', 's', 'P2'):
                        list_ser = self._list_sers[type_name]()
                        value_bys = list_ser.encode(subs)
                        stream.write(struct.pack("!i", len(value_bys)))
                        stream.write(value_bys)
                    else:
                        for sub_value in subs:
                            bys = ser.encode(sub_value)
                            stream.write(struct.pack("!i", len(bys)))
                            stream.write(bys)

            return stream.getvalue()
        return

    def decode(self, bys):
        if isinstance(bys, (bytes, bytearray)):
            stream = BytesIO(bys)
            item_len_bs = stream.read(4)
            result = []
            while len(item_len_bs) == 4:
                count = struct.unpack("!i", item_len_bs)[0]
                type_name_bys = []
                temp_bys = stream.read(1)
                if not temp_bys[0] == ord(b'!'):
                    raise ValueError("invalid input bytes")
                temp_bys = stream.read(1)
                while len(temp_bys) == 1:
                    if temp_bys[0] == ord(b';'):
                        break
                    type_name_bys.append(temp_bys[0])
                    temp_bys = stream.read(1)

                type_name = str(bytes(type_name_bys), "utf-8")
                if type_name == "n":
                    for i in range(count):
                        result.append(None)

                else:
                    if type_name in ('b', 'd', 'f', 'i', 'l', 's', 'P2'):
                        ser = self._list_sers[type_name]()
                        value_len = struct.unpack("!i", stream.read(4))[0]
                        result.extend(ser.decode(stream.read(value_len)))
                    else:
                        ser = DataSerializers.find(type_name)
                        if ser is None:
                            raise ValueError("Cannot find serializer for " + type_name)
                        for i in range(count):
                            len_v = struct.unpack("!i", stream.read(4))[0]
                            result.append(ser.decode(stream.read(len_v)))

                item_len_bs = stream.read(4)

            return result
        return


class MapSerializer(DataSerializer):

    def get_value_class(self):
        return dict

    def get_type_name(self):
        return "M"

    def encode(self, value):
        if isinstance(value, dict):
            io = BytesIO()
            for key, value in value.items():
                key_bytes = DataSerializers.serialize(key)
                value_bytes = DataSerializers.serialize(value)
                io.write(struct.pack("!i", len(key_bytes)))
                io.write(key_bytes)
                io.write(struct.pack("!i", len(value_bytes)))
                io.write(value_bytes)

            return io.getvalue()
        return

    def decode(self, bys):
        from iobjectspy.rpc._utils import read_length_and_bytes
        if isinstance(bys, (bytes, bytearray)):
            stream = BytesIO(bys)
            result = dict()
            while True:
                try:
                    key_bys = read_length_and_bytes(stream)
                    value_bys = read_length_and_bytes(stream)
                    key = DataSerializers.deserialize(key_bys)
                    value = DataSerializers.deserialize(value_bys)
                    result[key] = value
                except:
                    return result

            return result
        return


class DataSerializers:
    _name_providers = {}
    _value_class_providers = {}

    @classmethod
    def _register_value_serializers(cls):
        cls.register_default_serializer([bytes, bytearray], BytesSerializer())
        cls.register_default_serializer(float, DoubleSerializer())
        cls.register_default_serializer(int, LongSerializer())
        cls.register_default_serializer(bool, BoolSerializer())
        cls.register_default_serializer(str, StrSerializer())
        cls.register_default_serializer(type(None), NoneSerializer())
        cls.register_default_serializer(None, NoneSerializer())
        cls.register_default_serializer(datetime.datetime, TimestampSerializer())
        import iobjectspy
        cls.register_default_serializer(iobjectspy.FieldInfo, FieldInfoSerializer())
        cls.register_default_serializer(iobjectspy.Point2D, Point2DSerializer())
        cls.register_default_serializer(iobjectspy.Rectangle, Rect2DSerializer())
        cls.register_default_serializer(iobjectspy.Geometry, GeometrySerializer())
        cls.register_default_serializer(iobjectspy.GeoPoint, GeometrySerializer())
        cls.register_default_serializer(iobjectspy.GeoLine, GeometrySerializer())
        cls.register_default_serializer(iobjectspy.GeoRegion, GeometrySerializer())
        cls.register_default_serializer(iobjectspy.Feature, FeatureSerializer())
        cls.register_default_serializer(Tile, TileSerializer())
        cls.register_default_serializer(ProcessInfo, ProcessInfoSerializer())
        cls.register_default_serializer([list, tuple], ListSerializers())
        cls.register_default_serializer([dict], MapSerializer())

    @classmethod
    def _register_external_serializers(cls):
        cls.register(IntSerializer())
        cls.register(ShortSerializer())
        cls.register(FloatSerializer())
        cls.register(BoolsSerializer())
        cls.register(IntsSerializer())
        cls.register(LongsSerializer())
        cls.register(DoublesSerializer())
        cls.register(StrsSerializer())
        cls.register(DateSerializer())
        cls.register(Point2DsSerializer())
        cls.register(ShortsSerializer())

    @classmethod
    def _register_enum_serializers(cls):
        import iobjectspy

        def _get_all_classes(model, all_subclasses):
            for subclass in model.__subclasses__():
                if subclass.__name__ not in all_subclasses.keys():
                    all_subclasses[subclass.__name__] = subclass
                _get_all_classes(subclass, all_subclasses)

            return all_subclasses

        all_sub_class = {}
        _get_all_classes(iobjectspy._jsuperpy.JEnum, all_sub_class)
        for name, sub_class in all_sub_class.items():
            cls.register_default_serializer(sub_class, EnumSerializer(sub_class))

    @classmethod
    def register(cls, ser):
        if isinstance(ser, DataSerializer):
            type_name = ser.get_type_name()
            if type_name:
                cls._name_providers[ser.get_type_name()] = ser
        else:
            raise TypeError("required DataSerializer instance")

    @classmethod
    def register_default_serializer(cls, value_type, ser):
        if not isinstance(ser, DataSerializer):
            raise TypeError("required DataSerializer instance")
        cls.register(ser)
        if not isinstance(value_type, (list, tuple)):
            value_type = [
             value_type]
        for t in value_type:
            if isinstance(t, type):
                cls._value_class_providers[t] = ser

    @classmethod
    def find(cls, key):
        if isinstance(key, str):
            ser = cls._name_providers[key]
        else:
            if isinstance(key, type):
                ser = cls._value_class_providers[key]
            else:
                ser = cls._value_class_providers[type(key)]
        return ser

    @staticmethod
    def serialize(value):
        ser = DataSerializers.find(type(value))
        if ser is None:
            raise ValueError("cannot find serializer for " + type(value))
        return ser.serialize(value)

    @staticmethod
    def deserialize(bys):
        return DataSerializer.deserialize(bys)

    @staticmethod
    def encode(value):
        ser = DataSerializers.find(type(value))
        if ser is None:
            raise ValueError("cannot find serializer for " + type(value))
        return ser.encode(value)

    @staticmethod
    def decode(type_name, bys):
        ser = DataSerializers.find(type_name)
        if ser is None:
            raise ValueError("cannot find serializer for " + type_name)
        return ser.decode(bys)


DataSerializers._register_value_serializers()
DataSerializers._register_external_serializers()
DataSerializers._register_enum_serializers()
if __name__ == "__main__":
    from iobjectspy import DatasetType

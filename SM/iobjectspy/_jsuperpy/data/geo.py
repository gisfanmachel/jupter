# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/_jsuperpy\data\geo.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 202110 bytes
import datetime, json
from collections import OrderedDict
import copy
from ..enums import *
from .._gateway import get_jvm
from .._logger import log_error, log_info
from .._utils import java_color_to_tuple, to_java_color, tuple_to_java_color, color_to_tuple, to_java_double_array, split_input_list_from_str, oj
from ._jvm import JVMBase
from ._util import field_default_value_to_java, convert_value_to_python
from .style import *
from .ex import ObjectDisposedError
__all__ = [
 'FieldInfo', 'Point2D', 'Point3D', 'Rectangle', 'Geometry', 'GeoPoint', 'GeoPoint3D', 
 'GeoLine', 'GeoRegion', 
 'TextPart', 'GeoText', 'TextStyle', 'GeoStyle3D', 
 'Feature', 'Geometry3D', 'GeoBox', 'GeoModel3D', 
 'GeoCylinder', 'GeoCircle3D', 
 'GeoRegion3D', 'GeoLine3D', 'Plane', 'Matrix', 'PointM', 'GeoLineM']
INT32_MAX = 2147483647

class FieldInfo:
    __doc__ = "\n    字段信息类。字段信息类用来存储字段的名称、类型、默认值以及长度等相关信息。 每一个字段对应一个 FieldInfo。对于矢量数据集的每一个字段，只有字段的\n    别名（caption）可以被修改，其他属性的修改需要依据具体引擎是否支持。\n    "

    def __init__(self, name=None, field_type=None, max_length=None, default_value=None, caption=None, is_required=False, is_zero_length_allowed=True):
        """
        构造字段信息对象

        :param str name:  字段名称。字段的名称只能由数字、字母和下划线组成，但不能以数字或下划线开头；用户新建字段时，字段名称不能以 SM 作为前
                          缀，以 SM 作为前缀的都是 SuperMap 系统字段，另外，字段的名称不能超过30个字符，且字段的名称不区分大小写。名称用于
                          唯一标识该字段，所以字段不可重名。
        :param field_type: 字段类型
        :type field_type: FieldType or str
        :param int max_length: 字段值的最大长度，只对文本字段有效
        :param default_value: 字段的默认值
        :type default_value: int or float or datetime.datetime or str or bytes or bytearray
        :param str caption: 字段别名
        :param bool is_required: 是否是必填字段
        :param bool is_zero_length_allowed: 是否允许零长度。只对文本类型（TEXT，WTEXT，CHAR）字段有效
        """
        self._name = None
        self._type = None
        self._max_length = 255
        self._default_value = None
        self._caption = None
        self._is_required = False
        self._is_zero_length_allowed = True
        self.set_name(name).set_type(field_type).set_max_length(max_length).set_default_value(default_value).set_caption(caption).set_required(is_required).set_zero_length_allowed(is_zero_length_allowed)

    def clone(self):
        """
        拷贝一个新的 FieldInfo  对象

        :rtype: FieldInfo
        """
        return FieldInfo(self.name, self.type, self.max_length, self.default_value, self.caption, self.is_required, self.is_zero_length_allowed)

    @property
    def name(self):
        """str: 字段名称，字段的名称只能由数字、字母和下划线组成，但不能以数字或下划线开头；用户新建字段时，字段名称不能以 SM 作为前缀，以 SM 作为前
            缀的都是 SuperMap 系统字段，另外，字段的名称不能超过30个字符，且字段的名称不区分大小写。名称用于唯一标识该字段，所以字段不可重名。"""
        return self._name

    @property
    def type(self):
        """FieldType: 字段类型"""
        return self._type

    @property
    def max_length(self):
        """int:  字段值的最大长度，只对文本字段有效"""
        return self._max_length

    @property
    def default_value(self):
        """ int or float or datetime.datetime or str or bytes or bytearray:  字段的默认值"""
        return self._default_value

    @property
    def caption(self):
        """str: 字段别名"""
        return self._caption

    @property
    def is_required(self):
        """bool: 字段是否为必填字段"""
        return self._is_required

    @property
    def is_zero_length_allowed(self):
        """bool: 是否允许零长度。只对文本类型（TEXT，WTEXT，CHAR）字段有效"""
        return self._is_zero_length_allowed

    @property
    def _jobject(self):
        java_obj = get_jvm().com.supermap.data.FieldInfo()
        java_obj.setName(self.name)
        java_obj.setType(self.type._jobject)
        if self.caption is not None:
            java_obj.setCaption(str(self.caption))
        if self.max_length is not None:
            java_obj.setMaxLength(int(self.max_length))
        if self.default_value is not None:
            java_obj.setDefaultValue(field_default_value_to_java(self.default_value, self.type))
        if self.is_required is not None:
            java_obj.setRequired(bool(self.is_required))
        if self.is_zero_length_allowed is not None:
            java_obj.setZeroLengthAllowed(bool(self.is_zero_length_allowed))
        return java_obj

    @staticmethod
    def _from_java_object(java_obj):
        obj = FieldInfo()
        obj.set_name(java_obj.getName())
        obj.set_type(java_obj.getType().name())
        obj.set_caption(java_obj.getCaption())
        obj.set_zero_length_allowed(java_obj.isZeroLengthAllowed())
        obj.set_required(java_obj.isRequired())
        obj.set_max_length(java_obj.getMaxLength())
        obj.set_default_value(convert_value_to_python(java_obj.getDefaultValue(), obj.type))
        obj._java_object = java_obj
        return obj

    def set_name(self, value):
        """
        设置字段名称。字段的名称只能由数字、字母和下划线组成，但不能以数字或下划线开头；用户新建字段时，字段名称不能以 SM 作为前缀，以 SM 作为前缀
        的都是 SuperMap 系统字段，另外，字段的名称不能超过30个字符，且字段的名称不区分大小写。名称用于唯一标识该字段，所以字段不可重名。

        :param str value: 字段名称
        :return: self
        :rtype: FieldInfo
        """
        if value is not None:
            self._name = str(value)
            if self.caption is None:
                self.set_caption(value)
        return self

    def set_zero_length_allowed(self, value):
        """
        设置字段是否允许零长度。只对文本字段有效。

        :param bool value: 字段是否允许零长度。允许字段零长度设置为True，否则为False。默认值为True。
        :return: self
        :rtype: FieldInfo
        """
        if value is not None:
            self._is_zero_length_allowed = bool(value)
        return self

    def set_caption(self, value):
        """
        设置此字段的别名。别名可以不唯一，即不同的字段可以有相同的别名，而名称是用来唯一标识一个字段的，所以不可重名

        :param str value: 字段别名。
        :return: self
        :rtype: FieldInfo
        """
        if value is not None:
            self._caption = str(value)
        return self

    def set_max_length(self, value):
        """
        返回字段值的最大长度，只对文本字段有效。单位：字节

        :param int value: 字段值的最大长度
        :return: self
        :rtype: FieldInfo
        """
        if value is not None:
            self._max_length = int(value)
        return self

    def set_type(self, value):
        """
        设置字段类型

        :param value: 字段类型
        :type value: FieldType or str
        :return: self
        :rtype: FieldInfo
        """
        if value is not None:
            self._type = FieldType._make(value)
        return self

    def set_required(self, value):
        """
        设置字段是否为必填字段

        :param str value: 字段名称
        :return: self
        :rtype: FieldInfo
        """
        if value is not None:
            self._is_required = bool(value)
        return self

    def is_system_field(self):
        """
        判断当前对象是否是系统字段。对于所有以 Sm 开头（不区分大小写）的字段都是系统系统。

        :rtype: bool
        """
        if self.name is not None:
            if self.name.lower().startswith("sm"):
                return True
        return False

    def set_default_value(self, value):
        """
        设置字段的默认值。当添加一条记录时，如果该字段未被赋值，则以该默认值作为该字段的值。

        :param value: 字段的默认值
        :type value: bool or int or float or datetime.datetime or str or bytes or bytearray
        :return: self
        :rtype: FieldInfo
        """
        self._default_value = value
        return self

    def __repr__(self):
        return "FieldInfo(%s, %s)" % (self.name, self.type)

    def __str__(self):
        info = "FieldInfo: name=%s, type=%s, caption=%s " % (self.name, self.type, self.caption)
        if self.default_value is not None:
            str_default_value = field_default_value_to_java(self.default_value, self.type)
            info = "%s, default_value=%s" % (info, str_default_value)
        if self.type is FieldType.WTEXT or self.type is FieldType.TEXT:
            info = "%s, max_length=%d" % (info, self.max_length)
        return info

    def __getstate__(self):
        return (
         self.name, self.caption, self.type.name, self.max_length,
         self.default_value, self.is_required, self.is_zero_length_allowed)

    def __setstate__(self, state):
        if len(state) != 7:
            raise Exception("state length required 7 but " + str(len(state)))
        self.__init__(state[0], state[2], state[3], state[4], state[1], state[5], state[6])

    def to_dict(self):
        """
        将当前对象输出到 dict 对象中

        :rtype: dict
        """
        d = dict()
        if self.name is not None:
            d["name"] = self.name
        if self.type is not None:
            d["type"] = self.type.name
        if self.default_value is not None:
            d["default_value"] = self.default_value
        if self.is_zero_length_allowed is not None:
            d["is_zero_length_allowed"] = self.is_zero_length_allowed
        if self.is_required is not None:
            d["is_required"] = self.is_required
        if self.caption is not None:
            d["caption"] = self.caption
        if self.max_length is not None:
            if self.type in [FieldType.TEXT, FieldType.WTEXT, FieldType.CHAR]:
                d["max_length"] = self.max_length
        return d

    @staticmethod
    def make_from_dict(values):
        """
        从 dict 对象中构造一个新的 FieldInfo 对象

        :param dict values: 包含 FieldInfo 字段信息的 dict 对象
        :rtype: FieldInfo
        """
        return FieldInfo().from_dict(values)

    def from_dict(self, values):
        """
        从 dict 对象中读取字段信息

        :param dict values: 包含 FieldInfo 字段信息的 dict 对象
        :return: self
        :rtype: FieldInfo
        """
        if "name" in values.keys():
            self.set_name(values["name"])
        if "type" in values.keys():
            self.set_type(values["type"])
        if "default_value" in values.keys():
            self.set_default_value(values["default_value"])
        if "is_zero_length_allowed" in values.keys():
            self.set_zero_length_allowed(values["is_zero_length_allowed"])
        if "is_required" in values.keys():
            self.set_required(values["is_required"])
        if "caption" in values.keys():
            self.set_caption(values["caption"])
        if "max_length" in values.keys():
            self.set_max_length(values["max_length"])
        return self

    def to_json(self):
        """
        将当前对象输出为 json 字符串

        :rtype: str
        """
        d = self.to_dict()
        if "default_value" in d:
            value = d["default_value"]
            if isinstance(value, (bytes, bytearray)):
                d["default_value"] = value.decode("utf-8")
            else:
                if isinstance(value, datetime.datetime):
                    d["default_value"] = value.strftime("%Y-%m-%d %H:%M:%S")
        return json.dumps(d)

    @staticmethod
    def from_json(value):
        """
        从 json 字符串中构造 FieldInfo 对象

        :param str value: json 字符串
        :rtype: FieldInfo
        """
        return FieldInfo.make_from_dict(json.loads(value))


class Point2D:
    __doc__ = "\n    二维点对象，使用两个浮点数分别表示 x 和 y 轴的位置。\n    "

    def __init__(self, x=None, y=None):
        """
        使用 x 和 y 值构造二维点对象。

        :param float x: x 坐标轴值
        :param float y: y 坐标值
        """
        self.x = float(x) if x is not None else None
        self.y = float(y) if y is not None else None

    def __str__(self):
        return "[%f, %f]" % (self.x, self.y)

    def __repr__(self):
        return "Point2D(%f, %f)" % (self.x, self.y)

    def __eq__(self, other):
        return self.__cmp__(other) == 0

    def __len__(self):
        return 2

    def __getitem__(self, item):
        if item < 0:
            item = 2 + item
        if item == 0:
            return self.x
        if item == 1:
            return self.y
        return

    def __cmp__(self, other):
        other = Point2D.make(other)
        from .._utils import is_zero
        if is_zero(self.x - other.x):
            if is_zero(self.y - other.y):
                return 0
            if self.y > other.y:
                return 1
            return -1
        else:
            if self.x > other.x:
                return 1
            return -1

    def __lt__(self, other):
        if self.__cmp__(other) == -1:
            return True
        return False

    def equal(self, other, tolerance=0.0):
        """
        判断当前点与指定点在容限范围内是否相等

        :param Point2D other: 待判断的点
        :param float tolerance: 容限值
        :rtype: bool
        """
        if tolerance is None:
            d = 0.0
        else:
            d = float(tolerance)
        other = Point2D.make(other)
        from .._utils import is_equal
        return is_equal(self.x, other.x, d) and is_equal(self.y, other.y, d) or False
        from .op import compute_distance
        return compute_distance(self, other) <= d

    def distance_to(self, other):
        """
        计算当前点与指定点之间的距离

        :param Point2D other: 目标点
        :return: 返回两个点之间的几何距离
        :rtype: float
        """
        import math
        other = Point2D.make(other)
        return math.sqrt(math.pow(self.x - other.x, 2) + math.pow(self.y - other.y, 2))

    def clone(self):
        """
        复制当前对象，返回一个新的对象

        :rtype: Point2D
        """
        return Point2D(self.x, self.y)

    @property
    def _jobject(self):
        return get_jvm().com.supermap.data.Point2D(self.x, self.y)

    @staticmethod
    def _from_java_object(java_obj):
        if java_obj is None:
            return
        return Point2D(java_obj.getX(), java_obj.getY())

    def __getstate__(self):
        return (
         self.x, self.y)

    def __setstate__(self, state):
        if len(state) != 2:
            raise Exception("state length required 2 but " + str(len(state)))
        self.__init__(state[0], state[1])

    def to_json(self):
        """
        将当前二维点对象输出为 json 字符串

        :rtype: str
        """
        return json.dumps({"Point2D": [self.x, self.y]})

    @staticmethod
    def from_json(value):
        """
        从 json 字符串中构造二维点坐标

        :param str value: json 字符串
        :rtype: Point2D
        """
        d = json.loads(value)["Point2D"]
        return Point2D(d[0], d[1])

    def to_dict(self):
        """输出为 dict 对象

        :rtype: dict
        """
        return {'x':self.x, 
         'y':self.y}

    def from_dict(self, value):
        """
        从 dict 中读取点信息

        :param dict value: 包含 x 和 y 值的 dict
        :return: self
        :rtype: Point2D
        """
        self.x = value["x"]
        self.y = value["y"]
        return self

    @staticmethod
    def make_from_dict(value):
        """
        从 dict 中读取点信息构建二维点对象

        :param dict  value: 包含 x 和 y 值的 dict
        :rtype: Point2D
        """
        return Point2D().from_dict(value)

    @staticmethod
    def make(p):
        """
        构造一个二维点对象

        :param p: x 和 y 值
        :type p: tuple[float,float] or list[float,float] or GeoPoint or Point2D or dict
        :rtype: Point2D
        """
        if isinstance(p, Point2D):
            return p
            if isinstance(p, str):
                try:
                    p = p.strip().replace("[", "").replace("]", "").replace('"', "").replace("(", "").replace(")", "")
                    tokens = p.split(",")
                    return Point2D(float(tokens[0]), float(tokens[1]))
                except:
                    try:
                        return Point2D.make_from_dict(json.loads(p))
                    except:
                        return

        else:
            if isinstance(p, (tuple, list)):
                if len(p) >= 2:
                    return Point2D(float(p[0]), float(p[1]))
            else:
                if isinstance(p, GeoPoint):
                    return p.point
                    if isinstance(p, dict):
                        if "x" in p:
                            x = p["x"]
                        else:
                            if "X" in p:
                                x = p["X"]
                            else:
                                return
                        if "y" in p:
                            y = p["x"]
                elif "Y" in p:
                    y = p["Y"]
                else:
                    return
                return Point2D(x, y)
            return


class Point3D:

    def __init__(self, x=None, y=None, z=None):
        self.x = float(x) if x is not None else None
        self.y = float(y) if y is not None else None
        self.z = float(z) if z is not None else None

    def clone(self):
        """
        复制当前对象

        :rtype: Point3D
        """
        return Point3D(self.x, self.y, self.z)

    def __str__(self):
        return "[%f, %f, %f]" % (self.x, self.y, self.z)

    def __repr__(self):
        return "Point3D(%f, %f, %f)" % (self.x, self.y, self.z)

    def __eq__(self, other):
        return self.__cmp__(other) == 0

    def __len__(self):
        return 3

    def __getitem__(self, item):
        if item < 0:
            item = 3 + item
        if item == 0:
            return self.x
        if item == 1:
            return self.y
        if item == 2:
            return self.z
        return

    def __cmp__(self, other):
        if self.x < other.x:
            return -1
        if self.x > other.x:
            return 1
        if self.y < other.y:
            return -1
        if self.y > other.y:
            return 1
        if self.z < other.z:
            return -1
        if self.z > other.z:
            return 1
        return 0

    def __lt__(self, other):
        if self.__cmp__(other) == -1:
            return True
        return False

    @property
    def _jobject(self):
        return get_jvm().com.supermap.data.Point3D(self.x, self.y, self.z)

    def __getstate__(self):
        return (
         self.x, self.y, self.z)

    def __setstate__(self, state):
        if len(state) != 3:
            raise Exception("state length required 3 but " + str(len(state)))
        self.__init__(state[0], state[1], state[2])

    @staticmethod
    def _from_java_object(java_obj):
        if java_obj is None:
            return
        return Point3D(java_obj.getX(), java_obj.getY(), java_obj.getZ())

    def to_json(self):
        """
        将当前三维点对象输出为 json 字符串

        :rtype: str
        """
        return json.dumps({"Point3D": [self.x, self.y, self.y]})

    @staticmethod
    def from_json(value):
        """
        从 json 字符串中构造三维点坐标

        :param str value: json 字符串
        :rtype: Point3D
        """
        d = json.loads(value)["Point3D"]
        return Point3D(d[0], d[1], d[2])

    def to_dict(self):
        """输出为 dict 对象

        :rtype: dict
        """
        return {'x':self.x, 
         'y':self.y,  'z':self.z}

    def from_dict(self, value):
        """
        从 dict 中读取点信息

        :param dict value: 包含 x、y 和z值的 dict
        :return: self
        :rtype: Point3D
        """
        self.x = value["x"]
        self.y = value["y"]
        self.z = value["z"]
        return self

    @staticmethod
    def make_from_dict(value):
        """
        从 dict 中读取点信息构造三维点坐标

        :param dict value: 包含 x、y 和z值的 dict
        :return: self
        :rtype: Point3D
        """
        return Point3D().from_dict(value)

    @staticmethod
    def make(p):
        """
        构造一个三维点对象

        :param p: x，y 和 z 值
        :type p: tuple[float,float,float] or list[float,float,float] or GeoPoint3D or Point3D or dict
        :rtype: Point3D
        """
        if isinstance(p, Point3D):
            return p
            if isinstance(p, str):
                try:
                    p = p.strip().replace("[", "").replace("]", "").replace('"', "").replace("(", "").replace(")", "")
                    tokens = p.split(",")
                    return Point3D(float(tokens[0]), float(tokens[1]), float(tokens[2]))
                except:
                    try:
                        return Point3D.make_from_dict(json.loads(p))
                    except:
                        return

        else:
            if isinstance(p, (tuple, list)):
                if len(p) >= 3:
                    return Point3D(float(p[0]), float(p[1]), float(p[2]))
            else:
                if isinstance(p, GeoPoint3D):
                    return p.point
                    if isinstance(p, dict):
                        if "x" in p:
                            x = p["x"]
                        else:
                            if "X" in p:
                                x = p["X"]
                            else:
                                return
                        if "y" in p:
                            y = p["x"]
                        else:
                            if "Y" in p:
                                y = p["Y"]
                            else:
                                return
                        if "z" in p:
                            z = p["z"]
                elif "Z" in p:
                    z = p["Z"]
                else:
                    return
                return Point3D(x, y, z)
            return


class PointM:

    def __init__(self, x=None, y=None, m=None):
        self.x = float(x) if x is not None else None
        self.y = float(y) if y is not None else None
        self.m = float(m) if m is not None else None

    def clone(self):
        """
        复制当前对象

        :rtype: PointM
        """
        return PointM(self.x, self.y, self.m)

    def __str__(self):
        return "[%f, %f, %f]" % (self.x, self.y, self.m)

    def __repr__(self):
        return "PointM(%f, %f, %f)" % (self.x, self.y, self.m)

    def __eq__(self, other):
        return self.__cmp__(other) == 0

    def __len__(self):
        return 3

    def __getitem__(self, item):
        if item < 0:
            item = 3 + item
        if item == 0:
            return self.x
        if item == 1:
            return self.y
        if item == 2:
            return self.m
        return

    def __cmp__(self, other):
        if self.x < other.x:
            return -1
        if self.x > other.x:
            return 1
        if self.y < other.y:
            return -1
        if self.y > other.y:
            return 1
        if self.m < other.m:
            return -1
        if self.m > other.m:
            return 1
        return 0

    def __lt__(self, other):
        if self.__cmp__(other) == -1:
            return True
        return False

    @property
    def _jobject(self):
        return get_jvm().com.supermap.data.PointM(self.x, self.y, self.m)

    def __getstate__(self):
        return (
         self.x, self.y, self.m)

    def __setstate__(self, state):
        if len(state) != 3:
            raise Exception("state length required 3 but " + str(len(state)))
        self.__init__(state[0], state[1], state[2])

    @staticmethod
    def _from_java_object(java_obj):
        if java_obj is None:
            return
        return PointM(java_obj.getX(), java_obj.getY(), java_obj.getZ())

    def to_json(self):
        """
        将当前路由点对象输出为 json 字符串

        :rtype: str
        """
        return json.dumps({"PointM": [self.x, self.y, self.y]})

    @staticmethod
    def from_json(value):
        """
        从 json 字符串中构造路由点坐标

        :param str value: json 字符串
        :rtype: PointM
        """
        d = json.loads(value)["PointM"]
        return Point3D(d[0], d[1], d[2])

    def to_dict(self):
        """输出为 dict 对象

        :rtype: dict
        """
        return {'x':self.x, 
         'y':self.y,  'm':self.m}

    def from_dict(self, value):
        """
        从 dict 中读取点信息

        :param dict value: 包含 x、y 和m值的 dict
        :return: self
        :rtype: PointM
        """
        self.x = value["x"]
        self.y = value["y"]
        self.m = value["m"]
        return self

    @staticmethod
    def make_from_dict(value):
        """
        从 dict 中读取点信息构造路由点坐标

        :param dict value: 包含 x、y 和m值的 dict
        :return: self
        :rtype: PointM
        """
        return PointM().from_dict(value)

    @staticmethod
    def make(p):
        """
        构造一个路由点对象

        :param p: x，y 和 m 值
        :type p: tuple[float,float,float] or list[float,float,float] or PointM or dict
        :rtype: PointM
        """
        if isinstance(p, PointM):
            return p
            if isinstance(p, str):
                try:
                    p = p.strip().replace("[", "").replace("]", "").replace('"', "").replace("(", "").replace(")", "")
                    tokens = p.split(",")
                    return PointM(float(tokens[0]), float(tokens[1]), float(tokens[2]))
                except:
                    try:
                        return PointM.make_from_dict(json.loads(p))
                    except:
                        return

        elif isinstance(p, (tuple, list)):
            if len(p) >= 3:
                return PointM(float(p[0]), float(p[1]), float(p[2]))
        if isinstance(p, dict):
            if "x" in p:
                x = p["x"]
            else:
                if "X" in p:
                    x = p["X"]
                else:
                    return
            if "y" in p:
                y = p["x"]
            else:
                if "Y" in p:
                    y = p["Y"]
                else:
                    return
            if "m" in p:
                z = p["m"]
            else:
                if "M" in p:
                    z = p["M"]
                else:
                    return
            return PointM(x, y, z)
        return


class Rectangle:
    __doc__ = "\n        矩形对象使用四个浮点数表示一个矩形的范围。其中 left 代表 x 方向的最小值，top 代表 y 方向的最大值，\n        right 代表 x 方向的最大值，bottom 代表 y 方向的最小值。当使用矩形表示一个地理范围时，通常 left 表示经度的最小值，\n        right 表示经度的最大值，top 表示纬度的最大值，bottom表示维度的最小值\n        该类的对象通常用于确定范围，可用来表示几何对象的最小外接矩形、地图窗口的可视范围，数据集的范围等，另外在进行矩形选择，矩形查询等时也会用到此类的对象。\n    "

    def __init__(self, left=None, bottom=None, right=None, top=None):
        self._left = None
        self._right = None
        self._top = None
        self._bottom = None
        self.set_left(left).set_right(right).set_bottom(bottom).set_top(top)

    def clone(self):
        """
        复制当前对象

        :rtype: Rectangle
        """
        return Rectangle(self.left, self.bottom, self.right, self.top)

    @property
    def left(self):
        """
        float: 返回当前矩形对象左边界的坐标值
        """
        return self._left

    @property
    def right(self):
        """
        float: 返回当前矩形对象右边界的坐标值
        """
        return self._right

    @property
    def top(self):
        """
        float: 返回当前矩形对象上边界的坐标值
        """
        return self._top

    @property
    def bottom(self):
        """
        float: 返回当前矩形对象下边界的坐标值
        """
        return self._bottom

    @staticmethod
    def _from_java_object(jrc):
        if jrc is None:
            raise Exception("java object Rectangle2D is None")
        rc = Rectangle(jrc.getLeft(), jrc.getBottom(), jrc.getRight(), jrc.getTop())
        return rc

    @property
    def _jobject(self):
        """
        Py4J 映射的 Java 对象
        """
        return get_jvm().com.supermap.data.Rectangle2D(self.left, self.bottom, self.right, self.top)

    def __str__(self):
        return str(self.to_tuple())

    def __repr__(self):
        return "Rectangle(%f, %f, %f, %f)" % (self.left, self.bottom, self.right, self.top)

    def __eq__(self, other):
        """
        判断当前矩形对象与指定矩形对象是否相同。只有当上下左右边界完全相同时才能判断为相同。

        :param Rectangle other:  待判断的矩形对象。
        :return:  如果当前对象与矩形对象相同，返回True，否则返回False
        :rtype: bool
        """
        if other is None:
            return False
        import math
        if math.isclose(self.left, other.left):
            if math.isclose(self.right, other.right):
                if math.isclose(self.top, other.top):
                    if math.isclose(self.bottom, other.bottom):
                        return True
        return False

    def __len__(self):
        """
        :return: 当矩形对象使用四个二维坐标点描述具体的坐标位置时，返回点的数目。固定为4.
        :rtype: int
        """
        return 4

    def __getitem__(self, item):
        """
        当矩形对象使用四个二维坐标点描述具体的坐标位置时，返回点坐标值。

        :param int item: 0，1，2，3值
        :return: 根据 item 的值，分别返回左上点，右上点，右下点，左下点
        :rtype: float
        """
        if item < 0:
            item = 4 + item
        if item == 0:
            return Point2D(self.left, self.top)
        if item == 1:
            return Point2D(self.right, self.top)
        if item == 2:
            return Point2D(self.right, self.bottom)
        if item == 3:
            return Point2D(self.left, self.bottom)
        return

    @property
    def points(self):
        """
        tuple[Point2D]: 获取矩形四个顶点坐标值，返回一个4个二维点（Point2D）的元组。其中第一个点表示左上点，第二个点表示右上点，第三个点表示右下点，第四个点表示左下点。

        >>> rect = Rectangle(1.0, 3, 2.0, 20)
        >>> points = rect.points
        >>> len(points)
        4
        >>> points[0] == Point2D(1.0,20)
        True
        >>> points[2] == Point2D(2.0,3)
        True
        """
        return tuple((Point2D(self.left, self.top),
         Point2D(self.right, self.top),
         Point2D(self.right, self.bottom),
         Point2D(self.left, self.bottom)))

    def __getstate__(self):
        return (
         self.left, self.bottom, self.right, self.top)

    def __setstate__(self, state):
        if len(state) != 4:
            raise Exception("state length required 4 but " + str(len(state)))
        self.__init__(state[0], state[1], state[2], state[3])

    def _set_left_right(self, left, right):
        if left is not None and right is not None:
            self._left = min(float(left), float(right))
            self._right = max(float(left), float(right))
        else:
            if left is not None:
                self._left = float(left)
            else:
                self._left = None
            if right is not None:
                self._right = float(right)
            else:
                self._right = None
        return self

    def _set_top_bottom(self, top, bottom):
        if top is not None and bottom is not None:
            self._bottom = min(float(top), float(bottom))
            self._top = max(float(top), float(bottom))
        else:
            if bottom is not None:
                self._bottom = float(bottom)
            else:
                self._bottom = None
            if top is not None:
                self._top = float(top)
            else:
                self._top = None

    def set_left(self, value):
        """
        设置当前矩形对象的左边界值。如果左右边界值都有效，当左边界值大于右边界值，会将左右边界值互换

        :param float value:  左边界值
        :return: self
        :rtype: Rectangle
        """
        self._left = float(value) if value is not None else None
        if self.right is not None:
            if self.left is not None:
                if self.right < self.left:
                    self._right, self._left = self._left, self._right
        return self

    def set_right(self, value):
        """
        设置当前矩形对象的右边界值。如果左右边界值都有效，当左边界值大于右边界值，会将左右边界值互换

        :param float value:  右边界值
        :return: self
        :rtype: Rectangle

        >>> rc = Rectangle(left=10).set_right(5.0)
        >>> rc.right, rc.left
        (10.0, 5.0)

        """
        self._right = float(value) if value is not None else None
        if self.right is not None:
            if self.left is not None:
                if self.right < self.left:
                    self._right, self._left = self._left, self._right
        return self

    def set_top(self, value):
        """
        设置当前矩形对象的上边界值。如果上下边界值都有效，当下边界值大于上边界值，会将上下边界值互换

        :param float value:  上边界值
        :return: self
        :rtype: Rectangle

        >>> rc = Rectangle(bottom=10).set_top(5.0)
        >>> rc.top, rc.bottom
        (10.0, 5.0)

        """
        self._top = float(value) if value is not None else None
        if self.top is not None:
            if self.bottom is not None:
                if self.top < self.bottom:
                    self._top, self._bottom = self._bottom, self._top
        return self

    def set_bottom(self, value):
        """
        设置当前矩形对象的下边界值。如果上下边界值都有效，当下边界值大于上边界值，会将上下边界值互换

        :param float value:  下边界值
        :return: self
        :rtype: Rectangle
        """
        self._bottom = float(value) if value is not None else None
        if self.top is not None:
            if self.bottom is not None:
                if self.top < self.bottom:
                    self._top, self._bottom = self._bottom, self._top
        return self

    def to_region(self):
        """
        用一个几何面对象表示矩形对象所表示的范围。返回的面对象的点坐标顺序为：第一个点表示左上点，第二个点表示右上点，第三个点表示右下点，
        第四个点表示左下点，第五个点与第一个点坐标相同。

        :return: 返回由矩形范围所表示的几何面对象
        :rtype: GeoRegion

        >>> rc = Rectangle(2.0, 20, 3.0, 10)
        >>> geoRegion = rc.to_region()
        >>> print(geoRegion.area)
        10.0
        """
        pnts = list(self.points)
        pnts.append(pnts[0])
        return GeoRegion(pnts)

    def contains(self, item):
        """
        判断一个点对象或矩形矩形是否在当前矩形对象内部

        :param Point2D item: 二维点对象（含有x和y两个属性）或矩形对象。矩形对象要求非空（矩形对象是否为空，可以参考 @Rectangle.is_empty）
        :return: 待判断的对象在当前矩形内部返回 True，否则为 False
        :rtype: bool

        >>> rect = Rectangle(1.0, 20, 2.0, 3)
        >>> rect.contains(Point2D(1.1,10))
        True
        >>> rect.contains(Point2D(0,0))
        False
        >>> rect.contains(Rectangle(1.0,10,1.5,5))
        True

        """
        if isinstance(item, Rectangle):
            points = item.points
            if self.contains(points[0]):
                if self.contains(points[1]):
                    if self.contains(points[2]):
                        if self.contains(points[3]):
                            return True
            return False
        else:
            x = float(item.x)
            y = float(item.y)
            if self.left <= x <= self.right:
                if self.bottom <= y <= self.top:
                    return True
            return False

    def has_intersection(self, item):
        """
        判断一个二维点、矩形对象或空间几何对象是否与当前矩形对象相交。待判断的对象只要与当前矩形对象有相交区域或者接触都会判定为相交。

        :param Point2D  item: 待判断的二维点对象、矩形对象和空间几何对象，空间几何对象支持点线面和文本对象。
        :return: 判断相交返回True，否则返回False
        :rtype: bool

        >>> rc = Rectangle(1,2,2,1)
        >>> rc.has_intersection(Rectangle(0,1.5,1.5,0))
        True
        >>> rc.has_intersection(GeoLine([Point2D(0,0),Point2D(3,3)]))
        True
        """
        if self.is_empty():
            return False
        if isinstance(item, Point2D):
            return self.contains(item)
        if isinstance(item, Rectangle):
            if item.is_empty():
                return False
                if self.left <= item.left <= self.right:
                    if self.bottom <= item.top <= self.top:
                        return True
                    elif self.left <= item.left <= self.right:
                        if self.bottom <= item.bottom <= self.top:
                            return True
                    if self.left <= item.right <= self.right:
                        if self.bottom <= item.top <= self.top:
                            return True
            elif self.left <= item.right <= self.right:
                if self.bottom <= item.bottom <= self.top:
                    return True
            return False
        else:
            if isinstance(item, Geometry):
                return get_jvm().com.supermap.data.Geometrist.has_intersection(self.to_region()._jobject, item._jobject)
            raise Exception("unsupported input, required Rectangle or Geometry, buf not is " + str(type(item)))

    @property
    def center(self):
        """ Point2D: 返回当前矩形对象的中心点 """
        return Point2D((self.right + self.left) / 2.0, (self.top + self.bottom) / 2.0)

    @property
    def width(self):
        """float: 返回当前矩形对象的宽度值"""
        return abs(self.right - self.left)

    @property
    def height(self):
        """ float: 返回当前矩形对象的高度值 """
        return abs(self.top - self.bottom)

    def inflate(self, dx, dy):
        """
        对当前矩形对象在垂直(y方向）和水平(x方向）进行缩放。缩放完成后将会改变当前对象上下或左右值，但中心点不变。

        :param float dx: 水平方向缩放量
        :param float dy: 垂直方向缩放量
        :return: self
        :rtype: Rectangle

        >>> rc = Rectangle(1,2,2,1)
        >>> rc.inflate(3,None)
        (-2.0, 1.0, 5.0, 2.0)
        >>> rc.left == -2
        True
        >>> rc.right == 5
        True
        >>> rc.top == 2
        True
        >>> rc.inflate(0, 2)
        (-2.0, -1.0, 5.0, 4.0)
        >>> rc.left == -2
        True
        >>> rc.top == 4
        True

        """
        if self.is_empty():
            raise ValueError("Rectangle is empty")
        if dx is not None:
            self._set_left_right(self.left - dx, self.right + dx)
        if dy is not None:
            self._set_top_bottom(self.bottom - dy, self.top + dy)
        return self

    def is_emptyParse error at or near `RETURN_VALUE' instruction at offset 74

    def offset(self, dx, dy):
        """
        将此矩形在 x 方向平移 dx，在 y 方向平移 dy，此方法将改变当前对象。

        :param float dx: 水平偏移该位置的量。
        :param float dy: 垂直偏移该位置的量。
        :return: self
        :rtype: Rectangle

        >>> rc = Rectangle(1,2,2,1)
        >>> rc.offset(2,3)
        (3.0,4.0, 4.0, 5.0)
        """
        if self.is_empty():
            raise ValueError("Rectangle is empty")
        if dx is not None:
            self._set_left_right(self.left + float(dx), self.right + float(dx))
        if dy is not None:
            self._set_top_bottom(self.bottom + float(dy), self.top + float(dy))
        return self

    def union(self, rc):
        """
        当前矩形对象合并指定的矩形对象，合并完成后，矩形的范围将会是合并前的矩形与指定的矩形对象的并集。

        :param Rectangle rc: 指定的用于合并的矩形对象
        :return: self
        :rtype: Rectangle

        >>> rc = Rectangle(1,1,2,2)
        >>> rc.union(Rectangle(0,-2,1,0))
        (0.0, -2.0, 2.0, 2.0)
        """
        if self.is_empty():
            raise ValueError("Rectangle is empty")
        if rc.is_empty():
            raise ValueError("Input Rectangle is empty")
        rc = Rectangle.make(rc)
        self._set_left_right(min(self.left, rc.left), max(self.right, rc.right))
        self._set_top_bottom(min(self.bottom, rc.bottom), max(self.top, rc.top))
        return self

    def intersect(self, rc):
        """
        指定矩形对象与当前对象求交集，并改变当前矩形对象。

        :param Rectangle rc: 用于进行求交操作的矩形
        :return: 当前对象，self
        :rtype: Rectangle

        >>> rc = Rectangle(1,1,2,2)
        >>> rc.intersect(Rectangle(0,0,1.5,1.5))
        (1.0, 1.0, 1.5, 1.5)

        """
        if self.is_empty():
            raise ValueError("Rectangle is empty")
        if rc.is_empty():
            raise ValueError("Input Rectangle is empty")
        rc = Rectangle.make(rc)
        self._set_left_right(max(self.left, rc.left), min(self.right, rc.right))
        self._set_top_bottom(max(self.bottom, rc.bottom), min(self.top, rc.top))
        return self

    def to_tuple(self):
        """
        得到一个元组对象，元组对象的元素分别为矩形的左、下、右、上

        :rtype: tuple
        """
        return (
         self.left, self.bottom, self.right, self.top)

    def to_json(self):
        """
        得到矩形对象的 json 字符串形式

        :rtype: str

        >>> Rectangle(1,1,2,2).to_json()
        '{"rectangle": [1.0, 1.0, 2.0, 2.0]}'

        """
        return json.dumps({"rectangle": (self.to_tuple())})

    @staticmethod
    def from_json(value):
        """
        从 json 字符串中构造一个矩形对象。

        :param str value: json 字符串
        :return: 矩形对象
        :rtype: Rectangle

        >>> s = '{"rectangle": [1.0, 1.0, 2.0, 2.0]}'
        >>> Rectangle.from_json(s)
        (1.0, 1.0, 2.0, 2.0)

        """
        d = json.loads(value)["rectangle"]
        return Rectangle(d[0], d[1], d[2], d[3])

    def to_dict(self):
        """
        将矩形对象返回为一个字典对象

        :rtype: dict
        """
        return {'left':self.left, 
         'bottom':self.bottom,  'right':self.right,  'top':self.top}

    def from_dict(self, value):
        """
        从一个字典对象中读取矩形对象的边界值。读取成功后将会覆盖矩形对象现有的值。

        :param dict value: 字典对象，字典对象的keys 必须有 'left', 'top', 'right', 'bottom'
        :return: 返回当前对象，self
        :rtype: Rectangle
        """
        self.set_left(value["left"])
        self.set_top(value["top"])
        self.set_right(value["right"])
        self.set_bottom(value["bottom"])
        return self

    @staticmethod
    def make_from_dict(value):
        """
        从一个字典对象中构造出矩形对象。

        :param value: 字典对象，字典对象的keys 必须有 'left', 'top', 'right', 'bottom'
        :rtype: Rectangle

        """
        return Rectangle().from_dict(value)

    @staticmethod
    def make(value):
        """
        构造一个二维矩形对象

        :param value: 含有二维矩形对象左、下、右、上的信息
        :type value: Rectangle or list or str or dict
        :return:
        :rtype:
        """
        if isinstance(value, Rectangle):
            return value
            if isinstance(value, (list, tuple)):
                if len(value) == 4:
                    return Rectangle(value[0], value[1], value[2], value[3])
        elif isinstance(value, str):
            from .._utils import split_input_list_from_str
            value = value.strip().replace("[", "").replace("]", "").replace('"', "")
            tokens = split_input_list_from_str(value)
            if len(tokens) == 4:
                return Rectangle(tokens[0], tokens[1], tokens[2], tokens[3])
        elif isinstance(value, dict):
            return Rectangle().from_dict(value)
        return


class Geometry(JVMBase):
    __doc__ = "\n    几何对象基类，用于表示地理实体的空间特征。并提供相关的处理方法。根据地理实体的空间特征不同，分别用点（GeoPoint），线(GeoLine)，面(GeoRegion)等加以描述\n    "

    def __init__(self):
        JVMBase.__init__(self)

    @staticmethod
    def _make_geo_instance(geo_type):
        _geoType = GeometryType._make(geo_type)
        if _geoType is GeometryType.GEOPOINT:
            geo = GeoPoint()
        else:
            if _geoType is GeometryType.GEOLINE:
                geo = GeoLine()
            else:
                if _geoType is GeometryType.GEOREGION:
                    geo = GeoRegion()
                else:
                    if _geoType is GeometryType.GEOREGION3D:
                        geo = GeoRegion3D()
                    else:
                        if _geoType is GeometryType.GEOTEXT:
                            geo = GeoText()
                        else:
                            if _geoType is GeometryType.GEOPOINT3D:
                                geo = GeoPoint3D()
                            else:
                                if _geoType is GeometryType.GEOLINE3D:
                                    geo = GeoLine3D()
                                else:
                                    if _geoType is GeometryType.GEOBOX:
                                        geo = GeoBox()
                                    else:
                                        if _geoType is GeometryType.GEOCIRCLE3D:
                                            geo = GeoCircle3D()
                                        else:
                                            if _geoType is GeometryType.GEOCYLINDER:
                                                geo = GeoCylinder()
                                            else:
                                                if _geoType is GeometryType.GEOMODEL3D:
                                                    geo = GeoModel3D()
                                                else:
                                                    if _geoType is GeometryType.GEOLINEM:
                                                        geo = GeoLineM()
                                                    else:
                                                        geo = Geometry()
        return geo

    @staticmethod
    def _from_java_object(j_geometry):
        if j_geometry is None:
            return
        geo = Geometry._make_geo_instance(j_geometry.getType().name())
        geo._java_object = j_geometry
        return geo

    def _make_java_object(self):
        if self._java_object is None:
            self._create_java_object()
        return self._java_object

    def _create_java_object(self):
        pass

    @property
    def bounds(self):
        """Rectangle: 返回几何对象的最小外接矩形。点对象的最小外接矩形退化为一个点，即矩形的左边界坐标值等于其右边界坐标值，上边界坐标值等于其
        下边界的坐标值，分别为该点的 x 坐标和 y 坐标。 """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return Rectangle._from_java_object(self._jobject.getBounds())

    @property
    def type(self):
        """GeometryType: 返回几何对象类型"""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return GeometryType._make(self._jobject.getType().name())

    @property
    def id(self):
        """int: 返回几何对象的 ID """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jobject.getID()

    def set_id(self, value):
        """
        设置几何对象的 ID 值

        :param int value: ID 值。
        :return: self
        :rtype: Geometry
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        temp_id = int(value)
        if 0 < temp_id < INT32_MAX:
            self._jobject.setID(temp_id)
        return self

    def _set_bounds(self, bounds):
        """
        设置几何对象的最小外接矩形。使用此接口应该格外小心，除非确保设置的 Bounds 是几何对象的真正范围。

        :param Rectangle bounds: 几何对象的最小外接矩形
        :return: self
        :rtype: Geometry
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        if isinstance(bounds, Rectangle):
            self._jobject.setBounds(bounds._jobject)
        return self

    def get_inner_point(self):
        """
        获取几何对象的内点

        :rtype: Point2D
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            return Point2D._from_java_object(self._jobject.getInnerPoint())
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def hit_test(self, point, tolerance):
        """
        测试在指定容限允许的范围内，指定的点是否在几何对象的范围内。即判断以测试点为圆心，以指定的容限为半径的圆是否与该几何对象有交集，若有交集，
        则返回 True；否则返回 False。

        :param Point2D point:  测试点
        :param float tolerance: 容限值，单位与数据集的单位相同
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            if tolerance is None:
                tolerance = 1e-10
            return self._jobject.hitTest(point._jobject, float(tolerance))
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

        return False

    def is_empty(self):
        """
        判断几何对象是否为空值，不同的几何对象的是否为空的条件各异。

        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            return self._jobject.isEmpty()
        except Exception as e:
            try:
                log_error(e)
                raise e
            finally:
                e = None
                del e

    def set_empty(self):
        """清空几何对象中的空间数据，但几何对象的标识符和几何风格保持不变。"""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self._jobject.setEmpty()
        except Exception as e:
            try:
                log_error(e)
                raise e
            finally:
                e = None
                del e

    def offset(self, dx, dy):
        """
        将此几何对象偏移指定的量。

        :param float dx: 偏移 X 坐标的量
        :param float dy: 偏移 Y 坐标的量
        :return: self
        :rtype: Geometry
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self._jobject.offset(dx, dy)
        except Exception as e:
            try:
                log_error(e)
                raise e
            finally:
                e = None
                del e

    def resize(self, rc):
        """
        缩放此几何对象，使其最小外接矩形等于指定的矩形对象。
        对于几何点，该方法只改变其位置，将其移动到指定的矩形的中心点；对于文本对象，该方法将缩放文本大小。

        :param Rectangle rc: 调整大小后几何对象的范围。
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        rc = Rectangle.make(rc)
        try:
            self._jobject.resize(rc._jobject)
        except Exception as e:
            try:
                log_error(e)
                raise e
            finally:
                e = None
                del e

    def rotate(self, base_point, angle):
        """
        以指定点为基点将此几何对象旋转指定角度，逆时针方向为正方向，角度以度为单位。

        :param Point2D base_point: 旋转的基点。
        :param float angle: 旋转的角度，单位为度
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        base_point = Point2D.make(base_point)
        try:
            self._jobject.rotate(base_point._jobject, float(angle))
        except Exception as e:
            try:
                log_error(e)
                raise e
            finally:
                e = None
                del e

    def from_xml(self, xml):
        """
        根据传入的 XML 字符串重新构造几何对象。该 XML 必须符合 GML3.0 规范。
        调用该方法时，首先将该几何对象的原始数据清空，然后根据传入的 XML 字符串重新构造该几何对象。
        GML (Geography Markup Language)即地理标识语言， GML 能够表示地理空间对象的空间数据和非空间属性数据。GML 是基于 XML 的空间信息编码
        标准，由开放式地理信息系统协会 OpenGIS Consortium (OGC) 提出，得到了许多公司的大力支持，如 Oracle、Galdos、MapInfo、CubeWerx 等。
        GML 作为一个空间数据编码规范，提供了一套基本的标签、公共的数据模型，以及用户构建应用模式（GML Application Schemas）的机制。

        :param str xml:  XML 格式的字符串
        :return: 构造成功返回 True，否则返回 False。
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            return self._jobject.fromXML(xml)
        except Exception as e:
            try:
                log_error(e)
                raise e
            finally:
                e = None
                del e

    def to_xml(self):
        """
        根据 GML 3.0 规范，将该几何对象的空间数据输出为 XML 字符串。 注意：几何对象输出的 XML 字符串只含有该几何对象的地理坐标值，不含有该几何对象的风格和 ID 等信息。

        :rtype: str
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            return self._jobject.toXML()
        except Exception as e:
            try:
                log_error(e)
                raise e
            finally:
                e = None
                del e

    def clone(self):
        """
        拷贝对象

        :rtype: Geometry
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        geo = self._jobject.clone()
        if geo is not None:
            return Geometry._from_java_object(geo)
        return

    def _get_sjson_type_name(self):
        _type_name = {(GeometryType.GEOPOINT): "Point", 
         (GeometryType.GEOLINE): "Line", 
         (GeometryType.GEOREGION): "Region", 
         (GeometryType.GEOTEXT): "Text", 
         (GeometryType.GEOPOINT3D): "Point3D", 
         (GeometryType.GEOLINE3D): "Line3D", 
         (GeometryType.GEOREGION3D): "Region3D", 
         (GeometryType.GEOCIRCLE3D): "Circle3D", 
         (GeometryType.GEOCYLINDER): "Cylinder", 
         (GeometryType.GEOBOX): "Box", 
         (GeometryType.GEOLINEM): "LineM"}
        return _type_name[self.type]

    def to_json(self):
        """
        将当前对象输出为 json 字符串

        :rtype: str
        """
        pass

    @staticmethod
    def from_json(value):
        """
        从 json 中构造一个几何对象。参考 :py:meth:`to_json`

        :param str value: json 字符串
        :rtype: Geometry
        """
        d = json.loads(value)
        return Geometry._from_dict(d)

    @staticmethod
    def _from_dict(d):
        if "geometry" in d:
            d = d["geometry"]
        elif "Point" in d:
            geo_type = GeometryType.GEOPOINT
        else:
            if "Line" in d:
                geo_type = GeometryType.GEOLINE
            else:
                if "Region" in d:
                    geo_type = GeometryType.GEOREGION
                else:
                    if "Text" in d:
                        geo_type = GeometryType.GEOTEXT
                    else:
                        if "Point3D" in d:
                            geo_type = GeometryType.GEOPOINT3D
                        else:
                            if "Line3D" in d:
                                geo_type = GeometryType.GEOLINE3D
                            else:
                                if "Region3D" in d:
                                    geo_type = GeometryType.GEOREGION3D
                                else:
                                    if "Box" in d:
                                        geo_type = GeometryType.GEOBOX
                                    else:
                                        if "Circle3D" in d:
                                            geo_type = GeometryType.GEOCIRCLE3D
                                        else:
                                            if "Cylinder" in d:
                                                geo_type = GeometryType.GEOCYLINDER
                                            else:
                                                if "LineM" in d:
                                                    geo_type = GeometryType.GEOLINEM
                                                else:
                                                    return
        geo = Geometry._make_geo_instance(geo_type)
        geo._from_json(d)
        return geo

    def to_geojson(self):
        """
        将当前对象信息以  geojson 格式返回。只支持点、线和面对象。

        :rtype: str
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jvm.com.supermap.data.Toolkit.GeometryToGeoJson(self._jobject)

    @staticmethod
    def from_geojson(geojson):
        """
        从 geojson 中读取信息构造一个几何对象

        :param str geojson: geojson 字符串
        :return: 几何对象
        :rtype: Geometry
        """
        return Geometry._from_java_object(get_jvm().com.supermap.data.Toolkit.GeoJsonToGeometry(geojson))

    def __str__(self):
        return self.to_json()

    def linear_extrude(self, height=0.0, twist=0.0, scaleX=1.0, scaleY=1.0, bLonLat=False):
        """
        线性拉伸，支持二维和三维矢量面,二三维圆,GeoRectangle
        :param height: 拉伸高度
        :param twist: 旋转角度
        :param scaleX: 绕X轴缩放
        :param scaleY: 绕Y轴缩放
        :param bLonLat: 是否是经纬度
        :return: 返回GeoModel3D对象
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        if self.type != GeometryType.GEOREGION:
            if self.type != GeometryType.GEOREGION3D:
                if self.type != GeometryType.GEOCIRCLE:
                    if self.type != GeometryType.GEOCIRCLE3D:
                        if self.type != GeometryType.GEORECTANGLE:
                            raise TypeError("require type GeoRegion or GeoRegion3D")
        if height < 0:
            raise ValueError("height should greater than 0")
        geo = self._jvm.com.supermap.realspace.threeddesigner.ModelBuilder3D.linearExtrude(self._jobject, bLonLat, float(height), float(twist), float(scaleX), float(scaleY))
        if geo != None:
            geo = GeoModel3D._from_java_object(geo)
        return geo

    def rotate_extrude(self, angle, slices):
        """
        旋转拉伸，支持二维和三维矢量面，必须在平面坐标系下构建且不能跨Y轴
        :param angle: 旋转角度
        :return: 返回GeoModel3D对象
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        if self.type != GeometryType.GEOREGION:
            if self.type != GeometryType.GEOLINE:
                raise TypeError("require type GeoRegion or GeoLine")
        if slices <= 0:
            raise ValueError("slices should greater than 0")
        rotateExtrudeP = get_jvm().com.supermap.realspace.threeddesigner.RotateExtrudeParameter()
        rotateExtrudeP.setAngle(float(angle))
        rotateExtrudeP.setSlices(int(slices))
        geo = self._jvm.com.supermap.realspace.threeddesigner.ModelBuilder3D.rotateExtrude(self._jobject, rotateExtrudeP)
        if geo != None:
            geo = GeoModel3D._from_java_object(geo)
        return geo

    @staticmethod
    def _from_pb_bytes(bys):
        """
        从 protobuf bytes 中构造对象,支持点线面

        :param bys: protobuf 字节数组
        :type bys: bytearray
        :return: 几何对象，支持点线面
        :rtype: Geometry
        """
        return Geometry._from_java_object(get_jvm().com.supermap.jsuperpy.serializer.SerializerUtil.deserializeGeometry(bys))

    def _to_pb_bytes(self):
        """
        对当前几何对象序列化为 protobuf bytes

        :return: protobuf 字节数组
        :rtype: bytearray
        """
        return get_jvm().com.supermap.jsuperpy.serializer.SerializerUtil.serializeGeometry(self._jobject)

    def get_style(self):
        """
        获取几何对象的对象风格

        :rtype: GeoStyle
        """
        return GeoStyle._from_java_object(self._java_object.getStyle())

    def set_style(self, style):
        """
        设置几何对象风格

        :param GeoStyle style: 几何对象风格
        :return: 返回对象自身
        :rtype: Geometry
        """
        if isinstance(style, GeoStyle):
            from .._utils import oj
            self._java_object.setStyle(oj(style))
        else:
            raise ValueError("required GeoStyle")
        return self


class GeoPoint(Geometry):
    __doc__ = "\n    点几何对象类。\n    该类一般用于描述点状地理实体。Point2D 和 GeoPoint 都可用来表示二维点，所不同的是 GeoPoint 描述的是地物实体，而 Point2D 描述的是一个位\n    置点；当赋予 GeoPoint 不同的几何风格，即可用于表示不同的地物实体，而 Point2D 则是广泛用于定位的坐标点\n    "

    def __init__(self, point=None):
        """
        构造一个点几何对象。

        :param point: 点对象
        :type point: Point2D  or GeoPoint or tuple[float] or list[float]
        """
        Geometry.__init__(self)
        if isinstance(point, Point2D):
            point = point
        else:
            if isinstance(point, GeoPoint):
                point = point.point
            else:
                if isinstance(point, (tuple, list)) and len(point) > 1:
                    point = Point2D(point[0], point[1])
                else:
                    point = Point2D.make(point)
        if point is not None:
            self._jobject.setX(float(point.x))
            self._jobject.setY(float(point.y))

    def __getstate__(self):
        return (self.point, self.id)

    def __setstate__(self, state):
        if len(state) != 2:
            raise Exception("state length required 2 but " + str(len(state)))
        self.__init__(state[0])
        self.set_id(state[1])

    def _create_java_object(self):
        self._java_object = self._jvm.com.supermap.data.GeoPoint()
        return self

    @property
    def point(self):
        """
        返回点几何对象的地理位置

        :rtype: Point2D
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return Point2D(self._jobject.getX(), self._jobject.getY())

    def set_point(self, point):
        """
        设置点几何对象的地理位置

        :param Point2D point: 点几何对象的地理位置
        :return: self
        :rtype: GeoPoint
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self._jobject.setX(point.x)
        self._jobject.setY(point.y)
        return self

    def set_x(self, x):
        """
        设置点几何对象的 X 坐标

        :param float x: X 坐标值
        :return: self
        :rtype: GeoPoint
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self._jobject.setX(float(x) if x is not None else None)
        return self

    def get_x(self):
        """
        获取点几何对象的 X 坐标值

        :rtype: float
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jobject.getX()

    def set_y(self, y):
        """
        设置点几何对象的 Y 坐标

        :param float y: Y 坐标值
        :return: self
        :rtype: GeoPoint
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self._jobject.setY(float(y) if y is not None else None)
        return self

    def get_y(self):
        """
        获取点几何对象的 Y 坐标值

        :rtype: float
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jobject.getY()

    @property
    def bounds(self):
        """
        Rectangle: 获取点几何对象的地理范围
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        pnt = self.point
        return Rectangle(pnt.x, pnt.y, pnt.x, pnt.y)

    def create_buffer(self, distance, prj=None, unit=None):
        """
        在当前位置点构造一个缓冲区对象

        :param float distance: 缓冲区半径。如果设置了 prj 和 unit，将使用 unit 的单位作为缓冲区半径的单位。
        :param PrjCoordSys prj: 描述点几何对象的投影信息
        :param unit: 缓冲区半径单位
        :type unit: Unit or str
        :return: 缓冲区半径
        :rtype: GeoRegion
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        from .prj import PrjCoordSys
        prj = PrjCoordSys.make(prj)
        from ._util import create_geometry_buffer
        return create_geometry_buffer(self, distance, prj, unit)

    def _to_dict(self):
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        d = OrderedDict()
        d[self._get_sjson_type_name()] = [self.get_x(), self.get_y()]
        d["id"] = self.id
        return d

    def to_json(self):
        """
        将当前点对象以 simple json 格式返回。

        例如::

            >>> geo = GeoPoint((10,20))
            >>> print(geo.to_json())
            {"Point": [10.0, 20.0], "id": 0}

        :return: simple json 格式字符串
        :rtype: str
        """
        return json.dumps(self._to_dict())

    def _from_json(self, d):
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.set_id(d["id"])
        point = d[self._get_sjson_type_name()]
        self.set_x(point[0])
        self.set_y(point[1])


class GeoPoint3D(Geometry):
    __doc__ = "\n    点几何对象类。\n    该类一般用于描述点状地理实体。Point3D 和 GeoPoint3D 都可用来表示三维点，所不同的是 GeoPoint3D 描述的是地物实体，而 Point3D 描述的是一个位\n    置点；当赋予 GeoPoint3D 不同的几何风格，即可用于表示不同的地物实体，而 Point3D 则是广泛用于定位的坐标点\n    "

    def __init__(self, point=None):
        """
        构造一个点几何对象。

        :param point: 点对象
        :type point: Point3D  or GeoPoint3D or tuple[float] or list[float]
        """
        Geometry.__init__(self)
        if isinstance(point, Point3D):
            _p = point
        else:
            if isinstance(point, GeoPoint3D):
                _p = point.point
            else:
                if isinstance(point, (tuple, list)) and len(point) > 2:
                    _p = Point3D(point[0], point[1], point[2])
                else:
                    _p = Point3D.make(point)
        if _p is not None:
            self._jobject.setX(float(point.x))
            self._jobject.setY(float(point.y))
            self._jobject.setZ(float(point.z))

    def __getstate__(self):
        return (self.point, self.id)

    def __setstate__(self, state):
        if len(state) != 2:
            raise Exception("state length required 2 but " + str(len(state)))
        self.__init__(state[0])
        self.set_id(state[1])

    def _create_java_object(self):
        self._java_object = self._jvm.com.supermap.data.GeoPoint3D()
        return self

    @property
    def point(self):
        """
        返回点几何对象的地理位置

        :rtype: Point3D
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return Point3D(self._jobject.getX(), self._jobject.getY(), self._jobject.getZ())

    def set_point(self, point):
        """
        设置点几何对象的地理位置

        :param Point3D point: 点几何对象的地理位置
        :return: self
        :rtype: GeoPoint
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self._jobject.setX(point.x)
        self._jobject.setY(point.y)
        self._jobject.setZ(point.z)
        return self

    def set_x(self, x):
        """
        设置点几何对象的 X 坐标

        :param float x: X 坐标值
        :return: self
        :rtype: GeoPoint3D
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self._jobject.setX(float(x) if x is not None else None)
        return self

    def get_x(self):
        """
        获取点几何对象的 X 坐标值

        :rtype: float
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jobject.getX()

    def set_y(self, y):
        """
        设置点几何对象的 Y 坐标

        :param float y: Y 坐标值
        :return: self
        :rtype: GeoPoint3D
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self._jobject.setY(float(y) if y is not None else None)
        return self

    def get_y(self):
        """
        获取点几何对象的 Y 坐标值

        :rtype: float
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jobject.getY()

    def set_z(self, z):
        """
        设置点几何对象的 z 坐标

        :param float z: Z 坐标值
        :return: self
        :rtype: GeoPoint3D
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self._jobject.setY(float(z) if z is not None else None)
        return self

    def get_z(self):
        """
        获取点几何对象的 Z 坐标值

        :rtype: float
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jobject.getZ()

    @property
    def bounds(self):
        """
        Rectangle: 获取点几何对象的地理范围
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        pnt = self.point
        return Rectangle(pnt.x, pnt.y, pnt.x, pnt.y)

    def _to_dict(self):
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        d = OrderedDict()
        d[self._get_sjson_type_name()] = [self.get_x(), self.get_y(), self.get_z()]
        d["id"] = self.id
        return d

    def to_json(self):
        """
        将当前点对象以 simple json 格式返回。

        例如::

            >>> geo = GeoPoint3D((10,20,15))
            >>> print(geo.to_json())
            {"Point3D": [10.0, 20.0], "id": 0}

        :return: simple json 格式字符串
        :rtype: str
        """
        return json.dumps(self._to_dict())

    def _from_json(self, d):
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        if "id" in d:
            self.set_id(d["id"])
        point = d[self._get_sjson_type_name()]
        self.set_x(point[0])
        self.set_y(point[1])
        self.set_z(point[2])


class GeoLine(Geometry):
    __doc__ = "\n    线几何对象类。\n    该类用于描述线状地理实体，如河流，道路，等值线等，一般用一个或多个有序坐标点集合来表示。线的方向决定于有序坐标点的顺序，也可以通过调用 reverse\n    方法来改变线的方向。线对象由一个或多个部分组成，每个部分称为线对象的一个子对象，每个子对象用一个有序坐标点集合来表示。可以对子对象进行添加，删除，\n    修改等操作。\n\n    "

    def __init__(self, points=None):
        """
        构造一个线几何对象

        :param points: 包含点串信息的对象，可以为 list[Point2D] 、tuple[Point2D] 、 GeoLine 、GeoRegion 和 Rectangle
        :type points: list[Point2D] or tuple[Point2D] or GeoLine or GeoRegion or Rectangle
        """
        Geometry.__init__(self)
        if points is not None:
            if isinstance(points, (list, tuple)):
                java_point2ds = self._jvm.com.supermap.data.Point2Ds()
                for p in points:
                    pnt = Point2D.make(p)
                    if pnt is not None:
                        java_point2ds.add(pnt._jobject)

                if java_point2ds.getCount() >= 2:
                    self._jobject.addPart(java_point2ds)
            elif isinstance(points, GeoLine):
                self._java_object = self._jvm.com.supermap.data.GeoLine(points._jobject)
            else:
                if isinstance(points, GeoRegion):
                    self._java_object = self._jvm.com.supermap.data.GeoLine(points._jobject.convertToLine())
                else:
                    if isinstance(points, Rectangle):
                        java_point2ds = self._jvm.com.supermap.data.Point2Ds()
                        for p in points.points:
                            java_point2ds.add(p._jobject)

                        java_point2ds.add(points.points[0]._jobject)
                        self._jobject.addPart(java_point2ds)

    def _create_java_object(self):
        self._java_object = self._jvm.com.supermap.data.GeoLine()
        return self

    def __getitem__(self, item):
        return self.get_part(item)

    def __setitem__(self, item, value):
        if item < 0:
            item += self.get_part_count()
        points = self._jvm.com.supermap.data.Point2Ds()
        for p in value:
            points.add(p._jobject)

        self._jobject.setPart(item, points)

    def get_part_count(self):
        """
        获取子对象的个数

        :rtype: int
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jobject.getPartCount()

    def convert_to_region(self):
        """
        将当前线对象转换为面几何对象
        - 对于没有封闭的线对象，转换为面对象时，会把首尾自动连起来
        - GeoLine 对象实例的某个子对象的点数少于 3 时将失败

        :rtype: GeoRegion
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return Geometry._from_java_object(self._jobject.convertToRegion())

    def __getstate__(self):
        return (
         self.get_parts(), self.id, self.bounds)

    def __setstate__(self, state):
        if len(state) != 3:
            raise Exception("state length required 3 but " + str(len(state)))
        self.__init__()
        points = state[0]
        for pnts in points:
            if len(pnts) >= 2:
                self.add_part(pnts)

        self.set_id(int(state[1]))
        self._set_bounds(state[2])

    def remove_part(self, item):
        """
        删除此线几何对象中的指定序号的子对象。

        :param int item: 指定的子对象的序号
        :return: 成功则返回 true，否则返回 false
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        if item < 0:
            item += self.get_part_count()
        return self._jobject.removePart(item)

    def insert_part(self, item, points):
        """
        此线几何对象中的指定位置插入一个子对象。成功则返回 True，否则返回 False

        :param int item: 插入的位置
        :param list[Point2D] points: 插入的有序点集合
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        if item < 0:
            item += self.get_part_count()
        java_points = self._jvm.com.supermap.data.Point2Ds()
        for p in points:
            java_points.add(Point2D.make(p)._jobject)

        return self._jobject.insertPart(item, java_points)

    def add_part(self, points):
        """
        向此线几何对象追加一个子对象。成功返回添加的子对象的序号。

        :param list[Point2D] points: 一个有序点集
        :rtype: int
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        java_points = self._jvm.com.supermap.data.Point2Ds()
        for p in points:
            java_points.add(p._jobject)

        return self._jobject.addPart(java_points)

    def get_part(self, item):
        """
        返回此线几何对象中指定序号的子对象，以有序点集合的方式返回该子对象。 当二维线对象是简单线对象时，如果传入参数0，得到的是此线对象的节点的集合。

        :param int item: 子对象的序号。
        :return: 子对象的的节点
        :rtype: list[Point2D]
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        if item < 0:
            item += self.get_part_count()
        points = self._jobject.getPart(item)
        pnts = []
        for i in range(points.getCount()):
            p = points.getItem(i)
            pnts.append(Point2D(p.getX(), p.getY()))

        return pnts

    @property
    def length(self):
        """float: 返回线对象的长度"""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jobject.getLength()

    def clone(self):
        """
        复制对象

        :rtype: GeoLine
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        geoLine = GeoLine()
        java_geoLine = self._jobject.clone()
        geoLine._java_object = java_geoLine
        return geoLine

    def find_point_on_line_by_distance(self, distance):
        """
        在线上以指定的距离找点，查找的起始点为线的起始点。
        - 当 distance 大于 Length 时，返回线最后一个子对象的终点。
        - 当 distance=0 时，返回线几何对象的起始点；
        - 当线几何对象具有多个子对象的时候，按照子对象的序号依次查找

        :param float distance: 要找点的距离
        :return: 查找成功返回要找的点，否则返回 None
        :rtype: Point2D
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return Point2D._from_java_object(self._jobject.findPointOnLineByDistance(float(distance)))

    def create_buffer(self, distance, prj=None, unit=None):
        """
        构建当前线对象的缓冲区对象。将会构建线对象的圆头全缓冲区。

        :param float distance: 缓冲区半径。如果设置了 prj 和 unit，将使用 unit 的单位作为缓冲区半径的单位。
        :param PrjCoordSys prj: 描述点几何对象的投影信息
        :param unit: 缓冲区半径单位
        :type unit: Unit or str
        :return: 缓冲区半径
        :rtype: GeoRegion
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        from .prj import PrjCoordSys
        prj = PrjCoordSys.make(prj)
        from ._util import create_geometry_buffer
        return create_geometry_buffer(self, distance, prj, unit)

    def get_parts(self):
        """
        获取当前几何对象的所有点坐标。每个子对象使用一个 list 存储

        >>> points = [Point2D(1,2),Point2D(2,3)]
        >>> geo = GeoLine(points)
        >>> geo.add_part([Point2D(3,4),Point2D(4,5)])
        >>> print(geo.get_parts())
        [[(1.0, 2.0), (2.0, 3.0)], [(3.0, 4.0), (4.0, 5.0)]]

        :return: 包含所有点坐标list
        :rtype: list[list[Point2D]]
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        parts = []
        for i in range(self.get_part_count()):
            parts.append(self.get_part(i))

        return parts

    def _to_dict(self):
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        d = OrderedDict()
        points = []
        for i in range(self.get_part_count()):
            part = self[i]
            dp = [[p.x, p.y] for p in part]
            points.append(dp)

        d[self._get_sjson_type_name()] = points
        d["id"] = self.id
        return d

    def to_json(self):
        """
        将当前对象输出为 Simple Json 字符串

        >>> points = [Point2D(1,2), Point2D(2,3), Point2D(1,5), Point2D(1,2)]
        >>> geo = GeoLine(points)
        >>> print(geo.to_json())
        {"Line": [[[1.0, 2.0], [2.0, 3.0], [1.0, 5.0], [1.0, 2.0]]], "id": 0}

        :rtype: str
        """
        return json.dumps(self._to_dict())

    def _from_json(self, d):
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        if "id" in d:
            self.set_id(d["id"])
        points = d[self._get_sjson_type_name()]
        for part in points:
            self.add_part([Point2D(p[0], p[1]) for p in part])


class GeoLineM(Geometry):
    __doc__ = "\n    路由对象。是一组具有 X，Y 坐标与线性度量值的点组成的线性地物对象。M 值是所谓的 Measure 值，即度量值。在交通网络分析中常用于\n    标注一条线路的不同点距离某一点的距离。比如高速公路上的里程碑，交通管制部门经常使用高速公路上的里程碑来标注并管理高速公路的路况、\n    车辆的行驶限速和高速事故点等。\n    "

    def __init__(self, points=None):
        """
        构造一个路由对象

        :param points: 包含点串信息的对象，可以为 list[PointM] 、tuple[PointM] 、 GeoLineM
        :type points: list[PointM] 、tuple[PointM] 、 GeoLineM
        """
        Geometry.__init__(self)
        if points is not None:
            if isinstance(points, (list, tuple)):
                java_pointms = self._jvm.com.supermap.data.PointMs()
                for p in points:
                    pnt = PointM.make(p)
                    if pnt is not None:
                        java_pointms.add(oj(pnt))

                if java_pointms.getCount() >= 2:
                    self._jobject.addPart(java_pointms)
            elif isinstance(points, GeoLineM):
                self._java_object = self._jvm.com.supermap.data.GeoLineM(oj(points))

    def _create_java_object(self):
        self._java_object = self._jvm.com.supermap.data.GeoLineM()
        return self

    def __getitem__(self, item):
        return self.get_part(item)

    def __setitem__(self, item, value):
        if item < 0:
            item += self.get_part_count()
        points = self._jvm.com.supermap.data.PointMs()
        for p in value:
            points.add(oj(p))

        self._jobject.setPart(item, points)

    def get_part_count(self):
        """
        获取子对象的个数

        :rtype: int
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jobject.getPartCount()

    def convert_to_region(self):
        """
        将当前对象转换为面几何对象
        - 对于没有封闭的对象，转换为面对象时，会把首尾自动连起来
        - GeoLineM 对象实例的某个子对象的点数少于 3 时将失败

        :rtype: GeoRegion
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return Geometry._from_java_object(self._jobject.convertToRegion())

    def convert_to_line(self):
        """
        将该路由对象转换为二维线几何对象，成功返回线几何对象。

        :rtype: GeoLine
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return Geometry._from_java_object(self._jobject.convertToLine())

    def __getstate__(self):
        return (
         self.get_parts(), self.id, self.bounds)

    def __setstate__(self, state):
        if len(state) != 3:
            raise Exception("state length required 3 but " + str(len(state)))
        self.__init__()
        points = state[0]
        for pnts in points:
            if len(pnts) >= 2:
                self.add_part(pnts)

        self.set_id(int(state[1]))
        self._set_bounds(state[2])

    def remove_part(self, item):
        """
        删除此对象中的指定序号的子对象。

        :param int item: 指定的子对象的序号
        :return: 成功则返回 true，否则返回 false
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        if item < 0:
            item += self.get_part_count()
        return self._jobject.removePart(item)

    def insert_part(self, item, points):
        """
        在当前对中的指定位置插入一个子对象。成功则返回 True，否则返回 False

        :param int item: 插入的位置
        :param list[PointM] points: 插入的有序点集合
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        if item < 0:
            item += self.get_part_count()
        java_points = self._jvm.com.supermap.data.PointMs()
        for p in points:
            java_points.add(oj(PointM.make(p)))

        return self._jobject.insertPart(item, java_points)

    def add_part(self, points):
        """
        向当前对象追加一个子对象。成功返回添加的子对象的序号。

        :param list[PointM] points: 一个有序点集
        :rtype: int
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        java_points = self._jvm.com.supermap.data.PointMs()
        for p in points:
            java_points.add(oj(PointM.make(p)))

        return self._jobject.addPart(java_points)

    def get_part(self, item):
        """
        返回当前对象中指定序号的子对象，以有序点集合的方式返回该子对象。 当当前对象是简单路由对象时，如果传入参数0，
        得到的是此对象的节点的集合。

        :param int item: 子对象的序号。
        :return: 子对象的的节点
        :rtype: list[PointM]
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        if item < 0:
            item += self.get_part_count()
        points = self._jobject.getPart(item)
        pnts = []
        for i in range(points.getCount()):
            p = points.getItem(i)
            pnts.append(PointM(p.getX(), p.getY(), p.getM()))

        return pnts

    @property
    def length(self):
        """float: 返回当前对象的长度"""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jobject.getLength()

    def clone(self):
        """
        复制对象

        :rtype: GeoLineM
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        geoLine = GeoLineM()
        java_geoLine = self._jobject.clone()
        geoLine._java_object = java_geoLine
        return geoLine

    def get_parts(self):
        """
        获取当前对象的所有点坐标。每个子对象使用一个 list 存储

        :return: 包含所有点坐标list
        :rtype: list[list[PointM]]
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        parts = []
        for i in range(self.get_part_count()):
            parts.append(self.get_part(i))

        return parts

    def _to_dict(self):
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        d = OrderedDict()
        points = []
        for i in range(self.get_part_count()):
            part = self[i]
            dp = [[p.x, p.y, p.m] for p in part]
            points.append(dp)

        d[self._get_sjson_type_name()] = points
        d["id"] = self.id
        return d

    def to_json(self):
        """
        将当前对象输出为 Simple Json 字符串

        :rtype: str
        """
        return json.dumps(self._to_dict())

    def _from_json(self, d):
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        if "id" in d:
            self.set_id(d["id"])
        points = d[self._get_sjson_type_name()]
        for part in points:
            self.add_part([PointM(p[0], p[1], p[2]) for p in part])

    def get_max_measure(self):
        """
        返回最大线性度量值

        :rtype: float
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jobject.getMaxM()

    def get_min_measure(self):
        """
        返回最小线性度量值。

        :rtype: float
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jobject.getMaxM()

    def get_measure_at_distance(self, distance, is_ignore_gap=True, sub_index=-1):
        """
        返回指定距离处的点对象的 M 值。

        :param float distance: 指定的距离。该距离指的是到路由线路起点的距离。单位与该路由对象所属数据集的单位相同。
        :param bool is_ignore_gap: 是否忽略子对象之间的距离。
        :param int sub_index: 待返回的路由子对象的序号。如果为 -1，则从第一个对象开始计算，否则从指定的子对象开始计算。
        :return: 指定距离处的点对象的 M 值。
        :rtype: float
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        if sub_index >= 0:
            return self._jobject.getMAtDistance(float(distance), int(sub_index), bool(is_ignore_gap))
        return self._jobject.getMAtDistance(float(distance), bool(is_ignore_gap))

    def get_measure_at_point(self, point, tolerance, is_ignore_gap):
        """
        返回路由对象指定点处的 M 值。

        :param Point2D point: 指定的点对象。
        :param float tolerance: 容限值。用于判断指定的点是否在路由对象上，若点到路由对象垂足的距离大于该值，则视为指定的点无效，
                                不执行返回。单位与该路由对象所属数据集的单位相同。
        :param bool is_ignore_gap: 是否忽略子对象之间的间距。
        :return: 路由对象指定点处的 M 值。
        :rtype: float
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        point = Point2D.make(point)
        if point is None:
            raise ValueError("point required Point2D")
        return self._jobject.getMAtPoint(oj(point), float(tolerance), bool(is_ignore_gap))

    def get_distance_at_measure(self, measure, is_ignore_gap=True, sub_index=-1):
        """
        返回指定 M 值对应的点对象到指定路由子对象起点的距离。

        :param float measure: 指定的 M 值。
        :param bool is_ignore_gap:  指定是否忽略子对象之间的距离。
        :param int sub_index:  指定的路由子对象的索引值。如果为 -1，则从第一个子对象开始计算，否则从指定的子对象开始计算
        :return: 指定 M 值对应的点对象到指定路由子对象起点的距离。单位与该路由对象所属数据集的单位相同。
        :rtype: float
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        if sub_index >= 0:
            return self._jobject.getDistanceAtM(float(measure), int(sub_index), bool(is_ignore_gap))
        return self._jobject.getDistanceAtM(float(measure), bool(is_ignore_gap))

    def find_point_on_line_by_distance(self, distance):
        """
        在线上以指定的距离找点，查找的起始点为线的起始点。
        - 当 distance 大于 Length 时，返回线最后一个子对象的终点。
        - 当 distance=0 时，返回线几何对象的起始点；
        - 当线几何对象具有多个子对象的时候，按照子对象的序号依次查找

        :param float distance: 要找点的距离
        :return: 查找成功返回要找的点，否则返回 None
        :rtype: Point2D
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return Point2D._from_java_object(self._jobject.findPointOnLineByDistance(float(distance)))


class GeoRegion(Geometry):
    __doc__ = "\n    面几何对象类，派生于 Geometry 类。\n\n    该类用于描述面状地理实体，如行政区域，湖泊，居民地等，一般用一个或多个有序坐标点集合来表示。面几何对象由一个或多个部分组成，每个部分称为面几何对\n    象的一个子对象，每个子对象用一个有序坐标点集合来表示，其起始点和终止点重合。可以对子对象进行添加，删除，修改等操作。\n    "

    def __init__(self, points=None):
        """
        构造一个面几何对象

        :param points: 包含点串信息的对象，可以为 list[Point2D] 、tuple[Point2D] 、 GeoLine 、GeoRegion 和 Rectangle
        :type points: list[Point2D] or tuple[Point2D] or GeoLine or GeoRegion or Rectangle
        """
        Geometry.__init__(self)
        if points is not None:
            if isinstance(points, (list, tuple)):
                java_point2ds = self._jvm.com.supermap.data.Point2Ds()
                for p in points:
                    pnt = Point2D.make(p)
                    if pnt is not None:
                        java_point2ds.add(pnt._jobject)

                if java_point2ds.getCount() > 2:
                    self._jobject.addPart(java_point2ds)
            elif isinstance(points, GeoRegion):
                self._java_object = self._jvm.com.supermap.data.GeoRegion(points._jobject)
            else:
                if isinstance(points, GeoLine):
                    self._java_object = self._jvm.com.supermap.data.GeoRegion(points._jobject.convertToRegion())
                else:
                    if isinstance(points, Rectangle):
                        java_point2ds = self._jvm.com.supermap.data.Point2Ds()
                        for p in points.points:
                            java_point2ds.add(p._jobject)

                        java_point2ds.add(points[0]._jobject)
                        self._jobject.addPart(java_point2ds)

    @property
    def area(self):
        """float: 返回面对象的面积"""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jobject.getArea()

    @property
    def perimeter(self):
        """float: 返回面对象的周长"""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jobject.getPerimeter()

    def get_precise_area(self, prj):
        """
        精确计算投影参考系下多边形的面积

        :param prj: 指定的投影坐标系
        :type prj: PrjCoordSys
        :return: 二维面几何对象的面积
        :rtype: float
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        from .prj import PrjCoordSys
        prj = PrjCoordSys.make(prj)
        if prj is None:
            raise ValueError("prj is None")
        return self._jobject.getPreciseArea(prj._jobject)

    def get_parts_topology(self):
        """
        判断面对象的子对象之间的岛洞关系。 岛洞关系数组是由 1 和 -1 两个数值组成,数组大小与面对象的子对象相同。其中， 1 表示子对象为岛， -1 表示子对象为洞。

        :rtype: list[int]
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jobject.getPartTopo()

    def _create_java_object(self):
        self._java_object = get_jvm().com.supermap.data.GeoRegion()
        return self

    def __getitem__(self, item):
        return self.get_part(item)

    def __setitem__(self, item, value):
        if item < 0:
            item += self.get_part_count()
        if len(value) < 3:
            raise Exception("points count must be greater than 2")
        points = get_jvm().com.supermap.data.Point2Ds()
        for p in value:
            points.add(p._jobject)

        self._jobject.setPart(item, points)

    def get_part_count(self):
        """
        获取子对象的个数

        :rtype: int
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jobject.getPartCount()

    def convert_to_line(self):
        """
        将当前面对象转换为线对象

        :rtype: GeoLine
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return Geometry._from_java_object(self._jobject.convertToLine())

    def __getstate__(self):
        return (
         self.get_parts(), self.id, self.bounds)

    def __setstate__(self, state):
        if len(state) != 3:
            raise Exception("state length required 3 but " + str(len(state)))
        self.__init__()
        points = state[0]
        for pnts in points:
            if len(pnts) > 2:
                self.add_part(pnts)

        self.set_id(int(state[1]))
        self._set_bounds(state[2])

    def create_buffer(self, distance, prj=None, unit=None):
        """
        构建当前面对象的缓冲区对象

        :param float distance: 缓冲区半径。如果设置了 prj 和 unit，将使用 unit 的单位作为缓冲区半径的单位。
        :param PrjCoordSys prj: 描述点几何对象的投影信息
        :param unit: 缓冲区半径单位
        :type unit: Unit or str
        :return: 缓冲区半径
        :rtype: GeoRegion
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        from .prj import PrjCoordSys
        prj = PrjCoordSys.make(prj)
        from ._util import create_geometry_buffer
        return create_geometry_buffer(self, distance, prj, unit)

    def protected_decompose(self):
        """
        面对象保护性分解。区别于组合对象将子对象进行简单分解，保护性分解将复杂的具有多层岛洞嵌套关系的面对象分解成只有一层嵌套关系的面对象。 面对象
        中有子对象部分交叠的情形不能保证分解的合理性。

        :return: 保护性分解后得到的对象。
        :rtype: list[GeoRegion]
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            if self.get_part_count() > 1:
                geos = self._jobject.protectedDecompose()
                if geos is not None:
                    return [Geometry._from_java_object(geo) for geo in geos]
                return
            else:
                return [
                 self.clone()]
        except Exception as e:
            try:
                log_error(e)
                return
            finally:
                e = None
                del e

    def is_counter_clockwise(self, sub_index):
        """
        判断面对象的子对象的走向。true 表示走向为逆时针，false 表示走向为顺时针。

        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jobject.isCounterClockwise(sub_index)

    def contains(self, point):
        """
        判断点是否在面内

        :param point: 待判断的二维点对象
        :type point: Point2D or GeoPoint
        :return: 点在面内返回 True，否则返回\u3000False
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        elif isinstance(point, Point2D):
            java_point = self._jvm.com.supermap.data.GeoPoint(float(point.x), float(point.y))
        else:
            if isinstance(point, GeoPoint):
                java_point = point._jobject
            else:
                raise ValueError("invalid point, required Point or GeoPoint")
        return self._jvm.com.supermap.data.Geometrist.isWithin(java_point, self._jobject)

    def add_part(self, points):
        """
        向此面几何对象追加一个子对象。成功返回添加的子对象的序号。

        :param list[Point2D] points: 一个有序点集
        :rtype: int
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        java_points = self._jvm.com.supermap.data.Point2Ds()
        for p in points:
            java_points.add(p._jobject)

        return self._jobject.addPart(java_points)

    def remove_part(self, item):
        """
        删除此面几何对象中的指定序号的子对象。

        :param int item: 指定的子对象的序号
        :return: 成功则返回 true，否则返回 false
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        if item < 0:
            item += self.get_part_count()
        return self._jobject.removePart(item)

    def insert_part(self, item, points):
        """
        此面几何对象中的指定位置插入一个子对象。成功则返回 True，否则返回 False

        :param int item: 插入的位置
        :param list[Point2D] points: 插入的有序点集合
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        if item < 0:
            item += self.get_part_count()
        java_points = self._jvm.com.supermap.data.Point2Ds()
        for p in points:
            java_points.add(p._jobject)

        return self._jobject.insertPart(item, java_points)

    def get_part(self, item):
        """
        返回此面几何对象中指定序号的子对象，以有序点集合的方式返回该子对象。

        :param int item: 子对象的序号。
        :return: 子对象的的节点
        :rtype: list[Point2D]
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        if item < 0:
            item += self.get_part_count()
        points = self._jobject.getPart(item)
        pnts = []
        for i in range(points.getCount()):
            p = points.getItem(i)
            pnts.append(Point2D(p.getX(), p.getY()))

        return pnts

    def get_parts(self):
        """
        获取当前几何对象的所有点坐标。每个子对象使用一个 list 存储

        >>> points = [Point2D(1,2), Point2D(2,3), Point2D(1,5), Point2D(1,2)]
        >>> geo = GeoRegion(points)
        >>> geo.add_part([Point2D(2,3), Point2D(4,3), Point2D(4,2), Point2D(2,3)])
        >>> geo.get_parts()
        [[(1.0, 2.0), (2.0, 3.0), (1.0, 5.0), (1.0, 2.0)],
        [(2.0, 3.0), (4.0, 3.0), (4.0, 2.0), (2.0, 3.0)]]

        :return: 包含所有点坐标list
        :rtype: list[list[Point2D]]
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        parts = []
        for i in range(self.get_part_count()):
            parts.append(self.get_part(i))

        return parts

    def _to_dict(self):
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        d = OrderedDict()
        points = []
        for i in range(self.get_part_count()):
            part = self[i]
            dp = [[p.x, p.y] for p in part]
            points.append(dp)

        d[self._get_sjson_type_name()] = points
        d["id"] = self.id
        return d

    def to_json(self):
        """
        将当前对象输出为 Simple Json 字符串

        >>> points = [Point2D(1,2), Point2D(2,3), Point2D(1,5), Point2D(1,2)]
        >>> geo = GeoRegion(points)
        >>> print(geo.to_json())
        {"Region": [[[1.0, 2.0], [2.0, 3.0], [1.0, 5.0], [1.0, 2.0]]], "id": 0}

        :rtype: str
        """
        return json.dumps(self._to_dict())

    def _from_json(self, d):
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        if "id" in d:
            self.set_id(d["id"])
        points = d[self._get_sjson_type_name()]
        for part in points:
            self.add_part([Point2D(p[0], p[1]) for p in part])


class TextStyle(object):
    __doc__ = "\n    文本风格类。 用于设置 :py:class:`GeoText` 类对象的风格\n    "

    def __init__(self):
        self._stringAlignment = None
        self._borderSpacingWidth = None
        self._fontName = None
        self._italicAngle = None
        self._bold = None
        self._fontScale = None
        self._fontWidth = None
        self._outline = None
        self._shadow = None
        self._underline = None
        self._weight = None
        self._backOpaque = None
        self._opaqueRate = None
        self._outlineWidth = None
        self._rotation = None
        self._foreColor = None
        self._fontHeight = None
        self._italic = None
        self._backColor = None
        self._alignment = None
        self._sizeFixed = None
        self._strikeout = None

    def __str__(self):
        return str(self.to_dict())

    def set_string_alignment(self, value):
        """
        设置文本的排版方式，可以对多行文本设置左对齐、右对齐、居中对齐、两端对齐

        :param value: 文本的排版方式
        :type value: StringAlignment
        :return: self
        :rtype: TextStyle
        """
        self._stringAlignment = StringAlignment._make(value)
        return self

    @property
    def string_alignment(self):
        """StringAlignment: 文本的排版方式"""
        return self._stringAlignment

    @property
    def border_spacing_width(self):
        """int: 返回文字背景矩形框边缘与文字边缘的间隔，单位为：像素"""
        return self._borderSpacingWidth

    def set_border_spacing_width(self, value):
        """
        设置文字背景矩形框边缘与文字边缘的间隔，单位为：像素。

        :param int value:
        :return: self
        :rtype: TextStyle
        """
        if value is not None:
            self._borderSpacingWidth = int(value)
        return self

    def set_fore_color(self, value):
        """
        设置文本的前景色

        :param value: 文本的前景色
        :type value: int or tuple
        :return: self
        :rtype: TextStyle
        """
        value = Color.make(value)
        if value is not None:
            self._foreColor = color_to_tuple(value)
        return self

    def set_alignment(self, value):
        """
        设置文本的对齐方式

        :param value:  文本的对齐方式
        :type value: TextAlignment or str
        :return: self
        :rtype: TextStyle
        """
        self._alignment = TextAlignment._make(value)
        return self

    def set_bold(self, value):
        """
        设置文本是否为粗体字，True 表示为粗体

        :param bool value: 文本是否为粗体字
        :return: self
        :rtype: TextStyle
        """
        if value is not None:
            self._bold = bool(value)
        return self

    def set_size_fixed(self, value):
        """
        设置文本大小是否固定。False，表示文本为非固定尺寸的文本。

        :param bool value: 文本大小是否固定。False，表示文本为非固定尺寸的文本。
        :return: self
        :rtype: TextStyle
        """
        if value is not None:
            self._sizeFixed = bool(value)
        return self

    @property
    def font_name(self):
        """str: 返回文本字体的名称。如果在Windows平台下对地图中的文本图层指定了某种字体，并且该地图数据需要在Linux平台下进行应用，那么请确保您
        的Linux平台下也存在同样的字体，否则，文本图层的字体显示效果会有问题。文本字体的名称的默认值为 "Times New Roman"。 """
        return self._fontName

    @property
    def italic_angle(self):
        """float: 返回字体倾斜角度，正负度之间，以度为单位，精确到0.1度。当倾斜角度为0度，为系统默认的字体倾斜样式。
        正负度是指以纵轴为起始零度线，其纵轴左侧为正，右侧为负。允许的最大角度为60，最小-60。大于60按照60处理，小于-60按照-60处理。"""
        return self._italicAngle

    def set_underline(self, value):
        """
        设置文本字体是否加下划线。True 表示加下划线。

        :param bool value: 文本字体是否加下划线。True 表示加下划线
        :return: self
        :rtype: TextStyle
        """
        if value is not None:
            self._underline = bool(value)
        return self

    def set_font_scale(self, value):
        """
        设置注记字体的缩放比例

        :param float value: 注记字体的缩放比例
        :return: self
        :rtype: TextStyle
        """
        if value is not None:
            self._fontScale = float(value)
        return self

    @property
    def is_bold(self):
        """bool: 返回文本是否为粗体字，True 表示为粗体"""
        return self._bold

    def set_rotation(self, value):
        """
        设置文本旋转的角度。逆时针方向为正方向，单位为度。

        :param float value: 文本旋转的角度
        :return: self
        :rtype: TextStyle
        """
        if value is not None:
            self._rotation = float(value)
        return self

    @property
    def font_scale(self):
        """float: 注记字体的缩放比例"""
        return self._fontScale

    def set_italic_angle(self, value):
        """
        设置字体倾斜角度，正负度之间，以度为单位，精确到0.1度。当倾斜角度为0度，为系统默认的字体倾斜样式。
        正负度是指以纵轴为起始零度线，其纵轴左侧为正，右侧为负。允许的最大角度为60，最小-60。大于60按照60处理，小于-60按照-60处理。

        :param float value: 字体倾斜角度，正负度之间，以度为单位，精确到0.1度
        :return: self
        :rtype: TextStyle
        """
        if value is not None:
            self._italicAngle = float(value)
        return self

    @property
    def font_width(self):
        """float: 文本的宽度。字体的宽度以英文字符为标准，由于一个中文字符相当于两个英文字符。在固定大小时单位为1毫米，否则使用地理坐标单位。"""
        return self._fontWidth

    def set_outline(self, value):
        """
        设置是否以轮廓的方式来显示文本的背景。false，表示不以轮廓的方式来显示文本的背景。

        :param bool value: 是否以轮廓的方式来显示文本的背景
        :return: self
        :rtype: TextStyle
        """
        if value is not None:
            self._outline = bool(value)
        return self

    def set_opaque_rate(self, value):
        """
        设置注记文字的不透明度。不透明度的范围为0-100。

        :param int value: 注记文字的不透明度
        :return: self
        :rtype: TextStyle
        """
        if value is not None:
            self._opaqueRate = int(value)
        return self

    @property
    def is_outline(self):
        """bool: 返回是否以轮廓的方式来显示文本的背景"""
        return self._outline

    def set_font_height(self, value):
        """
        设置文本字体的高度。在固定大小时单位为1毫米，否则使用地理坐标单位。

        :param float value: 文本字体的高度
        :return: self
        :rtype: TextStyle
        """
        if value is not None:
            self._fontHeight = float(value)
        return self

    @property
    def is_shadow(self):
        """bool: 文本是否有阴影。True 表示给文本增加阴影 """
        return self._shadow

    def set_shadow(self, value):
        """
        设置文本是否有阴影。True 表示给文本增加阴影

        :param bool value: 文本是否有阴影
        :return: self
        :rtype: TextStyle
        """
        if value is not None:
            self._shadow = bool(value)
        return self

    @property
    def is_underline(self):
        """bool: 文本字体是否加下划线。True 表示加下划线。"""
        return self._underline

    @property
    def weight(self):
        """float: 文本字体的磅数，表示粗体的具体数值。取值范围为从0－900之间的整百数，如400表示正常显示，700表示为粗体，可参见微软 MSDN 帮助中
        关于 LOGFONT 类的介绍。默认值为400"""
        return self._weight

    @property
    def is_back_opaque(self):
        """bool: 文本背景是否不透明，True 表示文本背景不透明。 默认不透明"""
        return self._backOpaque

    @property
    def opaque_rate(self):
        """int: 设置注记文字的不透明度。不透明度的范围为0-100。 """
        return self._opaqueRate

    @property
    def outline_width(self):
        """float: 文本轮廓的宽度，数值的单位为：像素，数值范围是从0到5之间的任意整数。"""
        return self._outlineWidth

    @property
    def rotation(self):
        """float: 文本旋转的角度。逆时针方向为正方向，单位为度。 """
        return self._rotation

    @property
    def fore_color(self):
        """tuple: 文本的前景色，默认色为黑色。 """
        return self._foreColor

    def set_back_color(self, value):
        """
        设置文本的背景色。

        :param value: 文本的背景色
        :type value: int or tuple
        :return: self
        :rtype: TextStyle
        """
        if value is not None:
            self._backColor = Color.make(value)
        return self

    def set_strikeout(self, value):
        """
        设置文本字体是否加删除线。

        :param bool value:  文本字体是否加删除线。
        :return: self
        :rtype: TextStyle
        """
        if value is not None:
            self._strikeout = bool(value)
        return self

    def set_font_width(self, value):
        """
        设置文本的宽度。字体的宽度以英文字符为标准，由于一个中文字符相当于两个英文字符。在固定大小时单位为1毫米，否则使用地理坐标单位。

        :param float value: 文本的宽度
        :return: self
        :rtype: TextStyle
        """
        if value is not None:
            self._fontWidth = float(value)
        return self

    def set_outline_width(self, value):
        """
        设置文本轮廓的宽度，数值的单位为：像素，数值范围是从0到5之间的任意整数，其中设置为0值时表示没有轮廓。 必须通过方法 :py:meth:`is_outline` 为
        True 时，文本轮廓的宽度设置才有效。

        :param int value: 文本轮廓的宽度，数值的单位为：像素，数值范围是从0到5之间的任意整数，其中设置为0值时表示没有轮廓。
        :return: self
        :rtype: TextStyle
        """
        if value is not None:
            self._outlineWidth = int(value)
        return self

    @property
    def font_height(self):
        """float: 文本字体的高度。在固定大小时单位为1毫米，否则使用地理坐标单位。默认值为 6。 """
        return self._fontHeight

    @property
    def is_italic(self):
        """bool: 文本是否采用斜体，True 表示采用斜体"""
        return self._italic

    def set_italic(self, value):
        """
        设置文本是否采用斜体，true 表示采用斜体。

        :param bool value: 文本是否采用斜体
        :return: self
        :rtype: TextStyle
        """
        self._italic = value
        return self

    def set_back_opaque(self, value):
        """
        设置文本背景是否不透明，True 表示文本背景不透明

        :param bool value: 文本背景是否不透明
        :return: self
        :rtype: TextStyle
        """
        self._backOpaque = value
        return self

    def set_weight(self, value):
        """
        设置文本字体的磅数，表示粗体的具体数值。取值范围为从0－900之间的整百数，如400表示正常显示，700表示为粗体，可参见微软 MSDN 帮助中关于
        LOGFONT 类的介绍

        :param int value: 文本字体的磅数。
        :return: self
        :rtype: TextStyle
        """
        self._weight = value
        return self

    @property
    def back_color(self):
        """tuple: 文本的背景色，默认颜色为黑色"""
        return self._backColor

    @property
    def alignment(self):
        """TextAlignment: 文本的对齐方式。"""
        return self._alignment

    def set_font_name(self, value):
        """
        设置文本字体的名称。 如果在Windows平台下对地图中的文本图层指定了某种字体，并且该地图数据需要在Linux平台下进行应用，那么请确保您的Linux
        平台下也存在同样的字体，否则，文本图层的字体显示效果会有问题。

        :param str value: 文本字体的名称。文本字体的名称的默认值为 "Times New Roman"。
        :return: self
        :rtype: TextStyle
        """
        if value is not None:
            self._fontName = str(value)
        return self

    @property
    def is_size_fixed(self):
        """bool: 文本大小是否固定。False，表示文本为非固定尺寸的文本"""
        return self._sizeFixed

    @property
    def is_strikeout(self):
        """bool: 文本字体是否加删除线。True 表示加删除线。"""
        return self._strikeout

    @property
    def _jobject(self):
        java_obj = get_jvm().com.supermap.data.TextStyle()
        if self.string_alignment is not None:
            java_obj.setStringAlignment(self.string_alignment._jobject)
        if self.border_spacing_width is not None:
            java_obj.setBorderSpacingWidth(self.border_spacing_width)
        if self.fore_color is not None:
            java_obj.setForeColor(tuple_to_java_color(self.fore_color))
        if self.alignment is not None:
            java_obj.setAlignment(self.alignment._jobject)
        if self.is_bold is not None:
            java_obj.setBold(self.is_bold)
        if self.is_size_fixed is not None:
            java_obj.setSizeFixed(self.is_size_fixed)
        if self.is_underline is not None:
            java_obj.setUnderline(self.is_underline)
        if self.font_scale is not None:
            java_obj.setFontScale(self.font_scale)
        if self.rotation is not None:
            java_obj.setRotation(self.rotation)
        if self.italic_angle is not None:
            java_obj.setItalicAngle(self.italic_angle)
        if self.is_outline is not None:
            java_obj.setOutline(self.is_outline)
        if self.opaque_rate is not None:
            java_obj.setOpaqueRate(self.opaque_rate)
        if self.font_height is not None:
            java_obj.setFontHeight(self.font_height)
        if self.is_shadow is not None:
            java_obj.setShadow(self.is_shadow)
        if self.back_color is not None:
            java_obj.setBackColor(tuple_to_java_color(self.back_color))
        if self.is_strikeout is not None:
            java_obj.setStrikeout(self.is_strikeout)
        if self.font_width is not None:
            java_obj.setFontWidth(self.font_width)
        if self.outline_width is not None:
            java_obj.setOutlineWidth(self.outline_width)
        if self.is_italic is not None:
            java_obj.setItalic(self.is_italic)
        if self.is_back_opaque is not None:
            java_obj.setBackOpaque(self.is_back_opaque)
        if self.weight is not None:
            java_obj.setWeight(self.weight)
        if self.font_name is not None:
            java_obj.setFontName(self.font_name)
        return java_obj

    @staticmethod
    def _from_java_object(java_obj):
        if not java_obj:
            return
        obj = TextStyle()
        obj.set_string_alignment(StringAlignment._make(java_obj.getStringAlignment().name()))
        obj.set_border_spacing_width(java_obj.getBorderSpacingWidth())
        obj.set_font_name(java_obj.getFontName())
        obj.set_italic_angle(java_obj.getItalicAngle())
        obj.set_bold(java_obj.getBold())
        obj.set_font_scale(java_obj.getFontScale())
        obj.set_font_width(java_obj.getFontWidth())
        obj.set_outline(java_obj.getOutline())
        obj.set_shadow(java_obj.getShadow())
        obj.set_underline(java_obj.getUnderline())
        obj.set_weight(java_obj.getWeight())
        obj.set_back_opaque(java_obj.getBackOpaque())
        obj.set_opaque_rate(java_obj.getOpaqueRate())
        obj.set_outline_width(java_obj.getOutlineWidth())
        obj.set_rotation(java_obj.getRotation())
        obj.set_fore_color(java_color_to_tuple(java_obj.getForeColor()))
        obj.set_font_height(java_obj.getFontHeight())
        obj.set_italic(java_obj.getItalic())
        obj.set_back_color(java_color_to_tuple(java_obj.getBackColor()))
        obj.set_alignment(TextAlignment._make(java_obj.getAlignment().name()))
        obj.set_size_fixed(java_obj.isSizeFixed())
        obj.set_strikeout(java_obj.getStrikeout())
        return obj

    @staticmethod
    def make_from_dict(values):
        """
        从 dict 中读取文本风格信息构造 TextStyle

        :param dict values: 包含文本风格信息的 dict
        :rtype: TextStyle
        """
        return TextStyle().from_dict(values)

    def from_dict(self, values):
        """
        从 dict 中读取文本风格信息

        :param dict values: 包含文本风格信息的 dict
        :return: self
        :rtype: TextStyle
        """
        if "border_spacing_width" in values.keys():
            self.set_border_spacing_width(values["border_spacing_width"])
        if "string_alignment" in values.keys():
            self.set_string_alignment(values["string_alignment"])
        if "is_bold" in values.keys():
            self.set_bold(values["is_bold"])
        if "is_italic" in values.keys():
            self.set_italic(values["is_italic"])
        if "fore_color" in values.keys():
            self.set_fore_color(values["fore_color"])
        if "font_height" in values.keys():
            self.set_font_height(values["font_height"])
        if "is_outline" in values.keys():
            self.set_outline(values["is_outline"])
        if "is_strikeout" in values.keys():
            self.set_strikeout(values["is_strikeout"])
        if "font_scale" in values.keys():
            self.set_font_scale(values["font_scale"])
        if "opaque_rate" in values.keys():
            self.set_opaque_rate(values["opaque_rate"])
        if "alignment" in values.keys():
            self.set_alignment(values["alignment"])
        if "is_size_fixed" in values.keys():
            self.set_size_fixed(values["is_size_fixed"])
        if "font_width" in values.keys():
            self.set_font_width(values["font_width"])
        if "rotation" in values.keys():
            self.set_rotation(values["rotation"])
        if "italic_angle" in values.keys():
            self.set_italic_angle(values["italic_angle"])
        if "is_shadow" in values.keys():
            self.set_shadow(values["is_shadow"])
        if "is_underline" in values.keys():
            self.set_underline(values["is_underline"])
        if "outline_width" in values.keys():
            self.set_outline_width(values["outline_width"])
        if "font_name" in values.keys():
            self.set_font_name(values["font_name"])
        if "back_color" in values.keys():
            self.set_back_color(values["back_color"])
        if "weight" in values.keys():
            self.set_weight(values["weight"])
        if "is_back_opaque" in values.keys():
            self.set_back_opaque(values["is_back_opaque"])
        return self

    def to_dict(self):
        """
        将当前对象输出为 dict

        :rtype: dict
        """
        d = dict()
        if self.string_alignment is not None:
            d["string_alignment"] = self.string_alignment.name
        if self.border_spacing_width is not None:
            d["border_spacing_width"] = self.border_spacing_width
        if self.font_name is not None:
            d["font_name"] = self.font_name
        if self.italic_angle is not None:
            d["italic_angle"] = self.italic_angle
        if self.is_bold is not None:
            d["is_bold"] = self.is_bold
        if self.font_scale is not None:
            d["font_scale"] = self.font_scale
        if self.font_width is not None:
            d["font_width"] = self.font_width
        if self.is_outline is not None:
            d["is_outline"] = self.is_outline
        if self.is_shadow is not None:
            d["is_shadow"] = self.is_shadow
        if self.is_underline is not None:
            d["is_underline"] = self.is_underline
        if self.weight is not None:
            d["weight"] = self.weight
        if self.is_back_opaque is not None:
            d["is_back_opaque"] = self.is_back_opaque
        if self.opaque_rate is not None:
            d["opaque_rate"] = self.opaque_rate
        if self.outline_width is not None:
            d["outline_width"] = self.outline_width
        if self.rotation is not None:
            d["rotation"] = self.rotation
        if self.fore_color is not None:
            d["fore_color"] = self.fore_color
        if self.font_height is not None:
            d["font_height"] = self.font_height
        if self.is_italic is not None:
            d["is_italic"] = self.is_italic
        if self.back_color is not None:
            d["back_color"] = self.back_color
        if self.alignment is not None:
            d["alignment"] = self.alignment.name
        if self.is_size_fixed is not None:
            d["is_size_fixed"] = self.is_size_fixed
        if self.is_strikeout is not None:
            d["is_strikeout"] = self.is_strikeout
        return d

    def __getstate__(self):
        return self.to_dict()

    def __setstate__(self, state):
        self.__init__()
        self.from_dict(state)

    def to_json(self):
        """
        输出为 json 字符串

        :rtype: str
        """
        return json.dumps(self.to_dict())

    @staticmethod
    def from_json(value):
        """
        从 json 字符串中构建 TextStyle 对象

        :param str value:
        :rtype: TextStyle
        """
        ts = TextStyle()
        ts.from_dict(json.loads(value))
        return ts

    def clone(self):
        """
        拷贝对象

        :rtype: TextStyle
        """
        return TextStyle.make_from_dict(self.to_dict())


class TextPart(object):
    __doc__ = "\n    文本子对象类。 用于表示文本对象 :py:class:`GeoText` 的子对象，其存储子对象的文本，旋转角度，锚点等信息并提供对子对象进行处理的相关方法。\n    "

    def __init__(self, text=None, anchor_point=None, rotation=None):
        """
        构造文本子对象。

        :param str text:  文本子对象实例的文本内容。
        :param Point2D anchor_point: 文本子对象实例的锚点。
        :param float rotation: 文本子对象的旋转角度，以度为单位，逆时针为正方向。
        """
        self._anchorPoint = None
        self._rotation = None
        self._text = None
        self.set_text(text)
        self.set_anchor_point(anchor_point)
        self.set_rotation(rotation)

    @property
    def anchor_point(self):
        """文本子对象实例的锚点。该锚点与文本的对齐方式共同决定该文本子对象的显示位置。关于锚点与文本的对齐方式如何确定文本子对象的显示位置，
        请参见 :py:class:`TextAlignment` 类。 """
        if self._anchorPoint is None:
            self._anchorPoint = Point2D()
        return self._anchorPoint

    @property
    def rotation(self):
        """文本子对象的旋转角度，以度为单位，逆时针为正方向。"""
        return self._rotation

    def set_x(self, value):
        """
        设置此文本子对象锚点的横坐标

        :param float value: 此文本子对象锚点的横坐标
        :return: self
        :rtype: TextPart
        """
        if value is not None:
            self._anchorPoint.x = float(value)
        return self

    def set_anchor_point(self, value):
        """
        设置此文本子对象的锚点。该锚点与文本的对齐方式共同决定该文本子对象的显示位置。关于锚点与文本的对齐方式如何确定文本子对象的显示位置，请参见 :py:class:`TextAlignment` 类。

        :param Point2D value: 文本子对象的锚点
        :return: self
        :rtype: TextPart
        """
        value = Point2D.make(value)
        self._anchorPoint = Point2D()
        if value is not None:
            self._anchorPoint.x = float(value.x)
            self._anchorPoint.y = float(value.y)
        return self

    @property
    def text(self):
        """str: 此文本子对象的文本内容"""
        return self._text

    @property
    def x(self):
        """float: 文本子对象锚点的横坐标，默认值为0"""
        return self.anchor_point.x

    def set_rotation(self, value):
        """
        设置此文本子对象的旋转角度。逆时针为正方向，单位为度。
        文本子对象通过数据引擎存储后返回的旋转角度，精度为 0.1 度；通过构造函数直接构造的文本子对象，返回的旋转角度精度不变。

        :param float value:  文本子对象的旋转角度
        :return: self
        :rtype: TextPart
        """
        self._rotation = value
        return self

    @property
    def y(self):
        """float: 文本子对象锚点的纵坐标，默认值为0"""
        return self.anchor_point.y

    def set_text(self, value):
        """
        设置文本子对象的文本子内容

        :param str value: 文本子对象的文本子内容
        :return: self
        :rtype: TextPart
        """
        self._text = value
        return self

    def set_y(self, value):
        """
        设置文本子对象锚点的纵坐标

        :param float value: 文本对象锚点的纵坐标
        :return: self
        :rtype: TextPart
        """
        if value is not None:
            self.anchor_point.y = float(value)
        return self

    @property
    def _jobject(self):
        java_obj = get_jvm().com.supermap.data.TextPart()
        if self.anchor_point is not None:
            java_obj.setAnchorPoint(self.anchor_point._jobject)
        if self.rotation is not None:
            java_obj.setRotation(self.rotation)
        if self.text is not None:
            java_obj.setText(self.text)
        return java_obj

    @staticmethod
    def _from_java_object(java_obj):
        obj = TextPart()
        obj.set_anchor_point(Point2D._from_java_object(java_obj.getAnchorPoint()))
        obj.set_rotation(java_obj.getRotation())
        obj.set_text(java_obj.getText())
        return obj

    def to_dict(self):
        """
        将当前子对象输出为 dict

        :rtype: dict
        """
        d = dict()
        if self.anchor_point is not None:
            d["anchor_point"] = [
             self.x, self.y]
        if self.rotation is not None:
            d["rotation"] = self.rotation
        if self.text is not None:
            d["text"] = self.text
        return d

    @staticmethod
    def make_from_dict(values):
        """
        从 dict 中读取信息构造文本子对象

        :param dict values: 文本子对象
        :rtype: TextPart
        """
        return TextPart().from_dict(values)

    def from_dict(self, values):
        """
        从 dict 中读取文本子对象的信息

        :param dict values: 文本子对象
        :return: self
        :rtype: TextPart
        """
        if "anchor_point" in values.keys():
            self.set_anchor_point(values["anchor_point"])
        if "rotation" in values.keys():
            self.set_rotation(values["rotation"])
        if "text" in values.keys():
            self.set_text(values["text"])
        return self

    def __str__(self):
        return "TextPart: " + str(self.text)

    def __repr__(self):
        return "TextPart(%s)" % str(self.text)

    def __getstate__(self):
        return (
         self.text, self.anchor_point, self.rotation)

    def __setstate__(self, state):
        if len(state) != 3:
            raise Exception("state length required 3 but " + str(len(state)))
        self.__init__(state[0], state[1], state[2])

    def to_json(self):
        """
        将当前子对象输出为 json 字符串

        :rtype: str
        """
        return json.dumps(self.to_dict())

    @staticmethod
    def from_json(value):
        """
        从 json 字符串中读取信息构造文本子对象

        :param str value: json 字符串
        :rtype: TextPart
        """
        return TextPart.make_from_dict(json.loads(value))

    def clone(self):
        """
        复制对象

        :rtype: TextPart
        """
        return TextPart(self.text, self.anchor_point, self.rotation)


class GeoText(Geometry):
    __doc__ = "\n    文本类，派生于 Geometry 类。该类主要用于对地物要素进行标识和必要的注记说明。文本对象由一个或多个部分组成，每个部分称为文本对象的一个子对象，每\n    个子对象都是一个 TextPart 的实例。同一个文本对象的所有子对象都使用相同的文本风格，即使用该文本对象的文本风格进行显示。\n\n    "

    def __init__(self, text_part=None, text_style=None):
        """
        构造文本对象

        :param TextPart text_part: 文本子对象。
        :param TextStyle text_style: 文本对象的风格
        """
        Geometry.__init__(self)
        if text_part is not None:
            self._jobject.addPart(text_part._jobject)
        if text_style is not None:
            self._jobject.setStyle(text_style._jobject)

    def __str__(self):
        return "GeoText: " + self.get_text()

    def __getstate__(self):
        return (
         self.get_parts(), self.text_style, self.id)

    def __setstate__(self, state):
        if len(state) != 3:
            raise Exception("state length required 3 but " + str(len(state)))
        self.__init__()
        parts = state[0]
        for part in parts:
            self.add_part(part)

        self.set_text_style(state[1])
        self.set_id(state[2])

    def _create_java_object(self):
        self._java_object = self._jvm.com.supermap.data.GeoText()
        return self

    def add_part(self, text_part):
        """
        增加一个文本子对象

        :param TextPart text_part: 文本子对象
        :return: 当添加成功则返回子对象序号，失败时返回-1。
        :rtype: int
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jobject.addPart(text_part._jobject)

    def get_part(self, index):
        """
        获取指定的文本子对象

        :param int index: 文本子对象的序号
        :return:
        :rtype: int
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return TextPart._from_java_object(self._jobject.getPart(index))

    def get_part_count(self):
        """
        获取文本子对象的数目

        :rtype: int
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jobject.getPartCount()

    @property
    def text_style(self):
        """TextStyle: 文本对象的文本风格。文本风格用于指定文本对象显示时的字体、宽度、高度和颜色等。"""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return TextStyle._from_java_object(self._jobject.getTextStyle())

    def set_text_style(self, text_style):
        """
        设置文本对象的文本风格。文本风格用于指定文本对象显示时的字体、宽度、高度和颜色等。

        :param TextStyle text_style:  文本对象的文本风格。
        :return: self
        :rtype:  GeoText
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self._jobject.setTextStyle(text_style._jobject)
        return self

    def set_part(self, index, text_part):
        """
        修改此文本对象的指定序号的子对象，即用新的文本子对象来替换原来的文本子对象。

        :param int index: 文本子对象序号
        :param TextPart text_part: 文本子对象
        :return: 设置成功返回 True，否则返回 False。
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jobject.setPart(index, text_part._jobject)

    def get_text(self):
        """
        文本对象的内容。 如果该对象有多个子对象时，其值为子对象字符串之和。

        :rtype: str
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jobject.getText()

    def remove_part(self, index):
        """
        删除此文本对象的指定序号的文本子对象。

        :param int index:
        :return: 如果删除成功返回 True，否则返回 False。
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jobject.removePart(index)

    def get_parts(self):
        """
        获取当前文本对象的所有文本子对象

        :rtype: list[TextPart]
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        parts = []
        for i in range(self.get_part_count()):
            parts.append(self.get_part(i))

        return parts

    def _to_dict(self):
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        d = OrderedDict()
        d[self._get_sjson_type_name()] = [self.get_part(i).to_dict() for i in range(self.get_part_count())]
        d["id"] = self.id
        if self.text_style is not None:
            d["text_style"] = self.text_style.to_dict()
        return d

    def to_json(self):
        """
        将当前对象输出为 json 字符串

        :rtype: str
        """
        return json.dumps(self._to_dict())

    def _from_json(self, d):
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        if "id" in d:
            self.set_id(d["id"])
        parts = d[self._get_sjson_type_name()]
        for part in parts:
            self.add_part(TextPart().from_dict(part))

        if "text_style" in d.keys():
            self.set_text_style(TextStyle().from_dict(d["text_style"]))


class Feature(object):
    __doc__ = "\n    特征要素对象，特征要素对象可以用于描述空间信息和属性信息，也可以只用于属性信息的描述。\n    "

    def __init__(self, geometry=None, values=None, id_value='0', field_infos=None):
        """

        :param  Geometry geometry: 几何对象信息
        :param values: 特征要素对象的属性字段值。
        :type values: list or tuple or dict
        :param str id_value: 要素对象 ID
        :param list[FieldInfo] field_infos: 特征要素对con象的属性字段信息
        """
        self._name_indexes = None
        self._field_infos = []
        self._geometry = None
        self._values = []
        self._fid = None
        self.set_geometry(geometry)
        self.set_field_infos(field_infos)
        self.set_values(values)
        self.set_feature_id(id_value)

    def clone(self):
        """
        复制当前对象

        :rtype: Feature
        """
        if self.geometry is not None:
            _geo = self.geometry.clone()
        else:
            _geo = None
        if self.field_infos is not None:
            _fields = list([field.clone() for field in self.field_infos])
        else:
            _fields = None
        return Feature(_geo, (copy.deepcopy(self._values)), field_infos=_fields).set_feature_id(self.feature_id)

    def _init_values_list(self):
        if self._values is None:
            self._values = []
        elif len(self.field_infos) != len(self._values):
            if len(self.field_infos) > len(self._values):
                start = len(self._values)
                while start < len(self.field_infos):
                    if self.field_infos[start].default_value is not None:
                        self._values.append(self.field_infos[start].default_value)
                    else:
                        self._values.append(None)
                    start += 1

        else:
            pos = len(self.field_infos)
            count = len(self._values) - pos
            i = 0
            while i < count:
                del self._values[pos]
                i += 1

        return self

    def _reset_names_index(self, refresh=False):
        if self._name_indexes is None or refresh:
            self._name_indexes = {}
            for i in range(len(self.field_infos)):
                self._name_indexes[self.field_infos[i].name] = i

        return self._name_indexes

    @property
    def field_infos(self):
        """list[FieldInfo]: 返回要素对象的所有字段信息"""
        return self._field_infos

    def set_field_infos(self, field_infos):
        """
        设置属性字段信息

        :param list[FieldInfo] field_infos: 属性字段信息
        :return: self
        :rtype: Feature
        """
        if field_infos is not None:
            for fieldInfo in field_infos:
                self.add_field_info(fieldInfo)

        self._init_values_list()
        return self

    def add_field_info(self, field_info):
        """
        增加一个属性字段。增加一个属性字段后，如果没有属性字段没有设置默认值，将会将属性值设为 None

        :param FieldInfo field_info: 属性字段信息
        :return: 添加成功返回True，否则返回False
        :rtype: bool
        """
        self._reset_names_index()
        if field_info is not None:
            if field_info.name in self._name_indexes.keys():
                log_info("field name is existed in feature :" + field_info.name)
                return False
        self._field_infos.append(field_info)
        self._name_indexes[field_info.name] = len(self._field_infos) - 1
        self._init_values_list()
        return True

    def remove_field_info(self, name):
        """
        删除指定字段名称或序号的字段。删除字段后，字段值也会被删除

        :param name: 字段名称或序号
        :type name: int or str
        :return: 删除成功返回 True，否则返回 False
        :rtype: bool
        """
        self._reset_names_index()
        if name in self._name_indexes.keys():
            _index = self._get_field_index(name)
            del self._field_infos[_index]
            self._reset_names_index(True)
            self._init_values_list()
            return True
        return False

    @property
    def geometry(self):
        """Geometry: 返回几何对象"""
        return self._geometry

    def set_geometry(self, geo):
        """
        设置几何对象

        :param Geometry geo: 几何对象
        :return: self
        :rtype: Feature
        """
        self._geometry = geo
        return self

    @property
    def feature_id(self):
        """str: 返回 Feature ID"""
        return self._fid

    def set_feature_id(self, fid):
        """
        设置 Feature ID

        :param str fid: feature ID 值，一般用于表示要素对象的唯一的ID值
        :return:
        :rtype:
        """
        if fid is not None:
            self._fid = str(fid)
        else:
            self._fid = None
        return self

    @property
    def bounds(self):
        """Rectangle: 获取几何对象的地理范围。如果几何对象为空，则返回空"""
        if self.geometry is not None:
            return self.geometry.bounds
        return

    def _get_field_index(self, value):
        if isinstance(value, int):
            if value >= 0:
                return value
            return len(self.field_infos) + value
        else:
            if isinstance(value, str):
                return self._name_indexes[value]
            raise Exception("invalid value")

    def get_field_info(self, item):
        """
        获取指定名称和序号的字段信息

        :param item: 字段名称或序号
        :type item: str or int
        :rtype: FieldInfo
        """
        item = self._get_field_index(item)
        if isinstance(item, int):
            return self.field_infos[item]
        raise Exception("invalid value")

    def get_value(self, item):
        """
        获取当前对象中指定的属性字段的字段值

        :param item: 字段名称或序号
        :type item: str or int
        :rtype: int or float or str or datetime.datetime or bytes or bytearray
        """
        item = self._get_field_index(item)
        if isinstance(item, int):
            return self._values[item]
        raise ValueError("required field index or name.")

    def set_value(self, item, value):
        """
        设置当前对象中指定的属性字段的字段值

        :param item: 字段名称或序号
        :type item: str or int
        :param value: 字段值
        :type value: int or float or str or datetime.datetime or bytes or bytearray
        :rtype: bool
        """
        item = self._get_field_index(item)
        if value is None:
            self._values[item] = None
            return True
        try:
            fieldInfo = self.get_field_info(item)
            if fieldInfo is None:
                return False
                if fieldInfo.type == FieldType.BOOLEAN:
                    self._values[item] = bool(value)
                else:
                    if fieldInfo.type in (FieldType.CHAR, FieldType.TEXT, FieldType.WTEXT, FieldType.JSONB):
                        self._values[item] = str(value)
                    else:
                        if fieldInfo.type in (FieldType.BYTE, FieldType.INT16, FieldType.INT32, FieldType.INT64):
                            self._values[item] = int(value)
                        else:
                            if fieldInfo.type in (FieldType.SINGLE, FieldType.DOUBLE):
                                self._values[item] = float(value)
                            else:
                                if not fieldInfo.type == FieldType.LONGBINARY or isinstance(value, bytes) or isinstance(value, bytearray):
                                    self._values[item] = value
                                else:
                                    self._values[item] = bytes((str(value)), encoding="utf-8")
            else:
                pass
            if fieldInfo.type == FieldType.DATETIME:
                if isinstance(value, datetime.datetime):
                    self._values[item] = value
                else:
                    if isinstance(value, str):
                        try:
                            self._values[item] = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                        except:
                            self._values[item] = None

                    else:
                        if isinstance(value, int):
                            self._values[item] = datetime.datetime.fromtimestamp(value)
                        else:
                            self._values[item] = None
            return True
        except Exception as e:
            try:
                log_error(e)
                self._values[item] = None
            finally:
                e = None
                del e

        return False

    def get_values(self, exclude_system=True, is_dict=False):
        """
        获取当前对象的属性字段值。

        :param bool exclude_system: 是否包含系统字段。所有 "Sm" 开头的字段都是系统字段。默认为 True
        :param bool is_dict: 是否以 dict 形式返回，如果返回 dict，则 dict  的 key 为字段名称， value 为属性字段值。否则以 list 形式返回字段值。默认为 False
        :return: 属性字段值
        :rtype: dict or list
        """
        if is_dict:
            values = {}
        else:
            values = []
        i = -1
        for field in self.field_infos:
            i += 1
            if exclude_system:
                if field.is_system_field():
                    continue
            if is_dict:
                values[field.name] = self._values[i]
            else:
                values.append(self._values[i])

        return values

    def set_valuesParse error at or near `COME_FROM_LOOP' instruction at offset 114_3

    def __getitem__(self, item):
        return self.get_value(item)

    def __setitem__(self, key, value):
        self.set_value(key, value)

    def to_json(self):
        """
        将当前对象输出为 json 字符串

        :rtype: str
        """
        d = OrderedDict()
        d["Feature"] = self.feature_id
        if self.geometry is not None:
            d["geometry"] = self.geometry._to_dict()
        if self.field_infos is not None:
            if len(self.field_infos) > 0:
                d["fields"] = [field.to_json() for field in self.field_infos]
        values = self.get_values(False, False)
        if values is not None:
            if len(values) > 0:
                _values = []
                for v in values:
                    if v is not None:
                        if isinstance(v, (int, float, str)):
                            _values.append(v)
                        elif isinstance(v, datetime.datetime):
                            _values.append(v.strftime("%Y-%m-%d %H:%M:%S"))
                        elif isinstance(v, (bytearray, bytes)):
                            _values.append(v.decode("utf-8"))
                        else:
                            _values.append(v)
                    else:
                        _values.append(None)

                d["attributes"] = _values
        return json.dumps(d)

    @staticmethod
    def from_json(value):
        """
        从 json 字符串中读取信息构造特征要素对象

        :param dict value: 包含特征要素对象信息的json字符串
        :rtype: Feature
        """
        d = json.loads(value)
        feature = Feature()
        feature.set_feature_id(d["Feature"])
        if "geometry" in d.keys():
            feature.set_geometry(Geometry._from_dict(d["geometry"]))
        if "fields" in d.keys():
            feature.set_field_infos([FieldInfo.from_json(f) for f in d["fields"]])
        if "attributes" in d.keys():
            i = 0
            for v in d["attributes"]:
                feature.set_value(i, v)
                i += 1

        return feature


class Geometry3D(Geometry):
    __doc__ = "\n    所有三维几何类的基类，提供了基本的三维几何类的属性和方法。\n    通过本类可以对三维几何对象的姿态进行控制，包括对象的位置，旋转角度，缩放比例和内点；\n    还可以对三维几何对象进行偏移；还可以获取三维模型几何对象\n    "

    def __init__(self):
        JVMBase.__init__(self)

    @property
    def volume(self):
        """获取三维几何对象的体积，单位为立方米。"""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jobject.getVolume()

    @property
    def style3D(self):
        """获取三维几何对象的风格"""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        if self._jobject.getStyle3D() is None:
            return GeoStyle3D()
        return GeoStyle3D._from_java_object(self._jobject.getStyle3D())

    def set_style3D(self, value):
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        if not isinstance(value, GeoStyle3D):
            raise TypeError("require type GeoStyle3D")
        self._jobject.setStyle3D(value._jobject)

    @property
    def position(self):
        """获取设置三维几何对象的位置"""
        _p = self._java_object.getPosition()
        return Point3D._from_java_object(_p)

    def set_position(self, value):
        """
        设置三维几何对象的位置。
        该位置的坐标值是三维几何对象外接长方体底面中心点的三维坐标值。
        该中心点用来控制三维几何对象在地球上的放置位置
        :param value:
        :return:
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        value = Point3D.make(value)
        self._jobject.setPosition(value._jobject)

    def set_scale(self, x=1.0, y=1.0, z=1.0):
        """
        设置三维几何对象沿 X,Y,Z 轴方向的缩放比例
        :param x:沿 X 轴方向的缩放比例
        :param y:沿 Y 轴方向的缩放比例
        :param z:沿 Z 轴方向的缩放比例
        :return:
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self._jobject.setScaleX(float(x))
        self._jobject.setScaleY(float(y))
        self._jobject.setScaleZ(float(z))

    def get_scale(self):
        """
        三维几何对象沿 X,Y,Z 轴方向的缩放比例
        :return:
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        x = self._jobject.getScaleX()
        y = self._jobject.getScaleY()
        z = self._jobject.getScaleZ()
        return (x, y, z)

    def set_rotate(self, x=0.0, y=0.0, z=0.0):
        """
        设置三维几何对象沿 X,Y,Z 轴方向的旋转角度，单位为度
        :param x: 沿 X 轴方向的旋转角度
        :param y: 沿 Y 轴方向的旋转角度
        :param z: 沿 Z 轴方向的旋转角度
        :return:
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self._jobject.setRotationX(float(x))
        self._jobject.setRotationY(float(y))
        self._jobject.setRotationZ(float(z))

    def get_rotate(self):
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        x = self._jobject.getRotationX()
        y = self._jobject.getRotationY()
        z = self._jobject.getRotationZ()
        return (x, y, z)

    def translate(self, dx=0.0, dy=0.0, dz=0.0):
        """
        根据对象中心点进行偏移
        :param dx: x方向偏移量
        :param dy: y方向偏移量
        :param dz: z方向偏移量
        :return:
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        p = self.position
        self.set_position([p.x + dx, p.y + dy, p.z + dz])

    def convertToGeoModel3D(self, bLonLat=False, slice=None):
        """
        将三维几何对象转换为三维模型对象
        :param bLonLat:指定模型的顶点或插值点是否是经纬度
        :param slice:
        :return:转换后的三维模型对象
        """
        model = None
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        elif slice is None:
            model = self._jobject.convertToGeoModel3D(bLonLat)
        else:
            model = self._jobject.convertToGeoModel3D(bLonLat, int(slice))
        if model is not None:
            model = GeoModel3D._from_java_object(model)
        return model


class GeoStyle3D(object):
    __doc__ = "\n    三维场景中的几何对象风格类。该类主要用于设置三维场景中几何对象的显示风格\n    "

    def __init__(self):
        self._fillForeColor = (255, 255, 255, 255)
        self._lineColor = (255, 255, 255, 255)
        self._markerColor = (255, 255, 255, 255)
        self._markerSize = 4.0
        self._lineWidth = 0.1

    def __str__(self):
        return str(self.to_dict())

    @property
    def fillForeColor(self):
        return self._fillForeColor

    def set_fillForeColor(self, value):
        if value is not None:
            self._fillForeColor = value

    @property
    def lineColor(self):
        return self._lineColor

    def set_lineColor(self, value):
        if value is not None:
            self._lineColor = value

    @property
    def markerColor(self):
        return self._markerColor

    def set_markerColor(self, value):
        self._markerColor = value

    @property
    def lineWidth(self):
        return self._lineWidth

    def set_lineWidth(self, value):
        self._lineWidth = value

    @property
    def markerSize(self):
        return self.markerSize

    def set_markerSize(self, value):
        self._markerSize = value

    def to_dict(self):
        """
        将当前对象输出为 dict
        :rtype: dict
        """
        d = dict()
        if self._fillForeColor is not None:
            d["fillForeColor"] = self._fillForeColor
        if self._lineColor is not None:
            d["lineColor"] = self._lineColor
        if self._markerColor is not None:
            d["markerColor"] = self._markerColor
        if self._lineWidth is not None:
            d["lineWidth"] = self._lineWidth
        if self._markerSize is not None:
            d["markerSize"] = self._markerSize
        return d

    def __getstate__(self):
        return self.to_dict()

    def __setstate__(self, state):
        self.__init__()
        self.from_dict(state)

    def to_json(self):
        """
        输出为 json 字符串
        :rtype: str
        """
        return json.dumps(self.to_dict())

    @staticmethod
    def from_json(value):
        """
        从 json 字符串中构建 GeoStyle3D 对象
        :param str value:
        :rtype: GeoStyle3D
        """
        style3d = GeoStyle3D()
        style3d.from_dict(json.loads(value))
        return style3d

    def clone(self):
        """
        拷贝对象

        :rtype: TextStyle
        """
        return GeoStyle3D.make_from_dict(self.to_dict())

    @staticmethod
    def make_from_dict(values):
        """
        从 dict 中读取文本风格信息构造 GeoStyle3D
        :param dict values: 包含文本风格信息的 dict
        :rtype: GeoStyle3D
        """
        return GeoStyle3D().from_dict(values)

    def from_dict(self, values):
        """
        从 dict 中读取风格信息
        :param dict values: 包含风格信息的 dict
        :return: self
        :rtype: GeoStyle3D
        """
        if "fillForeColor" in values.keys():
            self.set_fillForeColor(values["fillForeColor"])
        if "lineColor" in values.keys():
            self.set_lineColor(values["lineColor"])
        if "markerColor" in values.keys():
            self.set_markerColor(values["markerColor"])
        if "lineWidth" in values.keys():
            self.set_lineWidth(values["lineWidth"])
        if "markerSize" in values.keys():
            self.set_markerSize(values["markerSize"])

    @property
    def _jobject(self):
        java_obj = get_jvm().com.supermap.data.GeoStyle3D()
        if self._fillForeColor is not None:
            java_obj.setFillForeColor(tuple_to_java_color(self._fillForeColor))
        if self._lineColor is not None:
            java_obj.setLineColor(tuple_to_java_color(self._lineColor))
        if self._markerColor is not None:
            java_obj.setMarkerColor(tuple_to_java_color(self._markerColor))
        if self._lineWidth is not None:
            java_obj.setLineWidth(float(self._lineWidth))
        if self._markerSize is not None:
            java_obj.setMarkerSize(float(self._markerSize))
        return java_obj

    @staticmethod
    def _from_java_object(java_obj):
        obj = GeoStyle3D()
        obj.set_fillForeColor(java_color_to_tuple(java_obj.getFillForeColor()))
        obj.set_lineColor(java_color_to_tuple(java_obj.getLineColor()))
        obj.set_markerColor(java_color_to_tuple(java_obj.getMarkerColor()))
        obj.set_lineWidth(java_obj.getLineWidth())
        obj.set_markerSize(java_obj.getMarkerSize())
        return obj


class GeoLine3D(Geometry3D):
    __doc__ = "\n    线几何对象类。\n    该类用于描述线状地理实体，如河流，道路，等值线等，一般用一个或多个有序坐标点集合来表示。线的方向决定于有序坐标点的顺序，也可以通过调用 reverse\n    方法来改变线的方向。线对象由一个或多个部分组成，每个部分称为线对象的一个子对象，每个子对象用一个有序坐标点集合来表示。可以对子对象进行添加，删除，\n    修改等操作。\n\n    "

    def __init__(self, points=None):
        """
        构造一个线几何对象

        :param points: 包含点串信息的对象，可以为 list[Point3D] 、tuple[Point3D] 、 GeoLine3D 、GeoRegion3D
        :type points: list[Point3D] or tuple[Point3D] or GeoLine3d or GeoRegion
        """
        Geometry.__init__(self)
        if points is not None:
            if isinstance(points, (list, tuple)):
                java_point3ds = self._jvm.com.supermap.data.Point3Ds()
                for p in points:
                    pnt = Point3D.make(p)
                    if pnt is not None:
                        java_point3ds.add(pnt._jobject)

                if java_point3ds.getCount() >= 2:
                    self._jobject.addPart(java_point3ds)
            elif isinstance(points, GeoLine3D):
                self._java_object = self._jvm.com.supermap.data.GeoLine3D(points._jobject)
            else:
                if isinstance(points, GeoRegion3D):
                    self._java_object = self._jvm.com.supermap.data.GeoLine3D(points._jobject.convertToLine())
                else:
                    if isinstance(points, Rectangle):
                        java_point3ds = self._jvm.com.supermap.data.Point3Ds()
                        for p in points.points:
                            java_point3ds.add(p._jobject)

                        java_point3ds.add(points.points[0]._jobject)
                        self._jobject.addPart(java_point3ds)

    def _create_java_object(self):
        self._java_object = self._jvm.com.supermap.data.GeoLine3D()
        return self

    def __getitem__(self, item):
        return self.get_part(item)

    def __setitem__(self, item, value):
        if item < 0:
            item += self.get_part_count()
        points = self._jvm.com.supermap.data.Point3Ds()
        for p in value:
            points.add(p._jobject)

        self._jobject.setPart(item, points)

    def get_part_count(self):
        """
        获取子对象的个数

        :rtype: int
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jobject.getPartCount()

    def convert_to_region(self):
        """
        将当前线对象转换为面几何对象
        - 对于没有封闭的线对象，转换为面对象时，会把首尾自动连起来
        - GeoLine 对象实例的某个子对象的点数少于 3 时将失败

        :rtype: GeoRegion3D
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return Geometry._from_java_object(self._jobject.convertToRegion())

    def __getstate__(self):
        return (
         self.get_parts(), self.id, self.bounds)

    def __setstate__(self, state):
        if len(state) != 3:
            raise Exception("state length required 3 but " + str(len(state)))
        self.__init__()
        points = state[0]
        for pnts in points:
            if len(pnts) >= 2:
                self.add_part(pnts)

        self.set_id(int(state[1]))
        self._set_bounds(state[2])

    def remove_part(self, item):
        """
        删除此线几何对象中的指定序号的子对象。

        :param int item: 指定的子对象的序号
        :return: 成功则返回 true，否则返回 false
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        if item < 0:
            item += self.get_part_count()
        return self._jobject.removePart(item)

    def insert_part(self, item, points):
        """
        此线几何对象中的指定位置插入一个子对象。成功则返回 True，否则返回 False

        :param int item: 插入的位置
        :param list[Point2D] points: 插入的有序点集合
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        if item < 0:
            item += self.get_part_count()
        java_points = self._jvm.com.supermap.data.Point3Ds()
        for p in points:
            java_points.add(Point3D.make(p)._jobject)

        return self._jobject.insertPart(item, java_points)

    def add_part(self, points):
        """
        向此线几何对象追加一个子对象。成功返回添加的子对象的序号。

        :param list[Point3D] points: 一个有序点集
        :rtype: int
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        java_points = self._jvm.com.supermap.data.Point3Ds()
        for p in points:
            java_points.add(p._jobject)

        return self._jobject.addPart(java_points)

    def get_part(self, item):
        """
        返回此线几何对象中指定序号的子对象，以有序点集合的方式返回该子对象。 当二维线对象是简单线对象时，如果传入参数0，得到的是此线对象的节点的集合。

        :param int item: 子对象的序号。
        :return: 子对象的的节点
        :rtype: list[Point2D]
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        if item < 0:
            item += self.get_part_count()
        points = self._jobject.getPart(item)
        pnts = []
        for i in range(points.getCount()):
            p = points.getItem(i)
            pnts.append(Point3D(p.getX(), p.getY(), p.getZ()))

        return pnts

    @property
    def length(self):
        """float: 返回线对象的长度"""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jobject.getLength()

    def clone(self):
        """
        复制对象

        :rtype: GeoLine
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        geoLine = GeoLine3D()
        java_geoLine = self._jobject.clone()
        geoLine._java_object = java_geoLine
        return geoLine

    def get_parts(self):
        """
        获取当前几何对象的所有点坐标。每个子对象使用一个 list 存储

        >>> points = [Point3D(1,2,0),Point3D(2,3,0)]
        >>> geo = GeoLine3D(points)
        >>> geo.add_part([Point3D(3,4,0),Point3D(4,5,0)])
        >>> print(geo.get_parts())
        [[(1.0, 2.0, 0.0), (2.0, 3.0, 0.0)], [(3.0, 4.0, 0.0), (4.0, 5.0, 0.0)]]

        :return: 包含所有点坐标list
        :rtype: list[list[Point3D]]
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        parts = []
        for i in range(self.get_part_count()):
            parts.append(self.get_part(i))

        return parts

    def _to_dict(self):
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        d = OrderedDict()
        points = []
        for i in range(self.get_part_count()):
            part = self[i]
            dp = [[p.x, p.y, p.z] for p in part]
            points.append(dp)

        d[self._get_sjson_type_name()] = points
        d["id"] = self.id
        return d

    def to_json(self):
        """
        将当前对象输出为 Simple Json 字符串

        >>> points = [Point3D(1,2,0), Point3D(2,3,0), Point3D(1,5,0), Point3D(1,2,0)]
        >>> geo = GeoLine(points)
        >>> print(geo.to_json())
        {"Line3D": [[[1.0, 2.0, 0.0], [2.0, 3.0, 0.0], [1.0, 5.0, 0.0], [1.0, 2.0, 0.0]]], "id": 0}

        :rtype: str
        """
        return json.dumps(self._to_dict())

    def _from_json(self, d):
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        if "id" in d:
            self.set_id(d["id"])
        points = d[self._get_sjson_type_name()]
        for part in points:
            self.add_part([Point3D(p[0], p[1], p[2]) for p in part])


class GeoRegion3D(Geometry3D):
    __doc__ = "\n    面几何对象类，派生于 Geometry3D 类。\n\n    该类用于描述面状地理实体，如行政区域，湖泊，居民地等，一般用一个或多个有序坐标点集合来表示。面几何对象由一个或多个部分组成，每个部分称为面几何对\n    象的一个子对象，每个子对象用一个有序坐标点集合来表示，其起始点和终止点重合。可以对子对象进行添加，删除，修改等操作。\n    "

    def __init__(self, points=None):
        """
        构造一个面几何对象

        :param points: 包含点串信息的对象，可以为 list[Point2D] 、tuple[Point2D] 、 GeoLine 、GeoRegion 和 Rectangle
        :type points: list[Point2D] or tuple[Point2D] or GeoLine or GeoRegion or Rectangle
        """
        Geometry.__init__(self)
        if points is not None:
            if isinstance(points, (list, tuple)):
                java_point3ds = self._jvm.com.supermap.data.Point3Ds()
                for p in points:
                    pnt = Point3D.make(p)
                    if pnt is not None:
                        java_point3ds.add(pnt._jobject)

                if java_point3ds.getCount() > 2:
                    self._jobject.addPart(java_point3ds)

    @property
    def area(self):
        """float: 返回面对象的面积"""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jobject.getArea()

    @property
    def perimeter(self):
        """float: 返回面对象的周长"""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jobject.getPerimeter()

    def _create_java_object(self):
        self._java_object = get_jvm().com.supermap.data.GeoRegion3D()
        return self

    def __getitem__(self, item):
        return self.get_part(item)

    def __setitem__(self, item, value):
        if item < 0:
            item += self.get_part_count()
        if len(value) < 3:
            raise Exception("points count must be greater than 2")
        points = get_jvm().com.supermap.data.Point3Ds()
        for p in value:
            points.add(p._jobject)

        self._jobject.setPart(item, points)

    def get_part_count(self):
        """
        获取子对象的个数
        :rtype: int
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jobject.getPartCount()

    def __getstate__(self):
        return (
         self.get_parts(), self.id, self.bounds)

    def __setstate__(self, state):
        if len(state) != 3:
            raise Exception("state length required 3 but " + str(len(state)))
        self.__init__()
        points = state[0]
        for pnts in points:
            if len(pnts) > 2:
                self.add_part(pnts)

        self.set_id(int(state[1]))
        self._set_bounds(state[2])

    def contains(self, point):
        """
        判断点是否在面内
        :param point: 待判断的点对象
        :type point: Point3D or GeoPoint3D
        :return: 点在面内返回 True，否则返回\u3000False
        :return type: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        elif isinstance(point, Point3D):
            java_point = self._jvm.com.supermap.data.GeoPoint3D(float(point.x), float(point.y), float(point.z))
        else:
            if isinstance(point, GeoPoint3D):
                java_point = point._jobject
            else:
                raise ValueError("invalid point, required Point3D or GeoPoint3D")
        return self._jvm.com.supermap.data.Geometrist.isWithin(java_point, self._jobject)

    def add_part(self, points):
        """
        向此面几何对象追加一个子对象。成功返回添加的子对象的序号。

        :param list[Point2D] points: 一个有序点集
        :rtype: int
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        java_points = self._jvm.com.supermap.data.Point3Ds()
        for p in points:
            java_points.add(p._jobject)

        return self._jobject.addPart(java_points)

    def remove_part(self, item):
        """
        删除此面几何对象中的指定序号的子对象。
        :param int item: 指定的子对象的序号
        :return: 成功则返回 true，否则返回 false
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        if item < 0:
            item += self.get_part_count()
        return self._jobject.removePart(item)

    def insert_part(self, item, points):
        """
        此面几何对象中的指定位置插入一个子对象。成功则返回 True，否则返回 False
        :param int item: 插入的位置
        :param list[Point3D] points: 插入的有序点集合
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        if item < 0:
            item += self.get_part_count()
        java_points = self._jvm.com.supermap.data.Point3Ds()
        for p in points:
            java_points.add(p._jobject)

        return self._jobject.insertPart(item, java_points)

    def get_part(self, item):
        """
        返回此面几何对象中指定序号的子对象，以有序点集合的方式返回该子对象。

        :param int item: 子对象的序号。
        :return: 子对象的的节点
        :rtype: list[Point3D]
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        if item < 0:
            item += self.get_part_count()
        points = self._jobject.getPart(item)
        pnts = []
        for i in range(points.getCount()):
            p = points.getItem(i)
            pnts.append(Point3D(p.getX(), p.getY(), p.getZ()))

        return pnts

    def get_parts(self):
        """
        获取当前几何对象的所有点坐标。每个子对象使用一个 list 存储

        >>> points = [Point3D(1,2,0), Point3D(2,3,0), Point3D(1,5,0), Point3D(1,2,0)]
        >>> geo = GeoRegion(points)
        >>> geo.add_part([Point3D(2,3,0), Point3D(4,3,0), Point3D(4,2,0), Point3D(2,3,0)])
        >>> geo.get_parts()
        :return: 包含所有点坐标list
        :rtype: list[list[Point2D]]
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        parts = []
        for i in range(self.get_part_count()):
            parts.append(self.get_part(i))

        return parts

    def translate(self, dx=0.0, dy=0.0, dz=0.0):
        """
        将面对象进行偏移，面中的每一个点都加上该偏移量
        :param dx: X 方向偏移量
        :param dy: Y 方向偏移量
        :param dz: Z 方向偏移量
        :return:
        """
        if self._java_object is None:
            raise ObjectDisposedError(type(self).__name__)
        points = []
        for i in range(self.get_part_count()):
            part = self[i]
            for p in part:
                dp = [
                 p.x + dx, p.y + dy, p.z + dz]
                points.append(dp)

        return GeoRegion3D(points)

    def _to_dict(self):
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        d = OrderedDict()
        points = []
        for i in range(self.get_part_count()):
            part = self[i]
            dp = [[p.x, p.y, p.z] for p in part]
            points.append(dp)

        d[self._get_sjson_type_name()] = points
        d["id"] = self.id
        return d

    def to_json(self):
        """
        将当前对象输出为 Simple Json 字符串

        >>> points = [Point2D(1,2), Point2D(2,3), Point2D(1,5), Point2D(1,2)]
        >>> geo = GeoRegion(points)
        >>> print(geo.to_json())
        {"Region": [[[1.0, 2.0], [2.0, 3.0], [1.0, 5.0], [1.0, 2.0]]], "id": 0}

        :rtype: str
        """
        return json.dumps(self._to_dict())

    def _from_json(self, d):
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        if "id" in d:
            self.set_id(d["id"])
        points = d[self._get_sjson_type_name()]
        for part in points:
            self.add_part([Point3D(p[0], p[1], p[2]) for p in part])


class GeoModel3D(Geometry3D):
    __doc__ = "\n    三维模型对象类\n    "

    def __init__(self, poin3dValues=None, faceIndices=None, bLonLat=False):
        """
        :由顶点，顶点索引构建三维模型对象
        :param poin3dValues:顶点包
        :param faceIndices:Face索引集合，需要注意的是顶点索引每个元素应该是一个个数大于等于4(第一个和最后一个相同)的list
        即每个Face顶点连接顺序。应当注意的是Face应是一个平面
        :return 三维模型对象
        例如构建一个中心点在原点的盒子三维模型
        8个顶点
        point3ds = [Point3D(-1,-1,-1), Point3D(1,-1,-1), Point3D(1,-1,1), Point3D(-1,-1,1),Point3D(-1,1,-1), Point3D(1, 1, -1), Point3D(1, 1, 1), Point3D(-1, 1, 1)]
        6个面
        faceIndices=[
                    [3,2,1,0,3],#front
                    [0,1,5,4,0],#bottom
                    [0,4,7,3,0],#right
                    [1,5,6,2,1],#left
                    [2,3,7,6,2],#top
                    [5,4,7,6,5] #back
                    ]
        geo=GeoModel3D(point3ds, faceIndices)

        """
        Geometry3D.__init__(self)
        result = None
        if isinstance(poin3dValues, list):
            if isinstance(faceIndices, list):
                models = []
                for face in faceIndices:
                    if isinstance(face, list) and len(face) >= 4:
                        indices = []
                        for index in face:
                            indices.append(poin3dValues[index])

                        region = GeoRegion3D(indices)
                        model = region.convertToGeoModel3D(bLonLat)
                        if model is not None:
                            models.append(model)

                if len(models) >= 2:
                    result = self._jvm.com.supermap.realspace.threeddesigner.ModelTools.compose(models)
        if result is not None:
            self._java_object = result

    def _create_java_object(self):
        self._java_object = self._jvm.com.supermap.data.GeoModel3D()
        return self

    def translate(self, x=0, y=0, z=0):
        """
        模型平移
        :param x: X方向平移量
        :param y: Y方向平移量
        :param z: Z方向平移量
        :return: 返回平移后的模型
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        geoArray = [
         self._jobject]
        result = self._jvm.com.supermap.realspace.threeddesigner.ModelTools.translate(geoArray, float(x), float(y), float(z))
        if len(result) > 0:
            return GeoModel3D._from_java_object(result[0])
        return self

    def set_color(self, value):
        """
        设置模型材质颜色，所有骨架都为该颜色
        :param value: 材质颜色
        :return:
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self._jvm.com.supermap.jsuperpy.threeddesigner.ModelBuilder3DTools.setModelColor(self._jobject, tuple_to_java_color(value))

    @property
    def max_z(self):
        """获得模型z方向的最大值"""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jobject.getMaxZ()

    @property
    def min_z(self):
        """获取模型z方向的最小值"""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jobject.getMinZ()

    def SetMatrix(self, basePoint, matrix):
        """
        模型变换
        :param basePoint:基准点
        :param matrix:变换矩阵
        :return:矩阵变换后的GeoModel3D
        """
        if isinstance(basePoint, Point3D):
            if isinstance(matrix, Matrix):
                self._java_object.SetMatrix(basePoint._jobject, matrix._java_object)
                return self
            return

    def Mirror(self, plane):
        """
        :镜像
        :param plane:镜像面
        :return:返回self关于plane镜像的模型对象
        """
        if isinstance(plane, Plane):
            result = self._jvm.com.supermap.realspace.threeddesigner.ModelBuilder3D.Mirror(self._java_object, plane._java_object)
            return result._java_object


class Size2D(JVMBase):

    def __init__(self, width=0.0, height=0.0):
        self.height = float(height)
        self.width = float(width)
        if self._jobject is not None:
            self._jobject.setWidth(self.width)
            self._jobject.setHeight(self.height)

    def _create_java_object(self):
        self._java_object = self._jvm.com.supermap.data.Size2D(0, 0)
        return self

    @staticmethod
    def _from_java_object(j_geometry):
        if j_geometry is None:
            return
        geo = Size2D
        geo._java_object = j_geometry
        return geo

    def __len__(self):
        return 2

    @property
    def width(self):
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jobject.getWidth()

    @width.setter
    def width(self, value):
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self._jobject.setWidth(float(value))

    @property
    def height(self):
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jobject.getHeight()

    @height.setter
    def height(self, value):
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self._jobject.setHeight(float(value))


class GeoCircle3D(Geometry3D):
    __doc__ = "\n    三维圆面几何对象类\n    "

    def __init__(self, r=0.0, position=None):
        Geometry3D.__init__(self)
        self._r = float(r)
        if self._jobject is not None:
            self._jobject.setRadius(self._r)
            if position is not None:
                self.set_position(position)

    def _create_java_object(self):
        self._java_object = self._jvm.com.supermap.data.GeoCircle3D()
        return self

    def __str__(self):
        return "GeoCircle3D: r=" + self._r

    @staticmethod
    def _from_java_object(j_geometry):
        if j_geometry is None:
            return
        geo = GeoCircle3D
        geo._java_object = j_geometry
        return geo

    @property
    def radius(self):
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jobject.getRadius()

    def set_radius(self, value):
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self._jobject.setRadius(float(value))


class GeoBox(Geometry3D):
    __doc__ = "\n    长方体几何对象类\n    "

    def __init__(self, len=0.0, width=None, height=None, position=None):
        Geometry3D.__init__(self)
        self._len = float(len)
        if width is not None:
            self._width = float(width)
        else:
            self._width = self._len
        if height is not None:
            self._height = float(height)
        else:
            self._height = self._len
        if self._jobject is not None:
            _jbottomSize = self._jvm.com.supermap.data.Size2D(self._len, self._width)
            self._jobject.setBottomSize(_jbottomSize)
            self._jobject.setHeight(self._height)
            if position is not None:
                self.set_position(position)

    def _create_java_object(self):
        self._java_object = self._jvm.com.supermap.data.GeoBox()
        return self

    def __str__(self):
        return "GeoBox: length=" + self._len + ",width=" + self._width + ",height=" + self._height

    @staticmethod
    def _from_java_object(j_geometry):
        if j_geometry is None:
            return
        geo = GeoBox
        geo._java_object = j_geometry
        return geo

    def _get_jbottomSize(self):
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jobject.getBottomSize()

    @property
    def length(self):
        return self._get_jbottomSize().getWidth()

    def set_length(self, value):
        _jbottomsize = self._get_jbottomSize()
        _jbottomsize.setWidth(float(value))
        self._jobject.setBottomSize(_jbottomsize)

    @property
    def width(self):
        return self._get_jbottomSize().getHeight()

    def set_width(self, value):
        _jbottomsize = self._get_jbottomSize()
        _jbottomsize.setHeight(float(value))
        self._jobject.setBottomSize(_jbottomsize)

    @property
    def height(self):
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jobject.getHeight()

    def set_height(self, value):
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self._jobject.setHeight(float(value))


class GeoCylinder(Geometry3D):
    __doc__ = "\n    圆台几何对象类，继承于 Geometry3D类。\n    如果设置该类对象的底面圆的半径和顶面圆的半径相等，就是圆柱几何对象\n    "

    def __init__(self, topRadius=0.0, bottomRadius=None, height=1.0, position=None):
        Geometry3D.__init__(self)
        self._topR = float(topRadius)
        if bottomRadius is not None:
            self._bottomR = float(bottomRadius)
        else:
            self._bottomR = self._topR
        self._height = float(height)
        if self._jobject is not None:
            self._jobject.setTopRadius(self._topR)
            self._jobject.setBottomRadius(self._bottomR)
            if self._height > 0:
                self._jobject.setHeight(self._height)
            if position is not None:
                self.set_position(position)

    def __str__(self):
        return "GeoCylinder: topRadius=" + self._topR + ",bottomRadius=" + self._bottomR + ",height=" + self._height

    def _create_java_object(self):
        self._java_object = self._jvm.com.supermap.data.GeoCylinder()
        return self

    @staticmethod
    def _from_java_object(j_geometry):
        if j_geometry is None:
            return
        geo = GeoCylinder
        geo._java_object = j_geometry
        return geo

    @property
    def topRadius(self):
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jobject.getTopRadius()

    def set_topRadius(self, value):
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self._jobject.setTopRadius(float(value))

    @property
    def bottomRadius(self):
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jobject.getBottomRadius()

    def set_bottomRadius(self, value):
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self._jobject.setBottomRadius(float(value))

    @property
    def height(self):
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jobject.getHeight()

    def set_height(self, value):
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self._jobject.setHeight(float(value))


class Plane(JVMBase):
    __doc__ = "\n    平面对象类。此平面为数学意义上无限延展的平面，主要用于三维模型进行截面投影和平面投影\n    用法：\n    p1 = Point3D(1, 1, 1)\n    p2 = Point3D(0, 3, 4)\n    p3 = Point3D(7, 4, 3)\n    plane = Plane([p1, p2, p3])\n    或者：\n    plane = Plane(PlaneType.PLANEXY)\n    "

    def __init__Parse error at or near `COME_FROM' instruction at offset 150_0

    def _create_java_object(self):
        self._java_object = get_jvm().com.supermap.data.Plane()
        return self

    @staticmethod
    def _from_java_object(j_object):
        if j_object is None:
            return
        plane = Plane()
        plane._java_object = j_object
        return plane

    def set_type(self, planeType):
        """
        设置平面类型
        :param planeType:
        :return:
        """
        self._jobject.setType(planeType._jobject)

    def set_normal(self, p):
        """
        设置面的法向量
        :param p:法向量，可以是Point3D，tuple[float,float,float] or list[float,float,float]
        :return:
        """
        point = Point3D.make(p)
        if point is not None:
            self._jobject.setNormal(point._jobject)

    def get_normal(self):
        """
         获取面的法向量
        :return: 返回法向量Point3D
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        j_point = self._jobject.getNormal()
        return Point3D._from_java_object(j_point)


class Matrix(JVMBase):
    __doc__ = "\n    4X4矩阵类，主要用于三维模型矩阵变换\n    如果需要连续变换，应该用静态方法Multiply相乘\n    "

    def __init__(self, arrayValue=None):
        self._java_object = get_jvm().com.supermap.data.Matrix()
        if arrayValue is not None:
            if isinstance(arrayValue, list):
                self.set_ArrayValue(arrayValue)

    @property
    def _ArrayValue(self):
        """
        :获取矩阵的值
        :return: 返回长度为16的数组
        """
        arrayData = list(self._jobject.getArrayValue())
        return arrayData

    def set_ArrayValue(self, value):
        """
        :设置矩阵
        :param value:长度为16的数组
        """
        if len(value) == 16:
            self._java_object.setArrayValue(to_java_double_array(value))

    @staticmethod
    def _from_java_object(j_object):
        if j_object is None:
            return
        mat = Matrix()
        mat._java_object = j_object
        return mat

    @staticmethod
    def rotate(rotationX, rotationY, rotationZ):
        """
        :旋转，单位:度
        :param rotationX:绕X轴旋转的角度
        :param rotationY:绕Y轴旋转的角度
        :param rotationZ:绕Z轴旋转的角度
        :return: 返回一个新的具有rotationX, rotationY, rotationZ缩放的矩阵
        """
        mat = get_jvm().com.supermap.data.Matrix.rotateXYZ(float(rotationX), float(rotationY), float(rotationZ))
        return Matrix._from_java_object(mat)

    @staticmethod
    def scale(scaleX, scaleY, scaleZ):
        """
        :缩放
        :param scaleX:X方向缩放
        :param scaleY:Y方向缩放
        :param scaleZ:Z方向缩放
        :return: 返回一个新的具有scaleX, scaleY, scaleZ缩放的矩阵
        """
        mat = get_jvm().com.supermap.data.Matrix.scale(float(scaleX), float(scaleY), float(scaleZ))
        return Matrix._from_java_object(mat)

    @staticmethod
    def translate(translateX, translateY, translateZ):
        """
        :平移
        :param translateX:X方向平移
        :param translateY:Y方向平移
        :param translateZ:Z方向平移
        :return: 返回一个新的具有translateX, translateY, translateZ平移的矩阵
        """
        mat = get_jvm().com.supermap.data.Matrix.translate(float(translateX), float(translateY), float(translateZ))
        return Matrix._from_java_object(mat)

    @staticmethod
    def multiply(value, matrix):
        """
        :矩阵乘法，第一个参数可以是Point3D，也可以是Matrix
        :param value:可以是Point3D,也可以是4X4矩阵，
        :param matrix:矩阵
        :return: 当第一个参数是Point3D时，返回值为Point3D；当是Matrix时，返回值为Matrix
        """
        if isinstance(matrix, Matrix):
            if isinstance(value, Point3D):
                pnt3d = get_jvm().com.supermap.data.Matrix.multiply(value._jobject, matrix._java_object)
                return Point3D._from_java_object(pnt3d)
            if isinstance(value, Matrix):
                mat = value._java_object.multipy(matrix._java_object)
                return Matrix._from_java_object(mat)
            return
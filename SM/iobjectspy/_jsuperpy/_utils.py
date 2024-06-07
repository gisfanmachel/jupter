# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/_jsuperpy\_utils.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 15765 bytes
import datetime, time, threading
from ._gateway import get_jvm, get_gateway
from ._logger import *
import struct, sys
__all__ = [
 'to_java_int_array', 'to_java_string_array', 'to_java_double_array', 'to_java_color_array', 
 'to_java_color', 
 'split_input_list_from_str', 'split_input_dict_from_str', 'datetime_to_java_date', 
 'tuple_to_java_color', 
 'java_color_to_tuple', 'get_datetime_timestamp', 'java_date_to_datetime', 
 'get_red', 
 'get_green', 'get_blue', 'get_alpha', 'get_unique_name', 'color_to_tuple', 
 'parse_datetime', 
 'tuple_to_color', 'get_datetime_str', 'parse_bool', 'is_equal', 
 'oj', 'get_struct_time', 'get_datetime', 
 'get_day_hour', 'split_input_list_tuple_item_from_str', 
 'read_int', 'read_float', 'write_int', 'write_float', 
 'is_linux', 'is_zero', 
 'check_lic', 'split_input_int_list_from_str', 'split_input_float_list_from_str', 
 'java_array_to_list', 
 'to_java_2d_array', 'to_java_array']

def java_array_to_list(java_array):
    if java_array is not None:
        return list(java_array)
    return


def parse_bool(value):
    if isinstance(value, bool):
        return value
        if isinstance(value, str):
            if value.lower() == "true":
                return True
            return False
    elif value:
        return True
    return False


def to_java_array(values, java_class):
    if values is None:
        return
    if not isinstance(values, (list, tuple, set)):
        values = [
         values]
    _size = len(values)
    java_array = get_gateway().new_array(java_class, _size)
    i = 0
    for value in values:
        java_array[i] = oj(value)
        i += 1

    return java_array


def to_java_2d_array(values, java_class):
    if values is None:
        return
    elif not isinstance(values, (list, tuple, set)):
        values = [
         values]
    java_array = isinstance(values[0], (list, tuple, set)) or get_gateway().new_array(java_class, len(values), 1)
    for i, value in enumerate(values):
        java_array[i][0] = value

    return java_array
    s_size = max(map((lambda l: len(l)), values))
    java_array = get_gateway().new_array(java_class, len(values), s_size)
    for i, item_values in enumerate(values):
        for j, item in enumerate(item_values):
            java_array[i][j] = item

    return java_array


def to_java_string_array(values):
    if values is None:
        return
    if isinstance(values, str):
        java_array = get_gateway().new_array(get_jvm().java.lang.String, 1)
        java_array[0] = values
        return java_array
    if isinstance(values, (list, tuple, set)):
        _size = len(values)
        java_array = get_gateway().new_array(get_jvm().java.lang.String, _size)
        i = 0
        for value in values:
            java_array[i] = value
            i += 1

        return java_array
    return


def to_java_color_array(values):
    if values is None:
        return
    if isinstance(values, tuple):
        java_array = get_gateway().new_array(get_jvm().java.awt.Color, 1)
        java_array[0] = get_jvm().java.awt.Color(int(values[0]), int(values[1]), int(values[2]), int(values[3]))
        return java_array
    if isinstance(values, list):
        _size = len(values)
        java_array = get_gateway().new_array(get_jvm().java.lang.String, _size)
        i = 0
        for value in values:
            java_array[i] = get_jvm().java.awt.Color(int(value[0]), int(value[1]), int(value[2]), int(value[3]))
            i += 1

        return java_array
    return


def to_java_color(value):
    if value is None:
        return
        if isinstance(value, tuple):
            if len(value) == 3:
                return get_jvm().java.awt.Color(int(value[0]), int(value[1]), int(value[2]))
            if len(value) == 4:
                return get_jvm().java.awt.Color(int(value[0]), int(value[1]), int(value[2]), int(value[3]))
    elif isinstance(value, int):
        return get_jvm().java.awt.Color(value)
    log_warning("cannot convert to java.awt.Color, required tuple of (float,int) or int, but now is " + str(type(value)))


def to_java_int_array(values):
    if values is None:
        return
    if isinstance(values, int):
        java_array = get_gateway().new_array(get_jvm().int, 1)
        java_array[0] = values
        return java_array
    if isinstance(values, (list, tuple, set)):
        _size = len(values)
        java_array = get_gateway().new_array(get_jvm().int, _size)
        i = 0
        for value in values:
            try:
                java_array[i] = int(value)
            except:
                pass

            i += 1

        return java_array
    return


def to_java_double_array(values):
    if values is None:
        return
    if isinstance(values, str):
        items = split_input_list_from_str(values)
        return to_java_double_array([float(item) for item in items])
    if isinstance(values, float):
        java_array = get_gateway().new_array(get_jvm().double, 1)
        java_array[0] = values
        return java_array
    if isinstance(values, (list, tuple, set)):
        _size = len(values)
        java_array = get_gateway().new_array(get_jvm().double, _size)
        i = 0
        for value in values:
            try:
                java_array[i] = float(value)
            except:
                pass

            i += 1

        return java_array
    return


def split_input_int_list_from_str(value):
    if isinstance(value, int):
        return [
         value]
    input_items = split_input_list_from_str(value)
    if input_items is not None:
        return list((int(item) for item in input_items))
    return


def split_input_float_list_from_str(value):
    if isinstance(value, (int, float)):
        return [
         float(value)]
    input_items = split_input_list_from_str(value)
    if input_items is not None:
        return list((float(item) for item in input_items))
    return


def split_input_list_from_str(value):
    if value is None:
        return
    if isinstance(value, str):
        res = []
        tokens = value.strip().split(";")
        for token in tokens:
            for item in token.split(","):
                res.append(item.strip())

        return res
    if isinstance(value, (tuple, list, set)):
        return list(value)
    return


def split_input_dict_from_str(value):
    if value is None:
        return
    if isinstance(value, str):
        res = dict()
        tokens = value.strip().split(",")
        for token in tokens:
            sub_tokens = token.split(";")
            for sub_token in sub_tokens:
                sub_item = sub_token.split(":")
                if len(sub_item) == 2:
                    res[sub_item[0].strip()] = sub_item[1].strip()

        return res
    if isinstance(value, dict):
        return value
    return


def split_input_list_tuple_item_from_str(value):
    if value is None:
        return
    if isinstance(value, str):
        res = list()
        tokens = value.strip().split(",")
        for token in tokens:
            sub_tokens = token.split(";")
            for sub_token in sub_tokens:
                sub_item = sub_token.split(":")
                if len(sub_item) == 2:
                    res.append((sub_item[0].strip(), sub_item[1].strip()))

        return res
    if isinstance(value, (list, tuple)):
        res = list()
        for item in value:
            if isinstance(item, str):
                sub_item = item.split(":")
                if len(sub_item) == 2:
                    res.append((sub_item[0].strip(), sub_item[1].strip()))
                elif isinstance(item, (tuple, list)):
                    res.append(tuple(item))

        return res
    return


def tuple_to_java_color(value):
    if value is None:
        return
    elif isinstance(value, tuple):
        if len(value) == 3:
            return get_jvm().java.awt.Color(int(value[0]), int(value[1]), int(value[2]))
        if len(value) == 4:
            return get_jvm().java.awt.Color(int(value[0]), int(value[1]), int(value[2]), int(value[3]))
    else:
        return


def java_color_to_tuple(value):
    if value is None:
        return
    return (
     value.getRed(), value.getGreen(), value.getBlue(), value.getAlpha())


is_little = sys.byteorder == "little"

def color_to_tuple(value):
    if value is None:
        return
        if isinstance(value, (float, int)):
            value = int(value)
            if is_little:
                r = value & 255
                g = value >> 8 & 255
                b = value >> 16 & 255
                a = value >> 24 & 255
                return (
                 r, g, b, a)
            a = value & 255
            b = value >> 8 & 255
            g = value >> 16 & 255
            r = value >> 24 & 255
            return (
             r, g, b, a)
    elif isinstance(value, (tuple, list)):
        if len(value) == 3:
            return (
             value[0], value[1], value[2], 255)
        if len(value) > 3:
            return (
             value[0], value[1], value[2], value[3])
        return
    return


def tuple_to_color(value):
    if value is None:
        return
        if isinstance(value, (tuple, list)):
            import sys
            if is_little:
                if len(value) == 3:
                    return int("%02x%02x%02x" % (value[2], value[1], value[0]), 16)
                if len(value) == 4:
                    return int("%02x%02x%02x%02x" % (value[3], value[2], value[1], value[0]), 16)
                return
        elif len(value) == 3:
            return int("%02x%02x%02x" % (value[0], value[1], value[2]), 16)
        if len(value) == 4:
            return int("%02x%02x%02x%02x" % (value[0], value[1], value[2], value[3]), 16)
        return
    else:
        if isinstance(value, (int, float)):
            return value
        return


def get_datetime_timestamp(dt):
    dt = get_datetime(dt)
    if dt is None:
        raise ValueError("invalid datetime value")
    dl = dt - datetime.datetime(1970, 1, 1)
    return int(dl.total_seconds())


def get_datetime(value):
    if isinstance(value, datetime.datetime):
        return value
    elif isinstance(value, str):
        try:
            return datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except:
            try:
                return datetime.datetime.strptime(value, "%Y-%m-%d")
            except:
                return

    else:
        if isinstance(value, int):
            try:
                return datetime.datetime.fromtimestamp(value)
            except:
                return datetime.datetime.fromtimestamp(value / 1000)


parse_datetime = get_datetime

def get_day_hour(value):
    if isinstance(value, str):
        try:
            return get_day_hour(datetime.datetime.strptime(value, "%H:%M:%S"))
        except:
            pass

    else:
        if isinstance(value, (float, int)):
            if 0 <= value <= 24:
                return float(value)
    dt = get_datetime(value)
    if dt is None:
        return
    d1 = datetime.datetime(dt.year, dt.month, dt.day)
    return (dt - d1).seconds / 3600.0


def get_datetime_str(value):
    time_str = None
    if isinstance(value, datetime.datetime):
        time_str = value.strftime("%Y-%m-%d %H:%M:%S")
    else:
        if isinstance(value, str):
            try:
                datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                time_str = value
            except:
                time_str = None

        else:
            if isinstance(value, int):
                try:
                    time_str = datetime.datetime.fromtimestamp(value).strftime("%Y-%m-%d %H:%M:%S")
                except:
                    time_str = datetime.datetime.fromtimestamp(value / 1000).strftime("%Y-%m-%d %H:%M:%S")

    return time_str


def datetime_to_java_date(value):
    time_str = get_datetime_str(value)
    if time_str is not None:
        return get_jvm().java.text.SimpleDateFormat("yyyy-MM-dd HH:mm:ss").parse(time_str)
    return


def java_date_to_datetime(value):
    if value is None:
        return
    elif isinstance(value, str):
        try:
            return datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            try:
                return
            finally:
                e = None
                del e

    else:
        if isinstance(value, int):
            try:
                return datetime.datetime.fromtimestamp(value)
            except:
                return datetime.datetime.fromtimestamp(value / 1000)

    sf = get_jvm().java.text.SimpleDateFormat("yyyy-MM-dd HH:mm:ss")
    str_t = sf.format(value)
    return datetime.datetime.strptime(str_t, "%Y-%m-%d %H:%M:%S")


def get_struct_time(value):
    if value is None:
        return
        if isinstance(value, str):
            try:
                return datetime.datetime.strptime(value, "%Y-%m-%d").timetuple()
            except:
                try:
                    return datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S").timetuple()
                except:
                    return

    elif isinstance(value, time.struct_time):
        return value
    if isinstance(value, datetime.date):
        return value.timetuple()
    if isinstance(value, datetime.datetime):
        return value.timetuple()
    return


def get_red(value):
    return color_to_tuple(value)[0]


def get_green(value):
    return color_to_tuple(value)[1]


def get_blue(value):
    return color_to_tuple(value)[2]


def get_alpha(value):
    return color_to_tuple(value)[3]


def get_unique_name(name):
    str_t = datetime.datetime.now().strftime("%H%M%S")
    import random
    return "%s_%s_%d_%d" % (str(name), str_t, threading.current_thread().ident, random.randint(1, 100))


def is_equal(a, b, d):
    a, b, d = float(a), float(b), float(d)
    temp = a - b
    if d > 0:
        return -d < temp < d
    if d == 0:
        return a == b
    return False


def oj(obj):
    if obj is None:
        return
    return getattr(obj, "_jobject")


def read_int(stream):
    length = stream.read(4)
    if not length:
        raise EOFError
    return struct.unpack("!i", length)[0]


def read_float(stream):
    length = stream.read(8)
    if not length:
        raise EOFError
    return struct.unpack("!d", length)[0]


def write_int(value, stream):
    stream.write(struct.pack("!i", int(value)))
    stream.flush()


def write_float(value, stream):
    stream.write(struct.pack("!d", float(value)))
    stream.flush()


def is_linux():
    import platform
    if platform.system() == "Linux":
        return True
    return False


def is_zero(value):
    return -1e-10 < value < 1e-10


def check_lic():
    jvm = get_jvm()
    result = jvm.com.supermap.jsuperpy.license.PythonLicense.check()
    if result.code() == 0:
        return
    raise RuntimeError(result.message())

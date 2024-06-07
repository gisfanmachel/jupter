# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/_jsuperpy\data\style.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 50693 bytes
from ..enums import *
from .._gateway import get_jvm
from .._utils import java_color_to_tuple, to_java_color, color_to_tuple, split_input_list_from_str, oj
from ._jvm import JVMBase
__all__ = [
 "Color", "GeoStyle"]

class Color(tuple):
    __doc__ = "\n    定义RGB 颜色对象，用户可以通过指定一个三个元素的元组指定 RGB 颜色值，也可以使用使用四个元素的元组指定 RGBA 颜色值。\n    默认情形下，Alpha 值为255。\n\n    .. image:: ../image/Colors.png\n\n    "

    def __init__(self, seq=(0, 0, 0)):
        """
        通过 tuple 构造一个 Color

        :param seq: 指定的 RGB 或 RGBA 颜色值
        :type seq: tuple[int,int,int] or tuple[int,int,int,int]
        """
        if len(seq) == 3 or len(seq) == 4:
            for item in seq:
                if not 0 <= item <= 255:
                    raise ValueError("value must in range [0,255]")

            tuple.__init__(seq)
        else:
            raise ValueError("input error")

    def __eq__(self, other):
        if isinstance(other, Color):
            if self.R == other.R:
                if self.G == other.G:
                    if self.B == other.B:
                        if self.A == other.A:
                            return True
        return False

    @staticmethod
    def _from_java_object(java_object):
        if java_object:
            return Color(java_color_to_tuple(java_object))

    @staticmethod
    def make(value):
        """
        构造 Color 对象

        :param value: 用于构造 Color 对象的值，如果是 str，可以是使用 ','拼接的字符串，例如：'0,255,232' or '0,255,234,54'
        :type value: Color or str or tuple[int,int,int] or tuple[int,int,int,int]
        :return: 颜色对象
        :rtype: Color
        """
        if isinstance(value, Color):
            return value
        if isinstance(value, str):
            list_value = split_input_list_from_str(value)
            if isinstance(list_value, (list, tuple)):
                if len(list_value) >= 3:
                    return Color.make((int(item) for item in list_value))
            return getattr(Color, value)()
        tuple_value = color_to_tuple(value)
        if len(tuple_value) == 3:
            return Color((tuple_value[0], tuple_value[1], tuple_value[2]))
        if len(tuple_value) == 4:
            return Color((tuple_value[0], tuple_value[1], tuple_value[2], tuple_value[3]))
        raise ValueError("invalid input for color")

    @staticmethod
    def rgb(red, green, blue, alpha=255):
        """
        通过指定 R、G、B、A 值构造 Color 对象

        :param int red: Red 值
        :param int green: Green 值
        :param int blue: Blue 值
        :param int alpha: Alpha 值
        :return: 颜色对象
        :rtype: Color
        """
        return Color((red, green, blue, alpha))

    def __str__(self):
        if len(self) == 4:
            return "Color(red={}, green={}, blue={}, alpha={})".format(self.R, self.G, self.B, self.A)
        return "Color(red={}, green={}, blue={})".format(self.R, self.G, self.B)

    __repr__ = __str__

    @property
    def R(self):
        """int: 获取 Color 的 R 值"""
        return self.__getitem__(0)

    @property
    def G(self):
        """int: 获取 Color 的 G 值"""
        return self.__getitem__(1)

    @property
    def B(self):
        """int: 获取 Color 的 B 值"""
        return self.__getitem__(2)

    @property
    def A(self):
        """int: 获取 Color 的 A 值"""
        if len(self) > 3:
            return self.__getitem__(3)
        return 255

    @staticmethod
    def aliceblue():
        """
        构造颜色值 (240, 248, 255)

        :return: 颜色值 (240, 248, 255)
        :rtype: Color
        """
        return Color((240, 248, 255))

    @staticmethod
    def antiquewhite():
        """
        构造颜色值 (250, 235, 215)

        :return: 颜色值 (250, 235, 215)
        :rtype: Color
        """
        return Color((250, 235, 215))

    @staticmethod
    def aqua():
        """
        构造颜色值 (0, 255, 255)

        :return: 颜色值 (0, 255, 255)
        :rtype: Color
        """
        return Color((0, 255, 255))

    @staticmethod
    def aquamarine():
        """
        构造颜色值 (127, 255, 212)

        :return: 颜色值 (127, 255, 212)
        :rtype: Color
        """
        return Color((127, 255, 212))

    @staticmethod
    def azure():
        """
        构造颜色值 (240, 255, 255)

        :return: 颜色值 (240, 255, 255)
        :rtype: Color
        """
        return Color((240, 255, 255))

    @staticmethod
    def beige():
        """
        构造颜色值 (245, 245, 220)

        :return: 颜色值 (245, 245, 220)
        :rtype: Color
        """
        return Color((245, 245, 220))

    @staticmethod
    def bisque():
        """
        构造颜色值 (255,228,196)

        :return: 颜色值 (255,228,196)
        :rtype: Color
        """
        return Color((255, 228, 196))

    @staticmethod
    def black():
        """
        构造颜色值 (0, 0, 0)

        :return: 颜色值 (0, 0, 0)
        :rtype: Color
        """
        return Color((0, 0, 0))

    @staticmethod
    def blanchedalmond():
        """
        构造颜色值 (255,235,205)

        :return: 颜色值 (255,235,205)
        :rtype: Color
        """
        return Color((255, 255, 205))

    @staticmethod
    def blue():
        """
        构造颜色值 (0, 0, 255)

        :return: 颜色值 (0, 0, 255)
        :rtype: Color
        """
        return Color((0, 0, 255))

    @staticmethod
    def blueviolet():
        """
        构造颜色值 (138, 43, 226)

        :return: 颜色值 (138, 43, 226)
        :rtype: Color
        """
        return Color((138, 43, 226))

    @staticmethod
    def burlywood():
        """
        构造颜色值 (222, 184, 135)

        :return: 颜色值 (222, 184, 135)
        :rtype: Color
        """
        return Color((222, 184, 135))

    @staticmethod
    def cadetblue():
        """
        构造颜色值 (95, 158, 160)

        :return: 颜色值 (95, 158, 160)
        :rtype: Color
        """
        return Color((95, 158, 160))

    @staticmethod
    def chartreuse():
        """
        构造颜色值 (127, 255, 0)

        :return: 颜色值 (127, 255, 0)
        :rtype: Color
        """
        return Color((127, 255, 0))

    @staticmethod
    def chocolate():
        """
        构造颜色值 (210, 105, 30)

        :return: 颜色值 (210, 105, 30)
        :rtype: Color
        """
        return Color((210, 105, 30))

    @staticmethod
    def coral():
        """
        构造颜色值 (255, 127, 80)

        :return: 颜色值 (255, 127, 80)
        :rtype: Color
        """
        return Color((255, 127, 80))

    @staticmethod
    def cornflowerblue():
        """
        构造颜色值 (100, 149, 237)

        :return: 颜色值 (100, 149, 237)
        :rtype: Color
        """
        return Color((100, 149, 237))

    @staticmethod
    def cornsilk():
        """
        构造颜色值 (255, 248, 220))

        :return: 颜色值 (255, 248, 220))
        :rtype: Color
        """
        return Color((255, 248, 220))

    @staticmethod
    def crimson():
        """
        构造颜色值 (220, 20, 60)

        :return: 颜色值 (220, 20, 60)
        :rtype: Color
        """
        return Color((220, 20, 60))

    @staticmethod
    def cyan():
        """
        构造颜色值 (0, 255, 255

        :return: 颜色值 (0, 255, 255
        :rtype: Color
        """
        return Color((0, 255, 255))

    @staticmethod
    def darkblue():
        """
        构造颜色值 (0, 0, 139)

        :return: 颜色值 (0, 0, 139)
        :rtype: Color
        """
        return Color((0, 0, 139))

    @staticmethod
    def darkcyan():
        """
        构造颜色值 (0, 139, 139)

        :return: 颜色值 (0, 139, 139)
        :rtype: Color
        """
        return Color((0, 139, 139))

    @staticmethod
    def darkgoldenrod():
        """
        构造颜色值 (184, 134, 11)

        :return: 颜色值 (184, 134, 11)
        :rtype: Color
        """
        return Color((184, 134, 11))

    @staticmethod
    def darkgray():
        """
        构造颜色值 (169, 169, 169)

        :return: 颜色值 (169, 169, 169)
        :rtype: Color
        """
        return Color((169, 169, 169))

    @staticmethod
    def darkgreen():
        """
        构造颜色值 (0, 100, 0)

        :return: 颜色值 (0, 100, 0)
        :rtype: Color
        """
        return Color((0, 100, 0))

    @staticmethod
    def darkkhaki():
        """
        构造颜色值 (189, 183, 107)

        :return: 颜色值 (189, 183, 107)
        :rtype: Color
        """
        return Color((189, 183, 107))

    @staticmethod
    def darkmagena():
        """
        构造颜色值 (139, 0, 139)

        :return: 颜色值 (139, 0, 139)
        :rtype: Color
        """
        return Color((139, 0, 139))

    @staticmethod
    def darkolivegreen():
        """
        构造颜色值 (85, 107, 47)

        :return: 颜色值 (85, 107, 47)
        :rtype: Color
        """
        return Color((85, 107, 47))

    @staticmethod
    def darkorange():
        """
        构造颜色值 (255, 140, 0)

        :return: 颜色值 (255, 140, 0)
        :rtype: Color
        """
        return Color((255, 140, 0))

    @staticmethod
    def darkorchid():
        """
        构造颜色值 (153, 50, 204)

        :return: 颜色值 (153, 50, 204)
        :rtype: Color
        """
        return Color((153, 50, 204))

    @staticmethod
    def darkred():
        """
        构造颜色值 (139, 0, 0)

        :return: 颜色值 (139, 0, 0)
        :rtype: Color
        """
        return Color((139, 0, 0))

    @staticmethod
    def darksalmon():
        """
        构造颜色值 (233, 150, 122)

        :return: 颜色值 (233, 150, 122)
        :rtype: Color
        """
        return Color((233, 150, 122))

    @staticmethod
    def darkseagreen():
        """
        构造颜色值 (143, 188, 143)

        :return: 颜色值 (143, 188, 143)
        :rtype: Color
        """
        return Color((143, 188, 143))

    @staticmethod
    def darkslateblue():
        """
        构造颜色值 (72, 61, 139)

        :return: 颜色值 (72, 61, 139)
        :rtype: Color
        """
        return Color((72, 61, 139))

    @staticmethod
    def darkturquoise():
        """
        构造颜色值 (0, 206, 209)

        :return: 颜色值 (0, 206, 209)
        :rtype: Color
        """
        return Color((0, 206, 209))

    @staticmethod
    def darkviolet():
        """
        构造颜色值 (148, 0, 211)

        :return: 颜色值 (148, 0, 211)
        :rtype: Color
        """
        return Color((148, 0, 211))

    @staticmethod
    def deeppink():
        """
        构造颜色值 (255, 20, 147)

        :return: 颜色值 (255, 20, 147)
        :rtype: Color
        """
        return Color((255, 20, 147))

    @staticmethod
    def deepskyblue():
        """
        构造颜色值 (0, 191, 255)

        :return: 颜色值 (0, 191, 255)
        :rtype: Color
        """
        return Color((0, 191, 255))

    @staticmethod
    def dimgray():
        """
        构造颜色值 (105, 105, 105)

        :return: 颜色值 (105, 105, 105)
        :rtype: Color
        """
        return Color((105, 105, 105))

    @staticmethod
    def dodgerblue():
        """
        构造颜色值 (30, 144, 255)

        :return: 颜色值 (30, 144, 255)
        :rtype: Color
        """
        return Color((30, 144, 255))

    @staticmethod
    def firebrick():
        """
        构造颜色值 (178, 34, 34)

        :return: 颜色值 (178, 34, 34)
        :rtype: Color
        """
        return Color((178, 34, 34))

    @staticmethod
    def floralwhite():
        """
        构造颜色值 (255, 250, 240)

        :return: 颜色值 (255, 250, 240)
        :rtype: Color
        """
        return Color((255, 250, 240))

    @staticmethod
    def forestgreen():
        """
        构造颜色值 (34, 139, 34)

        :return: 颜色值 (34, 139, 34)
        :rtype: Color
        """
        return Color((34, 139, 34))

    @staticmethod
    def fuschia():
        """
        构造颜色值 (255, 0, 255)

        :return: 颜色值 (255, 0, 255)
        :rtype: Color
        """
        return Color((255, 0, 255))

    @staticmethod
    def gainsboro():
        """
        构造颜色值 (220, 220, 220)

        :return: 颜色值 (220, 220, 220)
        :rtype: Color
        """
        return Color((220, 220, 220))

    @staticmethod
    def ghostwhite():
        """
        构造颜色值 (248, 248, 255)

        :return: 颜色值 (248, 248, 255)
        :rtype: Color
        """
        return Color((248, 248, 255))

    @staticmethod
    def gold():
        """
        构造颜色值 (255, 215, 0)

        :return: 颜色值 (255, 215, 0)
        :rtype: Color
        """
        return Color((255, 215, 0))

    @staticmethod
    def goldenrod():
        """
        构造颜色值 (218, 165, 32)

        :return: 颜色值 (218, 165, 32)
        :rtype: Color
        """
        return Color((218, 165, 32))

    @staticmethod
    def gray():
        """
        构造颜色值 (128, 128, 128)

        :return: 颜色值 (128, 128, 128)
        :rtype: Color
        """
        return Color((128, 128, 128))

    @staticmethod
    def green():
        """
        构造颜色值 (0, 128, 0)

        :return: 颜色值 (0, 128, 0)
        :rtype: Color
        """
        return Color((0, 128, 0))

    @staticmethod
    def greenyellow():
        """
        构造颜色值 (173, 255, 47)

        :return: 颜色值 (173, 255, 47)
        :rtype: Color
        """
        return Color((173, 255, 47))

    @staticmethod
    def honeydew():
        """
        构造颜色值 (240, 255, 240)

        :return: 颜色值 (240, 255, 240)
        :rtype: Color
        """
        return Color((240, 255, 240))

    @staticmethod
    def hotpink():
        """
        构造颜色值 (255, 105, 180)

        :return: 颜色值 (255, 105, 180)
        :rtype: Color
        """
        return Color((255, 105, 180))

    @staticmethod
    def indianred():
        """
        构造颜色值 (205, 92, 92)

        :return: 颜色值 (205, 92, 92)
        :rtype: Color
        """
        return Color((205, 92, 92))

    @staticmethod
    def indigo():
        """
        构造颜色值 (75, 0, 130)

        :return: 颜色值 (75, 0, 130)
        :rtype: Color
        """
        return Color((75, 0, 130))

    @staticmethod
    def ivory():
        """
        构造颜色值 (255, 240, 240)

        :return: 颜色值 (255, 240, 240)
        :rtype: Color
        """
        return Color((255, 240, 240))

    @staticmethod
    def khaki():
        """
        构造颜色值 (240, 230, 140)

        :return: 颜色值 (240, 230, 140)
        :rtype: Color
        """
        return Color((240, 230, 140))

    @staticmethod
    def lavender():
        """
        构造颜色值 (230, 230, 250)

        :return: 颜色值 (230, 230, 250)
        :rtype: Color
        """
        return Color((230, 230, 250))

    @staticmethod
    def lavenderblush():
        """
        构造颜色值 (255, 240, 245)

        :return: 颜色值 (255, 240, 245)
        :rtype: Color
        """
        return Color((255, 240, 245))

    @staticmethod
    def lawngreen():
        """
        构造颜色值 (124, 252, 0)

        :return: 颜色值 (124, 252, 0)
        :rtype: Color
        """
        return Color((124, 252, 0))

    @staticmethod
    def lemonchiffon():
        """
        构造颜色值 (255, 250, 205)

        :return: 颜色值 (255, 250, 205)
        :rtype: Color
        """
        return Color((255, 250, 205))

    @staticmethod
    def lightblue():
        """
        构造颜色值 (173, 216, 230)

        :return: 颜色值 (173, 216, 230)
        :rtype: Color
        """
        return Color((173, 216, 230))

    @staticmethod
    def lightcoral():
        """
        构造颜色值 (240, 128, 128)

        :return: 颜色值 (240, 128, 128)
        :rtype: Color
        """
        return Color((240, 128, 128))

    @staticmethod
    def lightcyan():
        """
        构造颜色值 (224, 255, 255)

        :return: 颜色值 (224, 255, 255)
        :rtype: Color
        """
        return Color((224, 255, 255))

    @staticmethod
    def lightgoldenrodyellow():
        """
        构造颜色值 (250, 250, 210)

        :return: 颜色值 (250, 250, 210)
        :rtype: Color
        """
        return Color((250, 250, 210))

    @staticmethod
    def lightgreen():
        """
        构造颜色值 (144, 238, 144)

        :return: 颜色值 (144, 238, 144)
        :rtype: Color
        """
        return Color((144, 238, 144))

    @staticmethod
    def lightgray():
        """
        构造颜色值 (211, 211, 211)

        :return: 颜色值 (211, 211, 211)
        :rtype: Color
        """
        return Color((211, 211, 211))

    @staticmethod
    def lightpink():
        """
        构造颜色值 (255, 182, 193)

        :return: 颜色值 (255, 182, 193)
        :rtype: Color
        """
        return Color((255, 182, 193))

    @staticmethod
    def lightsalmon():
        """
        构造颜色值 (255, 160, 122)

        :return: 颜色值 (255, 160, 122)
        :rtype: Color
        """
        return Color((255, 160, 122))

    @staticmethod
    def lightseagreen():
        """
        构造颜色值 (32, 178, 170)

        :return: 颜色值 (32, 178, 170)
        :rtype: Color
        """
        return Color((32, 178, 170))

    @staticmethod
    def lightskyblue():
        """
        构造颜色值 (135, 206, 250)

        :return: 颜色值 (135, 206, 250)
        :rtype: Color
        """
        return Color((135, 206, 250))

    @staticmethod
    def lightslategray():
        """
        构造颜色值 (119, 136, 153)

        :return: 颜色值 (119, 136, 153)
        :rtype: Color
        """
        return Color((119, 136, 153))

    @staticmethod
    def lightsteelblue():
        """
        构造颜色值 (176, 196, 222)

        :return: 颜色值 (176, 196, 222)
        :rtype: Color
        """
        return Color((176, 196, 222))

    @staticmethod
    def lightyellow():
        """
        构造颜色值 (255, 255, 224)

        :return: 颜色值 (255, 255, 224)
        :rtype: Color
        """
        return Color((255, 255, 224))

    @staticmethod
    def lime():
        """
        构造颜色值 (0, 255, 0)

        :return: 颜色值 (0, 255, 0)
        :rtype: Color
        """
        return Color((0, 255, 0))

    @staticmethod
    def limegreen():
        """
        构造颜色值 (50, 205, 50)

        :return: 颜色值 (50, 205, 50)
        :rtype: Color
        """
        return Color((50, 205, 50))

    @staticmethod
    def linen():
        """
        构造颜色值 (250, 240, 230)

        :return: 颜色值 (250, 240, 230)
        :rtype: Color
        """
        return Color((250, 240, 230))

    @staticmethod
    def magenta():
        """
        构造颜色值 (255, 0, 255)

        :return: 颜色值 (255, 0, 255)
        :rtype: Color
        """
        return Color((255, 0, 255))

    @staticmethod
    def maroon():
        """
        构造颜色值 (128, 0, 0)

        :return: 颜色值 (128, 0, 0)
        :rtype: Color
        """
        return Color((128, 0, 0))

    @staticmethod
    def mediumaquamarine():
        """
        构造颜色值 (102, 205, 170)

        :return: 颜色值 (102, 205, 170)
        :rtype: Color
        """
        return Color((102, 205, 170))

    @staticmethod
    def mediumblue():
        """
        构造颜色值 (0, 0, 205)

        :return: 颜色值 (0, 0, 205)
        :rtype: Color
        """
        return Color((0, 0, 205))

    @staticmethod
    def mediumorchid():
        """
        构造颜色值 (186, 85, 211)

        :return: 颜色值 (186, 85, 211)
        :rtype: Color
        """
        return Color((186, 85, 211))

    @staticmethod
    def mediumpurple():
        """
        构造颜色值 (147, 112, 219)

        :return: 颜色值 (147, 112, 219)
        :rtype: Color
        """
        return Color((147, 112, 219))

    @staticmethod
    def medium_sea_green():
        """
        构造颜色值 (60, 179, 113)

        :return: 颜色值 (60, 179, 113)
        :rtype: Color
        """
        return Color((60, 179, 113))

    @staticmethod
    def mediumslateblue():
        """
        构造颜色值 (123, 104, 238)

        :return: 颜色值 (123, 104, 238)
        :rtype: Color
        """
        return Color((123, 104, 238))

    @staticmethod
    def mediumspringgreen():
        """
        构造颜色值 (0, 250, 154)

        :return: 颜色值 (0, 250, 154)
        :rtype: Color
        """
        return Color((0, 250, 154))

    @staticmethod
    def mediumturquoise():
        """
        构造颜色值 (72, 209, 204)

        :return: 颜色值 (72, 209, 204)
        :rtype: Color
        """
        return Color((72, 209, 204))

    @staticmethod
    def mediumvioletred():
        """
        构造颜色值 (199, 21, 112)

        :return: 颜色值 (199, 21, 112)
        :rtype: Color
        """
        return Color((199, 21, 112))

    @staticmethod
    def midnightblue():
        """
        构造颜色值 (25, 25, 112)

        :return: 颜色值 (25, 25, 112)
        :rtype: Color
        """
        return Color((25, 25, 112))

    @staticmethod
    def mintcream():
        """
        构造颜色值 (245, 255, 250)

        :return: 颜色值 (245, 255, 250)
        :rtype: Color
        """
        return Color((245, 255, 250))

    @staticmethod
    def mistyrose():
        """
        构造颜色值 (255, 228, 225)

        :return: 颜色值 (255, 228, 225)
        :rtype: Color
        """
        return Color((255, 228, 225))

    @staticmethod
    def moccasin():
        """
        构造颜色值 (255, 228, 181)

        :return: 颜色值 (255, 228, 181)
        :rtype: Color
        """
        return Color((255, 228, 181))

    @staticmethod
    def navajowhite():
        """
        构造颜色值 (255, 222, 173)

        :return: 颜色值 (255, 222, 173)
        :rtype: Color
        """
        return Color((255, 222, 173))

    @staticmethod
    def navy():
        """
        构造颜色值 (0, 0, 128)

        :return: 颜色值 (0, 0, 128)
        :rtype: Color
        """
        return Color((0, 0, 128))

    @staticmethod
    def oldlace():
        """
        构造颜色值 (253, 245, 230)

        :return: 颜色值 (253, 245, 230)
        :rtype: Color
        """
        return Color((253, 245, 230))

    @staticmethod
    def olive():
        """
        构造颜色值 (128, 128, 0)

        :return: 颜色值 (128, 128, 0)
        :rtype: Color
        """
        return Color((128, 128, 0))

    @staticmethod
    def olivedrab():
        """
        构造颜色值 (107, 142, 45)

        :return: 颜色值 (107, 142, 45)
        :rtype: Color
        """
        return Color((107, 142, 45))

    @staticmethod
    def orange():
        """
        构造颜色值 (255, 165, 0)

        :return: 颜色值 (255, 165, 0)
        :rtype: Color
        """
        return Color((255, 165, 0))

    @staticmethod
    def orangered():
        """
        构造颜色值 (255, 69, 0)

        :return: 颜色值 (255, 69, 0)
        :rtype: Color
        """
        return Color((255, 69, 0))

    @staticmethod
    def orchid():
        """
        构造颜色值 (218, 112, 214)

        :return: 颜色值 (218, 112, 214)
        :rtype: Color
        """
        return Color((218, 112, 214))

    @staticmethod
    def pale_goldenrod():
        """
        构造颜色值 (238, 232, 170)

        :return: 颜色值 (238, 232, 170)
        :rtype: Color
        """
        return Color((238, 232, 170))

    @staticmethod
    def palegreen():
        """
        构造颜色值 (152, 251, 152)

        :return: 颜色值 (152, 251, 152)
        :rtype: Color
        """
        return Color((152, 251, 152))

    @staticmethod
    def paleturquoise():
        """
        构造颜色值 (175, 238, 238)

        :return: 颜色值 (175, 238, 238)
        :rtype: Color
        """
        return Color((175, 238, 238))

    @staticmethod
    def palevioletred():
        """
        构造颜色值 (219, 112, 147)

        :return: 颜色值 (219, 112, 147)
        :rtype: Color
        """
        return Color((219, 112, 147))

    @staticmethod
    def papayawhip():
        """
        构造颜色值 (255, 239, 213)

        :return: 颜色值 (255, 239, 213)
        :rtype: Color
        """
        return Color((255, 239, 213))

    @staticmethod
    def peachpuff():
        """
        构造颜色值 (255, 218, 155

        :return: 颜色值 (255, 218, 155
        :rtype: Color
        """
        return Color((255, 218, 155))

    @staticmethod
    def peru():
        """
        构造颜色值 (205, 133, 63)

        :return: 颜色值 (205, 133, 63)
        :rtype: Color
        """
        return Color((205, 133, 63))

    @staticmethod
    def pink():
        """
        构造颜色值 (255, 192, 203)

        :return: 颜色值 (255, 192, 203)
        :rtype: Color
        """
        return Color((255, 192, 203))

    @staticmethod
    def plum():
        """
        构造颜色值 (221, 160, 221)

        :return: 颜色值 (221, 160, 221)
        :rtype: Color
        """
        return Color((221, 160, 221))

    @staticmethod
    def powderblue():
        """
        构造颜色值 (176, 224, 230)

        :return: 颜色值 (176, 224, 230)
        :rtype: Color
        """
        return Color((176, 224, 230))

    @staticmethod
    def purple():
        """
        构造颜色值 (128, 0, 128)

        :return: 颜色值 (128, 0, 128)
        :rtype: Color
        """
        return Color((128, 0, 128))

    @staticmethod
    def red():
        """
        构造颜色值 (255, 0, 0)

        :return: 颜色值 (255, 0, 0)
        :rtype: Color
        """
        return Color((255, 0, 0))

    @staticmethod
    def rosybrown():
        """
        构造颜色值 (188, 143, 143)

        :return: 颜色值 (188, 143, 143)
        :rtype: Color
        """
        return Color((188, 143, 143))

    @staticmethod
    def royalblue():
        """
        构造颜色值 (65, 105, 225)

        :return: 颜色值 (65, 105, 225)
        :rtype: Color
        """
        return Color((65, 105, 225))

    @staticmethod
    def saddlebrown():
        """
        构造颜色值 (244, 164, 96)

        :return: 颜色值 (244, 164, 96)
        :rtype: Color
        """
        return Color((244, 164, 96))

    @staticmethod
    def sandybrown():
        """
        构造颜色值 (244, 144, 96)

        :return: 颜色值 (244, 144, 96)
        :rtype: Color
        """
        return Color((244, 144, 96))

    @staticmethod
    def seagreen():
        """
        构造颜色值 (46, 139, 87)

        :return: 颜色值 (46, 139, 87)
        :rtype: Color
        """
        return Color((46, 139, 87))

    @staticmethod
    def seashell():
        """
        构造颜色值 (255, 245, 238)

        :return: 颜色值 (255, 245, 238)
        :rtype: Color
        """
        return Color((255, 245, 238))

    @staticmethod
    def sienna():
        """
        构造颜色值 (160, 82, 45)

        :return: 颜色值 (160, 82, 45)
        :rtype: Color
        """
        return Color((160, 82, 45))

    @staticmethod
    def silver():
        """
        构造颜色值 (192, 192, 192)

        :return: 颜色值 (192, 192, 192)
        :rtype: Color
        """
        return Color((192, 192, 192))

    @staticmethod
    def skyblue():
        """
        构造颜色值 (135, 206, 235)

        :return: 颜色值 (135, 206, 235)
        :rtype: Color
        """
        return Color((135, 206, 235))

    @staticmethod
    def slateblue():
        """
        构造颜色值 (106, 90, 205)

        :return: 颜色值 (106, 90, 205)
        :rtype: Color
        """
        return Color((106, 90, 205))

    @staticmethod
    def slategray():
        """
        构造颜色值 (106, 90, 205)

        :return: 颜色值 (106, 90, 205)
        :rtype: Color
        """
        return Color((106, 90, 205))

    @staticmethod
    def snow():
        """
        构造颜色值 (255, 250, 250)

        :return: 颜色值 (255, 250, 250)
        :rtype: Color
        """
        return Color((255, 250, 250))

    @staticmethod
    def springgreen():
        """
        构造颜色值 (0, 255, 127)

        :return: 颜色值 (0, 255, 127)
        :rtype: Color
        """
        return Color((0, 255, 127))

    @staticmethod
    def steelblue():
        """
        构造颜色值 (70, 130, 180)

        :return: 颜色值 (70, 130, 180)
        :rtype: Color
        """
        return Color((70, 130, 180))

    @staticmethod
    def tan():
        """
        构造颜色值 (210, 180, 140)

        :return: 颜色值 (210, 180, 140)
        :rtype: Color
        """
        return Color((210, 180, 140))

    @staticmethod
    def teal():
        """
        构造颜色值 (0, 128, 128)

        :return: 颜色值 (0, 128, 128)
        :rtype: Color
        """
        return Color((0, 128, 128))

    @staticmethod
    def thistle():
        """
        构造颜色值 (216, 191, 216)

        :return: 颜色值 (216, 191, 216)
        :rtype: Color
        """
        return Color((216, 191, 216))

    @staticmethod
    def tomato():
        """
        构造颜色值 (253, 99, 71)

        :return: 颜色值 (253, 99, 71)
        :rtype: Color
        """
        return Color((253, 99, 71))

    @staticmethod
    def turquoise():
        """
        构造颜色值 (64, 224, 208)

        :return: 颜色值 (64, 224, 208)
        :rtype: Color
        """
        return Color((64, 224, 208))

    @staticmethod
    def violet():
        """
        构造颜色值 (238, 130, 238)

        :return: 颜色值 (238, 130, 238)
        :rtype: Color
        """
        return Color((238, 130, 238))

    @staticmethod
    def wheat():
        """
        构造颜色值 (245, 222, 179)

        :return: 颜色值 (245, 222, 179)
        :rtype: Color
        """
        return Color((245, 222, 179))

    @staticmethod
    def white():
        """
        构造颜色值 (255, 255, 255)

        :return: 颜色值 (255, 255, 255)
        :rtype: Color
        """
        return Color((255, 255, 255))

    @staticmethod
    def white_smoke():
        """
        构造颜色值 (245, 245, 245)

        :return: 颜色值 (245, 245, 245)
        :rtype: Color
        """
        return Color((245, 245, 245))

    @staticmethod
    def yellow():
        """
        构造颜色值 (255, 255, 0)

        :return: 颜色值 (255, 255, 0)
        :rtype: Color
        """
        return Color((255, 255, 0))

    @staticmethod
    def yellowgreen():
        """
        构造颜色值 (154, 205, 50)

        :return: 颜色值 (154, 205, 50)
        :rtype: Color
        """
        return Color((154, 205, 50))

    @staticmethod
    def darkgray():
        """
        构造颜色值 (64, 64, 64)

        :return: 颜色值 (64, 64, 64)
        :rtype: Color
        """
        return Color((64, 64, 64))


class GeoStyle(JVMBase):
    __doc__ = "\n    几何风格类。用于定义点状符号、线状符号、填充符号及其相关设置。对于文本对象只能设置文本风格，不能设置几何风格。\n    除复合数据集(CAD 数据集)之外，其他类型数据集都不存储几何对象的风格信息。\n    填充模式分为普通填充模式和渐变填充模式。在普通填充模式下，可以使用图片或矢量符号等进行填充；在渐变填充模式下，有四种渐变类型可供选择：线性渐变填充，辐射渐变填充，圆锥渐变填充和四角渐变填充\n    "

    def __init__(self):
        JVMBase.__init__(self)

    def _make_java_object(self):
        return self._jvm.com.supermap.data.GeoStyle()

    @staticmethod
    def _from_java_object(java_object):
        if java_object:
            geo_style = GeoStyle()
            geo_style._java_object = java_object
            return geo_style
        return

    @staticmethod
    def point_style(marker_id=0, marker_angle=0.0, marker_size=(4, 4), color=(0, 0, 0)):
        """
        构造一个点对象的对象风格

        :param int marker_id: 点状符号的编码。此编码用于唯一标识各点状符号。点状符号可以用户自定义，也可以使用系统自带的符号库。所指定的线型符号的 ID 值必须是符号库中已存在的 ID 值。
        :param float marker_angle: 点状符号的旋转角度。以度为单位，精确到0.1度，逆时针方向为正方向。此角度可以作为普通填充风格中填充符号的旋转角度。
        :param marker_size: 状符号的大小，单位为毫米，精确到0.1毫米。其值必须大于等于0。如果为0，则表示不显示，如果是小于0，会抛出异常。
        :type marker_size: tuple[int,int]
        :param color: 点状符号的颜色。
        :type color: Color or tuple[int,int,int] or tuple[int,int,int,int]
        :return: 点对象的对象风格
        :rtype: GeoStyle
        """
        if not marker_size:
            marker_size = marker_size(4, 4)
        return GeoStyle().set_marker_symbol_id(marker_id).set_marker_angle(marker_angle).set_marker_size(marker_size[0], marker_size[1]).set_line_color(color)

    @staticmethod
    def line_style(line_id=0, line_width=0.1, color=(0, 0, 0)):
        """
        构造一个线对象的对象风格

        :param int line_id: 线状符号的编码。此编码用于唯一标识各线状符号。线状符号可以用户自定义，也可以使用系统自带的符号库。
        :param float line_width: 线状符号的宽度。单位为毫米，精度到0.1。
        :param color: 状符号型风格
        :type color: Color or tuple[int,int,int] or tuple[int,int,int,int]
        :return: 线对象的对象风格
        :rtype: GeoStyle
        """
        return GeoStyle().set_line_symbol_id(line_id).set_line_width(line_width).set_line_color(color)

    @staticmethod
    def from_xml(xml):
        """
        根据 xml 描述信息构造 GeoStyle 对象

        :param str xml: 描述 GeoStyle 的 xml 信息。具体参考 :py:meth:`to_xml`
        :return: 几何对象风格
        :rtype: GeoStyle
        """
        java_style = get_jvm().com.supermap.data.GeoStyle()
        java_style.fromXML(xml)
        return GeoStyle._from_java_object(java_style)

    def to_xml(self):
        """
        返回表示 GeoStyle 对象的 XML 字符串。

        :rtype: str
        """
        return self._jobject.toXML()

    @property
    def fill_back_color(self):
        """Color: 填充符号的背景色。当填充模式为渐变填充时，该颜色为填充终止色。默认值 Color(255,255,255,255)"""
        return Color._from_java_object(self._jobject.getFillBackColor())

    def set_fill_back_color(self, value):
        """
        设置填充符号的背景色。当填充模式为渐变填充时，该颜色为渐变填充终止色。

        :param value: 用来设置填充符号的背景色。
        :type value: Color or tuple[int,int,int] or tuple[int,int,int,int]
        :return: 对象自身
        :rtype: GeoStyle
        """
        value = Color.make(value)
        if value:
            self._jobject.setFillBackColor(to_java_color(value))
        return self

    @property
    def fill_fore_color(self):
        """Color: 填充符号的前景色。当填充模式为渐变填充时，该颜色为渐变填充起始色。默认值 Color(189,235,255,255)"""
        return Color.make(java_color_to_tuple(self._jobject.getFillForeColor()))

    def set_fill_fore_color(self, value):
        """
        设置填充符号的前景色。当填充模式为渐变填充时，该颜色为渐变填充起始颜色。

        :param value: 用来设置填充符号的前景色
        :type value: Color or tuple[int,int,int] or tuple[int,int,int,int]
        :return: 对象自身
        :rtype: GeoStyle
        """
        value = Color.make(value)
        if value:
            self._jobject.setFillForeColor(to_java_color(value))
        return self

    @property
    def fill_gradient_angle(self):
        """float: 渐变填充的旋转角度，单位为0.1度，逆时针方向为正方向。"""
        return self._jobject.getFillGradientAngle()

    def set_fill_gradient_angle(self, value):
        """
        设置渐变填充的旋转角度，单位为0.1度，逆时针方向为正方向。有关各渐变填充风格类型的定义，请参见 FillGradientMode。
        对于不同的渐变填充，其旋转的后的效果各异，但都是以最小外接矩形的中心为旋转中心，逆时针旋转的:

        * 线性渐变

         当设置的角度为0-360度的任意角度时，经过起始点和终止点的线以最小外接矩形的中心为旋转中心逆时针旋转，渐变风格随之旋转，依然从
         线的起始端渐变到终止端的线性渐变。如下列举在特殊角度的渐变风格：

        - 当渐变填充角度设置为0度或者360度的时候，那么渐变填充风格为由左到右从起始色到终止色的线性渐变，如图所示起始色为黄色，终止色为粉红色；

            .. image: ./image/Fill_360.png

        - 当渐变填充角度设置为180度时，渐变填充风格与1中描述的风格正好相反，即从右到左，从起始色到终止色线性渐变；

            .. image: ./image/Fill_180.png

        - 当渐变填充角度设置为90度时，渐变填充风格为由下到上，起始色到终止色的线性渐变;

            .. image: ./image/Fill_90.png

        - 当渐变填充角度设置为270度时，渐变填充风格与3中描述的风格正好相反，即从上到下，起始色到终止色线性渐变。

            .. image: ./image/Fill_270.png

        * 辐射渐变

         渐变填充角度设置为任何角度（不超出正常范围）时，将定义辐射渐变的圆形按照设置的角度进行旋转，由于圆是关于填充范围的最小外接矩
         形的中心点对称的，所以旋转之后的渐变填充的风格始终保持一样，即从中心点到填充范围的边界，从前景色到背景色的辐射渐变。

        * 圆锥渐变

         当渐变角度设置为0-360度之间的任何角度，该圆锥的所有母线将发生旋转，以圆锥的中心点，即填充区域的最小外接矩形的中心为旋转中心，
         逆时针方向旋转。如图所示的例子中，旋转角度为90度，所有的母线都从起始位置（旋转角度为零的位置）开始旋转到指定角度，以经过起始点的母线为例，其从0度位置旋转到90度位置。

            .. image: ./image/GeoS_Angle1.png

            .. image: ./image/GeoS_Angle2.png

        * 四角渐变

         根据给定的渐变填充角度，将发生渐变的正方形以填充区域范围的中心为中心进行相应的旋转，所有正方形都是从初始位置即旋转角度为零的
         默认位置开始旋转。渐变依然是从内部的正方形到外部的正方形发生从起始色到终止色的渐变.

        :param float value: 来设置渐变填充的旋转角度
        :return: 对象自身
        :rtype: GeoStyle
        """
        self._jobject.setFillGradientAngle(float(value))
        return self

    @property
    def fill_gradient_offset_ratio_x(self):
        """float: 返回渐变填充中心点相对于填充区域范围中心点的水平偏移百分比。设填充区域范围中心点的坐标为（x0,y0），填充中心点的坐
        标为（x，y），填充区域范围的宽度为 a，水平偏移百分比为 dx，则 x=x0 + a*dx/100 该百分比可以为负，当其为负时，填充中心点相对
        于填充区域范围中心点向 x 轴负方向偏移。该方法对辐射渐变、圆锥渐变、四角渐变和线性渐变填充有效。 """
        return self._jobject.getFillGradientOffsetRatioX()

    def set_fill_gradient_offset_ratio_x(self, value):
        """
        设置渐变填充中心点相对于填充区域范围中心点的水平偏移百分比。设填充区域范围中心点的坐标为（x0,y0），填充中心点的坐标为（x，y），
        填充区域范围的宽度为 a，水平偏移百分比为 dx，则 x=x0 + a*dx/100 该百分比可以为负，当其为负时，填充中心点相对于填充区域范围
        中心点向 x 轴负方向偏移。该方法对辐射渐变、圆锥渐变、四角渐变和线性渐变填充有效。

        :param float value: 用于设置填充中心点的水平偏移量的值。
        :return: 对象自身
        :rtype: GeoStyle
        """
        self._jobject.setFillGradientOffsetRatioX(float(value))
        return self

    @property
    def fill_gradient_offset_ratio_y(self):
        """float: 返回填充中心点相对于填充区域范围中心点的垂直偏移百分比。设填充区域范围中心点的坐标为（x0,y0），填充中心点的坐标为
        （x，y），填充区域范围的高度为 b，垂直偏移百分比为 dy，则 y=y0 + b*dy/100 该百分比可以为负，当其为负时，填充中心点相对于填
        充区域范围中心点向 y 轴负方向偏移。该方法对辐射渐变、圆锥渐变、四角渐变和线性渐变填充有效。"""
        return self._jobject.getFillGradientOffsetRatioY()

    def set_fill_gradient_offset_ratio_y(self, value):
        """
        设置填充中心点相对于填充区域范围中心点的垂直偏移百分比。设填充区域范围中心点的坐标为（x0,y0），填充中心点的坐标为（x，y），
        填充区域范围的高度为 b，垂直偏移百分比为 dy，则 y=y0 + b*dy/100 该百分比可以为负，当其为负时，填充中心点相对于填充区域范围
        中心点向 y 轴负方向偏移。该方法对辐射渐变、圆锥渐变、四角渐变和线性渐变填充有效。

        :param float value: 用来设置填充中心点的垂直偏移量的值。
        :return: 对象自身
        :rtype: GeoStyle
        """
        self._jobject.setFillGradientOffsetRatioY(float(value))
        return self

    @property
    def fill_gradient_mode(self):
        """FillGradientMode: 返回渐变填充风格的渐变类型。关于各渐变填充类型的定义，请参见 :py:class:`FillGradientMode` """
        value = self._jobject.getFillGradientMode()
        if value:
            return FillGradientMode._make(value.name())

    def set_fill_gradient_mode(self, value):
        """
        设置渐变填充风格的渐变类型

        :param value: 渐变填充风格的渐变类型。
        :type value: FillGradientMode or str
        :return: 对象自身
        :rtype: GeoStyle
        """
        value = FillGradientMode._make(value)
        if isinstance(value, FillGradientMode):
            self._jobject.setFillGradientMode(oj(value))
        return self

    @property
    def fill_opaque_rate(self):
        """int: 返回填充不透明度，合法值0-100的数值。其值为0表示完全透明；若其值为100表示完全不透明。赋值小于0时按照0处理，大于100时按照100处理。"""
        return self._jobject.getFillOpaqueRate()

    def set_fill_opaque_rate(self, value):
        """
        设置填充不透明度，合法值0-100的数值。其值为0表示空填充；若其值为100表示完全不透明。赋值小于0时按照0处理，大于100时按照100处理。

        :param int value:  用来设置填充不透明度的整数值。
        :return: 对象自身
        :rtype: GeoStyle
        """
        self._jobject.setFillOpaqueRate(int(value))
        return self

    @property
    def fill_symbol_id(self):
        """int: 返回填充符号的编码。此编码用于唯一标识各普通填充风格的填充符号。填充符号可以用户自定义，也可以使用系统自带的符号库。 """
        return self._jobject.getFillSymbolID()

    def set_fill_symbol_id(self, value):
        """
        设置填充符号的编码。此编码用于唯一标识各普通填充风格的填充符号。填充符号可以用户自定义，也可以使用系统自带的符号库。所指定的填充符号的 ID 值必须是符号库中已存在的 ID 值。

        :param int value: 一个整数用来设置填充符号的编码。
        :return: 对象自身
        :rtype: GeoStyle
        """
        self._jobject.setFillSymbolID(int(value))
        return self

    @property
    def line_color(self):
        """Color: 线状符号型风格或点状符号的颜色。 """
        return Color._from_java_object(self._jobject.getLineColor())

    def set_line_color(self, value):
        """
        设置线状符号型风格或点状符号的颜色

        :param value: 一个 Color 对象用来设置线状符号型风格或点状符号的颜色。
        :type value: Color or tuple[int,int,int] or tuple[int,int,int,int]
        :return: 对象自身
        :rtype: GeoStyle
        """
        value = Color.make(value)
        if value:
            self._jobject.setLineColor(to_java_color(value))
        return self

    @property
    def line_symbol_id(self):
        """int: 线状符号的编码。此编码用于唯一标识各线状符号。线状符号可以用户自定义，也可以使用系统自带的符号库。 """
        return self._jobject.getLineSymbolID()

    def set_line_symbol_id(self, value):
        """
        设置线状符号的编码。此编码用于唯一标识各线状符号。 线状符号可以用户自定义，也可以使用系统自带的符号库。所指定的线型符号的 ID 值必须是符号库中已存在的 ID 值。

        :param int value: 一个用来设置线型符号的编码的整数值。
        :return: 对象自身
        :rtype: GeoStyle
        """
        self._jobject.setLineSymbolID(value)
        return self

    @property
    def line_width(self):
        """float: 线状符号的宽度。单位为毫米，精度到0.1。 """
        return self._jobject.getLineWidth()

    def set_line_width(self, value):
        """
        设置线状符号的宽度。单位为毫米，精度到0.1。

        :param float value:
        :return: 对象自身
        :rtype: GeoStyle
        """
        self._jobject.setLineWidth(float(value))
        return self

    @property
    def marker_angle(self):
        """float: 点状符号的旋转角度，以度为单位，精确到0.1度，逆时针方向为正方向。此角度可以作为普通填充风格中填充符号的旋转角度。 """
        return self._jobject.getMarkerAngle()

    def set_marker_angle(self, value):
        """
        设置点状符号的旋转角度，以度为单位，精确到0.1度，逆时针方向为正方向。此角度可以作为普通填充风格中填充符号的旋转角度。

        :param float value: 点状符号的旋转角度。
        :return: 对象自身
        :rtype: GeoStyle
        """
        self._jobject.setMarkerAngle(float(value))
        return self

    @property
    def marker_size(self):
        """tuple[float,float]: 点状符号的大小，单位为毫米，精确到0.1毫米。"""
        size = self._jobject.getMarkerSize()
        return (size.getWidth(), size.getHeight())

    def set_marker_size(self, width, height):
        """
        设置点状符号的大小，单位为毫米，精确到0.1毫米。其值必须大于等于0。如果为0，则表示不显示，如果是小于0，会抛出异常。

        当对点矢量图层设置风格时，如果使用的点符号为 TrueType 字体，在指定点符号的宽高尺寸时，不支持设置宽高值不相等的符号大小，即符号的宽高比例始终为 1：1。当用户设置了宽高值不相等的符号大小时，系统自动将符号大小的宽高值取为相等的值，并且等于用户所指定的高度值。

        :param float width: 宽度
        :param float height: 高度
        :return: 对象自身
        :rtype: GeoStyle
        """
        size = self._jvm.com.supermap.data.Size2D(float(width), float(height))
        self._jobject.setMarkerSize(size)
        return self

    @property
    def marker_symbol_id(self):
        """int: 点状符号的编码。此编码用于唯一标识各点状符号。点状符号可以用户自定义，也可以使用系统自带的符号库。 """
        return self._jobject.getMarkerSymbolID()

    def set_marker_symbol_id(self, value):
        """
        设置点状符号的编码。此编码用于唯一标识各点状符号。 点状符号可以用户自定义，也可以使用系统自带的符号库。 所指定的线型符号的 ID 值必须是符号库中已存在的 ID 值。

        :param int value: 点状符号的编码。
        :return: 对象自身
        :rtype: GeoStyle
        """
        self._jobject.setMarkerSymbolID(int(value))
        return self

    @property
    def is_fill_back_opaque(self):
        """bool: 当前填充背景是否不透明。当前填充背景是不透明的，则为 True，否则为 False。"""
        return self._jobject.getFillBackOpaque()

    def set_fill_back_opaque(self, value):
        """
        设置当前填充背景是否不透明。

        :param bool value: 当前填充背景是否透明，true 为不透明。
        :return: 对象自身
        :rtype: GeoStyle
        """
        self._jobject.setFillBackOpaque(bool(value))
        return self

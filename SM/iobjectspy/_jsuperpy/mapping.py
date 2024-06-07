# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/_jsuperpy\mapping.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 344712 bytes
from .data import Workspace, Colors, DatasetVector, Point2D, Geometry, Dataset, DatasetImage, DatasetGrid, GeoPoint, Rectangle, GeoRegion, PrjCoordSys, QueryParameter, GeoStyle, Feature, CoordSysTransParameter, Color, TextStyle, JoinItem
from data._jvm import JVMBase
from ._gateway import get_jvm
from data._util import get_input_dataset
from .enums import *
from enum import unique
from ._utils import *
from ._logger import log_error, log_warning
from data.ex import ObjectDisposedError
from collections import OrderedDict
__all__ = [
 'Map', 'LayerSetting', 'LayerSettingImage', 'LayerSettingVector', 'LayerSettingGrid', 
 'TrackingLayer', 
 'Layer', 'LayerGridAggregation', 'LayerHeatmap', 
 'ThemeType', 
 'Theme', 'ThemeUniqueItem', 'ThemeUnique', 'ThemeRangeItem', 'RangeMode', 
 'ThemeRange', 
 'MixedTextStyle', 'LabelMatrix', 'LabelMatrixImageCell', 
 'LabelMatrixSymbolCell', 'LabelBackShape', 
 'AvoidMode', 'AlongLineCulture', 
 'AlongLineDirection', 'AlongLineDrawingMode', 
 'OverLengthLabelMode', 'ThemeLabelRangeItem', 
 'ThemeLabelRangeItems', 'ThemeLabelUniqueItem', 
 'ThemeLabelUniqueItems', 
 'ThemeLabel', 'ThemeGraphItem', 'ThemeGraphType', 'ThemeGraphTextFormat', 
 'GraphAxesTextDisplayMode', 
 'ThemeGraph', 'GraduatedMode', 'ThemeGraduatedSymbol', 'ThemeDotDensity', 
 'ThemeGridUniqueItem', 
 'ThemeGridUnique', 'ThemeGridRangeItem', 'ThemeGridRange', 'ThemeCustom']

class LayerSetting(JVMBase):
    __doc__ = "\n    图层设置基类。该类是对图层的显示风格的设置的基类。\n    对矢量数据集，栅格数据集以及影像数据集的图层风格分别使用 LayerSettingVector， LayerSettingGrid 和 LayerSettingImage 类中提供的方法进行设置。\n    矢量图层中所有要素采用相同的渲染风格，栅格图层采用颜色表来显示其像元，影像的图层的风格设置是对影像的亮度，对比度以及透明度等的设置。\n    "

    def __init__(self):
        JVMBase.__init__(self)

    @staticmethod
    def _from_java_object(java_object):
        if not java_object:
            return
        else:
            layer_setting_type = java_object.getType().name()
            if layer_setting_type == "VECTOR":
                layer_setting = LayerSettingVector()
            else:
                if layer_setting_type == "GRID":
                    layer_setting = LayerSettingGrid()
                else:
                    if layer_setting_type == "IMAGE":
                        layer_setting = LayerSettingImage()
                    else:
                        log_warning("Unsupported layer setting type " + layer_setting_type)
                        return
        layer_setting._java_object = java_object
        return layer_setting


class LayerSettingVector(LayerSetting):
    __doc__ = "\n    矢量图层设置类。\n\n    该类主要用来设置矢量图层的显示风格。矢量图层用单一的符号或风格绘制所有的要素。当你只想可视化地显示你的空间数据，只关心空间数据中\n    各要素在什么位置，而不关心各要素在数量或性质上的不同时，可以用普通图层来显示要素数据。\n    "

    def __init__(self, style=None):
        LayerSetting.__init__(self)
        self.set_style(style)

    def _make_java_object(self):
        return self._jvm.com.supermap.mapping.LayerSettingVector()

    def get_style(self):
        """
        返回矢量图层的风格。

        :return: 矢量图层的风格。
        :rtype: GeoStyle
        """
        return GeoStyle._from_java_object(self._jobject.getStyle())

    def set_style(self, style):
        """
        设置矢量图层的风格。

        :param style: 矢量图层的风格。
        :type style: GeoStyle
        :return: self
        :rtype: LayerSettingVector
        """
        if isinstance(style, GeoStyle):
            self._jobject.setStyle(oj(style))
        return self


class LayerSettingGrid(LayerSetting):
    __doc__ = "\n    栅格图层设置类。\n\n    栅格图层设置是针对普通图层而言的。栅格图层采用颜色表来显示其像元。SuperMap 的颜色表是按照 8 比特的 RGB 彩色坐标系来显示像元的，\n    您可以根据像元的属性值来设置其显示颜色值，从而形象直观地表示栅格数据反映的现象。\n\n    "

    def __init__(self):
        LayerSetting.__init__(self)

    def _make_java_object(self):
        return self._jvm.com.supermap.mapping.LayerSettingGrid()

    def get_color_table(self):
        """
        返回颜色表

        :return: 颜色表
        :rtype: Colors
        """
        return Colors._from_java_object(self._jobject.getColorTable())

    def set_color_table(self, value):
        """
        设置颜色表。

        :param Colors value: 颜色表
        :return: self
        :rtype: LayerSettingGrid
        """
        if isinstance(value, Colors):
            self._jobject.setColorTable(oj(value))
        return self

    def get_special_value_color(self):
        """
        返回栅格数据集特殊值数据的颜色。

        :return: 栅格数据集特殊值数据的颜色。
        :rtype: Color
        """
        return Color._from_java_object(self._jobject.getSpecialValueColor())

    def set_special_value_color(self, value):
        """
        设置栅格数据集特殊值数据的颜色。

        :param value: 栅格数据集特殊值数据的颜色。
        :type value: Color or tuple[int,int,int] or tuple[int,int,int,int]
        :return: self
        :rtype: LayerSettingGrid
        """
        value = Color.make(value)
        if isinstance(value, Color):
            self._jobject.setSpecialValueColor(to_java_color(value))
        return self

    def get_special_value(self):
        """
        返回图层的特殊值。 在新增一个 Grid 图层时，该方法的返回值与数据集的 NoValue 属性值相等。

        :return:
        :rtype: float
        """
        return self._jobject.getSpecialValue()

    def set_special_value(self, value):
        """
        设置图层的特殊值。

        :param float value: 图层的特殊值
        :return: self
        :rtype: LayerSettingGrid
        """
        if value is not None:
            self._jobject.setSpecialValue(float(value))
        return self

    def get_brightness(self):
        """
        返回 Grid 图层的亮度，值域范围为 -100 到 100，增加亮度为正，降低亮度为负。

        :return: Grid 图层的亮度。
        :rtype: int
        """
        return self._jobject.getBrightness()

    def set_brightness(self, value):
        """
        设置 Grid 图层的亮度，值域范围为 -100 到 100，增加亮度为正，降低亮度为负。

        :param int value:
        :return: self
        :rtype: LayerSettingGrid
        """
        if value is not None:
            self._jobject.setBrightness(int(value))
        return self

    def get_contrast(self):
        """
        返回 Grid 图层的对比度，值域范围为 -100 到 100，增加对比度为正，降低对比度为负。

        :return: Grid 图层的对比度。
        :rtype: int
        """
        return self._jobject.getContrast()

    def set_contrast(self, value):
        """
        设置 Grid 图层的对比度，值域范围为 -100 到 100，增加对比度为正，降低对比度为负。

        :param int value: Grid 图层的对比度。
        :return: self
        :rtype: LayerSettingGrid
        """
        if value is not None:
            self._jobject.setContrast(int(value))
        return self

    def get_opaque_rate(self):
        """
        返回 Grid 图层显示不透明度。不透明度为一个 0-100 之间的数。0 为不显示；100 为完全不透明。只对栅格图层有效，在地图旋转的情况下也有效。

        :return: Grid 图层显示不透明度。
        :rtype: int
        """
        return self._jobject.getOpaqueRate()

    def set_opaque_rate(self, value):
        """
        设置 Grid 图层显示的不透明度。不透明度为一个 0-100 之间的数。0 为不显示；100 为完全不透明。只对栅格图层有效，在地图旋转的情况下也有效。

        :param int value: Grid 图层显示不透明度。
        :return: self
        :rtype: LayerSettingGrid
        """
        if value is not None:
            self._jobject.setOpaqueRate(int(value))
        return self

    def is_special_value_transparent(self):
        """
        返回图层的特殊值（SpecialValue）所处区域是否透明。

        :return: 一个布尔值，图层的特殊值（SpecialValue）所处区域透明返回 true，否则返回 false。
        :rtype: bool
        """
        return self._jobject.isSpecialValueTransparent()

    def set_special_value_transparent(self, value):
        """
        设置图层的特殊值（SpecialValue）所处区域是否透明。

        :param bool value: 图层的特殊值（SpecialValue）所处区域是否透明。
        :return: self
        :rtype: LayerSettingGrid
        """
        self._jobject.setSpecialValueTransparent(parse_bool(value))
        return self

    def get_color_dictionary(self):
        """
        返回图层的颜色对照表。

        :return: 图层的颜色对照表。
        :rtype: dict[float, Color]
        """
        color_dicts = self._jobject.getColorDictionary()
        if color_dicts:
            keys = color_dicts.getKeys()
            colors = {}
            for key in keys:
                colors[key] = Color._from_java_object(color_dicts.getColor(key))

            return colors

    def set_color_dictionary(self, colors):
        """
        设置图层的颜色对照表

        :param colors: 指定图层的颜色对照表。
        :type colors: dict[float, Color]
        :return: self
        :rtype: LayerSettingGrid
        """
        if isinstance(colors, dict):
            java_color = self._jvm.com.supermap.data.ColorDictionary()
            for key, value in colors.items():
                value = Color.make(value)
                if isinstance(value, Color):
                    java_color.setColor(float(key), to_java_color(value))

            self._jobject.setColorDictionary(java_color)
        return self

    def get_image_interpolation_mode(self):
        """
        返回显示图像时使用的插值算法。

        :return: 显示图像时使用的插值算法
        :rtype: ImageInterpolationMode
        """
        mode = self._jobject.getImageInterpolationMode()
        if mode:
            return ImageInterpolationMode._make(mode.name())
        return

    def set_image_interpolation_mode(self, value):
        """
        设置显示图像时使用的插值算法。

        :param value: 指定的插值算法。
        :type value: ImageInterpolationMode or str
        :return: self
        :rtype: LayerSettingGrid
        """
        value = ImageInterpolationMode._make(value)
        if isinstance(value, ImageInterpolationMode):
            self._jobject.setImageInterpolationMode(oj(value))
        return self


class LayerSettingImage(LayerSetting):
    __doc__ = "\n    影像图层设置类。\n    "

    def __init__(self):
        LayerSetting.__init__(self)

    def _make_java_object(self):
        return self._jvm.com.supermap.mapping.LayerSettingImage()

    def get_background_color(self):
        """
        获取背景值的显示颜色

        :return: 背景值的显示颜色
        :rtype: Color
        """
        return Color._from_java_object(self._jobject.getBackgroundColor())

    def set_background_color(self, value):
        """
        设置指定的背景值的显示颜色。

        :param value: 定的背景值的显示颜色
        :type value: Color or tuple[int,int,int] or tuple[int,int,int,int]
        :return: self
        :rtype: LayerSettingImage
        """
        value = Color.make(value)
        if isinstance(value, Color):
            self._jobject.setBackgroundColor(to_java_color(value))
        return self

    def get_background_value(self):
        """
        获取影像中被视为背景的值

        :return: 影像中被视为背景的值
        :rtype: float
        """
        return self._jobject.getBackgroundValue()

    def set_background_value(self, value):
        """
        设置影像中被视为背景的值

        :param float value: 影像中被视为背景的值
        :return: self
        :rtype: LayerSettingImage
        """
        if value is not None:
            self._jobject.setBackgroundValue(float(value))
        return self

    def get_brightness(self):
        """
        返回影像图层的亮度。值域范围为 -100 到 100，增加亮度为正，降低亮度为负。亮度值可以保存到工作空间。

        :return: 影像图层的亮度值。
        :rtype: int
        """
        return self._jobject.getBrightness()

    def set_brightness(self, value):
        """
        设置影像图层的亮度。值域范围为 -100 到 100，增加亮度为正，降低亮度为负。

        :param int value: 影像图层的亮度值。
        :return: self
        :rtype: LayerSettingImage
        """
        if value is not None:
            self._jobject.setBrightness(int(value))
        return self

    def get_contrast(self):
        """
        返回影像图层的对比度。值域范围为 -100 到 100，增加对比度为正，降低对比度为负。

        :return: 影像图层的对比度。
        :rtype: int
        """
        return self._jobject.getContrast()

    def set_contrast(self, value):
        """
        设置影像图层的对比度。值域范围为 -100 到 100，增加对比度为正，降低对比度为负。

        :param int value: 影像图层的对比度。
        :return: self
        :rtype: LayerSettingImage
        """
        if value is not None:
            self._jobject.setContrast(int(value))
        return self

    def get_display_band_indexes(self):
        """
        返回当前影像图层显示的波段索引。假设当前影像图层有若干波段，当需要按照设置的色彩模式(如 RGB)设置显示波段时，指定色彩(如 RGB 中的红色、绿色、蓝色)对应的波段索引(如0，2，1)即可。

        :return: 当前影像图层显示的波段索引。
        :rtype: list[int]
        """
        return self._jobject.getDisplayBandIndexes()

    def set_display_band_indexes(self, indexes):
        """
        设置当前影像图层显示的波段索引。假设当前影像图层有若干波段，当需要按照设置的色彩模式(如 RGB)设置显示波段时，指定色彩(如 RGB 中的红色、绿色、蓝色)对应的波段索引(如0，2，1)即可。

        :param indexes: 当前影像图层显示的波段索引。
        :type indexes: list[int] or tuple[int]
        :return: self
        :rtype: LayerSettingImage
        """
        values = split_input_list_from_str(indexes)
        if isinstance(values, list):
            self._jobject.setDisplayBandIndexes(to_java_int_array(values))
        return self

    def get_display_color_space(self):
        """
        返回影像图层的色彩显示模式。它会根据影像图层当前的色彩格式和显示的波段将该影像图层以该色彩模式进行显示。

        :return: 影像图层的色彩显示模式。
        :rtype: ColorSpaceType
        """
        return ColorSpaceType._make(self._jobject.getDisplayColorSpace().name())

    def set_display_color_space(self, value):
        """
        设置影像图层的色彩显示模式。它会根据影像图层当前的色彩格式和显示的波段将该影像图层以该色彩模式进行显示。

        :param value: 影像图层的色彩显示模式。
        :type value: ColorSpaceType
        :return: self
        :rtype: LayerSettingImage
        """
        value = ColorSpaceType._make(value)
        if isinstance(value, ColorSpaceType):
            self._jobject.setDisplayColorSpace(oj(value))
        return self

    def get_display_mode(self):
        """
        返回影像显示模式。

        :return: 影像显示模式。
        :rtype: ImageDisplayMode
        """
        return ImageDisplayMode._make(self._jobject.getDisplayMode().name())

    def set_display_mode(self, value):
        """
        设置影像显示模式。

        :param value: 影像显示模式，多波段支持两种显示模式，单波段只支持拉伸显示模式。
        :type value: ImageDisplayMode
        :return: self
        :rtype: LayerSettingImage
        """
        mode = ImageDisplayMode._make(value)
        if isinstance(mode, ImageDisplayMode):
            self._jobject.setDisplayMode(oj(mode))
        return self

    def get_image_interpolation_mode(self):
        """
        设置显示图像时使用的插值算法。

        :return: 显示图像时使用的插值算法
        :rtype: ImageInterpolationMode
        """
        mode = self._jobject.getImageInterpolationMode()
        if mode:
            return ImageInterpolationMode._make(mode.name())
        return

    def set_image_interpolation_mode(self, value):
        """
        设置显示图像时使用的插值算法

        :param value: 指定的插值算法
        :type value: ImageInterpolationMode or str
        :return: self
        :rtype: LayerSettingImage
        """
        value = ImageInterpolationMode._make(value)
        if isinstance(value, ImageInterpolationMode):
            self._jobject.setImageInterpolationMode(oj(value))
            return self
        raise ValueError("required ImageInterpolationMode")

    def get_opaque_rate(self):
        """
        返回影像图层显示的不透明度。不透明度为一个 0-100 之间的数。0为不显示；100为完全不透明。只对影像图层有效，在地图旋转的情况下也有效。

        :return: 影像图层显示的不透明度。
        :rtype: int
        """
        return self._jobject.getOpaqueRate()

    def set_opaque_rate(self, value):
        """
        设置影像图层显示的不透明度。不透明度为一个 0-100 之间的数。0为不显示；100为完全不透明。只对影像图层有效，在地图旋转的情况下也有效

        :param int value: 影像图层显示的不透明度
        :return: self
        :rtype: LayerSettingImage
        """
        if value is not None:
            self._jobject.setOpaqueRate(int(value))
        return self

    def get_special_value(self):
        """
        获取影像中的特殊值。该特殊值可以通过 :py:meth:`set_special_value_color` 指定显示颜色。

        :return: 影像中的特殊值
        :rtype: float
        """
        return self._jobject.getSpecialValue()

    def set_special_value(self, value):
        """
        设置影像中的特殊值，该特殊值可以通过 :py:meth:`set_special_value_color` 指定显示颜色。

        :param float value: 影像中的特殊值
        :return: self
        :rtype: LayerSettingImage
        """
        if value is not None:
            self._jobject.setSpecialValue(float(value))
        return self

    def get_special_value_color(self):
        """
        获取特殊值的显示颜色

        :return: 特殊值的显示颜色
        :rtype: Color
        """
        return Color._from_java_object(self._jobject.getSpecialValueColor())

    def set_special_value_color(self, color):
        """
        设置 :py:meth:`set_special_value` 所设定的特殊值的显示颜色

        :param color: 特殊值的显示颜色
        :type color: Color or tuple[int,int,int] or tuple[int,int,int,int]
        :return: self
        :rtype: LayerSettingImage
        """
        value = Color.make(color)
        if isinstance(value, Color):
            self._jobject.setSpecialValueColor(to_java_color(value))
        return self

    def get_transparent_color(self):
        """
        返回背景透明色

        :return: 背景透明色
        :rtype: Color
        """
        return Color._from_java_object(self._jobject.getTransparentColor())

    def set_transparent_color(self, color):
        """
        设置背景透明色。

        :param color: 背景透明色
        :type color: Color or tuple[int,int,int] or tuple[int,int,int,int]
        :return: self
        :rtype: LayerSettingImage
        """
        color = Color.make(color)
        if isinstance(color, Color):
            self._jobject.setTransparentColor(to_java_color(color))
        return self

    def get_transparent_color_tolerance(self):
        """
        返回背景透明色容限，容限值范围为[0,255]。

        :return: 背景透明色容限
        :rtype: int
        """
        return self._jobject.getTransparentColorTolerance()

    def set_transparent_color_tolerance(self, value):
        """
        设置背景透明色容限，容限值范围为[0,255]。

        :param int value: 背景透明色容限
        :return: self
        :rtype: LayerSettingImage
        """
        if value is not None:
            self._jobject.setTransparentColorTolerance(int(value))
        return self

    def is_transparent(self):
        """
        设置是否使影像图层背景透明

        :return: 一个布尔值指定是否使影像图层背景透明。
        :rtype: bool
        """
        return self._jobject.isTransparent()

    def set_transparent(self, value):
        """
        设置是否使影像图层背景透明

        :param bool value: 一个布尔值指定是否使影像图层背景透明
        :return: self
        :rtype: LayerSettingImage
        """
        self._jobject.setTransparent(parse_bool(value))
        return self


class Layer(JVMBase):
    __doc__ = "\n    图层类。\n\n    该类提供了图层显示和控制等的便于地图管理的一系列方法。当数据集被加载到地图窗口中显示时，就形成了一个图层，因此图层是数据集的可视\n    化显示。一个图层是对一个数据集的引用或参考。\n    图层分为普通图层和专题图层，矢量的普通图层中所有要素采用相同的渲染风格，栅格图层采用颜色表来显示其像元；而专题图层的则采用指定类\n    型的专题图风格来渲染其中的要素或像元。影像数据只对应普通图层。普通图层的风格通过 :py:meth:`get_layer_setting`\n     和 :py:meth:`set_layer_setting` 方法来返回或设置。\n\n    该类的实例不可被创建。只可以通过在 :py:class:`Map` 类 :py:meth:`Map.add_dataset` 方法来创建\n    "

    def __init__(self, java_object):
        JVMBase.__init__(self)
        self._java_object = java_object
        self._theme = None

    def from_xml(self, xml):
        """
        根据指定的XML字符串创建图层对象。 任何图层都可以导出成xml字符串，而图层的xml字符串也可以导入成为一个图层来进行显示。图层的
        xml字符串中存储了关于图层的显示的设置以及关联的数据信息等对图层的所有的设置。可以将图层的xml字符串保存成一个xml文件。

        :param str xml: 用来创建图层的XML字符串
        :return: 创建成功则返回true，否则返回false。

        :rtype: bool
        """
        if xml:
            return self._jobject.fromXML(str(xml))
        return False

    def to_xml(self):
        """
        返回此图层对象的 XML字符串形式的描述。 任何图层都可以导出成xml字符串，而图层的xml字符串也可以导入成为一个图层来进行显示。图
        层的xml字符串中存储了关于图层的显示的设置以及关联的数据信息等对图层的所有的设置。可以将图层的xml字符串保存成一个xml文件。

        :return: 返回此图层对象的 XML字符串形式的描述。
        :rtype: str
        """
        return self._jobject.toXML()

    @property
    def bounds(self):
        """Rectangle: 图层的范围"""
        return Rectangle._from_java_object(self._jobject.getBounds())

    @property
    def dataset(self):
        """Dataset: 返回此图层对应的数据集对象。图层是对数据集的引用，因而，一个图层与一个数据集相对应。 """
        java_dt = self._jobject.getDataset()
        if java_dt:
            ds = Workspace().get_datasource(java_dt.getDatasource().getAlias())
            return ds.get_dataset(java_dt.getName())

    def set_dataset(self, dt):
        """
        设置此图层对应的数据集对象。图层是对数据集的引用，因而，一个图层与一个数据集相对应

        :param Dataset dt: 此图层对应的数据集对象
        :return: self
        :rtype: Layer
        """
        dt = get_input_dataset(dt)
        if isinstance(dt, Dataset):
            if dt == self.dataset:
                return self
            self._jobject.setDataset(oj(dt))
            return self
        raise ValueError("required Dataset")

    @property
    def caption(self):
        """str: 返回图层的标题。图层的标题为图层的显示名称，例如在图例或排版制图时显示的图层的名称即为图层的标题。注意与图层的名称相区别。 """
        return self._jobject.getCaption()

    def set_caption(self, value):
        """
        设置图层的标题。图层的标题为图层的显示名称，例如在图例或排版制图时显示的图层的名称即为图层的标题。注意与图层的名称相区别。

        :param str value: 指定图层的标题。
        :return: self
        :rtype: Layer
        """
        if value is not None:
            self._jobject.setCaption(str(value))
        return self

    def get_clip_region(self):
        """
        返回图层的裁剪区域。

        :return: 返回图层的裁剪区域。
        :rtype: GeoRegion
        """
        region = self._jobject.getClipRegion()
        if region:
            return Geometry._from_java_object(region)

    def set_clip_region(self, region):
        """
        设置图层的裁剪区域。

        :param region:  图层的裁剪区域。
        :type region: GeoRegion or Rectangle
        :return: self
        :rtype: Layer
        """
        if isinstance(region, Rectangle):
            region = region.to_region()
        if isinstance(region, GeoRegion):
            self._jobject.setClipRegion(oj(region))
            return self
        raise ValueError("required GeoRegion")

    def get_display_filter(self):
        """
        返回图层显示过滤条件。通过设置显示过滤条件，可以使图层中的一些要素显示，而另一些要素不显示，以便重点分析感兴趣的要素，而过滤掉其他要素。

        注意：该方法仅支持属性查询，不支持空间查询

        :return: 图层显示过滤条件。
        :rtype: QueryParameter
        """
        param = self._jobject.getDisplayFilter()
        if param:
            return QueryParameter._from_java_object(param)
        return

    def set_display_filter(self, parameter):
        """
        设置图层显示过滤条件。通过设置显示过滤条件，可以使图层中的一些要素显示，而另一些要素不显示，以便重点分析感兴趣的要素，而过滤掉其他要素。比如说通过连接（JoinItem）的方式将一个外部表的字段作为专题图的表达字段，在生成专题图后进行显示时，需要调用此方法，否则专题图将创建失败。

        注意：该方法仅支持属性查询，不支持空间查询

        :param QueryParameter parameter:  指定图层显示过滤条件。
        :return: self
        :rtype: Layer
        """
        if isinstance(parameter, QueryParameter):
            self._jobject.setDisplayFilter(oj(parameter))
            return self
        return self

    def get_max_visible_scale(self):
        """
        返回此图层的最大可见比例尺。最大可见比例尺不可为负，当地图的当前显示比例尺大于或等于图层最大可见比例尺时，此图层将不显示。

        :return: 图层的最大可见比例尺。
        :rtype: float
        """
        return self._jobject.getMaxVisibleScale()

    def set_max_visible_scale(self, value):
        """
        设置此图层的最大可见比例尺。最大可见比例尺不可为负，当地图的当前显示比例尺大于或等于图层最大可见比例尺时，此图层将不显示。

        :param float value: 指定图层的最大可见比例尺。
        :return: self
        :rtype: Layer
        """
        if value is not None:
            self._jobject.setMaxVisibleScale(float(value))
        return self

    def get_min_visible_scale(self):
        """

        :return:
        :rtype: float
        """
        return self._jobject.getMinVisibleScale()

    def set_min_visible_scale(self, value):
        """
        返回此图层的最小可见比例尺。最小可见比例尺不可为负。当地图的当前显示比例尺小于图层最小可见比例尺时，此图层将不显示。

        :param float value: 图层的最小可见比例尺。
        :return: self
        :rtype: Layer
        """
        if value is not None:
            self._jobject.setMinVisibleScale(float(value))
        return self

    def get_opaque_rate(self):
        """
        返回图层的不透明度。

        :return: 图层的不透明度。
        :rtype: int
        """
        return self._jobject.getOpaqueRate()

    def set_opaque_rate(self, value):
        """
        设置图层的不透明度。

        :param int value: 图层的不透明度。
        :return: self
        :rtype: Layer
        """
        if value is not None:
            self._jobject.setOpaqueRate(int(value))
        return self

    def is_antialias(self):
        """
        返回图层是否开启反走样。

        :return: 指示图层是否开启反走样。true 为开启反走样，false 为不开启。
        :rtype: bool
        """
        return self._jobject.isAntialias()

    def set_antialias(self, value):
        """
        设置图层是否开启反走样。

        :param bool value: 指示图层是否开启反走样。true 为开启反走样，false 为不开启。
        :return: self
        :rtype: Layer
        """
        self._jobject.setAntialias(parse_bool(value))
        return self

    def is_clip_region_enabled(self):
        """
        返回裁剪区域是否有效。

        :return: 指定裁剪区域是否有效。true 表示有效，false 表示无效。
        :rtype: bool
        """
        return self._jobject.isClipRegionEnabled()

    def set_clip_region_enabled(self, value):
        """
        设置裁剪区域是否有效。

        :param bool value: 指定裁剪区域是否有效，true 表示有效，false 表示无效。

        :return: self
        :rtype: Layer
        """
        self._jobject.setClipRegionEnabled(parse_bool(value))
        return self

    def is_symbol_scalable(self):
        """
        返回图层的符号大小是否随图缩放。默认为 false。true 表示当图层被放大或缩小时，符号也随之放大或缩小。

        :return: 图层的符号大小是否随图缩放。
        :rtype: bool
        """
        return self._jobject.isSymbolScalable()

    def set_symbol_scalable(self, value):
        """
        设置图层的符号大小是否随图缩放。默认为 false。true 表示当图层被放大或缩小时，符号也随之放大或缩小。

        :param bool value: 指定图层的符号大小是否随图缩放。
        :return: self
        :rtype: Layer
        """
        self._jobject.setSymbolScalable(parse_bool(value))
        return self

    def is_visible(self):
        """
        返回此图层是否可见。true 表示此图层可见，false 表示图层不可见。当图层不可见时，其他所有的属性的设置将无效

        :return: 图层是否可见。
        :rtype: bool
        """
        return self._jobject.isVisible()

    def set_visible(self, value):
        """
        设置此图层是否可见。true 表示此图层可见，false 表示图层不可见。当图层不可见时，其他所有的属性的设置将无效。

        :param bool value: 指定图层是否可见。
        :return: self
        :rtype: Layer
        """
        self._jobject.setVisible(parse_bool(value))
        return self

    def is_visible_scale(self, scale):
        """
        返回指定的比例尺是否为可视比例尺，即在设定的最小显示比例尺和最大显示比例尺之间

        :param float scale: 指定的显示比例尺。
        :return: 返回 true，表示指定的比例尺为可视比例尺；否则为 false。
        :rtype: bool
        """
        if scale:
            return self._jobject.isVisibleScale(float(scale))

    def get_layer_setting(self):
        """
        返回普通图层的风格设置。普通图层风格的设置对矢量数据图层，栅格数据图层以及影像数据图层是不相同的。
        :py:class:`LayerSettingVector` , :py:class:`LayerSettingGrid` ， :py:class:`LayerSettingImage`  类分别用来对矢量数
        据图层，栅格数据图层和影像数据图层的风格进行设置和修改。

        :return: 普通图层的风格设置
        :rtype: LayerSetting
        """
        java_setting = self._jobject.getAdditionalSetting()
        if java_setting:
            return LayerSetting._from_java_object(java_setting)

    def set_layer_setting(self, setting):
        """
        设置普通图层的风格

        :param LayerSetting setting: 普通图层的风格设置。
        :return: self
        :rtype: Layer
        """
        if isinstance(setting, LayerSetting):
            self._jobject.setAdditionalSetting(oj(setting))
        return self

    def get_theme(self):
        """
        返回专题图层的专题图对象，针对专题图层。

        :return: 专题图层的专题图对象
        :rtype: Theme
        """
        if self._theme:
            return self._theme
        java_theme = self._jobject.getTheme()
        if java_theme is not None:
            self._theme = Theme._from_java_object(java_theme)
        return self._theme

    def _set_theme(self, value):
        self._theme = value
        return self


class LayerHeatmap(Layer):
    __doc__ = "\n    热力图图层类，该类继承自Layer类。\n\n    热力图是通过颜色分布，描述诸如人群分布、密度和变化趋势等的一种地图表现手法，因此，能够非常直观地呈现一些原本不易理解或表达的数据，比如密度、频度、温度等。\n    热力图图层除了可以反映点要素的相对密度，还可以表示根据属性进行加权的点密度，以此考虑点本身的权重对于密度的贡献。\n    热力图图层将随地图放大或缩小而发生更改，是一种动态栅格表面，例如，绘制全国旅游景点的访问客流量的热力图，当放大地图后，该热力图就可以反映某省内或者局部地区的旅游景点访问客流量分布情况。\n    "

    def __init__(self, java_object):
        Layer.__init__(self, java_object)

    def get_colorset(self):
        """
        返回用于显示当前热力图的颜色集合。

        :return: 用于显示当前热力图的颜色集合
        :rtype: Colors
        """
        return Colors._from_java_object(self._jobject.getColorset())

    def set_colorset(self, colors):
        """
        设置用于显示当前热力图的颜色集合。

        :param colors: 用于显示当前热力图的颜色集合
        :type colors: Colors
        :return: self
        :rtype: LayerHeatmap
        """
        if isinstance(colors, Colors):
            self._jobject.setColorset(oj(colors))
        return self

    def get_fuzzy_degree(self):
        """
        返回热力图中颜色渐变的模糊程度。

        :return: 热力图中颜色渐变的模糊程度
        :rtype: float
        """
        return self._jobject.getFuzzyDegree()

    def set_fuzzy_degree(self, value):
        """
        设置热力图中颜色渐变的模糊程度。

        :param float value: 热力图中颜色渐变的模糊程度。
        :return: self
        :rtype: LayerHeatmap
        """
        if value is not None:
            self._jobject.setFuzzyDegree(float(value))
        return self

    def get_intensity(self):
        """
        返回热力图中高点密度颜色（MaxColor）和低点密度颜色（MinColor）确定渐变色带中高点密度颜色（MaxColor）所占的比重，该值越
        大，表示在色带中高点密度颜色所占比重越大。

        :return: 热力图中高点密度颜色（MaxColor）和低点密度颜色（MinColor）确定渐变色带中高点密度颜色（MaxColor）所占的比重
        :rtype: float
        """
        return self._jobject.getIntensity()

    def set_intensity(self, value):
        """
        设置热力图中高点密度颜色（MaxColor）和低点密度颜色（MinColor）确定渐变色带中高点密度颜色（MaxColor）所占的比重，该值越大，表示在色带中高点密度颜色所占比重越大。

        :param float value: 热力图中高点密度颜色（MaxColor）和低点密度颜色（MinColor）确定渐变色带中高点密度颜色（MaxColor）所占的比重
        :return: self
        :rtype: LayerHeatmap
        """
        if value is not None:
            self._jobject.setIntensity(float(value))
        return self

    def get_kernel_radius(self):
        """
        返回用于计算密度的核半径。单位为：屏幕坐标。

        :return: 用于计算密度的核半径
        :rtype: int
        """
        return self._jobject.getKernelRadius()

    def set_kernel_radius(self, value):
        """
        设置用于计算密度的核半径。单位为：屏幕坐标。
        核半径在热力图中所起的作用如下所述：

        - 热力图将根据设置的核半径值对每个离散点建立一个缓冲区。核半径数值的单位为：屏幕坐标；

        - 对每个离散点建立缓冲区后，对每个离散点的缓冲区，使用渐进的灰度带（完整的灰度带是0~255）从内而外，由浅至深地填充；

        - 由于灰度值可以叠加（值越大颜色越亮，在灰度带中则显得越白。在实际中，可以选择ARGB模型中任一通道作为叠加灰度值），从而对于有缓冲区交叉的区域，可以叠加灰度值，因而缓冲区交叉的越多，灰度值越大，这块区域也就越“热”；

        - 以叠加后的灰度值为索引，从一条有256种颜色的色带中（例如彩虹色）映射颜色，并对图像重新着色，从而实现热力图。

        查找半径越大，生成的密度栅格越平滑且概化程度越高；值越小，生成的栅格所显示的信息越详细。

        :param int value: 计算密度的核半径
        :return: self
        :rtype: LayerHeatmap
        """
        if value is not None:
            self._jobject.setKernelRadius(int(value))
        return self

    def get_max_color(self):
        """
        返回高点密度的颜色，热力图图层将通过高点密度颜色（MaxColor）和低点密度颜色（MinColor）确定渐变的颜色方案。

        :return: 高点密度的颜色
        :rtype: Color
        """
        return Color._from_java_object(self._jobject.getMaxColor())

    def set_max_color(self, value):
        """
        设置高点密度的颜色，热力图图层将通过高点密度颜色（MaxColor）和低点密度颜色（MinColor）确定渐变的颜色方案。

        :param value: 高点密度的颜色
        :type value: Color or tuple[int,int,int]
        :return: self
        :rtype: LayerHeatmap
        """
        value = Color.make(value)
        if isinstance(value, Color):
            self._jobject.setMaxColor(to_java_color(value))
        return self

    def get_max_value(self):
        """
        返回一个最大值。当前热力图图层中最大值（MaxValue）与最小值（MinValue）之间栅格将使用MaxColor和MinColor所确定的色带进行渲
        染，其他大于MaxValue的栅格将以MaxColor渲染；而者小于MinValue的栅格将以MinColor渲染。

        :return: 最大值
        :rtype: float
        """
        return self._jobject.getMaxValue()

    def set_max_value(self, value):
        """
        设置一个最大值。当前热力图图层中最大值（MaxValue）与最小值（MinValue）之间栅格将使用MaxColor和MinColor所确定的色带进行渲
        染，其他大于MaxValue的栅格将以MaxColor渲染；而者小于MinValue的栅格将以MinColor渲染。 如果没有指定最大最小值，系统将自动
        计算获得当前热力图图层中的最大和最小值。

        :param float value: 最大值
        :return: self
        :rtype: LayerHeatmap
        """
        if value is not None:
            self._jobject.setMaxValue(float(value))
        return self

    def get_min_color(self):
        """
        返回低点密度的颜色，热力图图层将通过高点密度颜色（MaxColor）和低点密度颜色（MinColor）确定渐变的颜色方案。

        :return: 低点密度的颜色
        :rtype: Color
        """
        return Color._from_java_object(self._jobject.getMinColor())

    def set_min_color(self, value):
        """
        设置低点密度的颜色，热力图图层将通过高点密度颜色（MaxColor）和低点密度颜色（MinColor）确定渐变的颜色方案。

        :param value: 低点密度的颜色
        :type value: Color or tuple[int,int,int]
        :return: self
        :rtype: LayerHeatmap
        """
        value = Color.make(value)
        if isinstance(value, Color):
            self._jobject.setMinColor(to_java_color(value))
        return self

    def get_min_value(self):
        """
        返回一个最小值。当前热力图图层中最大值（MaxValue）与最小值（MinValue）之间栅格将使用MaxColor和MinColor所确定的色带进行渲
        染，其他大于MaxValue的栅格将以MaxColor渲染；而者小于MinValue的栅格将以MinColor渲染。

        :return: 最小值
        :rtype: float
        """
        return self._jobject.getMinValue()

    def set_min_value(self, value):
        """
        设置一个最小值。当前热力图图层中最大值（MaxValue）与最小值（MinValue）之间栅格将使用MaxColor和MinColor所确定的色带进行渲
        染，其他大于MaxValue的栅格将以MaxColor渲染；而者小于MinValue的栅格将以MinColor渲染。

        :param float value: 最小值
        :return: self
        :rtype: LayerHeatmap
        """
        if value is not None:
            self._jobject.setMinValue(float(value))
        return self

    def get_weight_field(self):
        """
        返回权重字段。热力图图层除了可以反映点要素的相对密度，还可以表示根据权重字段进行加权的点密度，以此考虑点本身的权重对于密度的贡献。

        :return: 权重字段
        :rtype: str
        """
        return self._jobject.getWeightField()

    def set_weight_field(self, value):
        """
        设置权重字段。热力图图层除了可以反映点要素的相对密度，还可以表示根据权重字段进行加权的点密度，以此考虑点本身的权重对于密度的贡献。
        根据核半径（KernelRadius）确定的离散点缓冲区，其叠加确定了热度分布密度，而权重则是确定了点对于密度的影响力，点的权重值确定了
        该点缓冲区的对于密度的影响力，即如果点缓冲区原来的影响系数为1，点的权重值为10，则引入权重后，该点缓冲区的影响系数为1*10=10，以此类推其他离散点缓冲区的密度影响系数。

        那么，引入权重后，将获得一个新的叠加后的灰度值为索引，在利用指定的色带为其着色，从而实现引入权重的热力图。

        :param str value: 权重字段。热力图图层除了可以反映点要素的相对密度，还可以表示根据权重字段进行加权的点密度，以此考虑点本身的权重对于密度的贡献。
        :return: self
        :rtype: LayerHeatmap
        """
        if value is not None:
            self._jobject.setWeightField(str(value))
        return self


class LayerGridAggregation(Layer):
    __doc__ = "\n    网格聚合图\n    "

    def __init__(self, java_object):
        Layer.__init__(self, java_object)

    def get_colorset(self):
        """
        返回网格单元统计值最大值对应的颜色，网格聚合图将通过MaxColor和MinColor确定渐变的颜色方案，然后基于网格单元统计值大小排序，对网格单元进行颜色渲染。

        :return: 网格单元统计值最大值对应的颜色
        :rtype: Colors
        """
        java_colorset = self._jobject.getColorset()
        return Colors._from_java_object(java_colorset)

    def set_colorset(self, colors):
        """
        设置网格单元统计值最大值对应的颜色，网格聚合图将通过MaxColor和MinColor确定渐变的颜色方案，然后基于网格单元统计值大小排序，对网格单元进行颜色渲染。

        :param colors: 网格单元统计值最大值对应的颜色
        :type colors: Colors
        :return: self
        :rtype: LayerGridAggregation
        """
        if isinstance(colors, Colors):
            self._jobject.setColorset(oj(colors))
        return self

    def get_grid_type(self):
        """
        返回网格聚合图的格网类型

        :return: 网格聚合图的格网类型
        :rtype: LayerGridAggregationType
        """
        java_type = self._jobject.getGridAggregationType()
        if java_type:
            return LayerGridAggregationType._make(java_type.name())

    def set_grid_type(self, value):
        """
        设置网格聚合图的格网类型，可以为矩形网格或者六边形网格。

        :param value: 网格聚合图的格网类型
        :type value: LayerGridAggregationType or str
        :return: self
        :rtype: LayerGridAggregation
        """
        value = LayerGridAggregationType._make(value)
        if isinstance(value, LayerGridAggregationType):
            self._jobject.setGridAggregationType(oj(value))
        return self

    def get_grid_height(self):
        """
        返回设置矩形格网的高度。单位为：屏幕坐标。

        :return: 矩形格网的高度
        :rtype: int
        """
        return self._jobject.getGridHeight()

    def set_grid_height(self, value):
        """
        设置矩形格网的高度。单位为：屏幕坐标。

        :param int value: 矩形格网的高度
        :return: self
        :rtype: LayerGridAggregation
        """
        if value is not None:
            self._jobject.setGridHeight(int(value))
        return self

    def get_grid_width(self):
        """
        返回六边形格网的边长，或者矩形格网的宽度。单位为：屏幕坐标。

        :return: 六边形格网的边长，或者矩形格网的宽度
        :rtype: int
        """
        return self._jobject.getGridwidth()

    def set_grid_width(self, value):
        """
        设置六边形格网的边长，或者矩形格网的宽度。单位为：屏幕坐标。

        :param int value: 六边形格网的边长，或者矩形格网的宽度
        :return: self
        :rtype: LayerGridAggregation
        """
        if value is not None:
            self._jobject.setGridWidth(int(value))
        return self

    def get_max_color(self):
        """
        返回网格单元统计值最大值对应的颜色，网格聚合图将通过MaxColor和MinColor确定渐变的颜色方案，然后基于网格单元统计值大小排序，对网格单元进行颜色渲染。

        :return: 网格单元统计值最大值对应的颜色
        :rtype: Color
        """
        return Color._from_java_object(self._jobject.getMaxColor())

    def set_max_color(self, value):
        """
        设置网格单元统计值最大值对应的颜色，网格聚合图将通过MaxColor和MinColor确定渐变的颜色方案，然后基于网格单元统计值大小排序，对网格单元进行颜色渲染。

        :param value: 网格单元统计值最大值对应的颜色
        :type value: Color or tuple[int,int,int]
        :return: self
        :rtype: LayerGridAggregation
        """
        value = Color.make(value)
        if isinstance(value, Color):
            self._jobject.setMaxColor(to_java_color(value))
        return self

    def get_min_color(self):
        """
        返回网格单元统计值最小值对应的颜色，网格聚合图将通过MaxColor和MinColor确定渐变的颜色方案，然后基于网格单元统计值大小排序，对网格单元进行颜色渲染。

        :return: 网格单元统计值最小值对应的颜色
        :rtype: Color
        """
        return Color._from_java_object(self._jobject.getMinColor())

    def set_min_color(self, value):
        """
        设置网格单元统计值最小值对应的颜色，网格聚合图将通过MaxColor和MinColor确定渐变的颜色方案，然后基于网格单元统计值大小排序，对网格单元进行颜色渲染。

        :param value: 网格单元统计值最小值对应的颜色
        :type value: Color or tuple[int,int,int]
        :return: self
        :rtype: LayerGridAggregation
        """
        value = Color.make(value)
        if isinstance(value, Color):
            self._jobject.setMinColor(to_java_color(value))
        return self

    def get_weight_field(self):
        """
        返回权重字段。网格聚合图每个网格单元的统计值默认为落在该单元格内的点对象数目，此外，还可以引入点的权重信息，考虑网格单元内点的加权值作为网格的统计值。

        :return: 权重字段
        :rtype: str
        """
        return self._jobject.getWeightField()

    def set_weight_field(self, value):
        """
        设置权重字段。网格聚合图每个网格单元的统计值默认为落在该单元格内的点对象数目，此外，还可以引入点的权重信息，考虑网格单元内点的加权值作为网格的统计值。

        :param str value: 权重字段。网格聚合图每个网格单元的统计值默认为落在该单元格内的点对象数目，此外，还可以引入点的权重信息，考虑网格单元内点的加权值作为网格的统计值。
        :return: self
        :rtype: LayerGridAggregation
        """
        if value is not None:
            self._jobject.setWeightField(str(value))
        return self

    def is_show_label(self):
        """
        是否显示网格单元标签

        :return: 是否显示网格单元标签，true表示显示；false表示不显示。
        :rtype: bool
        """
        return self._jobject.getIsShowGridLabel()

    def set_show_label(self, value):
        """
        设置是否显示网格单元标签。

        :param bool value: 指示是否显示网格单元标签，true表示显示；false表示不显示。
        :return: self
        :rtype: LayerGridAggregation
        """
        self._jobject.setIsShowGridLabel(parse_bool(value))
        return self

    def get_label_style(self):
        """
        返回网格单元内统计值标签的风格。

        :return: 网格单元内统计值标签的风格。
        :rtype: TextStyle
        """
        text_style = self._jobject.getGridLabelStyle()
        if text_style:
            return TextStyle._from_java_object(text_style)

    def set_label_style(self, value):
        """
        设置网格单元内统计值标签的风格。

        :param value: 网格单元内统计值标签的风格。
        :type value: TextStyle
        :return: self
        :rtype: LayerGridAggregation
        """
        if isinstance(value, TextStyle):
            self._jobject.setGridLabelStyle(oj(value))
        return self

    def get_line_style(self):
        """
        返回网格单元矩形边框线的风格。

        :return: 网格单元矩形边框线的风格
        :rtype: GeoStyle
        """
        return GeoStyle._from_java_object(self._jobject.getGridLineStyle())

    def set_line_style(self, value):
        """
        设置网格单元矩形边框线的风格。

        :param value: 网格单元矩形边框线的风格
        :type value: GeoStyle
        :return: self
        :rtype: LayerGridAggregation
        """
        if isinstance(value, GeoStyle):
            self._jobject.setGridLineStyle(oj(value))
        return self

    def get_original_point_style(self):
        """
        返回点数据显示的风格。对网格聚合图进行放大浏览，当比例尺较大时，将不显示聚合的网格效果，而显示原始点数据内容。

        :return: 点数据显示的风格。
        :rtype: GeoStyle
        """
        return GeoStyle._from_java_object(self._jobject.getOriginalPointStyle())

    def set_original_point_style(self, value):
        """
        设置点数据显示的风格。 对网格聚合图进行放大浏览，当比例尺较大时，将不显示聚合的网格效果，而显示原始点数据内容。

        :param value: 点数据显示的风格
        :type value: GeoStyle
        :return: self
        :rtype: LayerGridAggregation
        """
        if isinstance(value, GeoStyle):
            self._jobject.setOriginalPointStyle(oj(value))
        return self

    def update_data(self):
        """
        根据数据变化自动更新当前网格聚合图

        :return: self
        :rtype: LayerGridAggregation
        """
        self._jobject.updateData()
        return self


class TrackingLayer(JVMBase):
    __doc__ = "\n    跟踪图层类。\n\n    在 SuperMap 中，每个地图窗口都有一个跟踪图层，确切地说，每个地图显示时都有一个跟踪图层。 跟踪图层是一个空白的透明图层，总是在地\n    图各图层的最上层，主要用于在一个处理或分析过程中，临时存放一些图形对象，以及一些文本等。 只要地图显示，跟踪图层就会存在，你不可\n    以删除跟踪图层，也不可以改变其位置。\n\n    在 SuperMap 中跟踪图层的作用主要有以下方面：\n\n    - 当不想往记录集中添加几何对象，而又需要这个几何对象的时候，就可以把这个几何对象临时添加到跟踪图层上，用完该几何对象之后清除跟踪\n      图层即可。例如，当需要测量距离时，需要在地图上拉一条线，但是这一条线在地图上并不存在，此时就可以使用跟踪图层来实现。\n\n    - 当需要对目标进行动态跟踪的时候，如果把目标放到记录集中，要实现动态跟踪就得不断地刷新整个图层，这样会大大影响效率，如果将这个需\n      要进行跟踪地目标放到跟踪层上，这样就只需要刷新跟踪图层即可实现动态跟踪。\n\n    - 当需要进行批量地往记录集中添加几何对象的时候，可以先将这些对象临时放在跟踪图层上，确定需要添加之后再把跟踪图层上的几何对象批量\n      地添加到记录集中。\n\n    请注意避免把跟踪图层作为存储大量临时几何对象的容器，如果有大量的临时数据，建议在本地计算机临时目录下（如：c:\temp）创建临时数据\n    源，并在临时数据源中创建相应的临时数据集来保存临时数据。\n\n    你可以对跟踪图层进行控制，包括控制跟踪图层是否可显示以及符号是否随图缩放。跟普通图层不同的是，跟踪图层中的对象是不保存的，只是在\n    地图显示时，临时存在内存中。当地图关闭后，跟踪图层中的对象依然存在，相应内存释放掉才会消失，当地图再次被打开后，跟踪图层又显示为\n    一个空白而且透明的图层。\n\n    该类提供了对跟踪图层上的几何对象进行添加，删除等管理的方法。并且可以通过设置标签的方式对跟踪图层上的几何对象进行分类，你可以将标\n    签理解为对几何对象的描述，相同用途的几何对象可以具有相同的标签。\n    "

    def __init__(self, java_object):
        JVMBase.__init__(self)
        self._java_object = java_object

    def add(self, geo, tag):
        """
        向当前跟踪图层中添加一个几何对象，并给出其标签信息。

        :param geo: 要添加的几何对象。
        :type geo: Rectangle or Geometry or Point2D or Feature
        :param str tag: 要添加的几何对象的标签。
        :return: 添加到跟踪图层的几何对象的索引。
        :rtype: int
        """
        if isinstance(geo, Rectangle):
            geo = geo.to_region()
        else:
            if isinstance(geo, Point2D):
                geo = GeoPoint(geo)
            else:
                if isinstance(geo, Feature):
                    geo = geo.geometry
                elif not isinstance(geo, Geometry):
                    raise ValueError("required Geometry")
                if tag:
                    tag = str(tag)
                else:
                    tag = ""
                return self._jobject.add(oj(geo), tag)

    def get_tag(self, index):
        """
        返回此跟踪图层中指定索引的几何对象的标签。

        :param int index: 要返回标签的几何对象的索引。
        :return: 此跟踪图层中指定索引的几何对象的标签。
        :rtype: str
        """
        if index < 0:
            index = index + self._jobject.getCount()
        return self._jobject.getTag(index)

    def set_tag(self, index, tag):
        """
        设置此跟踪图层中指定索引的几何对象的标签

        :param int index: 要设置标签的几何对象的索引。
        :param str tag: 几何对象的新标签。
        :return: 设置成功返回 true；否则返回 false。
        :rtype: bool
        """
        if index < 0:
            index = index + self._jobject.getCount()
        return self._jobject.setTag(index, str(tag))

    def index_of(self, tag):
        """
        返回第一个与指定标签相同的几何对象所处的索引值。

        :param str tag: 需要进行索引检查的标签。
        :return: 返回第一个与指定标签相同的几何对象所处的索引值。
        :rtype: int
        """
        if tag:
            tag = str(tag)
        else:
            raise ValueError("tag required str")
        return self._jobject.indexOf(tag)

    def remove(self, index):
        """
        在当前跟踪图层中删除指定索引的几何对象。

        :param int index: 要删除的几何对象的索引。
        :return: 删除成功返回 true；否则返回 false。
        :rtype: bool
        """
        if index < 0:
            index = index + self._jobject.getCount()
        return self._jobject.remove(int(index))

    def clear(self):
        """
        清空此跟踪图层中的所有几何对象。

        :return: self
        :rtype: TrackingLayer
        """
        self._jobject.clear()
        return self

    def flush_bulk_edit(self):
        """
        批量更新时强制刷新并保存本次批量编辑的数据。

        :return: 强制刷新返回 true，否则返回 false。
        :rtype: bool
        """
        return self._jobject.flushBulkEdit()

    def start_edit_bulk(self):
        """
        开始批量更新

        :return: self
        :rtype: TrackingLayer
        """
        return self._jobject.setEditBulk(True)

    def finish_edit_bulk(self):
        """
        完成批量更新

        :return: self
        :rtype: TrackingLayer
        """
        self.flush_bulk_edit()
        self._jobject.setEditBulk(False)
        return self

    def get(self, index):
        """
        返回此跟踪图层中指定索引的几何对象。

        :param int index:
        :return: 指定索引的几何对象。
        :rtype: Geometry
        """
        if index < 0:
            index = index + self._jobject.getCount()
        geo = self._jobject.get(int(index))
        if geo:
            return Geometry._from_java_object(geo)

    def set(self, index, geo):
        """
        将跟踪图层中的指定的索引处的几何对象替换为指定的几何对象，若此索引处原先有其他几何对象，则会被删除。

        :param int index:  要替换几何对象的索引。
        :param geo: 用来替换的新 Geometry 对象。
        :type geo: Geometry or Point2D or Rectangle or Feature
        :return: 替换成功返回 true；否则返回 false。
        :rtype: bool
        """
        if isinstance(geo, Rectangle):
            geo = geo.to_region()
        else:
            if isinstance(geo, Point2D):
                geo = GeoPoint(geo)
            else:
                if isinstance(geo, Feature):
                    geo = geo.geometry
                else:
                    assert isinstance(geo, Geometry), "required Geometry"
                if index < 0:
                    index = index + self._jobject.getCount()
                return self._jobject.set(int(index), oj(geo))

    def __len__(self):
        return self._jobject.getCount()

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, value):
        self.set(key, value)

    def __delitem__(self, key):
        self.remove(key)

    def get_symbol_scale(self):
        """
        返回此跟踪图层的符号缩放基准比例尺。

        :return: 跟踪图层的符号缩放基准比例尺。
        :rtype: float
        """
        return self._jobject.getSymbolScale()

    def set_symbol_scale(self, value):
        """
        设置此跟踪图层的符号缩放基准比例尺。

        :param float value: 此跟踪图层的符号缩放基准比例尺。
        :return: self
        :rtype: TrackingLayer
        """
        if value is not None:
            self._jobject.setSymbolScale(float(value))
        return self

    def is_antialias(self):
        """
        返回一个布尔值指定是否反走样跟踪图层。文本、线型被设置为反走样后，可以去除一些显示锯齿，使显示更加美观。如图分别为线型和文本
        反走样前和反走样后的效果对比

        :return: 反走样跟踪图层返回 true；否则返回 false。
        :rtype: bool
        """
        return self._jobject.isAntialias()

    def set_antialias(self, value):
        """
        设置一个布尔值指定是否反走样跟踪图层。

        :param bool value: 指定是否反走样跟踪图层。
        :return: self
        :rtype: TrackingLayer
        """
        self._jobject.setAntialias(parse_bool(value))
        return self

    def is_symbol_scalable(self):
        """
        返回跟踪图层的符号大小是否随图缩放。true 表示当随着地图的缩放而缩放，在地图放大的同时，符号同时也放大。

        :return: 一个布尔值指示跟踪图层的符号大小是否随图缩放。
        :rtype: bool
        """
        return self._jobject.isSymbolScalable()

    def set_symbol_scalable(self, value):
        """
        设置跟踪图层的符号大小是否随图缩放。true 表示当随着地图的缩放而缩放，在地图放大的同时，符号同时也放大。

        :param bool value: 一个布尔值指示跟踪图层的符号大小是否随图缩放。
        :return: self
        :rtype: TrackingLayer
        """
        self._jobject.setSymbolScalable(parse_bool(value))
        return self

    def is_visible(self):
        """
        返回此跟踪图层是否可见。true 表示此跟踪图层可见，false 表示此跟踪图层不可见。当此跟踪图层不可见时，其他的设置都将无效。

        :return: 指示此图层是否可见。
        :rtype: bool
        """
        return self._jobject.isVisible()

    def set_visible(self, value):
        """
        设置此跟踪图层是否可见。true 表示此跟踪图层可见，false 表示此跟踪图层不可见。当此跟踪图层不可见时，其他的设置都将无效。

        :param bool value: 指示此图层是否可见。
        :return: self
        :rtype: TrackingLayer
        """
        self._jobject.setVisible(parse_bool(value))
        return self


class Map(JVMBase):
    __doc__ = "\n    地图类，负责地图显示环境的管理。\n\n    地图是对地理数据的可视化，通常由一个或多个图层组成。地图必须与一个工作空间相关联，以便来显示该工作空间中的数据。另外，对地图的显\n    示方式的设置将对其中的所有图层起作用。该类提供了对地图的各种显示方式的返回和设置，如地图的显示范围，比例尺，坐标系统以及文本、点\n    等图层的默认显示方式等，并提供了对地图进行的相关操作的方法，如地图的打开与关闭，缩放、全幅显示，以及地图的输出等。\n    "

    def __init__(self):
        JVMBase.__init__(self)
        self._java_object = self._jvm.com.supermap.mapping.Map(oj(Workspace()))
        self._dict_layer = OrderedDict()

    def open(self, name):
        """
        打开指定名称的地图。该指定名称为地图所关联的工作空间中的地图集合对象中的一个地图的名称，注意与地图的显示名称相区别。

        :param str name: 地图名称。
        :return:
        :rtype: bool
        """
        return self._jobject.open(str(name))

    def close(self):
        """
        关闭当前地图。
        """
        self._jobject.close()

    def set_image_size(self, width, height):
        """
        设置出图时图片的大小，以像素为单位。

        :param int width: 出图时图片的宽度
        :param int height: 出图时图片的高度
        :return: self
        :rtype: Map
        """
        if width:
            if height:
                dimension = self._jvm.java.awt.Dimension(int(width), int(height))
                self._jobject.setImageSize(dimension)
                return self
        raise ValueError("invalid input for width and height")

    def get_image_size(self):
        """
        返回出图时图片的大小，以像素为单位

        :return: 返回出图时图片的宽度和高度
        :rtype: tuple[int,int]
        """
        size = self._jobject.getImageSize()
        return (int(size.getWidth()), int(size.getHeight()))

    def set_dpi(self, dpi):
        """
        设置地图的DPI，代表每英寸有多少个像素，值域为(60，180)。

        :param float dpi: 图的DPI
        :return: self
        :rtype: Map
        """
        self._jobject.setDPI(float(dpi))
        return self

    def get_dpi(self):
        """
        返回地图的DPI，代表每英寸有多少个像素

        :return: 地图的DPI
        :rtype: float
        """
        return self._jobject.getDPI()

    def refresh(self, refresh_all=False):
        """
        重新绘制当前地图。

        :param bool refresh_all: 当 refresh_all 为 TRUE 时，在刷新地图时，同时刷新其中的快照图层。 快照图层，一种特殊的图层组，
                                 该图层组包含的图层作为地图的一个快照图层，采用特殊的绘制方式，快照图层只在第一次显示时进行绘制，
                                 此后，如果地图显示范围未发生变化，快照图层都将使用该显示，也就是快照图层不随地图刷新而重新绘制；
                                 如果地图显示范围发生变化，将自动触发快照图层的刷新绘制。快照图层是提高地图显示性能的手段之一。
                                 如果地图的显示范围不发生变化，刷新地图时，快照图层是不刷新的；如果需要强制刷新可以通过 refresh_all
                                 刷新地图便可以同时刷新快照图层。

        :return: self
        :rtype: Map
        """
        if refresh_all:
            self._jobject.refreshWithSnapshot()
        else:
            self._jobject.refresh()
        return self

    def refresh_tracking_layer(self):
        """
        用于刷新地图窗口中的跟踪图层。

        :return: self
        :rtype: Map
        """
        self._jobject.refreshTrackingLayer()
        return self

    def from_xml(self, xml, workspace_version=None):
        """
        根据指定的 XML 字符串创建地图对象。
        任何地图都可以导出成 xml 字符串，而地图的 xml 字符串也可以导入成为一个地图来显示。地图的 xml 字符串中存储了关于地图及其图
        层的显示设置以及关联的数据信息等。

        :param str xml: 用来创建地图的 xml 字符串。
        :param workspace_version: xml 内容所对应的工作空间的版本。使用该参数时，请确保指定的版本与 xml 内容相符。若不相符，可能会导致部分图层的风格丢失。
        :type workspace_version: WorkspaceVersion or str
        :return: 若地图对象创建成功，返回 true，否则返回 false。
        :rtype: bool
        """
        if workspace_version:
            workspace_version = WorkspaceVersion._make(workspace_version)
        if workspace_version:
            return self._jobject.fromXML(xml, oj(workspace_version))
        return self._jobject.fromXML(xml)

    def to_xml(self):
        """
        返回此地图对象的 XML 字符串形式的描述。
        任何地图都可以导出成 xml 字符串，而地图的 xml 字符串也可以导入成为一个地图来显示。地图的 xml 字符串中存储了关于地图及其图
        层的显示设置以及关联的数据信息等。此外，可以将地图的 xml 字符串保存成一个 xml 文件。

        :return: 地图的 XML 形式的描述
        :rtype: str
        """
        return self._jobject.toXML()

    def get_angle(self):
        """
        返回当前地图的旋转角度。单位为度，精度到 0.1 度。逆时针方向为正方向，如果用户输入负值，地图则以顺时针方向旋转。

        :return: 当前地图的旋转角度。
        :rtype: float
        """
        return self._jobject.getAngle()

    def set_angle(self, value):
        """
        设置当前地图的旋转角度。单位为度，精度到 0.1 度。逆时针方向为正方向，如果用户输入负值，地图则以顺时针方向旋转

        :param float value: 指定当前地图的旋转角度。
        :return: self
        :rtype: Map
        """
        if value is not None:
            self._jobject.setAngle(float(value))
        return self

    def set_view_bounds(self, bounds):
        """
        设置当前地图的可见范围，也称显示范围。当前地图的可见范围除了可以通过 :py:meth:`set_view_bounds` 方法来进行设置，还可以通过设置显示范
        围的中心点（:py:meth:`set_center`）和显示比例尺（:py:meth:`set_scale`）的方式来进行设置。

        :param Rectangle bounds: 指定当前地图的可见范围。
        :return: self
        :rtype: Map
        """
        bounds = Rectangle.make(bounds)
        if isinstance(bounds, Rectangle):
            self._jobject.setViewBounds(oj(bounds))
        return self

    def get_view_bounds(self):
        """
        返回当前地图的可见范围，也称显示范围。当前地图的可见范围除了可以通过 :py:meth:`set_view_bounds` 方法来进行设置，还可以通过设置显示范
        围的中心点（:py:meth:`set_center`）和显示比例尺（:py:meth:`set_scale`）的方式来进行设置。

        :return: 当前地图的可见范围。
        :rtype: Rectangle
        """
        return Rectangle._from_java_object(self._jobject.getViewBounds())

    def get_bounds(self):
        """
        返回当前地图的空间范围。地图的空间范围是其所显示的各数据集的范围的最小外接矩形，即包含各数据集范围的最小的矩形。当地图显示的数据集增加或删除时，其空间范围也会相应发生变化。

        :return: 当前地图的空间范围。
        :rtype: Rectangle
        """
        return Rectangle._from_java_object(self._jobject.getBounds())

    def get_prj(self):
        """
        返回地图的投影坐标系统

        :return: 地图的投影坐标系统。
        :rtype: PrjCoordSys
        """
        return PrjCoordSys._from_java_object(self._jobject.getPrjCoordSys())

    def set_prj(self, prj):
        """
        设置地图的投影坐标系统

        :param prj: 地图的投影坐标系统。
        :type prj: PrjCoordSys
        :return: self
        :rtype: Map
        """
        prj = PrjCoordSys.make(prj)
        if isinstance(prj, PrjCoordSys):
            self._jobject.setPrjCoordSys(oj(prj))
        return self

    def get_scale(self):
        """
        返回当前地图的显示比例尺。

        :return: 当前地图的显示比例尺。
        :rtype: float
        """
        return self._jobject.getScale()

    def set_scale(self, scale):
        """
        设置当前地图的显示比例尺。

        :param float scale: 指定当前地图的显示比例尺。
        :return: self
        :rtype: Map
        """
        self._jobject.setScale(float(scale))
        return self

    def get_min_scale(self):
        """
        返回地图的最小比例尺

        :return: 地图的最小比例尺。
        :rtype: float
        """
        return self._jobject.getMinScale()

    def set_min_scale(self, scale):
        """
        设置地图的最小比例尺。

        :param float scale: 地图的最小比例尺。
        :return: self
        :rtype: Map
        """
        self._jobject.setMinScale(float(scale))
        return self

    def get_max_scale(self):
        """
        返回地图的最大比例尺。

        :return: 地图的最大比例尺。
        :rtype: float
        """
        return self._jobject.getMaxScale()

    def set_max_scale(self, scale):
        """
        设置地图的最大比例尺

        :param float scale:  地图的最大比例尺。
        :return: self
        :rtype: Map
        """
        self._jobject.setMaxScale(float(scale))
        return self

    def get_clip_region(self):
        """
        返回地图显示裁剪的区域。
        用户可以任意设定一个地图显示的区域，该区域外的地图内容，将不会显示。

        :return: 地图显示裁剪的区域。
        :rtype: GeoRegion
        """
        clip_region = self._jobject.getClipRegion()
        if clip_region:
            return GeoRegion._from_java_object(clip_region)

    def set_clip_region(self, region):
        """
        设置地图显示裁剪的区域。
        用户可以任意设定一个地图显示的区域，该区域外的地图内容，将不会显示。

        :param region: 地图显示裁剪的区域。
        :type region: GeoRegion or Rectangle
        :return: self
        :rtype: Map
        """
        if isinstance(region, Rectangle):
            region = region.to_region()
        if isinstance(region, GeoRegion):
            self._jobject.setClipRegion(oj(region))
        return self

    def is_clip_region_enabled(self):
        """
        返回地图显示裁剪区域是否有效，true 表示有效。

        :return: 地图显示裁剪区域是否有效
        :rtype: bool
        """
        return self._jobject.isClipRegionEnabled()

    def set_clip_region_enabled(self, value):
        """
        设置地图显示裁剪区域是否有效，true 表示有效。

        :param bool value: 显示裁剪区域是否有效。
        :return: self
        :rtype: Map
        """
        self._jobject.setClipRegionEnabled(parse_bool(value))
        return self

    def view_entire(self):
        """
        全幅显示此地图。

        :return: self
        :rtype: Map
        """
        self._jobject.viewEntire()
        return self

    def zoom(self, ratio):
        """
        将地图放大或缩小指定的比例。缩放之后地图的比例尺=原比例尺 *ratio，其中 ratio 必须为正数，当 ratio 为大于1时，地图被放大；
        当 ratio 小于1时，地图被缩小。

        :param float ratio: 缩放地图比例，此值不可以为负。
        :return: self
        :rtype: Map
        """
        self._jobject.zoom(float(ratio))
        return self

    def get_center(self):
        """
        返回当前地图的显示范围的中心点。

        :return: 地图的显示范围的中心点。
        :rtype: Point2D
        """
        return Point2D._from_java_object(self._jobject.getCenter())

    def set_center(self, center):
        """
        设置当前地图的显示范围的中心点。

        :param Point2D center: 当前地图的显示范围的中心点。
        :return: self
        :rtype: Map
        """
        center = Point2D.make(center)
        if isinstance(center, Point2D):
            self._jobject.setCenter(oj(center))
        return self

    def get_color_mode(self):
        """
        返回当前地图的颜色模式。地图的颜色模式包括彩色模式，黑白模式，灰度模式以及黑白反色模式等，具体请参见 :py:class:`MapColorMode` 类。

        :return: 地图的颜色模式
        :rtype: MapColorMode
        """
        return MapColorMode._make(self._jobject.getColorMode().name())

    def set_color_mode(self, value):
        """
        设置当前地图的颜色模式

        :param value: 指定当前地图的颜色模式。
        :type value: str or MapColorMode
        :return: self
        :rtype: Map
        """
        value = MapColorMode._make(value)
        if isinstance(value, MapColorMode):
            self._jobject.setColorMode(oj(value))
        return self

    def get_description(self):
        """
        返回当前地图的描述信息。

        :return: 当前地图的描述信息。
        :rtype: str
        """
        return self._jobject.getDescription()

    def set_description(self, value):
        """
        设置当前地图的描述信息。

        :param str value: 指定当前地图的描述信息。
        :return: self
        :rtype: Map
        """
        if value is not None:
            self._jobject.setDescription(str(value))
        return self

    def is_dynamic_projection(self):
        """
        返回是否允许地图动态投影显示。地图动态投影显示是指如果当前地图窗口中地图的投影信息与数据源的投影信息不同，利用地图动态投影显
        示可以将当前地图的投影信息转换为数据源的投影信息。

        :return: 是否允许地图动态投影显示。
        :rtype: bool
        """
        return self._jobject.isDynamicProjection()

    def set_dynamic_projection(self, value):
        """
        设置是否允许地图动态投影显示。地图动态投影显示是指如果当前地图窗口中地图的投影信息与数据源的投影信息不同，利用地图动态投影显
        示可以将当前地图的投影信息转换为数据源的投影信息。

        :param bool value: 是否允许地图动态投影显示。
        :return: self
        :rtype: Map
        """
        self._jobject.setDynamicProjection(parse_bool(value))
        return self

    def get_dynamic_prj_trans_method(self):
        """
        返回地图动态投影时所使用的地理坐标系转换算法。默认值为 :py:attr:`CoordSysTransMethod.MTH_GEOCENTRIC_TRANSLATION`

        :return: 地图动态投影时所使用的投影算法
        :rtype: CoordSysTransMethod
        """
        method = self._jobject.getDynamicPrjTransMethod()
        if method:
            return CoordSysTransMethod._make(method.name())

    def set_dynamic_prj_trans_method(self, value):
        """
        设置地图动态投影时，当源投影与目标目标投影所基于的地理坐标系不同时，需要设置该转换算法。

        :param value: 地理坐标系转换算法
        :type value: CoordSysTransMethod or str
        :return: self
        :rtype: Map
        """
        value = CoordSysTransMethod._make(value)
        if isinstance(value, CoordSysTransMethod):
            self._jobject.setDynamicPrjTransMethod(oj(value))
        return self

    def get_dynamic_prj_trans_parameter(self):
        """
        设置地图动态投影时，当源投影与目标目标投影所基于的地理坐标系不同时，可以通过该方法设置转换参数。

        :return: 动态投影坐标系的转换参数。
        :rtype: CoordSysTransParameter
        """
        parameter = self._jobject.getDynamicPrjTransParameter()
        if parameter:
            return CoordSysTransParameter._from_java_object(parameter)

    def set_dynamic_prj_trans_parameter(self, parameter):
        """
        设置动态投影坐标系的转换参数。

        :param CoordSysTransParameter parameter: 动态投影坐标系的转换参数。
        :return: self
        :rtype: Map
        """
        if isinstance(parameter, CoordSysTransParameter):
            self._jobject.setDynamicPrjTransParameter(oj(parameter))
        return self

    def _refresh_dict_layers(self):
        layers = self._jobject.getLayers()
        if layers:
            temp_layer_dict = OrderedDict()
            for i in range(layers.getCount()):
                java_layer = layers.get(i)
                handle = self._get_object_handle(java_layer)
                if handle in self._dict_layer.keys():
                    temp_layer_dict[handle] = self._dict_layer[handle]
                else:
                    temp_layer_dict[handle] = Layer(java_layer)

            self._dict_layer.clear()
            self._dict_layer = temp_layer_dict
        else:
            self._dict_layer.clear()
        return self

    def get_layers(self):
        """
        返回当前地图所包含的所有图层。

        :return: 当前地图所包含的所有图层对象。
        :rtype: list[Layer]
        """
        self._refresh_dict_layers()
        return list(self._dict_layer.values())

    def get_name(self):
        """
        返回当前地图的名称。

        :return: 当前地图的名称。
        :rtype: str
        """
        return self._jobject.getName()

    def set_name(self, name):
        """
        设置当前地图的名称。

        :param str name: 当前地图的名称。
        :return: self
        :rtype: Map
        """
        if name:
            self._jobject.setName(str(name))
        return self

    def is_fill_marker_angle_fixed(self):
        """
        返回是否固定填充符号的填充角度。

        :return: 是否固定填充符号的填充角度。
        :rtype: bool
        """
        return self._jobject.isFillMarkerAngleFixed()

    def set_fill_marker_angle_fixed(self, value):
        """
        设置是否固定填充符号的填充角度。

        :param bool value:  是否固定填充符号的填充角度。
        :return: self
        :rtype: Map
        """
        self._jobject.setFillMarkerAngleFixed(parse_bool(value))
        return self

    def is_line_antialias(self):
        """
        返回是否地图线型反走样显示。

        :return: 是否地图线型反走样显示。
        :rtype: bool
        """
        return self._jobject.isLineAntialias()

    def set_line_antialias(self, value):
        """
        设置是否地图线型反走样显示。

        :param bool value:  是否地图线型反走样显示。
        :return: self
        :rtype: Map
        """
        self._jobject.setLineAntialias(parse_bool(value))
        return self

    def is_marker_angle_fixed(self):
        """
        返回一个布尔值指定点状符号的角度是否固定。针对地图中的所有点图层。

        :return: 用于指定点状符号的角度是否固定。
        :rtype: bool
        """
        return self._jobject.isMarkerAngleFixed()

    def set_mark_angle_fixed(self, value):
        """
        设置一个布尔值指定点状符号的角度是否固定。针对地图中的所有点图层。

        :param bool value: 指定点状符号的角度是否固定
        :return: self
        :rtype: Map
        """
        self._jobject.setMarkerAngleFixed(parse_bool(value))
        return self

    def is_map_thread_drawing_enabled(self):
        """
        返回是否另启线程绘制地图元素，true表示另启线程绘制地图元素，可以提升大数据量地图的绘制性能。

        :return: 指示是否另启线程绘制地图元素，true表示另启线程绘制地图元素，可以提升大数据量地图的绘制性能。
        :rtype: bool
        """
        return self._jobject.isMapThreadDrawingEnabled()

    def set_map_thread_drawing_enabled(self, value):
        """
        设置是否另启线程绘制地图元素，true表示另启线程绘制地图元素，可以提升大数据量地图的绘制性能。

        :param bool value: 一个布尔值，指示是否另启线程绘制地图元素，true表示另启线程绘制地图元素，可以提升大数据量地图的绘制性能。
        :return: self
        :rtype: Map
        """
        self._jobject.setMapThreadDrawingEnabled(parse_bool(value))
        return self

    def is_use_system_dpi(self):
        """
        是否使用系统的 DPI

        :return: 是否使用系统 DPI
        :rtype: bool
        """
        return self._jobject.isUseSystemDPI()

    def set_use_system_dpi(self, value):
        """
        设置是否使用系统 DPI

        :param bool value: 是否使用系统 DPI。True，表示使用系统的DPI，False，表示使用地图的设置。
        :return: self
        :rtype: Map
        """
        self._jobject.setUseSystemDPI(parse_bool(value))
        return self

    @staticmethod
    def _output_to_file(that_map, file_name, image_type, is_back_transparent):
        if image_type is ImageType.GIF:
            is_ok = oj(that_map).outputMapToGIF(file_name, is_back_transparent)
        else:
            if image_type is ImageType.BMP:
                is_ok = oj(that_map).outputMapToBMP(file_name)
            else:
                if image_type is ImageType.JPG:
                    is_ok = oj(that_map).outputMapToJPG(file_name)
                else:
                    if image_type is ImageType.PNG:
                        is_ok = oj(that_map).outputMapToPNG(file_name, is_back_transparent)
                    else:
                        if image_type is ImageType.TIFF:
                            is_ok = oj(that_map).outputMapToFile(file_name, oj(image_type), int(that_map.get_dpi()), oj(that_map.get_view_bounds()), is_back_transparent)
                        else:
                            if image_type is ImageType.PDF:
                                is_ok = oj(that_map).outputMapToPDF(file_name)
                            else:
                                raise ValueError("Unsupported image type " + image_type.name)
        return is_ok

    def output_to_file(self, file_name, output_bounds=None, dpi=0, image_size=None, is_back_transparent=False, is_show_to_ipython=False):
        """
        将当前地图输出的文件中，支持 BMP, PNG, JPG, GIF, PDF, TIFF 文件。不保存跟踪图层。

        :param str file_name: 结果文件路径，必须带文件后缀名。
        :param image_size: 设置出图时图片的大小，以像素为单位。如果不设置，使用当前地图的 image_size，具体参考 :py:meth:`.get_image_size`
        :type image_size: tuple[int,int]
        :param Rectangle output_bounds: 地图输出范围。如果不设置，默认使用当前地图的视图范围，具体参考 :py:meth:`.get_view_bounds`
        :param int dpi: 地图的DPI，代表每英寸有多少个像素。如果不设置，默认使用当前地图的 DPI，具体参考 :py:meth:`.get_dpi`
        :param bool is_back_transparent: 是否背景透明。该参数仅在 type 参数设置为 GIF 和 PNG 类型时有效。
        :param bool is_show_to_ipython: 是否在 ipython 中显示。注意，只能在 jupyter python 环境中显示，所以需要 ipython 和
                                        jupyter 环境。只支持 PNG、JPG 和 GIF 在 jupyter 中显示。
        :return: 输出成功返回 True， 否则返回 False
        :rtype: bool
        """
        image_type = ImageType._make(str(file_name).split(".")[-1])
        if not isinstance(image_type, ImageType):
            raise ValueError("invalid image type " + str(image_type))
        else:
            t_map = None
            if not output_bounds or output_bounds.is_empty():
                if dpi > 0 or isinstance(image_size, tuple):
                    t_map = Map()
                    t_map.from_xml(self.to_xml())
                    if dpi > 0:
                        t_map.set_use_system_dpi(False)
                        t_map.set_dpi(int(dpi))
                    if isinstance(image_size, tuple):
                        if len(image_size) > 1:
                            t_map.set_image_size(image_size[0], image_size[1])
                    if output_bounds:
                        t_map.set_view_bounds(Rectangle.make(output_bounds))
                    that_map = t_map
            that_map = self
        is_ok = Map._output_to_file(that_map, file_name, image_type, is_back_transparent)
        if is_ok:
            if image_type in (ImageType.JPG, ImageType.PNG, ImageType.GIF):
                if is_show_to_ipython:
                    width, height = that_map.get_image_size()
                    Map._show_to_ipython(file_name, width, height)
                if t_map:
                    t_map.close()
                return is_ok
        if t_map:
            t_map.close()
        return is_ok

    def output_tracking_layer_to_png(self, file_name, output_bounds=None, dpi=0, is_back_transparent=False, is_show_to_ipython=False):
        """
        将当前地图的跟踪图层输出为png 文件，在调用此接口前，用户可以通过 set_image_size 设置图片大小。

        :param str file_name: 结果文件路径，必须带文件后缀名。
        :param Rectangle output_bounds: 地图输出范围。如果不设置，默认使用当前地图的视图范围，具体参考 :py:meth:`.get_view_bounds`
        :param int dpi: 地图的DPI，代表每英寸有多少个像素。如果不设置，默认使用当前地图的 DPI，具体参考 :py:meth:`.get_dpi`
        :param bool is_back_transparent: 是否背景透明。
        :param bool is_show_to_ipython: 是否在 ipython 中显示。注意，只能在 jupyter python 环境中显示，所以需要 ipython 和
                                        jupyter 环境。
        :return: 输出成功返回 True， 否则返回 False
        :rtype: bool
        """
        if not output_bounds:
            output_bounds = self.get_view_bounds()
        else:
            output_bounds = Rectangle.make(output_bounds)
        is_ok = oj(self).outputTrackingLayerToPNG(file_name, is_back_transparent, dpi, oj(output_bounds))
        if is_ok:
            if is_show_to_ipython:
                width, height = self.get_image_size()
                Map._show_to_ipython(file_name, width, height)
        return is_ok

    def show_to_ipython(self):
        """
        将当前地图在 ipython 中显示，注意，只能在 jupyter python 环境中显示，所以需要 ipython 和 jupyter 环境

        :return: 显示成功返回 True，否则返回 False
        :rtype: bool
        """
        import tempfile
        temp_name = tempfile.mktemp(".png", "mapping_show_temp")
        return self.output_to_file(temp_name, is_show_to_ipython=True)

    @staticmethod
    def _show_to_ipython(file_name, width, height):
        try:
            from IPython.display import Image, display
            display(Image(filename=file_name, width=width, height=height))
        except Exception:
            import traceback
            log_error(traceback.format_exc())

    def add_dataset(self, dataset, is_add_to_head=True, layer_setting=None):
        """
        添加数据集到地图中

        :param dataset: 被添加的数据集对象
        :type dataset: Dataset or DatasetVector or DatasetImage or DatasetGrid
        :param bool is_add_to_head: 是否添加到地图的最上层
        :param layer_setting: 地图图层设置对象或专题图图层对象
        :type layer_setting: LayerSetting or Theme
        :return: 添加成功返回图层对象，否则返回 None
        :rtype: Layer
        """
        dt = get_input_dataset(dataset)
        if not isinstance(dt, (DatasetVector, DatasetImage, DatasetGrid)):
            raise ValueError("Required DatasetVector, DatasetImage, DatasetGrid")
        elif isinstance(layer_setting, LayerSetting):
            java_layer = self._jobject.getLayers().add(oj(dt), oj(layer_setting), parse_bool(is_add_to_head))
        else:
            if isinstance(layer_setting, Theme):
                java_layer = self._jobject.getLayers().add(oj(dt), oj(layer_setting), parse_bool(is_add_to_head))
            else:
                java_layer = self._jobject.getLayers().add(oj(dt), parse_bool(is_add_to_head))
        if java_layer:
            layer = Layer(java_layer)
            if isinstance(layer_setting, Theme):
                layer._set_theme(layer_setting)
            return self._add_layer(layer)

    @property
    def tracking_layer(self):
        """TrackingLayer: 返回当前地图的跟踪图层对象"""
        java_tracking_layer = self._jobject.getTrackingLayer()
        if java_tracking_layer:
            return TrackingLayer(java_tracking_layer)
        raise RuntimeError("Failed to get TrackingLayer")

    def add_to_tracking_layer(self, geos, style=None, is_antialias=False, is_symbol_scalable=False, symbol_scale=None):
        """
        添加几何对象到跟踪图层

        :param geos: 需要添加的几何对象
        :type geos: list[Geometry] or list[Feature] or list[Point2D] or list[Rectangle]
        :param GeoStyle style: 几何对象的对象风格
        :param bool is_antialias: 是否反走样
        :param bool is_symbol_scalable: 跟踪图层的符号大小是否随图缩放
        :param float symbol_scale: 此跟踪图层的符号缩放基准比例尺
        :return: 当前地图对象的跟踪图层对象
        :rtype: TrackingLayer
        """
        if not isinstance(geos, (list, tuple)):
            geos = [
             geos]
        tracking_layer = self.tracking_layer
        if isinstance(geos, (list, tuple)):
            tracking_layer.set_antialias(is_antialias)
            tracking_layer.set_symbol_scalable(is_symbol_scalable)
            tracking_layer.set_symbol_scale(symbol_scale)
            tracking_layer.start_edit_bulk()
            for geo in geos:
                if isinstance(geo, Feature):
                    geo = geo.geometry
                else:
                    if isinstance(geo, Point2D):
                        geo = GeoPoint(geo)
                    else:
                        if isinstance(geo, Rectangle):
                            geo = geo.to_region()
                if isinstance(geo, Geometry):
                    if style:
                        geo.set_style(style)
                    tracking_layer.add(geo, str(geo.id))

            tracking_layer.finish_edit_bulk()
        return tracking_layer

    def clear_layers(self):
        """
        删除此图层集合对象中所有的图层。

        :return: self
        :rtype: Map
        """
        self._jobject.getLayers().clear()
        self._dict_layer.clear()
        return self

    def is_contain_layer(self, layer_name):
        """
        判定此图层集合对象是否包含指定名称的图层。

        :param str layer_name: 可能包含在此图层集合中的图层对象的名称。
        :return: 若此图层中包含指定名称的图层则返回 true，否则返回 false。
        :rtype: bool
        """
        return self._jobject.getLayers().contains(str(layer_name))

    def find_layer(self, layer_name):
        """
        返回指定的图层名称的图层对象。

        :param str layer_name: 指定的图层名称。
        :return: 返回指定的图层名称的图层对象。
        :rtype: Layer
        """
        layer_index = self.index_of_layer(layer_name)
        if layer_index >= 0:
            return self.get_layers()[layer_index]

    def get_layers_count(self):
        """
        返回此图层集合中图层对象的总数。

        :return: 此图层集合中图层对象的总数
        :rtype: int
        """
        return self._jobject.getLayers().getCount()

    def index_of_layer(self, layer_name):
        """
        返回此图层集合中指定名称的图层的索引。

        :param str layer_name:  要查找的图层的名称。
        :return: 找到指定图层则返回图层索引，否则返回-1。
        :rtype: int
        """
        return self._jobject.getLayers().indexOf(str(layer_name))

    def get_layer(self, index_or_name):
        """
        返回此图层集合中指定名称的图层对象。

        :param index_or_name: 图层的名称或索引
        :type index_or_name: str or int
        :return: 此图层集合中指定名称的图层对象。
        :rtype: Layer
        """
        if isinstance(index_or_name, int):
            if index_or_name < 0:
                index_or_name += self.get_layers_count()
            return self.get_layers()[index_or_name]
        return self.find_layer(index_or_name)

    def remove_layer(self, index_or_name):
        """
        从此图层集合中删除一个指定名称的图层。删除成功则返回 true。

        :param index_or_name: 要删除图层的名称或索引
        :type index_or_name: str or int
        :return: 删除成功则返回 true，否则返回 false。
        :rtype: bool
        """
        if isinstance(index_or_name, int):
            self._refresh_dict_layers()
            if index_or_name < 0:
                index_or_name += self.get_layers_count()
        else:
            i = 0
            target_handle = None
            target_layer = None
            for handle, layer in self._dict_layer.items():
                if i == index_or_name:
                    target_handle = handle
                    target_layer = layer
                    break
                i += 1

            if target_handle:
                if target_layer:
                    del self._dict_layer[target_handle]
                    return self._jobject.getLayers().remove(index_or_name)
            return False
            if isinstance(index_or_name, Layer):
                return self.remove_layer(index_or_name.caption)
            target_handle = None
            target_layer = None
            self._refresh_dict_layers()
            for handle, layer in self._dict_layer.items():
                if layer.caption == index_or_name:
                    target_layer = layer
                    target_handle = handle

            if target_handle and target_layer:
                del self._dict_layer[target_handle]
                return self._jobject.getLayers().remove(index_or_name)
        return False

    def move_layer_to(self, src_index, tag_index):
        """
        将此图层集合中的指定索引的图层移动到指定的目标索引。

        :param int src_index: 要移动图层的原索引
        :param int tag_index: 图层要移动到的目标索引。
        :return: 移动成功返回 true，否则返回 false。
        :rtype: bool
        """
        if src_index < 0:
            src_index += self.get_layers_count()
        if tag_index < 0:
            tag_index += self.get_layers_count()
        if self._jobject.getLayers().moveTo(int(src_index), int(tag_index)):
            self._refresh_dict_layers()
            return True
        return False

    def add_heatmap(self, dataset, kernel_radius, max_color=None, min_color=None):
        """
        根据给定的点数据集和参数设置制作一幅热力图，也就是将给定的点数据以热力图的渲染方式进行显示。
        热力图是通过颜色分布，描述诸如人群分布、密度和变化趋势等的一种地图表现手法，因此，能够非常直观地呈现一些原本不易理解或表达的数据，比如密度、频度、温度等。
        热力图图层除了可以反映点要素的相对密度，还可以表示根据属性进行加权的点密度，以此考虑点本身的权重对于密度的贡献。

        :param dataset: 参与制作热力图的数据，该数据必须为点矢量数据集。
        :type dataset: DatasetVector
        :param int kernel_radius: 用于计算密度的查找半径。
        :param max_color: 低点密度的颜色。热力图图层将通过高点密度颜色（maxColor）和低点密度颜色（minColor）确定渐变的颜色方案。
        :type max_color: Color or tuple[int,int,int]
        :param min_color: 高点密度的颜色。热力图图层将通过高点密度颜色（maxColor）和低点密度颜色（minColor）确定渐变的颜色方案。
        :type min_color: Color or tuple[int,int,int]
        :return: 热力图图层对象
        :rtype: LayerHeatmap
        """
        dt = get_input_dataset(dataset)
        if not isinstance(dt, DatasetVector) or dt.type is not DatasetType.POINT:
            raise ValueError("Required Point Dataset")
        if min_color and max_color:
            layer = self._jobject.getLayers().AddHeatmap(oj(dt), int(kernel_radius), to_java_color(min_color), to_java_color(max_color))
        else:
            layer = self._jobject.getLayers().AddHeatmap(oj(dt), int(kernel_radius))
        if layer:
            return self._add_layer(LayerHeatmap(layer))

    def _add_layer(self, layer):
        if layer is None:
            return
        java_layer = layer._jobject
        handle = self._get_object_handle(java_layer)
        if handle == 0:
            raise ValueError("Layer is disposed (handle == 0)")
        self._dict_layer[handle] = layer
        return layer

    def add_aggregation(self, dataset, min_color=None, max_color=None):
        """
        根据给定的点数据集制作一幅默认风格的网格聚合图。

        :param dataset: 参与制作网格聚合图的数据，该数据必须为点矢量数据集。
        :type dataset: DatasetVector
        :param min_color:  网格单元统计值最小值对应的颜色，网格聚合图将通过maxColor和minColor确定渐变的颜色方案，然后基于网格单元统计值大小排序，对网格单元进行颜色渲染。
        :type min_color: Color or tuple[int,int,int]
        :param max_color: 网格单元统计值最大值对应的颜色，网格聚合图将通过maxColor和minColor确定渐变的颜色方案，然后基于网格单元统计值大小排序，对网格单元进行颜色渲染。
        :type max_color: Color or tuple[int,int,int]
        :return: 网格聚合图图层对象。
        :rtype: LayerGridAggregation
        """
        dt = get_input_dataset(dataset)
        if not isinstance(dt, DatasetVector) or dt.type is not DatasetType.POINT:
            raise ValueError("Required Point Dataset")
        if min_color and max_color:
            layer = self._jobject.getLayers().AddGridAggregation(oj(dt), to_java_color(min_color), to_java_color(max_color))
        else:
            layer = self._jobject.getLayers().AddGridAggregation(oj(dt))
        if layer:
            return self._add_layer(LayerGridAggregation(layer))

    def is_overlap_displayed(self):
        """
        返回重叠时是否显示对象。

        :return: 重叠时是否显示对象。
        :rtype: bool
        """
        return self._jobject.isOverlapDisplayed()

    def set_overlap_displayed(self, value):
        """
        设置重叠时是否显示对象。

        :param bool value: 重叠时是否显示对象
        :return: self
        :rtype: Map
        """
        self._jobject.setOverlapDisplayed(parse_bool(value))
        return self


@unique
class ThemeType(JEnum):
    __doc__ = "\n    专题图类型常量。\n\n    矢量数据和光栅数据都可以用来制作专题图，所不同的是矢量数据的专题图是基于其属性表中的属性信息，而光栅数据则是基于像元值。SuperMap 提供用于矢量\n    数据（点，线，面以及复合数据集）的专题图，包括单值专题图，范围分段专题图，点密度专题图，统计专题图，等级符号专题图，标签专题图和自定义专题图，也\n    提供了适合于光栅数据（栅格数据集）的专题图功能，包括栅格分段专题图和栅格单值专题图。\n\n    :var ThemeType.UNIQUE: 单值专题图。单值专题图中，专题变量的值相同的要素归为一类，为每一类设定一种渲染风格，如颜色或符号等，作为专题变量的字\n                           段或表达式的值相同的要素采用相同的渲染风格，从而用来区分不同的类别。\n\n    :var ThemeType.RANGE: 分段专题图。在分段专题图中，专题变量的值被分成多个范围段，在同一个范围段中要素或记录使用相同的颜色或符号风格进行显示。\n                          可使用的分段的方法有等距离分段法，平方根分段法，标准差分段法，对数分段法，等计数分段法。分段专题图所基于的专题变量必须\n                          为数值型。\n\n    :var ThemeType.GRAPH: 统计专题图。统计专题图为每个要素或记录绘制统计图来反映其对应的专题变量的值的大小。统计专题图可以基于多个变量，反映多种\n                          属性，即可以将多个变量的值绘制在一个统计图上。目前提供的统计图类型有：面积图，阶梯图，折线图，点状图，柱状图，三维柱状\n                          图，饼图，三维饼图，玫瑰图，三维玫瑰图，堆叠柱状图以及三维堆叠柱状图。\n\n                           .. image:: ../image/graphy.png\n\n    :var ThemeType.GRADUATEDSYMBOL: 等级符号专题图。等级符号专题图用符号的大小来表现要素或记录的所对应的字段或表达式（专题变量）的值的大小。\n                                    使用渐变的符号来绘制要素时，专题变量的值也被分成很多范围段，在一个范围段中的要素或记录用同样大小的符号来\n                                    绘制。等级符号专题图所基于的专题变量必须为数值型。\n\n                                     .. image:: ../image/graduatedSymbol.png\n\n    :var ThemeType.DOTDENSITY: 点密度专题图。点密度专题图使用点的个数的多少或密集程度来反映一个区域或范围所对应的专题数据的值，其中一个点代表\n                               了一定数量，则一个区域内的点的个数乘以点所表示的数量就是此区域对应的专题变量的值。点的个数越多越密集，则数据反\n                               的事物或现象在该区域的密度或浓度越大。点密度专题图所基于的专题变量必须为数值型。\n\n                                .. image:: ../image/dotDensity.png\n\n    :var ThemeType.LABEL: 标签专题图。标签专题图是用文本形式在图层上直接显示属性表中的数据，实质上是对图层的标注\n\n                           .. image:: ../image/labelM.png\n\n    :var ThemeType.CUSTOM: 自定义专题图。通过自定义专题图，用户可以对每个要素或记录设置特定的风格，并把这些设置存储到一个或多个字段中，然后基于\n                           这个或这些字段来绘制专题图。在 SuperMap 中各种符号，线型或填充等风格都有对应的 ID 值，而颜色值，符号大小，线宽等\n                           都可以用数值型的数据来设置。使用自定义专题图，用户非常自由地来表达各要素和数据。\n\n    :var ThemeType.GRIDRANGE: 栅格分段专题图。在栅格分段专题图中，栅格的所有像元值被分成多个范围段，像元值在同一个范围段中的像元使用相同的颜色\n                              进行显示。可使用的分段的方法有等距离分段法，平方根分段法，对数分段法。\n\n                               .. image:: ../image/gridRanges.png\n\n    :var ThemeType.GRIDUNIQUE: 栅格单值专题图。栅格单值专题图中，栅格中像元值相同的像元归为一类，为每一类设定一种颜色，从而用来区分不同的类别。\n                               如土地利用分类图中，土地利用类型相同的像元的值相同，将使用相同的颜色来渲染，从而区分不同的土地利用类型。\n\n                                .. image:: ../image/gridUnique.png\n\n    "
    UNIQUE = 1
    RANGE = 2
    GRAPH = 3
    GRADUATEDSYMBOL = 4
    DOTDENSITY = 5
    LABEL = 7
    CUSTOM = 8
    GRIDRANGE = 12
    GRIDUNIQUE = 11

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.mapping.ThemeType"


class Theme(JVMBase):
    __doc__ = "\n    专题图类，该类是所有专题图的基类。所有专题图类，如单值专题图，标签专题图，分段专题图等都继承自该类。\n    "

    def __init__(self):
        JVMBase.__init__(self)
        self._type = None

    @staticmethod
    def _create_instance(theme_type):
        if theme_type is ThemeType.UNIQUE:
            theme = ThemeUnique()
        else:
            if theme_type is ThemeType.GRAPH:
                theme = ThemeGraph()
            else:
                if theme_type is ThemeType.LABEL:
                    theme = ThemeLabel()
                else:
                    if theme_type is ThemeType.DOTDENSITY:
                        theme = ThemeDotDensity()
                    else:
                        if theme_type is ThemeType.GRADUATEDSYMBOL:
                            theme = ThemeGraduatedSymbol()
                        else:
                            if theme_type is ThemeType.GRIDUNIQUE:
                                theme = ThemeGridUnique()
                            else:
                                if theme_type is ThemeType.GRIDRANGE:
                                    theme = ThemeGridRange()
                                else:
                                    if theme_type is ThemeType.RANGE:
                                        theme = ThemeRange()
                                    else:
                                        if theme_type is ThemeType.CUSTOM:
                                            theme = ThemeCustom()
                                        else:
                                            theme = None
        return theme

    @staticmethod
    def _from_java_object(java_object):
        if java_object:
            theme_type = ThemeType._make(java_object.getType().name())
            theme = Theme._create_instance(theme_type)
            if theme:
                theme._java_object = java_object
            return theme

    @property
    def type(self):
        """ThemeType: 专题图的类型"""
        return self._type

    @staticmethod
    def make_from_xml(xml):
        """
        导入专题图信息，并构建一个新的专题图对象。

        :param xml: 包含专题图信息的 XML 字符串或文件路径
        :type xml: str
        :return: 专题图对象
        :rtype: Theme
        """
        if not xml:
            return
        else:
            from xml.etree import ElementTree
            import os
            if not xml.startswith("<sml:Theme>"):
                if os.path.isfile(xml):
                    all_lines = []
                    with open(xml, "r") as file_reader:
                        while True:
                            lines = file_reader.readlines()
                            if not lines:
                                break
                            all_lines.extend(lines)

                    xml = "".join(all_lines)
            if not xml:
                return
            format_xml = xml.replace("sml:", "")
            type_value = ElementTree.XML(format_xml).find("Type").text
            theme_type = ThemeType._make(int(type_value))
            theme = Theme._create_instance(theme_type)
            if theme and theme.from_xml(xml):
                return theme

    def from_xml(self, xml):
        """
        从 XML 字符串中导入专题图信息。
        在 SuperMap 中，各种专题图的风格的设置都可以导出成 XML 格式的字符串，此 XML 格式的字符串中记录了关于这种专题图的所有设置，如对于标签专
        题图的 XML 格式字符串会记录专题图类型，可见比例尺，标签风格的设置，是否流动显示，是否自动避让等等对该标签专题图的所有风格的设置以及用来制作
        标签专题图的字段或表达式。这种 XML 格式字符串可以用来导入，对专题图进行设置

        该接口需要注意的是，xml 记录的信息必须与当前对象的类型对应。例如，如果 xml 中记录的标签专题图信息，则当前对象必须为 ThemeLabel 对象。
        如果不清楚 xml 中记录的专题图类型，可以使用 :py:meth:`.Theme.make_from_xml` 从 xml 中构建一个新的专题图对象。

        :param xml: 包含专题图信息的 XML 字符串或文件路径
        :type xml: str
        :return: 导入成功返回 True， 否则返回 False。
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        import os
        if not xml.startswith("<sml:Theme>"):
            if os.path.isfile(xml):
                all_lines = []
                with open(xml, "r") as file_reader:
                    while True:
                        lines = file_reader.readlines()
                        if not lines:
                            break
                        all_lines.extend(lines)

                xml = "".join(all_lines)
        if self._jobject.fromXML(str(xml)):
            theme_type = ThemeType._make(self._jobject.getType().name())
            if theme_type is not self.type:
                raise ValueError("invalid xml for {} theme".format(self.type.name()))
            return True
        return False

    def to_xml(self):
        """
        导出专题图信息为 XML 字符串。

        :return: 专题图信息的 XML 字符串
        :rtype: str
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jobject.toXML()

    def __str__(self):
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jobject.toString()


class ThemeUniqueItem:
    __doc__ = "\n    单值专题图子项类。\n\n    单值专题图是将专题值相同的要素归为一类，为每一类设定一种渲染风格，其中每一类就是一个专题图子项。 比如，利用单值专题图制作行政区划图，Name 字\n    段代表省/直辖市名，该字段用来做专题变量，如果该字段的字段值总共有5种不同值，则该行政区划图有5个专题图子项，其中每一个子项内的要素 Name 字段值\n    都相同。\n    "

    def __init__(self, value, style, caption, visible=True):
        """

        :param str value: 单值专题图子项的单值
        :param GeoStyle style: 每个单值专题图子项的显示风格
        :param str caption: 单值专题图子项的名称
        :param bool visible: 单值专题图子项是否可见
        """
        self._value = ""
        self._caption = ""
        self._style = None
        self._visible = True
        self.set_value(value).set_style(style).set_caption(caption).set_visible(visible)

    def __str__(self):
        return "ThemeUniqueItem(value={}, caption={}, visible={})".format(self.value, self.style, self.visible)

    @property
    def value(self):
        """str: 单值专题图子项的单值"""
        return self._value

    def set_value(self, value):
        """
        设置单值专题图子项的单值

        :param str value: 单值专题图子项的单值
        :return: self
        :rtype: ThemeUniqueItem
        """
        self._value = str(value) if value else ""
        return self

    @property
    def style(self):
        """GeoStyle: 每个单值专题图子项的显示风格"""
        return self._style

    def set_style(self, value):
        """
        设置每个单值专题图子项的显示风格

        :param value: 每个单值专题图子项的显示风格
        :type value: GeoStyle
        :return: self
        :rtype: ThemeUniqueItem
        """
        if isinstance(value, GeoStyle):
            self._style = value
        return self

    @property
    def caption(self):
        """str: 每个单值专题图子项的名称"""
        return self._caption

    def set_caption(self, value):
        """
        设置每个单值专题图子项的名称

        :param str value: 每个单值专题图子项的名称
        :return: self
        :rtype: ThemeUniqueItem
        """
        self._caption = str(value) if value else None
        return self

    @property
    def visible(self):
        """bool: 单值专题图子项是否可见"""
        return self._visible

    def set_visible(self, value):
        """
        设置单值专题图子项是否可见

        :param bool value: 单值专题图子项是否可见
        :return: self
        :rtype: ThemeUniqueItem
        """
        self._visible = parse_bool(value)
        return self

    @property
    def _jobject(self):
        java_object = get_jvm().com.supermap.mapping.ThemeUniqueItem()
        java_object.setUnique(str(self.value))
        if self.style is not None:
            java_object.setStyle(oj(self.style))
        elif self.caption is not None:
            java_object.setCaption(self.caption)
        else:
            java_object.setCaption(str(self.value))
        java_object.setVisible(parse_bool(self.visible))
        return java_object

    @staticmethod
    def _from_java_object(java_object):
        if not java_object:
            return
        return ThemeUniqueItem(java_object.getUnique(), GeoStyle._from_java_object(java_object.getStyle()), java_object.getCaption(), java_object.isVisible())


class ThemeUnique(Theme):
    __doc__ = "\n    单值专题图类。\n\n    将字段或表达式的值相同的要素采用相同的风格来显示，从而用来区分不同的类别。例如，在表示土地的面数据中表示土地利用类型的字段中有草地，林地，居民地，\n    耕地等值，使用单值专题图进行渲染时，每种类型的土地利用类型被赋予一种颜色或填充风格，从而可以看出每种类型的土地利用的分布区域和范围。可用于地质图、\n    地貌图、植被图、土地利用图、政治行政区划图、自然区划图、经济区划图等。单值专题图着重表示现象质的差别，一般不表示数量的特征。尤其是有交叉或重叠现\n    象时，此类不推荐使用，例如：民族分布区等。\n\n    注意：如果通过连接（Join）或关联（Link）的方式与一个外部表建立了联系，当专题图的专题变量用到外部表的字段时，在显示专题图时，需要调\n    用 :py:meth:`.Layer.set_display_filter` 方法，否则专题图将出图失败。\n\n    以下代码演示通过数据集创建默认单值专题图::\n\n    >>> ds = open_datasource('/home/data/data.udb')\n    >>> dt = ds['zones']\n    >>> mmap = Map()\n    >>> theme = ThemeUnique.make_default(dt, 'zone', ColorGradientType.CYANGREEN)\n    >>> mmap.add_dataset(dt, True, theme)\n    >>> mmap.set_image_size(2000, 2000)\n    >>> mmap.view_entire()\n    >>> mmap.output_to_file('/home/data/mapping/unique_theme.png')\n\n    也可以通过以下方式创建单值专题图::\n\n    >>> ds = open_datasource('/home/data/data.udb')\n    >>> dt = ds['zones']\n    >>> mmap = Map()\n    >>> default_style = GeoStyle().set_fill_fore_color('yellow').set_fill_back_color('green').set_fill_gradient_mode('RADIAL')\n    >>> theme = ThemeUnique('zone', default_style)\n    >>> mmap.add_dataset(dt, True, theme)\n    >>> mmap.set_image_size(2000, 2000)\n    >>> mmap.view_entire()\n    >>> mmap.output_to_file('/home/data/mapping/unique_theme.png')\n\n    或者指定自定义项::\n\n    >>> ds = open_datasource('/home/data/data.udb')\n    >>> dt = ds['zones']\n    >>>\n    >>> theme = ThemeUnique()\n    >>> theme.set_expression('zone')\n    >>> color = [Color.gold(), Color.blueviolet(), Color.rosybrown(), Color.coral()]\n    >>> zone_values = dt.get_field_values(['zone'])['zone']\n    >>> for index, value in enumerate(zone_values):\n    >>>     theme.add(ThemeUniqueItem(value, GeoStyle().set_fill_fore_color(colors[index % 4]), str(index)))\n    >>>\n    >>> mmap.add_dataset(dt, True, theme)\n    >>> mmap.set_image_size(2000, 2000)\n    >>> mmap.view_entire()\n    >>> mmap.output_to_file('/home/data/mapping/unique_theme.png')\n\n    "

    def __init__(self, expression=None, default_style=None):
        """

        :param str expression: 单值专题图字段表达式。用于制作单值专题图的字段或字段表达式。该字段可以为要素的某一属性（如地质图中的年代或成份），
                               其值的数据类型可以为数值型或字符型。
        :param GeoStyle default_style: 单值专题图的默认风格。对于那些未在单值专题图子项之列的对象使用该风格显示。如未设置，则使用图层默认风格显示。
        """
        Theme.__init__(self)
        self._type = ThemeType.UNIQUE
        self.set_expression(expression).set_default_style(default_style)

    @staticmethod
    def make_default(dataset, expression, color_gradient_type=None, join_items=None):
        """
        根据给定的矢量数据集和单值专题图字段表达式生成默认的单值专题图。

        :param dataset: 矢量数据集
        :type dataset: DatasetVector or str
        :param str expression: 单值专题图字段表达式。
        :param color_gradient_type:  颜色渐变模式
        :type color_gradient_type: str or ColorGradientType
        :param join_items: 外部表连接项。如果要将制作的专题图添加到地图中，作为地图中的图层，需要对该专题图图层进行以下设置，通过该专题图图层对
                           应的 Layer 对象的 :py:meth:`.Layer.set_display_filter` 方法，该方法中的 parameter 参数为 :py:class:`.QueryParameter`
                           对象，这里需要通过 QueryParameter 对象的 :py:meth:`.QueryParameter.set_join_items` 方法，将专题的外部表
                           连接项（即当前方法的 join_items 参数）指定给该专题图图层对应的 Layer 对象，这样所做的专题图在地图中显示才正确。
        :type join_items: list[JoinItem] or tuple[JoinItem]
        :return: 新的单值专题图
        :rtype: ThemeUnique
        """
        dataset = get_input_dataset(dataset)
        if not isinstance(dataset, DatasetVector):
            raise ValueError("failed get dataset")
        else:
            unique_expression = expression if expression else ""
            color_gradient_type = ColorGradientType._make(color_gradient_type)
            if color_gradient_type is None:
                java_theme = get_jvm().com.supermap.mapping.ThemeUnique.makeDefault(oj(dataset), str(unique_expression))
            else:
                if isinstance(join_items, JoinItem):
                    join_items = [
                     join_items]
            if join_items:
                join_items = list(filter((lambda it: isinstance(it, JoinItem)), join_items))
            elif join_items:
                java_join_items = QueryParameter._to_java_join_items(join_items)
                java_theme = get_jvm().com.supermap.mapping.ThemeUnique.makeDefault(oj(dataset), str(unique_expression), oj(color_gradient_type), java_join_items)
            else:
                java_theme = get_jvm().com.supermap.mapping.ThemeUnique.makeDefault(oj(dataset), str(unique_expression), oj(color_gradient_type))
        return Theme._from_java_object(java_theme)

    @staticmethod
    def make_default_four_colors(dataset, color_field, colors=None):
        """
        根据指定的面数据集、颜色字段名称、颜色生成默认的四色单值专题图。 四色单值专题图是指在一幅地图上，只用四种颜色就能使具有公共边的面对象着上不
        同的颜色。

        注意：对于面数据集复杂度低的情形下，采用四种颜色即可生成四色单值专题图；若面数据集复杂度高，则着色结果可能为五色。

        :param dataset: 指定的面数据集。由于该构造函数将修改面数据集的属性信息，因此，需保证 dataset 为非只读。
        :type dataset: DatasetVector or str
        :param str color_field: 着色字段的名称。着色字段必须为整型字段。它可以为面数据集中已有属性字段，也可以是自定义的其它字段。若为已存在属
                                性字段，需保证该字段类型为整型，系统将修改该字段的属性值，并分别赋值为1、2、3、4；若为自定义的其它字段，需保证
                                字段名合法，则系统首先在面数据集中创建该字段，并分别赋值为1、2、3、4。由此，着色字段已分别赋值为1、2、3、4，
                                代表着四种不同的颜色，根据该字段的值即可生成四色专题图。
        :param Colors colors: 用户传入的用来制作专题图的颜色。系统对传入颜色的数目不做规定，比如，用户只传入了一种颜色，则在生成专题图时，系统
                              会自动补齐出图所需的颜色。
        :return: 四色单值专题图
        :rtype: ThemeUnique
        """
        dataset = get_input_dataset(dataset)
        if not isinstance(dataset, DatasetVector):
            raise ValueError("faield get dataset")
        if dataset.type is not DatasetType.REGION:
            raise ValueError("only support region dataset, but is " + str(dataset.type))
        color_field = color_field if color_field else ""
        java_theme = get_jvm().com.supermap.mapping.ThemeUnique.makeDefault(oj(dataset), color_field, oj(colors))
        return Theme._from_java_object(java_theme)

    def _make_java_object(self):
        return self._jvm.com.supermap.mapping.ThemeUnique()

    def extend(self, items):
        """
        批量添加单值专题图子项。

        :param items: 单值专题图子项列表
        :type items: list[ThemeUniqueItem] or tuple[ThemeUniqueItem]
        :return: self
        :rtype: ThemeUnique
        """
        if isinstance(items, ThemeUniqueItem):
            items = [
             items]
        if isinstance(items, (list, tuple)):
            r_items = list(items)
            r_items.reverse()
            for item in r_items:
                self.add(item)

        return self

    def add(self, item):
        """
        添加单值专题图子项。

        :param item: 单值专题图子项
        :type item: ThemeUniqueItem
        :return: self
        :rtype: ThemeUnique
        """
        if isinstance(item, ThemeUniqueItem):
            self._jobject.add(oj(item))
        return self

    def clear(self):
        """
        删除所有单值专题图子项。执行该方法后，所有的单值专题图子项都被释放，不再可用。

        :return: self
        :rtype: ThemeUnique
        """
        self._jobject.clear()
        return self

    def get_count(self):
        """

        :return:
        :rtype: int
        """
        return self._jobject.getCount()

    def __getitem__(self, index):
        return self.get_item(index)

    def get_item(self, index):
        """
        返回指定序号的单值专题图子项。

        :param int index: 指定的单值专题图子项的序号。
        :return: 单值专题图子项
        :rtype: ThemeUniqueItem
        """
        if index < 0:
            index = index + self._jobject.getCount()
        return ThemeUniqueItem._from_java_object(self._jobject.getItem(int(index)))

    def index_of(self, value):
        """
        返回单值专题图中指定子项单值在当前序列中的序号。

        :param str value: 给定的单值专题图子项单值。
        :return:
        :rtype: int
        """
        return self._jobject.indexOf(str(value) if value else "")

    def remove(self, index):
        """
        删除一个指定序号的单值专题图子项。

        :param int index: 指定的将被删除的单值专题图子项序列的序号。
        :return:
        :rtype: bool
        """
        if index < 0:
            index = index + self._jobject.getCount()
        return self._jobject.remove(int(index))

    def insert(self, index, item):
        """
        将给定的单值专题图子项插入到指定序号的位置。

        :param int index: 指定的单值专题图子项序列的序号。
        :param ThemeUniqueItem item: 将被插入的单值专题图子项。
        :return: 插入成功返回 True，否则返回 False
        :rtype: bool
        """
        if index < 0:
            index = index + self._jobject.getCount()
        if isinstance(item, ThemeUniqueItem):
            return self._jobject.insert(int(index), oj(item))
        return False

    def reverse_style(self):
        """
        对单值专题图中子项的风格进行反序显示。

        :return: self
        :rtype: ThemeUnique
        """
        self._jobject.reverseStyle()
        return self

    def set_default_style(self, style):
        """
        设置单值专题图的默认风格。对于那些未在单值专题图子项之列的对象使用该风格显示。如未设置，则使用图层默认风格显示。

        :param GeoStyle style:
        :return: self
        :rtype: ThemeUnique
        """
        if isinstance(style, GeoStyle):
            self._jobject.setDefaultStyle(oj(style))
        return self

    def get_default_style(self):
        """
        返回单值专题图的默认风格

        :return: 单值专题图的默认风格。
        :rtype: GeoStyle
        """
        return GeoStyle._from_java_object(self._jobject.getDefaultStyle())

    def is_default_style_visible(self):
        """
        单值专题图默认风格是否可见

        :return: 单值专题图默认风格是否可见。
        :rtype: bool
        """
        return self._jobject.isDefaultStyleVisible()

    def set_default_style_visible(self, value):
        """
        设置单值专题图默认风格是否可见。

        :param bool value: 单值专题图默认风格是否可见
        :return: self
        :rtype: ThemeUnique
        """
        self._jobject.setDefaultStyleVisible(parse_bool(value))
        return self

    def get_offset_x(self):
        """
        返回点、线、面图层制作的单值专题图中的对象相对于原来位置的水平偏移量。

        :return: 点、线、面图层制作的单值专题图中的对象相对于原来位置的水平偏移量。
        :rtype: str
        """
        return self._jobject.getOffsetX()

    def set_offset_x(self, value):
        """
        设置点、线、面图层制作的单值专题图中的对象相对于原来位置的水平偏移量。

        偏移量的单位由 :py:meth:`.set_offset_prj_coordinate_unit` 决定, 为True表示采用采用地理坐标单位，否则采用设备单位

        :param str value: 点、线、面图层制作的单值专题图中的对象相对于原来位置的水平偏移量。
        :return: self
        :rtype: ThemeUnique
        """
        if value is not None:
            self._jobject.setOffsetX(str(value))
        return self

    def get_offset_y(self):
        """
        返回点、线、面图层制作的单值专题图中的对象相对于原来位置的垂直偏移量。

        :return: 点、线、面图层制作的单值专题图中的对象相对于原来位置的垂直偏移量。
        :rtype: str
        """
        return self._jobject.getOffsetY()

    def set_offset_y(self, value):
        """
        设置点、线、面图层制作的单值专题图中的对象相对于原来位置的垂直偏移量。

        偏移量的单位由 :py:meth:`.set_offset_prj_coordinate_unit` 决定, 为True表示采用采用地理坐标单位，否则采用设备单位

        :param str value: 点、线、面图层制作的单值专题图中的对象相对于原来位置的垂直偏移量。
        :return: self
        :rtype: ThemeUnique
        """
        if value is not None:
            self._jobject.setOffsetY(str(value))
        return self

    def set_offset_prj_coordinate_unit(self, value):
        """
        设置水平或垂直偏移量的单位是否是地理坐标系单位。如果为 True 则是地理坐标单位，否则采用设备单位。具体查看 :py:meth:`set_offset_x` 和 :py:meth:`set_offset_y` 接口。

        :param bool value: 水平或垂直偏移量的单位是否是地理坐标系单位
        :return: self
        :rtype: ThemeUnique
        """
        self._jobject.setOffsetFixed(not parse_bool(value))
        return self

    def is_offset_prj_coordinate_unit(self):
        """
        获取水平或垂直偏移量的单位是否是地理坐标系单位

        :return: 水平或垂直偏移量的单位是否是地理坐标系单位。如果为 True 则是地理坐标单位，否则采用设备单位。
        :rtype: bool
        """
        return not self._jobject.isOffsetFixed()

    @property
    def expression(self):
        """str: 单值专题图字段表达式。用于制作单值专题图的字段或字段表达式。该字段可以为要素的某一属性（如地质图中的年代或成份），其值的数据类型可
                以为数值型或字符型。 """
        return self._jobject.getUniqueExpression()

    def set_expression(self, value):
        """
        设置单值专题图字段表达式。用于制作单值专题图的字段或字段表达式。该字段可以为要素的某一属性（如地质图中的年代或成份），其值的数据类型可以为数值型或字符型。

        :param str value: 指定单值专题图字段表达式
        :return: self
        :rtype: ThemeUnique
        """
        if value is not None:
            self._jobject.setUniqueExpression(str(value))
        return self

    def get_custom_marker_angle_expression(self):
        """
        返回一个字段表达式，该字段表达式用于控制对象对应的点单值题图中点符号的旋转角度，字段表达式中的字段必须为数值型字段。 通过该接口可以指定一个
        字段也可以指定一个字段表达式；还可以指定一个数值，此时所有专题图子项将以数值指定的角度统一进行旋转。

        :return: 字段表达式
        :rtype: str
        """
        return self._jobject.getCustomMarkerAngleExpression()

    def set_custom_marker_angle_expression(self, value):
        """
        设置一个字段表达式，该字段表达式用于控制对象对应的点单值题图中点符号的旋转角度，字段表达式中的字段必须为数值型字段。通过该接口可以指定一个字
        段也可以指定一个字段表达式；还可以指定一个数值，此时所有专题图子项将以数值指定的角度统一进行旋转。

        该项设置仅对点单值专题图有效。

        :param str value: 字段表达式
        :return: self
        :rtype: ThemeUnique
        """
        if value is not None:
            self._jobject.setCustomMarkerAngleExpression(str(value))
        return self

    def get_custom_marker_size_expression(self):
        """
        返回一个字段表达式，该字段表达式用于控制对象对应的点单值题图中点符号的大小，字段表达式中的字段必须为数值型字段。 通过该接口可以指定一个字段
        也可以指定一个字段表达式；还可以指定一个数值，此时所有专题图子项将以数值指定的大小统一显示。

        该项设置仅对点单值专题图有效。

        :return: 字段表达式
        :rtype: str
        """
        return self._jobject.getCustomMarkerSizeExpression()

    def set_custom_marker_size_expression(self, value):
        """
        设置一个字段表达式，该字段表达式用于控制对象对应的点单值题图中点符号的大小，字段表达式中的字段必须为数值型字段。 通过该接口可以指定一个字段
        也可以指定一个字段表达式；还可以指定一个数值，此时所有专题图子项将以数值指定的大小统一显示。

        该项设置仅对点单值专题图有效。

        :param str value: 字段表达式
        :return: self
        :rtype: ThemeUnique
        """
        if value is not None:
            self._jobject.setCustomMarkerSizeExpression(str(value))
        return self


class ThemeRangeItem:
    __doc__ = "\n    分段专题图子项类。\n    在分段专题图中，将分段字段的表达式的值按照某种分段模式被分成多个范围段。每个分段都有其分段起始值、终止值、名称和风格等。每个分段所表示的范围为 [Start, End)。\n    "

    def __init__(self, start, end, caption, style=None, visible=True):
        """
        :param float start: 分段专题图子项的起始值。
        :param float end: 分段专题图子项的终止值。
        :param str caption: 分段专题图子项的名称。
        :param GeoStyle style: 分段专题图子项的显示风格。
        :param bool visible: 分段专题图中的子项是否可见。
        """
        self._start = None
        self._end = None
        self._caption = ""
        self._style = None
        self._visible = True
        self.set_start(start).set_end(end).set_style(style).set_caption(caption).set_visible(visible)

    def __str__(self):
        return "ThemeRangeItem(start={}, end={}, caption={}, visible={})".format(self.start, self.end, self.caption, self.visible)

    @property
    def start(self):
        """float: 分段专题图子项的起始值"""
        return self._start

    def set_start(self, value):
        """
        设置分段专题图子项的起始值。

        如果该子项是分段中第一个子项，那么该起始值就是分段的最小值；如果子项的序号大于等于 1 的时候，该起始值必须与前一子项的终止值相同，否则系统会抛出异常。

        :param float value: 分段专题图子项的起始值
        :return: self
        :rtype: ThemeRangeItem
        """
        if value is not None:
            self._start = float(value)
        return self

    @property
    def end(self):
        """float: 分段专题图子项的终止值"""
        return self._end

    def set_end(self, value):
        """
        设置分段专题图子项的终止值。

        :param float value: 分段专题图子项的终止值
        :return: self
        :rtype: ThemeRangeItem
        """
        if value is not None:
            self._end = float(value)
        return self

    @property
    def style(self):
        """GeoStyle: 返回分段专题图中每一个分段专题图子项的对应的风格。 """
        return self._style

    def set_style(self, value):
        """
        设置分段专题图中每一个分段专题图子项的对应的风格。

        :param GeoStyle value: 分段专题图中每一个分段专题图子项的对应的风格。
        :return: self
        :rtype: ThemeRangeItem
        """
        if isinstance(value, GeoStyle):
            self._style = value
        return self

    @property
    def caption(self):
        """str: 分段专题图中子项的名称。"""
        return self._caption

    def set_caption(self, value):
        """
        设置分段专题图中子项的名称。

        :param str value: 分段专题图中子项的名称。
        :return: self
        :rtype: ThemeRangeItem
        """
        self._caption = str(value) if value else None
        return self

    @property
    def visible(self):
        """bool: 返回分段专题图中的子项是否可见。 """
        return self._visible

    def set_visible(self, value):
        """
        设置分段专题图中的子项是否可见。

        :param bool value:  指定分段专题图中的子项是否可见。
        :return: self
        :rtype: ThemeRangeItem
        """
        self._visible = parse_bool(value)
        return self

    @property
    def _jobject(self):
        java_object = get_jvm().com.supermap.mapping.ThemeRangeItem()
        if self.start is not None:
            java_object.setStart(float(self.start))
        if self.end is not None:
            java_object.setEnd(float(self.end))
        if self.style is not None:
            java_object.setStyle(oj(self.style))
        if self.caption is not None:
            java_object.setCaption(self.caption)
        java_object.setVisible(parse_bool(self.visible))
        return java_object

    @staticmethod
    def _from_java_object(java_object):
        if not java_object:
            return
        return ThemeRangeItem(java_object.getStart(), java_object.getEnd(), GeoStyle._from_java_object(java_object.getStyle()), java_object.getCaption(), java_object.isVisible())


@unique
class RangeMode(JEnum):
    __doc__ = "\n\n    该类定义了分段专题图的分段方式类型常量。\n\n    在分段专题图中，作为专题变量的字段或表达式的值按照某种分段方式被分成多个范围段，要素或记录根据其所对应的字段值或表达式值被分配到其中一个分段中，\n    在同一个范围段中要素或记录使用相同的风格进行显示。分段专题图一般用来表现连续分布现象的数量或程度特征，如降水量的分布，土壤侵蚀强度的分布等，\n    从而反映现象在各区域的集中程度或发展水平的分布差异。\n\n    SuperMap 组件产品提供多种分类的方法，包括等距离分段法，平方根分段法，标准差分段法，对数分段法，等计数分段法，以及自定义距离法，显然这些分段方法\n    根据一定的距离进行分段，因而分段专题图所基于的专题变量必须为数值型。\n\n    :var RangeMode.EUQALINTERVAL: 等距离分段。等距离分段是根据作为专题变量的字段或表达式的最大值和最小值，按照用户设定的分段数进行相等间距的分\n                                  段。在等距离分段中，每一段具有相等的长度。求算等距分段的距离间隔公式为:\n\n                                  .. image:: ../image/EqualInterval_d_s.png\n\n                                  其中，d 为分段的距离间隔，Vmax 为专题变量的最大值，Vmin 为专题变量的最小值，count 为用户指定的分段数。则每一分段的分段点的求算公式为：\n\n                                  .. image:: ../image/EqualInterval_v_s.png\n\n                                  其中，Vi 为分段点的值，i 为从0到 count-1 的正整数，表示各分段，当 i 等于0时，Vi 为 Vmin；当 i 等于 count-1 时，Vi 为 Vmax。\n\n                                  例如你选择一个字段作为专题变量，其值是从1到10，你需要用等距离分段法将其分为4段，则分别为1-2.5，2.5-5，5-7.5和7.5-10。注意，\n                                  分段中使用 “” 和 “”，所以分段点的值划归到下一段。\n\n                                  注意：按照这种分段方式，很有可能某个分段中没有数值，即落到该段中的记录或要素为0个。\n\n    :var RangeMode.SQUAREROOT: 平方根分段。平方根分段方法实质上是对原数据的平方根的等距离分段，其首先取所有数据的平方根进行等距离分段，得到处理\n                               后数据的分段点，然后将这些分段点的值进行平方作为原数据的分段点，从而得到原数据的分段方案。所以，按照这种分段方式，\n                               也很有可能某个分段中没有数值，即落到该段中的记录或要素为0个。该方法适用于一些特定数据，如最小值与最大值之间相差\n                               比较大时，用等距离分段法可能需要分成很多的段才能区分，用平方根分段方法可以压缩数据间的差异，用较少的分段数却比较\n                               准确地进行分段。专题变量的平方根的分段间隔距离计算公式为:\n\n                               .. image:: ../image/SquareRoot_d_s.png\n\n                               其中，d 为分段的距离间隔，Vmax 为专题变量的最大值，Vmin 为专题变量的最小值，count 为用户指定的分段数。则专题变量的分段的段点的求算公式为:\n\n                               .. image:: ../image/SquareRoot_v_s.png\n\n                               其中，Vi 为分段点的值，i 为从0到 count-1 的正整数，表示各分段，当 i 等于0时，Vi 为 Vmin。\n                               注意：数据中有负数则不适合这种方法。\n\n    :var RangeMode.STDDEVIATION: 标准差分段。标准差分段方法反映了各要素的某属性值对其平均值的偏离。该方法首先计算出专题变量的平均值和标准偏差，\n                                 在此基础上进行分段。标准差分段的每个分段长度都是一个标准差，最中间的那一段以平均值为中心，左边分段点和右边分段\n                                 点分别与平均值相差0.5个标准差。设专题变量值的平均值为 mean，标准偏差为 std，则分段效果如图所示：\n\n                                 .. image:: ../image/rangemode_little.png\n\n                                 例如对专题变量为1-100之间的值，且专题变量的平均值为50，标准偏差为20，则分段为40-60，20-40，60-80，0-20，80-100共5段。\n                                 落在不同分段范围内的要素分别被设置为不同的显示风格。\n\n                                 注意：标准差的段数由计算结果决定，用户不可控制。\n\n    :var RangeMode.LOGARITHM: 对数分段。对数分段方法的实现的原理与平方根分段方法基本相同，所不同的是平方根方法是对原数据取平方根，而对数分段方\n                              法是对原数据取对数，即对原数据的以10为底的对数值的等距离分段，其首先对原数据所有值的对数进行等距离分段，得到处\n                              理后数据的分段点，然后以10为底，这些分段点的值作为指数的幂得到原数据的各分段点的值，从而得到分段方案。适用于最大\n                              值与最小值相差很大，用等距离分段不是很理想的情况，对数分段法比平方根分段法具有更高的压缩率，使数据间的差异尺度更\n                              小，优化分段结果。专题变量的对数的等距离分段的距离间隔的求算公式为：\n\n                              .. image:: ../image/Logarithm_d_s.png\n\n                              其中，d 为分段的距离间隔，Vmax 为专题变量的最大值，Vmin 为专题变量的最小值，count 为用户指定的分段数。从而专题变量的分段点的求算公式为：\n\n                              .. image:: ../image/Logarithm_v_s.png\n\n                              其中，Vi 为分段点的值，i 为从0到 count-1 的正整数，表示各分段，当 i 等于0时，Vi 为 Vmin；当 i 等于 count-1 时，Vi 为 Vmax。\n                              注意：数据中有负数则不适合这种方法。\n\n    :var RangeMode.QUANTILE: 等计数分段。在等计数分段中，尽量保证每一段内的对象个数尽可能的相等。这个相等的个数是多少是由用户指定的分段数以及实\n                             际的要素个数来决定的，在可以均分的情况下，每段中对象数目应该是一样的，但是当每段对象数据均分时，分段结果的最后几段\n                             会多一个对象。 比如，有9个对象，分9段的话，每段一个对象；分8段的话，前7段是1个对象，第8段是2个对象；分7段的话，\n                             前5段是1个对象，第6段和第7段是2个对象。这种分段方法适合于线性分布的数据。等计数分段的每段中的要素个数的求算公式为:\n\n                             .. image:: ../image/Quantile_n_s.png\n\n                             其中，n 为每段中的要素个数，N 为要进行分段的要素的总个数，count 为用户指定的分段数。当 n 的计算结果不是整数时，采用取整方式。\n\n    :var RangeMode.CUSTOMINTERVAL: 自定义分段。在自定义分段中，由用户指定各段的长度，即间隔距离来进行分段，分段数由 SuperMap 根据指定的间隔\n                                   距离以及专题变量的最大和最小值来计算。各分段点的求算公式为：\n\n                                   .. image:: ../image/custominterval_s.png\n\n                                   其中，Vi 为各分段点的值，Vmin 为专题变量的最小值，d 为用户指定的距离，count 为计算出来的分段数，i 为从0到\n                                   count-1 的正整数，表示各分段，当 i 等于0时，Vi 为 Vmin；当 i 等于 count-1 时，Vi 为 Vmax。\n    :var RangeMode.NONE: 空分段模式\n    "
    EUQALINTERVAL = 0
    SQUAREROOT = 1
    STDDEVIATION = 2
    LOGARITHM = 3
    QUANTILE = 4
    CUSTOMINTERVAL = 5
    NONE = 6

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.mapping.RangeMode"

    @classmethod
    def _externals(cls):
        return {'square':RangeMode.SQUAREROOT,  'log':RangeMode.LOGARITHM, 
         'std':RangeMode.STDDEVIATION}


class ThemeRange(Theme):
    __doc__ = "\n    分段专题图类。\n    按照提供的分段方法对字段的属性值进行分段，并根据每个属性值所在的分段范围赋予相应对象的显示风格。\n\n    注意：\n    制作分段专题图，如果首尾区间没有设置风格，且没有设置默认风格，那么无论是添加到首部还是尾部，首尾区间默认采用用户所添加的第一个分段的风格，比如：\n    总共分5段，:py:meth:`.add` 方法依次添加 [0，1）、[1，2）、[2，4）三段，那么首区间(负无穷，0)，尾区间[4，正无穷),采用[0,1)的风格。\n\n    以下代码演示通过数据集创建默认分段专题图::\n\n    >>> ds = open_datasource('/home/data/data.udb')\n    >>> dt = ds['zones']\n    >>> mmap = Map()\n    >>> theme = ThemeRange.make_default(dt, 'SmID', RangeMode.EUQALINTERVAL, 6, ColorGradientType.RAINBOW)\n    >>> mmap.add_dataset(dt, True, theme)\n    >>> mmap.set_image_size(2000, 2000)\n    >>> mmap.view_entire()\n    >>> mmap.output_to_file('/home/data/mapping/range_theme.png')\n\n    也可以通过以下方式创建单值专题图::\n\n    >>> ds = open_datasource('/home/data/data.udb')\n    >>> dt = ds['zones']\n    >>>\n    >>> theme = ThemeRange('SmID')\n    >>> theme.add(ThemeRangeItem(1, 20, GeoStyle().set_fill_fore_color('gold'), '1'), is_add_to_head=True)\n    >>> theme.add(ThemeRangeItem(20, 50, GeoStyle().set_fill_fore_color('rosybrown'), '2'), is_add_to_head=False)\n    >>> theme.add(ThemeRangeItem(50, 90, GeoStyle().set_fill_fore_color('coral'), '3'), is_add_to_head=False)\n    >>> theme.add(ThemeRangeItem(90, 160, GeoStyle().set_fill_fore_color('crimson'), '4'), is_add_to_head=False)\n    >>> mmap.add_dataset(dt, True, theme)\n    >>> mmap.set_image_size(2000, 2000)\n    >>> mmap.view_entire()\n    >>> mmap.output_to_file('/home/data/mapping/range_theme.png')\n\n    "

    def __init__(self, expression=None, items=None):
        """
        :param str expression: 分段字段表达式。
        :param items: 分段专题图子项列表
        :type items: list[ThemeRangeItem] or tuple[ThemeRangeItem]
        """
        Theme.__init__(self)
        self._type = ThemeType.RANGE
        self.set_expression(expression).extend(items)

    def _make_java_object(self):
        return self._jvm.com.supermap.mapping.ThemeRange()

    @staticmethod
    def make_default(dataset, expression, range_mode, range_parameter, color_gradient_type=None, range_precision=0.1, join_items=None):
        """
        根据给定的矢量数据集、分段字段表达式、分段模式、相应的分段参数、颜色渐变填充模式、外部连接表项和舍入精度，生成默认的分段专题图。

        注意：通过连接外部表的方式制作专题图时，对于 UDB 数据源，连接类型不支持内连接，即不支持 :py:attr:`.JoinType.INNERJOIN` 连接类型。

        :param dataset: 矢量数据集。
        :type dataset: DatasetVector or str
        :param str expression: 分段字段表达式
        :param range_mode: 分段模式
        :type range_mode: str or RangeMode
        :param float range_parameter: 分段参数。当分段模式为等距离分段法，平方根分段，对数分段法，等计数分段法其中一种时，该参数为分段个数；
                                      当分段模式为标准差分段法的时候，该参数不起作用；当分段模式为自定义距离时，该参数表示自定义距离。
        :param color_gradient_type: 颜色渐变模式
        :type color_gradient_type: ColorGradientType or str
        :param float range_precision: 分段值的精度。如，计算得到的分段值为13.02145，而分段精度为0.001，则分段值取13.021
        :param join_items: 外部表连接项。如果要将制作的专题图添加到地图中，作为地图中的图层，需要对该专题图图层进行以下设置，通过该专题图图层对
                           应的 Layer 对象的 :py:meth:`.Layer.set_display_filter` 方法，该方法中的 parameter 参数为 :py:class:`.QueryParameter`
                           对象，这里需要通过 QueryParameter 对象的 :py:meth:`.QueryParameter.set_join_items` 方法，将专题的外部表
                           连接项（即当前方法的 join_items 参数）指定给该专题图图层对应的 Layer 对象，这样所做的专题图在地图中显示才正确。
        :type join_items: list[JoinItem] or tuple[JoinItem]
        :return: 结果分段专题图对象
        :rtype: ThemeRange
        """
        dataset = get_input_dataset(dataset)
        expression = expression if expression else ""
        range_mode = RangeMode._make(range_mode, "EUQALINTERVAL")
        color_gradient_type = ColorGradientType._make(color_gradient_type)
        if range_mode is RangeMode.STDDEVIATION:
            range_parameter = 0.0
        if isinstance(join_items, JoinItem):
            join_items = [
             join_items]
        if join_items:
            join_items = list(filter((lambda it: isinstance(it, JoinItem)), join_items))
        if join_items and len(join_items) > 0:
            java_join_items = QueryParameter._to_java_join_items(join_items)
        else:
            java_join_items = None
        java_color_gradient_type = oj(color_gradient_type)
        java_theme = get_jvm().com.supermap.mapping.ThemeRange.makeDefault(oj(dataset), str(expression), oj(range_mode), float(range_parameter), java_color_gradient_type, java_join_items, float(range_precision))
        return Theme._from_java_object(java_theme)

    def extend(self, items):
        """
        批量添加分段专题图子项

        :param items: 分段专题图子项列表
        :type items: list[ThemeRangeItem] or tuple[ThemeRangeItem]
        :return: self
        :rtype: ThemeRange
        """
        if isinstance(items, ThemeRangeItem):
            items = [
             items]
        if isinstance(items, (list, tuple)):
            r_items = list(items)
            r_items.reverse()
            for item in r_items:
                self.add(item)

        return self

    def add(self, item, is_normalize=True, is_add_to_head=False):
        """
        添加分段专题图子项

        :param item: 分段专题图子项
        :type item: ThemeRangeItem
        :param bool is_normalize:  表示是否规整化，is_normalize 为 True 时， item 值不合法，则进行规整，is_normalize 为 Fasle 时， item 值不合法则抛异常。
        :param bool is_add_to_head: 是否添加到分段列表的开头。如果为 False，则添加到分段列表的尾部。
        :return: self
        :rtype: ThemeRange
        """
        if isinstance(item, ThemeRangeItem):
            if is_add_to_head:
                return self._jobject.addToHead(oj(item), parse_bool(is_normalize))
            return self._jobject.addToTail(oj(item), parse_bool(is_normalize))
        return False

    def clear(self):
        """
        删除分段专题图的所有分段子项。执行该方法后，所有的分段专题图子项都被释放，不再可用。

        :return: self
        :rtype: ThemeRange
        """
        self._jobject.clear()
        return self

    def get_count(self):
        """
        返回分段专题图中分段的个数

        :return: 分段专题图中分段的个数
        :rtype: int
        """
        return self._jobject.getCount()

    def __getitem__(self, index):
        return self.get_item(index)

    def get_item(self, index):
        """
        返回指定序号的分段专题图中分段专题图子项

        :param int index: 指定的分段专题图序号
        :return: 分段专题图中分段专题图子项
        :rtype: ThemeRangeItem
        """
        if index < 0:
            index = index + self._jobject.getCount()
        return ThemeRangeItem._from_java_object(self._jobject.getItem(int(index)))

    def index_of(self, value):
        """
        返回分段专题图中指定分段字段值在当前分段序列中的序号。

        :param str value: 给定的分段字段值。
        :return: 分段字段值在分段序列中的序号。如果该值不存在，就返回 -1。
        :rtype: int
        """
        return self._jobject.indexOf(str(value) if value else "")

    def reverse_style(self):
        """
        对分段专题图中分段的风格进行反序显示。比如，专题图有三个分段，分别为 item1，item2，item3，调用反序显示后，item3 的风格与 item1 会调换，item2 的显示风格不变。

        :return: self
        :rtype: ThemeRange
        """
        self._jobject.reverseStyle()
        return self

    def get_precision(self):
        """
        获取范围分段专题图的舍入精度。

        :return: 舍入精度
        :rtype: float
        """
        return self._jobject.getPrecision()

    def set_precision(self, value):
        """
        设置范围分段专题图的舍入精度。

        如，计算得到的分段值为13.02145，而分段精度为0.001，则分段值取13.021。

        :param float value: 舍入精度
        :return: self
        :rtype: ThemeRange
        """
        if value is not None:
            self._jobject.setPrecision(float(value))
        return self

    @property
    def expression(self):
        """str: 分段字段表达式"""
        return self._jobject.getRangeExpression()

    def set_expression(self, value):
        """
        设置分段字段表达式。
        通过对比某要素分段字段表达式的值与（按照一定的分段模式确定的）各分段范围的分段值，来确定该要素所在的范围段，从而对落在不同分段内的要素设置为不同的风格。

        :param str value: 指定分段字段表达式。
        :return: self
        :rtype: ThemeRange
        """
        self._jobject.setRangeExpression(str(value) if value else "")
        return self

    @property
    def range_mode(self):
        """RangeMode: 分段模式"""
        java_mode = self._jobject.getRangeMode()
        if java_mode:
            return RangeMode._make(java_mode)

    def get_custom_interval(self):
        """
        获取自定义段长

        :return: 自定位段长
        :rtype: float
        """
        return self._jobject.getCustomInterval()

    def get_offset_x(self):
        """
        获取水平方向偏移量

        :return: 水平方向偏移量
        :rtype: str
        """
        return self._jobject.getOffsetX()

    def set_offset_x(self, value):
        """
        设置水平方向偏移量。

        偏移量的单位由 :py:meth:`.set_offset_prj_coordinate_unit` 决定, 为True表示采用采用地理坐标单位，否则采用设备单位

        :param str value: 水平方向偏移量。
        :return: self
        :rtype: ThemeRange
        """
        if value is not None:
            self._jobject.setOffsetX(str(value))
        return self

    def get_offset_y(self):
        """
        获取垂直方向偏移量

        :return: 垂直方向偏移量
        :rtype: str
        """
        return self._jobject.getOffsetY()

    def set_offset_y(self, value):
        """
        设置垂直方向偏移量。

        偏移量的单位由 :py:meth:`.set_offset_prj_coordinate_unit` 决定, 为True表示采用采用地理坐标单位，否则采用设备单位

        :param str value:
        :return: self
        :rtype: ThemeRange
        """
        if value is not None:
            self._jobject.setOffsetY(str(value))
        return self

    def set_offset_prj_coordinate_unit(self, value):
        """
        设置水平或垂直偏移量的单位是否是地理坐标系单位。如果为 True 则是地理坐标单位，否则采用设备单位。具体查看 :py:meth:`set_offset_x` 和 :py:meth:`set_offset_y` 接口。

        :param bool value: 水平或垂直偏移量的单位是否是地理坐标系单位
        :return: self
        :rtype: ThemeRange
        """
        self._jobject.setOffsetFixed(not parse_bool(value))
        return self

    def is_offset_prj_coordinate_unit(self):
        """
        获取水平或垂直偏移量的单位是否是地理坐标系单位

        :return: 水平或垂直偏移量的单位是否是地理坐标系单位。如果为 True 则是地理坐标单位，否则采用设备单位。
        :rtype: bool
        """
        return not self._jobject.isOffsetFixed()


class MixedTextStyle:
    __doc__ = "\n    文本复合风格类。\n\n    该类主要用于对标签专题图中标签的文本内容进行风格设置。通过该类用户可以使标签的文字显示不同的风格，比如文本 “喜马拉雅山”，通过本类可以将前三个字用红色显示，后两个字用蓝色显示。\n\n    对同一文本设置不同的风格实质上是对文本的字符进行分段，同一分段内的字符具有相同的显示风格。对字符分段有两种方式，一种是利用分隔符对文本进行分段；另一种是根据分段索引值进行分段。\n\n     * 利用分隔符对文本进行分段 比如用“&”作分隔符，它将文本“5&109”分为“5”和“109”两部分，在显示时，“5”和分隔符“&”使用同一个风格，字符串“109”使用相同的风格。\n\n     * 利用分段索引值进行分段 文本中字符的索引值是以0开始的整数，比如文本“珠穆朗玛峰”，第一个字符（“珠”）的索引值为0，第二个字符（“穆”）的索引值为1，\n       以此类推；当设置分段索引值为1，3，4，9时，字符分段范围相应的就是(-∞，1)，[1，3)，[3，4)，[4，9)，[9，+∞)，可以看出索引号为0的字符（即“珠” ）\n       在第一个分段内，索引号为1，2的字符（即“穆”、“朗”）位于第二个分段内，索引号为3的字符（“玛”）在第三个分段内，索引号为4的字符（“峰”）在第四个分段内，其余分段中没有字符。\n\n    "

    def __init__(self, default_style=None, styles=None, separator=None, split_indexes=None):
        """
        :param TextStyle default_style: 缺省时的风格
        :param styles: 文本样式集合。文本样式集合中的样式用于不同分段内的字符
        :type styles: list[TextStyle] or tuple[TextStyle]
        :param str separator: 文本的分隔符，分隔符的风格采用默认风格，并且分隔符只能设置一个字符
        :param split_indexes: 分段索引值，分段索引值用来对文本中的字符进行分段
        :type split_indexes: list[int] or tuple[int]
        """
        self._styles = None
        self._separator = None
        self._is_separator_enabled = False
        self._split_indexes = None
        self._default_style = None
        self.set_styles(styles).set_default_style(default_style).set_separator(separator).set_split_indexes(split_indexes)

    def set_styles(self, value):
        """
        设置文本样式集合。文本样式集合中的样式用于不同分段内的字符。

        :param value: 文本样式集合
        :type value: list[TextStyle] or tuple[TextStyle]
        :return: self
        :rtype: MixedTextStyle
        """
        if isinstance(value, TextStyle):
            value = [
             value]
        if isinstance(value, (list, tuple)):
            self._styles = list(filter((lambda it: isinstance(it, TextStyle)), value))
        return self

    @property
    def styles(self):
        """list[TextStyle]: 文本样式集合"""
        return self._styles

    def set_default_style(self, value):
        """
        设置缺省时的风格

        :param TextStyle value: 缺省时的风格
        :return: self
        :rtype: MixedTextStyle
        """
        if isinstance(value, TextStyle):
            self._default_style = value
        return self

    @property
    def default_style(self):
        """TextStyle: 缺省时的风格"""
        return self._default_style

    @property
    def is_separator_enabled(self):
        """bool: 文本的分隔符是否有效"""
        return self._is_separator_enabled

    def set_separator_enabled(self, value):
        """
        设置文本的分隔符是否有效。
        分隔符有效时利用分隔符对文本进行分段；无效时根据文本中字符的位置进行分段。分段后，同一分段内的字符具有相同的显示风格。

        :param bool value: 文本的分隔符是否有效
        :return: self
        :rtype: MixedTextStyle
        """
        self._is_separator_enabled = parse_bool(value)
        return self

    def get_separator(self):
        """
        获取文本的分隔符

        :return: 文本的分隔符。
        :rtype: str
        """
        return self._separator

    def set_separator(self, value):
        """
        设置文本的分隔符，分隔符的风格采用默认风格，并且分隔符只能设置一个字符。

        文本的分隔符是一个将文本分割开的符号，比如用“_”作分隔符，它将文本“5_109”分为“5”和“109”两部分，假设有风格数组：style1、style2和默认文
        本风格DefaultStyle。在显示时，“5”使用Style1风格显示，分隔符“_”使用默认风格（DefaultStyle），字符“1”，“0”，“9”使用Style2的风格。

        :param str value:  指定文本的分隔符
        :return: self
        :rtype: MixedTextStyle
        """
        if value is not None:
            self._separator = str(value)
        return self

    def get_split_indexes(self):
        """
        返回分段索引值，分段索引值用来对文本中的字符进行分段

        :return: 返回分段索引值
        :rtype: list[int]
        """
        return self._split_indexes

    def set_split_indexes(self, value):
        """
        设置分段索引值，分段索引值用来对文本中的字符进行分段。

        文本中字符的索引值是以 0 开始的整数，比如文本“珠穆朗玛峰”，第一个字符（“珠”）的索引值为0，第二个字符（“穆”）的索引值为1，以此类推；当设置
        分段索引值为1，3，4，9时，字符分段范围相应的就是(-∞，1)，[1，3)，[3，4)，[4，9)，[9，+∞)，可以看出索引号为0的字符（即“珠” ）在第一个
        分段内，索引号为1，2的字符（即“穆”、“朗”）位于第二个分段内，索引号为3的字符（“玛”）在第三个分段内，索引号为4的字符（“峰”）在第四个分段内，
        其余分段中没有字符。

        :param value: 指定分段索引值
        :type value: list[int] or tuple[int]
        :return: self
        :rtype: MixedTextStyle
        """
        self._split_indexes = split_input_int_list_from_str(value)
        return self

    @property
    def _jobject(self):
        java_object = get_jvm().com.supermap.mapping.MixedTextStyle()
        if self.default_style is not None:
            java_object.setDefaultStyle(oj(self.default_style))
        if self.styles is not None:
            java_styles = to_java_array(self.styles, get_jvm().com.supermap.data.TextStyle)
            if java_styles is not None:
                java_object.setStyles(java_styles)
        java_object.setSeparatorEnabled(parse_bool(self.is_separator_enabled))
        if self.get_separator() is not None:
            java_object.setSeparator(str(self.get_separator()))
        if self.get_split_indexes() is not None:
            java_object.setSplitIndexes(to_java_int_array(self.get_split_indexes()))
        return java_object

    @staticmethod
    def _from_java_object(java_object):
        if not java_object:
            return
        styles = list(map((lambda it: TextStyle._from_java_object(it)), java_object.getStyles()))
        default_style = TextStyle._from_java_object(java_object.getDefaultStyle())
        return MixedTextStyle(default_style, styles, java_object.getSeparator(), java_array_to_list(java_object.getSplitIndexes())).set_separator_enabled(java_object.isSeparatorEnabled())


class LabelMatrix:
    __doc__ = "\n    矩阵标签类。\n\n    通过该类可以制作出复杂的标签来标注对象。该类可以包含 n*n 个矩阵标签元素，矩阵标签元素的类型可以是图片，符号，标签专题图等。目前支持的矩阵标签元\n    素类型为 :py:class:`LabelMatrixImageCell` ， :py:class:`LabelMatrixSymbolCell` ， :py:class:`ThemeLabel` ，传入其他类型将\n    会抛出异常。 不支持矩阵标签元素中包含矩阵标签，矩阵标签元素不支持含有特殊符号的表达式，不支持沿线标注。\n\n    以下代码示范了如何通过 LabelMatrix 类制作复杂的标签来标注对象::\n\n    >>> label_matrix = LabelMatrix(2,2)\n    >>> label_matrix.set(0, 0, LabelMatrixImageCell('path', 5, 5, is_size_fixed=False))\n    >>> label_matrix.set(1, 0, ThemeLabel().set_label_expression('Country'))\n    >>> label_matrix.set(0, 1, LabelMatrixSymbolCell('Symbol', GeoStyle.point_style(0, 0, (6,6), 'red')))\n    >>> label_matrix.set(1, 1, ThemeLabel().set_label_expression('Capital'))\n    >>> theme_label = ThemeLabel()\n    >>> theme_label.set_matrix_label(label_matrix)\n\n    "

    def __init__(self, cols, rows):
        """
        :param int cols: 列数
        :param int rows: 行数
        """
        self._cols = int(cols)
        self._rows = int(rows)
        self._cells = list((None for i in range(cols * rows)))

    @property
    def cols(self):
        """int: 列数"""
        return self._cols

    @property
    def rows(self):
        """int: 行数"""
        return self._rows

    def set(self, col, row, value):
        """
        设置指定行列位置处所对应的对象。

        :param int col: 指定的列数。
        :param int row: 指定的行数
        :param value: 指定行列位置处所对应的对象
        :type value: LabelMatrixImageCell or LabelMatrixSymbolCell or ThemeLabel
        :return: self
        :rtype: LabelMatrix
        """
        if col < 0 or col > self.cols:
            raise ValueError("invalid col, required 0<=col<" + str(self.cols))
        elif row < 0 or row > self.rows:
            raise ValueError("invalid row, required 0<=row<" + str(self.rows))
        assert isinstance(value, (LabelMatrixImageCell, LabelMatrixSymbolCell, ThemeLabel)), "required LabelMatrixImageCell, LabelMatrixSymbolCell, ThemeLabel, but " + str(type(value))
        self._cells[row * self._cols + col] = value
        return self

    def get(self, col, row):
        """
        设置指定行列位置处所对应的对象。

        :param int col: 指定的列数
        :param int row: 指定的行数
        :return: 指定行列位置处所对应的对象
        :rtype: LabelMatrixImageCell or LabelMatrixSymbolCell or ThemeLabel
        """
        if col < 0 or col > self.cols:
            raise ValueError("invalid col, required 0<=col<" + str(self.cols))
        if row < 0 or row > self.rows:
            raise ValueError("invalid row, required 0<=row<" + str(self.rows))
        return self._cells[row * self._cols + col]

    @property
    def _jobject(self):
        java_object = get_jvm().com.supermap.mapping.LabelMatrix(int(self.cols), int(self.rows))
        for col in range(self.cols):
            for row in range(self.rows):
                java_object.set(int(col), int(row), oj(self.get_cell(col, row)))

        return java_object

    @staticmethod
    def _from_java_object(java_object):
        if not java_object:
            return
        cell_types = {'LabelMatrixImageCell':LabelMatrixImageCell, 
         'LabelMatrixSymbolCell':LabelMatrixSymbolCell, 
         'ThemeLabel':ThemeLabel}
        label_matrix = LabelMatrix(java_object.getColumnCount(), java_object.getRowCount())
        for col in range(label_matrix.cols):
            for row in range(label_matrix.rows):
                java_cell = java_object.get(col, row)
                if java_cell:
                    class_name = str(java_cell.getClass().getName()).split(".")[-1]
                    if class_name in cell_types.keys():
                        cell = cell_types[class_name]._from_java_object(java_cell)
                    else:
                        cell = None
                    label_matrix.set_cell(col, row, cell)

        return label_matrix


class LabelMatrixImageCell:
    __doc__ = "\n    图片类型的矩阵标签元素类。\n\n    该类型的对象可作为矩阵标签对象中的一个矩阵标签元素\n\n    具体参考 :py:class:`LabelMatrix` .\n    "

    def __init__(self, path_field, width=1.0, height=1.0, rotation=0.0, is_size_fixed=False):
        """

        :param str path_field: 记录了图片类型的矩阵标签元素所使用图片的路径的字段名称。
        :param float width: 图片的宽度，单位为毫米
        :param float height: 图片的高度，单位为毫米。
        :param float rotation: 图片的旋转角度。
        :param bool is_size_fixed: 图片的大小是否固定
        """
        self._path_field = None
        self._width = 1.0
        self._height = 1.0
        self._rotation = 0.0
        self._is_size_fixed = False
        self.set_path_field(path_field).set_width(width).set_height(height).set_rotation(rotation).set_size_fixed(is_size_fixed)

    @property
    def path_field(self):
        """str: """
        return self._path_field

    def set_path_field(self, value):
        """

        :param str value:
        :return: self
        :rtype: LabelMatrixImageCell
        """
        if value is not None:
            self._path_field = str(value)
        return self

    @property
    def width(self):
        """float: 返回图片的宽度，单位为毫米"""
        return self._width

    def set_width(self, value):
        """
        设置图片的宽度，单位为毫米

        :param float value: 图片的宽度，单位为毫米
        :return: self
        :rtype: LabelMatrixImageCell
        """
        if value is not None:
            self._width = float(value)
        return self

    @property
    def height(self):
        """float: 返回图片的高度，单位为毫米"""
        return self._height

    def set_height(self, value):
        """
        设置图片的高度，单位为毫米

        :param float value: 图片的高度
        :return: self
        :rtype: LabelMatrixImageCell
        """
        if value is not None:
            self._height = float(value)
        return self

    @property
    def rotation(self):
        """float: 图片的旋转角度"""
        return self._rotation

    def set_rotation(self, value):
        """
        设置图片的旋转角度。

        :param float value: 图片的旋转角度。
        :return: self
        :rtype: LabelMatrixImageCell
        """
        if value is not None:
            self._rotation = float(value)
        return self

    @property
    def is_size_fixed(self):
        """bool: 图片的大小是否固定"""
        return self._is_size_fixed

    def set_size_fixed(self, value):
        """
        设置图片的大小是否固定

        :param bool value: 图片的大小是否固定
        :return: self
        :rtype: LabelMatrixImageCell
        """
        self._is_size_fixed = parse_bool(value)
        return self

    @property
    def _jobject(self):
        java_object = get_jvm().com.supermap.mapping.LabelMatrixImageCell()
        java_object.setHeight(float(self.height))
        java_object.setWidth(float(self.width))
        if self.path_field:
            java_object.setPathField(str(self.path_field))
        java_object.setRotation(float(self.rotation))
        java_object.setSizeFixed(parse_bool(self.is_size_fixed))
        return java_object

    @staticmethod
    def _from_java_object(java_object):
        if not java_object:
            return
        return LabelMatrixImageCell(java_object.getPathField(), java_object.getWidth(), java_object.getHeight(), java_object.getRotation(), java_object.isSizeFixed())


class LabelMatrixSymbolCell:
    __doc__ = "\n    符号类型的矩阵标签元素类。\n\n    该类型的对象可作为矩阵标签对象中的一个矩阵标签元素。\n\n    具体参考 :py:class:`LabelMatrix` .\n    "

    def __init__(self, symbol_id_field, style=None):
        """

        :param str symbol_id_field: 记录所使用符号 ID 的字段名称。
        :param GeoStyle style: 所使用符号的样式
        """
        self._symbol_id_field = None
        self._style = None
        self.set_symbol_id_field(symbol_id_field).set_style(style)

    @property
    def symbol_id_field(self):
        """str: 返回记录所使用符号 ID 的字段名称。"""
        return self._symbol_id_field

    def set_symbol_id_field(self, value):
        """
        设置记录所使用符号 ID 的字段名称。

        :param str value: 记录所使用符号 ID 的字段名称。
        :return: self
        :rtype: LabelMatrixSymbolCell
        """
        if value is not None:
            self._symbol_id_field = str(value)
        return self

    @property
    def style(self):
        """GeoStyle: 返回所使用符号的样式"""
        return self._style

    def set_style(self, value):
        """
        设置所使用符号的样式

        :param GeoStyle value: 所使用符号的样式
        :return: self
        :rtype: LabelMatrixSymbolCell
        """
        if isinstance(value, GeoStyle):
            self._style = value
        return self

    @property
    def _jobject(self):
        java_object = get_jvm().com.supermap.mapping.LabelMatrixSymbolCell()
        if self.symbol_id_field is not None:
            java_object.setSymbolIDField(str(self.symbol_id_field))
        if self.style is not None:
            java_object.setStyle(oj(self.style))
        return java_object

    @staticmethod
    def _from_java_object(java_object):
        if not java_object:
            return
        return LabelMatrixSymbolCell(java_object.getSymbolIDField(), GeoStyle._from_java_object(java_object.getStyle()))


@unique
class LabelBackShape(JEnum):
    __doc__ = "\n    该类定义了标签专题图中标签背景的形状类型常量。\n\n    标签背景是 SuperMap iObjects 支持的一种标签的显示风格，是使用一定颜色的各种形状作为各标签背景，从而可以突出显示标签或者使标签专题图更美观。\n\n    :var LabelBackShape.NONE: 空背景, 不使用任何的形状作为标签的背景。\n    :var LabelBackShape.RECT: 矩形背景。标签背景的形状为矩形\n    :var LabelBackShape.ROUNDRECT: 圆角矩形背景。标签背景的形状为圆角矩形\n    :var LabelBackShape.ELLIPSE: 椭圆形背景。标签背景的形状为椭圆形\n    :var LabelBackShape.DIAMOND: 菱形背景。标签背景的形状为菱形\n    :var LabelBackShape.TRIANGLE: 三角形背景。标签背景的形状为三角形\n    :var LabelBackShape.MARKER: 符号背景。标签背景的形状为设定的符号，该符号可以分别通过 :py:meth:`.ThemeLabel.set_back_style` 的方法来设置。\n    "
    NONE = 0
    RECT = 1
    ROUNDRECT = 2
    ELLIPSE = 3
    DIAMOND = 4
    TRIANGLE = 5
    MARKER = 6

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.mapping.LabelBackShape"


@unique
class AvoidMode(JEnum):
    __doc__ = "\n    该枚举定义了标签专题图中标签文本的避让方式类型常量。\n\n    :var AvoidMode.TWO: 两方向文本避让。\n    :var AvoidMode.FOUR: 四方向文本避让\n    :var AvoidMode.EIGHT: 八方向文本避让。\n    :var AvoidMode.FREE: 环绕文本避让。\n    "
    TWO = 1
    FOUR = 2
    EIGHT = 3
    FREE = 4

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.mapping.AvoidMode"


@unique
class AlongLineCulture(JEnum):
    __doc__ = "\n    该类定义了沿线标注文字显示习惯的类型常量。\n\n    :var AlongLineCulture.ENGLISH: 以英文习惯显示，文字的走向总是与线的方向垂直。\n    :var AlongLineCulture.CHINESE: 以中文习惯显示，在线与水平方向的角度属于[]时，文字方向与线的方向平行，否则垂直。\n    "
    ENGLISH = 0
    CHINESE = 1

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.mapping.AlongLineCulture"


@unique
class AlongLineDirection(JEnum):
    __doc__ = "\n    该类定义了标签沿线标注方向类型常量。\n    路线与水平方向的锐角夹角在 60 度以上表示上下方向，60 度以下表示左右方向\n\n    :var AlongLineDirection.ALONG_LINE_NORMAL: 沿线的法线方向放置标签。\n    :var AlongLineDirection.LEFT_TOP_TO_RIGHT_BOTTOM: 从上到下，从左到右放置。\n    :var AlongLineDirection.RIGHT_TOP_TO_LEFT_BOTTOM: 从上到下，从右到左放置。\n    :var AlongLineDirection.LEFT_BOTTOM_TO_RIGHT_TOP: 从下到上，从左到右放置。\n    :var AlongLineDirection.RIGHT_BOTTOM_TO_LEFT_TOP: 从下到上，从右到左放置。\n    "
    ALONG_LINE_NORMAL = 0
    LEFT_TOP_TO_RIGHT_BOTTOM = 1
    RIGHT_TOP_TO_LEFT_BOTTOM = 2
    LEFT_BOTTOM_TO_RIGHT_TOP = 3
    RIGHT_BOTTOM_TO_LEFT_TOP = 4

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.mapping.AlongLineDirection"


@unique
class AlongLineDrawingMode(JEnum):
    __doc__ = "\n    该类定义了标签沿线标注绘制策略类型常量。\n\n    SuperMap GIS 8C(2017)版本开始，调整了沿线标注的绘制策略，为了兼容以前版本，提供了一个“兼容绘制”选项。\n\n    在新的绘制策略中，用户可根据实际应用需求，选择标签绘制的方式是将标签作为一个整体绘制还是将标签中的文字和字母拆分开绘制。一般情况下沿线标注中，采用\n    拆分绘制，标签与被标注的线走势相吻合；如果为整行绘制，那么标签将作为一个整体，此设置一般用于带背景标签的沿线标注。\n\n    .. image:: ../image/Labelchaifen.png\n\n    :var AlongLineDrawingMode.COMPATIBLE: 兼容绘制\n    :var AlongLineDrawingMode.WHOLEWORD: 整行绘制\n    :var AlongLineDrawingMode.EACHWORD: 拆分绘制\n    "
    COMPATIBLE = 0
    WHOLEWORD = 1
    EACHWORD = 2

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.mapping.AlongLineDrawingMode"


@unique
class OverLengthLabelMode(JEnum):
    __doc__ = "\n    该类定义了标签专题图中超长标签的处理模式类型常量。\n\n    对于标签的长度超过设置的标签最大长度的标签称为超长标签， 标签的最大长度可以通过 :py:meth:`.ThemeLabel.set_overlength_label` 方法来返回\n    和设置。 SuperMap 组件产品提供三种超长标签的处理方式来控制超长标签的显示行为。\n\n\n    :var OverLengthLabelMode.NONE: 对超长标签不进行处理。\n    :var OverLengthLabelMode.OMIT: 省略超出部分。此模式将超长标签中超出指定的标签最大长度（MaxLabelLength）的部分用省略号表示。\n    :var OverLengthLabelMode.NEWLINE: 换行显示。此模式将超长标签中超出指定的标签最大长度的部分换行显示，即用多行来显示超长标签。\n    "
    NONE = 0
    OMIT = 1
    NEWLINE = 2

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.mapping.OverLengthLabelMode"


class ThemeLabelRangeItem:
    __doc__ = "\n    分段标签专题图子项。\n\n    分段标签专题图是指对对象标签基于指定字段表达式的值进行分段，同一段内的对象标签相同的风格显示，不同段的标签使用不同风格显示。其中，一个分段对应一个\n    分段标签专题图子项。\n    "

    def __init__(self, start, end, caption, style, visible=True, offset_x=0.0, offset_y=0.0):
        """
        :param float start: 子项对应分段的起始值。
        :param float end: 子项对应分段的终止值。
        :param str caption: 子项的名称。
        :param TextStyle style: 子项的文本风格。
        :param bool visible: 分段标签专题图子项是否可见
        :param float offset_x: 子项中的标签在 X 方向偏移量。
        :param float offset_y: 子项中的标签在 Y 方向偏移量。
        """
        self._start = None
        self._end = None
        self._caption = ""
        self._style = None
        self._visible = True
        self._offset_x = 0.0
        self._offset_y = 0.0
        self.set_start(start).set_end(end).set_style(style).set_caption(caption).set_visible(visible).set_offset_x(offset_x).set_offset_y(offset_y)

    @property
    def start(self):
        """float: 子项对应分段的起始值。"""
        return self._start

    def set_start(self, value):
        """
        设置子项对应分段的起始值。

        :param float value: 子项对应分段的起始值。
        :return: self
        :rtype: ThemeLabelRangeItem
        """
        if value is not None:
            self._start = float(value)
        return self

    @property
    def end(self):
        """float: 子项对应分段的终止值。"""
        return self._end

    def set_end(self, value):
        """
        设置子项对应分段的终止值。

        :param float value:
        :return: self
        :rtype: ThemeLabelRangeItem
        """
        if value is not None:
            self._end = float(value)
        return self

    @property
    def style(self):
        """TextStyle: 子项的文本风格"""
        return self._style

    def set_style(self, value):
        """
        设置子项的文本风格

        :param TextStyle value: 子项的文本风格
        :return: self
        :rtype: ThemeLabelRangeItem
        """
        if isinstance(value, TextStyle):
            self._style = value
        return self

    @property
    def caption(self):
        """str: 子项的名称。"""
        return self._caption

    def set_caption(self, value):
        """
        设置子项的名称。

        :param str value: 子项的名称。
        :return: self
        :rtype: ThemeLabelRangeItem
        """
        self._caption = str(value) if value else None
        return self

    @property
    def visible(self):
        """bool: 分段标签专题图子项是否可见"""
        return self._visible

    def set_visible(self, value):
        """
        设置分段标签专题图子项是否可见

        :param bool value: 分段标签专题图子项是否可见
        :return: self
        :rtype: ThemeLabelRangeItem
        """
        self._visible = parse_bool(value)
        return self

    @property
    def offset_x(self):
        """float: 子项中的标签在X方向偏移量。"""
        return self._offset_x

    def set_offset_x(self, value):
        """
        设置子项中的标签在X方向偏移量

        :param float value: 子项中的标签在X方向偏移量
        :return: self
        :rtype: ThemeLabelRangeItem
        """
        if value is not None:
            self._offset_x = float(value)
        return self

    @property
    def offset_y(self):
        """float: 子项中的标签在Y方向偏移量。"""
        return self._offset_y

    def set_offset_y(self, value):
        """
        设置子项中的标签在Y方向偏移量。

        :param float value: 子项中的标签在Y方向偏移量。
        :return: self
        :rtype: ThemeLabelRangeItem
        """
        if value is not None:
            self._offset_y = float(value)
        return self

    @property
    def _jobject(self):
        java_object = get_jvm().com.supermap.mapping.ThemeLabelRangeItem()
        if self.start is not None:
            java_object.setStart(float(self.start))
        if self.end is not None:
            java_object.setEnd(float(self.end))
        if self.style is not None:
            java_object.setStyle(oj(self.style))
        if self.caption is not None:
            java_object.setCaption(self.caption)
        java_object.setVisible(parse_bool(self.visible))
        if self.offset_x is not None:
            java_object.setOffsetX(float(self.offset_x))
        if self.offset_y is not None:
            java_object.setOffsetY(float(self.offset_y))
        return java_object

    @staticmethod
    def _from_java_object(java_object):
        if not java_object:
            return
        return ThemeLabelRangeItem(java_object.getStart(), java_object.getEnd(), TextStyle._from_java_object(java_object.getStyle()), java_object.getCaption(), java_object.isVisible(), java_object.getOffsetX(), java_object.getOffsetY())


class ThemeLabelRangeItems(JVMBase):
    __doc__ = "\n    分段标签专题图子项集合。\n\n    分段标签专题图是指对对象标签基于指定字段表达式的值进行分段，同一段内的对象标签相同的风格显示，不同段的标签使用不同风格显示。其中，一个分段对应\n    一个分段标签专题图子项。\n    "

    def __init__(self, java_object):
        JVMBase.__init__(self)
        self._java_object = java_object

    def extend(self, items, is_normalize=True):
        """
        批量添加分段标签专题图子项。默认按顺序添加到子项列表的末尾。

        :param items: 分段标签专题图子项列表
        :type items: list[ThemeLabelRangeItem] or tuple[ThemeLabelRangeItem]
        :param bool is_normalize: 是否对不合法的子项进行修正，True进行修正，False 不进行修正并抛异常提示改子项为不合法值。
        :return: self
        :rtype: ThemeLabelRangeItems
        """
        if isinstance(items, ThemeLabelRangeItem):
            items = [
             items]
        if isinstance(items, (list, tuple)):
            r_items = list(items)
            r_items.reverse()
            for item in r_items:
                self.add(item, is_normalize)

        return self

    def add(self, item, is_normalize=True, is_add_to_head=False):
        """
        添加分段标签专题图子项

        :param ThemeLabelRangeItem item: 分段标签专题图子项
        :param bool is_normalize: 是否对不合法的子项进行修正，True进行修正，False 不进行修正并抛异常提示改子项为不合法值。
        :param bool is_add_to_head: 是否添加到列表的头部，为 True 时添加到列表的头部，为 False 时添加到尾部。
        :return: self
        :rtype: ThemeLabelRangeItems
        """
        if isinstance(item, ThemeLabelRangeItem):
            if is_add_to_head:
                return self._jobject.addToHead(oj(item), parse_bool(is_normalize))
            return self._jobject.addToTail(oj(item), parse_bool(is_normalize))
        return False

    def clear(self):
        """
        删除分段标签专题图的子项。 执行该方法后，所有的标签专题图子项都被释放，不再可用。

        :return: self
        :rtype: ThemeLabelRangeItems
        """
        self._jobject.clear()
        return self

    def get_count(self):
        """
        返回分段标签专题图子项集合中的子项个数。

        :return: 分段标签专题图子项集合中的子项个数
        :rtype: int
        """
        return self._jobject.getCount()

    def __getitem__(self, index):
        return self.get_item(index)

    def get_item(self, index):
        """
        返回指定序号的分段标签专题图子项集合中的子项。

        :param int index: 指定的分段标签专题图子项的序号。
        :return: 指定序号的分段标签专题图子项集合中的子项。
        :rtype: ThemeLabelRangeItem
        """
        if index < 0:
            index = index + self._jobject.getCount()
        return ThemeLabelRangeItem(self._jobject.getItem(int(index)))

    def index_of(self, value):
        """
        返回标签专题图中指定分段字段值在当前分段序列中的序号。

        :param str value: 给定的分段字段值。
        :return: 分段字段值在分段序列中的序号。如果该值不存在，就返回-1。
        :rtype: int
        """
        return self._jobject.indexOf(str(value) if value else "")

    def reverse_style(self):
        """
        对分段标签专题图中分段的风格进行反序显示。

        :return: self
        :rtype: ThemeLabelRangeItems
        """
        self._jobject.reverseStyle()
        return self


class ThemeLabelUniqueItem:
    __doc__ = "\n    单值标签专题图子项。\n\n    单值标签专题图是指对对象标签基于指定字段表达式的值进行分类，值相同的对象标签为一类使用相同的风格显示，不同类的标签使用不同风格显示；其中，一个单\n    值对应一个单值标签专题图子项。\n    "

    def __init__(self, unique_value, caption, style, visible=True, offset_x=0.0, offset_y=0.0):
        """

        :param str unique_value: 单值。
        :param str caption: 单值标签专题图子项的名称。
        :param TextStyle style:  单值对应的文本风格
        :param bool visible: 单值标签专题图子项是否可见
        :param float offset_x: 子项中的标签在X方向偏移量
        :param float offset_y: 子项中的标签在Y方向偏移量
        """
        self._unique_value = ""
        self._caption = ""
        self._style = None
        self._visible = True
        self._offset_x = 0.0
        self._offset_y = 0.0
        self.set_unique_value(unique_value).set_style(style).set_caption(caption).set_visible(visible).set_offset_x(offset_x).set_offset_y(offset_y)

    @property
    def unique_value(self):
        """str: 返回单值标签专题图子项对应的单值。 """
        return self._unique_value

    def set_unique_value(self, value):
        """
        设置单值标签专题图子项对应的单值。

        :param str value: 单值标签专题图子项对应的单值。
        :return: self
        :rtype: ThemeLabelUniqueItem
        """
        self._unique_value = str(value) if value else ""
        return self

    @property
    def style(self):
        """TextStyle: """
        return self._style

    def set_style(self, value):
        """

        :param TextStyle value:
        :return: self
        :rtype: ThemeLabelUniqueItem
        """
        if isinstance(value, TextStyle):
            self._style = value
        return self

    @property
    def caption(self):
        """str: 单值标签专题图子项的名称"""
        return self._caption

    def set_caption(self, value):
        """
        设置单值标签专题图子项的名称

        :param str value:
        :return: self
        :rtype: ThemeLabelUniqueItem
        """
        self._caption = str(value) if value else None
        return self

    @property
    def visible(self):
        """bool: 返回单值标签专题图子项是否可见。"""
        return self._visible

    def set_visible(self, value):
        """
        设置单值标签专题图子项是否可见。True 表示可见，False表示不可见。

        :param bool value: 单值标签专题图子项是否可见
        :return: self
        :rtype: ThemeLabelUniqueItem
        """
        self._visible = parse_bool(value)
        return self

    @property
    def offset_x(self):
        """float: 子项中的标签在X方向偏移量"""
        return self._offset_x

    def set_offset_x(self, value):
        """
        设置子项中的标签在X方向偏移量。

        :param float value: 子项中的标签在X方向偏移量
        :return: self
        :rtype: ThemeLabelUniqueItem
        """
        if value is not None:
            self._offset_x = float(value)
        return self

    @property
    def offset_y(self):
        """float: 子项中的标签在Y方向偏移量"""
        return self._offset_y

    def set_offset_y(self, value):
        """
        设置子项中的标签在Y方向偏移量。

        :param float value:  子项中的标签在Y方向偏移量
        :return: self
        :rtype: ThemeLabelUniqueItem
        """
        if value is not None:
            self._offset_y = float(value)
        return self

    @property
    def _jobject(self):
        java_object = get_jvm().com.supermap.mapping.ThemeLabelUniqueItem()
        java_object.setUnique(str(self.unique_value))
        if self.style is not None:
            java_object.setStyle(oj(self.style))
        if self.caption is not None:
            java_object.setCaption(self.caption)
        java_object.setVisible(parse_bool(self.visible))
        if self.offset_x is not None:
            java_object.setOffsetX(float(self.offset_x))
        if self.offset_y is not None:
            java_object.setOffsetY(float(self.offset_y))
        return java_object

    @staticmethod
    def _from_java_object(java_object):
        if not java_object:
            return
        return ThemeLabelUniqueItem(java_object.getUnique(), TextStyle._from_java_object(java_object.getStyle()), java_object.getCaption(), java_object.isVisible(), java_object.getOffsetX(), java_object.getOffsetY())


class ThemeLabelUniqueItems(JVMBase):
    __doc__ = "\n    单值标签专题图子项集合。\n\n    单值标签专题图是指对对象标签基于指定字段表达式的值进行分类，值相同的对象标签为一类使用相同的风格显示，不同类的标签使用不同风格显示；其中，一个单\n    值对应一个单值标签专题图子项。\n\n    "

    def __init__(self, java_object):
        JVMBase.__init__(self)
        self._java_object = java_object

    def extend(self, items):
        """
        批量添加单值标签专题图子项

        :param items: 单值标签专题图子项集合
        :type items: list[ThemeLabelUniqueItem] or tuple[ThemeLabelUniqueItem]
        :return: self
        :rtype: ThemeLabelUniqueItems
        """
        if isinstance(items, ThemeLabelUniqueItem):
            items = [
             items]
        if isinstance(items, (list, tuple)):
            r_items = list(items)
            r_items.reverse()
            for item in r_items:
                self.add(item)

        return self

    def add(self, item):
        """
        向单值标签专题图子项集合中添加一个子项。

        :param ThemeLabelUniqueItem item: 要添加到集合中的单值标签专题图子项
        :return: self
        :rtype: ThemeLabelUniqueItems
        """
        if isinstance(item, ThemeLabelUniqueItem):
            self._jobject.add(oj(item))
        return self

    def clear(self):
        """
        删除单值标签专题图子项集合中的子项。 执行该方法后，所有的单值标签专题图子项都被释放，不再可用。

        :return: self
        :rtype: ThemeLabelUniqueItems
        """
        self._jobject.clear()
        return self

    def get_count(self):
        """
        返回单值标签专题图子项集合中的子项个数。

        :return: 单值标签专题图子项集合中的子项个数
        :rtype: int
        """
        return self._jobject.getCount()

    def __getitem__(self, index):
        return self.get_item(index)

    def get_item(self, index):
        """
        返回指定序号的单值标签专题图子项集合中的子项

        :param int index: 指定序号
        :return: 单值标签专题图子项
        :rtype: ThemeLabelUniqueItem
        """
        if index < 0:
            index = index + self._jobject.getCount()
        return ThemeLabelUniqueItem._from_java_object(self._jobject.getItem(int(index)))

    def remove(self, index):
        """
        移除集合中指定序号位置处的单值标签专题图子项。

        :param int index: 要移除的单值标签专题图子项的序号
        :return: 移除成功返回 True，否则返回 False
        :rtype: bool
        """
        if index < 0:
            index = index + self._jobject.getCount()
        return self._jobject.remove(int(index))

    def insert(self, index, item):
        """
        向单值标签专题图子项集合中插入一个子项。

        :param int index:  指定子项插入的序号位置。
        :param ThemeLabelUniqueItem item: 指定的要添加到集合中的单值标签专题图子项。
        :return: 插入成功返回 True，否则返回 False。
        :rtype: bool
        """
        if index < 0:
            index = index + self._jobject.getCount()
        if isinstance(item, ThemeLabelUniqueItem):
            return self._jobject.insert(int(index), oj(item))
        return False

    def reverse_style(self):
        """
        对单值标签专题图中单值风格进行反序显示。

        :return: self
        :rtype: ThemeLabelUniqueItems
        """
        self._jobject.reverseStyle()
        return self

    def set_default_style(self, style):
        """
        设置单值标签专题图默认子项的文本风格，该默认风格用于未指定对应单值的子项。

        :param GeoStyle style: 单值标签专题图默认子项的文本风格
        :return: self
        :rtype: ThemeLabelUniqueItems
        """
        if isinstance(style, GeoStyle):
            self._jobject.setDefaultStyle(oj(style))
        return self

    def get_default_style(self):
        """
        返回单值标签专题图默认子项的文本风格

        :return: 单值标签专题图默认子项的文本风格
        :rtype: GeoStyle
        """
        return GeoStyle._from_java_object(self._jobject.getDefaultStyle())

    def get_default_offset_x(self):
        """
        返回单值标签专题图默认子项中标签在X方向上的偏移量

        :return: 单值标签专题图默认子项中标签在X方向上的偏移量
        :rtype: float
        """
        return self._jobject.getDefaultOffsetX()

    def set_default_offset_x(self, value):
        """
        设置单值标签专题图默认子项中标签在X方向上的偏移量

        :param float value: 单值标签专题图默认子项中标签在X方向上的偏移量
        :return: self
        :rtype: ThemeLabelUniqueItems
        """
        if value is not None:
            self._jobject.setDefaultOffsetX(float(value))
        return self

    def get_default_offset_y(self):
        """
        返回单值标签专题图默认子项中标签在Y方向上的偏移量

        :return: 单值标签专题图默认子项中标签在Y方向上的偏移量
        :rtype: float
        """
        return self._jobject.getDefaultOffsetY()

    def set_default_offset_y(self, value):
        """
        设置单值标签专题图默认子项中标签在Y方向上的偏移量

        :param float value: 单值标签专题图默认子项中标签在Y方向上的偏移量
        :return: self
        :rtype: ThemeLabelUniqueItems
        """
        if value is not None:
            self._jobject.setDefaultOffsetX(float(value))
        return self


class ThemeLabel(Theme):
    __doc__ = '\n    标签专题图类。\n\n    标签专题图的标注可以是数字、字母与文字，例如：河流、湖泊、海洋、山脉、城镇、村庄等地理名称，高程、等值线数值、河流流速、公路段里程、航海线里程等。\n\n    在标签专题图中，你可以对标签的显示风格和位置进行设置或控制，你可以为所有的标签都设置统一的显示风格和位置选项来显示；也可以通过单值标签专题图，基于\n    指定字段表达式的值进行分类，值相同的对象标签为一类使用相同的风格显示，不同类的标签使用不同风格显示；还可以通过分段标签专题图，基于指定字段表达式的\n    值进行分段，同一段内的对象标签相同的风格显示，不同段的标签使用不同风格显示。\n\n    标签专题图有多种类型：统一标签专题图、单值标签专题图、复合风格标签专题图、分段标签专题图以及自定义标签专题图，通过ThemeLabel类可以实现以上所有\n    风格标签专题图的设置，建议用户不要同时设置两种或两种以上的风格，如果同时设置了多种风格，标签专题图的显示将按照下表的优先级情况进行风格显示：\n\n    .. image:: ../image/themelabelmore.png\n\n    注意：地图上一般还会出现图例说明，图名，比例尺等等，那些都是制图元素，不属于标签专题图标注的范畴\n\n    注意：如果通过连接（Join）或关联（Link）的方式与一个外部表建立了联系，当专题图的专题变量用到外部表的字段时，在显示专题图时，需要调\n    用 :py:meth:`.Layer.set_display_filter` 方法，否则专题图将出图失败。\n\n    构建统一风格标签专题图::\n\n    >>> text_style = TextStyle().set_fore_color(Color.rosybrown()).set_font_name(\'微软雅黑\')\n    >>> theme = ThemeLabel().set_label_expression(\'zone\').set_uniform_style(text_style)\n\n    构建默认单值标签专题图::\n\n    >>> theme = ThemeLabel.make_default_unique(dataset, \'zone\', \'color_field\', ColorGradientType.CYANGREEN)\n\n    构建默认分段标签专题图::\n\n    >>> theme = ThemeLabel.make_default_range(dataset, \'zone\', \'color_field\', RangeMode.EUQALINTERVAL, 6)\n\n    构建复合风格标签专题图::\n\n    >>> mixed_style = MixedTextStyle()\n    >>> mixed_style.set_default_style(TextStyle().set_fore_color(\'rosybrown\'))\n    >>> mined_style.set_separator_enabled(True).set_separator("_")\n    >>> theme = ThemeLabel().set_label_expression(\'zone\').set_uniform_mixed_style(mixed_style)\n    '

    def __init__(self):
        Theme.__init__(self)
        self._type = ThemeType.LABEL

    def _make_java_object(self):
        return self._jvm.com.supermap.mapping.ThemeLabel()

    @property
    def label_expression(self):
        """str: 标注字段表达式"""
        return self._jobject.getLabelExpression()

    def set_label_expression(self, value):
        """
        设置标注字段表达式

        :param str value: 标注字段表达式
        :return: self
        :rtype: ThemeLabel
        """
        if value is not None:
            self._jobject.setLabelExpression(str(value))
        return self

    def get_uniform_style(self):
        """
        返回统一文本风格

        :return: 统一文本风格
        :rtype: TextStyle
        """
        return TextStyle._from_java_object(self._jobject.getUniformStyle())

    def set_uniform_style(self, value):
        """
        设置统一文本风格

        :param TextStyle value: 统一文本风格
        :return: self
        :rtype: ThemeLabel
        """
        if isinstance(value, TextStyle):
            self._jobject.setUniformStyle(oj(value))
        return self

    def get_uniform_mixed_style(self):
        """
        返回标签专题图统一的文本复合风格

        :return: 标签专题图统一的文本复合风格
        :rtype: MixedTextStyle
        """
        return MixedTextStyle._from_java_object(self._jobject.getUniformMixedStyle())

    def set_uniform_mixed_style(self, value):
        """
        设置标签专题图统一的文本复合风格。
        当同时设置了文本复合风格（ :py:meth:`.get_uniform_mixed_style` ）和文本风格 （ :py:meth:`.get_uniform_style` ）时，
        绘制风格优先级，文本复合风格大于文本风格。

        :param MixedTextStyle value: 标签专题图的文本复合风格
        :return: self
        :rtype: ThemeLabel
        """
        if isinstance(value, MixedTextStyle):
            self._jobject.setUniformMixedStyle(oj(value))
        return self

    def get_back_shape(self):
        """
        返回标签专题图中的标签背景的形状类型

        :return: 标签专题图中的标签背景的形状类型
        :rtype: LabelBackShape
        """
        java_back_shape = self._jobject.getBackShape()
        if java_back_shape:
            return LabelBackShape._make(java_back_shape.name())

    def set_back_shape(self, value):
        """
        设置标签专题图中的标签背景的形状类型，默认不显示任何背景

        :param value: 标签专题图中的标签背景的形状类型
        :type value: LabelBackShape or str
        :return: self
        :rtype: ThemeLabel
        """
        value = LabelBackShape._make(value, "NONE")
        if value is not None:
            self._jobject.setBackShape(oj(value))
        return self

    def get_back_style(self):
        """
        设置标签专题图中的标签背景风格。

        :return: 标签背景风格
        :rtype: GeoStyle
        """
        return GeoStyle._from_java_object(self._jobject.getBackStyle())

    def set_back_style(self, value):
        """
        返回标签专题图中的标签背景风格。

        :param GeoStyle value: 标签专题图中的标签背景风格。
        :return: self
        :rtype: ThemeLabel
        """
        if isinstance(value, GeoStyle):
            self._jobject.setBackStyle(oj(value))
        return self

    def get_offset_x(self):
        """
        返回标签专题图中标记文本相对于要素内点的水平偏移量

        :return: 标签专题图中标记文本相对于要素内点的水平偏移量。
        :rtype: str
        """
        return self._jobject.getOffsetX()

    def set_offset_x(self, value):
        """
        设置标签专题图中标记文本相对于要素内点的水平偏移量。
        该偏移量的值为一个常量值或者字段表达式所表示的值，即如果字段表达式为 SmID，其中 SmID=2，那么偏移量的值为 2。

        偏移量的单位由 :py:meth:`.set_offset_prj_coordinate_unit` 决定, 为True表示采用采用地理坐标单位，否则采用设备单位

        :param str value:
        :return: self
        :rtype: ThemeLabel
        """
        if value is not None:
            self._jobject.setOffsetX(str(value))
        return self

    def get_offset_y(self):
        """
        返回标签专题图中标记文本相对于要素内点的垂直偏移量

        :return: 标签专题图中标记文本相对于要素内点的垂直偏移量
        :rtype: str
        """
        return self._jobject.getOffsetY()

    def set_offset_y(self, value):
        """
        设置标签专题图中标记文本相对于要素内点的垂直偏移量。

        该偏移量的值为一个常量值或者字段表达式所表示的值，即如果字段表达式为 SmID，其中 SmID=2，那么偏移量的值为 2。

        :param str value: 标签专题图中标记文本相对于要素内点的垂直偏移量。
        :return: self
        :rtype: ThemeLabel
        """
        if value is not None:
            self._jobject.setOffsetY(str(value))
        return self

    def is_offset_prj_coordinate_unit(self):
        """
        获取水平或垂直偏移量的单位是否是地理坐标系单位

        :return: 水平或垂直偏移量的单位是否是地理坐标系单位。如果为 True 则是地理坐标单位，否则采用设备单位。
        """
        return not self._jobject.isOffsetFixed()

    def set_offset_prj_coordinate_unit(self, value):
        """
        设置水平或垂直偏移量的单位是否是地理坐标系单位。如果为 True 则是地理坐标单位，否则采用设备单位。具体查看 :py:meth:`set_offset_x` 和 :py:meth:`set_offset_y` 接口。

        :param bool value: 水平或垂直偏移量的单位是否是地理坐标系单位
        :return: self
        :rtype: ThemeLabel
        """
        self._jobject.setOffsetFixed(not parse_bool(value))
        return self

    def is_flow_enabled(self):
        """
        返回是否流动显示标签。默认为 True。

        :return: 是否流动显示标签
        :rtype: bool
        """
        return self._jobject.isFlowEnabled()

    def set_flow_enabled(self, value):
        """
        设置是否流动显示标签。 流动显示只适合于线和面要素的标注

        :param bool value: 是否流动显示标签。
        :return: self
        :rtype: ThemeLabel
        """
        self._jobject.setFlowEnabled(parse_bool(value))
        return self

    def is_small_geometry_labeled(self):
        """
        当标签的长度大于被标注对象本身的长度时，返回是否显示该标签。

        在标签的长度大于线或者面对象本身的长度时，如果选择继续标注，则标签文字会叠加在一起显示，为了清楚完整的显示该标签，可以采用换行模式来显示标
        签，但必须保证每行的长度小于对象本身的长度。

        :return: 是否显示长度大于被标注对象本身长度的标签
        :rtype: bool
        """
        return self._jobject.isSmallGeometryLabeled()

    def set_small_geometry_labeled(self, value):
        """
        当标签的长度大于被标注对象本身的长度时，设置是否显示该标签。

        在标签的长度大于线或者面对象本身的长度时，如果选择继续标注，则标签文字会叠加在一起显示，为了清楚完整的显示该标签，可以采用换行模式来显示标签，
        但必须保证每行的长度小于对象本身的长度。

        :param bool value: 是否显示长度大于被标注对象本身长度的标签
        :return: self
        :rtype: ThemeLabel
        """
        self._jobject.setSmallGeometryLabeled(parse_bool(value))
        return self

    def is_support_text_expression(self):
        """
        返回是否支持文本表达式，即上下标功能。默认值为 False,不支持文本表达式

        :return: 是否支持文本表达式，即上下标功能
        :rtype: bool
        """
        return self._jobject.isTextExpression()

    def set_support_text_expression(self, value):
        """
        设置是否支持文本表达式，即上下标功能。
        当选择字段为文本类型，文本中含有上下标，并且是根据特定的标准时（文本表达式请参考下面说明），需要设置此属性，以便正确显示文本（如下右图）。
        下图为分别设置此属性值为 False 和 True 时的效果对比：

        .. image:: ../image/isTextExpression.png

        注意:

         * 当设置该属性为true后，具有上下标的文本的标签的对齐方式只能显示为“左上角”效果，不具有上下标的文本的标签的对齐方式与文本风格中设置的对齐方式相同。
         * 不支持有旋转角度的文本标签，即文本标签的旋转角度不为0时，该属性的设置无效。
         * 不支持竖排、换行显示的文本标签。
         * 不支持包含删除线、下划线、分隔符的文本标签。
         * 不支持线数据集的标签专题图沿线标注的文本标签。
         * 当地图有旋转角度时，设置了支持文本表达式的文本标签不随地图的旋转而旋转。
         * 不支持特殊符号的标签专题图的文本标签。
         * 含有上下标的文本表达式中，#+表示上标；#-表示下标，#=表示分割一个字符串为两个上下标部分。
         * 设置了支持文本表达式的文本标签如果以"#+"、"#-"、"#="开始，整个字符串原样输出。

        下图为分别设置此属性值为false和true时的效果对比：

        .. image:: ../image/isTextExpression_1.png

        * 遇到#+或者#-，后边紧挨着的字符串都当成上下标内容、当第三次遇到#+或#-时采用新串规则。下图为分别设置此属性值为flse和true时的效果对比。

          .. image:: ../image/isTextExpression_2.png

        * 含有上下标的文本表达式中，两个连续的"#+"的效果同一个"#-"，两个连续的"#-"的效果同一个"#+"。 下图为分别设置此属性值为false和true时的效果对比：

          .. image:: ../image/isTextExpression_3.png

        * 目前支持该功能的标签专题图类型为统一风格标签专题图，分段风格标签专题图和标签矩阵专题图。

        :param bool value: 否支持文本表达式
        :return: self
        :rtype: ThemeLabel
        """
        self._jobject.setTextExpression(parse_bool(value))
        return self

    def is_vertical(self):
        """
        是否使用竖排标签

        :return: 是否使用竖排标签
        :rtype: bool
        """
        return self._jobject.isVertical()

    def set_vertical(self, value):
        """
        设置是否使用竖排标签。

         * 不支持矩阵标签和沿线标注。
         * 不支持有旋转角度的文本标签，即文本标签的旋转角度大于0时，该属性的设置无效。

        :param bool value: 是否使用竖排标签
        :return: self
        :rtype: ThemeLabel
        """
        self._jobject.setVertical(parse_bool(value))
        return self

    def is_on_top(self):
        """
        返回标签专题图图层是否显示在最上层。这里的最上层是指所有非标签专题图图层的上层。

        :return: 标签专题图图层是否显示在最上层
        :rtype: bool
        """
        return self._jobject.isOnTop()

    def set_on_top(self, value):
        """
        设置标签专题图图层是否显示在最上层。这里的最上层是指所有非标签专题图图层的上层。

        一般制图时，都会把地图中标签专题图图层放在所有非标签专题图图层的最前面，但当使用了图层分组时，分组内的标签专题图层有可能被位于上层图层分组中
        的其他普通图层掩盖，为了即保持图层分组状态，又要使标签不被掩盖，可以使用 set_on_top 方法传入true值，标签专题图不论当前在地图中的位置，都将显
        示在最前面；如果有多个标签专题图图层都通过 set_on_top 方法传入 true值，那么他们之间显示顺序，由他们所在地图的图层顺序决定。

        :param bool value: 标签专题图图层是否显示在最上层
        :return: self
        :rtype: ThemeLabel
        """
        self._jobject.setOnTop(parse_bool(value))
        return self

    def is_overlap_avoided(self):
        """
        返回是否允许以文本避让方式显示文本。只针对该标签专题图层中的文本数据。

        :return: 是否自动避免文本叠盖。
        :rtype: bool
        """
        return self._jobject.isOverlapAvoided()

    def set_overlap_avoided(self, value):
        """
        设置是否允许以文本避让方式显示文本。只针对该标签专题图层中的文本数据。

        注：在标签重叠度很大的情况下，即使使用自动避让功能，可能也无法完全避免标签重叠现象。当两个相互重叠的标签同时设置了文本避让时，ID 靠前的标签
        文本具有优先绘制权。

        :param bool value: 是否自动避免文本叠盖
        :return: self
        :rtype: ThemeLabel
        """
        self._jobject.setOverlapAvoided(parse_bool(value))
        return self

    def get_overlap_avoided_mode(self):
        """
        获取文本自动避让方式

        :return: 文本自动避让方式
        :rtype: AvoidMode
        """
        java_mode = self._jobject.getOverlapeAvoidMode()
        if not java_mode:
            return
        return AvoidMode._make(java_mode.name())

    def set_overlap_avoided_mode(self, value):
        """
        设置文本自动避让方式

        :param value: 文本自动避让方式
        :type value: AvoidMode or str
        :return: self
        :rtype: ThemeLabel
        """
        value = AvoidMode._make(value)
        if value is not None:
            self._jobject.setOverlapeAvoidMode(oj(value))
        return self

    def is_leader_line_displayed(self):
        """
        返回是否显示标签和它标注的对象之间的牵引线。默认值为 False，即不显示。

        :return: 是否显示标签和它标注的对象之间的牵引线。
        :rtype: bool
        """
        return self._jobject.isLeaderLineDisplayed()

    def get_leader_line_style(self):
        """
        返回标签与其标注对象之间牵引线的风格。

        :return: 标签与其标注对象之间牵引线的风格。
        :rtype: GeoStyle
        """
        return GeoStyle._from_java_object(self._jobject.getLeaderLineStyle())

    def set_leader_line(self, is_displayed=False, leader_line_style=None):
        """
        设置标签与其标注对象之间牵引线是否显示，以及牵引线风格等。

        :param bool is_displayed: 是否显示标签和它标注的对象之间的牵引线。
        :param GeoStyle leader_line_style: 标签与其标注对象之间牵引线的风格。
        :return: self
        :rtype: ThemeLabel
        """
        self._jobject.setLeaderLineDisplayed(parse_bool(is_displayed))
        if isinstance(leader_line_style, GeoStyle):
            self._jobject.setLeaderLineStyle(oj(leader_line_style))
        return self

    def get_numeric_precision(self):
        """
        返回标签中数字的精度。例如标签对应的数字是 8071.64529347，返回值为0时，显示8071，为1时，显示8071.6；为3时，则是8071.645

        :return: 标签中数字的精度。
        :rtype: int
        """
        return self._jobject.getNumericPrecision()

    def set_numeric_precision(self, value):
        """
        设置标签中数字的精度。例如标签对应的数字是8071.64529347，返回值为0时，显示8071，为1时，显示8071.6；为3时，则是8071.645。

        :param int value: 标签中数字的精度。
        :return: self
        :rtype: ThemeLabel
        """
        if value is not None:
            return self._jobject.setNumericPrecision(int(value))
        return self

    def get_label_font_type_expression(self):
        """
        返回一个字段名称，字段值为字体名称，如：微软雅黑、宋体，控制标签专题图中标签文本的字体样式。

        :return: 一个字段名称，该字段控制标签专题图中标签文本的字体样式。
        :rtype: str
        """
        return self._jobject.getLabelFontTypeExpression()

    def set_label_font_type_expression(self, value):
        """
        设置一个字段，该字段值为字体名称，如：微软雅黑、宋体，控制标签专题图中标签文本的字体样式。指定字段后，标签的字体样式将从对应记录的该字段值中读取。

        :param str value: 一个字段，该字段控制标签专题图中标签文本的字体样式。 如果字段值指定的字体在当前系统中不存在，或者字段值为无值，将按照
                          当前标签专题图所设置的具体字体进行显示，如：:py:meth:`set_uniform_style` 方法所设置的文本风格中的字体。
        :return: self
        :rtype: ThemeLabel
        """
        if value is not None:
            self._jobject.setLabelFontTypeExpression(str(value))
        return self

    def get_label_size_expression(self):
        """
        返回一个字段，该字段为数值型字段，字段值控制文字字高，数值单位为毫米。

        :return: 一个字段，该字段控制文字字高。
        :rtype: str
        """
        return self._jobject.getLabelSizeExpression()

    def set_label_size_expression(self, value):
        """
        设置一个字段，该字段为数值型字段，字段值控制文字字高，数值单位为毫米。指定字段后，标签的文字大小将从对应记录的该字段值中读取。

        :param str value:  一个字段，该字段控制文字字高。 如果字段值为无值，将按照当前标签专题图所设置的字体大小的具体数值进行显示
        :return: self
        :rtype: ThemeLabel
        """
        if value is not None:
            self._jobject.setLabelSizeExpression(str(value))
        return self

    def get_label_color_expression(self):
        """
        返回一个字段，该字段为数值型字段，控制文字颜色

        :return: 一个字段，该字段为数值型字段，控制文字颜色。
        :rtype: str
        """
        return self._jobject.getLabelColorExpression()

    def set_label_color_expression(self, value):
        """
        设置一个字段，该字段为数值型字段，控制文字颜色，指定字段后，标签的文字颜色将从对应记录的该字段值中读取。

        :param str value: 一个字段，该字段为数值型字段，控制文字颜色。
                          颜色值支持十六进制表达下为0xRRGGBB，即按照RGB排列。
        :return: self
        :rtype: ThemeLabel
        """
        if value is not None:
            self._jobject.setLabelColorExpression(str(value))
        return self

    def get_label_angle_expression(self):
        """
        返回一个字段，该字段为数值型字段，字段值控制文本的旋转角度

        :return: 一个字段，该字段为数值型字段，字段值控制文本的旋转角度
        :rtype: str
        """
        return self._jobject.getLabelAngleExpression()

    def set_label_angle_expression(self, value):
        """
        设置一个字段，该字段为数值型字段，字段值控制文本的旋转角度。指定字段后，标签的文字旋转角度将从对应记录的该字段值中读取。

        :param str value: 一个字段，该字段为数值型字段，字段值控制文本的旋转角度。
                          数值单位为度。角度旋转以逆时针方向为正方向，对应数值为正值；角度值支持负值，表示沿顺时针方向旋转。
                          关于标签旋转角度和偏移，如果两者同时设置后，先对标签进行角度旋转，再进行偏移。
        :return: self
        :rtype: ThemeLabel
        """
        if value is not None:
            self._jobject.setLabelAngleExpression(str(value))
        return self

    def is_along_line(self):
        """
        返回是否沿线显示文本。True 表示沿线显示文本，False 表示正常显示文本。沿线标注属性只适用于线数据集专题图。默认值为 True

        :return: 是否沿线显示文本。
        :rtype: bool
        """
        return self._jobject.isAlongLine()

    def is_angle_fixed(self):
        """
        当沿线显示文本时，是否将文本角度固定。True 表示按固定文本角度显示文本，False 表示按照沿线角度显示文本。默认值为 False。

        :return: 当沿线显示文本时，是否将文本角度固定。
        :rtype: bool
        """
        return self._jobject.isAngleFixed()

    def get_along_line_culture(self):
        """
        返回沿线标注使用的语言文化习惯。默认值与当前系统的非 Unicode 语言相关。如果是中文环境，为 CHINESE，否则为 ENGLISH。

        :return: 沿线标注使用的语言文化习惯
        :rtype: AlongLineCulture
        """
        java_object = self._jobject.getAlongLineCulture()
        if java_object:
            return AlongLineCulture._make(java_object.name())

    def get_along_line_direction(self):
        """
        返回标签沿线标注方向。默认值 :py:attr:`AlongLineDirection.ALONG_LINE_NORMAL` .

        :return: 标签沿线标注方向。
        :rtype: AlongLineDirection
        """
        java_object = self._jobject.getAlongLineDirection()
        if java_object:
            return AlongLineDirection._make(java_object.name())

    def get_along_line_drawing_mode(self):
        """
        返回设置在沿线标注中，标签绘制所采用的策略。默认为 :py:attr:`AlongLineDrawingMode.COMPATIBLE`

        :return: 标签绘制所采用的策略
        :rtype: AlongLineDrawingMode
        """
        java_object = self._jobject.getAlongLineDrawingMode()
        if java_object:
            return AlongLineDrawingMode._make(java_object.name())

    def get_along_line_space_ratio(self):
        """
        返回沿线文本间隔比率。该值为字高的倍数。

        注意:
         * 该值大于1就以线中心为准，按指定间隔往两边标注；
         * 该值在0到1之间（包含1）就在线中心按照沿线角度标注单个文本。
         * 该值小于等于0采用默认的沿线标注模式。

        :return: 沿线文本间隔比率
        :rtype: float
        """
        return self._jobject.getAlongLineSpaceRatio()

    def get_along_line_word_angle_range(self):
        """
        返回沿线标注中字与字或者字母与字母间相对角度的容限值，单位为：度。
        沿线标注中，中文标签与英文标签为了适应弯曲线的走势，文字或者字母会发生旋转，但是单个字或者字母始终与其当前标注点位的切线方向垂直，因此，会出
        现如下图所示的效果，相邻字或者字母形成一定的夹角，当线的弯曲度较大时，夹角也增大，会出现标签整体不美观的效果。因此，该接口通过一个给定的容限
        值，限制相邻字或者字母夹角最大值，以保证沿线标注的美观性。

        夹角容限值越小，标签越紧凑，但弯度大的地方可能就无法进行标注；夹角容限值越大，弯度大的地方也能显示标注，但是沿线标注的美观性降低了。

        .. image:: ../image/LabelWordAngle10.png

        .. image:: ../image/LabelWordAngle20.png

        .. image:: ../image/LabelWordAngle40.png

        沿线标注中字与字或者字母与字母间相对角度指的是什么？如下图所示：

        .. image:: ../image/LabelWordAngle.png

        :return: 沿线标注中字与字或者字母与字母间相对角度的容限值，单位为：度
        :rtype: int
        """
        return self._jobject.getAlongLineWordAngleRange()

    def get_label_repeat_interval(self):
        """
        返回在沿线标注时循环标注的间隔。所设置的间隔大小代表打印后相邻标注间隔的纸面距离，单位为0.1毫米。例如：循环标注间隔值设置为500，地图打印后，
        在纸面上量算相邻标注间的距离就为5厘米。

        :return: 沿线标注时循环标注的间隔
        :rtype: float
        """
        return self._jobject.getLabelRepeatInterval()

    def is_repeat_interval_fixed(self):
        """
        返回循环标注间隔是否固定。True 表示固定循环标注间隔，循环标注间隔不随地图的缩放而变化；False 表示循环标注间隔随地图的缩放而变化。

        :return: 循环标注间隔固定返回 True；否则返回 False
        :rtype: bool
        """
        return self._jobject.isRepeatIntervalFixed()

    def is_repeated_label_avoided(self):
        """
        返回是否避免地图重复标注。

        对于代表北京地铁四号线的线数据，假如由4条子线段组成，当以名称字段（字段值为：地铁四号线）做为专题变量制作标签专题图且设置沿线标注时，如果不
        选择避免地图重复标注，则显示效果如左图，如果选择了避免地图重复标注，系统会将这条折线的四个子线部分看成一条线来进行标注，其显示效果如下图所示。

        .. image:: ../image/IsRepeatedLabelAvoided.png

        :return:
        :rtype: bool
        """
        return self._jobject.isRepeatedLabelAvoided()

    def set_along_line(self, is_along_line=True, is_angle_fixed=False, culture=None, direction='ALONG_LINE_NORMAL', drawing_mode='COMPATIBLE', space_ratio=None, word_angle_range=None, repeat_interval=0, is_repeat_interval_fixed=False, is_repeated_label_avoided=False):
        """
        设置沿线显示文本，只适用于线数据及标签专题图。

        :param bool is_along_line: 是否沿线显示文本
        :param bool is_angle_fixed: 是否将文本角度固定
        :param culture: 沿线标注使用的语言文化习惯。默认与当前系统的非 Unicode 语言相关。如果是中文环境，为 CHINESE，否则为 ENGLISH。
        :type culture: AlongLineCulture or str
        :param direction: 标签沿线标注方向
        :type direction: AlongLineDirection or str
        :param drawing_mode: 标签绘制所采用的策略
        :type drawing_mode: AlongLineDrawingMode or str
        :param float space_ratio: 沿线文本间隔比率，为字高的倍数。
                                  注意:

                                   * 该值大于 1 就以线中心为准，按指定间隔往两边标注

                                   * 该值在 0 到 1 之间（包含1）就在线中心按照沿线角度标注单个文本

                                   * 该值小于等于 0 采用默认的沿线标注模式

        :param int word_angle_range: 字与字或者字母与字母间相对角度的容限值，单位为：度
        :param float repeat_interval: 沿线标注时循环标注的间隔。所设置的间隔大小代表打印后相邻标注间隔的纸面距离，单位为0.1毫米
        :param bool is_repeat_interval_fixed: 循环标注间隔是否固定
        :param bool is_repeated_label_avoided: 是否避免地图重复标注
        :return: self
        :rtype: ThemeLabel
        """
        self._jobject.setAlongLine(parse_bool(is_along_line))
        self._jobject.setAngleFixed(parse_bool(is_angle_fixed))
        culture = AlongLineCulture._make(culture)
        if culture:
            self._jobject.setAlongLineCulture(oj(culture))
        direction = AlongLineDirection._make(direction)
        if direction:
            self._jobject.getAlongLineDirection(oj(direction))
        drawing_mode = AlongLineDrawingMode._make(drawing_mode)
        if drawing_mode:
            self._jobject.setAlongLineDrawingMode(oj(drawing_mode))
        if space_ratio:
            self._jobject.setAlongLineSpaceRatio(float(space_ratio))
        if word_angle_range:
            self._jobject.setAlongLineWordAngleRange(int(word_angle_range))
        if repeat_interval:
            self._jobject.setLabelRepeatInterval(float(repeat_interval))
        self._jobject.setRepeatIntervalFixed(parse_bool(is_repeat_interval_fixed))
        self._jobject.setRepeatedLabelAvoided(parse_bool(is_repeated_label_avoided))
        return self

    def get_overlength_mode(self):
        """
        返回超长标签的处理方式。对超长标签可以不作任何处理，也可以省略超出的部分，或者以换行方式进行显示。

        :return: 超长标签的处理方式
        :rtype: OverLengthLabelMode
        """
        java_mode = self._jobject.getOverLengthMode()
        if java_mode:
            return OverLengthLabelMode._make(java_mode.name())

    def get_max_label_length(self):
        """
        返回标签在每一行显示的最大长度。默认值为256

        如果输入的字符超过设置的最大长度，可以采用两种方式处理，一种是以换行的方式进行显示，这种方式自动调整字间距，尽量使每一行的字符个数相近，故
        每一行显示的字符个数小于等于设置的最大长度； 另一种是以省略号方式进行显示，当输入的字符大于设置的最大长度时，多出的字符将以省略号的方式进行显示。

        :return: 每一行显示的最大长度。
        :rtype: int
        """
        return self._jobject.getMaxLabelLength()

    def get_split_separator(self):
        """
        获取用于标签文本换行的换行符，可以为：“/”、“；”、空格等

        如果通过 :py:meth:`set_overlength_label` 接口设置 overlength_mode 为 :py:attr:`.OverLengthLabelMode.NEWLINE` ，即换行
        方式，同时通过 split_separator 设置了换行符，那么，标签文本将按照特殊字符指定的位置进行换行显示。

        当标签专题图使用换行的方式进行超长文本处理时，可以通过给定特殊字符的方式控制文本的换行位置，这就需要您提前做好数据准备，在用于标注的字段中，
        在字段值需要换行的位置加入您设定的换行符，如“/”、“；”、空格，当使用特殊字符换行时，将在出现指定的特殊字符处进行换行，并且指定的特殊字符不显示。

        :return: 用于标签文本换行的换行符
        :rtype: str
        """
        return self._jobject.getSplitSeparator()

    def set_overlength_label(self, overlength_mode=None, max_label_length=256, split_separator=None):
        """
        设置处理超长文本。

        :param overlength_mode: 超长标签的处理方式。对超长标签可以不作任何处理，也可以省略超出的部分，或者以换行方式进行显示。
        :type overlength_mode: OverLengthLabelMode or str
        :param int max_label_length: 标签在每一行显示的最大长度。如果超过这个长度，可以采用两种方式来处理，一种是换行的模式进行显示，另一种是以省略号方式显示。
        :param str split_separator: 用于标签文本换行的换行符，可以为：“/”、“；”、空格等。当超长标签处理方式为 NEWLINE 时，将根据指定的字符进行换行。
        :return: self
        :rtype: ThemeLabel
        """
        overlength_mode = OverLengthLabelMode._make(overlength_mode)
        if overlength_mode:
            self._jobject.setOverLengthMode(oj(overlength_mode))
        if max_label_length:
            self._jobject.setMaxLabelLength(int(max_label_length))
        if split_separator:
            self._jobject.setSplitSeparator(str(split_separator))
        return self

    def get_max_text_height(self):
        """
        返回标签中文本的最大高度。该方法在标签不固定大小时有效，当放大后的文本高度超过最大高度之后就不再放大。高度单位为 0.1 毫米。

        :return: 标签中文本的最大高度。
        :rtype: int
        """
        return self._jobject.getMaxTextHeight()

    def set_max_text_height(self, value):
        """
        设置标签中文本的最大高度。该方法在标签不固定大小时有效，当放大后的文本高度超过最大高度之后就不再放大。高度单位为 0.1 毫米。

        :param int value: 标签中文本的最大高度。
        :return: self
        :rtype: ThemeLabel
        """
        if value is not None:
            self._jobject.setMaxTextHeight(int(value))
        return self

    def get_min_text_height(self):
        """
        返回标签中文本的最小高度。

        :return: 标签中文本的最小高度。
        :rtype: int
        """
        return self._jobject.getMinTextHeight()

    def set_min_text_height(self, value):
        """
        设置标签中文本的最小高度。

        :param int value: 标签中文本的最大宽度。
        :return: self
        :rtype: ThemeLabel
        """
        if value is not None:
            self._jobject.setMinTextHeight(int(value))
        return self

    def get_text_extent_inflation(self):
        """
        返回标签中文本在 X，Y 正方向上的缓冲范围。通过设置该值可以修改文本在地图中所占空间的大小，必须非负。

        :return: 标签中文本在 X，Y 正方向上的缓冲范围。
        :rtype: tuple[int,int]
        """
        java_size = self._jobject.getTextExtentInflation()
        if java_size:
            return (
             java_size.getWidth(), java_size.getHeight())

    def set_text_extent_inflation(self, width, height):
        """
        设置标签中文本在 X，Y 正方向上的缓冲范围。通过设置该值可以修改文本在地图中所占空间的大小，必须非负。

        :param int width:  X 方向的大小
        :param int height: Y 方向的大小
        :return: self
        :rtype: ThemeLabel
        """
        java_size = get_jvm().com.supermap.data.Size2D(float(width), float(height))
        self._jobject.setTextExtentInflation(java_size)
        return self

    def get_range_expression(self):
        """
        返回分段字段表达式。其中分段表达式中的值必须为数值型的。
        用户根据该方法的返回值来比较其从开始到结束的每一个分段值，以确定采用什么风格来显示给定标注字段表达式相应的标注文本。

        :return: 分段字段表达式
        :rtype: str
        """
        return self._jobject.getRangeExpression()

    def get_range_mode(self):
        """
        返回当前的分段模式。

        :return: 分段模式
        :rtype: RangeMode
        """
        java_mode = self._jobject.getRangeMode()
        if java_mode:
            return RangeMode._make(java_mode.name())

    def set_range_label(self, range_expression, range_mode):
        """
        设置分段标签专题图。

        :param str range_expression: 分段字段表达式。其中分段表达式中的值必须为数值型的。
        :param range_mode: 分段模式
        :type range_mode: RangeMode or str
        :return: self
        :rtype: ThemeLabel
        """
        if range_expression:
            self._jobject.setRangeExpression(str(range_expression))
        range_mode = RangeMode._make(range_mode)
        if range_mode:
            self._jobject.setRangeMode(oj(range_mode))
        return self.get_range_items()

    def get_range_items(self):
        """
        返回分段标签专题图子项集合。基于字段表达式值的分段结果，一个分段对应一个分段标签专题图子项。通过此对象添加分段标签专题图子项。

        :return: 分段标签专题图子项集合
        :rtype: ThemeLabelRangeItems
        """
        java_range_items = self._jobject.getRangeItems()
        if java_range_items:
            return ThemeLabelRangeItems(java_range_items)

    def get_unique_expression(self):
        """
        返回单值字段表达式，表达式可以为一个字段，也可以为多个字段构成的表达式，通过该表达式的值控制对象标签的风格，表达式值相同的对象标签使用相同的风格进行显示。

        :return: 单值字段表达式
        :rtype: str
        """
        return self._jobject.getUniqueExpression()

    def set_unique_label(self, unique_expression):
        """
        设置单值标签标签专题图。

        :param str unique_expression: 单值字段表达式
        :return: self
        :rtype: ThemeLabel
        """
        if unique_expression:
            self._jobject.setUniqueExpression(oj(unique_expression))
        return self.get_unique_items()

    def get_unique_items(self):
        """
        返回单值标签专题图子项集合。基于单值字段表达式值相同的对象标签为一类，一个单值对应一个单值标签专题图子项。

        :return: 单值标签专题图子项集合。
        :rtype: ThemeLabelUniqueItems
        """
        java_unique_items = self._jobject.getUniqueItems()
        if java_unique_items:
            return ThemeLabelUniqueItems(java_unique_items)

    def get_matrix_label(self):
        """
        返回标签专题图中的矩阵标签。在矩阵标签中，标签以矩阵的形式排列在一起。

        :return: 标签专题图中的矩阵标签
        :rtype: LabelMatrix
        """
        java_label_matrix = self._jobject.getLabels()
        if java_label_matrix:
            return LabelMatrix._from_java_object(java_label_matrix)

    def set_matrix_label(self, value):
        """
        设置标签专题图中的矩阵标签。在矩阵标签中，标签以矩阵的形式排列在一起。

        :param LabelMatrix value: 标签专题图中的矩阵标签
        :return: self
        :rtype: ThemeLabel
        """
        if isinstance(value, LabelMatrix):
            self._jobject.setLabels(oj(value))
        return self

    @staticmethod
    def make_default_unique(dataset, label_expression, unique_expression, color_gradient_type=None, join_items=None):
        """
        生成默认的单值标签专题图。

        :param dataset: 用于制作单值标签专题图的矢量数据集。
        :type dataset: DatasetVector or str
        :param str label_expression: 标注字段表达式
        :param str unique_expression: 指定一个字段或者多个字段组成的表达式。该表达式的值用来对对象标签进行分类，值相同的对象标签为一类使用相同的风格显示，不同类的标签使用不同风格显示。
        :param color_gradient_type: 颜色渐变模式
        :type color_gradient_type: ColorGradientType or str
        :param join_items: 外部表连接项
        :type join_items: list[JoinItem] or tuple[JoinItem]
        :return: 单值标签专题图对象
        :rtype: ThemeLabel
        """
        dataset = get_input_dataset(dataset)
        if not isinstance(dataset, DatasetVector):
            raise ValueError("failed get dataset")
        else:
            unique_expression = unique_expression if unique_expression else ""
            color_gradient_type = ColorGradientType._make(color_gradient_type)
            if join_items:
                if isinstance(join_items, JoinItem):
                    join_items = [
                     join_items]
            if join_items:
                join_items = list(filter((lambda it: isinstance(it, JoinItem)), join_items))
            if join_items:
                java_join_items = QueryParameter._to_java_join_items(join_items)
            else:
                java_join_items = None
        java_theme = get_jvm().com.supermap.mapping.ThemeLabel.makeDefault(oj(dataset), str(unique_expression), oj(color_gradient_type), java_join_items)
        theme = ThemeLabel._from_java_object(java_theme)
        if theme:
            return theme.set_label_expression(label_expression)

    @staticmethod
    def make_default_range(dataset, label_expression, range_expression, range_mode, range_parameter, color_gradient_type=None, join_items=None):
        """
        生成默认的分段标签专题图。

        :param dataset: 用于制作分段标签专题图的矢量数据集。
        :type dataset: DataestVector or str
        :param str label_expression: 标注字段表达式
        :param str range_expression: 分段字段表达式。
        :param range_mode: 分段模式
        :type range_mode: RangeMode or str
        :param float range_parameter: 分段参数。当分段模式为等距离分段法，平方根分段法其中一种时，该参数为分段值；当分段模式为标准差分段法的时候，该参数不起作用；当分段模式为自定义距离时，该参数表示自定义距离。
        :param color_gradient_type: 颜色渐变模式。
        :type color_gradient_type: ColorGradientType or str
        :param join_items: 外部表连接项
        :type join_items: list[JoinItem] or tuple[JoinItem]
        :return: 分段标签专题图对象
        :rtype: ThemeLabel
        """
        dataset = get_input_dataset(dataset)
        range_expression = range_expression if range_expression else ""
        range_mode = RangeMode._make(range_mode, "EUQALINTERVAL")
        color_gradient_type = ColorGradientType._make(color_gradient_type)
        if range_mode is RangeMode.STDDEVIATION:
            range_parameter = 0.0
        if isinstance(join_items, JoinItem):
            join_items = [
             join_items]
        if join_items:
            join_items = list(filter((lambda it: isinstance(it, JoinItem)), join_items))
        if join_items and len(join_items) > 0:
            java_join_items = QueryParameter._to_java_join_items(join_items)
        else:
            java_join_items = None
        java_color_gradient_type = oj(color_gradient_type)
        java_theme = get_jvm().com.supermap.mapping.ThemeLabel.makeDefault(oj(dataset), str(range_expression), oj(range_mode), float(range_parameter), java_color_gradient_type, java_join_items)
        theme = ThemeLabel._from_java_object(java_theme)
        if theme:
            return theme.set_label_expression(label_expression)


class ThemeGraphItem:
    __doc__ = "\n    统计专题图子项类。\n\n    统计专题图通过为每个要素或记录绘制统计图来反映其对应的专题值的大小。统计专题图可以基于多个变量，反映多种属性，即可以将多个专题变量的值绘制在一个\n    统计图上。每一个专题变量对应的统计图即为一个专题图子项。本类用来设置统计专题图子项的名称，专题变量，显示风格和分段风格。\n    "

    def __init__(self, expression, caption, style=None, range_setting=None):
        """
        :param str expression: 统计专题图的专题变量。专题变量可以是一个字段或字段表达式
        :param str caption: 专题图子项的名称
        :param GeoStyle style: 统计专题图子项的显示风格
        :param ThemeRange range_setting: 统计专题图子项的分段风格
        """
        self._expression = None
        self._caption = None
        self._style = None
        self._range_setting = None
        self.set_expression(expression).set_caption(caption).set_style(style).set_range_setting(range_setting)

    def __str__(self):
        return "ThemeGraphItem(expression={}, caption={})".format(self.expression, self.caption)

    @property
    def expression(self):
        """str: 统计专题图的专题变量"""
        return self._expression

    def set_expression(self, value):
        """
        设置统计专题图的专题变量。专题变量可以是一个字段或字段表达式。

        :param str value: 统计专题图的专题变量
        :return: self
        :rtype: ThemeGraphItem
        """
        if value is not None:
            self._expression = str(value)
        return self

    @property
    def caption(self):
        """str: 专题图子项的名称"""
        return self._caption

    def set_caption(self, value):
        """
        设置专题图子项的名称。

        :param str value: 专题图子项的名称
        :return: self
        :rtype: ThemeGraphItem
        """
        if value is not None:
            self._caption = str(value)
        return self

    @property
    def style(self):
        """GeoStyle: 返回统计专题图子项的分段风格。"""
        return self._style

    def set_style(self, value):
        """
        设置统计专题图子项的显示风格

        :param value:
        :type value: GeoStyle
        :return: self
        :rtype: ThemeGraphItem
        """
        if isinstance(value, GeoStyle):
            self._style = value
        return self

    @property
    def range_setting(self):
        """ThemeRange: 返回统计专题图子项的分段风格"""
        return self._range_setting

    def set_range_setting(self, value):
        """
        设置统计专题图子项的分段风格

        :param value: 统计专题图子项的分段风格
        :type value: ThemeRange
        :return: self
        :rtype: ThemeGraphItem
        """
        if isinstance(value, ThemeRange):
            self._range_setting = value
        return self

    @property
    def _jobject(self):
        java_object = get_jvm().com.supermap.mapping.ThemeGraphItem()
        if self.expression is not None:
            java_object.setGraphExpression(str(self.expression))
        if self.caption is not None:
            java_object.setCaption(str(self.caption))
        if self.style is not None:
            java_object.setUniformStyle(oj(self.style))
        if self.range_setting is not None:
            java_object.setRangeSetting(oj(self.range_setting))
        return java_object

    @staticmethod
    def _from_java_object(java_object):
        if not java_object:
            return
        return ThemeGraphItem(java_object.getGraphExpression(), java_object.getCaption(), GeoStyle._from_java_object(java_object.getUniformStyle()), Theme._from_java_object(java_object.getRangeSetting()))


@unique
class ThemeGraphType(JEnum):
    __doc__ = "\n    该类定义了统计专题图的统计图类型常量。\n\n    :var ThemeGraphType.AREA: 面积图。面积图显示的时候，多个 ThemeGraphItem 合成一个面，面的风格采用第一个 ThemeGraphItem 的风格渲染。\n\n                              .. image:: ../image/Area.png\n\n\n    :var ThemeGraphType.STEP: 阶梯图。\n\n                              .. image:: ../image/Step.png\n\n\n    :var ThemeGraphType.LINE: 折线图。\n\n                              .. image:: ../image/Line.png\n\n\n    :var ThemeGraphType.POINT: 点状图。\n\n                               .. image:: ../image/Point.png\n\n\n    :var ThemeGraphType.BAR: 柱状图\n\n                             .. image:: ../image/Bar.png\n\n\n    :var ThemeGraphType.BAR3D: 三维柱状图\n\n                               .. image:: ../image/Bar3D.png\n\n\n    :var ThemeGraphType.PIE: 饼图\n\n                              .. image:: ../image/Pie.png\n\n\n    :var ThemeGraphType.PIE3D: 三维饼图。三维饼状图注记标签的大小会根据统计符号的大小进行调整，以避免统计符号很多时，出现统计符号很小，而注记很大，界面上满屏幕都是注记的问题。\n\n                               .. image:: ../image/Pie3D.png\n\n\n    :var ThemeGraphType.ROSE: 玫瑰图\n\n                              .. image:: ../image/Rose.png\n\n\n    :var ThemeGraphType.ROSE3D: 三维玫瑰图\n\n                                .. image:: ../image/Rose3D.png\n\n\n    :var ThemeGraphType.STACK_BAR: 堆叠柱状图\n\n                                    .. image:: ../image/StackedBar.png\n\n\n    :var ThemeGraphType.STACK_BAR3D: 三维堆叠柱状图\n\n                                     .. image:: ../image/StackedBar3D.png\n\n\n    :var ThemeGraphType.RING: 环状图\n\n                              .. image:: ../image/Ring.png\n\n    "
    AREA = 0
    STEP = 1
    LINE = 2
    POINT = 3
    BAR = 4
    BAR3D = 5
    PIE = 6
    PIE3D = 7
    ROSE = 8
    ROSE3D = 9
    STACK_BAR = 12
    STACK_BAR3D = 13
    RING = 14

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.mapping.ThemeGraphType"


@unique
class ThemeGraphTextFormat(JEnum):
    __doc__ = "\n    该类定义了统计专题图文本显示格式类型常量。\n\n    :var ThemeGraphTextFormat.PERCENT: 百分数。以各子项所占的百分比来进行标注。\n\n                                       .. image:: ../image/percent.png\n\n\n    :var ThemeGraphTextFormat.VALUE: 真实数值。以各子项的真实数值来进行标注。\n\n                                      .. image:: ../image/value.png\n\n\n    :var ThemeGraphTextFormat.CAPTION: 标题。以各子项的标题来进行标注。\n\n                                       .. image:: ../image/caption.png\n\n\n    :var ThemeGraphTextFormat.CAPTION_PERCENT: 标题+百分数。以各子项的标题和百分比来进行标注。\n\n                                               .. image:: ../image/captionpercent.png\n\n\n    :var ThemeGraphTextFormat.CAPTION_VALUE: 标题+真实数值。以各子项的标题和真实数值来进行标注。\n\n                                             .. image:: ../image/captionvalue.png\n\n\n    "
    PERCENT = 1
    VALUE = 2
    CAPTION = 3
    CAPTION_PERCENT = 4
    CAPTION_VALUE = 5

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.mapping.ThemeGraphTextFormat"


@unique
class GraphAxesTextDisplayMode(JEnum):
    __doc__ = "\n    统计专题图坐标轴文本显示模式。\n\n    :var GraphAxesTextDisplayMode.NONE: 没有显示\n    :var GraphAxesTextDisplayMode.YAXES: 显示 Y 轴的文本\n    :var GraphAxesTextDisplayMode.ALL: 显示全部文本\n    "
    NONE = 0
    YAXES = 2
    ALL = 3

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.mapping.GraphAxesTextDisplayMode"


class ThemeGraph(Theme):
    __doc__ = "\n    统计专题图类。\n    统计专题图通过为每个要素或记录绘制统计图来反映其对应的专题值的大小。统计专题图可以基于多个变量，反映多种属性，即可以将多个专题变量的值绘制在一个统计图上。\n\n    "

    def __init__(self, graph_type='PIE3D', graduated_mode='CONSTANT', items=None):
        """
        :param graph_type: 统计专题图的统计图类型。根据实际的数据和用途的不同，可以选择不同类型的统计图。
        :type graph_type: ThemeGraphType or str
        :param graduated_mode: 专题图分级模式
        :type graduated_mode: GraduatedMode or str
        :param items: 统计专题图子项列表
        :type items: list[ThemeGraphItem] or tuple[ThemeGraphItem]
        """
        Theme.__init__(self)
        self._type = ThemeType.GRAPH
        self.set_graph_type(graph_type).set_graduated_mode(graduated_mode).extend(items)

    def _make_java_object(self):
        return self._jvm.com.supermap.mapping.ThemeGraph()

    def extend(self, items):
        """
        批量添加统计专题图子项

        :param items: 统计专题图子项列表
        :type items: list[ThemeGraphItem] or tuple[ThemeGraphItem]
        :return: self
        :rtype: ThemeGraph
        """
        if isinstance(items, ThemeGraphItem):
            items = [
             items]
        if isinstance(items, (list, tuple)):
            r_items = list(items)
            r_items.reverse()
            for item in r_items:
                self.add(item)

        return self

    def add(self, item):
        """
        添加统计专题图子项

        :param ThemeGraphItem item: 统计专题图子项
        :return: self
        :rtype: ThemeGraph
        """
        if isinstance(item, ThemeGraphItem):
            self._jobject.add(oj(item))
        return self

    def clear(self):
        """
        删除统计专题图中的所有子项。

        :return: self
        :rtype: ThemeGraph
        """
        self._jobject.clear()
        return self

    def get_count(self):
        """
        返回统计专题图子项的个数

        :return: 统计专题图子项的个数
        :rtype: int
        """
        return self._jobject.getCount()

    def __getitem__(self, index):
        return self.get_item(index)

    def get_item(self, index):
        """
        用指定的统计专题图子项替代指定序号上的专题图子项。

        :param int index: 指定的序号。
        :return: 统计专题图子项
        :rtype: ThemeGraphItem
        """
        if index < 0:
            index = index + self._jobject.getCount()
        return ThemeGraphItem._from_java_object(self._jobject.getItem(int(index)))

    def index_of(self, expression):
        """
        返回统计专题图中指定统计字段表达式的对象在当前统计图子项序列中的序号。

        :param str expression: 指定的统计字段表达式。
        :return: 统计专题图子项在序列中的序号。
        :rtype: int
        """
        return self._jobject.indexOf(str(expression) if expression else "")

    def remove(self, index):
        """
        在统计专题图子项序列中删除指定序号的统计专题图子项。

        :param int index: 指定的将被删除子项的序号
        :return: 删除成功，返回 True；否则返回 False。
        :rtype: bool
        """
        if index < 0:
            index = index + self._jobject.getCount()
        return self._jobject.remove(int(index))

    def insert(self, index, item):
        """
        将给定的统计专题图子项插入到指定序号的位置。

        :param int index: 指定的统计专题图子项序列的序号。
        :param ThemeGraphItem item: 将被插入的统计专题图子项。
        :return: 插入成功返回 True，否则为 False
        :rtype: bool
        """
        if index < 0:
            index = index + self._jobject.getCount()
        if isinstance(item, ThemeGraphItem):
            return self._jobject.insert(int(index), oj(item))
        return False

    def exchange_item(self, index1, index2):
        """
        将指定序号的两个子项进行位置交换。

        :param int index1: 指定的交换第一个子项的序号。
        :param int index2: 指定的交换第二个子项的序号。
        :return: 交换成功，返回 True，否则为 False
        :rtype: bool
        """
        if index1 < 0:
            index1 += self.get_count()
        if index2 < 0:
            index2 += self.get_count()
        return self._jobject.exchangeItem(int(index1), int(index2))

    @property
    def graduated_mode(self):
        """GraduatedMode: 专题图分级模式"""
        java_mode = self._jobject.getGraduatedMode()
        if java_mode:
            return GraduatedMode._make(java_mode.name())

    def set_graduated_mode(self, value):
        """
        设置设置专题图分级模式

        :param value: 设置专题图分级模式
        :type value: GraduatedMode or str
        :return: self
        :rtype: ThemeGraph
        """
        self._jobject.setGraduatedMode(oj(GraduatedMode._make(value, GraduatedMode.CONSTANT)))
        return self

    @property
    def graph_type(self):
        """ThemeGraphType: 统计专题图的统计图类型"""
        java_type = self._jobject.getGraphType()
        if java_type:
            return ThemeGraphType._make(java_type.name())

    def set_graph_type(self, value):
        """
        设置统计专题图的统计图类型。根据实际的数据和用途的不同，可以选择不同类型的统计图。

        :param value: 统计专题图的统计图类型
        :type value: ThemeGraphType or str
        :return: self
        :rtype: ThemeGraph
        """
        value = ThemeGraphType._make(value)
        if value is not None:
            self._jobject.setGraphType(oj(value))
        return self

    def get_graph_text_format(self):
        """
        返回统计专题图文本显示格式

        :return: 统计专题图文本显示格式
        :rtype: ThemeGraphTextFormat
        """
        java_text_format = self._jobject.getGraphTextFormat()
        if java_text_format:
            return ThemeGraphTextFormat._make(java_text_format.name())

    def set_display_graph_text(self, value):
        """
        设置是否显示统计图上的文本标注

        :param bool value: 指定是否显示统计图上的文本标注
        :return: self
        :rtype: ThemeGraph
        """
        if value is not None:
            self._jobject.setGraphTextDisplayed(parse_bool(value))
        return self

    def is_display_graph_text(self):
        """
        返回是否显示统计图上的文本标注

        :return: 是否显示统计图上的文本标注
        :rtype: bool
        """
        return self._jobject.isGraphTextDisplayed()

    def set_graph_text_format(self, value):
        """
        设置统计专题图文本显示格式。

        :param value: 统计专题图文本显示格式
        :type value: ThemeGraphTextFormat or str
        :return: self
        :rtype: ThemeGraph
        """
        value = ThemeGraphTextFormat._make(value, "PERCENT")
        if value is not None:
            self._jobject.setGraphTextFormat(oj(value))
        return self

    def get_graph_text_style(self):
        """
        返回统计图上的文字标注风格。统计专题图上坐标轴的文本对齐方式均采用右下角的对齐方式，以防止坐标轴压盖文本

        :return: 统计图上的文字标注风格。
        :rtype: TextStyle
        """
        return TextStyle._from_java_object(self._jobject.getGraphTextStyle())

    def set_graph_text_style(self, value):
        """
        设置统计图上的文字标注风格。统计专题图上坐标轴的文本对齐方式均采用右下角的对齐方式，以防止坐标轴压盖文本

        :param TextStyle value: 统计图上的文字标注风格
        :return: self
        :rtype: ThemeGraph
        """
        if isinstance(value, TextStyle):
            self._jobject.setGraphTextStyle(oj(value))
        return self

    def get_max_graph_size(self):
        """
        返回统计专题图中统计符号显示的最大值。统计图中统计符号的显示大小均在最大、最小值之间逐渐变化。统计图的最大、最小值是与统计对象的多少和图层大小相关系的一个值。

        :return: 统计专题图中统计符号显示的最大值
        :rtype: float
        """
        return self._jobject.getMaxGraphSize()

    def set_max_graph_size(self, value):
        """
        设置统计专题图中统计符号显示的最大值。统计图中统计符号的显示大小均在最大、最小值之间逐渐变化。统计图的最大、最小值是与统计对象的多少和图层大小相关系的一个值。

        当 :py:meth:`is_graph_size_fixed` 为 True 时，单位为 0.01mm，:py:meth:`is_graph_size_fixed` 为 False 时，使用地图单位。

        :param float value: 统计专题图中统计符号显示的最大值
        :return: self
        :rtype: ThemeGraph
        """
        if value is not None:
            self._jobject.setMaxGraphSize(float(value))
        return self

    def get_min_graph_size(self):
        """
        返回统计专题图中统计符号显示的最小值。

        :return: 统计专题图中统计符号显示的最小值。
        :rtype: float
        """
        return self._jobject.getMinGraphSize()

    def set_min_graph_size(self, value):
        """
        设置统计专题图中统计符号显示的最小值。统计图中统计符号的显示大小均在最大、最小值之间逐渐变化。统计图的最大、最小值是与统计对象的多少和图层大小相关系的一个值。

        当 :py:meth:`is_graph_size_fixed` 为 True 时，单位为 0.01mm，:py:meth:`is_graph_size_fixed` 为 False 时，使用地图单位。

        :param float value: 统计专题图中统计符号显示的最小值。
        :return: self
        :rtype: ThemeGraph
        """
        if value is not None:
            self._jobject.setMinGraphSize(float(value))
        return self

    def get_custom_graph_size_expression(self):
        """
        返回一个字段表达式，该字段表达式用于控制对象对应的统计专题图元素的大小，字段表达式中的字段必须为数值型字段。 该字段表达式可以指定一个字段也
        可以指定一个字段表达式；还可以指定一个数值，此时所有专题图子项将以该数值指定的大小统一显示。

        :return: 用于控制对象对应的统计专题图元素的大小的字段表达式
        :rtype: str
        """
        return self._jobject.getCustomGraphSizeExpression()

    def set_custom_graph_size_expression(self, value):
        """
        设置一个字段表达式，该字段表达式用于控制对象对应的统计专题图元素的大小，字段表达式中的字段必须为数值型字段。 该字段表达式可以指定一个字段也
        可以指定一个字段表达式；还可以指定一个数值，此时所有专题图子项将以该数值指定的大小统一显示。

        :param str value:  用于控制对象对应的统计专题图元素的大小的字段表达式
        :return: self
        :rtype: ThemeGraph
        """
        if value is not None:
            return self._jobject.setCustomGraphSizeExpression(str(value))
        return self

    def is_graph_size_fixed(self):
        """
        返回在放大或者缩小地图时统计图是否固定大小。

        :return: 在放大或者缩小地图时统计图是否固定大小。
        :rtype: bool
        """
        return self._jobject.isGraphSizeFixed()

    def set_graph_size_fixed(self, value):
        """
        设置在放大或者缩小地图时统计图是否固定大小。

        :param bool value: 在放大或者缩小地图时统计图是否固定大小。
        :return: self
        :rtype: ThemeGraph
        """
        self._jobject.setGraphSizeFixed(parse_bool(value))
        return self

    def is_global_max_value_enabled(self):
        """
        返回是否使用全局最大值制作统计专题图。True，表示使用全局最大值作为统计图元素的最大值，保证同一专题图层中统计图元素具有一致的刻度。

        :return: 是否使用全局最大值制作统计专题图
        :rtype: bool
        """
        return self._jobject.isGlobalMaxValueEnabled()

    def set_global_max_value_enabled(self, value):
        """
        设置是否使用全局最大值制作统计专题图。True，表示使用全局最大值作为统计图元素的最大值，保证同一专题图层中统计图元素具有一致的刻度。

        :param bool value: 是否使用全局最大值制作统计专题图
        :return: self
        :rtype: ThemeGraph
        """
        self._jobject.setGlobalMaxValueEnabled(parse_bool(value))
        return self

    def is_overlap_avoided(self):
        """
        返回统计图是否采用避让方式显示。采用避让方式显示返回 true，否则返回 false

        :return: 是否采用避让方式显示
        :rtype: bool
        """
        return self._jobject.isOverlapAvoided()

    def set_overlap_avoided(self, value):
        """
        设置统计图是否采用避让方式显示。

        * 对数据集制作统计专题图 当统计图采用避让方式显示时，如果 :py:meth:`.Map.is_overlap_displayed` 方法设置为 True，则在统计图重叠度很大的情况下，
          会出现无法完全避免统计图重叠的现象；当 :py:meth:`.Map.is_overlap_displayed` 方法设置为 False 时，会过滤掉一些统计图，从而保证所有的统计图均不重叠。

        * 对数据集同时制作统计专题图和标签专题图
          - 当统计图不显示子项文本时，标签专题图的标签即使和统计图重叠，两者也都可正常显示；
          - 当统计图显示子项文本时，如果统计图中的子项文本和标签专题图中的标签不重叠，则两者均正常显示；如果重叠，则会过滤掉统计图的子项文本，只显示标签。

        :param bool value: 是否采用避让方式显示
        :return: self
        :rtype: ThemeGraph
        """
        self._jobject.setOverlapAvoided(parse_bool(value))
        return self

    def is_all_directions_overlapped_avoided(self):
        """
        返回是否允许以全方向统计专题图避让

        :return: 是否允许以全方向统计专题图避让
        :rtype: bool
        """
        return self._jobject.isAllDirectionsOverlappedAvoided()

    def set_all_directions_overlapped_avoided(self, value):
        """
        设置是否允许以全方向统计专题图避让。全方向即指以统计专题图外边框和基准线而形成的 12 个方向。四方向是指以统计专题图外边矩形框的四个角点方向。

        通常统计专题图避让是以全方向进行的，虽然避让比较合理，但会影响显示效率；如果提高显示效率，请设置为False。

        :param bool value: 是否以全方向统计专题图避让
        :return: self
        :rtype: ThemeGraph
        """
        self._jobject.setAllDirectionsOverlappedAvoided(parse_bool(value))
        return self

    def is_negative_displayed(self):
        """
        返回专题图中是否显示属性为负值的数据。

        :return: 专题图中是否显示属性为负值的数据
        :rtype: bool
        """
        return self._jobject.isNegativeDisplayed()

    def set_negative_displayed(self, value):
        """
        设置专题图中是否显示属性为负值的数据。

        该方法对面积图、阶梯图、折线图、点状图、柱状图、三维柱状图无效，因为在绘制时会始终显示负值数据；

        对于饼图、三维饼图、玫瑰图、三维玫瑰图、金字塔专题图-条形、金字塔专题图-面形，如果用户将该方法参数设为 True，则将负值取绝对值后按照正值进
        行处理，若设置为 False，则不对其进行绘制（正、负值数据均不绘制）

        :param bool value: 专题图中是否显示属性为负值的数据
        :return: self
        :rtype: ThemeGraph
        """
        self._jobject.setNegativeDisplayed(parse_bool(value))
        return self

    def is_flow_enabled(self):
        """
        返回统计专题图是否流动显示。

        :return: 统计专题图是否流动显示
        :rtype: bool
        """
        return self._jobject.isFlowEnabled()

    def set_flow_enabled(self, value):
        """
        设置统计专题图是否流动显示。

        :param bool value: 统计专题图是否流动显示。
        :return: self
        :rtype: ThemeGraph
        """
        self._jobject.set_flow_enabled(parse_bool(value))
        return self

    def is_leader_line_displayed(self):
        """
        返回是否显示统计图和它所表示的对象之间的牵引线。如果渲染符号偏移该对象，图与对象之间可以采用牵引线进行连接。

        :return: 是否显示统计图和它所表示的对象之间的牵引线
        :rtype: bool
        """
        return self._jobject.isLeaderLineDisplayed()

    def get_leader_line_style(self):
        """
        返回统计图与其表示对象之间牵引线的风格。

        :return: 统计图与其表示对象之间牵引线的风格。
        :rtype: GeoStyle
        """
        return GeoStyle._from_java_object(self._jobject.getLeaderLineStyle())

    def set_leader_line(self, is_displayed, style):
        """
        设置显示统计图和它所表示的对象之间的牵引线

        :param bool is_displayed: 是否显示统计图和它所表示的对象之间的牵引线
        :param GeoStyle style: 统计图与其表示对象之间牵引线的风格。
        :return: self
        :rtype: ThemeGraph
        """
        self._jobject.setLeaderLineDisplayed(parse_bool(is_displayed))
        if isinstance(style, GeoStyle):
            self._jobject.setLeaderLineStyle(oj(style))
        return self

    def get_axes_color(self):
        """
        返回坐标轴颜色。

        :return: 坐标轴颜色。
        :rtype: Color
        """
        return Color._from_java_object(self._jobject.getAxesColor())

    def is_axes_displayed(self):
        """
        返回是否显示坐标轴

        :return: 是否显示坐标轴
        :rtype: bool
        """
        return self._jobject.isAxesDisplayed()

    def is_axes_grid_displayed(self):
        """
        获取是否在统计图坐标轴上显示网格

        :return: 是否在统计图坐标轴上显示网格
        :rtype: bool
        """
        return self._jobject.isAxesGridDisplayed()

    def is_axes_text_displayed(self):
        """
        返回是否显示坐标轴的文本标注。

        :return: 是否显示坐标轴的文本标注
        :rtype: bool
        """
        return self._jobject.isAxesTextDisplayed()

    def get_axes_text_display_mode(self):
        """
        显示坐标轴文本时，显示的文本模式

        :return: 显示坐标轴文本时，显示的文本模式
        :rtype: GraphAxesTextDisplayMode
        """
        java_mode = self._jobject.getAxesTextDisplayMode()
        if java_mode:
            return GraphAxesTextDisplayMode._make(java_mode.name())

    def get_axes_text_style(self):
        """
        返回统计图坐标轴文本的风格

        :return: 统计图坐标轴文本的风格
        :rtype: TextStyle
        """
        return TextStyle._from_java_object(self._jobject.getAxesTextStyle())

    def set_axes(self, is_displayed=True, color=(128, 128, 128), is_text_displayed=False, text_display_mode='', text_style=None, is_grid_displayed=False):
        """
        设置是否坐标轴，以及坐标轴文本标注相关内容。

        :param bool is_displayed: 是否显示坐标轴。
        :param color: 坐标轴颜色
        :type color: Color or str
        :param bool is_text_displayed: 是否显示坐标轴的文本标注
        :param text_display_mode: 显示坐标轴文本时，显示的文本模式
        :type text_display_mode: GraphAxesTextDisplayMode or str
        :param TextStyle text_style: 统计图坐标轴文本的风格
        :param bool is_grid_displayed: 是否在统计图坐标轴上显示网格
        :return: self
        :rtype: ThemeGraph
        """
        self._jobject.setAxesDisplayed(parse_bool(is_displayed))
        color = Color.make(color)
        if isinstance(color, Color):
            self._jobject.setAxesColor(to_java_color(color))
        self._jobject.setAxesTextDisplayed(parse_bool(is_text_displayed))
        display_mode = GraphAxesTextDisplayMode._make(text_display_mode)
        if display_mode:
            self._jobject.setAxesTextDisplayMode(oj(display_mode))
        if isinstance(text_style, TextStyle):
            self._jobject.setAxesTextStyle(oj(text_style))
        self._jobject.setAxesGridDisplayed(parse_bool(is_grid_displayed))
        return self

    def get_bar_space_ratio(self):
        """
        返回柱状专题图中柱体的间隔，返回值为一个系数值，数值范围为0到10，默认值为1

        :return: 柱状专题图中柱体的间隔
        :rtype: float
        """
        return self._jobject.getBarSpaceRatio()

    def set_bar_space_ratio(self, value):
        """
        设置柱状专题图中柱体的间隔，设置的值为一个系数值，数值范围为0到10，默认值为1。柱状统计图的柱体间隔等于原始间隔乘以系数值。

        :param float value:  柱状专题图中柱体的间隔
        :return: self
        :rtype: ThemeGraph
        """
        if value is not None:
            self._jobject.setBarSpaceRatio(float(value))
        return self

    def get_bar_width_ratio(self):
        """
        返回柱状专题图中每一个柱的宽度，返回值为一个系数值，数值范围为0到10，默认值为1。柱状统计图的柱宽等于原始柱宽乘以系数值。

        :return: 柱状专题图中每一个柱的宽度。为一个系数值，数值范围为0到10
        :rtype: float
        """
        return self._jobject.getBarWidthRatio()

    def set_bar_width_ratio(self, value):
        """
        设置柱状专题图中每一个柱的宽度，设置的值为一个系数值，数值范围为0到10，默认值为1。柱状统计图的柱宽等于原始柱宽乘以系数值。

        :param float value: 柱状专题图中每一个柱的宽度，该值为一个系数值，数值范围为0到10。
        :return: self
        :rtype: ThemeGraph
        """
        if value is not None:
            self._jobject.setBarWidthRatio(float(value))
        return self

    def get_rose_angle(self):
        """
        返回统计图中玫瑰图或三维玫瑰图分片的角度。单位为度，精确到 0.1 度

        :return: 统计图中玫瑰图或三维玫瑰图分片的角度
        :rtype: float
        """
        return self._jobject.getRoseAngle()

    def set_rose_angle(self, value):
        """
        设置统计图中玫瑰图或三维玫瑰图分片的角度。单位为度，精确到 0.1 度。

        :param float value: 统计图中玫瑰图或三维玫瑰图分片的角度。
        :return: self
        :rtype: ThemeGraph
        """
        if value is not None:
            self._jobject.setRoseAngle(float(value))
        return self

    def get_start_angle(self):
        """
        返回饼状统计图的起始角度，默认以水平方向为正向。单位为度，精确到 0.1 度。

        :return:
        饼状统计图的起始角度
        :rtype: float
        """
        return self._jobject.getStartAngle()

    def set_start_angle(self, value):
        """
        设置饼状统计图的起始角度，默认以水平方向为正向。单位为度，精确到 0.1 度。
        只有选择的统计图类型为饼状图（饼图、三维饼图、玫瑰图、三维玫瑰图）时才有效。

        :param float value:
        :return: self
        :rtype: ThemeGraph
        """
        if value is not None:
            self._jobject.setStartAngle(float(value))
        return self

    def get_offset_x(self):
        """
        返回统计图的水平偏移量

        :return: 水平偏移量
        :rtype: str
        """
        return self._jobject.getOffsetX()

    def set_offset_x(self, value):
        """
        设置统计图的水平偏移量

        :param str value: 水平偏移量
        :return: self
        :rtype: ThemeGraph
        """
        if value is not None:
            self._jobject.setOffsetX(str(value))
        return self

    def get_offset_y(self):
        """
        返回统计图的垂直偏移量

        :return: 垂直偏移量
        :rtype: str
        """
        return self._jobject.getOffsetY()

    def set_offset_y(self, value):
        """
        设置统计图的垂直偏移量

        :param str value: 垂直偏移量
        :return: self
        :rtype: ThemeGraph
        """
        if value is not None:
            self._jobject.setOffsetY(str(value))
        return self

    def set_offset_prj_coordinate_unit(self, value):
        """
        设置水平或垂直偏移量的单位是否是地理坐标系单位。如果为 True 则是地理坐标单位，否则采用设备单位。具体查看 :py:meth:`set_offset_x` 和 :py:meth:`set_offset_y` 接口。

        :param bool value: 水平或垂直偏移量的单位是否是地理坐标系单位
        :return: self
        :rtype: ThemeGraph
        """
        self._jobject.setOffsetFixed(not parse_bool(value))
        return self

    def is_offset_prj_coordinate_unit(self):
        """
        获取水平或垂直偏移量的单位是否是地理坐标系单位

        :return: 水平或垂直偏移量的单位是否是地理坐标系单位。如果为 True 则是地理坐标单位，否则采用设备单位。
        :rtype: bool
        """
        return not self._jobject.isOffsetFixed()


@unique
class GraduatedMode(JEnum):
    __doc__ = "\n    该类定义了专题图分级模式类型常量。主要用在统计专题图和等级符号专题图中。\n\n    分级主要是为了减少制作专题图时数据大小之间的差异。如果数据之间差距较大，则可以采用对数或者平方根的分级方式来进行，这样就减少了数据之间的绝对大小\n    的差异，使得专题图的视觉效果比较好，同时不同类别之间的比较也还是有意义的。有三种分级模式：常数、对数和平方根，对于有值为负数的字段，在采用对数和\n    平方根的分级方式时，将取负值的绝对值作为参与计算的值。\n\n    :var GraduatedMode.CONSTANT: 常量分级模式。按属性表中原始数值的线性比例进行分级运算。\n    :var GraduatedMode.SQUAREROOT: 平方根分级模式。按属性表中原始数值平方根的线性比例进行分级运算。\n    :var GraduatedMode.LOGARITHM: 对数分级模式。按属性表中原始数值自然对数的线性比例进行分级运算。\n    "
    CONSTANT = 0
    SQUAREROOT = 1
    LOGARITHM = 2

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.mapping.GraduatedMode"

    @classmethod
    def _externals(cls):
        return {'square':GraduatedMode.SQUAREROOT,  'log':GraduatedMode.LOGARITHM, 
         'const':GraduatedMode.CONSTANT}


class ThemeGraduatedSymbol(Theme):
    __doc__ = "\n    等级符号专题图类。\n\n    SuperMap iObjects 的等级符号专题图是采用不同的形状、颜色和大小的符号， 表示各自独立的、以整体概念显示的各个物体的数量与质量特征。\n    通常以符号的形状、颜色和大小反映物体的特定属性； 符号的形状与颜色表示质量特征，符号的大小表示数量特征。\n\n    例如，可以通过以下方式创建等级符号专题图对象::\n\n    >>> theme = ThemeGraduatedSymbol.make_default(dataset, 'SmID')\n\n    或者::\n\n    >>> theme = ThemeGraduatedSymbol()\n    >>> theme.set_expression('SmID').set_graduated_mode(GraduatedMode.CONSTANT).set_base_value(120).set_flow_enabled(True)\n\n    "

    def __init__(self, expression=None, base_value=0, positive_style=None, graduated_mode='CONSTANT'):
        """

        :param str expression: 用于创建等级符号专题图的字段或字段表达式。用于制作等级符号专题图的字段或者字段表达式应为数值型字段
        :param float base_value: 等级符号专题图的基准值，单位同专题变量的单位
        :param GeoStyle positive_style: 正值的等级符号风格
        :param graduated_mode: 等级符号专题图分级模式
        :type graduated_mode: GraduatedMode or str
        """
        Theme.__init__(self)
        self._type = ThemeType.GRADUATEDSYMBOL
        self.set_expression(expression).set_base_value(base_value).set_graduated_mode(graduated_mode).set_positive_style(positive_style)

    def _make_java_object(self):
        return self._jvm.com.supermap.mapping.ThemeGraduatedSymbol()

    @staticmethod
    def make_default(dataset, expression, graduated_mode='CONSTANT'):
        """
        生成默认的等级符号专题图。

        :param dataset: 矢量数据集。
        :type dataset: DataetVector or str
        :param str expression: 字段表达式
        :param graduated_mode: 专题图分级模式类型。
        :type graduated_mode: GraduatedMode or str
        :return: 等级符号专题图
        :rtype: ThemeGraduatedSymbol
        """
        dataset = get_input_dataset(dataset)
        if not isinstance(dataset, DatasetVector):
            raise ValueError("Failed get DatasetVector")
        graduated_mode = GraduatedMode._make(graduated_mode)
        if not expression:
            expression = ""
        java_theme = get_jvm().com.supermap.mapping.ThemeGraduatedSymbol.makeDefault(oj(dataset), str(expression), oj(graduated_mode))
        return Theme._from_java_object(java_theme)

    @property
    def base_value(self):
        """float: 等级符号专题图的基准值，单位同专题变量的单位。"""
        return self._jobject.getBaseValue()

    def set_base_value(self, value):
        """
        设置等级符号专题图的基准值，单位同专题变量的单位。

        每个符号的显示大小等于
        :py:meth:`.get_positive_style` (或 :py:meth:`.get_zero_style` 或 :py:meth:`.get_negative_style` ) :py:meth:`.GeoStyle.marker_size` *value/base_value，
        其中，value 指的是经过分级计算后的专题值， 即按照用户选择的分级模式( :py:attr:`.graduated_mode` )对专题值进行计算后得到的值。

        :param float value: 等级符号专题图的基准值
        :return: self
        :rtype: ThemeGraduatedSymbol
        """
        if value is not None:
            self._jobject.setBaseValue(float(value))
        return self

    @property
    def expression(self):
        """str: 用于创建等级符号专题图的字段或字段表达式。"""
        return self._jobject.getExpression()

    def set_expression(self, value):
        """
        设置用于创建等级符号专题图的字段或字段表达式。 用于制作等级符号专题图的字段或者字段表达式应为数值型字段。

        :param str value: 用于创建等级符号专题图的字段或字段表达式。
        :return: self
        :rtype: ThemeGraduatedSymbol
        """
        if value is not None:
            self._jobject.setExpression(str(value))
        return self

    @property
    def graduated_mode(self):
        """GraduatedMode: 返回等级符号专题图分级模式"""
        java_mode = self._jobject.getGraduatedMode()
        if java_mode:
            return GraduatedMode._make(java_mode.name())

    def set_graduated_mode(self, value):
        """
        设置等级符号专题图分级模式。

        * 分级主要是为了减少制作等级符号专题图中数据大小之间的差异。如果数据之间差距较大，则可以采用对数或者平方根的分级方式来进行，这样就减少了数据
          之间的绝对大小的差异，使得等级符号的视觉效果比较好，同时不同类别之间的比较也还是有意义的；

        * 有三种分级模式：常数、对数和平方根，对于有值为负数的字段，不可以采用对数和平方根的分级方式；

        * 不同的分级模式用于确定符号大小的数值是不相同的，常数按照字段的原始数据进行，对数则是对每条记录对应的专题值取自然对数、平方根则是对其取平方
          根，用最终得到的结果来确定其等级符号的大小。

        :param value: 等级符号专题图分级模式
        :type value: GraduatedMode or str
        :return: self
        :rtype: ThemeGraduatedSymbol
        """
        value = GraduatedMode._make(value, GraduatedMode.CONSTANT)
        if value is not None:
            self._jobject.setGraduatedMode(oj(value))
        return self

    def is_flow_enabled(self):
        """
        返回等级符号是否流动显示

        :return: 等级符号是否流动显示
        :rtype: bool
        """
        return self._jobject.isFlowEnabled()

    def set_flow_enabled(self, value):
        """
        设置等级符号是否流动显示。

        :param bool value: 等级符号是否流动显示。
        :return: self
        :rtype: ThemeGraduatedSymbol
        """
        self._jobject.setFlowEnabled(parse_bool(value))
        return self

    def get_positive_style(self):
        """
        返回正值的等级符号风格。

        :return: 正值的等级符号风格。
        :rtype: bool
        """
        return GeoStyle._from_java_object(self._jobject.getPositiveStyle())

    def set_positive_style(self, value):
        """
        设置正值的等级符号风格。

        :param GeoStyle value: 正值的等级符号风格。
        :return: self
        :rtype: ThemeGraduatedSymbol
        """
        if isinstance(value, GeoStyle):
            self._jobject.setPositiveStyle(oj(value))
        return self

    def get_leader_line_style(self):
        """
        返回等级符号及其相应对象之间的牵引线的风格。

        :return: 等级符号及其相应对象之间的牵引线的风格
        :rtype: GeoStyle
        """
        return GeoStyle._from_java_object(self._jobject.getLeaderLineStyle())

    def is_leader_line_displayed(self):
        """
        返回是否显示等级符号及其相应对象之间的牵引线。

        :return: 是否显示等级符号及其相应对象之间的牵引线
        :rtype: bool
        """
        return self._jobject.isLeadLineDisplayed()

    def set_leader_line(self, is_displayed, style):
        """
        设置显示等级符号及其相应对象之间的牵引线

        :param bool is_displayed: 是否显示 等级符号及其相应对象之间的牵引线的风格
        :param GeoStyle style:
        :return: self
        :rtype: ThemeGraduatedSymbol
        """
        self._jobject.setLeaderLineDisplayed(parse_bool(is_displayed))
        if isinstance(style, GeoStyle):
            self._jobject.setLeaderLineStyle(oj(style))
        return self

    def is_zero_displayed(self):
        """
        返回是否显示 0 值的等级符号风格，True 表示显示

        :return: 是否显示 0 值的等级符号风格
        :rtype: bool
        """
        return self._jobject.isZeroDisplayed()

    def get_zero_style(self):
        """
        返回 0 值的等级符号风格。

        :return: 0 值的等级符号风格
        :rtype: GeoStyle
        """
        return GeoStyle._from_java_object(self._jobject.getZeroStyle())

    def set_zero_displayed(self, is_displayed, style):
        """
        设置是否显示0值的等级符号风格。

        :param bool is_displayed: 是否显示0值的等级符号风格
        :param GeoStyle style: 0 值的等级符号风格
        :return: self
        :rtype: ThemeGraduatedSymbol
        """
        self._jobject.setZeroDisplayed(parse_bool(is_displayed))
        if isinstance(style, GeoStyle):
            self._jobject.setZeroStyle(oj(style))
        return self

    def is_negative_displayed(self):
        """
        返回是否显示负值的等级符号风格，true 表示显示

        :return: 是否显示负值的等级符号风格
        :rtype: bool
        """
        return self._jobject.isNegativeDisplayed()

    def get_negative_style(self):
        """
        返回负值的等级符号风格。

        :return: 负值的等级符号风格
        :rtype: GeoStyle
        """
        return GeoStyle._from_java_object(self._jobject.getNegativeStyle())

    def set_negative_displayed(self, is_displayed, style):
        """
        设置是否显示负值的等级符号风格，true 表示显示。

        :param bool is_displayed: 是否显示负值的等级符号风格
        :param GeoStyle style:  负值的等级符号风格
        :return: self
        :rtype: ThemeGraduatedSymbol
        """
        self._jobject.setNegativeDisplayed(parse_bool(is_displayed))
        if isinstance(style, GeoStyle):
            self._jobject.setNegativeStyle(oj(style))
        return self

    def get_offset_x(self):
        """
        获取等级符号 X 坐标方向（横向）偏移量

        :return: 等级符号 X 坐标方向（横向）偏移量
        :rtype: str
        """
        return self._jobject.getOffsetX()

    def set_offset_x(self, value):
        """
        设置等级符号 X 坐标方向（横向）偏移量

        :param str value: 等级符号 X 坐标方向（横向）偏移量
        :return: self
        :rtype: ThemeGraduatedSymbol
        """
        if value is not None:
            self._jobject.setOffsetX(str(value))
        return self

    def get_offset_y(self):
        """
        获取等级符号 Y 坐标方向（纵向）偏移量

        :return: 等级符号 Y 坐标方向（纵向）偏移量
        :rtype: str
        """
        return self._jobject.getOffsetY()

    def set_offset_y(self, value):
        """
        设置等级符号 Y 坐标方向（纵向）偏移量

        :param str value: 等级符号 Y 坐标方向（纵向）偏移量
        :return: self
        :rtype: ThemeGraduatedSymbol
        """
        if value is not None:
            self._jobject.setOffsetY(str(value))
        return self

    def set_offset_prj_coordinate_unit(self, value):
        """
        设置水平或垂直偏移量的单位是否是地理坐标系单位。如果为 True 则是地理坐标单位，否则采用设备单位。具体查看 :py:meth:`set_offset_x` 和 :py:meth:`set_offset_y` 接口。

        :param bool value: 水平或垂直偏移量的单位是否是地理坐标系单位
        :return: self
        :rtype: ThemeGraduatedSymbol
        """
        self._jobject.setOffsetFixed(not parse_bool(value))
        return self

    def is_offset_prj_coordinate_unit(self):
        """
        获取水平或垂直偏移量的单位是否是地理坐标系单位

        :return: 水平或垂直偏移量的单位是否是地理坐标系单位。如果为 True 则是地理坐标单位，否则采用设备单位。
        :rtype: bool
        """
        return not self._jobject.isOffsetFixed()


class ThemeDotDensity(Theme):
    __doc__ = "\n    点密度专题图类。\n\n    SuperMap iObjects 的点密度专题图用一定大小、形状相同的点表示现象分布范围、数量特征和分布密度。 点的多少和所代表的意义由地图的内容确定。\n\n    以下代码示范了如何制作点密度专题图::\n\n    >>> ds = open_datasource('/home/data/data.udb')\n    >>> dt = ds['world']\n    >>> mmap = Map()\n    >>> theme = ThemeDotDensity('Pop_1994', 10000000.0)\n    >>> mmap.add_dataset(dt, True, theme)\n    >>> mmap.set_image_size(2000, 2000)\n    >>> mmap.view_entire()\n    >>> mmap.output_to_file('/home/data/mapping/dotdensity_theme.png')\n    "

    def __init__(self, expression=None, value=None, style=None):
        """
        :param str expression: 用于创建点密度专题图的字段或字段表达式。
        :param float value: 专题图中每一个点所代表的数值。点值的确定与地图比例尺以及点的大小有关。 地图比例尺越大，相应的图面范围也越大，点相应
                            就可以越多，此时点值就可以设置相对小一些。 点形状越大，点值相应就应该设置的小一些。点值过大或过小都是不合适的。
        :param GeoStyle style: 点密度专题图中点的风格
        """
        Theme.__init__(self)
        self._type = ThemeType.DOTDENSITY
        self.set_expression(expression).set_style(style).set_value(value)

    def _make_java_object(self):
        return self._jvm.com.supermap.mapping.ThemeDotDensity()

    def set_value(self, value):
        """
        设置专题图中每一个点所代表的数值。

        点值的确定与地图比例尺以及点的大小有关。 地图比例尺越大，相应的图面范围也越大，点相应就可以越多，此时点值就可以设置相对小一些。 点形状越大，
        点值相应就应该设置的小一些。点值过大或过小都是不合适的。

        :param float value: 专题图中每一个点所代表的数值。
        :return: self
        :rtype: ThemeDotDensity
        """
        if value is not None:
            self._jobject.setValue(float(value))
        return self

    @property
    def value(self):
        """float: 专题图中每一个点所代表的数值"""
        return self._jobject.getValue()

    def set_expression(self, expression):
        """
        设置用于创建点密度专题图的字段或字段表达式。

        :param str expression: 用于创建点密度专题图的字段或字段表达式
        :return: self
        :rtype: ThemeDotDensity
        """
        if expression:
            self._jobject.setDotExpression(str(expression))
        return self

    @property
    def expression(self):
        """str: 用于创建点密度专题图的字段或字段表达式。"""
        return self._jobject.getDotExpression()

    def set_style(self, style):
        """
        设置点密度专题图中点的风格。

        :param GeoStyle style: 点密度专题图中点的风格
        :return: self
        :rtype: ThemeDotDensity
        """
        if isinstance(style, GeoStyle):
            self._jobject.setStyle(oj(style))
        return self

    @property
    def style(self):
        """GeoStyle: 点密度专题图中点的风格"""
        return GeoStyle._from_java_object(self._jobject.getStyle())


class ThemeGridUniqueItem:
    __doc__ = "\n    栅格单值专题图子项类。\n    "

    def __init__(self, unique_value, color, caption, visible=True):
        """
        :param str unique_value: 栅格单值专题图子项的单值
        :param Color color: 栅格单值专题图子项的显示颜色
        :param str caption: 栅格单值专题图子项的名称
        :param bool visible: 栅格单值专题图子项是否可见
        """
        self._unique_value = ""
        self._caption = ""
        self._color = None
        self._visible = True
        self.set_unique_value(unique_value).set_color(color).set_caption(caption).set_visible(visible)

    @property
    def unique_value(self):
        """str: 栅格单值专题图子项的单值"""
        return self._unique_value

    def set_unique_value(self, value):
        """
        设置栅格单值专题图子项的单值

        :param str value: 栅格单值专题图子项的单值
        :return: self
        :rtype: ThemeGridUniqueItem
        """
        self._unique_value = float(value) if value else ""
        return self

    @property
    def color(self):
        """Color: 栅格单值专题图子项的显示颜色"""
        return self._color

    def set_color(self, value):
        """
        设置每个栅格单值专题图子项的显示颜色。

        :param value: 栅格单值专题图子项的显示颜色。
        :type value: Color or str
        :return: self
        :rtype: ThemeGridUniqueItem
        """
        value = Color.make(value)
        if isinstance(value, Color):
            self._color = value
        return self

    @property
    def caption(self):
        """str: 栅格单值专题图子项的名称"""
        return self._caption

    def set_caption(self, value):
        """
        设置每个栅格单值专题图子项的名称

        :param str value: 每个栅格单值专题图子项的名称
        :return: self
        :rtype: ThemeGridUniqueItem
        """
        self._caption = str(value) if value else None
        return self

    @property
    def visible(self):
        """bool: 栅格单值专题图子项是否可见"""
        return self._visible

    def set_visible(self, value):
        """
        设置栅格单值专题图子项是否可见

        :param bool value: 栅格单值专题图子项是否可见
        :return: self
        :rtype: ThemeGridUniqueItem
        """
        self._visible = parse_bool(value)
        return self

    @property
    def _jobject(self):
        java_object = get_jvm().com.supermap.mapping.ThemeGridUniqueItem()
        java_object.setUnique(float(self.unique_value))
        if self.color is not None:
            java_object.setColor(to_java_color(self.color))
        if self.caption is not None:
            java_object.setCaption(self.caption)
        java_object.setVisible(parse_bool(self.visible))
        return java_object

    @staticmethod
    def _from_java_object(java_object):
        if not java_object:
            return
        return ThemeGridUniqueItem(java_object.getUnique(), Color._from_java_object(java_object.getColor()), java_object.getCaption(), java_object.isVisible())


class ThemeGridUnique(Theme):
    __doc__ = "\n    栅格单值专题图类。\n\n    栅格单值专题图，是将单元格值相同的归为一类，为每一类设定一种颜色，从而用来区分不同的类别。栅格单值专题图适用于离散栅格数据和部分连续栅格数据，对于\n    单元格值各不相同的那些连续栅格数据，使用栅格单值专题图不具有任何意义。\n\n    例如，可以通过以下方式创建栅格专题图对象::\n\n    >>> theme = ThemeGridUnique.make_default(dataset, 'RAINBOW')\n\n    或者::\n\n    >>> theme = ThemeGridUnique()\n    >>> theme.add(ThemeGridUniqueItem(1, Color.rosybrown(), '1'))\n    >>> theme.add(ThemeGridUniqueItem(2, Color.coral(), '2'))\n    >>> theme.add(ThemeGridUniqueItem(3, Color.darkred(), '3'))\n    >>> theme.add(ThemeGridUniqueItem(4, Color.blueviolet(), '4'))\n    >>> theme.add(ThemeGridUniqueItem(5, Color.greenyellow(), '5'))\n    >>> theme.set_default_color(Color.white())\n    "

    def __init__(self, items=None):
        """
        :param items: 栅格单值专题图子项列表
        :type items: list[ThemeGridUniqueItem] or tuple[ThemeGridUniqueItem]
        """
        Theme.__init__(self)
        self._type = ThemeType.GRIDUNIQUE
        self.extend(items)

    @staticmethod
    def make_default(dataset, color_gradient_type=None):
        """
        根据给定的栅格数据集和颜色渐变模式生成默认的栅格单值专题图。
        只支持对栅格值为整型的栅格数据集制作单值专题图，对于栅格值为浮点型的栅格数据集不能制作栅格单值专题图。

        :param dataset: 栅格数据集
        :type dataset: DatasetGrid or str
        :param color_gradient_type: 颜色渐变模式
        :type color_gradient_type: ColorGradientType or str
        :return: 新的栅格单值专题图类的对象实例
        :rtype: ThemeGridUnique
        """
        dataset = get_input_dataset(dataset)
        if not isinstance(dataset, DatasetGrid):
            raise ValueError("failed get DatasetGrid")
        color_gradient_type = ColorGradientType._make(color_gradient_type)
        java_theme = get_jvm().com.supermap.mapping.ThemeGridUnique.makeDefault(oj(dataset), oj(color_gradient_type))
        return Theme._from_java_object(java_theme)

    def _make_java_object(self):
        return self._jvm.com.supermap.mapping.ThemeGridUnique()

    def extend(self, items):
        """
        批量添加栅格单值专题图子项

        :param items: 栅格单值专题图子项列表
        :type items: list[ThemeGridUniqueItem] or tuple[ThemeGridUniqueItem]
        :return: self
        :rtype: ThemeGridUnique
        """
        if isinstance(items, ThemeGridUniqueItem):
            items = [
             items]
        if isinstance(items, (list, tuple)):
            r_items = list(items)
            r_items.reverse()
            for item in r_items:
                self.add(item)

    def add(self, item):
        """
        添加栅格单值专题图子项

        :param ThemeGridUniqueItem item: 栅格单值专题图子项
        :return: self
        :rtype: ThemeGridUnique
        """
        if isinstance(item, ThemeGridUniqueItem):
            self._jobject.add(oj(item))
        return self

    def clear(self):
        """
        删除所有栅格单值专题图子项。

        :return: self
        :rtype: ThemeGridUnique
        """
        self._jobject.clear()
        return self

    def get_count(self):
        """
        返回栅格单值专题图子项个数

        :return: 栅格单值专题图子项个数
        :rtype: int
        """
        return self._jobject.getCount()

    def __getitem__(self, index):
        return self.get_item(index)

    def get_item(self, index):
        """
        返回指定序号的栅格单值专题图子项

        :param int index: 指定的栅格单值专题图子项的序号
        :return: 指定序号的栅格单值专题图子项
        :rtype: ThemeGridUniqueItem
        """
        if index < 0:
            index = index + self._jobject.getCount()
        return ThemeGridUniqueItem._from_java_object(self._jobject.getItem(int(index)))

    def index_of(self, unique_value):
        """
        返回栅格单值专题图中指定子项单值在当前序列中的序号。

        :param int unique_value: 给定的栅格单值专题图子项的单值
        :return: 栅格专题图子项在序列中的序号值。如果该值不存在，就返回 -1。
        :rtype: int
        """
        return self._jobject.indexOf(str(unique_value) if unique_value else "")

    def remove(self, index):
        """
        删除一个指定序号的栅格单值专题图子项。

        :param int index: 指定的将被删除的栅格单值专题图子项序列的序号。
        :return: 删除成功，返回 True；否则返回 False。
        :rtype: bool
        """
        if index < 0:
            index = index + self._jobject.getCount()
        return self._jobject.remove(int(index))

    def insert(self, index, item):
        """
        将给定的栅格单值专题图子项插入到指定序号的位置。

        :param int index: 指定的栅格单值专题图子项序列的序号。
        :param ThemeGridUniqueItem item: 插入的栅格单值专题图子项。
        :return: self
        :rtype: ThemeGridUnique
        """
        if index < 0:
            index = index + self._jobject.getCount()
        if isinstance(item, ThemeGridUniqueItem):
            return self._jobject.insert(int(index), oj(item))
        return False

    def reverse_color(self):
        """
        对栅格单值专题图中子项的颜色进行反序显示。

        :return: self
        :rtype: ThemeGridUnique
        """
        self._jobject.reverseColor()
        return self

    def set_default_color(self, color):
        """
        设置栅格单值专题图的默认颜色，对于那些未在栅格单值专题图子项之列的对象使用该颜色显示。如未设置，则使用图层默认的颜色显示。

        :param color: 栅格单值专题图的默认颜色
        :type color: Color or str
        :return: self
        :rtype: ThemeGridUnique
        """
        color = Color.make(color)
        if isinstance(color, Color):
            self._jobject.setDefaultColor(to_java_color(color))
        return self

    def get_default_color(self):
        """
        返回栅格单值专题图的默认颜色，对于那些未在栅格单值专题图子项之列的对象使用该颜色显示。如未设置，则使用图层默认的颜色显示。

        :return: 栅格单值专题图的默认颜色。
        :rtype: Color
        """
        return Color._from_java_object(self._jobject.getDefaultColor())

    def get_special_value(self):
        """
        返回栅格单值专题图层的特殊值。 在新增一个栅格图层时，该方法的返回值与数据集的 NoValue 属性值相等。

        :return: 栅格单值专题图层的特殊值。
        :rtype: float
        """
        return self._jobject.getSpecialValue()

    def get_special_value_color(self):
        """
        返回栅格单值专题图层特殊值的颜色

        :return: 栅格单值专题图层特殊值的颜色。
        :rtype: Color
        """
        return Color._from_java_object(self._jobject.getSpecialValueColor())

    def is_special_value_transparent(self):
        """
        栅格单值专题图层的特殊值所处区域是否透明。

        :return: 栅格单值专题图层的特殊值所处区域是否透明；True表示透明；False表示不透明。
        :rtype: bool
        """
        return self._jobject.isSpecialValueTransparent()

    def set_special_value(self, value, color, is_transparent=False):
        """
        设置栅格单值专题图层的特殊值。

        :param float value: 栅格单值专题图层的特殊值。
        :param color: 栅格单值专题图层特殊值的颜色。
        :type color: Color or str
        :param bool is_transparent: 栅格单值专题图层的特殊值所处区域是否透明。True表示透明；False表示不透明。
        :return: self
        :rtype: ThemeGridUnique
        """
        if value is not None:
            self._jobject.setSpecialValue(int(value))
        color = Color.make(color)
        if isinstance(color, Color):
            self._jobject.setSpecialValueColor(to_java_color(color))
        self._jobject.setSpecialValueTransparent(parse_bool(is_transparent))
        return self


class ThemeGridRangeItem:
    __doc__ = "\n    栅格分段专题图子项类。\n\n    在栅格分段专题图中，将分段字段的表达式的值按照某种分段模式被分成多个范围段。本类用来设置每个范围段的分段起始值、终止值、名称和颜色等。\n    每个分段所表示的范围为 [Start,End)。\n    "

    def __init__(self, start, end, color, caption, visible=True):
        """
        :param float start: 栅格分段专题图子项的起始值
        :param float end: 栅格分段专题图子项的终止值
        :param Color color: 栅格分段专题图中每一个分段专题图子项的对应的颜色。
        :param str caption: 栅格分段专题图中子项的名称
        :param bool visible: 栅格分段专题图中的子项是否可见
        """
        self._start = None
        self._end = None
        self._caption = ""
        self._color = None
        self._visible = True
        self.set_start(start).set_end(end).set_color(color).set_caption(caption).set_visible(visible)

    @property
    def start(self):
        """float: 栅格分段专题图子项的起始值"""
        return self._start

    def set_start(self, value):
        """
        设置栅格分段专题图子项的起始值。
        注意：如果该子项是分段中第一个子项，那么该起始值就是分段的最小值；如果子项的序号大于等于 1 的时候，该起始值必须与前一子项的终止值相同，否则
        系统会抛出异常。

        :param float value: 栅格分段专题图子项的起始值。
        :return: self
        :rtype: ThemeGridRangeItem
        """
        if value is not None:
            self._start = float(value)
        return self

    @property
    def end(self):
        """float: 栅格分段专题图子项的终止值"""
        return self._end

    def set_end(self, value):
        """
        设置栅格分段专题图子项的终止值。
        注意：如果该子项是分段中最后一个子项，那么该终止值就是分段的最大值；如果不是最后一项，该终止值必须与下一子项的起始值相同，否则系统抛出异常。

        :param float value: 栅格分段专题图子项的终止值。
        :return: self
        :rtype: ThemeGridRangeItem
        """
        if value is not None:
            self._end = float(value)
        return self

    @property
    def color(self):
        """Color: 栅格分段专题图中每一个分段专题图子项的对应的颜色。"""
        return self._color

    def set_color(self, value):
        """
        设置栅格分段专题图中每一个分段专题图子项的对应的颜色。

        :param value: 栅格分段专题图中每一个分段专题图子项的对应的颜色。
        :type value: Color or str
        :return: self
        :rtype: ThemeGridRangeItem
        """
        value = Color.make(value)
        if isinstance(value, Color):
            self._color = value
        return self

    @property
    def caption(self):
        """str: 栅格分段专题图中子项的名称"""
        return self._caption

    def set_caption(self, value):
        """
        设置栅格分段专题图中子项的名称。

        :param str value: 栅格分段专题图中子项的名称。
        :return: self
        :rtype: ThemeGridRangeItem
        """
        self._caption = str(value) if value else None
        return self

    @property
    def visible(self):
        """bool: 栅格分段专题图中的子项是否可见"""
        return self._visible

    def set_visible(self, value):
        """
        设置栅格分段专题图中的子项是否可见

        :param bool value: 栅格分段专题图中的子项是否可见
        :return: self
        :rtype: ThemeGridRangeItem
        """
        self._visible = parse_bool(value)
        return self

    @property
    def _jobject(self):
        java_object = get_jvm().com.supermap.mapping.ThemeGridRangeItem()
        if self.start is not None:
            java_object.setStart(float(self.start))
        if self.end is not None:
            java_object.setEnd(float(self.end))
        if self.color is not None:
            java_object.setColor(to_java_color(self.color))
        if self.caption is not None:
            java_object.setCaption(self.caption)
        java_object.setVisible(parse_bool(self.visible))
        return java_object

    @staticmethod
    def _from_java_object(java_object):
        if not java_object:
            return
        return ThemeGridRangeItem(java_object.getStart(), java_object.getEnd(), Color._from_java_object(java_object.getColor()), java_object.getCaption(), java_object.isVisible())


class ThemeGridRange(Theme):
    __doc__ = "\n    栅格分段专题图类。\n\n    栅格分段专题图，是将所有单元格的值按照某种分段方式分成多个范围段，值在同一个范围段中的单元格使用相同的颜色进行显示。栅格分段专题图一般用来反映连\n    续分布现象的数量或程度特征。比如某年的全国降水量分布图，将各气象站点的观测值经过内插之后生成的栅格数据进行分段显示。该类类似于分段专题图类，不同\n    点在于分段专题图的操作对象是矢量数据，而栅格分段专题图的操作对象是栅格数据。\n\n    例如，可以通过以下方式创建栅格专题图对象::\n\n    >>>theme = ThemeGridRange.make_default(dataset, 'EUQALINTERVAL', 6, 'RAINBOW')\n\n    或者::\n\n    >>> theme = ThemeGridRange()\n    >>> theme.add(ThemeGridRangeItem(-999, 3, 'rosybrown', '1'))\n    >>> theme.add(ThemeGridRangeItem(3, 6, 'darkred', '2'))\n    >>> theme.add(ThemeGridRangeItem(6, 9, 'cyan', '3'))\n    >>> theme.add(ThemeGridRangeItem(9, 20, 'blueviolet', '4'))\n    >>> theme.add(ThemeGridRangeItem(20, 52, 'darkkhaki', '5'))\n\n    "

    def __init__(self, items=None):
        """
        :param items: 栅格分段专题图子项列表
        :type items: list[ThemeGridRangeItem] or tuple[ThemeGridRangeItem]
        """
        Theme.__init__(self)
        self._type = ThemeType.GRIDRANGE
        self.extend(items)

    def _make_java_object(self):
        return self._jvm.com.supermap.mapping.ThemeGridRange()

    @staticmethod
    def make_default(dataset, range_mode, range_parameter, color_gradient_type=None):
        """
        根据给定的栅格数据集、分段模式和相应的分段参数生成默认的栅格分段专题图。

        :param dataset: 栅格数据集。
        :type dataset: DatasetGrid or str
        :param range_mode: 分段模式。只支持等距离分段法，平方根分段法，对数分段法，以及自定义距离法。
        :type range_mode: RangeMode or str
        :param float range_parameter: 分段参数。当分段模式为等距离分段法，平方根分段法，对数分段法其中一种时，该参数为分段个数；当分段模式为自定义距离时，该参数表示自定义距离。
        :param color_gradient_type: 颜色渐变模式。
        :type color_gradient_type: ColorGradientType or str
        :return: 新的栅格分段专题图对象。
        :rtype: ThemeGridRange
        """
        dataset = get_input_dataset(dataset)
        if not isinstance(dataset, DatasetGrid):
            raise ValueError("failed get DatasetGrid")
        range_mode = RangeMode._make(range_mode, "EUQALINTERVAL")
        color_gradient_type = ColorGradientType._make(color_gradient_type)
        if range_mode is RangeMode.STDDEVIATION:
            range_parameter = 0.0
        java_color_gradient_type = oj(color_gradient_type)
        java_theme = get_jvm().com.supermap.mapping.ThemeGridRange.makeDefault(oj(dataset), oj(range_mode), float(range_parameter), java_color_gradient_type)
        return Theme._from_java_object(java_theme)

    def extend(self, items, is_normalize=True):
        """
        批量添加栅格分段专题图子项列表。默认添加到末尾。

        :param items: 栅格分段专题图子项列表
        :type items: list[ThemeGridRangeItem] or tuple[ThemeGridRangeItem]
        :param bool is_normalize: 表示是否规整化，normalize 为 true时， item 值不合法，则进行规整，normalize 为 fasle时， item 值不合法则抛异常
        :return: self
        :rtype: ThemeGridRange
        """
        if isinstance(items, ThemeGridRangeItem):
            items = [
             items]
        if isinstance(items, (list, tuple)):
            r_items = list(items)
            r_items.reverse()
            for item in r_items:
                self.add(item, is_normalize)

    def add(self, item, is_normalize=True, is_add_to_head=False):
        """
        添加栅格分段专题图子项列表

        :param ThemeGridRangeItem item: 栅格分段专题图子项列表
        :param bool is_normalize: 表示是否规整化，normalize 为 true时， item 值不合法，则进行规整，normalize 为 fasle时， item 值不合法则抛异常
        :param bool is_add_to_head: 是否添加到分段列表的头部，如果为True则添加到头部，否则添加到尾部。
        :return: self
        :rtype: ThemeGridRange
        """
        if isinstance(item, ThemeGridRangeItem):
            if is_add_to_head:
                return self._jobject.addToHead(oj(item), parse_bool(is_normalize))
            return self._jobject.addToTail(oj(item), parse_bool(is_normalize))
        return False

    def clear(self):
        """
        删除栅格分段专题图的一个分段值。执行该方法后，所有的栅格分段专题图子项都被释放，不再可用。

        :return: self
        :rtype: ThemeGridRange
        """
        self._jobject.clear()
        return self

    def get_count(self):
        """
        返回栅格分段专题图中分段的个数

        :return: 栅格分段专题图中分段的个数
        :rtype: int
        """
        return self._jobject.getCount()

    def __getitem__(self, index):
        return self.get_item(index)

    def get_item(self, index):
        """
        返回指定序号的栅格分段专题图中分段专题图子项

        :param int index: 指定的栅格分段专题图子项序号。
        :return: 指定序号的栅格分段专题图中分段专题图子项。
        :rtype: ThemeGridRangeItem
        """
        if index < 0:
            index = index + self._jobject.getCount()
        return ThemeGridRangeItem._from_java_object(self._jobject.getItem(int(index)))

    def index_of(self, value):
        """
        返回栅格分段专题图中指定分段字段值在当前分段序列中的序号。

        :param str value:
        :return: 分段字段值在分段序列中的序号。如果给定的分段字段的值不存在与其对应的序号，就返回-1。
        :rtype: int
        """
        return self._jobject.indexOf(str(value) if value else "")

    def reverse_color(self):
        """
        对分段专题图中分段的风格进行反序显示。

        :return: self
        :rtype: ThemeGridRange
        """
        self._jobject.reverseColor()
        return self

    @property
    def range_mode(self):
        """RangeMode: 当前专题图的分段模式"""
        java_mode = self._jobject.getRangeMode()
        if java_mode:
            return RangeMode._make(java_mode.name())

    def get_special_value(self):
        """
        返回栅格分段专题图层的特殊值。

        :return: 栅格分段专题图层的特殊值。
        :rtype: float
        """
        return self._jobject.getSpecialValue()

    def get_special_value_color(self):
        """
        返回栅格分段专题图层特殊值的颜色

        :return: 栅格分段专题图层特殊值的颜色
        :rtype: Color
        """
        return Color._from_java_object(self._jobject.getSpecialValueColor())

    def is_special_value_transparent(self):
        """
        栅格分段专题图层的特殊值所处区域是否透明。

        :return: 栅格分段专题图层的特殊值所处区域是否透明；True表示透明；False表示不透明。
        :rtype: bool
        """
        return self._jobject.isSpecialValueTransparent()

    def set_special_value(self, value, color, is_transparent=False):
        """
        设置栅格分段专题图层的特殊值。

        :param float value: 栅格分段专题图层的特殊值。
        :param color:  栅格分段专题图层特殊值的颜色。
        :type color: Color or str
        :param bool is_transparent: 栅格分段专题图层的特殊值所处区域是否透明。True表示透明；False表示不透明。
        :return: self
        :rtype: ThemeRangeUnique
        """
        if value is not None:
            self._jobject.setSpecialValue(int(value))
        color = Color.make(color)
        if isinstance(color, Color):
            self._jobject.setSpecialValueColor(to_java_color(color))
        self._jobject.setSpecialValueTransparent(parse_bool(is_transparent))
        return self


class ThemeCustom(Theme):
    __doc__ = "\n    自定义专题图类，该类可以通过字段表达式来动态设置显示的风格。\n    "

    def __init__(self):
        Theme.__init__(self)
        self._type = ThemeType.CUSTOM

    def _make_java_object(self):
        return self._jvm.com.supermap.mapping.ThemeCustom()

    def get_fill_back_color_expression(self):
        """
        返回表示填充背景色的字段表达式。

        :return: 表示填充背景色的字段表达式。
        :rtype: str
        """
        return self._jobject.getFillBackColorExpression()

    def set_fill_back_color_expression(self, value):
        """
        设置表示填充背景色的字段表达式

        :param str value: 表示填充背景色的字段表达式。
        :return: self
        :rtype: ThemeCustom
        """
        if value is not None:
            self._jobject.setFillBackColorExpression(str(value))
        return self

    def get_fill_fore_color_expression(self):
        """
        返回表示填充颜色的字段表达式。

        :return: 表示填充颜色的字段表达式
        :rtype: str
        """
        return self._jobject.getFillForeColorExpression()

    def set_fill_fore_color_expression(self, value):
        """
        设置表示填充颜色的字段表达式

        :param str value: 表示填充颜色的字段表达式
        :return: self
        :rtype: ThemeCustom
        """
        if value is not None:
            self._jobject.setFillForeColorExpression(str(value))
        return self

    def get_fill_gradient_angle_expression(self):
        """
        返回表示填充角度的字段表达式

        :return:表示填充角度的字段表达式
        :rtype: str
        """
        return self._jobject.getFillGradientAngleExpression()

    def set_fill_gradient_angle_expression(self, value):
        """
        设置表示填充角度的字段表达式

        :param str value: 表示填充角度的字段表达式
        :return: self
        :rtype: ThemeCustom
        """
        if value is not None:
            self._jobject.setFillGradientAngleExpression(str(value))
        return self

    def get_fill_gradient_mode_expression(self):
        """
        返回表示填充渐变类型的字段表达式。

        :return: 表示填充渐变类型的字段表达式。
        :rtype: str
        """
        return self._jobject.getFillGradientModeExpression()

    def set_fill_gradient_mode_expression(self, value):
        """
        设置表示填充渐变类型的字段表达式。

        :param str value: 表示填充渐变类型的字段表达式。
        :return: self
        :rtype: ThemeCustom
        """
        if value is not None:
            self._jobject.setFillGradientModeExpression(str(value))
        return self

    def get_fill_gradient_offset_ratio_x_expression(self):
        """
        返回表示填充中心点 X 方向偏移量的字段表达式

        :return: 表示填充中心点 X 方向偏移量的字段表达式
        :rtype: str
        """
        return self._jobject.getFillGradientOffsetRatioXExpression()

    def set_fill_gradient_offset_ratio_x_expression(self, value):
        """
        设置表示填充中心点 X 方向偏移量的字段表达式

        :param str value: 表示填充中心点 X 方向偏移量的字段表达式
        :return: self
        :rtype: ThemeCustom
        """
        if value is not None:
            self._jobject.setFillGradientOffsetRatioXExpression(str(value))
        return self

    def get_fill_gradient_offset_ratio_y_expression(self):
        """
        返回表示填充中心点 Y 方向偏移量的字段表达式

        :return: 表示填充中心点 Y 方向偏移量的字段表达式
        :rtype: str
        """
        return self._jobject.getFillGradientOffsetRatioYExpression()

    def set_fill_gradient_offset_ratio_y_expression(self, value):
        """
        设置表示填充中心点 Y 方向偏移量的字段表达式

        :param str value: 表示填充中心点 Y 方向偏移量的字段表达式
        :return: self
        :rtype: ThemeCustom
        """
        if value is not None:
            self._jobject.setFillGradientOffsetRatioYExpression(str(value))
        return self

    def get_fill_opaque_rate_expression(self):
        """
        返回表示填充不透明度的字段表达式

        :return: 表示填充不透明度的字段表达式
        :rtype: str
        """
        return self._jobject.getFillOpaqueRateExpression()

    def set_fill_opaque_rate_expression(self, value):
        """
        设置表示填充不透明度的字段表达式

        :param str value: 表示填充不透明度的字段表达式
        :return: self
        :rtype: ThemeCustom
        """
        if value is not None:
            return self._jobject.setFillOpaqueRateExpression(str(value))
        return self

    def get_fill_symbol_id_expression(self):
        """
        返回表示填充符号风格的字段表达式。

        :return: 表示填充符号风格的字段表达式。
        :rtype: str
        """
        return self._jobject.getFillSymbolIDExpression()

    def set_fill_symbol_id_expression(self, value):
        """
        设置表示填充符号风格的字段表达式。

        :param str value: 表示填充符号风格的字段表达式。
        :return: self
        :rtype: ThemeCustom
        """
        if value is not None:
            self._jobject.setFillSymbolIDExpression(str(value))
        return self

    def is_argb_color_mode(self):
        """
        返回颜色表达式中的颜色表示规则是否为RGB模式。默认值为 False。

        当返回值为true时，表示颜色表达式的值采用RRGGBB的方式来表达颜色。（RRGGBB为16进制的颜色转换为十进制的数值，一般通过将桌面颜色面板下的16
        进制值转为十进制数值获取。）

        当属性值为false时,表示颜色表达式的值采用BBGGRR的方式来表达颜色。（BBGGRR为16进制的颜色转换为十进制的数值，一般通过将桌面颜色面板，首先
        将目标颜色的R和B值互换，然后将获得的16进制值转为十进制数值即为目标颜色的BBGGRR十进制数值。）

        :return: 颜色表达式中的颜色表示规则是否为RGB模式
        :rtype: bool
        """
        return self._jobject.getIsColorModeARGB()

    def set_argb_color_mode(self, value):
        """
        设置颜色表达式中的颜色表示规则是否为RGB模式。默认值为 False。

        当返回值为true时，表示颜色表达式的值采用RRGGBB的方式来表达颜色。（RRGGBB为16进制的颜色转换为十进制的数值，一般通过将桌面颜色面板下的16
        进制值转为十进制数值获取。）

        当属性值为false时,表示颜色表达式的值采用BBGGRR的方式来表达颜色。（BBGGRR为16进制的颜色转换为十进制的数值，一般通过将桌面颜色面板，首先
        将目标颜色的R和B值互换，然后将获得的16进制值转为十进制数值即为目标颜色的BBGGRR十进制数值。）

        :param bool value: 颜色表达式中的颜色表示规则是否为RGB模式
        :return: self
        :rtype: ThemeCustom
        """
        self._jobject.setIsColorModeARGB(parse_bool(value))
        return self

    def get_line_color_expression(self):
        """

        :return:
        :rtype: str
        """
        return self._jobject.getLineColorExpression()

    def set_line_color_expression(self, value):
        """
        设置表示线型符号或是点符号的颜色的字段表达式

        :param str value: 表示线型符号或是点符号的颜色的字段表达式
        :return: self
        :rtype: ThemeCustom
        """
        if value is not None:
            self._jobject.setLineColorExpression(str(value))
        return self

    def get_line_symbol_id_expression(self):
        """
        获取表示线型符号或是点符号的颜色的字段表达式

        :return: 表示线型符号或是点符号的颜色的字段表达式
        :rtype: str
        """
        return self._jobject.getLineSymbolIDExpression()

    def set_line_symbol_id_expression(self, value):
        """
        设置表示线型符号风格的字段表达式

        :param str value: 表示线型符号风格的字段表达式
        :return: self
        :rtype: ThemeCustom
        """
        if value is not None:
            self._jobject.setLineSymbolIDExpression(str(value))
        return self

    def get_line_width_expression(self):
        """
        获取表示线型符号线宽的字段表达式

        :return: 表示线型符号线宽的字段表达式
        :rtype: str
        """
        return self._jobject.getLineWidthExpression()

    def set_line_width_expression(self, value):
        """
        设置表示线型符号线宽的字段表达式。

        :param str value: 表示线型符号线宽的字段表达式
        :return: self
        :rtype: ThemeCustom
        """
        if value is not None:
            self._jobject.setLineWidthExpression(str(value))
        return self

    def get_marker_angle_expression(self):
        """
        返回表示点符号旋转角度的字段表达式。旋转的方向为逆时针方向，单位为度

        :return: 表示点符号旋转角度的字段表达式
        :rtype: str
        """
        return self._jobject.getMarkerAngleExpression()

    def set_marker_angle_expression(self, value):
        """
        设置表示点符号旋转角度的字段表达式。旋转的方向为逆时针方向，单位为度

        :param str value: 表示点符号旋转角度的字段表达式。
        :return: self
        :rtype: ThemeCustom
        """
        if value is not None:
            self._jobject.setMarkerAngleExpression(str(value))
        return self

    def get_marker_size_expression(self):
        """
        返回表示点符号尺寸的字段表达式。单位为毫米

        :return: 表示点符号尺寸的字段表达式。
        :rtype: str
        """
        return self._jobject.getMarkerSizeExpression()

    def set_marker_size_expression(self, value):
        """
        设置表示点符号尺寸的字段表达式。单位为毫米。

        :param str value: 表示点符号尺寸的字段表达式。单位为毫米。
        :return: self
        :rtype: ThemeCustom
        """
        if value is not None:
            self._jobject.setMarkerSizeExpression(str(value))
        return self

    def get_marker_symbol_id_expression(self):
        """
        返回表示点符号风格的字段表达式。

        :return: 表示点符号风格的字段表达式。
        :rtype: str
        """
        return self._jobject.getMarkerSymbolIDExpression()

    def set_marker_symbol_id_expression(self, value):
        """
        设置表示点符号风格的字段表达式。

        :param str value: 表示点符号风格的字段表达式。
        :return: self
        :rtype: ThemeCustom
        """
        if value is not None:
            self._jobject.setMarkerSymbolIDExpression(str(value))
        return self

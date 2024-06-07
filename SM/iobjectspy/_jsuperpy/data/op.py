# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/_jsuperpy\data\op.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 67529 bytes
from .._gateway import get_jvm
from .._utils import *
from .._logger import *
from ..enums import *
from ._jvm import JVMBase
from .geo import *
from .prj import PrjCoordSys
from ._util import to_java_point2ds, java_point2ds_to_list
__all__ = ['GeometriesRelation', 'aggregate_points_geo', 'can_contain', 'has_area_intersection', 
 'has_cross', 
 'has_overlap', 'is_perpendicular', 
 'has_touch', 'has_common_point', 
 'has_common_line', 'has_hollow', 'is_disjointed', 'is_identical', 
 'is_within', 
 'is_left', 'is_right', 'is_on_same_side', 'is_parallel', 'is_point_on_line', 
 'has_intersection', 
 'is_project_on_line_segment', 'nearest_point_to_vertex', 
 'clip', 'erase', 'identity', 'intersect', 
 'intersect_line', 'intersect_polyline', 
 'union', 'update', 'xor', 'compute_concave_hull', 
 'compute_convex_hull', 
 'compute_geodesic_area', 'compute_geodesic_distance', 'compute_geodesic_line', 
 'compute_geodesic_line2', 
 'compute_parallel', 'compute_parallel2', 'compute_perpendicular', 
 'compute_perpendicular_position', 
 'compute_distance', 'point_to_segment_distance', 'resample', 'smooth', 
 'compute_default_tolerance', 
 'split_line', 'split_region', 'georegion_to_center_line', 
 'orthogonal_polygon_fitting']

class GeometriesRelation(JVMBase):
    __doc__ = "\n    几何对象关系判断类，区别与空间查询的是，此类用于几何对象的判断，而不是数据集，实现原理上与空间查询相同。\n\n    下面示例代码展示面查询点的功能，通过讲多个面对象（regions）插入到 GeometriesRelation 后，可以判断每个点对象被哪个面对象包含，\n    自然可以得到每个面对象包含的所有点对象，在需要处理大量的点对象时，此种方式具有比较好的性能::\n\n    >>> geos_relation = GeometriesRelation()\n    >>> for index in range(len(regions))\n    >>>     geos_relation.insert(regions[index], index)\n    >>> results = dict()\n    >>> for point in points:\n    >>>     region_values = geos_relation.matches(point, 'Contain')\n    >>>     for region_value in region_values:\n    >>>         region = regions[region_value]\n    >>>         if region in results:\n    >>>             results[region].append(point)\n    >>>         else:\n    >>>             results[region] = [point]\n    >>> del geos_relation\n    "

    def __init__(self, tolerance=1e-10, gridding_level='NONE'):
        """

        :param float tolerance: 节点容限
        :param gridding_level: 面对象格网化等级。
        :type gridding_level: GriddingLevel or str
        """
        JVMBase.__init__(self)
        self.set_tolerance(tolerance)
        self.set_gridding(gridding_level)

    def _make_java_object(self):
        self._java_object = self._jvm.com.supermap.data.GeometriesRelation()
        return self._java_object

    def get_bounds(self):
        """
        获取 GeometriesRelation 中所有插入的几何对象的地理范围

        :rtype: Rectangle
        """
        return Rectangle._from_java_object(self._jobject.getBounds())

    def set_tolerance(self, tolerance):
        """
        设置节点容限

        :param float tolerance: 节点容限
        :return: self
        :rtype: GeometriesRelation
        """
        if tolerance is not None:
            self._jobject.setTolerance(float(tolerance))
        return self

    def get_tolerance(self):
        """
        获取节点容限

        :rtype: float
        """
        return self._jobject.getTolerance()

    def get_gridding(self):
        """
        获取面对象格网化等级。默认不做面对象格网化

        :rtype: GriddingLevel
        """
        return GriddingLevel._make(self._jobject.getGridding().name())

    def set_gridding(self, gridding_level):
        """
        设置面对象格网化等级。默认不做面对象格网化。

        :param gridding_level: 格网化等级
        :type gridding_level: GriddingLevel or str
        :return: self
        :rtype: GeometriesRelation
        """
        if gridding_level is not None:
            gridding_level_ = GriddingLevel._make(gridding_level, "NONE")
            self._jobject.setGridding(gridding_level_._jobject)
        return self

    def get_sources_count(self):
        """
        获取 GeometriesRelation 中所有插入的几何对象数目

        :rtype: int
        """
        return self._jobject.getSourcesCount()

    def insert(self, data, value):
        """
        插入一个用于被匹配的几何对象，被匹配对象在空间查询模式中为查询对象，例如，要进行面包含点对象查询，需要插入面对象到
        GeometriesRelation 中，然后依次匹配得到与点对象满足包含关系的面对象。

        :param data: 被匹配的几何对象，必须是点线面，或点线面记录集或数据集
        :type data: Geometry or Point2D or Rectangle, Recordset, DatasetVector
        :param value: 被匹配的值，是一个唯一值，且必须大于等于0，比如几何对象的 ID 等。如果传入的是 Recordset 或 DatasetVector，
                      则 value 为有表示对象唯一整型值且值大于等于0的字段名称，如果为 None，则使用对象的 SmID 值。
        :type value: int
        :return: 插入成功返回 True，否则返回 False。
        :rtype: bool
        """
        from .dt import DatasetVector, Recordset
        if isinstance(data, (Point2D, Rectangle, Geometry)):
            if isinstance(data, Point2D):
                data = GeoPoint(data)
            else:
                if isinstance(data, Rectangle):
                    data = data.to_region()
            return self._jobject.insert(data._jobject, int(value))
        if isinstance(data, (Recordset, DatasetVector)):
            if isinstance(data, DatasetVector):
                if data.index_of_field(value) != -1 and data.get_field_info(value).type in (
                 FieldType.INT32, FieldType.INT16, FieldType.INT64):
                    field_name, fields = value, [value]
                else:
                    field_name, fields = None, list()
                rd = data.get_recordset(cursor_type="STATIC", fields=fields)
                get_jvm().com.supermap.jsuperpy.Utils.GeometriesRelation_InsertRecordset(self._jobject, rd._jobject, field_name)
                rd.close()
                del rd
            else:
                if data.index_of_field(value) != -1 and data.get_field_info(value).type in (
                 FieldType.INT32, FieldType.INT16, FieldType.INT64):
                    field_name = value
                else:
                    field_name = None
                get_jvm().com.supermap.jsuperpy.Utils.GeometriesRelation_InsertRecordset(self._jobject, data._jobject, field_name)
            return True
        log_warning("Failed to insert, geometry required Point2D, Rectangle and Geometry, but now is " + str(type(data)))
        return False

    def intersect_extents(self, rc):
        """
        返回与指定矩形范围相交的所有对象，即对象的矩形范围相交。

        :param rc: 指定的矩形范围
        :type rc: Rectangle
        :return:  与指定的矩形范围相交的对象的值
        :rtype: list[int]
        """
        rc = Rectangle.make(rc)
        if isinstance(rc, Rectangle):
            java_result = self._jobject.intersectExtents(rc._jobject)
            if java_result is not None:
                return list(java_result)
            return
        else:
            raise ValueError("rc required Rectangle, but now is " + str(type(rc)))

    def is_match(self, data, src_value, mode):
        """
        判断对象是否与指定对象满足空间关系

        :param data: 要进行匹配的对象
        :type data:  Geometry or Point2D or Rectangle
        :param src_value:  被匹配对象的值
        :type src_value: int
        :param mode: 匹配的空间查询模式
        :type mode: SpatialQueryMode or str
        :return: 如果指定对象与指定对象满足空间关系返回 True，否则为 False。
        :rtype: bool
        """
        spatial_mode = SpatialQueryMode._make(mode)
        if spatial_mode is None:
            raise ValueError("invalid spatial query mode")
        if isinstance(data, (Point2D, Rectangle, Geometry)):
            if isinstance(data, Rectangle):
                data = data.to_region()
            return self._jobject.isMatch(data._jobject, int(src_value), spatial_mode._jobject)
        raise ValueError("data required Point2D, Rectangle and Geometry, but now is " + str(type(data)))

    def matches(self, data, mode, excludes=None):
        """
        找出与匹配对象满足空间关系的所有被匹配对象的值。

        :param data: 匹配空间对象
        :type data:  Geometry or Point2D or Rectangle
        :param mode: 匹配的空间查询模式
        :type mode:  SpatialQueryMode or str
        :param excludes:  排除的值，即不参与匹配运算
        :type excludes: list[int]
        :return: 被匹配对象的值
        :rtype: list[int]
        """
        spatial_mode = SpatialQueryMode._make(mode)
        if spatial_mode is None:
            raise ValueError("invalid spatial query mode")
        excludes = split_input_list_from_str(excludes)
        if excludes is not None:
            excludes = to_java_int_array(excludes)
        elif not isinstance(data, (Point2D, Rectangle, Geometry)):
            raise ValueError("data required Point2D, Rectangle and Geometry, but now is " + str(type(data)))
        if isinstance(data, Rectangle):
            data = data.to_region()
        if excludes is not None:
            java_result = self._jobject.matches(data._jobject, spatial_mode._jobject, excludes)
        else:
            java_result = self._jobject.matches(data._jobject, spatial_mode._jobject)
        if java_result is not None:
            return list(java_result)
        return


def aggregate_points_geo(points, min_pile_point_count, distance, unit='Meter', prj=None, as_region=False):
    """
    对点集合进行密度聚类。密度聚类算法介绍参考 :py:meth:`iobjectspy.aggregate_points`

    :param points: 输入的点集合
    :type points: list[Point2D] or tuple[Point2D]
    :param int min_pile_point_count: 密度聚类点数目阈值，必须大于等于2。阈值越大表示能聚类为一簇的条件越苛刻。推荐值为4。
    :param float distance: 密度聚类半径。
    :param unit: 密度聚类半径的单位。如果空间参考坐标系prjCoordSys无效，此参数也无效
    :type unit: Unit or str
    :param prj:  点集合的空间参考坐标系
    :type prj: PrjCoordSys
    :param bool as_region: 是否返回聚类后的面对象
    :return: 当 as_region 为 False 时，返回一个list，list中每个值代表点对象的聚类类别，聚类类别从1开始，0表示为无效聚类。
             当 as_region 为 True 时，将返回每一簇点集聚集成的多边形对象
    :rtype: list[int] or list[GeoRegion]
    """
    prj = PrjCoordSys.make(prj)
    if prj is not None:
        java_prj = prj._jobject
    else:
        java_prj = None
    unit = Unit._make(unit, "Meter")
    if as_region:
        regions = get_jvm().com.supermap.data.Geometrist.aggregatePointsToRegions(to_java_point2ds(points), java_prj, float(distance), unit._jobject, int(min_pile_point_count))
        if regions is not None:
            return list((Geometry._from_java_object(geo) for geo in regions))
        return
    else:
        results = get_jvm().com.supermap.data.Geometrist.aggregatePoints(to_java_point2ds(points), java_prj, float(distance), unit._jobject, int(min_pile_point_count))
        return list(results)


def can_contain(geo_search, geo_target):
    """
    判断搜索几何对象是否包含被搜索几何对象。包含则返回 True。
    注意，如果存在包含关系，则：

        * 搜索几何对象的外部和被搜索几何对象的内部的交集为空；
        * 两个几何对象的内部交集不为空或者搜索几何对象的边界与被搜索几何对象的内部交集不为空；
        * 点查线，点查面，线查面，不存在包含情况；
        * 与 :py:meth:`is_within` 是逆运算；
        * 该关系适合的几何对象类型：

            * 搜索几何对象：点、线、面；
            * 被搜索几何对象：点、线、面。

    .. image:: ../image/Geometrist_CanContain.png

    :param Geometry geo_search: 搜索几何对象，支持点、线、面类型。
    :param Geometry geo_target: 被搜索几何对象，支持点、线、面类型。
    :return: 搜索几何对象包含被搜索几何对象返回 True；否则返回 False。
    :rtype: bool
    """
    if isinstance(geo_search, Point2D):
        geo_search = GeoPoint(geo_search)
    else:
        if isinstance(geo_search, Rectangle):
            geo_search = geo_search.to_region()
        elif isinstance(geo_target, Point2D):
            geo_target = GeoPoint(geo_target)
        else:
            if isinstance(geo_target, Rectangle):
                geo_target = geo_target.to_region()
        return get_jvm().com.supermap.data.Geometrist.canContain(geo_search._jobject, geo_target._jobject)


def has_intersection(geo_search, geo_target):
    """
    判断被搜索几何对象与搜索几何对象是否有面积相交。相交返回 true。
    注意：

    * 被搜索几何对象和搜索几何对象必须有一个为面对象；
    * 该关系适合的几何对象类型：

        * 搜索几何对象：点、线、面；
        * 被搜索几何对象：点、线、面。

    .. image:: ../image/Geometrist_HasIntersection.png

    :param Geometry geo_search: 查询对象
    :param Geometry geo_target: 目标对象
    :return: 两对象面积相交返回 True，否则为 False
    :rtype: bool
    """
    if isinstance(geo_search, Point2D):
        geo_search = GeoPoint(geo_search)
    else:
        if isinstance(geo_search, Rectangle):
            geo_search = geo_search.to_region()
        elif isinstance(geo_target, Point2D):
            geo_target = GeoPoint(geo_target)
        else:
            if isinstance(geo_target, Rectangle):
                geo_target = geo_target.to_region()
        return get_jvm().com.supermap.data.Geometrist.hasIntersection(geo_search._jobject, geo_target._jobject)


def has_area_intersection(geo_search, geo_target, tolerance=None):
    """
    判断对象是否面积相交，查询对象和目标对象至少有一个对象是面对象，相交的结果不包括仅接触的情形。支持点、线、面和文本对象。

    :param Geometry geo_search: 查询对象
    :param Geometry geo_target: 目标对象
    :param float tolerance: 节点容限
    :return: 两对象面积相交返回 True，否则为 False
    :rtype: bool
    """
    if isinstance(geo_search, Point2D):
        geo_search = GeoPoint(geo_search)
    else:
        if isinstance(geo_search, Rectangle):
            geo_search = geo_search.to_region()
        else:
            if isinstance(geo_target, Point2D):
                geo_target = GeoPoint(geo_target)
            else:
                if isinstance(geo_target, Rectangle):
                    geo_target = geo_target.to_region()
            if tolerance is not None:
                tolerance = float(tolerance)
            else:
                tolerance = 1e-10
        return get_jvm().com.supermap.data.Geometrist.hasAreaIntersection(geo_search._jobject, geo_target._jobject, tolerance)


def has_cross(geo_search, geo_target):
    """
    判断搜索几何对象是否穿越被搜索几何对象。穿越则返回 True。
    注意，如果两个几何对象存在穿越关系则：

    * 搜索几何对象内部与被搜索几何对象的内部的交集不为空且搜索几何对象的内部与被搜索几何对象的外部的交集不为空。
    * 被搜索几何对象为线时，搜索几何对象内部与被搜索几何对象的内部的交集不为空但是边界交集为空；
    * 该关系适合的几何对象类型：

        * 搜索几何对象：线；
        * 被搜索几何对象：线、面。

    .. image:: ../image/Geometrist_HasCross.png

    :param GeoLine geo_search: 搜索几何对象，只支持线类型。
    :param geo_target: 被搜索几何对象，支持线、面类型。
    :type geo_target: GeoLine or GeoRegion or Rectangle
    :return: 搜索几何对象穿越被搜索对象返回 True；否则返回 False。
    :rtype: bool
    """
    if isinstance(geo_target, Rectangle):
        geo_target = geo_target.to_region()
    return get_jvm().com.supermap.data.Geometrist.hasCross(geo_search._jobject, geo_target._jobject)


def has_overlap(geo_search, geo_target):
    """
    判断被搜索几何对象是否与搜索几何对象部分重叠。有部分重叠则返回 true。
    注意：

    * 点与任何一种几何对象都不存在部分重叠的情况；
    * 被搜索几何对象与搜索几何对象的维数要求相同，即只可以是线查询线或者面查询面；
    * 该关系适合的几何对象类型：

        * 搜索几何对象：线、面；
        * 被搜索几何对象：线、面。

    .. image:: ../image/Geometrist_HasOverlap.png

    :param geo_search: 搜索几何对象，只支持线、面类型。
    :type geo_search: GeoLine or GeoRegion or Rectangle
    :param geo_target: 被搜索几何对象，只支持线、面类型
    :type geo_target: GeoLine or GeoRegion or Rectangle
    :return: 被搜索几何对象与搜索几何对象部分重叠返回 True；否则返回 False
    :rtype: bool
    """
    if isinstance(geo_search, Rectangle):
        geo_search = geo_search.to_region()
    if isinstance(geo_target, Rectangle):
        geo_target = geo_target.to_region()
    return get_jvm().com.supermap.data.Geometrist.hasOverlap(geo_search._jobject, geo_target._jobject)


def has_touch(geo_search, geo_target):
    """
    判断被搜索几何对象的边界是否与搜索几何对象的边界相触。相触时搜索几何对象和被搜索几何对象的内部交集为空。
    注意：

    * 点与点不存在边界接触的情况；
    * 该关系适合的几何对象类型：

        * 搜索几何对象：点、线、面；
        * 被搜索几何对象：点、线、面。

    .. image:: ../image/Geometrist_HasTouch.png

    :param geo_search: 搜索几何对象。
    :type geo_search: Geometry
    :param geo_target: 被搜索几何对象。
    :type geo_target: Geometry
    :return: 被搜索几何对象的边界与搜索几何对象边界相触返回 True；否则返回 False。
    :rtype: bool
    """
    if isinstance(geo_search, Point2D):
        geo_search = GeoPoint(geo_search)
    else:
        if isinstance(geo_search, Rectangle):
            geo_search = geo_search.to_region()
        elif isinstance(geo_target, Point2D):
            geo_target = GeoPoint(geo_target)
        else:
            if isinstance(geo_target, Rectangle):
                geo_target = geo_target.to_region()
        return get_jvm().com.supermap.data.Geometrist.hasTouch(geo_search._jobject, geo_target._jobject)


def has_common_point(geo_search, geo_target):
    """
    判断搜索几何对象是否与被搜索几何对象有共同节点。有共同节点返回 true。

    .. image:: ../image/Geometrist_HasCommonPoint.png

    :param geo_search: 搜索几何对象，支持点、线、面类型。
    :type geo_search: Geometry
    :param geo_target: 被搜索几何对象，支持点、线、面类型。
    :type geo_target: Geometry
    :return: 搜索几何对象与被搜索几何对象有共同节点返回 true；否则返回 false。
    :rtype: bool
    """
    if isinstance(geo_search, Point2D):
        geo_search = GeoPoint(geo_search)
    else:
        if isinstance(geo_search, Rectangle):
            geo_search = geo_search.to_region()
        elif isinstance(geo_target, Point2D):
            geo_target = GeoPoint(geo_target)
        else:
            if isinstance(geo_target, Rectangle):
                geo_target = geo_target.to_region()
        return get_jvm().com.supermap.data.Geometrist.hasCommonPoint(geo_search._jobject, geo_target._jobject)


def has_common_line(geo_search, geo_target):
    """
    判断搜索几何对象是否与被搜索几何对象有公共线段。有公共线段返回 True。

    .. image:: ../image/Geometrist_HasCommonLine.png

    :param geo_search: 搜索几何对象，只支持线、面类型。
    :type geo_search: GeoLine or GeoRegion
    :param geo_target: 被搜索几何对象，只支持线、面类型。
    :type geo_target:  GeoLine or GeoRegion
    :return: 搜索几何对象与被搜索几何对象有公共线段返回 True；否则返回 False。
    :rtype: bool
    """
    if isinstance(geo_search, Rectangle):
        geo_search = geo_search.to_region()
    if isinstance(geo_target, Rectangle):
        geo_target = geo_target.to_region()
    return get_jvm().com.supermap.data.Geometrist.hasCommonLine(geo_search._jobject, geo_target._jobject)


def has_hollow(geometry):
    """
    判断指定的面对象是否包含有洞类型的子对象

    :param geometry: 待判断的面对象，目前只支持二维面对象
    :type geometry: GeoRegion
    :return: 面对象是否含有洞类型的子对象，包含则返回 True，否则返回 False
    :rtype: bool
    """
    return get_jvm().com.supermap.data.Geometrist.hasHollow(geometry._jobject)


def is_disjointed(geo_search, geo_target):
    """
    判断被搜索几何对象是否与搜索几何对象分离。分离返回 true。
    注意：

    * 搜索几何对象和被搜索几何对象分离，即无任何交集；
    * 该关系适合的几何对象类型：

         * 搜索几何对象：点、线、面；
         * 被搜索几何对象：点、线、面。

    .. image:: ../image/Geometrist_IsDisjointed.png

    :param geo_search:  搜索几何对象，支持点、线、面类型。
    :type geo_search: Geometry
    :param geo_target: 被搜索几何对象，支持点、线、面类型。
    :type geo_target: Geometry
    :return: 两个几何对象分离返回 True；否则返回 False
    :rtype: bool
    """
    if isinstance(geo_search, Point2D):
        geo_search = GeoPoint(geo_search)
    else:
        if isinstance(geo_search, Rectangle):
            geo_search = geo_search.to_region()
        elif isinstance(geo_target, Point2D):
            geo_target = GeoPoint(geo_target)
        else:
            if isinstance(geo_target, Rectangle):
                geo_target = geo_target.to_region()
        return get_jvm().com.supermap.data.Geometrist.isDisjointed(geo_search._jobject, geo_target._jobject)


def is_identical(geo_search, geo_target, tolerance=None):
    """
    判断被搜索几何对象是否与搜索几何对象完全相等。即几何对象完全重合、对象节点数目相等，正序或逆序对应的坐标值相等。
    注意：

    * 被搜索几何对象与搜索几何对象的类型必须相同；
    * 该关系适合的几何对象类型：

         * 搜索几何对象：点、线、面；
         * 被搜索几何对象：点、线、面。

    .. image:: ../image/Geometrist_IsIdentical.png

    :param geo_search: 搜索几何对象，支持点、线、面类型
    :type geo_search: Geometry
    :param geo_target: 被搜索几何对象，支持点、线、面类型。
    :type geo_target: Geometry
    :param float tolerance: 节点容限
    :return: 两个对象完全相等返回 True；否则返回 False
    :rtype: bool
    """
    if isinstance(geo_search, Point2D):
        geo_search = GeoPoint(geo_search)
    else:
        if isinstance(geo_search, Rectangle):
            geo_search = geo_search.to_region()
        elif isinstance(geo_target, Point2D):
            geo_target = GeoPoint(geo_target)
        else:
            if isinstance(geo_target, Rectangle):
                geo_target = geo_target.to_region()
        if tolerance is not None:
            return get_jvm().com.supermap.data.Geometrist.isIdentical(geo_search._jobject, geo_target._jobject, float(tolerance))
        return get_jvm().com.supermap.data.Geometrist.isIdentical(geo_search._jobject, geo_target._jobject)


def is_within(geo_search, geo_target, tolerance=None):
    """
    判断搜索几何对象是否在被搜索几何对象内。如果在则返回 True。
    注意：

    * 线查询点，面查询线或面查询点都不存在 Within 情况；
    * 与 can_contain 是逆运算；
    *  该关系适合的几何对象类型：

        * 搜索几何对象：点、线、面；
        * 被搜索几何对象：点、线、面。

    .. image:: ../image/Geometrist_IsWithin.png

    :param geo_search:  搜索几何对象，支持点、线、面类型。
    :type geo_search: Geometry
    :param geo_target: 被搜索几何对象，支持点、线、面类型
    :type geo_target: Geometry
    :param float tolerance: 节点容限
    :return: 搜索几何对象在被搜索几何对象内返回 True；否则返回 False
    :rtype: bool
    """
    if isinstance(geo_search, Point2D):
        geo_search = GeoPoint(geo_search)
    else:
        if isinstance(geo_search, Rectangle):
            geo_search = geo_search.to_region()
        elif isinstance(geo_target, Point2D):
            geo_target = GeoPoint(geo_target)
        else:
            if isinstance(geo_target, Rectangle):
                geo_target = geo_target.to_region()
        if tolerance is not None:
            return get_jvm().com.supermap.data.Geometrist.isWithin(geo_search._jobject, geo_target._jobject, float(tolerance))
        return get_jvm().com.supermap.data.Geometrist.isWithin(geo_search._jobject, geo_target._jobject)


def is_left(point, start_point, end_point):
    """
    判断点是否在线的左侧。

    :param Point2D point: 指定的待判断的点
    :param Point2D start_point: 指定的直线上的一点
    :param Point2D end_point: 指定的直线上的另一点。
    :return: 如果点在线的左侧，返回 True，否则返回 False
    :rtype: bool
    """
    point = Point2D.make(point)
    start_point = Point2D.make(start_point)
    end_point = Point2D.make(end_point)
    return get_jvm().com.supermap.data.Geometrist.isLeft(point._jobject, start_point._jobject, end_point._jobject)


def is_right(point, start_point, end_point):
    """
    判断点是否在线的右侧。

    :param Point2D point: 指定的待判断的点
    :param Point2D start_point: 指定的直线上的一点
    :param Point2D end_point: 指定的直线上的另一点。
    :return: 如果点在线的右侧，返回 True，否则返回 False
    :rtype: bool
       """
    point = Point2D.make(point)
    start_point = Point2D.make(start_point)
    end_point = Point2D.make(end_point)
    return get_jvm().com.supermap.data.Geometrist.isRight(point._jobject, start_point._jobject, end_point._jobject)


def is_on_same_side(point1, point2, start_point, end_point):
    """
    判断两点是否在线的同一侧。

    :param Point2D point1: 指定的待判断的一个点
    :param Point2D point2: 指定的待判断的另一个点
    :param Point2D start_point: 指定的直线上的一点。
    :param Point2D end_point: 指定的直线上的另一点。
    :return: 如果点在线的同一侧，返回 True，否则返回 False
    :rtype: bool
    """
    point1 = Point2D.make(point1)
    point2 = Point2D.make(point2)
    start_point = Point2D.make(start_point)
    end_point = Point2D.make(end_point)
    return get_jvm().com.supermap.data.Geometrist.isOnSameSide(point1._jobject, point2._jobject, start_point._jobject, end_point._jobject)


def is_parallel(start_point1, end_point1, start_point2, end_point2):
    """
    判断两条线是否平行。

    :param Point2D start_point1: 第一条线的起点。
    :param Point2D end_point1: 第一条线的终点。
    :param Point2D start_point2:  第二条线的起点。
    :param Point2D end_point2:  第二条线的终点。
    :return: 平行返回 True；否则返回 False
    :rtype: bool
    """
    start_point1 = Point2D.make(start_point1)
    end_point1 = Point2D.make(end_point1)
    start_point2 = Point2D.make(start_point2)
    end_point2 = Point2D.make(end_point2)
    return get_jvm().com.supermap.data.Geometrist.isParallel(start_point1._jobject, end_point1._jobject, start_point2._jobject, end_point2._jobject)


def is_perpendicular(start_point1, end_point1, start_point2, end_point2):
    """
    判断两条直线是否垂直。

    :param Point2D start_point1: 第一条线的起点。
    :param Point2D end_point1: 第一条线的终点。
    :param Point2D start_point2:  第二条线的起点。
    :param Point2D end_point2:  第二条线的终点。
    :return: 垂直返回 True；否则返回 False。
    :rtype: bool
    """
    start_point1 = Point2D.make(start_point1)
    end_point1 = Point2D.make(end_point1)
    start_point2 = Point2D.make(start_point2)
    end_point2 = Point2D.make(end_point2)
    return get_jvm().com.supermap.data.Geometrist.isPerpendicular(start_point1._jobject, end_point1._jobject, start_point2._jobject, end_point2._jobject)


def is_point_on_line(point, start_point, end_point, is_extended=True):
    """
    判断已知点是否在已知线段（直线）上，点在线上返回 True， 否则返回 False。

    :param Point2D point: 已知点
    :param Point2D start_point: 已知线段的起点
    :param Point2D end_point:  已知线段的终点
    :param bool is_extended: 是否将线段进行延长计算，如果为 True，就按直线计算，否则按线段计算
    :return: 点在线上返回 True；否则返回 False
    :rtype: bool
    """
    point = Point2D.make(point)
    start_point = Point2D.make(start_point)
    end_point = Point2D.make(end_point)
    return get_jvm().com.supermap.data.Geometrist.isPointOnLine(point._jobject, start_point._jobject, end_point._jobject, bool(is_extended))


def is_project_on_line_segment(point, start_point, end_point):
    """
    判断已知点到已知线段的垂足是否在该线段上，如果在，返回 True， 否则返回 False。

    :param Point2D point: 已知点
    :param Point2D start_point: 已知线段的起点
    :param Point2D end_point:  已知线段的终点
    :return: 点与线段的垂足是否在线段上。如果在，返回 True，否则返回 False。
    :rtype: bool
    """
    point = Point2D.make(point)
    start_point = Point2D.make(start_point)
    end_point = Point2D.make(end_point)
    return get_jvm().com.supermap.data.Geometrist.isProjectOnLineSegment(point._jobject, start_point._jobject, end_point._jobject)


def nearest_point_to_vertex(vertex, geometry):
    """
    从几何对象上找一点与给定的点距离最近。

    :param vertex: 指定的点
    :type vertex: Point2D
    :param geometry: 指定的几何对象
    :type geometry: Rectangle or GeoLine or GeoRegion
    :return: 几何对象上与指定点距离最近的一点。
    :rtype: Point2D
    """
    vertex = Point2D.make(vertex)
    if geometry is None:
        raise ValueError("geometry is None")
    if isinstance(geometry, Rectangle):
        geometry = geometry.to_region().convert_to_line()
    else:
        if isinstance(geometry, GeoRegion):
            geometry = geometry.convert_to_line()
        else:
            assert isinstance(geometry, GeoLine), "geometry required Rectangle, GeoRegion or GeoLine, but now is " + str(type(geometry))
        return get_jvm().com.supermap.data.Geometrist.nearestPointToVertex(vertex._jobject, geometry._jobject)


def erase(geometry, erase_geometry):
    """
    在被操作对象上擦除掉与操作对象相重合的部分。
    注意：

    * 如果对象全部被擦除了，则返回 None；
    * 操作几何对象定义了擦除区域，凡是落在操作几何对象区域内的被操作几何对象都将被去除，而落在区域外的特征要素都将被输出为结果几何对象，与 Clip 运算相反；
    * 该操作适合的几何对象类型：

        * 操作几何对象：面；
        * 被操作几何对象：点、线、面。

    .. image:: ../image/Geometrist_Erase.png

    :param geometry:  被操作几何对象，支持点、线、面对象类型
    :type geometry: GeoPoint or GeoLine or GeoRegion
    :param erase_geometry: 操作几何对象，必须为面对象类型。
    :type erase_geometry: GeoRegion or Rectangle
    :return: 擦除操作后的几何对象。
    :rtype: Geometry
    """
    if isinstance(geometry, Rectangle):
        geometry = geometry.to_region()
    if isinstance(erase_geometry, Rectangle):
        erase_geometry = erase_geometry.to_region()
    return Geometry._from_java_object(get_jvm().com.supermap.data.Geometrist.erase(geometry._jobject, erase_geometry._jobject))


def clip(geometry, clip_geometry):
    """
    生成被操作对象经过操作对象裁剪后的几何对象。
    注意：

    * 被操作几何对象只有落在操作几何对象内的那部分才会被输出为结果几何对象；
    * clip 与 intersect 在空间处理上是一致的，不同在于对结果几何对象属性的处理，clip 分析只是用来做裁剪，结果几何对象只保留被操作几何对象的非系统字段，而 Intersect 求交分析的结果则可以根据字段设置情况来保留两个几何对象的字段。
    * 该操作适合的几何对象类型：

        * 操作几何对象：面；
        * 被操作几何对象：线、面。

    .. image:: ../image/Geometrist_Clip.png

    :param geometry:  被操作几何对象，支持线和面类型。
    :type geometry: GeoLine or GeoRegion
    :param clip_geometry: 操作几何对象，必须是面对象。
    :type clip_geometry:  GeoRegion or Rectangle
    :return: 裁剪结果对象
    :rtype: Geometry
    """
    if isinstance(geometry, Rectangle):
        geometry = geometry.to_region()
    if isinstance(clip_geometry, Rectangle):
        clip_geometry = clip_geometry.to_region()
    return Geometry._from_java_object(get_jvm().com.supermap.data.Geometrist.clip(geometry._jobject, clip_geometry._jobject))


def identity(geometry, identity_geometry):
    """
    对被操作对象进行同一操作。即操作执行后，被操作几何对象包含来自操作几何对象的几何形状。
    注意：

    * 同一运算就是操作几何对象与被操作几何对象先求交，然后求交结果再与被操作几何对象求并的运算。

        * 如果被操作几何对象为点类型，则结果几何对象为被操作几何对象；
        * 如果被操作几何对象为线类型，则结果几何对象为被操作几何对象，但是与操作几何对象相交的部分将被打断；
        * 如果被操作几何对象为面类型，则结果几何对象保留以被操作几何对象为控制边界之内的所有多边形，并且把与操作几何对象相交的地方分割成多个对象。

    * 该操作适合的几何对象类型：
        操作几何对象：面；
        被操作几何对象：点、线、面。

    .. image:: ../image/Geometrist_Identity.png

    :param geometry: 被操作几何对象，支持点、线、面对象。
    :type geometry: GeoPoint or GeoLine or GeoRegion
    :param identity_geometry: 操作几何对象，必须为面对象。
    :type identity_geometry: GeoRegion or Rectangle
    :return: 同一操作后的几何对象
    :rtype: Geometry
    """
    if isinstance(geometry, Rectangle):
        geometry = geometry.to_region()
    if isinstance(identity_geometry, Rectangle):
        identity_geometry = identity_geometry.to_region()
    return Geometry._from_java_object(get_jvm().com.supermap.data.Geometrist.identity(geometry._jobject, identity_geometry._jobject))


def intersect(geometry1, geometry2, tolerance=None):
    """
    对两个几何对象求交，返回两个几何对象的交集。目前仅支持线线求交、面面求交。
    目前仅支持面面求交和线线求交，如下图示所示：

    .. image:: ../image/Geometrist_Intersect.png

    注意，如果两对象有多个相离的公共部分，求交的结果将是一个复杂对象。

    :param geometry1: 进行求交运算的第一个几何对象，支持线、面类型。
    :type geometry1: GeoLine or GeoRegion
    :param geometry2:  进行求交运算的第二个几何对象，支持线、面类型。
    :type geometry2: GeoLine or GeoRegion
    :param tolerance: 节点容限，目前仅支持线线求交。
    :type tolerance: float
    :return: 求交操作后的几何对象。
    :rtype: Geometry
    """
    if isinstance(geometry1, Rectangle):
        geometry1 = geometry1.to_region()
    elif isinstance(geometry2, Rectangle):
        geometry2 = geometry2.to_region()
    elif geometry1 is None:
        raise ValueError("geometry1 is None")
    if geometry2 is None:
        raise ValueError("geometry2 is None")
    if tolerance is not None and geometry1.type == GeometryType.GEOLINE and geometry2.type == GeometryType.GEOLINE:
        return Geometry._from_java_object(get_jvm().com.supermap.data.Geometrist.intersect(geometry1._jobject, geometry2._jobject, float(tolerance)))
    return Geometry._from_java_object(get_jvm().com.supermap.data.Geometrist.intersect(geometry1._jobject, geometry2._jobject))


def intersect_line(start_point1, end_point1, start_point2, end_point2, is_extended):
    """
    返回两条线段（直线）的交点。

    :param Point2D start_point1:  第一条线的起点。
    :param Point2D end_point1: 第一条线的终点。
    :param Point2D start_point2: 第二条线的起点。
    :param Point2D end_point2: 第二条线的终点。
    :param bool is_extended: 是否将线段进行延长计算，如果为 True，就按直线计算，否则按线段计算。
    :return: 两条线段（直线）的交点。
    :rtype: Point2D
    """
    start_point1 = Point2D.make(start_point1)
    end_point1 = Point2D.make(end_point1)
    start_point2 = Point2D.make(start_point2)
    end_point2 = Point2D.make(end_point2)
    return Point2D._from_java_object(get_jvm().com.supermap.data.Geometrist.intersectLine(start_point1._jobject, end_point1._jobject, start_point2._jobject, end_point2._jobject, bool(is_extended)))


def intersect_polyline(points1, points2):
    """
    返回两条折线的交点。

    :param points1:  构成第一条折线的点串。
    :type points1: list[Point2D] or tuple[Point2D]
    :param points2: 构成第二条折线的点串。
    :type points2: list[Point2D] or tuple[Point2D]
    :return: 点串构成的折线的交点。
    :rtype: list[Point2D]
    """
    java_points1 = to_java_point2ds(points1)
    java_points2 = to_java_point2ds(points2)
    result_points = get_jvm().com.supermap.data.Geometrist.intersectPolyLine(java_points1, java_points2)
    if result_points is not None:
        return list((Point2D._from_java_object(pnt) for pnt in result_points))
    return


def union(geometry1, geometry2):
    """
    对两个对象进行合并操作。进行合并后，两个面对象在相交处被多边形分割。
    注意：

    * 进行求并运算的两个几何对象必须是同类型的，目前版本只支持面、线类型的合并。
    * 该操作适合的几何对象类型：

        * 操作几何对象：面、线；
        * 被操作几何对象：面、线。

    .. image:: ../image/Geometrist_Union.png

    :param geometry1:  被操作几何对象。
    :type geometry1: GeoLine or GeoRegion
    :param geometry2: 操作几何对象。
    :type geometry2: GeoLine or GeoRegion
    :return: 合并操作后的几何对象。只支持生成简单线对象。
    :rtype: Geometry
    """
    if isinstance(geometry1, Rectangle):
        geometry1 = geometry1.to_region()
    if isinstance(geometry2, Rectangle):
        geometry2 = geometry2.to_region()
    return Geometry._from_java_object(get_jvm().com.supermap.data.Geometrist.union(geometry1._jobject, geometry2._jobject))


def update(geometry, update_geometry):
    """
    对被操作对象进行更新操作。用操作几何对象替换与被操作几何对象的重合部分，是一个先擦除后粘贴的过程。操作对象和被操作对象必须都是面对象。

    .. image:: ../image/Geometrist_Update.png

    :param geometry: 被操作几何对象，即被更新的几何对象，必须为面对象。
    :type geometry: GeoRegion  or Rectangle
    :param update_geometry: 操作几何对象，用于进行更新运算的几何对象，必须为面对象。
    :type update_geometry:  GeoRegion  or Rectangle
    :return: 更新操作后的几何对象。
    :rtype: GeoRegion
    """
    if isinstance(geometry, Rectangle):
        geometry = geometry.to_region()
    if isinstance(update_geometry, Rectangle):
        update_geometry = update_geometry.to_region()
    return Geometry._from_java_object(get_jvm().com.supermap.data.Geometrist.update(geometry._jobject, update_geometry._jobject))


def xor(geometry1, geometry2):
    """
    对两个对象进行异或运算。即对于每一个被操作几何对象，去掉其与操作几何对象相交的部分，而保留剩下的部分。
    进行异或运算的两个几何对象必须是同类型的，只支持面面。

    .. image:: ../image/Geometrist_XOR.png

    :param geometry1:  被操作几何对象，只支持面类型。
    :type geometry1: GeoRegion  or Rectangle
    :param geometry2:  操作几何对象，只支持面类型。
    :type geometry2: GeoRegion or Rectangle
    :return: 进行异或运算的结果几何对象。
    :rtype: GeoRegion
    """
    if isinstance(geometry1, Rectangle):
        geometry1 = geometry1.to_region()
    if isinstance(geometry2, Rectangle):
        geometry2 = geometry2.to_region()
    return Geometry._from_java_object(get_jvm().com.supermap.data.Geometrist.union(geometry1._jobject, geometry2._jobject))


def compute_concave_hull(points, angle=45.0):
    """
    计算点集的凹闭包。

    :param points:  指定的点集。
    :type points: list[Point2D] or tuple[Point2D]
    :param angle: 凹包内最小角度。 推荐值为 45度到75度，角度越大，凹包会更解决凸包的形状，角度越小，产生的凹多边形相邻顶点之间的夹角可能比较尖锐。
    :type angle: float
    :return: 返回可以包含指定点集中所有点的凹多边形。
    :rtype: GeoRegion
    """
    return Geometry._from_java_object(get_jvm().com.supermap.data.Geometrist.computeConcaveHull(to_java_point2ds(points), float(angle)))


def compute_convex_hull(points):
    """
    计算几何对象的凸闭包，即最小外接多边形。返回一个简单凸多边形。

    :param points:  点集
    :type points: list[Point2D] or tuple[Point2D] or Geometry
    :return: 最小外接多边形。
    :rtype: GeoRegion
    """
    if isinstance(points, Geometry):
        return Geometry._from_java_object(get_jvm().com.supermap.data.Geometrist.computeConvexHull(points._jobject))
    return Geometry._from_java_object(get_jvm().com.supermap.data.Geometrist.computeConvexHull(to_java_point2ds(points)))


def compute_geodesic_area(geometry, prj):
    """
    计算经纬度面积。

    注意：

    * 使用该方法计算经纬度面积，在通过 prj 参数指定投影坐标系类型对象（PrjCoordSys）时，必须通过该对象的 set_type 方法设置投影坐
      标系类型为地理经纬坐标系（ PrjCoordSysType.PCS_EARTH_LONGITUDE_LATITUDE），否则计算结果错误。

    :param geometry: 指定的需要计算经纬度面积的面对象。
    :type geometry: GeoRegion
    :param prj: 指定的投影坐标系类型
    :type prj: PrjCoordSys
    :return: 经纬度面积
    :rtype: float
    """
    if isinstance(geometry, Rectangle):
        geometry = geometry.to_region()
    else:
        prj = PrjCoordSys.make(prj)
        if prj is not None:
            java_prj = prj._jobject
        else:
            java_prj = None
    return get_jvm().com.supermap.data.Geometrist.computeGeodesicArea(geometry._jobject, java_prj)


def compute_geodesic_distance(points, major_axis, flatten):
    """
    计算测地线的长度。
    曲面上两点之间的短程线称为测地线。球面上的测地线即是大圆。
    测地线又称“大地线”或“短程线”，是地球椭球面上两点间的最短曲线。在大地线上，各点的主曲率方向均与该点上曲面法线相合。它在圆球面上为
    大圆弧， 在平面上就是直线。在大地测量中，通常用大地线来代替法截线，作为研究和计算椭球面上各种问题。

    测地线是在一个曲面上，每一点处测地曲率均为零的曲线。

    :param points:  构成测地线的经纬度坐标点串。
    :type points: list[Point2D] or tuple[Point2D]
    :param major_axis: 测地线所在椭球体的长轴。
    :type major_axis: float
    :param flatten:  测地线所在椭球体的扁率。
    :type flatten: float
    :return: 测地线的长度。
    :rtype: float
    """
    return get_jvm().com.supermap.data.Geometrist.computeGeodesicDistance(to_java_point2ds(points), float(major_axis), float(flatten))


def compute_geodesic_line(start_point, end_point, prj, segment=18000):
    """
    根据指定起始终止点计算测地线，返回结果线对象。

    :param Point2D start_point: 输入的测地线起始点。
    :param Point2D end_point: 输入的测地线终止点。
    :param prj:  空间参考坐标系。
    :type prj: PrjCoordSys
    :param int segment: 用来拟合半圆的弧段个数
    :return: 构造测地线成功，返回测地线对象，否则返回 None
    :rtype: GeoLine
    """
    start_point = Point2D.make(start_point)
    end_point = Point2D.make(end_point)
    java_parameter = get_jvm().com.supermap.data.GeodesicLineParameter()
    prj = PrjCoordSys.make(prj)
    if prj is not None:
        java_parameter.setPrjCoordSys(prj._jobject)
    if segment is not None:
        java_parameter.setSemicircleSegment(int(segment))
    java_parameter.setLineType(get_jvm().com.supermap.data.GeodesicLineType.GEODESIC)
    return Geometry._from_java_object(get_jvm().com.supermap.data.Geometrist.computeGeodesicLine(start_point._jobject, end_point._jobject, java_parameter))


def compute_geodesic_line2(start_point, angle, distance, prj, segment=18000):
    """
    根据指定起始点、方位角度以及距离计算测地线，返回结果线对象。

    :param Point2D start_point:  输入的测地线起始点。
    :param float angle: 输入的测地线方位角。正负均可。
    :param float distance: 输入的测地线长度。单位为米。
    :param prj:  空间参考坐标系。
    :type prj: PrjCoordSys
    :param int segment: 用来拟合半圆的弧段个数
    :return: 构造测地线成功，返回测地线对象，否则返回 None
    :rtype: GeoLine
    """
    start_point = Point2D.make(start_point)
    java_parameter = get_jvm().com.supermap.data.GeodesicLineParameter()
    prj = PrjCoordSys.make(prj)
    if prj is not None:
        java_parameter.setPrjCoordSys(prj._jobject)
    if segment is not None:
        java_parameter.setSemicircleSegment(int(segment))
    java_parameter.setLineType(get_jvm().com.supermap.data.GeodesicLineType.GEODESIC)
    return Geometry._from_java_object(get_jvm().com.supermap.data.Geometrist.computeGeodesicLine(start_point._jobject, float(angle), float(distance), java_parameter))


def compute_parallel(geo_line, distance):
    """
    根据距离求已知折线的平行线，返回平行线。

    :param GeoLine geo_line: 已知折线对象。
    :param float distance: 所求平行线间的距离。
    :return: 平行线。
    :rtype: GeoLine
    """
    return Geometry._from_java_object(get_jvm().com.supermap.data.Geometrist.computeParallel(geo_line._jobject, float(distance)))


def compute_parallel2(point, start_point, end_point):
    """
    求经过指定点与已知直线平行的直线。

    :param Point2D point: 直线外的任意一点。
    :param Point2D start_point: 直线上的一点。
    :param Point2D end_point:  直线上的另一点。
    :return: 平行线
    :rtype: GeoLine
    """
    point = Point2D.make(point)
    start_point = Point2D.make(start_point)
    end_point = Point2D.make(end_point)
    return Geometry._from_java_object(get_jvm().com.supermap.data.Geometrist.computeParallel(point._jobject, start_point._jobject, end_point._jobject))


def compute_perpendicular(point, start_point, end_point):
    """
    计算已知点到已知线的垂线。

    :param Point2D point:  已知一点。
    :param Point2D start_point: 直线上的一点。
    :param Point2D end_point: 直线上的另一点。
    :return: 点到直线的垂线
    :rtype: GeoLine
    """
    point = Point2D.make(point)
    start_point = Point2D.make(start_point)
    end_point = Point2D.make(end_point)
    return Geometry._from_java_object(get_jvm().com.supermap.data.Geometrist.computePerpendicular(point._jobject, start_point._jobject, end_point._jobject))


def compute_perpendicular_position(point, start_point, end_point):
    """
    计算已知点到已知线的垂足。

    :param Point2D point: 已知一点。
    :param Point2D start_point: 直线上的一点。
    :param Point2D end_point: 直线上的另一点。
    :return: 点在直线上的垂足
    :rtype: GeoLine
    """
    point = Point2D.make(point)
    start_point = Point2D.make(start_point)
    end_point = Point2D.make(end_point)
    return Point2D._from_java_object(get_jvm().com.supermap.data.Geometrist.computePerpendicularPosition(point._jobject, start_point._jobject, end_point._jobject))


def compute_distance(geometry1, geometry2):
    """
    求两个几何对象之间的距离。
    注意：几何对象的类型只能是点、线和面。这里的距离指的是两个几何对象边线间最短距离。例如：点到线的最短距离就是点到该线的垂直距离。

    :param geometry1: 第一个几何对象
    :type geometry1: Geometry or Point2D or Rectangle
    :param geometry2: 第二个几何对象
    :type geometry2: Geometry or Point2D or Rectangle
    :return: 两个几何对象之间的距离
    :rtype: float
    """
    if geometry1 is None:
        raise ValueError("geometry1 is None")
    else:
        if geometry2 is None:
            raise ValueError("geometry2 is None")
        else:
            if isinstance(geometry1, Point2D):
                p1 = geometry1
            else:
                if isinstance(geometry1, GeoPoint):
                    p1 = geometry1.point
                else:
                    p1 = None
            if isinstance(geometry2, Point2D):
                p2 = geometry2
            else:
                if isinstance(geometry2, GeoPoint):
                    p2 = geometry2.point
                else:
                    p2 = None
        if p1 is not None and p2 is not None:
            return p1.distance_to(p2)
    if isinstance(geometry1, Point2D):
        geometry1 = GeoPoint(geometry1)
    else:
        if isinstance(geometry1, Rectangle):
            geometry1 = geometry1.to_region()
        elif isinstance(geometry2, Point2D):
            geometry2 = GeoPoint(geometry2)
        else:
            if isinstance(geometry2, Rectangle):
                geometry2 = geometry2.to_region()
        return get_jvm().com.supermap.data.Geometrist.distance(geometry1._jobject, geometry2._jobject)


def point_to_segment_distance(point, start_point, end_point):
    """
    计算已知点到已知线段的距离。

    :param Point2D point:  已知点。
    :param Point2D start_point: 已知线段的起点。
    :param Point2D end_point: 已知线段的终点。
    :return: 点到线段的距离。如果点到线段的垂足不在线段上，则返回点到线段较近的端点的距离。
    :rtype: float
    """
    point = Point2D.make(point)
    start_point = Point2D.make(start_point)
    end_point = Point2D.make(end_point)
    pnt, sp, ep = point, start_point, end_point
    if sp == ep:
        return compute_distance(pnt, sp)
    else:
        da2 = (sp.x - pnt.x) * (sp.x - pnt.x) + (sp.y - pnt.y) * (sp.y - pnt.y)
        db2 = (ep.x - pnt.x) * (ep.x - pnt.x) + (ep.y - pnt.y) * (ep.y - pnt.y)
        dc2 = (sp.x - ep.x) * (sp.x - ep.x) + (sp.y - ep.y) * (sp.y - ep.y)
        temp = (da2 + dc2 - db2) / (2 * dc2)
        if temp < 0:
            temp = 0.0
        else:
            if temp > 1.0:
                temp = 1.0
    x = (ep.x - sp.x) * temp + sp.x
    y = (ep.y - sp.y) * temp + sp.y
    import math
    return math.sqrt((x - pnt.x) * (x - pnt.x) + (y - pnt.y) * (y - pnt.y))


def resample(geometry, distance, resample_type='RTBEND'):
    """
    对几何对象进行重采样。
    对几何对象重采样是按照一定规则剔除一些节点，以达到对数据进行简化的目的（如下图所示），其结果可能由于使用不同的重采样方法而不同。
    SuperMap 提供两种方法对几何对象进行重采样，分别为光栏法和道格拉斯-普克法。有关这两种方法的详细介绍，请参见 :py:class:`VectorResampleType` 类。

    .. image:: ../image/VectorResample.png

    :param geometry: 指定的要进行重采样的几何对象。支持线对象和面对象。
    :type geometry: GeoLine or GeoRegion
    :param distance:  指定的重采样容限。
    :type distance: float
    :param resample_type: 指定的重采样方法。
    :type resample_type: VectorResampleType or str
    :return: 重采样后的几何对象。
    :rtype: GeoLine or GeoRegion
    """
    resample_type = VectorResampleType._make(resample_type, "RTBEND")
    java_resample_fun = get_jvm().com.supermap.data.Geometrist.resample
    if isinstance(geometry, Geometry):
        return Geometry._from_java_object(java_resample_fun(geometry._jobject, resample_type._jobject, float(distance)))
    raise ValueError("geometry required Geometry, but now is " + str(type(geometry)))


def smooth(points, smoothness):
    """
    对指定的点串对象进行光滑处理

    有关光滑的更多内容，可以参考 :py:meth:`jsupepry.analyst.smooth` 方法的介绍。

    :param points: 需要进行光滑处理的点串。
    :type points: list[Point2D] or tuple[Point2D] or GeoLine or GeoRegion
    :param smoothness: 光滑系数。有效范围为大于等于2，设置为小于2的值会抛出异常。光滑系数越大，线对象或面对象边界的节点数越多，也就越光滑。 建议取值范围为[2,10]。
    :type smoothness: int
    :return: 光滑处理结果点串。
    :rtype: list[Point2D] or GeoLine or GeoRegion
    """
    java_smooth_func = get_jvm().com.supermap.data.Geometrist.smooth
    if isinstance(points, GeoLine):
        parts = points.get_parts()
        result = GeoLine()
        for part in parts:
            java_points = to_java_point2ds(part)
            result_java_points = java_smooth_func(java_points, int(smoothness))
            if result_java_points is not None:
                result.add_part(java_point2ds_to_list(result_java_points))

        if result.get_part_count() > 0:
            return result
        del result
        return
    else:
        if isinstance(points, (GeoRegion, Rectangle)):
            if isinstance(points, Rectangle):
                points = points.to_region()
            parts = points.get_parts()
            result = GeoRegion()
            for part in parts:
                java_points = to_java_point2ds(part)
                result_java_points = java_smooth_func(java_points, int(smoothness))
                if result_java_points is not None:
                    result.add_part(java_point2ds_to_list(result_java_points))

            if result.get_part_count() > 0:
                return result
            del result
            return
        else:
            if isinstance(points, (list, tuple)):
                result_java_points = java_smooth_func(to_java_point2ds(points), int(smoothness))
                return java_point2ds_to_list(result_java_points)
            raise ValueError("points required list[Point2D], tuple[Point2D] or GeoLine or GeoRegion")


def compute_default_tolerance(prj):
    """
    计算坐标系默认容限。

    :param prj:  指定的投影坐标系类型对象。
    :type prj: PrjCoordSys
    :return: 返回指定的投影坐标系类型对象的默认容限值。
    :rtype: float
    """
    prj = PrjCoordSys.make(prj)
    if prj is None:
        raise ValueError("prj is None")
    return get_jvm().com.supermap.data.Geometrist.getTolerance(prj._jobject)


def split_line(source_line, split_geometry, tolerance=1e-10):
    """
    使用点、线或面对象对线对象进行分割（打断）。
    该方法可用于使用点、线、面对象对线对象进行打断或分割。下面以一个简单线对象对这三种情况进行说明:

    * 点对象打断线对象。使用点对象对线对象进行打断，原线对象在点对象位置打断为两个线对象。如下图所示，使用点（黑色）对线（蓝色）进行打断，结果为两个线对象（红色线和绿色线 ）。

    .. image:: ../image/PointSplitLine.png

    * 使用点、线或面对象对线对象进行分割（打断）。 该方法可用于使用点、线、面对象对线对象进行打断或分割。下面以一个简单线对象
      对这三种情况进行说明

      * 当分割线为线段时，操作线将会在其与分割线的交点处被分割为两个线对象。如下图所示，图中黑色线为分割线，分割后原线对象被分为两个线对象（红色线和绿色线 ）。

      .. image:: ../image/LineSplitLine_1.png

      * 当分割线为折线时，可能与操作线有多个交点，此时会在所有交点处将操作线打断，然后按顺序将位于奇数和偶数次序的线段分别合并，产生两个线对象。也就是说， 使用
        折线分割线时，可能会产生复杂线对象。下图展示的就是这种情况，分割后，红色的线和绿色的线分别为一个复杂线对象。

      .. image:: ../image/LineSplitLine_2.png

    * 面对象分割线对象。面对象分割线对象与线分割线类似，会在分割面和操作线的所有交点处将操作线打断，然后分别将位于奇数和偶数位置的线合并，产生两个线对象。
      这种情况会产生至少一个复杂线对象。下图中，面对象（浅橙色）将线对象分割为红色和绿色两个复杂线对象。

    .. image:: ../image/RegionSplitLine.png

    注意：

    1. 如果被分割的线对象为复杂对象，那么如果分割线经过子对象，则会将该子对象分割为两个线对象，因此，分割复杂线对象可能产生多个线对象。
    2. 用于分割的线对象或者面对象如果有自相交，分割不会失败，但分割的结果可能不正确。因此，应尽量使用没有自相交的线或面对象来分割线。

    :param source_line: 待分割（打断）的线对象
    :type source_line: GeoLine
    :param split_geometry: 用于分割（打断）线对象的对象，支持点、线、面对象。
    :type split_geometry: GeoPoint or GeoRegion or GeoLine or Rectangle or Point2D
    :param tolerance: 指定的容限，用于判断点对象是否在线上，若点到线的垂足距离大于该容限值，则认为用于打断的点对象无效，从而不执行打断。
    :type tolerance: float
    :return: 分割后的线对象数组。
    :rtype: list[GeoLine]
    """
    if isinstance(split_geometry, Point2D):
        split_geometry = GeoPoint(split_geometry)
    else:
        if isinstance(split_geometry, Rectangle):
            split_geometry = split_geometry.to_region()
    results = get_jvm().com.supermap.data.Geometrist.splitLine(source_line._jobject, split_geometry._jobject, float(tolerance))
    if results is not None:
        return list((Geometry._from_java_object(geo) for geo in results))
    return


def split_region(source_region, split_geometry):
    """
    用线或面几何对象分割面几何对象。
    注意：参数中的分割对象与被分割对象必须至少有两个交点，否则的话会分割失败。

    :param source_region: 被分割的面对象。
    :type source_region: GeoRegion or Rectangle
    :param split_geometry:  用于分割的几何对象，可以是线或面几何对象。
    :type split_geometry: GeoLine or GeoRegion or Rectangle
    :return:  返回分割后的面对象，正确分隔后会得到两个面对象。
    :rtype: tuple[GeoRegion]
    """
    if isinstance(source_region, Rectangle):
        source_region = source_region.to_region()
    if isinstance(split_geometry, Rectangle):
        split_geometry = split_geometry.to_region()
    result_geo1 = GeoRegion()
    result_geo2 = GeoRegion()
    split_result = get_jvm().com.supermap.data.Geometrist.splitRegion(source_region._jobject, split_geometry._jobject, result_geo1._jobject, result_geo2._jobject)
    if split_result:
        return (
         result_geo1, result_geo2)
    return


def georegion_to_center_line(source_region, pnt_from=None, pnt_to=None):
    """
    提取面对象的中心线，一般用于提取河流的中心线。
    该方法用于提取面对象的中心线。如果面包含岛洞，提取时会绕过岛洞，采用最短路径绕过。如下图。

    .. image:: ../image/RegionToCenterLine_1.png

    如果面对象不是简单的长条形，而是具有分叉结构，则提取的中心线是最长的一段。如下图所示。

    .. image:: ../image/RegionToCenterLine_2.png

    如果提取的不是期望的中心线，可以通过指定起点和终点，提取面对象的中心线，一般用于提取河流的中心线。尤其是河流干流的中心线，
    并且可以指定提取的起点和终点。如果面包含岛洞，提取时会绕过岛洞，采用的是最短路径绕过。如下图。

    .. image:: ../image/RegionToCenterLine_3.png

    pnt_from 参数和 pnt_to 参数所指定起点和终点，是作为提取的参考点，也就是说，系统提取的中心线可能不会严格从指定的起点出发，到指定的终点结束。系统一般会在指定的起点和终点的附近，找到一个较近的点作为提取的起点或终点。
    同时需要注意：

        * 如果将起点和终点指定为相同的点，即等同于不指定提取的起点和终点，则提取的是面对象的最长的一条中心线。
        * 如果指定的起点或终点在面对象的外面，则提取失败。

    :param GeoRegion source_region: 指定的待提取中心线的面对象。
    :param Point2D pnt_from: 指定的提取中心线的起点。
    :param Point2D pnt_to: 指定的提取中心线的终点。
    :return: 提取的中心线，是一个二维线对象
    :rtype: GeoLine
    """
    if not isinstance(source_region, GeoRegion):
        raise ValueError("source_region required GeoRegion, but now is " + str(type(source_region)))
    if pnt_from is not None:
        if pnt_to is not None:
            if isinstance(pnt_from, GeoPoint):
                pnt_from = pnt_from.point
            if isinstance(pnt_to, GeoPoint):
                pnt_to = pnt_to.point
            return Geometry._from_java_object(get_jvm().com.supermap.analyst.spatialanalyst.Generalization.regionToCenterLine(source_region._jobject, pnt_from._jobject, pnt_to._jobject))
    return Geometry._from_java_object(get_jvm().com.supermap.analyst.spatialanalyst.Generalization.regionToCenterLine(source_region._jobject))


def orthogonal_polygon_fitting(geometry, width_threshold, height_threshold):
    """
    面对象的直角多边形拟合
    如果一串连续的节点到最小面积外接矩形的下界的距离大于 height_threshold，
    且节点的总宽度大于 width_threshold，则对连续节点进行拟合。

    :param geometry: 待直角化的多边形对象，只能是简单面对象
    :type geometry: GeoRegion or Rectangle
    :param float width_threshold: 点到最小面积外接矩形的左右边界的阈值
    :param float height_threshold: 点到最小面积外接矩形的上下边界的阈值
    :return: 进行直角化的多边形对象，如果失败，返回 None
    :rtype: GeoRegion
    """
    if isinstance(geometry, Rectangle):
        geometry = geometry.to_region()
    elif not width_threshold > 0:
        raise ValueError("width_threshold must be greater than 0")
    if not height_threshold > 0:
        raise ValueError("height_threshold must be greater than 0")
    assert isinstance(geometry, GeoRegion), "geometry required GeoRegion, but now is " + str(type(geometry))
    result_geo = get_jvm().com.supermap.data.Geometrist.orthogonalPolygonFitting(oj(geometry), float(width_threshold), float(height_threshold))
    if result_geo is not None:
        return Geometry._from_java_object(result_geo)

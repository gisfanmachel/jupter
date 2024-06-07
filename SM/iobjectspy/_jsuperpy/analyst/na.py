# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/_jsuperpy\analyst\na.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 307681 bytes
"""
二维网络分析模块
"""
from enum import unique
import sys
from iobjectspy._jsuperpy._gateway import get_gateway, get_jvm, safe_start_callback_server, close_callback_server
from iobjectspy._jsuperpy.data import DatasetVector, Point2D, Geometry, Rectangle, GeoLine, PrjCoordSys
from iobjectspy._jsuperpy.data._listener import ProgressListener
from iobjectspy._jsuperpy.data._util import get_input_dataset, get_output_datasource, check_output_datasource, try_close_output_datasource, to_java_geometry_array, to_java_geoline_array, to_java_datasetvector_array, to_java_point2ds, java_point2ds_to_list
from iobjectspy._jsuperpy.enums import JEnum, DatasetType, FieldSign
from iobjectspy._jsuperpy._utils import to_java_int_array, to_java_double_array, datetime_to_java_date, to_java_string_array, split_input_int_list_from_str, split_input_list_from_str, oj, java_date_to_datetime, parse_bool, java_array_to_list, parse_datetime, split_input_float_list_from_str, to_java_array
from iobjectspy._jsuperpy._logger import log_error
from iobjectspy._jsuperpy.data._jvm import JVMBase
__all__ = [
 'WeightFieldInfo', 'PathAnalystSetting', 'SSCPathAnalystSetting', 'TransportationPathAnalystSetting', 
 'TransportationAnalystSetting', 
 'PathInfo', 'PathInfoItem', 'PathGuide', 'PathGuideItem', 'SSCPathAnalyst', 
 'SSCCompilerParameter', 
 'TrackPoint', 
 'TrajectoryPreprocessing', 'TransportationAnalystParameter', 'TransportationAnalyst', 
 'TransportationAnalystResult', 
 'MapMatching', 'MapMatchingResult', 'MapMatchingLikelyResult', 
 'TrajectoryPreprocessingResult', 
 'split_track', 'build_facility_network_directions', 
 'build_network_dataset', 
 'fix_ring_edge_network_errors', 'build_facility_network_hierarchies', 
 'build_network_dataset_known_relation', 
 'append_to_network_dataset', 
 'validate_network_dataset', 'compile_ssc_data', 
 'AllocationDemandType', 
 'AllocationAnalystResult', 'BurstAnalystResult', 'DemandPointInfo', 
 'DirectionType', 
 'VRPAnalystType', 'VRPDirectionType', 'VRPAnalystParameter', 'VRPAnalystResult', 
 'FacilityAnalyst', 
 'TerminalPoint', 'FacilityAnalystResult', 'FacilityAnalystSetting', 'SideType', 
 'TurnType', 
 'ServiceAreaType', 'VehicleInfo', 'NetworkDatasetErrors', 'GroupAnalystResult', 
 'GroupAnalystResultItem', 
 'SupplyCenterType', 'SupplyCenter', 'SupplyResult', 'DemandResult', 
 'LocationAnalystResult', 
 'RouteType', 'NetworkSplitMode']

@unique
class NetworkSplitMode(JEnum):
    __doc__ = "\n    构建网络数据集打断模式。用来控制建立网络数据集时，处理线线打断或点线打断的模式\n\n    :var NetworkSplitMode.NO_SPLIT: 不打断\n    :var NetworkSplitMode.LINE_SPLIT_BY_POINT: 点打断线\n    :var NetworkSplitMode.LINE_SPLIT_BY_POINT_AND_LINE: 线与线打断，同时点打断线\n    :var NetworkSplitMode.TOPOLOGY_PROCESSING: 拓扑处理方式。使用该方式时，首先会对用于构建的线数据集进行去除重复线、长悬线延伸、\n                                               弧段求交、去除短悬线、去除冗余点、邻近端点合并和去除假结点等拓扑处理操作，然后再构建网络数据集。\n    "
    NO_SPLIT = 0
    LINE_SPLIT_BY_POINT = 1
    LINE_SPLIT_BY_POINT_AND_LINE = 2
    TOPOLOGY_PROCESSING = 3

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.networkanalyst.NetworkSplitMode"

    @classmethod
    def _externals(cls):
        return {"None": (cls.NO_SPLIT)}


@unique
class RouteType(JEnum):
    __doc__ = "\n    最佳路径分析的分析模式，用于基于 SSC 的最佳路径分析。\n\n    :var RouteType.RECOMMEND: 推荐模式\n    :var RouteType.MINLENGTH: 距离最短\n    :var RouteType.NOHIGHWAY: 不走高速\n    "
    RECOMMEND = 0
    MINLENGTH = 2
    NOHIGHWAY = 3

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.networkanalyst.RouteType"


class WeightFieldInfo:
    __doc__ = "\n    权值字段信息类。\n\n    存储了网络分析中权值字段的相关信息，包括正向权值字段与反向权值字段。权值字段是表示花费的权重值的字段。正向权值字段值表示沿弧段的\n    起点到终点所需的耗费。反向权值字段值表示沿弧段的终点到起点所需的耗费。\n    "

    def __init__(self, weight_name, ft_weight_field, tf_weight_field):
        """
        初始化对象

        :param str weight_name: 权值字段信息的名称
        :param str ft_weight_field: 正向权值字段或字段表达式
        :param str tf_weight_field: 反向权值字段或字段表达式
        """
        self._weight_name = weight_name
        self._ft_weight_field = ft_weight_field
        self._tf_weight_field = tf_weight_field

    @property
    def weight_name(self):
        """str: 权值字段信息的名称"""
        return self._weight_name

    def set_weight_name(self, value):
        """
        设置权值字段信息的名称

        :param str value: 权值字段信息的名称
        :return: self
        :rtype: WeightFieldInfo
        """
        self._weight_name = value
        return self

    @property
    def ft_weight_field(self):
        """str: 正向权值字段或字段表达式"""
        return self._ft_weight_field

    def set_ft_weight_field(self, value):
        """
        设置正向权值字段或字段表达式

        :param str value: 正向权值字段或字段表达式
        :return: self
        :rtype: WeightFieldInfo
        """
        self._ft_weight_field = value
        return self

    @property
    def tf_weight_field(self):
        """str: 反向权值字段或字段表达式"""
        return self._tf_weight_field

    def set_tf_weight_field(self, value):
        """
        设置反向权值字段或字段表达式

        :param str value: 反向权值字段或字段表达式
        :return: self
        :rtype: WeightFieldInfo
        """
        self._tf_weight_field = value
        return self

    @property
    def _jobject(self):
        java_object = get_jvm().com.supermap.analyst.networkanalyst.WeightFieldInfo()
        java_object.setFTWeightField(self.ft_weight_field)
        java_object.setTFWeightField(self.tf_weight_field)
        java_object.setName(self.weight_name)
        return java_object

    def __str__(self):
        return "WeightFieldInfo(%s, %s, %s)" % (self.weight_name, self.ft_weight_field, self.tf_weight_field)


class PathAnalystSetting:
    __doc__ = "最佳路径分析环境设置，该类抽象基类，用户可以选择使用 :py:class:`SSCPathAnalystSetting` 或 :py:class:`TransportationPathAnalystSetting` "

    def __init__(self):
        self._network_dt = None

    @property
    def network_dataset(self):
        """DatasetVector: 网络数据集"""
        return self._network_dt

    def set_network_dataset(self, dataset):
        """
        设置用于最佳路径分析的网络数据集

        :param dataset: 网络数据集
        :type dataset: DatasetVetor or str
        :return: 当前对象
        :rtype: PathAnalystSetting
        """
        if dataset is not None:
            dataset = get_input_dataset(dataset)
            if isinstance(dataset, DatasetVector):
                self._network_dt = dataset
                return self
            raise ValueError("required DatasetVector, but is " + str(type(dataset)))
        else:
            return self


class SSCPathAnalystSetting(PathAnalystSetting):
    __doc__ = "\n    基于 SSC 文件的最佳路径分析环境设置\n    "

    def __init__(self, network_dt=None, ssc_file_path=None):
        """

        :param DatasetVector network_dt: 网络数据集名称
        :param str ssc_file_path: SSC 文件路径
        """
        PathAnalystSetting.__init__(self)
        self.set_network_dataset(network_dt)
        self._ssc_file_path = None
        self.set_ssc_file_path(ssc_file_path)
        self._tolerance = 0.0

    @property
    def ssc_file_path(self):
        """str: SSC 文件路径"""
        return self._ssc_file_path

    def set_ssc_file_path(self, value):
        """
        设置 SSC 文件路径

        :param str value: SSC 文件路径
        :return: 当前对象
        :rtype: SSCPathAnalystSetting
        """
        if value:
            self._ssc_file_path = str(value)
        return self

    @property
    def tolerance(self):
        """float: 节点容限"""
        return self._tolerance

    def set_tolerance(self, value):
        """
        设置节点容限

        :param float value: 节点容限
        :return: 当前对象
        :rtype: SSCPathAnalystSetting
        """
        self._tolerance = float(value)

    @property
    def _jobject(self):
        java_object = get_jvm().com.supermap.analyst.networkanalyst.SSCPathAnalystSetting()
        java_object.setNetworkDataset(oj(self.network_dataset))
        java_object.setSSCFilePath(str(self.ssc_file_path))
        if self.tolerance > 0:
            java_object.setTolerance(float(self.tolerance))
        return java_object


class TransportationPathAnalystSetting(PathAnalystSetting):
    __doc__ = "\n    交通网络分析最佳路径分析环境。\n    "

    def __init__(self, network_dataset=None):
        """
        初始化对象

        :param network_dataset: 网络数据集
        :type network_dataset: DatasetVector or str
        """
        PathAnalystSetting.__init__(self)
        self.set_network_dataset(network_dataset)
        self._tolerance = 0.0
        self._node_id = None
        self._edge_id = None
        self._f_node_id = None
        self._t_node_id = None
        self._weight_fields = None
        self._barrier_node_ids = None
        self._barrier_edge_ids = None
        self._rule_field = None
        self._ft_single_way_rule_values = None
        self._tf_single_way_rule_values = None
        self._prohibited_way_rule_values = None
        self._two_way_rule_values = None
        self._edge_filter = None
        self._bounds = None
        self._edge_name_field = None

    @property
    def tolerance(self):
        """float: 节点容限"""
        return self._tolerance

    def set_tolerance(self, value):
        """
        设置节点容限

        :param float value: 节点容限
        :return: 当前对象
        :rtype: TransportationPathAnalystSetting
        """
        self._tolerance = float(value)
        return self

    @property
    def node_id_field(self):
        """str: 网络数据集中标识结点 ID 的字段"""
        return self._node_id

    def set_node_id_field(self, value):
        """
        设置网络数据集标识结点ID的字段

        :param str value: 网络数据集中标识结点 ID 的字段
        :return: self
        :rtype: TransportationPathAnalystSetting
        """
        self._node_id = value
        return self

    @property
    def edge_id_field(self):
        """str: 网络数据集中标志弧段 ID 的字段"""
        return self._edge_id

    def set_edge_id_field(self, value):
        """
        设置网络数据集中标识结点 ID 的字段

        :param str value:  网络数据集中标志弧段 ID 的字段
        :return: self
        :rtype: TransportationPathAnalystSetting
        """
        self._edge_id = value
        return self

    @property
    def f_node_id_field(self):
        """str: 网络数据集中标志弧段起始结点 ID 的字段"""
        return self._f_node_id

    def set_f_node_id_field(self, value):
        """
        设置网络数据集中标志弧段起始结点 ID 的字段

        :param str value: 网络数据集中标志弧段起始结点 ID 的字段
        :return: self
        :rtype: TransportationPathAnalystSetting
        """
        self._f_node_id = value
        return self

    @property
    def t_node_id_field(self):
        """str: 网络数据集中标志弧段起始结点 ID 的字段"""
        return self._t_node_id

    def set_t_node_id_field(self, value):
        """
        设置网络数据集中标志弧段起始结点 ID 的字段

        :param str value:
        :return: self
        :rtype: TransportationPathAnalystSetting
        """
        self._t_node_id = value
        return self

    @property
    def weight_fields(self):
        """list[WeightFieldInfo]: 权重字段"""
        return self._weight_fields

    def set_weight_fields(self, value):
        """
        设置权重字段

        :param value: 权重字段
        :type value: list[WeightFieldInfo] or tuple[WeightFieldInfo]
        :return: self
        :rtype: TransportationPathAnalystSetting
        """
        if self._weight_fields is None:
            self._weight_fields = []
        elif isinstance(value, WeightFieldInfo):
            self._weight_fields.append(value)
        else:
            if isinstance(value, (list, tuple)):
                self._weight_fields.extend(value)
            else:
                raise ValueError("required list[WeightFieldInfo] or WeightFieldInfo")
        return self

    @property
    def barrier_node_ids(self):
        """list[int]: 障碍结点的 ID 列表"""
        return self._barrier_node_ids

    def set_barrier_node_ids(self, value):
        """
        设置障碍结点的 ID 列表

        :param value: 障碍结点的 ID 列表
        :type value: str or list[int]
        :return: self
        :rtype: TransportationPathAnalystSetting
        """
        if isinstance(value, str):
            self._barrier_node_ids = split_input_int_list_from_str(value)
        else:
            if isinstance(value, (tuple, list)):
                self._barrier_node_ids = list(value)
            else:
                if isinstance(value, int):
                    self._barrier_node_ids = [
                     value]
                else:
                    self._barrier_node_ids = value
        return self

    @property
    def barrier_edge_ids(self):
        """list[int]: 障碍弧段的 ID 列表"""
        return self._barrier_edge_ids

    def set_barrier_edge_ids(self, value):
        """
        设置障碍弧段的 ID 列表

        :param value: 障碍弧段的 ID 列表
        :type value: str or list[int]
        :return: self
        :rtype: TransportationPathAnalystSetting
        """
        if isinstance(value, str):
            self._barrier_edge_ids = split_input_int_list_from_str(value)
        else:
            if isinstance(value, (tuple, list)):
                self._barrier_edge_ids = list(value)
            else:
                if isinstance(value, int):
                    self._barrier_edge_ids = [
                     value]
                else:
                    self._barrier_edge_ids = value
        return self

    @property
    def rule_field(self):
        """str: 网络数据集中表示网络弧段的交通规则的字段"""
        return self._rule_field

    def set_rule_field(self, value):
        """
        设置网络数据集中表示网络弧段的交通规则的字段

        :param str value: 网络数据集中表示网络弧段的交通规则的字段
        :return: self
        :rtype: TransportationPathAnalystSetting
        """
        self._rule_field = value
        return self

    @property
    def ft_single_way_rule_values(self):
        """list[str]: 用于表示正向单行线的字符串的数组"""
        return self._ft_single_way_rule_values

    def set_ft_single_way_rule_values(self, value):
        """
        设置用于表示正向单行线的字符串的数组

        :param value: 用于表示正向单行线的字符串的数组
        :type value: str or list[str]
        :return: self
        :rtype: TransportationPathAnalystSetting
        """
        self._ft_single_way_rule_values = split_input_list_from_str(value)
        return self

    @property
    def tf_single_way_rule_values(self):
        """list[str]: 表示逆向单行线的字符串的数组"""
        return self._tf_single_way_rule_values

    def set_tf_single_way_rule_values(self, value):
        """
        设置表示逆向单行线的字符串的数组

        :param value: 表示逆向单行线的字符串的数组
        :type value: str or list[str]
        :return: self
        :rtype: TransportationPathAnalystSetting
        """
        self._tf_single_way_rule_values = value
        return self

    @property
    def prohibited_way_rule_values(self):
        """list[str]: 表示禁行线的字符串的数组"""
        return self._prohibited_way_rule_values

    def set_prohibited_way_rule_values(self, value):
        """
        设置表示禁行线的字符串的数组

        :param value: 表示禁行线的字符串的数组
        :type value: str or list[str]
        :return: self
        :rtype: TransportationPathAnalystSetting
        """
        self._prohibited_way_rule_values = value
        return self

    @property
    def two_way_rule_values(self):
        """list[str]: 表示双向通行线的字符串的数组"""
        return self._two_way_rule_values

    def set_two_way_rule_values(self, value):
        """
        设置表示双向通行线的字符串的数组

        :param value: 表示双向通行线的字符串的数组
        :type value: str or list[str]
        :return: self
        :rtype: TransportationPathAnalystSetting
        """
        self._two_way_rule_values = value
        return self

    @property
    def edge_filter(self):
        """str: 交通网络分析中弧段过滤表达式"""
        return self._edge_filter

    def set_edge_filter(self, value):
        """
        设置交通网络分析中弧段过滤表达式

        :param value: 交通网络分析中弧段过滤表达式
        :return: self
        :rtype: TransportationPathAnalystSetting
        """
        self._edge_filter = value
        return self

    @property
    def bounds(self):
        """Rectangle: 最佳路径分析的分析范围"""
        return self._bounds

    def set_bounds(self, value):
        """
        设置最佳路径分析的分析范围

        :param value: 最佳路径分析的分析范围
        :type value: Rectangle or str
        :return: self
        :rtype: TransportationPathAnalystSetting
        """
        self._bounds = Rectangle.make(value)
        return self

    @property
    def edge_name_field(self):
        """str: 道路名称字段"""
        return self._edge_name_field

    def set_edge_name_field(self, value):
        """
        设置道路名称字段

        :param str value: 道路名称字段
        :return: self
        :rtype: TransportationPathAnalystSetting
        """
        if value is not None:
            self._edge_name_field = str(value)
        return self

    def _java_transportation_analyst_setting(self):
        java_object = get_jvm().com.supermap.analyst.networkanalyst.TransportationAnalystSetting()
        java_object.setNetworkDataset(oj(self.network_dataset))
        if self.tolerance > 0:
            java_object.setTolerance(float(self.tolerance))
        else:
            if self.node_id_field is not None:
                java_object.setNodeIDField(str(self.node_id_field))
            else:
                java_object.setNodeIDField(self.network_dataset.child_dataset.get_field_name_by_sign("NODEID"))
            if self.edge_id_field is not None:
                java_object.setEdgeIDField(str(self.edge_id_field))
            else:
                java_object.setEdgeIDField(self.network_dataset.get_field_name_by_sign("EDGEID"))
            if self.f_node_id_field is not None:
                java_object.setFNodeIDField(self.f_node_id_field)
            else:
                java_object.setFNodeIDField(self.network_dataset.get_field_name_by_sign("FNODE"))
            if self.t_node_id_field is not None:
                java_object.setTNodeIDField(self.t_node_id_field)
            else:
                java_object.setTNodeIDField(self.network_dataset.get_field_name_by_sign("TNODE"))
        if self.weight_fields is not None:
            java_weight_fields = get_jvm().com.supermap.analyst.networkanalyst.WeightFieldInfos()
            for weight in self.weight_fields:
                java_weight_fields.add(oj(weight))

            java_object.setWeightFieldInfos(java_weight_fields)
        if self.barrier_node_ids is not None:
            java_object.setBarrierNodes(to_java_int_array(split_input_int_list_from_str(self.barrier_node_ids)))
        if self.barrier_edge_ids is not None:
            java_object.setBarrierEdges(to_java_int_array(split_input_int_list_from_str(self.barrier_edge_ids)))
        if self.rule_field is not None:
            java_object.setRuleField(str(self.rule_field))
        if self.ft_single_way_rule_values is not None:
            java_object.setFTSingleWayRuleValues(to_java_string_array(split_input_list_from_str(self.ft_single_way_rule_values)))
        if self.tf_single_way_rule_values is not None:
            java_object.setTFSingleWayRuleValues(to_java_string_array(split_input_list_from_str(self.tf_single_way_rule_values)))
        if self.prohibited_way_rule_values is not None:
            java_object.setProhibitedWayRuleValues(to_java_string_array(split_input_list_from_str(self.prohibited_way_rule_values)))
        if self.two_way_rule_values is not None:
            java_object.setTwoWayRuleValues(to_java_string_array(split_input_list_from_str(self.two_way_rule_values)))
        if self.edge_filter is not None:
            java_object.setEdgeFilter(str(self.edge_filter))
        if self.bounds is not None:
            java_object.setBounds(oj(self.bounds))
        if self.edge_name_field is not None:
            java_object.setEdgeNameField(str(self.edge_name_field))
        return java_object

    @property
    def _jobject(self):
        """Py4J 映射的 Java 对象"""
        java_analyst_setting = self._java_transportation_analyst_setting()
        return get_jvm().com.supermap.analyst.networkanalyst.TransportationPathAnalystSetting(java_analyst_setting)


class TransportationAnalystSetting(TransportationPathAnalystSetting):
    __doc__ = "\n    交通网络分析环境设置类。该类用于提供交通网络分析时所需要的所有参数信息。交通网络分析环境设置类的各个参数的设置直接影响分析的结果。\n\n    在利用交通网络分析类（ :py:class:`TransportationAnalyst` ）进行各种交通网络分析时，都要首先设置交通网络分析的环境，而交通网络分析环境的设\n    置就是通过 :py:class:`TransportationAnalyst` 类对象的 :py:meth:`TransportationAnalyst.set_analyst_setting` 方法来完成的。\n    "

    def __init__(self):
        TransportationPathAnalystSetting.__init__(self)

    @property
    def _jobject(self):
        """Py4J 映射的 Java 对象"""
        return self._java_transportation_analyst_setting()


class _SSCPathAnalystParameter:
    __doc__ = "\n    基于 SSC 的最佳路径分析参数类\n    "

    def __init__(self, start_point, end_point, midpoints=None, route_type='RECOMMEND', is_alternative=False):
        """
        初始化对象

        :param Point2D start_point: 路径分析的起始点
        :param Point2D end_point: 路径分析的终止点
        :param midpoints: 路径分析中间途经点
        :type midpoints: list[Point2D] or tuple[Point2D]
        :param route_type: 路径分析模式
        :type route_type: RouteType or str
        :param bool is_alternative: 是否返回备选方案
        """
        self._start_point = None
        self._end_point = None
        self._midpoints = None
        self._route_type = RouteType._make(route_type)
        self._is_alternative = is_alternative
        self.set_start_point(start_point)
        self.set_end_point(end_point)
        self.set_midpoints(midpoints)

    @property
    def end_point(self):
        """Point2D: 路径分析的终止点"""
        return self._end_point

    def set_end_point(self, point):
        """
        设置路径分析的终止点

        :param Point2D point: 路径分析的终止点
        :return: self
        :rtype: SSCPathAnalystParameter
        """
        self._end_point = Point2D.make(point)
        return self

    @property
    def start_point(self):
        """Point2D: 路径分析的起始点"""
        return self._start_point

    def set_start_point(self, point):
        """
        设置路径分析的起始点

        :param Point2D point: 路径分析的起始点
        :return: self
        :rtype: SSCPathAnalystParameter
        """
        self._start_point = Point2D.make(point)
        return self

    @property
    def midpoints(self):
        """list[Point2D]: 路径分析中间途经点"""
        return self._midpoints

    def set_midpoints(self, points):
        """
        设置路径分析中间途经点

        :param points: 路径分析中间途经点
        :type points: list[Point2D] or tuple[Point2D]
        :return: self
        :rtype: SSCPathAnalystParameter
        """
        if points is not None:
            self._midpoints = []
            if not isinstance(points, (list, tuple)):
                points = [
                 points]
            for point in points:
                self._midpoints.append(Point2D.make(point))

        return self

    @property
    def route_type(self):
        """RouteType: 路径分析模式，默认值为：RECOMMEND"""
        return self._route_type

    def set_route_type(self, value):
        """
        设置路径分析模式

        :param value: 路径分析模式
        :type value: RouteType or str
        :return: self
        :rtype: SSCPathAnalystParameter
        """
        self._route_type = RouteType._make(value, "RECOMMEND")
        return self

    @property
    def is_alternative(self):
        """bool: 是否返回备选路径，默认值为 False"""
        return self._is_alternative

    def set_alternative(self, value):
        """
        设置是否返回备选路径

        :param bool value: 设置 True 将返回备选路径，否则只会返回一条最佳路径
        :return: self
        :rtype: SSCPathAnalystParameter
        """
        if parse_bool(value):
            self._is_alternative = True
        else:
            self._is_alternative = False
        return self

    @property
    def _jobject(self):
        java_object = get_jvm().com.supermap.analyst.networkanalyst.SSCPathAnalystParameter()
        java_object.setStartPoint(oj(self.start_point))
        java_object.setEndPoint(oj(self.end_point))
        if self.midpoints is not None:
            java_object.setMidpoints(to_java_point2ds(self.midpoints))
        if self.route_type is not None:
            java_object.setRouteType(oj(self.route_type))
        java_object.setAlternative(bool(self.is_alternative))
        return java_object


class PathInfoItem:
    __doc__ = "\n    引导信息项\n    "

    def __init__(self, java_object):
        self._length = java_object.getLength()
        self._direction_to_swerve = java_object.getDirectionToSwerve()
        self._route_name = java_object.getRouteName()
        self._junction = Point2D._from_java_object(java_object.getJunction())

    @property
    def length(self):
        """float:  返回当前道路的长度。"""
        return self._length

    @property
    def direction_to_swerve(self):
        """int: 返回到下一条道路的转弯方向。其中0表示直行，1表示左前转弯，2表示右前转弯，3表示左转弯，4表示右转弯，5表示左后转弯，
        6表示右后转弯，7表示掉头，8表示右转弯绕行至左，9表示直角斜边右转弯，10表示环岛。"""
        return self._direction_to_swerve

    @property
    def route_name(self):
        """str: 该接口可以返回当前道路的名称，当道路名称为“PathPoint”时，表示到达途径点。"""
        return self._route_name

    @property
    def junction(self):
        """Point2D: 通过该接口可以返回到下一条道路的路口点坐标"""
        return self._junction


class PathInfo:
    __doc__ = "\n    引导信息，通过该类，可以获得基于 SSC 路径分析后路线的导引信息\n    "

    def __init__(self, path_info_items):
        self._items = list(path_info_items)

    def __getitem__(self, item):
        """
        获取指定位置的行驶导引子项

        :param item: 指定的行驶导引索引下标
        :type item: int
        :return: 行驶导引子项
        :rtype: PathInfoItem
        """
        return self._items[item]

    def __iter__(self):
        return self._items.__iter__()

    def __len__(self):
        """
        返回行驶导引子项数目

        :return: 行驶导引子项数目
        :rtype: int
        """
        return self._items.__len__()

    _dir_str = {
     0: '"向前直行"', 
     1: '"左前转弯"', 
     2: '"右前转弯"', 
     3: '"左转弯"', 
     4: '"右转弯"', 
     5: '"左后转弯"', 
     6: '"右后转弯"', 
     7: '"掉头行驶"', 
     8: '"右转弯绕行至左"', 
     9: '"直角斜边右转弯"', 
     10: '"环岛形式"'}

    @staticmethod
    def _turn_type_str(dir_to_swerve):
        if dir_to_swerve in PathInfo._dir_str.keys():
            return PathInfo._dir_str[dir_to_swerve]
        return ""

    def __str__(self):
        if self._items:
            route_name = self._items[0].route_name if self._items[0].route_name else "匿名道路"
            if route_name == "PathPoint":
                route_name = "匿名道路"
            navigation_info = "导航开始, 从起点进入[{}]".format(route_name)
            navigation_infos = [
             navigation_info]
            for index, item in enumerate(self._items):
                route_name = item.route_name if item.route_name else "匿名道路"
                if route_name == "PathPoint":
                    route_name = "匿名道路"
                if index == len(self._items) - 1 and len(self._items) > 1:
                    navigation_info = "沿着[{}], 行驶{}, 即将到达终点".format(route_name, round(item.length, 2))
                else:
                    if item.length > 0:
                        next_route_name = self._items[index + 1].route_name if self._items[index + 1].route_name else "匿名道路"
                        if next_route_name == "PathPoint":
                            next_route_name = "匿名道路"
                        navigation_info = "沿着[{}], 行驶{}, 然后{}进入[{}]".format(route_name, round(item.length, 2), PathInfo._turn_type_str(item.direction_to_swerve), next_route_name)
                    else:
                        junction = item.junction
                        navigation_info = "到达途径点 [x={},y={}]".format(junction.x, junction.y)
                navigation_infos.append(navigation_info)

            return "\r\n".join(navigation_infos)
        return ""


class SSCPathAnalyst(JVMBase):
    __doc__ = "基于 SSC 文件的路径分析类。用户可以通过 :py:meth:`compile_ssc_data` 编译 ssc 文件。通常，使用 SSC 文件的路径分析性能要好于基于\n     网络数据集的交通网络路径分析性能。"

    def __init__(self, path_analyst_setting):
        """
        初始化对象

        :param path_analyst_setting: 基于 SSC 路径分析环境参数对象。
        :type path_analyst_setting: SSCPathAnalystSetting
        """
        JVMBase.__init__(self)
        self.set_analyst_setting(path_analyst_setting)

    def _make_java_object(self):
        return self._jvm.com.supermap.analyst.networkanalyst.SSCPathAnalyst()

    def set_analyst_setting(self, path_analyst_setting):
        """
        设置路径分析环境参数

        :param path_analyst_setting: 基于 SSC 路径分析环境参数对象。
        :type path_analyst_setting: SSCPathAnalystSetting
        :return: self
        :rtype: SSCPathAnalyst
        """
        if not isinstance(path_analyst_setting, SSCPathAnalystSetting):
            raise ValueError("required SSCPathAnalystSetting, but " + str(type(path_analyst_setting)))
        self._jobject.setAnalystSetting(oj(path_analyst_setting))
        return self

    def find_path(self, start_point, end_point, midpoints=None, route_type='RECOMMEND', is_alternative=False):
        """
        最佳路径分析

        :param Point2D start_point: 起始点
        :param Point2D end_point: 终止点
        :param midpoints: 中间途经点
        :type midpoints: list[Point2D] or tuple[Point2D] or Point2D
        :param route_type: 最佳路径分析的分析模式，默认值为 'RECOMMEND'
        :type route_type: RouteType or str
        :param bool is_alternative: 是否返回备选方案。True 将返回备选路径，否则只会返回一条最佳路径
        :return: 分析成功将返回 True，失败返回 False
        :rtype: bool
        """
        path_analyst_parameter = _SSCPathAnalystParameter(start_point, end_point, midpoints, route_type, is_alternative)
        return self._jobject.findPath(oj(path_analyst_parameter))

    def get_path_points(self):
        """
        返回分析结果的途经点集合。请保证在调用该接口之前路径分析成功。

        :return: 分析结果的途经点坐标的集合
        :rtype: list[Point2D]
        """
        java_points = self._jobject.getPathPoints()
        if java_points is not None:
            return java_point2ds_to_list(java_points)

    def get_path_length(self):
        """
        返回分析结果的总长度。请保证在调用该接口之前路径分析成功。

        :return: 分析结果的总长度。
        :rtype: float
        """
        return self._jobject.getPathLength()

    def get_path_infos(self):
        """
        返回分析结果的引导信息集合。请保证在调用该接口之前路径分析成功。

        :return: 分析结果的引导信息集合
        :rtype: PathInfo
        """
        java_path_infos = self._jobject.getPathInfos()
        if java_path_infos is not None:
            return PathInfo(list((PathInfoItem(java_path_info) for java_path_info in java_path_infos)))

    def get_path_time(self):
        """
        返回分析结果的行驶时间，单位为秒。如果想获取行驶时间，在编译 SSC 文件时需要指定正确的速度字段。

        :return: 分析结果的行驶时间
        :rtype: float
        """
        return self._jobject.getPathTime()

    def get_alternative_path_points(self):
        """
        返回备选分析结果的途经点集合。

        :return: 备选分析结果的途经点集合。
        :rtype: list[Point2D]
        """
        java_points = self._jobject.getAlternativePathPoints()
        if java_points is not None:
            return java_point2ds_to_list(java_points)

    def get_alternative_path_length(self):
        """
        返回备选分析结果的总长度。

        :return: 备选分析结果的总长度。
        :rtype: float
        """
        return self._jobject.getAlternativePathLength()

    def get_alternative_path_time(self):
        """
        返回备选分析结果的行驶时间，单位为秒。如果想获取行驶时间，在编译 SSC 文件时需要指定正确的速度字段。

        :return: 备选分析结果的行驶时间
        :rtype: float
        """
        return self._jobject.getAlternativePathTime()

    def get_alternative_path_infos(self):
        """
        返回备选分析结果的引导信息。

        :return: 备选分析结果的引导信息
        :rtype: PathInfo
        """
        java_path_infos = self._jobject.getAlternativePathInfos()
        if java_path_infos is not None:
            return PathInfo(list((PathInfoItem(java_path_info) for java_path_info in java_path_infos)))


class TrackPoint:
    __doc__ = "\n    带时间的轨迹坐标点。\n    "

    def __init__(self, point, t, key=0):
        """

        :param Point2D point: 二维点坐标
        :param datetime.datetime t: 时间值，表示坐标位置点的时间。
        :param int key: 关键值，用于标识点唯一性
        """
        self._point = Point2D.make(point)
        self._time = parse_datetime(t)
        self._key = int(key)

    @property
    def point(self):
        """Point2D: 二维点坐标"""
        return self._point

    @property
    def time(self):
        """datetime.datetime: 时间值，表示坐标位置点的时间"""
        return self._time

    @property
    def key(self):
        """int: 关键值，用于标识点唯一性"""
        return self._key

    def set_key(self, value):
        """
        设置关键值，用于标识点唯一性

        :param int value: 关键值
        :return: self
        :rtype: TrackPoint
        """
        self._key = int(value)
        return self

    def set_point(self, value):
        """
        设置位置点

        :param value: 位置点
        :type value: Point2D or str
        :return: self
        :rtype: TrackPoint
        """
        self._point = Point2D.make(value)
        return self

    def set_time(self, value):
        """
        设置时间值

        :param value: 时间值，表示坐标位置点的时间
        :type value: datetime.datetime or str
        :return: self
        :rtype: TrackPoint
        """
        self._time = parse_datetime(value)
        return self

    @property
    def _jobject(self):
        java_object = get_jvm().com.supermap.analyst.networkanalyst.TrackPoint(oj(self.point), datetime_to_java_date(self.time))
        java_object.setKey(int(self.key))
        return java_object

    @staticmethod
    def _from_java_object(java_object):
        return TrackPoint(Point2D._from_java_object(java_object.getPoint()), java_date_to_datetime(java_object.getTime()), java_object.getKey())


class MapMatchingResult(JVMBase):
    __doc__ = "\n    地图匹配结果类。包括匹配后得到的轨迹点、轨迹线、弧段id、匹配正确率、错误率等。\n    "

    def __init__(self, java_object):
        JVMBase.__init__(self)
        self._java_object = java_object

    @property
    def rectified_points(self):
        """list[Point2D]: 地图匹配后的轨迹点，它对应于每个输入点进行处理的点，数组大小等于输入点数目。"""
        return list((Point2D._from_java_object(p) for p in self._java_object.getRectifiedPoints()))

    @property
    def edges(self):
        """list[int]: 每条匹配路径经过的弧段ID"""
        return java_array_to_list(self._java_object.getEdges())

    @property
    def track_points(self):
        """list[Point2D]: 地图匹配后得到的轨迹点串，轨迹点串去掉了重复点以及一些匹配失败的点"""
        java_track_points = self._java_object.getTrackPoints()
        if java_track_points is not None:
            return list((Point2D._from_java_object(p) for p in java_track_points))

    @property
    def track_line(self):
        """GeoLine: 结果轨迹线对象。将 :py:attr:`track_points` 构造成的线对象。

                    .. image:: ../image/MapMatchingResult.png

         """
        java_track_line = self._java_object.getTrackLine()
        if java_track_line is not None:
            return GeoLine._from_java_object(java_track_line)

    def evaluate_truth(self, truth_edges):
        """
        评估当前地图匹配结果的正确性。
        输入真实的道路线对象，计算匹配结果的正确性。

        计算正确性的公式为:

        .. image:: ../image/evaluationTruth.png

        :param truth_edges: 真实的道路线对象
        :type truth_edges: list[GeoLine] or tuple[GeoLine]
        :return: 当前结果的正确性
        :rtype: float
        """
        if truth_edges is None:
            raise ValueError("required list[GeoLine], but " + str(type(truth_edges)))
        java_lines = to_java_geoline_array(truth_edges)
        return self._java_object.evaluateTruth(java_lines)

    def evaluate_error(self, truth_edges):
        """
        评估当前地图匹配结果的错误率。
        输入真实的道路线对象，计算匹配结果的错误率。

        :param truth_edges: 真实的道路线对象
        :type truth_edges: list[GeoLine] or tuple[GeoLine]
        :return: 当前结果的错误率
        :rtype: float
        """
        if truth_edges is None:
            raise ValueError("required list[GeoLine], but " + str(type(truth_edges)))
        java_lines = to_java_geoline_array(truth_edges)
        return self._java_object.evaluateError(java_lines)


class MapMatchingLikelyResult(JVMBase):
    __doc__ = "\n    实时地图匹配结果类\n    "

    def __init__(self, java_object):
        JVMBase.__init__(self)
        self._java_object = java_object

    @property
    def rectified_point(self):
        """Point2D: 地图匹配后的轨迹点，它对应于每个输入点进行处理的点，数组大小等于输入点数目。"""
        return Point2D._from_java_object(self._java_object.getRectifiedPoint())

    @property
    def probability(self):
        """float: 实时地图匹配时，计算当前点归属哪条道路时，算法会生成该点到附近所有可能道路的匹配概率值，选择概率值最高的作为该
                  点的匹配道路"""
        return self._java_object.getProbability()

    @property
    def distance_to_road(self):
        """float: 原始轨迹点到当前轨迹路径的最近距离。"""
        return self._java_object.getDistanceToRoad()

    @property
    def edges(self):
        """list[int]:匹配路径经过的弧段ID """
        return java_array_to_list(self._java_object.getEdges())

    @property
    def track_points(self):
        """list[Point2D]: 地图匹配后得到的轨迹点串，轨迹点串去掉了重复点以及一些匹配失败的点"""
        java_track_points = self._java_object.getTrackPoints()
        if java_track_points is not None:
            return list((Point2D._from_java_object(p) for p in java_track_points))

    @property
    def track_line(self):
        """GeoLine: 结果轨迹线对象。将 :py:attr:`track_points` 构造成的线对象。"""
        java_track_line = self._java_object.getTrackLine()
        if java_track_line is not None:
            return GeoLine._from_java_object(java_track_line)

    def evaluate_truth(self, truth_edges):
        """
        评估当前地图匹配结果的正确性。
        输入真实的道路线对象，计算匹配结果的正确性。

        计算正确性的公式为:

        .. image:: ../image/evaluationTruth.png

        :param truth_edges: 真实的道路线对象
        :type truth_edges: list[GeoLine] or tuple[GeoLine]
        :return: 当前结果的正确性
        :rtype: float
        """
        if truth_edges is None:
            raise ValueError("required list[GeoLine], but " + str(type(truth_edges)))
        java_lines = to_java_geoline_array(truth_edges)
        return self._java_object.evaluateTruth(java_lines)

    def evaluate_error(self, truth_edges):
        """
        评估当前地图匹配结果的错误率。
        输入真实的道路线对象，计算匹配结果的错误率。

        :param truth_edges: 真实的道路线对象
        :type truth_edges: list[GeoLine] or tuple[GeoLine]
        :return: 当前结果的错误率
        :rtype: float
        """
        if truth_edges is None:
            raise ValueError("required list[GeoLine], but " + str(type(truth_edges)))
        java_lines = to_java_geoline_array(truth_edges)
        return self._java_object.evaluateError(java_lines)


class MapMatching(JVMBase):
    __doc__ = "\n    基于HMM（隐式马尔科夫链）的地图匹配。\n    将轨迹点按照标识字段进行划分，按时间字段进行排序和分割轨迹，找到每条轨迹最可能的经过路线。目的是基于轨迹点还原真实路径。\n    "

    def __init__(self, path_analyst_setting=None):
        """
        初始化对象

        :param PathAnalystSetting path_analyst_setting: 最佳路径分析参数
        """
        JVMBase.__init__(self)
        self._path_analyst_setting = None
        self._measurement_error = 30.0
        self._max_limited_speed = 150.0
        self.set_path_analyst_setting(path_analyst_setting)

    def _make_java_object(self):
        return self._jvm.com.supermap.analyst.networkanalyst.MapMatching()

    @property
    def path_analyst_setting(self):
        """PathAnalystSetting: 最佳路径分析参数"""
        return self._path_analyst_setting

    def set_path_analyst_setting(self, path_analyst_setting):
        """
        设置最佳路径分析参数

        :param PathAnalystSetting path_analyst_setting: 最佳路径分析参数
        :return: self
        :rtype: MapMatching
        """
        if path_analyst_setting is not None:
            if not isinstance(path_analyst_setting, PathAnalystSetting):
                raise ValueError("required PathAnalystSetting, but " + str(type(path_analyst_setting)))
            self._jobject.setPathAnalystSetting(oj(path_analyst_setting))
            self._path_analyst_setting = path_analyst_setting
        else:
            self._path_analyst_setting = None
        return self

    def set_measurement_error(self, value):
        """
        设置轨迹点误差值。比如 GPS误差值，单位为米。如果轨迹点到最近道路的距离超出误差值，则认为轨迹点非法。所以，设定一个合理的
        误差值对地图匹配的结果有直接影响，如果得到的轨迹点精度高，设置 一个较小的值可以有效提升性能，例如，15米。默认值为 30米。

        :param float value: 轨迹点误差值
        :return: self
        :rtype: MapMatching
        """
        self._measurement_error = float(value)
        self._jobject.setMeasurementError(float(value))
        return self

    @property
    def measurement_error(self):
        """float: 轨迹点误差值"""
        return self._measurement_error

    def set_max_limited_speed(self, value):
        """
        设置最大限制速度。单位为km/h。对相邻两个点计算出来的速度值大于指定的限制速度时，则认为这两个点不可达，即没有有效的道路相通。
        默认值为 150 km/h。

        :param float value:
        :return: self
        :rtype: MapMatching
        """
        self._max_limited_speed = float(value)
        self._jobject.setMaxLimitedSpeed(float(value))
        return self

    @property
    def max_limited_speed(self):
        """float: 最大限制速度"""
        return self._max_limited_speed

    def batch_match(self, points):
        """
        批量地图匹配，输入一连串点进行地图匹配。注意，本方法默认认为输入的点串同属于一条轨迹线路。

        :param points: 待匹配的轨迹点
        :type points: list[TrackPoint] or tuple[TrackPoint]
        :return: 地图匹配结果
        :rtype: MapMatchingResult
        """
        if not points:
            raise ValueError("required list[TrackPoint], but " + str(type(points)))
        java_points = list((oj(p) for p in list(points)))
        java_result = self._jobject.batchMatch(java_points)
        if java_result:
            return MapMatchingResult(java_result)

    def match(self, point, is_new_track=False):
        """
        实时地图匹配。实时地图匹配每次只输入一个轨迹点，但在这之前的轨迹点匹配的信息将会继续保留以用于当次匹配。
        实时地图匹配返回的结果可能有多个，返回的结果数由当前点能匹配到的道路决定，返回的结果按照结果可能性从大到小排列。在轨迹线没有
        完成匹配之前，当前结果返回的结果只反应当前轨迹点及之前点的可能结果。

        当 is_new_track 为 True 时，表示将开启新的轨迹线，之前的匹配记录和信息将会清空，当前点将作为轨迹的第一个点。

        :param point: 待匹配轨迹点
        :type point: TrackPoint
        :param bool is_new_track:  是否开启新的轨迹
        :return: 实时地图匹配
        :rtype: list[MapMatchingLikelyResult]
        """
        if point is None:
            raise ValueError("required TrackPoint, but " + str(type(point)))
        java_results = self._jobject.match(oj(point), bool(is_new_track))
        if java_results:
            return list((MapMatchingLikelyResult(result) for result in java_results))

    def batch_match_dataset(self, source_dataset, id_field, time_field, split_time_milliseconds, out_data=None, out_dataset_name=None, result_track_index_field='TrackIndex'):
        """
        对数据集进行地图匹配，结果保存为点数据

        :param source_dataset: 原始轨迹点数据集
        :type source_dataset: DatasetVector or str
        :param str id_field:  轨迹的 ID 字段，相同 ID 值相同的轨迹点属于一条轨迹，比如手机号、车牌号等。没有指定 ID 字段时，数据集中所有点将归类为一条轨迹。
        :param str time_field:  轨迹点的时间字段，必须为时间或时间戳类型字段
        :param float split_time_milliseconds: 分割轨迹的时间间隔，如果时间相邻的两个点的时间间隔大于指定的分割轨迹的时间间隔，将从两个点间分割轨迹。
        :param out_data: 保存结果数据集的数据源
        :type out_data: Datasource or str
        :param str out_dataset_name:  结果数据集名称
        :param str result_track_index_field: 保存轨迹索引的字段，轨迹分割后，一条轨迹可能分割为多条子轨迹，
                                              result_track_index_field 将会保存子轨迹的索引值，值从1开始。 因为结果数据集会保
                                              存源轨迹点数据集的所有字段，所以必须确保 result_track_index_field 字段值在源轨
                                              迹点数据集中是没有被占用。
        :return: 结果轨迹点数据集，正确匹配到道路上的轨迹点。
        :rtype: DatasetVector
        """
        if not isinstance(source_dataset, DatasetVector):
            raise ValueError("source dataset required DatasetVector, but " + str(type(source_dataset)))
        else:
            if id_field is not None:
                id_field = str(id_field)
            else:
                if out_data is not None:
                    out_datasource = get_output_datasource(out_data)
                else:
                    out_datasource = source_dataset.datasource
                check_output_datasource(out_datasource)
                if out_dataset_name is None:
                    dest_name = source_dataset.name + "_rectify"
                else:
                    dest_name = out_dataset_name
            dest_name = out_datasource.get_available_dataset_name(dest_name)
            result_track_index_field = result_track_index_field or "TrackIndex"
        java_result = self._jobject.batchMatch(oj(source_dataset), id_field, str(time_field), float(split_time_milliseconds), oj(out_datasource), str(dest_name), str(result_track_index_field))
        if java_result is not None:
            return out_datasource[dest_name]


def split_track(track_points, split_time_milliseconds):
    """
    轨迹切分，根据时间间隔，将轨迹进行分段。

    .. image:: ../image/splitTrack.png

    :param track_points: 轨迹点串
    :type track_points: list[TrackPoint] or tuple[TrackPoint]
    :param float split_time_milliseconds: 时间间隔值，单位为毫秒。当时间连续的两个点之间的时间间隔大于指定的时间间隔值时，将会从
                                          两个点之间将轨迹分割
    :return: 结果轨迹段
    :rtype: list[list[TrackPoint]]
    """
    java_points = to_java_array(track_points, get_jvm().com.supermap.analyst.networkanalyst.TrackPoint)
    java_result = get_jvm().com.supermap.analyst.networkanalyst.TrajectoryPreprocessing.splitTrack(java_points, float(split_time_milliseconds))
    if java_result is not None:
        result = []
        for tracks in java_result:
            result.append(list((TrackPoint._from_java_object(point) for point in tracks)))

        return result


class TrajectoryPreprocessingResult(JVMBase):
    __doc__ = "\n    轨迹预处理结果类\n    "

    def __init__(self, java_object):
        JVMBase.__init__(self)
        self._java_object = java_object

    @property
    def rectified_points(self):
        """list[Point2D]: 处理后的轨迹点，它对应于每个输入点进行处理的点，数组大小等于输入点数目。"""
        java_points = self._java_object.getRectifiedPoints()

        def fun(p):
            if p:
                return TrackPoint._from_java_object(p)
            return

        if java_points is not None:
            return list(map(fun, java_points))

    @property
    def track_points(self):
        """list[Point2D]: 处理后得到的轨迹点。比如将重复点都去掉后剩余的轨迹点"""
        java_points = self._java_object.getTrackPoints()
        if java_points is not None:
            return list((Point2D._from_java_object(p) for p in java_points))

    @property
    def track_line(self):
        """GeoLine: 处理后轨迹点生成的轨迹线"""
        java_line = self._java_object.getTrackLine()
        if java_line is not None:
            return GeoLine._from_java_object(java_line)


class TrajectoryPreprocessing(JVMBase):
    __doc__ = "\n    轨迹预处理类。用于处理轨迹数据中的异常点，包括轨迹分段，处理偏移点、重复点、尖角等异常情形。\n    "

    def __init__(self):
        JVMBase.__init__(self)
        self._measurement_error = 30.0
        self._prj_coordsys = None
        self._valid_region_dt = None
        self._sharp_angle = 40.0
        self._is_remove_redundant_points = False

    def _make_java_object(self):
        return get_jvm().com.supermap.analyst.networkanalyst.TrajectoryPreprocessing()

    @property
    def measurement_error(self):
        """float: 轨迹点误差值"""
        return self._measurement_error

    def set_measurement_error(self, value):
        """
        设置轨迹点误差值，比如 GPS误差值，单位为米。需要根据数据的质量指定一个合适的误差值。轨迹点偏移超过该误差值，则将其处理掉。

        .. image:: ../image/MeasurementError.png

        :param float value: 轨迹点误差值
        :return: self
        :rtype: TrajectoryPreprocessing
        """
        self._measurement_error = float(value)
        self._jobject.setMeasurementError(float(value))
        return self

    @property
    def prj_coordsys(self):
        """PrjCoordSys: 待处理点的坐标系"""
        return self._prj_coordsys

    def set_prj_coordsys(self, value):
        """
        设置待处理点的坐标系

        :param PrjCoordSys value: 待处理点的坐标系
        :return: self
        :rtype: TrajectoryPreprocessing
        """
        self._prj_coordsys = PrjCoordSys.make(value)
        self._jobject.setPrjCoordSys(oj(value))
        return self

    @property
    def sharp_angle(self):
        """float: 尖角角度值"""
        return self._sharp_angle

    def set_sharp_angle(self, value):
        """
        设置尖角角度值。单位为角度，当连续时间段内三个不相等的点的夹角小于指定的尖角角度值时，中间的点将会被纠偏处理成首尾两个点的
        中点。当值小于等于0时，将不处理尖角。

        .. image:: ../image/SharpAngle.png

        :param float value: 尖角角度值
        :return: self
        :rtype: TrajectoryPreprocessing
        """
        self._sharp_angle = float(value)
        self._jobject.setSharpAngle(float(value))
        return self

    @property
    def is_remove_redundant_points(self):
        """bool: 是否去除空间位置相等的重复点"""
        return self._is_remove_redundant_points

    def set_remove_redundant_points(self, value):
        """
        设置是否去除空间位置相等的重复点

        .. image:: ../image/RemoveRedundantPoints.png

        :param bool value: 是否去除空间位置相等的重复点
        :return: self
        :rtype: TrajectoryPreprocessing
        """
        self._is_remove_redundant_points = parse_bool(value)
        self._jobject.setRemoveRedundantPoints(self._is_remove_redundant_points)
        return self

    @property
    def valid_region_dataset(self):
        """DatasetVector: 有效面数据集。"""
        return self._valid_region_dt

    def set_valid_region_dataset(self, value):
        """
        设置有效面，只有落在有效面内的点才是有效点。

        :param value: 有效面数据集
        :type value: DatasetVector or str
        :return: self
        :rtype: TrajectoryPreprocessing
        """
        self._valid_region_dt = get_input_dataset(value)
        self._jobject.setValidRegion(oj(self._valid_region_dt))
        return self

    def rectify(self, points):
        """
        轨迹预处理结果

        :param points: 待处理的轨迹点数据。
        :type points: list[TrackPoint] or tuple[TrackPoint]
        :return: 处理后的轨迹点数据集。
        :rtype: TrajectoryPreprocessingResult
        """
        java_points = to_java_array(points, get_jvm().com.supermap.analyst.networkanalyst.TrackPoint)
        java_result = self._jobject.rectify(java_points)
        if java_result is not None:
            return TrajectoryPreprocessingResult(java_result)

    def rectify_dataset(self, source_dataset, id_field, time_field, split_time_milliseconds, out_data=None, out_dataset_name=None, result_track_index_field='TrackIndex'):
        """
        对数据集进行轨迹预处理，结果保存为点数据

        :param source_dataset: 原始轨迹点数据集
        :type source_dataset: DatasetVector or str
        :param str id_field: 轨迹的 ID 字段，相同 ID 值相同的轨迹点属于一条轨迹，比如手机号、车牌号等。没有指定 ID 字段时，数据集
                             中所有点将归类为一条轨迹。
        :param str time_field: 轨迹点的时间字段，必须为时间或时间戳类型字段
        :param float split_time_milliseconds: 分割轨迹的时间间隔，如果时间相邻的两个点的时间间隔大于指定的分割轨迹的时间间隔，将
                                              会从两个点间分割轨迹。
        :param out_data: 保存结果数据集的数据源
        :type out_data: Datasource or str
        :param str out_dataset_name: 结果数据集名称
        :param str result_track_index_field: 保存轨迹索引的字段，轨迹分割后，一条轨迹可能分割为多条子轨迹，result_track_index_field
                                             将会保存子轨迹的索引值，值从1开始。 因为结果数据集会保存源轨迹点数据集的所有字段，
                                             所以必须确保 result_track_index_field 字段值在源轨迹点数据集中是没有被占用。
        :return: 结果点数据集，预处理后的结果点数据集。
        :rtype: DatasetVector
        """
        if not isinstance(source_dataset, DatasetVector):
            raise ValueError("source dataset required DatasetVector, but " + str(type(source_dataset)))
        else:
            if id_field is not None:
                id_field = str(id_field)
            else:
                if out_data is not None:
                    out_datasource = get_output_datasource(out_data)
                else:
                    out_datasource = source_dataset.datasource
                check_output_datasource(out_datasource)
                if out_dataset_name is None:
                    dest_name = source_dataset.name + "_rectify"
                else:
                    dest_name = out_dataset_name
            dest_name = out_datasource.get_available_dataset_name(dest_name)
            result_track_index_field = result_track_index_field or "TrackIndex"
        java_result = self._jobject.rectify(oj(source_dataset), id_field, str(time_field), float(split_time_milliseconds), oj(out_datasource), str(dest_name), str(result_track_index_field))
        if java_result is not None:
            return out_datasource[dest_name]


class SSCCompilerParameter:
    __doc__ = "\n    编译 SSC 文件的参数\n    "

    def __init__(self):
        self._network_dt = None
        self._node_id = None
        self._edge_id = None
        self._f_node_id = None
        self._t_node_id = None
        self._weight_field = None
        self._rule_field = None
        self._ft_single_way_rule_values = None
        self._tf_single_way_rule_values = None
        self._prohibited_way_rule_values = None
        self._two_way_rule_values = None
        self._edge_name = None
        self._file_path = None
        self._level_field = None
        self._speed_field = None

    @property
    def network_dataset(self):
        """DatasetVector: 网络数据集"""
        return self._network_dt

    def set_network_dataset(self, dataset):
        """
        设置网络数据集

        :param dataset: 网络数据集
        :type dataset: DatasetVetor or str
        :return: 当前对象
        :rtype: SSCCompilerParameter
        """
        dataset = get_input_dataset(dataset)
        if isinstance(dataset, DatasetVector):
            self._network_dt = dataset
            return self
        raise ValueError("required DatasetVector, but is " + str(type(dataset)))

    @property
    def node_id_field(self):
        """str: 网络数据集中标识结点 ID 的字段"""
        return self._node_id

    def set_node_id_field(self, value):
        """
        设置网络数据集标识结点ID的字段

        :param str value: 网络数据集中标识结点 ID 的字段
        :return: self
        :rtype: SSCCompilerParameter
        """
        self._node_id = value
        return self

    @property
    def edge_id_field(self):
        """str: 网络数据集中标志弧段 ID 的字段"""
        return self._edge_id

    def set_edge_id_field(self, value):
        """
        设置网络数据集中标识结点 ID 的字段

        :param str value:  网络数据集中标志弧段 ID 的字段
        :return: self
        :rtype: SSCCompilerParameter
        """
        self._edge_id = value
        return self

    @property
    def f_node_id_field(self):
        """str: 网络数据集中标志弧段起始结点 ID 的字段"""
        return self._f_node_id

    def set_f_node_id_field(self, value):
        """
        设置网络数据集中标志弧段起始结点 ID 的字段

        :param str value: 网络数据集中标志弧段起始结点 ID 的字段
        :return: self
        :rtype: SSCCompilerParameter
        """
        self._f_node_id = value
        return self

    @property
    def t_node_id_field(self):
        """str: 网络数据集中标志弧段起始结点 ID 的字段"""
        return self._t_node_id

    def set_t_node_id_field(self, value):
        """
        设置网络数据集中标志弧段起始结点 ID 的字段

        :param str value:
        :return: self
        :rtype: SSCCompilerParameter
        """
        self._t_node_id = value
        return self

    @property
    def weight_field(self):
        """str: 权重字段"""
        return self._weight_field

    def set_weight_field(self, value):
        """
        设置权重字段

        :param str value: 权重字段
        :return: self
        :rtype: SSCCompilerParameter
        """
        self._weight_field = value
        return self

    @property
    def rule_field(self):
        """str: 网络数据集中表示网络弧段的交通规则的字段"""
        return self._rule_field

    def set_rule_field(self, value):
        """
        设置网络数据集中表示网络弧段的交通规则的字段

        :param str value: 网络数据集中表示网络弧段的交通规则的字段
        :return: self
        :rtype: SSCCompilerParameter
        """
        self._rule_field = value
        return self

    @property
    def ft_single_way_rule_values(self):
        """list[str]: 用于表示正向单行线的字符串的数组"""
        return self._ft_single_way_rule_values

    def set_ft_single_way_rule_values(self, value):
        """
        设置用于表示正向单行线的字符串的数组

        :param value: 用于表示正向单行线的字符串的数组
        :type value: str or list[str]
        :return: self
        :rtype: SSCCompilerParameter
        """
        self._ft_single_way_rule_values = split_input_list_from_str(value)
        return self

    @property
    def tf_single_way_rule_values(self):
        """list[str]: 表示逆向单行线的字符串的数组"""
        return self._tf_single_way_rule_values

    def set_tf_single_way_rule_values(self, value):
        """
        设置表示逆向单行线的字符串的数组

        :param value: 表示逆向单行线的字符串的数组
        :type value: str or list[str]
        :return: self
        :rtype: SSCCompilerParameter
        """
        self._tf_single_way_rule_values = split_input_list_from_str(value)
        return self

    @property
    def prohibited_way_rule_values(self):
        """list[str]: 表示禁行线的字符串的数组"""
        return self._prohibited_way_rule_values

    def set_prohibited_way_rule_values(self, value):
        """
        设置表示禁行线的字符串的数组

        :param value: 表示禁行线的字符串的数组
        :type value: str or list[str]
        :return: self
        :rtype: SSCCompilerParameter
        """
        self._prohibited_way_rule_values = split_input_list_from_str(value)
        return self

    @property
    def two_way_rule_values(self):
        """list[str]: 表示双向通行线的字符串的数组"""
        return self._two_way_rule_values

    def set_two_way_rule_values(self, value):
        """
        设置表示双向通行线的字符串的数组

        :param value: 表示双向通行线的字符串的数组
        :type value: str or list[str]
        :return: self
        :rtype: SSCCompilerParameter
        """
        self._two_way_rule_values = split_input_list_from_str(value)
        return self

    @property
    def edge_name_field(self):
        """str: 弧段的名称字段"""
        return self._edge_name

    def set_edge_name_field(self, value):
        """
        设置弧段的字段名称

        :param str value: 弧段的名称字段。
        :return: self
        :rtype: SSCCompilerParameter
        """
        if value is not None:
            self._edge_name = value
        return self

    @property
    def file_path(self):
        """str: SSC文件的路径"""
        return self._file_path

    def set_file_path(self, value):
        """
        设置 SSC文件的路径

        :param str value: SSC文件的路径。
        :return: self
        :rtype: SSCCompilerParameter
        """
        self._file_path = str(value)
        return self

    @property
    def level_field(self):
        """str: 道路等级字段"""
        return self._level_field

    def set_level_field(self, value):
        """
        设置道路等级字段，取值范围为1-3，必须字段，其中3的道路等级最高（高速路等），1的道路等级最低（乡村道路等）。

        :param str value: 道路等级字段
        :return: self
        :rtype: SSCCompilerParameter
        """
        if value is not None:
            self._level_field = value
        return self

    @property
    def speed_field(self):
        """str: 道路速度字段"""
        return self._speed_field

    def set_speed_field(self, value):
        """
        设置道路速度字段，非必须字段。整数型字段，其中1的道路速度最高（150km/h），2的速度为130km/h，3的速度为100km/h，4的速度为90km/h，
        5的速度为70km/h，6的速度为50km/h，7的速度为30km/h，其他值的速度统一为10km/h

        :param str value: 道路速度字段
        :return: self
        :rtype: SSCCompilerParameter
        """
        if value is not None:
            self._speed_field = value
        return self

    @property
    def _jobject(self):
        """Py4J 映射的 Java 对象"""
        java_object = get_jvm().com.supermap.analyst.networkanalyst.SSCCompilerParameter()
        java_object.setNetworkDataset(oj(self.network_dataset))
        if self.node_id_field is not None:
            java_object.setNodeIDField(str(self.node_id_field))
        else:
            java_object.setNodeIDField(self.network_dataset.child_dataset.get_field_name_by_sign("NODEID"))
        if self.edge_id_field is not None:
            java_object.setEdgeIDField(str(self.edge_id_field))
        else:
            java_object.setEdgeIDField(self.network_dataset.get_field_name_by_sign("EDGEID"))
        if self.f_node_id_field is not None:
            java_object.setFNodeIDField(self.f_node_id_field)
        else:
            java_object.setFNodeIDField(self.network_dataset.get_field_name_by_sign("FNODE"))
        if self.t_node_id_field is not None:
            java_object.setTNodeIDField(self.t_node_id_field)
        else:
            java_object.setTNodeIDField(self.network_dataset.get_field_name_by_sign("TNODE"))
        if self.weight_field is not None:
            java_object.setWeightField(str(self.weight_field))
        if self.rule_field is not None:
            java_object.setRuleField(str(self.rule_field))
        if self.ft_single_way_rule_values is not None:
            java_object.setFTSingleWayRuleValues(to_java_string_array(split_input_list_from_str(self.ft_single_way_rule_values)))
        if self.tf_single_way_rule_values is not None:
            java_object.setTFSingleWayRuleValues(to_java_string_array(split_input_list_from_str(self.tf_single_way_rule_values)))
        if self.prohibited_way_rule_values is not None:
            java_object.setProhibitedWayRuleValues(to_java_string_array(split_input_list_from_str(self.prohibited_way_rule_values)))
        if self.two_way_rule_values is not None:
            java_object.setTwoWayRuleValues(to_java_string_array(split_input_list_from_str(self.two_way_rule_values)))
        if self.edge_name_field is not None:
            java_object.setEdgeNameField(self.edge_name_field)
        if self.file_path is not None:
            java_object.setFilePath(str(self.file_path))
        if self.level_field is not None:
            java_object.setLevelField(str(self.level_field))
        if self.speed_field is not None:
            java_object.setSpeedField(str(self.speed_field))
        return java_object


def compile_ssc_data(parameter, progress=None):
    """
    将网络数据编译为包含捷径信息的SSC文件

    :param SSCCompilerParameter parameter: SSC文件编译参数类。
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 成功返回 True，失败返回 False
    :rtype: bool
    """
    if parameter is None:
        raise ValueError("parameter is none")
    if not isinstance(parameter, SSCCompilerParameter):
        raise ValueError("required SSCCompilerParameter, but " + str(type(parameter)))
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "compile_ssc_data")
                        get_jvm().com.supermap.analyst.networkanalyst.DataCompiler.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            compiler = get_jvm().com.supermap.analyst.networkanalyst.DataCompiler()
            result = compiler.compileSSCData(oj(parameter))
        except Exception:
            import traceback
            log_error(traceback.format_exc())
            result = False

    finally:
        return

    if listener is not None:
        try:
            get_jvm().com.supermap.analyst.networkanalyst.DataCompiler.removeSteppedListener(listener)
        except Exception as e1:
            try:
                log_error(e1)
            finally:
                e1 = None
                del e1

        close_callback_server()
    return result


class FacilityAnalystSetting:
    __doc__ = "\n    设施网络分析环境设置类。 设施网络分析环境设置类。该类用于提供设施网络分析时所需要的所有参数信息。设施网络分析环境设置类的各个参数的设置直接影响分析的结果。\n    "

    def __init__(self):
        self._network_dt = None
        self._tolerance = 0.0
        self._node_id = None
        self._edge_id = None
        self._f_node_id = None
        self._t_node_id = None
        self._weight_fields = None
        self._barrier_node_ids = None
        self._barrier_edge_ids = None
        self._direction_field = None

    @property
    def network_dataset(self):
        """DatasetVector: 网络数据集"""
        return self._network_dt

    def set_network_dataset(self, dt):
        """
        设置网络数据集

        :param dt: 网络数据集
        :type dt: DatasetVetor or str
        :return: self
        :rtype: FacilityAnalystSetting
        """
        if dt is not None:
            dt = get_input_dataset(dt)
            if isinstance(dt, DatasetVector):
                self._network_dt = dt
                return self
            raise ValueError("required DatasetVector, but is " + str(type(dt)))
        else:
            return self

    @property
    def tolerance(self):
        """float: 节点容限"""
        return self._tolerance

    def set_tolerance(self, value):
        """
        设置节点容限

        :param float value: 节点容限
        :return: self
        :rtype: FacilityAnalystSetting
        """
        if value is not None:
            self._tolerance = float(value)
        return self

    @property
    def direction_field(self):
        """str: 流向字段"""
        return self._direction_field

    def set_direction_field(self, value):
        """
        设置流向字段

        :param str value: 流向字段
        :return: self
        :rtype: FacilityAnalystSetting
        """
        if value is not None:
            self._direction_field = str(value)
        else:
            self._direction_field = None
        return self

    @property
    def node_id_field(self):
        """str: 网络数据集中标识结点 ID 的字段"""
        return self._node_id

    def set_node_id_field(self, value):
        """
        设置网络数据集标识结点ID的字段

        :param str value: 网络数据集中标识结点 ID 的字段
        :return: self
        :rtype: FacilityAnalystSetting
        """
        self._node_id = value
        return self

    @property
    def edge_id_field(self):
        """str: 网络数据集中标志弧段 ID 的字段"""
        return self._edge_id

    def set_edge_id_field(self, value):
        """
        设置网络数据集中标识结点 ID 的字段

        :param str value:  网络数据集中标志弧段 ID 的字段
        :return: self
        :rtype: FacilityAnalystSetting
        """
        self._edge_id = value
        return self

    @property
    def f_node_id_field(self):
        """str: 网络数据集中标志弧段起始结点 ID 的字段"""
        return self._f_node_id

    def set_f_node_id_field(self, value):
        """
        设置网络数据集中标志弧段起始结点 ID 的字段

        :param str value: 网络数据集中标志弧段起始结点 ID 的字段
        :return: self
        :rtype: FacilityAnalystSetting
        """
        self._f_node_id = value
        return self

    @property
    def t_node_id_field(self):
        """str: 网络数据集中标志弧段起始结点 ID 的字段"""
        return self._t_node_id

    def set_t_node_id_field(self, value):
        """
        设置网络数据集中标志弧段起始结点 ID 的字段

        :param str value:
        :return: self
        :rtype: FacilityAnalystSetting
        """
        self._t_node_id = value
        return self

    @property
    def weight_fields(self):
        """list[WeightFieldInfo]: 权重字段"""
        return self._weight_fields

    def set_weight_fields(self, value):
        """
        设置权重字段

        :param value: 权重字段
        :type value: list[WeightFieldInfo] or tuple[WeightFieldInfo]
        :return: self
        :rtype: FacilityAnalystSetting
        """
        if self._weight_fields is None:
            self._weight_fields = []
        elif isinstance(value, WeightFieldInfo):
            self._weight_fields.append(value)
        else:
            if isinstance(value, (list, tuple)):
                self._weight_fields.extend(value)
            else:
                raise ValueError("required list[WeightFieldInfo] or WeightFieldInfo")
        return self

    @property
    def barrier_node_ids(self):
        """list[int]: 障碍结点的 ID 列表"""
        return self._barrier_node_ids

    def set_barrier_node_ids(self, value):
        """
        设置障碍结点的 ID 列表

        :param value: 障碍结点的 ID 列表
        :type value: str or list[int]
        :return: self
        :rtype: FacilityAnalystSetting
        """
        if isinstance(value, str):
            self._barrier_node_ids = split_input_int_list_from_str(value)
        else:
            if isinstance(value, (tuple, list)):
                self._barrier_node_ids = list(value)
            else:
                if isinstance(value, int):
                    self._barrier_node_ids = [
                     value]
                else:
                    self._barrier_node_ids = value
        return self

    @property
    def barrier_edge_ids(self):
        """list[int]: 障碍弧段的 ID 列表"""
        return self._barrier_edge_ids

    def set_barrier_edge_ids(self, value):
        """
        设置障碍弧段的 ID 列表

        :param value: 障碍弧段的 ID 列表
        :type value: str or list[int]
        :return: self
        :rtype: FacilityAnalystSetting
        """
        if isinstance(value, str):
            self._barrier_edge_ids = split_input_int_list_from_str(value)
        else:
            if isinstance(value, (tuple, list)):
                self._barrier_edge_ids = list(value)
            else:
                if isinstance(value, int):
                    self._barrier_edge_ids = [
                     value]
                else:
                    self._barrier_edge_ids = value
        return self

    @property
    def _jobject(self):
        java_object = get_jvm().com.supermap.analyst.networkanalyst.FacilityAnalystSetting()
        java_object.setNetworkDataset(oj(self.network_dataset))
        if self.tolerance > 0:
            java_object.setTolerance(float(self.tolerance))
        else:
            if self.node_id_field is not None:
                java_object.setNodeIDField(str(self.node_id_field))
            else:
                java_object.setNodeIDField(self.network_dataset.child_dataset.get_field_name_by_sign("NODEID"))
            if self.edge_id_field is not None:
                java_object.setEdgeIDField(str(self.edge_id_field))
            else:
                java_object.setEdgeIDField(self.network_dataset.get_field_name_by_sign("EDGEID"))
            if self.f_node_id_field is not None:
                java_object.setFNodeIDField(self.f_node_id_field)
            else:
                java_object.setFNodeIDField(self.network_dataset.get_field_name_by_sign("FNODE"))
            if self.t_node_id_field is not None:
                java_object.setTNodeIDField(self.t_node_id_field)
            else:
                java_object.setTNodeIDField(self.network_dataset.get_field_name_by_sign("TNODE"))
        if self.weight_fields is not None:
            java_weight_fields = get_jvm().com.supermap.analyst.networkanalyst.WeightFieldInfos()
            for weight in self.weight_fields:
                java_weight_fields.add(oj(weight))

            java_object.setWeightFieldInfos(java_weight_fields)
        if self.barrier_node_ids is not None:
            java_object.setBarrierNodes(to_java_int_array(split_input_int_list_from_str(self.barrier_node_ids)))
        if self.barrier_edge_ids is not None:
            java_object.setBarrierEdges(to_java_int_array(split_input_int_list_from_str(self.barrier_edge_ids)))
        if self.direction_field is not None:
            java_object.setDirectionField(str(self.direction_field))
        return java_object


def build_network_dataset(lines, points=None, split_mode='NO_SPLIT', tolerance=0.0, line_saved_fields=None, point_saved_fields=None, out_data=None, out_dataset_name=None, progress=None):
    """
    网络数据集是进行网络分析的数据基础。网络数据集由两个子数据集（一个线数据集和一个点数据集）构成，分别存储了网络模型的弧段和结点，
    并且描述了弧段与弧段、弧段与结点、结点与结点间的空间拓扑关系。

    此方法提供根据单个线数据集或多个线和点数据集构建网络数据集。如果用户的数据集已经有正确的网络关系，可以直接通过 :py:meth:`build_network_dataset_known_relation` 快
    速的构建一个网络数据集。

    构建的网络数据集，可以通过 :py:meth:`validate_network_dataset` 检查网络拓扑关系是否正确。

    :param lines: 用于构建网络数据集的线数据集，必须至少有一个线数据集。
    :type lines: DatasetVector or list[DatasetVector]
    :param points: 用于构建网络数据集的点数据集。
    :type points: DatasetVector or list[DatasetVector]
    :param split_mode: 打断模式，默认为不打断
    :type split_mode: NetworkSplitMode
    :param float tolerance: 节点容限
    :param line_saved_fields: 线数据集中需要保留的字段
    :type line_saved_fields: str or list[str]
    :param point_saved_fields: 点数据集中需要保留的字段。
    :type point_saved_fields: str or list[str]
    :param out_data: 保留结果网络数据集的数据源对象
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果网络数据集
    :rtype: DatasetVector
    """
    if isinstance(lines, (list, tuple)):
        line_dts = list(filter((lambda dt: dt.type is DatasetType.LINE), list((get_input_dataset(item) for item in lines))))
    else:
        line_dts = list(filter((lambda dt: dt.type is DatasetType.LINE), [get_input_dataset(lines)]))
    if not line_dts:
        raise ValueError("have no valid line dataset")
    else:
        if points is not None:
            if isinstance(points, (list, tuple)):
                point_dts = list(filter((lambda dt: dt.type is DatasetType.POINT), list((get_input_dataset(item) for item in points))))
            else:
                point_dts = [
                 get_input_dataset(points)]
        else:
            point_dts = None
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = line_dts[0].datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            dest_name = line_dts[0].name + "_Network"
        else:
            dest_name = out_dataset_name
        dest_name = out_datasource.get_available_dataset_name(dest_name)
        listener = None
        try:
            try:
                if progress is not None:
                    if safe_start_callback_server():
                        try:
                            listener = ProgressListener(progress, "build_network_dataset")
                            get_jvm().com.supermap.analyst.networkanalyst.NetworkBuilder.addSteppedListener(listener)
                        except Exception as e:
                            try:
                                close_callback_server()
                                log_error(e)
                                listener = None
                            finally:
                                e = None
                                del e

                java_line_dts = to_java_datasetvector_array(line_dts)
                java_point_dts = to_java_datasetvector_array(point_dts)
                network_builder_func = get_jvm().com.supermap.analyst.networkanalyst.NetworkBuilder.buildNetwork
                java_result = network_builder_func(java_line_dts, java_point_dts, to_java_string_array(split_input_list_from_str(line_saved_fields)), to_java_string_array(split_input_list_from_str(point_saved_fields)), oj(out_datasource), str(dest_name), oj(NetworkSplitMode._make(split_mode, "NO_SPLIT")), float(tolerance))
            except:
                import traceback
                log_error(traceback.format_exc())
                java_result = None

        finally:
            return

        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.networkanalyst.NetworkBuilder.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if java_result is not None:
            result_dt = out_datasource[dest_name]
        else:
            result_dt = None
    if out_data is not None:
        return try_close_output_datasource(result_dt, out_datasource)
    return result_dt


def build_network_dataset_known_relation(line, point, edge_id_field, from_node_id_field, to_node_id_field, node_id_field, out_data=None, out_dataset_name=None, progress=None):
    """
    根据点、线数据及其已有的表达弧段结点拓扑关系的字段，构建网络数据集。
    当已有的线、点数据集中的线、点对象分别对应着待构建网络的弧段和结点，并具有描述二者空间拓扑关系的信息，即线数据集含有弧段 ID、弧段
    起始结点 ID 和终止结点 ID 字段，点数据集含有点对象的结点 ID 字段时，可以采用本方法构建网络数据集。

    使用此方式构建网络数据集成功后，结果对象数与源数据的对象数一致，即线数据中一个线对象作为一个弧段写入，点数据中一个点对象作为一个
    结点写入，并且保留点、线数据集的所有非系统字段到结果数据集中。

    例如，对于用于建立管网而采集的管线、管点数据，管线和管点均使用唯一固定编码来标识。管网的特点之一是管点只位于管线的两端，因此管点
    对应了待构建管网的所有结点，管线对应了待构建管网的所有弧段，不需要在管线与管线相交处打断。在管线数据中，记录了管线对象两端的管点
    信息，即起始管点编码和终止管点编码，也就是说管线和管点数据中已经蕴含了二者空间拓扑关系的信息，因此适合使用此方法构建网络数据集。

    注意，使用此方式构建的网络数据集的弧段 ID、弧段起始结点 ID、弧段终止结点 ID 和结点 ID 字段即为调用此方法时指定的字段，而不再
    是 SmEdgeID、SmFNode、SmTNode、SmNodeID 等系统字段。具体可以通过 DatasetVector 的 :py:meth:`.DatasetVector.get_field_name_by_sign` 方法获取到相应的字段。

    :param line: 用于构建网络数据集的线数据集
    :type line: str or DatasetVector
    :param point: 用于构建网络数据集的点数据集
    :type point: str or DatasetVector
    :param str edge_id_field: 指定的线数据集中表示弧段 ID 的字段。如果指定为 null 或空字符串，或指定的字段不存在，则自动使用 SMID 作为弧段 ID。
                                仅支持 16 位整型、32 位整型字段。
    :param str from_node_id_field: 指定的线数据集中表示弧段的起始结点 ID 的字段。仅支持 16 位整型、32 位整型字段。
    :param str to_node_id_field: 指定的线数据集中表示弧段的终止结点 ID 的字段。仅支持 16 位整型、32 位整型字段。
    :param str node_id_field: 指定的点数据集中表示结点 ID 的字段。仅支持 16 位整型、32 位整型字段。
    :param out_data: 保留结果网络数据集的数据源对象
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果网络数据集
    :rtype: DatasetVector
    """
    source_line_dt = get_input_dataset(line)
    if not isinstance(source_line_dt, DatasetVector):
        raise ValueError("line required DatasetVector, but is " + str(type(source_line_dt)))
    else:
        source_point_dt = get_input_dataset(point)
        if not isinstance(source_point_dt, DatasetVector):
            raise ValueError("point required DatasetVector, but is " + str(type(source_point_dt)))
        else:
            if out_data is not None:
                out_datasource = get_output_datasource(out_data)
            else:
                out_datasource = source_line_dt.datasource
            check_output_datasource(out_datasource)
            if out_dataset_name is None:
                dest_name = source_line_dt.name + "_Network"
            else:
                dest_name = out_dataset_name
        dest_name = out_datasource.get_available_dataset_name(dest_name)
        listener = None
        try:
            try:
                if progress is not None:
                    if safe_start_callback_server():
                        try:
                            listener = ProgressListener(progress, "build_network_dataset_known_relation")
                            get_jvm().com.supermap.analyst.networkanalyst.NetworkBuilder.addSteppedListener(listener)
                        except Exception as e:
                            try:
                                close_callback_server()
                                log_error(e)
                                listener = None
                            finally:
                                e = None
                                del e

                network_builder_func = get_jvm().com.supermap.analyst.networkanalyst.NetworkBuilder.buildNetwork
                java_result = network_builder_func(oj(source_line_dt), oj(source_point_dt), str(edge_id_field), str(from_node_id_field), str(to_node_id_field), str(node_id_field), oj(out_datasource), str(dest_name))
            except:
                import traceback
                log_error(traceback.format_exc())
                java_result = None

        finally:
            return

        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.networkanalyst.NetworkBuilder.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if java_result is not None:
            result_dt = out_datasource[dest_name]
        else:
            result_dt = None
    if out_data is not None:
        return try_close_output_datasource(result_dt, out_datasource)
    return result_dt


def append_to_network_dataset(network_dataset, appended_datasets, progress=None):
    """
    向已有的网络数据集追加数据，可以追加点、线或网络。
    网络数据集一般由线数据（以及点数据）构建而成。一旦构建网络的数据发生变化，原有网络就会过时，如果不及时更新网络，就可能影响分析
    结果的正确性。通过将新增数据追加到原有网络的方式，可以不必重新构建网络而得到较新的网络。如下图所示，某区域新建了若干道路（红色线）
    ，将这些道路抽象为线数据，追加到扩建之前所构建的网络上，从而更新了路网。

    .. image:: ../image/AppendToNetwork.png

    此方法支持向已有网络追加点、线以及网络数据集，并且可以同时追加多个相同或不同类型的数据集，例如，同时追加一份点数据和两份线数据。
    注意，如果追加的数据具有多种类型，系统将按照先追加网络，再追加线，最后追加点的顺序来依次追加。下面分别介绍向网络中追加点、线和网络的方式和规则。

    * 向已有网络追加点:

      点被追加到已有网络后，将成为网络中新的结点。向已有网络追加点时，需要注意以下要点:

      1. 待追加的点必须在已有网络的弧段上。追加后，在弧段上该点位置处增加新的结点，该弧段将自动在新增结点处断开为两条弧段，如下图中的点 a、点 d。如果待追加的点不在网络上，即不在弧段上，也不与结点重叠，将被忽略，不会追加到网络上，因为孤立结点在网络中并无地学意义。下图中的点 b 就属于这种情况。
      2. 如果待追加的点与已有网络的结点重叠，则将待追加点与重叠结点合并，如下图中的点 c。

      .. image:: ../image/AppendPointsToNetwork.png

    * 向已有网络追加线

      线被追加到已有网络后，将成为网络中新的弧段，并且在线的端点、与其他线（或弧段）的交点处打断并增加新的结点。向已有网络追加点时，需要注意以下要点：

      1. 待追加的线不能存在与已有网络弧段重叠或部分重叠，否则会导致追加后的网络存在错误。

    * 向已有网络追加另一网络

      将一个网络追加到已有网络后，二者将成为一个网络，如下图所示。注意，与追加线相同，向已有网络中追加网络时，需要确保这两个网络不存在
      弧段的重叠或部分重叠，否则会导致追加后的网络存在错误。

      .. image:: ../image/AppendChildNet_1.png

      待追加网络与被追加网络叠加出现弧段相交的情形时，在相交处会添加新的结点，从而建立新的拓扑关系。

      .. image:: ../image/AppendChildNet_3.png

      网络的连通性不影响网络的追加。如下例中，将待追加网络追加到原始网络后，结果是一个包含两个子网的网络数据集，并且两子网不连通。

      .. image:: ../image/AppendChildNet_2.png

    * 注意:

      1. 该方法将直接修改被追加的网络数据集，不会生成新的网络数据集。
      2. 待追加的点、线或网络数据集必须与被追加的网络数据集具有相同的坐标系。
      3. 待追加的点、线或 网络数据集中，如果存在与网络数据集相同（名称和类型都必须相同）的属性字段，那么这些属性值会自动保留到追加后
         的网络数据集中；如果不存在相同的字段，则不保留。其中，点数据集、网络数据集的结点数据集的属性，保留到被追加网络的结点属性表
         中；线数据集的属性，保留到被追加网络的弧段属性表中。

    :param network_dataset: 被追加的网络数据集
    :type network_dataset: DatasetVector or str
    :param appended_datasets: 指定的待追加的数据，可以是点、线或网络数据集。
    :type appended_datasets: list[DatasetVector]
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 是否追加成功。如果成功，返回 True，否则返回 False.
    :rtype: bool
    """
    source_network = get_input_dataset(network_dataset)
    if source_network.is_readonly():
        raise ValueError("network dataset is readonly")
    if not isinstance(appended_datasets, (list, tuple)):
        appended_datasets = [
         appended_datasets]
    datasets = list(filter((lambda dt: dt is not None and (dt.type is DatasetType.LINE or dt.type is DatasetType.REGION)), list((get_input_dataset(p) for p in appended_datasets))))
    if not datasets:
        raise ValueError("hava no valid point or line dataset")
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "append_to_network_dataset")
                        get_jvm().com.supermap.analyst.networkanalyst.NetworkBuilder.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_function = get_jvm().com.supermap.analyst.networkanalyst.NetworkBuilder.appendToNetwork
            result = java_function(oj(source_network), to_java_datasetvector_array(datasets))
        except Exception:
            import traceback
            log_error(traceback.format_exc())
            result = False

    finally:
        return

    if listener is not None:
        try:
            get_jvm().com.supermap.analyst.networkanalyst.NetworkBuilder.removeSteppedListener(listener)
        except Exception as e1:
            try:
                log_error(e1)
            finally:
                e1 = None
                del e1

        close_callback_server()
    return result


def build_facility_network_directions(network_dataset, source_ids, sink_ids, ft_weight_field='SmLength', tf_weight_field='SmLength', direction_field='Direction', node_type_field='NodeType', progress=None):
    """
    根据指定网络数据集中源与汇的位置，为网络数据集创建流向。创建流向以后的网络数据集才可以进行各种设施网络分析。
    设施网络是具有方向的网络，因此，在创建网络数据集之后，必须为其创建流向，才能够用于进行各种设施网络路径分析、连通性分析、上下游追踪等。

    流向是指网络中资源流动的方向。网络中的流向由源和汇决定：资源总是从源点流出，流向汇点。该方法通过给定的源和汇，以及设施网络分析参数
    设置为网络数据集创建流向。创建流向成功后，会在网络数据集中写入两方面的信息：流向和结点类型。

    * 流向

      流向信息将写入网络数据集的子线数据集的流向字段中，如果不存在则会创建该字段。

      流向字段的值共有四个：0,1,2,3，其含义如下图所示。以线段 AB 为例：

      0 代表流向与数字化方向相同。线段 AB 的数字化方向为 A-->B，且 A 为源点，因此 AB 的流向为从 A 流到 B，即与其数字化方向相同。

      1 代表流向与数字化方向相反。线段 AB 的数字化方向为 A-->B，且 A 为汇点，因此 AB 的流向为从 B 流向 A，即与其数字化方向相反。

      2 代表无效方向，也称不确定流向。A 和 B 均为源点，则资源既可以从 A 流向 B，又可以从 B 流向 A，这就构成了一个无效的流向。

      3 代表不连通边，也称未初始化方向。线段 AB 与源点、汇点所在的结点不连通，则称为不连通边。

      .. image:: ../image/BuildFacilityNetworkDirections_1.png

    * 结点类型

      建立流向后，系统还会将结点类型信息写入指定的网络数据集的子点数据集的结点类型字段中。结点类型分为源点、汇点和普通结点。
      下表列出了结点类型字段的值及其含义：

      .. image:: ../image/BuildFacilityNetworkDirections_2.png

    :param network_dataset: 待创建流向的网络数据集，网络数据集必须可修改。
    :type network_dataset: DatasetVector or str
    :param source_ids: 源对应的网络结点 ID 数组。源与汇都是用来建立网络数据集的流向的。网络数据集的流向与源和汇的位置决定。
    :type source_ids: list[int] or tuple[int]
    :param sink_ids: 汇 ID 数组。汇对应的网络结点 ID 数组。源与汇都是用来建立网络数据集的流向的。网络数据集的流向与源和汇的位置决定。
    :type sink_ids: list[int] or tuple[int]
    :param str ft_weight_field: 正向权值字段或字段表达式
    :param str tf_weight_field: 反向权值字段或字段表达式
    :param str direction_field: 流向字段，用于保存网络数据集的流向信息
    :param str node_type_field: 结点类型字段名称，结点类型分为源结点、交汇结点、普通结点。该字段是网络结点数据集中的字段，如果不存在则创建该字段。
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 创建成功返回 true，否则 false
    :rtype: bool
    """
    network_dataset = get_input_dataset(network_dataset)
    if not isinstance(network_dataset, DatasetVector):
        raise ValueError("network_dataset required DatasetVector, but " + str(type(network_dataset)))
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "build_facility_network_directions")
                        get_jvm().com.supermap.analyst.networkanalyst.NetworkBuilder.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_function = get_jvm().com.supermap.analyst.networkanalyst.NetworkBuilder.buildFacilityNetworkDirections
            facility_analyst_setting = FacilityAnalystSetting()
            facility_analyst_setting.set_network_dataset(network_dataset)
            facility_analyst_setting.set_weight_fields([WeightFieldInfo("Length", ft_weight_field, tf_weight_field)])
            facility_analyst_setting.set_direction_field(direction_field)
            java_result = java_function(oj(facility_analyst_setting), to_java_int_array(split_input_int_list_from_str(source_ids)), to_java_int_array(split_input_int_list_from_str(sink_ids)), str("Length"), str(node_type_field))
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = False

    finally:
        return

    if listener is not None:
        try:
            get_jvm().com.supermap.analyst.networkanalyst.NetworkBuilder.removeSteppedListener(listener)
        except Exception as e1:
            try:
                log_error(e1)
            finally:
                e1 = None
                del e1

        close_callback_server()
    return java_result


def build_facility_network_hierarchies(network_dataset, source_ids, sink_ids, direction_field, is_loop_valid, ft_weight_field='SmLength', tf_weight_field='SmLength', hierarchy_field='Hierarchy', progress=None):
    """
    为具有流向的网络数据集创建等级，并在指定的等级字段中写入网络数据集的等级信息。

    为网络数据集建立等级，首先，该网络数据集必须已经建立了流向，即建立等级的方法所操作的网络数据集必须具有流向信息。

    等级字段中以整数的形式记录等级，数值从 1 开始，等级越高数值越小，如河流建立等级后，一级河流的等级记录为 1，二级河流的等级记录
    为 2，以此类推。注意，值为 0 表示未能确定等级，通常是由于该弧段为不连通弧段导致。

    :param network_dataset: 待创建等级的网络数据集，网络数据集必须可修改。
    :type network_dataset: DatasetVector or str
    :param source_ids: 源 ID 数组
    :type source_ids: list[int]
    :param sink_ids: 汇 ID 数组
    :type sink_ids: list[int]
    :param str direction_field: 流向字段
    :param bool is_loop_valid: 指定环路是否有效。当该参数为 true 时，环路有效；而当参数为 false 时，环路无效。
    :param str ft_weight_field: 正向权值字段或字段表达式
    :param str tf_weight_field: 反向权值字段或字段表达式
    :param hierarchy_field: 给定的等级字段名称，用于存储等级信息。
    :type hierarchy_field: str
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 创建成功返回 true，否则 false
    :rtype: bool
    """
    network_dataset = get_input_dataset(network_dataset)
    if not isinstance(network_dataset, DatasetVector):
        raise ValueError("network_dataset required DatasetVector, but " + str(type(network_dataset)))
    java_result = False
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "build_facility_network_hierarchies")
                        get_jvm().com.supermap.analyst.networkanalyst.NetworkBuilder.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            facility_analyst_setting = FacilityAnalystSetting()
            facility_analyst_setting.set_network_dataset(network_dataset)
            facility_analyst_setting.set_weight_fields([WeightFieldInfo("Length", ft_weight_field, tf_weight_field)])
            facility_analyst_setting.set_direction_field(direction_field)
            java_function = get_jvm().com.supermap.analyst.networkanalyst.NetworkBuilder.buildFacilityNetworkHierarchies
            java_result = java_function(oj(facility_analyst_setting), to_java_int_array(split_input_int_list_from_str(source_ids)), to_java_int_array(split_input_int_list_from_str(sink_ids)), "Length", str(hierarchy_field), parse_bool(is_loop_valid))
        except Exception:
            import traceback
            log_error(traceback.format_exc())
            java_result = False

    finally:
        return

    if listener is not None:
        try:
            get_jvm().com.supermap.analyst.networkanalyst.NetworkBuilder.removeSteppedListener(listener)
        except Exception as e1:
            try:
                log_error(e1)
            finally:
                e1 = None
                del e1

        close_callback_server()
    return java_result


class FacilityAnalystResult:
    __doc__ = "\n    设施网络分析结果类。该类用于获取查找源和汇、上下游追踪以及查找路径等设施网络分析的结果，包括结果弧段 ID 数组、结果结点 ID 数组以及耗费。\n    "

    def __init__(self, java_object):
        self._nodes = java_array_to_list(java_object.getNodes())
        self._edges = java_array_to_list(java_object.getEdges())
        self._cost = java_object.getCost()

    @property
    def nodes(self):
        """list[int]: 设施网络分析结果中的结点 ID 数组。
                      对于不同的设施网络分析功能，该方法的返回值含义有所不同:

                      - 查找源: 该值为分析弧段或结点到达源的最小耗费路径所包含的结点的结点 ID 数组。
                      - 查找汇: 该值为分析弧段或结点到达汇的最小耗费路径所包含的结点的结点 ID 数组。
                      - 上游追踪: 该值为分析弧段或结点的上游所包含的结点的结点 ID 数组。
                      - 下游追踪: 该值为分析弧段或结点的下游所包含的结点的结点 ID 数组。
                      - 路径分析: 该值为查找到的最小耗费路径所经过的结点的结点 ID 数组。
                      - 上游路径分析: 该值为查找到的上游最小耗费路径所经过的结点的结点 ID 数组。
                      - 下游路径分析: 该值为查找到的下游最小耗费路径所经过的结点的结点 ID 数组。
        """
        return self._nodes

    @property
    def edges(self):
        """list[int]: 设施网络分析结果中的弧段 ID 数组。
                      对于不同的设施网络分析功能，该方法的返回值含义有所不同:

                      - 查找源: 该值为分析弧段或结点到达源的最小耗费路径所包含的弧段的弧段 ID 数组。
                      - 查找汇: 该值为分析弧段或结点到达汇的最小耗费路径所包含的弧段的弧段 ID 数组。
                      - 上游追踪: 该值为分析弧段或结点的上游所包含的弧段的弧段 ID 数组。
                      - 下游追踪: 该值为分析弧段或结点的下游所包含的弧段的弧段 ID 数组。
                      - 路径分析: 该值为查找到的最小耗费路径所经过的弧段的弧段 ID 数组。
                      - 上游路径分析: 该值为查找到的上游最小耗费路径所经过的弧段的弧段 ID 数组。
                      - 下游路径分析: 该值为查找到的下游最小耗费路径所经过的弧段的弧段 ID 数组。
        """
        return self._edges

    @property
    def cost(self):
        """float: 设施网络分析结果中的耗费。
                  对于不同的设施网络分析功能，该方法的返回值含义有所不同:

                  - 查找源: 该值为分析弧段或结点到达源的最小耗费路径的耗费。
                  - 查找汇: 该值为分析弧段或结点到达汇的最小耗费路径耗费。
                  - 上游追踪: 该值为分析弧段或结点的上游所包含的弧段的总耗费。
                  - 下游追踪: 该值为分析弧段或结点的下游所包含的弧段的总耗费。
                  - 路径分析: 该值为查找到的最小耗费路径的耗费。
                  - 上游路径分析: 该值为查找到的上游最小耗费路径的耗费。
                  - 下游路径分析: 该值为查找到的下游最小耗费路径的耗费。
        """
        return self._cost


class BurstAnalystResult:
    __doc__ = "爆管分析结果类。爆管分析结果返回关键设施点、普通设施点以及弧段。"

    def __init__(self, java_object):
        self._edges = java_array_to_list(java_object.getEdges())
        self._critical_nodes = java_array_to_list(java_object.getCriticalNodes())
        self._normal_nodes = java_array_to_list(java_object.getNormalNodes())

    @property
    def edges(self):
        """list[int]: 上下游影响爆管位置的弧段和受爆管位置影响的弧段。是从爆管位置进行双向搜索关键设施点和普通设施点遍历到的弧段。"""
        return self._edges

    @property
    def critical_nodes(self):
        """list[int]: 爆管分析中影响爆管位置上下游的关键设施点。
                      关键设施点包括两种设施点：

                       1. 爆管位置上游中所有对爆管位置直接影响的设施点。
                       2. 下游中受爆管位置直接影响且有流出（即出度大于0）的设施点。
        """
        return self._critical_nodes

    @property
    def normal_nodes(self):
        """list[int]: 爆管分析中受爆管位置影响的普通设施点。
                      普通设施点包括三种设施点:

                       1. 受爆管位置直接影响且没有流出（出度为0）的设施点。
                       2. 每个上游关键设施点的流出弧段直接影响的所有设施点A（除去所有关键设施点），且设施点A需要满足，上游关键设施点
                          到设施点A的影响弧段与上下游关键设施点的影响弧段有公共部分。
                       3. 爆管位置下游受爆管位置直接影响的设施点A（关键设施点2和普通设施点1），设施点A上游中直接影响设施点A的设施
                          点B（除去所有关键设施点），且需要满足，设施点A到设施点B的影响弧段与上下游关键设施点的影响弧段有公共部分。

        """
        return self._normal_nodes


class FacilityAnalyst(JVMBase):
    __doc__ = "设施网络分析类。\n\n       设施网络分析类。它是网络分析功能类之一，主要用于进行各类连通性分析和追踪分析。\n\n       设施网络是具有方向的网络。即介质（水流、电流等）会根据网络本身的规则在网络中流动。\n\n       设施网络分析的前提是已经建立了用于设施网络分析的数据集，建立用于设施网络分析的数据集的基础是建立网络数据集，在此基础上利用\n       :py:meth:`build_facility_network_directions` 方法赋予网络数据集特有的用于进行设施网络分析的数据信息，也就是为网络数据集\n       建立流向，使原有的网络数据集具有了能够进行设施网络分析的最基本的条件 ，此时，就可以进行各种设施网络分析了。如果你的设施网络\n       具有等级信息，还可以进一步使用 :py:meth:`build_facility_network_hierarchies` 方法添加等级信息。\n    "

    def __init__(self, analyst_setting):
        """

        :param analyst_setting: 设置网络分析的环境。
        :type analyst_setting: FacilityAnalystSetting
        """
        JVMBase.__init__(self)
        self._analyst_setting = None
        self._is_load = False
        self.set_analyst_setting(analyst_setting)

    def _make_java_object(self):
        self._java_object = self._jvm.com.supermap.analyst.networkanalyst.FacilityAnalyst()
        return self._java_object

    def set_analyst_setting(self, value):
        """
        设置设施网络分析的环境。

        设施网络分析环境参数的设置，直接影响到设施网络分析的结果。设施网络分析所需要的参数包括：用于进行设施网络分析的数据集（ 即
        建立了流向的网络数据集或者同时建立了流向和等级的网络数据集，也就是说该方法对应的 :py:class:`FacilityAnalystSetting` 所指
        定的网络数据集必须有流向或者流向和等级信息）、结点 ID 字段、弧段 ID 字段、弧段起始结点 ID 字段、弧段终止结点 ID 字段、权
        值信息、点到弧段的距离容限、障碍结点、障碍弧段、流向等。

        :param value: 设施网络分析环境参数
        :type value: FacilityAnalystSetting
        :return: self
        :rtype: FacilityAnalyst
        """
        if isinstance(value, FacilityAnalystSetting):
            self._analyst_setting = value
            self._jobject.setAnalystSetting(oj(value))
            return self
        raise ValueError("required FacilityAnalystSetting, but " + str(type(value)))

    @property
    def analyst_setting(self):
        """FacilityAnalystSetting: 设施网络分析的环境"""
        return self._analyst_setting

    def load(self):
        """
        根据设施网络分析环境设置加载设施网络模型。

        注意，出现以下两种情况都必须重新调用 load 方法来加载网络模型，然后再进行分析。
             - 对设施网络分析环境设置对象的参数进行了修改，需要重新调用该方法，否则所作修改不会生效从而导致分析结果错误；
             - 对所使用的网络数据集进行了任何修改，包括修改网络数据集中的数据、替换数据集等，都需要重新加载网络模型，否则分析可能出错。

        :return: 用于指示加载设施网络模型是否成功。如果成功返回 true，否则返回 false。
        :rtype: bool
        """
        if self._is_load:
            self._java_object.dispose()
        self._is_load = self._jobject.load()
        return self._is_load

    def _load_internal(self):
        if self._is_load:
            return
        self._is_load = self.load()
        if not self._is_load:
            raise RuntimeError("Failed load network analyst model")

    def is_load(self):
        """
        判断网络数据集模型是否加载。

        :return: 网络数据集模型加载返回 True，否则返回 False
        :rtype: bool
        """
        return self._is_load

    def check_loops(self):
        """
        检查网络环路，返回构成环路的弧段 ID 数组。

        施网络中，环路是指两条或两条以上流向值为 2（即不确定流向）的弧段构成的闭合路径。这意味着环路必须同时满足以下两个条件：

         1. 是由至少两条弧段构成的闭合路径；
         2. 构成环路的弧段的流向均为 2，即不确定流向。

        有关流向请参阅 :py:meth:`build_facility_network_directions` 方法。

        下图是设施网络的一部分，使用不同的符号显示网络弧段的流向。对该网络进行环路检查，检查出两个环路，即图中的红色闭合路径。
        而右上方有一条流向为 2 的弧段，由于它未与其他流向同样为 2 的弧段构成闭合路径，因此不是环路：

        .. image:: ../image/CheckLoops.png

        :return: 构成环路的弧段 ID 数组。
        :rtype: list[int]
        """
        self._load_internal()
        return java_array_to_list(self._jobject.checkLoops())

    def burst_analyse(self, source_nodes, edge_or_node_id, is_uncertain_direction_valid=False, is_edge_id=True):
        """
        双向爆管分析，通过指定爆管弧段，查找爆管弧段上下游中对爆管位置产生直接影响的结点以及受爆管位置直接影响的结点

        :param source_nodes: 指定的设施结点 ID 数组。不能为空。
        :type source_nodes: list[int] or tuple[int]
        :param int edge_or_node_id:  指定的弧段 ID 或 结点 ID，爆管位置。
        :param bool is_uncertain_direction_valid: 指定不确定流向是否有效。指定为 true，表示不确定流向有效，遇到不确定流向时分析
                                                  继续进行；指定为 false，表示不确定流向无效，遇到不确定流向将停止在该方向上继
                                                  续查找。流向字段的值为 2 时代表该弧段的流向为不确定流向。
        :param bool is_edge_id: edge_or_node_id 是否表示弧段ID，True 表示为弧段ID，False表示为结点ID。
        :return: 爆管分析结果
        :rtype: BurstAnalyseResult
        """
        self._load_internal()
        if is_edge_id:
            func = self._jobject.burstAnalyseFromEdge
        else:
            func = self._jobject.burstAnalyseFromNode
        java_result = func(to_java_int_array(source_nodes), int(edge_or_node_id), parse_bool(is_uncertain_direction_valid))
        if java_result is not None:
            return BurstAnalystResult(java_result)

    def find_common_ancestors(self, edge_or_node_ids, is_uncertain_direction_valid=False, is_edge_ids=True):
        """
        根据给定的弧段 ID 数组或结点 ID 数组，查找这些弧段的共同上游弧段，返回弧段 ID 数组。
        共同上游是指多个结点（或弧段）的公共上游网络。该方法用于查找多条弧段的共同上游弧段，即取这些弧段的各自上游弧段的交集部分，结果返回这些弧段的弧段 ID。

        如下图所示，流向如图中的箭头所示的方向，前两幅图分别是对结点 1 和结点 2 进行上游追踪的结果，查找出各自的上游弧段（绿色），第
        三幅图则是对结点 1 和结点 2 查找共同上游弧段（橙色），容易看出，结点 1 和结点 2 的共同上游弧段，就是它们各自的上游弧段的交集。

        .. image:: ../image/CommonAncestors.png

        :param edge_or_node_ids: 指定的弧段 ID 数组 或 结点 ID 数组
        :type edge_or_node_ids: list[int] or tuple[int]
        :param bool is_uncertain_direction_valid: 指定不确定流向是否有效。指定为 true，表示不确定流向有效，遇到不确定流向时分析
                                                  继续进行；指定为 false，表示不确定流向无效，遇到不确定流向将停止在该方向上继
                                                  续查找。流向字段的值为 2 时代表该弧段的流向为不确定流向。
        :param bool is_edge_ids: edge_or_node_ids 是否表示弧段ID，True 表示为弧段ID，False表示为结点ID。
        :return: 弧段 ID 数组
        :rtype: list[int]
        """
        self._load_internal()
        if is_edge_ids:
            func = self._jobject.findCommonAncestorsFromEdges
        else:
            func = self._jobject.findCommonAncestorsFromNodes
        java_result = func(to_java_int_array(edge_or_node_ids), parse_bool(is_uncertain_direction_valid))
        return java_array_to_list(java_result)

    def find_common_catchments(self, edge_or_node_ids, is_uncertain_direction_valid=False, is_edge_ids=True):
        """
        根据指定的结点 ID 数组或弧段 ID 数组，查找这些结点的共同下游弧段，返回弧段 ID 数组。

        共同下游是指多个结点（或弧段）的公共下游网络。该方法用于查找多个结点的共同下游弧段，即取这些结点的各自下游弧段的交集部分，结果返回这些弧段的弧段 ID。

        如下图所示，流向如图中的箭头所示的方向，前两幅图分别是对结点 1 和结点 2 进行下游追踪的结果，查找出各自的下游弧段（绿色），第
        三幅图则是对结点 1 和结点 2 查找共同下游弧段（橙色），容易看出，结点 1 和结点 2 的共同下游弧段，就是它们各自的下游弧段的交集。

        .. image:: ../image/CommonCatchments.png

        :param edge_or_node_ids: 指定的结点 ID 数组或弧段 ID 数组
        :type edge_or_node_ids: list[int]
        :param bool is_uncertain_direction_valid: 指定不确定流向是否有效。指定为 true，表示不确定流向有效，遇到不确定流向时分析
                                                  继续进行；指定为 false，表示不确定流向无效，遇到不确定流向将停止在该方向上继
                                                  续查找。流向字段的值为 2 时代表该弧段的流向为不确定流向。
        :param bool is_edge_ids: edge_or_node_ids 是否表示弧段ID，True 表示为弧段ID，False表示为结点ID。
        :return: 给定结点的共同下游的弧段 ID 数组
        :rtype: list[int]
        """
        self._load_internal()
        if is_edge_ids:
            func = self._jobject.findCommonCatchmentsFromEdges
        else:
            func = self._jobject.findCommonCatchmentsFromNodes
        java_result = func(to_java_int_array(edge_or_node_ids), parse_bool(is_uncertain_direction_valid))
        return java_array_to_list(java_result)

    def find_connected_edges(self, edge_or_node_ids, is_edge_ids=True):
        """
        根据给定的结点 ID 数组或弧段 ID 数组，查找与这些弧段（或结点）相连通的弧段，返回弧段 ID 数组。
        该方法用于查找与给定弧段（或结点）相连通的弧段，查找出连通弧段后，可根据网络拓扑关系，即弧段的起始结点、终止结点查询出相应的连通结点。

        :param edge_or_node_ids: 结点 ID 数组或弧段 ID 数组
        :type edge_or_node_ids: list[int] or tuple[int]
        :param bool is_edge_ids: edge_or_node_ids 是否表示弧段ID，True 表示为弧段ID，False表示为结点ID。
        :return: 给定结点的共同下游的弧段 ID 数组
        :rtype: list[int]
        """
        self._load_internal()
        if is_edge_ids:
            func = self._jobject.findConnectedEdgesFromEdges
        else:
            func = self._jobject.findConnectedEdgesFromNodes
        return java_array_to_list(func(to_java_int_array(edge_or_node_ids)))

    def find_critical_facilities_down(self, source_node_ids, edge_or_node_id, is_uncertain_direction_valid=False, is_edge_id=True):
        """
        下游关键设施查找，即查找给定弧段的关键下游设施结点，返回关键设施结点 ID 数组及给定弧段影响到的下游弧段 ID 数组。
        在进行下游关键设施查找分析时，我们将设施网络的结点划分为普通结点和设施结点两类，其中设施结点认为是能够影响网络连通性的结点，
        例如供水管网中的阀门；普通结点是不影响网络连通性的结点，如供水管网中的消防栓或三通等。

        下游关键设施查找分析将从给定的设施结点中筛选出关键结点，这些关键结点是分析弧段与其下游保持连通性的最基本的结点，也就是说，
        关闭这些关键结点后，分析结点与下游无法连通。同时，该分析的结果还包含给定弧段影响的下游弧段并集。

        关键设施结点的查找方式可以归纳为：从分析弧段出发，向它的下游查找，每个方向上遇到的第一个设施结点，就是要查找的关键设施结点。

        :param source_node_ids: 指定的设施结点 ID 数组。不能为空。
        :type source_node_ids: list[int] or tuple[int]
        :param int edge_or_node_id: 指定的分析弧段 ID 或结点 ID
        :param bool is_uncertain_direction_valid: 指定不确定流向是否有效。指定为 true，表示不确定流向有效，遇到不确定流向时分析
                                                  继续进行；指定为 false，表示不确定流向无效，遇到不确定流向将停止在该方向上继
                                                  续查找。流向字段的值为 2 时代表该弧段的流向为不确定流向。
        :param bool is_edge_id: edge_or_node_id 是否表示弧段ID，True 表示为弧段ID，False表示为结点ID。
        :return: 设施网络分析结果
        :rtype: FacilityAnalystResult
        """
        self._load_internal()
        if is_edge_id:
            func = self._jobject.findCriticalFacilitiesDownFromEdge
        else:
            func = self._jobject.findCriticalFacilitiesDownFromNode
        java_result = func(to_java_int_array(source_node_ids), int(edge_or_node_id), parse_bool(is_uncertain_direction_valid))
        if java_result is not None:
            return FacilityAnalystResult(java_result)

    def find_critical_facilities_up(self, source_node_ids, edge_or_node_id, is_uncertain_direction_valid=False, is_edge_id=True):
        """
        上游关键设施查找，即查找给定弧段的上游中的关键设施结点，返回关键结点 ID 数组及其下游弧段 ID 数组。
        在进行上游关键设施查找分析时，我们将设施网络的结点划分为普通结点和设施结点两类，其中设施结点认为是能够影响网络连通性的结点，
        例如供水管网中的阀门；普通结点是不影响网络连通性的结点，如供水管网中的消防栓或三通等。上游关键设施查找分析需要指定设施结点和
        分析结点，其中分析结点可以是设施结点也可以是普通结点。

        上游关键设施查找分析将从给定的设施结点中筛选出关键结点，这些关键结点是分析弧段与其上游保持连通性的最基本的结点，也就是说，
        关闭这些关键结点后，分析结点与上游无法连通。同时，该分析的结果还包含查找出的关键结点的下游弧段的并集。

        关键设施结点的查找方式可以归纳为：从分析弧段出发，向它的上游回溯，每个方向上遇到的第一个设施结点，就是要查找的关键设施结点。
        如下图所示，从分析弧段（红色）出发，查找到的关键设施结点包括：2、8、9 和 7。而结点 4 和 11 不是回溯方向上遇到的第一个设施结
        点，因此不是关键设施结点。作为示意，这里仅给出了分析弧段的上游部分，但注意分析结果还会给出关键设施结点 2、8、9 和 7 的下游弧段。

        .. image:: ../image/findCriticalFacilitiesUp.png

        * 应用实例

        供水管网发生爆管后，可以将所有的阀门作为设施结点，将发生爆裂的管段或管点作为分析弧段或分析结点，进行上游关键设施查找分析，
        迅速找到上游中需要关闭的最少数量的阀门。关闭这些阀门后，爆裂管段或管点与它的上游不再连通，从而阻止水的流出，防止灾情加重和
        资源浪费。同时，分析得出需要关闭的阀门的下游弧段的并集，也就是关闭阀门后的影响范围，从而确定停水区域，及时做好通知工作和应急措施。

        .. image:: ../image/FindClosestFacilityUp.png

        :param source_node_ids: 指定的设施结点 ID 数组。不能为空。
        :type source_node_ids: list[int] or tuple[int]
        :param int edge_or_node_id: 分析弧段 ID 或结点 ID
        :param bool is_uncertain_direction_valid: 指定不确定流向是否有效。指定为 true，表示不确定流向有效，遇到不确定流向时分析
                                                  继续进行；指定为 false，表示不确定流向无效，遇到不确定流向将停止在该方向上继
                                                  续查找。流向字段的值为 2 时代表该弧段的流向为不确定流向。
        :param bool is_edge_id: edge_or_node_id 是否表示弧段ID，True 表示为弧段ID，False表示为结点ID
        :return: 设施网络分析结果
        :rtype: FacilityAnalystResult
        """
        self._load_internal()
        if is_edge_id:
            func = self._jobject.findCriticalFacilitiesUpFromEdge
        else:
            func = self._jobject.findCriticalFacilitiesUpFromNode
        java_result = func(to_java_int_array(split_input_int_list_from_str(source_node_ids)), int(edge_or_node_id), parse_bool(is_uncertain_direction_valid))
        if java_result is not None:
            return FacilityAnalystResult(java_result)

    def find_loops(self, edge_or_node_ids, is_edge_ids=True):
        """
        根据给定的结点 ID 数组或弧段 ID 数组，查找与这些结点（弧段）相连通的环路，返回构成环路的弧段 ID 数组。

        :param edge_or_node_ids: 指定的结点或弧段 ID 数组。
        :type edge_or_node_ids: list[int] or tuple[int]
        :param bool is_edge_ids: edge_or_node_ids 是否表示弧段ID，True 表示为弧段ID，False表示为结点ID
        :return: 与给定弧段相连通的环路的弧段 ID 数组。
        :rtype: list[int]
        """
        self._load_internal()
        if is_edge_ids:
            func = self._jobject.findLoopsFromEdges
        else:
            func = self._jobject.findLoopsFromNodes
        return java_array_to_list(func(to_java_int_array(edge_or_node_ids)))

    def find_path_down(self, edge_or_node_id, weight_name=None, is_uncertain_direction_valid=False, is_edge_id=True):
        """

        设施网络下游路径分析，根据给定的参与分析的结点 ID或弧段 ID，查询该结点（弧段）下游耗费最小的路径，返回该路径包含的弧段、结点及耗费。

        下游最小耗费路径的查找过程可以理解为：从给定结点（或弧段）出发，根据流向，查找出该结点（或弧段）的所有下游路径，然后从其中找出
        耗费最小的一条返回。 该方法用于查找给定结点的下游最小耗费路径。

        下图是一个简单的设施网络，在网络弧段上使用箭头标示了网络的流向，在弧段旁标注了权值。对于分析结点 H 进行下游最小耗费路径分析。
        首先从结点 H 出发，根据流向向下查找，找出结点 H 的所有下游路径，共有 4 条，包括：H-L-G、H-L-K、H-M-S 和 H-M-Q-R，然后根据
        网络阻力（即权值）计算这些路径的耗费，可以得出 H-L-K 这条路径的耗费最小，为 11.1，因此，结点 H 的下最小耗费路径就是 H-L-K。

        .. image:: ../image/PathDown.png

        :param int edge_or_node_id: 指定的结点 ID 或 弧段 ID
        :param str weight_name: 指定的权值字段信息对象的名称。即设置网络分析环境中指定的 :py:attr:`FacilityAnalystSetting.weight_fields` 中
                                具体某一个 :py:class:`WeightFieldInfo` 的 :py:attr:`WeightFieldInfo.weight_name` .
        :param bool is_uncertain_direction_valid: 指定不确定流向是否有效。指定为 true，表示不确定流向有效，遇到不确定流向时分析
                                                  继续进行；指定为 false，表示不确定流向无效，遇到不确定流向将停止在该方向上继
                                                  续查找。流向字段的值为 2 时代表该弧段的流向为不确定流向。
        :param bool is_edge_id: edge_or_node_id 是否表示弧段ID，True 表示为弧段ID，False表示为结点ID
        :return: 设施网络分析结果。
        :rtype: FacilityAnalystResult
        """
        self._load_internal()
        if is_edge_id:
            func = self._jobject.findPathDownFromEdge
        else:
            func = self._jobject.findPathDownFromNode
        java_result = func(int(edge_or_node_id), str(weight_name) if weight_name is not None else None, parse_bool(is_uncertain_direction_valid))
        if java_result is not None:
            return FacilityAnalystResult(java_result)

    def find_path(self, start_id, end_id, weight_name=None, is_uncertain_direction_valid=False, is_edge_id=True):
        """
        设施网络路径分析，即根据给定的起始和终止结点 ID，查找其间耗费最小的路径，返回该路径包含的弧段、结点及耗费。

        两结点间的最小耗费路径的查找过程为：从给定的起始结点出发，根据流向，查找到给定的终止结点的所有路径，然后从其中找出耗费最小的一条返回。

        下图是两结点最小耗费路径的示意图。从起始结点 B 出发，沿着网络流向，有三条路径能够到达终止结点 P，分别为 B-D-L-P、B-C-G-I-J-K-P
        和 E-E-F-H-M-N-O-P，其中路径 B-C-G-I-J-K-P 的耗费最小，为 105，因此该路径是结点 B 到 P 的最小耗费路径。

        .. image:: ../image/FacilityFindPath.png

        :param int start_id: 起始结点 ID 或弧段 ID。
        :param int end_id: 终止结点 ID 或弧段 ID。起始ID 和终止 ID 必须同时为结点 ID 或弧段 ID
        :param str weight_name:  指定的权值字段信息对象的名称。
        :param bool is_uncertain_direction_valid: 指定不确定流向是否有效。指定为 true，表示不确定流向有效，遇到不确定流向时分析
                                                  继续进行；指定为 false，表示不确定流向无效，遇到不确定流向将停止在该方向上继
                                                  续查找。流向字段的值为 2 时代表该弧段的流向为不确定流向。
        :param bool is_edge_id: edge_or_node_id 是否表示弧段ID，True 表示为弧段ID，False表示为结点ID
        :return: 设施网络分析结果。
        :rtype: FacilityAnalystResult
        """
        self._load_internal()
        if is_edge_id:
            func = self._jobject.findPathFromEdges
        else:
            func = self._jobject.findPathFromNodes
        java_result = func(int(start_id), int(end_id), str(weight_name) if weight_name is not None else None, parse_bool(is_uncertain_direction_valid))
        if java_result is not None:
            return FacilityAnalystResult(java_result)

    def find_path_up(self, edge_or_node_id, weight_name=None, is_uncertain_direction_valid=False, is_edge_id=True):
        """
        设施网络上游路径分析，根据给定的结点 ID或弧段 ID，查询该结点（弧段）上游耗费最小的路径，返回该路径包含的弧段、结点及耗费。

        上游最小耗费路径的查找过程可以理解为：从给定结点（或弧段）出发，根据流向，查找出该结点（或弧段）的所有上游路径，然后从其中找
        出耗费最小的一条返回。 该方法用于查找给定结点的上游最小耗费路径。

        下图是一个简单的设施网络，在网络弧段上使用箭头标示了网络的流向，在弧段旁标注了权值。对于分析结点 I 进行上游最小耗费路径分析。
        首先从结点 I 出发，根据流向向上回溯，找出结点 I 的所有上游路径，共有 6 条，包括：E-F-I、A-F-I、B-G-J-I、D-G-J-I、C-G-J-I
        和 H-J-I，然后根据网络阻力（即权值）计算这些路径的耗费，可以得出 E-F-I 这条路径的耗费最小，为 8.2，因此，结点 I 的上游最小
        耗费路径就是 E-F-I。

        .. image:: ../image/PathUp.png

        :param int edge_or_node_id: 结点 ID 或弧段 ID
        :param str weight_name: 权值字段信息对象的名称
        :param bool is_uncertain_direction_valid: 指定不确定流向是否有效。指定为 true，表示不确定流向有效，遇到不确定流向时分析
                                                  继续进行；指定为 false，表示不确定流向无效，遇到不确定流向将停止在该方向上继
                                                  续查找。流向字段的值为 2 时代表该弧段的流向为不确定流向。
        :param bool is_edge_id: edge_or_node_id 是否表示弧段ID，True 表示为弧段ID，False表示为结点ID
        :return: 设施网络分析结果
        :rtype: FacilityAnalystResult
        """
        self._load_internal()
        if is_edge_id:
            func = self._jobject.findPathUpFromEdge
        else:
            func = self._jobject.findPathUpFromNode
        java_result = func(int(edge_or_node_id), str(weight_name) if weight_name is not None else None, parse_bool(is_uncertain_direction_valid))
        if java_result is not None:
            return FacilityAnalystResult(java_result)

    def find_sink(self, edge_or_node_id, weight_name=None, is_uncertain_direction_valid=False, is_edge_id=True):
        """
        根据给定的结点 ID或弧段 ID 查找汇，即从给定结点（弧段）出发，根据流向查找流出该结点的下游汇点，并返回给定结点到达该汇的最小耗费路径所包含的弧段、结点及耗费。
        该方法从给定结点出发，按照流向，查找流出该结点的下游汇点，分析的结果为该结点到达查找到的汇的最小耗费路径所包含的弧段、结点及耗费。
        如果网络中有多个汇，将查找最远的也就是从给定结点出发最小耗费最大的那个汇。为了便于理解，可将该功能的实现过程分为三步：

         1. 从给定结点出发，根据流向，找到该结点下游所有的汇点；
         2. 分析给定结点到每个汇的最小耗费路径并计算耗费；
         3. 选择上一步中计算出的耗费中的最大值所对应的路径作为结果，给出该路径上的弧段 ID 数组、结点 ID 数组以及该路径的耗费。

        注意：分析结果中的结点 ID 数组不包括分析结点本身。

        下图是一个简单的设施网络，在网络弧段上使用箭头标示了网络的流向，在弧段旁标注了权值。对于分析结点 D 进行查找汇分析。可以知道，
        从 结点 D 出发，根据流向向下查找，共有 4 个汇，从结点 D 到达汇的最小耗费路径分别为：E-H-L-G、E-H-L-K、E-H-M-S 和 E-H-M-Q-R，
        根据网络阻力，也就是弧段权值，可以计算得出 E-H-M-Q-R 这条路径的耗费最大，为 16.6，因此，结点 R 就是查找到的汇。

        .. image:: ../image/FindSink.png

        :param int edge_or_node_id: 结点 ID 或弧段 ID
        :param str weight_name: 权值字段信息对象的名称
        :param bool is_uncertain_direction_valid: 指定不确定流向是否有效。指定为 true，表示不确定流向有效，遇到不确定流向时分析
                                                  继续进行；指定为 false，表示不确定流向无效，遇到不确定流向将停止在该方向上继
                                                  续查找。流向字段的值为 2 时代表该弧段的流向为不确定流向。
        :param bool is_edge_id: edge_or_node_id 是否表示弧段ID，True 表示为弧段ID，False表示为结点ID
        :return: 设施网络分析结果
        :rtype: FacilityAnalystResult
        """
        self._load_internal()
        if is_edge_id:
            func = self._jobject.findSinkFromEdge
        else:
            func = self._jobject.findSinkFromNode
        java_result = func(int(edge_or_node_id), str(weight_name) if weight_name is not None else None, parse_bool(is_uncertain_direction_valid))
        if java_result is not None:
            return FacilityAnalystResult(java_result)

    def find_source(self, edge_or_node_id, weight_name=None, is_uncertain_direction_valid=False, is_edge_id=True):
        """

        根据给定的结点 ID 或弧段 ID 查找源，即从给定结点（弧段）出发，根据流向查找流向该结点的网络源头，并返回该源到达给定结点的最小耗费路径所包含的弧段、结点及耗费。
        该方法从给定结点出发，按照流向，查找流向该结点的网络源头结点（即源点），分析的结果为查找到的源到达给定结点的最小耗费路径所包
        含的弧段、结点及耗费。 如果网络中有多个源，将查找最远的也就是到达给定结点的最小耗费最大的那个源。为了便于理解，可将该功能的实现过程分为三步：

         1. 从给定结点出发，根据流向，找到该结点上游所有的源点；
         2. 分析每个源到达给定结点的最小耗费路径并计算耗费；
         3. 选择上一步中计算出的耗费中的最大值所对应的路径作为结果，给出该路径上的弧段 ID 数组、结点 ID 数组以及该路径的耗费。

        注意：分析结果中的结点 ID 数组不包括分析结点本身。

        下图是一个简单的设施网络，在网络弧段上使用箭头标示了网络的流向，在弧段旁标注了权值。对于分析结点 M 进行查找源分析。可以知道，
        从 结点 M 出发，根据流向向上回溯，共有 7 个源，从源到结点 M 的最小耗费路径分别为：C-H-M、A-E-H-M、B-D-E-H-M、F-D-E-H-M、
        J-N-M、I-N-M 和 P-N-M，根据网络阻力，也就是弧段权值，可以计算得出 B-D-E-H-M 这条路径的耗费最大，为 18.4，因此，结点 B 就是查找到的源。

        .. image:: ../image/FindSource.png

        :param int edge_or_node_id: 结点 ID 或弧段 ID
        :param str weight_name: 权值字段信息对象的名称
        :param bool is_uncertain_direction_valid: 指定不确定流向是否有效。指定为 true，表示不确定流向有效，遇到不确定流向时分析
                                                  继续进行；指定为 false，表示不确定流向无效，遇到不确定流向将停止在该方向上继
                                                  续查找。流向字段的值为 2 时代表该弧段的流向为不确定流向。
        :param bool is_edge_id: edge_or_node_id 是否表示弧段ID，True 表示为弧段ID，False表示为结点ID
        :return: 设施网络分析结果
        :rtype: FacilityAnalystResult
        """
        self._load_internal()
        if is_edge_id:
            func = self._jobject.findSourceFromEdge
        else:
            func = self._jobject.findSourceFromNode
        java_result = func(int(edge_or_node_id), str(weight_name) if weight_name is not None else None, parse_bool(is_uncertain_direction_valid))
        if java_result is not None:
            return FacilityAnalystResult(java_result)

    def find_unconnected_edges(self, edge_or_node_ids, is_edge_ids=True):
        """
        根据给定的结点 ID 数组，查找与这些结点不相连通的弧段，返回弧段 ID 数组。
        该方法用于查找与给定结点不连通的弧段，查找出连通弧段后，可根据网络拓扑关系，即弧段的起始结点、终止结点查询出相应的不连通结点。

        :param edge_or_node_ids: 结点 ID 数组或弧段 ID 数组
        :type edge_or_node_ids: list[int] or tuple[int]
        :param bool is_edge_ids: edge_or_node_ids 是否表示弧段ID，True 表示为弧段ID，False表示为结点ID
        :return: 弧段 ID 数组
        :rtype: list[int]
        """
        self._load_internal()
        if is_edge_ids:
            func = self._jobject.findUnconnectedEdgesFromEdges
        else:
            func = self._jobject.findUnconnectedEdgesFromNodes
        return java_array_to_list(func(to_java_int_array(edge_or_node_ids)))

    def trace_down(self, edge_or_node_id, weight_name=None, is_uncertain_direction_valid=False, is_edge_id=True):
        """
        根据给定的弧段 ID 或结点 ID 进行下游追踪，即查找给定弧段（结点）的下游，返回下游包含的弧段、结点及总耗费。
        下游追踪，是从给定结点（或弧段）出发，根据流向，查找其下游的过程。该方法用于查找给定弧段的下游，分析结果为其下游所包含的弧段、结点， 及流经整个下游的耗费。

        下游追踪常用于影响范围的分析。例如：

        - 自来水供水管道爆管后，通过下游追踪分析事故位置的所有下游管道，然后通过空间查询，确定受影响的供水区域，从而及时发放通知，并采
          取应急措施， 如由消防车或自来水公司安排车辆为停水小区送水。

        - 当发现河流的某个位置发生污染时，可以通过下游追踪，分析出可能受到影响的所有下游河段，如下图所示。在分析前，还可以根据污染物的
          种类、 排放量等结合恰当的水质管理模型，分析出在污染清除前不会遭到污染的下游河段或位置，设置为障碍（在 FacilityAnalystSetting 中设置），
          下游追踪时，到达障碍即追踪停止 ，这样可以缩小分析的范围。确定了可能受影响的河段后，通过空间查询和分析标记出位于结果河段附近的所
          有用水单位和居民区 ，及时下发通知，并采取紧急措施，防止污染的危害进一步扩大。

        :param int edge_or_node_id: 结点 ID 或弧段 ID
        :param str weight_name: 权值字段信息对象的名称
        :param bool is_uncertain_direction_valid: 指定不确定流向是否有效。指定为 true，表示不确定流向有效，遇到不确定流向时分析
                                                  继续进行；指定为 false，表示不确定流向无效，遇到不确定流向将停止在该方向上继
                                                  续查找。流向字段的值为 2 时代表该弧段的流向为不确定流向。
        :param bool is_edge_id: edge_or_node_id 是否表示弧段ID，True 表示为弧段ID，False表示为结点ID
        :return: 设施网络分析结果。
        :rtype: FacilityAnalystResult
        """
        self._load_internal()
        if is_edge_id:
            func = self._jobject.traceDownFromEdge
        else:
            func = self._jobject.traceDownFromNode
        java_result = func(int(edge_or_node_id), str(weight_name) if weight_name is not None else None, parse_bool(is_uncertain_direction_valid))
        if java_result is not None:
            return FacilityAnalystResult(java_result)

    def trace_up(self, edge_or_node_id, weight_name=None, is_uncertain_direction_valid=False, is_edge_id=True):
        """
        根据给定的结点 ID 或弧段 ID 进行上游追踪，即查找给定结点的上游，返回上游包含的弧段、结点及总耗费。

        * 上游和下游

          对于设施网络的某个结点（或弧段）来说，网络中的资源最终流入该结点（或弧段）所经过的弧段和结点称为它的上游；从该结点（或弧段）
          流出最终流入汇点所经过的弧段和网络称为它的下游。

          下面以结点的上游和下游为例。下图是一个简单的设施网络的示意图，使用箭头标出了网络的流向。根据流向，可以看出，资源流经结点
          2、4、3、7、8 以及弧段 10、9、3、4、8 最终流入结点 10，因此这些结点和弧段称为结点 10 的上游，其中的结点称为它的上游结点，
          弧段称为它的上游弧段。同样的，资源从结点 10 流出，流经结点9、11、12 以及弧段 5、7、11 最终流出网络，因此，这些结点和弧段称
          为结点 10 的下游，其中的结点称为它的下游结点，弧段称为它的下游弧段。

          .. image:: ../image/UpAndDown.png

        * 上游追踪与下游追踪

          上游追踪，是从给定结点（或弧段）出发，根据流向，查找其上游的过程。类似的，下游追踪是从给定结点（或弧段）出发，根据流向，
          查找其下游的过程。 FacilityAnalyst 类分别提供了从结点或弧段出发，进行上游或下游追踪的方法，分析的结果为查找到的上游或下
          游所包含的弧段 ID 数组、结点 ID 数组，以及流经整个上游或者下游的耗费。本方法用于查找给定弧段的上游。

        * 应用实例

          上游追踪的一个常用应用是辅助定位河流水污染物来源。河流不仅是地球水循环的重要路径，也是人类最主要的淡水资源， 一旦河流发生
          污染而没有及时发现污染源并消除 ，很可能影响人们的正常饮水和健康。由于河流受重力影响从高处向低处流动，因此当河流发生污染时，
          应考虑其上游可能出现了污染源 ，如工业废水排放、生活污水排放、农药化肥污染等。河流水污染物来源追踪的大致步骤一般为:

            - 当水质监测站的监测数据显示水质发生异常，首先确定发生异常的位置，从而在河流网络（网络数据集）上找出该位置所在（或最近）的弧段或结点， 作为上游追踪的起点；
            - 如果知道在起点的上游中距离起点最近的水质监测正常的位置，可以将这些位置或其所在的河段设置为障碍，可以帮助进一步缩小分析的范围。因为可以认为， 水质监测正常的位置的上游，不可能存在此次调查的污染源。设置为障碍后，进行上游追踪分析，追踪到该位置后，将不会继续追踪该位置的上游；
            - 进行上游追踪分析，查找到向发生水质异常位置所在河段汇流的所有河段；
            - 使用空间查询、分析找出位于这些河段附近的所有可能的污染源，如化工厂、垃圾处理厂等；
            - 根据发生水质异常的监测数据对污染源进行进一步筛选；
            - 分析筛选出的污染源的排污负荷，按照其造成污染的可能性进行排序；
            - 对可能的污染源按照顺序进行实地调查与研究，最终确定污染物来源。

        :param int edge_or_node_id: 结点 ID 或弧段 ID
        :param str weight_name: 权值字段信息对象的名称
        :param bool is_uncertain_direction_valid: 指定不确定流向是否有效。指定为 true，表示不确定流向有效，遇到不确定流向时分析
                                                  继续进行；指定为 false，表示不确定流向无效，遇到不确定流向将停止在该方向上继
                                                  续查找。流向字段的值为 2 时代表该弧段的流向为不确定流向。
        :param bool is_edge_id: edge_or_node_id 是否表示弧段ID，True 表示为弧段ID，False表示为结点ID
        :return: 设施网络分析结果。
        :rtype: FacilityAnalystResult
        """
        self._load_internal()
        if is_edge_id:
            func = self._jobject.traceUpFromEdge
        else:
            func = self._jobject.traceUpFromNode
        java_result = func(int(edge_or_node_id), str(weight_name) if weight_name is not None else None, parse_bool(is_uncertain_direction_valid))
        if java_result is not None:
            return FacilityAnalystResult(java_result)


class TransportationAnalystParameter:
    __doc__ = "\n    交通网络分析参数设置类。\n\n    该类主要用来对交通网络分析的参数进行设置。通过交通网络分析参数设置类可以设置障碍边、障碍点、权值字段信息的名字标识、分析途径的\n    点或结点，还可以对分析结果进行一些设置，即在分析结果中是否包含分析途经的以下内容：结点集合，弧段集合，路由对象集合以及站点集合。\n\n    "

    def __init__(self):
        self._is_routes_return = False
        self._is_nodes_return = True
        self._is_edges_return = True
        self._is_path_guides_return = False
        self._is_stop_indexes_return = False
        self._nodes = None
        self._points = None
        self._weight_name = None
        self._barrier_nodes = None
        self._barrier_edges = None
        self._barrier_points = None

    @property
    def is_routes_return(self):
        """bool: 返回分析结果中是否包含路由（ :py:class:`GeoLineM` ）对象"""
        return self._is_routes_return

    def set_routes_return(self, value=True):
        """
       分析结果中是否包含路由（ :py:class:`GeoLineM` ）对象

        :param bool value: 指定是否包含路由对象。设置为 True，在分析成功后，可以从 TransportationAnalystResult 对象
                           的 :py:attr:`TransportationAnalystResult.route` 返回路由对象；为 False 则返回 None
        :return: self
        :rtype: TransportationAnalystParameter
        """
        self._is_routes_return = parse_bool(value)
        return self

    @property
    def is_nodes_return(self):
        """bool: 分析结果中是否包含途经结点"""
        return self._is_nodes_return

    def set_nodes_return(self, value=True):
        """
        设置分析结果中是否包含结点

        :param bool value: 指定分析结果中是否包含途经结点。设置为 True，在分析成功后，可以从 TransportationAnalystResult 对象
                            :py:attr:`TransportationAnalystResult.nodes` 方法返回途经结点；为 False 则返回 None
        :return: self
        :rtype: TransportationAnalystParameter
        """
        self._is_nodes_return = parse_bool(value)
        return self

    @property
    def is_edges_return(self):
        """bool: 分析结果中是否包含途经弧段"""
        return self._is_edges_return

    def set_edges_return(self, value=True):
        """
        设置分析结果中是否包含途经弧段

        :param bool value: 指定分析结果中是否包含途经弧段。设置为 True，在分析成功后，可以从 TransportationAnalystResult 对象
                            :py:attr:`TransportationAnalystResult.edges` 方法返回途经弧段；为 False 则返回 None
        :return: self
        :rtype: TransportationAnalystParameter
        """
        self._is_edges_return = parse_bool(value)
        return self

    @property
    def is_path_guides_return(self):
        """bool: 分析结果中是否包含行驶导引"""
        return self._is_path_guides_return

    def set_path_guides_return(self, value=True):
        """
        设置分析结果中是否包含行驶导引集合。

        必须将该方法设置为 True，并且通过 TransportationAnalystSetting 类的 :py:meth:`TransportationPathAnalystSetting.set_edge_name_field` 方
        法设置了弧段名称字段，分析结果中才会包含行驶导引集合，否则将不会返回行驶导引，但不影响分析结果中其他内容的获取。

        :param bool value: 分析结果中是否包含行驶导引。设置为 True，在分析成功后，可以从 TransportationAnalystResult 对
                           象 :py:attr:`TransportationAnalystResult.path_guides` 方法返回行驶导引；为 False 则返回 None
        :return: self
        :rtype: TransportationAnalystParameter
        """
        self._is_path_guides_return = parse_bool(value)
        return self

    @property
    def is_stop_indexes_return(self):
        """bool: 分析结果中是否要包含站点索引"""
        return self._is_stop_indexes_return

    def set_stop_indexes_return(self, value=True):
        """
        设置分析结果中是否要包含站点索引的

        :param bool value: 指定分析结果中是否要包含站点索引。设置为 True，在分析成功后，可以从 TransportationAnalystResult 对象
                            :py:attr:`TransportationAnalystResult.stop_indexes` 方法返回站点索引；为 False 则返回 None
        :return: self
        :rtype: TransportationAnalystParameter
        """
        self._is_stop_indexes_return = parse_bool(value)
        return self

    @property
    def nodes(self):
        """list[int]: 分析途经点"""
        return self._nodes

    def set_nodes(self, nodes):
        """
        设置分析途经点。必设，但与 :py:meth:`set_points` 方法互斥，如果同时设置，则只有分析前最后的设置有效。例如，先指定了结点
        集合，又指定了坐标点集合，然后分析，此时只对坐标点进行分析。

        :param nodes: 途经结点 ID
        :type nodes: list[int] or tuple[int]
        :return: self
        :rtype: TransportationAnalystParameter
        """
        self._nodes = split_input_int_list_from_str(nodes)
        return self

    @property
    def points(self):
        """list[Point2D]: 分析时途经点"""
        return self._points

    def set_points(self, points):
        """
        设置分析时途经点的集合。必设，但与 :py:meth:`set_nodes` 方法互斥，如果同时设置，则只有分析前最后的设置有效。例如，先指定了结点集合，又
        指定了坐标点集合，然后分析，此时只对坐标点进行分析。

        如果设置的途经点集合中的点不在网络数据集的范围内，则该点不会参与分析

        :param points: 途经点
        :type points: list[Point2D] or tuple[Point2D]
        :return: self
        :rtype: TransportationAnalystParameter
        """
        if isinstance(points, (list, tuple)):
            self._points = list(filter((lambda p: p is not None), list((Point2D.make(p) for p in points))))
        else:
            if isinstance(points, None):
                self._points = None
            else:
                raise ValueError("points required list[Point2D] or tuple[Point2D]")
        return self

    @property
    def weight_name(self):
        """str: 权值字段信息的名称"""
        return self._weight_name

    def set_weight_name(self, name):
        """
        设置权值字段信息的名称。如果未设置，则默认使用权值字段信息集合中的第一个权值字段信息对象的名称

        :param str name: 权值字段信息的名字标识
        :return: self
        :rtype: TransportationAnalystParameter
        """
        self._weight_name = name
        return self

    @property
    def barrier_nodes(self):
        """list[int]: 障碍结点 ID 列表"""
        return self._barrier_nodes

    def set_barrier_nodes(self, nodes):
        """
        设置障碍结点 ID 列表。可选。此处指定的障碍结点与交通网络分析环境（ :py:class:`TransportationAnalystSetting` ）中指定的
        障碍结点共同作用于交通网络分析。

        :param nodes: 障碍结点 ID 列表
        :type nodes: list[int] or tuple[int]
        :return: self
        :rtype: TransportationAnalystParameter
        """
        self._barrier_nodes = split_input_int_list_from_str(nodes)
        return self

    @property
    def barrier_edges(self):
        """list[int]: 障碍弧段 ID 列表"""
        return self._barrier_edges

    def set_barrier_edges(self, edges):
        """
        设置障碍弧段 ID 列表。可选。此处指定的障碍弧段与交通网络分析环境（:py:class:`TransportationAnalystSetting`）中指定的障
        碍弧段共同作用于交通网络分析。

        :param edges: 障碍弧段 ID 列表
        :type edges: list[int] or tuple[int]
        :return: self
        :rtype: TransportationAnalystParameter
        """
        self._barrier_edges = split_input_int_list_from_str(edges)
        return self

    @property
    def barrier_points(self):
        """list[Point2D]: 障碍点列表"""
        return self._barrier_points

    def set_barrier_points(self, points):
        """
        设置障碍结点的坐标列表。可选。指定的障碍点可以不在网络上（既不在弧段上也不在结点上），分析时将根据距离容限（ :py:attr:`.TransportationPathAnalystSetting.tolerance` ）把
        障碍点归结到最近的网络上。目前支持最佳路径分析、最近设施查找、旅行商分析和物流配送分析。

        :param points: 障碍结点的坐标列表
        :type points: list[Point2D] or tuple[Point2D]
        :return: self
        :rtype: TransportationAnalystParameter
        """
        if isinstance(points, (list, tuple)):
            self._barrier_points = list(filter((lambda p: p is not None), list((Point2D.make(p) for p in points))))
        else:
            if points is None:
                self._barrier_points = None
            else:
                raise ValueError("points required list[Point2D]")
        return self

    @property
    def _jobject(self):
        java_object = get_jvm().com.supermap.analyst.networkanalyst.TransportationAnalystParameter()
        if self.is_nodes_return is not None:
            java_object.setNodesReturn(bool(self.is_nodes_return))
        if self.is_edges_return is not None:
            java_object.setEdgesReturn(bool(self.is_edges_return))
        if self.is_routes_return is not None:
            java_object.setRoutesReturn(bool(self.is_routes_return))
        if self.is_path_guides_return is not None:
            java_object.setPathGuidesReturn(bool(self.is_path_guides_return))
        if self.is_stop_indexes_return is not None:
            java_object.setStopIndexesReturn(bool(self.is_stop_indexes_return))
        if self.nodes is not None:
            java_object.setNodes(to_java_int_array(self.nodes))
        if self.points is not None:
            java_object.setPoints(to_java_point2ds(self.points))
        if self.weight_name is not None:
            java_object.setWeightName(self.weight_name)
        if self.barrier_nodes is not None:
            java_object.setBarrierNodes(to_java_int_array(self.barrier_nodes))
        if self.barrier_edges is not None:
            java_object.setBarrierEdges(to_java_int_array(self.barrier_edges))
        if self.barrier_points is not None:
            java_object.setBarrierPoints(to_java_point2ds(self.barrier_points))
        return java_object


@unique
class DirectionType(JEnum):
    __doc__ = "\n    方向，用于行驶导引\n\n    :var DirectionType.EAST: 东\n    :var DirectionType.SOUTH: 南\n    :var DirectionType.WEST: 西\n    :var DirectionType.NORTH: 北\n    :var DirectionType.NONE: 结点没有方向\n    "
    EAST = 0
    SOUTH = 1
    WEST = 2
    NORTH = 3
    NONE = 4

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.networkanalyst.DirectionType"


@unique
class SideType(JEnum):
    __doc__ = "\n    表示在路的左边、右边还是在路上。用于行驶导引。\n\n    :var SideType.NONE: 无效值\n    :var SideType.MIDDLE: 在路上（即路的中间）\n    :var SideType.LEFT: 路的左侧\n    :var SideType.RIGHT: 路的右侧\n    "
    NONE = -1
    MIDDLE = 0
    LEFT = 1
    RIGHT = 2

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.networkanalyst.SideType"


@unique
class TurnType(JEnum):
    __doc__ = "\n    转弯方向，用于行驶导引\n\n    :var TurnType.NONE: 无效值\n    :var TurnType.END: 终点，不转弯\n    :var TurnType.LEFT: 左转弯\n    :var TurnType.RIGHT: 右转弯\n    :var TurnType.AHEAD: 表示向前直行\n    :var TurnType.BACK: 掉头\n    "
    NONE = 255
    END = 0
    LEFT = 1
    RIGHT = 2
    AHEAD = 3
    BACK = 4

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.networkanalyst.TurnType"


@unique
class ServiceAreaType(JEnum):
    __doc__ = "\n    服务区类型。用于服务区分析。\n\n    :var ServiceAreaType.SIMPLEAREA: 简单服务区\n    :var ServiceAreaType.COMPLEXAREA: 复杂服务区\n    "
    SIMPLEAREA = 0
    COMPLEXAREA = 1

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.networkanalyst.ServiceType"

    @classmethod
    def _externals(cls):
        return {'simple':ServiceAreaType.SIMPLEAREA,  'complex':ServiceAreaType.COMPLEXAREA}


class PathGuideItem:
    __doc__ = "\n\n    在交通网络分析中，行驶导引子项可以归纳为以下几类：\n\n    - 站点：即用户选择的用于分析的点，如进行最佳路径分析时指定的要经过的各个点。\n\n    - 站点到网络的线段：当站点为普通的坐标点时，需要首先将站点归结到网络上，才能基于网络进行分析。请参见 :py:attr:`TransportationPathAnalystSetting.tolerance` 方法的介绍。\n\n      如下图所示，红色虚线即为站点到网络的最短直线距离。注意，当站点在网络弧段的边缘附近时，如右图所示，这段距离是指站点与弧段端点的连线距离。\n\n      .. image:: ../image/PathGuideItem_4.png\n\n    - 站点在网络上的对应点：与“站点到网络的线段”对应，这个点就是将站点（普通坐标点）归结到网络上时，网络上相应的点。上面左图所示的\n      情形，这个点就是站点在对应弧段上的垂足点；上面右图所示的情形，这个点则为弧段的端点。\n\n    - 路段：也就是行驶经过的一段道路。交通网络中用弧段模拟道路，因此行驶路段都位于弧段上。注意，多个弧段可能被合并为一个行驶导引子项，\n      合并的条件是它们的弧段名称相同，并且相邻弧段间的转角小于 30 度。需要强调，到达站点前的最后一个行驶路段和到达站点后的第一个行驶\n      路段，仅包含一条弧段或弧段的一部分，即使满足上述条件也不会与相邻弧段合并为一个行驶导引。\n\n      如下图所示，使用不同的颜色标示出了两个站点之间的行驶路段。其中，站点 1 之后的第一条路段（红色），虽然其所在弧段的名称与后面几条\n      弧段的名称相同，且转向角度都小于 30 度，但由于它是站点后的第一条路段，因此并未将它们合并。而蓝色路段所覆盖的三条弧段，由于弧段\n      名称相同且转角小于 30 度，故将它们合并为一个行驶导引子项；粉色路段由于与之前的路段具有不同的弧段名称，故成为另一个行驶导引子\n      项；绿色路段由于是到达站点前的最后一条路段，因此也单独作为一个行驶导引子项。\n\n      .. image:: ../image/PathGuideItem_5.png\n\n    - 转向点：两个相邻的行驶路段之间的路口。路口是指有可能发生方向改变的实际道路的路口（如十字路口或丁字路口）。在转向点处行驶方向可\n      能发生改变。如上图中的结点 2783、2786 和 2691 都是转向点。转向点一定是网络结点。\n\n    通过 PathGuideItem 的各个方法返回的值，可以判断行驶导引子项属于哪种类型，下表总结了五种行驶导引子项的各个方法返回值的对照表，方\n    便用户理解和使用行驶导引。\n\n    .. image:: ../image/PathGuideItem_6.png\n\n\n    通过下面的实例，可以帮助用户理解行驶导引和行驶导引子项的内容和作用。下图中的蓝色虚线为最近设施查找分析的结果中的一条路径，在最近\n    设施查找的返回结果中，可以获得这条路径对应的行驶导引。\n\n    .. image:: ../image/PathGuideItem_1.png\n\n    用于描述这条路径的行驶导引共包含7个子项。这7个行驶导引子项包含2个站点（即起点和终点，对应序号为0和6）、3个弧段（即路段，序号分别\n    为1、3、5）和2个网络结点（即转向点，序号分别为2、4）。下表列出了这7个行驶导引子项的信息，包括是否为站点（ :py:attr:`is_stop` ）、\n    是否为弧段（ :py:attr:`is_edge` ）、序号（:py:attr:`index` ）、行驶方向（ :py:attr:`direction_type` ）、转弯方向（ :py:attr:`turn_type` ）\n    及弧段名称（ :py:attr:`name` ）等信息。\n\n    .. image:: ../image/PathGuideItem_2.png\n\n    将行驶导引子项记录的信息进行组织，可以得到如下表所示的该路径的导引描述。\n\n    .. image:: ../image/PathGuideItem_3.png\n\n    "

    def __init__(self, java_object):
        java_bounds = java_object.getBounds()
        if java_bounds is not None:
            self._bounds = Rectangle._from_java_object(java_bounds)
        else:
            self._bounds = None
        self._direction_type = DirectionType.NONE
        java_direction = java_object.getDirectionType()
        if java_direction is not None:
            self._direction_type = DirectionType._make(java_direction.name())
        self._distance = java_object.getDistance()
        self._guide_line = Geometry._from_java_object(java_object.getGuideLine())
        self._node_edge_id = java_object.getID()
        self._index = java_object.getIndex()
        self._length = java_object.getLength()
        self._name = java_object.getName()
        self._side_type = SideType.NONE
        java_side_type = java_object.getSideType()
        if java_side_type is not None:
            self._side_type = SideType._make(java_side_type.name())
        self._turn_angle = java_object.getTurnAngle()
        self._turn_type = TurnType.NONE
        java_turn_type = java_object.getTurnType()
        if java_turn_type is not None:
            self._turn_type = TurnType._make(java_turn_type.name())
        self._weight = java_object.getWeight()
        self._is_edge = java_object.isEdge()
        self._is_stop = java_object.isStop()

    @property
    def bounds(self):
        """Rectangle: 该行驶导引子项的范围。当行驶导引子项为线类型（即 :py:attr:`is_edge` 返回 True）时，为线的最小外接矩形；为
                      点类型（即 :py:attr:`is_edge` 返回 False）时，则为点本身"""
        return self._bounds

    @property
    def direction_type(self):
        """DirectionType: 该行驶导引子项的行驶方向，仅当行驶导引子项为线类型（即 :py:attr:`is_edge` 返回 True）时有意义，可以为东、南、西、北"""
        return self._direction_type

    @property
    def distance(self):
        """float: 站点到网络的距离，仅当行驶导引子项为站点时有效。站点可能不在网络上（既不在弧段上也不在结点上），必须将站点归结到
                  网络上，才能基于网络进行分析。该距离是指站点到最近一条弧段的距离。如下图所示，桔色点代表网络结点，蓝色代表弧段，
                  灰色点为站点，红色线段代表距离。

                  .. image:: ../image/PathGuideItemDistance.png

                  当行驶导引子项是站点以外的其他类型时，该值为 0.0。
        """
        return self._distance

    @property
    def guide_line(self):
        """GeoLineM: 返回该行驶导引子项为线类型（即 :py:attr:`is_edge` 返回 True ）时，对应的行驶导引线段。
                     当 :py:attr:`is_edge` 返回 false 时，该方法返回 None。"""
        return self._guide_line

    @property
    def node_edge_id(self):
        """int: 该行驶导引子项的 ID。
                除以下三种情形外，该方法均返回 -1：

                 - 当行驶导引子项为结点模式下的站点时，站点为结点，返回该结点的结点 ID；
                 - 当行驶导引子项为转向点时，转向点为结点，返回该结点的结点 ID；
                 - 当行驶导引子项为路段时，返回路段对应的弧段的弧段 ID。如果该路段由多条弧段合并而成，则返回第一条弧段的 ID。
        """
        return self._node_edge_id

    @property
    def index(self):
        """int: 行驶导引子项的序号。
                除以下两种情形外，该方法均返回 -1：

                 - 当行驶导引子项为站点时，该值为该站点在所有站点中的序号，从 1 开始。例如某个站点是行驶路线经过的第 2 个站点，则此
                   站点的 Index 值为 2；
                 - 当行驶导引子项为转向点时，该值为该点距离上一个转向点或站点的路口数。例如某个转向点之前的两个路口是最近的一个站点，
                   则这个转向点的 Index 值为 2；当某个点同时为站点和转向点时，Index 为在整个行驶过程的所有站点中该站点的位置。
        """
        return self._index

    @property
    def length(self):
        """float: 返回该行驶导引子项为线类型（即 :py:attr:`is_edge` 返回 True ）时，对应线段的长度。单位为米"""
        return self._length

    @property
    def name(self):
        """str: 该行驶导引子项的名称。
                除以下两种情形外，该方法均返回空字符串：

                - 当行驶导引子项为站点（结点模式）或转向点时，该值根据交通网络分析环境中指定的结点名称字段的值
                  给出，如未设置则为空字符串；
                - 当行驶导引子项为路段或站点到网络的线段时，该值根据交通网络分析环境中指定的结点名称字段的值
                  给出，如未设置则为空字符串。
        """
        return self._name

    @property
    def side_type(self):
        """SideType: 行驶导引子项为站点时，站点在道路的左侧、右侧还是在路上。当行驶导引子项为站点以外的类型时，该方法返回 NONE"""
        return self._side_type

    @property
    def turn_angle(self):
        """float: 该行驶导引子项为点类型时，该点处下一步行进的转弯角度。单位为度，精确到 0.1 度。 当 :py:attr:`is_edge` 返回 True 时，该方法返回 -1"""
        return self._turn_angle

    @property
    def turn_type(self):
        """TurnType: 返回该行驶导引子项为点类型（即 :py:attr:`is_edge` 返回 False）时，该点处下一步行进的转弯方向。
                     当 :py:attr:`is_edge` 返回 True 时，该方法返回 None"""
        return self._turn_type

    @property
    def weight(self):
        """float: 返回该行驶导引子项的权值，即行使导引对象子项的花费。单位与交通网络分析参数（TransportationAnalystParameter）所
                  指定的权值字段信息（ :py:class:`WeightFieldInfo` ）对象的权值字段的单位相同。
                  当行驶导引子项为路段、转向点或结点模式下的站点时，得到的花费才有意义，否则均为 0.0。

                  - 当行驶导引子项为路段时，根据弧段权值和转向权值计算得出相应的花费。如果未设置转向表，则转向权值为 0；
                  - 当行驶导引子项为转向点或结点模式下的站点时（二者均为结点），为相应的转向权值。如果未设置转向表，则为 0.0。
        """
        return self._weight

    @property
    def is_edge(self):
        """bool: 返回该行驶导引子项是线还是点类型。若为 True，表示为线类型，如站点到网络的线段、路段；若为 False，表示为点类型，
                 如站点、转向点或站点被归结到网络上的对应点。"""
        return self._is_edge

    @property
    def is_stop(self):
        """bool: 返回该行驶导引子项是否为站点，或站点被归结到网络上的对应点。当 is_stop 返回 true 时，对应的行驶导引子项可能是站点，或当站点为坐标点时，被归结到网络上的对应点。"""
        return self._is_stop


class PathGuide:
    __doc__ = "\n    行驶导引\n\n    行驶导引记录了如何从一条路径的起点一步步行驶到终点，其中路径上的每一个关键要素对应一个行驶导引子项。这些关键要素包括站点（用户输\n    入的用于分析的点，可以为普通点或结点），经过的弧段和网络结点。通过行驶导引子项对象，可以获取路径中关键要素的 ID、名称、序号、权\n    值、长度，还可以判断是弧段还是站点，以及行驶方向、转弯方向、花费等信息。按照行驶导引子项的序号对其存储的关键要素信息进行提取并\n    组织，就可以描绘出如何从路径起点到达终点。\n\n    下图是最近设施查找分析的一个实例，分析的结果给出了三条首选的路径。每一条路径的信息便由一个行驶导引对象来记录。如第二条路径，它由\n    站点（这里为起点和终点，可以为一般坐标点或网络结点）、路段（弧段）、路口（网络结点）等关键要素构成，从它对应的行驶导引的行驶导引\n    子项中可以获得这些关键要素的信息，从而使我们能够将该路径从起点如何行驶至终点描述清楚，如在什么路行驶多长距离向哪个方法转弯等。\n\n    .. image:: ../image/PathGuide.png\n\n\n    "

    def __init__(self, items):
        self._guide_items = list(items)

    def __getitem__(self, item):
        """
        获取指定位置的行驶导引子项

        :param item: 指定的行驶导引索引下标
        :type item: int
        :return: 行驶导引子项
        :rtype: PathGuideItem
        """
        return self._guide_items[item]

    def __iter__(self):
        return self._guide_items.__iter__()

    def __len__(self):
        """
        返回行驶导引子项数目

        :return: 行驶导引子项数目
        :rtype: int
        """
        return self._guide_items.__len__()

    @staticmethod
    def _side_type_str(side_type):
        if side_type is SideType.LEFT:
            return "左侧"
        if side_type is SideType.RIGHT:
            return "右侧"
        return ""

    @staticmethod
    def _turn_type_str(turn_type):
        if turn_type is TurnType.LEFT:
            return "左转弯"
        if turn_type is TurnType.RIGHT:
            return "右转弯"
        if turn_type is TurnType.AHEAD:
            return "向前直行"
        if turn_type is TurnType.BACK:
            return "掉头行驶"
        return ""

    def __str__(self):
        if self._guide_items:
            stop_index = 1
            index = 1
            navigation_infos = ["从起点出发"]
            while index < len(self._guide_items):
                guide_item = self._guide_items[index]
                road_name = guide_item.name if guide_item.name else "匿名道路"
                if guide_item.is_stop and guide_item.index != -1:
                    stop_index += 1
                    if index != len(self._guide_items) - 1:
                        if guide_item.side_type is (SideType.RIGHT, SideType.LEFT):
                            guide_info = "到达[{}号路由点]，在道路{} {}".format(stop_index, PathGuide._side_type_str(guide_item.side_type), round(guide_item.distance, 1))
                        else:
                            guide_info = "到达[{}号路由点]".format(stop_index)
                    else:
                        if guide_item.side_type is (SideType.RIGHT, SideType.LEFT):
                            if index > 1:
                                if self._guide_items[index - 3].name:
                                    next_road_name = self._guide_items[index - 3].name
                                else:
                                    next_road_name = "匿名路段"
                                guide_info = "到达终点，在道路[{}]{} {}".format(next_road_name, PathGuide._side_type_str(guide_item.side_type), round(guide_item.distance, 4))
                        else:
                            guide_info = "到达终点"
                    navigation_infos.append(guide_info)
                else:
                    if guide_item.is_edge and guide_item.node_edge_id != -1:
                        weight = round(guide_item.weight, 4)
                        guide_info = None
                        if self._guide_items[index + 1].is_stop and self._guide_items[index + 1].node_edge_id == -1:
                            guide_info = "沿着[{}], 行走 {}".format(road_name, weight)
                        else:
                            guide_next = self._guide_items[index + 1]
                            if guide_next.index != -1:
                                if guide_next.turn_type is not TurnType.NONE:
                                    if guide_next.turn_type is not TurnType.END:
                                        if self._guide_items[index + 2].name:
                                            next_road_name = self._guide_items[index + 2].name
                                        else:
                                            next_road_name = "匿名路段"
                                        guide_info = "沿着[{}], 行走{}, {}进入[{}]".format(road_name, weight, PathGuide._turn_type_str(guide_next.turn_type), next_road_name)
                            else:
                                guide_info = "沿着[{}], 行走{}".format(road_name, weight)
                    else:
                        if self._guide_items[index + 2].name:
                            next_road_name = self._guide_items[index + 2].name
                        else:
                            next_road_name = "匿名路段"
                        guide_info = "沿着[{}], 行走{}, 进入[{}]".format(road_name, weight, next_road_name)
                    if guide_info:
                        navigation_infos.append(guide_info)
                    index += 1

            return "\r\n".join(navigation_infos)
        return ""


class TransportationAnalystResult:
    __doc__ = "\n    交通网络分析结果类。\n\n    该类用于返回分析结果的路由集合、分析途经的结点集合以及弧段集合、行驶导引集合、站点集合和权值集合以及各站点的花费。通过该类的设置，\n    可以灵活地得到最佳路径分析、旅行商分析、物流配送和最近设施查找等分析的结果。\n    "

    def __init__(self, java_object, index):
        java_edges = java_object.getEdges()
        if java_edges is not None and len(java_edges) > index:
            self._edges = java_array_to_list(java_edges[index])
        else:
            self._edges = None
        java_nodes = java_object.getNodes()
        if java_nodes is not None and len(java_nodes) > index:
            self._nodes = java_array_to_list(java_nodes[index])
        else:
            self._nodes = None
        java_path_guides = java_object.getPathGuides()
        if java_path_guides is not None and len(java_path_guides) > index:
            java_path_guide_items = java_path_guides[index]
            self._path_guides = PathGuide(list((PathGuideItem(java_path_guide_items.get(i)) for i in range(java_path_guide_items.getCount()))))
        else:
            self._path_guides = None
        java_routes = java_object.getRoutes()
        if java_routes is not None and len(java_routes) > index:
            self._route = Geometry._from_java_object(java_routes[index])
        else:
            self._route = None
        java_stop_indexes = java_object.getStopIndexes()
        if java_stop_indexes is not None and len(java_stop_indexes) > index:
            self._stop_indexes = java_array_to_list(java_stop_indexes[index])
        else:
            self._stop_indexes = None
        java_stop_weights = java_object.getStopWeights()
        if java_stop_weights is not None and len(java_stop_weights) > index:
            self._stop_weights = java_stop_weights[index]
        else:
            self._stop_weights = None
        java_weights = java_object.getWeights()
        if java_weights is not None and len(java_weights) > index:
            self._weight = java_weights[index]
        else:
            self._weight = None

    @property
    def edges(self):
        """list[int]: 返回分析结果的途经弧段集合。注意，必须将 TransportationAnalystParameter 对象的 :py:meth:`TransportationAnalystParameter.set_edges_return`
                      方法设置为 True，分析结果中才会包含途经弧段集合，否则返回 None
        """
        return self._edges

    @property
    def nodes(self):
        """list[int]: 返回分析结果的途经结点集合。注意，必须将 TransportationAnalystParameter 对象的 :py:meth:`TransportationAnalystParameter.set_nodes_return` 方
                      法设置为 True，分析结果中才会包含途经结点集合，否则为一个空的数组。"""
        return self._nodes

    @property
    def path_guides(self):
        """PathGuide: 返回行驶导引。注意，必须将 TransportationAnalystParameter 对象的 :py:meth:`TransportationAnalystParameter.set_path_guides_return` 方
                                法设置为 True，分析结果中才会包含行驶导引，否则为一个空的数组。"""
        return self._path_guides

    @property
    def route(self):
        """GeoLineM: 返回分析结果的路由对象。注意，必须将 TransportationAnalystParameter 对象的 :py:meth:`TransportationAnalystParameter.set_routes_return` 方
                     法设置为 true，分析结果中才会包含路由对象，否则返回 None"""
        return self._route

    @property
    def stop_indexes(self):
        """list[int]: 返回站点索引，该数组反映了站点在分析后的排列顺序。注意，必须将 TransportationAnalystParameter 对象
                      的 :py:meth:`TransportationAnalystParameter.set_stop_indexes_return` 方法设置为 True，分析结果中才会
                      包含站点索引，否则为一个空的数组。

                      在不同的分析中，该方法的返回值代表的含义不一样：

                      - 最佳路径分析（ :py:meth:`TransportationAnalyst.find_path` 方法）:

                          - 结点模式：如设置的分析结点 ID 为 1，3，5 的三个结点，因为结果途经顺序必须为 1，3，5，所以元素值依
                            次为 0，1，2，即结果途经顺序在初始设置结点串中的索引。

                          - 坐标点模式：如设置的分析坐标点为 Pnt1，Pnt2，Pnt3，因为结果途经顺序必须为 Pnt1，Pnt2，Pnt3，所以元
                            素值依次为 0，1，2，即结果途经坐标点顺序在初始设置坐标点串中的索引。

                      - 旅行商分析（ :py:meth:`TransportationAnalyst.find_tsp_path` 方法）：

                         - 结点模式：如设置的分析结点 ID 为 1，3，5 的三个结点，而结果途经顺序为 3，5，1，则元素值依次为
                           1，2，0，即结果途经顺序在初始设置结点串中的索引。

                         - 坐标点模式：如设置的分析坐标点为 Pnt1，Pnt2，Pnt3，而结果途经顺序为 Pnt2，Pnt3，Pnt1，则元素值
                           依次为 1，2，0，即结果途经坐标点顺序在初始设置坐标点串中的索引。

                      - 多旅行商分析（ :py:meth:`TransportationAnalyst.find_mtsp_path` 方法）:

                        元素的含义与旅行商分析相同，表示对应的中心点的配送路径经过站点的次序。注意，配送模式为局部最优时，所有中
                        心点参与配送，为总花费最小模式时，参与配送的中心点数可能少于指定的中心点数。

                      - 对于最近设施查找分析（ :py:meth:`TransportationAnalyst.find_closest_facility` 方法），该方法无效。
        """
        return self._stop_indexes

    @property
    def stop_weights(self):
        """list[float]: 返回根据站点索引对站点排序后，站点间的花费（权值）。
                        该方法返回的是站点与站点间的耗费，这里的站点指的是用于分析结点或坐标点，而不是路径经过的所有结点或坐标点。
                        该方法返回的权值所关联的站点顺序与 :py:attr:`stop_indexes` 方法中返回的站点索引值的顺序一致，但对于不同的分析功能需注意其细微差别。例如：

                        - 最佳路径分析（ :py:meth:`TransportationAnalyst.find_path` 方法）: 假设指定经过点 1、2、3，则二维元素依次
                          为：1 到 2 的耗费、2 到 3 的耗费；

                        - 旅行商分析（ :py:meth:`TransportationAnalyst.find_tsp_path` 方法）：假设指定经过点 1、2、3，分析结果中站点
                          索引为 1、0、2，则二维元素依次为：2 到 1 的耗费、1 到 3 的耗费；

                        - 多旅行商分析（ :py:meth:`TransportationAnalyst.find_mtsp_path` 方法）: 即物流配送，元素为该路径所经过的站点的之间的耗费，
                          需要注意的是，多旅行商分析的路径经过的站点是包括中心点的，且路径的起终点均是中心点。例如，一条结果路径是
                          从中心点 1 出发，经过站点 2、3、4，对应的站点索引为 1、2、0，则站点权重依次为：1 到 3 的耗费、3 到 4 的
                          耗费、4 到 2 的耗费和 2 到 1 的耗费。

                        - 对于最近设施查找分析（ :py:meth:`TransportationAnalyst.find_closest_facility` 方法），该方法无效。
        """
        return self._stop_weights

    @property
    def weight(self):
        """float: 花费的权值。"""
        return self._weight


class NetworkDatasetErrors:
    __doc__ = "\n    网络数据集拓扑关系检查结果，包括网络数据集弧段错误信息、结点错误信息。\n    "

    def __init__(self, java_errors):
        self._node_errors = java_errors.getNodeErrorInfos()
        self._arc_errors = java_errors.getArcErrorInfos()

    @property
    def node_errors(self):
        """dict[int,int]: 结点错误信息。键为网络数据集中错误结点的 SmID，值为错误类型。"""
        return self._node_errors

    @property
    def arc_errors(self):
        """dict[int,int]: 弧段错误信息。键为网络数据集中错误弧段的 SmID，值为错误类型。"""
        return self._arc_errors


def validate_network_dataset(network_dataset, edge_id_field=None, f_node_id_field=None, t_node_id_field=None, node_id_field=None):
    """
    该方法用于对网络数据集进行检查，给出错误信息，便于用户针对错误信息对数据进行修改，以避免由于数据错误导致网络分析错误。

    对网络数据集进行检查的结果错误类型如下表所示：

    .. image:: ../image/TransportationNetwork_Check.png

    :param network_dataset: 被检查的网络数据集或三维网络数据集
    :type network_dataset: DatasetVector or str
    :param str edge_id_field: 网络数据集的弧段 ID 字段，如果为空，则默认使用网络数据集中存储的弧段 ID字段。
    :param str f_node_id_field: 网络数据集的起始结点 ID 字段，如果为空，则默认使用网络数据集中存储的起始结点  ID字段。
    :param str t_node_id_field: 网络数据集的终止结点 ID 字段，如果为空，则默认使用网络数据集中存储的终止结点 ID字段。
    :param str node_id_field: 网络数据集的结点 ID 字段，如果为空，则默认使用网络数据集中存储的结点 ID字段。
    :return: 网络数据集错误结果信息。
    :rtype: NetworkDatasetErrors
    """
    if network_dataset is None:
        raise ValueError("network_dataset is None")
    if network_dataset.type is not DatasetType.NETWORK:
        if network_dataset.type is not DatasetType.NETWORK3D:
            raise ValueError("only support NETWORK or NETWORK3D Dataset")
    if edge_id_field is None:
        edge_id_field = network_dataset.get_field_name_by_sign(FieldSign.EDGEID)
    if f_node_id_field is None:
        f_node_id_field = network_dataset.get_field_name_by_sign(FieldSign.FNODE)
    if t_node_id_field is None:
        t_node_id_field = network_dataset.get_field_name_by_sign(FieldSign.TNODE)
    if node_id_field is None:
        node_id_field = network_dataset.child_dataset.get_field_name_by_sign(FieldSign.NODEID)
    if network_dataset.type is DatasetType.NETWORK3D:
        java_analyst_setting = get_jvm().com.supermap.realspace.networkanalyst.FacilityAnalystSetting3D()
        java_analyst_setting.setNetworkDataset(oj(network_dataset))
        java_analyst_setting.setNodeIDField(node_id_field)
        java_analyst_setting.setEdgeIDField(edge_id_field)
        java_analyst_setting.setFNodeIDField(f_node_id_field)
        java_analyst_setting.setTNodeIDField(t_node_id_field)
        java_facility_analyst = get_jvm().com.supermap.realspace.networkanalyst.FacilityAnalyst3D()
        java_facility_analyst.setAnalystSetting(java_analyst_setting)
        java_errors = java_facility_analyst.check()
        if java_errors is not None:
            return NetworkDatasetErrors(java_errors)
        return
    java_analyst_setting = get_jvm().com.supermap.analyst.networkanalyst.TransportationAnalystSetting()
    java_analyst_setting.setNetworkDataset(oj(network_dataset))
    java_analyst_setting.setNodeIDField(node_id_field)
    java_analyst_setting.setEdgeIDField(edge_id_field)
    java_analyst_setting.setFNodeIDField(f_node_id_field)
    java_analyst_setting.setTNodeIDField(t_node_id_field)
    java_transportation_analyst = get_jvm().com.supermap.analyst.networkanalyst.TransportationAnalyst()
    java_transportation_analyst.setAnalystSetting(java_analyst_setting)
    java_errors = java_transportation_analyst.check()
    if java_errors is not None:
        return NetworkDatasetErrors(java_errors)
    return


def fix_ring_edge_network_errors(network_dataset, error_ids, edge_id_field=None, f_node_id_field=None, t_node_id_field=None, node_id_field=None):
    """
    修复网络数据集拓扑错误中弧段的首尾结点相等这种拓扑错误，关于网络数据集的拓扑错误检查，具体参考 :py:meth:`.validate_network_dataset` .

    对于首尾相等的弧段，会自动取弧段的中心点将弧段打断为两条。

    :param network_dataset: 待处理的网络数据集
    :type network_dataset: str or DatasetVector
    :param error_ids: 首尾相等弧段的 SmID。
    :type error_ids: list[int] or tuple[int] or str
    :param str edge_id_field: 网络数据集的弧段 ID 字段，如果为空，则默认使用网络数据集中存储的弧段 ID字段。
    :param str f_node_id_field: 网络数据集的起始结点 ID 字段，如果为空，则默认使用网络数据集中存储的起始结点  ID字段。
    :param str t_node_id_field: 网络数据集的终止结点 ID 字段，如果为空，则默认使用网络数据集中存储的终止结点 ID字段。
    :param str node_id_field: 网络数据集的结点 ID 字段，如果为空，则默认使用网络数据集中存储的结点 ID字段。
    :return: 成功返回 True, 失败返回 False
    :rtype: bool
    """
    network_dataset = get_input_dataset(network_dataset)
    if not isinstance(network_dataset, DatasetVector):
        raise ValueError("network_dataset required DatasetVector")
    elif network_dataset.type is not DatasetType.NETWORK:
        if network_dataset.type is not DatasetType.NETWORK3D:
            raise ValueError("only support NETWORK or NETWORK3D Dataset")
    error_ids = split_input_int_list_from_str(error_ids)
    if edge_id_field is None:
        edge_id_field = network_dataset.get_field_name_by_sign(FieldSign.EDGEID)
    if f_node_id_field is None:
        f_node_id_field = network_dataset.get_field_name_by_sign(FieldSign.FNODE)
    if t_node_id_field is None:
        t_node_id_field = network_dataset.get_field_name_by_sign(FieldSign.TNODE)
    if node_id_field is None:
        node_id_field = network_dataset.child_dataset.get_field_name_by_sign(FieldSign.NODEID)
    if network_dataset.type is DatasetType.NETWORK3D:
        result = get_jvm().com.supermap.realspace.networkanalyst.NetworkBuilder3D.fixRingEdgeErrors(oj(network_dataset), error_ids, str(edge_id_field), str(f_node_id_field), str(t_node_id_field), str(node_id_field))
    else:
        result = get_jvm().com.supermap.analyst.networkanalyst.NetworkBuilder.fixRingEdgeErrors(oj(network_dataset), error_ids, str(edge_id_field), str(f_node_id_field), str(t_node_id_field), str(node_id_field))
    return result


class ServiceAreaResult:
    __doc__ = "\n    服务区分析结果类。\n    "

    def __init__(self, java_object, index):
        java_edges = java_object.getEdges()
        if java_edges is not None:
            self._edges = java_array_to_list(java_edges[index])
        else:
            self._edges = None
        java_nodes = java_object.getNodes()
        if java_nodes is not None:
            self._nodes = java_array_to_list(java_nodes[index])
        else:
            self._nodes = None
        routes = java_object.getRoutes()
        if routes is not None:
            route_counts = java_object.getServiceRouteCounts()
            route_start_index = 0
            if index > 0:
                for i in range(index - 1):
                    route_start_index += route_counts[i]

            self._routes = []
            for i in range(route_start_index, route_start_index + route_counts[index], 1):
                self._routes.append(Geometry._from_java_object(routes[i]))

        else:
            self._routes = None
        java_weight = java_object.getWeights()
        if java_weight is not None:
            self._weight = java_weight[index]
        else:
            self._weight = None
        java_regions = java_object.getServiceRegions()
        if java_regions is not None:
            self._service_region = Geometry._from_java_object(java_regions[index])
        else:
            self._service_region = None

    @property
    def edges(self):
        """list[int]: 分析结果的途经弧段集合"""
        return self._edges

    @property
    def nodes(self):
        """list[int]: 分析结果的途经结点集合"""
        return self._nodes

    @property
    def routes(self):
        """list[GeoLineM]: 分析结果的路由对象集合。存储了按照中心点的指定顺序，每个服务区所覆盖（包括部分覆盖）的路由。"""
        return self._routes

    @property
    def weight(self):
        """float: 花费的权值"""
        return self._weight

    @property
    def service_region(self):
        """GeoRegion: 分析结果的服务区面对象"""
        return self._service_region


class SupplyCenter:
    __doc__ = "\n    资源供给中心类。资源供给中心类，存储了资源供给中心的信息，包括资源供给中心的 ID、最大耗费和类型。\n    "

    def __init__(self, supply_center_type, center_node_id, max_weight, resource=0):
        """
        初始化对象

        :param supply_center_type: 资源供给中心点的类型包括非中心，固定中心和可选中心。固定中心用于资源分配分析；固定中心和可选中心用于选址分析，
                                   非中心在两种网络分析时都不予考虑。
        :type supply_center_type: SupplyCenterType or str
        :param int center_node_id: 资源供给中心点的 ID。
        :param float max_weight: 资源供给中心的最大耗费（阻值）
        :param float resource: 资源供给中心的资源量
        """
        self._center_type = SupplyCenterType._make(supply_center_type, "null")
        self._center_node_id = int(center_node_id)
        self._max_weight = float(max_weight)
        self._resource = float(resource)

    @property
    def supply_center_type(self):
        """SupplyCenterType: 络分析中资源供给中心点的类型"""
        return self._center_type

    def set_supply_center_type(self, value):
        """
        设置网络分析中资源供给中心点的类型

        :param value: 资源供给中心点的类型包括非中心，固定中心和可选中心。固定中心用于资源分配分析；固定中心和可选中心用于选址分析，
                      非中心在两种网络分析时都不予考虑。
        :type value: SupplyCenterType or str
        :return: self
        :rtype: SupplyCenter
        """
        self._center_type = SupplyCenterType._make(value, "null")
        return self

    @property
    def center_node_id(self):
        """int: 资源供给中心点的 ID"""
        return self._center_node_id

    def set_center_node_id(self, value):
        """
        设置资源供给中心点的 ID。

        :param int value: 资源供给中心点的 ID
        :return: self
        :rtype: SupplyCenter
        """
        self._center_node_id = int(value)
        return self

    @property
    def max_weight(self):
        """float: 资源供给中心的最大耗费。"""
        return self._max_weight

    def set_max_weight(self, value):
        """
        设置 资源供给中心的最大耗费。中心点最大阻值设置越大，表示中心点所提供的资源可影响范围越大。
        最大阻力值是用来限制需求点到中心点的花费。如果需求点（弧段或结点）到此中心的花费大于最大阻力值，则该需求点被过滤掉。最大阻力值可编辑。

        :param float value: 资源供给中心的最大耗费（阻值）
        :return: self
        :rtype: SupplyCenter
        """
        self._max_weight = float(value)
        return self

    @property
    def resource(self):
        """float: 资源供给中心的资源量"""
        return self._resource

    def set_resource(self, value):
        """
        设置资源供给中心的资源量

        :param float value: 资源供给中心的资源量
        :return: self
        :rtype: SupplyCenter
        """
        self._resource = float(value)
        return self

    @property
    def _jobject(self):
        java_object = get_jvm().com.supermap.analyst.networkanalyst.SupplyCenter()
        if self.supply_center_type is not None:
            java_object.setType(oj(self.supply_center_type))
        if self.center_node_id is not None:
            java_object.setID(int(self.center_node_id))
        if self.max_weight is not None:
            java_object.setMaxWeight(float(self.max_weight))
        if self.resource is not None:
            java_object.setResourceValue(float(self.resource))
        return java_object


@unique
class SupplyCenterType(JEnum):
    __doc__ = "\n    网络分析中资源中心点类型常量，主要用于资源分配和选址分区\n\n    :var SupplyCenterType.NULL: 非中心点，在资源分配和选址分区时都不予考虑。\n    :var SupplyCenterType.OPTIONALCENTER: 可选中心点，用于选址分区\n    :var SupplyCenterType.FIXEDCENTER: 固定中心点，用于资源分配和选址分区。\n    "
    NULL = 0
    OPTIONALCENTER = 1
    FIXEDCENTER = 2

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.networkanalyst.SupplyCenterType"

    @classmethod
    def _externals(cls):
        return {'optional':SupplyCenterType.OPTIONALCENTER,  'fixed':SupplyCenterType.FIXEDCENTER, 
         'none':SupplyCenterType.NULL}


@unique
class AllocationDemandType(JEnum):
    __doc__ = "\n    资源分配需求模式\n\n    :var AllocationDemandType.NODE: 结点需求模式。这种模式下，分析时只考虑结点对资源的需求量，将弧段的需求排除。例如在圣诞节，圣\n                                    诞老人给儿童派送礼物，圣诞老人的位置为固定中心点、礼物数为资源量，儿童住址为需求结点、某个\n                                    儿童对礼物数量的需求为该结点的结点需求字段值。很明显圣诞老人结儿童派送礼物时，我们只考虑礼物\n                                    的分配则这就是一个结点需求事件。\n    :var AllocationDemandType.EDGE: 弧段需求模式。这种模式下，分析时只考虑弧段对资源的需求量，将结点的需求排除。例如在圣诞节，圣\n                                    诞老人给儿童派送礼物，圣诞老人的位置为固定中心点、圣诞老人汽车汽油存量为资源量，儿童住址为需求\n                                    结点、从固定中心点至相邻儿童住址以及相邻儿童住址见的行驶油耗为弧段需求字段值。很明显圣诞老人结\n                                    儿童派送礼物时，我们只考虑行驶油耗的分配则这就是一个弧段需求事件。\n    :var AllocationDemandType.BOTH: 结点和弧段需求模式。同时考虑结点的需求和弧段的需求。例如在圣诞节，圣诞老人给儿童派送礼物，即\n                                    考虑礼物的分配又考虑行驶油耗则这就是一个结点和弧段需求事件。\n\n    "
    NODE = 1
    EDGE = 2
    BOTH = 3

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.networkanalyst.AllocationDemandType"


class DemandResult:
    __doc__ = "\n    需求结果类。该类用于返回需求结果的相关信息，包括需求结点 ID和资源供给中心 ID等。\n    "

    def __init__(self, java_object):
        self._actual_resource = java_object.getActualResourceValue()
        self._demand_id = java_object.getID()
        self._supply_center_node_id = java_object.getSupplyCenterID()
        self._is_edge = java_object.isEdge()

    @property
    def actual_resource(self):
        """float: 实际被分配的资源量，仅对资源分配有效。"""
        return self._actual_resource

    @property
    def demand_id(self):
        """int: 当 :py:attr:`is_edge` 方法为 True 时，该方法返回的是弧段的 ID，当 为 False 时，该方法返回的是结点的 ID。"""
        return self._demand_id

    @property
    def supply_center_node_id(self):
        """int: 资源供给中心 ID"""
        return self._supply_center_node_id

    @property
    def is_edge(self):
        """bool: 返回需求结果是否是弧段。如果不是弧段，则需求结果是结点。仅对资源分配有效，否则为 False。"""
        return self._is_edge


class AllocationAnalystResult:
    __doc__ = "\n    资源分配分析结果类。\n    "

    def __init__(self, nodes, edges, demands, routes, node_id):
        self._nodes = nodes
        self._edges = edges
        self._demands = demands
        self._routes = routes
        self._supply_center_node_id = node_id

    @property
    def demand_results(self):
        """DemandResult: 需求结果对象"""
        return self._demands

    @property
    def edges(self):
        """list[int]: 分析结果中经过的弧段ID集合"""
        return self._edges

    @property
    def nodes(self):
        """list[int]: 分析结果中经过的结点ID集合"""
        return self._nodes

    @property
    def routes(self):
        """GeoLineM: 资源分配分析出的分配路径路由结果。"""
        return self._routes

    @property
    def supply_center_node_id(self):
        """int: 所属的资源供给中心点的 ID"""
        return self._supply_center_node_id

    @staticmethod
    def parse(java_object, supply_centers):
        java_nodes = java_object.getNodes()
        java_edges = java_object.getEdges()
        if len(java_nodes) == len(supply_centers):
            if len(java_edges) == len(supply_centers):
                java_demand_results = java_object.getDemandResults()
                demands = {}
                for center in supply_centers:
                    demands[center.center_node_id] = []

                if java_demand_results is not None:
                    for i in range(len(java_demand_results)):
                        demand = DemandResult(java_demand_results[i])
                        demands[demand.supply_center_node_id].append(demand)

                results = []
                nodes = java_array_to_list(java_nodes)
                edges = java_array_to_list(java_edges)
                java_routes = java_object.getRoutes()
                routes = []
                if len(java_routes) == sum(list((len(item) for item in edges))):
                    for i in range(len(java_routes)):
                        routes.append(Geometry._from_java_object(java_routes[i]))

                route_index = 0
                for i in range(len(nodes)):
                    item_nodes = java_array_to_list(nodes[i])
                    item_edges = java_array_to_list(edges[i])
                    center_node_id = supply_centers[i].center_node_id
                    item_demands = demands[center_node_id]
                    item_routes = []
                    if len(routes) > 0:
                        item_routes = routes[route_index[:route_index + len(item_edges)]]
                        route_index += len(item_edges)
                    results.append(AllocationAnalystResult(item_nodes, item_edges, item_demands, item_routes, center_node_id))

                return results


class TerminalPoint:
    __doc__ = "\n    终端点，用于分组分析，终端点包含坐标信息和负载量\n    "

    def __init__(self, point, load):
        """
        初始化对象

        :param Point2D point: 坐标点信息
        :param int load: 负载量
        """
        self._load = 1
        self._point = None
        self.set_point(point).set_load(load)

    def set_point(self, point):
        """
        设置坐标点

        :param Point2D point: 坐标点
        :return: self
        :rtype: TerminalPoint
        """
        self._point = Point2D.make(point)
        return self

    def set_load(self, load):
        """
        设置负载量

        :param int load: 负载量
        :return: self
        :rtype: TerminalPoint
        """
        self._load = int(load)
        return self

    @property
    def load(self):
        """int: 负载量"""
        return self._load

    @property
    def point(self):
        """Point2D: 坐标点"""
        return self._point

    @property
    def _jobject(self):
        java_object = get_jvm().com.supermap.analyst.networkanalyst.GroupPointInfo()
        java_object.setLoad(int(self.load))
        java_object.setPoint(oj(self.point))
        return java_object


class GroupAnalystResultItem:
    __doc__ = "\n    分组分析结果项类。组分析结果项记录了每一个分组中中心点索引，该组包含的分配点索引集合，该分组中的总耗费，各个分配点到中心点的线\n    路集合以及该分组的总负载量。\n    "

    def __init__(self, java_object):
        self._group_center = java_object.getGroupCenter()
        self._group_member = java_array_to_list(java_object.getGroupMember())
        self._cost = java_object.getCost()
        java_lines = java_object.getLines()
        if java_lines is not None:
            self._lines = list((Geometry._from_java_object(item) for item in java_lines))
        else:
            self._lines = None
        self._load_sum = java_object.getLoadSum()

    @property
    def center(self):
        """int: 分组结果的中心点索引"""
        return self._group_center

    @property
    def members(self):
        """list[int]: 分组结果的分配点索引集合"""
        return self._group_member

    @property
    def cost(self):
        """float: 分组结果的总耗费"""
        return self._cost

    @property
    def lines(self):
        """list[GeoLineM]: 分组结果的各个分配点到中心点的线路集合"""
        return self._lines

    @property
    def load_sum(self):
        """float: 分组结果的总负载量"""
        return self._load_sum


class GroupAnalystResult:
    __doc__ = "\n    分组分析结果类。该类用于返回分组分析的结果，包括未分配到的分配点集合和分析结果项集合。\n    "

    def __init__(self, java_object):
        self._errors = java_array_to_list(java_object.getErrors())
        java_items = java_object.getGroupAnalystResultItems()
        if java_items is not None:
            self._items = list((GroupAnalystResultItem(item) for item in java_items))
        else:
            self._items = None

    @property
    def error_terminal_point_indexes(self):
        """list[int]: 未分配到的分配点集合"""
        return self._errors

    @property
    def groups(self):
        """list[GroupAnalystResultItem]: 分析结果项集合"""
        return self._items


class SupplyResult:
    __doc__ = "\n    资源供给中心点结果类。\n\n    该类提供了资源供给的结果，包括资源供给中心的类型、ID、最大阻值、需求点的数量、平均耗费和总耗费等。\n    "

    def __init__(self, java_object):
        self._average_weight = java_object.getAverageWeight()
        self._demand_count = java_object.getDemandCount()
        self._center_node_id = java_object.getID()
        self._max_weight = java_object.getMaxWeight()
        self._total_weight = java_object.getTotalWeights()
        java_supply_type = java_object.getType()
        if java_supply_type is not None:
            self._supply_center_type = SupplyCenterType._make(java_supply_type.name())
        else:
            self._supply_center_type = None

    @property
    def average_weight(self):
        """float: 平均耗费，即总耗费除以需求点数"""
        return self._average_weight

    @property
    def demand_count(self):
        """int: 该资源供给中心所服务的需求结点的数量"""
        return self._demand_count

    @property
    def center_node_id(self):
        """int: 资源供给中心的 ID"""
        return self._center_node_id

    @property
    def max_weight(self):
        """float: 资源供给中心的最大耗费（阻值）。最大阻力值是用来限制需求点到中心点的花费。如果需求点（结点）到此中心的花费大于最
                  大阻力值，则该需求点被过滤掉。最大阻力值可编辑。"""
        return self._max_weight

    @property
    def total_weight(self):
        """float: 总耗费量。当选址分区分析选择从资源供给中心分配资源时，总耗费为从该资源供给中心到其所服务的所有需求结点的耗费的总
                  和；反之，不从资源供给中心分配，则总耗费为该资源供给中心所服务的所有需求结点到该资源供给中心的耗费的总和。"""
        return self._total_weight

    @property
    def type(self):
        """SupplyCenterType: 该资源供给中心的类型"""
        return self._supply_center_type


class LocationAnalystResult:
    __doc__ = "\n    选址分区分析结果类。\n    "

    def __init__(self, java_object):
        java_demand_results = java_object.getDemandResults()
        if java_demand_results is not None:
            self._demand_result = list((DemandResult(item) for item in java_demand_results))
        else:
            self._demand_result = None
        java_supply_results = java_object.getSupplyResults()
        if java_supply_results is not None:
            self._supply_center = list((SupplyResult(item) for item in java_supply_results))
        else:
            self._supply_center = None

    @property
    def demand_results(self):
        """list[DemandResult]: 需求结果对象数组"""
        return self._demand_result

    @property
    def supply_results(self):
        """list[SupplyResult]: 资源供给结果对象数组"""
        return self._supply_center


@unique
class VRPAnalystType(JEnum):
    __doc__ = "\n    物流分析中分析模式\n\n    :var VRPAnalystType.LEASTCOST: 耗费最少模式\n    :var VRPAnalystType.AVERAGECOST: 平均耗费模式\n    :var VRPAnalystType.AREAANALYST: 区域分析模式\n    "
    LEASTCOST = 0
    AVERAGECOST = 1
    AREAANALYST = 2

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.networkanalyst.AnalystType"

    @classmethod
    def _externals(cls):
        return {'least':VRPAnalystType.LEASTCOST,  'average':VRPAnalystType.AVERAGECOST, 
         'area':VRPAnalystType.AREAANALYST}


@unique
class VRPDirectionType(JEnum):
    __doc__ = "\n    VRP分析路线的类型\n\n    :var VRPDirectionType.ROUNDROUTE: 从中心点出发并回到中心点。\n    :var VRPDirectionType.STARTBYCENTER: 从中心点出发但不回到中心点。\n    :var VRPDirectionType.ENDBYCENTER: 不从中心点出发但回到中心点。\n    "
    ROUNDROUTE = 0
    STARTBYCENTER = 1
    ENDBYCENTER = 2

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.networkanalyst.VRPDirectionType"


class VRPAnalystParameter:
    __doc__ = "\n    物流配送分析参数设置类。\n\n    该类主要用来对物流配送分析的参数进行设置。通过交通网络分析参数设置类可以设置障碍边、障碍点、权值字段信息的名字标识，还可以对分析结果\n    进行一些设置，即在分析结果中是否包含分析途经的以下内容：结点集合，弧段集合，路由对象集合以及站点集合。\n    "

    def __init__(self):
        self._analyst_type = VRPAnalystType.LEASTCOST
        self._barrier_edges = None
        self._barrier_nodes = None
        self._barrier_points = None
        self._is_edges_return = False
        self._is_nodes_return = False
        self._is_path_guides_return = False
        self._is_routes_return = False
        self._route_count = 0
        self._is_stop_indexes_return = False
        self._time_weight_field = None
        self._weight_name = None
        self._vrp_direction_type = VRPDirectionType.ROUNDROUTE

    @property
    def analyst_type(self):
        """VRPAnalystType: 物流分析中的分析模式"""
        return self._analyst_type

    def set_analyst_type(self, value=True):
        """
        设置物流分析模式，包括 LEASTCOST 最小耗费模式（默认值）、AVERAGECOST 平均耗费模式、AREAANALYST 区域分析模式。

        :param value: 物流分析模式
        :type value: VRPAnalystType or str
        :return: self
        :rtype: VRPAnalystParameter
        """
        self._analyst_type = VRPAnalystType._make(value, VRPAnalystType.LEASTCOST)
        return self

    @property
    def barrier_edges(self):
        """list[int]: 障碍弧段 ID 列表"""
        return self._barrier_edges

    def set_barrier_edges(self, value=True):
        """
        设置障碍弧段 ID 列表

        :param value: 障碍弧段 ID 列表
        :type value: list[int]:
        :return: self
        :rtype: VRPAnalystParameter
        """
        self._barrier_edges = split_input_int_list_from_str(value)
        return self

    @property
    def barrier_nodes(self):
        """list[int]: 障碍结点 ID 列表"""
        return self._barrier_nodes

    def set_barrier_nodes(self, value=True):
        """
        设置障碍结点 ID 列表

        :param value: 障碍结点 ID 列表
        :type value: list[int]:
        :return: self
        :rtype: VRPAnalystParameter
        """
        self._barrier_nodes = split_input_int_list_from_str(value)
        return self

    @property
    def barrier_points(self):
        """list[Point2D]: 障碍结点的坐标列表"""
        return self._barrier_points

    def set_barrier_points(self, points=True):
        """
        设置障碍结点的坐标列表

        :param points: 障碍结点的坐标列表
        :type points: list[Point2D] or tuple[Point2D]
        :return: self
        :rtype: VRPAnalystParameter
        """
        if isinstance(points, Point2D):
            points = [
             points]
        elif isinstance(points, (list, tuple)):
            points = list((Point2D.make(p) for p in points))
            self._barrier_points = list(filter((lambda p: p is not None), points))
        else:
            if points is None:
                self._barrier_points = None
            else:
                raise ValueError("points required list[Point2D]")
        return self

    @property
    def is_edges_return(self):
        """bool: 分析结果中是否包含途经弧段"""
        return self._is_edges_return

    def set_edges_return(self, value=True):
        """
        设置分析结果中是否包含途经弧段

        :param bool value: 分析结果中是否包含途经弧段
        :return: self
        :rtype: VRPAnalystParameter
        """
        self._is_edges_return = parse_bool(value)
        return self

    @property
    def is_nodes_return(self):
        """bool: 分析结果中是否包含结点"""
        return self._is_nodes_return

    def set_nodes_return(self, value=True):
        """
        设置分析结果中是否包含结点

        :param bool value: 分析结果中是否包含结点
        :return: self
        :rtype: VRPAnalystParameter
        """
        self._is_nodes_return = parse_bool(value)
        return self

    @property
    def is_routes_return(self):
        """bool: 分析结果中是否包含路由对象"""
        return self._is_routes_return

    def set_routes_return(self, value=True):
        """
        设置分析结果中是否包含路由对象的集合

        :param bool value: 分析结果中是否包含路由对象的集合
        :return: self
        :rtype: VRPAnalystParameter
        """
        self._is_routes_return = parse_bool(value)
        return self

    @property
    def is_path_guides_return(self):
        """bool: 分析结果中是否包含行驶导引"""
        return self._is_path_guides_return

    def set_path_guides_return(self, value=True):
        """
        设置分析结果中是否包含行驶导引。

        :param bool value: 分析结果中是否包含行驶导引。必须将该方法设置为 True，并且通过 :py:class:`TransportationAnalystSetting` 类
                            的 :py:meth:`TransportationPathAnalystSetting.set_edge_name_field` 方法设置了弧段名称字段，分析结果
                            中才会包含行驶导引集合，否则将不会返回行驶导引，但不影响分析结果中其他内容的获取。
        :return: self
        :rtype: VRPAnalystParameter
        """
        self._is_path_guides_return = parse_bool(value)
        return self

    @property
    def is_stop_indexes_return(self):
        """bool: 是否包含站点索引"""
        return self._is_stop_indexes_return

    def set_stop_indexes_return(self, value=True):
        """
        设置是否包含站点索引

        :param bool value: 是否包含站点索引
        :return: self
        :rtype: VRPAnalystParameter
        """
        self._is_stop_indexes_return = parse_bool(value)
        return self

    @property
    def route_count(self):
        """int: 一次分析中派出车辆数目值"""
        return self._route_count

    def set_route_count(self, value):
        """
        设置一次分析中派出车辆数目值。按要求设置，此分析中以车辆数为前提得到线路数，线路数与实际派出车辆数相同；若不设置此参数，默认
        派出车辆数不会超过可以提供的车辆总数 N（vehicleInfo[N]）

        :param int value:  派出车辆数目
        :return: self
        :rtype: VRPAnalystParameter
        """
        if value is not None:
            self._route_count = int(value)
        return self

    @property
    def time_weight_field(self):
        """str: 时间字段信息的名称"""
        return self._time_weight_field

    def set_time_weight_field(self, value):
        """
        设置时间字段信息的名称。

        :param str value: 时间字段信息名称，设置的值是 :py:class:`TransportationAnalystSetting` 中权重字段信息的名称。
        :return: self
        :rtype: VRPAnalystParameter
        """
        if value is not None:
            self._time_weight_field = str(value)
        else:
            self._time_weight_field = None
        return self

    @property
    def weight_name(self):
        """str: 权值字段信息的名称"""
        return self._weight_name

    def set_weight_name(self, value):
        """
        设置权值字段信息的名称

        :param str value: 权值字段信息的名称
        :return: self
        :rtype: VRPAnalystParameter
        """
        if value is not None:
            self._weight_name = str(value)
        else:
            self._weight_name = None
        return self

    @property
    def vrp_direction_type(self):
        """VRPDirectionType:  物流分析路线的类型"""
        return self._vrp_direction_type

    def set_vrp_direction_type(self, value):
        """
        设置物流分析路线的类型

        :param value: 物流分析路线的类型
        :type value: VRPDirectionType or str
        :return: self
        :rtype: VRPAnalystParameter
        """
        self._vrp_direction_type = VRPDirectionType._make(value, VRPDirectionType.ROUNDROUTE)
        return self

    @property
    def _jobject(self):
        java_object = get_jvm().com.supermap.analyst.networkanalyst.VRPAnalystParameter()
        if self.analyst_type is not None:
            java_object.setAnalystType(oj(self.analyst_type))
        if self.barrier_edges is not None:
            java_object.setBarrierEdges(to_java_int_array(self.barrier_edges))
        if self.barrier_nodes is not None:
            java_object.setBarrierNodes(to_java_int_array(self.barrier_nodes))
        if self.barrier_points is not None:
            java_object.setBarrierPoints(to_java_point2ds(self.barrier_points))
        java_object.setEdgesReturn(bool(self.is_edges_return))
        java_object.setNodesReturn(bool(self.is_nodes_return))
        java_object.setPathGuidesReturn(bool(self.is_path_guides_return))
        java_object.setStopIndexesReturn(bool(self.is_stop_indexes_return))
        java_object.setRoutesReturn(bool(self.is_routes_return))
        java_object.setRouteCount(int(self.route_count))
        if self.time_weight_field is not None:
            java_object.setTimeWeight(self.time_weight_field)
        if self.weight_name is not None:
            java_object.setWeightName(str(self.weight_name))
        if self.vrp_direction_type is not None:
            java_object.setVRPDirectionType(oj(self.vrp_direction_type))
        return java_object


class VehicleInfo:
    __doc__ = "\n    车辆信息类。存储了车辆的最大耗费值、最大负载量等信息。\n    "

    def __init__(self):
        self._area_ratio = 0.25
        self._cost = sys.float_info.max
        self._start_time = None
        self._end_time = None
        self._load_weights = None
        self._se_node = -1
        self._se_point = None

    @property
    def area_ratio(self):
        """float: 物流分析的区域系数"""
        return self._area_ratio

    def set_area_ratio(self, value):
        """
        设置物流分析的区域系数。仅当 :py:class:`VRPAnalystType` 为 :py:attr:`VRPAnalystType.AREAANALYST` 时有效。

        :param float value: 物流分析的区域系数
        :return: self
        :rtype: VehicleInfo
        """
        if value is not None:
            self._area_ratio = float(value)
        return self

    @property
    def cost(self):
        """float: 车辆的最大耗费值"""
        return self._cost

    def set_cost(self, value):
        """
        设置车辆的最大耗费值

        :param float value: 车辆的最大耗费值。
        :return: self
        :rtype: VehicleInfo
        """
        if value is not None:
            self._cost = float(value)
        return self

    @property
    def start_time(self):
        """datetime.datetime: 车辆最早发车时间"""
        return self._start_time

    def set_start_time(self, value):
        """
        设置车辆最早发车时间

        :param value: 车辆最早发车时间
        :type value: datetime.datetime or int or str
        :return: self
        :rtype: VehicleInfo
        """
        self._start_time = parse_datetime(value)
        return self

    @property
    def end_time(self):
        """datetime.datetime: 车辆最晚返回时间"""
        return self._end_time

    def set_end_time(self, value):
        """
        设置车辆最晚返回时间

        :param value: 车辆最晚返回时间
        :type value: datetime.datetime or int or str
        :return: self
        :rtype: VehicleInfo
        """
        self._end_time = parse_datetime(value)
        return self

    @property
    def load_weights(self):
        """list[float]: 车辆的负载量"""
        return self._load_weights

    def set_load_weights(self, value):
        """
        设置车辆的负载量。负载量可以为多维，例如可以同时设置最大承载重量和最大承载体积。要求分析中每一条线路的运输车辆负载量都不超过此值。

        :param value: 车辆的负载量
        :type value: list[float]
        :return: self
        :rtype: VehicleInfo
        """
        self._load_weights = split_input_float_list_from_str(value)
        return self

    @property
    def se_node(self):
        """int: 物流分析单向路线中的起止结点ID"""
        return self._se_node

    def set_se_node(self, value):
        """
        设置物流分析单向路线中的起止结点ID。

        设置该方法时，路线类型 :py:class:`VRPDirectionType` 必须为 :py:attr:`VRPDirectionType.STARTBYCENTER` 或
        者 :py:attr:`VRPDirectionType.ENDBYCENTER` 该参数方起作用。

        当路线类型为 :py:attr:`VRPDirectionType.STARTBYCENTER`  时，该参数表示车辆最终的停靠位置。

        当路线类型为 :py:attr:`VRPDirectionType.ENDBYCENTER` 时，该参数表示车辆最初的起始位置。

        :param int value: 物流分析单向路线中的起止结点ID
        :return: self
        :rtype: VehicleInfo
        """
        if value is not None:
            self._se_node = int(value)
        return self

    @property
    def se_point(self):
        """Point2D: 物流分析单向路线中的起止点坐标"""
        return self._se_point

    def set_se_point(self, value):
        """
        设置物流分析单向路线中的起止点坐标。

        设置该方法时，路线类型 :py:class:`VRPDirectionType` 必须为 :py:attr:`VRPDirectionType.STARTBYCENTER` 或
        者 :py:attr:`VRPDirectionType.ENDBYCENTER` 该参数方起作用。

        当路线类型为 :py:attr:`VRPDirectionType.STARTBYCENTER` 时，该参数表示车辆最终的停靠位置。

        当路线类型为 :py:attr:`VRPDirectionType.ENDBYCENTER` 时，该参数表示车辆最初的起始位置。

        :param Point2D value: 物流分析单向路线中的起止点坐标
        :return: self
        :rtype: VehicleInfo
        """
        self._se_point = Point2D.make(value)
        return self

    @property
    def _jobject(self):
        java_object = get_jvm().com.supermap.analyst.networkanalyst.VehicleInfo()
        java_object.setAreaRatio(float(self.area_ratio))
        java_object.setCost(float(self.cost))
        if self.start_time is not None:
            java_object.setStartTime(datetime_to_java_date(self.start_time))
        if self.end_time is not None:
            java_object.setEndTime(datetime_to_java_date(self.end_time))
        if self.load_weights is not None:
            java_object.setLoadWeights(to_java_double_array(self.load_weights))
        if self.se_node is not None:
            if int(self.se_node) > 0:
                java_object.setSEID(int(self.se_node))
        if self.se_point is not None:
            java_object.setSEPoint(oj(self.se_point))
        return java_object


class DemandPointInfo:
    __doc__ = "\n    需求点信息类。存储了需求点的坐标或者结点ID，以及需求点的需求量。\n    "

    def __init__(self):
        self._demand_node = -1
        self._demand_point = None
        self._demands = None
        self._start_time = None
        self._end_time = None
        self._unload_time = None

    @property
    def demand_node(self):
        """int: 需求点ID"""
        return self._demand_node

    def set_demand_node(self, value):
        """
        设置需求点ID

        :param int value: 需求点ID
        :return: self
        :rtype: DemandPointInfo
        """
        if value is not None:
            self._demand_node = int(value)
        return self

    @property
    def demand_point(self):
        """Point2D: 需求点坐标"""
        return self._demand_point

    def set_demand_point(self, value):
        """
        设置需求点坐标

        :param Point2D value: 需求点坐标
        :return: self
        :rtype: DemandPointInfo
        """
        self._demand_point = Point2D.make(value)
        return self

    @property
    def demands(self):
        """list[float]: 需求点的需求量。"""
        return self._demands

    def set_demands(self, value):
        """
        设置需求点的需求量。需求量可以为多维，其维度必须和车辆负载维度和意义相同。若某目的地的需求量过大超过车辆最大负载，分析中会舍弃此点。

        :param value: 需求点的需求量。
        :type value: list[float] or tuple[float]
        :return: self
        :rtype: DemandPointInfo
        """
        self._demands = split_input_float_list_from_str(value)
        return self

    @property
    def start_time(self):
        """datetime.datetime: 到达最早时间，表示车辆到达该点的最早时间点"""
        return self._start_time

    def set_start_time(self, value):
        """
        设置到达最早时间。

        :param value: 到达最早时间，表示车辆到达该点的最早时间点
        :type value: datetime.datetime or str
        :return: self
        :rtype: DemandPointInfo
        """
        self._start_time = parse_datetime(value)
        return self

    @property
    def end_time(self):
        """datetime.datetime: 达到最晚时间，表示车辆到达该点的最晚时间点"""
        return self._end_time

    def set_end_time(self, value):
        """
        设置达到最晚时间

        :param value: 达到最晚时间，表示车辆到达该点的最晚时间点
        :type value: datetime.datetime
        :return: self
        :rtype: DemandPointInfo
        """
        self._end_time = parse_datetime(value)
        return self

    @property
    def unload_time(self):
        """int: 卸载货物时间，表示车辆在该点需要停留的时间。单位默认为分钟。"""
        return self._unload_time

    def set_unload_time(self, value):
        """
        设置卸载货物时间。

        :param value: 卸载货物时间，表示车辆在该点需要停留的时间。单位默认为分钟。
        :type value: int
        :return: self
        :rtype: DemandPointInfo
        """
        if value is not None:
            self._unload_time = int(value)
        return self

    @property
    def _jobject(self):
        java_object = get_jvm().com.supermap.analyst.networkanalyst.DemandPointInfo()
        java_object.setDemandID(int(self.demand_node))
        if self.demand_point is not None:
            java_object.setDemandPoint(oj(self.demand_point))
        if self.demands is not None:
            java_object.setDemands(to_java_double_array(self.demands))
        if self.start_time is not None:
            java_object.setStartTime(datetime_to_java_date(self.start_time))
        if self.end_time is not None:
            java_object.setEndTime(datetime_to_java_date(self.end_time))
        if self.unload_time is not None:
            java_object.setUnloadTime(int(self.unload_time))
        return java_object


class VRPAnalystResult:
    __doc__ = "\n    VRP分析结果类。\n\n    该类用于获取分析结果的路由集合、分析途经的结点集合以及弧段集合、行驶导引集合、站点集合和权值集合以及各站点的花费。以及VRP线路的时\n    间耗费与负载总耗费。\n    "

    def __init__(self, java_object, index):
        java_edges = java_object.getEdges()
        if java_edges is not None and len(java_edges) > index:
            self._edges = java_array_to_list(java_edges[index])
        else:
            self._edges = None
        java_nodes = java_object.getNodes()
        if java_nodes is not None and len(java_nodes) > index:
            self._nodes = java_array_to_list(java_nodes[index])
        else:
            self._nodes = None
        java_path_guides = java_object.getPathGuides()
        if java_path_guides is not None and len(java_path_guides) > index:
            java_path_guide_items = java_path_guides[index]
            self._path_guides = list((PathGuideItem(java_path_guide_items.get(i)) for i in range(java_path_guide_items.getCount())))
        else:
            self._path_guides = None
        java_routes = java_object.getRoutes()
        if java_routes is not None and len(java_routes) > index:
            self._route = Geometry._from_java_object(java_routes[index])
        else:
            self._route = None
        java_stop_indexes = java_object.getStopIndexes()
        if java_stop_indexes is not None and len(java_stop_indexes) > index:
            self._stop_indexes = java_array_to_list(java_stop_indexes[index])
        else:
            self._stop_indexes = None
        java_stop_weights = java_object.getStopWeights()
        if java_stop_weights is not None and len(java_stop_weights) > index:
            self._stop_weights = list(java_stop_weights[index])
        else:
            self._stop_weights = None
        java_weights = java_object.getWeights()
        if java_weights is not None and len(java_weights) > index:
            self._weight = java_weights[index]
        else:
            self._weight = None
        java_times = java_object.getTimes()
        if java_times is not None and len(java_times) > index:
            self._times = list((java_date_to_datetime(item) for item in java_times[index]))
        else:
            self._times = None
        java_vehicle_indexes = java_object.getVehicleIndexs()
        if java_vehicle_indexes is not None and len(java_vehicle_indexes) > index:
            self._vehicle_index = java_vehicle_indexes[index]
        else:
            self._vehicle_index = None
        java_demand_values = java_object.getVRPDemandValues()
        if java_demand_values is not None and len(java_demand_values) > index:
            self._demand_values = java_array_to_list(java_demand_values[index])
        else:
            self._demand_values = None

    @property
    def edges(self):
        """list[int]: 分析结果的途经弧段集合"""
        return self._edges

    @property
    def nodes(self):
        """list[int]: 分析结果的途经结点集合"""
        return self._nodes

    @property
    def path_guides(self):
        """list[PathGuideItem]: 返回行驶导引"""
        return self._path_guides

    @property
    def route(self):
        """GeoLineM: 分析结果的路由对象"""
        return self._route

    @property
    def stop_indexes(self):
        """list[int]: 站点索引，反映了站点在分析后的排列顺序。

                      根据不同的分析线路类型 :py:class:`VRPDirectionType` ，该数组的取值意义有所不同:

                       - ROUNDROUTE: 第一个元素和最后一个元素为中心点索引，其他元素为需求点索引。
                       - STARTBYCENTER: 第一个元素为中心点索引，其他元素为需求点索引。
                       - ENDBYCENTER:  最后一个元素为中心点索引，其他元素为需求点索引。
        """
        return self._stop_indexes

    @property
    def stop_weights(self):
        """list[float]: 根据站点索引对站点排序后，站点间的花费（权值）"""
        return self._stop_weights

    @property
    def weight(self):
        """float: 每条配送路线的总花费。"""
        return self._weight

    @property
    def times(self):
        """list[datetime.datetime]: 返回物流配送每条线路中各配送点出发的时间（最后一个点除外，其表示到达的时间）"""
        return self._times

    @property
    def vehicle_index(self):
        """int: 物流配送中每条线路的车辆索引"""
        return self._vehicle_index

    @property
    def vrp_demands(self):
        """list[int]: 物流配送中每条线路的负载量"""
        return self._demand_values


class TransportationAnalyst(JVMBase):
    __doc__ = "\n    交通网络分析类。该类用于提供路径分析、旅行商分析、服务区分析、多旅行商（物流配送）分析、最近设施查找和选址分区分析等交通网络分析的功能。\n\n    交通网络分析是网络分析的重要组成部分，是基于交通网络模型的分析。与设施网络模型不同，交通网络是没有方向的，即使可以为网络边线指定\n    方向，但流通介质（行人或传输的资源）可以自行决定方向、速度和目的地。\n    "

    def __init__(self, analyst_setting):
        """
        初始化对象

        :param TransportationAnalystSetting analyst_setting: 交通网络分析环境设置对象
        """
        JVMBase.__init__(self)
        self._analyst_setting = None
        self.set_analyst_setting(analyst_setting)
        self._is_load = False

    def _make_java_object(self):
        return self._jvm.com.supermap.analyst.networkanalyst.TransportationAnalyst()

    def set_analyst_setting(self, analyst_setting):
        """
        设置交通网络分析环境设置对象
        在利用交通网络分析类进行各种交通网络分析时，都要首先设置交通网络分析的环境，都要首先设置交通网络分析的环境

        :param TransportationAnalystSetting analyst_setting: 交通网络分析环境设置对象
        :return: self
        :rtype: TransportationAnalyst
        """
        if isinstance(analyst_setting, TransportationAnalystSetting):
            self._jobject.setAnalystSetting(oj(analyst_setting))
            self._analyst_setting = analyst_setting
            return self
        raise ValueError("required TransportationAnalystSetting, but " + str(type(analyst_setting)))

    @property
    def analyst_setting(self):
        """TransportationAnalystSetting: 交通网络分析环境设置对象"""
        return self._analyst_setting

    def load(self):
        """
        加载网络模型。
        该方法根据交通网络分析环境设置（TransportationAnalystSetting）对象中的环境参数，加载网络模型。在设置好交通网络分析环境的
        参数后又修改了相关参数，只有调用该方法，所做的交通网络分析环境设置才会在交通网络分析的过程中生效。

        :return: 加载成功返回 True，否则返回 False
        :rtype: bool
        """
        if self._is_load:
            self._jobject.dispose()
        self._is_load = self._jobject.load()
        return self._is_load

    def _load_internal(self):
        if self._is_load:
            return
        self._is_load = self.load()
        if not self._is_load:
            raise RuntimeError("Failed load network analyst model")

    def update_edge_weight(self, edge_id, from_node_id, to_node_id, weight_name, weight):
        """
        该方法用来更新弧段的权值。
        该方法用于对加载到内存中的网络模型的弧段权值进行修改，并不会修改网络数据集。

        该方法可以更新弧段的正向权值或反向权值。正向权重是指从弧段的起始结点到达终止结点的花费，反向权值为从弧段的终止结点到达起始
        结点的花费。因此，指定 from_node_id 为网络数据集中被更新弧段的起始结点 ID，to_node_id 为该弧段的终止结点 ID，则更新正向权值，
        反之，指定 from_node_id 为网络数据集中该弧段的终止结点 ID，to_node_id 为该弧段的起始结点 ID，则更新反向权值。

        注意，权值为负数表示弧段在该方向禁止通行。

        :param int edge_id:  被更新的弧段的 ID
        :param int from_node_id: 被更新的弧段的起始结点 ID。
        :param int to_node_id: 被更新的弧段的终止结点 ID。
        :param str weight_name: 被更新的权值字段所属的权值字段信息对象的名称
        :param float weight: 权值，即用该值更新旧值。单位与 weight_name 指定的权值信息字段对象中权值字段的单位相同。
        :return: 成功返回更新前的权值。失败返回-1.7976931348623157e+308
        :rtype: float
        """
        self._load_internal()
        if not weight_name:
            weight_name = self.analyst_setting.weight_fields[0].weight_name
        return self._jobject.updateEdgeWeight(int(edge_id), int(from_node_id), int(to_node_id), str(weight_name), float(weight))

    def find_path(self, parameter, is_least_edges=False):
        """
        最佳路径分析。
        最佳路径分析解决的问题是，在网络数据集中，给定 N 个点（N 大于等于2），找出按照给定点的次序依次经过这 N 个点的花费最小的路径。
        “花费最小”有多种理解，如时间最短、费用最低、风景最好、路况最佳、过桥最少、收费站最少、经过乡村最多等。

        .. image:: ../image/FindPath.png

        最佳路径分析的经过点是在  :py:class:`TransportationAnalystParameter` 类型的参数 parameter 中指定的。通过 TransportationAnalystParameter
        对象有两种方式可以指定经过点:

         - 使用该对象的 :py:meth:`TransportationAnalystParameter.set_nodes` 方法，以网络数据集中结点 ID 数组的形式指定最佳路径分析经过的点，因此分析过程中经过的点就是相应的网络结点；
         - 使用该对象的 :py:meth:`TransportationAnalystParameter.set_points` 方法，以坐标点串的形式指定最佳路径分析经过的点，因此分析过程中经过的点就是相应的坐标点。

        此外，通过 :py:class:`TransportationAnalystParameter` 对象还可以指定最佳路径分析需要的其他信息，如障碍点（边），分析结果是否包含路由、
        行驶导引、途经弧段或结点等。具体内容请参见 TransportationAnalystParameter 类。

        需要注意，网络分析中的旅行商分析（ :py:meth:`find_tsp_path` 方法）与最佳路径分析类似，都是在网络中寻找遍历所有经过点的花费
        最少的路径。但二者具有明显的区别，即在遍历经过点时，二者对访问经过点的顺序处理有所不同：

         - 最佳路径分析：必须按照给定的经过点的次序访问所有点；
         - 旅行商分析：需要确定最优次序来访问所有点，而并不一定按照给定的经过点的次序。

        :param TransportationAnalystParameter parameter: 交通网络分析参数对象
        :param bool is_least_edges: 是否弧段数最少。true 代表按照弧段数最少进行查询，由于弧段数少不代表弧段长度短，所以此时查出的
                                    结果可能不是最短路径。如下图所示，如果连接AB 的绿色路径的弧段数少于黄色路径，当本参数设置为 True 时，
                                    绿色路径就是查询得到的路径，当参数设置为 false 时，黄色路径就是查询得到的路径。

                                    .. image:: ../image/hasLeastEdgeCount.png

        :return: 最佳路径分析结果
        :rtype: TransportationAnalystResult
        """
        if not isinstance(parameter, TransportationAnalystParameter):
            raise ValueError("parameter required TransportationAnalystParameter, but " + str(type(parameter)))
        self._load_internal()
        java_result = self._jobject.findPath(oj(parameter), bool(is_least_edges))
        if java_result is not None:
            result = TransportationAnalyst._make_transportation_analyst_results(java_result)
            if result:
                return result[0]

    @staticmethod
    def _make_transportation_analyst_results(java_result):
        if java_result is not None:
            count = len(java_result.getWeights())
            return list((TransportationAnalystResult(java_result, i) for i in range(count)))

    def find_tsp_path(self, parameter, is_end_node_assigned=False):
        """
        旅行商分析。

        旅行商分析是查找经过指定一系列点的路径，旅行商分析是无序的路径分析。旅行商可以自己决定访问结点的顺序，目标是旅行路线阻抗总和最小（或接近最小）。

        旅行商分析的经过点是在 TransportationAnalystParameter 类型的参数 parameter 中指定的。通过 TransportationAnalystParameter 对象有两种方式可以指定经过点：

         - 使用该对象的 :py:meth:`TransportationAnalystParameter.set_nodes` 方法，以网络数据集中结点 ID 数组的形式指定旅行商分
           析经过的点，因此分析过程中经过的点就是相应的网络结点；
         - 使用该对象的 :py:meth:`TransportationAnalystParameter.set_points` 方法，以坐标点串的形式指定旅行商分析经过的点，因此
           分析过程中经过的点就是相应的坐标点。

        需要强调的是，此方法默认将给定的经过点集合中的第一个点（结点或坐标点）作为旅行商的起点。此外，用户还可以指定终点（对应方法中
        的 is_end_node_assigned 参数）。如果选择指定终点，则给定的经过点集合的最后一个点为终点，此时旅行商从第一个给定点出发，到指
        定的终点结束，而其他经过点的访问次序由旅行商自己决定。

        .. image:: ../image/FindTSPPath.png

        另外，如果选择指定终点，终点可以与起点相同，即经过点集合中的最后一个点与第一个点相同。此时，旅行商分析的结果是一条闭合路径
        ，即从起点出发，最终回到该点。

        .. image:: ../image/FindTSPPath_1.png

        注意：使用该方法时，如果选择指定终点（对应方法中的 is_end_node_assigned 参数），指定的经过点集合的第一个点与最后一点可以
        相同，也可以不同；其他点不允许有相同的点，否则会分析失败；当不指定终点时，不允许有相同的点，如果有相同点，分析会失败。

        需要注意，网络分析中的旅行商分析（ :py:meth:`find_path` 方法）与最佳路径分析类似，都是在网络中寻找遍历所有经过点的花费
        最少的路径。但二者具有明显的区别，即在遍历经过点时，二者对访问经过点的顺序处理有所不同：

         - 最佳路径分析：必须按照给定的经过点的次序访问所有点；
         - 旅行商分析：需要确定最优次序来访问所有点，而并不一定按照给定的经过点的次序。

        :param TransportationAnalystParameter parameter: 交通网络分析参数对象。
        :param bool is_end_node_assigned:  是否指定终点。指定为 true 表示指定终点，此时给定的经过点集合中最后一个点即为终点；否则不指定终点。
        :return: 旅行商分析结果
        :rtype: TransportationAnalystResult
        """
        if not isinstance(parameter, TransportationAnalystParameter):
            raise ValueError("parameter required TransportationAnalystParameter, but " + str(type(parameter)))
        self._load_internal()
        java_result = self._jobject.findTSPPath(oj(parameter), bool(is_end_node_assigned))
        if java_result is not None:
            result = TransportationAnalyst._make_transportation_analyst_results(java_result)
            if result:
                return result[0]

    def find_closest_facility(self, parameter, event_id_or_point, facility_count, is_from_event, max_weight):
        """
        根据指定的参数进行最近设施查找分析，事件点为结点 ID 或坐标。

        最近设施分析是指在网络上给定一个事件点和一组设施点，为事件点查找以最小耗费能到达的一个或几个设施点，结果为从事件点到设施点(或从设施点到事件点)的最佳路径。

        设施点和事件点是最近设施查找分析的基本要素。设施点是提供服务的设施，如学校、超市、加油站等；事件点则是需要设施点的服务的事件位置。

        例如，在某位置发生一起交通事故，要求查找在 10 分钟内最快到达的 3 家医院，超过 10 分钟能到达的都不予考虑。此例中，事故发生地即是一个事件点，周边的医院则是设施点。

        .. image:: ../image/FindClosestFacility.png

        事件点的指定方式有两种，一是通过坐标点来指定；二是以网络数据集中的结点 ID 指定，也就是将该网络结点看做事件点

        设施点则是在 TransportationAnalystParameter 类型的参数 parameter 中指定的。通过 TransportationAnalystParameter 对象有
        两种方式可以指定经过点：

         - 使用该对象的 :py:meth:`TransportationAnalystParameter.set_nodes` 方法，以网络数据集中结点 ID 数组的形式指定设施点，
           因此分析过程中使用到的设施点就是相应的网络结点；
         - 使用该对象的 :py:meth:`TransportationAnalystParameter.set_points`  方法，以坐标点串的形式指定设施点，因此分析过程中
           使用到的设施点就是相应的坐标点。

        注意：

         事件点和设施点必须为相同的类型，即都以坐标点形式指定，或都以结点 ID 形式指定。本方法要求设施点与事件点均为坐标点，即需要通过
         TransportationAnalystParameter 对象的 :py:meth:`TransportationAnalystParameter.set_points` 方法来设置设施点。

        :param TransportationAnalystParameter parameter: 交通网络分析参数对象。
        :param event_id_or_point: 事件点坐标或结点ID
        :type event_id_or_point: int or Point2D
        :param int facility_count: 要查找的设施点数量。
        :param bool is_from_event: 是否从事件点到设施点进行查找。
        :param float max_weight: 查找半径。单位同网络分析环境中设置的阻力字段，如果要查找整个网络，该值设为 0。
        :return: 分析结果。结果数量与与查找到的最近设施点的数目相同
        :rtype: list[TransportationAnalystResult]
        """
        if not isinstance(parameter, TransportationAnalystParameter):
            raise ValueError("parameter required TransportationAnalystParameter, but " + str(type(parameter)))
        else:
            self._load_internal()
            if not isinstance(event_id_or_point, int):
                event = Point2D.make(event_id_or_point)
                if event is None:
                    raise ValueError("event_id_or_point required int or Point2D")
                event = oj(event)
            else:
                event = int(event_id_or_point)
        java_result = self._jobject.findClosestFacility(oj(parameter), event, int(facility_count), parse_bool(is_from_event), float(max_weight))
        if java_result is not None:
            return TransportationAnalyst._make_transportation_analyst_results(java_result)

    def find_mtsp_path(self, parameter, center_nodes_or_points, is_least_total_cost=False):
        """
        多旅行商（物流配送）分析，配送中心为点坐标串或结点ID数组

        多旅行商分析也称为物流配送，是指在网络数据集中，给定 M 个配送中心点和 N 个配送目的地（M，N 为大于零的整数），查找经济有效的
        配送路径，并给出相应的行走路线。如何合理分配配送次序和送货路线，使配送总花费达到最小或每个配送中心的花费达到最小，是物流配送所解决的问题。

        配送中心点的指定方式有两种，一是通过坐标点集合指定，二是以网络结点 ID 数组指定。

        配送目的地则是在 TransportationAnalystParameter 类型的参数 parameter 中指定。通过 TransportationAnalystParameter 对象有两种方式可以指定配送目的地：

         - 使用该对象的 :py:meth:`TransportationAnalystParameter.set_nodes` 方法，以网络数据集中结点 ID 数组的形式指定配送目的
           地，因此分析过程中使用到的配送目的地就是相应的网络结点；
         - 使用该对象的 :py:meth:`TransportationAnalystParameter.set_points` 方法，以坐标点串的形式指定配送目的地，因此分析过
           程中使用到的配送目的地就是相应的坐标点。

        注意：

        配送中心点和配送目的地必须为相同的类型，即都以坐标点形式指定，或都以结点 ID 形式指定。本方法要求配送目的地与配送中心点均为
        坐标点。

        多旅行商分析的结果将给出每个配送中心所负责的配送目的地，以及这些配送目的地的经过顺序，和相应的行走路线，从而使该配送中心的配
        送花费最少，或者使得所有的配送中心的总花费最小。并且，配送中心点在完成其所负责的配送目的地的配送任务后，最终会回到配送中心点。

        应用实例：现有 50 个报刊零售地（配送目的地），和 4 个报刊供应地（配送中心），现寻求这 4 个供应地向报刊零售地发送报纸的最优路
        线，属物流配送问题。

        下图为报刊配送的分析结果，其中红色大一点的圆点代表 4 个报刊供应地（配送中心），而其他小一点的圆点代表报刊零售地（配送目的地），
        每个配送中心的配送方案采用不同的颜色标示，包括它所负责的配送目的地、配送次序以及配送线路。

        .. image:: ../image/MTSPPath_result1.png

        下图为上图中矩形框圈出的第 2 号配送中心的配送方案。蓝色的标有数字的小圆点是2号配送中心所负责的配送目的地（共有 18 个），2 号
        配送中心将按照配送目的地上标有数字的顺序依次发送报纸，即先送 1 号报刊零售地，再送 2 号报刊零售地，依次类推，并且沿着分析得出
        的蓝色线路完成配送，最终回到配送中心。

        .. image:: ../image/MTSPPath_result2.png

        需要注意，由于物流配送的目的是寻找使配送总花费最小或每个配送中心的花费最小的方案，因此，分析结果中有可能某些物流配送中心点不参与配送。

        :param TransportationAnalystParameter parameter: 交通网络分析参数对象。
        :param center_nodes_or_points: 配送中心点坐标串或结点 ID 数组
        :type center_nodes_or_points: list[Point2D] or list[int]
        :param bool is_least_total_cost: 配送模式是否为总花费最小方案。若为 true，则按照总花费最小的模式进行配送，此时可能会出现
                                         某些配送中心点配送的花费较多而其他的配送中心点的花费较少的情况。若为 false，则为局部最优，
                                         此方案会控制每个配送中心点的花费，使各个中心点花费相对平均，此时总花费不一定最小。
        :return: 多旅行商分析结果，结果数目为参与配送的中心点数。
        :rtype: list[TransportationAnalystResult]
        """
        if not isinstance(parameter, TransportationAnalystParameter):
            raise ValueError("parameter required TransportationAnalystParameter, but " + str(type(parameter)))
        self._load_internal()
        if isinstance(center_nodes_or_points, (list, tuple)):
            if center_nodes_or_points:
                if isinstance(center_nodes_or_points[0], int):
                    java_center = to_java_int_array(center_nodes_or_points)
            else:
                points = list((Point2D.make(p) for p in center_nodes_or_points))
                java_center = to_java_point2ds(points)
        else:
            raise ValueError("center_nodes_or_points required list[int] or list[Point2D]")
        java_result = self._jobject.findMTSPPath(oj(parameter), java_center, is_least_total_cost)
        if java_result is not None:
            return TransportationAnalyst._make_transportation_analyst_results(java_result)

    def find_service_area(self, parameter, weights, is_from_center, is_center_mutually_exclusive=False, service_area_type=ServiceAreaType.SIMPLEAREA):
        """
        服务区分析。
        服务区是以指定点为中心，在一定阻力范围内，包含所有可通达边、通达点的一个区域。服务区分析就是依据给定的阻力值（即服务半径）为
        网络上提供某种特定服务的位置（即中心点）查找其服务的范围（即服务区）的过程。阻力可以是到达的时间、距离或其他任何花费。例如：
        为网络上某点计算其 30 分钟的服务区，则结果服务区内，任意点出发到该点的时间都不会超过 30 分钟。

        服务区分析的结果包含了每个服务中心点所能服务到的路由和区域。路由是指从服务中心点出发，按照阻力值不大于所指定的服务半径的原则，
        沿网络弧段延伸出的路径；服务区则是按照一定算法将路由包围起来所形成的面状区域。如下图所示，红色圆点代表提供服务或资源的服务
        中心点，各种颜色的面状区域就是以相应的服务中心点为中心，在给定的阻力范围内的服务区，每个服务中心点所服务到的路由也以对应的颜色标示。

        .. image:: ../image/FindServiceArea_1.png

        - 服务中心点

         通过 :py:class:`TransportationAnalystParameter` 对象有两种方式可以指定服务中心点的位置:

          - 使用 :py:meth:`TransportationAnalystParameter.set_nodes` 方法，以网络数据集中结点 ID 数组的形式指定服务中心点，因
            此分析过程中使用到的服务中心点就是相应的网络结点。
          - 使用 :py:meth:`TransportationAnalystParameter.set_points` 方法，以服务中心点的坐标点串的形式指定服务中心点，因此分
            析过程中使用到的服务中心点就是相应的坐标点集合。

        - 是否从中心点分析

          是否从中心点开始分析，体现了服务中心和需要该服务的需求地的关系模式。从中心点开始分析，表示服务中心向服务需求地提供服务；
          而不从中心点开始分析，则代表服务需求地主动到服务中心获得服务。例如：某个奶站向各个居民点送牛奶，如果要对这个奶站进行服务区
          分析，查看这个奶站在允许的条件下所能服务的范围，那么在实际分析过程中应当使用从中心点开始分析的模式；另一个例子，如果想分析
          一个区域的某个学校在允许的条件下所能服务的区域时，由于在现实中都是学生主动来到学校学习，接受学校提供的服务，那么在实际分析
          过程中就应当使用不从中心点开始分析的模式。

        - 服务区互斥

          若两个或多个相邻的服务区有交集，可将它们进行互斥处理。互斥处理后，这些服务区不会有交叠。如图所示左图未进行互斥处理，右图进行了互斥处理。

          .. image:: ../image/FindServiceArea_2.png

        :param TransportationAnalystParameter parameter: 交通网络分析参数对象。
        :param weights: 服务区半径数组。数组长度应与给定的服务中心点的数量一致，且数组元素按照顺序与中心点一一对应。服务区半径的单位与指定的权值信息中的正向、反向阻力字段的单位一致。
        :type weights: list[float]
        :param bool is_from_center: 是否从中心点开始分析。
        :param bool is_center_mutually_exclusive: 是否进行服务区互斥处理。如果设置为 true，则进行互斥处理，设置为 false，则不进行互斥处理。
        :param  service_area_type: 服务区类型
        :type service_area_type: ServiceAreaType or str
        :return: 服务区分析结果
        :rtype: list[ServiceAreaResult]
        """
        if not isinstance(parameter, TransportationAnalystParameter):
            raise ValueError("parameter required TransportationAnalystParameter, but " + str(type(parameter)))
        self._load_internal()
        weights = split_input_float_list_from_str(weights)
        java_parameter = oj(parameter)
        if java_parameter is not None:
            java_parameter.setServiceType(oj(ServiceAreaType._make(service_area_type, "simple")))
        java_result = self._jobject.findServiceArea(oj(parameter), to_java_double_array(weights), parse_bool(is_from_center), parse_bool(is_center_mutually_exclusive))
        if java_result is not None:
            count = len(java_result.getWeights())
            return list((ServiceAreaResult(java_result, i) for i in range(count)))

    def find_critical_edges(self, start_node, end_node):
        """
        关键弧段查询。

        关键弧段，表示两点间必定会经过的弧段。

        通过调用该接口，可以获得两点间必定经过的弧段ID数组，如果返回值为空，则说明该两点不存在关键弧段。

        :param int start_node: 分析起点
        :param int end_node: 分析终点
        :return: 关键弧段ID数组。
        :rtype: list[int]
        """
        self._load_internal()
        return list(self._jobject.findCriticalEdges(int(start_node), int(end_node)))

    def find_critical_nodes(self, start_node, end_node):
        """
        关键结点查询。
        关键结点，表示两点间必定会经过的结点。

        通过调用该接口，可以获得两点间必定经过的结点ID数组，如果返回值为空，则说明该两点不存在关键结点。

        :param int start_node: 分析起点
        :param int end_node: 分析终点
        :return: 关键结点ID数组。
        :rtype: list[int]
        """
        self._load_internal()
        return list(self._jobject.findCriticalNodes(int(start_node), int(end_node)))

    def allocate(self, supply_centers, demand_type=AllocationDemandType.BOTH, is_connected=True, is_from_center=True, edge_demand_field="EdgeDemand", node_demand_field="NodeDemand", weight_name=None):
        """
        资源分配分析。
        资源分配分析模拟现实世界网络中资源的供需关系模型，资源根据网络阻力值的设置，由供应点逐步向需求点(包括弧段或结点)分配，并确保
        供应点能以最经济有效的方式为需求点提供资源。离中心点阻力值最小的需求点(包括弧段或结点)先得到资源，然后再分配剩余资源给阻力值
        次小的需求点(包括弧段或结点)，依此类推，直到中心点的资源耗尽，分配中止。

        :param supply_centers: 资源供给中心集合
        :type supply_centers: list[SupplyCenter] or tuple[SupplyCenter]
        :param demand_type: 资源分配模式
        :type demand_type: AllocationDemandType or str
        :param bool is_connected: 返回分析过程中生成的路由是否必须连通。进行资源分配分析过程中，允许某个中心点的资源穿越其他已完
                                  成资源分配的中心点的服务范围而继续将自己的资源分配给需求对象，即该项设置为false，这样得到的结果
                                  路由就不是连通的。如果设置为true，则在某个中心点的资源分配过程中，遇到已经被分配给其它中心的区域
                                  则停止分配，这样就可能有多余的资源堆积在该资源中心点。

                                  例如：电网送电问题是不允许有跨越情况的，它必须是相互连接的不能断开，而学生到学校上学的问题则允许
                                  设置为跨越分配。

        :param bool is_from_center: 是否从资源供给中心开始分配资源。由于网络数据中的弧段具有正反阻力，即弧段的正向阻力值与其反向阻
                                    力值可能不同，因此，在进行分析时， 从资源供给中心开始分配资源到需求点与从需求点向资源供给中心
                                    分配这两种分配形式下，所得的分析结果会不同。

                                    下面例举两个实际的应用场景，帮助进一步理解两种形式的差异，假设网络数据集中弧段的正反阻力值不同。

                                     - 从资源供给中心开始分配资源到需求点：

                                       如果你的资源中心是一些仓储中心，而需求点是各大超市，在实际的资源分配中，是将仓储中心的货物
                                       运输到其服务的超市， 这种形式就是由资源供给中心向需求点分配，即分析时要将 is_from_center
                                       设置为 true，即从资源供给中心开始分配。

                                     - 不从资源供给中心开始分配资源：

                                       如果你的资源中心是一些学校，而需求点是居民点，在实际的资源分配中，是学生从居民点出发去学校
                                       上学，这种形式就不是从资源供给中心向外分配资源了， 即分析时要将 is_from_center 设置为
                                       false，即不从资源供给中心开始分配。

        :param str edge_demand_field: 弧段需求量字段。该字段是网络数据集中，用于表示网络弧段作为需求地的所需资源量的字段名称。
        :param str node_demand_field: 结点需求量字段。该字段是网络数据集中，用于表示网络结点作为需求地的所需资源量的字段名称。
        :param str weight_name: 权值字段信息的名称
        :return: 资源分配分析结果对象
        :rtype: list[AllocationAnalystResult]
        """
        if supply_centers is None:
            raise ValueError("supply_centers is None")
        elif not isinstance(supply_centers, (list, tuple)):
            supply_centers = [
             supply_centers]
        self._load_internal()
        java_supply_centers = self._jvm.com.supermap.analyst.networkanalyst.SupplyCenters()
        for item in supply_centers:
            java_supply_centers.add(oj(item))

        java_parameter = self._jvm.com.supermap.analyst.networkanalyst.AllocationAnalystParameter()
        java_parameter.setConnected(parse_bool(is_connected))
        java_parameter.setDemandType(oj(AllocationDemandType._make(demand_type, "BOTH")))
        if edge_demand_field is not None:
            java_parameter.setEdgeDemandField(str(edge_demand_field))
        if node_demand_field is not None:
            java_parameter.setNodeDemandField(str(node_demand_field))
        java_parameter.setFromCenter(parse_bool(is_from_center))
        weight_name = weight_name or self.analyst_setting.weight_fields[0].weight_name
        java_parameter.setWeightName(str(weight_name))
        java_parameter.setSupplyCenters(java_supply_centers)
        java_result = self._jobject.allocate(java_parameter)
        return AllocationAnalystResult.parse(java_result, supply_centers)

    def find_group(self, terminal_points, center_points, max_cost, max_load, weight_name=None, barrier_nodes=None, barrier_edges=None, barrier_points=None, is_along_road=False):
        """
        分组分析。

        分组分析是基于网络分析模型，将分配点（:py:class:`TerminalPoint`）按照一定的规则（分配点到达中心点的距离不能大于最大耗费值 max_cost，
        并且每一个中心点的负载量不能大于最大负载量 max_load）寻找出所属的中心点，每当一个中心点被分配了一个分配点，则中心点所在的分组的负载量会增加该分配点对应的负载量。

        :param terminal_points: 分配点集合
        :type terminal_points: list[TerminalPoint]
        :param center_points: 中心点坐标集合
        :type center_points: list[Point2D]
        :param float max_cost: 最大耗费
        :param float max_load: 最大负载
        :param str weight_name: 权值字段信息的名称
        :param barrier_nodes: 障碍结点 ID 列表
        :type barrier_nodes: list[int] or tuple[int]
        :param barrier_edges: 障碍弧段 ID 列表
        :type barrier_edges: list[int] or tuple[int]
        :param barrier_points: 障碍坐标点列表
        :type barrier_points: list[Point2D] or tuple[Point2D]
        :param bool is_along_road: 是否沿道路进行，如果为 True，分配点会找到最近道路上一个点（可能位投影点或弧段节点），从路上上的最近点
                                   开始分析找到合理的中心点进行分簇，如果为False，则分配点会直接找到最近的中心点，再将各个中心点形成的小簇进行合并处理。
        :return: 分组分析结果
        :rtype: GroupAnalystResult
        """
        if terminal_points is None:
            raise ValueError("terminal_points is None")
        elif center_points is None:
            raise ValueError("center_points is None")
        self._load_internal()
        if not isinstance(terminal_points, (tuple, list)):
            terminal_points = [
             terminal_points]
        java_terminal_points = get_gateway().new_array(get_jvm().com.supermap.analyst.networkanalyst.GroupPointInfo, len(terminal_points))
        for index, value in enumerate(terminal_points):
            java_terminal_points[index] = oj(value)

        java_parameter = self._jvm.com.supermap.analyst.networkanalyst.GroupAnalystParameter()
        java_parameter.setPoints(to_java_point2ds(center_points))
        weight_name = weight_name or self.analyst_setting.weight_fields[0].weight_name
        java_parameter.setWeightName(str(weight_name))
        if barrier_nodes is not None:
            java_parameter.setBarrierNodes(to_java_int_array(split_input_int_list_from_str(barrier_nodes)))
        if barrier_edges is not None:
            java_parameter.setBarrierEdges(to_java_int_array(split_input_int_list_from_str(barrier_edges)))
        if barrier_points is not None:
            java_parameter.setBarrierPoints(to_java_point2ds(barrier_points))
        java_parameter.setAlongRoad(parse_bool(is_along_road))
        java_result = self._jobject.findGroup(java_parameter, java_terminal_points, float(max_cost), float(max_load))
        if java_result is not None:
            return GroupAnalystResult(java_result)

    def find_location(self, supply_centers, expected_supply_center_number=0, is_from_center=True, weight_name=None):
        """
        根据给定的参数进行选址分区分析。
        选址分区分析是为了确定一个或多个待建设施的最佳位置，使得设施可以用一种最经济有效的方式为需求方提供服务或者商品。选址分区不仅仅
        是一个选址过程，还要将需求点的需求分配到相应的设施的服务区中，因此称之为选址与分区。

        - 资源供给中心与需求点

          资源供给中心：即中心点，是提供资源和服务的设施，对应于网络结点，资源供给中心的相关信息包括最大阻力值、资源供给中心类型，资源供
          给中心在网络中所处结点的 ID 等。

          需求点：通常是指需要资源供给中心提供的服务和资源的位置，也对应于网络结点。

          最大阻力值用来限制需求点到资源供给中心的花费。如果需求点到此资源供给中心的花费大于最大阻力值，则该需求点被过滤掉，即该资源
          供给中心不能服务到此需求点。

          资源供给中心分为三种：非中心点，固定中心点和可选中心点。固定中心点是指网络中已经存在的、已建成或已确定要建立的服务设施（扮
          演资源供给角色）；可选中心点是指可以建立服务设施的资源供给中心，即待建服务设施将从这些可选中心点中选址；非中心点在分析时不
          予考虑，在实际中可能是不允许建立这项设施或者已经存在了其他设施。

          另外，分析过程中使用的需求点都为网络结点，即除了各种类型的中心点所对应的网络结点，所有网络结点都作为资源需求点参与选址分区
          分析，如果要排除某部分结点，可以将其设置为障碍点。

        - 是否从资源供给中心分配资源

          址分区可以选择从资源供给中心开始分配资源，或不从资源供给中心分配:

           - 从中心点开始分配（供给到需求）的例子：

             电能是从电站产生，并通过电网传送到客户那里去的。在这里，电站就是网络模型中的中心，因为它可以提供电力供应。电能的客户沿
             电网的线路（网络模型中的弧段）分布，他们产生了“需求”。在这种情况下，资源是通过网络由供方传输到需要来实现资源分配的。

           - 不从中心点开始分配（需求到供给）的例子：

             学校与学生的关系也构成一种在网络中供需分配关系。学校是资源提供方，它负责提供名额供适龄儿童入学。适龄儿童是资源的需求方，
             他们要求入学。作为需求方的适龄儿童沿街道网络分布，他们产生了对作为供给方的学校的资源--学生名额的需求。

        - 应用实例

          某个区域目前有 3 所小学，根据需求，拟在该区域内再建立 3 所小学。选择了 9 个地点作为待选地点，将在这些待选点中选择 3 个最
          佳地点建立新的小学。如图 1 所示，已有的 3 所小学为固定中心点，7 个候选位置为可选中心点。新建小学要满足的条件为：居民点中
          的居民步行去学校的时间要在 30 分钟以内。选址分区分析会根据这一条件给出最佳的选址位置，并且圈出每个学校，包括已有的 3 所
          学校的服务区域。如图 2 所示，最终序号为 5、6、8 的可选中心点被选为建立新学校的最佳地点。

          注：下面两幅中的网络数据集的所有网络结点被看做是该区域的居民点全部参与选址分区分析，居民点中的居民数目即为该居民点所需服务
          的数量。

          .. image:: ../image/FindLocation_1.png

          .. image:: ../image/FindLocation_2.png

        :param supply_centers: 资源供给中心集合
        :type supply_centers: list[SupplyCenter] or tuple[SupplyCenter]
        :param int expected_supply_center_number: 期望用于最终设施选址的资源供给中心数量。当输入值为0时，最终设施选址的资源供给中
                                                  心数量默认为覆盖分析区域内的所需最少的供给中心数
        :param bool is_from_center: 是否从资源供给中心开始分配资源。由于网络数据中的弧段具有正反阻力，即弧段的正向阻力值与其反向阻
                                    力值可能不同，因此，在进行分析时，从资源供给中心开始分配资源到需求点与从需求点向资源供给中心分
                                    配这两种分配形式下，所得的分析结果会不同。
                                    下面例举两个实际的应用场景，帮助进一步理解两种形式的差异，假设网络数据集中弧段的正反阻力值不同。

                                    - 从资源供给中心开始分配资源到需求点：

                                      如果你选址的对象是一些仓储中心，而需求点是各大超市，在实际的资源分配中，是将仓储中心的货物
                                      运输到其服务的超市，这种形式就是由资源供给中心向需求点分配，即分析时要将 is_from_center 设置为 True，
                                      即从资源供给中心开始分配。

                                    - 不从资源供给中心开始分配资源：

                                      如果你选址的对象是像邮局或者银行或者学校一类的服务机构，而需求点是居民点，在实际的资源分配
                                      中，是居民点中的居民会主动去其服务机构办理业务，这种形式就不是从资源供给中心向外分配资源了，
                                      即分析时要将 is_from_center 设置为 False，即不从资源供给中心开始分配。
        :param str weight_name: 权值字段信息的名称
        :return: 选址分析结果对象
        :rtype: LocationAnalystResult
        """
        if supply_centers is None:
            raise ValueError("supply_centers is None")
        elif not isinstance(supply_centers, (list, tuple)):
            supply_centers = [
             supply_centers]
        self._load_internal()
        java_supply_centers = self._jvm.com.supermap.analyst.networkanalyst.SupplyCenters()
        for item in supply_centers:
            java_supply_centers.add(oj(item))

        java_parameter = self._jvm.com.supermap.analyst.networkanalyst.LocationAnalystParameter()
        java_parameter.setExpectedSupplyCenterCount(int(expected_supply_center_number))
        java_parameter.setSupplyCenters(java_supply_centers)
        java_parameter.setFromCenter(parse_bool(is_from_center))
        weight_name = weight_name or self.analyst_setting.weight_fields[0].weight_name
        java_parameter.setWeightName(str(weight_name))
        java_result = self._jobject.findLocation(java_parameter)
        if java_result is not None:
            return LocationAnalystResult(java_result)

    def find_vrp(self, parameter, vehicles, center_nodes_or_points, demand_points):
        """
        物流配送分析。
        该接口和之前的物流配送接口 :py:meth:`find_mtsp_path` 相比，多出了车辆信息、需求量等的设置，可以更充分的满足不同情况下的需求。

        物流配送分析参数对象 :py:class:`VRPAnalystParameter` 可以设置障碍边、障碍点、权值字段信息的名字标识、转向权值字段，还可以对分析结果进行
        一些设置，即在分析结果中是否包含分析途经的以下内容：结点集合，弧段集合，路由对象集合以及站点集合。

        车辆信息 :py:class:`VehicleInfo` 中可以设置每辆车各自的负载量、最大耗费等条件。

        中心点信息 center_nodes_or_points 中可以设置包括中心的坐标或者结点ID；需求点信息 demand_points 中可以设置每个需求点的坐标或者结点ID，以及各自的需求量。

        通过对车辆、需求点和中心点相关信息的设置，该接口可以根据这些条件来合理划分路线，完成相应的分配任务。

        :param VRPAnalystParameter parameter: 物流配送分析参数对象。
        :param vehicles: 车辆信息数组
        :type vehicles: list[VehicleInfo] or tuple[VehicleInfo]
        :param center_nodes_or_points: 中心点信息数组
        :type center_nodes_or_points: list[int] or list[Point2D] or tuple[int] or tuple[Point2D]
        :param demand_points: 需求点信息数组
        :type demand_points: list[DemandPointInfo] or tuple[DemandPointInfo]
        :return: 物流配送结果
        :rtype: list[VRPAnalystResult]
        """
        if not isinstance(parameter, VRPAnalystParameter):
            raise ValueError("parameter required VRPAnalystParameter, but " + str(type(parameter)))
        elif not isinstance(vehicles, (list, tuple)):
            vehicles = [
             vehicles]
        vehicles = list(filter((lambda item: isinstance(item, VehicleInfo)), vehicles))
        java_vehicles = get_gateway().new_array(get_jvm().com.supermap.analyst.networkanalyst.VehicleInfo, len(vehicles))
        for index, value in enumerate(vehicles):
            java_vehicles[index] = oj(value)

        if isinstance(center_nodes_or_points, (list, tuple)):
            if center_nodes_or_points:
                if isinstance(center_nodes_or_points[0], int):
                    java_centers = get_gateway().new_array(get_jvm().com.supermap.analyst.networkanalyst.CenterPointInfo, len(center_nodes_or_points))
                    for index, value in enumerate(center_nodes_or_points):
                        java_center_info = get_jvm().com.supermap.analyst.networkanalyst.CenterPointInfo()
                        java_center_info.setCenterID(int(value))
                        java_centers[index] = java_center_info

            else:
                java_centers = get_gateway().new_array(get_jvm().com.supermap.analyst.networkanalyst.CenterPointInfo, len(center_nodes_or_points))
                for index, value in enumerate(center_nodes_or_points):
                    java_center_info = get_jvm().com.supermap.analyst.networkanalyst.CenterPointInfo()
                    java_center_info.setCenterPoint(oj(Point2D.make(value)))
                    java_centers[index] = java_center_info

        else:
            raise ValueError("center_nodes_or_points required list[int] or list[Point2D]")
        java_demands = get_gateway().new_array(get_jvm().com.supermap.analyst.networkanalyst.DemandPointInfo, len(demand_points))
        for index, value in enumerate(demand_points):
            java_demands[index] = oj(value)

        self._load_internal()
        java_result = self._jobject.findVRPPath(oj(parameter), java_vehicles, java_centers, java_demands)
        if java_result is not None:
            count = len(java_result.getWeights())
            return list((VRPAnalystResult(java_result, i) for i in range(count)))

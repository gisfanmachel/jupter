# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/_jsuperpy\analyst\na3d.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 91371 bytes
"""
三维网络分析模块
"""
from enum import unique
from iobjectspy._jsuperpy._gateway import get_jvm, safe_start_callback_server, close_callback_server
from iobjectspy._jsuperpy.data import DatasetVector, Point3D, Geometry
from iobjectspy._jsuperpy.data._listener import ProgressListener
from iobjectspy._jsuperpy.data._util import get_input_dataset, get_output_datasource, check_output_datasource, try_close_output_datasource, to_java_point3ds
from iobjectspy._jsuperpy.enums import JEnum, DatasetType
from iobjectspy._jsuperpy._utils import to_java_int_array, to_java_string_array, split_input_int_list_from_str, split_input_list_from_str, oj, parse_bool, java_array_to_list
from iobjectspy._jsuperpy._logger import log_error
from iobjectspy._jsuperpy.data._jvm import JVMBase
from .na import WeightFieldInfo
__all__ = [
 'NetworkSplitMode3D', 'build_network_dataset_known_relation_3d', 'build_facility_network_directions_3d', 
 'build_network_dataset_3d', 
 'FacilityAnalystResult3D', 'FacilityAnalystSetting3D', 
 'FacilityAnalyst3D', 
 'BurstAnalystResult3D', 'TransportationAnalyst3D', 'TransportationAnalystResult3D', 
 'TransportationAnalystParameter3D', 
 'TransportationAnalystSetting3D']

@unique
class NetworkSplitMode3D(JEnum):
    __doc__ = "\n    构建三维网络数据集打断模式。用来控制建立网络数据集时，处理线线打断或点线打断的模式\n\n    :var NetworkSplitMode.NO_SPLIT: 不打断\n    :var NetworkSplitMode.LINE_SPLIT_BY_POINT: 点打断线\n    :var NetworkSplitMode.LINE_SPLIT_BY_POINT_AND_LINE: 线与线打断，同时点打断线\n    "
    NO_SPLIT = 0
    LINE_SPLIT_BY_POINT = 1
    LINE_SPLIT_BY_POINT_AND_LINE = 2

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.realspace.networkanalyst.NetworkSplitMode3D"

    @classmethod
    def _externals(cls):
        return {"None": (cls.NO_SPLIT)}


def build_network_dataset_3d(line, point=None, split_mode='NO_SPLIT', tolerance=0.0, line_saved_fields=None, point_saved_fields=None, out_data=None, out_dataset_name=None, progress=None):
    """
    网络数据集是进行网络分析的数据基础。三维网络数据集由两个子数据集（一个三维线数据集和一个三维点数据集）构成，分别存储了网络模型的弧段和结点，
    并且描述了弧段与弧段、弧段与结点、结点与结点间的空间拓扑关系。

    此方法提供根据单个线数据集或单个线和单个点构建网络数据集。如果用户的数据集已经有正确的网络关系，可以直接通
    过 :py:meth:`build_network_dataset_known_relation_3d` 快速的构建一个网络数据集。

    构建的网络数据集，可以通过 :py:meth:`validate_network_dataset_3d` 检查网络拓扑关系是否正确。

    :param line: 用于构建网络数据集的线数据集
    :type line: DatasetVector
    :param point: 用于构建网络数据集的点数据集。
    :type point: DatasetVector
    :param split_mode: 打断模式，默认为不打断
    :type split_mode: NetworkSplitMode3D
    :param float tolerance: 节点容限
    :param line_saved_fields: 线数据集中需要保留的字段
    :type line_saved_fields: str or list[str]
    :param point_saved_fields: 点数据集中需要保留的字段。
    :type point_saved_fields: str or list[str]
    :param out_data: 保留结果网络数据集的数据源对象
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果三维网络数据集
    :rtype: DatasetVector
    """
    line = get_input_dataset(line)
    if line is None:
        raise ValueError("have no valid line dataset")
    if line.type is not DatasetType.LINE3D:
        raise ValueError("required Line3D dataset, but is " + str(line.type))
    else:
        point = get_input_dataset(point)
        if point is not None:
            if point.type is not DatasetType.POINT3D:
                raise ValueError("required Point3D dataset, but is " + str(point.type))
            else:
                if out_data is not None:
                    out_datasource = get_output_datasource(out_data)
                else:
                    out_datasource = line.datasource
                check_output_datasource(out_datasource)
                if out_dataset_name is None:
                    dest_name = line.name + "_Network3D"
                else:
                    dest_name = out_dataset_name
            dest_name = out_datasource.get_available_dataset_name(dest_name)
            listener = None
            try:
                try:
                    if progress is not None and safe_start_callback_server():
                        try:
                            listener = ProgressListener(progress, "build_network_dataset3d")
                            get_jvm().com.supermap.realspace.networkanalyst.NetworkBuilder3D.addSteppedListener(listener)
                        except Exception as e:
                            try:
                                close_callback_server()
                                log_error(e)
                                listener = None
                            finally:
                                e = None
                                del e

                    else:
                        network_builder_func = get_jvm().com.supermap.realspace.networkanalyst.NetworkBuilder3D.buildNetwork
                        if point is not None:
                            java_result = network_builder_func(oj(line), oj(point), to_java_string_array(split_input_list_from_str(line_saved_fields)), to_java_string_array(split_input_list_from_str(point_saved_fields)), oj(out_datasource), str(dest_name), oj(NetworkSplitMode3D._make(split_mode, "NO_SPLIT")), float(tolerance))
                        else:
                            java_result = network_builder_func(oj(line), to_java_string_array(split_input_list_from_str(line_saved_fields)), oj(out_datasource), str(dest_name), oj(NetworkSplitMode3D._make(split_mode, "NO_SPLIT")), float(tolerance))
                except:
                    import traceback
                    log_error(traceback.format_exc())
                    java_result = None

            finally:
                return

            if listener is not None:
                try:
                    get_jvm().com.supermap.realspace.networkanalyst.NetworkBuilder3D.removeSteppedListener(listener)
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


def build_network_dataset_known_relation_3d(line, point, edge_id_field, from_node_id_field, to_node_id_field, node_id_field, out_data=None, out_dataset_name=None, progress=None):
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

    :param line: 用于构建网络数据集的三维线数据集
    :type line: str or DatasetVector
    :param point: 用于构建网络数据集的三维点数据集
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
    if not isinstance(source_line_dt, DatasetVector) or source_line_dt.type is not DatasetType.LINE3D:
        raise ValueError("line required DatasetVector, but is " + str(type(source_line_dt)))
    source_point_dt = get_input_dataset(point)
    if not isinstance(source_point_dt, DatasetVector) or source_point_dt.type is not DatasetType.POINT3D:
        raise ValueError("point required DatasetVector, but is " + str(type(source_point_dt)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_line_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            dest_name = source_line_dt.name + "_Network3D"
        else:
            dest_name = out_dataset_name
    dest_name = out_datasource.get_available_dataset_name(dest_name)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "build_network_dataset_known_relation_3d")
                        get_jvm().com.supermap.realspace.networkanalyst.NetworkBuilder3D.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            network_builder_func = get_jvm().com.supermap.realspace.networkanalyst.NetworkBuilder3D.buildNetwork
            java_result = network_builder_func(oj(source_line_dt), oj(source_point_dt), str(edge_id_field), str(from_node_id_field), str(to_node_id_field), str(node_id_field), oj(out_datasource), str(dest_name))
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        return

    if listener is not None:
        try:
            get_jvm().com.supermap.realspace.networkanalyst.NetworkBuilder3D.removeSteppedListener(listener)
        except Exception as e1:
            try:
                log_error(e1)
            finally:
                e1 = None
                del e1

        close_callback_server()
    elif java_result is not None:
        result_dt = out_datasource[dest_name]
    else:
        result_dt = None
    if out_data is not None:
        return try_close_output_datasource(result_dt, out_datasource)
    return result_dt


def build_facility_network_directions_3d(network_dataset, source_ids, sink_ids, direction_field='Direction', node_type_field='NodeType', progress=None):
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

    :param network_dataset: 待创建流向的三维网络数据集，三维网络数据集必须可修改。
    :type network_dataset: DatasetVector or str
    :param source_ids: 源对应的网络结点 ID 数组。源与汇都是用来建立网络数据集的流向的。网络数据集的流向与源和汇的位置决定。
    :type source_ids: list[int] or tuple[int]
    :param sink_ids: 汇 ID 数组。汇对应的网络结点 ID 数组。源与汇都是用来建立网络数据集的流向的。网络数据集的流向与源和汇的位置决定。
    :type sink_ids: list[int] or tuple[int]
    :param str direction_field: 流向字段，用于保存网络数据集的流向信息
    :param str node_type_field: 结点类型字段名称，结点类型分为源结点、交汇结点、普通结点。该字段是网络结点数据集中的字段，如果不存在则创建该字段。
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 创建成功返回 true，否则 false
    :rtype: bool
    """
    network_dataset = get_input_dataset(network_dataset)
    if not isinstance(network_dataset, DatasetVector) or network_dataset.type is not DatasetType.NETWORK3D:
        raise ValueError("network_dataset required DatasetVector, but " + str(type(network_dataset)))
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "build_facility_network_directions_3d")
                        get_jvm().com.supermap.realspace.networkanalyst.NetworkBuilder3D.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            java_function = get_jvm().com.supermap.realspace.networkanalyst.NetworkBuilder3D.buildFacilityNetworkDirections
            facility_analyst_setting = FacilityAnalystSetting3D()
            facility_analyst_setting.set_network_dataset(network_dataset)
            facility_analyst_setting.set_direction_field(direction_field)
            java_result = java_function(oj(facility_analyst_setting), to_java_int_array(split_input_int_list_from_str(source_ids)), to_java_int_array(split_input_int_list_from_str(sink_ids)), str(node_type_field))
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = False

    finally:
        return

    if listener is not None:
        try:
            get_jvm().com.supermap.realspace.networkanalyst.NetworkBuilder3D.removeSteppedListener(listener)
        except Exception as e1:
            try:
                log_error(e1)
            finally:
                e1 = None
                del e1

        close_callback_server()
    return java_result


class FacilityAnalystSetting3D:
    __doc__ = "\n    设施网络分析环境设置类。 设施网络分析环境设置类。该类用于提供设施网络分析时所需要的所有参数信息。\n    设施网络分析环境设置类的各个参数的设置直接影响分析的结果。\n    "

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
        :rtype: FacilityAnalystSetting3D
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
        :rtype: FacilityAnalystSetting3D
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
        :rtype: FacilityAnalystSetting3D
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
        :rtype: FacilityAnalystSetting3D
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
        :rtype: FacilityAnalystSetting3D
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
        :rtype: FacilityAnalystSetting3D
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
        :rtype: FacilityAnalystSetting3D
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
        :rtype: FacilityAnalystSetting3D
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
        :rtype: FacilityAnalystSetting3D
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
        :rtype: FacilityAnalystSetting3D
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
        java_object = get_jvm().com.supermap.realspace.networkanalyst.FacilityAnalystSetting3D()
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
            java_weight_fields = get_jvm().com.supermap.realspace.networkanalyst.WeightFieldInfos3D()
            for weight in self.weight_fields:
                java_weight_info = get_jvm().com.supermap.realspace.networkanalyst.WeightFieldInfo3D()
                java_weight_info.setName(weight.weight_name)
                java_weight_info.setFTWeightField(weight.ft_weight_field)
                java_weight_info.setTFWeightField(weight.tf_weight_field)
                java_weight_fields.add(java_weight_info)

            java_object.setWeightFieldInfos(java_weight_fields)
        if self.barrier_node_ids is not None:
            java_object.setBarrierNodes(to_java_int_array(split_input_int_list_from_str(self.barrier_node_ids)))
        if self.barrier_edge_ids is not None:
            java_object.setBarrierEdges(to_java_int_array(split_input_int_list_from_str(self.barrier_edge_ids)))
        if self.direction_field is not None:
            java_object.setDirectionField(str(self.direction_field))
        return java_object


class FacilityAnalystResult3D:
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
        """
        return self._cost


class BurstAnalystResult3D:
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


class FacilityAnalyst3D(JVMBase):
    __doc__ = "设施网络分析类。\n\n       设施网络分析类。它是网络分析功能类之一，主要用于进行各类连通性分析和追踪分析。\n\n       设施网络是具有方向的网络。即介质（水流、电流等）会根据网络本身的规则在网络中流动。\n\n       设施网络分析的前提是已经建立了用于设施网络分析的数据集，建立用于设施网络分析的数据集的基础是建立网络数据集，在此基础上利用\n       :py:meth:`build_facility_network_directions_3d` 方法赋予网络数据集特有的用于进行设施网络分析的数据信息，也就是为网络数据集\n       建立流向，使原有的网络数据集具有了能够进行设施网络分析的最基本的条件 ，此时，就可以进行各种设施网络分析了。\n    "

    def __init__(self, analyst_setting):
        """

        :param analyst_setting: 设置网络分析的环境。
        :type analyst_setting: FacilityAnalystSetting3D
        """
        JVMBase.__init__(self)
        self._analyst_setting = None
        self._is_load = False
        self.set_analyst_setting(analyst_setting)

    def _make_java_object(self):
        self._java_object = self._jvm.com.supermap.realspace.networkanalyst.FacilityAnalyst3D()
        return self._java_object

    def set_analyst_setting(self, value):
        """
        设置设施网络分析的环境。

        设施网络分析环境参数的设置，直接影响到设施网络分析的结果。设施网络分析所需要的参数包括：用于进行设施网络分析的数据集（ 即
        建立了流向的网络数据集或者同时建立了流向和等级的网络数据集，也就是说该方法对应的 :py:class:`FacilityAnalystSetting3D` 所指
        定的网络数据集必须有流向或者流向和等级信息）、结点 ID 字段、弧段 ID 字段、弧段起始结点 ID 字段、弧段终止结点 ID 字段、权
        值信息、点到弧段的距离容限、障碍结点、障碍弧段、流向等。

        :param value: 设施网络分析环境参数
        :type value: FacilityAnalystSetting3D
        :return: self
        :rtype: FacilityAnalyst3D
        """
        if isinstance(value, FacilityAnalystSetting3D):
            self._analyst_setting = value
            self._jobject.setAnalystSetting(oj(value))
            return self
        raise ValueError("required FacilityAnalystSetting3D, but " + str(type(value)))

    @property
    def analyst_setting(self):
        """FacilityAnalystSetting3D: 设施网络分析的环境"""
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
        :rtype: BurstAnalystResult3D
        """
        self._load_internal()
        if is_edge_id:
            func = self._jobject.burstAnalyseFromEdge
        else:
            func = self._jobject.burstAnalyseFromNode
        java_result = func(to_java_int_array(source_nodes), int(edge_or_node_id), parse_bool(is_uncertain_direction_valid))
        if java_result is not None:
            return BurstAnalystResult3D(java_result)

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
        :rtype: FacilityAnalystResult3D
        """
        self._load_internal()
        if is_edge_id:
            func = self._jobject.findCriticalFacilitiesDownFromEdge
        else:
            func = self._jobject.findCriticalFacilitiesDownFromNode
        java_result = func(to_java_int_array(source_node_ids), int(edge_or_node_id), parse_bool(is_uncertain_direction_valid))
        if java_result is not None:
            return FacilityAnalystResult3D(java_result)

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
        :rtype: FacilityAnalystResult3D
        """
        self._load_internal()
        if is_edge_id:
            func = self._jobject.findCriticalFacilitiesUpFromEdge
        else:
            func = self._jobject.findCriticalFacilitiesUpFromNode
        java_result = func(to_java_int_array(split_input_int_list_from_str(source_node_ids)), int(edge_or_node_id), parse_bool(is_uncertain_direction_valid))
        if java_result is not None:
            return FacilityAnalystResult3D(java_result)

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
        :rtype: FacilityAnalystResult3D
        """
        self._load_internal()
        if is_edge_id:
            func = self._jobject.findSinkFromEdge
        else:
            func = self._jobject.findSinkFromNode
        java_result = func(int(edge_or_node_id), str(weight_name) if weight_name is not None else None, parse_bool(is_uncertain_direction_valid))
        if java_result is not None:
            return FacilityAnalystResult3D(java_result)

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
        :rtype: FacilityAnalystResult3D
        """
        self._load_internal()
        if is_edge_id:
            func = self._jobject.findSourceFromEdge
        else:
            func = self._jobject.findSourceFromNode
        java_result = func(int(edge_or_node_id), str(weight_name) if weight_name is not None else None, parse_bool(is_uncertain_direction_valid))
        if java_result is not None:
            return FacilityAnalystResult3D(java_result)

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
        :rtype: FacilityAnalystResult3D
        """
        self._load_internal()
        if is_edge_id:
            func = self._jobject.traceDownFromEdge
        else:
            func = self._jobject.traceDownFromNode
        java_result = func(int(edge_or_node_id), str(weight_name) if weight_name is not None else None, parse_bool(is_uncertain_direction_valid))
        if java_result is not None:
            return FacilityAnalystResult3D(java_result)

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
        :rtype: FacilityAnalystResult3D
        """
        self._load_internal()
        if is_edge_id:
            func = self._jobject.traceUpFromEdge
        else:
            func = self._jobject.traceUpFromNode
        java_result = func(int(edge_or_node_id), str(weight_name) if weight_name is not None else None, parse_bool(is_uncertain_direction_valid))
        if java_result is not None:
            return FacilityAnalystResult3D(java_result)


class TransportationAnalystSetting3D:
    __doc__ = "\n    交通网络分析分析环境。\n    "

    def __init__(self, network_dataset=None):
        """
        初始化对象

        :param network_dataset: 网络数据集
        :type network_dataset: DatasetVector or str
        """
        self._network_dt = None
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
        :rtype: TransportationAnalystSetting3D
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
        :rtype: TransportationAnalystSetting3D
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
        :rtype: TransportationAnalystSetting3D
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
        :rtype: TransportationAnalystSetting3D
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
        :rtype: TransportationAnalystSetting3D
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
        :rtype: TransportationAnalystSetting3D
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
        :rtype: TransportationAnalystSetting3D
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
        :rtype: TransportationAnalystSetting3D
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
        :rtype: TransportationAnalystSetting3D
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
        :rtype: TransportationAnalystSetting3D
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
        :rtype: TransportationAnalystSetting3D
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
        :rtype: TransportationAnalystSetting3D
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
        :rtype: TransportationAnalystSetting3D
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
        :rtype: TransportationAnalystSetting3D
        """
        self._edge_filter = value
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
        :rtype: TransportationAnalystSetting3D
        """
        if value is not None:
            self._edge_name_field = str(value)
        return self

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
        :rtype: TransportationAnalystSetting3D
        """
        if dataset is not None:
            dataset = get_input_dataset(dataset)
            if isinstance(dataset, DatasetVector):
                if dataset.type is DatasetType.NETWORK3D:
                    self._network_dt = dataset
                    return self
            raise ValueError("required DatasetVector, but is " + str(type(dataset)))
        else:
            return self

    def _java_transportation_analyst_setting_3d(self):
        java_object = get_jvm().com.supermap.realspace.networkanalyst.TransportationAnalystSetting3D()
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
            java_weight_fields = get_jvm().com.supermap.realspace.networkanalyst.WeightFieldInfos3D()
            for weight in self.weight_fields:
                java_weight_info = get_jvm().com.supermap.realspace.networkanalyst.WeightFieldInfo3D()
                java_weight_info.setName(weight.weight_name)
                java_weight_info.setFTWeightField(weight.ft_weight_field)
                java_weight_info.setTFWeightField(weight.tf_weight_field)
                java_weight_fields.add(java_weight_info)

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
        if self.edge_name_field is not None:
            java_object.setEdgeNameField(str(self.edge_name_field))
        return java_object

    @property
    def _jobject(self):
        """Py4J 映射的 Java 对象"""
        return self._java_transportation_analyst_setting_3d()


class TransportationAnalystResult3D:
    __doc__ = "\n    三维交通网络分析结果类。该类用于返回各种三维交通网络分析的结果，包括路由集合、分析途经的结点集合以及弧段集合、站点集合和权值集合\n    以及各站点的花费等。\n    "

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
        """list[int]: 返回分析结果的途经弧段集合。注意，必须将 TransportationAnalystParameter3D 对象的 :py:meth:`TransportationAnalystParameter3D.set_edges_return`
                      方法设置为 True，分析结果中才会包含途经弧段集合，否则返回 None
        """
        return self._edges

    @property
    def nodes(self):
        """list[int]: 返回分析结果的途经结点集合。注意，必须将 TransportationAnalystParameter3D 对象的 :py:meth:`TransportationAnalystParameter3D.set_nodes_return` 方
                      法设置为 True，分析结果中才会包含途经结点集合，否则为一个空的数组。"""
        return self._nodes

    @property
    def route(self):
        """GeoLineM: 返回分析结果的路由对象。注意，必须将 TransportationAnalystParameter3D 对象的 :py:meth:`TransportationAnalystParameter3D.set_routes_return` 方
                     法设置为 true，分析结果中才会包含路由对象，否则返回 None"""
        return self._route

    @property
    def stop_indexes(self):
        """list[int]: 返回站点索引，该数组反映了站点在分析后的排列顺序。注意，必须将 TransportationAnalystParameter3D 对象
                      的 :py:meth:`TransportationAnalystParameter3D.set_stop_indexes_return` 方法设置为 True，分析结果中才会
                      包含站点索引，否则为一个空的数组。

                      - 最佳路径分析（ :py:meth:`TransportationAnalyst3D.find_path` 方法）:

                          - 结点模式：如设置的分析结点 ID 为 1，3，5 的三个结点，因为结果途经顺序必须为 1，3，5，所以元素值依
                            次为 0，1，2，即结果途经顺序在初始设置结点串中的索引。

                          - 坐标点模式：如设置的分析坐标点为 Pnt1，Pnt2，Pnt3，因为结果途经顺序必须为 Pnt1，Pnt2，Pnt3，所以元
                            素值依次为 0，1，2，即结果途经坐标点顺序在初始设置坐标点串中的索引。
        """
        return self._stop_indexes

    @property
    def stop_weights(self):
        """list[float]: 返回根据站点索引对站点排序后，站点间的花费（权值）。
                        该方法返回的是站点与站点间的耗费，这里的站点指的是用于分析结点或坐标点，而不是路径经过的所有结点或坐标点。
                        该方法返回的权值所关联的站点顺序与 :py:attr:`stop_indexes` 方法中返回的站点索引值的顺序一致。

                        - 最佳路径分析（ :py:meth:`TransportationAnalyst3D.find_path` 方法）: 假设指定经过点 1、2、3，则二维元素依次
                          为：1 到 2 的耗费、2 到 3 的耗费；
        """
        return self._stop_weights

    @property
    def weight(self):
        """float: 花费的权值。"""
        return self._weight


class TransportationAnalystParameter3D:
    __doc__ = "\n    三维交通网络分析参数类。\n\n    该类用于设置三维交通网络分析所需的各种参数，如分析时途经的结点（或任意点）的集合、权值信息、障碍点和障碍弧段，以及分析结果中是\n    否包含途经结点集合、经过弧段集合、路由对象等。\n    "

    def __init__(self):
        self._is_routes_return = False
        self._is_nodes_return = True
        self._is_edges_return = True
        self._is_stop_indexes_return = False
        self._nodes = None
        self._points = None
        self._weight_name = None
        self._barrier_nodes = None
        self._barrier_edges = None
        self._barrier_points = None

    @property
    def is_routes_return(self):
        """bool: 返回分析结果中是否包含三维线（ :py:class:`GeoLine3D` ）对象"""
        return self._is_routes_return

    def set_routes_return(self, value=True):
        """
       分析结果中是否包含三维线（ :py:class:`GeoLine3D` ）对象

        :param bool value: 指定是否包含路由对象。设置为 True，在分析成功后，可以从 TransportationAnalystResult3D 对象
                           的 :py:attr:`TransportationAnalystResult3D.route` 返回路由对象；为 False 则返回 None
        :return: self
        :rtype: TransportationAnalystParameter3D
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

        :param bool value: 指定分析结果中是否包含途经结点。设置为 True，在分析成功后，可以从 TransportationAnalystResult3D 对象
                            :py:attr:`TransportationAnalystResult3D.nodes` 方法返回途经结点；为 False 则返回 None
        :return: self
        :rtype: TransportationAnalystParameter3D
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

        :param bool value: 指定分析结果中是否包含途经弧段。设置为 True，在分析成功后，可以从 TransportationAnalystResult3D 对象
                            :py:attr:`TransportationAnalystResult3D.edges` 方法返回途经弧段；为 False 则返回 None
        :return: self
        :rtype: TransportationAnalystParameter3D
        """
        self._is_edges_return = parse_bool(value)
        return self

    @property
    def is_stop_indexes_return(self):
        """bool: 分析结果中是否要包含站点索引"""
        return self._is_stop_indexes_return

    def set_stop_indexes_return(self, value=True):
        """
        设置分析结果中是否要包含站点索引的

        :param bool value: 指定分析结果中是否要包含站点索引。设置为 True，在分析成功后，可以从 TransportationAnalystResult3D 对象
                            :py:attr:`TransportationAnalystResult3D.stop_indexes` 方法返回站点索引；为 False 则返回 None
        :return: self
        :rtype: TransportationAnalystParameter3D
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
        :rtype: TransportationAnalystParameter3D
        """
        self._nodes = split_input_int_list_from_str(nodes)
        return self

    @property
    def points(self):
        """list[Point3D]: 分析时途经点"""
        return self._points

    def set_points(self, points):
        """
        设置分析时途经点的集合。必设，但与 :py:meth:`set_nodes` 方法互斥，如果同时设置，则只有分析前最后的设置有效。例如，先指定了结点集合，又
        指定了坐标点集合，然后分析，此时只对坐标点进行分析。

        如果设置的途经点集合中的点不在网络数据集的范围内，则该点不会参与分析

        :param points: 途经点
        :type points: list[Point3D] or tuple[Point3D]
        :return: self
        :rtype: TransportationAnalystParameter3D
        """
        if isinstance(points, (list, tuple)):
            self._points = list(filter((lambda p: p is not None), list((Point3D.make(p) for p in points))))
        else:
            if isinstance(points, None):
                self._points = None
            else:
                raise ValueError("points required list[Point3D] or tuple[Point3D]")
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
        :rtype: TransportationAnalystParameter3D
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
        :rtype: TransportationAnalystParameter3D
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
        :rtype: TransportationAnalystParameter3D
        """
        self._barrier_edges = split_input_int_list_from_str(edges)
        return self

    @property
    def barrier_points(self):
        """list[Point3D]: 障碍点列表"""
        return self._barrier_points

    def set_barrier_points(self, points):
        """
        设置障碍结点的坐标列表。可选。指定的障碍点可以不在网络上（既不在弧段上也不在结点上），分析时将根据距离容限（ :py:attr:`.TransportationPathAnalystSetting.tolerance` ）把
        障碍点归结到最近的网络上。目前支持最佳路径分析、最近设施查找、旅行商分析和物流配送分析。

        :param points: 障碍结点的坐标列表
        :type points: list[Point2D] or tuple[Point2D]
        :return: self
        :rtype: TransportationAnalystParameter3D
        """
        if isinstance(points, (list, tuple)):
            self._barrier_points = list(filter((lambda p: p is not None), list((Point3D.make(p) for p in points))))
        else:
            if points is None:
                self._barrier_points = None
            else:
                raise ValueError("points required list[Point3D] or tuple[Point3D]")
        return self

    @property
    def _jobject(self):
        java_object = get_jvm().com.supermap.realspace.networkanalyst.TransportationAnalystParameter3D()
        if self.is_nodes_return is not None:
            java_object.setNodesReturn(bool(self.is_nodes_return))
        if self.is_edges_return is not None:
            java_object.setEdgesReturn(bool(self.is_edges_return))
        if self.is_routes_return is not None:
            java_object.setRoutesReturn(bool(self.is_routes_return))
        if self.is_stop_indexes_return is not None:
            java_object.setStopIndexesReturn(bool(self.is_stop_indexes_return))
        if self.nodes is not None:
            java_object.setNodes(to_java_int_array(self.nodes))
        if self.points is not None:
            java_object.setPoints(to_java_point3ds(self.points))
        if self.weight_name is not None:
            java_object.setWeightName(self.weight_name)
        if self.barrier_nodes is not None:
            java_object.setBarrierNodes(to_java_int_array(self.barrier_nodes))
        if self.barrier_edges is not None:
            java_object.setBarrierEdges(to_java_int_array(self.barrier_edges))
        if self.barrier_points is not None:
            java_object.setBarrierPoints(to_java_point3ds(self.barrier_points))
        return java_object


class TransportationAnalyst3D(JVMBase):
    __doc__ = "\n    三维交通网络分析类。该类用于提供基于三维网络数据集的交通网络分析功能。目前只提供最佳路径分析。\n\n    道路、铁路、建筑物内通道、矿井巷道等可以使用交通网络进行模拟，与设施网络不同，交通网络是没有方向，即流通介质（行人或传输的资源）\n    可以自行决定方向、速度和目的地。当然，也可以进行一定的限制，例如设置交通规则，如单行线、禁行线等。\n\n    三维交通网络分析是基于三维网络数据集的分析，是三维网络分析的重要内容，目前提供了最佳路径分析。对于交通网络，尤其是对建筑物的内部\n    通道、矿井巷道这类在二维平面无法清晰展现的交通网络，三维网络能够更加真实的体现网络的空间拓扑结构和分析结果。\n\n    三维交通网络分析的一般步骤：\n\n    1. 构建三维网络数据集。根据研究需求和已有数据选择合适的网络模型构建方法。SuperMap 提供了两种三维网络数据集的构建方法，具体介绍请\n       参阅 :py:meth:`build_network_dataset_3d` 或 :py:meth:`build_network_dataset_know_relation_3d` .\n\n    2. （可选）建议对用于分析的网络数据集进行数据检查( :py:meth:`validate_network_dataset_3d` ).\n\n    3. 设置三维交通网络分析环境（set_analyst_setting 方法）；\n\n    4. 加载网络模型（load 方法）；\n\n    5. 使用 TransportationAnalyst3D 类提供的各种交通网络分析方法进行相应的分析。\n\n    "

    def __init__(self, analyst_setting):
        """
        初始化对象

        :param TransportationAnalystSetting3D analyst_setting: 交通网络分析环境设置对象
        """
        JVMBase.__init__(self)
        self._analyst_setting = None
        self.set_analyst_setting(analyst_setting)
        self._is_load = False

    def _make_java_object(self):
        return self._jvm.com.supermap.realspace.networkanalyst.TransportationAnalyst3D()

    def set_analyst_setting(self, analyst_setting):
        """
        设置交通网络分析环境设置对象
        在利用交通网络分析类进行各种交通网络分析时，都要首先设置交通网络分析的环境，都要首先设置交通网络分析的环境

        :param TransportationAnalystSetting3D analyst_setting: 交通网络分析环境设置对象
        :return: self
        :rtype: TransportationAnalyst3D
        """
        if isinstance(analyst_setting, TransportationAnalystSetting3D):
            self._jobject.setAnalystSetting(oj(analyst_setting))
            self._analyst_setting = analyst_setting
            return self
        raise ValueError("required TransportationAnalystSetting3D, but " + str(type(analyst_setting)))

    @property
    def analyst_setting(self):
        """TransportationAnalystSetting3D: 交通网络分析环境设置对象"""
        return self._analyst_setting

    def load(self):
        """
        加载网络模型。
        该方法根据交通网络分析环境设置（ :py:class:`TransportationAnalystSetting3D` ）对象中的环境参数，加载网络模型。在设置好交通网络分析环境的
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

    def find_path(self, parameter):
        """
        最佳路径分析。
        最佳路径分析，用于在网络数据集中，找出经过给定的 N 个点（N 大于等于 2）的最佳路径，这条最佳路径具有以下两个特征：

        这条路径必须按照给定的 N 点的次序依次经过这 N 个点，也就是说，最佳路径分析中经过的点是有序的；
        这条路径的耗费最小。耗费根据交通网络分析参数所指定的权重来决定。权重可以是长度、时间、路况、费用等，因此最佳路径可以是距离最
        短的路径、花费时间最少的路径、路况最好的路径、费用最低的路径等等。

        有两种方式来指定待分析的经过点：

        - 结点方式：通过 :py:class:`TransportationAnalystParameter3D` 类的 :py:meth:`TransportationAnalystParameter3D.set_nodes` 方
          法指定最佳路径分析所经过的结点的 ID，此时，分析过程中经过的点就是相应的网络结点，而经过点的次序是网络结点在这个结点 ID 数组中的次序；

        - 任意坐标点方式：通过 :py:class:`TransportationAnalystParameter3D` 类的 :py:meth:`TransportationAnalystParameter3D.set_points` 方
          法指定最佳路径分析所经过的点的坐标，此时，分析过程中经过的点就是相应的坐标点集合，分析过程中经过点的次序是坐标点在点集合中的次序。

        注意：两种方式只能选择一种使用，不能同时使用。

        :param TransportationAnalystParameter3D parameter: 交通网络分析参数对象
        :return: 最佳路径分析结果
        :rtype: TransportationAnalystResult3D
        """
        if not isinstance(parameter, TransportationAnalystParameter3D):
            raise ValueError("parameter required TransportationAnalystParameter3D, but " + str(type(parameter)))
        self._load_internal()
        java_result = self._jobject.findPath(oj(parameter))
        if java_result is not None:
            result = TransportationAnalyst3D._make_transportation_analyst_results(java_result)
            if result:
                return result[0]

    @staticmethod
    def _make_transportation_analyst_results(java_result):
        if java_result is not None:
            count = len(java_result.getWeights())
            return list((TransportationAnalystResult3D(java_result, i) for i in range(count)))

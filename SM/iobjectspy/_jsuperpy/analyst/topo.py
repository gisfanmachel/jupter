# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/_jsuperpy\analyst\topo.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 51550 bytes
"""拓扑模块"""
from iobjectspy._jsuperpy._gateway import get_jvm, safe_start_callback_server, close_callback_server
from iobjectspy._jsuperpy.data import Datasource, DatasetVector, Recordset, GeoRegion
from iobjectspy._jsuperpy.data._listener import ProgressListener
from iobjectspy._jsuperpy.data._util import to_java_recordset_array, get_input_dataset, get_output_datasource, check_output_datasource, try_close_output_datasource
from iobjectspy._jsuperpy.enums import *
from iobjectspy._jsuperpy._utils import *
from iobjectspy._jsuperpy._logger import *
__all__ = [
 'ProcessingOptions', 'topology_processing', 'topology_build_regions', 'pickup_border', 
 'PreprocessOptions', 
 'preprocess', 'topology_validate', 'split_lines_by_regions']

class ProcessingOptions(object):
    __doc__ = "\n    拓扑处理参数类。该类提供了关于拓扑处理的设置信息。\n\n    如果未通过 set_vertex_tolerance,set_overshoots_tolerance 和 set_undershoots_tolerance 方法设置节点容限、短悬线容限和长悬线容限，\n    或设置为0，系统将使用数据集的容限中相应的容限值进行处理\n\n    "

    def __init__(self, pseudo_nodes_cleaned=False, overshoots_cleaned=False, redundant_vertices_cleaned=False, undershoots_extended=False, duplicated_lines_cleaned=False, lines_intersected=False, adjacent_endpoints_merged=False, overshoots_tolerance=1e-10, undershoots_tolerance=1e-10, vertex_tolerance=1e-10, filter_vertex_recordset=None, arc_filter_string=None, filter_mode=None):
        """
        构造拓扑处理参数类

        :param bool pseudo_nodes_cleaned: 是否去除假结点
        :param bool overshoots_cleaned: 是否去除短悬线。
        :param bool redundant_vertices_cleaned: 是否去除冗余点
        :param bool undershoots_extended: 是否进行长悬线延伸。
        :param bool duplicated_lines_cleaned: 是否去除重复线
        :param bool lines_intersected: 是否进行弧段求交。
        :param bool adjacent_endpoints_merged: 是否进行邻近端点合并。
        :param float overshoots_tolerance:  短悬线容限，该容限用于在去除短悬线时判断悬线是否是短悬线。
        :param float undershoots_tolerance: 长悬线容限，该容限用于在长悬线延伸时判断悬线是否延伸。单位与进行拓扑处理的数据集单位相同。
        :param float vertex_tolerance: 节点容限。该容限用于邻近端点合并、弧段求交、去除假结点和去除冗余点。单位与进行拓扑处理的数据集单位相同。
        :param Recordset filter_vertex_recordset: 弧段求交的过滤点记录集，即此记录集中的点位置线段不进行求交打断。
        :param str arc_filter_string: 弧段求交的过滤线表达式。 在进行弧段求交时，通过该属性可以指定一个字段表达式，符合该表达式的线对象将不被打断。
                                      该表达式是否有效，与 filter_mode 弧段求交过滤模式有关
        :param filter_mode: 弧段求交的过滤模式。
        :type filter_mode: ArcAndVertexFilterMode or str
        """
        self._pseudo_nodes_cleaned = True
        self._overshoots_cleaned = True
        self._redundant_vertices_cleaned = True
        self._undershoots_extended = True
        self._duplicated_lines_cleaned = True
        self._lines_intersected = True
        self._adjacent_endpoints_merged = True
        self._overshoots_tolerance = 0.0
        self._undershoots_tolerance = 0.0
        self._vertex_tolerance = 0.0
        self._filter_vertex_recordset = None
        self._arc_filter_string = None
        self._filter_mode = None
        self.set_pseudo_nodes_cleaned(pseudo_nodes_cleaned).set_overshoots_cleaned(overshoots_cleaned).set_overshoots_tolerance(overshoots_tolerance).set_redundant_vertices_cleaned(redundant_vertices_cleaned).set_undershoots_extended(undershoots_extended).set_undershoots_tolerance(undershoots_tolerance).set_duplicated_lines_cleaned(duplicated_lines_cleaned).set_lines_intersected(lines_intersected).set_adjacent_endpoints_merged(adjacent_endpoints_merged).set_vertex_tolerance(vertex_tolerance).set_filter_vertex_recordset(filter_vertex_recordset).set_arc_filter_string(arc_filter_string).set_filter_mode(filter_mode)

    @property
    def pseudo_nodes_cleaned(self):
        """bool: 是否去除假结点"""
        return self._pseudo_nodes_cleaned

    @property
    def overshoots_cleaned(self):
        """bool:  是否去除短悬线"""
        return self._overshoots_cleaned

    @property
    def redundant_vertices_cleaned(self):
        """bool: 是否去除冗余点"""
        return self._redundant_vertices_cleaned

    @property
    def undershoots_extended(self):
        """bool: 是否进行长悬线延伸"""
        return self._undershoots_extended

    @property
    def duplicated_lines_cleaned(self):
        """bool: 是否去除重复线"""
        return self._duplicated_lines_cleaned

    @property
    def lines_intersected(self):
        """bool: 是否进行弧段求交"""
        return self._lines_intersected

    @property
    def adjacent_endpoints_merged(self):
        """bool: 是否进行邻近端点合并"""
        return self._adjacent_endpoints_merged

    @property
    def overshoots_tolerance(self):
        """float: 短悬线容限，该容限用于在去除短悬线时判断悬线是否是短悬线"""
        return self._overshoots_tolerance

    @property
    def undershoots_tolerance(self):
        """float: 长悬线容限，该容限用于在长悬线延伸时判断悬线是否延伸。单位与进行拓扑处理的数据集单位相同"""
        return self._undershoots_tolerance

    @property
    def vertex_tolerance(self):
        """float: 节点容限。该容限用于邻近端点合并、弧段求交、去除假结点和去除冗余点。单位与进行拓扑处理的数据集单位相同"""
        return self._vertex_tolerance

    @property
    def filter_vertex_recordset(self):
        """Recordset: 弧段求交的过滤点记录集，即此记录集中的点位置线段不进行求交打断"""
        return self._filter_vertex_recordset

    @property
    def arc_filter_string(self):
        """str:  弧段求交的过滤线表达式。 在进行弧段求交时，通过该属性可以指定一个字段表达式，符合该表达式的线对象将不被打断。该表达式是否有效，与 filter_mode 弧段求交过滤模式有关"""
        return self._arc_filter_string

    @property
    def filter_mode(self):
        """ArcAndVertexFilterMode: 弧段求交的过滤模式"""
        return self._filter_mode

    def set_pseudo_nodes_cleaned(self, value):
        """
        设置是否去除假结点。结点又称为弧段连接点，至少连接三条弧段的才可称为一个结点。如果弧段连接点只连接了一条弧段（岛屿的情况）或连接了两条弧段（即它是两条弧段的公共端点），则该结点被称为假结点

        :param bool value: 是否去除假结点，True 表示去除，False 表示不去除。
        :return: ProcessingOptions
        :rtype: self
        """
        self._pseudo_nodes_cleaned = bool(value)
        return self

    def set_overshoots_cleaned(self, value):
        """
        设置是否去除短悬线。去除短悬线指如果一条悬线的长度小于悬线容限，则在进行去除短悬线操作时就会把这条悬线删除。通过 set_overshoots_tolerance 方法可以指定短悬线容限，如不指定则使用数据集的短悬线容限。

        悬线：如果一个线对象的端点没有与其它任意一个线对象的端点相连，则这个端点称之为悬点。具有悬点的线对象称之为悬线。

        :param bool value: 是否去除短悬线，True 表示去除，False 表示不去除。
        :return: self
        :rtype: ProcessingOptions
        """
        self._overshoots_cleaned = bool(value)
        return self

    def set_redundant_vertices_cleaned(self, value):
        """
        设置是否去除冗余点。任意弧段上两节点之间的距离小于节点容限时，其中一个即被认为是一个冗余点，在进行拓扑处理时可以去除。

        :param bool value: : 是否去除冗余点，True 表示去除，False 表示不去除。
        :return: self
        :rtype: ProcessingOptions
        """
        self._redundant_vertices_cleaned = bool(value)
        return self

    def set_undershoots_extended(self, value):
        """
        设置是否进行长悬线延伸。 如果一条悬线按其行进方向延伸了指定的长度（悬线容限）之后与某弧段有交点，则拓扑处理后会将该悬线自动延伸到某弧段上，
        称为长悬线延伸。通过 set_undershoots_tolerance 方法可以指定长悬线容限，如不指定则使用数据集的长悬线容限。

        :param bool value:  是否进行长悬线延伸
        :return: self
        :rtype: ProcessingOptions
        """
        self._undershoots_extended = bool(value)
        return self

    def set_duplicated_lines_cleaned(self, value):
        """
        设置是否去除重复线

        重复线：两条弧段若其所有节点两两重合，则可认为是重复线。重复线的判断不考虑方向。

        去除重复线的目的是为避免建立拓扑多边形时产生面积为零的多边形对象，因此，重复的线对象只应保留其中一个，多余的应删除。

        通常，出现重复线多是由于弧段求交造成的。

        :param bool value: 是否去除重复线
        :return: self
        :rtype: ProcessingOptions
        """
        self._duplicated_lines_cleaned = bool(value)
        return self

    def set_lines_intersected(self, value):
        """
        设置是否进行弧段求交。

        线数据建立拓扑关系之前，首先要进行弧段求交计算，根据交点分解成若干线对象，一般而言，在二维坐标系统中凡是与其他线有交点的线对象都需要从交点处打断，如十字路口。且此方法是后续错误处理方法的基础。
        在实际应用中，相交线段完全打断的处理方式在很多时候并不能很好地满足研究需求。例如，一条高架铁路横跨一条公路，在二维坐标上来看是两个相交的线对象，但事实上并没有相交
        ，如果打断将可能影响进一步的分析。在交通领域还有很多类似的实际场景，如河流水系与交通线路的相交，城市中错综复杂的立交桥等，对于某些相交点是否打断，
        需要根据实际应用来灵活处理，而不能因为在二维平面上相交就一律打断。

        这种情况可以通过设置过滤线表达式（ :py:meth:`set_arc_filter_string` ）和过滤点记录集 ( :py:meth:`set_vertex_filter_recordset` ) 来
        确定哪些线对象以及哪些相交位置处不打断:

          - 过滤线表达式用于查询出不需要打断的线对象
          - 过滤点记录集中的点对象所在位置处不打断

        这两个参数单独或组合使用构成了弧段求交的四种过滤模式，还有一种是不进行过滤。过滤模式通过 :py:meth:`set_filter_mode` 方法设置。对于上面的例子，使用不同的过滤模式，弧段求交的结果也不相同。关于过滤模式的详细介绍请参阅 :py:class:`.ArcAndVertexFilterMode` 类。

        注意：进行弧段求交处理时，可通过 :py:meth:`set_vertex_tolerance` 方法设置节点容限（如不设置，将使用数据集的节点容限），用于判断过滤点是否有效。若过滤点到线对象的距离在设置的容限范围内，则线对象在过滤点到其的垂足位置上不被打断。

        :param bool value: 是否进行弧段求交
        :return: self
        :rtype: ProcessingOptions
        """
        self._lines_intersected = bool(value)
        return self

    def set_adjacent_endpoints_merged(self, value):
        """
        设置是否进行邻近端点合并。

        如果多条弧段端点的距离小于节点容限，那么这些点就会被合并成为一个结点，该结点位置是原有点的几何平均（即 X、Y 分别为所有原有点 X、Y 的平均值）。

        用于判断邻近端点的节点容限，可通过\u3000:py:meth:`set_vertex_tolerance` 设置，如果不设置或设置为0，将使用数据集的容限中的节点容限。

        需要注意的是，如果有两个邻近端点，那么合并的结果就会是一个假结点，还需要进行去除假结点的操作。

        :param bool value: 是否进行邻近端点合并
        :return: self
        :rtype: ProcessingOptions
        """
        self._adjacent_endpoints_merged = bool(value)
        return self

    def set_overshoots_tolerance(self, value):
        """
        设置短悬线容限，该容限用于在去除短悬线时判断悬线是否是短悬线。单位与进行拓扑处理的数据集单位相同。

        “悬线”的定义：如果一个线对象的端点没有与其它任意一个线对象的端点相连，则这个端点称之为悬点。具有悬点的线对象称之为悬线。

        :param float value:  短悬线容限
        :return: self
        :rtype: ProcessingOptions
        """
        self._overshoots_tolerance = float(value)
        return self

    def set_undershoots_tolerance(self, value):
        """
        设置长悬线容限，该容限用于在长悬线延伸时判断悬线是否延伸。单位与进行拓扑处理的数据集单位相同。

        :param float value: 长悬线容限
        :return: self
        :rtype: ProcessingOptions
        """
        self._undershoots_tolerance = float(value)
        return self

    def set_vertex_tolerance(self, value):
        """
        设置节点容限。该容限用于邻近端点合并、弧段求交、去除假结点和去除冗余点。单位与进行拓扑处理的数据集单位相同。

        :param float value: 节点容限
        :return: self
        :rtype: ProcessingOptions
        """
        self._vertex_tolerance = float(value)
        return self

    def set_filter_vertex_recordset(self, value):
        """
        设置弧段求交的过滤点记录集，即此记录集中的点位置线段不进行求交打断。

        如果过滤点在线对象上或到线对象的距离在容限范围内，在过滤点到线对象的垂足位置上线对象不被打断。详细介绍请参见 :py:meth:`set_lines_intersected` 方法。

        注意：过滤点记录集是否有效，与 :py:meth:`set_filter_mode` 方法设置的弧段求交过滤模式有关。可参见 :py:class:`.ArcAndVertexFilterMode` 类。

        :param Recordset value: 弧段求交的过滤点记录集
        :return: self
        :rtype: ProcessingOptions
        """
        if value is not None:
            if not isinstance(value, Recordset):
                raise ValueError("FilterVertexRecordset value must be Recordset")
        self._filter_vertex_recordset = value
        return self

    def set_arc_filter_string(self, value):
        """
        设置弧段求交的过滤线表达式。

        在进行弧段求交时，通过该属性可以指定一个字段表达式，符合该表达式的线对象将不被打断。详细介绍请参见 :py:meth:`set_lines_intersected`  方法。

        :param str value: 弧段求交的过滤线表达式
        :return: self
        :rtype: ProcessingOptions
        """
        self._arc_filter_string = value
        return self

    def set_filter_mode(self, value):
        """
        设置弧段求交的过滤模式

        :param value: 弧段求交的过滤模式
        :type value: ArcAndVertexFilterMode
        :return: self
        :rtype: ProcessingOptions
        """
        self._filter_mode = ArcAndVertexFilterMode._make(value)
        return self

    @property
    def _jobject(self):
        """Py4J 映射的 Java 端的对象"""
        jvm = get_jvm()
        java_options = jvm.com.supermap.data.topology.TopologyProcessingOptions()
        java_options.setAdjacentEndpointsMerged(self.adjacent_endpoints_merged)
        java_options.setDuplicatedLinesCleaned(self.duplicated_lines_cleaned)
        java_options.setLinesIntersected(self.lines_intersected)
        java_options.setOvershootsCleaned(self.overshoots_cleaned)
        java_options.setPseudoNodesCleaned(self.pseudo_nodes_cleaned)
        java_options.setRedundantVerticesCleaned(self.redundant_vertices_cleaned)
        java_options.setUndershootsExtended(self.undershoots_extended)
        java_options.setOvershootsTolerance(self.overshoots_tolerance)
        java_options.setUndershootsTolerance(self.undershoots_tolerance)
        java_options.setVertexTolerance(self.vertex_tolerance)
        if self.filter_vertex_recordset is not None:
            java_options.setVertexFilterRecordset(self.filter_vertex_recordset._jobject)
        if self.filter_mode is not None:
            java_options.setFilterMode(self.filter_mode._jobject)
        if self.arc_filter_string is not None:
            java_options.setArcFilterString(self.arc_filter_string)
        return java_options


def topology_processing(input_data, pseudo_nodes_cleaned=True, overshoots_cleaned=True, redundant_vertices_cleaned=True, undershoots_extended=True, duplicated_lines_cleaned=True, lines_intersected=True, adjacent_endpoints_merged=True, overshoots_tolerance=1e-10, undershoots_tolerance=1e-10, vertex_tolerance=1e-10, filter_vertex_recordset=None, arc_filter_string=None, filter_mode=None, options=None, progress=None):
    """
    根据拓扑处理选项对给定的数据集进行拓扑处理。将直接修改原始数据。

    :param input_data: 指定的拓扑处理的数据集。
    :type input_data: DatasetVector or str
    :param bool pseudo_nodes_cleaned: 是否去除假结点
    :param bool overshoots_cleaned: 是否去除短悬线。
    :param bool redundant_vertices_cleaned: 是否去除冗余点
    :param bool undershoots_extended: 是否进行长悬线延伸。
    :param bool duplicated_lines_cleaned: 是否去除重复线
    :param bool lines_intersected: 是否进行弧段求交。
    :param bool adjacent_endpoints_merged: 是否进行邻近端点合并。
    :param float overshoots_tolerance:  短悬线容限，该容限用于在去除短悬线时判断悬线是否是短悬线。
    :param float undershoots_tolerance: 长悬线容限，该容限用于在长悬线延伸时判断悬线是否延伸。单位与进行拓扑处理的数据集单位相同。
    :param float vertex_tolerance: 节点容限。该容限用于邻近端点合并、弧段求交、去除假结点和去除冗余点。单位与进行拓扑处理的数据集单位相同。
    :param Recordset filter_vertex_recordset: 弧段求交的过滤点记录集，即此记录集中的点位置线段不进行求交打断。
    :param str arc_filter_string: 弧段求交的过滤线表达式。 在进行弧段求交时，通过该属性可以指定一个字段表达式，符合该表达式的线对象将不被打断。
                                  该表达式是否有效，与 filter_mode 弧段求交过滤模式有关
    :param filter_mode: 弧段求交的过滤模式。
    :type filter_mode: ArcAndVertexFilterMode or str
    :param options: 拓扑处理参数类，如果 options 不为空，拓扑处理将会使用此参数设置的值。
    :type options: ProcessingOptions or None
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 是否拓扑处理成功
    :rtype: bool
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    elif not isinstance(_source_input, DatasetVector):
        raise ValueError("source input_data must be DatasetVector")
    _jvm = get_jvm()
    if options is not None:
        java_option = options._jobject
    else:
        java_option = ProcessingOptions(pseudo_nodes_cleaned, overshoots_cleaned, redundant_vertices_cleaned, undershoots_extended, duplicated_lines_cleaned, lines_intersected, adjacent_endpoints_merged, overshoots_tolerance, undershoots_tolerance, vertex_tolerance, filter_vertex_recordset, arc_filter_string, filter_mode)._jobject
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, "TopologyBuildRegions")
                _jvm.com.supermap.data.topology.TopologyProcessing.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            is_success = _jvm.com.supermap.data.topology.TopologyProcessing.clean(_source_input._jobject, java_option)
        except Exception as e:
            try:
                log_error(e)
                is_success = False
            finally:
                e = None
                del e

    finally:
        return

    if listener is not None:
        try:
            _jvm.com.supermap.data.topology.TopologyProcessing.removeSteppedListener(listener)
        except Exception as e1:
            try:
                log_error(e1)
            finally:
                e1 = None
                del e1

        close_callback_server()
    return is_success


def topology_build_regions(input_data, out_data=None, out_dataset_name=None, progress=None):
    """
    用于将线数据集或者网络数据集，通过拓扑处理来构建面数据集。在进行拓扑构面前，最好能使用拓扑处理 :py:meth:`topology_processing` 对数据集进行拓扑处理。

    :param input_data: 指定的用于进行多边形拓扑处理的源数据集，只能是线数据集或网络数据集。
    :type input_data: DatasetVector or str
    :param out_data: 用于存储结果数据集的数据源。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector or str
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    else:
        if not isinstance(_source_input, DatasetVector):
            raise ValueError("source input_data must be DatasetVector")
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = input_data.datasource
        check_output_datasource(_ds)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + "_region"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, "TopologyBuildRegions")
                _jvm.com.supermap.data.topology.TopologyProcessing.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            java_result_dt = _jvm.com.supermap.data.topology.TopologyProcessing.buildRegions(_source_input._jobject, _ds._jobject, _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.data.topology.TopologyProcessing.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def pickup_border(input_data, is_preprocess=True, extract_ids=None, out_data=None, out_dataset_name=None, progress=None):
    """
    提取面（或线）的边界，并保存为线数据集。若多个面（或线）共边界（线段），该边界（线段）只会被提取一次。

    不支持重叠面提取边界。

    :param input_data: 指定的面或线数据集。
    :type input_data: DatasetVector or str
    :param bool is_preprocess: 是否进行拓扑预处理
    :param extract_ids:  指定的面ID数组，可选参数，仅会提取给定ID数组对应的面对象边界。
    :type extract_ids: list[int] or str
    :param out_data: 用于存储结果数据集的数据源。
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector or str
    """
    check_lic()
    _source_input = get_input_dataset(input_data)
    if _source_input is None:
        raise ValueError("source input_data is None")
    else:
        if not isinstance(_source_input, DatasetVector):
            raise ValueError("source input_data must be DatasetVector")
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
            _ds = out_datasource
        else:
            _ds = input_data.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = _source_input.name + "_border"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, "PickupBorder")
                _jvm.com.supermap.data.topology.TopologyProcessing.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            pickupBorder = get_jvm().com.supermap.data.topology.TopologyProcessing.pickupBorder
            if extract_ids is None:
                java_result_dt = pickupBorder(oj(_source_input), oj(_ds), _outDatasetName, bool(is_preprocess))
            else:
                extract_ids = to_java_int_array(split_input_list_from_str(extract_ids))
                java_result_dt = pickupBorder(oj(_source_input), oj(_ds), _outDatasetName, extract_ids, bool(is_preprocess))
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.data.topology.TopologyProcessing.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


class PreprocessOptions(object):
    __doc__ = "\n    拓扑预处理参数类\n    "
    _arcs_inserted = False
    _vertex_arc_inserted = False
    _vertexes_snapped = False
    _polygons_checked = False
    _vertex_adjusted = False

    def __init__(self, arcs_inserted=False, vertex_arc_inserted=False, vertexes_snapped=False, polygons_checked=False, vertex_adjusted=False):
        """
        构造拓扑预处理参数类对象

        :param bool arcs_inserted: 是否进行线段间求交插入节点
        :param bool vertex_arc_inserted: 否进行节点与线段间插入节点
        :param bool vertexes_snapped: 是否进行节点捕捉
        :param bool polygons_checked: 是否进行多边形走向调整
        :param bool vertex_adjusted: 是否进行节点位置调整
        """
        self.set_arcs_inserted(arcs_inserted).set_polygons_checked(polygons_checked).set_vertex_adjusted(vertex_adjusted).set_vertex_arc_inserted(vertex_arc_inserted).set_vertexes_snapped(vertexes_snapped)

    @property
    def arcs_inserted(self):
        """bool: 是否进行线段间求交插入节点"""
        return self._arcs_inserted

    @property
    def vertex_arc_inserted(self):
        """bool: 否进行节点与线段间插入节点"""
        return self._vertex_arc_inserted

    @property
    def vertexes_snapped(self):
        """bool: 是否进行节点捕捉"""
        return self._vertexes_snapped

    @property
    def polygons_checked(self):
        """bool: 是否进行多边形走向调整"""
        return self._polygons_checked

    @property
    def vertex_adjusted(self):
        """bool: 是否进行节点位置调整"""
        return self._vertex_adjusted

    def set_arcs_inserted(self, value):
        """
        设置是否进行线段间求交插入节点

        :param bool value: 是否进行线段间求交插入节点
        :return: self
        :rtype: PreprocessOptions
        """
        self._arcs_inserted = bool(value)
        return self

    def set_polygons_checked(self, value):
        """
        设置是否进行多边形走向调整

        :param bool value: 是否进行多边形走向调整
        :return: self
        :rtype: PreprocessOptions
        """
        self._polygons_checked = bool(value)
        return self

    def set_vertex_adjusted(self, value):
        """
        设置是否进行节点位置调整

        :param bool value: 是否进行节点位置调整
        :return: self
        :rtype: PreprocessOptions
        """
        self._vertex_adjusted = bool(value)
        return self

    def set_vertex_arc_inserted(self, value):
        """
        设置否进行节点与线段间插入节点

        :param bool value: 否进行节点与线段间插入节点
        :return: self
        :rtype: PreprocessOptions
        """
        self._vertex_arc_inserted = bool(value)
        return self

    def set_vertexes_snapped(self, value):
        """
        设置是否进行节点捕捉

        :param bool value: 是否进行节点捕捉
        :return: self
        :rtype: PreprocessOptions
        """
        self._vertexes_snapped = bool(value)
        return self

    @property
    def _jobject(self):
        """Py4J 映射的 Java 对象"""
        java_option = get_jvm().com.supermap.data.topology.TopologyPreprocessOptions()
        java_option.setArcsInserted(self.arcs_inserted)
        java_option.setPolygonsChecked(self.polygons_checked)
        java_option.setVertexAdjusted(self.vertex_adjusted)
        java_option.setVertexArcInserted(self.vertex_arc_inserted)
        java_option.setVertexesSnapped(self.vertexes_snapped)
        return java_option


def preprocess(inputs, arcs_inserted=True, vertex_arc_inserted=True, vertexes_snapped=True, polygons_checked=True, vertex_adjusted=True, precisions=None, tolerance=1e-10, options=None, progress=None):
    """
    对给定的拓扑数据集进行拓扑预处理。

    :param inputs: 输入数据集或记录集，如果是数据集，不能是只读。
    :type inputs: DatasetVector or list[DatasetVector] or str or list[str] or Recordset or list[Recordset]
    :param bool arcs_inserted: 是否进行线段间求交插入节点
    :param bool vertex_arc_inserted: 否进行节点与线段间插入节点
    :param bool vertexes_snapped: 是否进行节点捕捉
    :param bool polygons_checked: 是否进行多边形走向调整
    :param bool vertex_adjusted: 是否进行节点位置调整
    :param precisions: 指定的精度等级数组。精度等级的值越小，代表对应记录集的精度越高，数据质量越好。在进行顶点捕捉时，低精度的记录集中的点将被捕捉到高精度记录集中的点的位置上。精度等级数组必须与要进行拓扑预处理的记录集集合元素数量相同并一一对应。
    :type precisions: list[int]
    :param float tolerance: 指定的处理时需要的容限控制。单位与进行拓扑预处理的记录集单位相同。
    :param PreprocessOption options: 拓扑预处理参数类对象，如果此参数不为空，将优先使用此参数为拓扑预处理参数
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 拓扑预处理是否成功
    :rtype: bool
    """
    check_lic()
    if inputs is None:
        raise ValueError("inputs is None")
    else:
        is_def_orders = True if precisions is not None else False
        if is_def_orders:
            _precisions = split_input_list_from_str(precisions)
        else:
            _datasets = []
            _recordsets = []
            _datasets_orders = []
            _recordsets_orders = []
            if isinstance(inputs, (list, tuple)):
                for i in range(len(inputs)):
                    item = inputs[i]
                    temp = get_input_dataset(item)
                    if temp is not None:
                        if isinstance(temp, DatasetVector):
                            _datasets.append(temp)
                            if is_def_orders:
                                _datasets_orders.append(int(_precisions[i]))
                            else:
                                _datasets_orders.append(0)
                        elif isinstance(temp, Recordset):
                            _recordsets.append(temp)
                            if is_def_orders:
                                _recordsets_orders.append(int(precisions[i]))
                            else:
                                _datasets_orders.append(0)
                        else:
                            raise ValueError("Only support DatasetVector or Recordset")
                    else:
                        raise ValueError("input_data item is None" + str(item))

            else:
                temp = get_input_dataset(inputs)
                if temp is not None:
                    if isinstance(temp, DatasetVector):
                        _datasets_orders.append(0)
                        _datasets.append(temp)
                    else:
                        if isinstance(temp, Recordset):
                            _recordsets_orders.append(0)
                            _recordsets.append(temp)
                        else:
                            raise ValueError("Only support DatasetVector or Recordset")
                else:
                    raise ValueError("input_data item is None" + str(inputs))
    if len(_datasets) + len(_recordsets) == 0:
        raise ValueError("have no valid inputs")
    if len(_datasets) != len(_datasets_orders):
        raise ValueError("the count of precisionOrders must be equal with inputs")
    if len(_recordsets) != len(_recordsets_orders):
        raise ValueError("the count of precisionOrders must be equal with inputs")
    if options is not None and isinstance(options, PreprocessOptions):
        parameters = options
    else:
        parameters = PreprocessOptions(arcs_inserted, vertex_arc_inserted, vertexes_snapped, polygons_checked, vertex_adjusted)
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, "preprocess")
                _jvm.com.supermap.data.topology.TopologyValidator.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            _all_recordsets = []
            _all_orders = []
            _queryed_recordsets = []
            i = -1
            for rd in _recordsets:
                i += 1
                _all_recordsets.append(rd)
                _queryed_recordsets.append(rd)
                if is_def_orders:
                    _all_orders.append(_recordsets_orders[i])
                else:
                    _all_orders.append(0)

            i = -1
            for dt in _datasets:
                i += 1
                rd = dt.get_recordset(False, CursorType.DYNAMIC)
                if rd is not None:
                    _all_recordsets.append(rd)
                    if is_def_orders:
                        _all_orders.append(_datasets_orders[i])
                    else:
                        _all_orders.append(0)

            is_success = _jvm.com.supermap.data.topology.TopologyValidator.preprocess(to_java_recordset_array(_all_recordsets), to_java_int_array(_all_orders), parameters._jobject, float(tolerance))
        except:
            import traceback
            log_error(traceback.format_exc())
            is_success = False

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.data.topology.TopologyValidator.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        for rd in _queryed_recordsets:
            rd.close()

        _queryed_recordsets.clear()

    return is_success


def topology_validate(source_data, validating_data, rule, tolerance, validate_region=None, out_data=None, out_dataset_name=None, progress=None):
    """
    对数据集或记录集进行拓扑错误检查，返回含有拓扑错误的结果数据集。

    该方法的 tolerance 参数用于指定使用 rule 参数指定的拓扑规则对数据集检查时涉及的容限。例如，使用“线内无打折”（TopologyRule.LINE_NO_SHARP_ANGLE）规则检查时，tolerance 参数设置的为尖角容限（一个角度值）。

    对于以下拓扑检查算子在调用该方法对数据进行拓扑检查之前，建议先对相应的数据进行拓扑预处理（即调用 :py:meth:`preprocess` 方法），否则检查的结果可能不正确:

        - REGION_NO_OVERLAP_WITH
        - REGION_COVERED_BY_REGION_CLASS
        - REGION_COVERED_BY_REGION
        - REGION_BOUNDARY_COVERED_BY_LINE
        - REGION_BOUNDARY_COVERED_BY_REGION_BOUNDARY
        - REGION_NO_OVERLAP_ON_BOUNDARY
        - REGION_CONTAIN_POINT
        - LINE_NO_OVERLAP_WITH
        - LINE_BE_COVERED_BY_LINE_CLASS
        - LINE_END_POINT_COVERED_BY_POINT
        - POINT_NO_CONTAINED_BY_REGION
        - POINT_COVERED_BY_LINE
        - POINT_COVERED_BY_REGION_BOUNDARY
        - POINT_CONTAINED_BY_REGION
        - POINT_BECOVERED_BY_LINE_END_POINT

    对于以下拓扑检查算法需要设置参考数据集或记录集:

        - REGION_NO_OVERLAP_WITH
        - REGION_COVERED_BY_REGION_CLASS
        - REGION_COVERED_BY_REGION
        - REGION_BOUNDARY_COVERED_BY_LINE
        - REGION_BOUNDARY_COVERED_BY_REGION_BOUNDARY
        - REGION_CONTAIN_POINT
        - REGION_NO_OVERLAP_ON_BOUNDARY
        - POINT_BECOVERED_BY_LINE_END_POINT
        - POINT_NO_CONTAINED_BY_REGION
        - POINT_CONTAINED_BY_REGION
        - POINT_COVERED_BY_LINE
        - POINT_COVERED_BY_REGION_BOUNDARY
        - LINE_NO_OVERLAP_WITH
        - LINE_NO_INTERSECT_OR_INTERIOR_TOUCH
        - LINE_BE_COVERED_BY_LINE_CLASS
        - LINE_NO_INTERSECTION_WITH
        - LINE_NO_INTERSECTION_WITH_REGION
        - LINE_EXIST_INTERSECT_VERTEX
        - VERTEX_DISTANCE_GREATER_THAN_TOLERANCE
        - VERTEX_MATCH_WITH_EACH_OTHER

    :param source_data: 被检查的数据集或记录集
    :type source_data: DatasetVector or str or Recordset
    :param validating_data:  用于检查的参考记录集。如果使用的拓扑规则不需要参考记录集，则设置为 None
    :type validating_data: DatasetVector or str or Recordset
    :param rule: 拓扑检查类型
    :type rule: TopologyRule or str
    :param float tolerance:   指定的拓扑错误检查时使用的容限。单位与进行拓扑错误检查的数据集单位相同。
    :param GeoRegion validate_region: 被检查区域，None，则默认对整个拓扑数据集（validating_data）进行检查，否则对 validate_region 区域进行拓扑检查。
    :param out_data: 结果数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param function progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :return: 结果数据集或数据集名称
    :rtype: DatasetVector or str
    """
    check_lic()
    if source_data is None:
        raise ValueError("sourceData is None")
    else:
        _rule_preprocess = {(TopologyRule.REGION_NO_OVERLAP): (True, False), 
         (TopologyRule.REGION_NO_GAPS): (True, False), 
         (TopologyRule.REGION_NO_OVERLAP_WITH): (True, True), 
         (TopologyRule.REGION_COVERED_BY_REGION_CLASS): (True, True), 
         (TopologyRule.REGION_COVERED_BY_REGION): (True, True), 
         (TopologyRule.REGION_BOUNDARY_COVERED_BY_LINE): (True, True), 
         (TopologyRule.REGION_BOUNDARY_COVERED_BY_REGION_BOUNDARY): (True, True), 
         (TopologyRule.REGION_CONTAIN_POINT): (False, True), 
         (TopologyRule.REGION_NO_OVERLAP_ON_BOUNDARY): (True, True), 
         (TopologyRule.REGION_NO_SELF_INTERSECTION): (True, False), 
         (TopologyRule.LINE_NO_INTERSECTION): (False, False), 
         (TopologyRule.LINE_NO_DANGLES): (False, False), 
         (TopologyRule.LINE_NO_PSEUDO_NODES): (False, False), 
         (TopologyRule.LINE_NO_OVERLAP_WITH): (True, True), 
         (TopologyRule.LINE_NO_INTERSECT_OR_INTERIOR_TOUCH): (True, False), 
         (TopologyRule.LINE_NO_SELF_OVERLAP): (False, False), 
         (TopologyRule.LINE_NO_SELF_INTERSECT): (False, False), 
         (TopologyRule.LINE_BE_COVERED_BY_LINE_CLASS): (True, True), 
         (TopologyRule.LINE_END_POINT_COVERED_BY_POINT): (False, True), 
         (TopologyRule.LINE_NO_INTERSECTION_WITH): (True, False), 
         (TopologyRule.LINE_NO_INTERSECTION_WITH_REGION): (True, False), 
         (TopologyRule.POINT_NO_IDENTICAL): (False, False), 
         (TopologyRule.POINT_NO_CONTAINED_BY_REGION): (True, True), 
         (TopologyRule.POINT_COVERED_BY_LINE): (True, True), 
         (TopologyRule.POINT_COVERED_BY_REGION_BOUNDARY): (True, True), 
         (TopologyRule.POINT_CONTAINED_BY_REGION): (True, True), 
         (TopologyRule.POINT_BECOVERED_BY_LINE_END_POINT): (True, True), 
         (TopologyRule.NO_MULTIPART): (False, False), 
         (TopologyRule.VERTEX_DISTANCE_GREATER_THAN_TOLERANCE): (True, False), 
         (TopologyRule.VERTEX_MATCH_WITH_EACH_OTHER): (True, False), 
         (TopologyRule.LINE_EXIST_INTERSECT_VERTEX): (True, False), 
         (TopologyRule.NO_REDUNDANT_VERTEX): (False, False), 
         (TopologyRule.LINE_NO_SHARP_ANGLE): (False, False), 
         (TopologyRule.LINE_NO_SMALL_DANGLES): (False, False), 
         (TopologyRule.LINE_NO_EXTENDED_DANGLES): (False, False), 
         (TopologyRule.REGION_NO_ACUTE_ANGLE): (False, False)}
        rule = TopologyRule._make(rule)
        if rule is None:
            raise ValueError("rule is None")
        else:
            if tolerance is None:
                tolerance = 1e-10
            else:
                tolerance = float(tolerance)
            _source_input = get_input_dataset(source_data)
            if _source_input is None:
                raise ValueError("source input_data data is None")
            if validating_data is not None:
                _validate_input = get_input_dataset(validating_data)
            else:
                _validate_input = None
        if isinstance(_source_input, DatasetVector):
            if _validate_input is not None and isinstance(_validate_input, Recordset):
                _source_input = _source_input.get_recordset()
        elif isinstance(_source_input, Recordset) and _validate_input is not None:
            if isinstance(_validate_input, DatasetVector):
                _validate_input = _validate_input.get_recordset()
            else:
                if _validate_input is not None:
                    java_validate_input = _validate_input._jobject
                else:
                    java_validate_input = None
                if out_data is not None:
                    out_datasource = get_output_datasource(out_data)
                    _ds = out_datasource
                else:
                    _ds = _source_input.datasource
            check_output_datasource(_ds)
            if out_dataset_name is None:
                _outDatasetName = "validate_Errors"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = _ds.get_available_dataset_name(_outDatasetName)
    _jvm = get_jvm()
    javaValidateRegion = None
    if validate_region is not None:
        javaValidateRegion = validate_region._jobject
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, "topology_validate")
                _jvm.com.supermap.data.topology.TopologyValidator.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            java_result_dt = _jvm.com.supermap.data.topology.TopologyValidator.validate(_source_input._jobject, java_validate_input, rule._jobject, tolerance, javaValidateRegion, _ds._jobject, _outDatasetName)
        except Exception as e:
            try:
                log_error(e)
                java_result_dt = None
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.data.topology.TopologyValidator.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result_dt is not None:
            result_dt = _ds[java_result_dt.getName()]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def split_lines_by_regions(line_input, region_input, progress=None):
    """
    用面对象分割线对象。在提取线对象的左右多边形（即 pickupLeftRightRegions() 方法）操作前，需要调用该方法分割线对象，否则会出现一个线对象对应多个左（右）多边形的情形。
    如下图：线对象 AB，如果不用面对象进行分割，则 AB 的左多边形有两个，分别为1，3；右多边形也有两个，分别为1和3，进行分割操作后，线对象 AB 分割为 AC 与 CB，此时 AC 与 CB 各自对应的左、右多边形分别只有一个。

    .. image:: ../image/SplitLinesByRegions.png

    :param line_input:  指定的被分割的线记录集或数据集。
    :type line_input: DatasetVector or Recordset
    :param region_input: 指定的用于分割线记录集的面记录集或数据集。
    :type region_input: DatasetVector or Recordset
    :param function progress: 处理进度信息的函数
    :return: 成功返回 True，失败返回 False。
    :rtype: bool
    """
    _line_input = get_input_dataset(line_input)
    if _line_input is None:
        raise ValueError("lineInput is None")
    if not isinstance(_line_input, (DatasetVector, Recordset)):
        raise ValueError("lineInput must be DatasetVector or Recordset")
    _region_input = get_input_dataset(region_input)
    if _region_input is None:
        raise ValueError("regionInput is None")
    else:
        if not isinstance(_region_input, (DatasetVector, Recordset)):
            raise ValueError("regionInput must be DatasetVector or Recordset")
        else:
            _is_release_line = False
            if isinstance(_line_input, DatasetVector):
                _line_rd = _line_input.get_recordset(False, CursorType.DYNAMIC)
                _is_release_line = True
            else:
                _line_rd = _line_input
        _is_release_region = False
        if isinstance(_region_input, DatasetVector):
            _region_rd = _region_input.get_recordset(False, CursorType.STATIC)
            _is_release_region = True
        else:
            _region_rd = _region_input
    _jvm = get_jvm()
    listener = None
    if progress is not None:
        if safe_start_callback_server():
            try:
                listener = ProgressListener(progress, "SplitLinesByRegions")
                _jvm.com.supermap.data.topology.TopologyProcessing.addSteppedListener(listener)
            except Exception as e:
                try:
                    close_callback_server()
                    log_error(e)
                    listener = None
                finally:
                    e = None
                    del e

    try:
        try:
            is_success = _jvm.com.supermap.data.topology.TopologyProcessing.splitLinesByRegions(_line_rd._jobject, _region_rd._jobject)
        except Exception as e:
            try:
                log_error(e)
                is_success = False
            finally:
                e = None
                del e

    finally:
        if listener is not None:
            try:
                _jvm.com.supermap.data.topology.TopologyProcessing.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()

    if _is_release_line:
        _line_rd.close()
    if _is_release_region:
        _region_rd.close()
    return is_success

# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/_jsuperpy\analyst\terrain.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 55722 bytes
"""
水文分析模块
"""
from iobjectspy._jsuperpy._gateway import get_jvm, safe_start_callback_server, close_callback_server
from iobjectspy._jsuperpy.data import Datasource, DatasetVector, Point2D, Geometry, DatasetGrid, GeoRegion
from iobjectspy._jsuperpy.data._listener import ProgressListener
from iobjectspy._jsuperpy.data._util import get_input_dataset, get_output_datasource, check_output_datasource, try_close_output_datasource, to_java_point2ds
from iobjectspy._jsuperpy.enums import *
from iobjectspy._jsuperpy._utils import *
from iobjectspy._jsuperpy._logger import *
__all__ = [
 'basin', 'build_quad_mesh', 'fill_sink', 'flow_accumulation', 'flow_direction', 
 'flow_length', 
 'stream_order', 'stream_to_line', 'stream_link', 'watershed', 'pour_points']

def basin(direction_grid, out_data=None, out_dataset_name=None, progress=None):
    """
    关于水文分析：

    * 水文分析基于数字高程模型（DEM）栅格数据建立水系模型，用于研究流域水文特征和模拟地表水文过程，并对未来的地表水文情况做出预估。水文分析模型能够帮助我们分析洪水的范围，定位径流污染源，预测地貌改变对径流的影响等，广泛应用于区域规划、农林、灾害预测、道路设计等诸多行业和领域。

    * 地表水的汇流情况很大程度上决定于地表形状，而 DEM 数据能够表达区域地貌形态的空间分布，在描述流域地形，如流域边界、坡度和坡向、河网提取等方面具有突出优势，因而非常适用于水文分析。

    * SuperMap 提供的水文分析主要内容有填充洼地、计算流向、计算流长、计算累积汇水量、流域划分、河流分级、连接水系及水系矢量化等。

        * 水文分析的一般流程为：

          .. image:: ../image/HydrologyAnalyst_2.png

        * 如何获得栅格水系？

          水文分析中很多功能都需要基于栅格水系数据，如提取矢量水系（:py:func:`stream_to_line` 方法）、河流分级（:py:func:`stream_order` 方法）、
          连接水系（::py:func:`stream_link` 方法）等。

          通常，可以从累积汇水量栅格中提取栅格水系数据。在累积汇水量栅格中，单元格的值越大，代表该区域的累积汇水量越大。累积汇水量
          较高的单元格可视为河谷，因此，可以通过设定一个阈值，提取累积汇水量大于该值的单元格，这些单元格就构成栅格水系。值得说明的
          是，对于不同级别的河谷、不同区域的相同级别的河谷，该值可能不同，因此该阈值的确定需要依据研究区域的实际地形地貌并通过不断的试验来确定。

          在 SuperMap 中，要求用于进一步分析（提取矢量水系、河流分级、连接水系等）的栅格水系为一个二值栅格，这可以通过栅格代数运算
          来实现，使大于或等于累积汇水量阈值的单元格为 1，否则为 0，如下图所示。

          .. image:: ../image/HydrologyAnalyst_3.png

          因此，提取栅格水系的过程如下：

           1. 获得累积汇水量栅格，可通过 :py:func:`flow_accumulation` 方法实现。
           2. 通过栅格代数运算 :py:func:`expression_math_analyst` 方法对累积汇水量栅格进行关系运算，就可以得到满足要求的栅格水系数据。假设设定
              阈值为 1000，则运算表达式为："[Datasource.FlowAccumulationDataset]>1000"。除此，使用 Con(x,y,z) 函数也可以得到想
              要的结果，即表达式为："Con([Datasource.FlowAccumulationDataset]>1000,1,0)"。

    根据流向栅格计算流域盆地。流域盆地即为集水区域，是用于描述流域的方式之一。

    计算流域盆地是依据流向数据为每个单元格分配唯一盆地的过程，如下图所示，流域盆地是描述流域的方式之一，展现了那些所有相互连接且处于同一流域盆地的栅格。

    .. image:: ../image/Basin.png

    :param direction_grid: 流向栅格数据集。
    :type direction_grid: DatasetGrid or str
    :param out_data: 存储结果数据集的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name: 结果数据集名称
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 流域盆地栅格数据集或数据集名称
    :rtype: DatasetGrid or str
    """
    check_lic()
    source_dt = get_input_dataset(direction_grid)
    if not isinstance(source_dt, DatasetGrid):
        raise ValueError("source required DatasetGrid, but is " + str(type(direction_grid)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = source_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = source_dt.name + "_basin"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "basin")
                        get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            func_basin = get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.basin
            java_result = func_basin(oj(source_dt), oj(out_datasource), _outDatasetName)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def build_quad_mesh(quad_mesh_region, left_bottom, left_top, right_bottom, right_top, cols=0, rows=0, out_col_field=None, out_row_field=None, out_data=None, out_dataset_name=None, progress=None):
    """
    对单个简单面对象进行网格剖分。
    流体问题是一个连续性的问题，为了简化对其的研究以及建模处理的方便，对研究区域进行离散化处理，其思路就是建立离散的网格，网格划分就是对连续的物理区域进行剖分，把它分成若干个网格，并确定各个网格中的节点，用网格内的一个值来代替整个网格区域的基本情况，网格作为计算与分析的载体，其质量的好坏对后期的数值模拟的精度和计算效率有重要的影响。

    网格剖分的步骤：

     1．数据预处理，包含去除重复点等。给定一个合理的容限，去除重复点，使得最后的网格划分结果更趋合理，不会出现看起来从1个点
       （实际是重复点）出发有多条线的现象。

     2．多边形分解：对于复杂的多边形区域，我们采用分块逐步划分的方法来进行网格的构建，将一个复杂的不规则多边形区域划分为多个简
        单的单连通区域，然后对每个单连通区域执行网格划分程序，最后再将各个子区域网格拼接起来构成对整个区域的划分。

     3．选择四个角点：这4个角点对应着网格划分的计算区域上的4个顶点，其选择会对划分的结果造成影响。其选择应尽量在原区域近似四边
        形的四个顶点上，同时要考虑整体的流势。

        .. image:: ../image/SelectPoint.png

     4．为了使划分的网格呈现四边形的特征，构成多边形的顶点数据（不在同一直线上）需参与构网。

     5．进行简单区域网格划分。

    注：简单多边形：多边形内任何直线或边都不会交叉。

        .. image:: ../image/QuadMeshPart.png

    说明：

     RightTopIndex 为右上角点索引号，LeftTopIndex 为左上角点索引号，RightBottomIndex 为右下角点索引号，LeftBottomIndex
     为左下角点索引号。则 nCount1=（RightTopIndex- LeftTopIndex+1）和 nCount2=（RightBottomIndex- LeftBottomIndex+1），
     如果：nCount1不等于nCount2，则程序不处理。

    水文分析的相关介绍，请参考 :py:func:`basin`

    :param quad_mesh_region: 网格剖分的面对象
    :type quad_mesh_region: GeoRegion
    :param Point2D left_bottom: 网格剖分的区域多边形左下角点坐标。四个角点选择依据：4个角点对应着网格剖分的计算区域上的4个顶点，
                                其选择会对剖分的结果造成影响。其选择应尽量在原区域近似四边形的四个顶点上，同时要考虑整体的流势。
    :param Point2D left_top: 网格剖分的区域多边形左上角点坐标
    :param Point2D right_bottom: 网格剖分的区域多边形右下角点坐标
    :param Point2D right_top: 网格剖分的区域多边形右上角点坐标
    :param int cols: 网格剖分的列方向节点数。默认值为0，表示不参与处理；若不为0，但是此值若小于多边形列方向的最大点数减一，则
                     以多边形列方向的最大点数减一作为列数（cols）；若大于多边形列方向的最大点数减一，则会自动加点，使列方
                     向的数目为 cols。
                     举例来讲：如果用户希望将一矩形面对象划分为2*3（高*宽）=6个小矩形，则列方向数目（cols）为3。
    :param int rows: 网格剖分的行方向节点数。默认值为0，表示不参与处理；若不为0，但是此值小于多边形行方向的最大点数减一，则以
                     多边形行方向的最大点数减一作为行数（rows）；若大于多边形行方向的最大点数减一，则会自动加点，使行方向的
                     数目为 rows。举例来讲：如果用户希望将一矩形面对象划分为2*3（高*宽）=6个小矩形，则行方向数目（rows）为2。
    :param str out_col_field: 格网剖分结果对象的列属性字段名称。此字段用来保存剖分结果对象的列号。
    :param str out_row_field: 格网剖分结果对象的行属性字段名称。此字段用来保存剖分结果对象的行号。
    :param out_data: 存放剖分结果数据集的数据源。
    :type out_data: DatasourceConnectionInfo or Datasource or str
    :param str out_dataset_name: 剖分结果数据集的名称。
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 剖分后的结果数据集，剖分出的多个面以子对象形式返回。
    :rtype: DatasetVector or str
    """
    check_lic()
    if not isinstance(quad_mesh_region, GeoRegion):
        raise ValueError("quad_mesh_region required GeoRegion, but now is " + str(type(quad_mesh_region)))
    elif out_data is not None:
        out_datasource = get_output_datasource(out_data)
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = "quadmesh"
        else:
            _outDatasetName = out_dataset_name
        _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    else:
        out_datasource = None
        _outDatasetName = None
    listener = None
    try:
        try:
            if progress is not None and safe_start_callback_server():
                try:
                    listener = ProgressListener(progress, "build_quad_mesh")
                    get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.addSteppedListener(listener)
                except Exception as e:
                    try:
                        close_callback_server()
                        log_error(e)
                        listener = None
                    finally:
                        e = None
                        del e

            else:
                java_param = get_jvm().com.supermap.analyst.terrainanalyst.QuadMeshParameter()
                java_param.setQuadMeshRegion(oj(quad_mesh_region))
                java_param.setLeftBottomPoint(oj(Point2D.make(left_bottom)))
                java_param.setLeftTopPoint(oj(Point2D.make(left_top)))
                java_param.setRightBottomPoint(oj(Point2D.make(right_bottom)))
                java_param.setRightTopPoint(oj(Point2D.make(right_top)))
                java_param.setColCount(int(cols))
                java_param.setRowCount(int(rows))
                if out_col_field is not None:
                    java_param.setColField(str(out_col_field))
                if out_row_field is not None:
                    java_param.setRowField(str(out_row_field))
                buildQuadMesh = get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.buildQuadMesh
                if out_datasource is None:
                    java_result = buildQuadMesh(java_param)
                else:
                    java_result = buildQuadMesh(java_param, oj(out_datasource), _outDatasetName)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        if java_result is None:
            if out_datasource is not None:
                try_close_output_datasource(None, out_datasource)
            return
        if out_datasource is None:
            return list((Geometry._from_java_object(geo) for geo in java_result))
        return try_close_output_datasource(out_datasource[_outDatasetName], out_datasource)


def fill_sink(surface_grid, exclude_area=None, out_data=None, out_dataset_name=None, progress=None):
    """
    对 DEM 栅格数据填充伪洼地。
    洼地是指周围栅格都比其高的区域，分为自然洼地和伪洼地。

    \u3000* 自然洼地，是实际存在的洼地，是地表真实形态的反映，如冰川或喀斯特地貌、采矿区、坑洞等，一般远少于伪洼地；
    \u3000* 伪洼地，主要是由数据处理造成的误差、不合适的插值方法导致，在 DEM 栅格数据中很常见。

    在确定流向时，由于洼地高程低于周围栅格的高程，一定区域内的流向都将指向洼地，导致水流在洼地聚集不能流出，引起汇水网络的中断，
    因此，填充洼地通常是进行合理流向计算的前提。

    在填充某处洼地后，有可能产生新的洼地，因此，填充洼地是一个不断重复识别洼地、填充洼地的过程，直至所有洼地被填充且不再产生新
    的洼地。下图为填充洼地的剖面示意图。

    .. image:: ../image/FillSink.png

    该方法可以指定一个点或面数据集，用于指示的真实洼地或需排除的洼地，这些洼地不会被填充。使用准确的该类数据，将获得更为真实的
    无伪洼地地形，使后续分析更为可靠。

    用于指示洼地的数据，如果是点数据集，其中的一个或多个点位于洼地内即可，最理想的情形是点指示该洼地区域的汇水点；如果是面数据
    集，每个面对象应覆盖一个洼地区域。

    可以通过 exclude_area 参数，指定一个点或面数据集，用于指示的真实洼地或需排除的洼地，这些洼地不会被填充。使用准确的该类数据，
    将获得更为真实的无伪洼地地形，使后续分析更为可靠。用于指示洼地的数据，如果是点数据集，其中的一个或多个点位于洼地内即可，最
    理想的情形是点指示该洼地区域的汇水点；如果是面数据集，每个面对象应覆盖一个洼地区域。

    如果 exclude_area 为 None，则会将 DEM 栅格中所有洼地填充，包括伪洼地和真实洼地

    水文分析的相关介绍，请参考 :py:func:`basin`

    :param surface_grid: 指定的要进行填充洼地的 DEM 数据
    :type surface_grid: DatasetGrid or str
    :param exclude_area: 指定的用于指示已知自然洼地或要排除的洼地的点或面数据。如果是点数据集，一个或多个点所在的区域指示为洼地；
                         如果是面数据集，每个面对象对应一个洼地区域。如果为 None，则会将 DEM 栅格中所有洼地填充，包括伪洼地和真实洼地
    :type exclude_area: DatasetVector or str
    :param out_data: 用于存储结果数据集的数据源
    :type out_data: DatasourceConnectionInfo or Datasource or str
    :param str out_dataset_name: 结果数据集的名称。
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 无伪洼地的 DEM 栅格数据集或数据集名称。如果填充伪洼地失败，则返回 None。
    :rtype: DatasetVector or str
    """
    check_lic()
    surface_dt = get_input_dataset(surface_grid)
    if not isinstance(surface_dt, DatasetGrid):
        raise ValueError("source required DatasetGrid, but is " + str(type(surface_grid)))
    else:
        if exclude_area is not None:
            exclude_dt = get_input_dataset(exclude_area)
        else:
            exclude_dt = None
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = surface_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = surface_dt.name + "_sink"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None and safe_start_callback_server():
                try:
                    listener = ProgressListener(progress, "fill_sink")
                    get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.addSteppedListener(listener)
                except Exception as e:
                    try:
                        close_callback_server()
                        log_error(e)
                        listener = None
                    finally:
                        e = None
                        del e

            else:
                fillSink = get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.fillSink
                if exclude_dt is not None:
                    java_result = fillSink(oj(surface_dt), oj(out_datasource), _outDatasetName)
                else:
                    java_result = fillSink(oj(surface_dt), oj(out_datasource), _outDatasetName, exclude_dt)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def flow_accumulation(direction_grid, weight_grid=None, out_data=None, out_dataset_name=None, progress=None):
    """
    根据流向栅格计算累积汇水量。可应用权重数据集计算加权累积汇水量。
    累积汇水量是指流向某个单元格的所有上游单元格的水流累积量，是基于流向数据计算得出的。

    累积汇水量的值可以帮助我们识别河谷和分水岭。单元格的累积汇水量较高，说明该地地势较低，可视为河谷；为0说明该地地势较高，可能为分水岭。因此，累积汇水量是提取流域的各种特征参数（如流域面积、周长、排水密度等）的基础。

    计算累积汇水量的基本思路是：假定栅格数据中的每个单元格处有一个单位的水量，依据水流方向图顺次计算每个单元格所能累积到的水量（不包括当前单元格的水量）。

    下图显示了由水流方向计算累积汇水量的过程。

    .. image:: ../image/FlowAccumulation_1.png

    下图为流向栅格和基于其生成的累积汇水量栅格。

    .. image:: ../image/FlowAccumulation_2.png

    在实际应用中，每个单元格的水量不一定相同，往往需要指定权重数据来获取符合需求的累积汇水量。使用了权重数据后，累积汇水量的计算过程中，每个单元格的水量不再是一个单位，而是乘以权重（权重数据集的栅格值）后的值。例如，将某时期的平均降雨量作为权重数据，计算所得的累积汇水量就是该时期的流经每个单元格的雨量。

    注意，权重栅格必须与流向栅格具有相同的范围和分辨率。

    水文分析的相关介绍，请参考 :py:func:`basin`

    :param direction_grid: 流向栅格数据。
    :type direction_grid: DatasetGrid or str
    :param weight_grid: 权重栅格数据。设置为 None 表示不使用权重数据集。
    :type weight_grid: DatasetGrid or str
    :param out_data: 用于存储结果数据集的数据源
    :type out_data: DatasourceConnectionInfo or Datasource or str
    :param str out_dataset_name: 结果数据集的名称。
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 累积汇水量栅格数据集或数据集名称。如果计算失败，则返回 None。
    :rtype: DatasetVector or str
    """
    direction_dt = get_input_dataset(direction_grid)
    if not isinstance(direction_dt, DatasetGrid):
        raise ValueError("direction_grid required DatasetGrid, but is " + str(type(direction_grid)))
    elif weight_grid is not None:
        weight_dt = get_input_dataset(weight_grid)
        if not isinstance(weight_dt, DatasetGrid):
            raise ValueError("weight_grid required DatasetGrid, but is " + str(type(weight_grid)))
        else:
            weight_dt = None
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = direction_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = direction_dt.name + "_accum"
    else:
        _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "flow_accumulation")
                        get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            flowAccumulation = get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.flowAccumulation
            java_result = flowAccumulation(oj(direction_dt), oj(weight_dt), oj(out_datasource), _outDatasetName)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def flow_direction(surface_grid, force_flow_at_edge, out_data=None, out_dataset_name=None, out_drop_grid_name=None, progress=None):
    """
    对 DEM 栅格数据计算流向。为保证流向计算的正确性，建议使用填充伪洼地之后的 DEM 栅格数据。

    流向，即水文表面水流的方向。计算流向是水文分析的关键步骤之一。水文分析的很多功能需要基于流向栅格，如计算累积汇水量、计算流
    长和流域等。

    SuperMap 使用最大坡降法（D8，Deterministic Eight-node）计算流向。这种方法通过计算单元格的最陡下降方向作为水流的方向。中心
    单元格与相邻单元格的高程差与距离的比值称为高程梯度。最陡下降方向即为中心单元格与高程梯度最大的单元格所构成的方向，也就是中
    心栅格的流向。单元格的流向的值，是通过对其周围的8个邻域栅格进行编码来确定的。如下图所示，若中心单元格的水流方向是左边，则其
    水流方向被赋值16；若流向右边，则赋值1。

    在 SuperMap 中，通过对中心栅格的 8 个邻域栅格编码（如下图所示），中心栅格的水流方向便可由其中的某一值来确定。例如，若中心
    栅格的水流方向是左边，则其水流方向被赋值 16；若流向右边，则赋值 1。

    .. image:: ../image/FlowDirection_1.png

    计算流向时，需要注意栅格边界单元格的处理。位于栅格边界的单元格比较特殊，通过 forceFlowAtEdge 参数可以指定其流向是否向外，
    如果向外，则边界栅格的流向值如下图（左）所示，否则，位于边界上的单元格将赋为无值，如下图（右）所示。

    .. image:: ../image/FlowDirection_2.png

    计算 DEM 数据每个栅格的流向得到流向栅格。下图显示了基于无洼地的 DEM 数据生成的流向栅格。

    .. image:: ../image/FlowDirection_3.png

    水文分析的相关介绍，请参考 :py:func:`basin`

    :param surface_grid: 用于计算流向的 DEM 数据
    :type surface_grid: DatasetGrid or str
    :param bool force_flow_at_edge: 指定是否强制边界的栅格流向为向外。如果为 True，则 DEM 栅格边缘处的所有单元的流向都是从栅格向外流动。
    :param out_data: 用于存储结果数据集的数据源
    :type out_data: DatasourceConnectionInfo or Datasource or str
    :param str out_dataset_name: 结果流向数据集的名称
    :param str out_drop_grid_name: 结果高程梯度栅格数据集名称。可选参数。用于计算流向的中间结果。中心单元格与相邻单元格的高程差与距离的比值称
                                   为高程梯度。如下图所示，为流向计算的一个实例，该实例中生成了高程梯度栅格

                                   .. image:: ../image/FlowDirection.png

    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 返回一个2个元素的tuple，第一个元素为 结果流向栅格数据集或数据集名称，如果设置了结果高程梯度栅格数据集名称，
             则第二个元素为结果高程梯度栅格数据集或数据集名称，否则为 None
    :rtype: tuple[DatasetGrid,DatasetGrid] or tuple[str,str]
    """
    surface_dt = get_input_dataset(surface_grid)
    if not isinstance(surface_dt, DatasetGrid):
        raise ValueError("surface_grid required DatasetGrid, but is " + str(type(surface_grid)))
    else:
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = surface_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = surface_dt.name + "_direct"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None and safe_start_callback_server():
                try:
                    listener = ProgressListener(progress, "flow_direction")
                    get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.addSteppedListener(listener)
                except Exception as e:
                    try:
                        close_callback_server()
                        log_error(e)
                        listener = None
                    finally:
                        e = None
                        del e

            else:
                flowDirection = get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.flowDirection
                if out_drop_grid_name is None:
                    java_result = flowDirection(oj(surface_dt), bool(force_flow_at_edge), oj(out_datasource), _outDatasetName)
                else:
                    java_result = flowDirection(oj(surface_dt), bool(force_flow_at_edge), oj(out_datasource), _outDatasetName, str(out_drop_grid_name))
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is None:
            if out_data is not None:
                try_close_output_datasource(None, out_datasource)
            return
            result_dt = out_datasource[_outDatasetName]
            if out_drop_grid_name is not None:
                drop_dt = out_datasource[str(out_drop_grid_name)]
        else:
            drop_dt = None
        if out_data is not None:
            return try_close_output_datasource((result_dt, drop_dt), out_datasource)
        return (
         result_dt, drop_dt)


def flow_length(direction_grid, up_stream, weight_grid=None, out_data=None, out_dataset_name=None, progress=None):
    """
    根据流向栅格计算流长，即计算每个单元格沿着流向到其流向起始点或终止点之间的距离。可应用权重数据集计算加权流长。

    流长，是指每个单元格沿着流向到其流向起始点或终止点之间的距离，包括上游方向和下游方向的长度。水流长度直接影响地面径流的速度，
    进而影响地面土壤的侵蚀力，因此在水土保持方面具有重要意义，常作为土壤侵蚀、水土流失情况的评价因素。

    流长的计算基于流向数据，流向数据表明水流的方向，该数据集可由流向分析创建；权重数据定义了每个单元格的水流阻力。流长一般用于
    洪水的计算，水流往往会受到诸如坡度、土壤饱和度、植被覆盖等许多因素的阻碍，此时对这些因素建模，需要提供权重数据集。

    流长有两种计算方式：

     * 顺流而下：计算每个单元格沿流向到下游流域汇水点之间的最长距离。
     * 溯流而上：计算每个单元格沿流向到上游分水线顶点的最长距离。

    下图分别为以顺流而下和溯流而上计算得出的流长栅格：

    .. image:: ../image/FlowLength.png

    权重数据定义了每个栅格单元间的水流阻力，应用权重所获得的流长为加权距离（即距离乘以对应权重栅格的值）。例如，将流长分析应用
    于洪水的计算，洪水流往往会受到诸如坡度、土壤饱和度、植被覆盖等许多因素的阻碍，此时对这些因素建模，需要提供权重数据集。

    注意，权重栅格必须与流向栅格具有相同的范围和分辨率。

    水文分析的相关介绍，请参考 :py:func:`basin`

    :param direction_grid: 指定的流向栅格数据。
    :type direction_grid: DatasetGrid or str
    :param bool up_stream: 指定顺流而下计算还是溯流而上计算。True 表示溯流而上，False 表示顺流而下。
    :param weight_grid:  指定的权重栅格数据。设置为 None 表示不使用权重数据集。
    :type weight_grid: DatasetGrid or str
    :param out_data: 用于存储结果数据集的数据源
    :type out_data: DatasourceConnectionInfo or Datasource or str
    :param str out_dataset_name: 结果流长栅格数据集的名称
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 结果流长栅格数据集或数据集名称
    :rtype: DatasetGrid or  str
    """
    direction_dt = get_input_dataset(direction_grid)
    if not isinstance(direction_dt, DatasetGrid):
        raise ValueError("direction_grid required DatasetGrid, but is " + str(type(direction_grid)))
    elif weight_grid is not None:
        weight_dt = get_input_dataset(weight_grid)
        if not isinstance(weight_dt, DatasetGrid):
            raise ValueError("weight_grid required DatasetGrid, but is " + str(type(weight_grid)))
        else:
            weight_dt = None
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = direction_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = direction_dt.name + "_flow"
    else:
        _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "flow_length")
                        get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            flowLength = get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.flowLength
            java_result = flowLength(oj(direction_dt), oj(weight_dt), parse_bool(up_stream), oj(out_datasource), _outDatasetName)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def pour_points(direction_grid, accumulation_grid, area_limit, out_data=None, out_dataset_name=None, progress=None):
    """
    根据流向栅格和累积汇水量栅格生成汇水点栅格。

    汇水点位于流域的边界上，通常为边界上的最低点，流域内的水从汇水点流出，所以汇水点必定具有较高的累积汇水量。根据这一特点，就可以基于累积汇水量和流向栅格来提取汇水点。

    汇水点的确定需要一个累积汇水量阈值，累积汇水量栅格中大于或等于该阈值的位置将作为潜在的汇水点，再依据流向最终确定汇水点的位置。该阈值的确定十分关键，影响着汇水点的数量、位置以及子流域的大小和范围等。合理的阈值，需要考虑流域范围内的土壤特征、坡度特征、气候条件等多方面因素，根据实际研究的需求来确定，因此具有较大难度。

    获得了汇水点栅格后，可以结合流向栅格来进行流域的分割（ :py:func:`watershed` 方法）。

    水文分析的相关介绍，请参考 :py:func:`basin`

    :param direction_grid: 流向栅格数据
    :type direction_grid: DatasetGrid or str
    :param accumulation_grid: 累积汇水量栅格数据
    :type accumulation_grid: DatasetGrid or str
    :param int area_limit: 汇水量限制值
    :param out_data: 用于存储结果数据集的数据源
    :type out_data: DatasourceConnectionInfo or Datasource or str
    :param str out_dataset_name: 结果栅格数据集的名称
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 结果栅格数据集或数据集名称
    :rtype: DatasetGrid or  str
    """
    direction_dt = get_input_dataset(direction_grid)
    if not isinstance(direction_dt, DatasetGrid):
        raise ValueError("direction_grid required DatasetGrid, but is " + str(type(direction_grid)))
    else:
        accumulation_dt = get_input_dataset(accumulation_grid)
        if not isinstance(accumulation_dt, DatasetGrid):
            raise ValueError("accumulation_grid required DatasetGrid, but is " + str(type(accumulation_grid)))
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = direction_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = direction_dt.name + "_pour"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "pour_points")
                        get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            pourPoints = get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.pourPoints
            java_result = pourPoints(oj(direction_dt), oj(accumulation_dt), int(area_limit), oj(out_datasource), _outDatasetName)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def stream_link(stream_grid, direction_grid, out_data=None, out_dataset_name=None, progress=None):
    """
    连接水系，即根据栅格水系和流向栅格为每条河流赋予唯一值。
    连接水系基于栅格水系和流向栅格，为水系中的每条河流分别赋予唯一值，值为整型。连接后的水系网络记录了水系节点的连接信息，体现了
    水系的网络结构。

    如下图所示，连接水系后，每条河段都有唯一的栅格值。图中红色的点为交汇点，即河段与河段相交的位置。河段是河流的一部分，它连接
    两个相邻交汇点，或连接一个交汇点和汇水点，或连接一个交汇点和分水线。因此，连接水系可用于确定流域盆地的汇水点。

    .. image:: ../image/StreamLink_1.png

    下图连接水系的一个实例。

    .. image:: ../image/StreamLink_2.png

    水文分析的相关介绍，请参考 :py:func:`basin`

    :param stream_grid: 栅格水系数据
    :type stream_grid: DatasetGrid or str
    :param direction_grid: 流向栅格数据
    :type direction_grid: DatasetGrid or str
    :param out_data: 用于存储结果数据集的数据源
    :type out_data: DatasourceConnectionInfo or Datasource or str
    :param str out_dataset_name: 结果栅格数据集的名称
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 连接后的栅格水系，为一个栅格数据集。返回结果栅格数据集或数据集名称
    :rtype: DatasetGrid or  str
    """
    direction_dt = get_input_dataset(direction_grid)
    if not isinstance(direction_dt, DatasetGrid):
        raise ValueError("direction_grid required DatasetGrid, but is " + str(type(direction_grid)))
    else:
        stream_dt = get_input_dataset(stream_grid)
        if not isinstance(stream_grid, DatasetGrid):
            raise ValueError("stream_grid required DatasetGrid, but is " + str(type(stream_grid)))
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = direction_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = direction_dt.name + "_stream"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "stream_link")
                        get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            streamLink = get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.streamLink
            java_result = streamLink(oj(stream_dt), oj(direction_dt), oj(out_datasource), _outDatasetName)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def stream_order(stream_grid, direction_grid, order_type, out_data=None, out_dataset_name=None, progress=None):
    """
    对河流进行分级，根据河流等级为栅格水系编号。

    流域中的河流分为干流和支流，在水文学中，根据河流的流量、形态等因素对河流进行分级。在水文分析中，可以从河流的级别推断出河流的某些特征。

    该方法以栅格水系为基础，依据流向栅格对河流分级，结果栅格的值即代表该条河流的等级，值越大，等级越高。SuperMap 提供两种河流
    分级方法：Strahler 法和 Shreve 法。有关这两种方法的介绍请参见 :py:class:`StreamOrderType` 枚举类型。

    如下图所示，是河流分级的一个实例。根据 Shreve 河流分级法，该区域的河流被分为14个等级。

    .. image:: ../image/StreamOrder.png

    水文分析的相关介绍，请参考 :py:func:`basin`

    :param stream_grid: 栅格水系数据
    :type stream_grid: DatasetGrid or str
    :param direction_grid: 流向栅格数据
    :type direction_grid: DatasetGrid or str
    :param order_type: 流域水系编号方法
    :type order_type: StreamOrderType or str
    :param out_data: 用于存储结果数据集的数据源
    :type out_data: DatasourceConnectionInfo or Datasource or str
    :param str out_dataset_name: 结果栅格数据集的名称
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 编号后的栅格流域水系网络，为一个栅格数据集。返回结果数据集或数据集名称。
    :rtype: DatasetGrid or  str
    """
    direction_dt = get_input_dataset(direction_grid)
    if not isinstance(direction_dt, DatasetGrid):
        raise ValueError("direction_grid required DatasetGrid, but is " + str(type(direction_grid)))
    else:
        stream_dt = get_input_dataset(stream_grid)
        if not isinstance(stream_grid, DatasetGrid):
            raise ValueError("stream_grid required DatasetGrid, but is " + str(type(stream_grid)))
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = direction_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = direction_dt.name + "_stream"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "stream_order")
                        get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            stream_order_type = StreamOrderType._make(order_type)
            streamOrder = get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.streamOrder
            java_result = streamOrder(oj(stream_dt), oj(direction_dt), oj(stream_order_type), oj(out_datasource), _outDatasetName)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def stream_to_line(stream_grid, direction_grid, order_type, out_data=None, out_dataset_name=None, progress=None):
    """
    提取矢量水系，即将栅格水系转化为矢量水系。

    提取矢量水系是基于流向栅格，将栅格水系转化为矢量水系（一个矢量线数据集）的过程。得到矢量水系后，就可以进行各种基于矢量的计
    算、处理和空间分析，如构建水系网络。下图为 DEM 数据以及对应的矢量水系。

    .. image:: ../image/StreamToLine.png

    通过该方法获得的矢量水系数据集，保留了河流的等级和流向信息。

     * 在提取矢量水系的同时，系统计算每条河流的等级，并在结果数据集中自动添加一个名为“StreamOrder”的属性字段来存储该值。分级的方式可
       通过 order_type 参数设置。

     * 流向信息存储在结果数据集中名为“Direction”的字段中，以0或1来表示，0表示流向与该线对象的几何方向一致，1表示与线对象的几何
       方向相反。通过该方法获得的矢量水系的流向均与其几何方向相同，即“Direction”字段值都为0。在对矢量水系构建水系网络后，可直接
       使用（或根据实际需要进行修改）该字段作为流向字段。

    水文分析的相关介绍，请参考 :py:func:`basin`

    :param stream_grid: 栅格水系数据
    :type stream_grid: DatasetGrid or str
    :param direction_grid: 流向栅格数据
    :type direction_grid: DatasetGrid or str
    :param order_type: 河流分级方法
    :type order_type: StreamOrderType or str
    :param out_data: 用于存储结果数据集的数据源
    :type out_data: DatasourceConnectionInfo or Datasource or str
    :param str out_dataset_name: 结果矢量水系数据集名称
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 矢量水系数据集或数据集名称
    :rtype: DatasetVector or  str
    """
    direction_dt = get_input_dataset(direction_grid)
    if not isinstance(direction_dt, DatasetGrid):
        raise ValueError("direction_grid required DatasetGrid, but is " + str(type(direction_grid)))
    else:
        stream_dt = get_input_dataset(stream_grid)
        if not isinstance(stream_grid, DatasetGrid):
            raise ValueError("stream_grid required DatasetGrid, but is " + str(type(stream_grid)))
        elif out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = direction_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = direction_dt.name + "_stream"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "stream_to_line")
                        get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            stream_order_type = StreamOrderType._make(order_type)
            streamToLine = get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.streamToLine
            java_result = streamToLine(oj(stream_dt), oj(direction_dt), oj(out_datasource), _outDatasetName, oj(stream_order_type))
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt


def watershed(direction_grid, pour_points_or_grid, out_data=None, out_dataset_name=None, progress=None):
    """

    流域分割，即生成指定汇水点（汇水点栅格数据集）的流域盆地。

    将一个流域划分为若干个子流域的过程称为流域分割。通过 :py:meth:`basin` 方法，可以获取较大的流域，但实际分析中，可能需要将较大的流域划
    分出更小的流域（称为子流域）。

    确定流域的第一步是确定该流域的汇水点，那么，流域分割同样首先要确定子流域的汇水点。与使用 basin 方法计算流域盆地不同，子流
    域的汇水点可以在栅格的边界上，也可能位于栅格的内部。该方法要求输入一个汇水点栅格数据，该数据可通过提取汇水点功能（ :py:meth:`pour_points` 方法）
    获得。此外，还可以使用另一个重载方法，输入表示汇水点的二维点集合来分割流域。

    水文分析的相关介绍，请参考 :py:func:`basin`

    :param direction_grid: 流向栅格数据
    :type direction_grid: DatasetGrid or str
    :param pour_points_or_grid: 汇水点栅格数据或指定的汇水点（二维点列表），汇水点使用地理坐标单位。
    :type pour_points_or_grid: DatasetGrid or str or list[Point2D]
    :param out_data: 用于存储结果数据集的数据源
    :type out_data: DatasourceConnectionInfo or Datasource or str
    :param str out_dataset_name: 结果汇水点的流域盆地栅格数据集名称
    :param progress: 进度信息处理函数，具体参考 :py:class:`.StepEvent`
    :type progress: function
    :return: 汇水点的流域盆地栅格数据集或数据集名称
    :rtype: DatasetGrid or  str
    """
    direction_dt = get_input_dataset(direction_grid)
    if not isinstance(direction_dt, DatasetGrid):
        raise ValueError("direction_grid required DatasetGrid, but is " + str(type(direction_grid)))
    else:
        if isinstance(pour_points_or_grid, (list, tuple)):
            java_pout_points = to_java_point2ds(pour_points_or_grid)
        else:
            java_pout_points = get_input_dataset(pour_points_or_grid)
            if not isinstance(java_pout_points, DatasetGrid):
                raise ValueError("pour_points_or_grid required DatasetGrid, but is " + str(type(pour_points_or_grid)))
            java_pout_points = oj(java_pout_points)
        if out_data is not None:
            out_datasource = get_output_datasource(out_data)
        else:
            out_datasource = direction_dt.datasource
        check_output_datasource(out_datasource)
        if out_dataset_name is None:
            _outDatasetName = direction_dt.name + "_watershed"
        else:
            _outDatasetName = out_dataset_name
    _outDatasetName = out_datasource.get_available_dataset_name(_outDatasetName)
    listener = None
    try:
        try:
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "watershed")
                        get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

            watershed = get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.watershed
            java_result = watershed(oj(direction_dt), java_pout_points, oj(out_datasource), _outDatasetName)
        except:
            import traceback
            log_error(traceback.format_exc())
            java_result = None

    finally:
        if listener is not None:
            try:
                get_jvm().com.supermap.analyst.terrainanalyst.HydrologyAnalyst.removeSteppedListener(listener)
            except Exception as e1:
                try:
                    log_error(e1)
                finally:
                    e1 = None
                    del e1

            close_callback_server()
        elif java_result is not None:
            result_dt = out_datasource[_outDatasetName]
        else:
            result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt

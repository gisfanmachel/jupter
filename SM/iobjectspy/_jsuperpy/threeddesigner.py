# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/_jsuperpy\threeddesigner.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 31532 bytes
from ._gateway import get_jvm, safe_start_callback_server, close_callback_server
from ._logger import *
from ._utils import tuple_to_java_color
from .data import *
from data._jvm import JVMBase
from .data._listener import *
from data._util import get_input_dataset, get_output_datasource, check_output_datasource, try_close_output_datasource, create_result_datasaet
from .data.step import *
from .enums import GeometryType, CursorType, ChamferStyle, Buffer3DJoinType
__all__ = [
 'linear_extrude', 'build_house', 'Material3D', 'compose_models', 'building_height_check', 
 'BoolOperation3D', 
 'ModelBuilder3D', 'ClassificationOperator', 'ClassificationInfos']

def _throw_un_supported():
    raise Exception("Unsupported")


def linear_extrude(input_data, out_data=None, out_dataset_name='Extrude_Result', height=None, twist=0.0, scaleX=1.0, scaleY=1.0, progress=None):
    """
    线性拉伸：将矢量面根据给定高度拉伸为白模模型
    :param input_data: 给定的面数据集
    :param out_data: 输出数据源
    :param out_dataset_name: 输出数据集名字
    :param bLonLat:
    :param height:
    :param twist:
    :param scaleX:
    :param scaleY:
    :return:
    """
    _input = get_input_dataset(input_data)
    _jvm = get_jvm()
    if _input is None:
        raise ValueError("input_data is None")
    if not isinstance(_input, (DatasetVector, Recordset)):
        raise ValueError("input_data required DatasetVector or Recordset, but now is " + str(type(_input)))
    if isinstance(_input, DatasetVector):
        _input = input_data.get_recordset(False, CursorType.STATIC)
    else:
        geoType = _input.get_geometry().type
        isRegion = geoType is GeometryType.GEOREGION
        isRegion3D = geoType is GeometryType.GEOREGION3D
        if not isRegion:
            if not isRegion3D:
                raise ValueError("input data type required GeoRegion or GeoRegion3D")
            elif out_data is not None:
                out_datasource = get_output_datasource(out_data)
                _ds = out_datasource
            else:
                _ds = _input.datasource
            check_output_datasource(_ds)
            if out_dataset_name is None:
                _outDatasetName = "Extrude_Result"
        else:
            _outDatasetName = out_dataset_name
    result_dt = create_result_datasaet(_ds, _outDatasetName, "MODEL")
    if isinstance(_input, DatasetVector):
        result_dt.set_prj_coordsys(_input.prj_coordsys)
    else:
        if isinstance(_input, Recordset):
            result_dt.set_prj_coordsys(_input.dataset.prj_coordsys)
        else:
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ThreeDDesignerProgressListener(progress, "linear_extrude")
                        _jvm.com.supermap.jsuperpy.threeddesigner.ModelBuilder3DTools.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

        result = False
        try:
            try:
                result = _jvm.com.supermap.jsuperpy.threeddesigner.ModelBuilder3DTools.linearExtrude(_input._jobject, result_dt._jobject, height, twist, scaleX, scaleY)
            except Exception as e:
                try:
                    log_error(e)
                    return
                finally:
                    e = None
                    del e

        finally:
            if not result:
                out_datasource.delete(result_dt.name)
                result_dt = None
            if out_data is not None:
                return try_close_output_datasource(result_dt, out_datasource)
            return result_dt


def rotate_extrude(input_data, out_data=None, out_dataset_name='Rotate_Result', angle=None, progress=None):
    """

    :param input_data:
    :param out_data:
    :param out_dataset_name:
    :param angle:
    :return:
    """
    _input = get_input_dataset(input_data)
    _jvm = get_jvm()
    if _input is None:
        raise ValueError("input_data is None")
    if not isinstance(_input, (DatasetVector, Recordset)):
        raise ValueError("input_data required DatasetVector or Recordset, but now is " + str(type(_input)))
    if isinstance(_input, DatasetVector):
        _input = input_data.get_recordset(False, CursorType.STATIC)
    else:
        geoType = _input.get_geometry().type
        isRegion = geoType is GeometryType.GEOREGION
        isRegion3D = geoType is GeometryType.GEOREGION3D
        if not isRegion:
            if not isRegion3D:
                raise ValueError("input data type required GeoRegion or GeoRegion3D")
            elif out_data is not None:
                out_datasource = get_output_datasource(out_data)
                _ds = out_datasource
            else:
                _ds = _input.datasource
            check_output_datasource(_ds)
            if out_dataset_name is None:
                _outDatasetName = "Extrude_Result"
        else:
            _outDatasetName = out_dataset_name
    result_dt = create_result_datasaet(_ds, _outDatasetName, "MODEL")
    if isinstance(_input, DatasetVector):
        result_dt.set_prj_coordsys(_input.prj_coordsys)
    else:
        if isinstance(_input, Recordset):
            result_dt.set_prj_coordsys(_input.dataset.prj_coordsys)
        else:
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ThreeDDesignerProgressListener(progress, "linear_extrude")
                        _jvm.com.supermap.jsuperpy.threeddesigner.ModelBuilder3DTools.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

        result = False
        try:
            try:
                result = _jvm.com.supermap.jsuperpy.threeddesigner.ModelBuilder3DTools.rotateExtrude(_input._jobject, result_dt._jobject, angle)
            except Exception as e:
                try:
                    log_error(e)
                    return
                finally:
                    e = None
                    del e

        finally:
            if not result:
                out_datasource.delete(result_dt.name)
                result_dt = None
            if out_data is not None:
                return try_close_output_datasource(result_dt, out_datasource)
            return result_dt


def build_house(input_data, out_data=None, out_dataset_name='House', wallHeight=0.0, wallMaterial=None, eaveHeight=0.0, eaveWidth=0.0, eaveMaterial=None, roofWidth=0.0, roofSlope=0.0, roofMaterial=None, progress=None):
    """
    构建房屋模型：由多边形构建房屋模型(可构建墙体、挑檐、屋顶)
    :param input_data:指定的源矢量数据集，支持二三维面数据集
    :param out_data:输出数据源
    :param out_dataset_name:输出数据集名称
    :param wallHeight:房屋的墙体高度
    :param wallMaterail:墙体材质参数
    :param eaveHeight:屋檐高度
    :param eaveWidth:屋檐宽度
    :param eaveMaterial:屋檐材质参数
    :param roofWidth:屋顶宽度
    :param roofSlope:屋顶坡度，单位度
    :param roofMaterail:屋顶材质参数
    :param progress:进度事件
    :return:返回模型数据集
    """
    _input = get_input_dataset(input_data)
    _jvm = get_jvm()
    if _input is None:
        raise ValueError("input_data is None")
    if not isinstance(_input, (DatasetVector, Recordset)):
        raise ValueError("input_data required DatasetVector, but now is " + str(type(_input)))
    if isinstance(_input, DatasetVector):
        _input = input_data.get_recordset(False, CursorType.STATIC)
    else:
        geoType = _input.get_geometry().type
        isRegion = geoType is GeometryType.GEOREGION
        isRegion3D = geoType is GeometryType.GEOREGION3D
        if not isRegion:
            if not isRegion3D:
                raise ValueError("input data type required GeoRegion or GeoRegion3D")
            elif out_data is not None:
                out_datasource = get_output_datasource(out_data)
                _ds = out_datasource
            else:
                _ds = _input.datasource
            check_output_datasource(_ds)
            if out_dataset_name is None:
                _outDatasetName = "House_Result"
        else:
            _outDatasetName = out_dataset_name
    result_dt = create_result_datasaet(_ds, _outDatasetName, "MODEL")
    if isinstance(_input, DatasetVector):
        result_dt.set_prj_coordsys(_input.prj_coordsys)
    else:
        if isinstance(_input, Recordset):
            result_dt.set_prj_coordsys(_input.dataset.prj_coordsys)
        else:
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ThreeDDesignerProgressListener(progress, "create_house")
                        _jvm.com.supermap.jsuperpy.threeddesigner.ModelBuilder3DTools.addSteppedListener(listener)
                    except Exception as e:
                        try:
                            close_callback_server()
                            log_error(e)
                            listener = None
                        finally:
                            e = None
                            del e

        result = False
        try:
            try:
                result = _jvm.com.supermap.jsuperpy.threeddesigner.ModelBuilder3DTools.buildHouse(_input._jobject, result_dt._jobject, wallHeight, material3DToJavaObject(wallMaterial), eaveHeight, eaveWidth, material3DToJavaObject(eaveMaterial), roofWidth, roofSlope, material3DToJavaObject(roofMaterial))
            except Exception as e:
                try:
                    log_error(e)
                    return
                finally:
                    e = None
                    del e

        finally:
            if not result:
                out_datasource.delete(result_dt.name)
                result_dt = None
            if out_data is not None:
                return try_close_output_datasource(result_dt, out_datasource)
            return result_dt


class Material3D:
    __doc__ = "\n    材质相关参数设置，主要是颜色，纹理图片和纹理重复模式和重复次数\n    "

    def __init__(self):
        self._color = None
        self._textureFile = None
        self._uTiling = None
        self._vTiling = None
        self._isTextureTimesRepeat = True

    @property
    def color(self):
        return self._color

    def set_color(self, color):
        if not isinstance(color, tuple):
            raise ValueError("value type error, color required tuple type")
        self._color = color

    @property
    def texture_file(self):
        return self._textureFile

    def set_texture_file(self, textureFile):
        self._textureFile = textureFile

    @property
    def uTiling(self):
        return self._uTiling

    def set_uTiling(self, uTiling):
        self._uTiling = uTiling

    @property
    def vTiling(self):
        return self._vTiling

    def set_vTiling(self, vTiling):
        self._vTiling = vTiling

    @property
    def is_texture_times_repeat(self):
        return self._isTextureTimesRepeat

    def set_is_texture_times_repeat(self, b):
        self._isTextureTimesRepeat = b


def material3DToJavaObject(material3D):
    java_obj = None
    if material3D is not None:
        java_obj = get_jvm().com.supermap.jsuperpy.threeddesigner.MaterailParameter()
        if material3D._color is not None:
            java_obj.setMaterialColor(tuple_to_java_color(material3D._color))
        if material3D._textureFile is not None:
            java_obj.setTextureFile(material3D._textureFile)
        if material3D._uTiling is not None:
            java_obj.setUTiling(float(material3D._uTiling))
        if material3D._vTiling is not None:
            java_obj.setVTiling(float(material3D._vTiling))
        if material3D._isTextureTimesRepeat:
            java_obj.setRealWorldMapSize(False)
            java_obj.setRealTexMapSize(False)
        else:
            java_obj.setRealWorldMapSize(True)
            java_obj.setRealTexMapSize(True)
    return java_obj


class ThreeDDesignerProgressListener(PythonListenerBase):
    __doc__ = "\n    进度事件，在中间层封装的，不是data的StepEvent，故再封装一个\n    目前只支持进度信息，不支持取消\n    "

    def __init__(self, progress_fun, name):
        self._stepped = StepEvent()
        PythonListenerBase.__init__(self, "Progress:" + name, progress_fun)

    def stepped(self, event):
        if self.func is not None:
            self._stepped._title = event.getTitle()
            self._stepped._message = event.getMessage()
            self._stepped._percent = event.getPercent()
            self.func(self._stepped)

    class Java:
        implements = [
         "com.supermap.jsuperpy.threeddesigner.SteppedListener"]


def compose_models(value):
    if value is None:
        return
    if len(value) < 2:
        raise ValueError("require more than one models")
    _jvm = get_jvm()
    j_geometrys = []
    for m in value:
        j_geometrys.append(m._jobject)

    result = _jvm.com.supermap.realspace.threeddesigner.ModelTools.compose(j_geometrys)
    if result is not None:
        result = GeoModel3D._from_java_object(result)
    return result


def building_height_check(input_data=None, height=0.0):
    """
    规划控高检查
    :param input_data:建筑模型记录集或者数据集
    :param height:限制高度
    :return:返回超高建筑ID
    """
    _input = get_input_dataset(input_data)
    _jvm = get_jvm()
    if _input is None:
        raise ValueError("input_data is None")
    if not isinstance(_input, (DatasetVector, Recordset)):
        raise ValueError("input_data required DatasetVector, but now is " + str(type(_input)))
    if isinstance(_input, DatasetVector):
        _input = input_data.get_recordset(False, CursorType.STATIC)
    if height < 0.0:
        raise ValueError("height should greater than 0")
    result = []
    while _input.has_next():
        geometry = _input.get_geometry()
        if geometry.max_z > height:
            result.append(_input.get_id())
        _input.move_next()

    _input.close()
    return result


class BoolOperation3D(JVMBase):

    def __init__(self):
        JVMBase.__init__(self)

    def check(geometry3d):
        """
        对模型对象进行检查是否满足布尔运算条件
        :param geometry3d:
        :return:
        """
        if geometry3d._jobject is None:
            raise ObjectDisposedError(type(geometry3d).__name__)
        return get_jvm().com.supermap.realspace.threeddesigner.BooleanOperator3D.check(geometry3d._jobject)

    def erase(geometry3d, erase_geomety3d):
        """
        两个指定三维几何对象的差运算
        :param geometry3d:
        :param erase_geomety3d:
        :return: 返回差集Geometry3D对象
        """
        if geometry3d._jobject is None:
            raise ObjectDisposedError(type(geometry3d).__name__)
        if erase_geomety3d._jobject is None:
            raise ObjectDisposedError(type(erase_geomety3d).__name__)
        geo = get_jvm().com.supermap.realspace.threeddesigner.BooleanOperator3D.erase(geometry3d._jobject, erase_geomety3d._jobject)
        if geo != None:
            geo = GeoModel3D._from_java_object(geo)
        return geo

    def union(geometry3d, union_geomety3d):
        """
        两个指定三维几何对象的并集
        :param geometry3d:
        :param union_geomety3d:
        :return: 返回并集Geometry3D对象
        """
        if geometry3d._jobject is None:
            raise ObjectDisposedError(type(geometry3d).__name__)
        if union_geomety3d._jobject is None:
            raise ObjectDisposedError(type(union_geomety3d).__name__)
        geo = get_jvm().com.supermap.realspace.threeddesigner.BooleanOperator3D.union(geometry3d._jobject, union_geomety3d._jobject)
        if geo != None:
            geo = GeoModel3D._from_java_object(geo)
        return geo

    def intersect(geometry3d, intersect_geomety3d):
        """
        两个指定三维几何对象的交集
        :param geometry3d:
        :param geomety3d:
        :return: 返回交集Geometry3D对象
        """
        if geometry3d._jobject is None:
            raise ObjectDisposedError(type(geometry3d).__name__)
        if intersect_geomety3d._jobject is None:
            raise ObjectDisposedError(type(intersect_geomety3d).__name__)
        geo = get_jvm().com.supermap.realspace.threeddesigner.BooleanOperator3D.intersect(geometry3d._jobject, intersect_geomety3d._jobject)
        if geo != None:
            geo = GeoModel3D._from_java_object(geo)
        return geo

    def isClosed(geometry3d):
        """
        检查Geometry3D对象是否闭合
        :param geometry3d:
        :return: true表示闭合，false表示不闭合
        """
        if geometry3d._jobject is None:
            raise ObjectDisposedError(type(geometry3d).__name__)
        return get_jvm().com.supermap.realspace.threeddesigner.BooleanOperator3D.isClosed(geometry3d._jobject)


class ModelBuilder3D(JVMBase):

    def linear_extrude(self, geometry, bLonLat, height):
        """
        线性拉伸
        该方法仅在 Windows 平台版本中支持，在 Linux版本中不提供
        :param geometry:待进行线性拉伸的面
        :param bLonLat:是否是经纬度
        :param height:拉伸高度
        :param twist:旋转角度
        :param scaleX:绕X轴方向缩放
        :param scaleY:绕Y轴方向缩放
        :param material:贴图设置
        :return:返回GeoModel3D对象
        """
        if geometry is None:
            raise ObjectDisposedError(type(geometry).__name__)
        linearExtrudeP = get_jvm().com.supermap.realspace.threeddesigner.LinearExtrudeParameter()
        linearExtrudeP.setHeight(float(height))
        textureP = get_jvm().com.supermap.realspace.threeddesigner.TextureMapParameter()
        result = get_jvm().com.supermap.realspace.threeddesigner.ModelBuilder3D.linearExtrude(geometry._jobject, bLonLat, linearExtrudeP, textureP)
        if result is not None:
            result = Geometry._from_java_object(result)
        return result

    def rotate_extrude(geometry, angle, slices, isgroup=False, hasStartFace=True, hasRingFace=True, hasEndFace=True):
        """
        旋转拉伸 该方法仅在 Windows 平台版本中支持，在 Linux版本中不提供
        :param geometry: 面对象（必须在平面坐标系下构建）
        :param angle:旋转角度
        :param slices:切分次数
        :param isgroup:是否拆分成多个对象
        :param hasStartFace:是否需要起始面
        :param hasRingFace:是否需要环
        :param hasEndFace:是否需要终止面
        :return: 返回GeoModel3D对象
        """
        if geometry is None:
            raise ObjectDisposedError(type(geometry).__name__)
        if not isinstance(geometry, (GeoLine, GeoRegion)):
            raise TypeError("require type GeoLine or GeoRegion")
        if slices <= 0:
            raise ValueError("slices should greater than 0")
        rotateExtrudeP = get_jvm().com.supermap.realspace.threeddesigner.RotateExtrudeParameter()
        rotateExtrudeP.setAngle(float(angle))
        rotateExtrudeP.setSlices(int(slices))
        rotateExtrudeP.setGroup(bool(isgroup))
        rotateExtrudeP.setStartFace(bool(hasStartFace))
        rotateExtrudeP.setRingFace(bool(hasRingFace))
        rotateExtrudeP.setEndFace(bool(hasEndFace))
        result = get_jvm().com.supermap.realspace.threeddesigner.ModelBuilder3D.rotateExtrude(geometry._jobject, rotateExtrudeP)
        if result is not None:
            result = GeoModel3D._from_java_object(result)
        return result

    def loft(geometry, line3D, bLonLat=False, nChamfer=50, chamferStyle=ChamferStyle.SOBC_CIRCLE_ARC):
        """
        放样,该方法仅在 Windows 平台版本中支持，在 Linux版本中不提供
        :param geometry:放样的横截面,
        支持二维对象：GeoLine,GeoLineEPS,GeoCirCle,GeoRegion,GeoRegionEPS,GeoEllipse,GeoRect
        支持三维对象：GeoLine3D,GeoCircle3D,GeoRegion3D
        :param line3D:待放样的线对象
        :param bLonLat:是否是经纬度
        :param nChamfer:平滑程度
        :param chamferStyle: 倒角样式
        :param material:贴图设置
        :return:返回GeoModel3D对象
        """
        if geometry is None:
            raise ObjectDisposedError(type(geometry).__name__)
        if not isinstance(line3D, GeoLine3D):
            raise TypeError("require type GeoLine3D")
        result = get_jvm().com.supermap.realspace.threeddesigner.ModelBuilder3D.loft(geometry._jobject, line3D._jobject, bLonLat, int(nChamfer), chamferStyle._jobject)
        if result is not None:
            result = Geometry._from_java_object(result)
        return result

    def section_projection(geomodel3d, plane=None):
        """
        截面投影,在 Linux版本中不提供
        :param geometry:待进行截面投影的三维几何模型对象
        :param plane:投影平面
        :return:返回投影面
        """
        if geomodel3d is None:
            raise ObjectDisposedError(type(geomodel3d).__name__)
        elif not isinstance(geomodel3d, GeoModel3D):
            raise TypeError("require type GeoModel3D")
        result = None
        if plane is None:
            result = get_jvm().com.supermap.realspace.threeddesigner.ModelBuilder3D.sectionProjection(geomodel3d._jobject)
        else:
            result = get_jvm().com.supermap.realspace.threeddesigner.ModelBuilder3D.sectionProjection(geomodel3d._jobject, plane._jobject)
        if result is not None:
            result = Geometry._from_java_object(result)
        return result

    def plane_projection(geomodel3d, plane=None):
        """
        平面投影,在 Linux版本中不提供
        :param geomodel3d:待进行截面投影的三维几何模型对象
        :param plane:投影平面
        :return:返回投影面
        """
        if geomodel3d is None:
            raise ObjectDisposedError(type(geomodel3d).__name__)
        elif not isinstance(geomodel3d, GeoModel3D):
            raise TypeError("require type GeoModel3D")
        result = None
        if plane is None:
            result = get_jvm().com.supermap.realspace.threeddesigner.ModelBuilder3D.planeProjection(geomodel3d._jobject)
        else:
            result = get_jvm().com.supermap.realspace.threeddesigner.ModelBuilder3D.planeProjection(geomodel3d._jobject, plane._jobject)
        if result is not None:
            result = Geometry._from_java_object(result)
        return result

    def create_buffer(geometry, offset, bLonLat=False, joinType=Buffer3DJoinType.ROUND):
        """
        三维缓冲，支持线、面缓冲（拓展）成面；模型缓冲（拓展）成三维实体模型
        :param geometry:线、面及模型对象
        :param offset:缓冲距离
        :param bLonLat:是否是经纬度
        :param joinType:衔接样式，包括尖角、圆角、斜角。
         三维线缓冲成面支持尖角衔接样式，缓冲成体支持尖角和圆角衔接样式。
         三维面仅支持缓冲成三维面，衔接样式包括尖角和圆角衔接样式。
         实体模型仅支持缓存成体，无衔接样式
        :return:
        """
        if geometry is None:
            raise ObjectDisposedError(type(geometry).__name__)
        bufferP = get_jvm().com.supermap.realspace.threeddesigner.BufferParameter()
        bufferP.setOffset(float(offset))
        bufferP.setType(joinType._jobject)
        result = get_jvm().com.supermap.realspace.threeddesigner.ModelBuilder3D.createBuffer(geometry._jobject, bLonLat, bufferP)
        if result is not None:
            result = Geometry._from_java_object(result)
        return result

    def straight_skeleton(geometry, dAngle, bLonLat=False):
        """
        直骨架生成
        :param geometry:待直骨架的面对象
        :param bLonLat:是否是经纬度
        :param dAngle:拆分的角度阈值
        :return:成功返回三维模型
        """
        if geometry is None:
            raise ObjectDisposedError(type(geometry).__name__)
        result = get_jvm().com.supermap.realspace.threeddesigner.ModelBuilder3D.straightSkeleton(geometry._jobject, bLonLat, float(dAngle))
        if result is not None:
            result = Geometry._from_java_object(result)
        return result

    def mirror(geomodel3d, plane=None):
        """
        :获取geomodel3d关于plane镜像的模型对象
        :param plane:镜像面
        :return:返回geomodel3d关于plane镜像的模型对象
        """
        if geomodel3d is None:
            raise ObjectDisposedError(type(geomodel3d).__name__)
        elif not isinstance(geomodel3d, GeoModel3D):
            raise TypeError("require type GeoModel3D")
        result = None
        if plane is None:
            result = geomodel3d._jobject
        else:
            result = get_jvm().com.supermap.realspace.threeddesigner.ModelBuilder3D.Mirror(geomodel3d._jobject, plane._jobject)
        if result is not None:
            result = GeoModel3D._from_java_object(result)


class ClassificationInfos(JVMBase):
    __doc__ = "\n    com.supermap.data.processing.ClassificationInfos 的python对象映射\n    单体化倾斜摄影数据OSGB，S3M的导出对象\n    "

    def __init__(self):
        JVMBase.__init__(self)

    @staticmethod
    def _from_java_object(j_classificationInfos):
        if j_classificationInfos is None:
            return
        ci = ClassificationInfos()
        ci._java_object = j_classificationInfos
        return ci

    @property
    def vertices(self):
        """
        顶点列表
        :return: list 顶点列表
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        result = self._jobject.getArrVertices()
        if result:
            return list(result)

    @property
    def normals(self):
        """
        法线列表
        :return: list 法线列表
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        result = self._jobject.getArrNormals()
        if result:
            return list(result)

    @property
    def labels(self):
        """
        标签列表
        :return: list标签列表
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        result = self._jobject.getArrLabels()
        if result:
            return list(result)


class ClassificationOperator(JVMBase):

    def extract_infos(osgbFilePath):
        """
        导入OSGB倾斜摄影数据，得到该数据的顶点、法线以及标签信息
        :param osgbFilePath:原始倾斜摄影切片OSGB数据
        """
        if osgbFilePath is None:
            raise ObjectDisposedError(type(osgbFilePath).__name__)
        j_object = get_jvm().com.supermap.data.processing.ClassificationOperator.extractInfos(osgbFilePath)
        return ClassificationInfos._from_java_object(j_object)

    def generate_training_set(diecretFilePath):
        """
        导入S3M单体化数据，得到该数据的顶点、法线以及标签信息
        :param diecretFilePath:单体化S3M数据
        """
        if diecretFilePath is None:
            raise ObjectDisposedError(type(diecretFilePath).__name__)
        j_object = get_jvm().com.supermap.data.processing.ClassificationOperator.generateTrainingSet(diecretFilePath)
        return ClassificationInfos._from_java_object(j_object)

    def add_labels_to_S3M_file(osgbFilePath, outputFolder, labelsArray):
        """
        导入OSGB倾斜摄影数据，利用标签数组生成S3M数据，并保存到outputFolder中
        :param osgbFilePath:OSGB倾斜摄影数据
        :param outputFolder:结果保存路径
        :param labelsArray:标签数组
        """
        if osgbFilePath is None:
            raise ObjectDisposedError(type(osgbFilePath).__name__)
        if outputFolder is None:
            raise ObjectDisposedError(type(outputFolder).__name__)
        if labelsArray is None:
            raise ObjectDisposedError(type(labelsArray).__name__)
        from ._utils import to_java_int_array
        return get_jvm().com.supermap.data.processing.ClassificationOperator.addLabelsToS3MFile(osgbFilePath, outputFolder, to_java_int_array(labelsArray))

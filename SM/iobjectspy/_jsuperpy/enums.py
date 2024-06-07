# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/_jsuperpy\enums.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 228243 bytes
from enum import IntEnum, unique
from ._gateway import get_jvm
from ._logger import log_error
__all__ = ['JEnum', 'PixelFormat', 'BlockSizeOption', 'AreaUnit', 'Unit', 'EngineType', 
 'DatasetType', 'FieldType', 
 'GeometryType', 'WorkspaceType', 'WorkspaceVersion', 
 'EncodeType', 'CursorType', 'Charset', 
 'OverlayMode', 'SpatialIndexType', 
 'DissolveType', 'TextAlignment', 
 'StringAlignment', 'ColorGradientType', 
 'SpatialQueryMode', 
 'StatisticsType', 'JoinType', 'BufferEndType', 'BufferRadiusUnit', 
 'StatisticMode', 
 'PrjCoordSysType', 'ImportMode', 'IgnoreMode', 'MultiBandImportMode', 
 'CADVersion', 
 'TopologyRule', 'GeoSpatialRefType', 'GeoCoordSysType', 'ProjectionType', 
 'GeoPrimeMeridianType', 
 'GeoSpheroidType', 'GeoDatumType', 'CoordSysTransMethod', 'StatisticsFieldType', 
 'VectorResampleType', 
 'ArcAndVertexFilterMode', 'RasterResampleMode', 'ResamplingMethod', 
 'AggregationType', 
 'ReclassPixelFormat', 'ReclassSegmentType', 'ReclassType', 'NeighbourShapeType', 
 'SearchMode', 
 'Exponent', 'VariogramMode', 'ComputeType', 'SmoothMethod', 'ShadowMode', 
 'SlopeType', 
 'NeighbourUnitType', 'InterpolationAlgorithmType', 'GriddingLevel', 
 'RegionToPointMode', 
 'LineToPointMode', 'EllipseSize', 'SpatialStatisticsType', 
 'DistanceMethod', 'KernelFunction', 'KernelType', 
 'BandWidthType', 'AggregationMethod', 
 'StreamOrderType', 'TerrainInterpolateType', 
 'TerrainStatisticType', 'EdgeMatchMode', 
 'FunctionType', 'StatisticsCompareType', 'GridStatisticsMode', 
 'ConceptualizationModel', 
 'AttributeStatisticsMode', 'VCTVersion', 'RasterJoinPixelFormat', 'RasterJoinType', 
 'PlaneType', 
 'ChamferStyle', 'Buffer3DJoinType', 'ViewShedType', 'ImageType', 'FillGradientMode', 
 'ColorSpaceType', 
 'ImageInterpolationMode', 'ImageDisplayMode', 'MapColorMode', 'LayerGridAggregationType', 
 'NeighbourNumber', 
 'MajorityDefinition', 'BoundaryCleanSortType', 'OverlayAnalystOutputType', 
 'FieldSign', 
 'PyramidResampleType']

class JEnum(IntEnum):
    __doc__ = "枚举值类型，提供根据名称和枚举值构造枚举项的接口。"
    __repr__ = IntEnum.__str__

    @property
    def _jobject(self):
        return self._to_java_enum_type()

    def _to_java_enum_type(self):
        jvm = get_jvm()
        java_class_full_name = self._get_java_class_type()
        if java_class_full_name is not None:
            try:
                if isinstance(self.value, IntEnum):
                    _value = self.value.value
                else:
                    _value = self.value
                cls = jvm.Class.forName(java_class_full_name)
                super_class_name = cls.getSuperclass().getName()
                if super_class_name == "com.supermap.data.Enum":
                    return jvm.com.supermap.data.Enum.parse(cls, _value)
                if super_class_name == "java.lang.Enum":
                    for item in cls.getEnumConstants():
                        if self.name.lower() == item.name().lower():
                            return item

                    return
                raise ValueError("invalid class type" + java_class_full_name)
            except:
                raise ValueError("invalid class type" + java_class_full_name)

        else:
            return

    @classmethod
    def _make(cls, value, default=None):
        """
        根据名称或枚举值构造具体的枚举项。枚举名称不区分大小写

        :param value: 枚举名称或值
        :type value: int\u3000or str
        :param default: 默认的枚举值。当设置的枚举名称或值不合法无法正常构造一个有效的枚举项时，将使用默认值。
        :type default: int or str
        :return: 返回对应的枚举项
        """
        try:
            if isinstance(value, str):
                all_names = cls._names()
                for t in all_names:
                    if value.upper() == t.upper():
                        return cls[t]

                exts = cls._externals()
                for t in exts.keys():
                    if value.upper() == t.upper():
                        return exts[t]

            else:
                if isinstance(value, cls):
                    return value
                    if isinstance(value, int):
                        for item in cls:
                            if item.value == value:
                                return item

                elif default is not None:
                    return cls._make(default)
                return
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

        if default is not None:
            return cls._make(default)
        return

    @classmethod
    def _values(cls):
        """
        返回当前枚举类所有的枚举值

        :rtype: list
        """
        return list(cls._member_map_.values())

    @classmethod
    def _names(cls):
        """
        返回当前枚举类所有的枚举名称

        :rtype:  list[str]:
        """
        return list(cls._member_map_.keys())

    @classmethod
    def _externals(cls):
        return {}


@unique
class CursorType(JEnum):
    __doc__ = "\n    游标类型：\n\n    :var CursorType.DYNAMIC: 动态游标类型。支持各种编辑操作，速度慢。动态游标含义：可以看见其他用户所作的添加、更改和删除。允许在记录集中进行前后移动, (但不包括\n      数据提供者不支持的书签操作，书签操作主要针对于 ADO 而言)。此类型的游标功能很强大，但同时也是耗费系统资源最多的游标。动态游标可以知道记录\n      集（Recordset）的所有变化。使用动态游标的用户可以看到其他用户对数据集所做的编辑、增加、删除等操作。如果数据提供者允许这种类型的游标，那么它\n      是通过每隔一段时间从数据源重取数据来动态刷新查询的记录集的。毫无疑问这会需要很多的资源。\n\n    :var CursorType.STATIC: 静态游标类型。静态游标含义：可以用来查找数据或生成报告的记录集合的静态副本。另外，对其他用户所作的添加、更改或删除不可见。静态游标只\n      是数据的一幅快照。也就是说，它无法看到自从被创建以后其他用户对记录集（Recordset）所做的编辑操作。\n      采用这类游标你可以向前和向后回溯。由于其功能简单，资源的耗费比动态游标（DYNAMIC）要小！）\n    "
    DYNAMIC = 2
    STATIC = 3

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.CursorType"


@unique
class BlockSizeOption(JEnum):
    __doc__ = "\n    该枚举定义了像素分块的类型常量。用于栅格数据集或影像数据:\n\n    :var BlockSizeOption.BS_64: 表示64像素*64像素的分块\n    :var BlockSizeOption.BS_128: 表示128像素*128像素的分块\n    :var BlockSizeOption.BS_256: 表示256像素*256像素的分块\n    :var BlockSizeOption.BS_512: 表示512像素*512像素的分块。\n    :var BlockSizeOption.BS_1024: 表示1024像素*1024像素的分块。\n\n    "
    BS_64 = 64
    BS_128 = 128
    BS_256 = 256
    BS_512 = 512
    BS_1024 = 1024

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.BlockSizeOption"


@unique
class AreaUnit(JEnum):
    __doc__ = "面积单位类型:\n\n    :var AreaUnit.SQUAREMILLIMETER: 公制单位，平方毫米。\n    :var AreaUnit.SQUARECENTIMETER: 公制单位，平方厘米。\n    :var AreaUnit.SQUAREDECIMETER: 公制单位，平方分米。\n    :var AreaUnit.SQUAREMETER: 公制单位，平方米。\n    :var AreaUnit.SQUAREKILOMETER: 公制单位，平方千米。\n    :var AreaUnit.HECTARE: 公制单位，公顷。\n    :var AreaUnit.ARE: 公制单位，公亩。\n    :var AreaUnit.QING: 市制单位，顷。\n    :var AreaUnit.MU: 市制单位，亩。\n    :var AreaUnit.SQUAREINCH: 英制单位，平方英寸。\n    :var AreaUnit.SQUAREFOOT: 英制单位，平方尺。\n    :var AreaUnit.SQUAREYARD: 英制单位，平方码。\n    :var AreaUnit.SQUAREMILE: 英制单位，平方英里。\n    :var AreaUnit.ACRE: 英制单位，英亩。\n    "
    SQUAREMILLIMETER = 1
    SQUARECENTIMETER = 2
    SQUAREDECIMETER = 3
    SQUAREMETER = 4
    SQUAREKILOMETER = 5
    HECTARE = 6
    ARE = 7
    QING = 8
    MU = 9
    SQUAREINCH = 10
    SQUAREFOOT = 11
    SQUAREYARD = 12
    SQUAREMILE = 13
    ACRE = 14

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.AreaUnit"


@unique
class EngineType(JEnum):
    __doc__ = "\n    该类定义了空间数据库引擎类型常量。\n    空间数据库引擎是在常规数据库管理系统之上的，除具备常规数据库管理系统所必备的功能之外，还提供特定的针对空间数据的存储和管理能力。\n    SuperMap SDX+ 是 supermap 的空间数据库技术，也是 SuperMap GIS 软件数据模型的重要组成部分。各种空间几何对象和影像数据都可以通过 SDX+\n    引擎，存放到关系型数据库中，形成空间数据和属性数据一体化的空间数据库\n\n    :var EngineType.IMAGEPLUGINS: 影像只读引擎类型，对应的枚举值为 5。针对通用影像格式如 BMP，JPG，TIFF 以及超图自定义影像格式 SIT，二维地图缓存配置文件格式SCI等。用户在进行二维地图缓存加载的时候，需要设置为此引擎类型，另外还需要使用 :py:meth:`DatasourceConnectionInfo.set_server` 方法，将参数设置为二维地图缓存配置文件（SCI）。对于MrSID和ECW，只读打开为了快速原则，以合成波段的方式打开，非灰度数据会默认为RGB或者RGBA的方式显示，灰度数据按原始方式显示。\n    :var EngineType.ORACLEPLUS:  Oracle 引擎类型\n    :var EngineType.SQLPLUS: SQL Server 引擎类型，仅在 Windows 平台版本中支持\n    :var EngineType.DB2: DB2 引擎类型\n    :var EngineType.KINGBASE:  Kingbase 引擎类型，针对 Kingbase 数据源，不支持多波段数据\n    :var EngineType.MEMORY:  内存数据源。\n    :var EngineType.OGC: OGC 引擎类型，针对于 Web 数据源，对应的枚举值为 23。目前支持的类型有 WMS，WFS，WCS 和 WMTS。WMTS服务中默认BoundingBox和TopLeftCorner标签读取方式为(经度,纬度)。而一部分服务提供商提供的坐标格式为(纬度,经度)，当你遇到这个情况时，为了保证坐标数据读取的正确性，请对SuperMap.xml文件（该文件位于Bin目录下）中相应的内容进行正确的修改。通常出现该情况的表现是本地矢量数据与发布的WMTS服务数据无法叠加到一起。\n    :var EngineType.MYSQL:  MYSQL 引擎类型，支持 MySQL 5.6.16以上版本\n    :var EngineType.MONGODB:  MongoDB 引擎类型,目前支持的认证方式为Mongodb-cr\n    :var EngineType.BEYONDB:  BeyonDB 引擎类型\n    :var EngineType.GBASE:  GBase 引擎类型\n    :var EngineType.HIGHGODB:  HighGoDB 引擎类型\n    :var EngineType.UDB: UDB 引擎类型\n    :var EngineType.POSTGRESQL: PostgreSQL 引擎类型\n    :var EngineType.GOOGLEMAPS: GoogleMaps 引擎类型，该引擎为只读引擎，且不能创建。该常量仅在 Windows 32 位平台版本中支持，在 Linux版本中不提供\n    :var EngineType.SUPERMAPCLOUD: 超图云服务引擎类型，该引擎为只读引擎，且不能创建。该常量仅在 Windows 32 位平台版本中支持，在 Linux版本中不提供。\n    :var EngineType.ISERVERREST: REST 地图服务引擎类型，该引擎为只读引擎，且不能创建。针对基于 REST 协议发布的地图服务。该常量仅在 Windows 32 位平台版本中支持，在 Linux版本中不提供。\n    :var EngineType.BAIDUMAPS: 百度地图服务引擎类型\n    :var EngineType.BINGMAPS: 必应地图服务引擎类型\n    :var EngineType.OPENSTREETMAPS: OpenStreetMap 引擎类型。该常量仅在 Windows 32 位平台版本中支持，在 Linux版本中不提供\n    :var EngineType.SCV: 矢量缓存引擎类型\n    :var EngineType.DM: 第三代DM引擎类型\n    :var EngineType.ORACLESPATIAL: Oracle Spatial 引擎类型\n    :var EngineType.SDE: ArcSDE 引擎类型:\n\n                         - 支持ArcSDE 9.2.0 及以上版本\n                         - 支持ArcSDE 9.2.0 及以上版本的点、线、面、文本和栅格数据集5种数据类型的读取，不支持写。\n                         - 不支持读取ArcSDE文本的风格，ArcSDE默认存放文本的字段“TEXTSTRING”不能删，否则我们读取不到文本。\n                         - 不支持ArcSDE 2bit位深的栅格的读取，其它位深均支持，并可拉伸显示。\n                         - 不支持多线程。\n                         - 使用SDE引擎，需要ArcInfo的许可，并把ArcSDE安装目录bin下的 sde.dll 、sg.dll 和 pe.dll这三个dll拷贝到SuperMap产品下的Bin目录（即SuSDECI.dll 和 SuEngineSDE.sdx 同级目录）\n                         - 支持平台：Windows 32位 ,Windows 64位。\n\n    :var EngineType.ALTIBASE: Altibase 引擎类型\n    :var EngineType.KDB: KDB 引擎类型\n    :var EngineType.SRDB: 上容关系数据库引擎类型\n    :var EngineType.MYSQLPlus: MySQLPlus数据库引擎类型，实质上为MySQL+Mongo\n    :var EngineType.VECTORFILE: 矢量文件引擎类型。针对通用矢量格式如 shp，tab，Acad等,支持矢量文件的编辑和保存,如果是FME支持的类型则需要对应的FME许可,目前没有FME许可不支持FileGDBVector格式。\n    :var EngineType.PGGIS: PostgreSQL的空间数据扩展PostGIS 引擎类型\n    :var EngineType.ES: Elasticsearch 引擎类型\n    :var EngineType.SQLSPATIAL: SQLSpatial 引擎类型\n    :var EngineType.UDBX: UDBX 引擎类型\n    "
    IMAGEPLUGINS = 5
    ORACLEPLUS = 12
    SQLPLUS = 16
    DB2 = 18
    KINGBASE = 19
    MEMORY = 20
    OGC = 23
    MYSQL = 32
    MONGODB = 401
    BEYONDB = 2001
    GBASE = 2002
    HIGHGODB = 2003
    UDB = 219
    POSTGRESQL = 221
    GOOGLEMAPS = 223
    SUPERMAPCLOUD = 224
    ISERVERREST = 225
    BAIDUMAPS = 227
    BINGMAPS = 230
    OPENSTREETMAPS = 228
    SCV = 229
    DM = 17
    ORACLESPATIAL = 10
    SDE = 4
    ALTIBASE = 2004
    KDB = 2005
    SRDB = 2006
    MYSQLPlus = 2007
    VECTORFILE = 101
    PGGIS = 2012
    ES = 2011
    SQLSPATIAL = 2013
    UDBX = 2054

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.EngineType"


@unique
class DatasetType(JEnum):
    __doc__ = "\n    该类定义了数据集类型常量。数据集一般为存储在一起的相关数据的集合；根据数据类型的不同，分为矢量数据集、栅格数据集和影像数据集，以及为了处理特定问题而设计的如拓扑数据集，网络\n    数据集等。根据要素的空间特征的不同，矢量数据集又分为点数据集，线数据集，面数据集，复合数据集，文本数据集，纯属性数据集等。\n\n    :var DatasetType.UNKNOWN: 未知类型数据集\n    :var DatasetType.TABULAR: 纯属性数据集。用于存储和管理纯属性数据，纯属性数据用来描述地形地物特征、形状等信息，如河流的长度、宽度等。该数据\n                              集没有空间图形数据。即纯属性数据集不能作为图层被添加到地图窗口中显示。\n    :var DatasetType.POINT: 点数据集。用于存储点对象的数据集类，例如离散点的分布。\n    :var DatasetType.LINE: 线数据集。用于存储线对象的数据集，例如河流、道路、国家边界线的分布。\n    :var DatasetType.REGION: 多边形数据集。用于存储面对象的数据集，例如表示房屋的分布、行政区域等。\n    :var DatasetType.TEXT: 文本数据集。用于存储文本对象的数据集，那么文本数据集中只能存储文本对象，而不能存储其他几何对象。例如表示注记的文本对象。\n    :var DatasetType.CAD: 复合数据集。指可以存储多种几何对象的数据集，即用来存储点、线、面、文本等不同类型的对象的集合。CAD 数据集中各对象可以\n                          有不同的风格，CAD 数据集为每个对象存储风格。\n    :var DatasetType.LINKTABLE: 数据库表。即外挂属性表，不包含系统字段（以 SM 开头的字段）。与一般的属性数据集一样使用，但该数据集只具有只读功能。\n    :var DatasetType.NETWORK: 网络数据集。网络数据集是用于存储具有网络拓扑关系的数据集。如道路交通网络等。网络数据集和点数据集、线数据集不同，\n                              它既包含了网络线对象，也包含了网络结点对象，还包含了两种对象之间的空间拓扑关系。基于网络数据集，可以进行路径分析、\n                              服务区分析、最近设施查找、选址分区、公交换乘以及邻接点、通达点分析等多种网络分析。\n    :var DatasetType.NETWORK3D: 三维网络数据集，用于存储三维网络对象的数据集。\n    :var DatasetType.LINEM: 路由数据集。是由一系列空间信息中带有刻度值Measure的线对象构成。通常可应用于线性参考模型或者作为网络分析的结果数据。\n    :var DatasetType.PARAMETRICLINE: 复合参数化线数据集，用于存储复合参数化线几何对象的数据集。\n    :var DatasetType.PARAMETRICREGION: 复合参数化面数据集，用于存储复合参数化面几何对象的数据集。\n    :var DatasetType.GRIDCOLLECTION: 存储栅格数据集集合对象的数据集。对栅格数据集集合对象的详细描述请参考 :py:class:`DatasetGridCollection` 。\n    :var DatasetType.IMAGECOLLECTION: 存储影像数据集集合对象的数据集。对影像数据集集合对象的详细描述请参考 :py:class:`DatasetImageCollection` 。\n    :var DatasetType.MODEL: 模型数据集。\n    :var DatasetType.TEXTURE:  纹理数据集，模型数据集的子数据集。\n    :var DatasetType.IMAGE: 影像数据集。不具备属性信息，例如影像地图、多波段影像和实物地图等。其中每一个栅格存储的是一个颜色值或颜色的索引值（RGB 值）。\n    :var DatasetType.WMS: WMS 数据集，是 DatasetImage 的一种类型。WMS （Web Map Service），即 Web 地图服务。WMS 利用具有地理空间位置\n                          信息的数据制作地图。Web 地图服务返回的是图层级的地图影像。其中将地图定义为地理数据可视的表现。\n    :var DatasetType.WCS: WCS 数据集，是 DatasetImage 的一种类型。 WCS（ Web Coverage Service），即 Web 覆盖服务，面向空间影像数据，\n                          它将包含地理位置值的地理空间数据作为“覆盖（Coverage）”在网上相互交换。\n    :var DatasetType.GRID: 栅格数据集。例如高程数据集和土地利用图。其中每一个栅格存储的是表示地物的属性值（例如高程值）。\n    :var DatasetType.VOLUME: 栅格体数据集合，以切片采样方式对三维体数据进行表达，例如指定空间范围的手机信号强度、雾霾污染指数等。\n    :var DatasetType.TOPOLOGY: 拓扑数据集。拓扑数据集实际上是一个对拓扑错误提供综合管理能力的容器。它覆盖了拓扑关联数据集、拓扑规则、拓扑预处理、\n                               拓扑错误生成以及定位修改、脏区自动维护等拓扑错误检查的关键要素，为拓扑错误检查提供了一套完整的解决方案。脏区指的\n                               是未进行拓扑检查的区域，就已经进行了拓扑检查的区域，若用户在局部对数据进行了部分编辑时，则在此局部区域又将生成新的脏区。\n    :var DatasetType.POINT3D: 三维点数据集，用于存储三维点对象的数据集。\n    :var DatasetType.LINE3D: 三维线数据集，用于存储三维线对象的数据集。\n    :var DatasetType.REGION3D: 三维面数据集，用于存储三维面对象的数据集。\n    :var DatasetType.POINTEPS: 清华山维点数据集，用于存储清华山维点对象的数据集。\n    :var DatasetType.LINEEPS: 清华山维线数据集，用于存储清华山维线对象的数据集。\n    :var DatasetType.REGIONEPS: 清华山维面数据集，用于存储清华山维面对象的数据集。\n    :var DatasetType.TEXTEPS: 清华山维文本数据集，用于存储清华山维文本对象的数据集。\n    :var DatasetType.VECTORCOLLECTION: 矢量数据集集合，用于存储多个矢量数据集，仅支持 PostgreSQL 引擎。\n    :var DatasetType.MOSAIC: 镶嵌数据集\n    "
    UNKNOWN = -1
    TABULAR = 0
    POINT = 1
    LINE = 3
    REGION = 5
    TEXT = 7
    CAD = 149
    LINKTABLE = 153
    NETWORK = 4
    NETWORK3D = 205
    LINEM = 35
    PARAMETRICLINE = 8
    PARAMETRICREGION = 9
    GRIDCOLLECTION = 199
    IMAGECOLLECTION = 200
    MODEL = 203
    TEXTURE = 204
    IMAGE = 81
    WMS = 86
    WCS = 87
    GRID = 83
    VOLUME = 89
    TOPOLOGY = 154
    POINT3D = 101
    LINE3D = 103
    REGION3D = 105
    POINTEPS = 157
    LINEEPS = 158
    REGIONEPS = 159
    TEXTEPS = 160
    VECTORCOLLECTION = 201
    MOSAIC = 206

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.DatasetType"


@unique
class GeometryType(JEnum):
    __doc__ = "\n    该类定义了一系列几何对象的类型常量。\n\n    :var GeometryType.GEOPOINT: 点几何对象\n    :var GeometryType.GEOLINE: 线几何对象。\n    :var GeometryType.GEOREGION: 面几何对象\n    :var GeometryType.GEOTEXT: 文本几何对象\n    :var GeometryType.GEOLINEM: 路由对象，是一组具有 X，Y 坐标与线性度量值的点组成的线性地物对象。\n    :var GeometryType.GEOCOMPOUND: 复合几何对象。复合几何对象由多个子对象构成，每一个子对象可以是任何一种类型的几何对象。\n    :var GeometryType.GEOPARAMETRICLINECOMPOUND: 复合参数化线几何对象。\n    :var GeometryType.GEOPARAMETRICREGIONCOMPOUND:  复合参数化面几何对象。\n    :var GeometryType.GEOPARAMETRICLINE: 参数化线几何对象。\n    :var GeometryType.GEOPARAMETRICREGION: 参数化面几何对象。\n    :var GeometryType.GEOMULTIPOINT: 多点对象，参数化的几何对象类型。\n    :var GeometryType.GEOROUNDRECTANGLE: 圆角矩形几何对象，参数化的几何对象类型。\n    :var GeometryType.GEOCIRCLE: 圆几何对象，参数化的几何对象类型。\n    :var GeometryType.GEOELLIPSE: 椭圆几何对象，参数化的几何对象类型。\n    :var GeometryType.GEOPIE: 扇面几何对象，参数化的几何对象类型。\n    :var GeometryType.GEOARC: 圆弧几何对象，参数化的几何对象类型。\n    :var GeometryType.GEOELLIPTICARC: 椭圆弧几何对象，参数化的几何对象类型。\n    :var GeometryType.GEOCARDINAL: 二维 Cardinal 样条曲线几何对象，参数化的几何对象类型。\n    :var GeometryType.GEOCURVE: 二维曲线几何对象，参数化的几何对象类型。\n    :var GeometryType.GEOBSPLINE: 二维 B 样条曲线几何对象，参数化的几何对象类型。\n    :var GeometryType.GEOPOINT3D: 三维点几何对象。\n    :var GeometryType.GEOLINE3D: 三维线几何对象。\n    :var GeometryType.GEOREGION3D: 三维面几何对象。\n    :var GeometryType.GEOCHORD:  弓形几何对象，参数化的几何对象类型。\n    :var GeometryType.GEOCYLINDER: 圆台几何对象。\n    :var GeometryType.GEOPYRAMID:  四棱锥几何对象。\n    :var GeometryType.GEORECTANGLE: 矩形几何对象，参数化的几何对象类型。\n    :var GeometryType.GEOBOX: 长方体几何对象。\n    :var GeometryType.GEOPICTURE: 二维图片几何对象。\n    :var GeometryType.GEOCONE: 圆锥体几何对象。\n    :var GeometryType.GEOPLACEMARK: 三维地标几何对象。\n    :var GeometryType.GEOCIRCLE3D: 三维圆面几何对象。\n    :var GeometryType.GEOSPHERE:  球体几何对象\n    :var GeometryType.GEOHEMISPHERE: 半球体几何对象。\n    :var GeometryType.GEOPIECYLINDER: 饼台几何对象。\n    :var GeometryType.GEOPIE3D: 三维扇面几何对象。\n    :var GeometryType.GEOELLIPSOID:  椭球体几何对象。\n    :var GeometryType.GEOPARTICLE: 三维粒子几何对象。\n    :var GeometryType.GEOTEXT3D: 三维文本几何对象。\n    :var GeometryType.GEOMODEL: 三维模型几何对象。\n    :var GeometryType.GEOMAP: 地图几何对象，用于在布局中添加地图。\n    :var GeometryType.GEOMAPSCALE: 地图比例尺几何对象。\n    :var GeometryType.GEONORTHARROW: 指北针几何对象。\n    :var GeometryType.GEOMAPBORDER: 地图几何对象边框。\n    :var GeometryType.GEOPICTURE3D: 三维图片几何对象。\n    :var GeometryType.GEOLEGEND: 图例对象。\n    :var GeometryType.GEOUSERDEFINED: 用户自定义的几何对象。\n    :var GeometryType.GEOPOINTEPS: EPS 点几何对象\n    :var GeometryType.GEOLINEEPS: EPS 线几何对象\n    :var GeometryType.GEOREGIONEPS: EPS 面几何对象\n    :var GeometryType.GEOTEXTEPS: EPS 文本几何对象\n    "
    GEOPOINT = 1
    GEOLINE = 3
    GEOREGION = 5
    GEOTEXT = 7
    GEOLINEM = 35
    GEOCOMPOUND = 1000
    GEOPARAMETRICLINECOMPOUND = 8
    GEOPARAMETRICREGIONCOMPOUND = 9
    GEOPARAMETRICLINE = 16
    GEOPARAMETRICREGION = 17
    GEOMULTIPOINT = 2
    GEOROUNDRECTANGLE = 13
    GEOCIRCLE = 15
    GEOELLIPSE = 20
    GEOPIE = 21
    GEOARC = 24
    GEOELLIPTICARC = 25
    GEOCARDINAL = 27
    GEOCURVE = 28
    GEOBSPLINE = 29
    GEOPOINT3D = 101
    GEOLINE3D = 103
    GEOREGION3D = 105
    GEOCHORD = 23
    GEOCYLINDER = 1206
    GEOPYRAMID = 1208
    GEORECTANGLE = 12
    GEOBOX = 1205
    GEOPICTURE = 1101
    GEOCONE = 1207
    GEOPLACEMARK = 108
    GEOCIRCLE3D = 1210
    GEOSPHERE = 1203
    GEOHEMISPHERE = 1204
    GEOPIECYLINDER = 1211
    GEOPIE3D = 1209
    GEOELLIPSOID = 1212
    GEOPARTICLE = 1213
    GEOTEXT3D = 107
    GEOMODEL = 1201
    GEOMODEL3D = 1218
    GEOMAP = 2001
    GEOMAPSCALE = 2005
    GEONORTHARROW = 2008
    GEOMAPBORDER = 2009
    GEOPICTURE3D = 1202
    GEOLEGEND = 2011
    GEOUSERDEFINED = 1001
    GEOPOINTEPS = 4000
    GEOLINEEPS = 4001
    GEOREGIONEPS = 4002
    GEOTEXTEPS = 4003
    GRAPHICOBJECT = 3000

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.GeometryType"


@unique
class FieldType(JEnum):
    __doc__ = "\n    该类定义了字段类型常量。 定义一系列常量表示存储不同类型值的字段。\n\n    :var FieldType.BOOLEAN: 布尔类型\n    :var FieldType.BYTE: 字节型字段\n    :var FieldType.INT16: 16位整型字段\n    :var FieldType.INT32: 32位整型字段\n    :var FieldType.INT64: 64位整型字段\n    :var FieldType.SINGLE: 32位精度浮点型字段\n    :var FieldType.DOUBLE: 64位精度浮点型字段\n    :var FieldType.DATETIME: 日期型字段\n    :var FieldType.LONGBINARY: 二进制型字段\n    :var FieldType.TEXT: 变长的文本型字段\n    :var FieldType.CHAR: 长的文本类型字段，例如指定的字符串长度为10，那么输入的字符串只有3个字符，则其他都用0来占位\n    :var FieldType.WTEXT: 宽字符类型字段\n    :var FieldType.JSONB: JSONB 类型字段（PostgreSQL独有字段）\n    "
    BOOLEAN = 1
    BYTE = 2
    INT16 = 3
    INT32 = 4
    INT64 = 16
    SINGLE = 6
    DOUBLE = 7
    DATETIME = 23
    LONGBINARY = 11
    TEXT = 10
    CHAR = 18
    WTEXT = 127
    JSONB = 129

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.FieldType"

    @classmethod
    def _externals(cls):
        return {'bool':FieldType.BOOLEAN,  'short':FieldType.INT16, 
         'int':FieldType.INT32, 
         'long':FieldType.INT64, 
         'float':FieldType.SINGLE, 
         'binary':FieldType.LONGBINARY, 
         'str':FieldType.WTEXT, 
         'string':FieldType.WTEXT, 
         'date':FieldType.DATETIME, 
         'integer':FieldType.INT32, 
         'bytes':FieldType.LONGBINARY, 
         'timestamp':FieldType.DATETIME}


@unique
class Unit(JEnum):
    __doc__ = "\n    该类定义了表示单位的类型常量。\n\n    :var Unit.MILIMETER: 毫米\n    :var Unit.CENTIMETER: 厘米\n    :var Unit.DECIMETER: 分米\n    :var Unit.METER: 米\n    :var Unit.KILOMETER: 千米\n    :var Unit.INCH: 英寸\n    :var Unit.FOOT: 英尺\n    :var Unit.YARD: 码\n    :var Unit.MILE: 英里\n    :var Unit.SECOND: 秒，角度单位\n    :var Unit.MINUTE: 分，角度单位\n    :var Unit.DEGREE: 度，角度单位\n    :var Unit.RADIAN: 弧度，弧度单位\n\n    "
    MILIMETER = 10
    CENTIMETER = 100
    DECIMETER = 1000
    METER = 10000
    KILOMETER = 10000000
    INCH = 254
    FOOT = 3048
    YARD = 9144
    MILE = 16090000
    SECOND = 1000000485
    MINUTE = 1000029089
    DEGREE = 1001745329
    RADIAN = 1100000000

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.Unit"


@unique
class BufferRadiusUnit(JEnum):
    __doc__ = "\n    该枚举定义了缓冲区分析半径单位类型常量\n\n    :var BufferRadiusUnit.MILIMETER: 毫米\n    :var BufferRadiusUnit.CENTIMETER: 厘米\n    :var BufferRadiusUnit.DECIMETER: 分米\n    :var BufferRadiusUnit.METER: 米\n    :var BufferRadiusUnit.KILOMETER: 千米\n    :var BufferRadiusUnit.INCH: 英寸\n    :var BufferRadiusUnit.FOOT: 英尺\n    :var BufferRadiusUnit.YARD: 码\n    :var BufferRadiusUnit.MILE: 英里\n    "
    MILIMETER = 10
    CENTIMETER = 100
    DECIMETER = 1000
    METER = 10000
    KILOMETER = 10000000
    INCH = 254
    FOOT = 3048
    YARD = 9144
    MILE = 16090000

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialanalyst.BufferRadiusUnit"


@unique
class Charset(JEnum):
    __doc__ = "\n    该类定义了矢量数据集的字符集类型常量。\n\n    :var Charset.ANSI:  ASCII 字符集\n    :var Charset.DEFAULT: 扩展的 ASCII 字符集。\n    :var Charset.SYMBOL: 符号字符集。\n    :var Charset.MAC: Macintosh 使用的字符\n    :var Charset.SHIFTJIS: 日语字符集\n    :var Charset.HANGEUL: 朝鲜字符集的其它常用拼写\n    :var Charset.JOHAB: 朝鲜字符集\n    :var Charset.GB18030: 在中国大陆使用的中文字符集\n    :var Charset.CHINESEBIG5: 在中国香港特别行政区和台湾最常用的中文字符集\n    :var Charset.GREEK: 希腊字符集\n    :var Charset.TURKISH: 土耳其语字符集\n    :var Charset.VIETNAMESE: 越南语字符集\n    :var Charset.HEBREW: 希伯来字符集\n    :var Charset.ARABIC: 阿拉伯字符集\n    :var Charset.BALTIC: 波罗的海字符集\n    :var Charset.RUSSIAN: 俄语字符集\n    :var Charset.THAI: 泰语字符集\n    :var Charset.EASTEUROPE: 东欧字符集\n    :var Charset.OEM: 扩展的 ASCII 字符集\n    :var Charset.UTF8: UTF-8（8 位元 Universal Character Set/Unicode Transformation Format）是针对Unicode 的一种可变长度字符编码。它可以用来表示 Unicode 标准中的任何字符，而且其编码中的第一个字节仍与 ASCII 相容，使得原来处理 ASCII 字符的软件无需或只作少部份修改后，便可继续使用。\n    :var Charset.UTF7: UTF-7 (7-位元 Unicode 转换格式（Unicode Transformation Format，简写成 UTF）) 是一种可变长度字符编码方式，用以将 Unicode 字符以 ASCII 编码的字符串来呈现。\n    :var Charset.WINDOWS1252: 英文常用的编码。Windows1252（Window 9x标准for西欧语言）。\n    :var Charset.KOREAN: 韩语字符集\n    :var Charset.UNICODE: 在计算机科学领域中，Unicode（统一码、万国码、单一码、标准万国码）是业界的一种标准。\n    :var Charset.CYRILLIC: Cyrillic (Windows)\n    :var Charset.XIA5: IA5\n    :var Charset.XIA5GERMAN: IA5 (German)\n    :var Charset.XIA5SWEDISH: IA5 (Swedish)\n    :var Charset.XIA5NORWEGIAN: IA5 (Norwegian)\n\n    "
    ANSI = 0
    DEFAULT = 1
    SYMBOL = 2
    MAC = 77
    SHIFTJIS = 128
    HANGEUL = 129
    JOHAB = 130
    GB18030 = 134
    CHINESEBIG5 = 136
    GREEK = 161
    TURKISH = 162
    VIETNAMESE = 163
    HEBREW = 177
    ARABIC = 178
    BALTIC = 186
    RUSSIAN = 204
    THAI = 222
    EASTEUROPE = 238
    OEM = 255
    UTF8 = 250
    UTF7 = 7
    WINDOWS1252 = 137
    KOREAN = 131
    UNICODE = 132
    CYRILLIC = 135
    XIA5 = 3
    XIA5GERMAN = 4
    XIA5SWEDISH = 5
    XIA5NORWEGIAN = 6

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.Charset"


@unique
class EncodeType(JEnum):
    __doc__ = "\n    该类定义了数据集存储时的压缩编码方式类型常量。\n\n    对矢量数据集，支持四种压缩编码方式，即单字节，双字节，三字节和四字节编码方式，这四种压缩编码方式采用相同的压缩编码机制，但是压缩的比率不同。\n    其均为有损压缩。需要注意的是点数据集、纯属性数据集以及 CAD 数据集不可压缩编码。对光栅数据，可以采用四种压缩编码方式，即 DCT、SGL、LZW 和\n    COMPOUND。其中 DCT 和 COMPOUND 为有损压缩编码方式，SGL 和 LZW 为无损压缩编码方式。\n\n    对于影像和栅格数据集，根据其像素格式（PixelFormat）选择合适的压缩编码方式，对提高系统运行的效率，节省存储空间非常有利。下表列出了影像和栅格数\n    据集不同像素格式对应的合理的编码方式:\n\n    .. image:: ../image/EncodeTypeRec.png\n\n    :var EncodeType.NONE: 不使用编码方式\n    :var EncodeType.BYTE: 单字节编码方式。使用1个字节存储一个坐标值。（只适用于线和面数据集）\n    :var EncodeType.INT16: 双字节编码方式。使用2个字节存储一个坐标值。（只适用于线和面数据集）\n    :var EncodeType.INT24: 三字节编码方式。使用3个字节存储一个坐标值。（只适用于线和面数据集）\n    :var EncodeType.INT32: 四字节编码方式。使用4个字节存储一个坐标值。（只适用于线和面数据集）\n    :var EncodeType.DCT: DCT（Discrete Cosine Transform），离散余弦编码。是一种广泛应用于图像压缩中的变换编码方法，这种变换方法在信息的压\n                         缩能力、重构图像质量、适应范围和算法复杂性等方面之间提供了一种很好的平衡，成为目前应用最广泛的图像压缩技术。其原理是通\n                         过变换降低图像原始空间域表示中存在的非常强的相关性，使信号更紧凑地表达。该方法有很高的压缩率和性能，但编码是有失真的。\n                         由于影像数据集一般不用来进行精确的分析，所以 DCT 编码方式是影像数据集存储的压缩编码方式。（适用于影像数据集）\n    :var EncodeType.SGL: SGL（SuperMap Grid LZW），SuperMap 自定义的一种压缩存储格式。其实质是改进的 LZW 编码方式。SGL 对 LZW 进行了改\n                         进，是一种更高效的压缩存储方式。目前 SuperMap 中的对 Grid 数据集和 DEM 数据集压缩存储采用的就是 SGL 的压缩编码方\n                         式，这是一种无损压缩。（适用于栅格数据集）\n    :var EncodeType.LZW: LZW 是一种广泛采用的字典压缩方法，其最早是用在文字数据的压缩方面。LZW的编码的原理是用代号来取代一段字符串，后续的相同\n                         的字符串就使用相同代号，所以该编码方式不仅可以对重复数据起到压缩作用，还可以对不重复数据进行压缩操作。适用于索引色影像\n                         的压缩方式，这是一种无损压缩编码方式。（适用于栅格和影像数据集）\n    :var EncodeType.PNG: PNG 压缩编码方式，支持多种位深的图像，是一种无损压缩方式。（适用于影像数据集）\n    :var EncodeType.COMPOUND: 数据集复合编码方式，其压缩比接近于 DCT 编码方式，主要针对 DCT 压缩导致的边界影像块失真的问题。（适用于 RGB 格式的影像数据集）\n\n    "
    NONE = 0
    BYTE = 1
    INT16 = 2
    INT24 = 3
    INT32 = 4
    DCT = 8
    SGL = 9
    LZW = 11
    PNG = 12
    COMPOUND = 17

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.EncodeType"


@unique
class PixelFormat(JEnum):
    __doc__ = "\n    该类定义了栅格与影像数据存储的像素格式类型常量。\n\n    光栅数据结构实际上就是像元的阵列，像元（或像素）是光栅数据的最基本信息存储单位。在 SuperMap 中有两种类型的光栅数据：栅格数据集（DatasetGrid）\n    和影像数据集（DatasetImage），栅格数据集多用来进行栅格分析，因而其像元值为地物的属性值，如高程，降水量等；而影像数据集一般用来进行显示或作为底\n    图，因而其像元值为颜色值或颜色的索引值。\n\n    :var PixelFormat.UNKONOWN: 未知的像素格式\n    :var PixelFormat.UBIT1: 每个像元用 1 个比特表示。对栅格数据集来说，可表示 0 和 1 两种值；对影像数据集来说，可表示黑白两种颜色，对应单色影像数据。\n    :var PixelFormat.UBIT4: 每个像元用 4 个比特表示。对栅格数据集来说，可表示 0 到 15 共 16 个整数值；对影像数据集来说，可表示 16 种颜色，这 16 种颜色为索引色，在其颜色表中定义，对应 16 色的影像数据。\n    :var PixelFormat.UBIT8: 每个像元用 8 个比特，即 1 个字节表示。对栅格数据集来说，可表示 0 到 255 共 256 个整数值；对影像数据集来说，可表示 256 种渐变的颜色，这 256 种颜色为索引色，在其颜色表中定义，对应 256 色的影像数据。\n    :var PixelFormat.BIT8: 每个像元用 8 个比特，即 1 个字节来表示。对栅格数据集来说，可表示 -128 到 127 共 256 个整数值。每个像元用 8 个比特，即 1 个字节来表示。对栅格数据集来说，可表示 -128 到 127 共 256 个整数值。\n    :var PixelFormat.BIT16: 每个像元用 16 个比特，即 2 个字节表示。对栅格数据集来说，可表示 -32768 到 32767 共 65536 个整数值；对影像数据集来说，16 个比特中，红，绿，蓝各用 5 比特来表示，剩余 1 比特未使用，对应彩色的影像数据。\n    :var PixelFormat.UBIT16: 每个像元用 16 个比特，即 2 个字节来表示。对栅格数据集来说，可表示 0 到 65535 共 65536 个整数值\n    :var PixelFormat.RGB: 每个像元用 24 个比特，即 3 个字节来表示。仅提供给影像数据集使用，24 比特中红、绿、蓝各用 8 比特来表示，对应真彩色的影像数据。\n    :var PixelFormat.RGBA: 每个像元用 32 个比特，即 4 个字节来表示。仅提供给影像数据集使用，32 比特中红、绿、蓝和 alpha 各用 8 比特来表示，对应增强真彩色的影像数据。\n    :var PixelFormat.BIT32: 每个像元用 32 个比特，即 4 个字节来表示。对栅格数据集来说，可表示 -231 到 (231-1) 共 4294967296 个整数值；对影像数据集来说，32 比特中，红，绿，蓝和 alpha 各用 8 比特来表示，对应增强真彩色的影像数据。该格式支持 DatasetGrid，DatasetImage（仅支持多波段）。\n    :var PixelFormat.UBIT32: 每个像元用 32 个比特，即 4 个字节来表示，可表示 0 到 4294967295 共 4294967296 个整数值。\n    :var PixelFormat.BIT64: 每个像元用 64 个比特，即 8 个字节来表示。可表示 -263 到 (263-1) 共 18446744073709551616 个整数值。。\n    :var PixelFormat.SINGLE: 每个像元用 4 个字节来表示。可表示 -3.402823E+38 到 3.402823E+38 范围内的单精度浮点数。\n    :var PixelFormat.DOUBLE: 每个像元用 8 个字节来表示。可表示 -1.79769313486232E+308 到 1.79769313486232E+308 范围内的双精度浮点数。\n\n    "
    UNKONOWN = 0
    UBIT1 = 1
    UBIT4 = 4
    UBIT8 = 8
    BIT8 = 80
    BIT16 = 16
    UBIT16 = 160
    RGB = 24
    RGBA = 32
    BIT32 = 320
    UBIT32 = 321
    BIT64 = 64
    SINGLE = 3200
    DOUBLE = 6400

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.PixelFormat"

    @classmethod
    def _externals(cls):
        return {'BYTE':cls.BIT8,  'UBYTE':cls.UBIT8, 
         'BIT':cls.UBIT1, 
         'SHORT':cls.BIT16, 
         'USHORT':cls.UBIT16, 
         'INT':cls.BIT32, 
         'LONG':cls.BIT64, 
         'FLOAT':cls.SINGLE, 
         'DOUBLE':cls.DOUBLE}


@unique
class WorkspaceType(JEnum):
    __doc__ = "\n    该类定义了工作空间类型常量。\n\n    SuperMap 支持的文件型工作空间的类型有四种，SSXWU 格式和 SMWU 格式；SuperMap 支持的数据库型工作空间的类型有两种：Oracle 工作空间 和 SQL Server 工作空间。\n\n    :var WorkspaceType.DEFAULT:   默认值， 表示工作空间未被保存时的工作空间类型。\n    :var WorkspaceType.ORACLE: Oracle 工作空间。工作空间保存在 Oracle 数据库中。\n    :var WorkspaceType.SQL: SQL Server 工作空间。工作空间保存在 SQL Server 数据库中。该常量仅在 Windows 平台版本中支持，在 Linux版本中不提供。\n    :var WorkspaceType.DM: DM 工作空间。工作空间保存在DM 数据库中。\n    :var WorkspaceType.MYSQL: MYSQL 工作空间。工作空间保存在MySQL 数据库中。\n    :var WorkspaceType.PGSQL: PostgreSQL 工作空间。工作空间保存在PostgreSQL 数据库中。\n    :var WorkspaceType.MONGO: MongoDB 工作空间。工作空间保存在 MongoDB 数据库中。\n    :var WorkspaceType.SXWU: SXWU工作空间，只有 6R 版本的工作空间能存成类型为 SXWU 的工作空间文件。另存为 6R 版本的工作空间时，文件型工作空间只能存为 SXWU 或是 SMWU。\n    :var WorkspaceType.SMWU: SMWU工作空间，只有 6R 版本的工作空间能存成类型为 SMWU 的工作空间文件。另存为 6R 版本的工作空间时，文件型工作空间只能存为 SXWU 或是 SMWU。该常量仅在 Windows 平台版本中支持，在 Linux版本中不提供。\n\n    "
    DEFAULT = 1
    ORACLE = 6
    SQL = 7
    DM = 12
    MYSQL = 13
    PGSQL = 14
    MONGO = 15
    SXWU = 8
    SMWU = 9

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.WorkspaceType"


@unique
class WorkspaceVersion(JEnum):
    __doc__ = "\n    该类定义了工作空间版本类型常量。\n\n    :var WorkspaceVersion.UGC60: SuperMap UGC 6.0 工作空间\n    :var WorkspaceVersion.UGC70: SuperMap UGC 7.0 工作空间\n\n    "
    UGC60 = 20090106
    UGC70 = 20120328

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.WorkspaceVersion"


@unique
class SpatialIndexType(JEnum):
    __doc__ = "\n    该类定义了空间索引类型常量。\n\n    空间索引用于提高数据空间查询效率的数据结构。在 SuperMap 中提供了 R 树索引，四叉树索引，图幅索引和多级网格索引。以上几种索引仅适用于矢量数据集。\n\n    同时，一个数据集在一种时刻只能使用一种索引，但是索引可以切换，即当对数据集创建完一种索引之后，必须删除旧的索引才能创建新的。数据集处于编辑状态时，\n    系统自动维护当前的索引。特别地，当数据被多次编辑后，索引的效率将会受到不同程度的影响，通过系统的判断得知是否要求重新建立空间索引:\n\n    - 当前版本 UDB 和 PostgreSQL 数据源只支持 R 树索引（RTree），DB2 数据源只支持多级网格索引（Multi_Level_Grid）；\n    - 数据库中的点数据集均不支持四叉树（QTree）索引和 R 树索引（RTree）；\n    - 网络数据集不支持任何类型的空间索引；\n    - 复合数据集不支持多级网格索引；\n    - 路由数据集不支持图幅索引（TILE）；\n    - 属性数据集不支持任何类型的空间索引；\n    - 对于数据库类型的数据源，数据库记录要大于1000条时才可以创建索引。\n\n    :var SpatialIndexType.NONE: 无空间索引就是没有空间索引，适用于数据量非常小的情况\n    :var SpatialIndexType.RTREE: R 树索引是基于磁盘的索引结构，是 B 树(一维)在高维空间的自然扩展，易于与现有数据库系统集成，能够支持各种类型\n                                 的空间查询处理操作，在实践中得到了广泛的应用，是目前最流行的空间索引方法之一。R 树空间索引方法是设计一些包含\n                                 空间对象的矩形，将一些空间位置相近的目标对象，包含在这个矩形内，把这些矩形作为空间索引，它含有所包含的空间对\n                                 象的指针。\n                                 注意：\n\n                                 - 此索引适合于静态数据（对数据进行浏览、查询操作时）。\n                                 - 此索引支持数据的并发操作。\n\n    :var SpatialIndexType.QTREE: 四叉树是一种重要的层次化数据集结构，主要用来表达二维坐标下空间层次关系，实际上它是一维二叉树在二维空间的扩展。\n                                 那么，四叉树索引就是将一张地图四等分，然后再每一个格子中再四等分，逐层细分，直至不能再分。现在在 SuperMap\n                                 中四叉树最多允许分成13层。基于希尔伯特（Hilbert）编码的排序规则，从四叉树中可确定索引类中每个对象实例的被索\n                                 引属性值是属于哪个最小范围。从而提高了检索效率\n    :var SpatialIndexType.TILE: 图幅索引。在 SuperMap 中根据数据集的某一属性字段或根据给定的一个范围，将空间对象进行分类，通过索引进行管理已\n                                分类的空间对象，以此提高查询检索速度\n    :var SpatialIndexType.MULTI_LEVEL_GRID: 多级网格索引，又叫动态索引。多级网格索引结合了 R 树索引与四叉树索引的优点，提供非常好的并发编辑\n                                            支持，具有很好的普适性。若不能确定数据适用于哪种空间索引，可为其建立多级网格索引。采用划分多层网\n                                            格的方式来组织管理数据。网格索引的基本方法是将数据集按照一定的规则划分成相等或不相等的网格，记录\n                                            每一个地理对象所占的网格位置。在 GIS 中常用的是规则网格。当用户进行空间查询时，首先计算出用户查\n                                            询对象所在的网格，通过该网格快速查询所选地理对象，可以优化查询操作。\n\n                                            当前版本中，定义网格的索引为一级，二级和三级，每一级都有各自的划分规则，第一级的网格最小，第二级\n                                            和第三级的网格要相应得比前面的大。在建立多级网格索引时，根据具体数据及其分布的情况，网格的大小和\n                                            网格索引的级数由系统自动给出，不需要用户进行设置。\n    :var SpatialIndexType.PRIMARY: 原生索引，创建的是空间索引。在PostgreSQL空间数据扩展PostGIS中是GIST索引，意思是通用的搜索树。在SQLServer空间数据扩展SQLSpatial中是多级格网索引:\n\n                                   - PostGIS的GIST索引是一种平衡的，树状结构的访问方法，主要使用了B-tree、R-tree、RD-tree索引算法。优点：适用于多维数据类型和集合数据类型，同样适用于其他的数据类型，GIST多字段索引在查询条件中包含索引字段的任何子集都会使用索引扫描。缺点：GIST索引创建耗时较长，占用空间也比较大。\n                                   - SQLSpatial的多级格网索引最多可以设置四级，每一级按照等分格网的方式依次进行。在创建索引时，可以选择高、中、低三种格网密度，分别对应（4*4）、（8*8）和（16*16），目前默认中格网密度。\n    "
    NONE = 1
    RTREE = 2
    QTREE = 3
    TILE = 4
    MULTI_LEVEL_GRID = 5
    PRIMARY = 7

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.SpatialIndexType"


@unique
class PrjCoordSysType(JEnum):
    PCS_USER_DEFINED = -1
    PCS_NON_EARTH = 0
    PCS_EARTH_LONGITUDE_LATITUDE = 1
    PCS_WORLD_PLATE_CARREE = 54001
    PCS_WORLD_EQUIDISTANT_CYLINDRICAL = 54002
    PCS_WORLD_MILLER_CYLINDRICAL = 54003
    PCS_WORLD_MERCATOR = 54004
    PCS_WORLD_SINUSOIDAL = 54008
    PCS_WORLD_MOLLWEIDE = 54009
    PCS_WORLD_ECKERT_VI = 54010
    PCS_WORLD_ECKERT_V = 54011
    PCS_WORLD_ECKERT_IV = 54012
    PCS_WORLD_ECKERT_III = 54013
    PCS_WORLD_ECKERT_II = 54014
    PCS_WORLD_ECKERT_I = 54015
    PCS_WORLD_GALL_STEREOGRAPHIC = 54016
    PCS_WORLD_BEHRMANN = 54017
    PCS_WORLD_WINKEL_I = 54018
    PCS_WORLD_WINKEL_II = 54019
    PCS_WORLD_POLYCONIC = 54021
    PCS_WORLD_QUARTIC_AUTHALIC = 54022
    PCS_WORLD_LOXIMUTHAL = 54023
    PCS_WORLD_BONNE = 54024
    PCS_WORLD_HOTINE = 54025
    PCS_WORLD_STEREOGRAPHIC = 54026
    PCS_WORLD_EQUIDISTANT_CONIC = 54027
    PCS_WORLD_CASSINI = 54028
    PCS_WORLD_VAN_DER_GRINTEN_I = 54029
    PCS_WORLD_ROBINSON = 54030
    PCS_WORLD_TWO_POINT_EQUIDISTANT = 54031
    PCS_SPHERE_PLATE_CARREE = 53001
    PCS_SPHERE_EQUIDISTANT_CYLINDRICAL = 53002
    PCS_SPHERE_MILLER_CYLINDRICAL = 53003
    PCS_SPHERE_MERCATOR = 53004
    PCS_SPHERE_SINUSOIDAL = 53008
    PCS_SPHERE_MOLLWEIDE = 53009
    PCS_SPHERE_ECKERT_VI = 53010
    PCS_SPHERE_ECKERT_V = 53011
    PCS_SPHERE_ECKERT_IV = 53012
    PCS_SPHERE_ECKERT_III = 53013
    PCS_SPHERE_ECKERT_II = 53014
    PCS_SPHERE_ECKERT_I = 53015
    PCS_SPHERE_GALL_STEREOGRAPHIC = 53016
    PCS_SPHERE_BEHRMANN = 53017
    PCS_SPHERE_WINKEL_I = 53018
    PCS_SPHERE_WINKEL_II = 53019
    PCS_SPHERE_POLYCONIC = 53021
    PCS_SPHERE_QUARTIC_AUTHALIC = 53022
    PCS_SPHERE_LOXIMUTHAL = 53023
    PCS_SPHERE_BONNE = 53024
    PCS_SPHERE_STEREOGRAPHIC = 53026
    PCS_SPHERE_EQUIDISTANT_CONIC = 53027
    PCS_SPHERE_CASSINI = 53028
    PCS_SPHERE_VAN_DER_GRINTEN_I = 53029
    PCS_SPHERE_ROBINSON = 53030
    PCS_SPHERE_TWO_POINT_EQUIDISTANT = 53031
    PCS_WGS_1984_UTM_1N = 32601
    PCS_WGS_1984_UTM_2N = 32602
    PCS_WGS_1984_UTM_3N = 32603
    PCS_WGS_1984_UTM_4N = 32604
    PCS_WGS_1984_UTM_5N = 32605
    PCS_WGS_1984_UTM_6N = 32606
    PCS_WGS_1984_UTM_7N = 32607
    PCS_WGS_1984_UTM_8N = 32608
    PCS_WGS_1984_UTM_9N = 32609
    PCS_WGS_1984_UTM_10N = 32610
    PCS_WGS_1984_UTM_11N = 32611
    PCS_WGS_1984_UTM_12N = 32612
    PCS_WGS_1984_UTM_13N = 32613
    PCS_WGS_1984_UTM_14N = 32614
    PCS_WGS_1984_UTM_15N = 32615
    PCS_WGS_1984_UTM_16N = 32616
    PCS_WGS_1984_UTM_17N = 32617
    PCS_WGS_1984_UTM_18N = 32618
    PCS_WGS_1984_UTM_19N = 32619
    PCS_WGS_1984_UTM_20N = 32620
    PCS_WGS_1984_UTM_21N = 32621
    PCS_WGS_1984_UTM_22N = 32622
    PCS_WGS_1984_UTM_23N = 32623
    PCS_WGS_1984_UTM_24N = 32624
    PCS_WGS_1984_UTM_25N = 32625
    PCS_WGS_1984_UTM_26N = 32626
    PCS_WGS_1984_UTM_27N = 32627
    PCS_WGS_1984_UTM_28N = 32628
    PCS_WGS_1984_UTM_29N = 32629
    PCS_WGS_1984_UTM_30N = 32630
    PCS_WGS_1984_UTM_31N = 32631
    PCS_WGS_1984_UTM_32N = 32632
    PCS_WGS_1984_UTM_33N = 32633
    PCS_WGS_1984_UTM_34N = 32634
    PCS_WGS_1984_UTM_35N = 32635
    PCS_WGS_1984_UTM_36N = 32636
    PCS_WGS_1984_UTM_37N = 32637
    PCS_WGS_1984_UTM_38N = 32638
    PCS_WGS_1984_UTM_39N = 32639
    PCS_WGS_1984_UTM_40N = 32640
    PCS_WGS_1984_UTM_41N = 32641
    PCS_WGS_1984_UTM_42N = 32642
    PCS_WGS_1984_UTM_43N = 32643
    PCS_WGS_1984_UTM_44N = 32644
    PCS_WGS_1984_UTM_45N = 32645
    PCS_WGS_1984_UTM_46N = 32646
    PCS_WGS_1984_UTM_47N = 32647
    PCS_WGS_1984_UTM_48N = 32648
    PCS_WGS_1984_UTM_49N = 32649
    PCS_WGS_1984_UTM_50N = 32650
    PCS_WGS_1984_UTM_51N = 32651
    PCS_WGS_1984_UTM_52N = 32652
    PCS_WGS_1984_UTM_53N = 32653
    PCS_WGS_1984_UTM_54N = 32654
    PCS_WGS_1984_UTM_55N = 32655
    PCS_WGS_1984_UTM_56N = 32656
    PCS_WGS_1984_UTM_57N = 32657
    PCS_WGS_1984_UTM_58N = 32658
    PCS_WGS_1984_UTM_59N = 32659
    PCS_WGS_1984_UTM_60N = 32660
    PCS_WGS_1984_UTM_1S = 32701
    PCS_WGS_1984_UTM_2S = 32702
    PCS_WGS_1984_UTM_3S = 32703
    PCS_WGS_1984_UTM_4S = 32704
    PCS_WGS_1984_UTM_5S = 32705
    PCS_WGS_1984_UTM_6S = 32706
    PCS_WGS_1984_UTM_7S = 32707
    PCS_WGS_1984_UTM_8S = 32708
    PCS_WGS_1984_UTM_9S = 32709
    PCS_WGS_1984_UTM_10S = 32710
    PCS_WGS_1984_UTM_11S = 32711
    PCS_WGS_1984_UTM_12S = 32712
    PCS_WGS_1984_UTM_13S = 32713
    PCS_WGS_1984_UTM_14S = 32714
    PCS_WGS_1984_UTM_15S = 32715
    PCS_WGS_1984_UTM_16S = 32716
    PCS_WGS_1984_UTM_17S = 32717
    PCS_WGS_1984_UTM_18S = 32718
    PCS_WGS_1984_UTM_19S = 32719
    PCS_WGS_1984_UTM_20S = 32720
    PCS_WGS_1984_UTM_21S = 32721
    PCS_WGS_1984_UTM_22S = 32722
    PCS_WGS_1984_UTM_23S = 32723
    PCS_WGS_1984_UTM_24S = 32724
    PCS_WGS_1984_UTM_25S = 32725
    PCS_WGS_1984_UTM_26S = 32726
    PCS_WGS_1984_UTM_27S = 32727
    PCS_WGS_1984_UTM_28S = 32728
    PCS_WGS_1984_UTM_29S = 32729
    PCS_WGS_1984_UTM_30S = 32730
    PCS_WGS_1984_UTM_31S = 32731
    PCS_WGS_1984_UTM_32S = 32732
    PCS_WGS_1984_UTM_33S = 32733
    PCS_WGS_1984_UTM_34S = 32734
    PCS_WGS_1984_UTM_35S = 32735
    PCS_WGS_1984_UTM_36S = 32736
    PCS_WGS_1984_UTM_37S = 32737
    PCS_WGS_1984_UTM_38S = 32738
    PCS_WGS_1984_UTM_39S = 32739
    PCS_WGS_1984_UTM_40S = 32740
    PCS_WGS_1984_UTM_41S = 32741
    PCS_WGS_1984_UTM_42S = 32742
    PCS_WGS_1984_UTM_43S = 32743
    PCS_WGS_1984_UTM_44S = 32744
    PCS_WGS_1984_UTM_45S = 32745
    PCS_WGS_1984_UTM_46S = 32746
    PCS_WGS_1984_UTM_47S = 32747
    PCS_WGS_1984_UTM_48S = 32748
    PCS_WGS_1984_UTM_49S = 32749
    PCS_WGS_1984_UTM_50S = 32750
    PCS_WGS_1984_UTM_51S = 32751
    PCS_WGS_1984_UTM_52S = 32752
    PCS_WGS_1984_UTM_53S = 32753
    PCS_WGS_1984_UTM_54S = 32754
    PCS_WGS_1984_UTM_55S = 32755
    PCS_WGS_1984_UTM_56S = 32756
    PCS_WGS_1984_UTM_57S = 32757
    PCS_WGS_1984_UTM_58S = 32758
    PCS_WGS_1984_UTM_59S = 32759
    PCS_WGS_1984_UTM_60S = 32760
    PCS_TOKYO_PLATE_ZONE_I = 32761
    PCS_TOKYO_PLATE_ZONE_II = 32762
    PCS_TOKYO_PLATE_ZONE_III = 32763
    PCS_TOKYO_PLATE_ZONE_IV = 32764
    PCS_TOKYO_PLATE_ZONE_V = 32765
    PCS_TOKYO_PLATE_ZONE_VI = 32766
    PCS_TOKYO_PLATE_ZONE_VII = 32767
    PCS_TOKYO_PLATE_ZONE_VIII = 32768
    PCS_TOKYO_PLATE_ZONE_IX = 32769
    PCS_TOKYO_PLATE_ZONE_X = 32770
    PCS_TOKYO_PLATE_ZONE_XI = 32771
    PCS_TOKYO_PLATE_ZONE_XII = 32772
    PCS_TOKYO_PLATE_ZONE_XIII = 32773
    PCS_TOKYO_PLATE_ZONE_XIV = 32774
    PCS_TOKYO_PLATE_ZONE_XV = 32775
    PCS_TOKYO_PLATE_ZONE_XVI = 32776
    PCS_TOKYO_PLATE_ZONE_XVII = 32777
    PCS_TOKYO_PLATE_ZONE_XVIII = 32778
    PCS_TOKYO_PLATE_ZONE_XIX = 32779
    PCS_TOKYO_UTM_51 = 32780
    PCS_TOKYO_UTM_52 = 32781
    PCS_TOKYO_UTM_53 = 32782
    PCS_TOKYO_UTM_54 = 32783
    PCS_TOKYO_UTM_55 = 32784
    PCS_TOKYO_UTM_56 = 32785
    PCS_JAPAN_PLATE_ZONE_I = 32786
    PCS_JAPAN_PLATE_ZONE_II = 32787
    PCS_JAPAN_PLATE_ZONE_III = 32788
    PCS_JAPAN_PLATE_ZONE_IV = 32789
    PCS_JAPAN_PLATE_ZONE_V = 32790
    PCS_JAPAN_PLATE_ZONE_VI = 32791
    PCS_JAPAN_PLATE_ZONE_VII = 32792
    PCS_JAPAN_PLATE_ZONE_VIII = 32793
    PCS_JAPAN_PLATE_ZONE_IX = 32794
    PCS_JAPAN_PLATE_ZONE_X = 32795
    PCS_JAPAN_PLATE_ZONE_XI = 32796
    PCS_JAPAN_PLATE_ZONE_XII = 32797
    PCS_JAPAN_PLATE_ZONE_XIII = 32798
    PCS_JAPAN_PLATE_ZONE_XIV = 32800
    PCS_JAPAN_PLATE_ZONE_XV = 32801
    PCS_JAPAN_PLATE_ZONE_XVI = 32802
    PCS_JAPAN_PLATE_ZONE_XVII = 32803
    PCS_JAPAN_PLATE_ZONE_XVIII = 32804
    PCS_JAPAN_PLATE_ZONE_XIX = 32805
    PCS_JAPAN_UTM_51 = 32806
    PCS_JAPAN_UTM_52 = 32807
    PCS_JAPAN_UTM_53 = 32808
    PCS_JAPAN_UTM_54 = 32809
    PCS_JAPAN_UTM_55 = 32810
    PCS_JAPAN_UTM_56 = 32811
    PCS_WGS_1972_UTM_1N = 32201
    PCS_WGS_1972_UTM_2N = 32202
    PCS_WGS_1972_UTM_3N = 32203
    PCS_WGS_1972_UTM_4N = 32204
    PCS_WGS_1972_UTM_5N = 32205
    PCS_WGS_1972_UTM_6N = 32206
    PCS_WGS_1972_UTM_7N = 32207
    PCS_WGS_1972_UTM_8N = 32208
    PCS_WGS_1972_UTM_9N = 32209
    PCS_WGS_1972_UTM_10N = 32210
    PCS_WGS_1972_UTM_11N = 32211
    PCS_WGS_1972_UTM_12N = 32212
    PCS_WGS_1972_UTM_13N = 32213
    PCS_WGS_1972_UTM_14N = 32214
    PCS_WGS_1972_UTM_15N = 32215
    PCS_WGS_1972_UTM_16N = 32216
    PCS_WGS_1972_UTM_17N = 32217
    PCS_WGS_1972_UTM_18N = 32218
    PCS_WGS_1972_UTM_19N = 32219
    PCS_WGS_1972_UTM_20N = 32220
    PCS_WGS_1972_UTM_21N = 32221
    PCS_WGS_1972_UTM_22N = 32222
    PCS_WGS_1972_UTM_23N = 32223
    PCS_WGS_1972_UTM_24N = 32224
    PCS_WGS_1972_UTM_25N = 32225
    PCS_WGS_1972_UTM_26N = 32226
    PCS_WGS_1972_UTM_27N = 32227
    PCS_WGS_1972_UTM_28N = 32228
    PCS_WGS_1972_UTM_29N = 32229
    PCS_WGS_1972_UTM_30N = 32230
    PCS_WGS_1972_UTM_31N = 32231
    PCS_WGS_1972_UTM_32N = 32232
    PCS_WGS_1972_UTM_33N = 32233
    PCS_WGS_1972_UTM_34N = 32234
    PCS_WGS_1972_UTM_35N = 32235
    PCS_WGS_1972_UTM_36N = 32236
    PCS_WGS_1972_UTM_37N = 32237
    PCS_WGS_1972_UTM_38N = 32238
    PCS_WGS_1972_UTM_39N = 32239
    PCS_WGS_1972_UTM_40N = 32240
    PCS_WGS_1972_UTM_41N = 32241
    PCS_WGS_1972_UTM_42N = 32242
    PCS_WGS_1972_UTM_43N = 32243
    PCS_WGS_1972_UTM_44N = 32244
    PCS_WGS_1972_UTM_45N = 32245
    PCS_WGS_1972_UTM_46N = 32246
    PCS_WGS_1972_UTM_47N = 32247
    PCS_WGS_1972_UTM_48N = 32248
    PCS_WGS_1972_UTM_49N = 32249
    PCS_WGS_1972_UTM_50N = 32250
    PCS_WGS_1972_UTM_51N = 32251
    PCS_WGS_1972_UTM_52N = 32252
    PCS_WGS_1972_UTM_53N = 32253
    PCS_WGS_1972_UTM_54N = 32254
    PCS_WGS_1972_UTM_55N = 32255
    PCS_WGS_1972_UTM_56N = 32256
    PCS_WGS_1972_UTM_57N = 32257
    PCS_WGS_1972_UTM_58N = 32258
    PCS_WGS_1972_UTM_59N = 32259
    PCS_WGS_1972_UTM_60N = 32260
    PCS_WGS_1972_UTM_1S = 32301
    PCS_WGS_1972_UTM_2S = 32302
    PCS_WGS_1972_UTM_3S = 32303
    PCS_WGS_1972_UTM_4S = 32304
    PCS_WGS_1972_UTM_5S = 32305
    PCS_WGS_1972_UTM_6S = 32306
    PCS_WGS_1972_UTM_7S = 32307
    PCS_WGS_1972_UTM_8S = 32308
    PCS_WGS_1972_UTM_9S = 32309
    PCS_WGS_1972_UTM_10S = 32310
    PCS_WGS_1972_UTM_11S = 32311
    PCS_WGS_1972_UTM_12S = 32312
    PCS_WGS_1972_UTM_13S = 32313
    PCS_WGS_1972_UTM_14S = 32314
    PCS_WGS_1972_UTM_15S = 32315
    PCS_WGS_1972_UTM_16S = 32316
    PCS_WGS_1972_UTM_17S = 32317
    PCS_WGS_1972_UTM_18S = 32318
    PCS_WGS_1972_UTM_19S = 32319
    PCS_WGS_1972_UTM_20S = 32320
    PCS_WGS_1972_UTM_21S = 32321
    PCS_WGS_1972_UTM_22S = 32322
    PCS_WGS_1972_UTM_23S = 32323
    PCS_WGS_1972_UTM_24S = 32324
    PCS_WGS_1972_UTM_25S = 32325
    PCS_WGS_1972_UTM_26S = 32326
    PCS_WGS_1972_UTM_27S = 32327
    PCS_WGS_1972_UTM_28S = 32328
    PCS_WGS_1972_UTM_29S = 32329
    PCS_WGS_1972_UTM_30S = 32330
    PCS_WGS_1972_UTM_31S = 32331
    PCS_WGS_1972_UTM_32S = 32332
    PCS_WGS_1972_UTM_33S = 32333
    PCS_WGS_1972_UTM_34S = 32334
    PCS_WGS_1972_UTM_35S = 32335
    PCS_WGS_1972_UTM_36S = 32336
    PCS_WGS_1972_UTM_37S = 32337
    PCS_WGS_1972_UTM_38S = 32338
    PCS_WGS_1972_UTM_39S = 32339
    PCS_WGS_1972_UTM_40S = 32340
    PCS_WGS_1972_UTM_41S = 32341
    PCS_WGS_1972_UTM_42S = 32342
    PCS_WGS_1972_UTM_43S = 32343
    PCS_WGS_1972_UTM_44S = 32344
    PCS_WGS_1972_UTM_45S = 32345
    PCS_WGS_1972_UTM_46S = 32346
    PCS_WGS_1972_UTM_47S = 32347
    PCS_WGS_1972_UTM_48S = 32348
    PCS_WGS_1972_UTM_49S = 32349
    PCS_WGS_1972_UTM_50S = 32350
    PCS_WGS_1972_UTM_51S = 32351
    PCS_WGS_1972_UTM_52S = 32352
    PCS_WGS_1972_UTM_53S = 32353
    PCS_WGS_1972_UTM_54S = 32354
    PCS_WGS_1972_UTM_55S = 32355
    PCS_WGS_1972_UTM_56S = 32356
    PCS_WGS_1972_UTM_57S = 32357
    PCS_WGS_1972_UTM_58S = 32358
    PCS_WGS_1972_UTM_59S = 32359
    PCS_WGS_1972_UTM_60S = 32360
    PCS_NAD_1927_BLM_14N = 32074
    PCS_NAD_1927_BLM_15N = 32075
    PCS_NAD_1927_BLM_16N = 32076
    PCS_NAD_1927_BLM_17N = 32077
    PCS_NAD_1927_UTM_3N = 26703
    PCS_NAD_1927_UTM_4N = 26704
    PCS_NAD_1927_UTM_5N = 26705
    PCS_NAD_1927_UTM_6N = 26706
    PCS_NAD_1927_UTM_7N = 26707
    PCS_NAD_1927_UTM_8N = 26708
    PCS_NAD_1927_UTM_9N = 26709
    PCS_NAD_1927_UTM_10N = 26710
    PCS_NAD_1927_UTM_11N = 26711
    PCS_NAD_1927_UTM_12N = 26712
    PCS_NAD_1927_UTM_13N = 26713
    PCS_NAD_1927_UTM_14N = 26714
    PCS_NAD_1927_UTM_15N = 26715
    PCS_NAD_1927_UTM_16N = 26716
    PCS_NAD_1927_UTM_17N = 26717
    PCS_NAD_1927_UTM_18N = 26718
    PCS_NAD_1927_UTM_19N = 26719
    PCS_NAD_1927_UTM_20N = 26720
    PCS_NAD_1927_UTM_21N = 26721
    PCS_NAD_1927_UTM_22N = 26722
    PCS_NAD_1983_UTM_3N = 26903
    PCS_NAD_1983_UTM_4N = 26904
    PCS_NAD_1983_UTM_5N = 26905
    PCS_NAD_1983_UTM_6N = 26906
    PCS_NAD_1983_UTM_7N = 26907
    PCS_NAD_1983_UTM_8N = 26908
    PCS_NAD_1983_UTM_9N = 26909
    PCS_NAD_1983_UTM_10N = 26910
    PCS_NAD_1983_UTM_11N = 26911
    PCS_NAD_1983_UTM_12N = 26912
    PCS_NAD_1983_UTM_13N = 26913
    PCS_NAD_1983_UTM_14N = 26914
    PCS_NAD_1983_UTM_15N = 26915
    PCS_NAD_1983_UTM_16N = 26916
    PCS_NAD_1983_UTM_17N = 26917
    PCS_NAD_1983_UTM_18N = 26918
    PCS_NAD_1983_UTM_19N = 26919
    PCS_NAD_1983_UTM_20N = 26920
    PCS_NAD_1983_UTM_21N = 26921
    PCS_NAD_1983_UTM_22N = 26922
    PCS_NAD_1983_UTM_23N = 26923
    PCS_ETRS_1989_UTM_28N = 25828
    PCS_ETRS_1989_UTM_29N = 25829
    PCS_ETRS_1989_UTM_30N = 25830
    PCS_ETRS_1989_UTM_31N = 25831
    PCS_ETRS_1989_UTM_32N = 25832
    PCS_ETRS_1989_UTM_33N = 25833
    PCS_ETRS_1989_UTM_34N = 25834
    PCS_ETRS_1989_UTM_35N = 25835
    PCS_ETRS_1989_UTM_36N = 25836
    PCS_ETRS_1989_UTM_37N = 25837
    PCS_ETRS_1989_UTM_38N = 25838
    PCS_PULKOVO_1942_GK_4 = 28404
    PCS_PULKOVO_1942_GK_5 = 28405
    PCS_PULKOVO_1942_GK_6 = 28406
    PCS_PULKOVO_1942_GK_7 = 28407
    PCS_PULKOVO_1942_GK_8 = 28408
    PCS_PULKOVO_1942_GK_9 = 28409
    PCS_PULKOVO_1942_GK_10 = 28410
    PCS_PULKOVO_1942_GK_11 = 28411
    PCS_PULKOVO_1942_GK_12 = 28412
    PCS_PULKOVO_1942_GK_13 = 28413
    PCS_PULKOVO_1942_GK_14 = 28414
    PCS_PULKOVO_1942_GK_15 = 28415
    PCS_PULKOVO_1942_GK_16 = 28416
    PCS_PULKOVO_1942_GK_17 = 28417
    PCS_PULKOVO_1942_GK_18 = 28418
    PCS_PULKOVO_1942_GK_19 = 28419
    PCS_PULKOVO_1942_GK_20 = 28420
    PCS_PULKOVO_1942_GK_21 = 28421
    PCS_PULKOVO_1942_GK_22 = 28422
    PCS_PULKOVO_1942_GK_23 = 28423
    PCS_PULKOVO_1942_GK_24 = 28424
    PCS_PULKOVO_1942_GK_25 = 28425
    PCS_PULKOVO_1942_GK_26 = 28426
    PCS_PULKOVO_1942_GK_27 = 28427
    PCS_PULKOVO_1942_GK_28 = 28428
    PCS_PULKOVO_1942_GK_29 = 28429
    PCS_PULKOVO_1942_GK_30 = 28430
    PCS_PULKOVO_1942_GK_31 = 28431
    PCS_PULKOVO_1942_GK_32 = 28432
    PCS_PULKOVO_1942_GK_4N = 28464
    PCS_PULKOVO_1942_GK_5N = 28465
    PCS_PULKOVO_1942_GK_6N = 28466
    PCS_PULKOVO_1942_GK_7N = 28467
    PCS_PULKOVO_1942_GK_8N = 28468
    PCS_PULKOVO_1942_GK_9N = 28469
    PCS_PULKOVO_1942_GK_10N = 28470
    PCS_PULKOVO_1942_GK_11N = 28471
    PCS_PULKOVO_1942_GK_12N = 28472
    PCS_PULKOVO_1942_GK_13N = 28473
    PCS_PULKOVO_1942_GK_14N = 28474
    PCS_PULKOVO_1942_GK_15N = 28475
    PCS_PULKOVO_1942_GK_16N = 28476
    PCS_PULKOVO_1942_GK_17N = 28477
    PCS_PULKOVO_1942_GK_18N = 28478
    PCS_PULKOVO_1942_GK_19N = 28479
    PCS_PULKOVO_1942_GK_20N = 28480
    PCS_PULKOVO_1942_GK_21N = 28481
    PCS_PULKOVO_1942_GK_22N = 28482
    PCS_PULKOVO_1942_GK_23N = 28483
    PCS_PULKOVO_1942_GK_24N = 28484
    PCS_PULKOVO_1942_GK_25N = 28485
    PCS_PULKOVO_1942_GK_26N = 28486
    PCS_PULKOVO_1942_GK_27N = 28487
    PCS_PULKOVO_1942_GK_28N = 28488
    PCS_PULKOVO_1942_GK_29N = 28489
    PCS_PULKOVO_1942_GK_30N = 28490
    PCS_PULKOVO_1942_GK_31N = 28491
    PCS_PULKOVO_1942_GK_32N = 28492
    PCS_PULKOVO_1995_GK_4 = 20004
    PCS_PULKOVO_1995_GK_5 = 20005
    PCS_PULKOVO_1995_GK_6 = 20006
    PCS_PULKOVO_1995_GK_7 = 20007
    PCS_PULKOVO_1995_GK_8 = 20008
    PCS_PULKOVO_1995_GK_9 = 20009
    PCS_PULKOVO_1995_GK_10 = 20010
    PCS_PULKOVO_1995_GK_11 = 20011
    PCS_PULKOVO_1995_GK_12 = 20012
    PCS_PULKOVO_1995_GK_13 = 20013
    PCS_PULKOVO_1995_GK_14 = 20014
    PCS_PULKOVO_1995_GK_15 = 20015
    PCS_PULKOVO_1995_GK_16 = 20016
    PCS_PULKOVO_1995_GK_17 = 20017
    PCS_PULKOVO_1995_GK_18 = 20018
    PCS_PULKOVO_1995_GK_19 = 20019
    PCS_PULKOVO_1995_GK_20 = 20020
    PCS_PULKOVO_1995_GK_21 = 20021
    PCS_PULKOVO_1995_GK_22 = 20022
    PCS_PULKOVO_1995_GK_23 = 20023
    PCS_PULKOVO_1995_GK_24 = 20024
    PCS_PULKOVO_1995_GK_25 = 20025
    PCS_PULKOVO_1995_GK_26 = 20026
    PCS_PULKOVO_1995_GK_27 = 20027
    PCS_PULKOVO_1995_GK_28 = 20028
    PCS_PULKOVO_1995_GK_29 = 20029
    PCS_PULKOVO_1995_GK_30 = 20030
    PCS_PULKOVO_1995_GK_31 = 20031
    PCS_PULKOVO_1995_GK_32 = 20032
    PCS_PULKOVO_1995_GK_4N = 20064
    PCS_PULKOVO_1995_GK_5N = 20065
    PCS_PULKOVO_1995_GK_6N = 20066
    PCS_PULKOVO_1995_GK_7N = 20067
    PCS_PULKOVO_1995_GK_8N = 20068
    PCS_PULKOVO_1995_GK_9N = 20069
    PCS_PULKOVO_1995_GK_10N = 20070
    PCS_PULKOVO_1995_GK_11N = 20071
    PCS_PULKOVO_1995_GK_12N = 20072
    PCS_PULKOVO_1995_GK_13N = 20073
    PCS_PULKOVO_1995_GK_14N = 20074
    PCS_PULKOVO_1995_GK_15N = 20075
    PCS_PULKOVO_1995_GK_16N = 20076
    PCS_PULKOVO_1995_GK_17N = 20077
    PCS_PULKOVO_1995_GK_18N = 20078
    PCS_PULKOVO_1995_GK_19N = 20079
    PCS_PULKOVO_1995_GK_20N = 20080
    PCS_PULKOVO_1995_GK_21N = 20081
    PCS_PULKOVO_1995_GK_22N = 20082
    PCS_PULKOVO_1995_GK_23N = 20083
    PCS_PULKOVO_1995_GK_24N = 20084
    PCS_PULKOVO_1995_GK_25N = 20085
    PCS_PULKOVO_1995_GK_26N = 20086
    PCS_PULKOVO_1995_GK_27N = 20087
    PCS_PULKOVO_1995_GK_28N = 20088
    PCS_PULKOVO_1995_GK_29N = 20089
    PCS_PULKOVO_1995_GK_30N = 20090
    PCS_PULKOVO_1995_GK_31N = 20091
    PCS_PULKOVO_1995_GK_32N = 20092
    PCS_BEIJING_1954_GK_13 = 21413
    PCS_BEIJING_1954_GK_14 = 21414
    PCS_BEIJING_1954_GK_15 = 21415
    PCS_BEIJING_1954_GK_16 = 21416
    PCS_BEIJING_1954_GK_17 = 21417
    PCS_BEIJING_1954_GK_18 = 21418
    PCS_BEIJING_1954_GK_19 = 21419
    PCS_BEIJING_1954_GK_20 = 21420
    PCS_BEIJING_1954_GK_21 = 21421
    PCS_BEIJING_1954_GK_22 = 21422
    PCS_BEIJING_1954_GK_23 = 21423
    PCS_BEIJING_1954_GK_13N = 21473
    PCS_BEIJING_1954_GK_14N = 21474
    PCS_BEIJING_1954_GK_15N = 21475
    PCS_BEIJING_1954_GK_16N = 21476
    PCS_BEIJING_1954_GK_17N = 21477
    PCS_BEIJING_1954_GK_18N = 21478
    PCS_BEIJING_1954_GK_19N = 21479
    PCS_BEIJING_1954_GK_20N = 21480
    PCS_BEIJING_1954_GK_21N = 21481
    PCS_BEIJING_1954_GK_22N = 21482
    PCS_BEIJING_1954_GK_23N = 21483
    PCS_ED_1950_UTM_28N = 23028
    PCS_ED_1950_UTM_29N = 23029
    PCS_ED_1950_UTM_30N = 23030
    PCS_ED_1950_UTM_31N = 23031
    PCS_ED_1950_UTM_32N = 23032
    PCS_ED_1950_UTM_33N = 23033
    PCS_ED_1950_UTM_34N = 23034
    PCS_ED_1950_UTM_35N = 23035
    PCS_ED_1950_UTM_36N = 23036
    PCS_ED_1950_UTM_37N = 23037
    PCS_ED_1950_UTM_38N = 23038
    PCS_ATS_1977_UTM_19N = 2219
    PCS_ATS_1977_UTM_20N = 2220
    PCS_KKJ_FINLAND_1 = 2391
    PCS_KKJ_FINLAND_2 = 2392
    PCS_KKJ_FINLAND_3 = 2393
    PCS_KKJ_FINLAND_4 = 2394
    PCS_SAD_1969_UTM_18N = 29118
    PCS_SAD_1969_UTM_19N = 29119
    PCS_SAD_1969_UTM_20N = 29120
    PCS_SAD_1969_UTM_21N = 29121
    PCS_SAD_1969_UTM_22N = 29122
    PCS_SAD_1969_UTM_17S = 29177
    PCS_SAD_1969_UTM_18S = 29178
    PCS_SAD_1969_UTM_19S = 29179
    PCS_SAD_1969_UTM_20S = 29180
    PCS_SAD_1969_UTM_21S = 29181
    PCS_SAD_1969_UTM_22S = 29182
    PCS_SAD_1969_UTM_23S = 29183
    PCS_SAD_1969_UTM_24S = 29184
    PCS_SAD_1969_UTM_25S = 29185
    PCS_AGD_1966_AMG_48 = 20248
    PCS_AGD_1966_AMG_49 = 20249
    PCS_AGD_1966_AMG_50 = 20250
    PCS_AGD_1966_AMG_51 = 20251
    PCS_AGD_1966_AMG_52 = 20252
    PCS_AGD_1966_AMG_53 = 20253
    PCS_AGD_1966_AMG_54 = 20254
    PCS_AGD_1966_AMG_55 = 20255
    PCS_AGD_1966_AMG_56 = 20256
    PCS_AGD_1966_AMG_57 = 20257
    PCS_AGD_1966_AMG_58 = 20258
    PCS_AGD_1984_AMG_48 = 20348
    PCS_AGD_1984_AMG_49 = 20349
    PCS_AGD_1984_AMG_50 = 20350
    PCS_AGD_1984_AMG_51 = 20351
    PCS_AGD_1984_AMG_52 = 20352
    PCS_AGD_1984_AMG_53 = 20353
    PCS_AGD_1984_AMG_54 = 20354
    PCS_AGD_1984_AMG_55 = 20355
    PCS_AGD_1984_AMG_56 = 20356
    PCS_AGD_1984_AMG_57 = 20357
    PCS_AGD_1984_AMG_58 = 20358
    PCS_GDA_1994_MGA_48 = 28348
    PCS_GDA_1994_MGA_49 = 28349
    PCS_GDA_1994_MGA_50 = 28350
    PCS_GDA_1994_MGA_51 = 28351
    PCS_GDA_1994_MGA_52 = 28352
    PCS_GDA_1994_MGA_53 = 28353
    PCS_GDA_1994_MGA_54 = 28354
    PCS_GDA_1994_MGA_55 = 28355
    PCS_GDA_1994_MGA_56 = 28356
    PCS_GDA_1994_MGA_57 = 28357
    PCS_GDA_1994_MGA_58 = 28358
    PCS_NAD_1927_AL_E = 26729
    PCS_NAD_1927_AL_W = 26730
    PCS_NAD_1927_AK_1 = 26731
    PCS_NAD_1927_AK_2 = 26732
    PCS_NAD_1927_AK_3 = 26733
    PCS_NAD_1927_AK_4 = 26734
    PCS_NAD_1927_AK_5 = 26735
    PCS_NAD_1927_AK_6 = 26736
    PCS_NAD_1927_AK_7 = 26737
    PCS_NAD_1927_AK_8 = 26738
    PCS_NAD_1927_AK_9 = 26739
    PCS_NAD_1927_AK_10 = 26740
    PCS_NAD_1927_AZ_E = 26748
    PCS_NAD_1927_AZ_C = 26749
    PCS_NAD_1927_AZ_W = 26750
    PCS_NAD_1927_AR_N = 26751
    PCS_NAD_1927_AR_S = 26752
    PCS_NAD_1927_CA_I = 26741
    PCS_NAD_1927_CA_II = 26742
    PCS_NAD_1927_CA_III = 26743
    PCS_NAD_1927_CA_IV = 26744
    PCS_NAD_1927_CA_V = 26745
    PCS_NAD_1927_CA_VI = 26746
    PCS_NAD_1927_CA_VII = 26747
    PCS_NAD_1927_CO_N = 26753
    PCS_NAD_1927_CO_C = 26754
    PCS_NAD_1927_CO_S = 26755
    PCS_NAD_1927_CT = 26756
    PCS_NAD_1927_DE = 26757
    PCS_NAD_1927_FL_E = 26758
    PCS_NAD_1927_FL_W = 26759
    PCS_NAD_1927_FL_N = 26760
    PCS_NAD_1927_GA_E = 26766
    PCS_NAD_1927_GA_W = 26767
    PCS_NAD_1927_HI_1 = 26761
    PCS_NAD_1927_HI_2 = 26762
    PCS_NAD_1927_HI_3 = 26763
    PCS_NAD_1927_HI_4 = 26764
    PCS_NAD_1927_HI_5 = 26765
    PCS_NAD_1927_ID_E = 26768
    PCS_NAD_1927_ID_C = 26769
    PCS_NAD_1927_ID_W = 26770
    PCS_NAD_1927_IL_E = 26771
    PCS_NAD_1927_IL_W = 26772
    PCS_NAD_1927_IN_E = 26773
    PCS_NAD_1927_IN_W = 26774
    PCS_NAD_1927_IA_N = 26775
    PCS_NAD_1927_IA_S = 26776
    PCS_NAD_1927_KS_N = 26777
    PCS_NAD_1927_KS_S = 26778
    PCS_NAD_1927_KY_N = 26779
    PCS_NAD_1927_KY_S = 26780
    PCS_NAD_1927_LA_N = 26781
    PCS_NAD_1927_LA_S = 26782
    PCS_NAD_1927_ME_E = 26783
    PCS_NAD_1927_ME_W = 26784
    PCS_NAD_1927_MD = 26785
    PCS_NAD_1927_MA_M = 26786
    PCS_NAD_1927_MA_I = 26787
    PCS_NAD_1927_MI_N = 26788
    PCS_NAD_1927_MI_C = 26789
    PCS_NAD_1927_MI_S = 26790
    PCS_NAD_1927_MN_N = 26791
    PCS_NAD_1927_MN_C = 26792
    PCS_NAD_1927_MN_S = 26793
    PCS_NAD_1927_MS_E = 26794
    PCS_NAD_1927_MS_W = 26795
    PCS_NAD_1927_MO_E = 26796
    PCS_NAD_1927_MO_C = 26797
    PCS_NAD_1927_MO_W = 26798
    PCS_AMERSFOORT_RD_NEW = 28992
    PCS_NAD_1927_MT_N = 32001
    PCS_NAD_1927_MT_C = 32002
    PCS_NAD_1927_MT_S = 32003
    PCS_NAD_1927_NE_N = 32005
    PCS_NAD_1927_NE_S = 32006
    PCS_NAD_1927_NV_E = 32007
    PCS_NAD_1927_NV_C = 32008
    PCS_NAD_1927_NV_W = 32009
    PCS_NAD_1927_NH = 32010
    PCS_NAD_1927_NJ = 32011
    PCS_NAD_1927_NM_E = 32012
    PCS_NAD_1927_NM_C = 32013
    PCS_NAD_1927_NM_W = 32014
    PCS_NAD_1927_NY_E = 32015
    PCS_NAD_1927_NY_C = 32016
    PCS_NAD_1927_NY_W = 32017
    PCS_NAD_1927_NY_LI = 32018
    PCS_NAD_1927_NC = 32019
    PCS_NAD_1927_ND_N = 32020
    PCS_NAD_1927_ND_S = 32021
    PCS_NAD_1927_OH_N = 32022
    PCS_NAD_1927_OH_S = 32023
    PCS_NAD_1927_OK_N = 32024
    PCS_NAD_1927_OK_S = 32025
    PCS_NAD_1927_OR_N = 32026
    PCS_NAD_1927_OR_S = 32027
    PCS_NAD_1927_PA_N = 32028
    PCS_NAD_1927_PA_S = 32029
    PCS_NAD_1927_RI = 32030
    PCS_NAD_1927_SC_N = 32031
    PCS_NAD_1927_SC_S = 32033
    PCS_NAD_1927_SD_N = 32034
    PCS_NAD_1927_SD_S = 32035
    PCS_NAD_1927_TN = 32036
    PCS_NAD_1927_TX_N = 32037
    PCS_NAD_1927_TX_NC = 32038
    PCS_NAD_1927_TX_C = 32039
    PCS_NAD_1927_TX_SC = 32040
    PCS_NAD_1927_TX_S = 32041
    PCS_NAD_1927_UT_N = 32042
    PCS_NAD_1927_UT_C = 32043
    PCS_NAD_1927_UT_S = 32044
    PCS_NAD_1927_VT = 32045
    PCS_NAD_1927_VA_N = 32046
    PCS_NAD_1927_VA_S = 32047
    PCS_NAD_1927_WA_N = 32048
    PCS_NAD_1927_WA_S = 32049
    PCS_NAD_1927_WV_N = 32050
    PCS_NAD_1927_WV_S = 32051
    PCS_NAD_1927_WI_N = 32052
    PCS_NAD_1927_WI_C = 32053
    PCS_NAD_1927_WI_S = 32054
    PCS_NAD_1927_WY_E = 32055
    PCS_NAD_1927_WY_EC = 32056
    PCS_NAD_1927_WY_WC = 32057
    PCS_NAD_1927_WY_W = 32058
    PCS_NAD_1927_PR = 32059
    PCS_NAD_1927_VI = 32060
    PCS_NAD_1927_GU = 65061
    PCS_NAD_1983_AL_E = 26929
    PCS_NAD_1983_AL_W = 26930
    PCS_NAD_1983_AK_1 = 26931
    PCS_NAD_1983_AK_2 = 26932
    PCS_NAD_1983_AK_3 = 26933
    PCS_NAD_1983_AK_4 = 26934
    PCS_NAD_1983_AK_5 = 26935
    PCS_NAD_1983_AK_6 = 26936
    PCS_NAD_1983_AK_7 = 26937
    PCS_NAD_1983_AK_8 = 26938
    PCS_NAD_1983_AK_9 = 26939
    PCS_NAD_1983_AK_10 = 26940
    PCS_NAD_1983_AZ_E = 26948
    PCS_NAD_1983_AZ_C = 26949
    PCS_NAD_1983_AZ_W = 26950
    PCS_NAD_1983_AR_N = 26951
    PCS_NAD_1983_AR_S = 26952
    PCS_NAD_1983_CA_I = 26941
    PCS_NAD_1983_CA_II = 26942
    PCS_NAD_1983_CA_III = 26943
    PCS_NAD_1983_CA_IV = 26944
    PCS_NAD_1983_CA_V = 26945
    PCS_NAD_1983_CA_VI = 26946
    PCS_NAD_1983_CO_N = 26953
    PCS_NAD_1983_CO_C = 26954
    PCS_NAD_1983_CO_S = 26955
    PCS_NAD_1983_CT = 26956
    PCS_NAD_1983_DE = 26957
    PCS_NAD_1983_FL_E = 26958
    PCS_NAD_1983_FL_W = 26959
    PCS_NAD_1983_FL_N = 26960
    PCS_NAD_1983_GA_E = 26966
    PCS_NAD_1983_GA_W = 26967
    PCS_NAD_1983_HI_1 = 26961
    PCS_NAD_1983_HI_2 = 26962
    PCS_NAD_1983_HI_3 = 26963
    PCS_NAD_1983_HI_4 = 26964
    PCS_NAD_1983_HI_5 = 26965
    PCS_NAD_1983_ID_E = 26968
    PCS_NAD_1983_ID_C = 26969
    PCS_NAD_1983_ID_W = 26970
    PCS_NAD_1983_IL_E = 26971
    PCS_NAD_1983_IL_W = 26972
    PCS_NAD_1983_IN_E = 26973
    PCS_NAD_1983_IN_W = 26974
    PCS_NAD_1983_IA_N = 26975
    PCS_NAD_1983_IA_S = 26976
    PCS_NAD_1983_KS_N = 26977
    PCS_NAD_1983_KS_S = 26978
    PCS_NAD_1983_KY_N = 26979
    PCS_NAD_1983_KY_S = 26980
    PCS_NAD_1983_LA_N = 26981
    PCS_NAD_1983_LA_S = 26982
    PCS_NAD_1983_ME_E = 26983
    PCS_NAD_1983_ME_W = 26984
    PCS_NAD_1983_MD = 26985
    PCS_NAD_1983_MA_M = 26986
    PCS_NAD_1983_MA_I = 26987
    PCS_NAD_1983_MI_N = 26988
    PCS_NAD_1983_MI_C = 26989
    PCS_NAD_1983_MI_S = 26990
    PCS_NAD_1983_MN_N = 26991
    PCS_NAD_1983_MN_C = 26992
    PCS_NAD_1983_MN_S = 26993
    PCS_NAD_1983_MS_E = 26994
    PCS_NAD_1983_MS_W = 26995
    PCS_NAD_1983_MO_E = 26996
    PCS_NAD_1983_MO_C = 26997
    PCS_NAD_1983_MO_W = 26998
    PCS_NAD_1983_MT = 32100
    PCS_NAD_1983_NE = 32104
    PCS_NAD_1983_NV_E = 32107
    PCS_NAD_1983_NV_C = 32108
    PCS_NAD_1983_NV_W = 32109
    PCS_NAD_1983_NH = 32110
    PCS_NAD_1983_NJ = 32111
    PCS_NAD_1983_NM_E = 32112
    PCS_NAD_1983_NM_C = 32113
    PCS_NAD_1983_NM_W = 32114
    PCS_NAD_1983_NY_E = 32115
    PCS_NAD_1983_NY_C = 32116
    PCS_NAD_1983_NY_W = 32117
    PCS_NAD_1983_NY_LI = 32118
    PCS_NAD_1983_NC = 32119
    PCS_NAD_1983_ND_N = 32120
    PCS_NAD_1983_ND_S = 32121
    PCS_NAD_1983_OH_N = 32122
    PCS_NAD_1983_OH_S = 32123
    PCS_NAD_1983_OK_N = 32124
    PCS_NAD_1983_OK_S = 32125
    PCS_NAD_1983_OR_N = 32126
    PCS_NAD_1983_OR_S = 32127
    PCS_NAD_1983_PA_N = 32128
    PCS_NAD_1983_PA_S = 32129
    PCS_NAD_1983_RI = 32130
    PCS_NAD_1983_SC = 32133
    PCS_NAD_1983_SD_N = 32134
    PCS_NAD_1983_SD_S = 32135
    PCS_NAD_1983_TN = 32136
    PCS_NAD_1983_TX_N = 32137
    PCS_NAD_1983_TX_NC = 32138
    PCS_NAD_1983_TX_C = 32139
    PCS_NAD_1983_TX_SC = 32140
    PCS_NAD_1983_TX_S = 32141
    PCS_NAD_1983_UT_N = 32142
    PCS_NAD_1983_UT_C = 32143
    PCS_NAD_1983_UT_S = 32144
    PCS_NAD_1983_VT = 32145
    PCS_NAD_1983_VA_N = 32146
    PCS_NAD_1983_VA_S = 32147
    PCS_NAD_1983_WA_N = 32148
    PCS_NAD_1983_WA_S = 32149
    PCS_NAD_1983_WV_N = 32150
    PCS_NAD_1983_WV_S = 32151
    PCS_NAD_1983_WI_N = 32152
    PCS_NAD_1983_WI_C = 32153
    PCS_NAD_1983_WI_S = 32154
    PCS_NAD_1983_WY_E = 32155
    PCS_NAD_1983_WY_EC = 32156
    PCS_NAD_1983_WY_WC = 32157
    PCS_NAD_1983_WY_W = 32158
    PCS_NAD_1983_PR_VI = 32161
    PCS_NAD_1983_GU = 65161
    PCS_ADINDAN_UTM_37N = 20137
    PCS_ADINDAN_UTM_38N = 20138
    PCS_AFGOOYE_UTM_38N = 20538
    PCS_AFGOOYE_UTM_39N = 20539
    PCS_AIN_EL_ABD_UTM_37N = 20437
    PCS_AIN_EL_ABD_UTM_38N = 20438
    PCS_AIN_EL_ABD_UTM_39N = 20439
    PCS_ARATU_UTM_22S = 20822
    PCS_ARATU_UTM_23S = 20823
    PCS_ARATU_UTM_24S = 20824
    PCS_BATAVIA_UTM_48S = 21148
    PCS_BATAVIA_UTM_49S = 21149
    PCS_BATAVIA_UTM_50S = 21150
    PCS_BOGOTA_UTM_17N = 21817
    PCS_BOGOTA_UTM_18N = 21818
    PCS_CAMACUPA_UTM_32S = 22032
    PCS_CAMACUPA_UTM_33S = 22033
    PCS_CARTHAGE_UTM_32N = 22332
    PCS_CORREGO_ALEGRE_UTM_23S = 22523
    PCS_CORREGO_ALEGRE_UTM_24S = 22524
    PCS_DATUM_73_UTM_ZONE_29N = 27429
    PCS_DOUALA_UTM_32N = 22832
    PCS_FAHUD_UTM_39N = 23239
    PCS_FAHUD_UTM_40N = 23240
    PCS_GAROUA_UTM_33N = 23433
    PCS_GGRS_1987_GREEK_GRID = 2100
    PCS_ID_1974_UTM_46N = 23846
    PCS_ID_1974_UTM_47N = 23847
    PCS_ID_1974_UTM_48N = 23848
    PCS_ID_1974_UTM_49N = 23849
    PCS_ID_1974_UTM_50N = 23850
    PCS_ID_1974_UTM_51N = 23851
    PCS_ID_1974_UTM_52N = 23852
    PCS_ID_1974_UTM_53N = 23853
    PCS_ID_1974_UTM_46S = 23886
    PCS_ID_1974_UTM_47S = 23887
    PCS_ID_1974_UTM_48S = 23888
    PCS_ID_1974_UTM_49S = 23889
    PCS_ID_1974_UTM_50S = 23890
    PCS_ID_1974_UTM_51S = 23891
    PCS_ID_1974_UTM_52S = 23892
    PCS_ID_1974_UTM_53S = 23893
    PCS_ID_1974_UTM_54S = 23894
    PCS_INDIAN_1954_UTM_47N = 23947
    PCS_INDIAN_1954_UTM_48N = 23948
    PCS_INDIAN_1975_UTM_47N = 24047
    PCS_INDIAN_1975_UTM_48N = 24048
    PCS_KERTAU_UTM_47N = 24547
    PCS_KERTAU_UTM_48N = 24548
    PCS_LA_CANOA_UTM_20N = 24720
    PCS_LA_CANOA_UTM_21N = 24721
    PCS_LOME_UTM_31N = 25231
    PCS_MPORALOKO_UTM_32N = 26632
    PCS_MPORALOKO_UTM_32S = 26692
    PCS_MALONGO_1987_UTM_32S = 25932
    PCS_MASSAWA_UTM_37N = 26237
    PCS_MHAST_UTM_32S = 26432
    PCS_MINNA_UTM_31N = 26331
    PCS_MINNA_UTM_32N = 26332
    PCS_NAHRWAN_1967_UTM_38N = 27038
    PCS_NAHRWAN_1967_UTM_39N = 27039
    PCS_NAHRWAN_1967_UTM_40N = 27040
    PCS_NGN_UTM_38N = 31838
    PCS_NGN_UTM_39N = 31839
    PCS_NORD_SAHARA_UTM_29N = 30729
    PCS_NORD_SAHARA_UTM_30N = 30730
    PCS_NORD_SAHARA_UTM_31N = 30731
    PCS_NORD_SAHARA_UTM_32N = 30732
    PCS_NAPARIMA_1972_UTM_20N = 27120
    PCS_POINTE_NOIRE_UTM_32S = 28232
    PCS_PSAD_1956_UTM_18N = 24818
    PCS_PSAD_1956_UTM_19N = 24819
    PCS_PSAD_1956_UTM_20N = 24820
    PCS_PSAD_1956_UTM_21N = 24821
    PCS_PSAD_1956_UTM_17S = 24877
    PCS_PSAD_1956_UTM_18S = 24878
    PCS_PSAD_1956_UTM_19S = 24879
    PCS_PSAD_1956_UTM_20S = 24880
    PCS_SAPPER_HILL_UTM_20S = 29220
    PCS_SAPPER_HILL_UTM_21S = 29221
    PCS_SCHWARZECK_UTM_33S = 29333
    PCS_SUDAN_UTM_35N = 29635
    PCS_SUDAN_UTM_36N = 29636
    PCS_TANANARIVE_UTM_38S = 29738
    PCS_TANANARIVE_UTM_39S = 29739
    PCS_TC_1948_UTM_39N = 30339
    PCS_TC_1948_UTM_40N = 30340
    PCS_TIMBALAI_1948_UTM_49N = 29849
    PCS_TIMBALAI_1948_UTM_50N = 29850
    PCS_YOFF_1972_UTM_28N = 31028
    PCS_ZANDERIJ_1972_UTM_21N = 31121
    PCS_KUDAMS_KTM = 31900
    PCS_LUZON_PHILIPPINES_I = 25391
    PCS_LUZON_PHILIPPINES_II = 25392
    PCS_LUZON_PHILIPPINES_III = 25393
    PCS_LUZON_PHILIPPINES_IV = 25394
    PCS_LUZON_PHILIPPINES_V = 25395
    PCS_MGI_FERRO_AUSTRIA_WEST = 31291
    PCS_MGI_FERRO_AUSTRIA_CENTRAL = 31292
    PCS_MGI_FERRO_AUSTRIA_EAST = 31293
    PCS_MONTE_MARIO_ROME_ITALY_1 = 26591
    PCS_MONTE_MARIO_ROME_ITALY_2 = 26592
    PCS_C_INCHAUSARGENTINA_1 = 22191
    PCS_C_INCHAUSARGENTINA_2 = 22192
    PCS_C_INCHAUSARGENTINA_3 = 22193
    PCS_C_INCHAUSARGENTINA_4 = 22194
    PCS_C_INCHAUSARGENTINA_5 = 22195
    PCS_C_INCHAUSARGENTINA_6 = 22196
    PCS_C_INCHAUSARGENTINA_7 = 22197
    PCS_DHDN_GERMANY_1 = 31491
    PCS_DHDN_GERMANY_2 = 31492
    PCS_DHDN_GERMANY_3 = 31493
    PCS_DHDN_GERMANY_4 = 31494
    PCS_DHDN_GERMANY_5 = 31495
    PCS_AIN_EL_ABD_BAHRAIN_GRID = 20499
    PCS_BOGOTA_COLOMBIA_WEST = 21891
    PCS_BOGOTA_COLOMBIA_BOGOTA = 21892
    PCS_BOGOTA_COLOMBIA_E_CENTRAL = 21893
    PCS_BOGOTA_COLOMBIA_EAST = 21894
    PCS_EGYPT_RED_BELT = 22992
    PCS_EGYPT_PURPLE_BELT = 22993
    PCS_EGYPT_EXT_PURPLE_BELT = 22994
    PCS_LEIGON_GHANA_GRID = 25000
    PCS_TM65_IRISH_GRID = 29900
    PCS_NZGD_1949_NORTH_ISLAND = 27291
    PCS_NZGD_1949_SOUTH_ISLAND = 27292
    PCS_MINNA_NIGERIA_WEST_BELT = 26391
    PCS_MINNA_NIGERIA_MID_BELT = 26392
    PCS_MINNA_NIGERIA_EAST_BELT = 26393
    PCS_PSAD_1956_PERU_WEST = 24891
    PCS_PSAD_1956_PERU_CENTRAL = 24892
    PCS_PSAD_1956_PERU_EAST = 24893
    PCS_LISBON_PORTUGUESE_GRID = 20700
    PCS_QATAR_GRID = 28600
    PCS_OSGB_1936_BRITISH_GRID = 27700
    PCS_RT38_STOCKHOLM_SWEDISH_GRID = 30800
    PCS_VOIROL_N_ALGERIE_ANCIENNE = 30491
    PCS_VOIROL_S_ALGERIE_ANCIENNE = 30492
    PCS_VOIROL_UNIFIE_N_ALGERIE = 30591
    PCS_VOIROL_UNIFIE_S_ALGERIE = 30592
    PCS_ATF_NORD_DE_GUERRE = 27500
    PCS_NTF_FRANCE_I = 27581
    PCS_NTF_FRANCE_II = 27582
    PCS_NTF_FRANCE_III = 27583
    PCS_NTF_FRANCE_IV = 27584
    PCS_NTF_NORD_FRANCE = 27591
    PCS_NTF_CENTRE_FRANCE = 27592
    PCS_NTF_SUD_FRANCE = 27593
    PCS_NTF_CORSE = 27594
    PCS_KALIANPUR_INDIA_0 = 24370
    PCS_KALIANPUR_INDIA_I = 24371
    PCS_KALIANPUR_INDIA_IIA = 24372
    PCS_KALIANPUR_INDIA_IIB = 24382
    PCS_KALIANPUR_INDIA_IIIA = 24373
    PCS_KALIANPUR_INDIA_IIIB = 24383
    PCS_KALIANPUR_INDIA_IVA = 24374
    PCS_KALIANPUR_INDIA_IVB = 24384
    PCS_JAMAICA_1875_OLD_GRID = 24100
    PCS_JAD_1969_JAMAICA_GRID = 24200
    PCS_MERCHICH_NORD_MAROC = 26191
    PCS_MERCHICH_SUD_MAROC = 26192
    PCS_MERCHICH_SAHARA = 26193
    PCS_CARTHAGE_NORD_TUNISIE = 22391
    PCS_CARTHAGE_SUD_TUNISIE = 22392
    PCS_KOC_LAMBERT = 24600
    PCS_BELGE_LAMBERT_1950 = 21500
    PCS_DEALUL_PISCULUI_1933_STEREO_33 = 31600
    PCS_DEALUL_PISCULUI_1970_STEREO_EALUL_PISCULUI_1970_STEREO_70 = 31700
    PCS_BEIJING_1954_3_DEGREE_GK_25 = 2401
    PCS_BEIJING_1954_3_DEGREE_GK_26 = 2402
    PCS_BEIJING_1954_3_DEGREE_GK_27 = 2403
    PCS_BEIJING_1954_3_DEGREE_GK_28 = 2404
    PCS_BEIJING_1954_3_DEGREE_GK_29 = 2405
    PCS_BEIJING_1954_3_DEGREE_GK_30 = 2406
    PCS_BEIJING_1954_3_DEGREE_GK_31 = 2407
    PCS_BEIJING_1954_3_DEGREE_GK_32 = 2408
    PCS_BEIJING_1954_3_DEGREE_GK_33 = 2409
    PCS_BEIJING_1954_3_DEGREE_GK_34 = 2410
    PCS_BEIJING_1954_3_DEGREE_GK_35 = 2411
    PCS_BEIJING_1954_3_DEGREE_GK_36 = 2412
    PCS_BEIJING_1954_3_DEGREE_GK_37 = 2413
    PCS_BEIJING_1954_3_DEGREE_GK_38 = 2414
    PCS_BEIJING_1954_3_DEGREE_GK_39 = 2415
    PCS_BEIJING_1954_3_DEGREE_GK_40 = 2416
    PCS_BEIJING_1954_3_DEGREE_GK_41 = 2417
    PCS_BEIJING_1954_3_DEGREE_GK_42 = 2418
    PCS_BEIJING_1954_3_DEGREE_GK_43 = 2419
    PCS_BEIJING_1954_3_DEGREE_GK_44 = 2420
    PCS_BEIJING_1954_3_DEGREE_GK_45 = 2421
    PCS_BEIJING_1954_3_DEGREE_GK_25N = 2422
    PCS_BEIJING_1954_3_DEGREE_GK_26N = 2423
    PCS_BEIJING_1954_3_DEGREE_GK_27N = 2424
    PCS_BEIJING_1954_3_DEGREE_GK_28N = 2425
    PCS_BEIJING_1954_3_DEGREE_GK_29N = 2426
    PCS_BEIJING_1954_3_DEGREE_GK_30N = 2427
    PCS_BEIJING_1954_3_DEGREE_GK_31N = 2428
    PCS_BEIJING_1954_3_DEGREE_GK_32N = 2429
    PCS_BEIJING_1954_3_DEGREE_GK_33N = 2430
    PCS_BEIJING_1954_3_DEGREE_GK_34N = 2431
    PCS_BEIJING_1954_3_DEGREE_GK_35N = 2432
    PCS_BEIJING_1954_3_DEGREE_GK_36N = 2433
    PCS_BEIJING_1954_3_DEGREE_GK_37N = 2434
    PCS_BEIJING_1954_3_DEGREE_GK_38N = 2435
    PCS_BEIJING_1954_3_DEGREE_GK_39N = 2436
    PCS_BEIJING_1954_3_DEGREE_GK_40N = 2437
    PCS_BEIJING_1954_3_DEGREE_GK_41N = 2438
    PCS_BEIJING_1954_3_DEGREE_GK_42N = 2439
    PCS_BEIJING_1954_3_DEGREE_GK_43N = 2440
    PCS_BEIJING_1954_3_DEGREE_GK_44N = 2441
    PCS_BEIJING_1954_3_DEGREE_GK_45N = 2442
    PCS_CHINA_2000_GK_13 = 21513
    PCS_CHINA_2000_GK_14 = 21514
    PCS_CHINA_2000_GK_15 = 21515
    PCS_CHINA_2000_GK_16 = 21516
    PCS_CHINA_2000_GK_17 = 21517
    PCS_CHINA_2000_GK_18 = 21518
    PCS_CHINA_2000_GK_19 = 21519
    PCS_CHINA_2000_GK_20 = 21520
    PCS_CHINA_2000_GK_21 = 21521
    PCS_CHINA_2000_GK_22 = 21522
    PCS_CHINA_2000_GK_23 = 21523
    PCS_CHINA_2000_GK_13N = 21573
    PCS_CHINA_2000_GK_14N = 21574
    PCS_CHINA_2000_GK_15N = 21575
    PCS_CHINA_2000_GK_16N = 21576
    PCS_CHINA_2000_GK_17N = 21577
    PCS_CHINA_2000_GK_18N = 21578
    PCS_CHINA_2000_GK_19N = 21579
    PCS_CHINA_2000_GK_20N = 21580
    PCS_CHINA_2000_GK_21N = 21581
    PCS_CHINA_2000_GK_22N = 21582
    PCS_CHINA_2000_GK_23N = 21583
    PCS_CHINA_2000_3_DEGREE_GK_25 = 21625
    PCS_CHINA_2000_3_DEGREE_GK_26 = 21626
    PCS_CHINA_2000_3_DEGREE_GK_27 = 21627
    PCS_CHINA_2000_3_DEGREE_GK_28 = 21628
    PCS_CHINA_2000_3_DEGREE_GK_29 = 21629
    PCS_CHINA_2000_3_DEGREE_GK_30 = 21630
    PCS_CHINA_2000_3_DEGREE_GK_31 = 21631
    PCS_CHINA_2000_3_DEGREE_GK_32 = 21632
    PCS_CHINA_2000_3_DEGREE_GK_33 = 21633
    PCS_CHINA_2000_3_DEGREE_GK_34 = 21634
    PCS_CHINA_2000_3_DEGREE_GK_35 = 21635
    PCS_CHINA_2000_3_DEGREE_GK_36 = 21636
    PCS_CHINA_2000_3_DEGREE_GK_37 = 21637
    PCS_CHINA_2000_3_DEGREE_GK_38 = 21638
    PCS_CHINA_2000_3_DEGREE_GK_39 = 21639
    PCS_CHINA_2000_3_DEGREE_GK_40 = 21640
    PCS_CHINA_2000_3_DEGREE_GK_41 = 21641
    PCS_CHINA_2000_3_DEGREE_GK_42 = 21642
    PCS_CHINA_2000_3_DEGREE_GK_43 = 21643
    PCS_CHINA_2000_3_DEGREE_GK_44 = 21644
    PCS_CHINA_2000_3_DEGREE_GK_45 = 21645
    PCS_CHINA_2000_3_DEGREE_GK_25N = 21675
    PCS_CHINA_2000_3_DEGREE_GK_26N = 21676
    PCS_CHINA_2000_3_DEGREE_GK_27N = 21677
    PCS_CHINA_2000_3_DEGREE_GK_28N = 21678
    PCS_CHINA_2000_3_DEGREE_GK_29N = 21679
    PCS_CHINA_2000_3_DEGREE_GK_30N = 21680
    PCS_CHINA_2000_3_DEGREE_GK_31N = 21681
    PCS_CHINA_2000_3_DEGREE_GK_32N = 21682
    PCS_CHINA_2000_3_DEGREE_GK_33N = 21683
    PCS_CHINA_2000_3_DEGREE_GK_34N = 21684
    PCS_CHINA_2000_3_DEGREE_GK_35N = 21685
    PCS_CHINA_2000_3_DEGREE_GK_36N = 21686
    PCS_CHINA_2000_3_DEGREE_GK_37N = 21687
    PCS_CHINA_2000_3_DEGREE_GK_38N = 21688
    PCS_CHINA_2000_3_DEGREE_GK_39N = 21689
    PCS_CHINA_2000_3_DEGREE_GK_40N = 21690
    PCS_CHINA_2000_3_DEGREE_GK_41N = 21691
    PCS_CHINA_2000_3_DEGREE_GK_42N = 21692
    PCS_CHINA_2000_3_DEGREE_GK_43N = 21693
    PCS_CHINA_2000_3_DEGREE_GK_44N = 21694
    PCS_CHINA_2000_3_DEGREE_GK_45N = 21695
    PCS_XIAN_1980_GK_13 = 2327
    PCS_XIAN_1980_GK_14 = 2328
    PCS_XIAN_1980_GK_15 = 2329
    PCS_XIAN_1980_GK_16 = 2330
    PCS_XIAN_1980_GK_17 = 2331
    PCS_XIAN_1980_GK_18 = 2332
    PCS_XIAN_1980_GK_19 = 2333
    PCS_XIAN_1980_GK_20 = 2334
    PCS_XIAN_1980_GK_21 = 2335
    PCS_XIAN_1980_GK_22 = 2336
    PCS_XIAN_1980_GK_23 = 2337
    PCS_XIAN_1980_GK_13N = 2338
    PCS_XIAN_1980_GK_14N = 2339
    PCS_XIAN_1980_GK_15N = 2340
    PCS_XIAN_1980_GK_16N = 2341
    PCS_XIAN_1980_GK_17N = 2342
    PCS_XIAN_1980_GK_18N = 2343
    PCS_XIAN_1980_GK_19N = 2344
    PCS_XIAN_1980_GK_20N = 2345
    PCS_XIAN_1980_GK_21N = 2346
    PCS_XIAN_1980_GK_22N = 2347
    PCS_XIAN_1980_GK_23N = 2348
    PCS_XIAN_1980_3_DEGREE_GK_25 = 2349
    PCS_XIAN_1980_3_DEGREE_GK_26 = 2350
    PCS_XIAN_1980_3_DEGREE_GK_27 = 2351
    PCS_XIAN_1980_3_DEGREE_GK_28 = 2352
    PCS_XIAN_1980_3_DEGREE_GK_29 = 2353
    PCS_XIAN_1980_3_DEGREE_GK_30 = 2354
    PCS_XIAN_1980_3_DEGREE_GK_31 = 2355
    PCS_XIAN_1980_3_DEGREE_GK_32 = 2356
    PCS_XIAN_1980_3_DEGREE_GK_33 = 2357
    PCS_XIAN_1980_3_DEGREE_GK_34 = 2358
    PCS_XIAN_1980_3_DEGREE_GK_35 = 2359
    PCS_XIAN_1980_3_DEGREE_GK_36 = 2360
    PCS_XIAN_1980_3_DEGREE_GK_37 = 2361
    PCS_XIAN_1980_3_DEGREE_GK_38 = 2362
    PCS_XIAN_1980_3_DEGREE_GK_39 = 2363
    PCS_XIAN_1980_3_DEGREE_GK_40 = 2364
    PCS_XIAN_1980_3_DEGREE_GK_41 = 2365
    PCS_XIAN_1980_3_DEGREE_GK_42 = 2366
    PCS_XIAN_1980_3_DEGREE_GK_43 = 2367
    PCS_XIAN_1980_3_DEGREE_GK_44 = 2368
    PCS_XIAN_1980_3_DEGREE_GK_45 = 2369
    PCS_XIAN_1980_3_DEGREE_GK_25N = 2370
    PCS_XIAN_1980_3_DEGREE_GK_26N = 2371
    PCS_XIAN_1980_3_DEGREE_GK_27N = 2372
    PCS_XIAN_1980_3_DEGREE_GK_28N = 2373
    PCS_XIAN_1980_3_DEGREE_GK_29N = 2374
    PCS_XIAN_1980_3_DEGREE_GK_30N = 2375
    PCS_XIAN_1980_3_DEGREE_GK_31N = 2376
    PCS_XIAN_1980_3_DEGREE_GK_32N = 2377
    PCS_XIAN_1980_3_DEGREE_GK_33N = 2378
    PCS_XIAN_1980_3_DEGREE_GK_34N = 2379
    PCS_XIAN_1980_3_DEGREE_GK_35N = 2380
    PCS_XIAN_1980_3_DEGREE_GK_36N = 2381
    PCS_XIAN_1980_3_DEGREE_GK_37N = 2382
    PCS_XIAN_1980_3_DEGREE_GK_38N = 2383
    PCS_XIAN_1980_3_DEGREE_GK_39N = 2384
    PCS_XIAN_1980_3_DEGREE_GK_40N = 2385
    PCS_XIAN_1980_3_DEGREE_GK_41N = 2386
    PCS_XIAN_1980_3_DEGREE_GK_42N = 2387
    PCS_XIAN_1980_3_DEGREE_GK_43N = 2388
    PCS_XIAN_1980_3_DEGREE_GK_44N = 2389
    PCS_XIAN_1980_3_DEGREE_GK_45N = 2390
    PCS_KERTAU_MALAYA_METERS = 23110
    PCS_TIMBALAI_1948_RSO_BORNEO = 23130
    PCS_WGS_1984_WORLD_MERCATOR = 3395
    PCS_LISBON_PORTUGUESE_OFFICIAL_GRID = 20791
    PCS_DATUM73_MODIFIED_PORTUGUESE_NATIONAL_GRID = 27492
    PCS_DATUM73_MODIFIED_PORTUGUESE_GRID = 27493
    PCS_Lisboa_Hayford_Gauss_IGeoE = 53700
    PCS_Lisboa_Hayford_Gauss_IPCC = 53791
    PCS_ETRS89_PORTUGAL_TM06 = 3763
    PCS_LISBON_1890_PORTUGAL_BONNE = 61008
    PCS_AZORES_OCCIDENTAL_1939_UTM_ZONE_25N = 2188
    PCS_AZORES_CENTRAL_1948_UTM_ZONE_26N = 2189
    PCS_AZORES_ORIENTAL_1940_UTM_ZONE_26N = 2190
    PCS_MADEIRA_1936_UTM_ZONE_28N = 2191
    PCS_ED50_ORIENTAL_GROUP = 61001
    PCS_ED50_CENTRAL_GROUP = 61002
    PCS_ED50_OCCIDENTAL_GROUP = 61003
    PCS_PTRA08_UTM28_ITRF93 = 61004
    PCS_PTRA08_UTM26_ITRF93 = 61006
    PCS_PTRA08_UTM25_ITRF93 = 61007

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.PrjCoordSysType"


@unique
class GeoCoordSysType(JEnum):
    GCS_USER_DEFINE = -1
    GCS_AIRY_1830 = 4001
    GCS_AIRY_MOD = 4002
    GCS_AUSTRALIAN = 4003
    GCS_BESSEL_1841 = 4004
    GCS_BESSEL_MOD = 4005
    GCS_BESSEL_NAMIBIA = 4006
    GCS_CLARKE_1858 = 4007
    GCS_CLARKE_1866 = 4008
    GCS_CLARKE_1866_MICH = 4009
    GCS_CLARKE_1880_BENOIT = 4010
    GCS_CLARKE_1880_IGN = 4011
    GCS_CLARKE_1880_RGS = 4012
    GCS_CLARKE_1880_ARC = 4013
    GCS_CLARKE_1880_SGA = 4014
    GCS_EVEREST_1830 = 4015
    GCS_EVEREST_DEF_1967 = 4016
    GCS_EVEREST_DEF_1975 = 4017
    GCS_EVEREST_MOD = 4018
    GCS_GRS_1980 = 4019
    GCS_HELMERT_1906 = 4020
    GCS_INDONESIAN = 4021
    GCS_INTERNATIONAL_1924 = 4022
    GCS_INTERNATIONAL_1967 = 4023
    GCS_KRASOVSKY_1940 = 4024
    GCS_NWL_9D = 4025
    GCS_PLESSIS_1817 = 4027
    GCS_STRUVE_1860 = 4028
    GCS_WAR_OFFICE = 4029
    GCS_GEM_10C = 4031
    GCS_OSU_86F = 4032
    GCS_OSU_91A = 4033
    GCS_CLARKE_1880 = 4034
    GCS_SPHERE = 4035
    GCS_GRS_1967 = 4036
    GCS_WGS_1966 = 37001
    GCS_FISCHER_1960 = 37002
    GCS_FISCHER_1968 = 37003
    GCS_FISCHER_MOD = 37004
    GCS_HOUGH_1960 = 37005
    GCS_EVEREST_MOD_1969 = 37006
    GCS_WALBECK = 37007
    GCS_SPHERE_AI = 37008
    GCS_GREEK = 4120
    GCS_GGRS_1987 = 4121
    GCS_ATS_1977 = 4122
    GCS_KKJ = 4123
    GCS_PULKOVO_1995 = 4200
    GCS_ADINDAN = 4201
    GCS_AGD_1966 = 4202
    GCS_AGD_1984 = 4203
    GCS_AIN_EL_ABD_1970 = 4204
    GCS_AFGOOYE = 4205
    GCS_AGADEZ = 4206
    GCS_LISBON = 4207
    GCS_ARATU = 4208
    GCS_ARC_1950 = 4209
    GCS_ARC_1960 = 4210
    GCS_BATAVIA = 4211
    GCS_BARBADOS = 4212
    GCS_BEDUARAM = 4213
    GCS_BEIJING_1954 = 4214
    GCS_BELGE_1950 = 4215
    GCS_BERMUDA_1957 = 4216
    GCS_BERN_1898 = 4217
    GCS_BOGOTA = 4218
    GCS_BUKIT_RIMPAH = 4219
    GCS_CAMACUPA = 4220
    GCS_CAMPO_INCHAUSPE = 4221
    GCS_CAPE = 4222
    GCS_CARTHAGE = 4223
    GCS_CHUA = 4224
    GCS_CORREGO_ALEGRE = 4225
    GCS_COTE_D_IVOIRE = 4226
    GCS_DEIR_EZ_ZOR = 4227
    GCS_DOUALA = 4228
    GCS_EGYPT_1907 = 4229
    GCS_ED_1950 = 4230
    GCS_ED_1987 = 4231
    GCS_FAHUD = 4232
    GCS_GANDAJIKA_1970 = 4233
    GCS_GAROUA = 4234
    GCS_GUYANE_FRANCAISE = 4235
    GCS_HU_TZU_SHAN = 4236
    GCS_HUNGARIAN_1972 = 4237
    GCS_INDONESIAN_1974 = 4238
    GCS_INDIAN_1954 = 4239
    GCS_INDIAN_1975 = 4240
    GCS_JAMAICA_1875 = 4241
    GCS_JAMAICA_1969 = 4242
    GCS_KALIANPUR = 4243
    GCS_KANDAWALA = 4244
    GCS_KERTAU = 4245
    GCS_KOC_ = 4246
    GCS_LA_CANOA = 4247
    GCS_PSAD_1956 = 4248
    GCS_LAKE = 4249
    GCS_LEIGON = 4250
    GCS_LIBERIA_1964 = 4251
    GCS_LOME = 4252
    GCS_LUZON_1911 = 4253
    GCS_HITO_XVIII_1963 = 4254
    GCS_HERAT_NORTH = 4255
    GCS_MAHE_1971 = 4256
    GCS_MAKASSAR = 4257
    GCS_ETRS_1989 = 4258
    GCS_MALONGO_1987 = 4259
    GCS_MANOCA = 4260
    GCS_MERCHICH = 4261
    GCS_MASSAWA = 4262
    GCS_MINNA = 4263
    GCS_MHAST = 4264
    GCS_MONTE_MARIO = 4265
    GCS_MPORALOKO = 4266
    GCS_NAD_1927 = 4267
    GCS_NAD_MICH = 4268
    GCS_NAD_1983 = 4269
    GCS_NAHRWAN_1967 = 4270
    GCS_NAPARIMA_1972 = 4271
    GCS_NZGD_1949 = 4272
    GCS_NGO_1948_ = 4273
    GCS_DATUM_73 = 4274
    GCS_NTF_ = 4275
    GCS_NSWC_9Z_2_ = 4276
    GCS_OSGB_1936 = 4277
    GCS_OSGB_1970_SN = 4278
    GCS_OS_SN_1980 = 4279
    GCS_PADANG_1884 = 4280
    GCS_PALESTINE_1923 = 4281
    GCS_POINTE_NOIRE = 4282
    GCS_GDA_1994 = 4283
    GCS_PULKOVO_1942 = 4284
    GCS_QATAR = 4285
    GCS_QATAR_1948 = 4286
    GCS_QORNOQ = 4287
    GCS_LOMA_QUINTANA = 4288
    GCS_AMERSFOORT = 4289
    GCS_SAD_1969 = 4291
    GCS_SAPPER_HILL_1943 = 4292
    GCS_SCHWARZECK = 4293
    GCS_SEGORA = 4294
    GCS_SERINDUNG = 4295
    GCS_SUDAN = 4296
    GCS_TANANARIVE_1925 = 4297
    GCS_TIMBALAI_1948 = 4298
    GCS_TM65 = 4299
    GCS_TM75 = 4300
    GCS_TOKYO = 4301
    GCS_TRINIDAD_1903 = 4302
    GCS_TRUCIAL_COAST_1948 = 4303
    GCS_VOIROL_1875 = 4304
    GCS_VOIROL_UNIFIE_1960 = 4305
    GCS_BERN_1938 = 4306
    GCS_NORD_SAHARA_1959 = 4307
    GCS_RT38_ = 4308
    GCS_YACARE = 4309
    GCS_YOFF = 4310
    GCS_ZANDERIJ = 4311
    GCS_MGI_ = 4312
    GCS_BELGE_1972 = 4313
    GCS_DHDNB = 4314
    GCS_CONAKRY_1905 = 4315
    GCS_DEALUL_PISCULUI_1933 = 4316
    GCS_DEALUL_PISCULUI_1970 = 4317
    GCS_NGN = 4318
    GCS_KUDAMS = 4319
    GCS_WGS_1972 = 4322
    GCS_WGS_1972_BE = 4324
    GCS_WGS_1984 = 4326
    GCS_BERN_1898_BERN = 4801
    GCS_BOGOTA_BOGOTA = 4802
    GCS_LISBON_LISBON = 4803
    GCS_MAKASSAR_JAKARTA = 4804
    GCS_MGI_FERRO = 4805
    GCS_MONTE_MARIO_ROME = 4806
    GCS_NTF_PARIS = 4807
    GCS_PADANG_1884_JAKARTA = 4808
    GCS_BELGE_1950_BRUSSELS = 4809
    GCS_TANANARIVE_1925_PARIS = 4810
    GCS_VOIROL_1875_PARIS = 4811
    GCS_VOIROL_UNIFIE_1960_PARIS = 4812
    GCS_BATAVIA_JAKARTA = 4813
    GCS_RT38_STOCKHOLM = 4814
    GCS_GREEK_ATHENS = 4815
    GCS_ATF_PARIS = 4901
    GCS_NDG_PARIS = 4902
    GCS_EUROPEAN_1979 = 37201
    GCS_EVEREST_BANGLADESH = 37202
    GCS_EVEREST_INDIA_NEPAL = 37203
    GCS_HJORSEY_1955 = 37204
    GCS_HONG_KONG_1963 = 37205
    GCS_OMAN = 37206
    GCS_S_ASIA_SINGAPORE = 37207
    GCS_AYABELLE = 37208
    GCS_BISSAU = 37209
    GCS_DABOLA = 37210
    GCS_POINT58 = 37211
    GCS_BEACON_E_1945 = 37212
    GCS_TERN_ISLAND_1961 = 37213
    GCS_ASTRO_1952 = 37214
    GCS_BELLEVUE = 37215
    GCS_CANTON_1966 = 37216
    GCS_CHATHAM_ISLAND_1971 = 37217
    GCS_DOS_1968 = 37218
    GCS_EASTER_ISLAND_1967 = 37219
    GCS_GUAM_1963 = 37220
    GCS_GUX_1 = 37221
    GCS_JOHNSTON_ISLAND_1961 = 37222
    GCS_CARTHAGE_DEGREE = 37223
    GCS_MIDWAY_1961 = 37224
    GCS_OLD_HAWAIIAN = 37225
    GCS_PITCAIRN_1967 = 37226
    GCS_SANTO_DOS_1965 = 37227
    GCS_VITI_LEVU_1916 = 37228
    GCS_WAKE_ENIWETOK_1960 = 37229
    GCS_WAKE_ISLAND_1952 = 37230
    GCS_ANNA_1_1965 = 37231
    GCS_GAN_1970 = 37232
    GCS_ISTS_073_1969 = 37233
    GCS_KERGUELEN_ISLAND_1949 = 37234
    GCS_REUNION = 37235
    GCS_ANTIGUA_ISLAND_1943 = 37236
    GCS_ASCENSION_ISLAND_1958 = 37237
    GCS_DOS_71_4 = 37238
    GCS_CACANAVERAL = 37239
    GCS_FORT_THOMAS_1955 = 37240
    GCS_GRACIOSA_1948 = 37241
    GCS_ISTS_061_1968 = 37242
    GCS_LC5_1961 = 37243
    GCS_MONTSERRAT_ISLAND_1958 = 37244
    GCS_OBSERV_METEOR_1939 = 37245
    GCS_PICO_DE_LAS_NIEVES = 37246
    GCS_PORTO_SANTO_1936 = 37247
    GCS_PUERTO_RICO = 37248
    GCS_SAO_BRAZ = 37249
    GCS_SELVAGEM_GRANDE_1938 = 37250
    GCS_TRISTAN_1968 = 37251
    GCS_SAMOA_1962 = 37252
    GCS_CAMP_AREA = 37253
    GCS_DECEPTION_ISLAND = 37254
    GCS_GUNUNG_SEGARA = 37255
    GCS_INDIAN_1960 = 37256
    GCS_S42_HUNGARY = 37257
    GCS_S_JTSK = 37258
    GCS_KUSAIE_1951 = 37259
    GCS_ALASKAN_ISLANDS = 37260
    GCS_JAPAN_2000 = 37301
    GCS_XIAN_1980 = 37312
    GCS_CHINA_2000 = 37313
    GCS_AZORES_OCCIDENTAL_1939 = 4182
    GCS_AZORES_CENTRAL_1948 = 4183
    GCS_AZORES_ORIENTAL_1940 = 4184
    GCS_MADEIRA_1936 = 4185
    GCS_ITRF_1993 = 4915
    GCS_LISBON_1890 = 4904

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.GeoCoordSysType"


@unique
class ProjectionType(JEnum):
    PRJ_NONPROJECTION = 43000
    PRJ_PLATE_CARREE = 43001
    PRJ_EQUIDISTANT_CYLINDRICAL = 43002
    PRJ_MILLER_CYLINDRICAL = 43003
    PRJ_MERCATOR = 43004
    PRJ_GAUSS_KRUGER = 43005
    PRJ_TRANSVERSE_MERCATOR = 43006
    PRJ_ALBERS = 43007
    PRJ_SINUSOIDAL = 43008
    PRJ_MOLLWEIDE = 43009
    PRJ_ECKERT_VI = 43010
    PRJ_ECKERT_V = 43011
    PRJ_ECKERT_IV = 43012
    PRJ_ECKERT_III = 43013
    PRJ_ECKERT_II = 43014
    PRJ_ECKERT_I = 43015
    PRJ_GALL_STEREOGRAPHIC = 43016
    PRJ_BEHRMANN = 43017
    PRJ_WINKEL_I = 43018
    PRJ_WINKEL_II = 43019
    PRJ_LAMBERT_CONFORMAL_CONIC = 43020
    PRJ_POLYCONIC = 43021
    PRJ_QUARTIC_AUTHALIC = 43022
    PRJ_LOXIMUTHAL = 43023
    PRJ_BONNE = 43024
    PRJ_HOTINE = 43025
    PRJ_STEREOGRAPHIC = 43026
    PRJ_EQUIDISTANT_CONIC = 43027
    PRJ_CASSINI = 43028
    PRJ_VAN_DER_GRINTEN_I = 43029
    PRJ_ROBINSON = 43030
    PRJ_TWO_POINT_EQUIDISTANT = 43031
    PRJ_EQUIDISTANT_AZIMUTHAL = 43032
    PRJ_LAMBERT_AZIMUTHAL_EQUAL_AREA = 43033
    PRJ_CONFORMAL_AZIMUTHAL = 43034
    PRJ_ORTHO_GRAPHIC = 43035
    PRJ_GNOMONIC = 43036
    PRJ_CHINA_AZIMUTHAL = 43037
    PRJ_SANSON = 43040
    PRJ_EQUALAREA_CYLINDRICAL = 43041
    PRJ_HOTINE_AZIMUTH_NATORIGIN = 43042
    PRJ_OBLIQUE_MERCATOR = 43043
    PRJ_HOTINE_OBLIQUE_MERCATOR = 43044
    PRJ_SPHERE_MERCATOR = 43045
    PRJ_BONNE_SOUTH_ORIENTATED = 43046
    PRJ_OBLIQUE_STEREOGRAPHIC = 43047
    PRJ_BAIDU_MERCATOR = 43048
    PRJ_RECTIFIED_SKEWED_ORTHOMORPHIC = 43049

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.ProjectionType"


class GeoSpatialRefType(JEnum):
    __doc__ = "\n    该类定义了空间坐标系类型常量。\n\n    空间坐标系类型，用以区分平面坐标系、地理坐标系、投影坐标系，其中地理坐标系又称为经纬度坐标系。\n\n    :var GeoSpatialRefType.SPATIALREF_NONEARTH: 平面坐标系。当坐标系为平面坐标系时，不能进行投影转换。\n    :var GeoSpatialRefType.SPATIALREF_EARTH_LONGITUDE_LATITUDE: 地理坐标系。地理坐标系由大地参照系、中央经线、坐标单位组成。在地理坐标系中，单位可以是度，分，秒。东西向（水平方向）的范围为-180度至180度。南北向（垂直方向）的范围为-90度至90度。\n    :var GeoSpatialRefType.SPATIALREF_EARTH_PROJECTION: 投影坐标系。投影坐标系统由地图投影方式、投影参数、坐标单位和地理坐标系组成。SuperMap Objects Java 中提供了很多预定义的投影系统，用户可以直接使用，此外，用户还可以定制自己的投影系统。\n    "
    SPATIALREF_NONEARTH = 0
    SPATIALREF_EARTH_LONGITUDE_LATITUDE = 1
    SPATIALREF_EARTH_PROJECTION = 2

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.GeoSpatialRefType"


@unique
class BufferEndType(JEnum):
    __doc__ = "\n    该类定义了缓冲区端点类型常量。\n\n    用以区分线对象缓冲区分析时的端点是圆头缓冲还是平头缓冲。\n\n    :var BufferEndType.ROUND: 圆头缓冲。圆头缓冲区是在生成缓冲区时，在线段的端点处做半圆弧处理\n    :var BufferEndType.FLAT: 平头缓冲。平头缓冲区是在生成缓冲区时，在线段的端点处做圆弧的垂线。\n    "
    ROUND = 1
    FLAT = 2

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialanalyst.BufferEndType"


@unique
class OverlayMode(JEnum):
    __doc__ = "\n    叠加分析模式类型\n\n    * 裁剪（CLIP）\n\n        用于对数据集进行擦除方式的叠加分析，将第一个数据集中包含在第二个数据集内的对象裁剪并删除。\n\n        * 裁剪数据集（第二数据集）的类型必须是面，被剪裁的数据集（第一数据集）可以是点、线、面。\n        * 在被裁剪数据集中，只有落在裁剪数据集多边形内的对象才会被输出到结果数据集中。\n        * 裁剪数据集、被裁剪数据集以及结果数据集的地理坐标系必须一致。\n        * clip 与 intersect 在空间处理上是一致的，不同在于对结果记录集属性的处理，clip 分析只是用来做裁剪，结果记录集与第一个记录集的属性表结构相同，此处叠加分析参数对象设置无效。而 intersect 求交分析的结果则可以根据字段设置情况来保留两个记录集的字段。\n        * 所有叠加分析的结果都不考虑数据集的系统字段。\n\n        .. image:: ../image/OverlayClip.png\n\n    * 擦除（ERASE）\n\n        用于对数据集进行同一方式的叠加分析，结果数据集中保留被同一运算的数据集的全部对象和被同一运算的数据集与用来进行同一运算的数据集相交的对象。\n\n        * 擦除数据集（第二数据集）的类型必须是面，被擦除的数据集（第一数据集）可以是点、线、面数据集。\n        * 擦除数据集中的多边形集合定义了擦除区域，被擦除数据集中凡是落在这些多边形区域内的特征都将被去除，而落在多边形区域外的特征要素都将被输出到结果数据集中，与 clip 运算相反。\n        * 擦除数据集、被擦除数据集以及结果数据集的地理坐标系必须一致。\n\n        .. image:: ../image/OverlayErase.png\n\n    * 同一（IDENTITY）\n\n        用于对数据集进行同一方式的叠加分析，结果数据集中保留被同一运算的数据集的全部对象和被同一运算的数据集与用来进行同一运算的数据集相交的对象。\n\n        * 同一运算就是第一数据集与第二数据集先求交，然后求交结果再与第一数据集求并的一个运算。其中，第二数据集的类型必须是面，第一数据集的类型可以是点、线、面数据集。如果第一个数据集为点数集，则新生成的数据集中保留第一个数据集的所有对象；如果第一个数据集为线数据集，则新生成的数据集中保留第一个数据集的所有对象，但是把与第二个数据集相交的对象在相交的地方打断；如果第一个数据集为面数据集，则结果数据集保留以第一数据集为控制边界之内的所有多边形，并且把与第二个数据集相交的对象在相交的地方分割成多个对象。\n        * identiy 运算与 union 运算有相似之处，所不同之处在于 union 运算保留了两个数据集的所有部分，而 identity 运算是把第一个数据集中与第二个数据集不相交的部分进行保留。identity 运算的结果属性表来自于两个数据集的属性表。\n        * 用于进行同一运算的数据集、被同一运算的数据集以及结果数据集的地理坐标系必须一致。\n\n        .. image:: ../image/OverlayIdentity.png\n\n    * 相交（INTERSECT）\n\n        进行相交方式的叠加分析，将被相交叠加分析的数据集中不包含在用来相交叠加分析的数据集中的对象切割并删除。即两个数据集中重叠的部分将被输出到结果数据集中，其余部分将被排除。\n\n        * 被相交叠加分析的数据集可以是点类型、线类型和面类型，用来相交叠加分析的数据集必须是面类型。第一数据集的特征对象（点、线和面）在与第二数据集中的多边形相交处被分裂（点对象除外），分裂结果被输出到结果数据集中。\n        * 求交运算与裁剪运算得到的结果数据集的空间几何信息相同的，但是裁剪运算不对属性表做任何处理，而求交运算可以让用户选择需要保留的属性字段。\n        * 用于相交叠加分析的数据集、被相交叠加分析的数据集以及结果数据集的地理坐标系必须一致。\n\n        .. image:: ../image/OverlayIntersect.png\n\n    * 对称差（XOR）\n\n        对两个面数据集进行对称差分析运算。即交集取反运算。\n\n        * 用于对称差分析的数据集、被对称差分析的数据集以及结果数据集的地理坐标系必须一致。\n        * 对称差运算是两个数据集的异或运算。操作的结果是，对于每一个面对象，去掉其与另一个数据集中的几何对象相交的部分，而保留剩下的部分。对称差运算的输出结果的属性表包含两个输入数据集的非系统属性字段。\n\n        .. image:: ../image/OverlayXOR.png\n\n    * 合并（UNION）\n\n        用于对两个面数据集进行合并方式的叠加分析，结果数据集中保存被合并叠加分析的数据集和用于合并叠加分析的数据集中的全部对象，并且对相交部分进行求交和分割运算。 注意：\n\n        * 合并是求两个数据集并的运算，合并后的图层保留两个数据集所有图层要素，只限于两个面数据集之间进行。\n        * 进行 union 运算后，两个面数据集在相交处多边形被分割，且两个数据集的几何和属性信息都被输出到结果数据集中。\n        * 用于合并叠加分析的数据集、被合并叠加分析的数据集以及结果数据集的地理坐标系必须一致。\n\n        .. image:: ../image/OverlayUnion.png\n\n    * 更新（UPDATE）\n\n        用于对两个面数据集进行更新方式的叠加分析, 更新运算是用用于更新的数据集替换与被更新数据集的重合部分，是一个先擦除后粘贴的过程。\n\n        * 用于更新叠加分析的数据集、被更新叠加分析的数据集以及结果数据集的地理坐标系必须一致。\n        * 第一数据集与第二数据集的类型都必须是面数据集。结果数据集中保留了更新数据集的几何形状和属性信息。\n\n        .. image:: ../image/OverlayUpdate.png\n\n    :var OverlayMode.CLIP: 裁剪\n    :var OverlayMode.ERASE: 擦除\n    :var OverlayMode.IDENTITY: 同一\n    :var OverlayMode.INTERSECT: 相交\n    :var OverlayMode.XOR: 对称差\n    :var OverlayMode.UNION: 合并\n    :var OverlayMode.UPDATE: 更新\n    "
    CLIP = 1
    ERASE = 2
    IDENTITY = 3
    INTERSECT = 4
    XOR = 5
    UNION = 6
    UPDATE = 7


@unique
class DissolveType(JEnum):
    __doc__ = "\n    融合类型常量\n\n    :var DissolveType.ONLYMULTIPART: 组合。将融合字段值相同的对象合并成一个复杂对象。\n    :var DissolveType.SINGLE: 融合。将融合字段值相同且拓扑邻近的对象合并成一个简单对象。\n    :var DissolveType.MULTIPART: 融合后组合。将融合字段值相同且拓扑邻近的对象合并成一个简单对象，然后将融合字段值相同的非邻近对象组合成一个复杂对象。\n    "
    ONLYMULTIPART = 1
    SINGLE = 2
    MULTIPART = 3

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialanalyst.DissolveType"


@unique
class StatisticsType(JEnum):
    __doc__ = "\n    字段统计类型常量\n\n    :var StatisticsType.MAX: 统计字段的最大值\n    :var StatisticsType.MIN: 统计字段的最小值\n    :var StatisticsType.SUM: 统计字段的和\n    :var StatisticsType.MEAN: 统计字段的平均值\n    :var StatisticsType.FIRST: 保留第一个对象的字段值\n    :var StatisticsType.LAST: 保留最后一个对象的字段值。\n    "
    MAX = 1
    MIN = 2
    SUM = 3
    MEAN = 4
    FIRST = 5
    LAST = 6

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialanalyst.StatisticsType"


@unique
class StatisticsFieldType(JEnum):
    __doc__ = "\n    点抽稀的统计类型，统计的是抽稀点原始点集的值\n\n    :var StatisticsFieldType.AVERAGE:  统计平均值\n    :var StatisticsFieldType.SUM: 统计和\n    :var StatisticsFieldType.MAXVALUE: 最大值\n    :var StatisticsFieldType.MINVALUE:  最小值\n    :var StatisticsFieldType.VARIANCE: 方差\n    :var StatisticsFieldType.SAMPLEVARIANCE: 样本方差\n    :var StatisticsFieldType.STDDEVIATION: 标准差\n    :var StatisticsFieldType.SAMPLESTDDEV: 样本标准差\n    "
    AVERAGE = 1
    SUM = 2
    MAXVALUE = 3
    MINVALUE = 4
    VARIANCE = 5
    SAMPLEVARIANCE = 6
    STDDEVIATION = 7
    SAMPLESTDDEV = 8

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialanalyst.StatisticsFieldType"

    @classmethod
    def _externals(cls):
        return {'mean':StatisticsFieldType.AVERAGE,  'max':StatisticsFieldType.MAXVALUE, 
         'min':StatisticsFieldType.MINVALUE, 
         'var':StatisticsFieldType.VARIANCE, 
         'stdev':StatisticsFieldType.STDDEVIATION}


@unique
class VectorResampleType(JEnum):
    __doc__ = "\n    矢量数据集重采样方法类型常量\n\n    :var VectorResampleType.RTBEND: 使用光栏采样算法进行重采样\n    :var VectorResampleType.RTGENERAL: 使用道格拉斯算法进行重采样\n    "
    RTBEND = 1
    RTGENERAL = 2

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.ResampleType"


@unique
class RasterResampleMode(JEnum):
    __doc__ = "\n    栅格重采样计算方式的类型常量\n\n    :var RasterResampleMode.NEAREST:  最邻近法。最邻近法是将最邻近的栅格值赋予新栅格。该方法的优点是不会改变原始栅格值，简单且处理速度快，但该种方法最大会有半个格子大小的位移。适用于表示分类或某种专题的离散数据，如土地利用，植被类型等。\n    :var RasterResampleMode.BILINEAR:  双线性内插法。双线性内插使用内插点在输入栅格中的 4 邻域进行加权平均来计算新栅格值，权值根据 4 邻域中每个格子中心距内插点的距离来决定。该种方法的重采样结果会比最邻近法的结果更光滑，但会改变原来的栅格值。适用于表示某种现象分布、地形表面的连续数据，如 DEM、气温、降雨量分布、坡度等，这些数据本来就是通过采样点内插得到的连续表面。\n    :var RasterResampleMode.CUBIC: 三次卷积内插法。三次卷积内插法较为复杂，与双线性内插相似，同样会改变栅格值，不同之处在于它使用 16 邻域来加权计算，会使计算结果得到一些锐化的效果。该种方法同样会改变原来的栅格值，且有可能会超出输入栅格的值域范围，且计算量大。适用于航片和遥感影像的重采样。\n\n    "
    NEAREST = 0
    BILINEAR = 1
    CUBIC = 2

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialanalyst.ResampleMode"


@unique
class AggregationType(JEnum):
    __doc__ = "\n    定义了聚合操作时结果栅格的计算方式类型常量\n\n    :var AggregationType.SUM: 一个聚合栅格内包含的所有栅格值之和\n    :var AggregationType.MIN: 一个聚合栅格内包含的所有栅格值中的最小值\n    :var AggregationType.MAX: 一个聚合栅格内包含的所有栅格值中的最大值\n    :var AggregationType.AVERRAGE: 一个聚合栅格内包含的所有栅格值中的平均值\n    :var AggregationType.MEDIAN: 一个聚合栅格内包含的所有栅格值中的中值\n    "
    SUM = 0
    MIN = 1
    MAX = 2
    AVERRAGE = 3
    MEDIAN = 4

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialanalyst.AggregationType"


@unique
class _AttributeStatisticsType(JEnum):
    VALUE = 1
    AVERAGE = 2
    SUM = 3
    MAXVALUE = 4
    MINVALUE = 5
    MINID = 6
    MAXID = 7
    MAXAREA = 8
    VARIANCE = 9
    STDDEVIATION = 10
    SAMPLEVARIANCE = 11
    SAMPLESTDDEV = 12
    MODALVALUE = 13


@unique
class _SpatialRelationType(JEnum):
    CONTAIN = 1
    WITHIN = 2
    INTERSECT = 3

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.SpatialRelationType"


@unique
class ArcAndVertexFilterMode(JEnum):
    __doc__ = "\n    该类定义了弧段求交过滤模式常量。\n\n    弧段求交用于将线对象在相交处打断，通常是对线数据建立拓扑关系时的首要步骤。\n\n    :var ArcAndVertexFilterMode.NONE: 不过滤，即在所有交点处打断线对象。该模式下设置过滤线表达式或过滤点数据集均无效。\n                                      如下图所示，线对象 A、B、C、D 在它们的相交处分别打断，即 A、B 在它们相交处分别被打断，C 在与 A、D 的相交处被打断。\n\n                                      .. image:: ../image/FilterMode_None.png\n\n    :var ArcAndVertexFilterMode.ARC: 仅由过滤线表达式过滤，即过滤线表达式查询出的线对象不打断。该模式下设置过滤点记录集无效。\n                                     如下图所示，线对象 C 是满足过滤线表达式的对象，则线对象 C 整条线不会在任何位置被打断。\n\n                                     .. image:: ../image/FilterMode_Arc.png\n\n    :var ArcAndVertexFilterMode.VERTEX:  仅由过滤点记录集过滤，即线对象在过滤点所在位置（或与过滤点的距离在容限范围内）处不打断。该模式下设置过滤线表达式无效。\n                                         如下图所示，某个过滤点位于线对象 A 和 C 在相交处，则在该处 C 不会被打断，其他相交位置仍会打断。\n\n                                         .. image:: ../image/FilterMode_Vertex.png\n\n    :var ArcAndVertexFilterMode.ARC_AND_VERTEX: 由过滤线表达式和过滤点记录集共同决定哪些位置不打断，二者为且的关系，即只有过滤线表达式查询出的线对象在过滤点位置处（或二者在容限范围内）不打断。\n                                                如下图所示，线对象 C 是满足过滤线表达式的对象，A、B 相交处，C、D 相交处分别有一个过滤点，根据该模式规则，过滤线上过滤点所在的位置不会被打断，即 C 在与 D 的相交处不打断。\n\n                                                .. image:: ../image/FilterMode_ArcAndVertex.png\n\n    :var ArcAndVertexFilterMode.ARC_OR_VERTEX: 过滤线表达式查询出的线对象以及过滤点位置处（或与过滤点距离在容限范围内）的线对象不打断，二者为并的关系。\n                                               如下图所示，线对象 C 是满足过滤线表达式的对象，A、B 相交处，C、D 相交处分别有一个过滤点，根据该模式规则，结果如右图所示，C 整体不被打断，A、B 相交处也不打断。\n\n                                               .. image:: ../image/FilterMode_ArcOrVertex.png\n\n    "
    NONE = 1
    ARC = 2
    VERTEX = 3
    ARC_AND_VERTEX = 4
    ARC_OR_VERTEX = 5

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.topology.ArcAndVertexFilterMode"


@unique
class TextAlignment(JEnum):
    __doc__ = "\n    该类定义了文本对齐类型常量。\n\n    指定文本中的各子对象的对齐方式。文本对象的每个子对象的位置是由文本的锚点和文本的对齐方式共同确定的。当文本子对象的锚点固定，对齐方式确定文本子对象与锚点的相对位置，从而确定文本子对象的位置。\n\n    :var TextAlignment.TOPLEFT: 左上角对齐。当文本的对齐方式为左上角对齐时，文本子对象的最小外接矩形的左上角点在该文本子对象的锚点位置\n    :var TextAlignment.TOPCENTER: 顶部居中对齐。当文本的对齐方式为上面居中对齐时，文本子对象的最小外接矩形的上边线的中点在该文本子对象的锚点位置\n    :var TextAlignment.TOPRIGHT: 右上角对齐。当文本的对齐方式为右上角对齐时，文本子对象的最小外接矩形的右上角点在该文本子对象的锚点位置\n    :var TextAlignment.BASELINELEFT: 基准线左对齐。当文本的对齐方式为基准线左对齐时，文本子对象的基线的左端点在该文本子对象的锚点位置\n    :var TextAlignment.BASELINECENTER: 基准线居中对齐。当文本的对齐方式为基准线居中对齐时，文本子对象的基线的中点在该文本子对象的锚点位置\n    :var TextAlignment.BASELINERIGHT: 基准线右对齐。当文本的对齐方式为基准线右对齐时，文本子对象的基线的右端点在该文本子对象的锚点位置\n    :var TextAlignment.BOTTOMLEFT: 左下角对齐。当文本的对齐方式为左下角对齐时，文本子对象的最小外接矩形的左下角点在该文本子对象的锚点位置\n    :var TextAlignment.BOTTOMCENTER: 底部居中对齐。当文本的对齐方式为底线居中对齐时，文本子对象的最小外接矩形的底线的中点在该文本子对象的锚点位置\n    :var TextAlignment.BOTTOMRIGHT: 右下角对齐。当文本的对齐方式为右下角对齐时，文本子对象的最小外接矩形的右下角点在该文本子对象的锚点位置\n    :var TextAlignment.MIDDLELEFT: 左中对齐。当文本的对齐方式为左中对齐时，文本子对象的最小外接矩形的左边线的中点在该文本子对象的锚点位置\n    :var TextAlignment.MIDDLECENTER: 中心对齐。当文本的对齐方式为中心对齐时，文本子对象的最小外接矩形的中心点在该文本子对象的锚点位置\n    :var TextAlignment.MIDDLERIGHT: 右中对齐。当文本的对齐方式为右中对齐时，文本子对象的最小外接矩形的右边线的中点在该文本子对象的锚点位置\n\n    "
    TOPLEFT = 0
    TOPCENTER = 1
    TOPRIGHT = 2
    BASELINELEFT = 3
    BASELINECENTER = 4
    BASELINERIGHT = 5
    BOTTOMLEFT = 6
    BOTTOMCENTER = 7
    BOTTOMRIGHT = 8
    MIDDLELEFT = 9
    MIDDLECENTER = 10
    MIDDLERIGHT = 11

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.TextAlignment"


@unique
class StringAlignment(JEnum):
    __doc__ = "\n    该类定义了多行文本排版方式类型常量\n\n    :var StringAlignment.LEFT:  左对齐\n    :var StringAlignment.CENTER: 居中对齐\n    :var StringAlignment.RIGHT: 右对齐\n    :var StringAlignment.DISTRIBUTED: 分散对齐（两端对齐）\n    "
    LEFT = 0
    CENTER = 16
    RIGHT = 32
    DISTRIBUTED = 144

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.StringAlignment"


@unique
class SpatialQueryMode(JEnum):
    __doc__ = "\n    该类定义了空间查询操作模式类型常量。\n    空间查询是通过几何对象之间的空间位置关系来构建过滤条件的一种查询方式。例如：通过空间查询可以找到被包含在面中的空间对象，相离或者相邻的空间对象等。\n\n    :var SpatialQueryMode.NONE: 无空间查询\n    :var SpatialQueryMode.IDENTITY: 重合空间查询模式。返回被搜索图层中与搜索对象完全重合的对象。注意：搜索对象与被搜索对象的类型必须相同；且两个对象的交集不为空，搜索对象的边界及内部分别和被搜索对象的外部交集为空。\n                                    该关系适合的对象类型：\n\n                                    - 搜索对象：点、线、面；\n                                    - 被搜索对象：点、线、面。\n\n                                    如图：\n\n                                     .. image:: ../image/SQIdentical.png\n\n    :var SpatialQueryMode.DISJOINT: 分离空间查询模式。返回被搜索图层中与搜索对象相离的对象。注意：搜索对象和被搜索对象相离，即无任何交集。\n                                    该关系适合的对象类型：\n\n                                    - 搜索对象：点、线、面；\n                                    - 被搜索对象：点、线、面。\n\n                                     如图：\n\n                                      .. image:: ../image/SQDsjoint.png\n\n    :var SpatialQueryMode.INTERSECT: 相交空间查询模式。返回与搜索对象相交的所有对象。注意：如果搜索对象是面，返回全部或部分被搜索对象包含的对象以及全部或部分包含搜索对象的对象；如果搜索对象不是面，返回全部或部分包含搜索对象的对象。\n                                     该关系适合的对象类型：\n\n                                     - 搜索对象：点、线、面；\n                                     - 被搜索对象：点、线、面。\n\n                                     如图：\n\n                                      .. image:: ../image/SQIntersect.png\n\n    :var SpatialQueryMode.TOUCH: 邻接空间查询模式。返回被搜索图层中其边界与搜索对象边界相触的对象。注意：搜索对象和被搜索对象的内部交集为空。\n                                 该关系不适合的对象类型为：\n\n                                 - 点查询点的空间关系。\n\n                                 如图：\n\n                                  .. image:: ../image/SQTouch.png\n\n    :var SpatialQueryMode.OVERLAP: 叠加空间查询模式。返回被搜索图层中与搜索对象部分重叠的对象。\n                                   该关系适合的对象类型为：\n\n                                   - 线/线，面/面。其中，两个几何对象的维数必须一致，而且他们交集的维数也应该和几何对象的维数一样\n\n                                   注意：点与任何一种几何对象都不存在部分重叠的情况\n\n                                   如图：\n\n                                    .. image:: ../image/SQOverlap.png\n\n    :var SpatialQueryMode.CROSS: 交叉空间查询模式。返回被搜索图层中与搜索对象（线）相交的所有对象（线或面）。注意：搜索对象和被搜索对象内部的交集不能为空；参与交叉（Cross）关系运算的两个对象必须有一个是线对象。\n                                 该关系适合的对象类型：\n\n                                 - 搜索对象：线；\n                                 - 被搜索对象：线、面。\n\n                                 如图：\n\n                                  .. image:: ../image/SQCross.png\n\n    :var SpatialQueryMode.WITHIN: 被包含空间查询模式。返回被搜索图层中完全包含搜索对象的对象。如果返回的对象是面，其必须全部包含（包括边接触）搜索对象；如果返回的对象是线，其必须完全包含搜索对象；如果返回的对象是点，其必须与搜索对象重合。该类型与包含（Contain）的查询模式正好相反。\n                                  该关系适合的对象类型：\n\n                                  - 搜索对象： 点、线、面；\n                                  - 被搜索对象： 点、线、面。\n\n                                  如图：\n\n                                   .. image:: ../image/SQWithin.png\n\n    :var SpatialQueryMode.CONTAIN: 包含空间查询模式。返回被搜索图层中完全被搜索对象包含的对象。注：搜索对象和被搜索对象的边界交集可以不为空；点查线/点查面/线查面，不存在包含情况。\n                                   该关系适合的对象类型：\n\n                                   - 搜索对象：点、线、面；\n                                   - 被搜索对象：点、线、面。\n\n                                   如图：\n\n                                    .. image:: ../image/SQContain.png\n\n    :var SpatialQueryMode.INNERINTERSECT: 内部相交查询模式，返回与搜索对象相交但不是仅接触的所有对象。也就是在相交算子的结果之上排除所有接触算子的结果。\n\n    "
    NONE = -1
    IDENTITY = 0
    DISJOINT = 1
    INTERSECT = 2
    TOUCH = 3
    OVERLAP = 4
    CROSS = 5
    WITHIN = 6
    CONTAIN = 7
    INNERINTERSECT = 13

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.SpatialQueryMode"


@unique
class JoinType(JEnum):
    __doc__ = "\n    该类定义了定义两个表之间连接类型常量。\n\n    该类用于对相连接的两个表之间进行查询时，决定了查询结果中得到的记录的情况\n\n    :var JoinType.INNERJOIN: 完全内连接，只有两个表中都有相关的记录才加入查询结果集。\n    :var JoinType.LEFTJOIN: 左连接，左边表中所有相关记录进入查询结果集，右边表中无相关的记录则其对应的字段值显示为空。\n    "
    INNERJOIN = 0
    LEFTJOIN = 1

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.JoinType"


@unique
class ReclassPixelFormat(JEnum):
    __doc__ = "\n    该类定义了栅格数据集的像元值的存储类型常量\n\n    :var ReclassPixelFormat.BIT32: 整型\n    :var ReclassPixelFormat.BIT64: 长整型\n    :var ReclassPixelFormat.SINGLE: 单精度\n    :var ReclassPixelFormat.DOUBLE: 双精度\n\n    "
    BIT32 = 320
    BIT64 = 64
    SINGLE = 3200
    DOUBLE = 6400

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialanalyst.ReclassPixelFormat"


@unique
class ReclassSegmentType(JEnum):
    __doc__ = "\n    该类定义了重分级区间类型常量。\n\n    :var ReclassSegmentType.OPENCLOSE: 左开右闭，如 (number1, number2]。\n    :var ReclassSegmentType.CLOSEOPEN: 左闭右开，如 [number1, number2）。\n\n    "
    OPENCLOSE = 0
    CLOSEOPEN = 1

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialanalyst.ReclassSegmentType"


@unique
class ReclassType(JEnum):
    __doc__ = "\n    该类定义了栅格重分级类型常量\n\n    :var ReclassType.UNIQUE: 单值重分级，即对指定的某些单值进行重新赋值。\n    :var ReclassType.RANGE: 范围重分级，即将一个区间内的值重新赋值为一个值。\n\n    "
    UNIQUE = 1
    RANGE = 2

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialanalyst.ReclassType"


@unique
class NeighbourShapeType(JEnum):
    __doc__ = "\n    :var NeighbourShapeType.RECTANGLE: 矩形邻域，矩形的大小由指定的宽和高来确定，矩形范围内的单元格参与邻域统计的计算。矩形邻域的默认宽和高均\n                                       为 0（单位为地理单位或栅格单位）。\n\n                                       .. image:: ../image/Rectangle.png\n\n    :var NeighbourShapeType.CIRCLE: 圆形邻域，圆形邻域的大小根据指定的半径来确定，圆形范围内的所有单元格都参与邻域处理，只要单元格有部分包含在\n                                    圆形范围内都将参与邻域统计。圆形邻域的默认半径为 0（单位为地理单位或栅格单位）。\n\n                                    .. image:: ../image/Circle.png\n\n    :var NeighbourShapeType.ANNULUS: 圆环邻域。环形邻域的大小根据指定的外圆半径和内圆半径来确定，环形区域内的单元格都参与邻域处理。环行邻域的\n                                    默认外圆半径和内圆半径均为 0（单位为地理单位或栅格单位）。\n\n                                    .. image:: ../image/Annulus.png\n\n    :var NeighbourShapeType.WEDGE: 扇形邻域。扇形邻域的大小根据指定的圆半径、起始角度和终止角度来确定。在扇形区内的所有单元格都参与邻域处理。\n                                   扇形邻域的默认半径为 0（单位为地理单位或栅格单位），起始角度和终止角度的默认值均为 0 度。\n\n                                   .. image:: ../image/Wedge.png\n\n    "
    RECTANGLE = 1
    CIRCLE = 2
    ANNULUS = 3
    WEDGE = 4

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialanalyst.NeighbourShapeType"


@unique
class SearchMode(JEnum):
    __doc__ = "\n    该类定义了内插时使用的样本点的查找方式类型常量。\n\n    对于同一种插值方法，样本点的选择方法不同，得到的插值结果也会不同。SuperMap 提供四种插值查找方式，分别为不进行查找，块（QUADTREE） 查找，定长查找（KDTREE_FIXED_RADIUS）和 变长查找（KDTREE_FIXED_COUNT）。\n\n    :var SearchMode.NONE: 不进行查找，使用所有的输入点进行内插分析。\n    :var SearchMode.QUADTREE: 块查找方式，即根据设置的每个块内的点的最多数量对数据集进行分块，使用块内的点进行插值运算。\n                              注意: 目前只对 Kriging、RBF 插值方法起作用，而对 IDW 插值方法不起作用。\n    :var SearchMode.KDTREE_FIXED_RADIUS: 定长查找方式，即指定半径范围内所有的采样点都参与栅格单元的插值运算。该方式由查找半径（search_radius）和\n                                         期望参与运算的最少样点数（expected_count）两个参数来最终确定参与运算的采样点。\n                                         当计算某个位置的未知数值时，会以该位置为圆心，以设定的定长值（即查找半径）为半径，落在这个范围内的\n                                         采样点都将参与运算；但如果设置了期望参与运算的最少点数，若查找半径范围内的点数达不到该数值，将自动\n                                         扩展查找半径直到找到指定的数目的采样点。\n    :var SearchMode.KDTREE_FIXED_COUNT: 变长查找方式，即距离栅格单元最近的指定数目的采样点参与插值运算。该方式由期望参与运算的最多样\n                                        点数（expected_count）和查找半径（search_radius）两个参数来最终确定参与运算的采样点。当计算某\n                                        个位置的未知数值时，会查找该位置附近的 N 个采样点，N 值即为设定的固定点数（即期望参与运算的最多样点\n                                        数），那么这 N 个采样点都将参与运算；但如果设置了查找半径，若半径范围内的点数少于设置的固定点数，则\n                                        范围之外的采样点被舍弃，不参与运算。\n    "
    NONE = 0
    QUADTREE = 1
    KDTREE_FIXED_RADIUS = 2
    KDTREE_FIXED_COUNT = 3

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialanalyst.SearchMode"


@unique
class Exponent(JEnum):
    __doc__ = "\n    该类定义了泛克吕金（UniversalKriging）插值时样点数据中趋势面方程的阶数的类型常量。样点数据集中样点之间固有的某种趋势，可以通过函数或者多项式的拟合呈现。\n\n    :var SearchMode.EXP1: 阶数为1，表示样点数据集中趋势面呈一阶趋势。\n    :var SearchMode.EXP2: 阶数为2，表示样点数据集中趋势面呈二阶趋势。\n\n    "
    EXP1 = 1
    EXP2 = 2

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialanalyst.Exponent"


@unique
class VariogramMode(JEnum):
    __doc__ = "\n    该类定义了克吕金（Kriging）插值时的半变函数类型常量。 定义克吕金（Kriging）插值时的半变函数类型。包括指数型、球型和高斯型。用户所选择的半变函\n    数类型会影响未知点的预测，特别是曲线在原点处的不同形状有重要意义。曲线在原点处越陡，则较近领域对该预测值的影响就越大。因此输出表面就会越不光滑。\n    每种类型都有各自适用的情况。\n\n    :var VariogramMode.EXPONENTIAL: 指数函数（Exponential Variogram Mode）。这种类型适用于在空间自相关关系随距离增加成指数递减的情况。\n                                    下图所示为空间自相关关系在无穷处完全消失。指数函数较为常用。\n\n                                    .. image:: ../image/VariogramMode_Exponential.png\n\n    :var VariogramMode.GAUSSIAN: 高斯函数（Gaussian Variogram Mode）。\n\n                                .. image:: ../image/variogrammode_Gaussian.png\n\n    :var VariogramMode.SPHERICAL: 球型函数（Spherical Variogram Mode）。这种类型显示了空间自相关关系逐渐减少的情况下（即半变函数值逐渐\n                                  增加），直到超出一定的距离，空间自相关关系为0。球型函数较为常用。\n\n                                  .. image:: ../image/VariogramMode_Spherical.png\n\n\n    "
    EXPONENTIAL = 0
    GAUSSIAN = 1
    SPHERICAL = 9

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialanalyst.VariogramMode"


@unique
class InterpolationAlgorithmType(JEnum):
    __doc__ = "\n    该类定义了插值分析所支持的算法的类型常量。\n\n    对于一个区域，如果只有部分离散点数据已知，要想创建或者模拟一个表面或者场，需要对未知点的值进行估计，通常采用的是内插表面的方法。SuperMap 中提供\n    三种内插方法，用于模拟或者创建一个表面，分别是：距离反比权重法（IDW）、克吕金插值方法（Kriging）、径向基函数插值法（RBF）。选用何种方法进行内\n    插，通常取决于样点数据的分布和要创建表面的类型。\n\n    :var InterpolationAlgorithmType.IDW: 距离反比权值（Inverse Distance Weighted）插值法。该方法通过计算附近区域离散点群的平均值来估算\n                                         单元格的值，生成栅格数据集。这是一种简单有效的数据内插方法，运算速度相对较快。距离离散中心越近的点，其估算值越受影响。\n    :var InterpolationAlgorithmType.SIMPLEKRIGING: 简单克吕金（Simple Kriging）插值法。简单克吕金是常用的克吕金插值方法之一，该方法假\n                                                   定用于插值的字段值的期望（平均值）已知的某一常数。\n    :var InterpolationAlgorithmType.KRIGING: 普通克吕金（Kriging）插值法。最常用的克吕金插值方法之一。该方法假定用于插值的字段值的期望（平\n                                             均值）未知且恒定。它利用一定的数学函数，通过对给定的空间点进行拟合来估算单元格的值，生\n                                             成格网数据集。它不仅可以生成一个表面，还可以给出预测结果的精度或者确定性的度量。因此，此方法计\n                                             算精度较高，常用于社会科学及地质学。\n    :var InterpolationAlgorithmType.UNIVERSALKRIGING: 泛克吕金（Universal Kriging）插值法。泛克吕金也是常用的克吕金插值方法之一，该\n                                                      方法假定用于插值的字段值的期望（平均值）未知的变量。在样点数据中存在某种主导趋势，并且该趋势可以通过某一个确定\n                                                      的函数或者多项式进行拟合的情况下适用泛克吕金插值法。\n    :var InterpolationAlgorithmType.RBF: 径向基函数（Radial Basis Function）插值法。该方法假设变化是平滑的，它有两个特点：\n\n                                         - 表面必须精确通过数据点；\n                                         - 表面必须有最小曲率。\n\n                                         该插值在创建有视觉要求的曲线和等高线方面有优势。\n    :var InterpolationAlgorithmType.DENSITY: 点密度（Density）插值法\n\n    "
    IDW = 0
    SIMPLEKRIGING = 1
    KRIGING = 2
    UNIVERSALKRIGING = 3
    RBF = 6
    DENSITY = 9

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialanalyst.InterpolationAlgorithmType"


@unique
class ComputeType(JEnum):
    __doc__ = "\n    该类定义了距离栅格最短路径分析的计算方式类型常量\n\n    :var ComputeType.CELL: 像元路径，目标对象对应的每一个栅格单元都生成一条最短路径。如下图所示，红色点作为源，黑线框多边形作为目标，采用该方式\n                           进行栅格最短路径分析，得到蓝色单元格表示的最短路径。\n\n                           .. image:: ../image/ComputeType_CELL.png\n\n    :var ComputeType.ZONE: 区域路径，每个目标对象对应的栅格区域都只生成一条最短路径。如下图所示，红色点作为源，黑线框多边形作为目标，采用该方\n                           式进行栅格最短路径分析，得到蓝色单元格表示的最短路径。\n\n                           .. image:: ../image/ComputeType_ZONE.png\n\n    :var ComputeType.ALL: 单一路径，所有目标对象对应的单元格只生成一条最短路径，即对于整个目标区域数据集来说所有路径中最短的那一条。如下图所示，\n                          红色点作为源，黑线框多边形作为目标，采用该方式进行栅格最短路径分析，得到蓝色单元格表示的最短路径。\n\n                          .. image:: ../image/ComputeType_ALL.png\n    "
    CELL = 0
    ZONE = 1
    ALL = 2

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialanalyst.ComputeType"


@unique
class SmoothMethod(JEnum):
    __doc__ = "\n    该类定义了光滑方法类型常量。用于从 Grid 或 DEM 数据生成等值线或等值面时对等值线或者等值面的边界线进行平滑。\n\n    等值线的生成是通过对原栅格数据进行插值，然后连接等值点得到，所以得到的结果是棱角分明的折线，等值面的生成是通过对原栅格数据进行插值，然后连接等值\n    点得到等值线，再由相邻等值线封闭组成的，所以得到的结果是棱角分明的多边形面，这两者均需要进行一定的光滑处理，SuperMap 提供两种光滑处理的方法，\n    B 样条法和磨角法。\n\n    :var SmoothMethod.NONE: 不进行光滑。\n    :var SmoothMethod.BSPLINE: B 样条法。B 样条法是以一条通过折线中一些节点的 B 样条曲线代替原始折线来达到光滑的目的。B 样条曲线是贝塞尔曲线\n                               的一种扩展。如下图所示，B 样条曲线不必通过原线对象的所有节点。除经过的原折线上的一些点外，曲线上的其他点通过\n                               B 样条函数拟合得出。\n\n                               .. image:: ../image/BSpline.png\n\n                               对非闭合的线对象使用 B 样条法后，其两端点的相对位置保持不变。\n    :var SmoothMethod.POLISH: 磨角法。磨角法是一种运算相对简单，处理速度比较快的光滑方法，但是效果比较局限。它的主要过程是将折线上的两条相邻的\n                              线段，分别在距离夹角顶点三分之一线段长度处添加节点，将夹角两侧新添加的两节点相连，从而将原线段的节点磨平，故称\n                              磨角法。下图为进行一次磨角法的过程示意图。\n\n                              .. image:: ../image/Polish.png\n\n                              可以多次磨角以得到接近光滑的线。对非闭合的线对象使用磨角法后，其两端点的相对位置保持不变。\n    "
    NONE = -1
    BSPLINE = 0
    POLISH = 1

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialanalyst.SmoothMethod"


@unique
class ShadowMode(JEnum):
    __doc__ = "\n    该类定义了晕渲图渲染方式类型常量。\n\n    :var ShadowMode.IllUMINATION_AND_SHADOW: 渲染和阴影。同时考虑当地的光照角以及阴影的作用。\n    :var ShadowMode.SHADOW: 阴影。只考虑区域是否位于阴影中。\n    :var ShadowMode.IllUMINATION: 渲染。只考虑当地的光照角。\n    "
    IllUMINATION_AND_SHADOW = 1
    SHADOW = 2
    IllUMINATION = 3

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialanalyst.ShadowMode"


@unique
class SlopeType(JEnum):
    __doc__ = "\n    该类定义了坡度的单位类型常量。\n\n    :var SlopeType.DEGREE: 以角度为单位来表示坡度。\n    :var SlopeType.RADIAN: 以弧度为单位来表示坡度。\n    :var SlopeType.PERCENT:  以百分数来表示坡度。 该百分数为垂直高度和水平距离的比值乘以100，即单位水平距离上的高度值乘以100， 或者说是坡度的正切值乘以100。\n    "
    DEGREE = 1
    RADIAN = 2
    PERCENT = 3

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialanalyst.SlopeType"


@unique
class StatisticMode(JEnum):
    __doc__ = "\n    该类定义了字段统计方法类型常量。对单一字段提供常用统计功能。SuperMap 提供的统计功能有6种，统计字段的最大值，最小值，平均值，总和，标准差以及方差。\n\n    :var StatisticMode.MAX: 统计所选字段的最大值。\n    :var StatisticMode.MIN: 统计所选字段的最小值。\n    :var StatisticMode.AVERAGE: 统计所选字段的平均值。\n    :var StatisticMode.SUM: 统计所选字段的总和。\n    :var StatisticMode.STDDEVIATION: 统计所选字段的标准差。\n    :var StatisticMode.VARIANCE: 统计所选字段的方差。\n    "
    MAX = 1
    MIN = 2
    AVERAGE = 3
    SUM = 4
    STDDEVIATION = 5
    VARIANCE = 6

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.StatisticMode"


@unique
class _FileType(JEnum):
    NONE = 0
    BMP = 121
    GRIB = 120
    PNG = 123
    TIF = 103
    JPG = 122
    GIF = 124
    IMG = 101
    GRD = 142
    GBDEM = 143
    USGSDEM = 144
    RAW = 161
    TEMSClutter = 146
    TEMSTEXT = 43
    SCV = 63
    COVERAGE = 6
    E00 = 7
    SHP = 8
    TAB = 11
    MIF = 12
    WOR = 13
    LIDAR = 17
    DXF = 3
    DWG = 2
    GML = 51
    KML = 53
    KMZ = 54
    MAPGIS = 55
    TEMSVector = 41
    TEMSBuildingVector = 42
    CSV = 64
    SDEVector = 68
    SDERaster = 69
    FileGDBVector = 70
    FileGDBRaster = 71
    SIT = 204
    DGN = 16
    VCT = 22
    GJB5068 = 73
    Model3DS = 501
    ModelX = 503
    ModelOSG = 505
    ModelDXF = 507
    ModelFBX = 508
    ModelOpenFlight = 509
    BIL = 141
    BIP = 148
    BSQ = 149
    ARCINFO_BINGRID = 145
    MrSID = 102
    ECW = 106
    JP2 = 150
    DBF = 61
    EGC = 205
    GeoPackage = 206
    ORANGETAB = 207
    GEOJSON = 74
    OSM = 75
    SimpleJson = 76
    VRT = 104

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.conversion.FileType"


@unique
class ImportMode(JEnum):
    __doc__ = "\n    该类定义了导入模式类型常量。用于控制在数据导入时出现的设置的目标对象（数据集等）名称已存在情况下，即设置的名称已有名称冲突时的操作模式。\n\n    :var ImportMode.NONE: 如存在名称冲突，则自动修改目标对象的名称后进行导入。\n    :var ImportMode.OVERWRITE: 如存在名称冲突，则进行强制覆盖。\n    :var ImportMode.APPEND: 如存在名称冲突，则进行数据集的追加。\n    "
    NONE = 0
    OVERWRITE = 1
    APPEND = 2

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.conversion.ImportMode"


@unique
class IgnoreMode(JEnum):
    __doc__ = "\n    该类定义了忽略颜色值模式的类型常量。\n\n    :var IgnoreMode.IGNORENONE: 不忽略颜色值。\n    :var IgnoreMode.IGNORESIGNAL: 按值忽略，忽略某个或某几个颜色值。\n    :var IgnoreMode.IGNOREBORDER: 按照扫描线的方式忽略颜色值。\n    "
    IGNORENONE = 0
    IGNORESIGNAL = 1
    IGNOREBORDER = 2

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.conversion.IgnoreMode"


@unique
class MultiBandImportMode(JEnum):
    __doc__ = "\n    该类定义了多波段导入模式类型常量，提供了导入多波段数据所采用的模式。\n\n    :var MultiBandImportMode.SINGLEBAND: 将多波段数据导入为多个单波段数据集\n    :var MultiBandImportMode.MULTIBAND: 将多波段数据导入为一个多波段数据集\n    :var MultiBandImportMode.COMPOSITE: 将多波段数据导入为一个单波段数据集，目前此模式适用于以下两种情况：\n\n                                        - 三波段 8 位的数据导入为一个 RGB 单波段 24 位的数据集；\n                                        - 四波段 8 位的数据导入为一个 RGBA 单波段 32 位的数据集。\n    "
    SINGLEBAND = 0
    MULTIBAND = 1
    COMPOSITE = 2

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.conversion.MultiBandImportMode"


@unique
class CADVersion(JEnum):
    __doc__ = "\n    该类定义了 AutoCAD 版本类型常量。提供了 AutoCAD 的不同版本类型及说明。\n\n    :var CADVersion.CAD12: OdDb::vAC12 R11-12\n    :var CADVersion.CAD13: OdDb::vAC13 R13\n    :var CADVersion.CAD14: OdDb::vAC14 R14\n    :var CADVersion.CAD2000: OdDb::vAC15 2000-2002\n    :var CADVersion.CAD2004: OdDb::vAC18 2004-2006\n    :var CADVersion.CAD2007: OdDb::vAC21 2007\n    "
    CAD12 = 12
    CAD13 = 13
    CAD14 = 14
    CAD2000 = 2000
    CAD2004 = 2004
    CAD2007 = 2007

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.conversion.CADVersion"


@unique
class TopologyRule(JEnum):
    __doc__ = "\n    该类定义了拓扑规则类型常量。\n\n    该类主要用于对点、线和面数据进行拓扑检查，是拓扑检查的一个参数。根据相应的拓扑规则，返回不符合规则的对象。\n\n    :var TopologyRule.REGION_NO_OVERLAP: 面内无重叠，用于对面数据进行拓扑检查。检查一个面数据集（或者面记录集）中相互有重叠的面对象。此规则\n                                         多用于一个区域不能同时属于两个对象的情况。如行政区划面，相邻的区划之间要求不能有任何重叠，行政区划\n                                         数据上必须是每个区域都有明确的地域定义。此类数据还包括：土地利用图斑、邮政编码覆盖区划、公民投票选\n                                         区区划等。重叠部分作为错误生成到结果数据集中，错误数据集类型：面。注意：只对一个数据集或记录集本身进行检查。\n    :var TopologyRule.REGION_NO_GAPS: 面内无缝隙，用于对面数据进行拓扑检查。返回一个面数据集（或者面记录集）中相邻面之间有空隙的面对象。此规\n                                      则多用于检查一个面数据中，单个区域或相邻区域之间有空隙的情况。一般对于如土地利用图斑这样的数据，要求不\n                                      能有未定义土地利用类型的斑块，可使用此规则进行检查。\n\n                                      注意：\n\n                                      - 只对一个数据集或记录集本身进行检查。\n                                      - 若被检查的面数据集（或记录集）中存在自相交面对象，则检查可能失败或结果错误。建议检查时，先进行\n                                        “面内无自相交”（REGION_NO_SELF_INTERSECTION）规则检查，或自行对自相交面进行修改，确认无自相交\n                                        对象后再进行“面内无缝隙”规则检查。\n\n    :var TopologyRule.REGION_NO_OVERLAP_WITH: 面与面无重叠，用于对面数据进行拓扑检查。检查两个面数据集中重叠的所有对象。此规则检查第一个面数\n                                              据中，与第二个面数据有重叠的所有对象。如将水域数据与旱地数据叠加，可用此规则检查。重叠部分作为\n                                              错误生成到结果数据集中，错误数据集类型：面\n    :var TopologyRule.REGION_COVERED_BY_REGION_CLASS: 面被多个面覆盖，用于对面数据进行拓扑检查。检查第一个面数据集（或者面记录集）中没有\n                                                      被第二个面数据集（或者面记录集）覆盖的对象。如：省界 Area1 中每一个省域都必须完全\n                                                      被县界 Area2 中属于该省的面域所覆盖。未覆盖的部分将作为错误生成到结果数据集中，错误数据集类型：面\n\n    :var TopologyRule.REGION_COVERED_BY_REGION: 面被面包含，用于对面数据进行拓扑检查。\n                                                检查第一个面数据集（或者面记录集）中没有被第二个面数据集（或者面记录集）中任何对象包含的对象。即面数据 1 的区域都必须被面数据 2 的某一个区域完全包含。\n                                                未被包含的面对象整个将作为错误生成到结果数据集中，错误数据集类型：面。\n    :var TopologyRule.REGION_BOUNDARY_COVERED_BY_LINE: 面边界被多条线覆盖，用于对面数据进行拓扑检查。\n                                                       检查面数据集（或者面记录集）中对象的边界没有被线数据集（或者线记录集）中的线覆盖的对象。\n                                                       通常用于行政区界或地块和存储有边界线属性的线数据进行检查。面数据中不能存储一些边界线的属性，\n                                                       此时需要专门的边界线数据，存储区域边界的不同属性，要求边界线与区域边界线完全重合。\n                                                       未被覆盖的边界将作为错误生成到结果数据集中，错误数据集类型：线。\n    :var TopologyRule.REGION_BOUNDARY_COVERED_BY_REGION_BOUNDARY: 面边界被边界覆盖，用于对面数据进行拓扑检查。\n                                                                  检查面数据集（或者面记录集）中边界没有被另一面数据集（或者面记录集）中对象（可以为多个）的边界覆盖的对象。\n                                                                  未被覆盖的边界将作为错误生成到结果数据集中，错误数据集类型：线。\n    :var TopologyRule.REGION_CONTAIN_POINT: 面包含点，用于对面数据进行拓扑检查。\n                                            检查面数据集（或者面记录集）中没有包含任何点数据集（或者点记录集）中点的对象。例如省域数据与省会数据进行检查，每个省内都必须有一个省会城市，不包含任何点数据的面对象，都将被检查出来。\n                                            未包含点的面对象将作为错误生成到结果数据集中，错误数据集类型：面。\n    :var TopologyRule.LINE_NO_INTERSECTION: 线内无相交，用于对线数据进行拓扑检查。\n                                            检查一个线数据集（或者线记录集）中相互有相交（不包括端点和内部接触及端点和端点接触）的线对象。交点将作为错误生成到结果数据集中，错误数据集类型：点。\n                                            注意：只对一个数据集或记录集本身进行检查。\n    :var TopologyRule.LINE_NO_OVERLAP: 线内无重叠，用于对线数据进行拓扑检查。检查一个线数据集（或者线记录集）中相互有重叠的线对象。对象之间重叠的部分将作为错误生成到结果数据集中，错误数据集类型：线。\n                                       注意：只对一个数据集或记录集本身进行检查。\n    :var TopologyRule.LINE_NO_DANGLES: 线内无悬线，用于对线数据进行拓扑检查。检查一个线数据集（或者线记录集）中被定义为悬线的对象，包括过头线和长悬线。悬点将作为错误生成到结果数据集中，错误数据集类型：点。\n                                       注意：只对一个数据集或记录集本身进行检查。\n    :var TopologyRule.LINE_NO_PSEUDO_NODES: 线内无假结点，用于对线数据进行拓扑检查。返回一个线数据集（或者线记录集）中包含假结点的线对象。假结点将作为错误生成到结果数据集中，错误数据集类型：点。\n                                            注意：只对一个数据集或记录集本身进行检查。\n    :var TopologyRule.LINE_NO_OVERLAP_WITH: 线与线无重叠，用于对线数据进行拓扑检查。检查第一个线数据集（或者线记录集）中和第二个线数据集（或者线记录集）中的对象有重叠的所有对象。如交通路线中的公路和铁路不能出现重叠。\n                                            重叠部分作为错误生成到结果数据集中，错误数据集类型：线。\n    :var TopologyRule.LINE_NO_INTERSECT_OR_INTERIOR_TOUCH: 线内无相交或无内部接触，用于对线数据进行拓扑检查。返回一个线数据集（或者线记录集）中和其它线对象相交的线对象，即除端点之间接触外其它所有的相交或内部接触的线对象。\n                                                           交点作为错误生成到结果数据集中，错误数据集类型：点。\n                                                           注意：线数据集（或者线记录集）中所有交点必须是线的端点，即相交的弧段必须被打断，否则就违反此规则（自交不检查）。\n    :var TopologyRule.LINE_NO_SELF_OVERLAP: 线内无自交叠，用于对线数据进行拓扑检查。检查一个线数据集（或者线记录集）内相互有交叠（交集是线）的线对象。自交叠部分（线）将作为错误生成到结果数据集中，错误数据集类型：线。\n                                            注意：只对一个数据集或记录集本身进行检查。\n    :var TopologyRule.LINE_NO_SELF_INTERSECT: 线内无自相交，用于对线数据进行拓扑检查。检查一个线数据集（或者线记录集）内自相交的线对象（包括自交叠的情况）。\n                                              交点将作为错误生成到结果数据集中，错误数据集类型：点。\n                                              注意：只对一个数据集或记录集本身进行检查。\n    :var TopologyRule.LINE_BE_COVERED_BY_LINE_CLASS: 线被多条线完全覆盖，用于对线数据进行拓扑检查。\n                                                     检查第一个线数据集（或者线记录集）中没有与第二个线数据集（或者线记录集）中的对象有重合的对象。\n                                                     未被覆盖的部分将作为错误生成到结果数据集中，错误数据集类型：线。\n                                                     注意：线数据集（或线记录集）中每一个对象，都必须被另一个线数据集（或者线记录集）中的一个或多个线对象覆盖。如Line1中的某条公交路线必须被Line2中的一系列相连的街道覆盖。\n    :var TopologyRule.LINE_COVERED_BY_REGION_BOUNDARY: 线被面边界覆盖，用于对线数据进行拓扑检查。检查线数据集（或者线记录集）中没有与面数据集（或者面记录集）中某个对象的边界重合的对象。（可被多个面的边界覆盖）。\n                                                       未被边界覆盖的部分将作为错误生成到结果数据集中，错误数据集类型：线。\n    :var TopologyRule.LINE_END_POINT_COVERED_BY_POINT: 线端点必须被点覆盖，用于对线数据进行拓扑检查。\n                                                       检查线数据集（或者线记录集）中的端点没有与点数据集（或者点记录集）中任何一个点重合的对象。\n                                                       未被覆盖的端点将作为错误生成到结果数据集中，错误数据集类型：点。\n    :var TopologyRule.POINT_COVERED_BY_LINE: 点必须在线上，用于对点数据进行拓扑检查。\n                                             返回点数据集（或者点记录集）中没有被线数据集（或者线记录集）中的某个对象覆盖的对象。如高速公路上的收费站。\n                                             未被覆盖的点将作为错误生成到结果数据集中，错误数据集类型：点。\n    :var TopologyRule.POINT_COVERED_BY_REGION_BOUNDARY: 点必须在面的边界上，用于对点数据进行拓扑检查。\n                                                        检查点数据集（或者点记录集）中没有在面数据集（或者面记录集）中某个对象的边界上的对象。\n                                                        不在面边界上的点将作为错误生成到结果数据集中，错误数据集类型：点。\n    :var TopologyRule.POINT_CONTAINED_BY_REGION: 点被面完全包含，用于对点数据进行拓扑检查。\n                                                 检查点数据集（或者点记录集）中没有被面数据集（或者面记录集）中任何一个对象内部包含的点对象。\n                                                 不在面内的点将作为错误生成到结果数据集中，错误数据集类型：点。\n    :var TopologyRule.POINT_BECOVERED_BY_LINE_END_POINT: 点必须被线端点覆盖，用于对点数据进行拓扑检查。\n                                                         返回点数据集（或者点记录集）中没有被线数据集（或者线记录集）中任意对象的端点覆盖的对象。\n    :var TopologyRule.NO_MULTIPART: 无复杂对象。检查一个数据集或记录集内包含子对象的复杂对象，适用于面和线。\n                                    复杂对象将作为错误生成到结果数据集中，错误数据集类型：线或面。\n    :var TopologyRule.POINT_NO_IDENTICAL: 无重复点，用于对点数据进行拓扑检查。检查点数据集中的重复点对象。点数据集内发生重叠的对象都将作为拓扑错误生成。\n                                          所有重复的点将作为错误生成到结果数据集中，错误数据集类型：点。\n                                          注意：只对一个数据集或记录集本身进行检查。\n    :var TopologyRule.POINT_NO_CONTAINED_BY_REGION: 点不被面包含。检查点数据集（或者点记录集）中被面数据集（或者面记录集）中某一个对象内部包含的点对象。\n                                                    被面包含的点将作为错误生成到结果数据集中，错误数据集类型：点。\n                                                    注意：点若位于面边界上，则不违背此规则。\n    :var TopologyRule.LINE_NO_INTERSECTION_WITH_REGION: 线不能和面相交或被包含。检查线数据集（或者线记录集）中和面数据集（或者面记录集）中的面对象相交或者被面对象包含的线对象。\n                                                        线面交集部分将作为错误生成到结果数据集中，错误数据集类型：线。\n    :var TopologyRule.REGION_NO_OVERLAP_ON_BOUNDARY: 面边界无交叠，用于对面数据进行拓扑检查。\n                                                     检查面数据集或记录集中的面对象的边界与另一面数据集或记录集中的对象边界有交叠的部分。\n                                                     边界重叠的部分将作为错误生成到结果数据集中，错误数据集类型：线。\n    :var TopologyRule.REGION_NO_SELF_INTERSECTION: 面内无自相交，用于对面数据进行拓扑检查。\n                                                   检查面数据中是否存在自相交的对象。\n                                                   面对象自相交的交点将作为错误生成到结果数据集中，错误数据集类型：点。\n    :var TopologyRule.LINE_NO_INTERSECTION_WITH: 线与线无相交，即线对象和线对象不能相交。\n                                                 检查第一个线数据集（或者线记录集）中没有与第二个线数据集（或者线记录集）中的对象有相交的对象。\n                                                 交点将作为错误生成到结果数据集中，错误数据集类型：点。\n    :var TopologyRule.VERTEX_DISTANCE_GREATER_THAN_TOLERANCE: 节点距离必须大于容限。检查点、线、面类型的两个数据集内部或者两个数据集之间对象的节点距离是否小于容限。\n                                                              不大于容限的节点将作为错误生成到结果数据集中，错误数据集类型：点。\n                                                              注意：如果两节点重合，即距离为0，则不视为拓扑错误。\n    :var TopologyRule.LINE_EXIST_INTERSECT_VERTEX: 线段相交处必须存在交点。线、面类型的数据集内部或两个数据集之间，线段与线段十字相交处必须存在节点，且此节点至少存在于两个相交线段中的一个。\n                                                   如不满足则将此交点计算出来作为错误生成到结果数据集中，错误数据集类型：点。\n                                                   注意：两条线段端点相接的情况不违反规则。\n    :var TopologyRule.VERTEX_MATCH_WITH_EACH_OTHER: 节点之间必须互相匹配，即容限范围内线段上存在垂足点。\n                                                    检查线、面类型数据集内部或两个数据集之间，点数据集和线数据集、点数据集和面数据之间，在当前节点 P 的容限范围内，线段 L 上应存在一个节点 Q 在与之匹配，即 Q 在 P 的容限范围内。如不满足，则计算 P 到 L 的“垂足” A 点（即 A 与 P 匹配）作为错误生成到结果数据集中，错误数据集类型：点。\n    :var TopologyRule.NO_REDUNDANT_VERTEX: 线或面边界无冗余节点。检查线数据集或面数据集中是否存在有冗余节点的对象。线对象或面对象边界上的两节点之间如果存在其他共线节点，则这些共线节点为冗余节点。\n                                           冗余节点将作为错误生成到结果数据集中，错误数据类型：点\n    :var TopologyRule.LINE_NO_SHARP_ANGLE: 线内无打折。检查线数据集（或记录集）中线对象是否存在打折。若一条线上连续四个节点形成的两个夹角均小于所给的尖角角度容限，则认为线段在此处打折。\n                                           产生尖角的第一个折点作为错误生成到结果数据集中，错误数据类型：点。\n                                           注意：在使用 :py:meth:`topology_validate` 方法对该规则检查时，通过该方法的 tolerance 参数设置尖角容\n    :var TopologyRule.LINE_NO_SMALL_DANGLES: 线内无短悬线，用于对线数据进行拓扑检查。检查线数据集（或记录集）中线对象是否是短悬线。一条悬线的长度小于悬线容限的线对象即为短悬线\n                                             短悬线的端点作为错误生成到结果数据集中，错误数据类型：点。\n                                             注意：在使用 :py:meth:`topology_validate` 方法对该规则检查时，通过该方法的 tolerance 参数设置短悬线容限。\n    :var TopologyRule.LINE_NO_EXTENDED_DANGLES: 线内无长悬线，用于对线数据进行拓扑检查。检查线数据集（或记录集）中线对象是否是长悬线。一条悬线按其行进方向延伸了指定的长度（悬线容限）之后与某弧段有交点，则该线对象为长悬线。\n                                                长悬线需要延长一端的端点作为错误生成到结果数据集中，错误数据类型：点。\n                                                注意：在使用 :py:meth:`topology_validate` 方法对该规则检查时，通过该方法的 tolerance 参数设置长悬线容限。\n    :var TopologyRule.REGION_NO_ACUTE_ANGLE: 面内无锐角,用于对面数据进行拓扑检查。检查面数据集（或记录集）中面对象是否存在锐角。若面边界线上连续三个节点形成的夹角小于所给的锐角角度容限，则认为此夹角为锐角。\n                                             产生锐角的第二个节点作为错误生成到结果数据集中，错误数据类型：点。\n                                             注意：在使用 :py:meth:`topology_validate` 方法对该规则检查时，通过该方法的 tolerance 参数设置锐角容限。\n    "
    REGION_NO_OVERLAP = 0
    REGION_NO_GAPS = 1
    REGION_NO_OVERLAP_WITH = 2
    REGION_COVERED_BY_REGION_CLASS = 3
    REGION_COVERED_BY_REGION = 4
    REGION_BOUNDARY_COVERED_BY_LINE = 5
    REGION_BOUNDARY_COVERED_BY_REGION_BOUNDARY = 6
    REGION_CONTAIN_POINT = 7
    LINE_NO_INTERSECTION = 8
    LINE_NO_OVERLAP = 9
    LINE_NO_DANGLES = 10
    LINE_NO_PSEUDO_NODES = 11
    LINE_NO_OVERLAP_WITH = 12
    LINE_NO_INTERSECT_OR_INTERIOR_TOUCH = 13
    LINE_NO_SELF_OVERLAP = 14
    LINE_NO_SELF_INTERSECT = 15
    LINE_BE_COVERED_BY_LINE_CLASS = 16
    LINE_COVERED_BY_REGION_BOUNDARY = 17
    LINE_END_POINT_COVERED_BY_POINT = 18
    POINT_COVERED_BY_LINE = 19
    POINT_COVERED_BY_REGION_BOUNDARY = 20
    POINT_CONTAINED_BY_REGION = 21
    POINT_BECOVERED_BY_LINE_END_POINT = 22
    NO_MULTIPART = 23
    POINT_NO_IDENTICAL = 24
    POINT_NO_CONTAINED_BY_REGION = 25
    LINE_NO_INTERSECTION_WITH_REGION = 26
    REGION_NO_OVERLAP_ON_BOUNDARY = 27
    REGION_NO_SELF_INTERSECTION = 28
    LINE_NO_INTERSECTION_WITH = 29
    VERTEX_DISTANCE_GREATER_THAN_TOLERANCE = 30
    LINE_EXIST_INTERSECT_VERTEX = 31
    VERTEX_MATCH_WITH_EACH_OTHER = 32
    NO_REDUNDANT_VERTEX = 33
    LINE_NO_SHARP_ANGLE = 34
    LINE_NO_SMALL_DANGLES = 35
    LINE_NO_EXTENDED_DANGLES = 36
    REGION_NO_ACUTE_ANGLE = 37

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.TopologyRule"


@unique
class GeoDatumType(JEnum):
    DATUM_USER_DEFINED = -1
    DATUM_AIRY_1830 = 6001
    DATUM_AIRY_MOD = 6002
    DATUM_AUSTRALIAN = 6003
    DATUM_BESSEL_1841 = 6004
    DATUM_BESSEL_MOD = 6005
    DATUM_BESSEL_NAMIBIA = 6006
    DATUM_CLARKE_1858 = 6007
    DATUM_CLARKE_1866 = 6008
    DATUM_CLARKE_1866_MICH = 6009
    DATUM_CLARKE_1880 = 6034
    DATUM_CLARKE_1880_ARC = 6013
    DATUM_CLARKE_1880_BENOIT = 6010
    DATUM_CLARKE_1880_IGN = 6011
    DATUM_CLARKE_1880_RGS = 6012
    DATUM_CLARKE_1880_SGA = 6014
    DATUM_EVEREST_1830 = 6015
    DATUM_EVEREST_DEF_1967 = 6016
    DATUM_EVEREST_DEF_1975 = 6017
    DATUM_EVEREST_MOD = 6018
    DATUM_GEM_10C = 6031
    DATUM_GRS_1967 = 6036
    DATUM_GRS_1980 = 6019
    DATUM_HELMERT_1906 = 6020
    DATUM_INDONESIAN = 6021
    DATUM_INTERNATIONAL_1924 = 6022
    DATUM_INTERNATIONAL_1967 = 6023
    DATUM_KRASOVSKY_1940 = 6024
    DATUM_NWL_9D = 6025
    DATUM_OSU_86F = 6032
    DATUM_OSU_91A = 6033
    DATUM_PLESSIS_1817 = 6027
    DATUM_SPHERE = 6035
    DATUM_STRUVE_1860 = 6028
    DATUM_WAR_OFFICE = 6029
    DATUM_WGS_1966 = 39001
    DATUM_FISCHER_1960 = 39002
    DATUM_FISCHER_1968 = 39003
    DATUM_FISCHER_MOD = 39004
    DATUM_HOUGH_1960 = 39005
    DATUM_EVEREST_MOD_1969 = 39006
    DATUM_WALBECK = 39007
    DATUM_SPHERE_AI = 39008
    DATUM_ADINDAN = 6201
    DATUM_AFGOOYE = 6205
    DATUM_AGADEZ = 6206
    DATUM_AGD_1966 = 6202
    DATUM_AGD_1984 = 6203
    DATUM_AIN_EL_ABD_1970 = 6204
    DATUM_AMERSFOORT = 6289
    DATUM_ARATU = 6208
    DATUM_ARC_1950 = 6209
    DATUM_ARC_1960 = 6210
    DATUM_ATF = 6901
    DATUM_ATS_1977 = 6122
    DATUM_BARBADOS = 6212
    DATUM_BATAVIA = 6211
    DATUM_BEDUARAM = 6213
    DATUM_BEIJING_1954 = 6214
    DATUM_BELGE_1950 = 6215
    DATUM_BELGE_1972 = 6313
    DATUM_BERMUDA_1957 = 6216
    DATUM_BERN_1898 = 6217
    DATUM_BERN_1938 = 6306
    DATUM_BOGOTA = 6218
    DATUM_BUKIT_RIMPAH = 6219
    DATUM_CAMACUPA = 6220
    DATUM_CAMPO_INCHAUSPE = 6221
    DATUM_CAPE = 6222
    DATUM_CARTHAGE = 6223
    DATUM_CHUA = 6224
    DATUM_CONAKRY_1905 = 6315
    DATUM_CORREGO_ALEGRE = 6225
    DATUM_COTE_D_IVOIRE = 6226
    DATUM_DATUM_73 = 6274
    DATUM_DEIR_EZ_ZOR = 6227
    DATUM_DEALUL_PISCULUI_1933 = 6316
    DATUM_DEALUL_PISCULUI_1970 = 6317
    DATUM_DHDN = 6314
    DATUM_DOUALA = 6228
    DATUM_ED_1950 = 6230
    DATUM_ED_1987 = 6231
    DATUM_EGYPT_1907 = 6229
    DATUM_ETRS_1989 = 6258
    DATUM_FAHUD = 6232
    DATUM_GANDAJIKA_1970 = 6233
    DATUM_GAROUA = 6234
    DATUM_GDA_1994 = 6283
    DATUM_GGRS_1987 = 6121
    DATUM_GREEK = 6120
    DATUM_GUYANE_FRANCAISE = 6235
    DATUM_HERAT_NORTH = 6255
    DATUM_HITO_XVIII_1963 = 6254
    DATUM_HU_TZU_SHAN = 6236
    DATUM_HUNGARIAN_1972 = 6237
    DATUM_INDIAN_1954 = 6239
    DATUM_INDIAN_1975 = 6240
    DATUM_INDONESIAN_1974 = 6238
    DATUM_JAMAICA_1875 = 6241
    DATUM_JAMAICA_1969 = 6242
    DATUM_KALIANPUR = 6243
    DATUM_KANDAWALA = 6244
    DATUM_KERTAU = 6245
    DATUM_KKJ = 6123
    DATUM_KOC = 6246
    DATUM_KUDAMS = 6319
    DATUM_LA_CANOA = 6247
    DATUM_LAKE = 6249
    DATUM_LEIGON = 6250
    DATUM_LIBERIA_1964 = 6251
    DATUM_LISBON = 6207
    DATUM_LOMA_QUINTANA = 6288
    DATUM_LOME = 6252
    DATUM_LUZON_1911 = 6253
    DATUM_MAHE_1971 = 6256
    DATUM_MAKASSAR = 6257
    DATUM_MALONGO_1987 = 6259
    DATUM_MANOCA = 6260
    DATUM_MASSAWA = 6262
    DATUM_MERCHICH = 6261
    DATUM_MGI = 6312
    DATUM_MHAST = 6264
    DATUM_MINNA = 6263
    DATUM_MONTE_MARIO = 6265
    DATUM_MPORALOKO = 6266
    DATUM_NAD_MICH = 6268
    DATUM_NAD_1927 = 6267
    DATUM_NAD_1983 = 6269
    DATUM_NAHRWAN_1967 = 6270
    DATUM_NAPARIMA_1972 = 6271
    DATUM_NDG = 6902
    DATUM_NGN = 6318
    DATUM_NGO_1948 = 6273
    DATUM_NORD_SAHARA_1959 = 6307
    DATUM_NSWC_9Z_2 = 6276
    DATUM_NTF = 6275
    DATUM_NZGD_1949 = 6272
    DATUM_OS_SN_1980 = 6279
    DATUM_OSGB_1936 = 6277
    DATUM_OSGB_1970_SN = 6278
    DATUM_PADANG_1884 = 6280
    DATUM_PALESTINE_1923 = 6281
    DATUM_POINTE_NOIRE = 6282
    DATUM_PSAD_1956 = 6248
    DATUM_PULKOVO_1942 = 6284
    DATUM_PULKOVO_1995 = 6200
    DATUM_QATAR = 6285
    DATUM_QATAR_1948 = 6286
    DATUM_QORNOQ = 6287
    DATUM_SAD_1969 = 6291
    DATUM_SAPPER_HILL_1943 = 6292
    DATUM_SCHWARZECK = 6293
    DATUM_SEGORA = 6294
    DATUM_SERINDUNG = 6295
    DATUM_STOCKHOLM_1938 = 6308
    DATUM_SUDAN = 6296
    DATUM_TANANARIVE_1925 = 6297
    DATUM_TIMBALAI_1948 = 6298
    DATUM_TM65 = 6299
    DATUM_TM75 = 6300
    DATUM_TOKYO = 6301
    DATUM_TRINIDAD_1903 = 6302
    DATUM_TRUCIAL_COAST_1948 = 6303
    DATUM_VOIROL_1875 = 6304
    DATUM_VOIROL_UNIFIE_1960 = 6305
    DATUM_WGS_1972 = 6322
    DATUM_WGS_1972_BE = 6324
    DATUM_WGS_1984 = 6326
    DATUM_YACARE = 6309
    DATUM_YOFF = 6310
    DATUM_ZANDERIJ = 6311
    DATUM_EUROPEAN_1979 = 39201
    DATUM_EVEREST_BANGLADESH = 39202
    DATUM_EVEREST_INDIA_NEPAL = 39203
    DATUM_HJORSEY_1955 = 39204
    DATUM_HONG_KONG_1963 = 39205
    DATUM_OMAN = 39206
    DATUM_S_ASIA_SINGAPORE = 39207
    DATUM_AYABELLE = 39208
    DATUM_BISSAU = 39209
    DATUM_DABOLA = 39210
    DATUM_POINT58 = 39211
    DATUM_BEACON_E_1945 = 39212
    DATUM_TERN_ISLAND_1961 = 39213
    DATUM_ASTRO_1952 = 39214
    DATUM_BELLEVUE = 39215
    DATUM_CANTON_1966 = 39216
    DATUM_CHATHAM_ISLAND_1971 = 39217
    DATUM_DOS_1968 = 39218
    DATUM_EASTER_ISLAND_1967 = 39219
    DATUM_GUAM_1963 = 39220
    DATUM_GUX_1 = 39221
    DATUM_JOHNSTON_ISLAND_1961 = 39222
    DATUM_KUSAIE_1951 = 39259
    DATUM_MIDWAY_1961 = 39224
    DATUM_OLD_HAWAIIAN = 39225
    DATUM_PITCAIRN_1967 = 39226
    DATUM_SANTO_DOS_1965 = 39227
    DATUM_VITI_LEVU_1916 = 39228
    DATUM_WAKE_ENIWETOK_1960 = 39229
    DATUM_WAKE_ISLAND_1952 = 39230
    DATUM_ANNA_1_1965 = 39231
    DATUM_GAN_1970 = 39232
    DATUM_ISTS_073_1969 = 39233
    DATUM_KERGUELEN_ISLAND_1949 = 39234
    DATUM_REUNION = 39235
    DATUM_ANTIGUA_ISLAND_1943 = 39236
    DATUM_ASCENSION_ISLAND_1958 = 39237
    DATUM_DOS_71_4 = 39238
    DATUM_CACANAVERAL = 39239
    DATUM_FORT_THOMAS_1955 = 39240
    DATUM_GRACIOSA_1948 = 39241
    DATUM_ISTS_061_1968 = 39242
    DATUM_LC5_1961 = 39243
    DATUM_MONTSERRAT_ISLAND_1958 = 39244
    DATUM_OBSERV_METEOR_1939 = 39245
    DATUM_PICO_DE_LAS_NIEVES = 39246
    DATUM_PORTO_SANTO_1936 = 39247
    DATUM_PUERTO_RICO = 39248
    DATUM_SAO_BRAZ = 39249
    DATUM_SELVAGEM_GRANDE_1938 = 39250
    DATUM_TRISTAN_1968 = 39251
    DATUM_SAMOA_1962 = 39252
    DATUM_CAMP_AREA = 39253
    DATUM_DECEPTION_ISLAND = 39254
    DATUM_GUNUNG_SEGARA = 39255
    DATUM_INDIAN_1960 = 39256
    DATUM_S42_HUNGARY = 39257
    DATUM_S_JTSK = 39258
    DATUM_ALASKAN_ISLANDS = 39260
    DATUM_JAPAN_2000 = 39301
    DATUM_XIAN_1980 = 39312
    DATUM_CHINA_2000 = 39313
    DATUM_POPULAR_VISUALISATION = 6055

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.GeoDatumType"


@unique
class GeoSpheroidType(JEnum):
    SPHEROID_USER_DEFINED = -1
    SPHEROID_AIRY_1830 = 7001
    SPHEROID_AIRY_MOD = 7002
    SPHEROID_ATS_1977 = 7041
    SPHEROID_AUSTRALIAN = 7003
    SPHEROID_BESSEL_1841 = 7004
    SPHEROID_BESSEL_MOD = 7005
    SPHEROID_BESSEL_NAMIBIA = 7006
    SPHEROID_CLARKE_1858 = 7007
    SPHEROID_CLARKE_1866 = 7008
    SPHEROID_CLARKE_1866_MICH = 7009
    SPHEROID_CLARKE_1880 = 7034
    SPHEROID_CLARKE_1880_ARC = 7013
    SPHEROID_CLARKE_1880_BENOIT = 7010
    SPHEROID_CLARKE_1880_IGN = 7011
    SPHEROID_CLARKE_1880_RGS = 7012
    SPHEROID_CLARKE_1880_SGA = 7014
    SPHEROID_EVEREST_1830 = 7015
    SPHEROID_EVEREST_DEF_1967 = 7016
    SPHEROID_EVEREST_DEF_1975 = 7017
    SPHEROID_EVEREST_MOD = 7018
    SPHEROID_GEM_10C = 7031
    SPHEROID_GRS_1967 = 7036
    SPHEROID_GRS_1980 = 7019
    SPHEROID_HELMERT_1906 = 7020
    SPHEROID_INDONESIAN = 7021
    SPHEROID_INTERNATIONAL_1924 = 7022
    SPHEROID_INTERNATIONAL_1967 = 7023
    SPHEROID_KRASOVSKY_1940 = 7024
    SPHEROID_NWL_9D = 7025
    SPHEROID_OSU_86F = 7032
    SPHEROID_OSU_91A = 7033
    SPHEROID_PLESSIS_1817 = 7027
    SPHEROID_SPHERE = 7035
    SPHEROID_STRUVE_1860 = 7028
    SPHEROID_WAR_OFFICE = 7029
    SPHEROID_NWL_10D = 7026
    SPHEROID_WGS_1972 = 7043
    SPHEROID_WGS_1984 = 7030
    SPHEROID_WGS_1966 = 40001
    SPHEROID_FISCHER_1960 = 40002
    SPHEROID_FISCHER_1968 = 40003
    SPHEROID_FISCHER_MOD = 40004
    SPHEROID_HOUGH_1960 = 40005
    SPHEROID_EVEREST_MOD_1969 = 40006
    SPHEROID_WALBECK = 40007
    SPHEROID_SPHERE_AI = 40008
    SPHEROID_INTERNATIONAL_1975 = 40023
    SPHEROID_CHINA_2000 = 7044
    SPHEROID_POPULAR_VISUALISATON = 7059

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.GeoSpheroidType"


@unique
class GeoPrimeMeridianType(JEnum):
    __doc__ = '\n    该类定义了中央经线类型常量。\n\n    :var GeoPrimeMeridianType.PRIMEMERIDIAN_USER_DEFINED: 用户自定义\n    :var GeoPrimeMeridianType.PRIMEMERIDIAN_GREENWICH: 格林威治本初子午线，即0°经线\n    :var GeoPrimeMeridianType.PRIMEMERIDIAN_LISBON: 9°07\'54".862 W\n    :var GeoPrimeMeridianType.PRIMEMERIDIAN_PARIS: 2°20\'14".025 E\n    :var GeoPrimeMeridianType.PRIMEMERIDIAN_BOGOTA: 74°04\'51".3 W\n    :var GeoPrimeMeridianType.PRIMEMERIDIAN_MADRID: 3°41\'16".58 W\n    :var GeoPrimeMeridianType.PRIMEMERIDIAN_ROME: 12°27\'08".4 E\n    :var GeoPrimeMeridianType.PRIMEMERIDIAN_BERN: 7°26\'22".5 E\n    :var GeoPrimeMeridianType.PRIMEMERIDIAN_JAKARTA: 106°48\'27".79 E\n    :var GeoPrimeMeridianType.PRIMEMERIDIAN_FERRO: 17°40\'00" W\n    :var GeoPrimeMeridianType.PRIMEMERIDIAN_BRUSSELS: 4°22\'04".71 E\n    :var GeoPrimeMeridianType.PRIMEMERIDIAN_STOCKHOLM: 18°03\'29".8 E\n    :var GeoPrimeMeridianType.PRIMEMERIDIAN_ATHENS: 23°42\'58".815 E\n    '
    PRIMEMERIDIAN_USER_DEFINED = -1
    PRIMEMERIDIAN_GREENWICH = 8901
    PRIMEMERIDIAN_LISBON = 8902
    PRIMEMERIDIAN_PARIS = 8903
    PRIMEMERIDIAN_BOGOTA = 8904
    PRIMEMERIDIAN_MADRID = 8905
    PRIMEMERIDIAN_ROME = 8906
    PRIMEMERIDIAN_BERN = 8907
    PRIMEMERIDIAN_JAKARTA = 8908
    PRIMEMERIDIAN_FERRO = 8909
    PRIMEMERIDIAN_BRUSSELS = 8910
    PRIMEMERIDIAN_STOCKHOLM = 8911
    PRIMEMERIDIAN_ATHENS = 8912

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.GeoPrimeMeridianType"


@unique
class CoordSysTransMethod(JEnum):
    __doc__ = "\n    该类定义了投影转换方法类型常量。\n\n    在投影转换中，如果源投影和目标投影的地理坐标系不同，则需要进行参照系的转换。\n\n    参照系的转换有两种，基于网格的转换和基于公式的转换。本类所提供的转换方法均为基于公式的转换。依据转换参数的不同可以分为三参数法和七参数法。目前使\n    用最广泛的是七参数法。参数信息参见 :py:class:`CoordSysTransParameter`；如果源投影和目标投影的地理坐标系相同，用户无需进行参照系的转换，即可以不进行\n    :py:class:`CoordSysTransParameter` 参数信息的设置。本版本中的 GeocentricTranslation、Molodensky、MolodenskyAbridged 是基于地心的三参数转换\n    法；PositionVector、CoordinateFrame、BursaWolf都是七参数法。\n\n    :var CoordSysTransMethod.MTH_GEOCENTRIC_TRANSLATION: 基于地心的三参数转换法\n    :var CoordSysTransMethod.MTH_MOLODENSKY: 莫洛金斯基（Molodensky）转换法\n    :var CoordSysTransMethod.MTH_MOLODENSKY_ABRIDGED: 简化的莫洛金斯基转换法\n    :var CoordSysTransMethod.MTH_POSITION_VECTOR: 位置矢量法\n    :var CoordSysTransMethod.MTH_COORDINATE_FRAME: 基于地心的七参数转换法\n    :var CoordSysTransMethod.MTH_BURSA_WOLF: Bursa-Wolf 方法\n    :var CoordSysTransMethod.MolodenskyBadekas: 莫洛金斯基—巴待卡斯投影转换方法，一种十参数的空间坐标转换模型。\n    "
    MTH_GEOCENTRIC_TRANSLATION = 9603
    MTH_MOLODENSKY = 9604
    MTH_MOLODENSKY_ABRIDGED = 9605
    MTH_POSITION_VECTOR = 9606
    MTH_COORDINATE_FRAME = 9607
    MTH_BURSA_WOLF = 42607
    MolodenskyBadekas = 49607

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.CoordSysTransMethod"


@unique
class ResamplingMethod(JEnum):
    __doc__ = "\n    该类定义了创建金字塔类型常量。\n\n    :var ResamplingMethod.AVERAGE: 平均值\n    :var ResamplingMethod.NEAR: 邻近值\n    "
    AVERAGE = 1
    NEAR = 2

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.ResamplingMethod"


@unique
class ColorSpaceType(JEnum):
    __doc__ = "\n    该类定义了色彩空间类型常量。\n\n    由于成色原理的不同，决定了显示器、投影仪这类靠色光直接合成颜色的颜色设备和打印机、印刷机这类靠使用颜料的印刷设备在生成颜色方式上的区别。针对上述不同成色方式，针对上述不同成色方式，SuperMap提供 7 种色彩空间，分别为 RGB、CMYK、RGBA、CMY、YIQ、YUV 和 YCC，可以适用于不同的系统之中。\n\n    :var ColorSpaceType.RGB: 该类型主要在显示系统中使用。RGB 是红色，绿色，蓝色的缩写。RGB 色彩模式使用 RGB 模型为图像中每一个像素的 RGB 分量分配一个0~255范围内的强度值\n    :var ColorSpaceType.CMYK: 该类型主要在印刷系统使用。CMYK 分别为青色，洋红，黄，黑。它通过调整青色、品红、黄色三种基本色的浓度混合出各种颜色的颜料，利用黑色调节明度和纯度。\n    :var ColorSpaceType.RGBA: 该类型主要在显示系统中使用。RGB 是红色，绿色，蓝色的缩写，A则用来控制透明度。\n    :var ColorSpaceType.CMY: 该类型主要在印刷系统使用。CMY(Cyan,Magenta,Yellow)分别为青色，品红，黄。该类型通过调整青色、品红、黄色三种基本色的浓度混合出各种颜色的颜料。\n    :var ColorSpaceType.YIQ: 该类型主要用于北美电视系统(NTSC).\n    :var ColorSpaceType.YUV: 该类型主要用于欧洲电视系统(PAL).\n    :var ColorSpaceType.YCC: 该类型主要用于 JPEG 图像格式。\n    :var ColorSpaceType.UNKNOW: 未知\n    "
    RGB = 1
    CMYK = 4
    RGBA = 2
    CMY = 3
    YIQ = 5
    YUV = 6
    YCC = 7
    UNKNOW = 0

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.ColorSpaceType"


@unique
class ColorGradientType(JEnum):
    __doc__ = "\n    该类定义了颜色渐变类型常量。\n\n    颜色渐变是多种颜色间的逐渐混合，可以是从起始色到终止色两种颜色的渐变，或者在起始色到终止色之间具有多种中间颜色进行渐变。该颜色渐变类型可应用于专题图对象的颜色方案设置中如：单值专题图、 分段专题图、 统计专题图、标签专题图、栅格分段专题图和栅格单值专题图。\n\n    :var ColorGradientType.BLACKWHITE: 黑白渐变色\n    :var ColorGradientType.REDWHITE: 红白渐变色\n    :var ColorGradientType.GREENWHITE: 绿白渐变色\n    :var ColorGradientType.BLUEWHITE: 蓝白渐变色\n    :var ColorGradientType.YELLOWWHITE: 黄白渐变色\n    :var ColorGradientType.PINKWHITE: 粉红白渐变色\n    :var ColorGradientType.CYANWHITE: 青白渐变色\n    :var ColorGradientType.REDBLACK: 红黑渐变色\n    :var ColorGradientType.GREENBLACK: 绿黑渐变色\n    :var ColorGradientType.BLUEBLACK: 蓝黑渐变色\n    :var ColorGradientType.YELLOWBLACK: 黄黑渐变色\n    :var ColorGradientType.PINKBLACK: 粉红黑渐变色\n    :var ColorGradientType.CYANBLACK: 青黑渐变色\n    :var ColorGradientType.YELLOWRED: 黄红渐变色\n    :var ColorGradientType.YELLOWGREEN: 黄绿渐变色\n    :var ColorGradientType.YELLOWBLUE: 黄蓝渐变色\n    :var ColorGradientType.GREENBLUE: 绿蓝渐变色\n    :var ColorGradientType.GREENRED: 绿红渐变色\n    :var ColorGradientType.BLUERED: 蓝红渐变色\n    :var ColorGradientType.PINKRED: 粉红红渐变色\n    :var ColorGradientType.PINKBLUE: 粉红蓝渐变色\n    :var ColorGradientType.CYANBLUE: 青蓝渐变色\n    :var ColorGradientType.CYANGREEN: 青绿渐变色\n    :var ColorGradientType.RAINBOW: 彩虹色\n    :var ColorGradientType.GREENORANGEVIOLET: 绿橙紫渐变色\n    :var ColorGradientType.TERRAIN: 地形渐变\n    :var ColorGradientType.SPECTRUM: 光谱渐变\n\n    "
    BLACKWHITE = 0
    REDWHITE = 1
    GREENWHITE = 2
    BLUEWHITE = 3
    YELLOWWHITE = 4
    PINKWHITE = 5
    CYANWHITE = 6
    REDBLACK = 7
    GREENBLACK = 8
    BLUEBLACK = 9
    YELLOWBLACK = 10
    PINKBLACK = 11
    CYANBLACK = 12
    YELLOWRED = 13
    YELLOWGREEN = 14
    YELLOWBLUE = 15
    GREENBLUE = 16
    GREENRED = 17
    BLUERED = 18
    PINKRED = 19
    PINKBLUE = 20
    CYANBLUE = 21
    CYANGREEN = 22
    RAINBOW = 23
    GREENORANGEVIOLET = 24
    TERRAIN = 25
    SPECTRUM = 26

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.ColorGradientType"


@unique
class NeighbourUnitType(JEnum):
    __doc__ = "\n    该类定义了邻域分析的单位类型常量。\n\n    :var NeighbourUnitType.CELL: 栅格坐标，即使用栅格数作为邻域单位。\n    :var NeighbourUnitType.MAP: 地理坐标，即使用地图的长度单位作为邻域单位。\n    "
    CELL = 1
    MAP = 2

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialanalyst.NeighbourUnitType"


@unique
class GriddingLevel(JEnum):
    __doc__ = "\n    对于几何面对象的查询(GeometriesRelation)，通过设置面对象的格网化，可以加快判断速度，比如面包含点判断。 单个面对象的格网化\n    等级越高，所需的内存也越多，一般适用于面对象少但单个面对象比较大的情形。\n\n    :var GriddingLevel.NONE: 无格网化\n    :var GriddingLevel.LOWER: 低等级格网化，对每个面使用 32*32 个方格进行格网化\n    :var GriddingLevel.MIDDLE: 中等级格网化，对每个面使用 64*64 个方格进行格网化\n    :var GriddingLevel.NORMAL: 一般等级格网化，对每个面使用 128*128 个方格进行格网化\n    :var GriddingLevel.HIGHER: 高等级格网化，对每个面使用 256*256 个方格进行格网化\n    "
    NONE = 0
    LOWER = 1
    MIDDLE = 2
    NORMAL = 3
    HIGHER = 4

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.GriddingLevel"


@unique
class TerrainInterpolateType(JEnum):
    __doc__ = "\n    地形插值类型常量\n\n    :var TerrainInterpolateType.IDW: 距离反比权值插值法。参考 :py:attr:`.InterpolationAlgorithmType.IDW`\n    :var TerrainInterpolateType.KRIGING: 克吕金内插法。参考 :py:attr:`.InterpolationAlgorithmType.KRIGING`\n    :var TerrainInterpolateType.TIN: 不规则三角网。先将给定的线数据集生成一个TIN模型，然后根据给定的极值点信息以及湖信息生成DEM模型。\n    "
    IDW = 1
    KRIGING = 2
    TIN = 3

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialanalyst.TerrainInterpolateType"


@unique
class TerrainStatisticType(JEnum):
    __doc__ = "\n    地形统计类型常量\n\n    :var TerrainStatisticType.UNIQUE: 去重复点统计。\n    :var TerrainStatisticType.MEAN: 平均数统计。\n    :var TerrainStatisticType.MIN: 最小值统计。\n    :var TerrainStatisticType.MAX: 最大值统计。\n    :var TerrainStatisticType.MAJORITY: 众数指的是出现频率最高的栅格值。目前只用于栅格分带统计。\n    :var TerrainStatisticType.MEDIAN: 中位数指的是按栅格值从小到大排列，位于中间位置的栅格值。目前只用于栅格分带统计。\n    "
    UNIQUE = 1
    MEAN = 2
    MIN = 3
    MAX = 4
    MAJORITY = 5
    MEDIAN = 6

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialanalyst.TerrainStatisticType"


@unique
class StreamOrderType(JEnum):
    __doc__ = "\n    流域水系编号（即河流分级）方法类型常量\n\n    :var StreamOrderType.STRAHLER: Strahler 河流分级法。Strahler 河流分级法由 Strahler 于 1957 年提出。其规则定义为：直接发\n                                   源于河源的河流为 1 级河流；同级的两条河流交汇形成的河流的等级比原来增加 1 级；不同等级的两\n                                   条河流交汇形成的河流的级等于原来河流中级等较高者。\n\n                                   .. image:: ../image/Strahler.png\n\n    :var StreamOrderType.SHREVE: Shreve 河流分级法。Shreve 河流分级法由 Shreve 于 1966 年提出。其规则定义为：直接发源于河源\n                                 的河流等级为 1 级，两条河流交汇形成的河流的等级为两条河流等级的和。例如，两条 1 级河流交汇形\n                                 成 2 级河流，一条 2 级河流和一条 3 级河流交汇形成一条 5 级河流。\n\n                                 .. image:: ../image/Shreve.png\n    "
    STRAHLER = 1
    SHREVE = 2

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.terrainanalyst.StreamOrderType"


@unique
class AggregationMethod(JEnum):
    __doc__ = "\n    用于通过事件点创建数据集进行分析的聚合方法常量\n\n    :var AggregationMethod.NETWORKPOLYGONS: 计算合适的网格大小,创建网格面数据集，生成的网格面数据集以面网格单元的点计数将作\n                                            为分析字段执行热点分析。网格会覆盖在输入事件点的上方，并将计算每个面网格单元内的\n                                            点数目。如果未提供事件点发生区域的边界面数据(参阅 :py:func:`optimized_hot_spot_analyst` 的 bounding_polygons 参数),\n                                            则会利用输入事件点数据集范围划分网格，并且会删除不含点的面网格单元，仅会分析剩下的\n                                            面网格单元;如果提供了边界面数据，则只会保留并分析在边界面数据集范围内的面网格单元。\n\n    :var AggregationMethod.AGGREGATIONPOLYGONS: 需要提供聚合事件点以获得事件计数的面数据集（参阅 参阅 :py:func:`optimized_hot_spot_analyst` 的 aggregating_polygons 参数）,\n                                                将计算每个面对象内的点事件数目，然后对面数据集以点事件数目作为分析字段执行热点分析。\n\n    :var AggregationMethod.SNAPNEARBYPOINTS: 为输入事件点数据集计算捕捉距离并使用该距离聚合附近的事件点，为每个聚合点提供一个\n                                             点计数，代表聚合到一起的事件点数目，然后对生成聚合点数据集以聚合在一起的点事件数\n                                             目作为分析字段执行热点分析\n    "
    NETWORKPOLYGONS = 1
    AGGREGATIONPOLYGONS = 2
    SNAPNEARBYPOINTS = 3

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialstatistics.AggregationMethod"


@unique
class KernelType(JEnum):
    __doc__ = "\n    地理加权回归分析带宽类型常量\n\n    :var KernelType.FIXED: 固定型带宽。针对每个回归分析点，使用一个固定的值作为带宽范围。\n    :var KernelType.ADAPTIVE: 可变型带宽。针对每个回归分析点，使用回归点与第K个最近相邻点之间的距离作为带宽范围。其中,K为相邻数目。\n    "
    FIXED = 1
    ADAPTIVE = 2

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialstatistics.KernelType"


@unique
class BandWidthType(JEnum):
    __doc__ = '\n    地理加权回归分析带宽确定方式常量。\n\n    :var BandWidthType.AICC: 使用" Akaike 信息准则（AICc）"确定带宽范围。\n    :var BandWidthType.CV: 使用"交叉验证"确定带宽范围。\n    :var BandWidthType.BANDWIDTH: 根据给定的固定距离或固定相邻数确定带宽范围。\n    '
    AICC = 1
    CV = 2
    BANDWIDTH = 3

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialstatistics.BandWidthType"


@unique
class KernelFunction(JEnum):
    __doc__ = "\n    地理加权回归分析核函数类型常量。\n\n    :var KernelFunction.GAUSSIAN: 高斯核函数。\n\n                                  高斯核函数计算公式:\n\n                                  W_ij=e^(-((d_ij/b)^2)/2)。\n\n                                  其中W_ij为点i和点j之间的权重，d_ij为点i和点j之间的距离,b为带宽范围。\n\n    :var KernelFunction.BISQUARE: 二次核函数。\n                                  二次核函数计算公式:\n\n                                  如果d_ij≤b, W_ij=(1-(d_ij/b)^2))^2;否则,W_ij=0。\n\n                                  其中W_ij为点i和点j之间的权重，d_ij为点i和点j之间的距离,b为带宽范围。\n\n    :var KernelFunction.BOXCAR: 盒状核函数。\n\n                                盒状核函数计算公式:\n\n                                如果d_ij≤b, W_ij=1;否则,W_ij=0。\n\n                                其中W_ij为点i和点j之间的权重，d_ij为点i和点j之间的距离,b为带宽范围。\n\n    :var KernelFunction.TRICUBE: 立方体核函数。\n\n                                 立方体核函数计算公式:\n\n                                 如果d_ij≤b, W_ij=(1-(d_ij/b)^3))^3;否则,W_ij=0。\n\n                                 其中W_ij为点i和点j之间的权重，d_ij为点i和点j之间的距离,b为带宽范围。\n    "
    GAUSSIAN = 1
    BISQUARE = 2
    BOXCAR = 3
    TRICUBE = 4

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialstatistics.KernelFunction"


@unique
class SpatialStatisticsType(JEnum):
    __doc__ = "\n    数据集进行空间度量后的字段统计类型常量\n\n    :var SpatialStatisticsType.MAX: 统计字段的最大值。只对数值型字段有效。\n    :var SpatialStatisticsType.MIN: 统计字段的最小值。只对数值型字段有效。\n    :var SpatialStatisticsType.SUM: 统计字段的和。只对数值型字段有效。\n    :var SpatialStatisticsType.MEAN: 统计字段的平均值。只对数值型字段有效。\n    :var SpatialStatisticsType.FIRST: 保留第一个对象的字段值。对数值、布尔、时间和文本型字段都有效。\n    :var SpatialStatisticsType.LAST: 保留最后一个对象的字段值。对数值、布尔、时间和文本型字段都有效。\n    :var SpatialStatisticsType.MEDIAN: 统计字段的中位数。只对数值型字段有效。\n    "
    MAX = 1
    MIN = 2
    SUM = 3
    MEAN = 4
    FIRST = 5
    LAST = 6
    MEDIAN = 7

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialstatistics.StatisticsType"


@unique
class DistanceMethod(JEnum):
    __doc__ = "\n    距离计算方法常量\n\n    :var DistanceMethod.EUCLIDEAN: 欧式距离。计算两点间的直线距离。\n\n                                   DistanceMethod_EUCLIDEAN.png\n\n    :var DistanceMethod.MANHATTAN: 曼哈顿距离。计算两点的x和y坐标的差值绝对值求和。该类型暂时不可用，仅作为测试,使用结果未知。\n\n                                   DistanceMethod_MANHATTAN.png\n    "
    EUCLIDEAN = 1
    MANHATTAN = 2

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialstatistics.DistanceMethod"


@unique
class EllipseSize(JEnum):
    __doc__ = "\n    输出椭圆的大小常量\n\n    :var EllipseSize.SINGLE: 一个标准差。输出椭圆的长半轴和短半轴是对应的标准差的一倍。当几何对象具有空间正态分布时，即这些几\n                             何对象在中心处集中而朝向外围时较少，则生成的椭圆将会包含约占总数68%的几何对象在内。\n\n                             .. image:: ../image/EllipseSize_SINGLE.png\n\n\n    :var EllipseSize.TWICE: 二个标准差。输出椭圆的长半轴和短半轴是对应的标准差的二倍。当几何对象具有空间正态分布时，即这些几\n                            何对象在中心处集中而朝向外围时较少，则生成的椭圆将会包含约占总数95%的几何对象在内。\n\n                            .. image:: ../image/EllipseSize_TWICE.png\n\n    :var EllipseSize.TRIPLE: 三个标准差。输出椭圆的长半轴和短半轴是对应的标准差的三倍。当几何对象具有空间正态分布时，即这些几\n                             何对象在中心处集中而朝向外围时较少，则生成的椭圆将会包含约占总数99%的几何对象在内。\n\n                             .. image:: ../image/EllipseSize_TRIPLE.png\n    "
    SINGLE = 1
    TWICE = 2
    TRIPLE = 3

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialstatistics.EllipseSize"


@unique
class EdgeMatchMode(JEnum):
    __doc__ = "\n    该枚举定义了图幅接边的方式常量。\n\n    :var EdgeMatchMode.THEOTHEREDGE: 向一边接边。接边连接点为接边目标数据集中发生接边关联的记录的端点，源数据集中接边关联到的记录的端点将移动到该连接点。\n    :var EdgeMatchMode.THEMIDPOINT: 在中点位置接边。 接边连接点为接边目标数据集和源数据集中发生接边关联记录端点的中点，源和目标数据集中发生接边关联的记录的端点将移动到该连接点。\n    :var EdgeMatchMode.THEINTERSECTION: 在交点位置接边。接边连接点为接边目标数据集和源数据集中发生接边关联记录端点的连线和接边线的交点，源和目标数据集中发生接边关联的记录的端点将移动到该连接点。\n    "
    THEOTHEREDGE = 1
    THEMIDPOINT = 2
    THEINTERSECTION = 3

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialanalyst.EdgeMatchMode"


@unique
class FunctionType(JEnum):
    __doc__ = "\n    变换函数类型常量\n\n    :var FunctionType.NONE: 不使用变换函数。\n    :var FunctionType.LOG: 变换函数为log，要求原值大于0。\n    :var FunctionType.ARCSIN: 变换函数为 arcsin，要求原值在范围[-1,1]内。\n    "
    NONE = 1
    LOG = 2
    ARCSIN = 3

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialanalyst.FunctionType"


@unique
class StatisticsCompareType(JEnum):
    __doc__ = "\n    比较类型常量\n\n    :var StatisticsCompareType.LESS: 小于。\n    :var StatisticsCompareType.LESS_OR_EQUAL: 小于或等于。\n    :var StatisticsCompareType.EQUAL: 等于。\n    :var StatisticsCompareType.GREATER: 大于。\n    :var StatisticsCompareType.GREATER_OR_EQUAL: 大于或等于。\n    "
    LESS = 1
    LESS_OR_EQUAL = 2
    EQUAL = 3
    GREATER = 4
    GREATER_OR_EQUAL = 5

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialanalyst.StatisticsCompareType"


@unique
class GridStatisticsMode(JEnum):
    __doc__ = "\n    栅格统计类型常量\n\n    :var GridStatisticsMode.MIN: 最小值\n    :var GridStatisticsMode.MAX: 最大值\n    :var GridStatisticsMode.MEAN: 平均值\n    :var GridStatisticsMode.STDEV: 标准差\n    :var GridStatisticsMode.SUM: 总和\n    :var GridStatisticsMode.VARIETY: 种类\n    :var GridStatisticsMode.RANGE: 值域，即最大值与最小值的差\n    :var GridStatisticsMode.MAJORITY: 众数（出现频率最高的栅格值）\n    :var GridStatisticsMode.MINORITY: 最少数（出现频率最低的栅格值）\n    :var GridStatisticsMode.MEDIAN: 中位数（将所有栅格的值从小到大排列，取位于中间位置的栅格值）\n    "
    MIN = 1
    MAX = 2
    MEAN = 3
    STDEV = 4
    SUM = 5
    VARIETY = 6
    RANGE = 7
    MAJORITY = 8
    MINORITY = 9
    MEDIAN = 10

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialanalyst.GridStatisticsMode"


@unique
class ConceptualizationModel(JEnum):
    __doc__ = '\n    空间关系概念化模型常量\n\n    :var ConceptualizationModel.INVERSEDISTANCE: 反距离模型。任何要素都会影响目标要素,但是随着距离的增加,影响会越小。要素之间的权重为距离分之一。\n    :var ConceptualizationModel.INVERSEDISTANCESQUARED: 反距离平方模型。与"反距离模型"相似,随着距离的增加,影响下降的更快。要素之间的权重为距离的平方分之一。\n    :var ConceptualizationModel.FIXEDDISTANCEBAND: 固定距离模型。在指定的固定距离范围内的要素具有相等的权重（权重为1）,在指定的固定距离范围之外的要素不会影响计算（权重为0）。\n    :var ConceptualizationModel.ZONEOFINDIFFERENCE: 无差别区域模型。 该模型是"反距离模型"和"固定距离模型"的结合。在指定的固定距离范围内的要素具有相等的权重（权重为1）;在指定的固定距离范围之外的要素,随着距离的增加,影响会越小。\n    :var ConceptualizationModel.CONTIGUITYEDGESONLY: 面邻接模型。只有面面在有共享边界、重叠、包含、被包含的情况才会影响目标要素（权重为1）,否则,将会排除在目标要素计算之外（权重为0）。\n    :var ConceptualizationModel.CONTIGUITYEDGESNODE: 面邻接模型。只有面面在有接触的情况才会影响目标要素（权重为1）,否则,将会排除在目标要素计算之外（权重为0）。\n    :var ConceptualizationModel.KNEARESTNEIGHBORS: K最邻近模型。 距目标要素最近的K个要素包含在目标要素的计算中（权重为1）,其余的要素将会排除在目标要素计算之外（权重为0）。\n    :var ConceptualizationModel.SPATIALWEIGHTMATRIXFILE: 提供空间权重矩阵文件。\n    '
    INVERSEDISTANCE = 1
    INVERSEDISTANCESQUARED = 2
    FIXEDDISTANCEBAND = 3
    ZONEOFINDIFFERENCE = 4
    CONTIGUITYEDGESONLY = 5
    CONTIGUITYEDGESNODE = 6
    KNEARESTNEIGHBORS = 7
    SPATIALWEIGHTMATRIXFILE = 8

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialstatistics.ConceptualizationModel"


@unique
class LineToPointMode(JEnum):
    __doc__ = "\n    线转点的方式\n\n    :var LineToPointMode.VERTEX: 节点模式，将线对象的每个节点都转换为一个点对象\n    :var LineToPointMode.INNER_POINT: 内点模式，将线对象的内点转换为一个点对象\n    :var LineToPointMode.SUB_INNER_POINT: 子对象内点模式，将线对象的每个子对象的内点分别转换为一个点对象，如果线的子对象数目为1，将与 INNER_POINT 的结果相同。\n    :var LineToPointMode.START_NODE: 起始点模式，将线对象的第一个节点，即起点，转换为一个点对象\n    :var LineToPointMode.END_NODE: 终止点模式，将线对象的最后一个节点，即终点，转换为一个点对象\n    :var LineToPointMode.START_END_NODE: 起始终止点模式，将线对象的起点和终点分别转换为一个点对象\n    :var LineToPointMode.SEGMENT_INNER_POINT: 线段内点模式，将线对象的每个线段的内点，分别转换为一个点对象，线段指的是相邻两个节点构成的线。\n    :var LineToPointMode.SUB_START_NODE: 子对象起始点模式，将线对象的每个子对象的第一个点，分别转换为一个点对象\n    :var LineToPointMode.SUB_END_NODE: 子对象终止点模式，将线对象的每个子对象的对后一个点，分别转换为一个点对象\n    :var LineToPointMode.SUB_START_END_NODE: 子对象起始终止点模式，将线对象的每个子对象的第一个点和最后一个点，分别转换为一个点对象。\n\n    "
    VERTEX = 1
    INNER_POINT = 2
    SUB_INNER_POINT = 3
    START_NODE = 4
    END_NODE = 5
    START_END_NODE = 6
    SEGMENT_INNER_POINT = 7
    SUB_START_NODE = 8
    SUB_END_NODE = 9
    SUB_START_END_NODE = 10

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.jsuperpy.LineToPointMode"


@unique
class RegionToPointMode(JEnum):
    __doc__ = "\n    面转点的方式\n\n    :var RegionToPointMode.VERTEX: 节点模式，将面对象的每个节点都转换为一个点对象\n    :var RegionToPointMode.INNER_POINT: 内点模式，将面对象的内点转换为一个点对象\n    :var RegionToPointMode.SUB_INNER_POINT: 子对象内点模式，将面对象的每个子对象的内点分别转换为一个点对象\n    :var RegionToPointMode.TOPO_INNER_POINT: 拓扑内点模式，对复杂面对象进行保护性分解后得到的多个面对象的内点，分别转换为一个子对象。\n    "
    VERTEX = 1
    INNER_POINT = 2
    SUB_INNER_POINT = 3
    TOPO_INNER_POINT = 4

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.jsuperpy.RegionToPointMode"


@unique
class AttributeStatisticsMode(JEnum):
    __doc__ = "\n    在进行点连接成线时和矢量数据集属性更新时，进行属性统计的模式。\n\n    :var AttributeStatisticsMode.MAX: 统计最大值，可以对数值型、文本型和时间类型的字段进行统计。\n    :var AttributeStatisticsMode.MIN: 统计最小值，可以对数值型、文本型和时间类型的字段进行统计。\n    :var AttributeStatisticsMode.SUM: 统计一组数的和，只对数值型字段有效\n    :var AttributeStatisticsMode.MEAN: 统计一组数的平均值，只对数值型字段有效\n    :var AttributeStatisticsMode.STDEV: 统计一组数的标准差，只对数值型字段有效\n    :var AttributeStatisticsMode.VAR: 统计一组数的方差，只对数值型字段有效\n    :var AttributeStatisticsMode.MODALVALUE: 取众数，众数是出现频率最高的的值，可以是任何类型字段\n    :var AttributeStatisticsMode.RECORDCOUNT: 统计一组数的记录数。统计记录数不针对特定的字段，只针对一个分组。\n    :var AttributeStatisticsMode.MAXINTERSECTAREA: 取相交面积最大。如果面对象与提供属性的多个面对象相交，则取与原面对象相交面积最大的对象属性值用于更新。对任意类型的字段有效。\n                                                   只对矢量数据集属性更新（ :py:func:`update_attributes` )有效\n    "
    MAX = 1
    MIN = 2
    SUM = 3
    MEAN = 4
    STDEV = 5
    VAR = 6
    MODALVALUE = 7
    COUNT = 8
    MAXINTERSECTAREA = 9

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.jsuperpy.StatisticsMode"


@unique
class VCTVersion(JEnum):
    __doc__ = "\n    VCT 版本\n\n    :var VCTVersion.CNSDTF_VCT: 国家自然标准 1.0\n    :var VCTVersion.LANDUSE_VCT: 国家土地利用 2.0\n    :var VCTVersion.LANDUSE_VCT30: 国家土地利用 3.0\n    "
    CNSDTF_VCT = 1
    LANDUSE_VCT = 3
    LANDUSE_VCT30 = 6

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.conversion.VCTVersion"


@unique
class RasterJoinType(JEnum):
    __doc__ = "\n    定义了镶嵌结果栅格值的统计类型常量。\n\n    :var RasterJoinType.RJMFIRST: 栅格重叠区域镶嵌后取第一个栅格数据集中的值。\n    :var RasterJoinType.RJMLAST: 栅格重叠区域镶嵌后取最后一个栅格数据集中的值。\n    :var RasterJoinType.RJMMAX: 栅格重叠区域镶嵌后取所有栅格数据集中相应位置的最大值。\n    :var RasterJoinType.RJMMIN: 栅格重叠区域镶嵌后取所有栅格数据集中相应位置的最小值。\n    :var RasterJoinType.RJMMean: 栅格重叠区域镶嵌后取所有栅格数据集中相应位置的平均值。\n    "
    RJMFIRST = 0
    RJMLAST = 1
    RJMMAX = 2
    RJMMIN = 3
    RJMMean = 4

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialanalyst.RasterJoinType"


@unique
class RasterJoinPixelFormat(JEnum):
    __doc__ = "\n    定义了镶嵌结果像素格式类型常量。\n\n    :var RasterJoinPixelFormat.RJPMONO: 即 PixelFormat.UBIT1。\n    :var RasterJoinPixelFormat.RJPFBIT: 即 PixelFormat.UBIT4\n    :var RasterJoinPixelFormat.RJPBYTE: 即 PixelFormat.UBIT8\n    :var RasterJoinPixelFormat.RJPTBYTE: 即 PixelFormat.BIT16\n    :var RasterJoinPixelFormat.RJPRGB: 即 PixelFormat.RGB\n    :var RasterJoinPixelFormat.RJPRGBAFBIT: 即 PixelFormat.RGBA\n    :var RasterJoinPixelFormat.RJPLONGLONG: 即 PixelFormat.BIT64\n    :var RasterJoinPixelFormat.RJPLONG: 即 PixelFormat.BIT32\n    :var RasterJoinPixelFormat.RJPFLOAT: 即 PixelFormat.SINGLE\n    :var RasterJoinPixelFormat.RJPDOUBLE: 即 PixelFormat.DOUBLE\n    :var RasterJoinPixelFormat.RJPFIRST: 参与镶嵌的第一个栅格数据集的像素格式。\n    :var RasterJoinPixelFormat.RJPLAST: 参与镶嵌的最后一个栅格数据集的像素格式。\n    :var RasterJoinPixelFormat.RJPMAX: 参与镶嵌的栅格数据集中最大的像素格式。\n    :var RasterJoinPixelFormat.RJPMIN: 参与镶嵌的栅格数据集中最小的像素格式。\n    :var RasterJoinPixelFormat.RJPMAJORITY: 参与镶嵌的栅格数据集中出现频率最高的像素格式，如果像素格式出现的频率相同，取索引值最小的。\n\n    "
    RJPMONO = 1
    RJPFBIT = 4
    RJPBYTE = 8
    RJPTBYTE = 16
    RJPRGB = 24
    RJPRGBAFBIT = 32
    RJPLONGLONG = 64
    RJPLONG = 320
    RJPFLOAT = 3200
    RJPDOUBLE = 6400
    RJPFIRST = 10000
    RJPLAST = 20000
    RJPMAX = 30000
    RJPMIN = 40000
    RJPMAJORITY = 50000

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialanalyst.RasterJoinPixelFormat"

    @classmethod
    def _externals(cls):
        return {'UBIT1':RasterJoinPixelFormat.RJPMONO,  'UBIT4':RasterJoinPixelFormat.RJPFBIT, 
         'UBIT8':RasterJoinPixelFormat.RJPBYTE, 
         'BIT16':RasterJoinPixelFormat.RJPTBYTE, 
         'RGB':RasterJoinPixelFormat.RJPRGB, 
         'RGBA':RasterJoinPixelFormat.RJPRGBAFBIT, 
         'BIT32':RasterJoinPixelFormat.RJPLONG, 
         'SINGLE':RasterJoinPixelFormat.RJPFLOAT, 
         'DOUBLE':RasterJoinPixelFormat.RJPDOUBLE, 
         'FIRST':RasterJoinPixelFormat.RJPFIRST, 
         'LAST':RasterJoinPixelFormat.RJPLAST, 
         'MAX':RasterJoinPixelFormat.RJPMAX, 
         'MIN':RasterJoinPixelFormat.RJPMIN, 
         'MAJORITY':RasterJoinPixelFormat.RJPMAJORITY}


@unique
class PlaneType(JEnum):
    __doc__ = "\n    平面类型常量\n    :var PlaneType.PLANEXY:由X、Y坐标方向构成的平面，即XY平面\n    :var PlaneType.PLANEYZ:由X、Z坐标方向构成的平面，即YZ平面\n    :var PlaneType.PLANEXZ:由Y、Z坐标方向构成的平面，即XZ平面\n    "
    PLANEXY = 0
    PLANEYZ = 1
    PLANEXZ = 2

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.PlaneType"


@unique
class ChamferStyle(JEnum):
    __doc__ = "\n    放样的倒角样式类型常量\n    :var ChamferStyle.SOBC_CIRCLE_ARC:二阶贝塞尔曲线(the second order bezier curve)圆弧\n    :var ChamferStyle.SOBC_ELLIPSE_ARC:二阶贝塞尔曲线(the second order bezier curve)椭圆弧\n    "
    SOBC_CIRCLE_ARC = 0
    SOBC_ELLIPSE_ARC = 1

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.realspace.threeddesigner.ChamferStyle"


@unique
class PlaneType(JEnum):
    __doc__ = "\n    平面类型常量\n    :var PlaneType.PLANEXY:由X、Y坐标方向构成的平面，即XY平面\n    :var PlaneType.PLANEYZ:由X、Z坐标方向构成的平面，即YZ平面\n    :var PlaneType.PLANEXZ:由Y、Z坐标方向构成的平面，即XZ平面\n    "
    PLANEXY = 0
    PLANEYZ = 1
    PLANEXZ = 2

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.PlaneType"


@unique
class Buffer3DJoinType(JEnum):
    __doc__ = "\n    放样的倒角样式类型常量\n    :var Buffer3DJoinType.SQUARE:尖角衔接样式\n    :var Buffer3DJoinType.ROUND:圆角衔接样式\n    :var Buffer3DJoinType.MITER:斜角衔接样式\n    "
    SQUARE = 0
    ROUND = 1
    MITER = 2

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.realspace.threeddesigner.JoinType"


@unique
class ViewShedType(JEnum):
    __doc__ = "\n    该类定义了对多个观察点（被观察点）进行可视域分析时，可视域的类型常量。\n    :var ViewShedType.VIEWSHEDINTERSECT: 共同可视域，取多个观察点可视域范围的交集。\n    :var ViewShedType.VIEWSHEDUNION: 非共同可视域，取多个观察点可视域范围的并集。\n    "
    VIEWSHEDINTERSECT = 0
    VIEWSHEDUNION = 1

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialanalyst.ViewShedType"


@unique
class ImageType(JEnum):
    __doc__ = "\n    该类定义了地图出图的图片类型常量\n\n    :var ImageType.BMP: BMP 是 Windows 使用的一种标准格式，用于存储设备无关和应用程序无关的图像。一个给定 BMP 文件的每像素位数值（1、4、8、15、24、32 或 64）在文件头中指定。每像素 24 位的 BMP 文件是通用的。BMP 文件通常是不压缩的，因此，不太适合通过 Internet 传输。\n    :var ImageType.GIF: GIF 是一种用于在网页中显示图像的通用格式。GIF 文件适用于画线、有纯色块的图片和在颜色之间有清晰边界的图片。GIF 文件是压缩的，但是在压缩过程中没有信息丢失；解压缩的图像与原始图像完全一样。GIF 文件中的一种颜色可以被指定为透明，这样，图像将具有显示它的任何网页的背景色。在单个文件中存储一系列 GIF 图像可以形成一个动画 GIF。GIF 文件每像素最多能存储 8 位，所以它们只限于使用 256 种颜色。\n    :var ImageType.JPG: JPEG 是一种适应于自然景观（如扫描的照片）的压缩方案。一些信息会在压缩过程中丢失，但是这些丢失人眼是察觉不到的。JPEG 文件每像素存储 24 位，因此它们能够显示超过 16,000,000 种颜色。JPEG 文件不支持透明或动画。JPEG 不是一种文件格式。“JPEG 文件交换格式 (JFIF)”是一种文件格式，常用于存储和传输已根据 JPEG 方案压缩的图像。Web 浏览器显示的 JFIF 文件使用 .jpg 扩展名。\n    :var ImageType.PDF: PDF(Portable Document Format) 文件格式是 Adobe 公司开发的电子文件格式。这种文件格式与操作系统平台无关，也就是说，PDF 文件不管是在 Windows，Unix 还是在苹果公司的 Macos 操作系统中都是通用的\n    :var ImageType.PNG: PNG 类型。PNG 格式不但保留了许多 GIF 格式的优点，还提供了超出 GIF 的功能。像 GIF 文件一样，PNG 文件在压缩时也不损失信息。PNG 文件能以每像素 8、24 或 48 位来存储颜色，并以每像素 1、2、4、8 或 16 位来存储灰度。相比之下，GIF 文件只能使用每像素 1、2、4 或 8 位。PNG 文件还可为每个像素存储一个 alpha 值，该值指定了该像素颜色与背景颜色混合的程度。PNG 优于 GIF 之处在于，它能渐进地显示一幅图像（也就是说，在图像通过网络连接传递的过程中，显示的图像将越来越完整）。PNG 文件可包含灰度校正和颜色校正信息，以便图像可在各种各样的显示设备上精确地呈现。\n    :var ImageType.TIFF: TIFF 是一种灵活的和可扩展的格式，各种各样的平台和图像处理应用程序都支持这种格式。TIFF 文件能以每像素任意位来存储图像，并可以使用各种各样的压缩算法。单个的多页 TIFF 文件可以存储数幅图像。可以把与图像相关的信息（扫描仪制造商、主机、压缩类型、打印方向和每像素采样，等等）存储在文件中并使用标签来排列这些信息。可以根据需要通过批准和添加新标签来扩展 TIFF 格式。\n    "
    BMP = 121
    GIF = 124
    JPG = 122
    PDF = 33
    PNG = 123
    TIFF = 103

    @classmethod
    def _externals(cls):
        return {"tif": (cls.TIFF)}

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.mapping.ImageType"


@unique
class FillGradientMode(JEnum):
    __doc__ = "\n    定义渐变填充模式的渐变模式。所有渐变模式都是两种颜色之间的渐变，即从渐变起始色到渐变终止色之间的渐变。\n\n    对于不同的渐变模式风格，可以在 :py:class:`GeoStyle` 中对其旋转角度，渐变的起始色（前景色）和终止色（背景色），渐变填充中心点的位置（对线性渐变无效）等进行设置。默认情况下，渐变旋转角度为0，渐变填充中心点为填充区域范围的中心点。以下对各种渐变模式的说明都采用默认的渐变旋转角度和中心点。\n    关于渐变填充旋转的详细信息，请参见 :py:class:`GeoStyle`  类中的 :py:meth:`set_fill_gradient_angle` 方法;\n    关于渐变填充中心点的设置，请参见 :py:class:`GeoStyle`  类中的 :py:meth:`set_fill_gradient_offset_ratio_x` 和 :py:meth:`set_fill_gradient_offset_ratio_y` 方法。\n    渐变风格的计算都是以填充区域的边界矩形，即最小外接矩形作为基础的，因而以下提到的填充区域范围即为填充区域的最小外接矩形。\n\n    :var FillGradientMode.NONE: 无渐变。当使用普通填充模式时，设置渐变模式为无渐变\n    :var FillGradientMode.LINEAR: 线性渐变。从水平线段的起始点到终止点的渐变。如图所示，从水平线段的起始点到终止点，其颜色从起始色均匀渐变到终止色，垂直于该线段的直线上颜色相同，不发生渐变\n\n                                 .. image:: ../image/Gra_Linear.png\n\n    :var FillGradientMode.RADIAL: 辐射渐变。 以填充区域范围的中心点作为渐变填充的起始点，距离中心点最远的边界点作为终止点的圆形渐变。注意在同一个圆周上颜色不发生变化，不同的圆之间颜色发生渐变。\n                                  如图所示，从渐变填充的起始点到终止点，其以起始点为圆心的各个圆的颜色随着圆的半径的增大从起始色均匀渐变到终止色\n\n                                  .. image:: ../image/Gra_Radial.png\n\n    :var FillGradientMode.CONICAL: 圆锥渐变。从起始母线到终止母线，渐变在逆时针和顺时针两个方向发生渐变，都是从起始色渐变到终止色。注意填充区域范围中心点为圆锥的顶点，在圆锥的母线上颜色不发生变化。\n                                   如图所示，渐变的起始母线在填充区域范围中心点右侧的并经过该中心点的水平线上，上半圆锥颜色按逆时针发生渐变，下半圆锥按顺时针发生渐变，两个方向渐变的起始母线和终止母线分别相同，在逆时针方向和顺时针方向两个方向从起始母线转到终止母线的过程中，渐变都是从起始色均匀渐变到终止色\n\n                                  .. image:: ../image/Gra_Conical.png\n\n    :var FillGradientMode.SQUARE: 四角渐变。以填充区域范围的中心点作为渐变填充的起始点，以填充区域范围的最小外接矩形的较短边的中点为终止点的正方形渐变。注意在每个正方形上的颜色不发生变化, 不同的正方形之间颜色发生变化。\n                                  如图所示，从渐变填充的起始点到终止点，其以起始点为中心的正方形的颜色随着边长的增大从起始色均匀渐变到终止色\n\n                                  .. image:: ../image/Gra_Square2.png\n\n    "
    NONE = 0
    LINEAR = 1
    RADIAL = 2
    CONICAL = 3
    SQUARE = 4

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.FillGradientMode"


@unique
class ImageInterpolationMode(JEnum):
    __doc__ = "\n    该类定义了影像插值模式常量。\n\n    :var ImageInterpolationMode.NEARESTNEIGHBOR: 最临近插值模式。\n    :var ImageInterpolationMode.LOW: 低质量插值模式。\n    :var ImageInterpolationMode.HIGH: 高质量插值模式。\n    :var ImageInterpolationMode.DEFAULT: 默认插值模式。\n    :var ImageInterpolationMode.HIGHQUALITYBICUBIC: 高质量的双线性插值模式。 \n    :var ImageInterpolationMode.HIGHQUALITYBILINEAR: 最高质量的双三次插值法模式。\n    "
    NEARESTNEIGHBOR = 0
    LOW = 1
    HIGH = 2
    DEFAULT = 3
    HIGHQUALITYBICUBIC = 5
    HIGHQUALITYBILINEAR = 4

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.mapping.ImageInterpolationMode"


@unique
class ImageDisplayMode(JEnum):
    __doc__ = "\n    影像显示模式，目前支持组合模式和拉伸模式两种。\n\n    :var ImageDisplayMode.COMPOSITE: 组合模式。 组合模式针对多波段影像，影像按照设置的波段索引顺序组合为RGB显示，目前只支持RGB和RGBA色彩空间的显示。\n    :var ImageDisplayMode.STRETCHED: 拉伸模式。拉伸模式支持所有影像（包括单波段和多波段），针对多波段影像，当设置了该显示模式后，将显示设置的波段索引的第一个波段去显示。\n\n    "
    COMPOSITE = 0
    STRETCHED = 1

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.mapping.ImageDisplayMode"


@unique
class MapColorMode(JEnum):
    __doc__ = "\n    该类定义了地图颜色模式类型常量。\n\n    该颜色模式只是针对地图显示而言，而且只对矢量要素起作用。 各颜色模式在转换时，地图的专题风格不会改变，而且各种颜色模式的转换是根据\n    地图的专题风格颜色来的。 SuperMap 组件产品在设置地图风格时，提供了5种颜色模式。\n\n    :var MapColorMode.DEFAULT: 默认彩色模式，对应 32 位增强真彩色模式。用 32 个比特来存储颜色，其中红，绿，蓝和 alpha 各用 8 比特来表示。\n    :var MapColorMode.BLACK_WHITE: 黑白模式。根据地图的专题风格（默认彩色模式），将地图要素用两种颜色显示：黑色和白色。 专题风格颜色为白色的要素仍显示成白色，其余颜色都以黑色显示。\n    :var MapColorMode.GRAY: 灰度模式。根据地图的专题风格（默认彩色模式），对红，绿，蓝分量设置不同的权重，以灰度显示出来。\n    :var MapColorMode.BLACK_WHITE_REVERSE: 黑白反色模式。根据地图的专题风格（默认彩色模式），专题风格颜色为黑色的要素转换成白色，其余颜色都以黑色显示\n    :var MapColorMode.ONLY_BLACK_WHITE_REVERSE: 黑白反色，其它颜色不变。根据地图的专题风格（默认彩色模式），把专题风格颜色为黑色的要素 转换成白色，专题风格颜色为白色的要素转换成黑色，其它颜色不变。\n\n    "
    DEFAULT = 0
    BLACK_WHITE = 1
    GRAY = 2
    BLACK_WHITE_REVERSE = 3
    ONLY_BLACK_WHITE_REVERSE = 4

    @classmethod
    def _externals(cls):
        return {"BLACKWHITE": (cls.BLACK_WHITE)}

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.mapping.MapColorMode"


@unique
class LayerGridAggregationType(JEnum):
    __doc__ = "\n    网格聚合图的格网类型。\n\n    :var LayerGridAggregationType.QUADRANGLE: 矩形格网\n    :var LayerGridAggregationType.HEXAGON: 六边形格网\n    "
    QUADRANGLE = 1
    HEXAGON = 2

    @classmethod
    def _externals(cls):
        return {'Hex':cls.HEXAGON,  'Grid':cls.QUADRANGLE}

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.mapping.LayerGridAggregationType"


@unique
class NeighbourNumber(JEnum):
    __doc__ = "\n    空间连通性的邻域像元个数\n\n    :var NeighbourNumber.FOUR: 上下左右4个像元作为邻近像元。仅当具有相同值的像元与上下左右四个最邻近像元中的每个像元直接连接时，才\n                               会定义这些像元之间的连通性。正交像元会保留矩形区域的拐角。\n\n                               .. image:: ../image/four.png\n\n    :var NeighbourNumber.EIGHT: 相邻8个像元作为邻近像元。仅当具有相同值的像元位于彼此最近的8个最邻近像元时，才会定义这些像元间的连\n                                通性。八个相邻像元使矩形变得光滑。\n\n                                 .. image:: ../image/eight.png\n\n    "
    FOUR = 1
    EIGHT = 2

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialanalyst.NeighborNumber"


@unique
class MajorityDefinition(JEnum):
    __doc__ = "\n    在进行替换之前指定必须具有相同值的相邻（空间连接）像元数，即相邻像元的相同值在连续为多少时，才进行替换。\n\n    :var MajorityDefinition.HALF: 表示半数像元必须具有相同值并且相邻，即大于等于四分之二或八分之四的已连接像元必须具有相同值，此时\n                                  可获得更平滑的效果。\n    :var MajorityDefinition.MAJORITY: 表示多数像元必须具有相同值并且相邻，即大于等于四分之三或八分之五的已连接像元必须具有相同值。\n    "
    HALF = 1
    MAJORITY = 2

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialanalyst.MajorityDefinition"


@unique
class BoundaryCleanSortType(JEnum):
    __doc__ = "\n    边界清理的排序方法。即指定要在平滑处理中使用的排序类型。这将确定像元可扩展到相邻像元的优先级\n\n    :var BoundaryCleanSortType.NOSORT: 不按大小排序。值较大的区域具有较高的优先级，可以扩展到值较小的若干区域。\n    :var BoundaryCleanSortType.DESCEND: 以大小的降序顺序对区域进行排序。总面积较大的区域具有较高的优先级，可以扩展到总面积较小的\n                                        若干区域。\n    :var BoundaryCleanSortType.ASCEND: 以大小的升序顺序对区域进行排序。总面积较小的区域具有较高的优先级，可以扩展到总面积较大的\n                                       若干区域。\n    "
    NOSORT = 1
    DESCEND = 2
    ASCEND = 3

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialanalyst.BoundaryCleanSortType"


@unique
class OverlayAnalystOutputType(JEnum):
    __doc__ = "\n    叠加分析返回结果几何对象类型。只对面面相交算子有效。\n\n    :var OverlayAnalystOutputType.INPUT: 结果对象类型与输入的源数据类型保持一致\n    :var OverlayAnalystOutputType.POINT: 结果对象类型为点对象\n    "
    INPUT = 0
    POINT = 1

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.analyst.spatialanalyst.OverlayAnalystOutputType"


@unique
class FieldSign(JEnum):
    __doc__ = "\n    字段标识常量\n\n    :var FieldSign.ID: ID 字段\n    :var FieldSign.GEOMETRY: Geometry 字段\n    :var FieldSign.NODEID: NodeID 字段\n    :var FieldSign.FNODE: FNode 字段\n    :var FieldSign.TNODE: TNode 字段\n    :var FieldSign.EDGEID: EdgeID 字段\n    "
    ID = 11
    GEOMETRY = 12
    NODEID = 1
    FNODE = 2
    TNODE = 3
    EDGEID = 4

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.FieldSign"


@unique
class PyramidResampleType(JEnum):
    __doc__ = "\n    建立影像金字塔时所采用的重采样方式。\n\n    :var PyramidResampleType.NONE: 不进行重采样\n    :var PyramidResampleType.NEAREST: 最临近法，一种简单的采样方式\n    :var PyramidResampleType.AVERAGE: 平均值法，计算所有有效值的均值进行重采样计算。\n    :var PyramidResampleType.GAUSS: 使用高斯内核计算的方式进行重采样，这种对于高对比度和图案边界比较明显的图像效果比较好。\n    :var PyramidResampleType.AVERAGE_MAGPHASE: 平均联合数据法，在一个 magphase 空间中平均联合数据，用于复数数据空间的图像的重采样方式。\n    "
    NONE = 0
    NEAREST = 1
    AVERAGE = 2
    GAUSS = 3
    AVERAGE_MAGPHASE = 4

    @classmethod
    def _get_java_class_type(cls):
        return "com.supermap.data.PyramidResampleType"

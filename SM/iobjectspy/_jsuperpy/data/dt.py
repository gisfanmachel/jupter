# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/_jsuperpy\data\dt.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 295873 bytes
import json, datetime
from collections import OrderedDict
from ._jvm import JVMBase
from .prj import PrjCoordSys
from .geo import *
from .style import Color
from .ex import ObjectDisposedError
from ._listener import ProgressListener
from .._logger import log_error, log_warning
from .._gateway import get_jvm, get_gateway, safe_start_callback_server, close_callback_server
from ..enums import DatasetType, PixelFormat, EncodeType, CursorType, JoinType, SpatialIndexType, StatisticMode, BlockSizeOption, SpatialQueryMode, Charset, ColorGradientType, ResamplingMethod, FieldType, FieldSign, PyramidResampleType
from .._utils import datetime_to_java_date, java_date_to_datetime, split_input_list_from_str, split_input_dict_from_str, to_java_string_array, color_to_tuple, tuple_to_color, to_java_color, to_java_color_array, to_java_int_array, tuple_to_java_color, java_color_to_tuple, oj
__all__ = [
 'Dataset', 'DatasetVector', 'DatasetVectorInfo', 'DatasetImageInfo', 'DatasetGridInfo', 
 'DatasetImage', 
 'DatasetGrid', 'DatasetTopology', 'DatasetMosaic', 'DatasetVolume', 'Colors', 
 'JoinItem', 
 'LinkItem', 'SpatialIndexInfo', 'QueryParameter', 'TimeCondition', 
 'combine_band', 'Recordset']

class Dataset(JVMBase):
    __doc__ = "\n    数据集（矢量数据集，栅格数据集，影像数据集等）的基类，提供各种数据集数据集公共的属性，方法。\n    数据集一般为存储在一起的相关数据的集合；根据数据类型的不同，分为矢量数据集和栅格数据集，以及为了处理特定问题而设计的如拓扑数据集，网络数据集\n    等。数据集是 GIS 数据组织的最小单位。其中矢量数据集是由同种类型空间要素组成的集合，所以也可以称为要素集。根据要素的空间特征的不同，矢量数据集\n    又分为点数据集，线数据集，面数据集等，各矢量数据集是空间特征和性质相同而组织在一起的数据的集合。而栅格数据集由像元阵列组成，在表现要素上比矢量\n    数据集欠缺，但是可以很好的表现空间现象的位置关系。\n\n    "

    def __init__(self):
        JVMBase.__init__(self)
        self._datasource = None
        self._table_name = None

    def __str__(self):
        return self.__module__ + "." + type(self).__name__ + ": name=%s, type=%s" % (self.name, self.type.name)

    def __repr__(self):
        return type(self).__name__ + "(%s, %s)" % (self.name, self.type.name)

    def _make_java_object(self):
        return self._java_object

    @property
    def type(self):
        """DatasetType: 返回数据集类型"""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            return DatasetType._make(self._jobject.getType().name())
        except Exception as e:
            try:
                log_error(e)
                return
            finally:
                e = None
                del e

    @property
    def datasource(self):
        """ Datasource : 返回当前数据集所属的数据源对象"""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._datasource

    @property
    def name(self):
        """str: 返回数据集名称"""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            return self._jobject.getName()
        except Exception as e:
            try:
                log_error(e)
                return
            finally:
                e = None
                del e

    @property
    def table_name(self):
        """str: 返回数据集的表名。对数据库型数据源，返回此数据集在数据库中所对应的数据表名称；对文件型数据源，返回此数据集的存储属性的表名称."""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            if self._table_name is None:
                self._table_name = self._jobject.getTableName()
            return self._table_name
        except Exception as e:
            try:
                log_error(e)
                self._table_name = None
                return
            finally:
                e = None
                del e

    @property
    def prj_coordsys(self):
        """PrjCoordSys: 返回数据集的投影信息."""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            return PrjCoordSys._from_java_object(self._jobject.getPrjCoordSys())
        except Exception as e:
            try:
                log_error(e)
                return
            finally:
                e = None
                del e

    def set_prj_coordsys(self, value):
        """
        设置数据集的投影信息

        :param PrjCoordSys value: 投影信息
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        elif value is None:
            raise ValueError("value is None")
        try:
            self.open()
            value = PrjCoordSys.make(value)
            if isinstance(value, PrjCoordSys):
                self._jobject.setPrjCoordSys(value._jobject)
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def is_open(self):
        """
        判断数据集是否已经打开，数据集打开返回 True，否则返回 False

        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            return self._jobject.isOpen()
        except Exception as e:
            try:
                log_error(e)
                return False
            finally:
                e = None
                del e

    def is_readonly(self):
        """
        判断数据集是否是只读。如果数据集是只读，无法进行任何改写数据集的操作。 数据集是只读返回 True，否则返回 False。

        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            return self._jobject.isReadOnly()
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

        return False

    def open(self):
        """
        打开数据集， 打开数据集成功返返回 True，否则返回 False

        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            if not self._jobject.isOpen():
                return self._jobject.open()
            return True
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

        return False

    def close(self):
        """
        用于关闭当前数据集
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self._jobject.close()
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    @property
    def encode_type(self):
        """
        EncodeType: 返回此数据集数据存储时的编码方式。对数据集采用压缩编码方式，可以减少数据存储所占用的空间，降低数据传输时的网络负载和服务器的负载。矢量数
        据集支持的编码方式有Byte，Int16，Int24，Int32，SGL，LZW，DCT，也可以指定为不使用编码方式。光栅数据支持的编码方式有DCT，SGL，LZW
        或不使用编码方式。具体请参见 :py:class:`EncodeType` 类型
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            return EncodeType[self._jobject.getEncodeType().name()]
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    @property
    def bounds(self):
        """
        Rectangle: 返回数据集中包含所有对象的最小外接矩形。对于矢量数据集来说，为数据集中所有对象的最小外接矩形；对于栅格数据集来说，为当前栅格或影像的
        地理范围。
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            return Rectangle._from_java_object(self._jobject.getBounds())
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def set_bounds(self, rc):
        """
        设置数据集中包含所有对象的最小外接矩形。对于矢量数据集来说，为数据集中所有对象的最小外接矩形；对于栅格数据集来说，为
        当前栅格或影像的地理范围。

        :param Rectangle rc: 数据集中包含所有对象的最小外接矩形。
        :return: self
        :rtype: Dataset
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        rc = Rectangle.make(rc)
        try:
            self._jobject.setBounds(rc._jobject)
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

        return self

    @staticmethod
    def _from_java_object(java_dataset, datasource):
        if java_dataset is not None:
            data_type = DatasetType[java_dataset.getType().name()]
            if data_type is DatasetType.IMAGE:
                dt = DatasetImage()
            else:
                if data_type is DatasetType.GRID:
                    dt = DatasetGrid()
                else:
                    if data_type is DatasetType.VOLUME:
                        dt = DatasetVolume()
                    else:
                        if data_type is DatasetType.MOSAIC:
                            dt = DatasetMosaic()
                        else:
                            if data_type in [DatasetType.CAD, DatasetType.LINE, DatasetType.POINT, DatasetType.REGION,
                             DatasetType.TABULAR, DatasetType.LINEM, DatasetType.NETWORK, DatasetType.LINKTABLE,
                             DatasetType.TEXT, DatasetType.POINT3D, DatasetType.LINE3D, DatasetType.REGION3D,
                             DatasetType.PARAMETRICLINE, DatasetType.PARAMETRICREGION, DatasetType.MODEL,
                             DatasetType.NETWORK3D, DatasetType.POINTEPS, DatasetType.LINEEPS, DatasetType.REGIONEPS,
                             DatasetType.TEXTEPS, DatasetType.VECTORCOLLECTION]:
                                dt = DatasetVector()
                            else:
                                if data_type is DatasetType.TOPOLOGY:
                                    dt = DatasetTopology()
                                else:
                                    dt = DatasetUnsupported()
                                    log_warning("Unsupported dataset type " + str(data_type))
            dt._datasource = datasource
            dt._table_name = java_dataset.getTableName()
            dt._java_object = java_dataset
            return dt
        return

    @property
    def description(self):
        """str: 返回用户加入的对数据集的描述信息。"""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            return self._jobject.getDescription()
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def set_description(self, value):
        """
        设置用户加入的对数据集的描述信息。

        :param str value: 用户加入的对数据集的描述信息。
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self._jobject.setDescription(value)
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def to_json(self):
        """
        输出数据集的信息到 json 字符串中。数据集的 json 串内容包括数据源的连接信息和数据集名称两项。

        :rtype: str

        示例::
         >>> ds = Workspace().get_datasource('data')
         >>> print(ds[0].to_json())
         {"name": "location", "datasource": {"type": "UDB", "alias": "data", "server": "E:/data.udb", "is_readonly": false}}

        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return json.dumps({'datasource':(self.datasource.connection_info.to_dict)(),  'name':self.name})

    @staticmethod
    def from_json(value):
        """
        从数据集的 json 字符串中获取数据集，如果数据源没有打开，将自动打开数据源。

        :param str value:  json 字符串
        :return: 数据集对象
        :rtype: Dataet
        """
        d = json.loads(value)
        from .ds import DatasourceConnectionInfo
        from .ws import open_datasource
        conn = DatasourceConnectionInfo.make_from_dict(d["datasource"])
        ds = open_datasource(conn, True)
        return ds[d["name"]]

    def rename(self, new_name):
        """
        修改数据集名称

        :param str new_name: 新的数据集名称
        :return: 修改成功返回True，否则返回False
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            return self.datasource._jobject.getDatasets().rename(self.name, new_name)
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

        return False

    def _clear_handle(self):
        self._java_object = None


class TimeCondition(object):
    __doc__ = "\n    定义了单时间字段时空模型管理查询功能接口\n    "

    def __init__(self, field_name=None, time=None, condition=None, back_condition=None):
        """
        构造时空模型查询条件对象

        :param field_name: 字段名称
        :type field_name: str
        :param time: 查询条件的时间
        :type time: datetime.datetime
        :param condition: 查询时间的条件操作符。例如：>、<、>=、<=、=
        :type condition: str
        :param back_condition: 指定的后一个条件操作符，例如：and、or
        :type back_condition: str
        """
        self._time = None
        self._condition = None
        self._back_condition = None
        self._field_name = None
        self.set_time(time).set_condition(condition).set_field_name(field_name).set_back_condition(back_condition)

    def __str__(self):
        return "TimeCondition(%s, %s, %s, %s)" % (self.time, self.condition, self.back_condition, self.field_name)

    @property
    def time(self):
        """datetime.datetime: 作为查询条件的时间"""
        return self._time

    @property
    def field_name(self):
        """str: 字段名称"""
        return self._field_name

    @property
    def condition(self):
        """str: 查询时间的条件操作符。例如：>、<、>=、<=、= """
        return self._condition

    @property
    def back_condition(self):
        """指定的后一个条件操作符，例如：and、or"""
        return self._back_condition

    def set_time(self, value):
        """
        设置查询条件的时间值

        :param datetime.datetime value: 时间值
        :return: self
        :rtype: TimeCondition
        """
        if value is not None:
            if isinstance(value, datetime.datetime):
                self._time = value
        return self

    def set_field_name(self, value):
        """
        设置查询条件的字段名

        :param str value: 查询条件的字段名
        :return: self
        :rtype: TimeCondition
        """
        self._field_name = value
        return self

    def set_back_condition(self, value):
        """
        查询条件的后一个条件操作符。例如：and、or

        :param str value: 查询条件的后一个条件操作符
        :return: self
        :rtype: TimeCondition
        """
        self._back_condition = value
        return self

    def set_condition(self, value):
        """
        设置查询条件的条件操作符。

        :param str value: 查询条件的条件操作符，>、<、>=、<=、=
        :return: self
        :rtype: TimeCondition
        """
        self._condition = value
        return self

    @property
    def _jobject(self):
        """Py4J 映射的 Java 对象"""
        java_obj = get_jvm().com.supermap.data.TimeCondition()
        if self.time is not None:
            java_obj.setTime(datetime_to_java_date(self.time))
        if self.field_name is not None:
            java_obj.setFieldName(self.field_name)
        if self.back_condition is not None:
            java_obj.setBackCondition(self.back_condition)
        if self.condition is not None:
            java_obj.setCondition(self.condition)
        return java_obj

    @staticmethod
    def _from_java_object(java_obj):
        obj = TimeCondition()
        obj.set_time(java_date_to_datetime(java_obj.getTime()))
        obj.set_condition(java_obj.getCondition())
        obj.set_back_condition(java_obj.getBackCondition())
        obj.set_field_name(java_obj.getFieldName())
        return obj

    def to_dict(self):
        """
        将当前对象输出为 dict 对象

        :rtype: dict
        """
        d = dict()
        if self.time is not None:
            d["time"] = self.time
        if self.condition is not None:
            d["condition"] = self.condition
        if self.back_condition is not None:
            d["back_condition"] = self.back_condition
        if self.field_name is not None:
            d["field_name"] = self.field_name
        return d

    @staticmethod
    def make_from_dict(values):
        """
        从 dict 对象中构造 TimeCondition 对象

        :param dict values:  包含 TimeCondition 信息的 dict，具体参考 to_dict
        :rtype: TimeCondition
        """
        return TimeCondition().from_dict(values)

    def from_dict(self, values):
        """
        从 dict 对象中读取 TimeCondition 信息。

        :param dict values:  包含 TimeCondition 信息的 dict，具体参考 to_dict
        :rtype: TimeCondition
        :rtype: TimeCondition
        """
        if "time" in values.keys():
            self.set_time(values["time"])
        if "condition" in values.keys():
            self.set_condition(values["condition"])
        if "back_condition" in values.keys():
            self.set_back_condition(values["back_condition"])
        if "field_name" in values.keys():
            self.set_field_name(values["field_name"])
        return self

    def to_json(self):
        """
        将当前对象输出为 json 字符串

        :rtype: str
        """
        return json.dumps(self.to_dict())

    @staticmethod
    def from_json(value):
        """
        从 json 字符串中构造 TimeCondition。

        :param str value: json 字符串
        :rtype: TimeCondition
        """
        tc = TimeCondition()
        tc.from_dict(json.loads(value))
        return tc


class JoinItem(object):
    __doc__ = "\n    连接信息类。用于矢量数据集与外部表的连接。外部表可以为另一个矢量数据集（其中纯属性数据集中没有空间几何信息）所对应的DBMS表，也可以是用户自建\n    的业务表。需要注意的是，矢量数据集与外部表必须属于同一数据源。当两个表格之间建立了连接，通过对主表进行操作，可以对外部表进行查询，制作专题图以\n    及分析等。当两个表格之间是一对一或多对一的关系时，可以使用join连接。当为多对一的关系时，允许指定多个字段之间的关联。该类型的实例可被创建。\n\n    数据集表之间的联系的建立有两种方式，一种是连接（join），一种是关联（link）。连接的相关设置是通过 JoinItem 类实现的，关联的相关设置是通过\n    LinkItem 类实现的，另外，用于建立连接的两个数据集表必须在同一个数据源下，而用于建立关联关系的两个数据集表可以不在同一个数据源下。\n\n    下面通过查询的例子来说明连接和关联的区别，假设用来进行查询的数据集表为 DatasetTableA，被关联或者连接的表为 DatasetTableB，现通过建立\n    DatasetTableA 与 DatasetTableB 的连接或关联关系来查询 DatasetTableA 中满足查询条件的记录:\n\n        - 连接（join）\n            设置将 DatasetTableB 连接 DatasetTableA 的连接信息，即建立 JoinItem 类并设置其属性，当执行 DatasetTableA 的查询操作时，\n            系统将根据连接条件及查询条件，将满足条件的 DatasetTableA 中的内容与满足条件的 DatasetTableB 中的内容构成一个查询结果表，并且这个\n            查询表保存在内存中，需要返回结果时，再从内存中取出相应的内容。\n\n        - 关联（link）\n            设置将 DatasetTableB （副表）关联到 DatasetTableA （主表）的关联信息，即建立 LinkItem 类并设置其属性，DatasetTableA 与\n            DatasetTableB 是通过主表 DatasetTableA 的外键（LinkItem.foreign_keys）和副表 DatasetTableB 的主键\n            （LinkItem.primary_keys 方法）实现关联的，当执行 DatasetTableA 的查询操作时，系统将根据关联信息中的过滤条件及查询条件，\n            分别查询 DatasetTableA 与 DatasetTableB 中满足条件的内容，DatasetTableA 的查询结果与 DatasetTableB 的查询结果分别作为独立\n            的两个结果表保存在内存中，当需要返回结果时，SuperMap 将对两个结果进行拼接并返回，因此，在应用层看来，连接和关联操作很相似。\n\n        - LinkItem 只支持左连接，UDB、PostgreSQL 和 DB2 数据源不支持 LinkItem，即对 UDB、PostgreSQL 和 DB2 类型的数据引擎设置 LinkItem 不起作用；\n\n        - JoinItem 目前支持左连接和内连接，不支持全连接和右连接，UDB 引擎不支持内连接；\n\n        - 使用 LinkItem 的约束条件：空间数据和属性数据必须有关联条件，即主空间数据集与外部属性表之间存在关联字段。主空间数据集：用来与外部表进行关联的数据集。外部属性表：用户通过 Oracle 或者 SQL Server 创建的数据表，或者是另一个矢量数据集所对应的 DBMS 表。\n\n\n    示例::\n\n        >>> ds = Workspace().get_datasource('data')\n        >>> dataset_world = ds['World']\n        >>> dataset_capital = ds['Capital']\n        >>> foreign_table_name = dataset_capital.table_name\n        >>>\n        >>> join_item = JoinItem()\n        >>> join_item.set_foreign_table(foreign_table_name)\n        >>> join_item.set_join_filter('World.capital=%s.capital' % foreign_table_name)\n        >>> join_item.set_join_type(JoinType.LEFTJOIN)\n        >>> join_item.set_name('Connect')\n\n        >>> query_parameter  = QueryParameter()\n        >>> query_parameter.set_join_items([join_item])\n        >>> recordset = dataset_world.query(query_parameter)\n        >>> print(recordset.get_record_count())\n        >>> recordset.close()\n\n    "

    def __init__(self, name=None, foreign_table=None, join_filter=None, join_type=None):
        """
        构造 JoinItem 对象

        :param str name: 连接信息对象的名称
        :param str foreign_table: 外部表的名称
        :param str join_filter:  与外部表之间的连接表达式，即设定两个表之间关联的字段
        :param str join_type: 两个表之间连接的类型
        """
        self._name = None
        self._foreign_table = None
        self._join_filter = None
        self._join_type = None
        self.set_name(name).set_foreign_table(foreign_table).set_join_filter(join_filter).set_join_type(join_type)

    def __str__(self):
        return "JoinItem: " + str((self.name, self.foreign_table, self.join_filter, self.join_type))

    @property
    def name(self):
        """str:  连接信息对象的名称"""
        return self._name

    @property
    def foreign_table(self):
        """str: 外部表的名称"""
        return self._foreign_table

    @property
    def join_filter(self):
        """str: 与外部表之间的连接表达式，即设定两个表之间关联的字段"""
        return self._join_filter

    @property
    def join_type(self):
        """JoinType: 两个表之间连接的类型"""
        return self._join_type

    def set_name(self, value):
        """
        设置连接信息对象的名称

        :param str value:  连接信息名称
        :return: self
        :rtype: JoinItem
        """
        self._name = value
        return self

    def set_foreign_table(self, value):
        """
        设置连接信息外部表名称

        :param str value: 外部表名称
        :return: self
        :rtype: JoinItem
        """
        self._foreign_table = value
        return self

    def set_join_filter(self, value):
        """
        设置与外部表之间的连接表达式，即设定两个表之间关联的字段。例如，将一个房屋的面数据集（Building）的 district 字段与一个房屋拥有者的纯属
        性数据集（Owner）的 region 字段相连接，两个数据集对应的表名称分别为 Table_Building 和 Table_Owner，则连接表达式为
        Table_Building.district = Table_Owner.region，当有多个字段相连接时，用 AND 将多个表达式相连。

        :param str value: 与外部表之间的连接表达式，即设定两个表之间关联的字段
        :return: self
        :rtype: JoinItem
        """
        self._join_filter = value
        return self

    def set_join_type(self, value):
        """
        设置两个表之间连接的类型。连接类型用于对两个连接的表进行查询时，决定了返回的记录的情况。

        :param value: 两个表之间连接的类型
        :type value: JoinType or str
        :return: self
        :rtype: JoinItem
        """
        self._join_type = JoinType._make(value)
        return self

    @property
    def _jobject(self):
        """Py4J 映射的 Java 对象"""
        java_obj = get_jvm().com.supermap.data.JoinItem()
        if self.name is not None:
            java_obj.setName(self.name)
        if self.foreign_table is not None:
            java_obj.setForeignTable(self.foreign_table)
        if self.join_filter is not None:
            java_obj.setJoinFilter(self.join_filter)
        if self.join_type is not None:
            java_obj.setJoinType(self.join_type._jobject)
        return java_obj

    @staticmethod
    def _from_java_object(java_obj):
        obj = JoinItem()
        obj.set_name(java_obj.getName())
        obj.set_foreign_table(java_obj.getForeignTable())
        obj.set_join_filter(java_obj.getJoinFilter())
        obj.set_join_type(java_obj.getJoinType().name())
        return obj

    def to_dict(self):
        """
        将当前对象信息输出为 dict

        :rtype: dict
        """
        d = dict()
        if self.name is not None:
            d["name"] = self.name
        if self.foreign_table is not None:
            d["foreign_table"] = self.foreign_table
        if self.join_filter is not None:
            d["join_filter"] = self.join_filter
        if self.join_type is not None:
            d["join_type"] = self.join_type
        return d

    @staticmethod
    def make_from_dict(values):
        """
        从 dict 读取信息构造 JoinItem 对象。

        :param dict values: 含有 JoinItem 信息的 dict，具体查看 to_dict
        :rtype: JoinItem
        """
        return JoinItem().from_dict(values)

    def from_dict(self, values):
        """
        从 dict 读取JoinItem 信息

        :param dict values: 含有 JoinItem 信息的 dict，具体查看 to_dict
        :return: self
        :rtype: JoinItem
        """
        if "name" in values.keys():
            self.set_name(values["name"])
        if "foreign_table" in values.keys():
            self.set_foreign_table(values["foreign_table"])
        if "join_filter" in values.keys():
            self.set_join_filter(values["join_filter"])
        if "join_type" in values.keys():
            self.set_join_type(values["join_type"])
        return self

    def to_json(self):
        """
        将当前对象输出为 json 字符串

        :rtype: str
        """
        return json.dumps(self.to_dict())

    @staticmethod
    def from_json(value):
        """
        从 json 字符串中解析 JoinItem 信息，构造一个新的 JoinItem 对象

        :param str value:  json 字符串
        :rtype: JoinItem
        """
        return JoinItem.make_from_dict(json.loads(value))


class LinkItem(object):
    __doc__ = "\n    关联信息类，用于矢量数据集与其它数据集的关联。关联数据集可以为另一个矢量数据集（其中纯属性数据集中没有空间几何信息）所对应的 DBMS 表，用户自\n    建业务表需要外挂到 SuperMap 数据源中。需要注意的是，矢量数据集与关联数据集可以属于不同的数据源。数据集表之间的联系的建立有两种方式，一种是\n    连接（join），一种是关联（link）。连接的相关设置是通过 JoinItem 类实现的，关联的相关设置是通过 LinkItem 类实现的，另外，用于建立连接的两\n    个数据集表必须在同一个数据源下，而用于建立关联关系的两个数据集表可以不在同一个数据源下。\n    下面通过查询的例子来说明连接和关联的区别，假设用来进行查询的数据集表为 DatasetTableA，被关联或者连接的表为 DatasetTableB，现通过建立\n    DatasetTableA 与 DatasetTableB 的连接或关联关系来查询 DatasetTableA 中满足查询条件的记录:\n\n        - 连接（join）\n            设置将 DatasetTableB 连接 DatasetTableA 的连接信息，即建立 JoinItem 类并设置其属性，当执行 DatasetTableA 的查询操作时，\n            系统将根据连接条件及查询条件，将满足条件的 DatasetTableA 中的内容与满足条件的 DatasetTableB 中的内容构成一个查询结果表，并且这个\n            查询表保存在内存中，需要返回结果时，再从内存中取出相应的内容。\n\n        - 关联（link）\n            设置将 DatasetTableB （副表）关联到 DatasetTableA （主表）的关联信息，即建立 LinkItem 类并设置其属性，DatasetTableA 与\n            DatasetTableB 是通过主表 DatasetTableA 的外键（LinkItem.foreign_keys）和副表 DatasetTableB 的主键\n            （LinkItem.primary_keys 方法）实现关联的，当执行 DatasetTableA 的查询操作时，系统将根据关联信息中的过滤条件及查询条件，\n            分别查询 DatasetTableA 与 DatasetTableB 中满足条件的内容，DatasetTableA 的查询结果与 DatasetTableB 的查询结果分别作为独立\n            的两个结果表保存在内存中，当需要返回结果时，SuperMap 将对两个结果进行拼接并返回，因此，在应用层看来，连接和关联操作很相似。\n\n        - LinkItem 只支持左连接，UDB、PostgreSQL 和 DB2 数据源不支持 LinkItem，即对 UDB、PostgreSQL 和 DB2 类型的数据引擎设置 LinkItem 不起作用；\n\n        - JoinItem 目前支持左连接和内连接，不支持全连接和右连接，UDB 引擎不支持内连接；\n\n        - 使用 LinkItem 的约束条件：空间数据和属性数据必须有关联条件，即主空间数据集与外部属性表之间存在关联字段。主空间数据集：用来与外部表进行关联的数据集。外部属性表：用户通过 Oracle 或者 SQL Server 创建的数据表，或者是另一个矢量数据集所对应的 DBMS 表。\n\n    示例:\n        # 'source' 数据集为主数据集，source 数据集用于关联的字段为 'LinkID'，'lind_dt' 数据集为外表数据集，即被关联的数据集，link_dt 中用于关联的字段为 'ID'\n\n        >>> ds_db1 = Workspace().get_datasource('data_db_1')\n        >>> ds_db2 = Workspace().get_datasource('data_db_2')\n        >>> source_dataset = ds_db1['source']\n        >>> linked_dataset = ds_db2['link_dt']\n        >>> linked_dataset_name = linked_dataset.name\n        >>> linked_dataset_table_name = linked_dataset.table_name\n        >>>\n        >>> link_item = LinkItem()\n        >>>\n        >>> link_item.set_connection_info(ds_db2.connection_info)\n        >>> link_item.set_foreign_table(linked_dataset_name)\n        >>> link_item.set_foreign_keys(['LinkID'])\n        >>> link_item.set_primary_keys(['ID'])\n        >>> link_item.set_link_fields([linked_dataset_table_name+'.polulation'])\n        >>> link_item.set_link_filter('ID < 100')\n        >>> link_item.set_name('link_name')\n\n    "

    def __init__(self, foreign_keys=None, name=None, foreign_table=None, primary_keys=None, link_fields=None, link_filter=None, connection_info=None):
        """
        构造 LinkItem 对象

        :param list[str] foreign_keys: 主数据集用于关联外表的字段
        :param str name: 关联信息对象的名称
        :param str foreign_table: 外表的数据集名称，即被关联的数据集名称
        :param list[str] primary_keys: 外表数据集中用于关联的字段
        :param list[str] link_fields: 外表数据集中被查询的字段名称
        :param str link_filter: 外表数据集的查询条件
        :param DatasourceConnectionInfo connection_info: 外表数据集所在数据源的连接信息
        """
        self._foreign_keys = None
        self._name = None
        self._foreign_table = None
        self._primary_keys = None
        self._link_fields = None
        self._link_filter = None
        self._connection_info = None
        self.set_foreign_table(foreign_table)
        self.set_link_filter(link_filter)
        self.set_name(name)
        self.set_link_fields(link_fields)
        self.set_foreign_keys(foreign_keys)
        self.set_primary_keys(primary_keys)
        self.set_connection_info(connection_info)

    @property
    def foreign_table(self):
        """str: 外表的数据集名称，即被关联的数据集名称"""
        return self._foreign_table

    def link_filter(self):
        """str:  外表数据集的查询条件"""
        return self._link_filter

    @property
    def name(self):
        """str: 关联信息对象的名称"""
        return self._name

    @property
    def link_fields(self):
        """list[str]: 外表数据集中被查询的字段名称"""
        return self._link_fields

    @property
    def foreign_keys(self):
        """list[str]: 主数据集用于关联外表的字段"""
        return self._foreign_keys

    @property
    def primary_keys(self):
        """list[str]:  外表数据集中用于关联的字段"""
        return self._primary_keys

    @property
    def connection_info(self):
        """DatasourceConnectionInfo: 外表数据集所在数据源的连接信息"""
        return self._connection_info

    def set_name(self, value):
        """
        设置关联信息对象的名称

        :param str value: 关联信息对象的名称
        :return: self
        :rtype: LinkItem
        """
        self._name = value
        return self

    def set_connection_info(self, value):
        """
        设置外表数据集所在数据源的连接信息

        :param DatasourceConnectionInfo value: 外表数据集所在数据源的连接信息
        :return: self
        :rtype: LinkItem
        """
        if value is not None:
            from .ds import DatasourceConnectionInfo
            self._connection_info = DatasourceConnectionInfo.make(value)
        return self

    def set_primary_keys(self, value):
        """
        设置外表数据集中用于关联的字段

        :param list[str] value: 外表数据集中用于关联的字段
        :return: self
        :rtype: LinkItem
        """
        if value is not None:
            self._primary_keys = split_input_list_from_str(value)
        return self

    def set_foreign_keys(self, value):
        """
        设置主数据集用于关联外表的字段

        :param list[str] value: 主数据集用于关联外表的字段
        :return: self
        :rtype: LinkItem
        """
        if value is not None:
            self._foreign_keys = split_input_list_from_str(value)
        return self

    def set_foreign_table(self, value):
        """
        设置外表的数据集名称，即被关联的数据集名称

        :param str value: 外表的数据集名称，即被关联的数据集名称
        :return: self
        :rtype: LinkItem
        """
        self._foreign_table = value
        return self

    def set_link_filter(self, value):
        """
        设置外表数据集的查询条件

        :param str value: 外表数据集的查询条件
        :return: self
        :rtype: LinkItem
        """
        self._link_filter = value
        return self

    def set_link_fields(self, value):
        """
        设置外表数据集中被查询的字段名称

        :param list[str] value: 外表数据集中被查询的字段名称
        :return: self
        :rtype: LinkItem
        """
        if value is not None:
            self._link_fields = split_input_list_from_str(value)
        return self

    @property
    def _jobject(self):
        """Py4J 映射的 Java 对象"""
        java_obj = get_jvm().com.supermap.data.LinkItem()
        if self.name is not None:
            java_obj.setName(self.name)
        if self.connection_info is not None:
            java_obj.setConnectionInfo(self.connection_info._jobject)
        if self.primary_keys is not None:
            java_obj.setPrimaryKeys(to_java_string_array(self.primary_keys))
        if self.foreign_keys is not None:
            java_obj.setForeignKeys(to_java_string_array(self.foreign_keys))
        if self.foreign_table is not None:
            java_obj.setForeignTable(self.foreign_table)
        if self.link_filter is not None:
            java_obj.setLinkFilter(self.link_filter)
        if self.link_fields is not None:
            java_obj.setLinkFields(to_java_string_array(self.link_fields))
        return java_obj

    @staticmethod
    def _from_java_object(java_obj):
        obj = LinkItem()
        obj.set_name(java_obj.getName())
        from .ds import DatasourceConnectionInfo
        obj.set_connection_info(DatasourceConnectionInfo._from_java_object(java_obj.getConnectionInfo()))
        obj.set_link_fields(java_obj.getLinkFields())
        obj.set_foreign_keys(java_obj.getForeignKeys())
        obj.set_link_filter(java_obj.getLinkFilter())
        obj.set_foreign_table(java_obj.getForeignTable())
        obj.set_primary_keys(java_obj.getPrimaryKeys())
        return obj

    def to_dict(self):
        """
        将当前对象的信息输出到dict中

        :rtype: dict
        """
        d = dict()
        if self.name is not None:
            d["name"] = self.name
        if self.connection_info is not None:
            d["connection_info"] = self.connection_info.to_dict()
        if self.link_fields is not None:
            d["link_fields"] = self.link_fields
        if self.foreign_keys is not None:
            d["foreign_keys"] = self.foreign_keys
        if self.link_filter is not None:
            d["link_filter"] = self.link_filter
        if self.foreign_table is not None:
            d["foreign_table"] = self.foreign_table
        if self.primary_keys is not None:
            d["primary_keys"] = self.primary_keys
        return d

    @staticmethod
    def make_from_dict(values):
        """
        从 dict 读取信息构造 LinkItem 对象，构造一个新的 LinkItem 对象

        :param dict values: 含有 LinkItem 信息的 dict，具体查看 to_dict
        :rtype: LinkItem
        """
        return LinkItem().from_dict(values)

    def from_dict(self, values):
        """
        从 dict 读取信息构造 LinkItem 对象。

        :param dict values:  含有 LinkItem 信息的 dict，具体查看 to_dict
        :return: self
        :rtype: LinkItem
        """
        if "name" in values.keys():
            self.set_name(values["name"])
        if "connection_info" in values.keys():
            self.set_connection_info(values["connection_info"])
        if "link_fields" in values.keys():
            self.set_link_fields(values["link_fields"])
        if "foreign_keys" in values.keys():
            self.set_foreign_keys(values["foreign_keys"])
        if "link_filter" in values.keys():
            self.set_link_filter(values["link_filter"])
        if "foreign_table" in values.keys():
            self.set_foreign_table(values["foreign_table"])
        if "primary_keys" in values.keys():
            self.set_primary_keys(values["primary_keys"])
        return self

    def to_json(self):
        """
        将当前对象信息输出到 json 字符串中，具体查看 to_dict.

        :rtype: str
        """
        return json.dumps(self.to_dict())

    @staticmethod
    def from_json(value):
        """
        从 json 字符串中构造 LinkItem 对象

        :param str value:  json 字符串信息
        :rtype: LinkItem
        """
        return JoinItem.make_from_dict(json.loads(value))


def _to_java_time_condition_array(values):
    if values is None:
        return
    if isinstance(values, TimeCondition):
        java_array = get_gateway().new_array(get_jvm().com.supermap.data.TimeCondition, 1)
        java_array[0] = values._jobject
        return java_array
    if isinstance(values, (list, tuple, set)):
        _size = len(values)
        java_array = get_gateway().new_array(get_jvm().com.supermap.data.TimeCondition, _size)
        i = 0
        for value in values:
            if value is not None:
                java_array[i] = value._jobject
            i += 1

        return java_array
    return


class QueryParameter(object):
    __doc__ = "\n    查询参数类。 用于描述一个条件查询的限制条件，如所包含的 SQL 语句，游标方式，空间数据的位置关系条件设定等。条件查询，是查询满足一定条件的所\n    有要素的记录，其查询得到的结果是记录集。查询参数类是用来设置条件查询的查询条件从而得到记录集。条件查询包括两种最主要的查询方式，一种为 SQL\n    查询，又称属性查询，即通过构建包含属性字段、运算符号和数值的 SQL 条件语句来选择记录，从而得到记录集；另一种为空间查询，即根据要素间地理或空间\n    的关系来查询记录来得到记录集。\n\n    QueryParameter 包含以下参数:\n\n    - attribute_filter : str\n        查询所构建的 SQL 条件语句，即 SQL WHERE clause 语句。SQL 查询又称为属性查询，是通过一个或多个 SQL 条件语句来查询记录。\n        SQL 语句是包含属性字段、运算符号和数值的条件语句。例如，你希望查询一个商业区内去年的年销售额超过30万的服装店，则构建的 SQL 查询语句为::\n\n        >>> attribute_filter = 'Sales > 30,0000 AND SellingType = ‘Garment’'\n\n        对于不同引擎的数据源，不同函数的适用情况及函数用法有所不同，对于数据库型数据源（Oracle Plus、SQL Server Plus、PostgreSQL 和 DB2 数据源），函数的用法请参见数据库相关文档。\n\n    - cursor_type : CursorType\n        查询所采用的游标类型。SuperMap 支持两种类型的游标，分别为动态游标和静态游标。使用动态游标查询时，记录集会动态的刷新，耗费很多的资源，\n        而当使用静态游标时，查询的为记录集的静态副本，效率较高。推荐在查询时使用静态游标，使用静态游标获得的记录集是不可编辑的。\n        详细信息请参见 CursorType 类型。\n        默认使用 DYNAMIC 类型。\n\n    - has_geometry : bool\n        查询结果是否包含几何对象字段。 若查询时不取空间数据，即只查询属性信息，则在返回的 Recordset 中，凡是对记录集的空间对象进行操作的方法，\n        都将无效，例如，调用 :py:meth:`Recordset.get_geometry` 将返回空。\n\n    - result_fields : list of str\n        设置查询结果字段集合。对于查询结果的记录集中，可以设置其中所包含的字段，如果为空，则查询所有字段。\n\n    - order_by : list of str\n        SQL 查询排序的字段。 对于 SQL 查询得到的记录集中的各记录，可以根据指定的字段进行排序，并可以指定为升序排列或是降序排列，其中 asc 表示升序，desc 表示降序。用于排序的字段必须为数值型。例如按 SmID 降序排序，可以设置为::\n\n        >>> query_paramater.set_order_by(['SmID desc'])\n\n    - group_by : list of str\n        SQL 查询分组条件的字段。对于 SQL 查询得到的记录集中的各字段，可以根据指定的字段进行分组，指定的字段值相同的记录将被放置在一起。\n        注意：\n\n            - 空间查询不支持 group_by ，否则可能导致空间查询的结果不正确\n            - 只有 cursor_type 为 STATIC 时， group_by 才有效\n\n    - spatial_query_mode : SpatialQueryMode\n        空间查询模式\n\n    - spatial_query_object : DatasetVector or Recordset or Geometry or Rectangle or Point2D\n        空间查询的搜索对象。\n        若搜索对象是数据集或是记录集类型，则必须同被搜索图层对应的数据集的地理坐标系一致。\n        当搜索数据集/记录集中存在对象重叠的情况时，空间查询的结果可能不正确，建议采用遍历搜索数据集/记录集，逐个使用单对象查询的方式进行空间查询。\n\n    - time_conditions : list of TimeCondition\n        时空模型查询条件。具体查看 :py:class:`TimeCondition` 说明。\n\n    - link_items : list of LinkItem\n        关联查询的信息。当被查询的矢量数据集有相关联的外部表时，查询得到的结果中会包含相关联的外部表中满足条件的记录。具体查看 :py:class:`LinkItem` 说明\n\n    -  join_items: list of JoinItem\n        连接查询的信息。当被查询的矢量数据集有相连接的外部表时，查询得到的结果中会包含相连接的外部表中满足条件的记录。具体查看 :py:class:`JoinItem` 说明\n\n\n    示例::\n        # 进行 SQL 查询\n\n        >>> parameter = QueryParameter('SmID < 100', 'STATIC', False)\n        >>> ds = Datasource.open('E:/data.udb')\n        >>> dt = ds['point']\n        >>> rd = dt.query(parameter)\n        >>> print(rd.get_record_count())\n        99\n        >>> rd.close()\n\n\n        # 进行空间查询\n\n        >>> geo = dt.get_geometries('SmID = 1')[0]\n        >>> query_geo = geo.create_buffer(10, dt.prj_coordsys, 'meter')\n        >>> parameter.set_spatial_query_mode('contain').set_spatial_query_object(query_geo)\n        >>> rd2 = dt.query(parameter)\n        >>> print(rd2.get_record_count())\n        10\n        >>> rd2.close()\n\n    "

    def __init__(self, attr_filter=None, cursor_type=CursorType.DYNAMIC, has_geometry=True, result_fields=None, order_by=None, group_by=None):
        self._attribute_filter = None
        self._cursor_type = None
        self._has_geometry = None
        self._result_fields = None
        self._order_by = None
        self._group_by = None
        self._spatial_query_object = None
        self._spatial_query_mode = SpatialQueryMode.NONE
        self._time_conditions = None
        self._link_items = None
        self._join_items = None
        self.set_group_by(group_by)
        self.set_order_by(order_by)
        self.set_result_fields(result_fields)
        self.set_has_geometry(has_geometry)
        self.set_cursor_type(cursor_type)
        self.set_attribute_filter(attr_filter)

    @property
    def attribute_filter(self):
        """str : 查询所构建的 SQL 条件语句，即 SQL WHERE clause 语句。"""
        return self._attribute_filter

    @property
    def cursor_type(self):
        """ CursorType: 查询所采用的游标类型"""
        return self._cursor_type

    @property
    def has_geometry(self):
        """bool: 查询结果是否包含几何对象字段"""
        return self._has_geometry

    @property
    def result_fields(self):
        """list[str]: 查询结果字段集合。对于查询结果的记录集中，可以设置其中所包含的字段，如果为空，则查询所有字段。"""
        return self._result_fields

    @property
    def order_by(self):
        """list[str]:  SQL 查询排序的字段。"""
        return self._order_by

    @property
    def group_by(self):
        """list[str]: SQL 查询分组条件的字段 """
        return self._group_by

    @property
    def spatial_query_object(self):
        """DatasetVector or Recordset or Geometry or Rectangle or Point2D: 空间查询的搜索对象。"""
        return self._spatial_query_object

    @property
    def spatial_query_mode(self):
        """SpatialQueryMode: 空间查询模式。"""
        return self._spatial_query_mode

    @property
    def time_conditions(self):
        """list[TimeCondition]:  时空模型查询条件。具体查看 :py:class:`TimeCondition` 说明。"""
        return self._time_conditions

    @property
    def link_items(self):
        """list[LinkItem]: 关联查询的信息。当被查询的矢量数据集有相关联的外部表时，查询得到的结果中会包含相关联的外部表中满足条件的记录。具体查看 :py:class:`LinkItem` 说明"""
        return self._link_items

    @property
    def join_items(self):
        """list[JoinItem]: 连接查询的信息。当被查询的矢量数据集有相连接的外部表时，查询得到的结果中会包含相连接的外部表中满足条件的记录。具体查看 :py:class:`JoinItem` 说明"""
        return self._join_items

    def set_attribute_filter(self, value):
        """
        设置属性查询条件

        :param str value: 属性查询条件
        :return: self
        :rtype: QueryParameter
        """
        self._attribute_filter = value
        return self

    def set_spatial_query_object(self, value):
        """
        设置空间查询的搜索对象

        :param value: 空间查询的搜索对象
        :type value: DatasetVector or Recordset or Geometry or Rectangle or Point2D
        :return: self
        :rtype: QueryParameter
        """
        self._spatial_query_object = value
        return self

    def set_time_conditions(self, value):
        """
        设置时间字段进行时空查询的查询条件

        :param list[TimeCondition] value: 时空查询的查询条件
        :return: self
        :rtype: QueryParameter
        """
        if value is not None:
            self._time_conditions = list(value)
        return self

    def set_spatial_query_mode(self, value):
        """
        设置空间查询模式，具体查看 :py:class:`.SpatialQueryMode` 说明

        :param  value: 空间查询的查询模式。
        :type value: SpatialQueryMode or str
        :return: self
        :rtype: QueryParameter
        """
        self._spatial_query_mode = SpatialQueryMode._make(value)
        return self

    def set_group_by(self, value):
        """
        设置 SQL 查询分组条件的字段。

        :param list[str] value:  SQL 查询分组条件的字段
        :return: self
        :rtype: QueryParameter
        """
        if value is not None:
            self._group_by = split_input_list_from_str(value)
        return self

    def set_join_items(self, value):
        """
        设置连接查询的查询条件

        :param list[JoinItem] value:  接查询的查询条件
        :return: self
        :rtype: QueryParameter
        """
        if value is not None:
            self._join_items = list(value)
        return self

    def set_result_fields(self, value):
        """
        设置查询结果字段

        :param list[str] value:  查询结果字段
        :return: self
        :rtype: QueryParameter
        """
        if value is not None:
            self._result_fields = split_input_list_from_str(value)
        return self

    def set_link_items(self, value):
        """
        设置关联查询的查询条件

        :param list[LinkItem] value:  关联查询的查询条件
        :return: self
        :rtype: QueryParameter
        """
        if value is not None:
            self._link_items = list(value)
        return self

    def set_has_geometry(self, value):
        """
        设置是否查询几何对象。如果设置为 False，将不会返回几何对象，默认为 True

        :param bool value: 查询是否包含几何对象。
        :return: self
        :rtype: QueryParameter
        """
        self._has_geometry = bool(value)
        return self

    def set_cursor_type(self, value):
        """
        设置查询所采用的游标类型。默认为 DYNAMIC

        :param value: 游标类型
        :type value: CursorType or str
        :return: self
        :rtype: QueryParameter
        """
        self._cursor_type = CursorType._make(value)
        return self

    def set_order_by(self, value):
        """
        设置 SQL 查询排序的字段

        :param list[str] value: SQL查询排序的字段
        :return: self
        :rtype: QueryParameter
        """
        if value is not None:
            self._order_by = split_input_list_from_str(value)
        return self

    @property
    def _jobject(self):
        java_obj = get_jvm().com.supermap.data.QueryParameter()
        if self.attribute_filter is not None:
            java_obj.setAttributeFilter(self.attribute_filter)
        if self.spatial_query_object is not None:
            java_obj.setSpatialQueryObject(self.spatial_query_object._jobject)
        if self.time_conditions is not None:
            java_obj.setTimeConditions(_to_java_time_condition_array(self.time_conditions))
        if self.spatial_query_mode is not None:
            java_obj.setSpatialQueryMode(self.spatial_query_mode._jobject)
        if self.group_by is not None:
            java_obj.setGroupBy(to_java_string_array(self.group_by))
        if self.join_items is not None:
            java_obj.setJoinItems(QueryParameter._to_java_join_items(self.join_items))
        if self.result_fields is not None:
            java_obj.setResultFields(to_java_string_array(self.result_fields))
        if self.link_items is not None:
            java_obj.setLinkItems(QueryParameter._to_java_link_items(self.link_items))
        if self.has_geometry is not None:
            java_obj.setHasGeometry(self.has_geometry)
        if self.cursor_type is not None:
            java_obj.setCursorType(self.cursor_type._jobject)
        if self.order_by is not None:
            java_obj.setOrderBy(to_java_string_array(self.order_by))
        return java_obj

    @staticmethod
    def _to_java_join_items(items):
        if items is None:
            return
        else:
            join_items = get_jvm().com.supermap.data.JoinItems()
            if isinstance(items, JoinItem):
                join_items.add(items._jobject)
            else:
                for item in items:
                    if isinstance(item, JoinItem):
                        join_items.add(item._jobject)

        return join_items

    @staticmethod
    def _to_java_link_items(items):
        if items is None:
            return
        else:
            link_items = get_jvm().com.supermap.data.LinkItems()
            if isinstance(items, LinkItem):
                link_items.add(items._jobject)
            else:
                for item in items:
                    if isinstance(item, LinkItem):
                        link_items.add(item._jobject)

        return link_items

    @staticmethod
    def _from_java_object(java_obj):
        obj = QueryParameter()
        obj.set_spatial_query_mode(java_obj.getSpatialQueryMode().name())
        obj.set_attribute_filter(java_obj.getAttributeFilter())
        spatial_query_object = java_obj.getSpatialQueryObject()
        if spatial_query_object is not None:
            from .ws import get_datasource
            classname = spatial_query_object.getClass().getName()
            if classname == "com.supermap.data.DatasetVector":
                name = spatial_query_object.getName()
                java_datasource_alias = spatial_query_object.getDatasource().getAlias()
                obj.set_spatial_query_object(get_datasource(java_datasource_alias)[name])
            else:
                if classname == "com.supermap.data.Recordset":
                    java_dataset = spatial_query_object.getDataset()
                    name = java_dataset.getName()
                    java_datasource_alias = java_dataset.getDatasource().getAlias()
                    dt = get_datasource(java_datasource_alias)[name]
                    obj.set_spatial_query_object(Recordset._from_java_object(spatial_query_object, dt))
                else:
                    if classname == "com.supermap.data.Rectangle2D":
                        obj.set_spatial_query_object(Rectangle._from_java_object(spatial_query_object))
                    else:
                        if classname == "com.supermap.data.Point2D":
                            obj.set_spatial_query_object(Point2D._from_java_object(spatial_query_object))
                        else:
                            obj.set_spatial_query_object(Geometry._from_java_object(spatial_query_object))
        timeConds = java_obj.getTimeConditions()
        if timeConds is not None:
            if len(timeConds) > 0:
                obj.set_time_conditions(list([TimeCondition._from_java_object(item) for item in timeConds]))
        obj.set_group_by(java_obj.getGroupBy())
        java_join_items = java_obj.getJoinItems()
        if java_join_items is not None:
            if java_join_items.getCount() > 0:
                joins = []
                for i in range(java_join_items.getCount()):
                    joins.append(JoinItem._from_java_object(java_join_items.get(i)))

                obj.set_join_items(joins)
        obj.set_order_by(java_obj.getOrderBy())
        obj.set_result_fields(java_obj.getResultFields())
        java_link_items = java_obj.getLinkItems()
        if java_link_items is not None:
            if java_link_items.getCount() > 0:
                links = []
                for i in range(java_link_items.getCount()):
                    links.append(LinkItem._from_java_object(java_link_items.get(i)))

                obj.set_link_items(links)
        obj.set_has_geometry(java_obj.getHasGeometry())
        obj.set_cursor_type(java_obj.getCursorType().name())
        return obj

    def to_dict(self):
        """
        将数据集查询参数信息输出到 dict 中

        :rtype: dict
        """
        d = dict()
        if self.spatial_query_mode is not None:
            d["spatial_query_mode"] = self.spatial_query_mode.name
        if self.attribute_filter:
            d["attribute_filter"] = self.attribute_filter
        if self.spatial_query_object is not None:
            d["spatial_query_object"] = self.spatial_query_object
        if self.time_conditions is not None:
            d["time_conditions"] = self.time_conditions
        if self.group_by is not None:
            d["group_by"] = self.group_by
        if self.join_items is not None:
            d["join_items"] = self.join_items
        if self.order_by is not None:
            d["order_by"] = self.order_by
        if self.result_fields is not None:
            d["result_fields"] = self.result_fields
        if self.link_items is not None:
            d["link_items"] = self.link_items
        if self.has_geometry is not None:
            d["has_geometry"] = self.has_geometry
        if self.cursor_type is not None:
            d["cursor_type"] = self.cursor_type.name
        return d

    @staticmethod
    def make_from_dict(values):
        """
        从 dict 中构造数据集查询参数对象

        :param dict values: 包含查询参数的 dict 对象。具体查看 :py:meth:`to_dict`
        :rtype: QueryParameter
        """
        return QueryParameter().from_dict(values)

    def from_dict(self, values):
        """
        从 dict 中读取查询参数

        :param dict values: 包含查询参数的 dict 对象。具体查看 :py:meth:`to_dict`
        :return: self
        :rtype: QueryParameter
        """
        if "spatial_query_mode" in values.keys():
            self.set_spatial_query_mode(values["spatial_query_mode"])
        if "attribute_filter" in values.keys():
            self.set_attribute_filter(values["attribute_filter"])
        if "spatial_query_object" in values.keys():
            self.set_spatial_query_object(values["spatial_query_object"])
        if "time_conditions" in values.keys():
            self.set_time_conditions(values["time_conditions"])
        if "group_by" in values.keys():
            self.set_group_by(values["group_by"])
        if "join_items" in values.keys():
            self.set_join_items(values["join_items"])
        if "order_by" in values.keys():
            self.set_order_by(values["order_by"])
        if "result_fields" in values.keys():
            self.set_result_fields(values["result_fields"])
        if "link_items" in values.keys():
            self.set_link_items(values["link_items"])
        if "has_geometry" in values.keys():
            self.set_has_geometry(values["has_geometry"])
        if "cursor_type" in values.keys():
            self.set_cursor_type(values["cursor_type"])
        return self

    def to_json(self):
        """
        将查询参数输出为 json 字符串

        :rtype: str
        """
        d = self.to_dict()
        if "spatial_query_object" in d.keys():
            obj = d["spatial_query_object"]
            if isinstance(obj, Point2D):
                dp = {'type':"P2", 
                 'data':(obj.to_json)()}
            else:
                if isinstance(obj, Rectangle):
                    dp = {'type':"RC", 
                     'data':(obj.to_json)()}
                else:
                    if isinstance(obj, Geometry):
                        dp = {'type':"G", 
                         'data':(obj.to_json)()}
                    else:
                        if isinstance(obj, Recordset):
                            dp = {'type':"RD", 
                             'data':(obj.to_json)()}
                        else:
                            if isinstance(obj, DatasetVector):
                                dp = {'type':"DT", 
                                 'data':(obj.to_json)()}
                            else:
                                dp = None
            if dp is not None:
                d["spatial_query_object"] = dp
        if "time_conditions" in d.keys():
            items = d["time_conditions"]
            d["time_conditions"] = list([item.to_json() for item in items])
        if "link_items" in d.keys():
            items = d["link_items"]
            d["link_items"] = list([item.to_json() for item in items])
        if "join_items" in d.keys():
            items = d["join_items"]
            d["join_items"] = list([item.to_json() for item in items])
        return json.dumps(d)

    @staticmethod
    def from_json(value):
        """
        从 json 字符串中构造数据集查询参数对象

        :param str value:  json 字符串
        :rtype: QueryParameter
        """
        d = json.loads(value)
        if "spatial_query_object" in d:
            dp = d["spatial_query_object"]
            _type = dp["type"]
            if _type == "P2":
                sp = Point2D.from_json(dp["data"])
            else:
                if _type == "RC":
                    sp = Rectangle.from_json(dp["data"])
                else:
                    if _type == "G":
                        sp = Geometry.from_json(dp["data"])
                    else:
                        if _type == "RD":
                            sp = Recordset.from_json(dp["data"])
                        else:
                            if _type == "DT":
                                sp = Dataset.from_json(dp["data"])
                            else:
                                sp = None
            d["spatial_query_object"] = sp
        if "time_conditions" in d:
            items = d["time_conditions"]
            d["time_conditions"] = list([TimeCondition.from_json(item) for item in items])
        if "link_items" in d:
            items = d["link_items"]
            d["link_items"] = list([LinkItem.from_json(item) for item in items])
        if "join_items" in d:
            items = d["join_items"]
            d["join_items"] = list([JoinItem.from_json(item) for item in items])
        return QueryParameter.make_from_dict(d)


class DatasetVectorInfo(object):
    __doc__ = "\n    矢量数据集信息类。包括了矢量数据集的信息，如矢量数据集的名称，数据集的类型，编码方式，是否选用文件缓存等。文件缓存只针对图幅索引而言\n\n    "

    def __init__(self, name=None, dataset_type=None, encode_type=None, is_file_cache=True):
        """
        构造矢量数据集信息类

        :param str name: 数据集名称
        :param dataset_type:  数据集类型
        :type dataset_type: DatasetType or str
        :param encode_type:  数据集的压缩编码方式。支持四种压缩编码方式，即单字节，双字节，三字节和四字节编码方式
        :type encode_type: EncodeType or str
        :param bool is_file_cache: 是否使用文件形式的缓存。文件形式的缓存只针对图幅索引有用
        """
        self._name = None
        self._type = None
        self._is_file_cache = False
        self._encode_type = None
        self.set_name(name).set_type(dataset_type).set_encode_type(encode_type).set_file_cache(is_file_cache)

    def __repr__(self):
        return "DatasetVectorInfo(%s, %s, %s, %s)" % (
         self.name, self.type, self.encode_type, str(self.is_file_cache))

    @property
    def name(self):
        """str:   数据集名称，数据集的名称限制：数据集名称的长度限制为30个字符（也就是可以为30个英文字母或者15个汉字），组成数据集名称的字符可以
        为字母、汉字、数字和下划线，数据集名称不可以用数字和下划线开头，如果用字母开头，数据集名称不可以和数据库的保留关键字冲突。"""
        return self._name

    @property
    def type(self):
        """DatasetType: 数据集类型"""
        return self._type

    @property
    def encode_type(self):
        """EncodeType: 数据集的压缩编码方式。支持四种压缩编码方式，即单字节，双字节，三字节和四字节编码方式"""
        return self._encode_type

    @property
    def is_file_cache(self):
        """bool: 是否使用文件形式的缓存。文件形式的缓存只针对图幅索引有用"""
        return self._is_file_cache

    def set_name(self, value):
        """
        设置数据集的名称

        :param str value: 数据集名称
        :return: self
        :rtype: DatasetVectorInfo
        """
        self._name = value
        return self

    def set_type(self, value):
        """
        设置数据集的类型

        :param value: 数据集类型
        :type value: DatasetType or str
        :return: self
        :rtype: DatasetVectorInfo
        """
        self._type = DatasetType._make(value)
        return self

    def set_encode_type(self, value):
        """
        设置数据集的压缩编码方式

        :param value: 数据集的压缩编码方式
        :type value: EncodeType or str
        :return: self
        :rtype: DatasetVectorInfo
        """
        self._encode_type = EncodeType._make(value)
        return self

    def set_file_cache(self, value):
        """
        设置是否使用文件形式的缓存。文件形式的缓存只针对图幅索引有用。

        :param bool value: 是否使用文件形式的缓存
        :return: self
        :rtype: DatasetVectorInfo
        """
        self._is_file_cache = value
        return self

    @property
    def _jobject(self):
        java_obj = get_jvm().com.supermap.data.DatasetVectorInfo()
        if self.name is not None:
            java_obj.setName(self.name)
        if self.encode_type is not None:
            java_obj.setEncodeType(self.encode_type._jobject)
        if self.type is not None:
            java_obj.setType(self.type._jobject)
        if self.is_file_cache is not None:
            java_obj.setFileCache(self.is_file_cache)
        return java_obj

    @staticmethod
    def _from_java_object(java_obj):
        obj = DatasetVectorInfo()
        obj.set_name(java_obj.getName())
        obj.set_type(DatasetType._make(java_obj.getType().name()))
        obj.set_file_cache(java_obj.isFileCache())
        obj.set_encode_type(EncodeType._make(java_obj.getEncodeType()))
        return obj

    def to_dict(self):
        """
        将当前对象的信息输出为 dict 对象

        :rtype: dict
        """
        d = dict()
        if self.name is not None:
            d["name"] = self.name
        if self.type is not None:
            d["type"] = self.type.name
        if self.is_file_cache is not None:
            d["is_file_cache"] = self.is_file_cache
        if self.encode_type is not None:
            d["encode_type"] = self.encode_type.name
        return d

    @staticmethod
    def make_from_dict(values):
        """
        从 dict 中构造 DatasetVectorInfo 对象

        :param dict values: 包含矢量数据集信息的 dict 对象，具体查看 :py:meth:`to_dict`
        :rtype: DatasetVectorInfo
        """
        return DatasetVectorInfo().from_dict(values)

    def from_dict(self, values):
        """
        从 dict 中读取 DatasetVectorInfo 对象

        :param dict values: 包含矢量数据集信息的 dict 对象，具体查看 :py:meth:`to_dict`
        :rtype: self
        :rtype: DatasetVectorInfo
        """
        if "name" in values.keys():
            self.set_name(values["name"])
        if "type" in values.keys():
            self.set_type(values["type"])
        if "is_file_cache" in values.keys():
            self.set_file_cache(values["is_file_cache"])
        if "encode_type" in values.keys():
            self.set_encode_type(values["encode_type"])
        return self


class DatasetVector(Dataset):
    __doc__ = "\n    矢量数据集类。用于对矢量数据集进行描述，并对之进行相应的管理和操作。对矢量数据集的操作主要包括数据查询、修改、删除、建立索引等。\n    "

    def __init__(self):
        Dataset.__init__(self)

    def __str__(self):
        if not self._java_object:
            return ""
        infos = []
        infos.append("name:         " + self.name)
        infos.append("table name:   " + self.table_name)
        infos.append("type:         " + self.type.name)
        infos.append("record count: " + str(self.get_record_count()))
        infos.append("fields count: " + str(self.get_field_count()))
        fields = self.field_infos
        rd = self.get_recordset(cursor_type="STATIC")
        max_len = []
        for i in range(len(fields)):
            max_len.append(0)

        top_10_values = []
        i = 0
        while rd.has_next() and i < 10:
            values = rd.get_values(False, False)
            values_str = []
            for j in range(len(values)):
                value = values[j]
                if value is None:
                    values_str.append(" ")
                elif isinstance(value, float):
                    values_str.append("%.6f" % value)
                elif isinstance(value, datetime.datetime):
                    values_str.append(value.strftime("%Y-%m-%d %H:%M:%S"))
                elif isinstance(value, (bytes, bytearray)):
                    try:
                        str_d = value.decode("utf-8")
                        if len(str_d) > 32:
                            str_d = str_d[0[:29]] + "..."
                        values_str.append(str_d)
                    except:
                        values_str.append("...")

                else:
                    str_d = str(value)
                    if len(str_d) > 32:
                        str_d = str_d[0[:29]] + "..."
                    values_str.append(str_d)

            rd.move_next()
            i += 1
            for j in range(len(values)):
                if len(values_str[j]) > max_len[j]:
                    max_len[j] = len(values_str[j])

            top_10_values.append(values_str)

        rd.close()
        field_formats = []
        titles = []
        for i in range(len(fields)):
            field = fields[i]
            format_len = max(len(field.name), max_len[i], len(field.type.name))
            field_formats.append("%-" + str(format_len) + "s")
            title = ""
            for j in range(format_len):
                title += "-"

            titles.append(title)

        f_format = "  ".join(field_formats)
        infos.append(f_format % tuple((field.name for field in fields)))
        infos.append(f_format % tuple((field.type.name for field in fields)))
        infos.append(f_format % tuple(titles))
        for values in top_10_values:
            infos.append(f_format % tuple(values))

        return "\n".join(infos)

    def get_recordset(self, is_empty=False, cursor_type=CursorType.DYNAMIC, fields=None):
        """
        根据给定的参数来返回空的记录集或者返回包括所有记录的记录集对象。

        :param bool is_empty: 是否返回空的记录集参数。为 true 时返回空记录集。为 false 时返回包含所有记录的记录集合对象。
        :param cursor_type: 游标类型，以便用户控制查询出来的记录集的属性。当游标类型为动态时，记录集可以被修改，当游标类型为静态时，记录集为只读。可以为枚举值或名称
        :type cursor_type:  CursorType or str
        :param fields:  需要输出的结果字段名称，如果为 None 则保留所有的字段
        :type fields: list[str] or str
        :return: 满足条件的记录集对象
        :rtype: Recordset
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            if fields is None:
                rd = Recordset._from_java_object(self._jobject.getRecordset(is_empty, CursorType._make(cursor_type, CursorType.DYNAMIC)._jobject), self)
                if rd is not None:
                    d = {'func':"get_recordset", 
                     'params':{'is_empty':is_empty, 
                      'cursor_type':(CursorType._make(cursor_type, CursorType.DYNAMIC)).name}}
                    rd._set_custom_params(d)
            else:
                return rd
                if is_empty:
                    attrFilter = "SmID < 0"
                else:
                    attrFilter = "SmID > 0"
            return self.query_with_filter(attrFilter, cursor_type, fields)
        except Exception as e:
            try:
                import traceback
                log_error(traceback.format_exc())
                return
            finally:
                e = None
                del e

    @property
    def field_infos(self):
        """list[FieldInfo]: 数据集的所有字段信息"""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            from ._util import java_field_infos_to_list
            return java_field_infos_to_list(self._jobject.getFieldInfos())
        except Exception as e:
            try:
                log_error(e)
                return
            finally:
                e = None
                del e

    def get_field_count(self):
        """
        返回数据集所有的字段的数目

        :rtype: int
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            return self._jobject.getFieldInfos().getCount()
        except Exception as e:
            try:
                log_error(e)
                return 0
            finally:
                e = None
                del e

    def get_field_info(self, item):
        """
        获取指定名称或序号的字段

        :param item:  字段名称或序号
        :type item: int or str
        :return: 字段信息
        :rtype: FieldInfo
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            java_fieldInfos = self._jobject.getFieldInfos()
            if isinstance(item, int):
                if item < 0:
                    item += java_fieldInfos.getCount()
                return FieldInfo._from_java_object(java_fieldInfos.get(item))
            if isinstance(item, str):
                if java_fieldInfos.indexOf(item) >= 0:
                    return FieldInfo._from_java_object(java_fieldInfos.get(item))
        except Exception as e:
            try:
                log_error(e)
                return
            finally:
                e = None
                del e

    def remove_field(self, item):
        """
        删除指定的字段

        :param item:  字段名称或序号
        :type item: int or str
        :return: 删除成功返回 True，否则返回 False
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            java_fieldInfos = self._jobject.getFieldInfos()
            if isinstance(item, int):
                if item < 0:
                    item += java_fieldInfos.getCount()
            return java_fieldInfos.remove(item)
        except Exception as e:
            try:
                log_error(e)
                return False
            finally:
                e = None
                del e

        return False

    def index_of_field(self, name):
        """
        获取指定字段名称序号

        :param str name: 字段名称
        :return: 如果字段存在返回字段的序号，否则返回 -1
        :rtype: int
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            java_fieldInfos = self._jobject.getFieldInfos()
            return java_fieldInfos.indexOf(name)
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

        return -1

    def create_field(self, field_info):
        """
        创建字段

        :param FieldInfo field_info:  字段信息，如果字段的类型是必填字段，必须设置默认值，没有设置默认值时，添加失败。
        :rtype: bool
        :return: 创建字段成功返回 True，否则返回 False
        """
        if field_info is None:
            raise ValueError("field_info is None")
        elif self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            java_fieldInfos = self._jobject.getFieldInfos()
            return java_fieldInfos.add(field_info._jobject) >= 0
        except Exception as e:
            try:
                log_error(e)
                return False
            finally:
                e = None
                del e

        return False

    def create_fields(self, field_infos):
        """
        创建多个字段

        :param list[FieldInfo] field_infos: 字段信息集合
        :return: 创建字段成功返回 True，否则返回 False
        :rtype: bool
        """
        if field_infos is None:
            raise ValueError("field_infos is None")
        elif self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            java_fieldInfos = self._jobject.getFieldInfos()
            for field in field_infos:
                if not field.name.lower().startswith("sm"):
                    java_fieldInfos.add(field._jobject)

            return True
        except Exception as e:
            try:
                log_error(e)
                return False
            finally:
                e = None
                del e

        return False

    @property
    def charset(self):
        """Charset: 矢量数据集的字符集"""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            return Charset._make(self._jobject.getCharset().name())
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def set_charset(self, value):
        """
        设置数据集的字符集

        :param value: 数据集的字符集
        :type value: Charset or str
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self._jobject.setCharset(Charset._make(value, Charset.UTF8)._jobject)
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def get_geometries(self, attr_filter=None):
        """
        根据指定的属性过滤条件获取几何对象

        :param str attr_filter: 属性过滤条件，默认为 None，即返回当前数据集的所有几何对象
        :return: 满足指定条件的所有几何对象
        :rtype: list[Geometry]
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            rd = self.query_with_filter(attr_filter, CursorType.STATIC, "SmID", True)
            geos = rd.get_geometries()
            rd.close()
            return geos
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def get_features(self, attr_filter=None, has_geometry=True, fields=None):
        """
        根据指定的属性过滤条件获取要素对象

        :param str attr_filter: 属性过滤条件，默认为 None，即返回当前数据集的所有要素对象
        :param bool has_geometry:  是否获取几何对象，为 False 时将只返回字段值
        :param fields:  结果字段名称
        :type fields: list[str] or str
        :return: 满足指定条件的所有要素对象
        :rtype: list[Feature]

        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            rd = self.query_with_filter(attr_filter, CursorType.STATIC, fields, has_geometry)
            features = rd.get_features()
            rd.close()
            return features
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def delete_records(self, ids):
        """
        通过 ID 数组删除数据集中的记录。

        :param list[int] ids: 待删除记录的 ID 数组
        :return: 删除成功返回 True，否则返回 False
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            return self._jobject.deleteRecords(to_java_int_array(ids))
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

        return False

    def truncate(self):
        """
        清除矢量数据集中的所有记录。

        :return: 清除记录是否成功，成功返回 True，失败返回 False。
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            return self._jobject.truncate()
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

        return False

    def is_file_cache(self):
        """
        返回是否使用文件形式的缓存。文件形式的缓存可以提高浏览速度。
        注意：文件形式的缓存只对 Oracle 数据源下已创建图幅索引的矢量数据集有效。

        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            return self._jobject.isFileCache()
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

        return False

    def set_file_cache(self, value):
        """
        设置是否使用文件形式的缓存。

        :param bool value: 是否使用文件形式的缓存
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            self._jobject.setFileCache(bool(value))
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def get_field_values(self, fields):
        """
        获取指定字段的字段值

        :param fields: 字段名称列表
        :type fields: str or list[str]
        :return: 获取得到的字段值，每个字段名称对应一个列表
        :rtype: dist[str,list]
        """
        fields = split_input_list_from_str(fields)
        if not fields:
            valid_fields = []
            for i in range(self.get_field_count()):
                field_info = self.get_field_info(i)
                if not field_info.is_system_field():
                    valid_fields.append(field_info.name)

        else:
            valid_fields = list(filter((lambda item: self.index_of_field(item) >= 0), fields))
        valid_fields_index = []
        for i, it in enumerate(valid_fields):
            valid_fields_index.append((i, it))

        result_values = []
        for i in range(len(valid_fields)):
            result_values.append([])

        recordset = self.query_with_filter("SmID > 0", CursorType.STATIC, valid_fields, False)
        if recordset:
            while recordset.has_next():
                for index, name in valid_fields_index:
                    value = recordset.get_value(name)
                    result_values[index].append(value)

                recordset.move_next()

            recordset.dispose()
        values = {}
        for index, name in valid_fields_index:
            values[name] = result_values[index]

        return values

    def query(self, query_param=None):
        """
        通过设置查询条件对矢量数据集进行查询，该方法默认查询空间信息与属性信息。

        :param QueryParameter query_param: 查询条件
        :return: 满足查询条件的结果记录集
        :rtype: Recordset
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            if query_param is None:
                query_param = QueryParameter()
            self.open()
            java_recordset = self._jobject.query(query_param._jobject)
            if java_recordset is not None:
                return Recordset._from_java_object(java_recordset, self)
            return
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def query_with_ids(self, ids, id_field_name="SmID", cursor_type=CursorType.DYNAMIC):
        """
        根据跟定的 ID 数组，查询满足记录的记录集

        :param list[int] ids: ID 数组
        :param str id_field_name: 数据集中用于表示 ID 的字段名称。默认为 “SmID”
        :param cursor_type:   游标类型
        :type cursor_type: CursorType or str
        :return: 满足查询条件的结果记录集
        :rtype: Recordset
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            if ids is None:
                ids = []
            _idFieldName = id_field_name if id_field_name is not None else "SmID"
            java_recordset = self._jobject.query(to_java_int_array(ids), _idFieldName, CursorType._make(cursor_type, CursorType.DYNAMIC)._jobject)
            if java_recordset is not None:
                rd = Recordset._from_java_object(java_recordset, self)
                if rd is not None:
                    rd._set_custom_params({'func':"query_with_ids",  'params':{'ids':ids, 
                      'id_field_name':id_field_name, 
                      'cursor_type':(CursorType._make(cursor_type, CursorType.DYNAMIC)).name}})
                return rd
            return
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def query_with_bounds(self, bounds, attr_filter=None, cursor_type=CursorType.DYNAMIC):
        """
        根据地理范围查询记录集

        :param Rectangle bounds: 已知的空间范围
        :param str attr_filter: 查询过滤条件，相当于 SQL 语句中的 Where 子句部分
        :param cursor_type: 游标类型，可以为枚举值或名称
        :type cursor_type: CursorType or str
        :return: 满足查询条件的结果记录集
        :rtype: Recordset
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            if bounds is None:
                bounds = self.bounds
            java_recordset = self._jobject.query(bounds._jobject, attr_filter, CursorType._make(cursor_type, CursorType.DYNAMIC)._jobject)
            if java_recordset is not None:
                rd = Recordset._from_java_object(java_recordset, self)
                if rd is not None:
                    rd._set_custom_params({'func':"query_with_bounds",  'params':{'bounds':(bounds.to_json)(), 
                      'attr_filter':attr_filter, 
                      'cursor_type':(CursorType._make(cursor_type, CursorType.DYNAMIC)).name}})
                return rd
            return
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def query_with_distance(self, geometry, distance, unit=None, attr_filter=None, cursor_type=CursorType.DYNAMIC):
        """
        用于查询数据集中落在指定空间对象的缓冲区内，并且满足一定条件的记录。

        :param geometry: 用于查询的空间对象。
        :type geometry: Geometry or Point2D or Rectangle
        :param float distance: 查询半径
        :param unit: 查询半径的单位，如果为 None 则查询半径的单位与数据集的单位相同。
        :type unit: Unit or str
        :param str attr_filter:  查询过滤条件，相当于 SQL 语句中的 Where 子句部分
        :param cursor_type: 游标类型，可以为枚举值或名称
        :type cursor_type: CursorType or str
        :return: 满足查询条件的结果记录集
        :rtype: Recordset
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            if isinstance(geometry, Point2D):
                geometry = GeoPoint(geometry)
            else:
                if isinstance(geometry, Rectangle):
                    geometry = geometry.to_region()
                elif unit is None:
                    if self.prj_coordsys is not None:
                        unit = self.prj_coordsys.coord_unit
                    else:
                        unit = "Meter"
                self.open()
                from ._util import create_geometry_buffer
                bufferGeo = create_geometry_buffer(geometry, distance, self.prj_coordsys, unit)
                if bufferGeo is not None:
                    queryParam = QueryParameter()
                    queryParam.set_spatial_query_object(bufferGeo).set_spatial_query_mode(SpatialQueryMode.INTERSECT).set_attribute_filter(attr_filter).set_cursor_type(cursor_type)
                    java_recordset = self._jobject.query(queryParam._jobject)
                    del bufferGeo
                    if java_recordset is not None:
                        return Recordset._from_java_object(java_recordset, self)
                    return
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def query_with_filter(self, attr_filter=None, cursor_type=CursorType.DYNAMIC, result_fields=None, has_geometry=True):
        """
        根据指定的属性过滤条件查询记录集

        :param str attr_filter:  查询过滤条件，相当于 SQL 语句中的 Where 子句部分
        :param cursor_type: 游标类型，可以为枚举值或名称
        :type cursor_type: CursorType or str
        :param result_fields: 结果字段名称
        :type result_fields: list[str] or str
        :param bool has_geometry: 是否包含几何对象
        :return: 满足查询条件的结果记录集
        :rtype: Recordset
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            queryParam = QueryParameter().set_attribute_filter(attr_filter).set_cursor_type(cursor_type).set_result_fields(result_fields).set_has_geometry(has_geometry).set_order_by([
             "SmID ASC"])
            java_recordset = self._jobject.query(queryParam._jobject)
            if java_recordset is not None:
                return Recordset._from_java_object(java_recordset, self)
            return
        except Exception as e:
            try:
                import traceback
                log_error(traceback.format_exc())
            finally:
                e = None
                del e

    def stat(self, item, stat_mode):
        """
        对指定的字段按照给定的方式进行统计。
        当前版本提供了6种统计方式。统计字段的最大值，最小值，平均值，总和，标准差，以及方差。
        当前版本支持的统计字段类型为布尔，字节，双精度，单精度，16位整型，32位整型。

        :param item:  字段名称或序号
        :type item: str or int
        :param stat_mode: 字段统计模式
        :type stat_mode: StatisticMode or str
        :return: 统计结果
        :rtype: float
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            if isinstance(item, int):
                if item < 0:
                    item += len(self.field_infos)
            return self._jobject.statistic(item, StatisticMode._make(stat_mode)._jobject)
        except Exception as e:
            try:
                log_error(e)
                return
            finally:
                e = None
                del e

    def update_field_express(self, item, express, attr_filter=None):
        """
        根据指定的需要更新的字段名，用指定的表达式计算结果更新符合查询条件的所有记录的字段值。需要更新的字段不能够为系统字段，也就是说不可以为 Sm 开头的字段（smUserID 除外）。

        :param item:  字段名称或序号
        :type item: str or int
        :param str express: 指定的表达式，表达式可以是字段的运算或函数的运算。例如："SMID" 、"abs(SMID)"、"SMID+1"、 " '字符串'"。
        :param str attr_filter: 要更新记录的查询条件，如果 attributeFilter 为空字符串，则更新表中所有的记录
        :return: 更新字段成功返回 True，否则返回 False
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            if isinstance(item, int):
                if item < 0:
                    item += len(self.field_infos)
            self.open()
            return get_jvm().com.supermap.jsuperpy.DatasetUtils.updateFieldsEx(self._jobject, item, express, attr_filter)
        except Exception as e:
            try:
                log_error(e)
                return
            finally:
                e = None
                del e

    def update_field(self, item, value, attr_filter=None):
        """
        根据指定的需要更新的字段名称，用指定的用于更新的字段值更新符合 attributeFilter 条件的所有记录的字段值。需要更新的字段不能够为系统字段，
        也就是说待更新字段不可以为 sm 开头的字段（smUserID 除外）。

        :param item:  字段名称或序号
        :type item: str or int
        :param value: 指定用于更新的字段值。
        :type value: int or float or str or datetime.datetime or bytes or bytearray
        :param str attr_filter: 要更新记录的查询条件，如果 attributeFilter 为空字符串，则更新表中所有的记录
        :return: 更新字段成功返回 True，否则返回 False
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            if isinstance(item, int):
                if item < 0:
                    item += len(self.field_infos)
            self.open()
            from ._util import convert_value_to_java
            _value = convert_value_to_java(value, self.get_field_info(item).type)
            return get_jvm().com.supermap.jsuperpy.DatasetUtils.updateFields(self._jobject, item, _value, attr_filter)
        except Exception as e:
            try:
                log_error(e)
                return
            finally:
                e = None
                del e

    def compute_bounds(self):
        """
        重新计算数据集的空间范围。

        :rtype: Rectangle
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            return Rectangle._from_java_object(self._jobject.computeBounds())
        except Exception as e:
            try:
                log_error(e)
                return
            finally:
                e = None
                del e

    @property
    def child_dataset(self):
        """DatasetVector: 矢量数据集的子数据集。主要用于网络数据集"""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            return Dataset._from_java_object(self._jobject.getChildDataset(), self.datasource)
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    @property
    def parent_dataset(self):
        """DatasetVector: 矢量数据集的父数据集。主要用于网络数据集"""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            return Dataset._from_java_object(self._jobject.getParentDataset(), self.datasource)
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def get_record_count(self):
        """
        返回矢量数据集中全部记录的数目。

        :rtype: int
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            return self._jobject.getRecordCount()
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

        return 0

    def is_available_field_name(self, name):
        """
        判断指定的字段名称是否是合法而且没有被占用的字段名称

        :param str name:  字段名称
        :return: 字段名称合法且没有被占用返回 True，否则返回 False
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            return self._jobject.isAvailableFieldName(name)
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

        return False

    def get_available_field_name(self, name):
        """
        根据传入参数生成一个合法的字段名。

        :param str name: 字段名称
        :rtype: str
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            return self._jobject.getAvailableFieldName(name)
        except Exception as e:
            try:
                log_error(e)
                return
            finally:
                e = None
                del e

    def get_tolerance_dangle(self):
        """
        获取短悬线容限

        :rtype: float
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            return self._jobject.getTolerance().getDangle()
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def set_tolerance_dangle(self, value):
        """
        设置短悬线容限

        :param float value: 短悬线容限

        """
        if self._jobject is None:
            log_error("DatasetVector object has been disposed")
            return
        try:
            self.open()
            self._jobject.getTolerance().setDangle(float(value))
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def get_tolerance_extend(self):
        """
        获取长悬线容限

        :rtype: float
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            return self._jobject.getTolerance().getExtend()
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def set_tolerance_extend(self, value):
        """
        设置长悬线容限

        :param float value: 长悬线容限
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            self._jobject.getTolerance().setExtend(float(value))
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def get_tolerance_grain(self):
        """
        获取颗粒容限

        :rtype: float
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            return self._jobject.getTolerance().getGrain()
        except Exception as e:
            try:
                log_error(e)
                return
            finally:
                e = None
                del e

    def set_tolerance_grain(self, value):
        """
        设置颗粒容限

        :param float value: 颗粒容限
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            self._jobject.getTolerance().setGrain(float(value))
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def get_tolerance_node_snap(self):
        """
        获取节点容限

        :rtype: float
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            return self._jobject.getTolerance().getNodeSnap()
        except Exception as e:
            try:
                log_error(e)
                return
            finally:
                e = None
                del e

    def set_tolerance_node_snap(self, value):
        """
        设置节点容限

        :param float value: 节点容限
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            self._jobject.getTolerance().setNodeSnap(float(value))
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def get_tolerance_small_polygon(self):
        """
        获取最小多边形容限

        :rtype: float
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            return self._jobject.getTolerance().getSmallPolygon()
        except Exception as e:
            try:
                log_error(e)
                return
            finally:
                e = None
                del e

    def set_tolerance_small_polygon(self, value):
        """
        设置最小多边形容限

        :param float value:  最小多边形容限
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            self._jobject.getTolerance().setSmallPolygon(float(value))
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def reset_tolerance_as_default(self):
        """
        将所有的容限设为缺省值，单位与矢量数据集坐标系单位相同:

         - 节点容限的默认值为数据集宽度的1/1000000；
         - 颗粒容限的默认值为数据集宽度的1/1000；
         - 短悬线容限的默认值为数据集宽度的1/10000；
         - 长悬线容限的默认值为数据集宽度的1/10000；
         - 最小多边形容限的默认值为0。

        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            self._jobject.getTolerance().setDefault()
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def build_field_index(self, field_names, index_name):
        """
        为数据集的非空间字段创建索引

        :param field_names:  非空间字段名称
        :type field_names: list[str] or str
        :param str index_name: 索引名称
        :return: 创建成功返回 true，否则返回 false
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            return self._jobject.buildFieldIndex(to_java_string_array(split_input_list_from_str(field_names)), index_name)
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

        return False

    def drop_field_index(self, index_name):
        """
        根据索引名指定字段，删除该字段的索引

        :param str index_name: 字段索引名称
        :return:  删除成功返回 True，否则返回 False
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            return self._jobject.dropFieldIndex(index_name)
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

        return False

    def drop_spatial_index(self):
        """
        删除空间索引，删除成功返回 True，否则返回 False

        :rtype: bool

        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            return self._jobject.dropSpatialIndex()
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

        return False

    def get_field_indexes(self):
        """
        返回当前数据集属性表建的索引与建索引的字段的关系映射对象。其中键值为索引值，映射值为索引所在字段。

        :rtype: dict
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            return self._jobject.getFieldIndexes()
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def get_spatial_index_type(self):
        """
        获取空间索引类型

        :rtype: SpatialIndexType
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            return SpatialIndexType._make(self._jobject.getSpatialIndexType().name())
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def is_spatial_index_dirty(self):
        """
        判断当前数据集的空间索引是否需要重建。因为在修改数据过程后，可能需要重建空间索引。
        注意：

         - 当矢量数据集无空间索引时，如果其记录条数已达到建立空间索引的要求，则返回 True，建议用户创建空间索引；否则返回 False。
         - 如果矢量数据集已有空间索引（图库索引除外），但其记录条数已经不能达到建立空间索引的要求时，返回 True。

        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            return self._jobject.isSpatialIndexDirty()
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

        return False

    def is_spatial_index_type_supported(self, spatial_index_type):
        """
        判断当前数据集是否支持指定的类型的空间索引。

        :param spatial_index_type: 空间索引类型，可以为枚举值或名称
        :type spatial_index_type: SpatialIndexType or str
        :return: 如果支持指定的空间索引类型，返回值为 true，否则为 false。
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            return self._jobject.isSpatialIndexTypeSupported(SpatialIndexType._make(spatial_index_type)._jobject)
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

        return False

    def re_build_spatial_index(self):
        """
        在原有的空间索引的基础上进行重建，如果原来的空间索引被破坏，那么重建成功之后还可以继续使用。

        :return: 重建索引成功返回 Ture，否则返回 False。
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            return self._jobject.reBuildSpatialIndex()
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

        return False

    def build_spatial_index(self, spatial_index_info):
        """
        根据指定的空间索引信息或索引类型为矢量数据集创建空间索引。
        注意:

            - 数据库中的点数据集不支持四叉树（QTree）索引和 R 树索引（RTree）；
            - 网络数据集不支持任何类型的空间索引；
            - 属性数据集不支持任何类型的空间索引；
            - 路由数据集不支持图幅索引（TILE）；
            - 复合数据集不支持多级网格索引；
            - 数据库记录要大于1000条时才可以创建索引。

        :param spatial_index_info: 空间索引信息，或者空间索引类型，当为空间索引类型时，可以为枚举值或名称
        :type spatial_index_info: SpatialIndexInfo or SpatialIndexType
        :return: 创建索引成功返回 True，否则返回 False。
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            if isinstance(spatial_index_info, str):
                spatial_index_info = SpatialIndexType._make(spatial_index_info)
            return self._jobject.buildSpatialIndex(spatial_index_info._jobject)
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

        return False

    def appendParse error at or near `COME_FROM' instruction at offset 1334_0

    def append_fields(self, source, source_link_field, target_link_field, source_fields, target_fields=None):
        """
        从源数据集向目标数据集追加字段，并根据关联字段查询结果对字段进行赋值。

        注意：

         * 如果指定的源数据集中被追加到目标数据集的字段名集合的某字段在源数据集中不存在，则忽略此字段，只追加源数据集中存在的字段；
         * 如果指定了追加字段在目标数据集中相对应的字段名集合，则按所指定的字段名在目标数据集中创建所追加的字段；当指定的字段名在目标数据集中已存在时，则自动加_x(1、2、3...)进行字段的创建；
         * 如果在目标数据集中创建字段失败，则忽略此字段，继续追加其它字段；
         * 必须指定源字段名集合，否则追加不成功；
         * 可以不必指定目标字段名集合，一旦指定目标字段名集合，则此集合中字段名必须与源字段名集合中的字段名一一对应。

        :param source: 源数据集
        :type source: DatasetVector or str
        :param str  source_link_field: 源数据集中的与目标数据集的关联字段。
        :param str target_link_field: 目标数据集中的与源数据集的关联字段。
        :param source_fields: 源数据集中被追加到目标数据集的字段名集合。
        :type source_fields: list[str] or str
        :param target_fields: 追加字段在目标数据集中相对应的字段名集合。
        :type target_fields: list[str] or str
        :return: 一个布尔值，表示追加字段是否成功，成功返回 true，否则返回 false。
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError("Datasource")
        elif source is None:
            raise ValueError("source is None")
        from ._util import get_input_dataset
        source_dt = get_input_dataset(source)
        if not isinstance(source_dt, DatasetVector):
            raise ValueError("source must be Dataset")
        try:
            source_names = to_java_string_array(split_input_list_from_str(source_fields))
            if target_fields is not None:
                target_names = to_java_string_array(split_input_list_from_str(target_fields))
                result = self._jobject.appendFields(source_dt._jobject, str(source_link_field), str(target_link_field), source_names, target_names)
            else:
                result = self._jobject.appendFields(source_dt._jobject, str(source_link_field), str(target_link_field), source_names)
            return result
        except Exception as e:
            try:
                log_error(e)
                return False
            finally:
                e = None
                del e

    def get_field_name_by_sign(self, field_sign):
        """
        根据字段标识获取字段名。

        :param field_sign: 字段标识类型
        :type field_sign: FieldSign or str
        :return: 字段类型
        :rtype: str
        """
        if self._jobject is None:
            raise ObjectDisposedError("Datasource")
        field_sign = FieldSign._make(field_sign)
        if field_sign is None:
            raise ValueError("required FieldSign")
        return self._jobject.getFieldNameBySign(oj(field_sign))


class SpatialIndexInfo(object):
    __doc__ = "\n    空间索引信息类。该类提供了创建空间索引的所需信息，包括空间索引的类型、叶结点个数、图幅字段、图幅宽高和多级网格的大小等信息。\n    "

    def __init__(self, index_type=None):
        """
        构造数据集空间索引信息类。

        :param index_type: 数据集空间索引类型
        :type index_type:  SpatialIndexType or str
        """
        self._type = None
        self._leaf_object_count = None
        self._grid_center = None
        self._grid_size0 = None
        self._grid_size1 = None
        self._grid_size2 = None
        self._tile_height = None
        self._tile_width = None
        self._quad_level = None
        self.set_type(index_type)

    @property
    def type(self):
        """ SpatialIndexType: 空间索引的类型"""
        return self._type

    @property
    def leaf_object_count(self):
        """int: R 树空间索引中叶结点的个数 """
        return self._leaf_object_count

    @property
    def grid_center(self):
        """Point2D:  网格索引的中心点。一般为数据集的中心点。"""
        return self._grid_center

    @property
    def grid_size0(self):
        """float:  多级网格索引的第一层网格的大小"""
        return self._grid_size0

    @property
    def grid_size1(self):
        """float: 多级网格索引的第二层网格的大小 """
        return self._grid_size1

    @property
    def grid_size2(self):
        """float: 多级网格索引的第三层网格的大小"""
        return self._grid_size2

    @property
    def tile_height(self):
        """float: 空间索引的图幅高度"""
        return self._tile_height

    @property
    def tile_width(self):
        """float: 空间索引的图幅宽度"""
        return self._tile_width

    @property
    def quad_level(self):
        """int: 四叉树索引的层级"""
        return self._quad_level

    @staticmethod
    def make_qtree(level):
        """
        构建四叉树索引信息。
        四叉树索引。四叉树是一种重要的层次化数据集结构，主要用来表达二维坐标下空间层次关系，实际上它是一维二叉树在二维空间的扩展。那么，四叉树索引
        就是将一张地图四等分，然后再每一个格子中再四等分，逐层细分，直至不能再分。现在在 SuperMap 中四叉树最多允许分成13层。基于希尔伯特
        （Hilbert）编码的排序规则，从四叉树中可确定索引类中每个对象实例的被索引属性值是属于哪个最小范围。从而提高了检索效率

        :param int level: 四叉树的层级，最大为13级
        :return: 四叉树索引信息
        :rtype: SpatialIndexInfo
        """
        return SpatialIndexInfo().set_type(SpatialIndexType.QTREE).set_quad_level(level)

    @staticmethod
    def make_tile(tile_width, tile_height):
        """
        构建图幅索引信息。
        在 SuperMap 中根据数据集的某一属性字段或根据给定的一个范围，将空间对象进行分类，通过索引进行管理已分类的空间对象，以此提高查询检索速度

        :param float tile_width: 图幅宽度
        :param float tile_height: 图幅高度
        :return: 图幅索引信息
        :rtype: SpatialIndexInfo
        """
        return SpatialIndexInfo().set_type(SpatialIndexType.TILE).set_tile_width(tile_width).set_tile_height(tile_height)

    @staticmethod
    def make_rtree(leaf_object_count):
        """
        构建 R 树索引信息。
        R 树索引是基于磁盘的索引结构，是 B 树(一维)在高维空间的自然扩展，易于与现有数据库系统集成，能够支持各种类型的空间查询处理操作，在实践中得
        到了广泛的应用，是目前最流行的空间索引方法之一。R 树空间索引方法是设计一些包含空间对象的矩形，将一些空间位置相近的目标对象，包含在这个矩形
        内，把这些矩形作为空间索引，它含有所包含的空间对象的指针。

        在进行空间检索的时候，首先判断哪些矩形落在检索窗口内，再进一步判断哪些目标是被检索的内容。这样可以提高检索速度。

        :param int leaf_object_count: R 树空间索引中叶结点的个数
        :return: R 树索引信息
        :rtype: SpatialIndexInfo
        """
        return SpatialIndexInfo().set_type(SpatialIndexType.QTREE).set_leaf_object_count(leaf_object_count)

    @staticmethod
    def make_mgrid(center, grid_size0, grid_size1, grid_size2):
        """
        构建多级网格索引

        多级网格索引，又叫动态索引。
        多级网格索引结合了 R 树索引与四叉树索引的优点，提供非常好的并发编辑支持，具有很好的普适性。若不能确定数据适用于哪种空间索引，可为其建立多级
        网格索引。采用划分多层网格的方式来组织管理数据。网格索引的基本方法是将数据集按照一定的规则划分成相等或不相等的网格，记录每一个地理对象所占的
        网格位置。在 GIS 中常用的是规则网格。当用户进行空间查询时，首先计算出用户查询对象所在的网格，通过该网格快速查询所选地理对象，可以优化查询操作。

        :param Point2D center: 指定的网格中心点
        :param float grid_size0: 一级网格的大小。单位与数据集同
        :param float grid_size1: 二级网格的大小。单位与数据集同
        :param float grid_size2: 三级网格的大小。单位与数据集同
        :return: 多级网格索引信息
        :rtype: SpatialIndexInfo
        """
        return SpatialIndexInfo().set_type(SpatialIndexType.MULTI_LEVEL_GRID).set_grid_center(center).set_grid_size0(grid_size0).set_grid_size1(grid_size1).set_grid_size2(grid_size2)

    def set_quad_level(self, value):
        """
        设置四叉树索引的层级，最大值为13

        :param int value: 四叉树索引的层级
        :return: self
        :rtype: SpatialIndexInfo
        """
        self._quad_level = int(value)
        return self

    def set_leaf_object_count(self, value):
        """
        设置 R 树空间索引中叶结点的个数。

        :param int value: R 树空间索引中叶结点的个数
        :return: self
        :rtype: SpatialIndexInfo
        """
        self._leaf_object_count = int(value)
        return self

    def set_grid_size2(self, value):
        """
        设置多级格网索引中第三级格网的大小。

        :param float value:  三级网格的大小。单位与数据集同
        :return: self
        :rtype: SpatialIndexInfo
        """
        self._grid_size2 = float(value)
        return self

    def set_type(self, value):
        """
        设置空间索引类型

        :param value: 空间索引类型
        :type value: SpatialIndexType or str
        :return: self
        :rtype: SpatialIndexInfo
        """
        self._type = SpatialIndexType._make(value)
        return self

    def set_grid_size0(self, value):
        """
        设置多级格网索引中第一级格网的大小。

        :param float value:  多级格网索引中第一级格网的大小。
        :return: self
        :rtype: SpatialIndexInfo
        """
        self._grid_size0 = float(value)
        return self

    def set_tile_height(self, value):
        """
        设置空间索引的图幅高度。单位与数据集范围的单位一致

        :param float value: 空间索引的图幅高度
        :return: self
        :rtype: SpatialIndexInfo
        """
        self._tile_height = float(value)
        return self

    def set_grid_center(self, value):
        """
        设置网格索引的中心点。一般为数据集的中心点。

        :param Point2D value: 网格索引的中心点
        :return: self
        :rtype: SpatialIndexInfo
        """
        self._grid_center = float(value)
        return self

    def set_grid_size1(self, value):
        """
        设置多级网格索引的第二级索引网格的大小。单位与数据集的单位一致

        :param float value: 多级网格索引的第二级索引网格的大小
        :return: self
        :rtype: SpatialIndexInfo
        """
        self._grid_size1 = float(value)
        return self

    def set_tile_width(self, value):
        """
        设置空间索引的图幅宽度。单位与数据集范围的单位一致。

        :param float value: 空间索引的图幅宽度
        :return: self
        :rtype: SpatialIndexInfo
        """
        self._tile_width = float(value)
        return self

    @property
    def _jobject(self):
        java_obj = get_jvm().com.supermap.data.SpatialIndexInfo()
        if self.type is None:
            raise ValueError("The type of SpatialIndexInfo is None")
        elif self.leaf_object_count is not None:
            if self.type == SpatialIndexType.QTREE:
                java_obj.setLeafObjectCount(self.quad_level)
            else:
                java_obj.setLeafObjectCount(self.leaf_object_count)
        if self.grid_size2 is not None:
            java_obj.setGridSize2(self.grid_size2)
        if self.type is not None:
            java_obj.setType(self.type._jobject)
        if self.grid_size0 is not None:
            java_obj.setGridSize0(self.grid_size0)
        if self.tile_height is not None:
            java_obj.setTileHeight(self.tile_height)
        if self.grid_center is not None:
            java_obj.setGridCenter(self.grid_center)
        if self.grid_size1 is not None:
            java_obj.setGridSize1(self.grid_size1)
        if self.tile_width is not None:
            java_obj.setTileWidth(self.tile_width)
        return java_obj

    @staticmethod
    def _from_java_object(java_obj):
        obj = SpatialIndexInfo()
        obj.set_type(SpatialIndexType._make(java_obj.getType().name()))
        if obj.type == SpatialIndexType.QTREE:
            obj.set_quad_level(java_obj.getLeafObjectCount())
        else:
            obj.set_leaf_object_count(java_obj.getLeafObjectCount())
        obj.set_grid_center(java_obj.getGridCenter())
        obj.set_grid_size1(java_obj.getGridSize1())
        obj.set_grid_size2(java_obj.getGridSize2())
        obj.set_tile_height(java_obj.getTileHeight())
        obj.set_tile_width(java_obj.getTileWidth())
        obj.set_grid_size0(java_obj.getGridSize0())
        return obj

    def to_dict(self):
        """
        将当前对象输出到 dict 中

        :rtype: dict
        """
        d = dict()
        if self.type is not None:
            d["type"] = self.type.name
        if self.leaf_object_count is not None:
            d["leaf_object_count"] = self.leaf_object_count
        if self.quad_level is not None:
            d["quad_level"] = self.quad_level
        if self.grid_center is not None:
            d["grid_center"] = self.grid_center
        if self.grid_size1 is not None:
            d["grid_size1"] = self.grid_size1
        if self.grid_size2 is not None:
            d["grid_size2"] = self.grid_size2
        if self.tile_height is not None:
            d["tile_height"] = self.tile_height
        if self.tile_width is not None:
            d["tile_width"] = self.tile_width
        if self.grid_size0 is not None:
            d["grid_size0"] = self.grid_size0
        return d

    @staticmethod
    def make_from_dict(values):
        """
        从 dict 中读取信息构造 SpatialIndexInfo 对象。

        :param dict values:
        :rtype: SpatialIndexInfo
        """
        return SpatialIndexInfo().from_dict(values)

    def from_dict(self, values):
        """
         从 dict 中读取 SpatialIndexInfo 信息

        :param dict values:
        :return: self
        :rtype: SpatialIndexInfo
        """
        if "type" in values.keys():
            self.set_type(values["type"])
        if "leaf_object_count" in values.keys():
            self.set_leaf_object_count(values["leaf_object_count"])
        if "quad_level" in values.keys():
            self.set_quad_level(values["quad_level"])
        if "grid_center" in values.keys():
            self.set_grid_center(values["grid_center"])
        if "grid_size1" in values.keys():
            self.set_grid_size1(values["grid_size1"])
        if "grid_size2" in values.keys():
            self.set_grid_size2(values["grid_size2"])
        if "tile_height" in values.keys():
            self.set_tile_height(values["tile_height"])
        if "tile_width" in values.keys():
            self.set_tile_width(values["tile_width"])
        if "grid_size0" in values.keys():
            self.set_grid_size0(values["grid_size0"])
        return self


class Colors(object):
    __doc__ = "颜色集合类。该类主要作用是提供颜色序列。提供各种渐变色和随机色的生成，以及 SuperMap 预定义渐变色的生成。"

    def __init__(self, seq=None):
        self._values = []
        if seq is not None:
            self.extend(seq)

    def _check_value_is_valid(self, value):
        if isinstance(value, tuple):
            if len(value) != 4 and len(value) != 3:
                raise ValueError("value must be tuple has 4 or 3 items")
        elif isinstance(value, int):
            pass
        else:
            raise ValueError("required tuple have 4 or 3 items or int")

    @property
    def _jobject(self):
        jvm = get_jvm()
        java_obj = jvm.com.supermap.data.Colors()
        for item in self._values:
            java_obj.add(to_java_color(item))

        return java_obj

    @staticmethod
    def _from_java_object(javaColors):
        if javaColors:
            colors = Colors()
            count = javaColors.getCount()
            for i in range(count):
                color = javaColors.get(i)
                colors.append(Color._from_java_object(color))

            return colors

    def append(self, value):
        """
        添加一个颜色值到颜色集合中

        :param value: RGB 颜色值或 RGBA 颜色值
        :type value: tuple[int] or int
        """
        self._check_value_is_valid(value)
        self._values.append(Color.make(value))

    def extend(self, iterable):
        """
        添加一个颜色值的集合

        :param iterable: 颜色值集合
        :type iterable: range[int] or range[tuple]
        """
        return self._values.extend(map((lambda value: Color.make(value)), iterable))

    def insert(self, index, value):
        """
        添加颜色到指定的位置

        :param int  index: 指定的位置
        :param value:  RGB 颜色值或 RGBA 颜色值
        :type value: tuple[int] or int
        """
        self._check_value_is_valid(value)
        return self._values.insert(index, Color.make(value))

    def index(self, value, start=None, end=None):
        """
        返回颜色值的序号

        :param value: RGB 颜色值或 RGBA 颜色值
        :type value: tuple[int] or int
        :param int start: 开始查找位置
        :param int end: 终止查找位置
        :return: 满足条件的颜色值所在的位置
        :rtype: int
        """
        self._check_value_is_valid(value)
        return self._values.index(Color.make(value), start, end)

    def remove(self, value):
        """
        删除指定的颜色值

        :param value: 被删除的颜色值
        :type value: tuple[int] or int
        """
        self._check_value_is_valid(value)
        return self._values.remove(Color.make(value))

    def clear(self):
        """ 清空所有颜色值 """
        self._values.clear()

    def pop(self, index=None):
        """
        删除指定位置的颜色值，并返回颜色值。当 index 为 None 时删除最后一个颜色值

        :param int index: 指定的位置
        :return: 被删除的颜色值
        :rtype: tuple
        """
        return self._values.pop(index)

    def __getitem__(self, key):
        return self._values.__getitem__(key)

    def __setitem__(self, key, value):
        self._check_value_is_valid(value)
        return self._values.__setitem__(key, Color.make(value))

    def __delitem__(self, key):
        return self._values.__delitem__(key)

    def __str__(self):
        return self._values.__str__()

    def __iter__(self):
        return self._values.__iter__()

    def __len__(self):
        return len(self._values)

    def values(self):
        """
        返回所有的颜色值

        :rtype: list[tuple]
        """
        return list(self._values)

    @staticmethod
    def make_gradient(count, gradient_type, reverse=False, gradient_colors=None):
        """
        给定颜色的数量和控制颜色生成一组渐变色，或生成生成系统预定义渐变色。gradient_colors 和 gradient_type 不能同时有效，但 gradient_type 有效时
        会优先使用 gradient_type 生成系统预定义的渐变色。

        :param int count: 要生成的渐变色的颜色总数。
        :param gradient_type: 渐变颜色的类型。
        :type gradient_type:  ColorGradientType or str
        :param bool reverse: 是否反向生成渐变色，即是否从终止色到起始色生成渐变色。仅对 gradient_type 有效时起作用。
        :param Colors gradient_colors: 渐变颜色集。即生成渐变色的控制颜色。
        :return:
        :rtype:
        """
        _type = ColorGradientType._make(gradient_type)
        if _type is None:
            if gradient_colors is None:
                raise ValueError("gradientType and gradientColors have at least one valid.")
        else:
            jvm = get_jvm()
            if _type is None:
                if gradient_colors is not Colors:
                    raise ValueError("gradientColors must be Colors")
                java_obj = jvm.com.supermap.data.Colors.makeGradient(count, to_java_color_array(gradient_colors.values()))
            else:
                java_obj = jvm.com.supermap.data.Colors.makeGradient(count, _type._jobject, reverse)
        return Colors._from_java_object(java_obj)

    @staticmethod
    def make_random(count, colors=None):
        """
        用于生成一定数量的随机颜色。

        :param int count: 间隔色个数
        :param Colors colors: 控制色集合。
        :return: 由间隔色个数和控制色集合生成的随机颜色表。
        :rtype: Colors
        """
        if colors is not None:
            if colors is not Colors:
                raise ValueError("colors must be Colors")
        else:
            jvm = get_jvm()
            if colors is not None:
                java_obj = jvm.com.supermap.data.Colors()
                java_obj.makeRandom(int(count), to_java_color_array(list(colors.values())))
            else:
                java_obj = jvm.com.supermap.jsuperpy.Utils.ColorsMakeRandom(int(count))
        return Colors._from_java_object(java_obj)


class DatasetGridInfo(object):
    __doc__ = "\n    栅格数据集信息类。该类包括了返回和设置栅格数据集的相应的设置信息等，例如栅格数据集的名称、宽度、高度、像素格式、编码方式、存储分块大小和空值等。\n\n    "

    def __init__(self, name=None, width=None, height=None, pixel_format=None, encode_type=None, block_size_option=BlockSizeOption.BS_256):
        """
        构造栅格数据集信息对象

        :param str name: 数据集名称
        :param int width: 数据集的宽度，单位为像素
        :param int height: 数据集的高度，单位为像素
        :param pixel_format: 数据集存储的像素格式
        :type pixel_format: PixelFormat or str
        :param encode_type: 数据集存储的编码方式
        :type encode_type: EncodeType or str
        :param block_size_option: 数据集的像素分块类型
        :type block_size_option:  BlockSizeOption
        """
        self._name = None
        self._block_size_option = None
        self._min_value = None
        self._bounds = None
        self._width = None
        self._encode_type = None
        self._pixel_format = None
        self._no_value = None
        self._height = None
        self._max_value = None
        self.set_name(name).set_width(width).set_height(height).set_pixel_format(pixel_format).set_encode_type(encode_type).set_block_size_option(block_size_option)

    @property
    def name(self):
        """str: 数据集名称"""
        return self._name

    @property
    def block_size_option(self):
        """BlockSizeOption: 数据集的像素分块类型"""
        return self._block_size_option

    @property
    def min_value(self):
        """float: 格数据集栅格行列中的最小值"""
        return self._min_value

    @property
    def bounds(self):
        """Rectangle: 栅格数据集的地理范围."""
        return self._bounds

    @property
    def width(self):
        """int: 栅格数据集的栅格数据的宽度。单位为像素"""
        return self._width

    @property
    def encode_type(self):
        """EncodeType: 返回栅格数据集数据存储时的编码方式。对数据集采用压缩编码方式，可以减少数据存储所占用的空间，降低数据传输时的网络负载和服务器的负载。
        光栅数据支持的编码方式有 DCT，SGL，LZW 或不使用编码方式"""
        return self._encode_type

    @property
    def pixel_format(self):
        """PixelFormat: 栅格数据存储的像素格式。每个象素采用不同的字节进行表示，单位是比特（bit）。"""
        return self._pixel_format

    @property
    def no_value(self):
        """float: 栅格数据集的空值，当此数据集为空值时，用户可采用-9999来表示"""
        return self._no_value

    @property
    def height(self):
        """int:  栅格数据集的栅格数据的高度。单位为像素"""
        return self._height

    @property
    def max_value(self):
        """float: 栅格数据集栅格行列中的最大值"""
        return self._max_value

    def set_name(self, value):
        """
        设置数据集的名称

        :param str value: 数据集名称
        :return: self
        :rtype: DatasetGridInfo
        """
        self._name = value
        return self

    def set_block_size_option(self, value):
        """
        设置数据集的像素分块类型。以正方形方式进行分块存储。其中在进行分块过程中，如果
        栅格数据不足以进行完整地分块，那么采用空格补充完整进行存储。默认值为 BlockSizeOption.BS_256。

        :param value: 栅格数据集的像素分块
        :type value: BlockSizeOption or str
        :return: self
        :rtype: DatasetGridInfo
        """
        self._block_size_option = BlockSizeOption._make(value)
        return self

    def set_no_value(self, value):
        """
        设置栅格数据集的空值，当此数据集为空值时，用户可采用-9999来表示。

        :param float value: 栅格数据集的空值
        :return: self
        :rtype: DatasetGridInfo
        """
        self._no_value = float(value)
        return self

    def set_height(self, value):
        """
        设置栅格数据集的栅格数据的高度。单位为像素。

        :param float value: 栅格数据集的栅格数据的高度
        :return: self
        :rtype: DatasetGridInfo
        """
        self._height = value
        return self

    def set_encode_type(self, value):
        """
        设置格栅格数据集数据存储时的编码方式。对数据集采用压缩编码方式，可以减少数据存储所占用的空间，降低数据传输时的网络负载和服务器的负载。
        光栅数据支持的编码方式有 DCT，SGL，LZW 或不使用编码方式。

        :param value: 栅格数据集数据存储时的编码方式
        :type value: EncodeType or str
        :return: self
        :rtype: DatasetGridInfo
        """
        self._encode_type = EncodeType._make(value)
        return self

    def set_min_value(self, value):
        """
        设置栅格数据集栅格行列中的最小值

        :param float value: 栅格数据集栅格行列中的最小值
        :return: self
        :rtype: DatasetGridInfo
        """
        self._min_value = value
        return self

    def set_max_value(self, value):
        """
        设置栅格数据集栅格行列中的最大值。

        :param float value: 栅格数据集栅格行列中的最大值
        :return: self
        :rtype: DatasetGridInfo
        """
        self._max_value = value
        return self

    def set_width(self, value):
        """
        设置栅格数据集的栅格数据的宽度。单位为像素。

        :param int value: 栅格数据集的栅格数据的宽度。单位为像素。
        :return: self
        :rtype: DatasetGridInfo
        """
        self._width = value
        return self

    def set_bounds(self, value):
        """
        设置栅格数据集的地理范围。

        :param Rectangle value: 栅格数据集的地理范围。
        :return: self
        :rtype: DatasetGridInfo
        """
        self._bounds = value
        return self

    def set_pixel_format(self, value):
        """
        设置栅格数据集的存储的像素格式

        :param value: 栅格数据集的存储的像素格式
        :type value: PixelFormat or str
        :return: self
        :rtype: DatasetGridInfo
        """
        self._pixel_format = PixelFormat._make(value)
        return self

    @property
    def _jobject(self):
        java_obj = get_jvm().com.supermap.data.DatasetGridInfo()
        if self.name is not None:
            java_obj.setName(self.name)
        if self.block_size_option is not None:
            java_obj.setBlockSizeOption(self.block_size_option._jobject)
        if self.no_value is not None:
            java_obj.setNoValue(self.no_value)
        if self.height is not None:
            java_obj.setHeight(self.height)
        if self.encode_type is not None:
            java_obj.setEncodeType(self.encode_type._jobject)
        if self.min_value is not None:
            java_obj.setMinValue(self.min_value)
        if self.max_value is not None:
            java_obj.setMaxValue(self.max_value)
        if self.width is not None:
            java_obj.setWidth(self.width)
        if self.bounds is not None:
            java_obj.setBounds(self.bounds._jobject)
        if self.pixel_format is not None:
            java_obj.setPixelFormat(self.pixel_format._jobject)
        return java_obj

    @staticmethod
    def _from_java_object(java_obj):
        obj = DatasetGridInfo()
        obj.set_name(java_obj.getName())
        obj.set_block_size_option(BlockSizeOption._make(java_obj.getBlockSizeOption().name()))
        obj.set_min_value(java_obj.getMinValue())
        obj.set_bounds(Rectangle._from_java_object(java_obj.getBounds()))
        obj.set_width(java_obj.getWidth())
        obj.set_encode_type(EncodeType._make(java_obj.getEncodeType().name()))
        obj.set_pixel_format(PixelFormat._make(java_obj.getPixelFormat().name()))
        obj.set_no_value(java_obj.getNoValue())
        obj.set_height(java_obj.getHeight())
        obj.set_max_value(java_obj.getMaxValue())
        return obj

    def to_dict(self):
        """
        将当前对象信息输出为 dict

        :rtype: dict
        """
        d = dict()
        if self.name is not None:
            d["name"] = self.name
        if self.block_size_option is not None:
            d["block_size_option"] = self.block_size_option.name
        if self.min_value is not None:
            d["min_value"] = self.min_value
        if self.bounds is not None:
            d["bounds"] = self.bounds
        if self.width is not None:
            d["width"] = self.width
        if self.encode_type is not None:
            d["encode_type"] = self.encode_type.name
        if self.pixel_format is not None:
            d["pixel_format"] = self.pixel_format.name
        if self.no_value is not None:
            d["no_value"] = self.no_value
        if self.height is not None:
            d["height"] = self.height
        if self.max_value is not None:
            d["max_value"] = self.max_value
        return d

    @staticmethod
    def make_from_dict(values):
        """
        从 dict 中读取信息构建 DatasetGridInfo 对象

        :param dict values:
        :rtype: DatasetGridInfo
        """
        return DatasetGridInfo().from_dict(values)

    def from_dict(self, values):
        """
        从 dict 中读取 DatasetGridInfo 信息

        :param dict values:
        :return: self
        :rtype: DatasetGridInfo
        """
        if "name" in values.keys():
            self.set_name(values["name"])
        if "block_size_option" in values.keys():
            self.set_block_size_option(values["block_size_option"])
        if "min_value" in values.keys():
            self.set_min_value(values["min_value"])
        if "bounds" in values.keys():
            self.set_bounds(values["bounds"])
        if "width" in values.keys():
            self.set_width(values["width"])
        if "encode_type" in values.keys():
            self.set_encode_type(values["encode_type"])
        if "pixel_format" in values.keys():
            self.set_pixel_format(values["pixel_format"])
        if "no_value" in values.keys():
            self.set_no_value(values["no_value"])
        if "height" in values.keys():
            self.set_height(values["height"])
        if "max_value" in values.keys():
            self.set_max_value(values["max_value"])
        return self


class DatasetGrid(Dataset):
    __doc__ = "\n    栅格数据集类。栅格数据集类，该类用于描述栅格数据，例如高程数据集和土地利用图。栅格数据采用网格形式组织并使用二维的栅格的像素值来记录数据，每个栅\n    格（cell）代表一个像素要素，栅格值可以描述各种数据信息。栅格数据集中每一个栅格（cell）存储的是表示地物的属性值，属性值可以是土壤类型、密度值、\n    高程、温度、湿度等。\n\n    "

    def __init__(self):
        Dataset.__init__(self)

    def build_pyramid(self, resample_method=None, progress=None):
        """
        给栅格数据创建指定类型的金字塔，目的是提高栅格数据的显示速度。。金字塔只能针对原始的数据进行创建；用户仅能给一个数据集创建一次金字塔，如果想
        再次创建需要将原来创建的金字塔进行删除，当该栅格数据集显示的时候，已创建的金字塔都将被访问。下图所示为不同比例尺下金字塔的建立过程。

        :param resample_method: 建金字塔方法的类型
        :type resample_method: ResamplingMethod or str
        :param function progress: 进度信息处理函数，参考 :py:class:`.StepEvent`
        :return:  创建是否成功，成功返回 True，失败返回 False
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        listener = None
        if progress is not None:
            if safe_start_callback_server():
                try:
                    listener = ProgressListener(progress, "BuildPyramid")
                    self._jobject.addSteppedListener(listener)
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
                self.open()
                if resample_method is not None:
                    result = self._jobject.buildPyramid(ResamplingMethod._make(resample_method)._jobject)
                else:
                    result = self._jobject.buildPyramid()
            except Exception as e:
                try:
                    log_error(e)
                    result = False
                finally:
                    e = None
                    del e

        finally:
            if listener is not None:
                try:
                    self._jobject.removeSteppedListener(listener)
                except Exception as e1:
                    try:
                        log_error(e1)
                    finally:
                        e1 = None
                        del e1

                close_callback_server()

        return result

    def has_pyramid(self):
        """
        栅格数据集是否已创建金字塔。

        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        return self._jobject.getHasPyramid()

    def remove_pyramid(self):
        """
        删除已创建的金字塔

        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        return self._jobject.removePyramid()

    def update_pyramid(self, rect):
        """
        指定范围更新栅格数据集影像金字塔。

        :param Rectangle rect:  更新金字塔的指定影像范围
        :return: 更新成功，返回 True，否则返回 False。
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        return self._jobject.updatePyramid(rect._jobject)

    def build_statistics(self):
        """
        对栅格数据集执行统计操作，返回该栅格数据集的统计结果对象。统计的结果包括栅格数据集的最大值、最小值、均值、中值、众数、稀数、方差、标准差等。

        :return: 包含 最大值、最小值、均值、中值、众数、稀数、方差、标准差 的 dict 对象。其中 dict 中的 key 值:

                - average : 平均值
                - majority : 众数
                - minority : 稀数
                - max : 最大值
                - median : 中值
                - min : 最小值
                - stdDev : 标准差
                - var : 方差
                - is_dirty :  是否为“脏”数据

        :rtype: dict
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        statResult = self._jobject.buildStatistics()
        if statResult is not None:
            result = dict()
            result["average"] = statResult.getAverage()
            result["minority"] = list(statResult.getMinority())
            result["majority"] = list(statResult.getMajority())
            result["max"] = statResult.getMaxValue()
            result["median"] = statResult.getMedianValue()
            result["min"] = statResult.getMinValue()
            result["stdDev"] = statResult.getStdDeviation()
            result["var"] = statResult.getVariance()
            result["is_dirty"] = statResult.isDirty()
            return result
        return

    def build_value_table(self, out_data=None, out_dataset_name=None):
        """
        创建栅格值属性表，其类型为属性表数据集类型TABULAR。
        栅格数据集的像素格式为SINGLE 和 DOUBLE ，无法创建属性表，即调用该方法返回为 None。
        返回属性表数据集含有系统字段和两个记录栅格信息字段，GRIDVALUE 记录栅格值，GRIDCOUNT 记录栅格值对应的像元个数。

        :param out_data: 结果数据集所在的数据源
        :type out_data: Datasource or DatasourceConnectionInfo or str
        :param str out_dataset_name: 结果数据集名称
        :return: 结果数据集或数据集名称
        :rtype: DatasetVector or str
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        elif not self.pixel_format is PixelFormat.DOUBLE:
            if self.pixel_format is PixelFormat.SINGLE:
                raise RuntimeError("Unsupport SINGLE and DOUBLE pixel format dataset")
            if out_data is not None:
                from ._util import get_output_datasource
                ds = get_output_datasource(out_data)
            else:
                ds = self.datasource
            if ds is None:
                log_error("Failed to get output datasource")
                return
            self.open()
            if out_dataset_name is None:
                out_dataset_name = self.name + "_valueTable"
            out_dataset_name = ds.get_available_dataset_name(out_dataset_name)
            try:
                result = self._jobject.buildValueTable(ds._jobject, out_dataset_name)
            except Exception as e:
                try:
                    log_error(e)
                    result = None
                finally:
                    e = None
                    del e

            from ._util import try_close_output_datasource
            if result is not None:
                result_dt = ds[result.getName()]
                if out_data is not None:
                    return try_close_output_datasource(result_dt, ds)
                return result_dt
        else:
            return try_close_output_datasource(None, ds)

    def calculate_extremum(self):
        """
        计算栅格数据集的极值，即最大值和最小值。建议：栅格数据集在一些分析或者操作之后，建议调用此接口，计算一下最大最小值。

        :return: 如果计算成功返回 true，否则返回 false。
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        return self._jobject.calculateExtremum()

    @property
    def block_size_option(self):
        """BlockSizeOption: 数据集的像素分块类型"""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        return BlockSizeOption._make(self._jobject.getBlockSizeOption().name())

    @property
    def clip_region(self):
        """GeoRegion: 栅格数据集的显示区域"""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        return Geometry._from_java_object(self._jobject.getClipRegion())

    def set_clip_region(self, region):
        """
        设置栅格数据集的显示区域。
        当用户设置此方法后，栅格数据集就按照给定的区域进行显示，区域之外的都不显示。

        注意：

         - 当用户所设定的栅格数据集的地理范围（即调用 :py:meth:`set_geo_reference` 方法）与所设定的裁剪区域无重叠区域，栅格数据集不显示。
         - 当重新设置栅格数据集的地理范围，不自动修改栅格数据集的裁剪区域。

        :param region: 栅格数据集的显示区域。
        :type region: GeoRegion or Rectangle
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        if isinstance(region, Rectangle):
            region = region.to_region()
        self._jobject.setClipRegion(region._jobject)

    @property
    def column_block_count(self):
        """
        int: 栅格数据集分块后的所得到的总列数。
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        return self._jobject.getColumnBlockCount()

    @property
    def row_block_count(self):
        """
        int: 栅格数据经过分块后所得到的总行数。
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        return self._jobject.getRowBlockCount()

    @property
    def width(self):
        """int: 栅格数据集的栅格数据的宽度。单位为像素"""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        return self._jobject.getWidth()

    @property
    def height(self):
        """int:  栅格数据集的栅格数据的高度。单位为像素"""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        return self._jobject.getHeight()

    @property
    def max_value(self):
        """float:栅格数据集中栅格值的最大值。"""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        return self._jobject.getMaxValue()

    @property
    def min_value(self):
        """float:栅格数据集中栅格值的最小值"""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        return self._jobject.getMinValue()

    @property
    def no_value(self):
        """float: 栅格数据集的空值，当此数据集为空值时，用户可采用-9999来表示"""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        return self._jobject.getNoValue()

    def set_no_value(self, value):
        """
        设置栅格数据集的空值，当此数据集为空值时，用户可采用-9999来表示

        :param float value: 空值
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        if value is None:
            return
        self.open()
        self._jobject.setNoValue(float(value))

    @property
    def pixel_format(self):
        """PixelFormat: 栅格数据存储的像素格式。每个象素采用不同的字节进行表示，单位是比特（bit）。"""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        return PixelFormat._make(self._jobject.getPixelFormat().name())

    def update(self, dataset):
        """
        根据指定的栅格数据集更新。
        注意：指定的栅格数据集和被更新的栅格数据集的编码方式（EncodeType）和像素类型（PixelFormat）必须保持一致

        :param dataset:  指定的栅格数据集。
        :type dataset: DatasetGrid or str
        :return: 如果更新成功，返回 True，否则返回 False。
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        from ._util import get_input_dataset
        dt = get_input_dataset(dataset)
        if dt is None:
            raise ValueError("Input dataset is None")
        return self._jobject.update(dt._jobject)

    def set_geo_reference(self, rect):
        """
        将栅格数据集对应到地理坐标系中指定的地理范围。

        :param  Rectangle rect: 指定的地理范围
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        rect = Rectangle.make(rect)
        self._jobject.setGeoReference(rect._jobject)

    def get_value(self, col, row):
        """
        根据给定的行数和列数返回栅格数据集的栅格所对应的栅格值。注意：该方法的参数值的行、列数从零开始计数。

        :param int col: 指定的栅格数据集的列。
        :param int row: 指定栅格数据集的行。
        :return: 栅格数据集的栅格所对应的栅格值。
        :rtype: float
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        return self._jobject.getValue(int(col), int(row))

    def set_value(self, col, row, value):
        """
        根据给定的行数和列数设置栅格数据集的栅格所对应的栅格值。注意：该方法的参数值的行、列数从零开始计数。

        :param int col: 指定的栅格数据集的列。
        :param int row: 指定栅格数据集的行。
        :param float value: 指定的栅格数据集的栅格所对应的栅格值。
        :return: 栅格数据集的栅格所对应的修改之前的栅格值。
        :rtype: float
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        if value is None:
            value = self.no_value
        return self._jobject.setValue(int(col), int(row), float(value))

    def grid_to_xy(self, col, row):
        """
        根据指定的行数和列数所对应的栅格点转换为地理坐标系下的点，即 X, Y 坐标。

        :param int col: 指定的列
        :param int row: 指定的行
        :return: 地理坐标系下的对应的点坐标。
        :rtype: Point2D
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        return Point2D._from_java_object(self._jobject.gridToXY(self._jvm.java.awt.Point(int(col), int(row))))

    def xy_to_grid(self, point):
        """
        将地理坐标系下的点（X Y）转换为栅格数据集中对应的栅格。

        :param point: 地理坐标系下的点
        :type point: Point2D
        :return: 栅格数据集对应的栅格，分别返回列和行
        :rtype: tuple[int]
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        point = Point2D.make(point)
        pnt = self._jobject.xyToGrid(point._jobject)
        if pnt is not None:
            return (
             int(pnt.getY()), int(pnt.getX()))
        return

    @property
    def color_table(self):
        """
        Colors: 数据集的颜色表
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        return Colors._from_java_object(self._jobject.getColorTable())

    def set_color_table(self, colors):
        """
        设置数据集的颜色表

        :param Colors colors: 颜色集合
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        self._jobject.setColorTable(colors._jobject)


class DatasetImageInfo(object):
    __doc__ = "\n    影像数据集信息类，该类用于设置影像数据集的创建信息，包括名称、宽度、高度、波段数和存储分块大小等。\n\n    通过该类设置影像数据集的创建信息时，需要注意：\n\n    - 需要指定影像的波段数，波段数可以设置为 0，创建之后可以再向影像中添加波段；\n    - 所有波段被设置为相同的像素格式和编码方式，创建影像成功后，可以根据需求，再为每个波段设置不同的像素格式和其编码类型。\n\n    "

    def __init__(self, name=None, width=None, height=None, pixel_format=None, encode_type=None, block_size_option=BlockSizeOption.BS_256, band_count=None):
        """
        构造影像数据集信息对象

        :param str name: 数据集名称
        :param int width: 数据集的宽度，单位为像素
        :param int height: 数据集的高度，单位为像素
        :param pixel_format: 数据集存储的像素格式
        :type pixel_format: PixelFormat or str
        :param encode_type: 数据集存储的编码方式
        :type encode_type: EncodeType or str
        :param block_size_option: 数据集的像素分块类型
        :type block_size_option:  BlockSizeOption
        :param int band_count: 波段数目
        """
        self._name = None
        self._block_size_option = None
        self._bounds = None
        self._width = None
        self._encode_type = None
        self._pixel_format = None
        self._height = None
        self._band_count = None
        self.set_name(name).set_width(width).set_height(height).set_pixel_format(pixel_format).set_encode_type(encode_type).set_block_size_option(block_size_option).set_band_count(band_count)

    @property
    def name(self):
        """str: 数据集名称"""
        return self._name

    @property
    def block_size_option(self):
        """BlockSizeOption: 数据集的像素分块类型"""
        return self._block_size_option

    @property
    def bounds(self):
        """Rectangle: 影像数据集的地理范围."""
        return self._bounds

    @property
    def width(self):
        """int: 影像数据集的影像数据的宽度。单位为像素"""
        return self._width

    @property
    def encode_type(self):
        """EncodeType: 返回影像数据集数据存储时的编码方式。对数据集采用压缩编码方式，可以减少数据存储所占用的空间，降低数据传输时的网络负载和服务器的负载。
        光栅数据支持的编码方式有 DCT，SGL，LZW 或不使用编码方式"""
        return self._encode_type

    @property
    def pixel_format(self):
        """PixelFormat: 影像数据存储的像素格式。每个象素采用不同的字节进行表示，单位是比特（bit）。"""
        return self._pixel_format

    @property
    def height(self):
        """int:  影像数据集的影像数据的高度。单位为像素"""
        return self._height

    @property
    def band_count(self):
        """int: 波段数目"""
        return self._band_count

    def set_name(self, value):
        """
        设置数据集的名称

        :param str value: 数据集名称
        :return: self
        :rtype: DatasetImageInfo
        """
        if value is not None:
            self._name = value
        return self

    def set_block_size_option(self, value):
        """
        设置数据集的像素分块类型。以正方形方式进行分块存储。其中在进行分块过程中，如果果影像数据不足以进行完整地分块，那么采用空格补充完整进行存储。默认值为 BlockSizeOption.BS_256。

        :param value: 影像数据集的像素分块
        :type value: BlockSizeOption or str
        :return: self
        :rtype: DatasetImageInfo
        """
        if value is not None:
            self._block_size_option = BlockSizeOption._make(value)
        return self

    def set_pixel_format(self, value):
        """
        设置影像数据集的存储的像素格式。影像数据集不支持 DOUBLE、SINGLE、BIT64 类型的像素格式。

        :param value: 影像数据集的存储的像素格式
        :type value: PixelFormat or str
        :return: self
        :rtype: DatasetImageInfo
        """
        if value is not None:
            self._pixel_format = PixelFormat._make(value)
        return self

    def set_bounds(self, value):
        """
        设置影像数据集的地理范围。

        :param Rectangle value: 影像数据集的地理范围。
        :return: self
        :rtype: DatasetImageInfo
        """
        if value is not None:
            self._bounds = value
        return self

    def set_height(self, value):
        """
        设置影像数据集的影像数据的高度。单位为像素。

        :param int value: 影像数据集的影像数据的高度。单位为像素。
        :return: self
        :rtype: DatasetImageInfo
        """
        if value is not None:
            self._height = int(value)
        return self

    def set_width(self, value):
        """
        设置影像数据集的影像数据的宽度。单位为像素。

        :param int value: 影像数据集的影像数据的宽度。单位为像素。
        :return: self
        :rtype: DatasetImageInfo
        """
        if value is not None:
            self._width = int(value)
        return self

    def set_band_count(self, value):
        """
        设置影像数据集的波段数目。创建影像数据集时，波段数可以设置为 0，此时，像素格式（pixel_format）和编码格式（encode_type）的设置是无效的
        ，因为这些信息是针对波段而言，因此波段为 0 时无法保存。此影像数据集的像素格式和编码格式，将以向其中添加的第一个波段的相关信息为准。

        :param int value: 波段数目。
        :return: self
        :rtype: DatasetImageInfo
        """
        if value is not None:
            self._band_count = int(value)
        return self

    def set_encode_type(self, value):
        """
        设置影像数据集数据存储时的编码方式。对数据集采用压缩编码方式，可以减少数据存储所占用的空间，降低数据传输时的网络负载和服务器的负载。
        光栅数据支持的编码方式有 DCT，SGL，LZW 或不使用编码方式。

        :param value: 像数据集数据存储时的编码方式
        :type value: EncodeType or str
        :return: self
        :rtype: DatasetImageInfo
        """
        if value is not None:
            self._encode_type = EncodeType._make(value)
        return self

    @property
    def _jobject(self):
        java_obj = get_jvm().com.supermap.data.DatasetImageInfo()
        if self.band_count is not None:
            java_obj.setBandCount(self.band_count)
        if self.name is not None:
            java_obj.setName(self.name)
        if self.block_size_option is not None:
            java_obj.setBlockSizeOption(self.block_size_option._jobject)
        if self.pixel_format is not None:
            java_obj.setPixelFormat(self.pixel_format._jobject)
        if self.bounds is not None:
            java_obj.setBounds(self.bounds._jobject)
        if self.height is not None:
            java_obj.setHeight(int(self.height))
        if self.width is not None:
            java_obj.setWidth(int(self.width))
        if self.encode_type is not None:
            java_obj.setEncodeType(self.encode_type._jobject)
        return java_obj

    @staticmethod
    def _from_java_object(java_obj):
        obj = DatasetImageInfo()
        obj.set_name(java_obj.getName())
        obj.set_block_size_option(BlockSizeOption._make(java_obj.getBlockSizeOption().name()))
        obj.set_pixel_format(PixelFormat._make(java_obj.getPixelFormat().name()))
        obj.set_encode_type(EncodeType._make(java_obj.getEncodeType().name()))
        obj.set_band_count(java_obj.getBandCount())
        obj.set_bounds(Rectangle._from_java_object(java_obj.getBounds()))
        obj.set_width(java_obj.getWidth())
        obj.set_height(java_obj.getHeight())
        return obj

    def to_dict(self):
        """
        将当前对象信息输出为 dict

        :rtype: dict
        """
        d = dict()
        if self.name is not None:
            d["name"] = self.name
        if self.block_size_option is not None:
            d["block_size_option"] = self.block_size_option.name
        if self.pixel_format is not None:
            d["pixel_format"] = self.pixel_format.name
        if self.encode_type is not None:
            d["encode_type"] = self.encode_type.name
        if self.band_count is not None:
            d["band_count"] = self.band_count
        if self.bounds is not None:
            d["bounds"] = self.bounds
        if self.width is not None:
            d["width"] = self.width
        if self.height is not None:
            d["height"] = self.height
        return d

    @staticmethod
    def make_from_dict(values):
        """
        从 dict 中读取信息构建 DatasetImageInfo 对象

        :param dict values:
        :rtype: DatasetImageInfo
        """
        return DatasetImageInfo().from_dict(values)

    def from_dict(self, values):
        """
        从 dict 中读取 DatasetImageInfo 信息

        :param dict values:
        :return: self
        :rtype: DatasetImageInfo
        """
        if "name" in values.keys():
            self.set_name(values["name"])
        if "block_size_option" in values.keys():
            self.set_block_size_option(values["block_size_option"])
        if "pixel_format" in values.keys():
            self.set_pixel_format(values["pixel_format"])
        if "encode_type" in values.keys():
            self.set_encode_type(values["encode_type"])
        if "band_count" in values.keys():
            self.set_band_count(values["band_count"])
        if "bounds" in values.keys():
            self.set_bounds(values["bounds"])
        if "width" in values.keys():
            self.set_width(values["width"])
        if "height" in values.keys():
            self.set_height(values["height"])
        return self


class DatasetImage(Dataset):
    __doc__ = "\n    影像数据集类。 影像数据集类，该类用于描述影像数据，不具备属性信息，例如影像地图、多波段影像和实物地图等。 光栅数据采用网格形式组织并使用二维栅格\n    的像素值来记录数据，每个栅格（cell）代表一个像素要素，栅格值可以描述各种数据信息。影像数据集中每一个栅格存储的是一个颜色值或颜色的索引值（RGB 值）。\n\n    "

    def __init__(self):
        Dataset.__init__(self)

    def build_pyramid(self, progress=None):
        """
        给影像数据集创建金字塔。目的是提高影像数据集的显示速度。金字塔只能针对原始的数据进行创建；一次仅能给一个数据集创建金字塔，当显示该影像数据集的
        时候，已创建的金字塔都将被访问。

        :param function progress: 进度信息处理函数，参考 :py:class:`.StepEvent`
        :return:  创建是否成功，成功返回 True，失败返回 False
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        listener = None
        if progress is not None:
            if safe_start_callback_server():
                try:
                    listener = ProgressListener(progress, "BuildPyramid")
                    self._jobject.addSteppedListener(listener)
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
                self.open()
                result = self._jobject.buildPyramid()
            except Exception as e:
                try:
                    log_error(e)
                    result = False
                finally:
                    e = None
                    del e

        finally:
            if listener is not None:
                try:
                    self._jobject.removeSteppedListener(listener)
                except Exception as e1:
                    try:
                        log_error(e1)
                    finally:
                        e1 = None
                        del e1

                close_callback_server()

        return result

    def has_pyramid(self):
        """
        影像数据集是否已创建金字塔。

        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        return self._jobject.getHasPyramid()

    def remove_pyramid(self):
        """
        影像已创建的金字塔

        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        return self._jobject.removePyramid()

    def update_pyramid(self, rect):
        """
        指定范围更新影像数据集影像金字塔。

        :param Rectangle rect:  更新金字塔的指定影像范围
        :return: 更新成功，返回 True，否则返回 False。
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        rc = Rectangle.make(rect)
        return self._jobject.updatePyramid(rc._jobject)

    def build_statistics(self):
        """
        对影像数据集执行统计操作，返回该影像数据集的统计结果对象。统计的结果包括影像数据集的最大值、最小值、均值、中值、众数、稀数、方差、标准差等。

        :return: 返回一个dict，dict中包含每个波段的统计结果，统计结果为包含最大值、最小值、均值、中值、众数、稀数、方差、标准差 的 dict 对象。其中 dict 中的 key 值:

                - average : 平均值
                - majority : 众数
                - minority : 稀数
                - max : 最大值
                - median : 中值
                - min : 最小值
                - stdDev : 标准差
                - var : 方差
                - is_dirty :  是否为“脏”数据

        :rtype: dict[dict]
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        statResult = self._jobject.buildStatistics()
        if statResult is not None:
            statResults = OrderedDict()
            for item, value in statResult.items():
                result = dict()
                result["average"] = value.getAverage()
                result["majority"] = list(value.getMajority())
                result["minority"] = list(value.getMinority())
                result["max"] = value.getMaxValue()
                result["median"] = value.getMedianValue()
                result["min"] = value.getMinValue()
                result["stdDev"] = value.getStdDeviation()
                result["var"] = value.getVariance()
                result["is_dirty"] = value.isDirty()
                statResults[item] = result

            return statResults
        return

    def calculate_extremum(self, band=0):
        """
        计算影像数据指定波段的极值，即最大值和最小值。

        :param int band:  要计算极值的影像数据的波段序号。
        :return: 如果计算成功返回 true，否则返回 false。
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        return self._jobject.calculateExtremum(int(band))

    @property
    def block_size_option(self):
        """BlockSizeOption: 数据集的像素分块类型"""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        return BlockSizeOption._make(self._jobject.getBlockSizeOption().name())

    @property
    def clip_region(self):
        """GeoRegion: 影像数据集的显示区域"""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        return Geometry._from_java_object(self._jobject.getClipRegion())

    def set_clip_region(self, region):
        """
        设置影像数据集的显示区域。
        当用户设置此方法后，影像格数据集就按照给定的区域进行显示，区域之外的都不显示。

        注意：

        - 当用户所设定的影像数据集的地理范围（即调用 :py:meth:`set_geo_reference` 方法）与所设定的裁剪区域无重叠区域，影像数据集不显示。
        - 当重新设置影像数据集的地理范围，不自动修改影像数据集的裁剪区域。

        :param region: 影像数据集的显示区域。
        :type region: GeoRegion or Rectangle
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        if isinstance(region, Rectangle):
            region = region.to_region()
        self._jobject.setClipRegion(region._jobject)

    @property
    def width(self):
        """int: 影像数据集的影像数据的宽度。单位为像素"""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        return self._jobject.getWidth()

    @property
    def height(self):
        """int:  影像数据集的影像数据的高度。单位为像素"""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        return self._jobject.getHeight()

    def get_max_value(self, band=0):
        """
        获取影像数据集指定波段的最大像素值

        :param int band: 指定的波段索引号，从 0 开始。
        :return: 影像数据集指定波段的最大像素值
        :rtype: float
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        return self._jobject.getMaxValue(int(band))

    def get_min_value(self, band=0):
        """
        获取影像数据集指定波段的最小像素值

        :param int band: 指定的波段索引号，从 0 开始。
        :return: 影像数据集指定波段的最小像素值
        :rtype: float
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        return self._jobject.getMinValue(int(band))

    def get_no_value(self, band=0):
        """
        返回影像数据集指定波段的无值。

        :param int band: 指定的波段索引号，从 0 开始
        :return: 影像数据集中指定波段的无值
        :rtype: float
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        return self._jobject.getNoData(int(band))

    def set_no_value(self, value, band):
        """
        设置影像数据集指定波段的无值。

        :param float value: 指定的无值。
        :param int band: 指定的波段索引号，从 0 开始。
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        if value is not None:
            self.open()
            return self._jobject.setNoData(float(value), int(band))
        return False

    def get_pixel_format(self, band):
        """
        返回影像数据集指定波段的像素格式。

        :param int band: 指定的波段索引号，从 0 开始。
        :return: 影像数据集指定波段的像素格式。
        :rtype: PixelFormat
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        return PixelFormat._make(self._jobject.getPixelFormat(int(band)).name())

    def update(self, dataset):
        """
        根据指定的影像数据集更新。
        注意：指定的影像数据集和被更新的影像数据集的编码方式（EncodeType）和像素类型（PixelFormat）必须保持一致。

        :param dataset: 指定的影像数据集。
        :type dataset: DatasetImage or str
        :return: 如果更新成功，返回 True，否则返回 False。
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        from ._util import get_input_dataset
        dt = get_input_dataset(dataset)
        if dt is None:
            raise ValueError("Input dataset is None")
        return self._jobject.update(dt._jobject)

    def set_geo_reference(self, rect):
        """
        将影像数据集对应到地理坐标系中指定的地理范围。

        :param  Rectangle rect: 指定的地理范围
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        rect = Rectangle.make(rect)
        self._jobject.setGeoReference(rect._jobject)

    def get_value(self, col, row, band):
        """
        根据给定的行数和列数返回影像数据集的栅格所对应的像素值。注意：该方法的参数值的行、列数从零开始计数。

        :param int col: 指定的影像数据集的列。
        :param int row: 指定的影像数据集的行。
        :param int band: 指定的波段数
        :return: 影像数据集中所对应的像素值。
        :rtype: float or tuple
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        value = self._jobject.getValue(int(col), int(row), int(band))
        pix = self.get_pixel_format(band)
        if pix == PixelFormat.RGBA or pix == PixelFormat.RGB:
            return color_to_tuple(value)
        return value

    def set_value(self, col, row, value, band):
        """
        根据给定的行数和列数设置影像数据集的所对应的像素值。注意：该方法的参数值的行、列数从零开始计数。

        :param int col: 指定的影像数据集的列。
        :param int row: 指定的影像数据集的行。
        :param value: 指定的影像数据集的所对应的像素值。
        :type value: tuple or float
        :param int band: 指定的波段序号
        :return: 影像数据集中所对应的修改之前的像素值。
        :rtype: float
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        if value is None:
            value = self.get_no_value(band)
        value = tuple_to_color(value)
        old_value = self._jobject.setValue(int(col), int(row), float(value), int(band))
        pix = self.get_pixel_format(band)
        if pix == PixelFormat.RGBA or pix == PixelFormat.RGB:
            return color_to_tuple(old_value)
        return old_value

    def image_to_xy(self, col, row):
        """
        根据指定的行数和列数所对应的影像点转换为地理坐标系下的点，即 X, Y 坐标。

        :param int col: 指定的列
        :param int row: 指定的行
        :return: 地理坐标系下的对应的点坐标。
        :rtype: Point2D
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        return Point2D._from_java_object(self._jobject.imageToXY(self._jvm.java.awt.Point(int(col), int(row))))

    def xy_to_image(self, point):
        """
        将地理坐标系下的点（X Y）转换为影像数据集中对应的像素值。

        :param point: 地理坐标系下的点
        :type point: Point2D
        :return: 影像数据集对应的影像点
        :rtype: tuple[int]
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        point = Point2D.make(point)
        pnt = self._jobject.xyToImage(point._jobject)
        return (int(pnt.getX()), int(pnt.getY()))

    def get_palette(self, band=0):
        """
        获取影像数据集指定波段的颜色调色板

        :param int band:  指定的波段索引号，从 0 开始。
        :return: 影像数据集指定波段的颜色调色板
        :rtype: Colors
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        return Colors._from_java_object(self._jobject.getPalette(int(band)))

    def set_palette(self, colors, band):
        """
        设置影像数据集指定波段的颜色调色板

        :param Colors colors: 颜色调色板。
        :param int band:  指定的波段索引号，从 0 开始。
        """
        if self._jobject is None:
            log_error("DatasetVector object has been disposed")
            return
        self.open()
        self._jobject.setPalette(colors._jobject, int(band))

    def add_band(self, datasets, indexes=None):
        """
        向指定的多波段影像数据集中按照指定的索引追加多个波段

        :param datasets: 影像数据集合
        :type datasets: list[DatasetImage] or DatasetImage
        :param indexes:  要追加的波段索引，当输入的是单个 DatasetImage 数据才有效。
        :type indexes: list[int]
        :return: 添加的波段个数
        :rtype: int
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        else:
            self.open()
            if isinstance(datasets, DatasetImage):
                if indexes is not None:
                    return self._jobject.addBand(datasets._jobject, to_java_int_array(indexes))
                return self._jobject.addBand(datasets._jobject)
            else:
                if isinstance(datasets, (list, tuple)):
                    if len(datasets) == 1:
                        return self.add_band(datasets[0], indexes)
                    from ._util import to_java_datasetimage_array
                    return self._jobject.addBand(to_java_datasetimage_array(datasets))
            raise ValueError("datasets is invalid, required DatasetImage or DatasetImage list")

    def delete_band(self, start_index, count=1):
        """
        根据指定索引号删除某个波段

        :param int start_index: 指定删除波段的开始索引号。
        :param int count:  要删除的波段的个数。
        :return: 删除成功返回 true；否则返回 false。
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        if int(count) < 1:
            raise ValueError("invalid count, required greater with 0, but now is " + str(count))
        return self._jobject.deleteBand(int(start_index), count)

    def get_band_name(self, band):
        """
        返回指定序号的波段的名称。

        :param int band: 波段序号
        :return: 波段名称
        :rtype: str
        """
        if self._jobject is None:
            log_error("DatasetVector object has been disposed")
            return
        self.open()
        return self._jobject.get(int(band))

    def set_band_name(self, band, name):
        """
        设置指定序号的波段的名称。

        :param int band:  波段序号
        :param str name: 波段名称
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        return self._jobject.set(int(band), str(name))

    def get_band_index(self, name):
        """
        获取指定波段名称所在的序号

        :param str name: 波段名称
        :return: 波段所在的序号
        :rtype: int
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        return self._jobject.indexOf(str(name))

    @property
    def band_count(self):
        """int: 返回波段数目"""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        self.open()
        return self._jobject.getBandCount()


class DatasetVolume(Dataset):

    def __init__(self):
        Dataset.__init__(self)


class DatasetTopology(Dataset):

    def __init__(self):
        Dataset.__init__(self)


class DatasetMosaic(Dataset):
    __doc__ = "\n    镶嵌数据集。用于高效管理和显示海量影像数据。 如今，影像的获取已越来越便捷、高效，针对海量影像的管理、服务发布的需求也越来越普遍。为了更便捷高效地\n    完成这一工作，SuperMap GIS提供了基于镶嵌数据集的解决方案。镶嵌数据集采用元数据+原始影像文件的方式进行管理。把影像数据添加到镶嵌数据集时，只会\n    在镶嵌数据集中记录影像文件的路径、轮廓、分辨率等元信息，在使用时才会根据元信息加载所需的影像文件。该模式相比传统的入库管理方式，大大提升了入库的\n    速度，同时也减少了磁盘的占用。\n    "

    def __init__(self):
        Dataset.__init__(self)

    @property
    def bound_count(self):
        """int: 镶嵌数据集波段数"""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        return self._jobject.getBandCount()

    @property
    def pixel_format(self):
        """PixelFormat: 镶嵌数据集的位深"""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        pixel = self._jobject.getPixelFormat()
        if pixel is not None:
            return PixelFormat._make(pixel.name())

    @property
    def boundary_dataset(self):
        """DatasetVector: 镶嵌数据集的边界子数据集"""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            return Dataset._from_java_object(self._jobject.getBoundaryDataset(), self.datasource)
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    @property
    def clip_dataset(self):
        """DatasetVector: 镶嵌数据集的裁剪子数据集"""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            return Dataset._from_java_object(self._jobject.getClipDataset(), self.datasource)
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    @property
    def footprint_dataset(self):
        """DatasetVector: 镶嵌数据集的轮廓子数据集"""
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            self.open()
            return Dataset._from_java_object(self._jobject.getFootprintDataset(), self.datasource)
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def list_files(self):
        """
        获取镶嵌数据集的所有栅格文件

        :return: 镶嵌数据集的所有栅格文件
        :rtype: list[str]
        """
        return self.footprint_dataset.get_field_values("SmPath")["SmPath"]

    def build_pyramid(self, resample_type=PyramidResampleType.NONE, is_skip_exists=True):
        """
        为镶嵌数据集中的所有影像创建影像金字塔。

        :param resample_type: 金字塔重采样方式
        :type resample_type: PyramidResampleType or str
        :param bool is_skip_exists: 一个布尔值，指示如果影像已经创建了金字塔是否忽略，True 表示忽略，即不再重新创建金字塔；False 表示对已经
                                    创建金字塔的影像重新创建金字塔。
        :return: 成功创建返回 True；否则返回 False
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        try:
            from .._utils import parse_bool
            self.open()
            resample_type = PyramidResampleType._make(resample_type, "NONE")
            return self._jobject.buildPyramid(oj(resample_type), parse_bool(is_skip_exists))
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

        return False

    def add_files(self, directory_paths, extension=None, clip_file_extension=None):
        """
        向镶嵌数据集中添加影像，实质是将给定路径下的指定扩展名的所有影像的文件名添加并记录，即镶嵌数据集并没有对影像文件进行拷贝入库，只是记录了影像的全路径（绝对路径）信息。

        :param directory_paths: 指定添加影像的路径，即要添加的影像所在的文件夹路径（绝对路径）或 要添加的多个影像文件的全路径（绝对路径）列表。
        :type directory_paths: str or list[str]
        :param extension: 影像文件的扩展名，当 directory_paths 为文件夹路径时（即 directory_paths 类型为 str 时），用来过滤文件夹内影像文件。
                                         当 directory_paths 类型为 list 时，该参数不生效。
        :type extension: str
        :param clip_file_extension:裁剪形状文件的后缀名，如.shp，该文件中的对象将作为该影像的裁剪显示范围。影像的裁剪显示一般用于：
                                   当影像经过校正后产生无值区域，通过裁剪形状绘制影像的有效值区域，经过裁剪显示后达到去除无值区域的目的。
                                   另外，影像与裁剪形状是一一对应的关系，因此，裁剪形状文件必须存储在 directory_path 参数指定的路径下，
                                   即裁剪形状文件与影像文件在同一目录下。
        :type clip_file_extension: str
        :return: 添加影像是否成功，True表示成功；False表示失败。
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError(type(self).__name__)
        elif clip_file_extension is not None:
            if not isinstance(clip_file_extension, str):
                raise TypeError("clip_file_extension must be string, but now is " + str(type(clip_file_extension)))
        try:
            if isinstance(directory_paths, str):
                if not isinstance(extension, str):
                    raise TypeError("extension must be string, but now is " + str(type(extension)))
                self.open()
                return self._jobject.addFiles(directory_paths, extension, clip_file_extension)
            if isinstance(directory_paths, list):
                if extension is not None:
                    log_warning("The type of directory_paths is list, arg extension is invalid!")
                self.open()
                return self._jobject.addFiles(to_java_string_array(directory_paths), clip_file_extension)
            raise TypeError("directory_paths must be string or list, but now is " + str(type(directory_paths)))
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

        return False


class DatasetUnsupported(Dataset):

    def __init__(self):
        Dataset.__init__(self)


def combine_band(red_dataset, green_dataset, blue_dataset, out_data=None, out_dataset_name=None):
    """
    三个单波段数据集合成RGB数据集

    :param red_dataset:  单波段数据集R。
    :type red_dataset: Dataset or str
    :param green_dataset: 单波段数据集G
    :type green_dataset: Dataset or str
    :param blue_dataset: 单波段数据集B
    :type blue_dataset: Dataset or str
    :param out_data: 结果数据集所在的数据源，为空时使用 red_dataset 数据集所在的数据源
    :type out_data: Datasource or DatasourceConnectionInfo or str
    :param str out_dataset_name:  合成RGB数据集的名称。
    :return: 合成成功返回数据集对象或数据集名称，失败返回 None
    :rtype: Dataset
    """
    from ._util import get_input_dataset, get_output_datasource, check_output_datasource, try_close_output_datasource
    try:
        _red_data = get_input_dataset(red_dataset)
        if _red_data is None:
            raise ValueError("source red_dataset is None")
        else:
            _green_data = get_input_dataset(green_dataset)
            if _green_data is None:
                raise ValueError("source green_dataset is None")
            else:
                _blue_data = get_input_dataset(blue_dataset)
                if _blue_data is None:
                    raise ValueError("source blue_dataset is None")
                elif out_data is not None:
                    out_datasource = get_output_datasource(out_data)
                    check_output_datasource(out_datasource)
                else:
                    out_datasource = red_dataset.datasource
                if out_dataset_name is None:
                    _out_dataset_name = "CombineDataset"
                else:
                    _out_dataset_name = out_dataset_name
            _out_dataset_name = out_datasource.get_available_dataset_name(_out_dataset_name)
            result = get_jvm().com.supermap.data.Toolkit.CombineBand(_out_dataset_name, out_datasource._jobject, _red_data._jobject, _green_data._jobject, _blue_data._jobject)
            if result:
                result_dt = out_datasource[_out_dataset_name]
            else:
                result_dt = None
        if out_data is not None:
            return try_close_output_datasource(result_dt, out_datasource)
        return result_dt
    except:
        import traceback
        traceback.print_exc()


class Recordset(JVMBase):
    __doc__ = "\n    记录集类。 通过此类，可以实现对矢量数据集中的数据进行操作。 数据源有文件型和数据库型，数据库型数据中空间几何信息和属性信息一体化存储，一个矢量数\n    据集对应一个 DBMS 表，其几何形状以及属性信息都一体化存储其中，表中的几何字段存储要素的空间几何信息。对于矢量数据集中的纯属性数据集，其中没有几\n    何字段，记录集为 DBMS 表的一个子集；而在文件型数据中空间几何信息和属性信息是分别存储的，记录集的应用可能比较让人费解，实际上，操作时是屏蔽掉文\n    件型和数据库型数据的区别，将数据都看成是一个空间信息和属性信息一体化存储的表，而记录集是从其中取出的用来操作的一个子集。记录集中的一条记录，即一\n    行，对应着一个要素，包含该要素的空间几何信息和属性信息。记录集中的一列对应一个字段的信息。\n\n    记录集可以直接从矢量数据集中获得一个记录集，有两种方法：用户可以通过 :py:meth:`DatasetVector.get_recordset` 方法直接从矢量数据集中返回\n    记录集，也可以通过查询语句返回记录集，所不同的是前者得到的记录集包含该类集合的全部空间几何信息和属性信息，而后者得到的是经过查询语句条件过滤的记录集。\n\n    以下代码演示从记录集中读取数据以及批量写入数据到新的记录集中::\n\n    >>> dt = Datasource.open('E:/data.udb')['point']\n    >>> rd = dt.query_with_filter('SmID < 100 or SmID > 1000', 'STATIC')\n    >>> all_points = []\n    >>> while rd.has_next():\n    >>>     geo = rd.get_geometry()\n    >>>     all_points.append(geo.point)\n    >>>     rd.move_next()\n    >>> rd.close()\n    >>>\n    >>> new_dt = dt.datasource.create_vector_dataset('new_point', 'Point', adjust_name=True)\n    >>> new_dt.create_field(FieldInfo('object_time', FieldType.DATETIME))\n    >>> new_rd = new_dt.get_recordset(True)\n    >>> new_rd.batch_edit()\n    >>> for point in all_points:\n    >>>     new_rd.add(point, {'object_time': datetime.datetime.now()} )\n    >>> new_rd.batch_update()\n    >>> print(new_rd.get_record_count())\n    >>> new_rd.close()\n\n    "

    def __init__(self):
        JVMBase.__init__(self)
        self._dataset = None
        self._name_indexes = None
        self._fieldInfos = None
        self._custom_params = None
        self._java_fieldInfos = None
        self._batchEditor = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def _batch(self):
        if self._batchEditor is None:
            self._batchEditor = self._jobject.getBatch()
        return self._batchEditor

    def set_batch_record_max(self, count):
        """
        设置批量更新操作结果提交的最大记录数，当所有需要更新的记录批量更新完成后，在提交更新结果时，如果更新的记录数超过了这个最大记录数时，系统将分
        批提交更新的结果，即每次提交最大记录数目个记录，直到所有的更新记录都提交完毕。例如，如果设定提交的最大记录数为1000，而需要更新的记录数为3800，
        那么批量更新记录后，在提交结果时，系统将分四次提交更新结果，即第一次提交1000条记录，第二次1000条，第三次1000条，第四次800条。

        :param int count: 批量更新操作结果提交的最大记录数。
        """
        self._batch.setMaxRecordCount(int(count))

    def get_batch_record_max(self):
        """int: 返回批量更新操作结果自动提交的最大记录数"""
        return self._batch.getMaxRecordCount()

    def _set_custom_params(self, value):
        self._custom_params = value

    @property
    def datasource(self):
        """Datasource: 记录集所在的数据源"""
        return self.dataset.datasource

    @property
    def dataset(self):
        """DatasetVector: 记录集所在的数据集"""
        return self._dataset

    @staticmethod
    def _from_java_object(java_recordset, dataset):
        rd = Recordset()
        rd._java_object = java_recordset
        rd._dataset = dataset
        rd._java_fieldInfos = java_recordset.getFieldInfos()
        return rd

    def _make_java_object(self):
        return self._java_object

    def _get_field_index(self, value):
        if isinstance(value, int):
            if value >= 0:
                return value
            return len(self.field_infos) + value
        else:
            if isinstance(value, str):
                if value in self._get_names_indexes().keys():
                    return self._get_names_indexes()[value]
                return -1
            else:
                return -1

    def index_of_field(self, name):
        """
        获取指定字段名称序号

        :param str name: 字段名称
        :return: 如果字段存在返回字段的序号，否则返回 -1
        :rtype: int
        """
        if isinstance(name, str):
            return self._get_field_index(name)
        return -1

    @property
    def field_infos(self):
        """list[FieldInfo]: 数据集的所有字段信息"""
        if self._jobject is None:
            raise ObjectDisposedError("Recordset")
        if self._fieldInfos is None:
            from ._util import java_field_infos_to_list
            self._fieldInfos = java_field_infos_to_list(self._java_fieldInfos)
        return self._fieldInfos

    def _get_names_indexes(self):
        if self._name_indexes is None:
            self._name_indexes = {}
            field_infos = self.field_infos
            for i in range(len(field_infos)):
                self._name_indexes[field_infos[i].name] = i

        return self._name_indexes

    def get_field_info(self, value):
        """
        根据字段名称或序号获取字段信息

        :param value: 字段名称或序号
        :type value: str or int
        :return: 字段信息
        :rtype: FieldInfo
        """
        if self._jobject is None:
            raise ObjectDisposedError("Recordset")
        elif isinstance(value, int):
            return self.field_infos[value]
            if isinstance(value, str):
                _index = self._get_field_index(value)
                if _index >= 0:
                    self.field_infos[_index]
                else:
                    return
        else:
            return

    def __iter__(self):
        return self

    def __next__(self):
        if self.has_next():
            feature = self.get_feature()
            self.move_next()
            return feature
        raise StopIteration()

    def has_next(self):
        """
        记录集是否还有下一条记录可以读取，如果有返回 True，否则返回 False

        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError("Recordset")
        try:
            return not self._jobject.isEOF()
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

        return False

    def is_eof(self):
        """
        记录集是否到达末尾，如果到达末尾返回 True，否则返回 False

        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError("Recordset")
        try:
            return self._jobject.isEOF()
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

        return True

    def move_next(self):
        """
        动当前记录位置到下一条记录，使该记录成为当前记录。成功则返回 True，否则返回 False

        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError("Recordset")
        try:
            return self._jobject.moveNext()
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

        return False

    def get_geometry(self):
        """
        获取当前记录的几何对象，如果记录集没有几何对象或获取失败，返回 None

        :rtype: Geometry
        """
        if self._jobject is None:
            raise ObjectDisposedError("Recordset")
        try:
            return Geometry._from_java_object(self._jobject.getGeometry())
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def get_feature(self):
        """
        获取当前记录的要素对象，如果获取失败返回 None

        :rtype: Feature
        """
        if self._jobject is None:
            raise ObjectDisposedError("Recordset")
        try:
            geometry = self.get_geometry()
            values = self.get_values(False, False)
            return Feature(geometry, values, self.get_id(), self.field_infos)
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def get_value(self, item):
        """
        获取当前记录中指定的属性字段的字段值

        :param item: 字段名称或序号
        :type item: str or int
        :rtype: int or float or str or datetime.datetime or bytes or bytearray
        """
        if self._jobject is None:
            raise ObjectDisposedError("Recordset")
        try:
            _index = self._get_field_index(item)
            java_value = self._jobject.getFieldValue(_index)
            fieldInfo = self.get_field_info(_index)
            from ._util import convert_value_to_python
            return convert_value_to_python(java_value, fieldInfo.type)
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def get_values(self, exclude_system=True, is_dict=False):
        """
        获取当前记录的属性字段值。

        :param bool exclude_system: 是否包含系统字段。所有 "Sm" 开头的字段都是系统字段。默认为 True
        :param bool is_dict: 是否以 dict 形式返回，如果返回 dict，则 dict  的 key 为字段名称， value 为属性字段值。否则以 list 形式返回字段值。默认为 False
        :return: 属性字段值
        :rtype: dict or list
        """
        if self._jobject is None:
            raise ObjectDisposedError("Recordset")
        try:
            if is_dict:
                values = {}
            else:
                values = []
            for i in range(len(self.field_infos)):
                try:
                    field = self.field_infos[i]
                    if exclude_system:
                        if field.is_system_field():
                            continue
                    else:
                        java_value = self._jobject.getFieldValue(i)
                        from ._util import convert_value_to_python
                        value = convert_value_to_python(java_value, field.type)
                        if is_dict:
                            values[field.name] = value
                        else:
                            values.append(value)
                except Exception as e:
                    try:
                        log_warning(e)
                        if not is_dict:
                            values.append(None)
                    finally:
                        e = None
                        del e

            return values
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def add(self, data, values=None):
        """
        向记录集中新增一条记录。记录集必须开启编辑模式，具体查看 :py:meth:`edit` 和 :py:meth:`batch_edit`

        :param data: 被写入的空间对象，如果记录集的数据集为属性表，则传入 None。如果 data 不为空，几何对象的类型必须与数据集的类型想匹配才能写入成功。
                     例如:

                     - :py:class:`Point2D` 和 :py:class:`GeoPoint` 支持写入到点数据集和 CAD 数据集
                     - :py:class:`GeoLine` 支持写入到线数据集和CAD数据集
                     - :py:class:`Rectangle` 和 :py:class:`GeoRegion` 支持写入到面数据集和 CAD 数据集
                     - :py:class:`GeoText` 支持写入到文本数据集和 CAD 数据集

        :type data: Point2D or Rectangle or Geometry or Feature
        :param dict values: 要写入的属性字段值。必须是 dict，dict 的键值为字段名称，dict 的值为字段值。如果 data 为 Feature，此参数无效，因为 Feature 已经包含有属性字段值。
        :return: 写入成功返回 True，否则返回 False
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError("Recordset")
        try:
            if data is None or isinstance(data, (Point2D, Geometry, Rectangle)):
                geometry = data
                if geometry is None:
                    result = self._jobject.addNew(None)
                else:
                    if isinstance(data, Point2D):
                        java_geo = self._jvm.com.supermap.data.GeoPoint(float(data.x), float(data.y))
                    else:
                        if isinstance(data, Rectangle):
                            java_geo = data.to_region()._jobject
                        else:
                            java_geo = geometry._jobject
                    result = self._jobject.addNew(java_geo)
                if result:
                    if isinstance(values, dict):
                        for name, value in values.items():
                            self.set_value(name, value)

                    return result
                return False
            else:
                if isinstance(data, Feature):
                    return self.add(data.geometry, data.get_values(True, True))
                log_error("invalid input")
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

        return False

    def set(self, data, values=None):
        """
        修改当前记录。记录集必须开启编辑模式，具体查看 :py:meth:`edit` 和 :py:meth:`batch_edit`

        :param data: 被写入的空间对象。如果记录集的数据集为属性表，则传入 None。如果 data 不为空，几何对象的类型必须与数据集的类型想匹配才能写入成功。
                     例如:

                     - :py:class:`Point2D` 和 :py:class:`GeoPoint` 支持写入到点数据集和 CAD 数据集
                     - :py:class:`GeoLine` 支持写入到线数据集和CAD数据集
                     - :py:class:`Rectangle` 和 :py:class:`GeoRegion` 支持写入到面数据集和 CAD 数据集
                     - :py:class:`GeoText` 支持写入到文本数据集和 CAD 数据集

        :type data:  Point2D or Rectangle or Geometry or Feature
        :param values: 要写入的属性字段值。必须是 dict，dict 的键值为字段名称，dict 的值为字段值。如果 data 为 Feature，此参数无效，因为
                       Feature 已经包含有属性字段值。如果 data 为空，将只写入属性字段值。
        :return: 写入成功返回 True，否则返回 False
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError("Recordset")
        try:
            if data is not None:
                if isinstance(data, (Point2D, Geometry, Rectangle)):
                    geometry = data
                    if isinstance(data, Point2D):
                        java_geo = self._jvm.com.supermap.data.GeoPoint(float(data.x), float(data.y))
                    else:
                        if isinstance(data, Rectangle):
                            java_geo = data.to_region()._jobject
                        else:
                            java_geo = geometry._jobject
                    self._jobject.setGeometry(java_geo)
                    if isinstance(values, dict):
                        for name, value in values.items():
                            self.set_value(name, value)

                    return True
                if isinstance(data, Feature):
                    return self.set(data.geometry, data.get_values(True, True))
                log_error("invalid input")
            else:
                if isinstance(values, dict):
                    for name, value in values.items():
                        self.set_value(name, value)

                return True
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

        return False

    def set_values(self, values):
        """
        设置字段值。记录集必须开启编辑模式，具体查看 :py:meth:`edit` 和 :py:meth:`batch_edit`

        :param dict values: 要写入的属性字段值。必须是 dict，dict 的键值为字段名称，dict 的值为字段值
        :return: 返回成功写入的字段数目
        :rtype: int
        """
        if self._jobject is None:
            raise ObjectDisposedError("Recordset")
        success_count = 0
        if isinstance(values, dict):
            for name, value in values.items():
                if self.set_value(name, value):
                    success_count += 1

        return success_count

    def set_value(self, item, value):
        """
        写入字段值到指定的字段中。记录集必须开启编辑模式，具体查看 :py:meth:`edit` 和 :py:meth:`batch_edit`

        :param item: 字段名称或序号，不能为系统字段。
        :type item: str or int
        :param value: 待写入的字段值。字段类型与值类型对应关系为:

                      - BOOLEAN: bool
                      - BYTE: int
                      - INT16: int
                      - INT32: int
                      - INT64: int
                      - SINGLE: float
                      - DOUBLE: float
                      - DATETIME: datetime.datetime 或 int（时间戳，单位为秒）或满足 ”%Y-%m-%d %H:%M:%S“ 格式的 字符串
                      - LONGBINARY: bytearray or bytes
                      - TEXT: str
                      - CHAR: str
                      - WTEXT: str
                      - JSONB: str

        :type value: bool or int or float or datetime.datetime or bytes or bytearray or str
        :return: 成功返回 True,否则返回 False
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError("Recordset")
        try:
            index = self._get_field_index(item)
            if index < 0:
                return False
                fieldInfo = self.get_field_info(index)
                result = False
                if value is None:
                    result = self._jobject.setFieldValueNull(index)
            else:
                field_type = fieldInfo.type
            if field_type == FieldType.BOOLEAN:
                result = self._jobject.setBoolean(index, bool(value))
            else:
                if field_type == FieldType.CHAR:
                    result = self._jobject.setString(index, str(value))
                else:
                    if field_type == FieldType.WTEXT or field_type == FieldType.TEXT:
                        result = self._jobject.setString(index, str(value))
                    else:
                        if field_type == FieldType.BYTE:
                            result = self._jobject.setByte(index, int(value))
                        else:
                            if field_type == FieldType.INT16:
                                result = self._jobject.setInt16(index, int(value))
                            else:
                                if field_type == FieldType.INT32:
                                    result = self._jobject.setInt32(index, int(value))
                                else:
                                    if field_type == FieldType.INT64:
                                        result = self._jobject.setInt64(index, int(value))
                                    else:
                                        if field_type == FieldType.SINGLE:
                                            result = self._jobject.setSingle(index, float(value))
                                        else:
                                            if field_type == FieldType.DOUBLE:
                                                result = self._jobject.setDouble(index, float(value))
                                            else:
                                                if field_type == FieldType.JSONB:
                                                    result = self._jobject.setJsonB(index, str(value))
                                                else:
                                                    if field_type == FieldType.LONGBINARY:
                                                        if isinstance(value, bytes) or isinstance(value, bytearray):
                                                            result = self._jobject.setLongBinary(index, value)
                                                        else:
                                                            result = self._jobject.setLongBinary(index, bytes((str(value)), encoding="utf-8"))
                                                    else:
                                                        if field_type == FieldType.DATETIME:
                                                            t = datetime_to_java_date(value)
                                                            if t is not None:
                                                                result = self._jobject.setDateTime(index, t)
            return result
        except Exception as e:
            try:
                log_error(e)
                return False
            finally:
                e = None
                del e

    def close(self):
        """
        释放记录集，记录集完成操作不再使用后必须释放记录集
        """
        if not self.is_close():
            if self._jobject is None or self._dataset._jobject is None:
                return
            try:
                self._jobject.dispose()
                self._java_object = None
            except Exception:
                import traceback
                log_error(traceback.format_exc())
                self._java_object = None

    def dispose(self):
        """
        释放记录集，记录集完成操作不再使用后必须释放记录集, 与 close 功能相同
        """
        self.close()

    def get_record_count(self):
        """
        返回记录集中记录数目

        :rtype: int
        """
        if self._jobject is None:
            raise ObjectDisposedError("Recordset")
        try:
            return self._jobject.getRecordCount()
        except Exception as e:
            try:
                log_error(e)
                raise e
            finally:
                e = None
                del e

    def is_bof(self):
        """
        判断当前记录的位置是否在记录集中第一条记录的前面（当然第一条记录的前面是没有数据的），如果是返回 True；否则返回 False。

        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError("Recordset")
        try:
            return self._jobject.isBOF()
        except Exception as e:
            try:
                log_error(e)
                raise e
            finally:
                e = None
                del e

    def seek_id(self, value):
        """
        在记录中搜索指定 ID 号的记录，并定位该记录为当前记录。成功则返回 true，否则返回 false

        :param int value: 要搜索的 ID 号
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError("Recordset")
        try:
            return self._jobject.seekID(int(value))
        except Exception as e:
            try:
                log_error(e)
                raise e
            finally:
                e = None
                del e

    def is_readonly(self):
        """
        判断记录集是否是只读的，只读返回 True，否则返回 False

        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError("Recordset")
        try:
            return self._jobject.isReadOnly()
        except Exception as e:
            try:
                log_error(e)
                raise e
            finally:
                e = None
                del e

    def refresh(self):
        """
        刷新当前记录集，用来反映数据集中的变化。如果成功返回 True，否则返回 False。此方法与 :py:meth:`update` 的区别在于 update 方法是提交
        修改结果，而 refresh 方法是动态刷新记录集，在多用户并发操作时，为了动态显示数据集中的变化，经常用到 refresh 方法。

        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError("Recordset")
        try:
            return self._jobject.refresh()
        except Exception as e:
            try:
                log_error(e)
                raise e
            finally:
                e = None
                del e

    def is_empty(self):
        """
        判断记录集中是否有记录。True 表示该记录集中无数据

        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError("Recordset")
        try:
            return self._jobject.isEmpty()
        except Exception as e:
            try:
                log_error(e)
                raise e
            finally:
                e = None
                del e

    def is_close(self):
        """
        判断记录集是否已经被关闭。被关闭返回 True，否则返回 False。

        :rtype: bool
        """
        if self._jobject is None:
            return True
        try:
            if self._dataset._jobject is None:
                self._java_object = None
                return True
            if self._jobject.isClosed():
                self._java_object = None
                return True
            return False
        except Exception as e:
            try:
                import traceback
                log_error(traceback.format_exc())
                raise e
            finally:
                e = None
                del e

    def get_id(self):
        """
        返回数据集的属性表中当前记录对应的几何对象的 ID 号（即 SmID 字段的值）。

        :rtype: int
        """
        if self._jobject is None:
            raise ObjectDisposedError("Recordset")
        try:
            return self._jobject.getID()
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

        return -1

    def move_first(self):
        """
        用于移动当前记录位置到第一条记录，使第一条记录成为当前记录。成功则返回 True。

        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError("Recordset")
        try:
            return self._jobject.moveFirst()
        except Exception as e:
            try:
                log_error(e)
                raise e
            finally:
                e = None
                del e

    def move_last(self):
        """
        用于移动当前记录位置到最后一条记录，使最后一条记录成为当前记录。成功则返回 True

        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError("Recordset")
        try:
            return self._jobject.moveLast()
        except Exception as e:
            try:
                log_error(e)
                raise e
            finally:
                e = None
                del e

    def move_prev(self):
        """
        移动当前记录位置到上一条记录，使该记录成为当前记录。成功则返回 True。

        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError("Recordset")
        try:
            return self._jobject.movePrev()
        except Exception as e:
            try:
                log_error(e)
                raise e
            finally:
                e = None
                del e

    def move_to(self, position):
        """
        用于移动当前记录位置到指定的位置，将该指定位置的记录作为当前记录。成功则返回 True。

        :param int position: 移动到的位置，即第几条记录
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError("Recordset")
        try:
            return self._jobject.moveTo(int(position))
        except Exception as e:
            try:
                log_error(e)
                raise e
            finally:
                e = None
                del e

    def move(self, count):
        """
        将当前记录位置移动 count 行，将该位置的记录设置为当前记录。成功返回 True。count 小于0表示向前移，大于0表示向后移动，等于0时不移动。如
        果移动的行数太多，超出了 Recordset 的范围，将会返回 False，当前记录不移动。

        :param int count: 移动的记录数
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError("Recordset")
        try:
            return self._jobject.moveTo(int(count))
        except Exception as e:
            try:
                log_error(e)
                raise e
            finally:
                e = None
                del e

    def edit(self):
        """
        锁定并编辑记录集的当前记录，成功则返回 True。用该方法编辑后，一定要用 :py:meth:`update` 方法更新记录集，而且在 :py:meth:`update` 之
        前不能移动当前记录的位置，否则编辑失败，记录集也可能被损坏。

        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError("Recordset")
        try:
            return self._jobject.edit()
        except Exception as e:
            try:
                log_error(e)
                raise e
            finally:
                e = None
                del e

    def update(self):
        """
        用于提交对记录集的修改，包括添加、编辑记录、修改字段值的操作。使用 :py:meth:`edit`  对记录集做修改之后，都需要使用 update 来提交修改。每对一条记录做完修改就
        需要调用一次 update 来提交修改。

        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError("Recordset")
        try:
            return self._jobject.update()
        except Exception as e:
            try:
                log_error(e)
                raise e
            finally:
                e = None
                del e

    def batch_edit(self):
        """
        批量更新操作开始。批量更新操作完成后，需要使用 :py:meth:`batch_update` 来提交修改的记录。可以使用 :py:meth:`set_batch_record_max` 修改
        批量更新操作结果提交的最大记录数，具体查看 :py:meth:`set_batch_record_max`

        """
        if self._jobject is None:
            raise ObjectDisposedError("Recordset")
        try:
            if self._batch is None:
                raise RuntimeError("BatchEditor is None")
            self._batch.begin()
        except Exception as e:
            try:
                log_error(e)
                raise e
            finally:
                e = None
                del e

    def batch_update(self):
        """
        批量更新操作的统一提交。调用该方法后，之前进行的批量更新操作才会生效，同时更新状态将变为单条更新，如果需要之后的操作批量进行，还需再次调用 :py:meth:`batch_edit` 方法。
        """
        if self._jobject is None:
            raise ObjectDisposedError("Recordset")
        try:
            if self._batch is None:
                raise RuntimeError("BatchEditor is None")
            self._batch.update()
        except Exception as e:
            try:
                log_error(e)
                raise e
            finally:
                e = None
                del e

    def get_features(self):
        """
        获取记录集的所有要素对象。调用该方法后，记录集的位置会移动的最开始的位置。

        :rtype: list[Feature]
        """
        if self._jobject is None:
            raise ObjectDisposedError("Recordset")
        try:
            features = []
            self.move_first()
            for f in self:
                features.append(f)

            self.move_first()
            return features
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def get_geometries(self):
        """
        获取记录集的所有几何对象。调用该方法后，记录集的位置会移动的最开始的位置。

        :rtype: list[Geometry]
        """
        if self._jobject is None:
            raise ObjectDisposedError("Recordset")
        try:
            geos = []
            self.move_first()
            while self.has_next():
                geos.append(self.get_geometry())
                self.move_next()

            self.move_first()
            return geos
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def get_query_parameter(self):
        """
        获取当前记录集对应的查询参数

        :rtype: QueryParameter
        """
        if self._jobject is None:
            raise ObjectDisposedError("Recordset")
        try:
            java_parameter = self._jobject.getQueryParameter()
            return QueryParameter._from_java_object(java_parameter)
        except Exception as e:
            try:
                log_error(e)
                raise e
            finally:
                e = None
                del e

    def get_field_count(self):
        """
        获取字段数目

        :rtype: int
        """
        if self._jobject is None:
            raise ObjectDisposedError("Recordset")
        try:
            return self._jobject.getFieldCount()
        except Exception as e:
            try:
                log_error(e)
                raise e
            finally:
                e = None
                del e

    def statistic(self, item, stat_mode):
        """
        通过字段名称或序号，对指定字段进行诸如最大值、最小值、平均值，总和，标准差和方差等方式的统计。

        :param item: 字段名称或序号
        :type item: str or int
        :param stat_mode: 统计方式
        :type stat_mode:  StatisticMode or str
        :return: 统计结果。
        :rtype: float
        """
        if self._jobject is None:
            raise ObjectDisposedError("Recordset")
        try:
            if isinstance(item, int):
                if item < 0:
                    item += len(self.field_infos)
            return self._jobject.statistic(item, StatisticMode._make(stat_mode)._jobject)
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def to_json(self):
        """
        将当前记录集的数据集和查询参数输出为 json 字符串。注意，使用 Recordset 的 to_json 只保存数据集信息的查询参数，只适用于使用 DatasetVector 入口查询得到的结果记录集，包括
        :py:meth:`DatasetVector.get_recordset` , :py:meth:`DatasetVector.query`, :py:meth:`DatasetVector.query_with_bounds`,
        :py:meth:`DatasetVector.query_with_distance`, :py:meth:`DatasetVector.query_with_filter` 和 :py:meth:`DatasetVector.query_with_ids`。
        如果是由其他功能内部查询得到的记录集，可能无法完全确保查询参数的是否与查询时输入的查询参数是否一致。

        :rtype: str
        """
        if self._jobject is None:
            raise ObjectDisposedError("Recordset")
        else:
            d = dict()
            d["dataset"] = self.dataset.to_json()
            d1 = {}
            if self._custom_params is not None:
                d1["type"] = "custom"
                d1["params"] = self._custom_params
            else:
                d1["type"] = "pre"
            d1["params"] = self.get_query_parameter().to_json()
        d["query_params"] = d1
        return json.dumps(d)

    @staticmethod
    def from_json(value):
        """
        从 json 字符串中解析获取记录集

        :param str value: json 字符串
        :rtype: Recordset
        """
        d = json.loads(value)
        dataset = Dataset.from_json(d["dataset"])
        if dataset is None:
            raise ValueError("Failed to get dataset from json " + d["dataset"])
        d1 = d["query_params"]
        if d1["type"] == "pre":
            params = QueryParameter.from_json(d1["params"])
            return dataset.query(params)
        params = d1["params"]["params"]
        _method = d1["params"]["func"]
        if _method == "get_recordset":
            return dataset.get_recordset(is_empty=(params["is_empty"]), cursor_type=(params["cursor_type"]))
        if _method == "query_with_ids":
            return dataset.query_with_ids(ids=(params["ids"]), id_field_name=(params["id_field_name"]), cursor_type=(params["cursor_type"]))
        if _method == "query_with_bounds":
            return dataset.query_with_bounds(bounds=(Rectangle.from_json(params["bounds"])), attr_filter=(params["attr_filter"]),
              cursor_type=(params["cursor_type"]))
        raise RuntimeError("Unknown method name " + _method)

    def delete(self):
        """
        用于删除数据集中的当前记录，成功则返回 true。

        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError("Recordset")
        try:
            return self._jobject.delete()
        except Exception as e:
            try:
                log_error(e)
                raise e
            finally:
                e = None
                del e

        return False

    def delete_all(self):
        """
        物理性删除指定记录集中的所有记录，即把记录从计算机的物理存储介质上删除，无法恢复。

        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError("Recordset")
        try:
            return self._jobject.deleteAll()
        except Exception as e:
            try:
                log_error(e)
                raise e
            finally:
                e = None
                del e

        return False

    @property
    def bounds(self):
        """Rectangle: 返回记录集的属性数据表中所有记录对应的几何对象的外接矩形。"""
        if self._jobject is None:
            raise ObjectDisposedError("Recordset")
        try:
            return Rectangle._from_java_object(self._jobject.getBounds())
        except Exception as e:
            try:
                log_error(e)
                raise e
            finally:
                e = None
                del e

    def __del__(self):
        if not self.is_close():
            self.close()
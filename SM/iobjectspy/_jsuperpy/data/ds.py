# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/_jsuperpy\data\ds.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 88359 bytes
import os, json, datetime
from ._jvm import JVMBase
from .prj import PrjCoordSys
from .geo import *
from .ex import ObjectDisposedError
from ._listener import ProgressListener
from .._logger import log_error, log_warning
from .._gateway import get_jvm, safe_start_callback_server, close_callback_server
from .._utils import get_unique_name
from ..enums import DatasetType, EngineType, PixelFormat, PrjCoordSysType, EncodeType, FieldType, CursorType
from .dt import *
from collections import OrderedDict
__all__ = [
 "DatasourceConnectionInfo", "Datasource"]

class DatasourceConnectionInfo(JVMBase):
    __doc__ = "\n    数据源连接信息类。包括了进行数据源连接的所有信息，如所要连接的服务器名称，数据库名称、用户名、密码等。当保存工作空间时，工作空间中的数据源的\n    连接信息都将存储到工作空间文件中。对于不同类型的数据源，其连接信息有所区别。所以在使用该类所包含的成员时，请注意该成员所适用的数据源类型。\n\n    例如::\n        >>> conn_info = DatasourceConnectionInfo('E:/data.udb')\n        >>> print(conn_info.server)\n        'E:\\data.udb'\n        >>> print(conn_info.type)\n        EngineType.UDB\n\n\n    创建 OraclePlus 数据库连接信息::\n\n        >>> conn_info = (DatasourceConnectionInfo().\n        >>>                    set_type(EngineType.ORACLEPLUS).\n        >>>                    set_server('server').\n        >>>                    set_database('database').\n        >>>                    set_alias('alias').\n        >>>                    set_user('user').\n        >>>                    set_password('password'))\n        >>> print(conn_info.database)\n        'server'\n\n\n    "

    def __init__(self, server=None, engine_type=None, alias=None, is_readonly=None, database=None, driver=None, user=None, password=None):
        """
        构造数据源连接对象

        :param str server: 数据库服务器名、文件名或服务地址:

                           - 对于 MEMORY， 为 ':memory:'
                           - 对于 UDB 文件，为其文件的绝对路径。注意：当绝对路径的长度超过 UTF-8 编码格式的260字节长度，该数据源无法打开。
                           - 对于 Oracle 数据库，其服务器名为其 TNS 服务名称；
                           - 对于 SQL Server 数据库，其服务器名为其系统的 DSN（Database Source Name）名称;
                           - 对于 PostgreSQL 数据库，其服务器名为"IP:端口号"，默认的端口号是 5432；
                           - 对于 DB2 数据库，已经进行了编目，所以不需要进行服务器的设置；
                           - 对于 Kingbase 数据库，其服务器名为其 IP 地址；
                           - 对于 GoogleMaps 数据源，为其服务地址，默认设置为 "http://maps.google.com"，且不可更改；
                           - 对于 SuperMapCloud 数据源，为其服务地址；
                           - 对于 MAPWORLD 数据源，为其服务地址，默认设置为 "http://www.tianditu.cn"，且不可更改；
                           - 对于 OGC 和 REST 数据源，为其服务地址。
                           - 若用户设置为 IMAGEPLUGINS 时，将此方法的参数设置为地图缓存配置文件（SCI）名称，则用户可以实现对地图缓存的加载

        :param engine_type: 数据源连接的引擎类型，可以使用 EngineType 枚举值和名称
        :type engine_type: EngineType or str
        :param str alias: 数据源别名。别名是数据源的唯一标识。该标识不区分大小写
        :param bool is_readonly: 是否以只读方式打开数据源。如果以只读方式打开数据源，数据源的相关信息以及其中的数据都不可修改。
        :param str database: 数据源连接的数据库名
        :param str driver: 数据源连接所需的驱动名称:

                               - 对于SQL Server 数据库，它使用 ODBC 连接，返回的驱动程序名为 SQL Server 或 SQL Native Client。
                               - 对于 iServer 发布的 WMTS 服务，返回的驱动名称为 WMTS。

        :param str user: 登录数据库的用户名。对于数据库类型数据源适用。
        :param str password: 登录数据源连接的数据库或文件的密码。对于 GoogleMaps 数据源，如果打开的是基于早期版本的数据源，则返回的密码为用户在 Google 官网注册后获取的密钥
        """
        JVMBase.__init__(self)
        self._server = None
        self._alias = None
        self._type = None
        self._readOnly = False
        self._database = None
        self._driver = None
        self._user = None
        self._password = None
        self.set_server(server)
        self.set_alias(alias)
        self.set_type(engine_type)
        self.set_readonly(is_readonly)
        self.set_database(database)
        self.set_driver(driver)
        self.set_user(user)
        self.set_password(password)

    @staticmethod
    def _parse_engine_type_from_server(server):
        _server = server.lower()
        if _server == ":memory:":
            return EngineType.MEMORY
        if _server.endswith(".udb") or _server.endswith(".udd"):
            return EngineType.UDB
        if _server.endswith(".udbx"):
            return EngineType.UDBX
        return

    def __str__(self):
        conn_info = self
        str_info = []
        if conn_info.server:
            str_info.append("server: " + conn_info.server)
        elif conn_info.alias:
            str_info.append("alias: " + conn_info.alias)
        if conn_info.type:
            str_info.append("type: " + conn_info.type.name)
        if conn_info.database:
            str_info.append("database: " + conn_info.database)
        if conn_info.driver:
            str_info.append("driver: " + conn_info.driver)
        if conn_info.user:
            str_info.append("user: " + conn_info.user)
        if conn_info.password:
            str_info.append("password: " + conn_info.password)
        if conn_info.is_readonly:
            str_info.append("readonly: true")
        else:
            str_info.append("readonly: false")
        return "\n".join(str_info)

    def __repr__(self):
        return type(self).__name__ + "(%s, %s)" % (self.alias, self.type.name)

    def _make_java_object(self):
        if self._java_object:
            return self._java_object
        conninfo = self._jvm.com.supermap.data.DatasourceConnectionInfo()
        conninfo.setServer(self.server)
        if self.alias is not None:
            conninfo.setAlias(self.alias)
        if self.driver is not None:
            conninfo.setDriver(self.driver)
        if self.is_readonly is not None:
            conninfo.setReadOnly(self.is_readonly)
        if self.database is not None:
            conninfo.setDatabase(self.database)
        if self.user is not None:
            conninfo.setUser(self.user)
        if self.password is not None:
            conninfo.setPassword(self.password)
        if self.type is not None:
            conninfo.setEngineType(self.type._jobject)
        self._java_object = conninfo
        return self._java_object

    @staticmethod
    def _from_java_object(java_conn_info):
        if java_conn_info is None:
            raise Exception("java datasource connectioninfo object is None")
        conninfo = DatasourceConnectionInfo()
        conninfo._java_object = java_conn_info
        conninfo.set_type(EngineType._make(java_conn_info.getEngineType().name()))
        conninfo.set_server(java_conn_info.getServer())
        conninfo.set_password(java_conn_info.getPassword())
        conninfo.set_database(java_conn_info.getDatabase())
        conninfo.set_readonly(java_conn_info.isReadOnly())
        conninfo.set_driver(java_conn_info.getDriver())
        conninfo.set_alias(java_conn_info.getAlias())
        conninfo.set_user(java_conn_info.getUser())
        return conninfo

    @staticmethod
    def load_from_dcf(file_path):
        """
        从 dcf 文件中加载数据库连接信息，返回一个新的数据库连接信息对象。

        :param str file_path: dcf 文件路径。
        :return: 数据源连接信息对象
        :type: DatasourceConnectionInfo
        """
        if file_path is None:
            raise ValueError("file_path is None")
        conninfo = get_jvm().com.supermap.data.DatasourceConnectionInfo()
        if conninfo.loadFromDCF(file_path):
            return DatasourceConnectionInfo._from_java_object(conninfo)
        raise Exception("Failed to load dcf file.")

    def save_as_dcf(self, file_path):
        """
        将当前数据集连接信息对象保存到 dcf 文件中。

        :param str file_path: dcf 文件路径。
        :return: 成功保存返回 True, 否则返回 False
        :type: bool
        """
        if file_path is None:
            raise ValueError("file_path is None")
        if self._jobject is not None:
            return self._jobject.saveAsDCF(file_path)
        raise ObjectDisposedError("DatasourceConnectionInfo")

    @staticmethod
    def load_from_xml(xml):
        """
        从指定的 xml 字符串中加载数据库连接信息，并返回一个新的数据库连接信息对象。

        :param str xml: 导入的数据源的连接信息的 xml 字符串
        :return: 数据源连接信息对象
        :type: DatasourceConnectionInfo
        """
        if xml is None:
            raise ValueError("xml is None")
        conninfo = get_jvm().com.supermap.data.DatasourceConnectionInfo()
        if conninfo.fromXML(xml):
            return DatasourceConnectionInfo._from_java_object(conninfo)
        raise ObjectDisposedError("DatasourceConnectionInfo")

    def to_xml(self):
        """
        将当前数据集连接信息输出为 xml 字符串

        :return:  由当前数据源连接信息对象转换而得到的 XML 字符串。
        :rtype: str
        """
        if self._jobject is not None:
            return self._jobject.toXML()
        raise ObjectDisposedError("DatasourceConnectionInfo")

    @property
    def type(self):
        """EngineType: 数据源类型"""
        if self._type is None:
            if self._server is not None:
                self._type = DatasourceConnectionInfo._parse_engine_type_from_server(self._server)
        return self._type

    def set_type(self, value):
        """
        设置数据源连接的引擎类型。

        :param value: 数据源连接的引擎类型
        :type value: EngineType or str
        :return: self
        :rtype: DatasourceConnectionInfo
        """
        if value is not None:
            self._type = EngineType._make(value)
        return self

    @property
    def serverParse error at or near `JUMP_FORWARD' instruction at offset 78

    def set_serverParse error at or near `JUMP_FORWARD' instruction at offset 74

    @property
    def alias(self):
        """str: 数据源别名，别名是数据源的唯一标识。该标识不区分大小写"""
        if self._alias is None:
            if self.server.lower().endswith(".udb") or self.server.lower().endswith(".udbx"):
                base_name = os.path.basename(self.server)
                _alias = base_name[None[:base_name.index(".")]]
                from .ws import Workspace
                self._alias = Workspace().is_contains_datasource(_alias) or _alias
            else:
                self._alias = get_unique_name(_alias)
        if self._alias is None:
            self._alias = get_unique_name("ds")
        return self._alias

    def set_alias(self, value):
        """
        设置数据源别名

        :param str value:  别名是数据源的唯一标识。该标识不区分大小写
        :return: self
        :rtype: DatasourceConnectionInfo
        """
        if value is not None:
            self._alias = value
        return self

    @property
    def is_readonly(self):
        """bool: 是否以只读方式打开数据源"""
        return self._readOnly

    def set_readonly(self, value):
        """
        设置是否以只读方式打开数据源。

        :param bool value:  指定是否以只读方式打开数据源。对于 UDB 数据源，如果其文件属性为只读的，必须设置为只读时才能打开。
        :return: self
        :rtype: DatasourceConnectionInfo
        """
        if value is not None:
            self._readOnly = bool(value)
        return self

    @property
    def database(self):
        """str: 数据源连接的数据库名"""
        return self._database

    def set_database(self, value):
        """
        设置数据源连接的数据库名。对于数据库类型数据源适用

        :param str value:  数据源连接的数据库名。
        :return: self
        :rtype: DatasourceConnectionInfo
        """
        if value is not None:
            self._database = value
        return self

    @property
    def driver(self):
        """str: 数据源连接所需的驱动名称"""
        return self._driver

    def set_driver(self, value):
        """
        设置数据源连接所需的驱动名称。

        :param str value: 数据源连接所需的驱动名称:

                              - 对于SQL Server 数据库，它使用 ODBC 连接，所设置的驱动程序名为 SQL Server 或 SQL Native Client。
                              - 对于 iServer 发布的 WMTS 服务，设置的驱动名称为 WMTS，并且该方法必须调用该方法设置其驱动名称。

        :return: self
        :rtype: DatasourceConnectionInfo
        """
        if value is not None:
            self._driver = value
        return self

    @property
    def user(self):
        """str: 登录数据库的用户名"""
        return self._user

    def set_user(self, value):
        """
        设置登录数据库的用户名。对于数据库类型数据源适用

        :param str value: 登录数据库的用户名
        :return: self
        :rtype: DatasourceConnectionInfo
        """
        if value is not None:
            self._user = value
        return self

    @property
    def password(self):
        """str: 登录数据源连接的数据库或文件的密码"""
        return self._password

    def set_password(self, value):
        """
        设置登录数据源连接的数据库或文件的密码

        :param str value:  登录数据源连接的数据库或文件的密码。对于 GoogleMaps 数据源，如果打开的是基于早期版本的数据源，则需要输入密码，其密码为用户在 Google 官网注册后获取的密钥。
        :return: self
        :rtype: DatasourceConnectionInfo
        """
        if value is not None:
            self._password = value
        return self

    def to_dict(self):
        """
        将当前数据源连接信息输出为 dict 对象。

        :return: 包含数据源连接信息的 dict
        :rtype: dict

        示例::
            >>> conn_info = (DatasourceConnectionInfo().
            >>>                set_type(EngineType.ORACLEPLUS).
            >>>                set_server('oracle_server').
            >>>                set_database('database_name').
            >>>                set_alias('alias_name').
            >>>                set_user('user_name').
            >>>                set_password('password_123'))
            >>>
            >>> print(conn_info.to_dict())
            {'type': 'ORACLEPLUS', 'alias': 'alias_name', 'server': 'oracle_server', 'user': 'user_name', 'is_readonly': False, 'password': 'password_123', 'database': 'database_name'}

        """
        d = dict()
        d["server"] = self.server
        d["type"] = self.type.name
        if self.alias:
            d["alias"] = self.alias
        if self.driver:
            d["driver"] = self.driver
        if self.is_readonly is not None:
            d["is_readonly"] = self.is_readonly
        if self.database:
            d["database"] = self.database
        if self.user:
            d["user"] = self.user
        if self.password:
            d["password"] = self.password
        return d

    @staticmethod
    def make_from_dict(values):
        """
        从 dict 对象中构造数据源连接对象。返回一个新的数据库连接信息对象。

        :param dict values: 包含数据源连接信息的 dict.
        :return: 数据源连接信息对象
        :rtype: DatasourceConnectionInfo
        """
        return DatasourceConnectionInfo().from_dict(values)

    def from_dict(self, values):
        """
        从 dict 对象中读取数据库数据源连接信息。读取后会覆盖当前对象中的值。

        :param dict values: 包含数据源连接信息的 dict.
        :return: self
        :rtype: DatasourceConnectionInfo
        """
        if "server" in values.keys():
            self.set_server(values["server"])
        if "type" in values.keys():
            self.set_type(EngineType._make(values["type"]))
        if "alias" in values.keys():
            self.set_alias(values["alias"])
        if "driver" in values.keys():
            self.set_driver(values["driver"])
        if "is_readonly" in values.keys():
            self.set_readonly(values["is_readonly"])
        if "database" in values.keys():
            self.set_database(values["database"])
        if "user" in values.keys():
            self.set_user(values["user"])
        if "password" in values.keys():
            self.set_password(values["password"])
        return self

    def is_same(self, other):
        """
        判断当前对象与指定的数据库连接信息对象是否是指向同一个数据源对象。
        如果两个数据库连接信息指向同一个数据源，则必须:

            - 数据库引擎类型 (type) 相同
            - 数据库服务器名、文件名或服务地址 (server) 相同
            - 数据库连接的数据库名称 (database) 相同如果需要设置。
            - 数据库的用户名 (user) 相同，如果需要设置。
            - 数据源连接的数据库或文件的密码 (password) 相同，如果需要设置。
            - 是否以只读方式打开 (is_readonly) 相同，如果需要设置。

        :param DatasourceConnectionInfo other: 需要比较的数据库连接信息对象。
        :return: 返回\u3000True 表示与指定的数据库连接信息是指向同一个数据源对象。否则为 False
        :rtype: bool
        """
        if other is None:
            raise ValueError("other is None")
        elif not isinstance(other, DatasourceConnectionInfo):
            raise ValueError("required DatasourceConnectionInfo, but now is " + str(type(DatasourceConnectionInfo)))
        else:
            if self.type != other.type:
                return False
                if self.server != other.server:
                    return False
                if self.type in set([EngineType.UDB, EngineType.UDBX, EngineType.VECTORFILE, EngineType.MEMORY,
                 EngineType.IMAGEPLUGINS, EngineType.SUPERMAPCLOUD, EngineType.BAIDUMAPS,
                 EngineType.GOOGLEMAPS, EngineType.BINGMAPS,
                 EngineType.OPENSTREETMAPS, EngineType.ISERVERREST]):
                    return True
                if self.database is not None:
                    if len(self.database) > 0:
                        if other.database is not None:
                            if len(other.database) > 0:
                                if self.database != other.database:
                                    return False
                if self.user is not None and len(self.user) > 0 and other.user is not None and len(other.user) > 0:
                    if self.user != other.user:
                        return False
            elif self.password is not None:
                if len(self.password) > 0:
                    if other.password is not None:
                        if len(other.password) > 0 and self.password != other.password:
                            return False
            if self.is_readonly is not None and other.is_readonly is not None and self.is_readonly != other.is_readonly:
                return False
        return True

    @staticmethod
    def makeParse error at or near `POP_BLOCK' instruction at offset 170

    def to_json(self):
        """
        输出为 json 格式字符串

        :return:  json 格式字符串
        :rtype: str
        """
        return json.dumps(self.to_dict())

    @staticmethod
    def from_json(value):
        """
        从 json 字符串构造数据源连接信息对象。

        :param str value:    json 字符串
        :return: 数据源连接信息对象
        :rtype: DatasourceConnectionInfo
        """
        return DatasourceConnectionInfo.make_from_dict(json.loads(value))


class Datasource(JVMBase):
    __doc__ = "\n    数据源定义了一致的数据访问接口和规范。数据源的物理存储既可以是文件方式，也可以是数据库方式。区别不同存储方式的主要依据是其所采用的数据引擎类型：\n    采用 UDB 引擎时，数据源以文件方式存储（*.udb，*.udd）——文件型数据源文件用.udb 文件存储空间数据，采用空间数据库引擎时，数据源存储在指定的\n    DBMS 中。每个数据源都存在于一个工作空间中，不同的数据源通过数据源别名进行区分。通过数据源对象，可以对数据集进行创建、删除、复制等操作。\n\n\n    使用 create_vector_dataset 快速创建矢量数据集::\n\n        >>> ds = Datasource.create('E:/data.udb')\n        >>> location_dt = ds.create_vector_dataset('location', 'Point')\n        >>> print(location_dt.name)\n        location\n\n\n    追加数据到点数据集中::\n\n        >>> location_dt.append([Point2D(1,2), Point2D(2,3), Point2D(3,4)])\n        >>> print(location_dt.get_record_count())\n        3\n\n    数据源可以直接写入几何对象，要素对象，点数据等::\n\n        >>> rect = location_dt.bounds\n        >>> location_coverage = ds.write_spatial_data([rect], 'location_coverage')\n        >>> print(location_coverage.get_record_count())\n        1\n        >>> ds.delete_all()\n        >>> ds.close()\n    "

    def __init__(self):
        self._workspace = None
        self._dict_dt = OrderedDict()
        JVMBase.__init__(self)

    def __str__(self):
        if self._java_object is not None:
            try:
                conn_info = self.connection_info
                str_info = conn_info.__str__()
                datasets = self.datasets
                datasets_infos = []
                str_info += "\n"
                datasets_infos.append("%-31s %-10s" % ('name', 'type'))
                datasets_infos.append("%-31s %-10s" % ('----------', '-----------'))
                for dt in datasets:
                    datasets_infos.append("%-31s %-10s" % (dt.name, dt.type.name))

                datasets_str = "\n".join(datasets_infos)
                return str_info + datasets_str
            except:
                import traceback
                log_error(traceback.format_exc())
                return ""

        else:
            return ""

    def __repr__(self):
        return "Datasource(%s,%s)" % (self.alias, self.type)

    def _set_existed(self):
        setattr(self, "_is_exist", True)

    def _is_existed(self):
        if hasattr(self, "_is_exist"):
            return bool(getattr(self, "_is_exist"))
        return False

    @property
    def workspace(self):
        """Workspace: 当前数据源所属的工作空间对象"""
        return self._workspace

    @property
    def alias(self):
        """str: 数据源的别名。别名用于在工作空间中唯一标识数据源，可以通过它访问数据源。数据源的别名在创建数据源或打开数据源时给定，
        打开同一个数据源可以使用不同的别名。"""
        if self._jobject is None:
            raise ObjectDisposedError("Datasource")
        try:
            return self._jobject.getAlias()
        except Exception as e:
            try:
                import traceback
                log_error(traceback.format_exc())
                return
            finally:
                e = None
                del e

    @property
    def connection_info(self):
        """DatasourceConnectionInfo : 数据源连接信息"""
        if self._jobject is None:
            raise ObjectDisposedError("Datasource")
        try:
            return DatasourceConnectionInfo._from_java_object(self._jobject.getConnectionInfo())
        except Exception as e:
            try:
                import traceback
                log_error(traceback.format_exc())
                return
            finally:
                e = None
                del e

    @property
    def datasets(self):
        """list[Dataset]:  当前数据源中所有的数据集对象"""
        if self._jobject is None:
            raise ObjectDisposedError("Datasource")
        try:
            temp_dt_dict = OrderedDict()
            jdatasets = self._jobject.getDatasets()
            for i in range(jdatasets.getCount()):
                jdt = jdatasets.get(i)
                handle = self._get_object_handle(jdt)
                if handle in self._dict_dt.keys():
                    temp_dt_dict[handle] = self._dict_dt[handle]
                else:
                    temp_dt_dict[handle] = Dataset._from_java_object(jdt, self)

            self._dict_dt.clear()
            self._dict_dt = temp_dt_dict
            return list(self._dict_dt.values())
        except Exception:
            import traceback
            log_error(traceback.format_exc())
            return

    def _make_java_object(self):
        return self._java_object

    @staticmethod
    def _from_java_object(java_datasource, workspace=None):
        if java_datasource is None:
            raise ValueError("datasource object is None")
        else:
            ds = Datasource()
            ds._java_object = java_datasource
            if workspace is not None:
                ds._workspace = workspace
            else:
                from .ws import Workspace
            ds._workspace = Workspace()
        return ds

    @staticmethod
    def open(conn_info):
        """
        根据数据源连接信息打开数据源。如果设置的连接信息是UDB类型数据源。则会直接返回。不支持直接打开内存数据源，要使用内存数据源，需要使用 :py:meth:`create` 。

        :param conn_info: 数据源连接信息，具体可以参考 :py:meth:`DatasourceConnectionInfo.make`
        :type conn_info:  str or dict or DatasourceConnectionInfo
        :return:  数据源对象
        :rtype: Datasource
        """
        from .ws import Workspace
        return Workspace().open_datasource(conn_info, True)

    @staticmethod
    def create(conn_info):
        """
        根据指定的数据源连接信息，创建新的数据源。

        :param conn_info: 数据源连接信息，具体可以参考 :py:meth:`DatasourceConnectionInfo.make`
        :type conn_info:  str or dict or DatasourceConnectionInfo
        :return:  数据源对象
        :rtype: Datasource
        """
        from .ws import Workspace
        return Workspace().create_datasource(conn_info)

    def get_dataset(self, item):
        """
        根据数据集名称或序号，获取数据集对象

        :param item:  数据集的名称或序号
        :type: str or int
        :return: 数据集对象
        :rtype: Dataset
        """
        if self._jobject is None:
            raise ObjectDisposedError("Datasource")
        else:
            _datasets = self.datasets
            if _datasets is None:
                return
            try:
                if isinstance(item, Dataset):
                    return item
                if isinstance(item, int):
                    if item < 0:
                        item = item + len(_datasets)
                    return _datasets[item]
                if isinstance(item, str):
                    for dt in _datasets:
                        if dt.name == item:
                            return dt

                return
            except Exception as e:
                try:
                    log_error(e)
                    return
                finally:
                    e = None
                    del e

    def __getitem__(self, item):
        return self.get_dataset(item)

    @property
    def type(self):
        """EngineType: 数据源引擎类型"""
        if self._jobject is None:
            raise ObjectDisposedError("Datasource")
        try:
            if self.connection_info is not None:
                return self.connection_info.type
            return
        except Exception as e:
            try:
                log_error(e)
                return
            finally:
                e = None
                del e

    def close(self):
        """
        关闭当前数据源。

        :return: 成功关闭返回 True，否则返回 False
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError("Datasource")
        try:
            if self.workspace is not None:
                if self.workspace.close_datasource(self.alias):
                    self._clear_handle()
                    return True
            return False
        except Exception as e:
            try:
                log_error(e)
                return False
            finally:
                e = None
                del e

    def create_dataset(self, dataset_info, adjust_name=False):
        """
        创建数据集。根据指定的数据集信息创建数据集，如果数据集名称不合法或者已经存在，创建数据集会失败，用户可以设定 adjust_name 为 True 自动
        获取一个合法的数据集名称。

        :param dataset_info: 数据集信息
        :type dataset_info: DatasetVectorInfo or DatasetImageInfo or DatasetGridInfo
        :param bool adjust_name: 当数据集名称不合法时，是否自动调整数据集名称，使用一个合法的数据集名称。默认为 False。
        :return: 创建成功则返回结果数据集对象，否则返回None
        :rtype: Dataset
        """
        if dataset_info is None:
            raise ValueError("datasetInfo is None")
        elif self._jobject is None:
            raise ObjectDisposedError("Datasource")
        try:
            if not self.is_available_dataset_name(dataset_info.name):
                if adjust_name:
                    dataset_info.set_name(self.get_available_dataset_name(dataset_info.name))
            elif isinstance(dataset_info, (DatasetVectorInfo, DatasetImageInfo, DatasetGridInfo)):
                jdt = self._jobject.getDatasets().create(dataset_info._jobject)
            else:
                raise ValueError("invalid datasetInfo, required DatasetVectorInfo,DatasetImageInfo, DatasetGridInfo, but now is " + str(type(dataset_info)))
            return self._add_java_dataset(jdt)
        except:
            import traceback
            log_error(traceback.format_exc())

    def create_vector_dataset(self, name, dataset_type, adjust_name=False):
        """
        根据数据集名称和类型，创建矢量数据集对象。

        :param str name: 数据集名称
        :param dataset_type: 数据集类型，可以为数据集类型枚举值或名称。支持 TABULAR, POINT, LINE, REGION, TEXT, CAD, POINT3D, LINE3D, REGION3D
        :type dataset_type: DatasetType or str
        :param bool adjust_name: 当数据集名称不合法时，是否自动调整数据集名称，使用一个合法的数据集名称。默认为 False。
        :return: 创建成功则返回结果数据集对象，否则返回None
        :rtype: DatasetVector
        """
        if name is None:
            raise ValueError("name is None")
        else:
            dt_type = DatasetType._make(dataset_type)
            if dt_type is None:
                raise ValueError("dataset_type is Invalid")
            if self._jobject is None:
                raise ObjectDisposedError("Datasource")
            try:
                if not self.is_available_dataset_name(name):
                    if adjust_name:
                        name = self.get_available_dataset_name(name)
                return self.create_dataset(DatasetVectorInfo(name, dataset_type), adjust_name)
            except Exception as e:
                try:
                    log_error(e)
                finally:
                    e = None
                    del e

    def create_dataset_from_template(self, template, name, adjust_name=False):
        """
        根据指定的模板数据集，创建新的数据集对象。

        :param Dataset template: 模板数据集
        :param str name: 数据集名称
        :param bool adjust_name: 当数据集名称不合法时，是否自动调整数据集名称，使用一个合法的数据集名称。默认为 False。
        :return: 创建成功则返回结果数据集对象，否则返回None
        :rtype: Dataset
        """
        if template is None:
            raise ValueError("template dataset is None")
        else:
            from ._util import get_input_dataset
            template_dt = get_input_dataset(template)
            if not isinstance(template_dt, Dataset):
                raise ValueError("template must be dataset object, but now is " + str(type(template_dt)))
            if name is None:
                raise ValueError("name is None")
            if self._jobject is None:
                raise ObjectDisposedError("Datasource")
            try:
                if not self.is_available_dataset_name(name):
                    if adjust_name:
                        name = self.get_available_dataset_name(name)
                java_dataset = self._jobject.getDatasets().createFromTemplate(name, template_dt._jobject)
                return self._add_java_dataset(java_dataset)
            except Exception as e:
                try:
                    log_error(e)
                finally:
                    e = None
                    del e

    def create_mosaic_dataset(self, name, prj_coordsys=None, adjust_name=False):
        """
        根据数据集名称和投影信息，创建镶嵌数据集对象。

        :param name: 数据集名称
        :type name: str
        :param prj_coordsys: 指定镶嵌数据集的投影信息。支持 epsg 编码，PrjCoordSys 对象，PrjCoordSysType 类型，xml 或 wkt或投影信息文件。
                             注意，如果传入整型值，必须是 epsg 编码，不能是 PrjCoordSysType 类型的整型值。
        :type prj_coordsys: int or str or PrjCoordSys or PrjCoordSysType
        :param adjust_name: 数据集名称不合法时，是否自动调整数据集名称，使用一个合法的数据集名称。默认为 False。
        :type adjust_name: bool
        :return: 创建成功则返回结果数据集对象，否则返回None
        :rtype: DatasetMosaic
        """
        if name is None:
            raise ValueError("name is None")
        elif not isinstance(prj_coordsys, (PrjCoordSysType, PrjCoordSys, int, str)):
            if prj_coordsys is not None:
                raise TypeError("The type of prj_coordsys must be int or str or PrjCoordSys or PrjCoordSysType object, but now is: " + str(type(prj_coordsys)))
        if self._jobject is None:
            raise ObjectDisposedError("Datasource")
        try:
            if prj_coordsys is None:
                prj_coordsys = PrjCoordSys()
            else:
                prj_coordsys = PrjCoordSys.make(prj_coordsys)
            if not self.is_available_dataset_name(name):
                if adjust_name:
                    name = self.get_available_dataset_name(name)
            java_dataset = self._jobject.getDatasets().createDatasetMosaic(name, prj_coordsys._make_java_object())
            return self._add_java_dataset(java_dataset)
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def get_available_dataset_name(self, name):
        """
        返回一个数据源中未被使用的数据集的名称。数据集的名称限制：数据集名称的长度限制为30个字符（也就是可以为30个英文字母或者15个汉字），
        组成数据集名称的字符可以为字母、汉字、数字和下划线，数据集名称不可以用数字和下划线开头，数据集名称不可以和数据库的保留关键字冲突。

        :param str name: 数据集名称
        :return: 合法的数据集名称
        :rtype: str
        """
        if self._jobject is None:
            raise ObjectDisposedError("Datasource")
        elif self.is_available_dataset_name(name):
            return name
        try:
            return self._jobject.getDatasets().getAvailableDatasetName(name)
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def is_available_dataset_name(self, name):
        """
        判断用户传进来的数据集的名称是否合法。创建数据集时应检查其名称的合法性。

        :param str name: 待检查的数据集名称
        :return: 如果数据集名称合法，返回 True，否则返回 False
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError("Datasource")
        try:
            return self._jobject.getDatasets().isAvailableDatasetName(name)
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def _clear_datasets(self):
        for dt in self._dict_dt.values():
            dt._clear_handle()

        self._dict_dt.clear()

    def _clear_handle(self):
        self._clear_datasets()
        self._java_object = None
        self._workspace = None

    def write_recordset(self, source, out_dataset_name=None):
        """
        将一个记录集对象或数据集对象写到当前数据源中。

        :param source: 待写入的记录集或数据集对象
        :param str out_dataset_name:  结果数据集名称。当名称为空或者不合法时，会自动获取到一个合法的数据集名称
        :return:  写入数据成功返回 DatasetVector，否则返回 None
        :rtype: DatasetVector
        """
        if source is None:
            raise ValueError("source is None")
        elif not isinstance(source, (Recordset, DatasetVector)):
            raise ValueError("source must be Recordset or DatasetVector")
        if self._jobject is None:
            raise ObjectDisposedError("Datasource")
        try:
            if isinstance(source, DatasetVector):
                return self.copy_dataset(source, out_dataset_name)
            if out_dataset_name is None:
                out_dataset_name = "NewDataset"
            dest_name = self.get_available_dataset_name(out_dataset_name)
            java_dataset = self._jobject.recordsetToDataset(source._jobject, dest_name)
            return self._add_java_dataset(java_dataset)
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def write_attr_values(self, data, out_dataset_name=None):
        """
        写入属性数据到属性数据集(DatasetType.TABULAR)中。

        :param data: 待写入的数据。data 必须为一个 list 或者 tuple 或者 set, list(或tuple) 中每个元素项，可以为 list or tuple, 此时
                     data 相当于一个二维的数组，例如::

                     >>> data = [[1,2.0,'a1'], [2,3.0,'a2'], [3,4.0,'a3']]

                     或者::

                     >>> data = [(1,2.0,'a1'), (2,3.0,'a2'), (3,4.0,'a3')]

                     data 中元素项如果不是 list 和 tuple，将会被当作一个元素对待。例如::

                     >>> data = [1,2,3]

                     或::

                     >>> data = ['test1','test2','test3']

                     则最后结果数据集将会含有1列3行的数据集。而对于data中的元素项为 dict 这种，则会将每个 dict 对象作为一个字符串写入::

                     >>> data = [{1:'a'}, {2:'b'}, {3:'c'}]

                     等价于写入了::

                     >>> data = ["{1: 'a'}", "{2: 'b'}", "{3: 'c'}"]

                     另外，用户需要确保list中每个元素项结构相同。程序内部会自动采样最多20条记录，根据采样的字段值类型计算合理的字段类型，具体对应为:

                      - int: FieldType.INT64
                      - str: FieldType.WTEXT
                      - float: FieldType.DOUBLE
                      - bool: FieldType.BOOLEAN
                      - datetime.datetime: FieldType.DATETIME
                      - bytes: FieldType.LONGBINARY
                      - bytearray: FieldType.LONGBINARY
                      - 其他: FieldType.WTEXT

        :type data: list or tuple
        :param str out_dataset_name: 结果数据集名称。当名称为空或者不合法时，会自动获取到一个合法的数据集名称
        :return: 写入数据成功返回 DatasetVector，否则返回 None
        :rtype: DatasetVector
        """
        if self._jobject is None:
            raise ObjectDisposedError("Datasource")
        elif data is None:
            raise ValueError("data is None")
        if not isinstance(data, (list, tuple)):
            raise ValueError("data required list or tuple, but now is " + str(type(data)))
        if len(data) == 0:
            raise ValueError("count of data is 0")
        try:
            from ._util import from_value_get_field_type
            if out_dataset_name is None:
                out_dataset_name = "NewDataset"
            destName = self.get_available_dataset_name(out_dataset_name)
            resultDt = self.create_dataset(DatasetVectorInfo(destName, DatasetType.TABULAR), True)
            if resultDt is None:
                log_error("Failed to create result dataset : " + destName)
                return
            fieldTypes = []
            select_random_count = min(20, len(data))
            import random
            for i in range(select_random_count):
                row_index = random.randint(0, len(data) - 1)
                row_values = data[row_index]
                if row_values is None:
                    continue
                if not isinstance(row_values, (list, tuple)):
                    row_values = [
                     row_values]
                for k in range(len(row_values)):
                    _fieldType = from_value_get_field_type(row_values[k])
                    if k > len(fieldTypes) - 1:
                        fieldTypes.append(_fieldType)
                    elif fieldTypes[k] is None:
                        fieldTypes[k] = _fieldType
                    elif _fieldType is not None and fieldTypes[k] != _fieldType:
                        fieldTypes[k] = FieldType.WTEXT

            fieldInfos = []
            for i in range(len(fieldTypes)):
                fieldInfos.append(FieldInfo("Field" + str(i), fieldTypes[i]))

            resultDt.open()
            resultDt.create_fields(fieldInfos)
            rd = resultDt.get_recordset(True, CursorType.DYNAMIC)
            rd.batch_edit()
            for i in range(len(data)):
                row_values = data[i]
                if row_values is None:
                    continue
                if not isinstance(row_values, (list, tuple)):
                    row_values = [
                     row_values]
                try:
                    rd.add(None)
                    for j in range(len(fieldInfos)):
                        rd.set_value(fieldInfos[j].name, row_values[j])

                except Exception as e:
                    try:
                        log_warning(e)
                    finally:
                        e = None
                        del e

            rd.batch_update()
            rd.close()
            return resultDt
        except:
            import traceback
            log_error(traceback.format_exc())

    def write_spatial_data(self, data, out_dataset_name=None, values=None):
        """
        将空间数据(Point2D, Point3D, Rectangle, Geometry) 等写入到矢量数据集中。

        :param data:  待写入的数据。data 必须为一个 list 或者 tuple 或者 set, list(或tuple) 中每个元素项，可以为 Point2D, Point, GeoPoint, GeoLine, GeoRegion, Rectangle:
                        - 如果 data 中所有的元素都是 Point2D 或 GeoPoint，则会创建一个点数据集
                        - 如果 data 中所有的元素都是 Point3D 或 GeoPoint3D，则会创建一个三维点数据集
                        - 如果 data 中所有的元素都是 GeoLine，则会创建一个线数据集
                        - 如果 data 中所有的元素都是 Rectangle 或 GeoRegion，则会创建一个面数据集
                        - 否则，将会创建一个 CAD 数据集。
        :type data: list o tuple
        :param str out_dataset_name:  结果数据集名称。当名称为空或者不合法时，会自动获取到一个合法的数据集名称
        :param values:  空间数据要写到数据集中的属性字段值。如果不为 None，必须为 list 或 tuple，且长度必须与 data 长度相同。
                        values 中每个元素项可以为 list 或 tuple，此时 values 相当于一个二维的数组，例如::

                        >>> values = [[1,2.0,'a1'], [2,3.0,'a2'], [3,4.0,'a3']]

                        或者

                        >>> values = [(1,2.0,'a1'), (2,3.0,'a2'), (3,4.0,'a3')]

                        values 中元素项如果不是 list 和 tuple，将会被当作一个元素对待。例如::

                        >>> values = [1,2,3]

                        或::

                        >>> values = ['test1','test2','test3']

                        则最后结果数据集将会含有1列3行的数据集。而对于data中的元素项为 dict 这种，则会将每个 dict 对象作为一个字符串写入::

                        >>> data = [{1:'a'}, {2:'b'}, {3:'c'}]

                        等价于写入了::

                        >>> values = ["{1: 'a'}", "{2: 'b'}", "{3: 'c'}"]

                        另外，用户需要确保list中每个元素项结构相同。程序内部会自动采样最多20条记录，根据采样的字段值类型计算合理的字段类型，具体对应为:

                         - int: FieldType.INT64
                         - str: FieldType.WTEXT
                         - float: FieldType.DOUBLE
                         - bool: FieldType.BOOLEAN
                         - datetime.datetime: FieldType.DATETIME
                         - bytes: FieldType.LONGBINARY
                         - bytearray: FieldType.LONGBINARY
                         - 其他: FieldType.WTEXT

        :return: 写入数据成功返回 DatasetVector，否则返回 None
        :rtype: DatasetVector
        """
        if self._jobject is None:
            raise ObjectDisposedError("Datasource")
        else:
            if data is None:
                raise ValueError("data is None")
            else:
                from ._util import from_value_get_field_type
                if isinstance(data, Recordset):
                    return self.write_recordset(data, out_dataset_name)
                if not isinstance(data, (list, tuple)):
                    raise ValueError("required list or tuple, but now is " + str(type(data)))
                if len(data) == 0:
                    raise ValueError("count of data is 0")
                if values is not None and len(values) != len(data):
                    raise ValueError("values count must be equal with spatial data")
            try:
                if out_dataset_name is None:
                    out_dataset_name = "NewDataset"
                else:
                    destName = self.get_available_dataset_name(out_dataset_name)
                    datasetType = None
                    fieldTypes = None
                    select_random_count = min(20, len(data))
                    import random
                    for i in range(select_random_count):
                        row_index = random.randint(0, len(data) - 1)
                        row_data = data[row_index]
                        if row_data is not None:
                            if isinstance(row_data, (Point2D, GeoPoint)):
                                if datasetType is None:
                                    datasetType = DatasetType.POINT
                                else:
                                    if datasetType != DatasetType.POINT:
                                        datasetType = DatasetType.CAD
                            else:
                                if isinstance(row_data, (Point3D, GeoPoint3D)):
                                    if datasetType is None:
                                        datasetType = DatasetType.POINT3D
                                    else:
                                        if datasetType != DatasetType.POINT3D:
                                            datasetType = DatasetType.CAD
                                else:
                                    if isinstance(row_data, GeoLine):
                                        if datasetType is None:
                                            datasetType = DatasetType.LINE
                                        else:
                                            if datasetType != DatasetType.LINE:
                                                datasetType = DatasetType.CAD
                                    else:
                                        if isinstance(row_data, (Rectangle, GeoRegion)):
                                            if datasetType is None:
                                                datasetType = DatasetType.REGION
                                            else:
                                                if datasetType != DatasetType.REGION:
                                                    datasetType = DatasetType.CAD
                                        else:
                                            datasetType = DatasetType.CAD
                        if values is not None:
                            row_values = values[row_index]
                            if row_values is None:
                                continue
                            if not isinstance(row_values, (list, tuple)):
                                row_values = [
                                 row_values]
                            if fieldTypes is None:
                                fieldTypes = []
                            for k in range(len(row_values)):
                                _fieldType = from_value_get_field_type(row_values[k])
                                if k > len(fieldTypes) - 1:
                                    fieldTypes.append(_fieldType)
                                elif fieldTypes[k] is None:
                                    fieldTypes[k] = _fieldType
                                elif _fieldType is not None and fieldTypes[k] != _fieldType:
                                    fieldTypes[k] = FieldType.WTEXT

                    resultDt = self.create_dataset(DatasetVectorInfo(destName, datasetType), True)
                    if resultDt is None:
                        log_error("Failed to create result dataset : " + destName)
                        return
                        resultDt.open()
                        if values is not None:
                            fieldInfos = []
                            for i in range(len(fieldTypes)):
                                fieldInfos.append(FieldInfo("Field" + str(i), fieldTypes[i]))

                            resultDt.create_fields(fieldInfos)
                    else:
                        fieldInfos = None
                rd = resultDt.get_recordset(True, CursorType.DYNAMIC)
                rd.batch_edit()
                i = -1
                for item in data:
                    i += 1
                    try:
                        if isinstance(item, Rectangle):
                            isAdd = rd.add(GeoRegion(item))
                        else:
                            if isinstance(item, Point2D):
                                isAdd = rd.add(GeoPoint(item))
                            else:
                                if isinstance(item, Point3D):
                                    isAdd = rd.add(GeoPoint3D(item))
                                else:
                                    isAdd = rd.add(item)
                        if isAdd:
                            if values is not None:
                                row_data = values[i]
                                if row_data is not None:
                                    if not isinstance(row_data, (list, tuple)):
                                        row_data = [
                                         row_data]
                                    for j in range(len(fieldInfos)):
                                        rd.set_value(fieldInfos[j].name, row_data[j])

                    except Exception as e:
                        try:
                            log_warning(e)
                        finally:
                            e = None
                            del e

                rd.batch_update()
                rd.close()
                return resultDt
            except Exception as e:
                try:
                    log_error(e)
                finally:
                    e = None
                    del e

    def write_features(self, data, out_dataset_name=None):
        """
        将要素对象写入到数据集中。

        :param data: 写入的要素对象集合。用户需确保集合中所有要素的结构必须相同，包括几何对象类型和字段信息都相同。
        :type data: list[Feature] or tuple[Feature]
        :param str out_dataset_name: 结果数据集名称。当名称为空或者不合法时，会自动获取到一个合法的数据集名称
        :return: 写入成功返回结果数据集对象，否则返回 None
        :rtype: DatasetVector
        """
        if self._jobject is None:
            raise ObjectDisposedError("Datasource")
        elif data is None:
            raise ValueError("data is None")
        if len(data) == 0:
            raise ValueError("count of data is 0")
        try:
            from ._util import get_dataset_type_from_geometry_type
            if out_dataset_name is None:
                out_dataset_name = "NewDataset"
            else:
                destName = self.get_available_dataset_name(out_dataset_name)
                features = list(filter((lambda f: isinstance(f, Feature)), data))
                fieldInfos = features[0].field_infos
                if features[0].geometry is None:
                    resultDt = self.create_dataset(DatasetVectorInfo(destName, DatasetType.TABULAR), True)
                else:
                    datasetType = get_dataset_type_from_geometry_type(features[0].geometry.type)
                resultDt = self.create_dataset(DatasetVectorInfo(destName, datasetType), True)
            if resultDt is None:
                log_error("Failed to create result dataset : " + destName)
                return
            resultDt.open()
            resultDt.create_fields(fieldInfos)
            rd = resultDt.get_recordset(True, CursorType.DYNAMIC)
            rd.batch_edit()
            for i in range(len(features)):
                try:
                    rd.add(features[i].geometry, features[i].get_values(True, True))
                except Exception as e:
                    try:
                        log_warning(e)
                    finally:
                        e = None
                        del e

            rd.batch_update()
            rd.close()
            return resultDt
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def copy_dataset(self, source, out_dataset_name=None, encode_type=None, progress=None):
        r"""
        复制数据集。复制数据集之前必须保证当前数据源已经打开而且可写。复制数据集时，可通过 EncodeType 参数来对数据集的编码方式进行修改。
        有关数据集存储的编码方式请参见 EncodeType 枚举类型。由于CAD数据集不支持任何编码，对 CAD 数据集进行复制操作时设置的 EncodeType 无效

        :param source:  要复制的源数据集。可以为数据集对象，也可以是数据源别名和数据集名称的组合，数据源名称和数据集名称组合可以使用 "|","\\\","/"任意一种。
                        例如::

                        >>> source = 'ds_alias/point_dataset'

                        或者::

                        >>> source = 'ds_alias|point_dataset'

        :type source: Dataset or str
        :param str out_dataset_name:  目标数据集的名称。当名称为空或者不合法时，会自动获取到一个合法的数据集名称
        :param encode_type: 数据集的编码方式。可以为 :py:class:`EncodeType` 枚举值或名称。
        :type encode_type:  EncodeType or str
        :param function progress: 处理进度信息的函数，具体参考 :py:class:`.StepEvent`。
        :return: 复制成功返回结果数据集对象，否则返回 None
        :rtype: Dataset
        """
        if self._jobject is None:
            raise ObjectDisposedError("Datasource")
        elif source is None:
            raise ValueError("source is None")
        else:
            from ._util import get_input_dataset
            if isinstance(source, str):
                if source.find("/") == -1:
                    if source.find("\\") == -1:
                        if source.find("|") == -1:
                            source = self.alias + "|" + source
            source_dt = get_input_dataset(source)
            if not isinstance(source_dt, Dataset):
                raise ValueError("source must be Dataset, but is " + str(type(source_dt)))
            if out_dataset_name is None:
                out_dataset_name = source_dt.name + "_copy"
            destName = self.get_available_dataset_name(out_dataset_name)
            _encodType = EncodeType._make(encode_type, source_dt.encode_type)
            if _encodType is not None:
                _encodType = _encodType._jobject
            listener = None
            if progress is not None:
                if safe_start_callback_server():
                    try:
                        listener = ProgressListener(progress, "CopyDataset")
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
                java_dataset = self._jobject.copyDataset(source_dt._jobject, destName, _encodType)
            except Exception as e:
                try:
                    log_error(e)
                    java_dataset = None
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

        return self._add_java_dataset(java_dataset)

    def change_password(self, old_password, new_password):
        """
        修改已经打开的数据源的密码

        :param str old_password: 旧密码
        :param str new_password: 新的密码
        :return: 成功返回True，否则返回False
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError("Datasource")
        try:
            return self._jobject.changePassword(old_password, new_password)
        except Exception as e:
            try:
                log_error(e)
                return False
            finally:
                e = None
                del e

    def last_date_updated(self):
        """
        获取数据源最后更新的时间

        :rtype: datetime.datetime
        """
        if self._jobject is None:
            raise ObjectDisposedError("Datasource")
        try:
            _t = self._jobject.getDateLastUpdated()
            return datetime.datetime.strptime(_t, "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            try:
                log_error(e)
                return
            finally:
                e = None
                del e

    @property
    def description(self):
        """str: 返回用户添加的关于数据源的描述信息"""
        if self._jobject is None:
            raise ObjectDisposedError("Datasource")
        try:
            return self._jobject.getDescription()
        except Exception as e:
            try:
                log_error(e)
                return
            finally:
                e = None
                del e

    def set_description(self, description):
        """
        设置用户添加的关于数据源的描述信息。用户可以在描述信息里加入你想加入的任何信息，例如建立数据源的人员、数据的来源、数据的主要内容、
        数据的精度、质量等信息，这些信息对于维护数据具有重要的意义

        :param str description: 用户添加的关于数据源的描述信息
        """
        if self._jobject is None:
            raise ObjectDisposedError("Datasource")
        try:
            self._jobject.setDescription(description)
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def is_opened(self):
        """
        返回数据源是否打开的状态，如果数据源处于打开状态，返回 true，如果数据源被关闭，则返回 false。

        :return: 数据源是否打开的状态
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError("Datasource")
        try:
            return self._jobject.isOpened()
        except Exception as e:
            try:
                log_error(e)
                return False
            finally:
                e = None
                del e

    def is_readonly(self):
        """
        返回数据源是否以只读方式打开。对文件型数据源，如果只读方式打开，就是共享的，可以打开多次；如果以非只读方式打开，则只能打开一次。
        对于影像数据源(IMAGEPLUGINS 引擎类型)只会以只读方式打开。

        :return: 数据源是否以只读方式打开
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError("Datasource")
        try:
            return self._jobject.isReadOnly()
        except Exception as e:
            try:
                log_error(e)
                return False
            finally:
                e = None
                del e

    def refresh(self):
        """对数据库类型的数据源进行刷新"""
        if self._jobject is None:
            raise ObjectDisposedError("Datasource")
        try:
            self._jobject.refresh()
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def flush(self, dataset_name=None):
        """
        将内存中暂未写入数据库中的数据保存到数据库

        :param str dataset_name: 需要刷新的数据集名称。当传入长度为空的字符串或None，表示对所有数据集进行刷新；否则对指定名字的数据集进行刷新。
        :return:  成功返回True，否则返回False
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError("Datasource")
        try:
            if dataset_name is None:
                dataset_name = ""
            return self._jobject.flush(str(dataset_name))
        except Exception as e:
            try:
                log_error(e)
                return False
            finally:
                e = None
                del e

    def inner_point_to_dataset(self, source_dataset, out_dataset_name=None):
        """
        创建矢量数据集的内点数据集,并把矢量数据集中几何对象的属性复制到相应的点数据集属性表中

        :param source_dataset: 要计算内点数据集的矢量数据集
        :type source_dataset: DatasetVector or str
        :param str out_dataset_name: 目标数据集的名称。当名称为空或者不合法时，会自动获取到一个合法的数据集名称
        :return: 创建成功返回内点数据集。创建失败返回 None
        :rtype: DatasetVector
        """
        if source_dataset is None:
            raise ValueError("srcDataset is None")
        elif self._jobject is None:
            raise ObjectDisposedError("Datasource")
        try:
            from ._util import get_input_dataset
            dt = get_input_dataset(source_dataset)
            if dt is None:
                log_error("Failed to get dataset" + str(source_dataset))
                return
            elif out_dataset_name is None:
                dest_name = dt.name + "_innerPoint"
            else:
                dest_name = out_dataset_name
            dest_name = self.get_available_dataset_name(dest_name)
            java_dataset = self._jobject.innerPointToDataset(dt._jobject, dest_name)
            return self._add_java_dataset(java_dataset)
        except Exception as e:
            try:
                log_error(e)
                return
            finally:
                e = None
                del e

    def label_to_text_dataset(self, source_dataset, text_field, text_style=None, out_dataset_name=None):
        """
        用于将数据集的属性字段生成一个文本数据集。通过此方法生成的文本数据集中的文本对象，均以其对应的空间对象的内点作为对应的锚点，
        对应的空间对象即当前文本对象的内容来源于相应空间对象的属性值。

        :param source_dataset: 要计算内点数据集的矢量数据集
        :type source_dataset: DatasetVector or str
        :param str text_field: 要转换的属性字段的名称。
        :param TextStyle text_style:  结果文本对象的风格
        :param str out_dataset_name: 目标数据集的名称。当名称为空或者不合法时，会自动获取到一个合法的数据集名称
        :return:  成功返回一个文本数据集，否则返回None
        :rtype: DatasetVector
        """
        if source_dataset is None:
            raise ValueError("srcDataset is None")
        elif self._jobject is None:
            raise ObjectDisposedError("Datasource")
        try:
            from ._util import get_input_dataset
            dt = get_input_dataset(source_dataset)
            if dt is None:
                log_error("Failed to get dataset" + str(source_dataset))
                return
            if not isinstance(dt, DatasetVector):
                raise ValueError("required DatasetVector, but now is " + str(type(dt)))
            elif out_dataset_name is None:
                dest_name = dt.name + "_text"
            else:
                dest_name = out_dataset_name
            dest_name = self.get_available_dataset_name(dest_name)
            if text_style is None:
                text_style = TextStyle()
            java_dataset = self._jobject.labelToTextDataset(dt._jobject, dest_name, text_field, text_style._jobject)
            return self._add_java_dataset(java_dataset)
        except Exception as e:
            try:
                log_error(e)
                return
            finally:
                e = None
                del e

    def field_to_point_dataset(self, source_dataset, x_field, y_field, out_dataset_name=None):
        """
        从一个矢量数据集的属性表中的 X、Y 坐标字段创建点数据集。即以该矢量数据集的属性表中的 X 、Y 坐标字段作为数据集的 X、Y 坐标来创建点数据集。

        :param source_dataset: 关联属性表中带有坐标字段的矢量数据集
        :type source_dataset: DatasetVector or str
        :param str x_field: 表示点横坐标的字段。
        :param str y_field: 表示点纵坐标的字段。
        :param str out_dataset_name: 目标数据集的名称。当名称为空或者不合法时，会自动获取到一个合法的数据集名称
        :return: 成功返回一个点数据集，否则返回None
        :rtype: DatasetVector
        """
        if source_dataset is None:
            raise ValueError("srcDataset is None")
        elif self._jobject is None:
            raise ObjectDisposedError("Datasource")
        try:
            from ._util import get_input_dataset
            dt = get_input_dataset(source_dataset)
            if dt is None:
                log_error("Failed to get dataset" + str(source_dataset))
                return
            if not isinstance(dt, DatasetVector):
                raise ValueError("required DatasetVector, but now is " + str(type(dt)))
            elif out_dataset_name is None:
                dest_name = dt.name + "_point"
            else:
                dest_name = out_dataset_name
            dest_name = self.get_available_dataset_name(dest_name)
            java_dataset = self._jobject.fieldToPointDataset(dt._jobject, dest_name, x_field, y_field)
            return self._add_java_dataset(java_dataset)
        except Exception as e:
            try:
                log_error(e)
                return
            finally:
                e = None
                del e

    @property
    def prj_coordsys(self):
        """PrjCoordSys: 获取数据源的投影信息"""
        if self._jobject is None:
            raise ObjectDisposedError("Datasource")
        try:
            return PrjCoordSys._from_java_object(self._jobject.getPrjCoordSys())
        except Exception as e:
            try:
                log_error(e)
                return
            finally:
                e = None
                del e

    def set_prj_coordsys(self, prj):
        """
        设置数据源的投影信息

        :param PrjCoordSys prj: 投影信息
        """
        if self._jobject is None:
            raise ObjectDisposedError("Datasource")
        try:
            prj = PrjCoordSys.make(prj)
            self._jobject.setPrjCoordSys(prj._jobject)
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def contains(self, name):
        """
        检查当前数据源中是否有指定名称的数据集

        :param str name: 数据集名称
        :return: 当前数据源含有指定名称的数据集返回 True，否则返回 False
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError("Datasource")
        try:
            return self._jobject.getDatasets().contains(name)
        except Exception as e:
            try:
                log_error(e)
                return False
            finally:
                e = None
                del e

    def delete(self, item):
        """
        删除指定的数据集，可以为数据集名称或序号

        :param item: 要删除的数据集的名称或序号
        :type item: str or int
        :return: 删除数据集成功返回True，否则返回False
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError("Datasource")
        try:
            if isinstance(item, int):
                if item < 0:
                    item = item + len(self._dict_dt.keys())
                i = 0
                target_handle = None
                target_dt = None
                for handle, dt in self._dict_dt.items():
                    if i == item:
                        target_handle = handle
                        target_dt = dt
                        break
                    i += 1

                if target_handle:
                    if target_dt:
                        target_dt._clear_handle()
                        del self._dict_dt[target_handle]
                        return self._jobject.getDatasets().delete(item)
                return False
            if isinstance(item, str):
                target_handle = None
                target_dt = None
                for handle, dt in self._dict_dt.items():
                    if dt.name == item:
                        target_dt = dt
                        target_handle = handle

                if target_handle:
                    target_dt._clear_handle()
                    del self._dict_dt[target_handle]
                    return self._jobject.getDatasets().delete(item)
                return False
        except Exception as e:
            try:
                log_error(e)
                return False
            finally:
                e = None
                del e

        return False

    def delete_all(self):
        """删除当前数据源下所有的数据集"""
        if self._jobject is None:
            raise ObjectDisposedError("Datasource")
        try:
            self._clear_datasets()
            self._jobject.getDatasets().deleteAll()
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def get_count(self):
        """
        获取数据集的个数

        :rtype: int
        """
        if self._jobject is None:
            raise ObjectDisposedError("Datasource")
        try:
            return self._jobject.getDatasets().getCount()
        except Exception as e:
            try:
                log_error(e)
                return 0
            finally:
                e = None
                del e

    def index_of(self, name):
        """
        返回给定数据集名称对应的数据集在数据集集合中所处的索引值

        :param str name: 数据集名称
        :rtype: int
        """
        if self._jobject is None:
            raise ObjectDisposedError("Datasource")
        try:
            _index = self._jobject.getDatasets().indexOf(name)
        except Exception as e:
            try:
                log_error(e)
                _index = -1
            finally:
                e = None
                del e

        if _index >= 0:
            return _index
        raise ValueError(name + "not found")

    def to_json(self):
        """
        将数据源返回为 json 格式字符串。具体返回数据源连接信息的 json 字符串，即使用 :py:class:`DatasourceConnectionInfo.to_json` 。

        :rtype: str
        """
        if self._jobject is None:
            raise ObjectDisposedError("Datasource")
        return self.connection_info.to_json()

    @staticmethod
    def from_json(value):
        """
        从 json 格式字符串打开数据源。json 串格式为 DatasourceConnectionInfo 的 json 字符串格式。具体参
        :py:meth:`DatasourceConnectionInfo.to_json` 和 :py:meth:`to_json`

        :param str value: json 字符串格式
        :return: 数据源对象
        :rtype: Datasource
        """
        connInfo = DatasourceConnectionInfo.from_json(value)
        from .ws import Workspace
        return Workspace().open_datasource(connInfo, True)

    def _add_java_dataset(self, java_dataset):
        if java_dataset is None:
            return
        handle = self._get_object_handle(java_dataset)
        if handle == 0:
            raise ValueError("Dataset is disposed (handle == 0)")
        dt = Dataset._from_java_object(java_dataset, self)
        self._dict_dt[handle] = dt
        return dt
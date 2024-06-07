# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/_jsuperpy\data\ws.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 51813 bytes
from .._logger import log_error, log_info
from .._gateway import get_jvm
from ..enums import WorkspaceVersion, WorkspaceType, EngineType
from ._jvm import JVMBase
from .ex import DatasourceOpenedFailedError, ObjectDisposedError, DatasourceCreatedFailedError
from .ds import *
from collections import OrderedDict
__all__ = [
 'WorkspaceConnectionInfo', 'Workspace', 'open_datasource', 'get_datasource', 
 'close_datasource', 
 'list_datasources', 'create_datasource', 'list_maps', 
 'get_map', 'remove_map', 'add_map']

class WorkspaceConnectionInfo(JVMBase):
    __doc__ = "\n    工作空间连接信息类。包括了进行工作空间连接的所有信息，如所要连接的服务器名称，数据库名称，用户名，密码等。对不同类型的工作空间，所以在使用该类所\n    包含的成员时，请注意该成员所适用的工作空间类型。\n    "

    def __init__(self, server=None, workspace_type=None, version=None, driver=None, database=None, name=None, user=None, password=None):
        """
        初始化工作空间链接信息对象。

        :param str server:  数据库服务器名或文件名
        :param workspace_type:  工作空间的类型
        :type workspace_type: WorkspaceType or str
        :param version: 工作空间的版本
        :type version: WorkspaceVersion or str
        :param str driver: 设置使用 ODBC 连接的数据库的驱动程序名，对目前支持的数据库工作空间中，SQL Server 数据库使用 ODBC 连接，SQL Server 数据库的驱动程序名如为 SQL Server 或 SQL Native Client
        :param str database: 工作空间连接的数据库名
        :param str name: 工作空间在数据库中的名
        :param str user: 登录数据库的用户名
        :param str password: 登录工作空间连接的数据库或文件的密码。
        """
        JVMBase.__init__(self)
        self._server = None
        self._driver = None
        self._database = None
        self._name = None
        self._user = None
        self._password = None
        self._workspaceType = None
        self._version = WorkspaceVersion.UGC70
        self.set_server(server)
        self.set_driver(driver)
        self.set_database(database)
        self.set_name(name)
        self.set_user(user)
        self.set_password(password)
        self.set_type(workspace_type)
        self.set_version(version)

    @property
    def server(self):
        """str: 数据库服务器名或文件名"""
        return self._server

    def set_server(self, value):
        """
        设置数据库服务器名或文件名。

        :param str value: 对于 Oracle 数据库，其服务器名为其 TNS 服务名称； 对于 SQL Server 数据库，其服务器名为其系统的 DNS（Database Source Name）名称；对于 SXWU 和 SMWU 文件，其服务器名称为其文件名称，其中包括路径名称和文件的后缀名。特别地，此处的路径为绝对路径。
        :return: self
        :rtype: WorkspaceConnectionInfo
        """
        if value is not None:
            self._server = str(value)
        return self

    @property
    def name(self):
        """str: 工作空间在数据库中的名称，对文件型的工作空间，此名称为空"""
        return self._name

    def set_name(self, value):
        """
        设置工作空间在数据库中的名称。

        :param str value: 工作空间在数据库中的名称，对文件型的工作空间，此名称设为空
        :return: self
        :rtype: WorkspaceConnectionInfo
        """
        if value is not None:
            self._name = str(value)
        return self

    @property
    def database(self):
        """str: 工作空间连接的数据库名。对数据库类型工作空间适用"""
        return self._database

    def set_database(self, value):
        """
        设置工作空间连接的数据库名。对数据库类型工作空间适用

        :param str value:  工作空间连接的数据库名
        :return: self
        :rtype: WorkspaceConnectionInfo
        """
        if value is not None:
            self._database = value
        return self

    @property
    def driver(self):
        """str: 使用 ODBC 连接的数据库的驱动程序名"""
        return self._driver

    def set_driver(self, value):
        """
        设置 使用 ODBC 连接的数据库的驱动程序名。对目前支持的数据库工作空间中，SQL Server 数据库使用 ODBC 连接，SQL Server 数据库的驱动
        程序名如为 SQL Server 或 SQL Native Client。

        :param str value:   使用 ODBC 连接的数据库的驱动程序名
        :return: self
        :rtype: WorkspaceConnectionInfo

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
        设置登录数据库的用户名。对数据库类型工作空间适用。

        :param str value:  登录数据库的用户名
        :return: self
        :rtype: WorkspaceConnectionInfo
        """
        if value is not None:
            self._user = value
        return self

    @property
    def password(self):
        """str: 登录工作空间连接的数据库或文件的密码"""
        return self._password

    def set_password(self, value):
        """
        设置登录工作空间连接的数据库或文件的密码。此密码的设置只对 Oracle 和 SQL 数据源有效，对本地（UDB）数据源无效。

        :param str value:  登录工作空间连接的数据库或文件的密码
        :return: self
        :rtype: WorkspaceConnectionInfo
        """
        if value is not None:
            self._password = value
        return self

    @property
    def type(self):
        """WorkspaceType: 工作空间的类型。工作空间可以存储在文件中，也可以存储在数据库中。目前支持的文件型的工作空间的类型为 SXWU 格式和 SMWU 格式的工作空间；
        数据库型工作空间为 ORACLE 格式和 SQL 格式的工作空间；默认的工作空间类型为未存储的工作空间"""
        if self.server is not None:
            if self._workspaceType is None:
                self._workspaceType = WorkspaceConnectionInfo._parse_type_and_version_from_server(self.server)
        return self._workspaceType

    def set_type(self, value):
        """
        设置工作空间的类型。

        :param value:  工作空间的类型
        :type value: WorkspaceType or str
        :return: self
        :rtype: WorkspaceConnectionInfo

        """
        if value is not None:
            self._workspaceType = WorkspaceType._make(value)
        return self

    @property
    def version(self):
        """WorkspaceVersion: 工作空间的版本。默认为 UGC70."""
        return self._version

    def set_version(self, value):
        """
        设置工作空间版本。

        :param value:  工作空间的版本
        :type value: WorkspaceVersion or str
        :return: self
        :rtype: WorkspaceConnectionInfo

        例如，设置工作空间版本为 UGC60::

            >>> conn_info = WorkspaceConnectionInfo()
            >>> conn_info.set_version('UGC60')
            >>> print(conn_info.version)
            WorkspaceVersion.UGC60

        """
        if value is not None:
            if isinstance(value, str):
                self._version = WorkspaceVersion[value]
            else:
                if isinstance(value, WorkspaceVersion):
                    self._version = value
        return self

    @staticmethod
    def _parse_type_and_version_from_server(server):
        """从文件型工作空间路径名称中解析出工作空间类型。"""
        _server = server.lower()
        if _server.endswith(".sxwu"):
            return WorkspaceType.SXWU
        if _server.endswith(".smwu"):
            return WorkspaceType.SMWU
        return

    def _make_java_object(self):
        if self._java_object is None:
            java_connection_info = self._jvm.com.supermap.data.WorkspaceConnectionInfo()
            if self.type is not None:
                java_connection_info.setType(self.type._jobject)
            java_connection_info.setServer(self.server)
            java_connection_info.setDriver(self.driver)
            java_connection_info.setDatabase(self.database)
            java_connection_info.setName(self.name)
            java_connection_info.setUser(self.user)
            java_connection_info.setPassword(self.password)
            if self.version is not None:
                java_connection_info.setVersion(self.version._jobject)
            self._java_object = java_connection_info
        return self._java_object

    @staticmethod
    def _from_java_object(java_info):
        info = WorkspaceConnectionInfo((java_info.getServer()), (WorkspaceType._make(java_info.getType().name())),
          driver=(java_info.getDriver()),
          database=(java_info.getDatabase()),
          name=(java_info.getName()),
          user=(java_info.getUser()),
          password=(java_info.getPassword()),
          version=(WorkspaceVersion._make(java_info.getVersion())))
        return info


class Workspace(JVMBase):
    __doc__ = "\n    工作空间是用户的工作环境，主要完成数据的组织和管理，包括打开、关闭、创建、保存工作空间文件。工作空间（Workspace）是 SuperMap 中的一个重要的\n    概念，工作空间存储了一个工程项目（同一个事务过程）中所有的数据源，地图的组织关系。通过工作空间对象可以管理数据源和地图。工作空间中只存储数据源的\n    连接信息和位置等，实际的数据源都是存储在数据库或者 UDB 中。工作空间只存储地图的一些配置信息，如地图包含图层的个数，图层引用的数据集，地图范围，\n    背景风格等。在当前版本中，一个程序只能存在一个工作空间对象，如果用户没有打开特定的工作空间，程序将默认创建一个工作空间对象。用户如果需要打开新的\n    工作空间对象，需要先将当前工作空间保存和关闭，否则，存储在工作空间中的一些信息可能会丢失。\n\n    例如，创建数据源对象::\n\n        >>> ws = Workspace()\n        >>> ws.create_datasource(':memory:')\n        >>> print(len(ws.datasources))\n        1\n        >>> ws_a = Workspace()\n        >>> ws_a.create_datasource(':memory:')\n        >>> ws == ws_a\n        True\n        >>> print(len(ws_a.datasources))\n        2\n        >>> ws.close()\n\n    "
    _created_python = False
    _Workspace__instance = None
    _ds_dict = OrderedDict()

    def __init__(self):
        pass

    def __new__(cls):
        if cls._Workspace__instance is None:
            cls._Workspace__instance = object.__new__(cls)
            JVMBase.__init__(cls._Workspace__instance)
            _jworkspace = get_jvm().com.supermap.jsuperpy.RegisterWorkspace.getWorkspace()
            if _jworkspace is None:
                _jworkspace = get_jvm().com.supermap.jsuperpy.RegisterWorkspace.newPythonWorkspace()
            cls._Workspace__instance._java_object = _jworkspace
            cls._Workspace__instance._created_python = get_jvm().com.supermap.jsuperpy.RegisterWorkspace.isCreatedByPython()
        return cls._Workspace__instance

    def _make_java_object(self):
        return self._java_object

    @property
    def datasources(self):
        """list[Datasource]: 当前工作空间下的所有数据源对象。"""
        if self._java_object is not None:
            try:
                java_datasources = self._java_object.getDatasources()
                temp_ds_dict = OrderedDict()
                for i in range(java_datasources.getCount()):
                    handle = self._get_object_handle(java_datasources.get(i))
                    if handle == 0:
                        continue
                    if handle in self._ds_dict:
                        temp_ds_dict[handle] = self._ds_dict[handle]
                    else:
                        temp_ds_dict[handle] = Datasource._from_java_object(java_datasources.get(i))

                self._ds_dict.clear()
                self._ds_dict = temp_ds_dict
                return list(self._ds_dict.values())
            except Exception as e:
                try:
                    raise e
                finally:
                    e = None
                    del e

        else:
            raise ObjectDisposedError("Workspace")

    @property
    def caption(self):
        """str: 工作空间显示名称，便于用户做一些标识。"""
        if self._jobject is None:
            raise ObjectDisposedError("Workspace")
        try:
            return self._jobject.getCaption()
        except Exception as e:
            try:
                log_error(e)
                return
            finally:
                e = None
                del e

    def set_caption(self, caption):
        """
        设置工作空间显示名称。

        :param str caption: 工作空间显示名称
        """
        if caption is None:
            raise ValueError("caption is None")
        elif self._jobject is None:
            raise ObjectDisposedError("Workspace")
        try:
            self._jobject.setCaption(caption)
        except Exception as e:
            try:
                raise e
            finally:
                e = None
                del e

    @property
    def description(self):
        """str: 用户加入的对当前工作空间的描述或说明性信息"""
        if self._jobject is None:
            raise ObjectDisposedError("Workspace")
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
        设置用户加入的对当前工作空间的描述或说明性信息

        :param str description: 用户加入的对当前工作空间的描述或说明性信息
        """
        if description is None:
            raise ValueError("description is None")
        elif self._jobject is None:
            raise ObjectDisposedError("Workspace")
        try:
            self._jobject.setDescription(description)
        except Exception as e:
            try:
                raise e
            finally:
                e = None
                del e

    def is_modified(self):
        """
        返回工作空间的内容是否有改动，如果对工作空间的内容进行了一些修改，则返回 True，否则返回 False。工作空间负责管理数据源、地图，其中任何
        一项内容发生变动，此属性都会返回 True，在关闭整个应用程序时，先用此属性判断工作空间是否已有改动，可用于提示用户是否需要存盘。

        :return: 对工作空间的内容进行了一些修改，则返回 True，否则返回 False
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError("Workspace")
        try:
            return self._jobject.isModified()
        except Exception as e:
            try:
                raise e
            finally:
                e = None
                del e

    @property
    def connection_info(self):
        """WorkspaceConnectionInfo: 工作空间的连接信息"""
        if self._jobject is None:
            raise ObjectDisposedError("Workspace")
        try:
            return WorkspaceConnectionInfo._from_java_object(self._jobject.getConnectionInfo())
        except Exception as e:
            try:
                log_error(e)
                return
            finally:
                e = None
                del e

    @classmethod
    def open(cls, conn_info, save_existed=True, saved_connection_info=None):
        """
        打开一个新的工作空间对象。在打开新的工作空间前，用户可以通过设定 save_existed 为 True 先保存当前工作空间对象，也可以设定
        saved_connection_info 将当前工作空间另存为指定的位置。

        :param WorkspaceConnectionInfo conn_info: 工作空间的连接信息
        :param bool save_existed:  是否保存当前的工作空间工作。如果设置为 True，则会先将当前工作空间保存然后再关闭当前工作空间，否则会直接关闭当前工作空间，然后再打开新的工作空间对象。save_existed 只适合用于当前工作空间不在内存中的情形。默认为 True。
        :param WorkspaceConnectionInfo saved_connection_info: 选择将当前工作另存到 saved_connection_info 指定的工作空间中。 默认为 None。
        :return:  新的工作空间对象
        :rtype: Workspace

        """
        if conn_info is None:
            raise ValueError("connectionInfo is None")
        elif not isinstance(conn_info, WorkspaceConnectionInfo):
            raise ValueError("conn_info required WorkspaceConnectionInfo, but now is " + str(type(conn_info)))
        if cls._Workspace__instance is not None:
            if saved_connection_info is not None:
                cls._Workspace__instance.save_as(saved_connection_info)
            else:
                if save_existed:
                    cls._Workspace__instance.save()
            cls._Workspace__instance.close()
            cls._Workspace__instance = None
        try:
            if cls._Workspace__instance is None:
                cls._Workspace__instance = object.__new__(cls)
                JVMBase.__init__(cls._Workspace__instance)
                _jworkspace = get_jvm().com.supermap.jsuperpy.RegisterWorkspace.getWorkspace()
                if _jworkspace is None:
                    _jworkspace = get_jvm().com.supermap.jsuperpy.RegisterWorkspace.newPythonWorkspace()
                    if not _jworkspace.open(conn_info._jobject):
                        raise RuntimeError("Failed to open workspace")
                cls._Workspace__instance._java_object = _jworkspace
                cls._Workspace__instance._created_python = get_jvm().com.supermap.jsuperpy.RegisterWorkspace.isCreatedByPython()
            return cls._Workspace__instance
        except Exception as e:
            try:
                log_error(e)
                cls._Workspace__instance = None
            finally:
                e = None
                del e

        return cls._Workspace__instance

    @classmethod
    def create(cls, conn_info, save_existed=True, saved_connection_info=None):
        """
        创建一个新的工作空间对象。在创建新的工作空间前，用户可以通过设定 save_existed 为 True 先保存当前工作空间对象，也可以设定
        saved_connection_info 将当前工作空间另存为指定的位置。

        :param WorkspaceConnectionInfo conn_info: 工作空间的连接信息
        :param bool save_existed:  是否保存当前的工作空间工作。如果设置为 True，则会先将当前工作空间保存然后再关闭当前工作空间，否则会直接关闭当前工作空间，然后再打开新的工作空间对象。save_existed 只适合用于当前工作空间不在内存中的情形。默认为 True。
        :param WorkspaceConnectionInfo saved_connection_info: 选择将当前工作另存到 saved_connection_info 指定的工作空间中。 默认为 None。
        :return:  新的工作空间对象
        :rtype: Workspace
        """
        if conn_info is None:
            raise ValueError("connectionInfo is None")
        elif not isinstance(conn_info, WorkspaceConnectionInfo):
            raise ValueError("conn_info required WorkspaceConnectionInfo, but now is " + str(type(conn_info)))
        if cls._Workspace__instance is not None:
            if saved_connection_info is not None:
                cls._Workspace__instance.save_as(saved_connection_info)
            else:
                if save_existed:
                    cls._Workspace__instance.save()
            cls._Workspace__instance.close()
            cls._Workspace__instance = None
        try:
            if cls._Workspace__instance is None:
                cls._Workspace__instance = object.__new__(cls)
                JVMBase.__init__(cls._Workspace__instance)
                _jworkspace = get_jvm().com.supermap.jsuperpy.RegisterWorkspace.getWorkspace()
                if _jworkspace is None:
                    _jworkspace = get_jvm().com.supermap.jsuperpy.RegisterWorkspace.newPythonWorkspace()
                if not _jworkspace.create(conn_info._jobject):
                    raise RuntimeError("Failed to create workspace")
                cls._Workspace__instance._java_object = _jworkspace
                cls._Workspace__instance._created_python = get_jvm().com.supermap.jsuperpy.RegisterWorkspace.isCreatedByPython()
            return cls._Workspace__instance
        except Exception as e:
            try:
                log_error(e)
                cls._Workspace__instance = None
            finally:
                e = None
                del e

        return cls._Workspace__instance

    @classmethod
    def save(cls):
        """
        用于将现存的工作空间存盘，不改变原有的名称

        :return:  保存成功返回 True，否则返回 False
        :rtype: bool
        """
        if cls._Workspace__instance is not None:
            if cls._Workspace__instance._java_object is not None:
                try:
                    return cls._Workspace__instance._java_object.save()
                except Exception as e:
                    try:
                        log_error(e)
                        return False
                    finally:
                        e = None
                        del e

            else:
                log_error("Workspace object has been disposed")
                return False
        else:
            return False

    @classmethod
    def save_as(cls, conn_info):
        """
        用指定的工作空间连接信息对象来保存工作空间文件。

        :param WorkspaceConnectionInfo conn_info: 工作空间连接信息对象
        :return: 另存成功返回 True，否则返回 False
        :rtype: bool
        """
        if conn_info is None:
            raise ValueError("connectionInfo is None")
        elif not isinstance(conn_info, WorkspaceConnectionInfo):
            raise ValueError("conn_info required WorkspaceConnectionInfo, but now is " + str(type(conn_info)))
        if cls._Workspace__instance is not None:
            if cls._Workspace__instance._java_object is not None:
                try:
                    return cls._Workspace__instance._java_object.saveAs(conn_info._jobject)
                except Exception as e:
                    try:
                        log_error(e)
                        return False
                    finally:
                        e = None
                        del e

            else:
                log_error("Workspace object has been disposed")
                return False
        else:
            return False

    @classmethod
    def close(cls):
        """
        关闭工作空间，关闭工作空间将会销毁当前工作空间的实例对象。工作空间的关闭之前确保使用的该工作空间的地图等内容关闭或断开链接。
        如果工作空间是在 Java 端注册的，将不会实际关闭工作空间对象，只会解除对 Java 工作空间对象的绑定关系，后续将不能继续操作 Java
        的工作空间对象，除非使用 Workspace() 构造新的实例。
        """
        if cls._Workspace__instance is not None:
            if cls._Workspace__instance._java_object is not None:
                if cls._Workspace__instance._created_python:
                    try:
                        _alias = cls._Workspace__instance.caption
                        log_info("try to close python workspace " + _alias)
                        get_jvm().com.supermap.jsuperpy.RegisterWorkspace.closePythonWorkspace()
                        cls._Workspace__instance._java_object = get_jvm().com.supermap.jsuperpy.RegisterWorkspace.getWorkspace()
                        log_info("success close python workspace " + _alias)
                    except:
                        try:
                            cls._Workspace__instance._java_object.close()
                            get_jvm().com.supermap.jsuperpy.RegisterWorkspace.setWorkspace(None)
                            cls._Workspace__instance._java_object = get_jvm().com.supermap.jsuperpy.RegisterWorkspace.getWorkspace()
                            log_info("success close python workspace " + _alias)
                        except Exception as e:
                            try:
                                log_error(e)
                                log_error("Failed to close workspace")
                            finally:
                                e = None
                                del e

                else:
                    cls._Workspace__instance._clear_handle()
                    cls._Workspace__instance = None
            else:
                log_error("Workspace object has been disposed")

    def _get_existed_datasource(self, conn_info):
        if conn_info is None:
            raise ValueError("connInfo is None")
        if self.datasources is None or len(self.datasources) == 0:
            return
        for ds in self.datasources:
            try:
                if ds.connection_info.is_same(conn_info):
                    return ds
            except Exception as e:
                try:
                    log_error(e)
                finally:
                    e = None
                    del e

    def open_datasource(self, conn_info, is_get_existed=True):
        """
        根据数据源连接信息打开数据源。如果设置的连接信息是UDB类型数据源，或者 is_get_existed 为 True，如果工作空间中已经存在对应的数据源，则
        会直接返回。不支持直接打开内存数据源，要使用内存数据源，需要使用 :py:meth:`create_datasource` 创建内存数据源。

        :param conn_info: udb文件路径或数据源连接信息:
                          - 数据源连接信息。具体可以参考 :py:meth:`DatasourceConnectionInfo.make`
                          - 如果 conn_info 为 str 时，可以为 ':memory:', udb 文件路径，udd 文件路径，dcf 文件路径，数据源连接信息的 xml 字符串
                          - 如果 conn_info 为 dict，为  :py:meth:`DatasourceConnectionInfo.to_dict` 的返回结果。
        :type conn_info: str or dict or DatasourceConnectionInfo
        :param bool is_get_existed: is_get_existed 为 True，如果工作空间中已经存在对应的数据源，则会直接返回。为 false 时，则会打开新的数据源。对于 UDB 类型数据源，无论 is_get_existed 为 True 还是 False，都会优先返回工作空间中的数据源。判断 DatasourceConnectionInfo 是否与工作空间中的数据源是同一个数据源，可以查看 :py:meth:`DatasourceConnectionInfo.is_same`
        :return: 数据源对象
        :rtype: Datasource

        >>> ws = Workspace()
        >>> ds = ws.open_datasource('E:/data.udb')
        >>> print(ds.type)
        EngineType.UDB

        """
        if conn_info is None:
            raise ValueError("connectionInfo is None")
        else:
            if self._jobject is None:
                raise ObjectDisposedError("Workspace")
            else:
                _connInfo = DatasourceConnectionInfo.make(conn_info)
                if _connInfo is None:
                    raise RuntimeError("Failed to get DatasourceConnectionInfo")
                else:
                    if _connInfo.type is EngineType.UDB or EngineType.UDBX or is_get_existed:
                        ds = self._get_existed_datasource(_connInfo)
                ds = None
            if ds is not None:
                ds._set_existed()
                return ds
            try:
                java_datasources = self._jobject.getDatasources()
                jds = java_datasources.open(_connInfo._jobject)
                ds = Datasource._from_java_object(jds, self)
                handle = self._get_object_handle(jds)
                if handle != 0:
                    self._ds_dict[handle] = ds
                return ds
            except:
                import traceback
                log_error(traceback.format_exc())
                raise DatasourceOpenedFailedError(_connInfo.to_json())

    def create_datasource(self, conn_info):
        """
        根据指定的数据源连接信息，创建新的数据源。

        :param conn_info: udb文件路径或数据源连接信息:
                          - 数据源连接信息。具体可以参考 :py:meth:`DatasourceConnectionInfo.make`
                          - 如果 conn_info 为 str 时，可以为 ':memory:', udb 文件路径，udd 文件路径，dcf 文件路径，数据源连接信息的 xml 字符串
                          - 如果 conn_info 为 dict，为  :py:meth:`DatasourceConnectionInfo.to_dict` 的返回结果。
        :type conn_info: str or dict or DatasourceConnectionInfo
        :return: 数据源对象
        :rtype: Datasource
        """
        if self._jobject is None:
            raise ObjectDisposedError("Workspace")
        try:
            _connInfo = DatasourceConnectionInfo.make(conn_info)
            if _connInfo is None:
                log_error("Failed to get DatasourceConnectionInfo")
                return
            java_datasources = self._jobject.getDatasources()
            jds = java_datasources.create(_connInfo._jobject)
            ds = Datasource._from_java_object(jds, self)
            handle = self._get_object_handle(jds)
            if handle != 0:
                self._ds_dict[handle] = ds
            return ds
        except Exception as e:
            try:
                import traceback
                log_error(traceback.format_exc())
                raise DatasourceCreatedFailedError(_connInfo.to_json())
            finally:
                e = None
                del e

    def get_datasource(self, item):
        """
        获取指定的数据源对象。

        :param item: 数据源的别名或序号
        :type item:  str or int
        :return: 数据源对象
        :rtype: Datasource
        """
        if self._jobject is None:
            raise ObjectDisposedError("Workspace")
        if isinstance(item, str):
            for ds in self.datasources:
                if ds.alias == item:
                    return ds

            return
        if isinstance(item, int):
            return self.datasources[item]
        raise ValueError("item required int or str, but now is " + str(type(item)))

    def modify_datasource_alias(self, old_alias, new_alias):
        """
        修改数据源的别名。数据源别名不区分大小写

        :param str old_alias: 待修改的数据源别名
        :param str new_alias: 数据源的新别名
        :return: 如果对数据源修改别名成功，则返回 True，否则返回 False
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError("Workspace")
        return self._jobject.getDatasources().modifyAlias(old_alias, new_alias)

    def is_contains_datasource(self, item):
        """
        是否存在指定序号或者数据源别名的数据源

        :param item: 数据源的别名或序号
        :type item:  str or int
        :return:  存在返回 True，否则返回 False
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError("Workspace")
        if isinstance(item, str):
            for ds in self._ds_dict.values():
                if ds.alias == item:
                    return True

            return False
        if isinstance(item, int):
            return self.datasources[item] is not None
        raise ValueError("item required int or str, but now is " + str(type(item)))

    def index_of_datasource(self, alias):
        """
        查找指定的数据源别名所在序号。不存在将抛出异常。

        :param str alias: 数据源别名
        :return: 数据源所在的序号
        :rtype: int
        :raise ValueError: 不存在指定的数据源别名时抛出异常。
        """
        if self._jobject is None:
            raise ObjectDisposedError("Workspace")
        try:
            _index = self._jobject.getDatasources().indexOf(alias)
        except Exception as e:
            try:
                log_error(e)
                _index = -1
            finally:
                e = None
                del e

        if _index >= 0:
            return _index
        raise ValueError(alias + " not found")

    def close_all_datasources(self):
        """关闭所有的数据源"""
        if self._jobject is None:
            raise ObjectDisposedError("Workspace")
        try:
            for ds in self._ds_dict.values():
                ds._clear_handle()

            self._ds_dict.clear()
            self._jobject.getDatasources().closeAll()
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

    def close_datasource(self, item):
        """
        关闭指定的数据源。

        :param item: 数据源的别名或序号
        :type item: str or int
        :return: 关闭成功返回 True，否则返回 False
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError("Workspace")
        try:
            if isinstance(item, Datasource):
                _alias = item.alias
            else:
                _alias = item
            target_handle = None
            for handle, ds in self._ds_dict.items():
                if ds.alias == _alias:
                    target_handle = handle
                    break

            if target_handle:
                del self._ds_dict[target_handle]
                self._jobject.getDatasources().close(_alias)
                return True
            return False
        except Exception as e:
            try:
                log_error(e)
            finally:
                e = None
                del e

        return False

    def _clear_handle(self):
        self._java_object = None
        for ds in self._ds_dict.values():
            ds._clear_handle()

        self._ds_dict.clear()

    def get_maps(self):
        """
        返回所有的Map

        :return: 当前工作空间中的所有 Map
        :rtype: list[Map]
        """
        if self._jobject is None:
            raise ObjectDisposedError("Workspace")
        java_maps = self._jobject.getMaps()
        if java_maps:
            maps = []
            from ..mapping import Map
            for i in range(java_maps.getCount()):
                map_xml = java_maps.getMapXML(i)
                my_map = Map()
                if my_map.from_xml(map_xml):
                    maps.append(my_map)
                else:
                    log_error("Failed to create map from xml")
                    del my_map

            return maps

    def add_map(self, map_name, map_or_xml):
        """
        添加 Map 到当前工作空间中

        :param str map_name: 地图名称
        :param map_or_xml: 地图对象或地图的 XML 描述
        :type map_or_xml: Map or str
        :return: 新添加的地图在此地图集合对象中的序号。
        :rtype: int
        """
        if self._jobject is None:
            raise ObjectDisposedError("Workspace")
        else:
            from ..mapping import Map
            if isinstance(map_or_xml, Map):
                map_xml = map_or_xml.to_xml()
            else:
                map_xml = str(map_or_xml)
        if isinstance(map_xml, str):
            return self._jobject.getMaps().add(str(map_name), map_xml)
        raise ValueError("invalid input for map_xml")
        return -1

    def insert_map(self, index, map_name, map_or_xml):
        """
        在指定序号的位置处添加一个地图，地图的内容由 XML 字符串来确定。

        :param int index: 指定的序号。
        :param str map_name: 指定的地图名称。该名称不区分大小写。
        :param map_or_xml: 用来表示待插入地图或地图的 XML 字符串。
        :type map_or_xml: Map or str
        :return: 如果插入地图成功，返回 true；否则返回 false。
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError("Workspace")
        else:
            from ..mapping import Map
            if isinstance(map_or_xml, Map):
                map_xml = map_or_xml.to_xml()
            else:
                map_xml = str(map_or_xml)
        if isinstance(map_xml, str):
            return self._jobject.getMaps().insert(int(index), str(map_name), map_xml)
        raise ValueError("invalid input for map_xml")
        return -1

    def set_map(self, index_or_name, map_or_xml):
        """
        将指定地图或地图的 XML 字符串表示的地图替换地图集合对象中指定序号的地图。

        :param index_or_name: 指定的序号或地图名称
        :type index_or_name: int or str
        :param map_or_xml: 用来替换指定地图的新地图的 XML 字符串表示。
        :type map_or_xml: Map or str
        :return: 如果操作成功，返回 true；否则返回 false。
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError("Workspace")
        else:
            from ..mapping import Map
            if isinstance(map_or_xml, Map):
                map_xml = map_or_xml.to_xml()
            else:
                map_xml = str(map_or_xml)
        if isinstance(map_xml, str):
            return self._jobject.getMaps().setMapXML(index_or_name, map_xml)
        raise ValueError("invalid input for map_xml")
        return False

    def remove_map(self, index_or_name):
        """
        删除此地图集合对象中指定序号或名称的地图

        :param index_or_name: 待删除地图的序号或名称
        :type index_or_name: str or int
        :return: 删除成功，返回 true；否则返回 false。
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError("Workspace")
        return self._jobject.getMaps().remove(index_or_name)

    def clear_maps(self):
        """
        删除此地图集合对象中的所有地图，即工作空间保存的所有地图。

        :return: Workspace 对象自身
        :rtype: Workspace
        """
        if self._jobject is None:
            raise ObjectDisposedError("Workspace")
        self._jobject.getMaps().clear()
        return self

    def get_map_xml(self, index_or_name):
        """
        返回指定名称或序号的地图的 XML 描述

        :param index_or_name: 指定的地图名称或序号
        :type index_or_name: int or str
        :return: 地图的 XML 描述
        :rtype: str
        """
        if self._jobject is None:
            raise ObjectDisposedError("Workspace")
        return self._jobject.getMaps().getMapXML(index_or_name)

    def get_map(self, index_or_name):
        """
        获取指定名称或序号的地图对象

        :param index_or_name: 指定的地图名称或序号
        :type index_or_name: int or str
        :return: 地图对象
        :rtype: Map
        """
        map_xml = self.get_map_xml(index_or_name)
        if map_xml:
            from ..mapping import Map
            my_map = Map()
            my_map.from_xml(map_xml)
            return my_map
        raise ValueError("Failed to get Map")

    def rename_map(self, old_name, new_name):
        """
        修改地图对象的名称

        :param str old_name: 地图对象当前的名称
        :param str new_name: 指定的新的地图名称
        :return: 修改成功返回 True，否则返回  False
        :rtype: bool
        """
        if self._jobject is None:
            raise ObjectDisposedError("Workspace")
        return self._jobject.getMaps().rename(str(old_name), str(new_name))


def create_datasource(conn_info):
    """
    根据指定的数据源连接信息，创建新的数据源。

    :param conn_info: udb文件路径或数据源连接信息:
                      - 数据源连接信息。具体可以参考 :py:meth:`DatasourceConnectionInfo.make`
                      - 如果 conn_info 为 str 时，可以为 ':memory:', udb 文件路径，udd 文件路径，dcf 文件路径，数据源连接信息的 xml 字符串
                      - 如果 conn_info 为 dict，为  :py:meth:`DatasourceConnectionInfo.to_dict` 的返回结果。
    :type conn_info: str or dict or DatasourceConnectionInfo
    :return: 数据源对象
    :rtype: Datasource
    """
    return Workspace().create_datasource(conn_info)


def open_datasource(conn_info, is_get_existed=True):
    """
    根据数据源连接信息打开数据源。如果设置的连接信息是UDB类型数据源，或者 is_get_existed 为 True，如果工作空间中已经存在对应的数据源，则
    会直接返回。不支持直接打开内存数据源，要使用内存数据源，需要使用 :py:meth:`create_datasource` 创建内存数据源。

    具体参考  :py:meth:`Workspace.open_datasource`

    :param conn_info: udb文件路径或数据源连接信息:
                          - 数据源连接信息。具体可以参考 :py:meth:`DatasourceConnectionInfo.make`
                          - 如果 conn_info 为 str 时，可以为 ':memory:', udb 文件路径，udd 文件路径，dcf 文件路径，数据源连接信息的 xml 字符串
                          - 如果 conn_info 为 dict，为  :py:meth:`DatasourceConnectionInfo.to_dict` 的返回结果。
    :type conn_info: str or dict or DatasourceConnectionInfo
    :param bool is_get_existed: is_get_existed 为 True，如果工作空间中已经存在对应的数据源，则会直接返回。为 false 时，则会打开新的数据源。对于 UDB 类型数据源，无论 is_get_existed 为 True 还是 False，都会优先返回工作空间中的数据源。判断 DatasourceConnectionInfo 是否与工作空间中的数据源是同一个数据源，可以查看 :py:meth:`DatasourceConnectionInfo.is_same`
    :return: 数据源对象
    :rtype: Datasource
    """
    return Workspace().open_datasource(conn_info, is_get_existed)


def get_datasource(item):
    """
    获取指定的数据源对象。

    具体参考  :py:meth:`Workspace.get_datasource`

    :param item: 数据源的别名或序号
    :type item:  str or int
    :return: 数据源对象
    :rtype: Datasource
    """
    return Workspace().get_datasource(item)


def close_datasource(item):
    """
    关闭指定的数据源。

    具体参考  :py:meth:`Workspace.close_datasource`

    :param item: 数据源的别名或序号
    :type item: str or int
    :return: 关闭成功返回 True，否则返回 False
    :rtype: bool
    """
    return Workspace().close_datasource(item)


def list_datasources():
    """
    返回当前工作空间下的所有数据源对象。

    具体参考  :py:attr:`Workspace.datasources`

    :return: 当前工作空间下的所有数据源对象
    :rtype: list[Datasource]
    """
    return Workspace().datasources


def list_maps():
    """
    返回当前工作空间下的所有地图对象

    :return: 当前工作空间下的所有地图
    :rtype: list[Map]
    """
    return Workspace().get_maps()


def get_map(index_or_name):
    """
    获取指定名称或序号的地图对象

    :param index_or_name: 指定的地图名称或序号
    :type index_or_name: int or str
    :return: 地图对象
    :rtype: Map
    """
    return Workspace().get_map(index_or_name)


def remove_map(index_or_name):
    """
    删除此地图集合对象中指定序号或名称的地图

    :param index_or_name: 待删除地图的序号或名称
    :type index_or_name: str or int
    :return: 删除成功，返回 true；否则返回 false。
    :rtype: bool
    """
    return Workspace().remove_map(index_or_name)


def add_map(map_name, map_or_xml):
    """
    添加 Map 到当前工作空间中

    :param str map_name: 地图名称
    :param map_or_xml: 地图对象或地图的 XML 描述
    :type map_or_xml: Map or str
    :return: 新添加的地图在此地图集合对象中的序号。
    :rtype: int
    """
    return Workspace().add_map(map_name, map_or_xml)

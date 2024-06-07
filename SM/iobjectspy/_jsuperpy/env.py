# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/_jsuperpy\env.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 9851 bytes
import json, threading, os
__all__ = [
 'is_auto_close_output_datasource', 'set_auto_close_output_datasource', 'is_use_analyst_memory_mode', 
 'set_analyst_memory_mode', 
 'get_omp_num_threads', 'set_omp_num_threads', 'set_iobjects_java_path', 
 'get_iobjects_java_path']
IS_USE_ANALYST_MEMORY_MODE = "is_use_analyst_memory_mode"
OMP_NUM_THREADS = "omp_num_threads"
AUTO_CLOSE_OUTPUT_DATASOURCE = "auto_close_output_datasource"
IOBJECTS_JAVA_BIN_PATH = "iobjects_java_bin_path"

def _setting_file():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    return curr_dir + "/env.json"


def _load_settings(file_f):
    with open(file_f, encoding="utf-8") as f:
        s = f.read()
    return json.loads(s, encoding="utf-8")


class Env:
    __doc__ = "\n    环境设置类，配置文件为当前目录下的 env.json 文件\n    "
    _lock = threading.Lock()
    _setting_file = _setting_file()
    _settings = _load_settings(_setting_file)

    @classmethod
    def set_iobjects_java_bin_path(cls, iobjects_java_bin_path):
        import os
        if iobjects_java_bin_path is not None:
            if os.path.isdir(iobjects_java_bin_path) and os.path.exists(iobjects_java_bin_path):
                cls._prepare_set()
                cls._lock.acquire()
                cls._settings[IOBJECTS_JAVA_BIN_PATH] = str(iobjects_java_bin_path)
                cls._write()
                cls._lock.release()
        else:
            cls._prepare_set()
            cls._lock.acquire()
            cls._settings[IOBJECTS_JAVA_BIN_PATH] = None
            cls._write()
            cls._lock.release()

    @classmethod
    def get_iobjects_java_bin_path(cls):
        if IOBJECTS_JAVA_BIN_PATH in cls._settings:
            try:
                value = cls._settings[IOBJECTS_JAVA_BIN_PATH]
                if value is not None:
                    return str(value)
            except:
                return

    @classmethod
    def load(cls, force_load=False):
        """
        从 env.json 设置文件中读取所有的设置项

        :param bool force_load: 是否强制加载。
        """
        if force_load or cls._settings is None or len(cls._settings) == 0:
            cls._lock.acquire()
            cls._settings = _load_settings(cls._setting_file)
            cls._lock.release()

    @classmethod
    def _write(cls):
        try:
            import codecs
            writer = codecs.open((cls._setting_file), "w", encoding="utf-8")
            writer.write(json.dumps((cls._settings), indent=4))
            writer.flush()
            writer.close()
        except:
            pass

    @classmethod
    def _prepare_set(cls):
        if cls._settings is None or len(cls._settings) == 0:
            cls.load()

    @classmethod
    def is_auto_close_output_datasource(cls):
        """
        是否自动关闭结果数据源对象。在处理数据或分析时，设置的结果数据源信息如果是程序自动打开的（即当前工作空间下不存在此数据源），默认情形下程序在
        完成单个功能后会自动关闭。用户可以通过设置 :py:meth:`set_auto_close_output_datasource` 使结果数据源不被自动关闭，这样，结果数据源将存在于当前的工作空间中。

        :rtype: bool
        """
        if AUTO_CLOSE_OUTPUT_DATASOURCE in cls._settings:
            try:
                return bool(cls._settings[AUTO_CLOSE_OUTPUT_DATASOURCE])
            except:
                return True

        else:
            return True

    @classmethod
    def set_auto_close_output_datasource(cls, auto_close):
        """
        设置是否关闭结果数据源对象。在处理数据或分析时，设置的结果数据源信息如果是程序自动打开的（不是用户调用打开数据源接口打开，即当前工作空间下不存在此数据源），默认情形下程序在
        完成单个功能后会自动关闭。用户可以通过此接口设置 auto_close 为 False 使结果数据源不被自动关闭，这样，结果数据源将存在于当前的工作空间中。

        :param bool auto_close: 是否自动关闭程序内部打开的数据源对象。
        """
        cls._prepare_set()
        cls._lock.acquire()
        cls._settings[AUTO_CLOSE_OUTPUT_DATASOURCE] = bool(auto_close)
        cls._write()
        cls._lock.release()

    @classmethod
    def is_use_analyst_memory_mode(cls):
        """
        空间分析是否使用内存模式

        :rtype: bool
        """
        if IS_USE_ANALYST_MEMORY_MODE in cls._settings:
            try:
                return bool(cls._settings[IS_USE_ANALYST_MEMORY_MODE])
            except:
                return True

        else:
            return True

    @classmethod
    def set_analyst_memory_mode(cls, is_use_memory):
        """
        设置空间分析是否启用内存模式。

        :param bool is_use_memory: 启用内存模式设置\u3000True ，\u3000否则设置为\u3000False
        """
        cls._prepare_set()
        cls._lock.acquire()
        cls._settings[IS_USE_ANALYST_MEMORY_MODE] = bool(is_use_memory)
        cls._write()
        cls._lock.release()
        cls._set_java_analyst_memory_mode()

    @classmethod
    def _set_java_analyst_memory_mode(cls):
        from ._gateway import get_jvm
        jvm = get_jvm()
        if jvm is not None:
            if cls.is_use_analyst_memory_mode():
                jvm.com.supermap.data.Environment.setAnalystMemorySize(-1)
            else:
                jvm.com.supermap.data.Environment.setAnalystMemorySize(0)

    @classmethod
    def get_omp_num_threads(cls):
        """
        获取并行计算所使用的线程数

        :rtype: int
        """
        if OMP_NUM_THREADS in cls._settings:
            try:
                return int(cls._settings[OMP_NUM_THREADS])
            except:
                return 2

        else:
            return 2

    @classmethod
    def set_omp_num_threads(cls, num_threads):
        """
        设置并行计算所使用的线程数

        :param int num_threads: 并行计算所使用的线程数
        """
        cls._prepare_set()
        cls._lock.acquire()
        cls._settings[OMP_NUM_THREADS] = int(num_threads)
        cls._write()
        cls._lock.release()
        cls._set_java_omp_num_threads()

    @classmethod
    def _set_java_omp_num_threads(cls):
        from ._gateway import get_jvm
        jvm = get_jvm()
        if jvm is not None:
            jvm.com.supermap.data.Environment.setOMPNumThreads(cls.get_omp_num_threads())

    @classmethod
    def _set_all_to_java(cls):
        from ._gateway import get_jvm
        jvm = get_jvm()
        if jvm is not None:
            if cls.is_use_analyst_memory_mode():
                jvm.com.supermap.data.Environment.setAnalystMemorySize(-1)
            else:
                jvm.com.supermap.data.Environment.setAnalystMemorySize(0)
            jvm.com.supermap.data.Environment.setOMPNumThreads(cls.get_omp_num_threads())


def is_auto_close_output_datasource():
    """
    是否自动关闭结果数据源对象。在处理数据或分析时，设置的结果数据源信息如果是程序自动打开的（即当前工作空间下不存在此数据源），默认情形下程序在
    完成单个功能后会自动关闭。用户可以通过设置 :py:meth:`set_auto_close_output_datasource` 使结果数据源不被自动关闭，这样，结果数据源将存在于当前的工作空间中。

    :rtype: bool
    """
    return Env.is_auto_close_output_datasource()


def set_auto_close_output_datasource(auto_close):
    """
    设置是否关闭结果数据源对象。在处理数据或分析时，设置的结果数据源信息如果是程序自动打开的（不是用户调用打开数据源接口打开，即当前工作空间下不存在此数据源），默认情形下程序在
    完成单个功能后会自动关闭。用户可以通过此接口设置 auto_close 为 False 使结果数据源不被自动关闭，这样，结果数据源将存在于当前的工作空间中。

    :param bool auto_close: 是否自动关闭程序内部打开的数据源对象。
    """
    Env.set_auto_close_output_datasource(auto_close)


def is_use_analyst_memory_mode():
    """
    空间分析是否使用内存模式

    :rtype: bool
    """
    return Env.is_use_analyst_memory_mode()


def set_analyst_memory_mode(is_use_memory):
    """
    设置空间分析是否启用内存模式。

    :param bool is_use_memory: 启用内存模式设置\u3000True ，\u3000否则设置为\u3000False
    """
    Env.set_analyst_memory_mode(is_use_memory)


def get_omp_num_threads():
    """
    获取并行计算所使用的线程数

    :rtype: int
    """
    return Env.get_omp_num_threads()


def set_omp_num_threads(num_threads):
    """
    设置并行计算所使用的线程数

    :param int num_threads: 并行计算所使用的线程数
    """
    Env.set_omp_num_threads(num_threads)


def set_iobjects_java_path(bin_path, is_copy_jars=True):
    """
    设置 iObjects Java 组件 Bin 目录地址。设置的 Bin 目录地址会保存到 env.json 文件中。

    :param str bin_path:  iObjects Java 组件 Bin 目录地址
    :param bool is_copy_jars: 是否同时拷贝 iObjects Java 组件的 jars 到 iObjectsPy 目录。
    """
    if bin_path is not None:
        if is_copy_jars:
            from ._copyjars import copy_jars
            copy_jars(bin_path, True)
    Env.set_iobjects_java_bin_path(bin_path)


def get_iobjects_java_path():
    """
    获取设置的 iObjects Java 组件 Bin 目录地址。只能获取到主动设置或保存到 env.json 文件中的目录地址。默认值为 None。

    :rtype: str
    """
    return Env.get_iobjects_java_bin_path()

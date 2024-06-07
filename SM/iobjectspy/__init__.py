# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/__init__.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 1535 bytes
from . import _version
__version__ = _version.get_version()
try:
    from . import _jsuperpy as supermap
    from ._jsuperpy import set_gateway_port
    from ._jsuperpy import set_gateway
except ImportError as e:
    try:
        from . import _csuperpy as supermap
    finally:
        e = None
        del e

from .env import *
from .enums import *
from .data import *
from .conversion import *
from .analyst import *
from .threeddesigner import *
from .mapping import *
try:
    from ml.utils import recordset_to_numpy_array, datasetvector_to_numpy_array, numpy_array_to_datasetvector, datasetraster_to_numpy_array, numpy_array_to_datasetraster, recordset_to_df, datasetvector_to_df, df_to_datasetvector, datasetraster_to_df_or_xarray, df_or_xarray_to_datasetraster
except ImportError:
    pass

import atexit
is_objects_java_release = _version.is_objects_java_release

@atexit.register
def _close():
    """
    关闭工作空间，如果 iobjectspy 基于 iObjects Java 组件，会关闭 Java 端的 Gateway Server。
    """
    if _version.is_objects_java_release():
        supermap.gateway_shutdown()
    else:
        Workspace.close()


if is_objects_java_release():
    _main = supermap.main
else:

    def _main():
        print("iobjectspy unsupported iobjectspy script")


main = _main

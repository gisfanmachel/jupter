# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/_jsuperpy\__init__.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 1652 bytes
from ._gateway import gateway_shutdown, set_gateway_port, set_gateway
from .env import *
from .enums import *
from .data import *
from .analyst import *
from .conversion import *
from .threeddesigner import *
from .mapping import *
from .._logger import log_warning
try:
    from ._numpy import *
except:
    log_warning("failed to load `numpy` ")

del log_warning

def internal_tag():
    return "iobjects-java"


def main(args=None):
    if args is None:
        import sys
        args = sys.argv[1[:None]]
    else:
        usages = []
        usages.append("usage: iobjectspy command args")
        usages.append("  ")
        usages.append("  ")
        usages.append("  iobjectspy set-iobjects-java iobjects-path is_copy_jars[Option]")
        usages.append("      example:")
        usages.append("           iobjectspy set-iobjects-java /home/data/iobjects/Bin")
        usages.append("           iobjectspy set-iobjects-java /home/data/iobjects/Bin false")
        help_info = "\r\n".join(usages)
        command = args[0].lower()
        if command == "set-iobjects-java":
            if len(args) < 2:
                print("invalid input")
                print(help_info)
                return
            is_copy_jars = True
            if len(args) > 2:
                if args[2].lower() == "false":
                    is_copy_jars = False
            bin_path = args[1]
            if not bin_path or str(bin_path).lower() in ('none', 'null'):
                bin_path = None
            set_iobjects_java_path(bin_path, is_copy_jars)
            if get_iobjects_java_path() == bin_path:
                print("set `{}` as iobjects-java bin, OK".format(bin_path))
        elif command == "help":
            print(help_info)

# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/_jsuperpy\_copyjars.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 1354 bytes
from ._logger import log_info

def _copy_jars(source_dir, target_dir, is_command=False):
    import os, shutil
    files = os.listdir(source_dir)
    for f in files:
        if os.path.isfile(os.path.join(source_dir, f)) and f.endswith(".jar"):
            try:
                shutil.copyfile(os.path.join(source_dir, f), os.path.join(target_dir, f))
                if is_command:
                    print("copy {}, OK".format(f))
                else:
                    log_info("copy {}, OK".format(f))
            except:
                import traceback
                from ._logger import log_warning
                log_warning("failed copy {} to iobjectspy jars directory".format(f))


def copy_jars(source_jar_path, is_command=False):
    import os
    if source_jar_path is not None:
        if os.path.isdir(source_jar_path):
            if os.path.exists(source_jar_path):
                target_jars_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jars")
                if is_command:
                    print("source jar path: " + source_jar_path)
                    print("target jar path: " + target_jars_path)
                else:
                    log_info("source jar path: " + source_jar_path)
                    log_info("target jar path: " + target_jars_path)
                _copy_jars(source_jar_path, target_jars_path, is_command)

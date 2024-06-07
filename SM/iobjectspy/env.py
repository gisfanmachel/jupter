# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/env.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 863 bytes
try:
    from . import _jsuperpy as supermap
except ImportError as e:
    try:
        from . import _csuperpy as supermap
    finally:
        e = None
        del e

is_auto_close_output_datasource = supermap.is_auto_close_output_datasource
set_auto_close_output_datasource = supermap.set_auto_close_output_datasource
is_use_analyst_memory_mode = supermap.is_use_analyst_memory_mode
set_analyst_memory_mode = supermap.set_analyst_memory_mode
get_omp_num_threads = supermap.get_omp_num_threads
set_omp_num_threads = supermap.set_omp_num_threads
set_iobjects_java_path = supermap.set_iobjects_java_path
get_iobjects_java_path = supermap.get_iobjects_java_path
__all__ = [
 'is_auto_close_output_datasource', 'set_auto_close_output_datasource', 'is_use_analyst_memory_mode', 
 'set_analyst_memory_mode', 
 'get_omp_num_threads', 'set_omp_num_threads', 'set_iobjects_java_path', 
 'get_iobjects_java_path']

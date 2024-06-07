# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/_logger.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 362 bytes
import logging.config
__all__ = ['log_error', 'log_warning', 'log_debug', 'log_fatal', 'log_info']
import os
logging.config.fileConfig(os.path.dirname(os.path.abspath(__file__)) + "/log.conf")
logger = logging.getLogger("root")
log_error = logger.error
log_warning = logger.warning
log_fatal = logger.critical
log_info = logger.info
log_debug = logger.debug

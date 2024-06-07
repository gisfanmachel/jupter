# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/_jsuperpy\data\step.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 1973 bytes
__all__ = [
 "StepEvent"]

class StepEvent(object):
    __doc__ = "\n    指示进度条的事件。当监听器的目标进度发生变化时触发该事件。\n    某些功能能返回当前任务执行的进度信息，进度信息通过 StepEvent 返回，用户可以从 StepEvent 中获取当前任务进行的状态。\n\n    例如，用户可以定义一个函数来显示缓冲区分析的进度信息。\n\n    >>> def progress_function(step_event):\n            print('%s-%s' % (step_event.title, step_event.message))\n    >>>\n    >>> ds = Workspace().open_datasource('E:/data.udb')\n    >>> dt = ds['point'].query('SmID < 1000')\n    >>> buffer_dt = create_buffer(dt, 10, 10, progress=progress_function)\n\n    "

    def __init__(self, title=None, message=None, percent=None, remain_time=None, cancel=None):
        self._title = title
        self._message = message
        self._percent = percent
        self._is_cancel = cancel
        self._remain_time = remain_time

    def __repr__(self):
        "%s, %s, %s, %d%% \n" % (self.title, self.message, self._remain_time, self.percent)

    @property
    def title(self):
        """str: 进度信息的标题"""
        return self._title

    @property
    def message(self):
        """str: 正在进行操作的信息"""
        return self._message

    @property
    def percent(self):
        """int: 当前操作完成的百分比"""
        return self._percent

    @property
    def remain_time(self):
        """int: 完成当前操作预计的剩余时间，单位为秒"""
        return self._remain_time

    @property
    def is_cancel(self):
        """bool: 事件的取消状态"""
        return self._is_cancel

    def set_cancel(self, value):
        """
        设置事件的取消状态。操作进行时如果设置为取消，则任务会中断执行。

        :param bool value: 事件取消的状态，如果为true，则中断执行
        """
        self._is_cancel = bool(value)

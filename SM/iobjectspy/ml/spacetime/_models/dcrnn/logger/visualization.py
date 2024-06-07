# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\spacetime\_models\dcrnn\logger\visualization.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 2847 bytes
import importlib
from lib.utils import Timer

class TensorboardWriter:

    def __init__(self, log_dir, logger, enabled):
        self.writer = None
        self.selected_module = ""
        if enabled:
            log_dir = str(log_dir)
            succeeded = False
            for module in ('torch.utils.tensorboard', 'tensorboardX'):
                try:
                    self.writer = importlib.import_module(module).SummaryWriter(log_dir)
                    succeeded = True
                    break
                except ImportError:
                    succeeded = False

                self.selected_module = module

            if not succeeded:
                message = "Warning: visualization (Tensorboard) is configured to use, but currently not installed on this machine. Please install either TensorboardX with 'pip install tensorboardx', upgrade PyTorch to version >= 1.1 for using 'torch.utils.tensorboard' or turn off the option in the 'config.json' file."
                logger.warning(message)
        self.step = 0
        self.mode = ""
        self.tb_writer_ftns = {
         'add_scalar', 'add_scalars', 'add_image', 'add_images', 
         'add_audio', 
         'add_text', 'add_histogram', 
         'add_pr_curve', 'add_embedding'}
        self.tag_mode_exceptions = {
         "add_histogram", "add_embedding"}
        self.timer = Timer()

    def set_step(self, step, mode='train'):
        self.mode = mode
        self.step = step
        if step == 0:
            self.timer.reset()
        else:
            duration = self.timer.check()
            self.add_scalar("steps_per_sec", 1 / duration)

    def __getattr__(self, name):
        """
        If visualization is configured to use:
            return add_data() methods of tensorboard with additional information (step, tag) added.
        Otherwise:
            return a blank function handle that does nothing
        """
        if name in self.tb_writer_ftns:
            add_data = getattr(self.writer, name, None)

            def wrapper(tag, data, *args, **kwargs):
                if add_data is not None:
                    if name not in self.tag_mode_exceptions:
                        tag = "{}/{}".format(tag, self.mode)
                    add_data(tag, data, self.step, *args, **kwargs)

            return wrapper
        try:
            attr = object.__getattr__(name)
        except AttributeError:
            raise AttributeError("type object '{}' has no attribute '{}'".format(self.selected_module, name))

        return attr

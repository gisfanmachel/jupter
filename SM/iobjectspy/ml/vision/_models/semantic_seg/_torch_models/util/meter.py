# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_torch_models\util\meter.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 1658 bytes
import numpy as np

class Meter(object):
    __doc__ = "Meters provide a way to keep track of important statistics in an online manner.\n    This class is abstract, but provides a standard interface for all meters to follow.\n    "

    def reset(self):
        """Resets the meter to default settings."""
        pass

    def add(self, value):
        """Log a new value to the meter
        Args:
            value: Next restult to include.
        """
        pass

    def value(self):
        """Get the value of the meter in the current state."""
        pass


class AverageValueMeter(Meter):

    def __init__(self):
        super(AverageValueMeter, self).__init__()
        self.reset()
        self.val = 0

    def add(self, value, n=1):
        self.val = value
        self.sum += value
        self.var += value * value
        self.n += n
        if self.n == 0:
            self.mean, self.std = np.nan, np.nan
        else:
            if self.n == 1:
                self.mean = 0.0 + self.sum
                self.std = np.inf
                self.mean_old = self.mean
                self.m_s = 0.0
            else:
                self.mean = self.mean_old + (value - n * self.mean_old) / float(self.n)
                self.m_s += (value - self.mean_old) * (value - self.mean)
                self.mean_old = self.mean
                self.std = np.sqrt(self.m_s / (self.n - 1.0))

    def value(self):
        return (
         self.mean, self.std)

    def reset(self):
        self.n = 0
        self.sum = 0.0
        self.var = 0.0
        self.val = 0.0
        self.mean = np.nan
        self.mean_old = 0.0
        self.m_s = 0.0
        self.std = np.nan

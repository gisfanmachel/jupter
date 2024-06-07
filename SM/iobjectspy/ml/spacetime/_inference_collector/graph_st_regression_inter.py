# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\spacetime\_inference_collector\graph_st_regression_inter.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 1748 bytes
import os
from _models.torch_st_regression import GraphSTRegressionEstimation
from _models.dcrnn.lib.utils import read_yaml, write_yaml
from pathlib import Path

class GraphSTRegression:

    def __init__(self, input_data_dir, model_path, out_data, location_data_path=None, fields_as_point=[
 "longitude", "latitude"], **kwargs):
        self.model_path = os.path.abspath(os.path.splitext(model_path)[0] + ".pth")
        self.config = read_yaml(Path(model_path))
        self.input_data_dir = input_data_dir
        self.out_data = out_data
        self.kwargs = kwargs
        self.location_data_path = location_data_path

    def infer(self):
        """
        根据func_str拼接字符串自动执行各个网络的函数
        :return:
        """
        result = eval("self.dcrnn_pytorch")()
        print("The graph st-regression have done!")
        return result

    def dcrnn_pytorch(self):
        estimator = GraphSTRegressionEstimation((self.model_path), (self.input_data_dir),
          (self.out_data),
          (self.location_data_path),
          fields_as_point=[
         "longitude", "latitude"])
        if self.location_data_path is not None:
            return estimator.estimate_dataset((self.location_data_path), (self.out_data),
              fields_as_point=[
             "longitude", "latitude"])
        return estimator.estimate_datatable()

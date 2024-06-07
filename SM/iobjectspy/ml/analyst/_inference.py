# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\analyst\_inference.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 1090 bytes
import os, tempfile
from iobjectspy._jsuperpy._utils import check_lic
from analyst._tabular.classification import ClsEstimater

class Inference:

    def __init__(self, model_path, **kwargs):
        """
        表格数据模型推理初始化入口

        :param model_path: 模型存储路径
        :type  model_path: str
        """
        self.model_path = model_path
        self.kwargs = kwargs
        check_lic()

    def cls_tabular_infer(self, input_data, out_data, out_dataset_name=None, **kwargs):
        """
        表格数据模型推理功能入口

        :param input_data: 输入数据路径，暂时支持csv
        :param out_data: 输出数据路径，暂时支持csv
        :param out_dataset_name: 输出文件名
        :param kwargs: 其他参数
        :return: （预测结果 ，输出数据路径）
        """
        result = (ClsEstimater((self.model_path), **self.kwargs).estimate_file)(input_data, out_data, out_dataset_name, **kwargs)
        return result

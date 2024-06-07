# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\geoparsing\_inference.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 893 bytes
from ._ger import *

class Inference:
    __doc__ = "\n    地理编码工具相关功能预测入口\n\n    "

    @staticmethod
    def ger_infer(input_data=None, addr_field=0, model_path='./model', out_name='result', out_data='/tmp/result.csv'):
        """
        地址要素识别预测接口

        :param input_data: 输入数据
        :type input_data: str or dataset
        :param addr_field: 地址文本字段名或字段索引值
        :type addr_field: str or int
        :param model_path: 模型路径
        :type model_path: str
        :param out_name: 输出文件名
        :type out_name: str
        :param out_data: 输出路径或数据源
        :type out_data: str or datasource
        :return: None
        """
        print("初始化地理实体识别功能")
        ger = GER()
        ger.parse_batch(input_data, addr_field, model_path, out_name, out_data)

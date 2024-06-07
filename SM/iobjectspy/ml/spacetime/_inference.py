# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\spacetime\_inference.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 2175 bytes
import os
from iobjectspy._jsuperpy._utils import check_lic
from ._inference_collector import GraphSTRegression
from toolkit._toolkit import del_dir

class Inference:

    def __init__(self, input_data_dir, model_path, out_data, location_data_path=None, fields_as_point=[
 "longitude",
 "latitude"]):
        """
        图时空回归模型推理功能入口

        :param input_data_dir: 待推理的数据所在目录
        :type  input_data_dir: str
        :param model_path: 模型存储路径
        :type  model_path: str
        :param out_data: 输出文件路径
        :type  out_data: str
        :type  location_data_path: str 数据坐标文件,返回矢量预测结果所需,字段名顺序为【id字段，观察位置id, fields_as_point指定两个字段】
        :type  fields_as_point:  (list[str] or list[int]) -- 指定字段为 X、Y 生成点数据集,默认为[latitude, longitude]
        """
        if isinstance(input_data_dir, str):
            if os.path.isdir(input_data_dir):
                self.is_del_tmp_file = False
        self.input_data_dir = input_data_dir
        self.model_path = model_path
        self.out_data = out_data
        self.location_data_path = location_data_path
        check_lic()

    def graph_st_regress_infer(self, **kwargs):
        """
        基于图时空回归的交通时空预测

        输入和输出文件为numpy二进制序列化文件( *.npz )

        :param result_type: 结果返回类型
        :type result_type:  List
        :return: 若提供location_data_path,返回矢量数据集的预测结果,否则返回预测结果与GroundTruth的列表数据

        """
        result = GraphSTRegression(self.input_data_dir,
 self.model_path,
 self.out_data,
 self.location_data_path, fields_as_point=[
                           "longitude",
                           "latitude"], **kwargs).infer()
        return result

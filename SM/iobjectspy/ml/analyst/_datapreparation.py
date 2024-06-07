# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\analyst\_datapreparation.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 1579 bytes
import os
from iobjectspy._jsuperpy._utils import check_lic
from _tabular.classification import create_cls_tabular_data

class DataPreparation:
    __doc__ = "\n    表格数据准备流程入口\n\n    "

    @staticmethod
    def create_training_data(input_data, label_class_field, output_path, output_name, training_data_format, **kwargs):
        """
        表格数据创建训练数据集

        :param input_data: 输入数据路径，暂时只支持csv
        :param label_class_field: 数据标签所在列名
        :param output_path: 输出路径
        :param output_name: 输出文件名
        :param training_data_format: 要制作的训练数据格式
        :param kwargs: 其他附加参数
        :return:
        """
        check_lic()
        if isinstance(input_data, str):
            if not os.path.exists(input_data):
                raise Exception("input_data does not exist ")
        if isinstance(label_class_field, str):
            if not os.path.exists(input_data):
                raise Exception("input_data does not exist ")
        if not isinstance(output_path, str):
            raise TypeError("output_path must be str ")
        elif not isinstance(training_data_format, str):
            raise TypeError("training_data_format must be str ")
        if training_data_format == "TABULAR":
            create_cls_tabular_data(input_data, label_class_field, output_path, output_name)
        else:
            raise Exception("{} Format not supported".format(training_data_format))
        print("The create training data have done!")

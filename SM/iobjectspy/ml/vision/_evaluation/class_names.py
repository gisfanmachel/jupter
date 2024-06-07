# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_evaluation\class_names.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 3224 bytes
import os
from collections import OrderedDict
import yaml
from dotmap import DotMap
from iobjectspy.ml.toolkit._create_training_data_util import _get_input_feature
from iobjectspy.ml.toolkit._toolkit import save_config_to_yaml

def get_classe_names_from_dataset(dataset, label_class_field, out_path=None, out_name=None):
    """ class_names = get_classe_names(dataset, label_class_field, out_path=None)

        通过矢量数据集获取记录集中的所有类别

        :param dataset: 数据集
        :type dataset: DataSetVector
        :param label_class_field: 游标类型，可以为枚举值或名称
        :type label_class_field: CursorType or str
        :param out_path: 输出文件路径
        :type out_path: str
        :param out_name: 输出文件名称
        :type out_name: str
        :return class_names : 记录集中类别信息
        :rtype: list
        """
    class_names = []
    if out_path is not None:
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        try:
            with open(os.path.join(out_path, out_name + ".yml")) as f:
                config_dict = yaml.load(f, Loader=(yaml.FullLoader))
            voc_config = DotMap(config_dict)
            class_names = voc_config.get("class_names")
        except:
            print('`{:s}`.yml is not exist, please modify the directory, or enter "None" as "out path" '.format(out_name))

    else:
        class_names = []
    temp_input_label = _get_input_feature(dataset)
    for i in temp_input_label:
        category = str(i.get_value(label_class_field))
        if category not in class_names:
            class_names.append(category)

    if out_path is not None:
        dic_voc_yml = OrderedDict({"class_names": class_names})
        save_config_to_yaml(dic_voc_yml, os.path.join(out_path, out_name + ".yml"))
    return class_names


def get_classe_names_from_model(model_config, out_path=None, out_name=None):
    """ class_names = get_classe_names(dataset, label_class_field, out_path=None)

        通过矢量数据集获取记录集中的所有类别

        :param dataset: 数据集
        :type dataset: DataSetVector
        :param label_class_field: 游标类型，可以为枚举值或名称
        :type label_class_field: CursorType or str
        :param out_path: 输出文件路径
        :type out_path: str
        :param out_name: 输出文件名称
        :type out_name: str
        :return class_names : 记录集中类别信息
        :rtype: list
        """
    with open(model_config) as f:
        config_dict = yaml.load(f, Loader=(yaml.FullLoader))
    config = DotMap(config_dict)
    config.get("model").get("categorys").remove("__background__")
    class_names = config.get("model").get("categorys")
    if out_path is not None & out_name is not None:
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        dic_voc_yml = OrderedDict({"class_names": class_names})
        save_config_to_yaml(dic_voc_yml, os.path.join(out_path, out_name + ".yml"))
    return class_names

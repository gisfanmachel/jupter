# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\analyst\_tabular\classification\cls_data_loader.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 3196 bytes
"""
@author: YangRuijie
@license: 
@contact: yangruijie@supermap.com
@software: 
@file: base_data_loader.py
@time: 5/21/20 12:25 PM
@desc:
"""
import os, random
from collections import OrderedDict
import pandas as pd, pickle
from base.base_dataloader import BaseDataloader
from toolkit._toolkit import save_config_to_yaml, get_config_from_yaml

def create_cls_tabular_data(input_data, label_class_field, output_path, output_name, class_count=None):
    """
    制作训练数据
    :param input_data:
    :param label_class_field:
    :param output_path:
    :param output_name:
    :param class_count:
    :return:
    """
    output_path = os.path.join(output_path, output_name)
    os.makedirs(output_path, exist_ok=True)
    out_sda_path = os.path.join(output_path, output_name + ".sda")
    out_data_path = os.path.join(output_path, "data.pkl")
    df = pd.read_csv(input_data)
    unique = df[label_class_field].unique()
    unique_dict = {v: i for i, v in enumerate(unique)}

    def replace_v(x):
        x[0] = unique_dict[x[0]]
        return x

    df = df.apply(replace_v, axis=1)
    x_feature_names = list(df.columns.values)
    x_feature_names.remove(label_class_field)
    pickle.dump(df, open(out_data_path, "wb"))
    dic_cls_tabular_sda = OrderedDict({"dataset": (OrderedDict({'name':"example_cls_tabular",  'data_type':"cls_tabular", 
                 'x_names':x_feature_names, 
                 'x_count':len(x_feature_names), 
                 'y_name':label_class_field, 
                 'data_path':"data.pkl", 
                 'class_type':OrderedDict(unique_dict)}))})
    save_config_to_yaml(dic_cls_tabular_sda, out_sda_path)


class ClsDataloader(BaseDataloader):

    def __init__(self, sda_path):
        self.sda_path = sda_path
        self.data_config = get_config_from_yaml(self.sda_path)
        self.base_dir = os.path.dirname(sda_path)
        self.data_path = os.path.join(self.base_dir, self.data_config.dataset.data_path)
        self.data = pickle.load(open(self.data_path, "rb"))
        self.x_names = self.data_config.dataset.x_names
        self.y_name = self.data_config.dataset.y_name

    def load(self, test_size=0.3, random_seed=None):
        index = [i for i in range(self.data.values.shape[0])]
        random.seed(random_seed)
        random.shuffle(index)
        train_end = int(len(index) * (1 - test_size))
        train_x, train_y = self.data[self.x_names].values[(None[:train_end], None[:None])], self.data[[self.y_name]].values[None[:train_end]]
        test_x, test_y = self.data[self.x_names].values[(train_end[:None], None[:None])], self.data[[self.y_name]].values[train_end[:None]]
        return (
         train_x, test_x, train_y, test_y)

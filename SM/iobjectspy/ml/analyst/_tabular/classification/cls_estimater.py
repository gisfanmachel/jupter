# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\analyst\_tabular\classification\cls_estimater.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 1739 bytes
"""
@author: YangRuijie
@license: 
@contact: yangruijie@supermap.com
@software: 
@file: base_estimater.py
@time: 5/21/20 12:28 PM
@desc:
"""
import os.path as osp
import pickle, numpy as np, pandas as pd
from toolkit._toolkit import get_config_from_yaml
from base.base_estimater import BaseEstimater

class ClsEstimater(BaseEstimater):

    def __init__(self, model_path, **kwargs):
        self.sdm_path = model_path
        self.model_base_name = osp.splitext(osp.basename(self.sdm_path))[0]
        self.model_pkl_path = osp.join(osp.dirname(model_path), self.model_base_name + ".pkl")
        with open(self.model_pkl_path, "rb") as f:
            self.model = pickle.load(f)
        self.config = get_config_from_yaml(self.sdm_path)
        self.class_type = self.config.class_type
        self.sort_class_type = list(sorted((self.class_type.items()), key=(lambda d: d[1])))

    def estimate_line(self, features):
        proa = self.model.predict_proba(np.expand_dims((np.array(features)), axis=0))
        result_dict = {}
        for i, p in enumerate(list(proa[(0, None[:None])])):
            result_dict[self.sort_class_type[i][0]] = p

        return result_dict

    def estimate_file(self, input_data, out_data, out_dataset_name=None):
        df = pd.read_csv(input_data)
        result = self.model.predict_proba(df.values[(None[:None], 1[:None])])
        result_df = pd.DataFrame(data=result, columns=[n[0] for n in self.sort_class_type])
        result_df.to_csv(out_data, index=False)
        return (
         result_df, out_data)

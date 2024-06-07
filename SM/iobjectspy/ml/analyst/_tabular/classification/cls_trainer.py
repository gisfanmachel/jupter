# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\analyst\_tabular\classification\cls_trainer.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 2931 bytes
"""
@author: YangRuijie
@license: 
@contact: yangruijie@supermap.com
@software: 
@file: base_trainer.py
@time: 5/21/20 12:26 PM
@desc:
"""
import os, pickle
from collections import OrderedDict
from xgboost import XGBClassifier
from toolkit._tabular_utils import f1_score
from .cls_data_loader import ClsDataloader
from ..base import BaseTrainer
from toolkit._toolkit import save_config_to_yaml, get_config_from_yaml

class ClsTrainer(BaseTrainer):

    def __init__(self):
        pass

    def find_best_params(self):
        pass

    def train(self, train_data_path, config, lr, output_model_path, output_model_name, model_params=None, test_size=0.2, **kwargs):
        self.data_config = get_config_from_yaml(train_data_path)
        self.train_config = get_config_from_yaml(config)
        data_loader = ClsDataloader(train_data_path)
        train_x, test_x, train_y, test_y = data_loader.load(test_size=test_size, random_seed=None)
        if len(self.data_config.dataset.class_type) > 2:
            objective = "multi:softprob"
            eval_metric = "mlogloss"
        xgb_params = {
         'n_estimators': 325, 
         'max_depth': 3, 
         'min_child_weight': 1, 
         'gamma': 0, 
         'subsample': 0.3, 
         'colsample_bytree': 0.7, 
         'colsample_bylevel': 0.5, 
         'objective': objective}
        config_model_params = self.train_config.model.model_params.toDict()
        if config_model_params is not None:
            xgb_params.update(config_model_params)
        if model_params is not None:
            xgb_params.update(model_params)
        print(xgb_params)
        xgb = XGBClassifier(learning_rate=lr, 
         seed=3, **xgb_params)
        xgb.fit(train_x, train_y, eval_set=[(test_x, test_y)], eval_metric=eval_metric, early_stopping_rounds=200)
        val_f1 = f1_score(test_y, (xgb.predict(test_x)), average="micro")
        print("valdata_f1: {}".format(val_f1))
        output_model_path = os.path.join(output_model_path, output_model_name)
        os.makedirs(output_model_path, exist_ok=True)
        output_model_sdm = os.path.join(output_model_path, output_model_name + ".sdm")
        output_model_file = os.path.join(output_model_path, output_model_name + ".pkl")
        with open(output_model_file, "wb") as f:
            pickle.dump(xgb, f)
        dict_model_sdm = OrderedDict({'model_type':"", 
         'framework':"xgb", 
         'model_architecture':"", 
         'model_categorys':"", 
         'model_tag':"standard", 
         'class_type':OrderedDict(self.data_config.dataset.class_type)})
        save_config_to_yaml(dict_model_sdm, output_model_sdm)

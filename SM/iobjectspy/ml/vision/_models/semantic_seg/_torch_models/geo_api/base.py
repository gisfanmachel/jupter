# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_torch_models\geo_api\base.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 1779 bytes
import os.path as osp
import shutil, torch
from torch import nn

class BaseTorchEstimation:

    def __init__(self, model_path, config):
        pass

    def estimate_img(self):
        pass

    def estimate_tile(self):
        pass

    def load_model(self, model_path):
        pass

    def close_model(self):
        pass

    @torch.no_grad()
    def _predict_tile_local(self, predict_tile, out_shape):
        pass

    @torch.no_grad()
    def _predict_on_batch(self, predict_tiles, out_shape):
        pass


class BaseTorchTrainer:

    def __init__(self):
        pass

    def train(self):
        pass

    def _saving_model(self):
        pass

    def init_callbacks(self, log_path):
        pass

    def _save_model_pth(self, i, model, model_clone, replace=True, **kwargs):
        try:
            model_sd = model.module.state_dict()
        except:
            model_sd = model.state_dict()

        model_clone.load_state_dict(model_sd)
        save_name, ext = osp.splitext(self.torch_model_path)
        if isinstance(model, nn.parallel.DistributedDataParallel):
            if kwargs.get("local_rank") == 0:
                torch.save(model_clone, save_name + "_" + str(i + 1) + ext)
                if replace:
                    shutil.move(save_name + "_" + str(i + 1) + ext, self.torch_model_path)
                else:
                    shutil.copy(save_name + "_" + str(i + 1) + ext, self.torch_model_path)
        else:
            torch.save(model_clone, save_name + "_" + str(i + 1) + ext)
            if replace:
                shutil.move(save_name + "_" + str(i + 1) + ext, self.torch_model_path)
            else:
                shutil.copy(save_name + "_" + str(i + 1) + ext, self.torch_model_path)

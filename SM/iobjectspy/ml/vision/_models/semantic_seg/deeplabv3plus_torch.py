# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\deeplabv3plus_torch.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 1160 bytes
from _torch_models.geo_api.predict_api import SegTorchEstimation
from _torch_models.geo_api.model_builder import build_torch_seg_model
from _torch_models.geo_api.train_api import SegTorchTrainer

class Deeplabv3PlusEstimation(SegTorchEstimation):

    def __init__(self, model_path, config, test_aug=False, **kwargs):
        (super(Deeplabv3PlusEstimation, self).__init__)(model_path, config, test_aug, **kwargs)


class Deeplabv3PlusTrainer(SegTorchTrainer):

    def __init__(self):
        super().__init__()
        self.callbacks = []
        self.loss = []
        self.acc = []
        self.val_loss = []
        self.val_acc = []
        self.model_architecture = "deeplabv3plus"

    def get_model(self):
        self.model_architecture = "deeplabv3plus"
        model = build_torch_seg_model(in_channels=(self.data_config.dataset.x_bandnum),
          classes=(len(self.class_type) if len(self.class_type) > 2 else 1),
          backbone_name=(self.backbone_name),
          encoder_weights=(self.encoder_weights),
          net_type="deeplabv3plus",
          activation=(self.activation))
        return model

# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_torch_models\util\train.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 5017 bytes
import sys, time, torch
from tqdm import tqdm
from .meter import AverageValueMeter

class Epoch:

    def __init__(self, model, loss, metrics, stage_name, device='cpu', verbose=True):
        self.model = model
        self.loss = loss
        self.metrics = metrics
        self.stage_name = stage_name
        self.verbose = verbose
        self.device = device
        self._to_device()

    def _to_device(self):
        self.model.to(self.device)
        self.loss.to(self.device)
        for metric in self.metrics:
            metric.to(self.device)

    def _format_logs(self, logs):
        str_logs = ["{} - {:.4}".format(k, v) for k, v in logs.items()]
        s = ", ".join(str_logs)
        return s

    def batch_update(self, x, y):
        raise NotImplementedError

    def on_epoch_start(self):
        pass

    def run(self, dataloader):
        self.on_epoch_start()
        logs = {}
        loss_meter = AverageValueMeter()
        metrics_meters = {metric.__name__: AverageValueMeter() for metric in self.metrics}
        import time
        with tqdm(dataloader, desc=(self.stage_name), file=(sys.stdout), disable=(not self.verbose)) as iterator:
            for x, y in iterator:
                x, y = x.to(self.device), y.to(self.device)
                loss, y_pred = self.batch_update(x, y)
                if hasattr(self, "optimizer"):
                    lr = self.optimizer.param_groups[0]["lr"]
                    s = self.optimizer.state_dict()
                    lr_logs = {"lr": lr}
                    logs.update(lr_logs)
                loss_value = loss.cpu().detach().numpy()
                loss_meter.add(loss_value)
                loss_logs = {(self.loss.__name__): (loss_meter.mean)}
                logs.update(loss_logs)
                for metric_fn in self.metrics:
                    metric_value = metric_fn(y_pred, y).cpu().detach().numpy()
                    metrics_meters[metric_fn.__name__].add(metric_value)

                metrics_logs = {k: v.mean for k, v in metrics_meters.items()}
                logs.update(metrics_logs)
                if self.verbose:
                    s = self._format_logs(logs)
                    iterator.set_postfix_str(s)

        return logs


class TrainEpoch(Epoch):

    def __init__(self, model, loss, metrics, optimizer, device='cpu', verbose=True, warm_step=None, total_step=None, **kwargs):
        super().__init__(model=model,
          loss=loss,
          metrics=metrics,
          stage_name="train",
          device=device,
          verbose=verbose)
        self.optimizer = optimizer
        self.init_lr = self.optimizer.param_groups[0]["lr"]
        self.global_step = 0
        self.total_step = total_step
        if self.total_step:
            if warm_step:
                self.warm_step = warm_step
            else:
                self.warm_step = int(total_step * 0.2)
        else:
            self.warm_step = warm_step
        self.lr_sh = kwargs.get("lr_sh")

    def on_epoch_start(self):
        self.model.train()

    def batch_update(self, x, y):
        self.global_step += 1
        self.optimizer.zero_grad()
        prediction = self.model.forward(x)
        loss = self.loss(prediction, y)
        loss.backward()
        self.optimizer.step()
        return (
         loss, prediction)


class ValidEpoch(Epoch):

    def __init__(self, model, loss, metrics, device='cpu', verbose=True):
        super().__init__(model=model,
          loss=loss,
          metrics=metrics,
          stage_name="valid",
          device=device,
          verbose=verbose)

    def on_epoch_start(self):
        self.model.eval()

    def batch_update(self, x, y):
        with torch.no_grad():
            prediction = self.model.forward(x)
            loss = self.loss(prediction, y)
        return (
         loss, prediction)

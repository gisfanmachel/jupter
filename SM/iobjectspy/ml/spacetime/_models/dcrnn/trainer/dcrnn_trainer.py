# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\spacetime\_models\dcrnn\trainer\dcrnn_trainer.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 8659 bytes
import numpy as np, torch
from ..base import BaseTrainer
import math, time
from tqdm import tqdm

class DCRNNTrainer(BaseTrainer):
    __doc__ = "\n    DCRNN trainer class\n    "

    def __init__(self, model, loss, metrics, optimizer, config, data_loader, epochs=None, valid_data_loader=None, lr_scheduler=None, len_epoch=None, val_len_epoch=None):
        super(DCRNNTrainer, self).__init__(model, loss, metrics, optimizer, config)
        self.config = config
        self.data_loader = data_loader
        if epochs is not None:
            if isinstance(epochs, int):
                self.epochs = epochs
        else:
            self.len_epoch = len_epoch
            self.val_len_epoch = val_len_epoch
            self.cl_decay_steps = config["trainer"]["cl_decay_steps"]
            self.null_val = config["metrics"]["null_val"]
            self.max_grad_norm = config["trainer"]["max_grad_norm"]
            self.valid_data_loader = valid_data_loader
            self.do_validation = self.valid_data_loader is not None
            self.lr_scheduler = lr_scheduler
            self.log_step = int(20)
            self._n_gpu = config["n_gpu"]
            self._seq_len = config["arch"]["args"]["seq_len"]
            self._output_dim = 0
            self._base_size = 0
            self._num_nodes = 0
            if self._n_gpu > 1:
                self._output_dim = self.model.module.output_dim
                self._batch_size = self.model.module.batch_size * self._n_gpu
                self._num_nodes = self.model.module.num_nodes
            else:
                self._output_dim = self.model.output_dim
            self._batch_size = self.model.batch_size
            self._num_nodes = self.model.num_nodes
        print("output_dim=", self._output_dim)

    def _eval_metrics(self, output, target):
        acc_metrics = np.zeros(len(self.metrics))
        for i, metric in enumerate(self.metrics):
            acc_metrics[i] += metric(output, target, null_val=(self.null_val))

        return acc_metrics

    def _train_epoch(self, epoch):
        """
        Training logic for an epoch

        :param epoch: Current training epoch.
        :return: A log that contains all information you want to save.

        Note:
            If you have additional information to record, for example:
                > additional_log = {"x": x, "y": y}
            merge it with log before return. i.e.
                > log = {**log, **additional_log}
                > return log

            The metrics in log must have the key 'metrics'.
        """
        self.model.train()
        start_time = time.time()
        total_loss = 0
        total_metrics = np.zeros(len(self.metrics))
        for batch_idx, (data, target) in enumerate(self.data_loader.get_iterator()):
            data = torch.FloatTensor(data)
            target = torch.FloatTensor(target)
            label = target[(..., None[:self._output_dim])]
            data, target = data.to(self.device), target.to(self.device)
            self.optimizer.zero_grad()
            global_step = (epoch - 1) * self.len_epoch + batch_idx
            teacher_forcing_ratio = self._compute_sampling_threshold(global_step, self.cl_decay_steps)
            output = self.model(data, target, teacher_forcing_ratio)
            output = torch.transpose(output.view(self._seq_len, self._batch_size, self.model.num_nodes, self.model.output_dim), 0, 1)
            loss = self.loss(output.cpu(), label)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.max_grad_norm)
            self.optimizer.step()
            training_time = time.time() - start_time
            total_loss += loss.item()
            total_metrics += self._eval_metrics(output.detach().numpy(), label.numpy())
            if batch_idx % self.log_step == 0:
                self.logger.debug("Train Epoch: {} {} Loss: {:.6f}".format(epoch, self._progress(batch_idx), loss.item()))
                print("Train Epoch: {} {} Loss: {:.6f}".format(epoch, self._progress(batch_idx), loss.item()))
            if batch_idx == self.len_epoch:
                break

        log = {'loss':total_loss / (self.len_epoch), 
         'metrics':((total_metrics / self.len_epoch).tolist)()}
        if self.do_validation:
            val_log = self._valid_epoch(epoch)
            log.update(val_log)
        if self.lr_scheduler is not None:
            self.lr_scheduler.step()
        log.update({"Time": ("{:.4f}s".format(training_time))})
        return (log, training_time)

    def _valid_epoch(self, epoch):
        """
        Validate after training an epoch

        :return: A log that contains information about validation

        Note:
            The validation metrics in log must have the key 'val_metrics'.
        """
        self.model.eval()
        total_val_loss = 0
        total_val_metrics = np.zeros(len(self.metrics))
        with torch.no_grad():
            for batch_idx, (data, target) in enumerate(self.valid_data_loader.get_iterator()):
                data = torch.FloatTensor(data)
                target = torch.FloatTensor(target)
                label = target[(..., None[:self.model.output_dim])]
                data, target = data.to(self.device), target.to(self.device)
                output = self.model(data, target, 0)
                output = torch.transpose(output.view(self._seq_len, self.model.batch_size, self.model.num_nodes, self.model.output_dim), 0, 1)
                loss = self.loss(output.cpu(), label)
                total_val_loss += loss.item()
                total_val_metrics += self._eval_metrics(output.detach().numpy(), label.numpy())

        return {'val_loss':total_val_loss / (self.val_len_epoch), 
         'val_metrics':((total_val_metrics / self.val_len_epoch).tolist)()}

    def _progress(self, batch_idx):
        base = "[{}/{} ({:.0f}%)]"
        if hasattr(self.data_loader, "n_samples"):
            current = batch_idx * self.data_loader.batch_size
            total = self.data_loader.n_samples
        else:
            current = batch_idx
            total = self.len_epoch
        return base.format(current, total, 100.0 * current / total)

    @staticmethod
    def _compute_sampling_threshold(global_step, k):
        """
        Computes the sampling probability for scheduled sampling using inverse sigmoid.
        :param global_step:
        :param k:
        :return:
        """
        return k / (k + math.exp(global_step / k))

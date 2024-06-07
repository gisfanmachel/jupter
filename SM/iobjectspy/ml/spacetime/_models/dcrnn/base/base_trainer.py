# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\spacetime\_models\dcrnn\base\base_trainer.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 8439 bytes
import torch
from abc import abstractmethod
from numpy import inf

class BaseTrainer:
    __doc__ = "\n    Base class for all trainers\n    "

    def __init__(self, model, loss, metrics, optimizer, config):
        self.config = config
        self.logger = config.get_logger("trainer", config["trainer"]["verbosity"])
        self.device, device_ids = self._prepare_device(config["n_gpu"])
        self.model = model.to(self.device)
        if len(device_ids) > 1:
            self.model = torch.nn.DataParallel(model, device_ids=device_ids, dim=0)
        self.loss = loss
        self.metrics = metrics
        self.optimizer = optimizer
        cfg_trainer = config["trainer"]
        self.epochs = cfg_trainer["epochs"]
        self.save_period = cfg_trainer["save_period"]
        self.monitor = cfg_trainer.get("monitor", "off")
        if self.monitor == "off":
            self.mnt_mode = "off"
            self.mnt_best = 0
        else:
            self.mnt_mode, self.mnt_metric = self.monitor.split()
            assert self.mnt_mode in ('min', 'max')
            self.mnt_best = inf if self.mnt_mode == "min" else -inf
            self.early_stop = cfg_trainer.get("early_stop", inf)
        self.start_epoch = 1
        self.checkpoint_dir = config.save_dir
        if config.resume is not None:
            self._resume_checkpoint(config.resume)

    @abstractmethod
    def _train_epoch(self, epoch):
        """
        Training logic for an epoch

        :param epoch: Current epoch number
        """
        raise NotImplementedError

    def trainParse error at or near `LOAD_DICTCOMP' instruction at offset 104

    def _prepare_device(self, n_gpu_use):
        """
        setup GPU device if available, move model into configured device
        """
        n_gpu = torch.cuda.device_count()
        if n_gpu_use > 0:
            if n_gpu == 0:
                self.logger.warning("Warning: There's no GPU available on this machine,training will be performed on CPU.")
                n_gpu_use = 0
        if n_gpu_use > n_gpu:
            self.logger.warning("Warning: The number of GPU's configured to use is {}, but only {} are available on this machine.".format(n_gpu_use, n_gpu))
            n_gpu_use = n_gpu
        device = torch.device("cuda:0" if n_gpu_use > 0 else "cpu")
        list_ids = list(range(n_gpu_use))
        return (device, list_ids)

    def _save_checkpoint(self, epoch, save_best=False):
        """
        Saving checkpoints

        :param epoch: current epoch number
        :param log: logging information of the epoch
        :param save_best: if True, rename the saved checkpoint to 'model_best.pth'
        """
        arch = type(self.model).__name__
        state = {'arch':arch, 
         'epoch':epoch, 
         'state_dict':(self.model.state_dict)(), 
         'optimizer':(self.optimizer.state_dict)(), 
         'monitor_best':self.mnt_best}
        if save_best:
            best_path = str(self.checkpoint_dir / "graph_streg_metrla.pth")
            torch.save(state, best_path)
            self.logger.info("Saving current best: graph_streg_metrla.pth ...")
        else:
            filename = str(self.checkpoint_dir / "graph_streg_metrla.pth")
            torch.save(state, filename)
            self.logger.info("Saving checkpoint: {} ...".format(filename))

    def _resume_checkpoint(self, resume_path):
        """
        Resume from saved checkpoints

        :param resume_path: Checkpoint path to be resumed
        """
        resume_path = str(resume_path)
        self.logger.info("Loading checkpoint: {} ...".format(resume_path))
        if torch.cuda.is_available():
            map_location = lambda storage, loc: storage.cuda()
        else:
            map_location = "cpu"
        checkpoint = torch.load(resume_path, map_location=map_location)
        self.start_epoch = 1
        self.mnt_best = checkpoint["monitor_best"]
        self.model.load_state_dict(checkpoint["state_dict"])
        self.optimizer.load_state_dict(checkpoint["optimizer"])
        self.logger.info("Checkpoint loaded. Resume training from epoch {}".format(self.start_epoch))
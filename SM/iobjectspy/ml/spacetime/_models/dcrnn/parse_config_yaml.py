# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\spacetime\_models\dcrnn\parse_config_yaml.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 5769 bytes
import os, logging
from pathlib import Path
from functools import reduce
from operator import getitem
from datetime import datetime
from .logger import setup_logging
from lib.utils import read_yaml, write_yaml
from dotmap import DotMap

class ConfigParser:

    def __init__(self, args, options='', timestamp=True):
        if args.resume:
            self.resume = Path(args.resume)
            self.cfg_fname = self.resume.parent / "graph_streg_metrla.sdm"
        else:
            msg_no_cfg = "Configuration file need to be specified. Add '-c config.yaml', for example."
            assert args.config is not None, msg_no_cfg
            self.resume = None
            self.cfg_fname = Path(args.config)
        config_suffix = os.path.splitext(self.cfg_fname)[1]
        self._train = config_suffix == ".sdt"
        config = read_yaml(self.cfg_fname)
        self._config = _update_config(config, options, args)
        self._graph_pkl_filename = self.config["graph_pkl_filename"]
        if args.graph_pkl_filename:
            self._graph_pkl_filename = args.graph_pkl_filename
        self._input_data_dir = self.config["dataloader"]["args"]["data_dir"]
        if args.input_data_dir:
            self._input_data_dir = args.input_data_dir
        elif hasattr(args, "out_data"):
            if args.out_data:
                self.out_data = args.out_data
            elif hasattr(args, "output_model_path"):
                save_dir = Path(args.output_model_path)
            else:
                save_dir = Path(self.config.trainer.save_dir)
            timestamp = datetime.now().strftime("%m%d_%H%M%S") if timestamp else ""
            exper_name = self.config.name
            self._save_dir = save_dir
            self.save_dir.mkdir(parents=True, exist_ok=True)
            if self._train:
                sdm_config = DotMap()
                sdm_config["model_type"] = config["model_type"]
                sdm_config["framework"] = config["framework"]["name"]
                sdm_config["model_architecture"] = config["model"]["name"]
                sdm_config["name"] = config["name"]
                sdm_config["n_gpu"] = config["n_gpu"]
                sdm_config["graph_pkl_filename"] = config["graph_pkl_filename"]
                sdm_config["arch"] = config["arch"]
                sdm_config["dataloader"] = config["dataloader"]
                sdm_config["optimizer"] = config["optimizer"]
                sdm_config["loss"] = config["loss"]
                sdm_config["metrics"] = config["metrics"]
                sdm_config["lr_scheduler"] = config["lr_scheduler"]
                sdm_config["trainer"] = config["trainer"]
        else:
            sdm_config = config
        write_yaml(sdm_config.toDict(), self.save_dir / "graph_streg_metrla.sdm")
        self.log_levels = {0:logging.WARNING, 
         1:logging.INFO, 
         2:logging.DEBUG}

    def initialize(self, name, module, *args, **kwargs):
        """
        finds a function handle with the name given as 'type' in config, and returns the
        instance initialized with corresponding keyword args given as 'args'.
        """
        module_name = self[name]["type"]
        module_args = self[name]["args"].toDict()
        assert all([k not in module_args for k in kwargs]), "Overwriting kwargs given in config file is not allowed"
        module_args.update(kwargs)
        return (getattr(module, module_name))(*args, **module_args)

    def __getitem__(self, name):
        return self.config[name]

    def get_logger(self, name, verbosity=2):
        msg_verbosity = "verbosity option {} is invalid. Valid options are {}.".format(verbosity, self.log_levels.keys())
        assert verbosity in self.log_levels, msg_verbosity
        logger = logging.getLogger(name)
        logger.setLevel(self.log_levels[verbosity])
        return logger

    @property
    def config(self):
        return self._config

    @property
    def save_dir(self):
        return self._save_dir

    @property
    def graph_pkl_filename(self):
        return self._graph_pkl_filename

    @property
    def input_data_dir(self):
        return self._input_data_dir


def _update_config(config, options, args):
    for opt in options:
        value = getattr(args, _get_opt_name(opt.flags))
        if value is not None:
            _set_by_path(config, opt.target, value)

    return config


def _get_opt_name(flags):
    for flg in flags:
        if flg.startswith("--"):
            return flg.replace("--", "")

    return flags[0].replace("--", "")


def _set_by_path(tree, keys, value):
    """Set a value in a nested object in tree by sequence of keys."""
    _get_by_path(tree, keys[None[:-1]])[keys[-1]] = value


def _get_by_path(tree, keys):
    """Access a nested object in tree by sequence of keys."""
    return reduce(getitem, keys, tree)

# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\spacetime\_models\dcrnn\lib\utils.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 8002 bytes
import logging, numpy as np, os, pickle
import scipy.sparse as sp
import sys
from scipy.sparse import linalg
import json
from pathlib import Path
from datetime import datetime
from itertools import repeat
from collections import OrderedDict
import yaml
from dotmap import DotMap

def ensure_dir(dirname):
    dirname = Path(dirname)
    if not dirname.is_dir():
        dirname.mkdir(parents=True, exist_ok=False)


def read_yaml(fname):
    """read_yaml. 读取配置文件
    :param fname: 配置文件的路径名
    """
    with fname.open("rt") as handle:
        config_dict = yaml.load(handle, Loader=(yaml.FullLoader))
        config = DotMap(config_dict)
        return config


def read_json(fname):
    with fname.open("rt") as handle:
        return json.load(handle, object_hook=OrderedDict)


def write_json(content, fname):
    with fname.open("wt") as handle:
        json.dump(content, handle, indent=4, sort_keys=False)


def write_yaml(content, fname):
    with fname.open("wt") as handle:
        yaml.dump(content, handle, default_flow_style=False, indent=4, sort_keys=False)


def inf_loop(data_loader):
    """
    wrapper function for endless data loader.
    """
    for loader in repeat(data_loader):
        yield from loader

    if False:
        yield None


class Timer:

    def __init__(self):
        self.cache = datetime.now()

    def check(self):
        now = datetime.now()
        duration = now - self.cache
        self.cache = now
        return duration.total_seconds()

    def reset(self):
        self.cache = datetime.now()


class DataLoader(object):

    def __init__(self, xs, ys, batch_size, pad_with_last_sample=True, shuffle=False):
        """

        :param xs:
        :param ys:
        :param batch_size:
        :param pad_with_last_sample: pad with the last sample to make number of samples divisible to batch_size.
        """
        self.batch_size = batch_size
        self.current_ind = 0
        if pad_with_last_sample:
            num_padding = (batch_size - len(xs) % batch_size) % batch_size
            x_padding = np.repeat((xs[(-1)[:None]]), num_padding, axis=0)
            y_padding = np.repeat((ys[(-1)[:None]]), num_padding, axis=0)
            xs = np.concatenate([xs, x_padding], axis=0)
            ys = np.concatenate([ys, y_padding], axis=0)
        self.size = len(xs)
        self.num_batch = int(self.size // self.batch_size)
        if shuffle:
            permutation = np.random.permutation(self.size)
            xs, ys = xs[permutation], ys[permutation]
        self.xs = xs
        self.ys = ys

    def get_iterator(self):
        self.current_ind = 0

        def _wrapper():
            while self.current_ind < self.num_batch:
                start_ind = self.batch_size * self.current_ind
                end_ind = min(self.size, self.batch_size * (self.current_ind + 1))
                x_i = self.xs[(start_ind[:end_ind], ...)]
                y_i = self.ys[(start_ind[:end_ind], ...)]
                yield (x_i, y_i)
                self.current_ind += 1

        return _wrapper()


class StandardScaler:
    __doc__ = "\n    Standard the input\n    "

    def __init__(self, mean, std):
        self.mean = mean
        self.std = std

    def transform(self, data):
        return (data - self.mean) / self.std

    def inverse_transform(self, data):
        return data * self.std + self.mean


def calculate_normalized_laplacian(adj):
    """
    # L = D^-1/2 (D-A) D^-1/2 = I - D^-1/2 A D^-1/2
    # D = diag(A 1)
    :param adj:
    :return:
    """
    adj = sp.coo_matrix(adj)
    d = np.array(adj.sum(1))
    d_inv_sqrt = np.power(d, -0.5).flatten()
    d_inv_sqrt[np.isinf(d_inv_sqrt)] = 0.0
    d_mat_inv_sqrt = sp.diags(d_inv_sqrt)
    normalized_laplacian = sp.eye(adj.shape[0]) - adj.dot(d_mat_inv_sqrt).transpose().dot(d_mat_inv_sqrt).tocoo()
    return normalized_laplacian


def calculate_random_walk_matrix(adj_mx):
    adj_mx = sp.coo_matrix(adj_mx)
    d = np.array(adj_mx.sum(1))
    d_inv = np.power(d, -1).flatten()
    d_inv[np.isinf(d_inv)] = 0.0
    d_mat_inv = sp.diags(d_inv)
    random_walk_mx = d_mat_inv.dot(adj_mx).tocoo()
    return random_walk_mx


def calculate_reverse_random_walk_matrix(adj_mx):
    return calculate_random_walk_matrix(np.transpose(adj_mx))


def calculate_scaled_laplacian(adj_mx, lambda_max=2, undirected=True):
    if undirected:
        adj_mx = np.maximum.reduce([adj_mx, adj_mx.T])
    L = calculate_normalized_laplacian(adj_mx)
    if lambda_max is None:
        lambda_max, _ = linalg.eigsh(L, 1, which="LM")
        lambda_max = lambda_max[0]
    M, _ = L.shape
    I = sp.identity(M, format="coo", dtype=(L.dtype))
    L = 2 / lambda_max * L - I
    return L.tocoo()


def config_logging(log_dir, log_filename="info.log", level=logging.INFO):
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    try:
        os.makedirs(log_dir)
    except OSError:
        pass

    file_handler = logging.FileHandler(os.path.join(log_dir, log_filename))
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level=level)
    console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(level=level)
    logging.basicConfig(handlers=[file_handler, console_handler], level=level)


def get_logger(log_dir, name, log_filename="info.log", level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler = logging.FileHandler(os.path.join(log_dir, log_filename))
    file_handler.setFormatter(formatter)
    console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.info("Log directory: %s", log_dir)
    return logger


def count_parameters(model):
    return sum((p.numel() for p in model.parameters() if p.requires_grad))


def load_dataset(dataset_dir, batch_size, test_batch_size=None, **kwargs):
    data = {}
    for category in ('train', 'val', 'test'):
        cat_data = np.load(os.path.join(dataset_dir, category + ".npz"))
        data["x_" + category] = cat_data["x"]
        data["y_" + category] = cat_data["y"]

    scaler = StandardScaler(mean=(data["x_train"][(Ellipsis, 0)].mean()), std=(data["x_train"][(Ellipsis,
                                                                                                0)].std()))
    for category in ('train', 'val', 'test'):
        data["x_" + category][(Ellipsis, 0)] = scaler.transform(data["x_" + category][(Ellipsis,
                                                                                       0)])
        data["y_" + category][(Ellipsis, 0)] = scaler.transform(data["y_" + category][(Ellipsis,
                                                                                       0)])

    data["train_loader"] = DataLoader((data["x_train"]), (data["y_train"]), batch_size, shuffle=True)
    data["val_loader"] = DataLoader((data["x_val"]), (data["y_val"]), test_batch_size, shuffle=False)
    data["test_loader"] = DataLoader((data["x_test"]), (data["y_test"]), test_batch_size, shuffle=False)
    data["scaler"] = scaler
    return data


def load_graph_data(pkl_filename):
    sensor_ids, sensor_id_to_ind, adj_mx = load_pickle(pkl_filename)
    return (sensor_ids, sensor_id_to_ind, adj_mx)


def load_pickle(pickle_file):
    try:
        with open(pickle_file, "rb") as f:
            pickle_data = pickle.load(f)
    except UnicodeDecodeError as e:
        try:
            with open(pickle_file, "rb") as f:
                pickle_data = pickle.load(f, encoding="latin1")
        finally:
            e = None
            del e

    except Exception as e:
        try:
            print("Unable to load data ", pickle_file, ":", e)
            raise
        finally:
            e = None
            del e

    return pickle_data

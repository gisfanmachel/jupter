# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\spacetime\_models\dcrnn\test_yaml.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 5935 bytes
import argparse
from lib import utils
import math, os, collections
from parse_config_yaml import ConfigParser
import argparse, torch, numpy as np
from lib import metrics
import model.dcrnn_model as module_arch
from lib import utils
from tqdm import tqdm
import math, time, os, easydict
from lib.utils import write_yaml
from pathlib import Path

def main(config):
    logger = config.get_logger("test")
    graph_pkl_filename = "data/METR-LA/adj_mat.pkl"
    if config.graph_pkl_filename:
        graph_pkl_filename = config.graph_pkl_filename
    _, _, adj_mat = utils.load_graph_data(graph_pkl_filename)
    data = utils.load_dataset(dataset_dir="data/METR-LA", batch_size=(config["arch"]["args"]["batch_size"]),
      test_batch_size=(config["arch"]["args"]["batch_size"]))
    test_data_loader = data["test_loader"]
    scaler = data["scaler"]
    num_test_iteration = math.ceil(data["x_test"].shape[0] / config["arch"]["args"]["batch_size"])
    adj_arg = {"adj_mat": adj_mat}
    model = (config.initialize)("arch", module_arch, **adj_arg)
    logger.info(model)
    logger.info("Loading checkpoint: {} ...".format(config.resume))
    checkpoint = torch.load(config.resume)
    state_dict = checkpoint["state_dict"]
    if config["n_gpu"] > 1:
        model = torch.nn.DataParallel(model)
    model.load_state_dict(state_dict)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    model.eval()
    y_preds = torch.FloatTensor([])
    y_truths = data["y_test"]
    y_truths = scaler.inverse_transform(y_truths)
    predictions = []
    groundtruth = list()
    start_time = time.time()
    with torch.no_grad():
        for i, (x, y) in tqdm((enumerate(test_data_loader.get_iterator())), total=num_test_iteration):
            x = torch.FloatTensor(x).cuda()
            y = torch.FloatTensor(y).cuda()
            outputs = model(x, y, 0)
            y_preds = torch.cat([y_preds, outputs], dim=1)

    inference_time = time.time() - start_time
    logger.info("Inference time: {:.4f} s".format(inference_time))
    y_preds = torch.transpose(y_preds, 0, 1)
    y_preds = y_preds.detach().numpy()
    print("--------test results--------")
    for horizon_i in range(y_truths.shape[1]):
        y_truth = np.squeeze(y_truths[(None[:None], horizon_i, None[:None], 0)])
        y_pred = scaler.inverse_transform(y_preds[(None[:None], horizon_i, None[:None])])
        predictions.append(y_pred)
        groundtruth.append(y_truth)
        mae = metrics.masked_mae_np((y_pred[None[:y_truth.shape[0]]]), y_truth, null_val=0)
        mape = metrics.masked_mape_np((y_pred[None[:y_truth.shape[0]]]), y_truth, null_val=0)
        rmse = metrics.masked_rmse_np((y_pred[None[:y_truth.shape[0]]]), y_truth, null_val=0)
        log = "Horizon {:02d}, MAE: {:.2f}, MAPE: {:.4f}, RMSE: {:.2f}".format(horizon_i + 1, mae, mape, rmse)
        logger.info(log)

    outputs = {'predictions':predictions,  'groundtruth':groundtruth}
    target_dir = "saved/results/"
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    (np.savez_compressed)(*('saved/results/dcrnn_predictions.npz', ), **outputs)
    print("Predictions saved as {}.".format("saved/results/dcrnn_predictions.npz"))


def test_model(checkpoint_path, device=0, graph_pkl_filename=None):
    args = easydict.EasyDict()
    args.graph_pkl_filename = None
    args.resume = None
    args.device = None
    if checkpoint_path is not None:
        if not os.path.exists(checkpoint_path):
            args.resume = False
            print("[ERROR] checkpoint file not exists")
        else:
            args.resume = checkpoint_path
    else:
        if not isinstance(device, int):
            if isinstance(device, str):
                if not device.isdigit():
                    print("[ERROR] device id is not integer")
                else:
                    args.device = device
            else:
                print("[ERROR] wrong type of device ID")
        else:
            args.device = str(device)
        if graph_pkl_filename is not None:
            if not os.path.exists(graph_pkl_filename):
                args.graph_pkl_filename = False
                print("[ERROR] graph pickle file not exists")
            else:
                args.graph_pkl_filename = graph_pkl_filename
    config = ConfigParser(args)
    main(config)


if __name__ == "__main__":
    args = argparse.ArgumentParser(description="PyTorch DCRNN")
    args.add_argument("-c", "--config", default=None, type=str, help="config file path (default: None)")
    args.add_argument("-g", "--graph_pkl_filename", default=None,
      type=str,
      help="graph pkl file path")
    args.add_argument("-r", "--resume", default=None, type=str, help="path to latest checkpoint (default: None)")
    args.add_argument("-d", "--device", default=0, type=str, help="indices of GPUs to enable (default: all)")
    CustomArgs = collections.namedtuple("CustomArgs", "flags type target")
    options = [
     CustomArgs(["--lr", "--learning_rate"], type=float, target=('optimizer', 'args', 'lr')),
     CustomArgs(["--bs", "--batch_size"], type=int, target=('data_loader', 'args', 'batch_size'))]
    args = args.parse_args()
    config = ConfigParser(args)
    main(config)

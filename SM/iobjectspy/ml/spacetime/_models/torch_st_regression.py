# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\spacetime\_models\torch_st_regression.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 15564 bytes
import argparse, math, shutil, pandas as pd, torch, numpy as np
from dcrnn.lib import metrics
from dcrnn.lib import metrics as module_metric
from dcrnn.model import dcrnn_model as module_arch
from dcrnn.parse_config_yaml import ConfigParser
from dcrnn.trainer.dcrnn_trainer import DCRNNTrainer
from dcrnn.lib import utils
from tqdm import tqdm
import time, os, easydict, collections, iobjectspy

class GraphSTRegressionEstimation:

    def __init__(self, model_path, input_data_dir, out_data, location=None, fields_as_point=[
 "longitude", "latitude"]):
        self.location = location
        if not isinstance(model_path, str):
            raise TypeError("model_path 数据类型不正确, 应为 str")
        if not os.path.exists(model_path):
            raise TypeError("model_path 路径不存在")
        self.model_path = model_path
        if not isinstance(input_data_dir, str):
            raise TypeError("intput_data_dir 数据类型不正确, 应为 str")
        if not os.path.exists(input_data_dir):
            raise TypeError("input_data_dir 路径不存在")
        self.input_data_dir = input_data_dir
        if not isinstance(out_data, str):
            raise TypeError("out_data 数据类型不正确, 应为 str")
        self.out_data = out_data

    def _main(self, config):
        logger = config.get_logger("test")
        graph_pkl_filename = os.path.abspath(os.path.join(self.model_path, "..", "adj_mat.pkl"))
        _, _, adj_mat = utils.load_graph_data(graph_pkl_filename)
        if config.input_data_dir:
            dataset_dir = config.input_data_dir
        else:
            dataset_dir = os.path.abspath(config["dataloader"]["args"]["data_dir"])
        data = utils.load_dataset(dataset_dir=dataset_dir,
          batch_size=(config["arch"]["args"]["batch_size"]),
          test_batch_size=(config["arch"]["args"]["batch_size"]))
        test_data_loader = data["test_loader"]
        scaler = data["scaler"]
        num_test_iteration = math.ceil(data["x_test"].shape[0] / config["arch"]["args"]["batch_size"])
        adj_arg = {"adj_mat": adj_mat}
        model = (config.initialize)("arch", module_arch, **adj_arg)
        logger.info(model)
        logger.info("Loading checkpoint: {} ...".format(config.resume))
        if torch.cuda.is_available():

            def map_location(storage, loc):
                return storage.cuda()

        else:
            map_location = "cpu"
        checkpoint = torch.load((config.resume), map_location=map_location)
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
                x = torch.FloatTensor(x)
                y = torch.FloatTensor(y)
                if torch.cuda.device_count() > 0:
                    x = x.cuda()
                    y = y.cuda()
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
            mae = metrics.masked_mae_np((y_pred[None[:y_truth.shape[0]]]),
              y_truth,
              null_val=0)
            mape = metrics.masked_mape_np((y_pred[None[:y_truth.shape[0]]]),
              y_truth,
              null_val=0)
            rmse = metrics.masked_rmse_np((y_pred[None[:y_truth.shape[0]]]),
              y_truth,
              null_val=0)
            log = "Horizon {:02d}, MAE: {:.2f}, MAPE: {:.4f}, RMSE: {:.2f}".format(horizon_i + 1, mae, mape, rmse)
            logger.info(log)
            print(log)

        outputs = {'predictions':predictions,  'groundtruth':groundtruth}
        target_dir = os.path.dirname(self.out_data)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        (np.savez_compressed)((self.out_data), **outputs)
        print("Predictions saved as {}.".format(self.out_data))
        return [predictions, groundtruth]

    def estimate_datatable(self, **kwargs):
        return self._predict_with_datatable(self.model_path)

    def estimate_dataset(self, location_data_path, output, out_dataset_name="dcrnn_prediction", fields_as_point=[
 "longitude", "latitude"]):
        result = self._predict_with_datatable(self.model_path)
        sensor_loc = pd.read_csv(location_data_path)
        sensor_loc.columns = ["index_usr", "sensor_id", "latitude", "longitude"]
        dftest = pd.DataFrame(result[0][0][None[:result[1][0].shape[0]]])
        dftest.columns = [str(i) for i in dftest.columns]
        dftest = dftest.T
        dftest.columns = ["time_" + str(i) for i in dftest.columns]
        dftest["id"] = dftest.index
        dftest = pd.melt(dftest, id_vars="id", var_name="time",
          value_name="speed")
        dftest["id"] = dftest["id"].astype(int)
        sp_res = sensor_loc.merge(dftest, left_on="index_usr",
          right_on="id",
          how="left")

        def progress_function(step_event):
            print("%s-%s" % ("正在矢量化预测结果", step_event.message))

        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as temp_folder:
            sp_res.to_csv((os.path.join(temp_folder, "dcrnn_pred.csv")),
              index=False)
            res_1 = iobjectspy.conversion.import_csv((os.path.join(temp_folder, "dcrnn_pred.csv")),
              output,
              out_dataset_name=out_dataset_name,
              fields_as_point=[
             "longitude", "latitude"],
              progress=None)

    def _predict_with_datatable(self, checkpoint_path, device=0, graph_pkl_filename=None):
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
        elif self.input_data_dir is not None:
            if not os.path.exists(self.input_data_dir):
                print("[ERROR] self.input_data_dir not exists")
            else:
                args.input_data_dir = self.input_data_dir
        else:
            if self.out_data is not None:
                args.out_data = self.out_data
            elif not isinstance(device, int):
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
                args.graph_pkl_filename = os.path.exists(graph_pkl_filename) or False
                print("[ERROR] graph pickle file not exists")
            else:
                args.graph_pkl_filename = graph_pkl_filename
        config = ConfigParser(args)
        return self._main(config)


class GraphSTRegressionTrainer:

    def __init__(self, train_data_path, config, output_model_path, epochs=None, batch_size=None, lr=None, checkpoint_filename=None, graph_pkl_filename=None):
        super().__init__()
        self.train_data_path = train_data_path
        self.config = config
        if epochs is not None:
            if isinstance(epochs, int):
                self.epochs = epochs
        self.output_model_path = output_model_path
        self.checkpoint_filename = checkpoint_filename
        self.lr = lr
        self.batch_size = batch_size
        self.graph_pkl_filename = graph_pkl_filename

    def train(self):
        args = easydict.EasyDict()
        args.graph_pkl_filename = None
        args.config = None
        args.resume = None
        args.device = None
        args.lr = None
        args.bs = None
        args.input_data_dir = None
        if self.output_model_path is not None:
            args.output_model_path = self.output_model_path
        elif self.train_data_path is not None:
            if not os.path.exists(self.train_data_path):
                print("[ERROR] self.input_data_dir not exists")
            else:
                args.input_data_dir = self.train_data_path
        else:
            if not os.path.exists(self.config):
                print("[ERROR] config file not exists")
            else:
                args.config = self.config
            if self.graph_pkl_filename is not None:
                if not os.path.exists(self.graph_pkl_filename):
                    args.graph_pkl_filename = False
                    print("[ERROR] graph pickle file not exists")
                else:
                    args.graph_pkl_filename = self.graph_pkl_filename
            args.graph_pkl_filename = os.path.abspath(os.path.join(self.train_data_path, "adj_mat.pkl"))
            if self.checkpoint_filename is not None:
                args.resume = os.path.exists(self.checkpoint_filename) or False
                print("[ERROR] checkpoint file not exists")
            else:
                args.resume = self.checkpoint_filename
        args.device = "0"
        if self.lr is not None:
            args.lr = self.lr
        if self.batch_size is not None:
            args.bs = self.batch_size
        CustomArgs = collections.namedtuple("CustomArgs", "flags type target")
        options = [
         CustomArgs(["--lr", "--learning_rate"], type=float, target=('optimizer', 'args', 'lr')),
         CustomArgs(["--bs", "--batch_size"], type=int, target=('arch', 'args', 'batch_size'))]
        config = ConfigParser(args, options)
        shutil.copyfile(str(args.graph_pkl_filename), os.path.join(str(args.output_model_path), "adj_mat.pkl"))
        self._dcrnn_train(config)

    def _dcrnn_train(self, config):
        logger = config.get_logger("train")
        print("[INFO] Loading {graph_pkl}".format(graph_pkl=(config.graph_pkl_filename)))
        _, _, adj_mat = utils.load_graph_data(config.graph_pkl_filename)
        if config.input_data_dir:
            dataset_dir = config.input_data_dir
        else:
            dataset_dir = os.path.abspath(config["dataloader"]["args"]["data_dir"])
        data = utils.load_dataset(dataset_dir=dataset_dir,
          batch_size=(config["arch"]["args"]["batch_size"]),
          test_batch_size=(config["arch"]["args"]["batch_size"]))
        for k, v in data.items():
            if hasattr(v, "shape"):
                print(k, v.shape)

        train_data_loader = data["train_loader"]
        val_data_loader = data["val_loader"]
        num_train_sample = data["x_train"].shape[0]
        num_val_sample = data["x_val"].shape[0]
        num_train_iteration_per_epoch = math.ceil(num_train_sample / config["arch"]["args"]["batch_size"])
        num_val_iteration_per_epoch = math.ceil(num_val_sample / config["arch"]["args"]["batch_size"])
        adj_arg = {"adj_mat": adj_mat}
        model = (config.initialize)("arch", module_arch, **adj_arg)
        adj_arg = {"adj_mat": adj_mat}
        print("adj_arg=", adj_mat.shape)
        model = (config.initialize)("arch", module_arch, **adj_arg)
        logger.info(model)
        print("num_nodes=", model.num_nodes)
        loss = (config.initialize)(
         "loss", module_metric, **{"scaler": (data["scaler"])})
        metrics = [getattr(module_metric, met) for met in config["metrics"]["funs"]]
        trainable_params = filter((lambda p: p.requires_grad), model.parameters())
        optimizer = config.initialize("optimizer", torch.optim, trainable_params)
        lr_scheduler = config.initialize("lr_scheduler", torch.optim.lr_scheduler, optimizer)
        trainer = DCRNNTrainer(model, loss, metrics, optimizer, config=config,
          data_loader=train_data_loader,
          epochs=(self.epochs),
          valid_data_loader=val_data_loader,
          lr_scheduler=lr_scheduler,
          len_epoch=num_train_iteration_per_epoch,
          val_len_epoch=num_val_iteration_per_epoch)
        trainer.train()

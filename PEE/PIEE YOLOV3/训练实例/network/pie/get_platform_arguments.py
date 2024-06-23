import json
import os
import time
import argparse
import numpy as np

from pie.train_center.common.metrics_piexl import Metrics_multi
from pie.train_center.middle_result.best import best
from pie.train_center.middle_result.metrics_build_in import metrics_list_bulid_in
from pie.train_center.middle_result.middle_file import save_picture, trainlog_json_epoch
from pie.dataset.dataset import load_dataset
from pie.network.init_model import builder_model
from pie.train_center.pytorch.train_epoch_step import model_gpu_loader
from pie.utils.registry import registry_fun_init
from pie.utils.registry import Registry
from pie.utils import dist_utils

from pie.train_center.common import optimizer_utils
from pie.train_center.common import scheduler_utils


class parse_platform_arguments():
    """
    获取参数并进行相关注册
    :return:
    """

    def __init__(self, root_path="/train"):
        # 程序根目录
        self.root_path = os.path.abspath(root_path)
        # 仅供测试使用，通过traincfg.json文件读入
        # config_path = "./traincfg_sig_diff.json"
        # config_path = "./traincfg_dinknet.json"
        config_path = "./traincfg_yolo.json"
        with open(config_path, 'r', encoding='utf-8') as f:
            params = json.load(f)

        # 解析torch.distributed.launch传入的local_rank参数，表示当前进程在当前node里所有GPU中的rank
        parser = argparse.ArgumentParser(description='PIE AI Training Parameters')
        parser.add_argument("--local_rank", type=int, default=0, help='local rank of this process among all GPUs')
        args = parser.parse_args()
        self.local_rank = args.local_rank

        # conf = input()
        # params = json.loads(conf)

        self.training_id = str(params['training_id'])

        # 数据集
        dataset_id = str(params['dataset_id'])

        # 网络结构相关
        network_info = str(params['network'])

        # 网络结构类型   语义分割 1 目标识别 2 变化检测 3
        self.network_type = int(params['type'])

        # 模型
        network_params = json.loads(network_info)
        self.model_name = str(network_params['model_name'])
        # 主干
        self.model_backbone = None
        if network_params.get('backbone'):
            self.model_backbone = str(network_params['backbone'])
        # 数据增强及数据处理
        trans_pipelines = None
        if network_params.get('transformers'):
            trans_pipelines = str(network_params['transformers'])
        # 输入数据大小
        self.load_size = None
        if params.get('load_size'):
            self.load_size = params['load_size'].split(',')
            self.load_size = input_size_deal(self.load_size)
        self.input_shape = (int(self.load_size[0]), int(self.load_size[1]))

        # 输入网络结构shape
        self.input = None
        if network_params.get('input'):
            self.input = network_params['input']
        # 网络结构冻结层数
        if network_params.get('freeze'):
            freeze = int(network_params['freeze'])
        # 权重文件名称
        self.weight_name = None
        if network_params.get('weight_name'):
            self.weight_name = str(network_params['weight_name'])
        if not self.weight_name:
            self.weight_name = str(network_params['model_name']) + '.th'

        # 权重文件
        self.resume_path = params['resume_path']
        # 输出的相关路径
        # self.root_path = os.path.abspath(os.path.dirname("train.py"))
        self.result_path = self.root_path + '/output/'
        # 各结果文件保存的路径
        self.get_result_path()

        # 中间结果
        # 平均指标列表
        if network_params.get('metrics'):
            self.metrics_list = network_params['metrics']
            self.train_best = best(self.metrics_list)
            self.valid_best = best(self.metrics_list)

        # 训练过程图片生成策略
        middle_results = []
        if network_params.get('middle_results'):
            middle_name = network_params['middle_results']['name']
            middle_count = int(network_params['middle_results']['count'])
            middle_results.append(middle_name)
            middle_results.append(middle_count)
        self.middle_results = middle_results

        # 损失函数
        if network_params.get('loss'):
            loss_fun_name = str(network_params['loss'])
            # 获取得到loss 的function
            # self.loss_fun = self.loss_fun_loader(loss_fun_name)

        # 需要进行注册
        self.optimizer_params = None
        if network_params.get('optimizer'):
            self.optimizer_name = network_params['optimizer']['name']
            if network_params.get('optimizer').get('params'):
                self.optimizer_params = network_params['optimizer']['params']

        self.scheduler_params = None
        if network_params.get('scheduler'):
            self.scheduler_name = network_params['scheduler']['name']
            if network_params.get('scheduler').get('params'):
                self.scheduler_params = network_params['scheduler']['params']

        label = str(params['label'])
        # label 中相关数据处理获取
        self.label_deal(label)
        self.num_classes = len(self.class_name_list)  # 类别数
        self.class_name = ",".join(self.class_name_list)

        # 训练相关参数
        self.batch_size = int(params['batch_size'])
        self.epochs = int(params['epochs'])
        # 学习率
        self.learning_rate = float(params['learning_rate'])
        # 是否提前停止
        self.auto_termination = int(params['auto_termination'])

        # node数量，大于1则使用ddp分布式训练
        # self.node_num = int(params['node_num'])
        self.node_num = 1

        # 初始化分布式进程组
        if dist_utils.should_distribute(self.node_num):
            backend = "nccl"
            print(
                "Initializes distributed backend={}, local_rank={}, global_rank={}, node_num={}, world_size={}".format(
                    backend, self.local_rank, dist_utils.CURRENT_RANK, self.node_num, dist_utils.WORLD_SIZE))
            dist_utils.init_process_group(self.local_rank, backend=backend)

        # 初始化dataset
        if self.network_type==1 or self.network_type==3:
            # 语义分割与变化检测
            self.dataset_loader = load_dataset(dataset_id=dataset_id, network_type=self.network_type,
                                               root_path=self.root_path,
                                               batch_size=self.batch_size, node_num=self.node_num,
                                               invert_palette=self.rgb_trianval_mapping,
                                               train_value_palette=self.actval_trainval_mapping,
                                               trans_pipelines=trans_pipelines)
            self.train_loader, self.valid_loader = self.dataset_loader.train_loader, self.dataset_loader.valid_loader
        else:
            # 目标识别
            self.dataset_loader = load_dataset(dataset_id=dataset_id, network_type=self.network_type,
                                               root_path=self.root_path,
                                               batch_size=self.batch_size, node_num=self.node_num,
                                               class_name_list=self.class_name_list,
                                               image_size=(self.load_size[0], self.load_size[1]))
            self.train_loader, self.valid_loader = self.dataset_loader.train_loader, self.dataset_loader.valid_loader
            self.anchors = self.dataset_loader.save_pre_anchors(self.result_path)

        self.dataset_bands = self.dataset_loader.img_band()
        # self.dataset_bands = 3

        # gpu
        self.device_ids = []
        gpu_num = int(params['gpu_num'])
        for i in range(0, gpu_num):
            self.device_ids.append(i)

        # 初始化日志
        self.init_log = self.traincfg_log_init()

    # 定义输出相关路径
    def get_result_path(self):
        # 输出路径
        if not os.path.exists(self.result_path + 'picture/'):
            os.makedirs(self.result_path + 'picture/')

        # 日志保存路径名称
        self.log_save_path = self.result_path + 'trainlog.json'
        # 图片保存
        self.picture_path = self.result_path + 'picture/'
        # 权重文件保存
        self.weight_path = self.result_path + self.weight_name

        return self.log_save_path, self.picture_path, self.weight_path

    # 数据加载
    def dataset_train_valid_loader(self):
        return self.train_loader, self.valid_loader

    # ================== 内置模型初始化 start ==================================
    def model_loader_build_in(self, model_dir=None, s3_path=None):
        network_name = self.model_name
        network_backbone = self.model_backbone
        num_classes = self.num_classes
        in_channal = self.dataset_bands
        print(self.__dict__)
        if 'anchors' in self.__dict__:
            anchors = len(self.anchors[0])
        else:
            anchors = None
        if not s3_path:
            s3_path = self.resume_path
        if s3_path and not model_dir:
            model_dir = os.path.join(self.root_path, s3_path.split('/')[-1])

        kwargs = {
            "network_name":network_name,
            "network_backbone":network_backbone,
            "num_classes":num_classes,
            "in_channal":in_channal,
            "num_anchors":anchors,
            "s3_path":s3_path,
            "model_dir":model_dir
        }
        model = builder_model(network_name, network_backbone,**kwargs)
        # 加载到gpu
        net = model_gpu_loader(model, self.device_ids, self.node_num, self.local_rank)
        return net

    # 初始化损失函数
    # def loss_fun_loader(self):
    #     if self.loss_fun_name == "hybrid_loss":
    #         return loss_hybrid
    #     elif self.loss_fun_name == "yolo_loss":
    #         return epoch_loss_train
    #     return None

    # 初始化优化器
    def optimizer_build_in(self,net=None):
        # 内置的 优化器
        if not net:
            print('net params is not none....')
        optimizer_name = self.optimizer_name
        lr = self.learning_rate
        if self.optimizer_params:
            optimizer_params = self.optimizer_params

        if not lr and not optimizer_name and optimizer_name not in Registry.__dict__.keys():
            print('not find {} in optimizer build in ...'.format(optimizer_name))
            return None
        optimizer_fun = {"type": optimizer_name,
                         "params": {"model": net, "lr": lr}}
        if optimizer_params:
            optimizer_fun["params"].update(optimizer_params)

        optimizer = registry_fun_init(optimizer_fun)
        return optimizer

    # 初始化学习率优化
    def lr_scheduler_build_in(self, optimizer, lr_scheduler_name=None):
        # 内置的 学习率策略 optimizer,milestones, gamma
        if not optimizer:
            print('optimizer params is not none....')
        if not lr_scheduler_name:
            lr_scheduler_name = self.scheduler_name
        if self.scheduler_params:
            scheduler_params = self.scheduler_params

        if not lr_scheduler_name and lr_scheduler_name not in Registry.__dict__.keys():
            print('not find {} in lr_scheduler build in ...'.format(lr_scheduler_name))
            return None
        lr_scheduler_fun = {"type": lr_scheduler_name,
                            "params": {"optimizer": optimizer}}
        if scheduler_params:
            lr_scheduler_fun["params"].update(scheduler_params)

        lr_scheduler = registry_fun_init(lr_scheduler_fun)
        return lr_scheduler

    # 评价指标初始化
    def metrics_build_in(self, num_classes=None):
        if not num_classes:
            num_classes = self.num_classes
        return Metrics_multi(num_classes)

    # 初始化日志log信息
    def traincfg_log_init(self, description_log_dict=None):
        metrics_dict_mapping = {"precision": "精确度", "recall": "召回率", "score": "F1分数", "mAP": "mAP", "loss": "损失值"}
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        if not description_log_dict:
            description_log_dict = {}
            for i, name in enumerate(self.metrics_list):
                if name in metrics_dict_mapping.keys():
                    description_log_dict[name] = metrics_dict_mapping[name]
        print(description_log_dict)

        log_init = {'training_id': self.training_id, "create_time": start_time,
                    "description": description_log_dict, "epochs": [], 'best': {},
                    "end_time": ""}
        return log_init

    # 数据label相关数据处理及获取
    def label_deal(self, dataset_lables):
        # 获取label 中的参数
        self.rgb_trianval_mapping = {}  # (r,g,b)对应训练的value
        self.trainval_rgb_mapping = {}  # 训练的value 对应rgb(r,g,b)
        self.actval_trainval_mapping = {}  # 真实value转换为训练value
        self.class_name_list = []  # 类别名称列表

        # 以下参数不包括背景中的trainval值
        trainval_title_mapping = {}
        trainval_class_mapping = {}
        class_title_mapping = {}
        backgroud_value = None

        labels = eval(dataset_lables)
        for i, val in enumerate(labels):
            for key in val.keys():
                if key == "class_color":
                    color_ = val[key]
                    rgb_ = "rgb(" + color_ + ")"
                    rgb = tuple(list(map(int, color_.split(','))))
                elif key == "class_name":
                    cls_name = val[key]
                elif key == "class_value":
                    value = int(val[key])
                    trainValue = int(i)
                elif key == "class_title":
                    cls_title = val[key]
                else:
                    continue

            if rgb and value >= 0:
                self.rgb_trianval_mapping[rgb] = trainValue
                self.trainval_rgb_mapping[trainValue] = rgb
                self.actval_trainval_mapping[value] = trainValue
                self.class_name_list.append(cls_name)

    # 保存评价指标等日志信息
    def save_trainlog_json_epoch(self, epoch, epochs, epoch_loss, len_loader, epoch_metrics,
                                 middle_results_dict=None, act_label=None,
                                 log_train=True, log_init=None):
        if not log_init:
            log_init = self.init_log

        epoch_loss /= len_loader

        # 20211125：分布式需要汇总不同GPU上的epoch_metrics到rank0进程，形成汇总后的epoch_metrics
        if dist_utils.should_distribute(self.node_num):
            # TODO：区分语义分割变化检测和目标检测：
            # 混淆矩阵每类的tp、tn、fp、fn分别汇总；为保证tensor维度统一，epoch_loss扩展为长度为num_class的list
            metrics_reduced = dist_utils.reduce_data([epoch_metrics.tp, epoch_metrics.tn, epoch_metrics.fp,
                                                      epoch_metrics.fn, [epoch_loss] * self.num_classes], 0)
            # 非rank0进程不进行后续的指标计算及中间图片保存
            if dist_utils.CURRENT_RANK != 0:
                return log_init
            # rank0进程汇总指标，Tensor转回list
            epoch_metrics.tp = metrics_reduced[0].cpu().numpy().tolist()
            epoch_metrics.tn = metrics_reduced[1].cpu().numpy().tolist()
            epoch_metrics.fp = metrics_reduced[2].cpu().numpy().tolist()
            epoch_metrics.fn = metrics_reduced[3].cpu().numpy().tolist()
            # 当前进程各batch的平均loss求和之后再平均，然后不同进程下的loss再次平均
            epoch_loss = float(metrics_reduced[4][0] / dist_utils.WORLD_SIZE)

        # 验证集保存图片
        # 20211125：增加逻辑，rank0进程保存中间图片
        if not log_train and len(middle_results_dict) > 0:
            save_picture(epoch, middle_results_dict, self.network_type, self.picture_path,
                         self.trainval_rgb_mapping, self.class_name_list, self.input_shape)

        metrics_list = self.metrics_list
        print('metrics_list------------- ')
        print(metrics_list)
        print(epoch_loss)
        print(len_loader)
        # if 'loss' in metrics_list:
        #     epoch_loss /= len_loader

        # 获取相应的评价指标
        epoch_train_metrics_dict_list = metrics_list_bulid_in(epoch_metrics, metrics_list,self.network_type,
                                                              actu_labels=act_label)

        best_ = None
        if True:
            self.train_best.add(epoch_loss, epoch_train_metrics_dict_list)
            best_ = self.train_best.show()
            print('loss: ', self.train_best['loss'])
            print('train metrics : ', self.train_best.show())
        else:
            self.valid_best.add(epoch_loss, epoch_train_metrics_dict_list)
            best_ = self.valid_best.show()
            print('loss: ', self.valid_best['loss'])
            print('valid metrics :', self.valid_best.show())
        # print(epoch_train_metrics_dict_list)
        print('loss: ')
        print(epoch_loss, '\n')

        # 日志保存
        # 目标识别中可能存在未识别的类别
        if act_label is not None:
            class_name_list = np.unique(act_label).astype("int32")
        else:
            class_name_list = self.class_name_list

        log_init = trainlog_json_epoch(best_, log_init, epoch, epochs, epoch_loss, epoch_train_metrics_dict_list,
                                       class_name_list, self.log_save_path, log_train=log_train)
        return log_init

# 数据大小进行 32倍处理
def input_size_deal(load_size,input_size_count=32):

    load_size[0] = round(float(load_size[0]) / input_size_count) * input_size_count
    load_size[1] = round(float(load_size[1]) / input_size_count) * input_size_count
    if load_size[1] > load_size[0]:
        load_size[1] = load_size[0]
    else:
        load_size[0] = load_size[1]
    return load_size

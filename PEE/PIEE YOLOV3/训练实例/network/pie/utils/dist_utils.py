import os
import datetime
import torch
from torch import distributed as dist

# 所有机器的GPU总数
WORLD_SIZE = int(os.environ.get('WORLD_SIZE', 1))
# 当前进程所使用GPU在所有GPU中的rank
CURRENT_RANK = int(os.environ.get('RANK', 0))
print("WORLD_SIZE: {}, CURRENT_RANK: {}".format(WORLD_SIZE, CURRENT_RANK))


# TODO: 20211201，考虑CPU分布式训练
def should_distribute(node_num):
    """
    根据node_num判断是否使用DDP分布式训练
    :param node_num: 节点个数
    :return: bool
    """
    return dist.is_available() and node_num > 1


def is_distributed():
    return dist.is_available() and dist.is_initialized()


def init_process_group(local_rank, backend="nccl", timeout=datetime.timedelta(0, 180)):
    """
    初始化pytorch进程组
    :param local_rank: 当前进程在当前node里所有GPU中的rank
    :param backend: 分布式训练使用的通信后端，GPU使用nccl，CPU使用gloo，默认nccl
    :param timeout: 不同进程间建立通信的超时时长，超时后程序终止
    :return:
    """
    dist.init_process_group(backend=backend, timeout=timeout)
    # 设置当前进程使用当前node的第几个GPU
    torch.cuda.set_device(local_rank)


def reduce_data(src_data: list, dest_rank):
    """
    分维度汇总不同rank进程的src_data中的数值到dest_rank进程，dest_rank进程的src_data原地更新
    :param src_data: 各rank下待汇总的list，list中元素的数据类型需为number
    :param dest_rank: 汇总的目标rank
    :return: 汇总后的tensor
    """
    data_reduced = torch.tensor(src_data, requires_grad=False, device='cuda')
    # print("before metrics_reduced: {}".format(metrics_reduced))
    dist.reduce(data_reduced, dest_rank, op=dist.ReduceOp.SUM)
    # print("after metrics_reduced: {}".format(metrics_reduced))
    return data_reduced

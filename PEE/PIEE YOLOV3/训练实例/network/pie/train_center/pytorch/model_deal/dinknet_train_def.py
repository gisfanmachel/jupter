

# 评价指标
import torch
import numpy as np
from pie.train_center.common.loss_hybrid import hybrid_loss

# 自定义损失函数
def loss_def(outputs, targets, **kwargs):

    loss = hybrid_loss(outputs, targets)

    return loss


def data_pocessing(outputs,**kwargs):
    outputs = np.argmax(outputs.data.cpu().numpy(), axis=1)
    return outputs


def metrics_def(outputs, targets,**kwargs):
    if kwargs.get('metrics_class'):
        metrics_class = kwargs.get('metrics_class')
    else:
        print('not find metrics...')
        exit(1)
    train_target = targets.data.cpu().numpy()

    for actual, output in zip(train_target, outputs):
        metrics_class.add(actual, output)

    return metrics_class

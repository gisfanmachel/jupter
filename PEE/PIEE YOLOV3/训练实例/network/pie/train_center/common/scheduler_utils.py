
# 学习率策略
from torch import optim

from pie.utils.registry import Registry


@Registry.divfun
def LambdaLR(optimizer,lr_lambda=None):
    return optim.lr_scheduler.LambdaLR(optimizer, lr_lambda=lr_lambda)

@Registry.divfun
def StepLR(optimizer,step_size=1, gamma=0.8):
    return optim.lr_scheduler.StepLR(optimizer, step_size, gamma)

@Registry.divfun
def MultiStepLR(optimizer,milestones=[10,20,50], gamma=0.8):
    return optim.lr_scheduler.MultiStepLR(optimizer, milestones, gamma)

@Registry.divfun
def CosineAnnealingLR(optimizer, T_max=5, eta_min=1e-7):
    return optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max, eta_min)

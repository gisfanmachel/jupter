
# 优化器
from torch import optim

from pie.utils.registry import Registry


@Registry.divfun
def SGD(model,lr=1e-2,momentum=0.9, weight_decay=5e-4):
    return optim.SGD(model.parameters(), lr, momentum, weight_decay)


@Registry.divfun
def Adam(model,lr=1e-3,betas=(0.9, 0.999), eps=1e-8,weight_decay=0):
    return optim.Adam(model.parameters(), lr, betas, eps,weight_decay)

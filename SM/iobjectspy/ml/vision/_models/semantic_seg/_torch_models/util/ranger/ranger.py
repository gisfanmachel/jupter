# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_torch_models\util\ranger\ranger.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 7025 bytes
import math, torch
from torch.optim.optimizer import Optimizer, required
import itertools as it

class Ranger(Optimizer):

    def __init__(self, params, lr=0.001, alpha=0.5, k=6, N_sma_threshhold=5, betas=(0.95, 0.999), eps=1e-05, weight_decay=0):
        if not 0.0 <= alpha <= 1.0:
            raise ValueError(f"Invalid slow update rate: {alpha}")
        elif not 1 <= k:
            raise ValueError(f"Invalid lookahead steps: {k}")
        if not lr > 0:
            raise ValueError(f"Invalid Learning Rate: {lr}")
        assert eps > 0, f"Invalid eps: {eps}"
        defaults = dict(lr=lr, alpha=alpha, k=k, step_counter=0, betas=betas, N_sma_threshhold=N_sma_threshhold, eps=eps, weight_decay=weight_decay)
        super().__init__(params, defaults)
        self.N_sma_threshhold = N_sma_threshhold
        self.alpha = alpha
        self.k = k
        self.radam_buffer = [[None, None, None] for ind in range(10)]

    def __setstate__(self, state):
        print("set state called")
        super(Ranger, self).__setstate__(state)

    def step(self, closure=None):
        loss = None
        for group in self.param_groups:
            for p in group["params"]:
                if p.grad is None:
                    continue
                else:
                    grad = p.grad.data.float()
                    if grad.is_sparse:
                        raise RuntimeError("Ranger optimizer does not support sparse gradients")
                    else:
                        p_data_fp32 = p.data.float()
                        state = self.state[p]
                        if len(state) == 0:
                            state["step"] = 0
                            state["exp_avg"] = torch.zeros_like(p_data_fp32)
                            state["exp_avg_sq"] = torch.zeros_like(p_data_fp32)
                            state["slow_buffer"] = torch.empty_like(p.data)
                            state["slow_buffer"].copy_(p.data)
                        else:
                            state["exp_avg"] = state["exp_avg"].type_as(p_data_fp32)
                            state["exp_avg_sq"] = state["exp_avg_sq"].type_as(p_data_fp32)
                        exp_avg, exp_avg_sq = state["exp_avg"], state["exp_avg_sq"]
                        beta1, beta2 = group["betas"]
                        exp_avg_sq.mul_(beta2).addcmul_(1 - beta2, grad, grad)
                        exp_avg.mul_(beta1).add_(1 - beta1, grad)
                        state["step"] += 1
                        buffered = self.radam_buffer[int(state["step"] % 10)]
                        if state["step"] == buffered[0]:
                            N_sma, step_size = buffered[1], buffered[2]
                        else:
                            buffered[0] = state["step"]
                            beta2_t = beta2 ** state["step"]
                            N_sma_max = 2 / (1 - beta2) - 1
                            N_sma = N_sma_max - 2 * state["step"] * beta2_t / (1 - beta2_t)
                            buffered[1] = N_sma
                            if N_sma > self.N_sma_threshhold:
                                step_size = math.sqrt((1 - beta2_t) * (N_sma - 4) / (N_sma_max - 4) * (N_sma - 2) / N_sma * N_sma_max / (N_sma_max - 2)) / (1 - beta1 ** state["step"])
                            else:
                                step_size = 1.0 / (1 - beta1 ** state["step"])
                        buffered[2] = step_size
                    if group["weight_decay"] != 0:
                        p_data_fp32.add_(-group["weight_decay"] * group["lr"], p_data_fp32)
                    if N_sma > self.N_sma_threshhold:
                        denom = exp_avg_sq.sqrt().add_(group["eps"])
                        p_data_fp32.addcdiv_(-step_size * group["lr"], exp_avg, denom)
                    else:
                        p_data_fp32.add_(-step_size * group["lr"], exp_avg)
                p.data.copy_(p_data_fp32)
                if state["step"] % group["k"] == 0:
                    slow_p = state["slow_buffer"]
                    slow_p.add_(self.alpha, p.data - slow_p)
                    p.data.copy_(slow_p)

        return loss

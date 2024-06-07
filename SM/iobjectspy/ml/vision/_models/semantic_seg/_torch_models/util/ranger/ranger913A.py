# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_torch_models\util\ranger\ranger913A.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 8360 bytes
import math, torch
from torch.optim.optimizer import Optimizer, required
import itertools as it

class RangerVA(Optimizer):

    def __init__(self, params, lr=0.001, alpha=0.5, k=6, n_sma_threshhold=5, betas=(0.95, 0.999), eps=1e-05, weight_decay=0, amsgrad=True, transformer='softplus', smooth=50, grad_transformer='square'):
        if not 0.0 <= alpha <= 1.0:
            raise ValueError(f"Invalid slow update rate: {alpha}")
        elif not 1 <= k:
            raise ValueError(f"Invalid lookahead steps: {k}")
        if not lr > 0:
            raise ValueError(f"Invalid Learning Rate: {lr}")
        assert eps > 0, f"Invalid eps: {eps}"
        defaults = dict(lr=lr, alpha=alpha, k=k, step_counter=0, betas=betas, n_sma_threshhold=n_sma_threshhold,
          eps=eps,
          weight_decay=weight_decay,
          smooth=smooth,
          transformer=transformer,
          grad_transformer=grad_transformer,
          amsgrad=amsgrad)
        super().__init__(params, defaults)
        self.n_sma_threshhold = n_sma_threshhold
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
                    amsgrad = group["amsgrad"]
                    smooth = group["smooth"]
                    grad_transformer = group["grad_transformer"]
                    p_data_fp32 = p.data.float()
                    state = self.state[p]
                    if len(state) == 0:
                        state["step"] = 0
                        state["exp_avg"] = torch.zeros_like(p_data_fp32)
                        state["exp_avg_sq"] = torch.zeros_like(p_data_fp32)
                        if amsgrad:
                            state["max_exp_avg_sq"] = torch.zeros_like(p.data)
                        state["slow_buffer"] = torch.empty_like(p.data)
                        state["slow_buffer"].copy_(p.data)
                    else:
                        state["exp_avg"] = state["exp_avg"].type_as(p_data_fp32)
                    state["exp_avg_sq"] = state["exp_avg_sq"].type_as(p_data_fp32)
                exp_avg, exp_avg_sq = state["exp_avg"], state["exp_avg_sq"]
                beta1, beta2 = group["betas"]
                if amsgrad:
                    max_exp_avg_sq = state["max_exp_avg_sq"]
                exp_avg_sq.mul_(beta2).addcmul_(1 - beta2, grad, grad)
                exp_avg.mul_(beta1).add_(1 - beta1, grad)
                if grad_transformer == "square":
                    grad_tmp = grad ** 2
                else:
                    if grad_transformer == "abs":
                        grad_tmp = grad.abs()
                    else:
                        exp_avg_sq.mul_(beta2).add_((1 - beta2) * grad_tmp)
                        if amsgrad:
                            torch.max(max_exp_avg_sq, exp_avg_sq, out=max_exp_avg_sq)
                            denomc = max_exp_avg_sq.clone()
                        else:
                            denomc = exp_avg_sq.clone()
                        if grad_transformer == "square":
                            denomc.sqrt_()
                        state["step"] += 1
                        if group["weight_decay"] != 0:
                            p_data_fp32.add_(-group["weight_decay"] * group["lr"], p_data_fp32)
                        bias_correction1 = 1 - beta1 ** state["step"]
                        bias_correction2 = 1 - beta2 ** state["step"]
                        step_size = group["lr"] * math.sqrt(bias_correction2) / bias_correction1
                        if group["transformer"] == "softplus":
                            sp = torch.nn.Softplus(smooth)
                            denomf = sp(denomc)
                            p_data_fp32.addcdiv_(-step_size, exp_avg, denomf)
                        else:
                            denom = exp_avg_sq.sqrt().add_(group["eps"])
                            p_data_fp32.addcdiv_(-step_size * group["lr"], exp_avg, denom)
                    p.data.copy_(p_data_fp32)
                if state["step"] % group["k"] == 0:
                    slow_p = state["slow_buffer"]
                    slow_p.add_(self.alpha, p.data - slow_p)
                    p.data.copy_(slow_p)

        return loss

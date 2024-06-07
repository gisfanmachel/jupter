# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_torch_models\util\ranger\rangerqh.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 6752 bytes
import torch
from torch.optim.optimizer import Optimizer

class RangerQH(Optimizer):
    __doc__ = "Implements the QHAdam optimization algorithm `(Ma and Yarats, 2019)`_.\n    Along with Hinton/Zhang Lookahead.\n    Args:\n        params (iterable):\n            iterable of parameters to optimize or dicts defining parameter\n            groups\n        lr (float, optional): learning rate (:math:`\\alpha` from the paper)\n            (default: 1e-3)\n        betas (Tuple[float, float], optional): coefficients used for computing\n            running averages of the gradient and its square\n            (default: (0.9, 0.999))\n        nus (Tuple[float, float], optional): immediate discount factors used to\n            estimate the gradient and its square\n            (default: (1.0, 1.0))\n        eps (float, optional): term added to the denominator to improve\n            numerical stability\n            (default: 1e-8)\n        weight_decay (float, optional): weight decay (default: 0.0)\n        decouple_weight_decay (bool, optional): whether to decouple the weight\n            decay from the gradient-based optimization step\n            (default: False)\n    Example:\n        >>> optimizer = qhoptim.pyt.QHAdam(\n        ...     model.parameters(),\n        ...     lr=3e-4, nus=(0.8, 1.0), betas=(0.99, 0.999))\n        >>> optimizer.zero_grad()\n        >>> loss_fn(model(input), target).backward()\n        >>> optimizer.step()\n    .. _`(Ma and Yarats, 2019)`: https://arxiv.org/abs/1810.06801\n    "

    def __init__(self, params, lr=0.001, betas=(0.9, 0.999), nus=(0.7, 1.0), weight_decay=0.0, k=6, alpha=0.5, decouple_weight_decay=False, eps=1e-08):
        if not 0.0 <= lr:
            raise ValueError("Invalid learning rate: {}".format(lr))
        if not 0.0 <= eps:
            raise ValueError("Invalid epsilon value: {}".format(eps))
        if not 0.0 <= betas[0] < 1.0:
            raise ValueError("Invalid beta parameter at index 0: {}".format(betas[0]))
        if not 0.0 <= betas[1] < 1.0:
            raise ValueError("Invalid beta parameter at index 1: {}".format(betas[1]))
        if weight_decay < 0.0:
            raise ValueError("Invalid weight_decay value: {}".format(weight_decay))
        defaults = {
         'lr': lr, 
         'betas': betas, 
         'nus': nus, 
         'weight_decay': weight_decay, 
         'decouple_weight_decay': decouple_weight_decay, 
         'eps': eps}
        super().__init__(params, defaults)
        self.alpha = alpha
        self.k = k

    def step(self, closure=None):
        """Performs a single optimization step.
        Args:
            closure (callable, optional):
                A closure that reevaluates the model and returns the loss.
        """
        loss = None
        if closure is not None:
            loss = closure()
        for group in self.param_groups:
            lr = group["lr"]
            beta1, beta2 = group["betas"]
            nu1, nu2 = group["nus"]
            weight_decay = group["weight_decay"]
            decouple_weight_decay = group["decouple_weight_decay"]
            eps = group["eps"]
            for p in group["params"]:
                if p.grad is None:
                    continue
                else:
                    d_p = p.grad.data
                    if d_p.is_sparse:
                        raise RuntimeError("QHAdam does not support sparse gradients")
                    if weight_decay != 0:
                        if decouple_weight_decay:
                            p.data.mul_(1 - lr * weight_decay)
                        else:
                            d_p.add_(weight_decay, p.data)
                d_p_sq = d_p.mul(d_p)
                param_state = self.state[p]
                if len(param_state) == 0:
                    param_state["beta1_weight"] = 0.0
                    param_state["beta2_weight"] = 0.0
                    param_state["step"] = 0
                    param_state["exp_avg"] = torch.zeros_like(p.data)
                    param_state["exp_avg_sq"] = torch.zeros_like(p.data)
                    param_state["slow_buffer"] = torch.empty_like(p.data)
                    param_state["slow_buffer"].copy_(p.data)
                param_state["step"] += 1
                param_state["beta1_weight"] = 1.0 + beta1 * param_state["beta1_weight"]
                param_state["beta2_weight"] = 1.0 + beta2 * param_state["beta2_weight"]
                beta1_weight = param_state["beta1_weight"]
                beta2_weight = param_state["beta2_weight"]
                exp_avg = param_state["exp_avg"]
                exp_avg_sq = param_state["exp_avg_sq"]
                beta1_adj = 1.0 - 1.0 / beta1_weight
                beta2_adj = 1.0 - 1.0 / beta2_weight
                exp_avg.mul_(beta1_adj).add_(1.0 - beta1_adj, d_p)
                exp_avg_sq.mul_(beta2_adj).add_(1.0 - beta2_adj, d_p_sq)
                avg_grad = exp_avg.mul(nu1)
                if nu1 != 1.0:
                    avg_grad.add_(1.0 - nu1, d_p)
                avg_grad_rms = exp_avg_sq.mul(nu2)
                if nu2 != 1.0:
                    avg_grad_rms.add_(1.0 - nu2, d_p_sq)
                avg_grad_rms.sqrt_()
                if eps != 0.0:
                    avg_grad_rms.add_(eps)
                p.data.addcdiv_(-lr, avg_grad, avg_grad_rms)
                if param_state["step"] % self.k == 0:
                    slow_p = param_state["slow_buffer"]
                    slow_p.add_(self.alpha, p.data - slow_p)
                    p.data.copy_(slow_p)

        return loss

    @classmethod
    def _params_to_dict(cls, params):
        return {'lr':params.alpha,  'nus':(params.nu1, params.nu2),  'betas':(params.beta1, params.beta2)}

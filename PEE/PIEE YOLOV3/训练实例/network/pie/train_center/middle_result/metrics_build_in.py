# 训练过程内置的方法
import numpy as np

# 获取评价指标对应的值metrics (内置)
from pie.train_center.common.metrics_obj import ap_per_class

metrics_name_key_piexl = ['precision','recall','f1','oa','miou']
metrics_name_key_obj = ['precision','recall','ap','f1']

def metrics_list_bulid_in(metrics, metrics_name_list, network_type,actu_labels=None):
    '''
        评价指标
    :param metrics:
    :param name: 评价指标名称 ["precision","recall","f1","oa","miou"]
    :return: {“precision”: [mean-precision_array,class_precision_array],“recall”: [mean-recall_array,class_recall_array]}
    '''
    epoch_metrics_dict_list = []
    if network_type == 1 or network_type == 3:     # 像素级别
        for i, name in enumerate(metrics_name_list):
            epoch_metrics = None
            epoch_metrics_dict = {}
            if name == "precision":
                epoch_metrics = metrics.get_precision()
            elif name == "recall":
                epoch_metrics = metrics.get_recall()
            elif name == "f1":
                epoch_metrics = metrics.get_f_score()
            elif name == "oa":
                epoch_metrics = metrics.get_oa()
            elif name == "miou":
                epoch_metrics = metrics.get_miou()
            elif name == "loss":
                epoch_metrics = None
            else:
                print('not find metrics name ...')
            if epoch_metrics:
                epoch_metrics_dict[name + '_part'] = epoch_metrics
                epoch_metrics_mean = sum(epoch_metrics) / len(epoch_metrics)
                epoch_metrics_dict[name + '_all'] = epoch_metrics_mean
                epoch_metrics_dict_list.append(epoch_metrics_dict)
    else:  # 目标识别
        if len(metrics) != 0:
            # 获取得到 epoch所有的真实labels
            true_positives, pred_scores, pred_labels = [np.concatenate(x, 0) for x in list(zip(*metrics))]

            precision, recall, AP, f1, ap_class = ap_per_class(true_positives, pred_scores, pred_labels, actu_labels)

            # 组合为需显示的
            metrics_dict = {}
            if 'precision' in metrics_name_list:
                metrics_dict['precision'] = precision.tolist()
            if 'recall' in metrics_name_list:
                metrics_dict['recall'] = recall.tolist()
            if 'AP' in metrics_name_list:
                metrics_dict['AP'] = AP.tolist()
            if 'f1' in metrics_name_list:
                metrics_dict['score'] = f1.tolist()
            epoch_metrics_dict_list = create_metrics_list_for_log(metrics_dict)
    return epoch_metrics_dict_list


# 根据对应评价名称及值 组成相应的类型
def create_metrics_list_for_log(metrics_value_dict,is_mean=True):
    epoch_metrics_dict_list = []
    for name, metrics_arr in metrics_value_dict.items():
        epoch_metrics_dict = {}

        if is_mean or len(metrics_arr) == 1:
            epoch_metrics_mean = sum(metrics_arr) / len(metrics_arr)
            epoch_metrics_dict[name + '_all'] = epoch_metrics_mean   # 1个 或者 mean
        elif len(metrics_arr) > 1:
            epoch_metrics_dict[name + '_part'] = metrics_arr  # 多个

        epoch_metrics_dict_list.append(epoch_metrics_dict)

    return epoch_metrics_dict_list
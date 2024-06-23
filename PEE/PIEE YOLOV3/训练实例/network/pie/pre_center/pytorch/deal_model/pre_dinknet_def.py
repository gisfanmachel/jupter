'''
    dinknet 网络结构对应的 预测 方法
    wangtuo 20211207
'''


import json
import os

import torch
import numpy as np

# 设置参数
# 手动填写（了解相关参数意义）
from pie.get_platform_arguments import parse_platform_arguments


'''
    导入 读取参数方法，获取input()中输入参数，当代码中存在traincfg.json时，会进行读取
:return:
'''
init = parse_platform_arguments()

platform_arguments = {
    'estimate_id': init.estimate_id,  # 任务ID
    'image_path': init.image_path,  # 训练图片路径
    'device_ids': init.device_ids,  # gpu device id 数
    'result_path': init.result_path, # 输出结果文件 output
    'network_type': 1,  # 预测的类别 （必填）
    'load_size': init.load_size,  # 图片加载大小
    'value_name_map': init.trainval_class_mapping,  # 训练value对应英文名称
    'value_title_map': init.trainval_title_mapping,  # 训练value对应类别中文名称
    'name_title_map': init.class_title_mapping,  # 类别英文名称 对应类别中文名称
    'value_color': init.trainval_rgb_mapping,  # 训练value对应 rgb()颜色
    'background_value': init.background_value,  # 背景对应的训练value
    'class_name_list': init.class_name_list,  # 除背景外的类别列表
    'nms': 0.3,  # 目标识别
}

def load_pre_argment():
    return platform_arguments

# 加载权重文件
def load_model():
    '''
        加载模型
    Returns:

    '''

    basedir = os.path.abspath(os.path.dirname(__file__))
    weight_root = '/tmp/pycharm_project_364/weight/'
    weights_file = weight_root + 'DinkNet34.th'


    # 内置的网络结构
    model = init.model_loader_build_in(model_dir=weights_file)
    # 加载模型
    # cuda = torch.cuda.is_available()

    # if cuda:
    #     model = model.cuda()
    # device = torch.device('cuda' if cuda else 'cpu')
    # model.load_state_dict(torch.load(weights_file, map_location=device))

    return model

from torch.autograd import Variable as Variable
def deal_data_img(image):
    '''
    获取得到（H,W,C）ndarray数组，进行处理，可以直接输入模型进行预测
    Args:
        img:

    Returns:

    '''
    img = np.array(image, np.float32).transpose(2,0,1)
    img = torch.from_numpy(img).unsqueeze(0)
    img = Variable(torch.Tensor(img).cuda())
    return img

def deal_pred_result(pred_image):
    '''
    获取得到模型生成的结果，进行操作，将其修改为（H,W）数组
    Args:
        pre_img:

    Returns:

    '''
    pred = np.argmax(pred_image[0].data.cpu().numpy(), axis=0)
    pred = pred.astype(np.uint8)
    return pred


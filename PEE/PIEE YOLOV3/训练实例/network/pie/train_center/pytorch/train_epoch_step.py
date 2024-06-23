import datetime
from inspect import isfunction

import torch
from torch.autograd import Variable
import numpy as np

from pie.train_center.common.metrics_obj import ap_per_class, metics_value_one
from pie.train_center.common.metrics_piexl import precision_recall_mean_image
from pie.train_center.middle_result.middle_file import middle_image_array
from pie.utils import dist_utils

def train_model_step(net, train_loader, network_type, optimizer, cuda,
                     loss_col, post_prcessing=None, metrics_col=None, **kwargs):
    train_loss = 0.
    train_labels = []
    train_metrics = []
    time4545 = datetime.datetime.now()

    # 数据集loader
    print('training...')
    net.train()

    for iteration, batch in enumerate(train_loader):
        time12 = datetime.datetime.now()

        # 判断类型
        images2 = None
        if len(batch) == 2:
            images, targets = batch[0], batch[1]
        elif len(batch) == 3:
            images, images2, targets = batch[0], batch[1], batch[2]

        if network_type == 2:
            for num_i in range(len(targets)):
                if targets[num_i] is None:
                    continue
                annotations = targets[num_i]
                train_labels += annotations[:, -1].tolist() if len(annotations) else []

        if network_type == 2:
            if cuda:
                images = Variable(torch.from_numpy(images).type(torch.FloatTensor)).cuda()
                targets = [Variable(torch.from_numpy(ann.astype(np.float32)).type(torch.FloatTensor)) for ann in
                           targets]
            else:
                images = Variable(torch.from_numpy(images).type(torch.FloatTensor))
                targets = [Variable(torch.from_numpy(ann.astype(np.float32)).type(torch.FloatTensor)) for ann in
                           targets]
        else:
            if cuda:
                images, targets = Variable(images.cuda()), Variable(targets.cuda())
                if images2 is not None:
                    images2 = Variable(images2.cuda())
            else:
                images, targets = Variable(images), Variable(targets)
                if images2 is not None:
                    images2 = Variable(images2)

        optimizer.zero_grad()
        if images2 is not None:
            outputs = net(images,images2)
        else:
            outputs = net(images)

        # loss
        if isfunction(loss_col):
            loss = loss_col(outputs, targets, **kwargs)
        else:
            print('loss_function is not None ...')
            exit(1)

        # 模型数据后处理
        if isfunction(post_prcessing):
            outputs = post_prcessing(outputs, **kwargs)

        # 评价指标
        if isfunction(metrics_col):
            if network_type == 2:
                train_metrics += metrics_col(outputs, targets, **kwargs)
            else:
                train_metrics = metrics_col(outputs, targets, **kwargs)

        loss.backward()
        optimizer.step()

        train_loss += loss.item()

        time246 = datetime.datetime.now()
        # print('one batch --- ' + str(time246 - time12))

    time2 = datetime.datetime.now()
    print('training--- ' + str(time2 - time4545))
    print("train_loss:" + str(train_loss))

    return net,optimizer,train_metrics, train_loss,train_labels


def test_model_step(net, test_loader,network_type, cuda,
                    middel_img_result,
                    loss_col,post_prcessing,metrics_col,**kwargs):

    valid_loss = 0.
    valid_labels = []
    valid_metrics = []

    net.eval()

    time1 = datetime.datetime.now()

    with torch.no_grad():
        for iteration, batch in enumerate(test_loader):

            time12 = datetime.datetime.now()

            images2_val = None
            if len(batch) == 2:
                images_val, targets_val = batch[0], batch[1]
            elif len(batch) == 3:
                images_val, images2_val, targets_val = batch[0], batch[1], batch[2]

            if network_type == 2:
                for num_i in range(len(targets_val)):
                    if targets_val[num_i] is None:
                        continue
                    annotations = targets_val[num_i]
                    valid_labels += annotations[:, -1].tolist() if len(annotations) else []

            if network_type == 2:
                if cuda:
                    images_val = Variable(torch.from_numpy(images_val).type(torch.FloatTensor)).cuda()
                    targets_val = [Variable(torch.from_numpy(ann.astype(np.float32)).type(torch.FloatTensor)) for ann in
                                   targets_val]
                else:
                    images_val = Variable(torch.from_numpy(images_val).type(torch.FloatTensor))
                    targets_val = [Variable(torch.from_numpy(ann.astype(np.float32)).type(torch.FloatTensor)) for ann in
                                   targets_val]
            else:
                if cuda:
                    images_val, targets_val = Variable(images_val.cuda()), Variable(targets_val.cuda())
                    if images2_val is not None:
                        images2_val = Variable(images2_val.cuda())
                else:
                    images_val, targets_val = Variable(images_val), Variable(targets_val)
                    if images2_val is not None:
                        images2_val = Variable(images2_val)

            if images2_val is not None:
                val_outputs = net(images_val,images2_val)
            else:
                val_outputs = net(images_val)

            if isfunction(loss_col):
                loss = loss_col(val_outputs, targets_val, **kwargs)
            else:
                print('ssssss loss')
                exit(1)

            # 解码data_post_processing,
            if isfunction(post_prcessing):
                val_outputs = post_prcessing(val_outputs, **kwargs)

            # 评价指标
            if isfunction(metrics_col):
                if network_type == 2:
                    valid_metrics += metrics_col(val_outputs, targets_val, **kwargs)
                else:
                    valid_metrics = metrics_col(val_outputs, targets_val, **kwargs)

            valid_loss += loss.item()
            # TODO：rank0进程保存中间图片
            if dist_utils.CURRENT_RANK == 0:
                if images2_val is not None:
                    images2_val = images2_val.cpu().numpy()

                # 记录中间涂图片信息
                middel_img_result = middele_image_array(
                    [images_val.cpu().numpy(), images2_val, targets_val, val_outputs],
                    network_type, middel_img_result, **kwargs)

            time42 = datetime.datetime.now()
            # print('test_model --- ' + str(time42 - time12))

        time4 = datetime.datetime.now()
        # print('test_model --- ' + str(time4 - time1))
        print("val_loss:" + str(valid_loss))

    return net,valid_metrics, valid_loss, middel_img_result,valid_labels


# 验证集中根据中间策略保存相应的图片数组
def middele_image_array(image_list,network_type,middle_results_list,**kwargs):
# def middele_image_array(image_list, network_type, middle_results_list, loss_dict, **kwargs):
    # 统计 batch中对应每张图片相应的评价指标，并进行记录

    middel_results_data = kwargs['middel_results_name']

    if kwargs.get('num_classes'):
        num_class = kwargs['num_classes']
    if kwargs.get('input_shape'):
        input_shape = kwargs['input_shape']

    middel_results_name, middle_results_count = middel_results_data[0],middel_results_data[1]

    images_batch = image_list[0]
    images2_batch = image_list[1]
    masks_batch = image_list[2]
    outputs_batch = image_list[3]

    if images2_batch is not None and network_type == 3:
        for img,img2, mask, pred in zip(images_batch,images2_batch, masks_batch, outputs_batch):

            if pred is None:
                continue

            mask = mask.cpu().numpy()
            mean_metric = precision_recall_mean_image(mask, pred, num_class, name=middel_results_name)

            # 根据策略保存对应的数组列表middle_metrics_list, middle_results_count,image_list, mean_metric
            middle_results_list = middle_image_array(middle_results_list, middle_results_count,
                                                                        [img,img2,mask,pred], mean_metric)
    else:
        for img, mask, pred in zip(images_batch, masks_batch, outputs_batch):

            if pred is None:
                continue

            if network_type == 1:  # 像素级别
                mask = mask.cpu().numpy()
                mean_metric = precision_recall_mean_image(mask, pred, num_class, name=middel_results_name)

            elif network_type == 2:     # 目标框
                mean_metric = metics_value_one(input_shape,[mask],[pred], name=middel_results_name,conf_thres=0.5,iou_threshold=0.5)
                pred = pred.cpu().numpy()

            # 根据策略保存对应的数组列表middle_metrics_list, middle_results_count,image_list, mean_metric
            middle_results_list = middle_image_array(middle_results_list, middle_results_count,
                                                                        [img,mask,pred], mean_metric)

            # 根据策略保存对应的数组列表loss_dict
            # loss_dict = middle_image_array(middle_results_list, middle_results_count,
            #                                                             [img,mask,pred], mean_metric)

    # return middle_results_list, loss_dict
    return middle_results_list
    # return middle_results_list, loss_dict


# 输出权重文件
def save_checkpoint(model, path):
    # 20211124，增加多机多卡情况下，由rank0进程保存模型的判断
    # TODO：需要验证单机多卡DataParallel情况下，是否会有冲突（DP采用单进程多线程方式，理论上单进程只会执行一次该函数，不会有冲突）
    if dist_utils.CURRENT_RANK == 0:
        torch.save(model.state_dict(), path)


# 训练提前停止
def auto_termination(model, epoch, train_epoch_loss, train_epoch_best_loss, lr, no_optim, outputSaveDir):
    if train_epoch_loss >= train_epoch_best_loss:
        no_optim += 1
        if no_optim < 2:
            save_checkpoint(model, outputSaveDir)
    else:
        no_optim = 0
        save_checkpoint(model, outputSaveDir)

    if no_optim > 6:
        print('early stop at %d epoch' % epoch)
        exit(0)
    if no_optim > 5:
        if lr < 5e-7:
            print('learning_rate too lower ... ')
            exit(0)

    return train_epoch_best_loss,no_optim


# 网络结构在gpu上进行加载
def model_gpu_loader(net, device_ids, node_num, local_rank):
    if torch.cuda.is_available() and len(device_ids) > 0:
        net = net.cuda()
    if node_num <= 1:
        # 单节点使用dp
        if torch.cuda.device_count() > 1 and len(device_ids) > 1:
            net = torch.nn.DataParallel(net, device_ids)
    else:
        # 多节点使用ddp
        net = torch.nn.parallel.DistributedDataParallel(net, device_ids=[local_rank],
                                                        output_device=local_rank)
    return net

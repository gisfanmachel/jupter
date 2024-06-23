import datetime
from inspect import isfunction

import torch
from torch.autograd import Variable
import numpy as np

from pie.train_center.common.metrics_obj import get_batch_statistics, ap_per_class
from pie.train_center.common.metrics_piexl import precision_recall_mean_image
from pie.train_center.middle_result.middle_file import middle_image_array
from pie.train_center.pytorch.utils_obj import non_max_suppression


def main(epochs,net,optimizer,lr_scheduler,input_shape,num_classes,yolo_losses,yolo_decodes,train_loader,valid_loader,cuda,auto_termination):
    train_epoch_best_loss = 1000000.
    no_optim = 0.

    for epoch in range(0,epochs):
        time1 = datetime.datetime.now()
        print('Epoch:' + str(epoch + 1) + '/' + str(epochs))

        train_loss = 0
        valid_loss = 0

        train_labels = []
        valid_labels = []

        train_metrics = []
        valid_metrics = []

        net = net.train()
        print('training...')

        for iteration,batch in enumerate(train_loader):
            time11 = datetime.datetime.now()
            images,targets = batch[0],batch[1]

            for num_i in range(len(targets)):
                if targets[num_i] is None:
                    continue
                annotations = targets[num_i]
                train_labels += annotations[:,-1].tolist() if len(annotations) else []

            with torch.no_grad():
                if cuda:
                    images = Variable(torch.from_numpy(images).type(torch.FloatTensor)).cuda()
                    targets = [Variable(torch.from_numpy(ann.astype(np.float32)).type(torch.FloatTensor)) for ann in
                               targets]
                else:
                    images = Variable(torch.from_numpy(images).type(torch.FloatTensor))
                    targets = [Variable(torch.from_numpy(ann.astype(np.float32)).type(torch.FloatTensor)) for ann in
                               targets]
            optimizer.zero_grad()
            outputs = net(images)

            # loss
            losses = []
            for i in range(3):
                loss_item = yolo_losses[i](outputs[i],targets)
                losses.append(loss_item[0])
            loss = sum(losses)

            # 解码
            output_list = []
            for i in range(3):
                output_list.append(yolo_decodes[i](outputs[i]))

            # 模型后处理
            cat_outputs = torch.cat(output_list,1)
            num_outputs = non_max_suppression(cat_outputs,num_classes, conf_thres=0.4, nms_thres=0.3)

            # 评价指标
            train_metrics += get_batch_statistics(input_shape, num_outputs, targets, conf_thres=0.4, iou_threshold=0.3)

            loss.backward()
            optimizer.step()
            train_loss += loss.item()
            time12 = datetime.datetime.now()
            # print('one batch --- ' + str(time12-time11))

        if len(train_metrics) != 0:
            true_positives, pred_scores, pred_labels = [np.concatenate(x, 0) for x in list(zip(*train_metrics))]
            train_precision, train_recall, train_AP, train_f1, ap_class = ap_per_class(true_positives, pred_scores,
                                                                                       pred_labels, train_labels)
            train_mp, train_mr, train_mf1, train_map = train_precision.mean(), train_recall.mean(), train_f1.mean(), train_AP.mean()
            print('%10s' * 5 % ('Class', 'P', 'R', 'F1_score', 'mAP'))
            pf = '%20s' + '%12.3g' * 4  # print format
            print(pf % ('all', train_mp, train_mr, train_mf1, train_map))
        time2 = datetime.datetime.now()
        print('training--- ' + str(time2-time1))

        # 是否停止
        if auto_termination == 1:
            if train_loss >= train_epoch_best_loss:
                no_optim += 1
            else:
                no_optim = 0
                train_epoch_best_loss = train_loss
            if no_optim > 6:
                print('loss not hava change, early stop at %d epoch' % epoch)
                break
            if no_optim > 3:
                if lr_scheduler.get_lr()[0] < 5e-7:
                    print('early stop at %d epoch' % epoch)
                    break
                lr_scheduler.step()
        time3 = datetime.datetime.now()
        print('auto_termination --- ' + str(time3 - time2))

        # 验证集
        print('valid....')
        net = net.eval()

        for iteration, batch in enumerate(valid_loader):
            images_val, targets_val = batch[0], batch[1]

            for num_i in range(len(targets_val)):
                if targets_val[num_i] is None:
                    continue
                annotations = targets_val[num_i]
                valid_labels += annotations[:, -1].tolist() if len(annotations) else []

            with torch.no_grad():
                if cuda:
                    images_val = Variable(torch.from_numpy(images_val).type(torch.FloatTensor)).cuda()
                    targets_val = [Variable(torch.from_numpy(ann.astype(np.float32)).type(torch.FloatTensor)) for ann in
                                   targets_val]
                else:
                    images_val = Variable(torch.from_numpy(images_val).type(torch.FloatTensor))
                    targets_val = [Variable(torch.from_numpy(ann.astype(np.float32)).type(torch.FloatTensor)) for ann in
                                   targets_val]

                optimizer.zero_grad()
                val_outputs = net(images_val)
                # loss
                losses = []
                for i in range(3):
                    loss_item = yolo_losses[i](val_outputs[i], targets_val)
                    losses.append(loss_item[0])
                loss = sum(losses)

                # 解码
                output_list = []
                for i in range(3):
                    output_list.append(yolo_decodes[i](val_outputs[i]))

                # 数据后处理
                val_cat_outputs = torch.cat(output_list, 1)
                val_nms_outputs = non_max_suppression(val_cat_outputs, num_classes, conf_thres=0.4, nms_thres=0.3)

                # 评价指标
                valid_metrics += get_batch_statistics(input_shape, val_nms_outputs, targets_val, conf_thres=0.4,
                                                           iou_threshold=0.3)

                valid_loss += loss.item()

        print("val_loss:" + str(valid_loss))
        if len(valid_metrics) != 0:
            val_true_positives, val_pred_scores, val_pred_labels = [np.concatenate(x, 0) for x in
                                                                    list(zip(*valid_metrics))]
            val_precision, val_recall, val_AP, val_f1, val_ap_class = ap_per_class(val_true_positives, val_pred_scores,
                                                                                   val_pred_labels, valid_labels)
            val_mp, val_mr, val_mf1, val_map = val_precision.mean(), val_recall.mean(), val_f1.mean(), val_AP.mean()

            print('%10s' * 5 % ('Class', 'P', 'R', 'F1_score', 'mAP'))
            pf = '%20s' + '%12.3g' * 4  # print format
            print(pf % ('all', val_mp, val_mr, val_mf1, val_map))

        time4 = datetime.datetime.now()
        print('auto_termination --- ' + str(time4 - time3))

    lr_scheduler.step()


def train_net_step2(net,train_loader,cuda,optimizer,
                    loss_fun,data_post_processing,metrics_fun,**kwargs):
    time1 = datetime.datetime.now()

    train_loss = 0
    train_labels = []
    train_metrics = []

    net = net.train()
    print('training...')

    for iteration,batch in enumerate(train_loader):
        time11 = datetime.datetime.now()
        images,targets = batch[0],batch[1]

        for num_i in range(len(targets)):
            if targets[num_i] is None:
                continue
            annotations = targets[num_i]
            train_labels += annotations[:,-1].tolist() if len(annotations) else []

        with torch.no_grad():
            if cuda:
                images = Variable(torch.from_numpy(images).type(torch.FloatTensor)).cuda()
                targets = [Variable(torch.from_numpy(ann.astype(np.float32)).type(torch.FloatTensor)) for ann in
                           targets]
            else:
                images = Variable(torch.from_numpy(images).type(torch.FloatTensor))
                targets = [Variable(torch.from_numpy(ann.astype(np.float32)).type(torch.FloatTensor)) for ann in
                           targets]

        optimizer.zero_grad()
        outputs = net(images)


        # loss
        if isfunction(loss_fun):
            loss = loss_fun(outputs,targets,**kwargs)
        else:
            print('ssssss loss')
            exit(1)
        # losses = []
        # for i in range(3):
        #     loss_item = yolo_losses[i](outputs[i],targets)
        #     losses.append(loss_item[0])
        # loss = sum(losses)

        # 解码data_post_processing,
        if isfunction(data_post_processing):
            outputs = data_post_processing(outputs,**kwargs)
        # output_list = []
        # for i in range(3):
        #     output_list.append(yolo_decodes[i](outputs[i]))
        #
        # # 模型后处理
        # cat_outputs = torch.cat(output_list,1)
        # num_outputs = non_max_suppression(cat_outputs,num_classes, conf_thres=0.4, nms_thres=0.3)

        # 评价指标

        if isfunction(metrics_fun):
            train_metrics += metrics_fun(outputs,targets,**kwargs)
        # train_metrics += get_batch_statistics(input_shape, num_outputs, targets, conf_thres=0.4, iou_threshold=0.3)

        loss.backward()
        optimizer.step()
        train_loss += loss.item()
        time12 = datetime.datetime.now()
        # print('one batch --- ' + str(time12-time11))

    if len(train_metrics) != 0:
        true_positives, pred_scores, pred_labels = [np.concatenate(x, 0) for x in list(zip(*train_metrics))]
        train_precision, train_recall, train_AP, train_f1, ap_class = ap_per_class(true_positives, pred_scores,
                                                                                   pred_labels, train_labels)
        train_mp, train_mr, train_mf1, train_map = train_precision.mean(), train_recall.mean(), train_f1.mean(), train_AP.mean()
        print('%10s' * 5 % ('Class', 'P', 'R', 'F1_score', 'mAP'))
        pf = '%20s' + '%12.3g' * 4  # print format
        print(pf % ('all', train_mp, train_mr, train_mf1, train_map))
    time2 = datetime.datetime.now()
    print('training--- ' + str(time2-time1))

    return net,optimizer,train_loss,train_metrics,train_labels


def test_net_step2(net,valid_loader,cuda,optimizer,middel_img_result,loss_fun,data_post_processing,metrics_fun,**kwargs):
    time3 = datetime.datetime.now()

    valid_loss = 0
    valid_labels = []
    valid_metrics = []

    # 验证集
    print('valid....')
    net = net.eval()

    for iteration, batch in enumerate(valid_loader):
        images_val, targets_val = batch[0], batch[1]

        for num_i in range(len(targets_val)):
            if targets_val[num_i] is None:
                continue
            annotations = targets_val[num_i]
            valid_labels += annotations[:, -1].tolist() if len(annotations) else []

        with torch.no_grad():
            if cuda:
                images_val = Variable(torch.from_numpy(images_val).type(torch.FloatTensor)).cuda()
                targets_val = [Variable(torch.from_numpy(ann.astype(np.float32)).type(torch.FloatTensor)) for ann in
                               targets_val]
            else:
                images_val = Variable(torch.from_numpy(images_val).type(torch.FloatTensor))
                targets_val = [Variable(torch.from_numpy(ann.astype(np.float32)).type(torch.FloatTensor)) for ann in
                               targets_val]

            optimizer.zero_grad()
            val_outputs = net(images_val)

            if isfunction(loss_fun):
                loss = loss_fun(val_outputs, targets_val, **kwargs)
            else:
                print('ssssss loss')
                exit(1)
            # losses = []
            # for i in range(3):
            #     loss_item = yolo_losses[i](outputs[i],targets)
            #     losses.append(loss_item[0])
            # loss = sum(losses)

            # 解码data_post_processing,
            if isfunction(data_post_processing):
                val_outputs = data_post_processing(val_outputs, **kwargs)

            # 解码
            # output_list = []
            # for i in range(3):
            #     output_list.append(yolo_decodes[i](val_outputs[i]))
            #
            # # 数据后处理
            # val_cat_outputs = torch.cat(output_list, 1)
            # val_nms_outputs = non_max_suppression(val_cat_outputs, num_classes, conf_thres=0.4, nms_thres=0.3)

            # 评价指标
            if isfunction(metrics_fun):
                valid_metrics = metrics_fun(val_outputs,targets_val, **kwargs)
            # valid_metrics += get_batch_statistics(input_shape, val_nms_outputs, targets_val, conf_thres=0.4,
            #                                       iou_threshold=0.3)

            valid_loss += loss.item()

            # 记录中间涂图片信息
            middel_img_result = middele_image_array([images_val.cpu().numpy(), images_val, targets_val, val_outputs],
                                                    2,middel_img_result, **kwargs)

    print("val_loss:" + str(valid_loss))
    if len(valid_metrics) != 0:
        val_true_positives, val_pred_scores, val_pred_labels = [np.concatenate(x, 0) for x in
                                                                list(zip(*valid_metrics))]
        val_precision, val_recall, val_AP, val_f1, val_ap_class = ap_per_class(val_true_positives, val_pred_scores,
                                                                               val_pred_labels, valid_labels)
        val_mp, val_mr, val_mf1, val_map = val_precision.mean(), val_recall.mean(), val_f1.mean(), val_AP.mean()

        print('%10s' * 5 % ('Class', 'P', 'R', 'F1_score', 'mAP'))
        pf = '%20s' + '%12.3g' * 4  # print format
        print(pf % ('all', val_mp, val_mr, val_mf1, val_map))

    time4 = datetime.datetime.now()
    print('auto_termination --- ' + str(time4 - time3))

    return net,optimizer,valid_metrics,valid_labels,middel_img_result


# 验证集中根据中间策略保存相应的图片数组
def middele_image_array(image_list,network_type,middle_results_list,**kwargs):
    # 统计 batch中对应每张图片相应的评价指标，并进行记录

    middel_results_data = kwargs['middel_results_name']

    num_class  = kwargs['num_classes']
    input_shape = kwargs['input_shape']

    middel_results_name, middle_results_count = middel_results_data[0],middel_results_data[1]

    images_batch = image_list[0]
    images2_batch = image_list[1]
    masks_batch = image_list[2]
    outputs_batch = image_list[3]

    for img, mask, pred in zip(images_batch, masks_batch, outputs_batch):

        if pred is None:
            continue

        if network_type == 1 or network_type == 3:  # 像素级别
            mean_metric = precision_recall_mean_image(img, pred, num_class, name=middel_results_name)
        elif network_type == 2:     # 目标框
            mean_metric = metics_value_one(input_shape,[mask],[pred], name=middel_results_name,conf_thres=0.5,iou_threshold=0.5)
            pred = pred.cpu().numpy()

        # 根据策略保存对应的数组列表middle_metrics_list, middle_results_count,image_list, mean_metric
        middle_results_list = middle_image_array(middle_results_list, middle_results_count,
                                                                    [img,mask,pred], mean_metric)

    return middle_results_list


# 获取得到label标签
def true_labe_list(targets):
    val_labels = []
    for num_i in range(len(targets)):
        if targets[num_i] is None:
            continue
        annotations = targets[num_i]
        val_labels += annotations[:, -1].tolist() if len(annotations) else []
    return val_labels

# 一张图片的混淆矩阵及相关评价指标
def metics_value_one(input_shape,target,output,name='each_epoch_error',conf_thres=0.4,
                         iou_threshold=0.3):

    val_labels = true_labe_list(target)
    metric_ = 0.
    metrics = get_batch_statistics(input_shape, output, target, conf_thres, iou_threshold)
    if len(metrics) > 0:
        val_true_positives, val_pred_scores, val_pred_labels = [np.concatenate(x, 0) for x in
                                                                list(zip(*metrics))]

        train_precision, train_recall, train_AP, train_f1, ap_class = ap_per_class(val_true_positives, val_pred_scores, val_pred_labels, val_labels)

        metric_ = None
        if name == "each_epoch_error":  # 误检率FP/(FP+TN)
            metric_ = 1 - train_precision.mean()
        elif name == 'each_epoch_error':  # 漏检率 1-racall
            metric_ = 1 - train_recall.mean()

    # miss_rate,fp_rate = miss_fp_rate_per(val_true_positives, val_pred_scores, val_pred_labels, val_labels,name)
    return metric_

def train_net_step(net,train_loader,cuda,optimizer,yolo_losses,yolo_decodes,num_classes,input_shape):
    time1 = datetime.datetime.now()

    train_loss = 0
    train_labels = []
    train_metrics = []

    net = net.train()
    print('training...')

    for iteration,batch in enumerate(train_loader):
        time11 = datetime.datetime.now()
        images,targets = batch[0],batch[1]

        for num_i in range(len(targets)):
            if targets[num_i] is None:
                continue
            annotations = targets[num_i]
            train_labels += annotations[:,-1].tolist() if len(annotations) else []

        with torch.no_grad():
            if cuda:
                images = Variable(torch.from_numpy(images).type(torch.FloatTensor)).cuda()
                targets = [Variable(torch.from_numpy(ann.astype(np.float32)).type(torch.FloatTensor)) for ann in
                           targets]
            else:
                images = Variable(torch.from_numpy(images).type(torch.FloatTensor))
                targets = [Variable(torch.from_numpy(ann.astype(np.float32)).type(torch.FloatTensor)) for ann in
                           targets]
        optimizer.zero_grad()
        outputs = net(images)

        # loss
        losses = []
        for i in range(3):
            loss_item = yolo_losses[i](outputs[i],targets)
            losses.append(loss_item[0])
        loss = sum(losses)

        # 解码
        output_list = []
        for i in range(3):
            output_list.append(yolo_decodes[i](outputs[i]))

        # 模型后处理
        cat_outputs = torch.cat(output_list,1)
        num_outputs = non_max_suppression(cat_outputs,num_classes, conf_thres=0.4, nms_thres=0.3)

        # 评价指标
        train_metrics += get_batch_statistics(input_shape, num_outputs, targets, conf_thres=0.4, iou_threshold=0.3)

        loss.backward()
        optimizer.step()
        train_loss += loss.item()
        time12 = datetime.datetime.now()
        # print('one batch --- ' + str(time12-time11))

    if len(train_metrics) != 0:
        true_positives, pred_scores, pred_labels = [np.concatenate(x, 0) for x in list(zip(*train_metrics))]
        train_precision, train_recall, train_AP, train_f1, ap_class = ap_per_class(true_positives, pred_scores,
                                                                                   pred_labels, train_labels)
        train_mp, train_mr, train_mf1, train_map = train_precision.mean(), train_recall.mean(), train_f1.mean(), train_AP.mean()
        print('%10s' * 5 % ('Class', 'P', 'R', 'F1_score', 'mAP'))
        pf = '%20s' + '%12.3g' * 4  # print format
        print(pf % ('all', train_mp, train_mr, train_mf1, train_map))
    time2 = datetime.datetime.now()
    print('training--- ' + str(time2-time1))

    return net,optimizer,train_loss


def test_net_step(net,valid_loader,cuda,optimizer,yolo_losses,yolo_decodes,num_classes,input_shape):
    time3 = datetime.datetime.now()

    valid_loss = 0
    valid_labels = []
    valid_metrics = []

    # 验证集
    print('valid....')
    net = net.eval()

    for iteration, batch in enumerate(valid_loader):
        images_val, targets_val = batch[0], batch[1]

        for num_i in range(len(targets_val)):
            if targets_val[num_i] is None:
                continue
            annotations = targets_val[num_i]
            valid_labels += annotations[:, -1].tolist() if len(annotations) else []

        with torch.no_grad():
            if cuda:
                images_val = Variable(torch.from_numpy(images_val).type(torch.FloatTensor)).cuda()
                targets_val = [Variable(torch.from_numpy(ann.astype(np.float32)).type(torch.FloatTensor)) for ann in
                               targets_val]
            else:
                images_val = Variable(torch.from_numpy(images_val).type(torch.FloatTensor))
                targets_val = [Variable(torch.from_numpy(ann.astype(np.float32)).type(torch.FloatTensor)) for ann in
                               targets_val]

            optimizer.zero_grad()
            val_outputs = net(images_val)
            # loss
            losses = []
            for i in range(3):
                loss_item = yolo_losses[i](val_outputs[i], targets_val)
                losses.append(loss_item[0])
            loss = sum(losses)

            # 解码
            output_list = []
            for i in range(3):
                output_list.append(yolo_decodes[i](val_outputs[i]))

            # 数据后处理
            val_cat_outputs = torch.cat(output_list, 1)
            val_nms_outputs = non_max_suppression(val_cat_outputs, num_classes, conf_thres=0.4, nms_thres=0.3)

            # 评价指标
            valid_metrics += get_batch_statistics(input_shape, val_nms_outputs, targets_val, conf_thres=0.4,
                                                  iou_threshold=0.3)

            valid_loss += loss.item()

    print("val_loss:" + str(valid_loss))
    if len(valid_metrics) != 0:
        val_true_positives, val_pred_scores, val_pred_labels = [np.concatenate(x, 0) for x in
                                                                list(zip(*valid_metrics))]
        val_precision, val_recall, val_AP, val_f1, val_ap_class = ap_per_class(val_true_positives, val_pred_scores,
                                                                               val_pred_labels, valid_labels)
        val_mp, val_mr, val_mf1, val_map = val_precision.mean(), val_recall.mean(), val_f1.mean(), val_AP.mean()

        print('%10s' * 5 % ('Class', 'P', 'R', 'F1_score', 'mAP'))
        pf = '%20s' + '%12.3g' * 4  # print format
        print(pf % ('all', val_mp, val_mr, val_mf1, val_map))

    time4 = datetime.datetime.now()
    print('auto_termination --- ' + str(time4 - time3))

    return net,optimizer


def auto_stop_net(train_loss,train_epoch_best_loss,no_optim,lr_scheduler,epoch):
    # 是否停止
    time2 = datetime.datetime.now()
    if train_loss >= train_epoch_best_loss:
        no_optim += 1
    else:
        no_optim = 0
        train_epoch_best_loss = train_loss
    if no_optim > 6:
        print('loss not hava change, early stop at %d epoch' % epoch)
        exit(0)
    if no_optim > 3:
        if lr_scheduler.get_lr()[0] < 5e-7:
            print('early stop at %d epoch' % epoch)
            exit(0)
        lr_scheduler.step()
    time3 = datetime.datetime.now()
    print('auto_termination --- ' + str(time3 - time2))

    return train_epoch_best_loss,no_optim,lr_scheduler



# 网络结构在gpu上进行加载
def model_gpu_loader(net, device_ids,network_type):
    if torch.cuda.is_available():
        net = torch.nn.DataParallel(net, device_ids)

        if network_type == 2:
            import torch.backends.cudnn as cudnn
            cudnn.benchmark = True
        net = net.cuda()
    return net

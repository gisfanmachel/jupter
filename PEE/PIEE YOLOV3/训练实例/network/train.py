# 引入网络结构封装代码
from pie.get_platform_arguments import *
from pie.train_center.pytorch.train_epoch_step import train_model_step, auto_termination, save_checkpoint, \
    test_model_step,model_gpu_loader
from yolov3_train_def import metrics_yolo_train, yolo_post_processing, epoch_loss_train, \
    create_decode, create_loss
# from pie.train_center.pytorch.model_deal.yolo_train_def import yolo_post_processing, epoch_loss_train, \
#     create_decode, create_loss
from nets.yolov3 import YoloV3
import torch

if __name__ == '__main__':

    # 获取参数 初始化
    init_parse = parse_platform_arguments()

    # 获取数据
    train_loader,valid_loader = init_parse.dataset_train_valid_loader()

    # 训练相关参数
    # loss方法
    anchors = init_parse.anchors
    num_classes = init_parse.num_classes
    input_shape = init_parse.input_shape

    # 系统内置的模型
    # net = init_parse.model_loader_build_in()
    net = YoloV3(anchors, num_classes)

    # 创建网络结构，并加载预训练模型
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(DEVICE)
    net.to(DEVICE)
    if DEVICE == 'cuda':
        if torch.cuda.device_count() > 1:
            net = torch.nn.DataParallel(network, device_ids)
    # net = model_gpu_loader(net, init_parse.device_ids, init_parse.node_num, init_parse.local_rank)
    # 学习率
    optimizer = init_parse.optimizer_build_in(net)
    lr_scheduler = init_parse.lr_scheduler_build_in(optimizer)
    # optimizer = torch.optim.Adam(net.parameters(), init_parse.learning_rate, weight_decay=5e-5)
    # lr_scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=5, eta_min=1e-7)

    # 初始化loss
    yolo_losses = create_loss(anchors, num_classes, input_shape)

    # 解码
    yolo_decodes = create_decode(anchors, num_classes, input_shape)

    # 输出中间图片策略

    # 中间输出图片相关参数
    middel_results_name = init_parse.middle_results
    middle_image_dict = {}
    middle_results_dict = {}
    middel_img_result = [middle_results_dict, middle_image_dict]

    # 参数
    kwards = {
        "yolo_losses": yolo_losses,
        "yolo_decodes": yolo_decodes,
        "input_shape": input_shape,
        "num_classes": num_classes,
        "middel_results_name":middel_results_name
    }
    # loss损失计算
    loss_col = epoch_loss_train
    # 模型后处理
    post_prcessing = yolo_post_processing
    # 评价指标方法
    metrics_col = metrics_yolo_train

    epochs = init_parse.epochs
    cuda = True
    epoch_best_loss = 1e5
    no_optim = 0
    log_init = None
    for epoch in range(0, init_parse.epochs):

        print('epoch : ' + str(epoch + 1))
        # 训练
        net,optimizer,train_metrics, train_loss ,lables_ = train_model_step(net, train_loader,init_parse.network_type,optimizer,cuda,
                                                     loss_col, post_prcessing,metrics_col,**kwards)

        # 保存日志
        log_init = init_parse.save_trainlog_json_epoch(epoch, epochs, train_loss, len(iter(train_loader)), train_metrics,
                                                       middle_results_dict=None, act_label=lables_,
                                            log_train=True, log_init=None)
        # 保存权重文件
        save_checkpoint(net, init_parse.weight_path)

        # 是否提前停止
        if init_parse.auto_termination == 1:
            if epoch_best_loss > train_loss:
                epoch_best_loss = train_loss
            auto_termination(net, epoch, train_loss, epoch_best_loss, init_parse.learning_rate, no_optim,
                             init_parse.weight_path)

        # ========================================================
        # 验证
        # 初始化混淆矩阵函数
        valid_metrics = None
        valid_epoch_loss = 0.


        net,valid_metrics, test_epoch_loss, middel_img_result,valid_labels = test_model_step(net,valid_loader,init_parse.network_type ,
                                                                                                 cuda,
                                                                                                 middel_img_result,
                                                                                                 loss_col,post_prcessing,metrics_col,**kwards)

        # 保存日志及中间图片
        log_init = init_parse.save_trainlog_json_epoch(epoch, epochs,test_epoch_loss, len(iter(valid_loader)), valid_metrics,
                                                       middle_results_dict=middel_img_result[0],act_label=valid_labels,
                                                       log_train=False,log_init=log_init)



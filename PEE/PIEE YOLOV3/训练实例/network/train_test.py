from pie.get_platform_arguments  import *

if __name__ == '__main__':

    print('22222222')
    init_parse = parse_platform_arguments()
    print('ssssssssss')

    # 获取得到模型
    # net = LinkNet34()

    # 系统内置的模型
    model_build_in = init_parse.model_loader_build_in()
    net = model_build_in

    # 获取数据
    train_loader,valid_loader = init_parse.dataset_train_valid_loader()

    # 训练相关参数
    # loss方法
    loss_class = init_parse.loss_fun

    # 评价指标方法
    metrics = init_parse.metrics_build_in()
    metrics_list = init_parse.metrics_list

    # 学习策略
    optimizer = init_parse.optimizer_build_in(net=net)

    # 优化器
    lr_step = init_parse.lr_scheduler_build_in(optimizer=optimizer)

    # 数据类别
    num_classes = init_parse.num_classes
    # 输出中间图片策略
    middle_result_name = init_parse.middle_result_name
    middle_result_count = init_parse.middle_result_count

    middle_image_dict = {}
    middle_results_dict = {}
    epoch_best_loss = 1e5
    no_optim = 0
    log_init = None
    for epoch in range(0, init_parse.epoch):
        # 初始化混淆矩阵函数
        train_metrics = metrics
        # 训练
        train_epoch_loss = 0.

        # 数据集loader
        train_data_loader_iter = iter(train_loader)

        net.train()
        train_metrics, train_loss = train_model_step(net, train_data_loader_iter,init_parse.network_type ,optimizer, loss_class,
                                                     train_epoch_loss, train_metrics)

        # 保存日志
        log_init = init_parse.save_trainlog_json_epoch(epoch, train_loss, train_data_loader_iter, train_metrics,log_init=log_init)

        # 保存权重文件
        save_checkpoint(net, init_parse.weight_path)

        # 是否提前停止
        if init_parse.auto_termination == 1:
            if epoch_best_loss > train_loss:
                epoch_best_loss = train_loss
            auto_termination(net, epoch, train_epoch_loss, epoch_best_loss, init_parse.learning_rate, no_optim,
                             init_parse.weight_path)

        # ========================================================
        # 验证
        # 初始化混淆矩阵函数
        valid_metrics = metrics
        valid_epoch_loss = 0.
        # 数据集loader
        valid_data_loader_iter = iter(valid_loader)

        net.eval()
        valid_metrics, test_epoch_loss, middle_results_dict, middle_image_dict = test_model_step(net,
                                                                                                 valid_data_loader_iter,init_parse.network_type ,
                                                                                                 loss_class,
                                                                                                 valid_epoch_loss,
                                                                                                 valid_metrics,
                                                                                                 num_classes,
                                                                                                 middle_result_name,
                                                                                                 middle_result_count,
                                                                                                 middle_results_dict,
                                                                                                 middle_image_dict )

        # 保存日志及中间图片
        log_init = init_parse.save_trainlog_json_epoch(epoch, test_epoch_loss, valid_data_loader_iter, valid_metrics,
                                                       middle_results_dict=middle_results_dict, log_train=False,log_init=log_init)





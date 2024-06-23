def builder_model(model_name, backbone, **kwargs):
    """
    根据 name, backbone构造相应的网络结构
    :param model_name:
    :param backbone:
    :param kwargs:
    :return:
    """
    num_classes = kwargs['num_classes']
    in_channal = kwargs['in_channal']
    model_dir = kwargs['model_dir']
    s3_path = kwargs['s3_path']
    num_anchors = None
    if kwargs.get('num_anchors'):
        num_anchors = kwargs['num_anchors']
    model = None
    if model_name == "dinknet":
        from pie.network.models.pytorch.segmentation.Dinknet import dinknet34, dinknet50, dinknet101
        if backbone == "resnet34":
            model = dinknet34(num_classes, in_channal, model_dir, s3_path)
        elif backbone == "resnet50":
            model = dinknet50(num_classes, in_channal, model_dir, s3_path)
        elif backbone == "resnet101":
            model = dinknet101(num_classes, in_channal, model_dir, s3_path)
        else:
            print('not find network...')
    elif model_name == "siamunet_diff":
        from pie.network.models.pytorch.change.siamunet_diff import siamunet_diff
        network_name = 'siamunet_diff'
        if network_name:
            model = siamunet_diff(in_channal, num_classes, model_dir, s3_path)
    elif model_name == "yolov4":
        from pie.network.models.pytorch.detection.yolov4 import yolov4
        network_name = 'yolov4'
        if network_name:
            print('network_name--------------')
            print(network_name)
            model = yolov4(num_classes, num_anchors, model_dir, s3_path)
    elif model_name == "yolov3":
        from pie.network.models.pytorch.detection.yolov3 import yolov3
        network_name = 'yolov3'
        if network_name:
            print('network_name--------------')
            print(network_name)
            model = yolov3(num_classes, num_anchors, model_dir, s3_path)
    return model

# def builder_model(model_name,backbone):
#     network_name = None
#     if model_name == "dinknet":
#         if backbone == "resnet34":
#             network_name = 'dinknet34'
#         elif backbone == "resnet50":
#             network_name = 'dinknet50'
#         elif backbone == "resnet101":
#             network_name = 'dinknet101'
#         else:
#             print('not find network...')
#         if network_name:
#             import pie.network.models.pytorch.segmentation.Dinknet
#     elif model_name == "siamunet_diff":
#         network_name = 'siamunet_diff'
#         if network_name:
#             import pie.network.models.pytorch.change.siamunet_diff
#     elif model_name == "yolov4":
#         network_name = 'yolov4'
#         if network_name:
#             import pie.network.models.pytorch.detection.yolov4
#     return network_name

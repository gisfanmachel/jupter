'''
    智能解译 读取图片，预测，并进行相关处理
    wangtuo 20211206
'''

# 语义分割中间单波段名称
one_bands_file = 'pre_tem.tif'

import os

from pie.pre_center.common.deal_result import create_zip, save_log, \
     generateOvrFile, raster_shp, create_shp_detection, \
    shp_to_geojson, static_label, insert_pg
from pie.pre_center.common.pred_image import pred_image_seg_change, pred_image_detection, init_gdal, read_img


def predict_image(**platform_arguments):
    '''
    模型评估预测图片

    :param load_model: 模型
    :param preprocess:  数据预处理
    :param postprocess:  数据后处理
    :param platform_argumnets: 相关参数
    :return:
    '''

    load_model = platform_arguments['load_model']
    preprocess = platform_arguments['data_preprocessing']
    postprocess = platform_arguments['data_post_processing']

    network_type = platform_arguments['network_type']
    estimate_id = platform_arguments['estimate_id']
    load_size_ = platform_arguments['load_size']

    # 预测数据处理需要字段
    value_color_ = platform_arguments['value_color']
    background_value_ = platform_arguments['background_value']
    value_name_map = platform_arguments['value_name_map']
    value_title_map_ = platform_arguments['value_title_map']
    name_title_map = platform_arguments['name_title_map']
    class_name_ = platform_arguments['class_name_list']
    nms_value = platform_arguments['nms']
    ehance = platform_arguments['trans_pipelines']
    print('ehance--------'+ ehance) 

    out_root_path = platform_arguments['result_path']
    outputSaveDir = os.path.join(out_root_path,'picture')
    json_file = os.path.join(out_root_path,'trainlog.json')

    cuda = True

    s3gdal = init_gdal()
    # 加载模型
    model = load_model(**platform_arguments)
    model = model.eval()

    # 获取预测图片列表
    input_list = platform_arguments['image_path'].split(',')

    # 记录日志
    # TODO : outputSaveDir 输出位置
    log_new = {"zipOutFile": '/' + '/'.join(outputSaveDir.split('/')[2:]) + "/result.zip", "total_output_size": "",
               "task_list": []}

    total_output_size = 0

    # 遍历图片，进行每张图片预测
    for index, imagePath in enumerate(input_list):
        process = float((index + 1) / len(input_list))
        log_new["process"] = process
        taskIdAndIndex = estimate_id + ":" + str(index + 1)

        tmpfilename = os.path.basename(imagePath)
        filename, extension = os.path.splitext(tmpfilename)

        # 重命名，例如： 1_xxx_pred
        filename = str(index + 1) + "_" + filename + "_pred"

        # 输出
        tif_path = outputSaveDir + "/"+filename + ".tif"
        shp_file = outputSaveDir + "/"+filename + ".shp"

        # 读取数据
        data,data2 = read_img(s3gdal, imagePath)

        im_proj=data.GetProjection()
        # 预测并处理
        if network_type == 1 or network_type == 3:
            # 预测
            pred_image_seg_change(model,data,data2,s3gdal,tif_path, load_size_, preprocess, postprocess, value_color_,
                                  background_value_,cuda,ehance,**platform_arguments)
            # 处理
            staticMap = deal_piexl_result(network_type,tif_path,taskIdAndIndex, value_name_map, value_title_map_,
                              value_color_,name_title_map,im_proj)
        elif network_type == 2:
            # 预测
            strcoordinates_box = pred_image_detection(model,data,shp_file,load_size_,class_name_,preprocess,
                                 postprocess,value_title_map_,cuda,ehance,nms_value,**platform_arguments)

            staticMap = deal_obj_result(network_type,shp_file,strcoordinates_box,taskIdAndIndex,
                            value_title_map_,value_color_,name_title_map,im_proj)
        else:
            print('输入类型有误！')
            exit(1)

        # 日志信息
        log_info_dict = {
            "task_result_id": taskIdAndIndex,
            "output_shp_static": staticMap,
            "output_size": "",
            "input": imagePath,
            "output": [],
        }
        # 记录日志信息
        save_log(json_file,log_info_dict, total_output_size, tif_path,log_new,index,len(input_list))

    # 矢量进行压缩
    create_zip(outputSaveDir)


def deal_piexl_result(network_type,tif_path,taskIdAndIndex, value_name_map, value_title_map, value_color,name_title_map,im_proj):
    '''
    处理 像素级别结果 获取得到单波段 预测数据
    1. 生成金字塔
    2. tif转为shp矢量
    3. shp矢量存入数据库
    :return:
    '''
    # 1. 生成金字塔
    generateOvrFile(tif_path)
    # 2. tif转shp
    one_file = '/'.join(tif_path.split('/')[:-2]) + '/' + one_bands_file
    shp_file = tif_path[:-4] + ".shp"
    staticMap = raster_shp(one_file, shp_file, value_name_map, value_title_map, value_color)
    # 3. 矢量保存到数据库
    insert_pg(network_type, shp_file, name_title_map, taskIdAndIndex,im_proj)

    return staticMap


def deal_obj_result(network_type,shp_file,strcoordinates_box,taskIdAndIndex,value_title_map,value_color,name_title_map,im_proj):
    '''
    处理 目标识别结果 获取得到 目标检测框矢量
    1. shp矢量转转为 geojson
    2. 统计目标框 类别及个数
    3. shp矢量存入数据库
    :return:
    '''
    json_file = shp_file.replace('.shp', '.json')

    # 2. 统计
    statisticList = create_shp_detection(strcoordinates_box, shp_file, value_title_map)
    shp_to_geojson(shp_file, json_file, name_title_map)
    staticMap = static_label(statisticList, value_color)

    # 3. 矢量保存到数据库
    insert_pg(network_type, shp_file, name_title_map, taskIdAndIndex,im_proj)

    return staticMap


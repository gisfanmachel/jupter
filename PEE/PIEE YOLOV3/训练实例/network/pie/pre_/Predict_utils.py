import glob
import os
import sys
import numpy as np
import json
import torch

try:
    from osgeo import ogr
    from osgeo import osr
except ImportError:
    import ogr
    import osr

import gdalconst

import warnings
import zipfile

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
warnings.filterwarnings('ignore')

basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(basedir + '/so/torch')
import shp2pg_utils
import raster2shp

# 写入trainlog.json中output的后缀集合
fileKey = ['.tif', '.json', '.cpg', '.dbf', '.prj', '.shx', '.shp', '.ovr']
# 压缩包添加矢量后缀
shpFileKey = ['.cpg', '.dbf', '.prj', '.shx', '.shp']

# 输出保存位置
outputSaveDir = basedir + '/output/picture/'
if not os.path.exists(outputSaveDir):
    os.makedirs(outputSaveDir)


# 加载输入数据 (不同方式获取数据)
def parse_platform_arguments_example():
    '''
        从 traincfg.json中读取参数，设置 network_type 类型
    :return:
    '''
    basedir = os.getcwd()
    config_path = basedir + "/traincfg.json"
    with open(config_path, 'r', encoding='utf-8') as f:
        params = json.load(f)
    load_size = params["load_size"]
    labels = params["label"]

    platform_arguments = {
        'estimate_id': None,  # 任务ID
        'image_path': None,  # 训练图片路径
        'device_ids': None,  # gpu device id 数
        'network_type': 1,  # 预测的类别 （必填）
        'load_size': None,  # 图片加载大小
        'value_name_map': None,  # 训练value对应英文名称
        'value_title_map': None,  # 训练value对应类别中文名称
        'name_title_map': None,  # 类别英文名称 对应类别中文名称
        'value_color': None,  # 训练value对应 rgb()颜色
        'background_value': None,  # 背景对应的训练value
        'class_name_list': None,  # 除背景外的类别列表
        'load_model': None,  # 模型加载方法
        'deal_data_img': None,  # 处理进入到模型里面的数据方法
        'deal_pred_result': None,  # 处理模型预测后的结果方法
        'nms': 0.3,  # 目标识别
    }
    conf = input()
    params_estimate = json.loads(conf)
    platform_arguments['estimate_id'] = params_estimate['estimate_id']
    platform_arguments['image_path'] = params_estimate["image_path"]

    platform_arguments['device_ids'] = []
    gpu_num = int(params_estimate["gpu_num"])
    if gpu_num != 0:
        for i in range(0, gpu_num):
            platform_arguments['device_ids'].append(i)

    network_type = platform_arguments["network_type"]
    platform_arguments['network_type'] = network_type

    # 图片大小处理
    load_size = load_size.split(',')
    load_size[0] = round(float(load_size[0]) / 32) * 32
    load_size[1] = round(float(load_size[1]) / 32) * 32
    if load_size[1] > load_size[0]:
        load_size[1] = load_size[0]
    else:
        load_size[0] = load_size[1]
    platform_arguments['load_size'] = load_size

    # 标签处理
    labels = labels
    labels = eval(labels)

    # 图片对应从0开始的数值，训练时使用的数据
    # 训练value对应类别英文名称
    platform_arguments['value_name_map'] = {}
    # 训练value对应类别中文名称
    platform_arguments['value_title_map'] = {}
    # 类别英文名称 对应类别中文名称
    platform_arguments['name_title_map'] = {}
    # 训练value对应 rgb()颜色
    platform_arguments['value_color'] = {}
    # 背景的训练值
    platform_arguments['background_value'] = None
    platform_arguments['class_name_list'] = []
    rgb = None
    value = None

    for i, val in enumerate(labels):
        for key in val.keys():
            if key == "class_name":
                name = val[key]
                if network_type == 2 and name == 'background':
                    break
            elif key == "class_color":
                color_ = val[key]
                rgb = tuple(list(map(int, color_.split(','))))
            elif key == "class_value":
                value = int(val[key])
                if network_type == 2:
                    trainValue = int(i) - 1
                else:
                    trainValue = int(i)
            elif key == "class_title":
                title = val[key]
            else:
                continue
        if rgb and value >= 0:
            platform_arguments['value_name_map'][trainValue] = name
            platform_arguments['value_title_map'][trainValue] = title
            platform_arguments['name_title_map'][name] = title
            platform_arguments['value_color'][trainValue] = rgb
            platform_arguments['name_title_map'][name] = title
            if name == "background":
                platform_arguments['background_value'] = trainValue
            else:
                platform_arguments['class_name_list'].append(name)
    return platform_arguments


def generateOvrFile(src_file, update=True):
    """
    生产金字塔文件
    :param src_file:
    :param update:
    :return:
    """
    print("generateOvrFile process file: {0}".format(src_file))
    if not os.path.exists(src_file):
        print("generateOvrFile: {0} is not exist".format(src_file))
        return
    _ovr_file = "{}.ovr".format(src_file)
    if os.path.exists(_ovr_file):
        if update:
            os.remove(_ovr_file)
        else:
            return
    cmd_str = "gdaladdo -r NEAREST -ro --config COMPRESS_OVERVIEW LZW {0}".format(src_file)
    return os.system(cmd_str)

# 转换为3波段的tif
def classToRGB( mask, trainvalue_rgb):
    '''

    Args:
        mask: 预测的单波段tif，其中数值为预测的value
        trainvalue_rgb: 训练用的value 对应 rgb 颜色

    Returns:
        三波段的tif

    '''
    import ast
    colmap = np.zeros(shape=(mask.shape[0], mask.shape[1], 3)).astype(np.uint8)
    for train_value in trainvalue_rgb.keys():
        rgb = ast.literal_eval(trainvalue_rgb[train_value][3:])
        indices = np.where(mask == train_value)
        colmap[indices[0].tolist(),
        indices[1].tolist(), :] = np.array(rgb)
    return colmap

def shp_to_geojson(shpFile, jsonPath, clsname_clstitle_map):
    '''

    Args: 目标识别
        shpFile: 矢量shp路径
        jsonPath: json的路径
        clsname_clstitle_map: 类别名称与类别title对应

    Returns: geojson

    '''
    print("convert to geojson start........")
    # 打开矢量图层
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
    gdal.SetConfigOption("SHAPE_ENCODING", "GBK")
    shp_ds = ogr.Open(shpFile)
    shp_lyr = shp_ds.GetLayer()

    # 创建结果Geojson
    baseName = os.path.basename(jsonPath)
    out_driver = ogr.GetDriverByName('GeoJSON')
    out_ds = out_driver.CreateDataSource(jsonPath)
    if out_ds.GetLayer(baseName):
        out_ds.DeleteLayer(baseName)
    out_lyr = out_ds.CreateLayer(baseName, shp_lyr.GetSpatialRef())
    out_lyr.CreateFields(shp_lyr.schema)

    out_feat = ogr.Feature(out_lyr.GetLayerDefn())

    # 生成结果文件
    for feature in shp_lyr:
        out_feat.SetGeometry(feature.geometry())
        for j in range(feature.GetFieldCount()):
            # 将类别名称转换为中文
            if feature.GetField(j) in clsname_clstitle_map.keys():
                out_feat.SetField(j, clsname_clstitle_map[feature.GetField(j)])

            out_feat.SetField(j, feature.GetField(j))
        out_lyr.CreateFeature(out_feat)

    del(out_ds,shp_ds)
    del(out_feat,out_lyr)
    print("convert to geojson Success........")

# 目标识别统计
def static_label(statisticList,class_color):
    if not statisticList or  len(statisticList)==0:
        print('未检测到目标')
        return None
    staticMap = []
    uniqueClassTitle = []
    for ind in statisticList:

        classTitle = ind['classTitle']
        classId = ind['classId']

        if uniqueClassTitle and classTitle in uniqueClassTitle:
            for i in staticMap:
                cln = i.get('classTitle')
                if cln and cln in uniqueClassTitle:
                    i['count'] = int(i.get('count')) + 1
        else:
            classDic = {}
            classDic['classTitle'] = classTitle
            classDic['count'] = 1
            classDic['color'] = class_color[classId]
            staticMap.append(classDic)

        if classTitle not in uniqueClassTitle:
            uniqueClassTitle.append(classTitle)
    return staticMap

def bytes(bytes):
    '''

    Args:
        bytes: 字节统计

    Returns: 返回字符串，字节相应得到大小，带单位

    '''
    if bytes < 1024:  # 比特
        bytes = str(round(bytes, 2)) + ' B'  # 字节
    elif bytes >= 1024 and bytes < 1024 * 1024:
        bytes = str(round(bytes / 1024, 2)) + ' KB'  # 千字节
    elif bytes >= 1024 * 1024 and bytes < 1024 * 1024 * 1024:
        bytes = str(round(bytes / 1024 / 1024, 2)) + ' MB'  # 兆字节
    elif bytes >= 1024 * 1024 * 1024 and bytes < 1024 * 1024 * 1024 * 1024:
        bytes = str(round(bytes / 1024 / 1024 / 1024, 2)) + ' GB'  # 千兆字节
    elif bytes >= 1024 * 1024 * 1024 * 1024 and bytes < 1024 * 1024 * 1024 * 1024 * 1024:
        bytes = str(round(bytes / 1024 / 1024 / 1024 / 1024, 2)) + ' TB'  # 太字节
    elif bytes >= 1024 * 1024 * 1024 * 1024 * 1024 and bytes < 1024 * 1024 * 1024 * 1024 * 1024 * 1024:
        bytes = str(round(bytes / 1024 / 1024 / 1024 / 1024 / 1024, 2)) + ' PB'  # 拍字节
    elif bytes >= 1024 * 1024 * 1024 * 1024 * 1024 * 1024 and bytes < 1024 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024:
        bytes = str(round(bytes / 1024 / 1024 / 1024 / 1024 / 1024 / 1024, 2)) + ' EB'  # 艾字节
    return bytes


# 整张图的位置
def get_region_boxes(patch_box, x_start, y_start):
    xmin = x_start + patch_box[2]
    ymin = y_start + patch_box[3]
    xmax = x_start + patch_box[4]
    ymax = y_start + patch_box[5]

    image_box = [patch_box[0], patch_box[1], xmin, ymin, xmax, ymax]
    return image_box

# 非极大值抑制的实现
def py_cpu_nms(dets, thresh):

    if len(dets) == 0:
        return []
    """Pure Python NMS baseline."""
    dets = np.array(dets)
    # print(dets)
    x1 = dets[:, 2]
    y1 = dets[:, 3]
    x2 = dets[:, 4]
    y2 = dets[:, 5]
    scores = dets[:, 1]  # bbox打分
    boxes = []
    areas = (x2 - x1 + 1) * (y2 - y1 + 1)
    # 打分从大到小排列，取index
    order = scores.argsort()[::-1]
    # keep为最后保留的边框
    keep = []
    while order.size > 0:
        # order[0]是当前分数最大的窗口，肯定保留
        i = order[0]
        boxes.append(dets[i])
        keep.append(i)
        # 计算窗口i与其他所有窗口的交叠部分的面积
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])

        w = np.maximum(0.0, xx2 - xx1 + 1)
        h = np.maximum(0.0, yy2 - yy1 + 1)
        inter = w * h
        # 交/并得到iou值
        ovr = inter / (areas[i] + areas[order[1:]] - inter)
        # inds为所有与窗口i的iou值小于threshold值的窗口的index，其他窗口此次都被窗口i吸收
        inds = np.where(ovr <= thresh)[0]
        # order里面只保留与窗口i交叠面积小于threshold的那些窗口，由于ovr长度比order长度少1(不包含i)，所以inds+1对应到保留的窗口
        order = order[inds + 1]

    return boxes


# 目标识别通过框数据生成shp 并进行个类别统计
def create_shp_detection(strcoordinates_box,strcoordinates,ShpFileName,value_title_map):
    n = len(strcoordinates_box)
    print('rect number:', n)
    strcoordinates = strcoordinates[0:n - 1] + ")"

    # 为了支持中文路径，请添加下面这句代码
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "NO")
    # 为了使属性表字段支持中文，请添加下面这句
    gdal.SetConfigOption("SHAPE_ENCODING", "")
    # 注册所有的驱动

    # 注册所有的驱动
    ogr.RegisterAll()

    # 创建数据，这里以创建ESRI的shp文件为例
    strDriverName = "ESRI Shapefile"
    oDriver = ogr.GetDriverByName(strDriverName)
    if oDriver == None:
        print("%s 驱动不可用！\n", strDriverName)
        return

    # 创建数据源
    oDS = oDriver.CreateDataSource(ShpFileName)
    if oDS == None:
        print("创建文件【%s】失败！", ShpFileName)
        return

    # 创建图层，创建一个多边形图层，这里没有指定空间参考，如果需要的话，需要在这里进行指定
    papszLCO = []
    oLayer = oDS.CreateLayer("TestPolygon", None, ogr.wkbPolygon, papszLCO)
    if oLayer == None:
        print("图层创建失败！\n")
        return
    # 下面创建属性表
    # 先创建一个叫FieldID的整型属性
    oFieldID = ogr.FieldDefn("FieldID", ogr.OFTInteger)
    oLayer.CreateField(oFieldID, 1)

    # 再创建一个叫FeatureName的字符型属性，字符长度为50
    oFieldName = ogr.FieldDefn("FieldName", ogr.OFTString)
    oFieldName.SetWidth(100)
    oLayer.CreateField(oFieldName, 1)

    # 再创建一个叫FeatureName的字符型属性，score
    oFieldscore = ogr.FieldDefn("score", ogr.OFTReal)
    oLayer.CreateField(oFieldscore, 1)

    # 再创建一个叫FeatureName的字符型属性，字符长度为50
    oFieldColor = ogr.FieldDefn("Color", ogr.OFTString)
    oFieldColor.SetWidth(100)
    oLayer.CreateField(oFieldColor, 1)

    oDefn = oLayer.GetLayerDefn()
    statisticList = []
    # 创建矩形要素
    for i in range(len(strcoordinates_box)):
        oFeatureRectangle = ogr.Feature(oDefn)
        # oFeatureRectangle.SetField(0, 1)
        # print(strcoordinates_box[i])
        oFeatureRectangle.SetField(0, i)
        geomRectangle = ogr.CreateGeometryFromWkt('POLYGON ((%f1 %f2,%f3 %f4,%f5 %f6,%f7 %f8,%f9 %f10))' %
                                                  (strcoordinates_box[i][0], strcoordinates_box[i][1],
                                                   strcoordinates_box[i][2], strcoordinates_box[i][3],
                                                   strcoordinates_box[i][4],
                                                   strcoordinates_box[i][5], strcoordinates_box[i][6],
                                                   strcoordinates_box[i][7], strcoordinates_box[i][8],
                                                   strcoordinates_box[i][9]))
        oFeatureRectangle.SetGeometry(geomRectangle)
        oFeatureRectangle.SetField(1, strcoordinates_box[i][11])
        oFeatureRectangle.SetField(2, strcoordinates_box[i][12])
        oFeatureRectangle.SetField(3, "rgb(255,0,0)")

        classMap = {'classId': int(strcoordinates_box[i][10])}
        classMap['classTitle'] = value_title_map[int(strcoordinates_box[i][10])]
        statisticList.append(classMap)

        oLayer.CreateFeature(oFeatureRectangle)

    oDS.Destroy()
    return statisticList

# 预测结果前的准备工作
class pred_prepare():
    def __init__(self,model,s3gdal,imagePath):

        self.imagePath = imagePath
        self.model = model
        self.dataset = None
        self.dataset2 = None
        self.im_projection = None
        self.statisticList = None
        self.cuda = torch.cuda.is_available()
        self.get_image_data()
        self.gdal = s3gdal

    def get_image_data(self):
        # gdal读取图片
        # s3文件需要转换成gdal可读的虚拟文件路径
        img = self.imagePath
        img2 = None
        print('img------------' + img)
        if ';' in self.imagePath:
            img = self.imagePath.split(';')[0]
            img2 = self.imagePath.split(';')[1]

        imageFilePrefix = img.split("/")[0]
        if imageFilePrefix == "s3:":
            img = img.replace("s3://", "")
            img = f"/vsis3/{img}"

        dataset = self.gdal.Open(img)
        if not dataset:
            print('not get image data from : ' + img)
        im_proj = dataset.GetProjection()  # 获取投影信息
        if im_proj:
            srs_ = osr.SpatialReference()
            srs_.SetWellKnownGeogCS('WGS84')
            dataset = self.gdal.AutoCreateWarpedVRT(dataset, None, srs_.ExportToWkt())  # , gdal.GRA_Bilinear)
        width = dataset.RasterXSize  # 获取数据宽度
        height = dataset.RasterYSize  # 获取数据高度
        data_band_count = dataset.RasterCount

        self.im_projection = im_proj
        self.dataset = dataset

        if img2:
            if img2.split("/")[0] == "s3:":
                img2 = img2.replace("s3://", "")
                img2 = f"/vsis3/{img2}"

            dataset2 = self.gdal.Open(img2)
            if not dataset2:
                print('not get image data from : ' + img2)
            im_proj2 = dataset2.GetProjection()  # 获取投影信息
            if im_proj2:
                srs_ = osr.SpatialReference()
                srs_.SetWellKnownGeogCS('WGS84')
                dataset2 = self.gdal.AutoCreateWarpedVRT(dataset, None, srs_.ExportToWkt())  # , gdal.GRA_Bilinear)

            width2 = dataset2.RasterXSize  # 获取数据宽度
            height2 = dataset2.RasterYSize  # 获取数据高度
            data_band_count2 = dataset2.RasterCount
            if height != height2 or width != width2 or data_band_count != data_band_count2:
                print('{} and {} size must equal !'.format(img, img2))
                exit(1)

            self.dataset2 = dataset2

    #  目标识别
    def pred_image_detection(self,outputPath,load_size,class_name,del_images,del_pred_result,value_title_map,name_title_map,nms=0.3):
        # 获取预测图片的相关数据
        width = self.dataset.RasterXSize
        height = self.dataset.RasterYSize
        outbandsize = self.dataset.RasterCount
        im_proj = self.dataset.GetProjection()  # 获取投影信息
        im_geotrans = self.dataset.GetGeoTransform()  # 获取仿射矩阵信息
        # 创建矢量文件用
        xoffset = im_geotrans[1]
        yoffset = im_geotrans[5]
        xbase = im_geotrans[0]
        ybase = im_geotrans[3]
        xscale = im_geotrans[2]
        yscale = im_geotrans[4]

        strcoordinates = "POLYGON ("
        # 创建输出文件
        ShpFileName = outputPath[:-4] + ".shp"
        # ------------------------------------设置投影信息---------------------------
        srs = osr.SpatialReference()
        srs.ImportFromWkt(self.dataset.GetProjectionRef())
        prjFile = open(ShpFileName[:-4] + ".prj", 'w')
        # 转为字符
        srs.MorphToESRI()
        prjFile.write(srs.ExportToWkt())
        prjFile.close()

        cut_size = int(load_size[0])
        bias = int(cut_size / 8)

        x_idx = range(0, width, cut_size - bias)
        y_idx = range(0, height, cut_size - bias)

        boxes_all = []
        strcoordinates_box = []

        total_progress = len(x_idx) * len(y_idx)
        count = 0
        process = "%.1f%%" % (0)
        print("[ROUTINE] [{process}]".format(process=process), flush=True)
        for x_start in x_idx:
            for y_start in y_idx:
                x_stop = x_start + cut_size
                if x_stop > width:
                    x_start = width - cut_size
                y_stop = y_start + cut_size
                if y_stop > height:
                    y_start = height - cut_size

                cut_width = cut_size
                cut_height = cut_size
                switch_flag = 0
                if x_start < 0 and y_start >= 0:
                    x_start = 0
                    x_stop = width
                    cut_width = width
                    switch_flag = 1
                elif x_start >= 0 and y_start < 0:
                    y_start = 0
                    y_stop = height
                    cut_height = height
                    switch_flag = 2
                elif x_start < 0 and y_start < 0:
                    x_start = 0
                    x_stop = width
                    cut_width = width
                    y_start = 0
                    y_stop = height
                    cut_height = height
                    switch_flag = 3

                croped_img = self.dataset.ReadAsArray(x_start, y_start, cut_width, cut_height)
                croped_img = croped_img.transpose(1, 2, 0)

                if switch_flag == 1:
                    temp = np.zeros((croped_img.shape[0], cut_size, croped_img.shape[2]), dtype=np.uint8)
                    temp[0:croped_img.shape[0], 0:croped_img.shape[1], :] = croped_img
                    croped_img = temp
                elif switch_flag == 2:
                    temp = np.zeros((cut_size, croped_img.shape[1], croped_img.shape[2]), dtype=np.uint8)
                    temp[0:croped_img.shape[0], 0:croped_img.shape[1], :] = croped_img
                    croped_img = temp
                elif switch_flag == 3:
                    temp = np.zeros((cut_size, cut_size, croped_img.shape[2]), dtype=np.uint8)
                    temp[0:croped_img.shape[0], 0:croped_img.shape[1], :] = croped_img
                    croped_img = temp

                photo = np.array(croped_img, dtype=np.float64)

                # 处理输入到模型中的数据
                images = del_images(photo)
                with torch.no_grad():
                    images = torch.from_numpy(images)
                    if self.cuda:
                        images = images.cuda()
                    outputs = self.model(images)

                patch_box = del_pred_result(outputs)

                # 还原到整张图的坐标位置
                for i,box in enumerate(patch_box):
                    out_boxes = get_region_boxes(box, x_start, y_start)
                    boxes_all.append(out_boxes)

                count += 1
                now_progress = int(100 * count / total_progress)
                process = "%.1f%%" % (now_progress)
                print("[ROUTINE] [{process}]".format(process=process), flush=True)

                del(images,outputs)

        out_boxes = py_cpu_nms(np.array(boxes_all), float(nms))

        if len(out_boxes) == 0:
            print('not pred ... ')
            exit(0)

        for k, out_box in enumerate(out_boxes):  # 对每个目标进行处理，按原始尺寸进行缩放
            classes = class_name[int(out_boxes[k][0])]
            classId = int(out_boxes[k][0])
            score = float(out_boxes[k][1])

            xmin = xbase + out_boxes[k][2] * xoffset + out_boxes[k][3] * xscale
            ymin = ybase + out_boxes[k][3] * yoffset + out_boxes[k][2] * yscale
            xmax = xbase + out_boxes[k][4] * xoffset + out_boxes[k][5] * xscale
            ymax = ybase + out_boxes[k][5] * yoffset + out_boxes[k][4] * xscale

            if not im_proj:
                ymin = -1 * ymin
                ymax = -1 * ymax

            strcoordinates = strcoordinates + '(%f1 %f2,%f3 %f4,%f5 %f6,%f7 %f8,%f9 %f10,%s,%f)' % (
                xmin, ymin, xmax, ymin, xmax, ymax, xmin, ymax, xmin, ymin, classes, score)
            strcoordinates = strcoordinates + ','
            str = (xmin, ymin, xmax, ymin, xmax, ymax, xmin, ymax, xmin, ymin, classId, classes, score)
            strcoordinates_box.append(str)

        statisticList = create_shp_detection(strcoordinates_box,strcoordinates,ShpFileName,value_title_map)
        self.statisticList = statisticList

        del self.dataset

        # shp装好为gepjson
        shp_to_geojson( ShpFileName, ShpFileName.replace('.shp', '.json'),name_title_map)


    def pred_image_seg_change(self,outputPath,load_size,del_images,del_pred_result,trainvalue_rgb,background_value=0):
        # 获取预测图片的相关数据
        width = self.dataset.RasterXSize
        height = self.dataset.RasterYSize
        outbandsize = self.dataset.RasterCount
        im_proj = self.dataset.GetProjection()  # 获取投影信息
        im_geotrans = self.dataset.GetGeoTransform()  # 获取仿射矩阵信息

        band_count = 3
        # 输出output
        format = "GTiff"
        tiff_driver = gdal.GetDriverByName(format)
        output_ds = tiff_driver.Create(outputPath, width, height, band_count, gdalconst.GDT_Byte)
        output_ds.SetGeoTransform(im_geotrans)
        output_ds.SetProjection(im_proj)
        for band_index in range(band_count):
            output_ds.GetRasterBand(band_index + 1).SetNoDataValue(background_value)

        # 单波段图片
        format = "GTiff"
        tiff_driver2 = gdal.GetDriverByName(format)
        output_ds_tmp = tiff_driver2.Create(basedir + '/pred_tmp.tif', width, height,
                                            1, gdalconst.GDT_Byte)
        if not im_proj:
            im_geotrans_ = (im_geotrans[0], im_geotrans[1], im_geotrans[2], im_geotrans[3], im_geotrans[4], -1.0)
            output_ds_tmp.SetGeoTransform(im_geotrans_)
        else:
            output_ds_tmp.SetGeoTransform(im_geotrans)

        output_ds_tmp.SetProjection(im_proj)
        output_ds_tmp.GetRasterBand(1).SetNoDataValue(background_value)

        width = self.dataset.RasterXSize  # 获取数据宽度
        height = self.dataset.RasterYSize  # 获取数据高度
        # 裁切大小，活动重叠的间隔
        cut_size = int(load_size[0])
        bias = int(cut_size / 4)

        # 滑动裁切
        block_size = int(cut_size / 2.0)
        overlap = int(cut_size / 4)
        block_xcount = int((width - 1) / block_size) + 1
        block_ycount = int((height - 1) / block_size) + 1

        for y_index in range(block_ycount):
            y_start = y_index * block_size
            y_end = y_start + block_size
            if y_index == block_ycount - 1:
                y_end = height
                y_start = y_end - block_size

            block_height = y_end - y_start

            y_overlap_start = y_start - overlap
            y_real_start = 0
            if y_overlap_start < 0:
                y_real_start = -1 * y_overlap_start
                y_overlap_start = 0

            y_overlap_end = y_end + overlap
            y_real_end = cut_size
            if y_overlap_end > height:
                y_real_end = cut_size - (y_overlap_end - height)
                y_overlap_end = height

            read_height = y_overlap_end - y_overlap_start

            for x_index in range(block_xcount):
                x_start = x_index * block_size
                x_end = x_start + block_size
                if x_index == block_xcount - 1:
                    x_end = width
                    x_start = x_end - block_size

                block_width = x_end - x_start

                x_overlap_start = x_start - overlap
                x_real_start = 0
                if x_overlap_start < 0:
                    x_real_start = -1 * x_overlap_start
                    x_overlap_start = 0

                x_overlap_end = x_end + overlap
                x_real_end = cut_size
                if x_overlap_end > width:
                    x_real_end = cut_size - (x_overlap_end - width)
                    x_overlap_end = width

                read_width = x_overlap_end - x_overlap_start

                read_img = self.dataset.ReadAsArray(x_overlap_start, y_overlap_start, read_width, read_height)
                read_img = read_img.transpose(1, 2, 0)
                # 预测前的数据处理
                img = del_images(read_img)

                if self.dataset2:
                    read_img2 = self.dataset2.ReadAsArray(x_overlap_start, y_overlap_start, read_width, read_height)
                    read_img2 = read_img2.transpose(1, 2, 0)
                    # 预测前的数据处理
                    img2 = del_images(read_img2)
                    # 模型预测
                    pre_img = self.model(img,img2)
                else:
                    # 模型预测
                    pre_img = self.model(img)

                # 模型预测结果处理
                pred = del_pred_result(pre_img)

                pred = pred[overlap:cut_size - overlap, overlap:cut_size - overlap]

                output_ds_tmp.GetRasterBand(1).WriteArray(pred, x_start, y_start)

                if len(trainvalue_rgb) > 0 :
                    pred = classToRGB(pred, trainvalue_rgb)
                    for band_index in range(3):
                        output_ds.GetRasterBand(band_index + 1).WriteArray(pred[:, :, band_index], x_start,
                                                                           y_start)
                else:
                    self.output_ds.GetRasterBand(1).WriteArray(pred, x_start, y_start)

                del (img, pre_img)

        del (output_ds_tmp, output_ds)

# 初始化gdal
def inint_gdal():
    # gdal读取数据
    s3Client = aiUtils.s3GetImg()
    gdal = s3Client.gdal

    ogr.RegisterAll()
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
    gdal.SetConfigOption("SHAPE_ENCODING", "CP936")
    return gdal

# 获取模型
def get_model(load_model):
    model = load_model()
    model = model.eval()
    return model

# 语义分割及变化检测的相关操作
def shp_tif_deal(outputFile,pred_utils,taskIdAndIndex,**platform_arguments):

    # 单波段tif转shp
    # 1: 语义分割  2：目标识别 3：变化检测
    if platform_arguments['network_type'] == 1 or platform_arguments['network_type'] == 3:
        # 生成金字塔
        generateOvrFile(outputFile)
        outputFile = outputFile[:-4] + ".shp"
        staticMap = raster2shp.vectorize(basedir + '/pred_tmp.tif', outputFile,
                              platform_arguments['value_name_map'], platform_arguments['value_title_map'],
                              platform_arguments['value_color'])
    elif platform_arguments['network_type'] == 2:
        # 统计类别个数
        outputFile = outputFile[:-4] + ".shp"
        staticMap = static_label(pred_utils.statisticList, platform_arguments['value_color'])
    else:
        print('输入类型有误！')
        exit(1)

    # shp转换投影 并存入数据库
    # 转换shp的投影
    shp_path = outputFile
    if not pred_utils.im_projection:
        out_path = basedir + '/tmp_prj.shp'
        shp2pg_utils.reproject(shp_path, out_path, 3857, 4326)
        shp_path = out_path

    # 语义分割的type 1,变化检测 type 2
    if platform_arguments['network_type'] == 1:
        shp2pg_utils.shp2pg_tosql_seg_change(shp_path, 1, cls2title=platform_arguments['name_title_map'],
                                      taskIdAndIndex=taskIdAndIndex,isZS=False)
    elif platform_arguments['network_type'] == 3:
        shp2pg_utils.shp2pg_tosql_seg_change(shp_path, 2, cls2title=platform_arguments['name_title_map'],
                                      taskIdAndIndex=taskIdAndIndex,isZS=False)
    else:
        shp2pg_utils.shp2pg_tosql_detect(shp_path, cls2title=platform_arguments['name_title_map'],
                                         taskIdAndIndex=taskIdAndIndex,isZS=False)

    return staticMap

# 预测
def prediction_image(**platform_arguments):
    # 用户编写的3个方法
    load_model = platform_arguments['load_model']
    deal_data_img = platform_arguments['deal_data_img']
    deal_pred_result = platform_arguments['deal_pred_result']
    network_type = platform_arguments['network_type']

    # 获取参数
    # platform_arguments = parse_platform_arguments()
    # 获取读取s3的gdal
    s3gdal = inint_gdal()
    # 加载模型
    model = get_model(load_model)

    # 获取预测图片列表
    inputList = platform_arguments['image_path'].split(',')

    # 记录日志
    log_new = {"zipOutFile": '/' + '/'.join(outputSaveDir.split('/')[2:]) + "result.zip", "total_output_size": "",
               "task_list": []}

    total_output_size = 0

    # 遍历图片，进行每张图片预测
    for index, imagePath in enumerate(inputList):
        process = float((index + 1) / len(inputList))
        log_new["process"] = process
        taskIdAndIndex = platform_arguments['estimate_id'] + ":" + str(index + 1)

        tmpfilename = os.path.basename(imagePath)
        filename, extension = os.path.splitext(tmpfilename)

        # 重命名，例如： 1_xxx_pred
        filename = str(index + 1) + "_" + filename + "_pred"

        # 输出
        outputFile = outputSaveDir + filename + ".tif"

        pred_utils = pred_prepare(model,s3gdal,imagePath)
        if network_type == 1 or network_type == 3:
            # 预测图片，生成三波段展示tif 及 临时单波段tif
            pred_utils.pred_image_seg_change(outputFile, platform_arguments['load_size'],deal_data_img,deal_pred_result,platform_arguments['value_color'],platform_arguments['background_value'])
            # 生成金字塔 及 转换为shp 并保存入数据库
            staticMap = shp_tif_deal(outputFile, pred_utils, taskIdAndIndex, **platform_arguments)
        elif network_type == 2:
            # 预测图片，生成 shp,并 生成geojson
            pred_utils.pred_image_detection(outputFile[:-4] + '.shp',platform_arguments['load_size'],platform_arguments['class_name_list'], deal_data_img,deal_pred_result,platform_arguments['value_title_map'],platform_arguments['name_title_map'],nms=0.3)

            # 存入数据库
            staticMap = shp_tif_deal(outputFile, pred_utils, taskIdAndIndex, **platform_arguments)
        else:
            print('输入类型有误！')
            exit(1)

        # 日志信息
        task_list_inner = {
            "task_result_id": taskIdAndIndex,
            "output_shp_static": staticMap,
            "output_size": "",
            "input": imagePath,
            "output": [],
        }
        # 记录日志信息
        create_log(task_list_inner,outputFile,total_output_size,log_new)
        print("[Process: {process}]".format(process=str(index + 1) + '/' + str(len(inputList))))

    # 矢量进行压缩
    create_zip()

def create_log(task_list_inner,outputFile,total_output_size,log_new):

    sizeInt = int(0)
    sizeStr = 0

    for key in fileKey:
        outFileName = None
        if os.path.exists(outputFile + key):
            outFileName = outputFile + key
        elif os.path.exists(outputFile[:-4] + key):
            outFileName = outputFile[:-4] + key
        else:
            continue
        if os.path.exists(outFileName):
            fileSize = os.stat(outFileName).st_size
            if fileSize > 0:
                sizeInt = sizeInt + int(fileSize)
                fileSize = bytes(fileSize)
                sizeStr = bytes(sizeInt)
            output_log = {"name": "", "size": ""}
            output_log["name"] = '/' + '/'.join(outFileName.split('/')[2:])
            output_log["size"] = fileSize
            task_list_inner["output"].append(output_log)

    total_output_size += sizeInt
    task_list_sizes = bytes(total_output_size)

    task_list_inner["output_size"] = sizeStr
    log_new['task_list'].append(task_list_inner)
    log_new['total_output_size'] = task_list_sizes
    trainlog = json.dumps(log_new, indent=4)
    with open(basedir + '/output/trainlog' + '.json', 'w', encoding='utf-8') as log_file:
        log_file.write(trainlog)

def create_zip():
    # 压缩矢量文件，生成矢量文件时，设置文件名_zip
    zf = zipfile.ZipFile(outputSaveDir + 'result.zip', "w", zipfile.zlib.DEFLATED)
    fileList = glob.glob(outputSaveDir + '*.*')
    for tar in fileList:
        fileAllName = os.path.basename(tar)
        if fileAllName[-4:] in shpFileKey:
            zf.write(tar, fileAllName)
    zf.close()
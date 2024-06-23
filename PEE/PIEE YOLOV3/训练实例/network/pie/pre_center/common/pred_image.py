'''
    预测
'''
import numpy as np
#  目标识别
from osgeo import gdalconst

from pie.pre_center.pytorch.pre_tools import estimate_img
from pie.utils import aiUtils
from pie.utils.registry import Registry
import pie.dataset.ehance
try:
    from osgeo import ogr
    from osgeo import osr
except ImportError:
    import ogr
    import osr

# 语义分割中间单波段名称
one_bands_file = 'pre_tem.tif'

# 初始化gdal
def init_gdal():
    # gdal读取数据
    s3Client = aiUtils.s3GetImg()
    gdal = s3Client.gdal

    ogr.RegisterAll()
    gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
    gdal.SetConfigOption("SHAPE_ENCODING", "CP936")
    return gdal


# 获取模型
def get_model(load_model, **kwargs):
    model = load_model(**kwargs)
    model = model.eval()
    return model


def read_img(s3gdal, imagePath):
    '''
    读取数据信息
    :param s3gdal:    读取s3数据的gdal
    :param imagePath:
    :return:
    '''
    # gdal读取图片
    # s3文件需要转换成gdal可读的虚拟文件路径
    img = imagePath
    img2 = None
    if ';' in imagePath:
        img = imagePath.split(';')[0]
        img2 = imagePath.split(';')[1]

    imageFilePrefix = img.split("/")[0]
    if imageFilePrefix == "s3:":
        img = img.replace("s3://", "")
        img = f"/vsis3/{img}"

    dataset = s3gdal.Open(img)
    if not dataset:
        print('not get image data from : ' + img)
    im_proj = dataset.GetProjection()  # 获取投影信息
    if im_proj:
        srs_ = osr.SpatialReference()
        srs_.SetWellKnownGeogCS('WGS84')
        dataset = s3gdal.AutoCreateWarpedVRT(dataset, None, srs_.ExportToWkt())  # , gdal.GRA_Bilinear)
    width = dataset.RasterXSize  # 获取数据宽度
    height = dataset.RasterYSize  # 获取数据高度
    data_band_count = dataset.RasterCount

    im_projection = im_proj
    dataset = dataset

    dataset2 = None
    if img2:
        if img2.split("/")[0] == "s3:":
            img2 = img2.replace("s3://", "")
            img2 = f"/vsis3/{img2}"

        dataset2 = s3gdal.Open(img2)
        if not dataset2:
            print('not get image data from : ' + img2)
        im_proj2 = dataset2.GetProjection()  # 获取投影信息
        if im_proj2:
            srs_ = osr.SpatialReference()
            srs_.SetWellKnownGeogCS('WGS84')
            dataset2 = s3gdal.AutoCreateWarpedVRT(dataset2, None, srs_.ExportToWkt())  # , gdal.GRA_Bilinear)

        width2 = dataset2.RasterXSize  # 获取数据宽度
        height2 = dataset2.RasterYSize  # 获取数据高度
        data_band_count2 = dataset2.RasterCount
        if height != height2 or width != width2 or data_band_count != data_band_count2:
            print('{} and {} size must equal !'.format(img, img2))
            exit(1)

        dataset2 = dataset2

    return dataset, dataset2


# 数据相关处理 （除旋转等操作外）
def data_transforms(img,img2,ehance):
    if ehance is not None:
        if ehance == None:
            ehance = [  # 流程， 由之前创建的 train_pipeline 传递进来。
                dict(name='randomShiftScaleRotate'),
                dict(name='randomHorizontalFlip'),
                dict(name='randomVerticleFlip'),
                dict(name='randomRotate90'),
                dict(name='Normalization',params=dict(region=[0,1]))]
        else:
            ehance = eval(ehance)

        fun_name_list = Registry.get_divfun('trans')
        if fun_name_list:
            for i in fun_name_list:
                ehancefun = Registry[i]
                try:
                    img, img2, _ = ehancefun(img, img2, None)
                except:
                    print(i, '出错！')

        Registry.get_divfun()
        if ehance:
            for i in ehance:
                param = i.get('params')
                # u = param.get('random')
                # if u == None:
                #     param['random'] = 0.5
                if i.get('name') == 'Normalization':
                    try:
                        ehancefun = Registry[i.get('name')]
                        img, img2, _ = ehancefun(img, img2, None, param)
                    except:
                        print(i.get('name'), '出错！')
        return img, img2


def pred_image_detection(model, dataset, shp_file, load_size_, class_name_, preprocess, postprocess, value_title_map_,
                         cuda,ehance=None,
                         nms_=0.3, **kwargs):
    '''
        预测目标识别
    :param model:  模型
    :param dataset:  数据
    :param shp_file: 预测生成的shp
    :param load_size: 裁切进行预测的图片大小
    :param class_name: 类别列表
    :param proprocess: 数据预处理
    :param postprocess: 数据后处理
    :param cuda:
    :param nms:
    :return:
    '''
    nms = nms_
    load_size = load_size_
    class_name = class_name_
    value_title_map = value_title_map_
    # 获取预测图片的相关数据
    width = dataset.RasterXSize
    height = dataset.RasterYSize
    outbandsize = dataset.RasterCount
    im_proj = dataset.GetProjection()  # 获取投影信息
    im_geotrans = dataset.GetGeoTransform()  # 获取仿射矩阵信息
    # 创建矢量文件用
    xoffset = im_geotrans[1]
    yoffset = im_geotrans[5]
    xbase = im_geotrans[0]
    ybase = im_geotrans[3]
    xscale = im_geotrans[2]
    yscale = im_geotrans[4]

    strcoordinates = "POLYGON ("
    # 创建输出文件
    # ------------------------------------设置投影信息---------------------------
    srs = osr.SpatialReference()
    srs.ImportFromWkt(dataset.GetProjectionRef())
    prjFile = open(shp_file[:-4] + ".prj", 'w')
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

            croped_img = dataset.ReadAsArray(x_start, y_start, cut_width, cut_height)
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

            # 模型预测图片
            patch_box = estimate_image(model, croped_img, None, ehance,preprocess, postprocess,**kwargs)

            # 处理输入到模型中的数据

            # photo = np.array(croped_img, dtype=np.float64)

            # 处理输入到模型中的数据
            # images = preprocess(photo, **kwargs)

            # with torch.no_grad():
            #     outputs = self.model(images)

            # patch_box = postprocess(outputs, **kwargs)

            # 还原到整张图的坐标位置
            for i, box in enumerate(patch_box):
                out_boxes = get_region_boxes(box, x_start, y_start)
                boxes_all.append(out_boxes)

            count += 1
            now_progress = int(100 * count / total_progress)
            process = "%.1f%%" % (now_progress)
            print("[ROUTINE] [{process}]".format(process=process), flush=True)

            # del (images, outputs)

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

    del dataset

    return strcoordinates_box


def pred_image_seg_change(model, dataset, dataset2, s3gdal, outputPath, load_size_, preprocess, postprocess,
                          trainvalue_rgb, background_value_=0, cuda=False, ehance=None, **kwargs):
    '''
        预测图像（语义分割及变化检测）
    :param model:     模型
    :param dataset:   数据1
    :param dataset2:  变化检测 数据2
    :param s3gdal:    读取s3数据的gdal
    :param outputPath: 输出路径
    :param load_size:  预测图片裁切大小
    :param del_images: 数据预处理方法
    :param del_pred_result: 数据后处理方法 要求输出为单波段数组
    :param trainvalue_rgb: 训练值与rgb对应map
    :param background_value: 背景值
    :param cuda:
    :return:
    '''
    load_size = load_size_
    background_value = background_value_
    # 获取预测图片的相关数据
    width = dataset.RasterXSize
    height = dataset.RasterYSize
    outbandsize = dataset.RasterCount
    im_proj = dataset.GetProjection()  # 获取投影信息
    im_geotrans = dataset.GetGeoTransform()  # 获取仿射矩阵信息

    band_count = 3
    # 输出output
    format = "GTiff"
    tiff_driver = s3gdal.GetDriverByName(format)
    output_ds = tiff_driver.Create(outputPath, width, height, band_count, gdalconst.GDT_Byte)
    output_ds.SetGeoTransform(im_geotrans)
    output_ds.SetProjection(im_proj)
    for band_index in range(band_count):
        output_ds.GetRasterBand(band_index + 1).SetNoDataValue(background_value)

    # 单波段图片
    output_root = '/'.join(outputPath.split('/')[:-2])
    format = "GTiff"
    tiff_driver2 = s3gdal.GetDriverByName(format)
    output_ds_tmp = tiff_driver2.Create(output_root + '/' + one_bands_file, width, height,
                                        1, gdalconst.GDT_Byte)
    if not im_proj:
        im_geotrans_ = (im_geotrans[0], im_geotrans[1], im_geotrans[2], im_geotrans[3], im_geotrans[4], -1.0)
        output_ds_tmp.SetGeoTransform(im_geotrans_)
    else:
        output_ds_tmp.SetGeoTransform(im_geotrans)

    output_ds_tmp.SetProjection(im_proj)
    output_ds_tmp.GetRasterBand(1).SetNoDataValue(background_value)

    width = dataset.RasterXSize  # 获取数据宽度
    height = dataset.RasterYSize  # 获取数据高度
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

            read_img = dataset.ReadAsArray(x_overlap_start, y_overlap_start, read_width, read_height)
            read_img = read_img.transpose(1, 2, 0)

            read_img2 = None
            if dataset2:
                read_img2 = dataset2.ReadAsArray(x_overlap_start, y_overlap_start, read_width, read_height)
                read_img2 = read_img2.transpose(1, 2, 0)

            # 模型预测图片
            pred = estimate_image(model, read_img, read_img2, ehance,preprocess, postprocess,**kwargs)

            # 数据处理（除数据增强相关处理外）
            # read_img,read_img2 = data_transforms(read_img,read_img2,ehance)
            # 预测前的数据处理
            # img = preprocess(read_img, **kwargs)

            # img2 = None
            # if dataset2:
            # 预测前的数据处理
            # img2 = preprocess(read_img2, **kwargs)
            # 模型预测
            # pre_img = model(img, img2)
            # else:
            # 模型预测
            # pre_img = model(img)

            # 模型预测结果处理
            # pred = postprocess(pre_img, **kwargs)

            pred = pred[overlap:cut_size - overlap, overlap:cut_size - overlap]

            output_ds_tmp.GetRasterBand(1).WriteArray(pred, x_start, y_start)

            if len(trainvalue_rgb) > 0:
                print(np.unique(pred))
                pred = classToRGB(pred, trainvalue_rgb)
                for band_index in range(3):
                    output_ds.GetRasterBand(band_index + 1).WriteArray(pred[:, :, band_index], x_start,
                                                                       y_start)
            else:
                output_ds.GetRasterBand(1).WriteArray(pred, x_start, y_start)

            # del (img, pre_img)

    del (output_ds_tmp, output_ds)


def estimate_image(model,read_img,read_img2,ehance,del_images,del_pred_result,**kwargs):
    # 预测前的数据处理
    # print(ehance)
    read_img,read_img2 = data_transforms(read_img,read_img2,ehance)
    img = del_images(read_img,**kwargs)

    if read_img2 is not None:
        # 预测前的数据处理
        img2 = del_images(read_img2,**kwargs)
        # 模型预测
        pre_img = model(img, img2)
    else:
        # 模型预测
        pre_img = model(img)

    # 模型预测结果处理
    pred = del_pred_result(pre_img,**kwargs)

    return pred

# 转换为3波段的tif
def classToRGB(mask, trainvalue_rgb):
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
        if 'rgb(' in trainvalue_rgb[train_value]:
            rgb = ast.literal_eval(trainvalue_rgb[train_value][3:])
        else:
            rgb = train_value
        indices = np.where(mask == train_value)
        colmap[indices[0].tolist(),
        indices[1].tolist(), :] = np.array(rgb)
    return colmap


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
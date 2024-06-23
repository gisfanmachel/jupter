'''
    模型预测评估相关工具方法
    王拓
    2021.11.30
'''
import glob
import json
import os
import sys
import zipfile

try:
    from osgeo import gdal
    from osgeo import ogr
except ImportError:
    import gdal
    import ogr

from pie.pre_center.common import raster2shp

# 写入trainlog.json中output的后缀集合
fileKey = ['.tif', '.json', '.cpg', '.dbf', '.prj', '.shx', '.shp', '.ovr']
# 压缩包添加矢量后缀
shpFileKey = ['.cpg', '.dbf', '.prj', '.shx', '.shp']
# 数据是否保存到正式数据库
isZS = False

# 导入工具
basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(basedir + '/so/torch')
import shp2pg_utils


# -------------------- 公共 -----------------

def bytes(bytes):
    '''
    字节统计
    Args:
        bytes: 字节个数

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


def save_log(json_file,log_info_dict, total_output_size, output_file, log_new, index_, indexs):
    '''
    生成日志
    :param json_file :  '/output/trainlog' + '.json'
    :param log_info_dict: 日志信息
        {
            "task_result_id": taskIdAndIndex,
            "output_shp_static": staticMap,
            "output_size": "",
            "input": imagePath,
            "output": [],
        }
    :param total_output_size: 全部输出文件字节大小
    :param output_file: 输出的路径，到文件tif上级目录
    :param log_new: 输入的日志信息
    :param index_: 当前图片索引号
    :param indexs: 预测图片个数
    :return:
    '''
    sizeInt = int(0)
    sizeStr = 0

    for key in fileKey:
        outFileName = None
        if os.path.exists(output_file + key):
            outFileName = output_file + key
        elif os.path.exists(output_file[:-4] + key):
            outFileName = output_file[:-4] + key
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
            log_info_dict["output"].append(output_log)

    total_output_size += sizeInt
    task_list_sizes = bytes(total_output_size)

    log_info_dict["output_size"] = sizeStr
    log_new['task_list'].append(log_info_dict)
    log_new['total_output_size'] = task_list_sizes
    trainlog = json.dumps(log_new, indent=4)
    with open(json_file, 'w', encoding='utf-8') as log_file:
        log_file.write(trainlog)
    print("[Process: {process}]".format(process=str(index_ + 1) + '/' + str(indexs)))


def create_zip(outputSaveDir):
    # 压缩矢量文件，生成矢量文件时，设置文件名_zip
    zf = zipfile.ZipFile(outputSaveDir + '/result.zip', "w", zipfile.zlib.DEFLATED)
    fileList = glob.glob(outputSaveDir + '/*.*')
    for tar in fileList:
        fileAllName = os.path.basename(tar)
        if fileAllName[-4:] in shpFileKey:
            zf.write(tar, fileAllName)
    zf.close()


# -------------- 像素级别 ------------------


# 生成金字塔
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


def reload_project(shp_path, out_path, prj=3657, new_prj=4326):
    '''
    投影转换
    :param shp_path: 原始shp文件
    :param out_path: 转换后生成的文件
    :param prj: 原投影
    :param new_prj: 转换投影
    :return:
    '''
    shp2pg_utils.reproject(shp_path, out_path, prj, new_prj)


def insert_pg(network_type, shp_path, cls2title, taskIdAndIndex, im_projection):
    '''
    shp文件保存到数据库中
    :param network_type:
    :param shp_path:
    :param cls2title:
    :param taskIdAndIndex:
    :return:
    '''
    # 语义分割的type 1,目标识别2，变化检测 type 3

    # shp转换投影 并存入数据库
    # 转换shp的投影
    if not im_projection:
        out_path = basedir + '/tmp_prj.shp'
        shp2pg_utils.reproject(shp_path, out_path, 3857, 4326)
        shp_path = out_path
    try:
        if network_type == 1:
            shp2pg_utils.shp2pg_tosql_seg_change(shp_path, 1, cls2title=cls2title,
                                                 taskIdAndIndex=taskIdAndIndex, isZS=isZS)
        elif network_type == 3:
            shp2pg_utils.shp2pg_tosql_seg_change(shp_path, 2, cls2title=cls2title,
                                                 taskIdAndIndex=taskIdAndIndex, isZS=isZS)
        else:
            shp2pg_utils.shp2pg_tosql_detect(shp_path, cls2title=cls2title,
                                             taskIdAndIndex=taskIdAndIndex, isZS=isZS)
    except:
        print("save shp file is error !")


def raster_shp(tif_path, output_file, value_name_map, value_title_map, value_color):
    '''
    将单波段tif 转换为shp
    :param tif_path:
    :param output_file:
    :param value_name_map:
    :param value_title_map:
    :param value_color:
    :return: 统计信息
    '''
    staticMap = raster2shp.vectorize(tif_path, output_file,
                                     value_name_map, value_title_map, value_color)

    return staticMap


# ---------------------- 目标识别 ------------------------

def shp_to_geojson(shpFile, jsonPath, clsname_clstitle_map):
    '''
    矢量转geojson
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

    del (out_ds, shp_ds)
    del (out_feat, out_lyr)
    print("convert to geojson Success........")


def static_label(statisticList, class_color):
    '''
    目标识别统计
    :param statisticList:
    :param class_color:
    :return:
    '''
    if not statisticList or len(statisticList) == 0:
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


def create_shp_detection(strcoordinates_box, shp_file, value_title_map):
    '''
    通过目标框生成shp
    :param strcoordinates_box: 目标框box
    :param shp_file:      shp路径及名称
    :param value_title_map: classid对应的类别中文名称
    :return:
    '''
    n = len(strcoordinates_box)
    print('rect number:', n)

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
    oDS = oDriver.CreateDataSource(shp_file)
    if oDS == None:
        print("创建文件【%s】失败！", shp_file)
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

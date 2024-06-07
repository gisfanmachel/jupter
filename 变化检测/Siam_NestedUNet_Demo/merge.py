
import numpy as np
import cv2
import os
from os import path
from osgeo import gdal, ogr, osr


# 影像裁剪到256*256
def merge_image(img_read_dir, save_path_tif, save_path_shp,logger):
    # 获取原始影像的信息
    img_before = gdal.Open(img_read_dir)
    img_before_np = img_before.ReadAsArray()

    # 获取裁剪行列数
    m, n = img_before_np.shape[1], img_before_np.shape[2]

    a1 = (m // 256) + 1
    b1 = (n // 256) + 1

    # 合并
    pre_read_dir = './output_img'

    img_change = np.zeros((a1 * 256, b1 * 256), dtype=np.uint8)
    # Y方向
    for i in range(a1):
        # X方向
        for j in range(b1):
            #  b1是裁剪的列数，b1 * i + j 表示第几个裁剪的图片提取的变化二值图（将所有裁剪图片拉平）
            path1 = path.join(pre_read_dir, 'Test_' + str(b1 * i + j) + '.png')
            pre = cv2.imread(path1, 1)
            # pre[:, :, 0] // 255 二值图 pre 为0,256，对255求余后 值为 0,1
            img_change[i * 256:(i + 1) * 256, j * 256:(j + 1) * 256] = pre[:, :, 0] // 255

    # 存储tif影像
    # 因为填充的图和原图，在原点位置不变，所以空间位置没有发生改变，只是在最右边和最下面填充了黑色的条，变化结果为无变化
    Driver = gdal.GetDriverByName('GTiff')
    out_img = Driver.Create(save_path_tif, b1 * 256, a1 * 256, 1, gdal.GDT_Byte)
    out_img.SetProjection(img_before.GetProjection())  # 投影信息
    out_img.SetGeoTransform(img_before.GetGeoTransform())  # 仿射信息
    out_img.GetRasterBand(1).WriteArray(img_change)  # 写入数值

    logger.info("tif保存")

    # 存储为shp
    layer_name = os.path.basename(save_path_shp)
    layer_name2 = layer_name.split(".shp")[0]

    prj = osr.SpatialReference()
    prj.ImportFromWkt(img_before.GetProjection())  # 读取栅格数据的投影信息，用来为后面生成的矢量做准备

    drv = ogr.GetDriverByName("ESRI Shapefile")
    Polygon = drv.CreateDataSource(save_path_shp)  # 创建一个目标文件

    Poly_layer = Polygon.CreateLayer(layer_name2, srs=prj, geom_type=ogr.wkbMultiPolygon)  # 对shp文件创建一个图层，定义为多个面类
    newField = ogr.FieldDefn('value', ogr.OFTInteger)  # 给目标shp文件添加一个字段，用来存储原始栅格的pixel value
    Poly_layer.CreateField(newField)
    gdal.Polygonize(out_img.GetRasterBand(1), None, Poly_layer, 0)  # 核心函数，执行的就是栅格转矢量操作

    Polygon.SyncToDisk()

    out_img.FlushCache()
    del out_img

    logger.info("shp保存")

    # 去除属性为0的要素，黑色背景的（包含没有变化的黑色，以及最开始填充的边缘黑色）
    Poly_layer.SetAttributeFilter("value = '" + str(0) + "'")
    for pFeature in Poly_layer:
        pFeatureFID = pFeature.GetFID()
        Poly_layer.DeleteFeature(int(pFeatureFID))
    strSQL = "REPACK " + str(Poly_layer.GetName())
    Polygon.ExecuteSQL(strSQL, None, "")
    Polygon.SyncToDisk()

    logger.info("shp过滤处理")




'''
    智能评估使用工具
    12211208 wangtuo
'''
import numpy as np
import cv2
import os

try:
    from osgeo import gdal,ogr
except ImportError:
    import gdal,ogr

#数据格式转化
def normalization(data):
    _range = np.max(data) - np.min(data)
    return (data - np.min(data)) / _range

def imgto8bit(img):
    img_nrm = normalization(img)
    img_8 = np.uint8(255 * img_nrm)
    return img_8

def tif_jpg(rasterfile,jpg_file):
    '''
        tif 数组转换为
    :param rasterfile:
    :return:
    '''
    in_ds = gdal.Open(rasterfile)  # 打开样本文件
    xsize = in_ds.RasterXSize  # 获取行列数
    ysize = in_ds.RasterYSize
    bands = in_ds.RasterCount
    B_band = in_ds.GetRasterBand(1)
    B= B_band.ReadAsArray(0, 0, xsize, ysize).astype(np.int16)
    G_band = in_ds.GetRasterBand(2)
    G = G_band.ReadAsArray(0, 0, xsize, ysize).astype(np.int16)
    R_band = in_ds.GetRasterBand(3)
    R = R_band.ReadAsArray(0, 0, xsize, ysize).astype(np.int16)
    R1 = imgto8bit(R)
    G1 = imgto8bit(G)
    B1 = imgto8bit(B)
    data2 = cv2.merge([R1,G1,B1])

    cv2.imencode('.jpg', data2)[1].tofile(jpg_file)
    return data2



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

    del(out_ds,shp_ds)
    del(out_feat,out_lyr)
    print("convert to geojson Success........")

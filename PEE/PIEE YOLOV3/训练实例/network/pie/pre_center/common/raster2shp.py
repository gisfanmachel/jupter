from functools import partial
from collections import defaultdict
import multiprocessing as mp

import numpy as np
import rasterio as rio
from rasterio import features
import shapely
from shapely import geometry, ops
import geopandas as gpd
import cv2
import math

from skimage import morphology
from skimage.morphology import remove_small_holes, remove_small_objects, disk


# from regulization import coarse_adjustment, buffer

# def preprocess(img, min_hole=300, min_object=300):
#     dtype = img.dtype
#     assert dtype == np.uint8
#     class_ids = np.unique(img)[1:]  # exclude zero value

#     img_copy = img.copy()
#     for class_id in class_ids:
#         tmp_img = img == class_id
#         morphology.binary_opening(tmp_img, selem=disk(7), out=tmp_img)
#         remove_small_objects(tmp_img, min_object, in_place=True)
#         remove_small_holes(tmp_img, min_hole, in_place=True)
#         img_copy[tmp_img] = class_id

#     return img_copy.astype(dtype)


def find_contours(image, bkg_value=0):
    assert image.dtype == np.uint8
    # Tuple(GeoJSON, value)
    shapes = features.shapes(image, mask=image != bkg_value)
    results = [(int(v), geometry.shape(s)) for s, v in shapes]

    return results


def simplify(shapes):
    """Using DP algorithm to simplify polygon.
    """
    ret_shapes = []
    for class_id, geom in shapes:
        # tol = 0.5 if geom.area < 10 else 2.0
        tol = 0.5
        geom = geom.simplify(tol, preserve_topology=True)

        ret_shapes.append((class_id, geom))

    return ret_shapes


def polygonize(image, bkg_value, min_hole, min_object):
    """

    Return:
        List[tuple(dict, int)]: {GeoJSON format shapes: raster value}
    """
    # image = preprocess(image, min_hole, min_object)
    shapes = find_contours(image, bkg_value)
    shapes = simplify(shapes)

    return shapes


def tsf_coords(coords, tsf):
    ret = []
    for poly_coords in coords:
        cur = []
        for coord in poly_coords:
            cur.append(tsf * coord)
        ret.append(np.array(cur))

    return ret


def get_window_info(rfile, win_size=1000):
    window_list = []
    with rio.open(rfile) as src:
        height = src.height
        width = src.width
        for i in range(0, height, win_size - 3):
            if i + win_size < height:
                ysize = win_size
            else:
                ysize = height - i

            for j in range(0, width, win_size - 3):
                if j + win_size < width:
                    xsize = win_size
                else:
                    xsize = width - j

                window = rio.windows.Window(j, i, xsize, ysize)
                window_list.append(window)

    return window_list, src.crs, src.transform


def to_shapely(affine):
    """Return an affine transformation matrix compatible with shapely.

    (a,b,d,e,xoff,yoff)
    """

    return (affine.a, affine.b, affine.d, affine.e, affine.xoff, affine.yoff)


def extract_shapes(raster_file, window, bkg_value):
    results = []
    with rio.open(raster_file) as src:
        tsf = src.transform
        tsf = to_shapely(tsf)

        img_patch = src.read(1, window=window)
        x, y = window.col_off, window.row_off
        offset = np.array([x, y])
        shapes = polygonize(img_patch, bkg_value, 300, 300)
        for i, (class_id, geom) in enumerate(shapes, start=1):
            ext_coords = np.array(geom.exterior.coords) + offset
            int_coords = []
            if geom.interiors:
                for c in geom.interiors:
                    int_coords.append(np.array(c) + offset)
            geom = geometry.Polygon(ext_coords, int_coords)
            # geom = shapely.affinity.affine_transform(geom, tsf)

            results.append((class_id, geom))

    results = merge(results)

    return results


def merge(results):
    d = defaultdict(list)
    for v, geom in results:
        d[v].append(geom)

    ret = []
    for k, geoms in d.items():
        ret.append((k, ops.cascaded_union(geoms)))

    return ret


def explode(results):
    gdf = gpd.GeoDataFrame([{
        'class_id': v,
        'geometry': geom
    } for v, geom in results])
    geoms = gdf.explode()

    results = [(class_id, geom) for i, (class_id, geom) in geoms.iterrows()]
    return results


import pandas


def to_file(results, filename, tsf, crs, class_map,valueTitile,rgbValue, driver='ESRI Shapefile'):
    # df = gpd.GeoDataFrame([{
    #     'class_id':
    #     v,
    #     'class_name':
    #     class_map[v],
    #     'geometry':
    #     shapely.affinity.affine_transform(geom, tsf)
    # } for v, geom in results])

    unit = None

    if crs:
        unit = 'm²'
    df = gpd.GeoDataFrame([{
        'class_id': v,
        'area': geom.area,
        'unit': unit,
        'FieldName': class_map[v],
        'geometry':
            shapely.affinity.affine_transform(geom, tsf)
    } for v, geom in results])

    if crs:
        # df['area'] = round(math.fabs(df['area'] / 2) * 9101160000.085981, 2)
        # print(df['area'])
        # df['area'] = df['area'].apply(lambda x: round(math.fabs(x / 2) * 9101160000.085981, 2))
        df['area'] = df['area'].apply(lambda x: round(x, 2))
        # print(df['area'])
        df.crs = crs.to_dict()

    # 统计
    static_data = []

    clsId_count = df['class_id'].value_counts().to_dict()
    # print(clsId_count)
    clsId_area_pd = df.groupby(by=['class_id'], as_index=False)['area'].sum()

    clsId_area_dic = clsId_area_pd.set_index('class_id')['area'].to_dict()
    # print(clsId_area_dic)
    for clsId in clsId_count:
        classDic = {}
        classDic['classTitle'] = valueTitile[clsId]
        classDic['count'] = clsId_count[clsId]
        classDic['area'] = clsId_area_dic[clsId]
        classDic['unit'] = unit
        classDic['color'] = rgbValue[clsId]
        static_data.append(classDic)

    # exit(1)
    df.to_file(filename, driver=driver, encoding='utf-8')
    return static_data


def vectorize(rfile, shpfile, class_id_map=None,valueTitile=None,rgbValue=None, bkg_value=0):
    window_list, crs, tsf = get_window_info(rfile, win_size=1000)

    results = []
    for win in window_list:
        res = extract_shapes(rfile, win, bkg_value)
        results.extend(res)

    if len(results) == 0:
        print('not estimate ...')
        exit(0)
    results = merge(results)
    results = explode(results)

    static_data = to_file(results, shpfile, to_shapely(tsf), crs, class_id_map,valueTitile,rgbValue)
    return static_data

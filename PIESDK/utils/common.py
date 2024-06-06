# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   common.py
@Time    :   2020/8/4 下午3:20
@Author  :   lsw
@Version :   1.0
@Contact :   shi_weihappy@126.com
@License :   (C)Copyright 2019-2020, lsw
@Desc    :   公共方法
"""
import subprocess
import datetime
import os
import tarfile
import string
import random
import zipfile
import urllib.request
from urllib.parse import unquote, quote
import uuid
import math
import numpy as np
import glob
import matplotlib.pyplot as plt
import json
import pyproj
import warnings
warnings.filterwarnings("ignore")

def encodeURIComponent(content, encoding="utf-8"):
    """
    编码
    :param content:
    :param encoding:
    :return:
    """
    new_content = str(content).encode(encoding)
    return quote(new_content)


def decodeURIComponent(content, encoding="utf-8"):
    """
    解码
    :param content:
    :param encoding:
    :return:
    """
    return unquote(content, encoding=encoding)


def encodeJSON(json_data):
    """
    json对象变为字符串
    :param json_data:
    :return:
    """
    if not json_data:
        return ""
    return json.dumps(json_data)


def decodeJSON(data):
    """
    字符串解析为json对象
    :param data:
    :return:
    """
    if not data:
        return {}
    return json.loads(data)


def uuid1():
    """
    生成uuid
    """
    return ''.join([each for each in str(uuid.uuid1()).split('-')])


def download_from_url(url, out_file_name=None, out_dir='.', unzip=True):
    """
    Download file form the url.
    """
    in_file_name = os.path.basename(url)
    if out_file_name is None:
        out_file_name = in_file_name
    out_file_path = os.path.join(os.path.abspath(out_dir), out_file_name)

    print("DownLoading {}...".format(url))
    try:
        urllib.request.urlretrieve(url, out_file_name)
    except:
        print("The url is invalid, Please check the url.")
        return

    final_path = out_file_path

    if unzip:
        if '.zip' in out_file_name:
            print("Unzipping {}...".format(out_file_name))
            with zipfile.ZipFile(out_file_path, "r") as zip_ref:
                zip_ref.extractall(out_dir)
            final_path = os.path.join(os.path.abspath(out_dir), out_file_name.replace('.zip', ''))
        if '.tar' in out_file_name:
            print("Unzipping {}...".format(out_file_name))
            with tarfile.open(out_file_path, "r", encoding="UTF-8") as tar_ref:
                tar_ref.extractall(out_dir)
            final_path = os.path.join(os.path.abspath(out_dir), out_file_name.replace('.tar', ''))
    print("Download successfully to: {}".format(final_path))


def random_string(string_length=3):
    """
    随机生成指定长度的字符串
    @param string_length
    @renturn:
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


def random_color(randomNumber: tuple):
    """
    生成随机颜色
    @param randomNumber:
    @return:
    """
    digit = list(map(str, range(10))) + list("ABCDEF")
    if isinstance(randomNumber, tuple):
        fir = '#'
        for i in randomNumber:
            a1 = i // 16
            a2 = i % 16
            fir += digit[a1] + digit[a2]
        return fir
    elif isinstance(randomNumber, str):
        a1 = digit.index(randomNumber[1]) * 16 + digit.index(randomNumber[2])
        a2 = digit.index(randomNumber[3]) * 16 + digit.index(randomNumber[4])
        a3 = digit.index(randomNumber[5]) * 16 + digit.index(randomNumber[6])
        return [a1, a2, a3]
    else:
        return None


def check_package(package, import_name=None):
    """
    监测包是否安装
    @param package:
    @param import_name:
    @return:
    """
    try:
        if import_name is not None:
            __import__(import_name)
        else:
            __import__(package)
    except ImportError:
        print("{} 包没有安装，现在开始安装 ".format(package))
        try:
            subprocess.check_call(["pip3", "install", package, "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"])
        except Exception as e:
            print("安装 {} 包失败".format(package))
            print(e)
        print("成功安装 {}".format(package))


def render_size(fileSize):
    if not fileSize:
        return "0 Bytes"
    unitArr = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
    _size = float(fileSize)
    index = math.floor(math.log(_size) / math.log(1024))
    size = _size / math.pow(1024, index)
    return "{:.2f} {}".format(size, unitArr[index])


def rgb_to_hex(rgb=(255, 255, 255)):
    """Converts RGB to hex color. In RGB color R stands for Red, G stands for Green, and B stands for Blue, and it ranges from the decimal value of 0 – 255.

    Args:
        rgb (tuple, optional): RGB color code as a tuple of (red, green, blue). Defaults to (255, 255, 255).

    Returns:
        str: hex color code
    """
    return "%02x%02x%02x" % rgb


def planet_monthly(api_key=None, token_name="PLANET_API_KEY"):
    """Generates Planet monthly imagery URLs based on an API key. To get a Planet API key, see https://developers.planet.com/quickstart/apis/

    Args:
        api_key (str, optional): The Planet API key. Defaults to None.
        token_name (str, optional): The environment variable name of the API key. Defaults to "PLANET_API_KEY".

    Raises:
        ValueError: If the API key could not be found.

    Returns:
        list: A list of tile URLs.
    """
    # from datetime import date

    if api_key is None:
        api_key = os.environ.get(token_name)
        if api_key is None:
            raise ValueError("The Planet API Key must be provided.")

    today = datetime.date.today()
    year_now = int(today.strftime("%Y"))
    month_now = int(today.strftime("%m"))

    link = []
    prefix = "https://tiles.planet.com/basemaps/v1/planet-tiles/global_monthly_"
    subfix = "_mosaic/gmap/{z}/{x}/{y}.png?api_key="

    for year in range(2016, year_now + 1):

        for month in range(1, 13):
            m_str = str(year) + "_" + str(month).zfill(2)

            if year == year_now and month >= month_now:
                break

            url = f"{prefix}{m_str}{subfix}{api_key}"
            link.append(url)

    return link


def planet_quarterly(api_key=None, token_name="PLANET_API_KEY"):
    """Generates Planet quarterly imagery URLs based on an API key. To get a Planet API key, see https://developers.planet.com/quickstart/apis/

    Args:
        api_key (str, optional): The Planet API key. Defaults to None.
        token_name (str, optional): The environment variable name of the API key. Defaults to "PLANET_API_KEY".

    Raises:
        ValueError: If the API key could not be found.

    Returns:
        list: A list of tile URLs.
    """
    # from datetime import date

    if api_key is None:
        api_key = os.environ.get(token_name)
        if api_key is None:
            raise ValueError("The Planet API Key must be provided.")

    today = datetime.date.today()
    year_now = int(today.strftime("%Y"))
    month_now = int(today.strftime("%m"))
    quarter_now = (month_now - 1) // 3 + 1

    link = []
    prefix = "https://tiles.planet.com/basemaps/v1/planet-tiles/global_quarterly_"
    subfix = "_mosaic/gmap/{z}/{x}/{y}.png?api_key="

    for year in range(2016, year_now + 1):

        for quarter in range(1, 5):
            m_str = str(year) + "q" + str(quarter)

            if year == year_now and quarter >= quarter_now:
                break

            url = f"{prefix}{m_str}{subfix}{api_key}"
            link.append(url)

    return link


def planet_quarterly_tiles(
        api_key=None, token_name="PLANET_API_KEY", tile_format="ipyleaflet"
):
    """Generates Planet  quarterly imagery TileLayer based on an API key. To get a Planet API key, see https://developers.planet.com/quickstart/apis/

    Args:
        api_key (str, optional): The Planet API key. Defaults to None.
        token_name (str, optional): The environment variable name of the API key. Defaults to "PLANET_API_KEY".
        tile_format (str, optional): The TileLayer format, can be either ipyleaflet or folium. Defaults to "ipyleaflet".

    Raises:
        ValueError: If the tile layer format is invalid.

    Returns:
        dict: A dictionary of TileLayer.
    """
    import folium
    import ipyleaflet

    if tile_format not in ["ipyleaflet", "folium"]:
        raise ValueError("The tile format must be either ipyleaflet or folium.")

    tiles = {}
    links = planet_quarterly(api_key, token_name)

    for url in links:
        index = url.find("20")
        name = "Planet_" + url[index: index + 6]

        if tile_format == "ipyleaflet":
            tile = ipyleaflet.TileLayer(url=url, attribution="Planet", name=name)
        else:
            tile = folium.TileLayer(
                tiles=url,
                attr="Planet",
                name=name,
                overlay=True,
                control=True,
            )

        tiles[name] = tile

    return tiles


def planet_monthly_tiles(
        api_key=None, token_name="PLANET_API_KEY", tile_format="ipyleaflet"
):
    """Generates Planet  monthly imagery TileLayer based on an API key. To get a Planet API key, see https://developers.planet.com/quickstart/apis/

    Args:
        api_key (str, optional): The Planet API key. Defaults to None.
        token_name (str, optional): The environment variable name of the API key. Defaults to "PLANET_API_KEY".
        tile_format (str, optional): The TileLayer format, can be either ipyleaflet or folium. Defaults to "ipyleaflet".

    Raises:
        ValueError: If the tile layer format is invalid.

    Returns:
        dict: A dictionary of TileLayer.
    """
    import folium
    import ipyleaflet

    if tile_format not in ["ipyleaflet", "folium"]:
        raise ValueError("The tile format must be either ipyleaflet or folium.")

    tiles = {}
    link = planet_monthly(api_key, token_name)

    for url in link:
        index = url.find("20")
        name = "Planet_" + url[index: index + 7]

        if tile_format == "ipyleaflet":
            tile = ipyleaflet.TileLayer(url=url, attribution="Planet", name=name)
        else:
            tile = folium.TileLayer(
                tiles=url,
                attr="Planet",
                name=name,
                overlay=True,
                control=True,
            )

        tiles[name] = tile

    return tiles


def get_wms_layers(url):
    """Returns a list of WMS layers from a WMS service.

    Args:
        url (str): The URL of the WMS service.

    Returns:
        list: A list of WMS layers.
    """
    try:
        from owslib.wms import WebMapService
    except ImportError:
        raise ImportError("Please install owslib using 'pip install owslib'.")

    wms = WebMapService(url)
    layers = list(wms.contents)
    layers.sort()
    return layers


def planet_tiles(api_key=None, token_name="PLANET_API_KEY", tile_format="ipyleaflet"):
    """Generates Planet imagery TileLayer based on an API key. To get a Planet API key, see https://developers.planet.com/quickstart/apis/

    Args:
        api_key (str, optional): The Planet API key. Defaults to None.
        token_name (str, optional): The environment variable name of the API key. Defaults to "PLANET_API_KEY".
        tile_format (str, optional): The TileLayer format, can be either ipyleaflet or folium. Defaults to "ipyleaflet".

    Raises:
        ValueError: If the tile layer format is invalid.

    Returns:
        dict: A dictionary of TileLayer.
    """

    catalog = {}
    quarterly = planet_quarterly_tiles(api_key, token_name, tile_format)
    monthly = planet_monthly_tiles(api_key, token_name, tile_format)

    for key in quarterly:
        catalog[key] = quarterly[key]

    for key in monthly:
        catalog[key] = monthly[key]

    return catalog


def search_pie_data(keywords, regex=False, keys=None):
    """Searches Earth Engine data catalog.

    Args:
        keywords (str | list): Keywords to search for can be id, provider, tag and so on. Split by space if string, e.g. "1 2" becomes ['1','2'].
        regex (bool, optional): Allow searching for regular expressions. Defaults to false.
        keys (list, optional): List of metadata fields to search from.  Defaults to ['id','provider','tags','title']
    Returns:
        list: Returns a list of assets.
    """
    if keys is None:
        keys = ["id", "source", "labels", "title"]

    if isinstance(keywords, str):
        keywords = keywords.split(" ")

    import re
    from functools import reduce
    from pie.utils.pieHttp import GET
    from pie.utils.config import Config

    def search_collection(pattern, dict_):
        if regex:
            if any(re.match(pattern, dict_[key]) for key in keys):
                return dict_
        elif any(pattern in dict_[key] for key in keys):
            return dict_
        return {}

    def search_all(pattern):
        # updated daily
        config = Config()
        urlInfo = config.getFuzzyQuery()
        response = GET(urlInfo=urlInfo)
        datasets = response["data"]
        matches = []
        matches += [search_collection(pattern, x) for x in datasets]
        matches = [x for x in matches if x]
        return matches

    try:
        assets = list(
            {json.dumps(match) for match in search_all(pattern=k)} for k in keywords
        )
        assets = sorted(list(reduce(set.intersection, assets)))
        assets = [json.loads(x) for x in assets]

        results = []
        for asset in assets:
            asset_dates = (
                    asset.get("start_date", "Unknown")
                    + " - "
                    + asset.get("end_date", "Unknown")
            )
            asset_id = asset["id"]

            asset["dates"] = asset_dates
            asset["id"] = asset_id
            asset["uid"] = asset_id.replace("/", "_")

            results.append(asset)

        return results

    except Exception as e:
        print(e)


def pie_data_html(asset):
    """Generates HTML from an asset to be used in the HTML widget.

    Args:
        asset (dict): A dictionary containing an Earth Engine asset.

    Returns:
        str: A string containing HTML.
    """
    try:
        asset_title = asset.get("title", "Unknown")
        asset_dates = asset.get("dates", "Unknown")
        pie_id_snippet = asset.get("id", "Unknown")
        template = f"""
            <html>
            <body>
                <h3>{asset_title}</h3>
                <h4>Dataset Availability</h4>
                    <p style="margin-left: 40px">{asset_dates}</p>
                <h4>Earth Engine Snippet</h4>
                    <p style="margin-left: 40px">{pie_id_snippet}</p>
            </body>
            </html>
        """
        return template

    except Exception as e:
        print(e)


def pngsToGif(in_dir, out_gif, fps=10, loop=0):
    """
    png图片列表转为gif动画
    :param in_dir:
    :param out_gif:
    :param fps:
    :param loop:
    :return:
    """
    check_package("Pillow", "PIL")
    from PIL import Image

    if os.path.exists(out_gif):
        os.remove(out_gif)

    if not out_gif.endswith(".gif"):
        raise ValueError("输出的文件必须是GIF文件。")

    out_dir = os.path.dirname(out_gif)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # Create the frames
    frames = []
    imgs = list(glob.glob(os.path.join(in_dir, "*.png")))
    imgs.sort()

    if len(imgs) == 0:
        raise FileNotFoundError(f"没有PNG图片 {in_dir}.")

    for i in imgs:
        new_frame = Image.open(i)
        frames.append(new_frame)

    # Save into a GIF file that loops forever
    frames[0].save(
        out_gif,
        format="GIF",
        append_images=frames[1:],
        save_all=True,
        duration=1000 / fps,
        loop=loop,
    )


def vectorToGif(shp_file, out_gif, col_name, title, color='black',
                fig_size=(10, 8), dpi=300, fps=10, step=10):
    """
    将矢量数据转为GIF东湖
    :param shp_file:
    :param out_gif:
    :param col_name:
    :param title:
    :param color:
    :param fig_size:
    :param dpi:
    :param fps:
    :param step:
    :return:
    """
    check_package("geopandas")
    import geopandas as gpd

    out_dir = os.path.dirname(out_gif)
    tmp_dir = os.path.join(out_dir, "tmp_png")
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    if isinstance(shp_file, str):
        gdf = gpd.read_file(shp_file)
    elif isinstance(shp_file, gpd.GeoDataFrame):
        gdf = shp_file
    else:
        raise ValueError("shp_file必须是文件路径或者geopandas.GeoDataFrame对象。")

    bbox = gdf.total_bounds
    if col_name not in gdf.columns:
        raise Exception(f"{gdf.columns}不包含字段{col_name}")

    values = gdf[col_name].unique().tolist()
    values = [int(v) for v in values]
    values.sort()
    values = values[::step]
    W = bbox[2] - bbox[0]
    H = bbox[3] - bbox[1]
    xy = (int(0.05 * W), int(0.05 * H))
    x, y = xy
    x = bbox[0] + x
    y = bbox[1] + y

    for v in values:
        yrdf = gdf[gdf[col_name] <= v]
        fig, ax = plt.subplots()
        ax = yrdf.plot(facecolor=color, figsize=fig_size)
        ax.set_title(title, fontsize=20)
        ax.set_axis_off()
        ax.set_xlim([bbox[0], bbox[2]])
        ax.set_ylim([bbox[1], bbox[3]])
        ax.text(x, y, v, fontsize=20)
        fig = ax.get_figure()
        plt.tight_layout(pad=3)
        fig.savefig(tmp_dir + os.sep + "%s.png" % v, dpi=dpi)
        plt.clf()
        plt.close("all")

    pngsToGif(tmp_dir, out_gif, fps=fps)
    imgs = list(glob.glob(os.path.join(tmp_dir, "*.png")))
    for img in imgs:
        os.remove(img)
    if os.path.exists(tmp_dir):
        os.removedirs(tmp_dir)


################################# 转boundingbox ###########################################
def roi_to_bbox(GeoJSON_dic):
    bbox_list = []
    for feature in GeoJSON_dic['features']:
        geometry_type = feature['geometry']['type']
        if geometry_type == 'Polygon':
            coordinates = feature['geometry']['coordinates']
            # 计算边界框
            xmin = min(coord[0] for ring in coordinates for coord in ring)
            ymin = min(coord[1] for ring in coordinates for coord in ring)
            xmax = max(coord[0] for ring in coordinates for coord in ring)
            ymax = max(coord[1] for ring in coordinates for coord in ring)

            bbox = [xmin, ymin, xmax, ymax]
            bbox_list.append(bbox)

    return bbox_list


################################# 与下载tile有关的函数 #######################################

def download_file(
    url=None,
    output=None,
    quiet=False,
    proxy=None,
    speed=None,
    use_cookies=True,
    verify=True,
    id=None,
    fuzzy=False,
    resume=False,
    unzip=True,
    overwrite=False,
    subfolder=False
):
    check_package("gdown")
    try:
        import gdown
    except ImportError:
        print(
            "The gdown package is required for this function. Use `pip install gdown` to install it."
        )
        return

    if output is None:
        if isinstance(url, str) and url.startswith("http"):
            output = os.path.basename(url)

    out_dir = os.path.abspath(os.path.dirname(output))
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    if isinstance(url, str):
        if os.path.exists(os.path.abspath(output)) and (not overwrite):
            print(
                f"{output} already exists. Skip downloading. Set overwrite=True to overwrite."
            )
            return os.path.abspath(output)

    output = gdown.download(
        url, output, quiet, proxy, speed, use_cookies, verify, id, fuzzy, resume
    )

    if unzip and output.endswith(".zip"):
        with zipfile.ZipFile(output, "r") as zip_ref:
            if not quiet:
                print("Extracting files...")
            if subfolder:
                basename = os.path.splitext(os.path.basename(output))[0]

                output = os.path.join(out_dir, basename)
                if not os.path.exists(output):
                    os.makedirs(output)
                zip_ref.extractall(output)
            else:
                zip_ref.extractall(os.path.dirname(output))

    return os.path.abspath(output)

# def image_to_cog(source, dst_path=None, profile="deflate", **kwargs):
#     """Converts an image to a COG file.
#
#     Args:
#         source (str): A dataset path, URL or rasterio.io.DatasetReader object.
#         dst_path (str, optional): An output dataset path or or PathLike object. Defaults to None.
#         profile (str, optional): COG profile. More at https://cogeotiff.github.io/rio-cogeo/profile. Defaults to "deflate".
#
#     Raises:
#         ImportError: If rio-cogeo is not installed.
#         FileNotFoundError: If the source file could not be found.
#     """
#     try:
#         from rio_cogeo.cogeo import cog_translate
#         from rio_cogeo.profiles import cog_profiles
#
#     except ImportError:
#         raise ImportError(
#             "The rio-cogeo package is not installed. Please install it with `pip install rio-cogeo` or `conda install rio-cogeo -c conda-forge`."
#         )
#
#     if not source.startswith("http"):
#         source = check_file_path(source)
#
#         if not os.path.exists(source):
#             raise FileNotFoundError("The provided input file could not be found.")
#
#     if dst_path is None:
#         if not source.startswith("http"):
#             dst_path = os.path.splitext(source)[0] + "_cog.tif"
#         else:
#             dst_path = temp_file_path(extension=".tif")
#
#     dst_path = check_file_path(dst_path)
#
#     dst_profile = cog_profiles.get(profile)
#     cog_translate(source, dst_path, dst_profile, **kwargs)


def reproject(image, output, dst_crs="EPSG:4326", resampling="nearest", **kwargs):
    import rasterio as rio
    from rasterio.warp import calculate_default_transform, reproject, Resampling

    if isinstance(resampling, str):
        resampling = getattr(Resampling, resampling)

    image = os.path.abspath(image)
    output = os.path.abspath(output)

    if not os.path.exists(os.path.dirname(output)):
        os.makedirs(os.path.dirname(output))

    with rio.open(image, **kwargs) as src:
        transform, width, height = calculate_default_transform(
            src.crs, dst_crs, src.width, src.height, *src.bounds
        )
        kwargs = src.meta.copy()
        kwargs.update(
            {
                "crs": dst_crs,
                "transform": transform,
                "width": width,
                "height": height,
            }
        )

        with rio.open(output, "w", **kwargs) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rio.band(src, i),
                    destination=rio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=dst_crs,
                    resampling=resampling,
                    **kwargs,
                )


def tms_to_geotiff(
        output,
        bbox,
        zoom=None,
        resolution=None,
        source="SATELLITE",
        crs="EPSG:3857",
        to_cog=False,
        return_image=False,
        overwrite=False,
        quiet=False,
        **kwargs,
):
    """
    """
    import os
    import io
    import math
    import itertools
    import concurrent.futures

    import numpy
    from PIL import Image

    try:
        from osgeo import gdal, osr
    except ImportError:
        raise ImportError("GDAL is not installed. Install it with pip install GDAL")

    try:
        import httpx
        SESSION = httpx.Client()
    except ImportError:
        import requests
        SESSION = requests.Session()

    if not overwrite and os.path.exists(output):
        print(
            f"The output file {output} already exists. Use `overwrite=True` to overwrite it."
        )
        return

    xyz_tiles = {"SATELLITE": "https://webst04.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}"}
    source = xyz_tiles[source.upper()]

    def resolution_to_zoom_level(resolution):
        """
        Convert map resolution in meters to zoom level for Web Mercator (EPSG:3857) tiles.
        """
        # Web Mercator tile size in meters at zoom level 0
        initial_resolution = 156543.03392804097

        # Calculate the zoom level
        zoom_level = math.log2(initial_resolution / resolution)

        return int(zoom_level)

    if isinstance(bbox, list) and len(bbox) == 4:
        west, south, east, north = bbox
    else:
        raise ValueError(
            "bbox must be a list of 4 coordinates in the format of [xmin, ymin, xmax, ymax]"
        )

    if zoom is None and resolution is None:
        raise ValueError("Either zoom or resolution must be provided")
    elif zoom is not None and resolution is not None:
        raise ValueError("Only one of zoom or resolution can be provided")

    if resolution is not None:
        zoom = resolution_to_zoom_level(resolution)

    EARTH_EQUATORIAL_RADIUS = 6378137.0

    Image.MAX_IMAGE_PIXELS = None

    gdal.UseExceptions()
    web_mercator = osr.SpatialReference()
    web_mercator.ImportFromEPSG(3857)

    WKT_3857 = web_mercator.ExportToWkt()

    def from4326_to3857(lat, lon):
        xtile = math.radians(lon) * EARTH_EQUATORIAL_RADIUS
        ytile = (
                math.log(math.tan(math.radians(45 + lat / 2.0))) * EARTH_EQUATORIAL_RADIUS
        )
        return (xtile, ytile)

    def deg2num(lat, lon, zoom):
        lat_r = math.radians(lat)
        n = 2 ** zoom
        xtile = (lon + 180) / 360 * n
        ytile = (1 - math.log(math.tan(lat_r) + 1 / math.cos(lat_r)) / math.pi) / 2 * n
        return (xtile, ytile)

    def is_empty(im):
        extrema = im.getextrema()
        if len(extrema) >= 3:
            if len(extrema) > 3 and extrema[-1] == (0, 0):
                return True
            for ext in extrema[:3]:
                if ext != (0, 0):
                    return False
            return True
        else:
            return extrema[0] == (0, 0)

    def paste_tile(bigim, base_size, tile, corner_xy, bbox):
        if tile is None:
            return bigim
        im = Image.open(io.BytesIO(tile))
        mode = "RGB" if im.mode == "RGB" else "RGBA"
        size = im.size
        if bigim is None:
            base_size[0] = size[0]
            base_size[1] = size[1]
            newim = Image.new(
                mode, (size[0] * (bbox[2] - bbox[0]), size[1] * (bbox[3] - bbox[1]))
            )
        else:
            newim = bigim

        dx = abs(corner_xy[0] - bbox[0])
        dy = abs(corner_xy[1] - bbox[1])
        xy0 = (size[0] * dx, size[1] * dy)
        if mode == "RGB":
            newim.paste(im, xy0)
        else:
            if im.mode != mode:
                im = im.convert(mode)
            if not is_empty(im):
                newim.paste(im, xy0)
        im.close()
        return newim

    def finish_picture(bigim, base_size, bbox, x0, y0, x1, y1):
        xfrac = x0 - bbox[0]
        yfrac = y0 - bbox[1]
        x2 = round(base_size[0] * xfrac)
        y2 = round(base_size[1] * yfrac)
        imgw = round(base_size[0] * (x1 - x0))
        imgh = round(base_size[1] * (y1 - y0))
        retim = bigim.crop((x2, y2, x2 + imgw, y2 + imgh))
        if retim.mode == "RGBA" and retim.getextrema()[3] == (255, 255):
            retim = retim.convert("RGB")
        bigim.close()
        return retim

    def get_tile(url):
        retry = 3
        while 1:
            try:
                r = SESSION.get(url, timeout=60)
                break
            except Exception:
                retry -= 1
                if not retry:
                    raise
        if r.status_code == 404:
            return None
        elif not r.content:
            return None
        r.raise_for_status()
        return r.content

    def draw_tile(
            source, lat0, lon0, lat1, lon1, zoom, filename, quiet=False, **kwargs
    ):
        x0, y0 = deg2num(lat0, lon0, zoom)
        x1, y1 = deg2num(lat1, lon1, zoom)
        if x0 > x1:
            x0, x1 = x1, x0
        if y0 > y1:
            y0, y1 = y1, y0
        corners = tuple(
            itertools.product(
                range(math.floor(x0), math.ceil(x1)),
                range(math.floor(y0), math.ceil(y1)),
            )
        )
        totalnum = len(corners)
        futures = []
        with concurrent.futures.ThreadPoolExecutor(5) as executor:
            for x, y in corners:
                futures.append(
                    executor.submit(get_tile, source.format(z=zoom, x=x, y=y))
                )
            bbox = (math.floor(x0), math.floor(y0), math.ceil(x1), math.ceil(y1))
            bigim = None
            base_size = [256, 256]
            for k, (fut, corner_xy) in enumerate(zip(futures, corners), 1):
                bigim = paste_tile(bigim, base_size, fut.result(), corner_xy, bbox)
                if not quiet:
                    print(
                        f"Downloaded image {str(k).zfill(len(str(totalnum)))}/{totalnum}"
                    )

        if not quiet:
            print("Saving GeoTIFF. Please wait...")
        img = finish_picture(bigim, base_size, bbox, x0, y0, x1, y1)
        imgbands = len(img.getbands())
        driver = gdal.GetDriverByName("GTiff")

        if "options" not in kwargs:
            kwargs["options"] = [
                "COMPRESS=DEFLATE",
                "PREDICTOR=2",
                "ZLEVEL=9",
                "TILED=YES",
            ]

        gtiff = driver.Create(
            filename,
            img.size[0],
            img.size[1],
            imgbands,
            gdal.GDT_Byte,
            **kwargs,
        )
        xp0, yp0 = from4326_to3857(lat0, lon0)
        xp1, yp1 = from4326_to3857(lat1, lon1)
        pwidth = abs(xp1 - xp0) / img.size[0]
        pheight = abs(yp1 - yp0) / img.size[1]
        gtiff.SetGeoTransform((min(xp0, xp1), pwidth, 0, max(yp0, yp1), 0, -pheight))
        gtiff.SetProjection(WKT_3857)
        for band in range(imgbands):
            array = numpy.array(img.getdata(band), dtype="u8")
            array = array.reshape((img.size[1], img.size[0]))
            band = gtiff.GetRasterBand(band + 1)
            band.WriteArray(array)
        gtiff.FlushCache()
        if not quiet:
            print(f"Image saved to {filename}")
        return img
    try:
        image = draw_tile(
            source, south, west, north, east, zoom, output, quiet, **kwargs
        )

        if return_image:
            return image
        if crs.upper() != "EPSG:3857":
            reproject(output, output, crs)

    except Exception as e:
        raise Exception(e)


################################# 与SAM有关的函数  #######################################

def find_pie_dir():
    current_file_path = os.path.abspath(__file__)

    pie_dir = None
    current_dir = os.path.dirname(current_file_path)
    # 逐级向上获取父目录的路径，直到找到 "pie" 目录为止
    while current_dir != os.path.dirname(current_dir):
        if "pie" in os.listdir(current_dir):
            pie_dir = os.path.join(current_dir, "pie")
            break
        current_dir = os.path.dirname(current_dir)

    if pie_dir is None:
        raise Exception("Unable to find 'pie' directory")
    return os.path.join(pie_dir, "Classifier")


def download_checkpoint(url=None, output=None, overwrite=False, **kwargs):
    checkpoints = {
        "sam_vit_h_4b8939.pth": "https://pie-engine-static-data.obs.cn-north-4.myhuaweicloud.com/engine-studio-data/sam_vit_h_4b8939.pth",
        "sam_vit_b_01ec64.pth": "https://pie-engine-static-data.obs.cn-north-4.myhuaweicloud.com/engine-studio-data/sam_vit_b_01ec64.pth",
    }

    if isinstance(url, str) and url in checkpoints:
        url = checkpoints[url]

    if url is None:
        url = checkpoints["sam_vit_h_4b8939.pth"]

    if output is None:
        output = os.path.basename(url)

    return download_file(url, output, overwrite=overwrite, **kwargs)


def array_to_image(value, output, source=None, dtype=None, compress="deflate", **kwargs):
    # 这里考虑直接使用pieImage
    check_package("Pillow", "PIL")
    check_package("opencv-python", "cv2")
    check_package("rasterio")
    from PIL import Image
    import cv2
    import rasterio

    if isinstance(value, str) and os.path.exists(value):
        data = cv2.imread(value)
        image_array = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
    else:
        image_array = value

    if output.endswith(".tif") and source is not None:
        # print('运行到这里了')
        with rasterio.open(source) as src:
            crs = src.crs
            transform = src.transform
            if compress is None:
                compress = src.compression
        # Determine the minimum and maximum values in the array
        min_value = np.min(image_array)
        max_value = np.max(image_array)

        if dtype is None:
            # Determine the best dtype for the array
            if min_value >= 0 and max_value <= 1:
                dtype = np.float32
            elif min_value >= 0 and max_value <= 255:
                dtype = np.uint8
            elif min_value >= -128 and max_value <= 127:
                dtype = np.int8
            elif min_value >= 0 and max_value <= 65535:
                dtype = np.uint16
            elif min_value >= -32768 and max_value <= 32767:
                dtype = np.int16
            else:
                dtype = np.float64
        else:
            dtype = image_array.dtype

        if image_array.ndim == 2:
            metadata = {
                "driver": "GTiff",
                "height": image_array.shape[0],
                "width": image_array.shape[1],
                "count": 1,
                "dtype": dtype,
                "crs": crs,
                "transform": transform,
            }
        elif image_array.ndim == 3:
            metadata = {
                "driver": "GTiff",
                "height": image_array.shape[0],
                "width": image_array.shape[1],
                "count": image_array.shape[2],
                "dtype": dtype,
                "crs": crs,
                "transform": transform,
            }
        else:
            raise ValueError("Array must be 2D or 3D.")
        if compress is not None:
            metadata["compress"] = compress

        with rasterio.open(output, "w", **metadata) as dst:
            if image_array.ndim == 2:
                dst.write(image_array, 1)
            elif image_array.ndim == 3:
                for i in range(image_array.shape[2]):
                    dst.write(image_array[:, :, i], i + 1)

    else:
        img = Image.fromarray(image_array)
        img.save(output, **kwargs)

def blend_images(
        img1,
        img2,
        alpha=0.5,
        output=False,
        show=True,
        figsize=(12, 10),
        axis="off",
        **kwargs,
):
    """
    Blends two images together using the addWeighted function from the OpenCV library.

    Args:
        img1 (numpy.ndarray): The first input image on top represented as a NumPy array.
        img2 (numpy.ndarray): The second input image at the bottom represented as a NumPy array.
        alpha (float): The weighting factor for the first image in the blend. By default, this is set to 0.5.
        output (str, optional): The path to the output image. Defaults to False.
        show (bool, optional): Whether to display the blended image. Defaults to True.
        figsize (tuple, optional): The size of the figure. Defaults to (12, 10).
        axis (str, optional): The axis of the figure. Defaults to "off".
        **kwargs: Additional keyword arguments to pass to the cv2.addWeighted() function.

    Returns:
        numpy.ndarray: The blended image as a NumPy array.
    """
    check_package("opencv-python", "cv2")
    import cv2

    if isinstance(img1, str):
        if img1.startswith("http"):
            img1 = download_file(img1)

        if not os.path.exists(img1):
            raise ValueError(f"Input path {img1} does not exist.")

        img1 = cv2.imread(img1)

    if isinstance(img2, str):
        if img2.startswith("http"):
            img2 = download_file(img2)

        if not os.path.exists(img2):
            raise ValueError(f"Input path {img2} does not exist.")

        img2 = cv2.imread(img2)

    if img1.dtype == np.float32:
        img1 = (img1 * 255).astype(np.uint8)

    if img2.dtype == np.float32:
        img2 = (img2 * 255).astype(np.uint8)

    if img1.dtype != img2.dtype:
        img2 = img2.astype(img1.dtype)

    img1 = cv2.resize(img1, (img2.shape[1], img2.shape[0]))

    # Blend the images using the addWeighted function
    beta = 1 - alpha
    blend_img = cv2.addWeighted(img1, alpha, img2, beta, 0, **kwargs)

    if output:
        array_to_image(blend_img, output, img2)

    if show:
        plt.figure(figsize=figsize)
        plt.imshow(blend_img)
        plt.axis(axis)
        plt.show()
    else:
        return blend_img


def vector_to_geojson(filename, output=None, **kwargs):
    check_package("geopandas")
    import geopandas as gpd

    if not filename.startswith("http"):
        filename = download_file(filename)
    gdf = gpd.read_file(filename, **kwargs)
    if output is None:
        return gdf.__geo_interface__
    else:
        gdf.to_file(output, driver="GeoJSON")

def raster_to_vector(source, output, simplify_tolerance=None, **kwargs):
    """Vectorize a raster dataset.

    Args:
        source (str): The path to the tiff file.
        output (str): The path to the vector file.
        simplify_tolerance (float, optional): The maximum allowed geometry displacement.
            The higher this value, the smaller the number of vertices in the resulting geometry.
    """
    check_package("shapely")
    check_package("geopandas")
    check_package("rasterio")
    import shapely.geometry
    import geopandas as gpd
    import rasterio
    from rasterio import features

    with rasterio.open(source) as src:
        band = src.read()
        mask = band != 0
        shapes = features.shapes(band, mask=mask, transform=src.transform)

    fc = [
        {"geometry": shapely.geometry.shape(shape), "properties": {"value": value}}
        for shape, value in shapes
    ]
    if simplify_tolerance is not None:
        for i in fc:
            i["geometry"] = i["geometry"].simplify(tolerance=simplify_tolerance)

    gdf = gpd.GeoDataFrame.from_features(fc)
    if src.crs is not None:
        gdf.set_crs(crs=src.crs, inplace=True)
    gdf.to_file(output, **kwargs)


def transform_coords(x, y, src_crs, dst_crs, **kwargs):
    """Transform coordinates from one CRS to another.

    Args:
        x (float): The x coordinate.
        y (float): The y coordinate.
        src_crs (str): The source CRS, e.g., "EPSG:4326".
        dst_crs (str): The destination CRS, e.g., "EPSG:3857".

    Returns:
        dict: The transformed coordinates in the format of (x, y)
    """
    transformer = pyproj.Transformer.from_crs(
        src_crs, dst_crs, always_xy=True, **kwargs
    )
    return transformer.transform(x, y)


def geojson_to_coords(
        geojson: [str, dict], src_crs: str = "epsg:4326", dst_crs: str = "epsg:4326"
) -> list:
    check_package("geopandas")
    import geopandas as gpd

    if isinstance(geojson, dict):
        geojson = json.dumps(geojson)
    gdf = gpd.read_file(geojson, driver="GeoJSON")
    centroids = gdf.geometry.centroid
    centroid_list = [[point.x, point.y] for point in centroids]
    if src_crs != dst_crs:
        centroid_list = transform_coords(
            [x[0] for x in centroid_list],
            [x[1] for x in centroid_list],
            src_crs,
            dst_crs,
        )
        centroid_list = [[x, y] for x, y in zip(centroid_list[0], centroid_list[1])]
    return centroid_list


def coords_to_xy(src_fp: str, coords: list, coord_crs: str = "epsg:4326", **kwargs) -> list:
    check_package("rasterio")
    import rasterio

    if isinstance(coords, np.ndarray):
        coords = coords.tolist()

    xs, ys = zip(*coords)
    # print(src_fp)
    with rasterio.open(src_fp) as src:
        if coord_crs != src.crs:
            xs, ys = transform_coords(xs, ys, coord_crs, src.crs, **kwargs)
        rows, cols = rasterio.transform.rowcol(src.transform, xs, ys, **kwargs)
        result = [[col, row] for col, row in zip(cols, rows)]

        result = [
            [x, y] for x, y in result if 0 <= x < src.width and 0 <= y < src.height
        ]
        if len(result) == 0:
            print("No valid pixel coordinates found.")
        elif len(result) < len(coords):
            print("Some coordinates are out of the image boundary.")

    return result


def bbox_to_xy(
        src_fp: str, coords: list, coord_crs: str = "epsg:4326", **kwargs
) -> list:
    check_package("geopandas")
    check_package("rasterio")
    import geopandas as gpd
    import rasterio

    if isinstance(coords, str):
        gdf = gpd.read_file(coords)
        coords = gdf.geometry.bounds.values.tolist()
        if gdf.crs is not None:
            coord_crs = f"epsg:{gdf.crs.to_epsg()}"
    elif isinstance(coords, np.ndarray):
        coords = coords.tolist()
    if isinstance(coords, dict):
        import json

        geojson = json.dumps(coords)
        gdf = gpd.read_file(geojson, driver="GeoJSON")
        coords = gdf.geometry.bounds.values.tolist()

    elif not isinstance(coords, list):
        raise ValueError("coords must be a list of coordinates.")

    if not isinstance(coords[0], list):
        coords = [coords]

    new_coords = []

    with rasterio.open(src_fp) as src:
        width = src.width
        height = src.height

        for coord in coords:
            minx, miny, maxx, maxy = coord

            if coord_crs != src.crs:
                minx, miny = transform_coords(minx, miny, coord_crs, src.crs, **kwargs)
                maxx, maxy = transform_coords(maxx, maxy, coord_crs, src.crs, **kwargs)

                rows1, cols1 = rasterio.transform.rowcol(
                    src.transform, minx, miny, **kwargs
                )
                rows2, cols2 = rasterio.transform.rowcol(
                    src.transform, maxx, maxy, **kwargs
                )

                new_coords.append([cols1, rows1, cols2, rows2])

            else:
                new_coords.append([minx, miny, maxx, maxy])

    result = []

    for coord in new_coords:
        minx, miny, maxx, maxy = coord

        if (
                minx >= 0
                and miny >= 0
                and maxx >= 0
                and maxy >= 0
                and minx < width
                and miny < height
                and maxx < width
                and maxy < height
        ):
            result.append(coord)

    if len(result) == 0:
        print("No valid pixel coordinates found.")
        return None
    elif len(result) == 1:
        return result[0]
    elif len(result) < len(coords):
        print("Some coordinates are out of the image boundary.")

    return result


if __name__ == "__main__":
    print("test ...")
    # _content = "hello 你好啊<> var abc"
    # data =  encodeURIComponent(_content)
    # print(data)
    # print(decodeURIComponent(data))
    # a = json.dumps({"a":1, "b": 2})
    # b = json.loads(a)
    # print(random_color((12, 20, 32)))
    # vectorToGif("/Users/lishiwei/Desktop/shapefile2gif-main/mtbf33_wgs84_08013_boulder_subset.shp",
    #             "/Users/lishiwei/Desktop/mtbf33_wgs84_08013_boulder_subset.gif",
    #             "year_built", "building")

    # bbox = [116.147803,39.909748,116.149537,39.911091]

    # import tempfile
    # TEMP_IMG_DIR = "temp_IMG"

    # # with tempfile.NamedTemporaryFile(mode="w", suffix=".tif", dir=TEMP_IMG_DIR,delete=False) as temp_file:
    # #     temp_file_name = temp_file.name
    # #     tms_to_geotiff(temp_file_name,bbox,18,overwrite=True)
    # #     print(temp_file_name)
    # # data = {'type': 'FeatureCollection', 'features': [{'type': 'Feature', 'properties': {}, 'geometry': {'type': 'Polygon', 'coordinates': [[[115.920868, 39.99606], [115.920868, 40.027614], [115.974426, 40.027614], [115.974426, 39.99606], [115.920868, 39.99606]]]}}, {'type': 'Feature', 'properties': {}, 'geometry': {'type': 'Polygon', 'coordinates': [[[116.045837, 39.984486], [116.045837, 39.998164], [116.069183, 39.998164], [116.069183, 39.984486], [116.045837, 39.984486]]]}}, {'type': 'Feature', 'properties': {}, 'geometry': {'type': 'Polygon', 'coordinates': [[[116.086349, 39.984486], [116.085663, 39.958701], [116.117935, 39.969753], [116.086349, 39.984486]]]}}, {'type': 'Feature', 'properties': {}, 'geometry': {'type': 'Point', 'coordinates': [116.112442, 39.995534]}}]}

    # bbox_list = [[115.920868, 39.99606, 115.974426, 40.027614], [116.045837, 39.984486, 116.069183, 39.998164], [116.085663, 39.958701, 116.117935, 39.984486]]

    # def clear_temp_dir(directory):
    # # 遍历目录中的文件
    #     for filename in os.listdir(directory):
    #         file_path = os.path.join(directory, filename)
    #         os.remove(file_path)

    # clear_temp_dir(TEMP_IMG_DIR)

    # for bbox in bbox_list:
    #      print(bbox)
    #      with tempfile.NamedTemporaryFile(mode="w", suffix=".tif", dir=TEMP_IMG_DIR,delete=False) as temp_file:
    #         temp_file_name = temp_file.name
    #         tms_to_geotiff(temp_file_name,bbox,10,overwrite=True)

    height = 176
    width = 156
    # 创建一个随机的二维数组
    array = np.random.rand(height, width)
    array_to_image(array, output='mask2.tif',
                   source='/Users/liyujia/Documents/svn/PIE-Engine-Python/pie/Classifier/temp_IMG/roi/tmp96ptxar_.tif')

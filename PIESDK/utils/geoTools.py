# -*- coding:utf-8 -*-
"""
@Project :   PyCharm
@File    :   geoTools.py
@Time    :   2021/4/18 18:28 下午
@Author  :   lsw
@Version :   1.0
@Contact :   shi_weihappy@126.com
@License :   (C)Copyright 2019-2020, lsw
@Desc    :   None
"""
import math
import os
import base64
from IPython.display import Javascript, display
import json
from pandas import read_csv
from mss import mss
import shapefile as shp
import csv
from pie.utils.common import download_from_url
from pie.utils.config import config
from pie.utils.pieHttp import GET
from pie.vector.featureCollection import PIEFeatureCollection
from pie.vector.geometry import PIEGeometry
from pie.image.image import PIEImage
from pie.vector.feature import PIEFeature
from pie.image.imageCollection import PIEImageCollection

# Adds other method of not Map class
def screen_capture(outfile, monitor=1):
    """
    全屏截屏
    :param outfile: 存放路径
    :param monitor:
    :return:
    """
    out_dir = os.path.dirname(outfile)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    if not isinstance(monitor, int):
        print('The monitor number must be an integer.')
        return
    try:
        with mss() as sct:
            sct.shot(output=outfile, mon=monitor)
            return outfile
    except Exception as e:
        print(e)

def csv_to_shp(csvfile, shpfile, longitude='longitude', latitude='latitude'):
    """
    Transform the csv file to shp file.
    :param csvfile:
    :param shpfile:
    :param longitude:
    :param latitude:
    :return:
    """
    if not os.path.exists(csvfile):
        print("The csv file don't exists.")
        return
    if not csvfile.endswith('.csv'):
        print("The csv file must end with .csv!")
        return

    outdir = os.path.dirname(shpfile)
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    try:
        points = shp.Writer(shpfile, shapeType=shp.POINT)
        with open(csvfile, "r", encoding="UTF-8") as cf:
            csvreader = csv.DictReader(cf)
            header = csvreader.fieldnames
            [points.field(field) for field in header]
            for row in csvreader:
                points.point((float(row[longitude])), (float(row[latitude])))
                points.record(*tuple([row[f] for f in header]))

        outprj = shpfile.replace('.shp', '.prj')
        with open(outprj, 'w', encoding="UTF-8") as f:
            prjstr = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.0174532925199433]] '
            f.write(prjstr)
    except Exception as e:
        print(e)

def csv_to_txt(csvfile, txtfile):
    """
    Transform csv file to txt file
    @param csvfile:
    @param txtfile:
    @return:
    """
    # if os.path.exists(txtfile):
    #     os.remove(txtfile)
    try:
        data = read_csv(csvfile, sep=",")

        with open(txtfile, 'a+', encoding='UTF-8') as f:
            f.write((str("id") + '\t' + str("latitude") + '\t' + str("longitude") + '\t' + '\n'))
            for line in data.values:
                f.write((str(line[0]) + '\t' + str(line[1]) + '\t' + str(line[2]) + '\t' + '\n'))
            f.close()
    except Exception as e:
        print(e)

def installPackage_fromGithub(url):
    """
    Install a package from a github repository.
    @param url
    """
    try:
        download_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        reponame = os.path.basename(url)
        zipurl = os.path.join(url, 'archive/master.zip')
        filename = reponame + '-master.zip'
        download_from_url(url=zipurl, out_file_name=filename, out_dir=download_dir, unzip=True)

        pkgdir = os.path.join(download_dir, reponame + '-master')
        pkgname = os.path.basename(url)
        workdir = os.getcwd()
        os.chdir(pkgdir)
        print("Installing {}...".format(pkgname))
        cmd = 'pip install .'
        os.system(cmd)
        os.chdir(workdir)
        print("{} has been installed successfully.".format(pkgname))

    except Exception as e:
        print(e)

def create_code_cell(code='', where='below'):
    """
    创建代码块
    :param code:
    :param where:
    :return:
    """
    encoded_code = (base64.b64encode(str.encode(code))).decode()
    display(Javascript("""var code = IPython.notebook.insert_cell_{0}('code');
                            code.set_text(atob("{1}"));""".format(
        where, encoded_code
    )))

def geocode(location, reverse=False):
    """
    Search location by address and lat/lng coordinates.
    编码：
    {
        "location": {
            "lon": "116.001688",
            "level": "地名地址",
            "lat": "40.453228"
        },
        "status": "0",
        "msg": "ok",
        "searchVersion": "4.8.0"
    }
    逆地理编码
    {
        "result": {
            "formatted_address": "北京市西城区西什库大街31号院23东方开元信息科技公司",
            "location": {
                "lon": 116.37304,
                "lat": 39.92594
            },
            "addressComponent": {
                "address": "西什库大街31号院23",
                "city": "北京市西城区",
                "road": "大红罗厂街",
                "poi_position": "东北",
                "address_position": "东北",
                "road_distance": 49,
                "poi": "东方开元信息科技公司",
                "poi_distance": "38",
                "address_distance": 38
            }
        },
        "msg": "ok",
        "status": "0"
    }

    :param location:
    :param reverse:
    :return:
    """
    if not isinstance(location, str):
        print("The location must be a string")
        return None

    if not reverse:
        locations = []
        addresses = set()
        url = config.getGeoURL()
        result = GET(url.format(ds='\{"keyWord":{location}\}'.format(location=location)), {}, {})
        if result.get("status", -1) == "0":
            _location = result.get("location")
            locations.append([_location.get("lon", -1), _location.get("lat"), -1])
            addresses.add(_location.get("level", ""))
        if len(locations) > 0:
            return locations
        else:
            return None
    else:
        try:
            if ',' in location:
                latlon = [float(x) for x in location.split(',')]
            elif ' ' in location:
                latlon = [float(x) for x in location.split(' ')]
            else:
                print("The lat/lon coordinates should be numbers only and separated by comma or space, such as 30.2, 110.2")
                return
            locations = []
            addresses = set()
            url = config.getGeoURL()
            result = GET(url.format(postStr="\{'lon':{lon},'lat':{lat},'ver':1\}".format(lon=latlon[0], lat=latlon[1])), {}, {})
            if result.get("status", -1) == "0":
                _result = result.get("result")
                _location = _result.get("location")
                locations.append([_location.get("lon", -1), _location.get("lat"), -1])
                addresses.add(_result.get("formatted_address", ""))
            if len(locations) > 0:
                return locations
            else:
                return None
        except Exception as e:
            print(e)
            return

def latlon_from_text(location):
    """
    获取指定的经纬度
    :param location:
    :return:
    """
    try:
        if ',' in location:
            latlon = [float(x) for x in location.split(',')]
        elif ' ' in location:
            latlon = [float(x) for x in location.split(' ')]
        else:
            print('经纬度录入错误')
            return None

        lat, lon = latlon[0], latlon[1]
        if -90 <= lat <= 90 and -180 <= lon <= 180:
            return lat, lon
        else:
            return None
    except Exception as e:
        print(f"转换参数错误: {e}")
        return None

def search_pie_data(keywords):
    """
    Searches Pie Enging data catalog.
    """
    try:
        cmd = "pieadd search --keywords '{}'".format(str(keywords))
        output = os.popen(cmd).read()
        start_index = output.index('[')
        assets = eval(output[start_index:])

        results = []
        for asset in assets:
            asset_dates = asset['start_date'] + ' - ' + asset['end_date']
            asset_snippet = asset['pie_id_snippet']
            start_index = asset_snippet.index("'") + 1
            end_index = asset_snippet.index("'", start_index)
            asset_id = asset_snippet[start_index:end_index]

            asset['dates'] = asset_dates
            asset['id'] = asset_id
            asset['uid'] = asset_id.replace('/', '_')
            results.append(asset)
        return results
    except Exception as e:
        print(e)

def geojson_to_pie(geojson, geodesic=True):
    """
    Transform a geojson to pie geometry
    """
    try:
        if not isinstance(geojson, dict) and os.path.isfile(geojson):
            with open(os.path.abspath(geojson), "r", encoding="UTF-8") as f:
                geojson = json.load(f)

        if geojson['type'] == 'FeatureCollection':
            features = PIEFeatureCollection(geojson['features'])
            return features
        elif geojson['type'] == 'Feature':
            keys = geojson['properties']['style'].keys()
            if 'radius' in keys:
                geom = PIEGeometry(geojson['geometry'])
                radius = geojson['properties']['style']['radius']
                geom = geom.buffer(radius)
            elif geojson['geometry']['type'] == 'Point':
                coordinates = geojson['geometry']['coordinates']
                longitude = coordinates[0]
                latitude = coordinates[1]
                geom = PIEGeometry.Point(longitude, latitude)
            else:
                geom = PIEGeometry(geojson['geometry'], "", geodesic)
            return geom
        else:
            print("Could not convert the geojson to geometry")
    except Exception as e:
        print("Could not convert the geojson to geometry")
        print(e)

def calculate_center_coordinates(coordinatesList):
    """
    coordinates list
    @param coordinatesList:
    @return:
    """
    coordinatesList = coordinatesList[0] if len(coordinatesList[0])>1 else coordinatesList[0][0]
    total = len(coordinatesList)
    X = Y = Z = 0
    for _lon, _lat in coordinatesList:
        lat = _lat * math.pi / 180
        lon = _lon * math.pi / 180
        x = math.cos(lat) * math.cos(lon)
        y = math.cos(lat) * math.sin(lon)
        z = math.sin(lat)
        X += x
        Y += y
        Z += z
    X = X / total
    Y = Y / total
    Z = Z / total
    lon = math.atan2(Y, X)
    hyp = math.sqrt(X*X + Y*Y)
    lat = math.atan2(Z, hyp)

    lat = lat * 180 / math.pi
    lon = lon * 180 / math.pi
    return [lat, lon]

def getCenter(pieObject, zoom):
    if zoom is None:
        zoom = 9
    if isinstance(pieObject, PIEGeometry):
        coordinates = pieObject.getInfo().get("coordinates")
        center = calculate_center_coordinates(coordinates)
        lat = center[0]
        lon = center[1]
    elif isinstance(pieObject, PIEFeature):
        coordinates = pieObject.geometry().getInfo().get('coordinates')
        center = calculate_center_coordinates(coordinates)
        lat = center[0]
        lon = center[1]
    elif isinstance(pieObject, PIEFeatureCollection):
        coordinates = pieObject.getAt(0).geometry().getInfo().get("coordinates")
        center = calculate_center_coordinates(coordinates)
        lat = center[0]
        lon = center[1]
    elif isinstance(pieObject, PIEImage):
        coordinates = pieObject.geometry().getInfo().get('coordinates')
        center = calculate_center_coordinates(coordinates)
        lat = center[0]
        lon = center[1]
    elif isinstance(pieObject, PIEImageCollection):
        coordinates = pieObject.getAt(0).geometry().getInfo().get("coordinates")
        center = calculate_center_coordinates(coordinates)
        lat = center[0]
        lon = center[1]
    else:
        lat = 31.24709900539396
        lon = 121.27765674850913

    return lon, lat, zoom
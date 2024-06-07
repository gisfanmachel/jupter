# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   piefolium.py
@Time    :   2022/7/27 09:52
@Author  :   lishiwei
@Version :   1.0
@Contact :   shi_weihappy@126.com
@License :   (C)Copyright 2021-2022, lishiwei
@Desc    :   None
"""
import math
import os
import json
import random
import folium
from folium import plugins
from IPython.display import display
import ipywidgets as widgets
from pie.utils.geoTools import latlon_from_text, screen_capture, getCenter
from pie.utils.common import render_size, random_string, check_package
from pie.utils.config import config
from pie.utils.pieHttp import GET
from pie.utils.geoTools import create_code_cell
from pie.utils.basemapInfo import folium_basemap
from pie.map.foliumTileLayer import generateTileLayer
from pie.map.mapstyle import formatStyle
import streamlit as st
import streamlit.components.v1 as components
from streamlit_folium import st_folium

class PIEMap(folium.Map):
    def __init__(self, center=None, zoom=10, **kwargs):
        if center is None:
            center = [39.8948591963122, 116.33867898233117]
        self.zoom = zoom

        kwargs["location"] = center
        kwargs["zoom_start"] = self.zoom
        if "height" not in kwargs:
            kwargs["height"] = "100%"
        else:
            height = kwargs["height"]
            if isinstance(height, int) or isinstance(height, float):
                kwargs["height"] = float(height)
            elif ("height" in kwargs
                and isinstance(height, str)
                and ("%" not in height)):
                kwargs["height"] = float(height.replace("px", "").strip())
            else:
                kwargs["height"] = height
        if "width" not in kwargs:
            kwargs["width"] = "100%"
        else:
            width = kwargs["width"]
            if isinstance(width, int) or isinstance(width, float):
                kwargs["width"] = float(width)
            elif ("width" in kwargs
                  and isinstance(width, str)
                  and ("%" not in width)):
                kwargs["width"] = float(width.replace("px", "").strip())
            else:
                kwargs["width"] = width
        kwargs["tiles"] = None
        if "plugin_LatLngPopup" not in kwargs:
            kwargs["plugin_LatLngPopup"] = False
        if "plugin_Fullscreen" not in kwargs:
            kwargs["plugin_Fullscreen"] = True
        if "plugin_Draw" not in kwargs:
            kwargs["plugin_Draw"] = True
        if "Draw_export" not in kwargs:
            kwargs["Draw_export"] = False
        if "plugin_MiniMap" not in kwargs:
            kwargs["plugin_MiniMap"] = False
        if "plugin_LayerControl" not in kwargs:
            kwargs["plugin_LayerControl"] = True
        super(PIEMap, self).__init__(**kwargs)

        self._add_basemap(kwargs.get("map_list"))
        if kwargs.get("plugin_LatLngPopup"):
            folium.LatLngPopup().add_to(self)
        if kwargs.get("plugin_Fullscreen"):
            plugins.Fullscreen().add_to(self)
        if kwargs.get("plugin_Draw"):
            plugins.Draw(export=kwargs.get("Draw_export")).add_to(self)
        if kwargs.get("plugin_MiniMap"):
            plugins.MiniMap().add_to(self)

        self.search_datasets = None
        self.search_user_assets = None
        self.search_loc_marker = None
        self.select_tag = None
        self.screenshot = None
        self.layerControl = False

    def _add_basemap(self, map_list=None):
        if map_list is None:
            _basemap = folium_basemap()
            _basemap["GaodeImg"].add_to(self)
            _basemap["GaodeVec"].add_to(self)
        else:
            for _info in map_list:
                _url = _info.get("url")
                _name = _info.get("name")
                folium_basemap(_url, _name, _name).add_to(self)

    @staticmethod
    def name():
        return "PIEMap"

    def addLayerControl(self):
        if not self.layerControl:
            folium.LayerControl().add_to(self)
        self.layerControl = True

    def setCenter(self, lon, lat, zoom=None):
        """
        设置居中位置
        :param lon:
        :param lat:
        :param zoom:
        :return:
        """
        if zoom is not None:
            self.zoom = zoom
        self.fit_bounds([[lat, lon], [lat, lon]], max_zoom=self.zoom)

    def addLayer(self, pieObject, style, name, visible=True, opacity=1.0):
        """
        添加指定图层
        :param pieObject:
        :param style:
        :param name:
        :param visible:
        :param opacity:
        :return:
        """
        style = formatStyle(style)
        tileLayer = generateTileLayer(
            pieObject=pieObject,
            style=style,
            name=name,
            visible=visible,
            opacity=opacity
        )
        if not tileLayer:
            return
        tileLayer.add_to(self)

    def imgInfo(self, pieImage):
        """
        点击影像获取指定信息。
        :param pieImage:
        :return:
        """
        print("请使用 leaflet模式查看指定位置的信息")

    def addGeoJSON(self, jsonfile, name="geojson"):
        """
        Load the JSON file
        args:
            jsonfile: the path of local json file
        """
        if name is None:
            name = str(jsonfile)

        with open(jsonfile, 'r') as f:
            data = json.load(f)

        geo_json = folium.GeoJson(
            data=data,
            style_function=lambda feature: {
                'opacity': 1,
                'fillOpacity': 0.8,
                'weight': 1,
                'color': 'black',
                'fillColor': random.choice(['red', 'yellow', 'green', 'orange']),
            },
            highlight_function=lambda feature: {
                'color': 'red', 'fillOpacity': 0.5
            },
            name=name
        )
        geo_json.add_to(self)

    def imageOverlay(self, url, bounds, attribution="", name=None):
        """
        加载图片
        :param url:
        :param bounds:
        :param attribution:
        :param name:
        :return:
        """
        if name is None:
            name = str(url)
        kwargs = {
            'url': url,
            'bounds': bounds,
            'alt': attribution,
            'name': name
        }
        img_overlay = folium.raster_layers.ImageOverlay(**kwargs)
        self.add_child(img_overlay)

    def videoOverlay(self, url, bounds, attribution="", name=None):
        """
        加载视屏
        :param url:
        :param bounds:
        :param attribution:
        :param name:
        :return:
        """
        if name is None:
            name = str(url)

        kwargs = {
            'video_url': url,
            'bounds': bounds,
            # 'attribution': attribution,
            'name': name
        }
        vid_overlay = folium.raster_layers.VideoOverlay(**kwargs)
        self.add_child(vid_overlay)

    def getScale(self):
        """Returns the approximate pixel scale of the current map view, in meters.
        Returns:
            float: Map resolution in meters.
        """
        zoomLevel = self.zoom
        resolution = 156543.04 * math.cos(0) / math.pow(2, zoomLevel)
        # print("地图分辨率：", resolution)
        return resolution

    def centerObject(self, pieObject, zoom=None):
        """
        设置居中显示
        :param pieObject:
        :param zoom:
        :return:
        """
        _lon, _lat, _zoom = getCenter(pieObject, zoom)
        self.setCenter(_lon, _lat, _zoom)

    def addMarker(self, latlon, draggable=False, name="marker"):
        if not latlon:
            print("请输入具体位置")
            return
        marker = folium.Marker(
            location=latlon,
            draggable=draggable,
            name=name
        )
        marker.add_to(self)

    def addTileLayer(self, url, name=None, attribution="", opacity=1):
        """
        添加瓦片地图
        :param url:
        :param name:
        :param attribution:
        :param opacity:
        :return:
        """
        if name is None:
            name = str(url)
        try:
            tileLayer = folium.raster_layers.TileLayer(
                tiles=url,
                name=name,
                attr=attribution,
                opacity=opacity,
                show=True
            )
            tileLayer.add_to(self)
        except Exception as e:
            print(e, '\n', "Failed to add the specified tileLayer.")

    def addWmsLayer(self, url, layers, name=None, attribution='', format='image/jpeg', transparent=False, opacity=1.0):
        """
        添加wms服务
        :param url:
        :param layers:
        :param name:
        :param attribution:
        :param format:
        :param transparent:
        :param opacity:
        :return:
        """
        if name is None:
            name = str(layers)
        try:
            wmsLayer = folium.raster_layers.WmsTileLayer(
                url=url,
                layers=layers,
                name=name,
                attr=attribution,
                fmt=format,
                transparent=transparent,
                opacity=opacity,
                show=True
            )
            wmsLayer.add_to(self)
        except Exception as e:
            print(e, '\n', "Failed to add the specified wms tilelayer.")

    def toImage(self, outfile=None, monitor=1):
        """
        保存地图为图片
        :param outfile:
        :param monitor:
        :return:
        """
        if outfile is None:
            outfile = os.path.join(os.getcwd(), 'pieMap.png')

        if outfile.endswith('.png') or outfile.endswith('.jpg'):
            pass
        else:
            print('The output file must be a PNG or JPG image.')
            return
        work_dir = os.path.dirname(outfile)
        if not os.path.exists(work_dir):
            os.makedirs(work_dir)

        self.screenshot = screen_capture(outfile, monitor)

    def initUIPanel(self):
        search_type = widgets.ToggleButtons(
            options=["查询位置", "公共数据集", "个人数据资源"],
            tooltips=[
                "输入经纬度查询位置",
                "查询公共数据集资源",
                "查询个人数据资源",
            ]
        )
        search_type.style.button_width = "120px"

        search_box = widgets.Text(
            placeholder="输入经纬度查询位置",
            tooltip="查询位置",
            layout=widgets.Layout(width="372px")
        )

        search_output = widgets.Output(
            layout={
                "max_width": "372px",
                "max_height": "250px",
                "overflow": "scroll",
            }
        )

        assets_dropdown = widgets.Dropdown(
            options=[],
            layout=widgets.Layout(min_width="311px", max_width="311px")
        )

        import_btn = widgets.Button(
            description="导入",
            button_style="primary",
            tooltip="点击导入引入资源",
            layout=widgets.Layout(min_width="57px", max_width="57px")
        )

        def import_btn_clicked(b):
            if assets_dropdown.value is not None:
                dropdown_index = assets_dropdown.index
                dataset_uid = "dataset_" + random_string(string_length=3)
                if self.select_tag == "公共数据集":
                    datasets = self.search_datasets
                    dataset = datasets[dropdown_index]
                    _id = dataset["id"]
                    if dataset.get("category") == "raster":
                        content = f"{dataset_uid} = pie.ImageCollection('{_id}')"
                    else:
                        content = f"{dataset_uid} = pie.FeatureCollection('{_id}')"
                    create_code_cell(content)
                elif self.select_tag == "个人数据资源":
                    datasets = self.search_user_assets
                    dataset = datasets[dropdown_index]
                    _id = dataset["fullPath"]
                    _type = dataset.get("type")
                    if _type == 2:
                        content = f"{dataset_uid} = pie.ImageCollection('{_id}')"
                        create_code_cell(content)
                    elif _type == 3:
                        content = f"{dataset_uid} = pie.Image('{_id}')"
                        create_code_cell(content)
                    elif _type == 4:
                        content = f"{dataset_uid} = pie.FeatureCollection('{_id}')"
                        create_code_cell(content)
                    else:
                        print("找不到指定的类型")
                else:
                    print("查找数据资源失败！")
                    return

        import_btn.on_click(import_btn_clicked)

        html_widget = widgets.HTML()

        def dropdown_change(change):
            dropdown_index = assets_dropdown.index
            if dropdown_index is not None and dropdown_index >= 0:
                with search_output:
                    search_output.clear_output(wait=True)
                    print("Loading ...")
                    if self.select_tag == "公共数据集":
                        datasets = self.search_datasets
                        dataset = datasets[dropdown_index]
                        dataset_html = _pie_dataset_html(dataset)
                        html_widget.value = dataset_html
                        search_output.clear_output(wait=True)
                        display(html_widget)
                    elif self.select_tag == "个人数据资源":
                        datasets = self.search_user_assets
                        dataset = datasets[dropdown_index]
                        dataset_html = _pie_user_asset_html(dataset)
                        html_widget.value = dataset_html
                        search_output.clear_output(wait=True)
                        display(html_widget)
                    else:
                        print("查找数据资源失败！")

        assets_dropdown.observe(dropdown_change, names="value")

        assets_combo = widgets.HBox()
        assets_combo.children = [import_btn, assets_dropdown]

        def _search_dataset():
            urlInfo = config.getFuzzyQuery()
            response = GET(urlInfo=urlInfo)
            result = []
            if response:
                result = response.get("data", [])
            return result

        def _pie_dataset_html(asset):
            """
            :param asset:
            :return:
            """
            template = """
                <html>
                <body>
                    <h3>{title}</h3>
                    <h4>日期</h4>
                        <p style="margin-left: 40px">{start_time} - {end_time}</p>
                    <h4>代码</h4>
                        <p style="margin-left: 40px">{snippet}</p>
                    <h4>简介</h4>
                        <p style="margin-left: 40px">{desc}</p>
                    <h4>资源ID</h4>
                        <p style="margin-left: 40px"><a href="link" target="_blank">{id}</a></p>
                    <h4>缩略图</h4>
                        <img src="https://pie-engine-preview-images.obs.cn-north-4.myhuaweicloud.com/Dataset/{thumbnail}">
                </body>
                </html>
            """
            text = ""
            try:
                text = template.format(
                    title=asset.get("title"),
                    start_time=asset.get("start_time"),
                    end_time=asset.get("end_time"),
                    snippet=asset.get("snippet"),
                    desc=asset.get("desc"),
                    id=asset.get("id"),
                    link=asset.get("link"),
                    thumbnail=asset.get("thumbnail")
                )
            except Exception as e:
                print(e)
            return text

        def _search_user_assets():
            urlInfo = config.getQueryCatalogURL()

            def recur_get(url_Info):
                result = GET(url_Info)
                _data = result.get("data", [])
                _result = []
                for d in _data:
                    _type = d.get("type")
                    if _type == 1:
                        _uuid = d.get("uuid")
                        _url = urlInfo.get("url") + "?" + "parentId={}".format(_uuid)
                        _urlInfo = {"url": _url, "x-api": urlInfo.get("x-api")}
                        _result.extend(recur_get(_urlInfo))
                    elif _type == 2 or _type == 3 or _type == 4:
                        _result.append(d)
                return _result

            return recur_get(urlInfo)

        def _pie_user_asset_html(asset):
            """
            :param asset:
            :return:
            """
            image_template = """
                <html>
                <body>
                    <h3>{name}</h3>
                    <h4>文件ID</h4>
                        <p style="margin-left: 40px">{fullPath}</p>
                    <h4>创建日期</h4>
                        <p style="margin-left: 40px">{createTime}</p>
                    <h4>文件大小</h4>
                        <p style="margin-left: 40px">{fileSize}</p>
                    <h4>更新日期</h4>
                        <p style="margin-left: 40px">{updateTime}</p>
                    <h4>缩略图</h4>
                        <img src="https://pie-engine-preview-images.obs.cn-north-4.myhuaweicloud.com/{uri}.jpg">
                </body>
                </html>
            """

            feature_template = """
                <html>
                <body>
                    <h3>{name}</h3>
                    <h4>文件ID</h4>
                        <p style="margin-left: 40px">{fullPath}</p>
                    <h4>创建日期</h4>
                        <p style="margin-left: 40px">{createTime}</p>
                    <h4>文件大小</h4>
                        <p style="margin-left: 40px">{fileSize}</p>
                    <h4>更新日期</h4>
                        <p style="margin-left: 40px">{updateTime}</p>
                </body>
                </html>
            """

            dateset_template = """
                <html>
                <body>
                    <h3>{name}</h3>
                    <h4>文件ID</h4>
                        <p style="margin-left: 40px">{fullPath}</p>
                    <h4>创建日期</h4>
                        <p style="margin-left: 40px">{createTime}</p>
                    <h4>更新日期</h4>
                        <p style="margin-left: 40px">{updateTime}</p>
                </body>
                </html>
            """
            text = ""
            try:
                _type = asset.get("type")
                if _type == 2:
                    text = dateset_template.format(
                        name=asset.get("name"),
                        fullPath=asset.get("fullPath"),
                        createTime=asset.get("createTime"),
                        updateTime=asset.get("updateTime")
                    )
                elif _type == 3:
                    text = image_template.format(
                        name=asset.get("name"),
                        fullPath=asset.get("fullPath"),
                        createTime=asset.get("createTime"),
                        updateTime=asset.get("updateTime"),
                        uri=asset.get("uri"),
                        fileSize=render_size(asset.get("fileSize"))
                    )
                elif _type == 4:
                    text = feature_template.format(
                        name=asset.get("name"),
                        fullPath=asset.get("fullPath"),
                        createTime=asset.get("createTime"),
                        updateTime=asset.get("updateTime"),
                        fileSize=render_size(asset.get("fileSize"))
                    )
                else:
                    print("找不到指定的类型")
            except Exception as e:
                print(e)
            return text

        def search_type_changed(change):
            search_box.value = ""
            search_output.clear_output()
            assets_dropdown.options = []
            self.select_tag = change['new']
            if change["new"] == "查询位置":
                search_box.continuous_update = False
                search_box.placeholder = "输入经纬度，格式是：纬度,经度。例如：40,-100"
                search_result_widget.children = [
                    search_type,
                    search_box,
                    search_output,
                ]
            elif change["new"] == "公共数据集":
                # UI界面
                # search_box.placeholder = (
                #     "输入搜索的关键词，比如：landsat"
                # )
                search_result_widget.children = [
                    search_type,
                    # search_box,
                    assets_combo,
                    search_output,
                ]
                # 逻辑操作
                self.default_style = {"cursor": "wait"}
                if not self.search_datasets:
                    self.search_datasets = _search_dataset()
                asset_titles = [x["title"] for x in self.search_datasets]
                assets_dropdown.options = asset_titles
                if len(self.search_datasets) > 0:
                    html_widget.value = _pie_dataset_html(self.search_datasets[0])
                with search_output:
                    search_output.clear_output()
                    display(html_widget)
                self.default_style = {"cursor": "default"}
            elif change["new"] == "个人数据资源":
                # search_box.placeholder = (
                #     "输入搜索的关键词，比如：dem"
                # )
                search_result_widget.children = [
                    search_type,
                    # search_box,
                    assets_combo,
                    search_output,
                ]

                # 逻辑操作
                self.default_style = {"cursor": "wait"}
                if not self.search_user_assets:
                    self.search_user_assets = _search_user_assets()
                asset_titles = [x["fullPath"] for x in self.search_user_assets]
                assets_dropdown.options = asset_titles
                if len(self.search_user_assets) > 0:
                    html_widget.value = _pie_user_asset_html(self.search_user_assets[0])
                with search_output:
                    search_output.clear_output()
                    display(html_widget)
                self.default_style = {"cursor": "default"}

        search_type.observe(search_type_changed, names="value")

        def search_box_callback(text):
            if text.value != "":
                with search_output:
                    search_output.clear_output()
                if search_type.value == "查询位置":
                    latlon = latlon_from_text(text.value)
                    if latlon:
                        if self.search_loc_marker is None:
                            marker = folium.Marker(
                                location=latlon,
                                draggable=False,
                                name="位置",
                            )
                            self.search_loc_marker = marker
                            marker.add_to(self)
                            self.setCenter(latlon[1], latlon[0], 8)
                        else:
                            marker = self.search_loc_marker
                            marker.location = (latlon[1], latlon[0])
                            self.setCenter(latlon[1], latlon[0], 8)
                    else:
                        print(f"找不到指定的位置：{latlon}")
                elif search_type.value == "公共数据集":
                    pass
                elif search_type.value == "个人数据资源":
                    pass
                else:
                    print("找不到输出结果")

        search_box.on_submit(search_box_callback)
        search_result_widget = widgets.VBox([search_type, search_box])

        return search_result_widget

    def toHtml(self, filename=None, **kwargs):
        """
        生成HTML
        :param filename:
        :param kwargs:
        :return:
        """
        if filename is not None:
            if not filename.endswith(".html"):
                raise ValueError("文件名称必须是html")
            filename = os.path.abspath(filename)
            out_dir = os.path.dirname(filename)
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)
            self.save(filename, **kwargs)
        else:
            filename = os.path.abspath(random_string() + ".html")
            self.save(filename, **kwargs)
            with open(filename) as f:
                lines = f.readlines()
                out_html = "".join(lines)
            os.remove(filename)
            return out_html

    def toStreamlitLayer(
            self,
            width=800,
            height=400,
            responsive=True,
            scrolling=False,
            add_layer_control=True,
            bidirectional=False,
            **kwargs,
    ):
        """
        渲染Streamlit地图
        :param width:
        :param height:
        :param responsive:
        :param scrolling:
        :param add_layer_control:
        :param bidirectional:
        :param kwargs:
        :return:
        """
        try:

            if add_layer_control:
                self.addLayerControl()

            if bidirectional:
                output = st_folium(self, width=width, height=height)
                return output
            else:
                if responsive:
                    make_map_responsive = """
                    <style>
                    [title~="st.iframe"] { width: 100%}
                    </style>
                    """
                    st.markdown(make_map_responsive, unsafe_allow_html=True)
                return components.html(
                    self.toHtml(height=f"{height}px"), width=width, height=height, scrolling=scrolling
                )

        except Exception as e:
            raise Exception(e)

    def addLocalRaster(self, imageFile, band=1, palette=None, layer_name=None):
        """
        加载本地的tif
        :param imageFile:
        :param band:
        :param palette:
        :param layer_name:
        :return:
        """
        check_package("localtileserver")
        from localtileserver import get_folium_tile_layer,TileClient

        if isinstance(imageFile, str):
            if not os.path.exists(imageFile):
                raise ValueError("The source path does not exist.")
        else:
            raise ValueError("The source must either be a string or TileClient")

        if layer_name is None:
            layer_name = os.path.basename(imageFile)
        port = "default"
        projection = "EPSG:3857"
        debug = False

        tile_client = TileClient(imageFile, port=port, debug=debug)
        tile_layer = get_folium_tile_layer(
            tile_client,
            port=port,
            debug=debug,
            projection=projection,
            band=band,
            palette=palette,
            name=layer_name
        )
        center = tile_client.center()
        tile_layer.add_to(self)
        self.centerObject(center)
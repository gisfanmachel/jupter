# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   pieleaflet.py
@Time    :   2020/8/6 下午5:19
@Author  :   liuxiaodong
@Version :   1.0
@Contact :   2152550864@qq.com
@License :   (C)Copyright 2019-2020, liuxiaodong
@Desc    :   None
"""
import math
import os
import time
import threading
import json
import random

from IPython.display import display
import ipywidgets as widgets
from ipyleaflet import Map, TileLayer, SplitMapControl, WMSLayer, WidgetControl, Marker, \
    VideoOverlay, ImageOverlay, GeoJSON, LayersControl, AwesomeIcon, SearchControl, \
    DrawControl, MeasureControl, ScaleControl, FullScreenControl, basemaps, link, \
    LayerGroup
import tempfile

from pie.utils.geoTools import latlon_from_text, screen_capture, getCenter
from pie.utils.common import render_size, random_string, rgb_to_hex, check_package,\
                              tms_to_geotiff, roi_to_bbox, find_pie_dir
from pie.utils.config import config
from pie.utils.pieHttp import GET, getUserInfo
from pie.utils.geoTools import create_code_cell
from pie.utils.basemapInfo import leaflet_basemap
from pie.vector.geometry import PIEGeometry
from pie.reducer import PIEReducer
from pie.map.leafletTileLayer import generateTileLayer
from pie.map.legends import builtin_legends
from pie.map.mapstyle import formatStyle
import streamlit as st
import streamlit.components.v1 as components
import ipytree

from pie.Classifier import sam


def _generatePIEMap(pre, statement):
    """
    生成 PIEMap 的对象
    :param pre:
    :param statement:
    :return:
    """
    _object = PIEMap()
    _object.pre = pre
    _object.statement = statement
    return _object

class PIEMap(Map):
    def __init__(self, center=None, zoom=10, sam = None, **kwargs):
        super(PIEMap, self).__init__(basemap=basemaps.Gaode.Satellite)
        self.pre = None
        self.statement = None
        
        self.layer_control = None
        self.screenshot = None
        self.search_locations = None
        self.search_common_datasets = None
        self.search_user_tree = None
        self.search_user_datasets = None
        self.search_loc_marker = None
        self.select_tag = None
        self.sam = sam
        self.user_rois = None
        self.user_roi = None
        self.draw_features = []
        self._initMap(center, zoom , **kwargs)

    def _initMap(self, center, zoom , **kwargs):
        """
        初始化地图
        :param center:
        :param zoom:
        :param kwargs:
        :return:
        """
        if center is None:
            center = [39.8948591963122,116.33867898233117]
        self.center = center
        self.zoom = zoom
        if "height" not in kwargs:
            self.layout.height = "500px"
        else:
            if isinstance(kwargs["height"], int) or isinstance(kwargs["height"], float):
                kwargs["height"] = f'{kwargs["height"]}px'
            self.layout.height = kwargs["height"]
        if "width" in kwargs:
            if isinstance(kwargs["width"], int) or isinstance(kwargs["width"], float):
                kwargs["width"] = f'{kwargs["width"]}px'
            self.layout.width = kwargs["width"]
        else:
            self.layout.width = "100%"
        self.touch_zoom = True
        self.scroll_wheel_zoom = True

        self._addBaseMap(kwargs.get("map_list"))
        self._addResourcePanel()
        # self._addWhiteBoxTools()
        self.add(FullScreenControl(position="topleft"))
        self.add(ScaleControl(position='bottomleft'))
        self._addDrawControl()
        self._addMeasureControl()
        self._addLayerControl()
        self._addShowLatLon()
        if self.sam is not None:
            self._addSamGeoControl()

    @staticmethod
    def name():
        return "PIEMap"

    def setCenter(self, lon, lat, zoom=None):
        """
        设置居中位置
        :param lon:
        :param lat:
        :param zoom:
        :return:
        """
        self.center = (lat, lon)
        if zoom is not None:
            self.zoom = zoom

    def _addBaseMap(self, map_list=None):
        """
        添加基础地图
        :param map_list:
        [
            {
                url: "xyz地图"
                name: "地图名称"
            }
        ]
        :return:
        """
        try:
            if map_list is None:
                self.add(leaflet_basemap()["GaodeVec"])
            else:
                for _info in map_list:
                    _url = _info.get("url")
                    _name = _info.get("name")
                    self.add(leaflet_basemap(_url, _name, _name))
        except Exception as e:
            print("addBasemap errors {}".format(e))

    def _addLayerControl(self):
        """
        添加基础控制图层
        :return:
        """
        try:
            self.layer_control = LayersControl(position='topright')
            self.add(self.layer_control)
        except Exception as e:
            print("addLayerControl errors {}".format(e))

    def _addMeasureControl(self):
        """
        Add measurement tools
        """
        measure = MeasureControl(position="topleft",
                                 active_color='#ABE67E',
                                 completed_color='#C8F2BE',
                                 primary_length_unit='meters',
                                 secondary_length_unit='feet',
                                 primary_area_unit='hectares',
                                 secondary_area_unit='sqmeters')
        self.add(measure)

    def _addDrawControl(self):
        """
        Add a drawing tool
        """
        draw_control = DrawControl()
        draw_control.polyline = {
            "shapeOptions": {
                "color": "#6bc2e5",
                "weight": 8,
                "opacity": 1
            }
        }
        draw_control.polygon = {
            "shapeOptions": {
                "fillColor": "#6be5c3",
                "color": "#6be5c3",
                "fillOpacity": 0.1
            },
            "drawError": {
                "color": "#dd253b",
                "message": "Oups!"
            },
            "allowIntersection": False
        }
        draw_control.circle = {
            "shapeOptions": {
                "fillColor": "#efed69",
                "color": "#efed69",
                "fillOpacity": 0.3
            }
        }
        draw_control.rectangle = {
            "shapeOptions": {
                "fillColor": "#fca45d",
                "color": "#fca45d",
                "fillOpacity": 0.3
            }
        }
        self.add(draw_control)

        def handle_draw(target, action, geo_json):
            if "style" in geo_json["properties"]:
                del geo_json["properties"]["style"]
            self.user_roi = geo_json
            if action in ["created", "edited"]:
                self.draw_features.append(geo_json)
            elif action == "deleted":
                geometries = [
                    feature["geometry"] for feature in self.draw_control.data
                ]
                for geom in geometries:
                    if geom == geo_json["geometry"]:
                        geometries.remove(geom)
                for feature in self.draw_features:
                    if feature["geometry"] not in geometries:
                        self.draw_features.remove(feature)
            self.user_rois = {
                "type": "FeatureCollection",
                "features": self.draw_features,
            }
        self.draw_control = draw_control
        draw_control.on_draw(handle_draw)

    def clear_drawings(self):
        self.draw_control.clear()
        self.draw_features = []
        self.user_rois = None
        self.user_roi = None

    def _addSearchControl(self):
        """
        Adding a Query Tool
        """
        marker = Marker(icon=AwesomeIcon(name="check", marker_color='green', icon_color='darkgreen'))
        search_control = SearchControl(
            position="topleft",
            url="'https://nominatim.openstreetmap.org/search?format=json&q={s}'",
            zoom=5,
            marker=marker
        )
        self.add(search_control)

    def _addSamGeoControl(self):
        '''
        Adding a segment tool
        '''
        self.add(leaflet_basemap()["GaodeImg"])
        self.default_style = {"cursor": "crosshair"}

        self.fg_markers = []
        self.bg_markers = []

        fg_layer = LayerGroup(layers=self.fg_markers, name="Foreground")
        bg_layer = LayerGroup(layers=self.bg_markers, name="Background")

        self.add(fg_layer)
        self.add(bg_layer)
        self.fg_layer = fg_layer
        self.bg_layer = bg_layer
        self.user_roi = None
        widget_width = "280px"
        button_width = "90px"
        padding = "0px 0px 0px 4px"  # upper, right, bottom, left
        style = {"description_width": "initial"}

        toolbar_button = widgets.ToggleButton(
        value=True,
        tooltip="Toolbar",
        icon="gear",
        layout=widgets.Layout(width="28px", height="28px", padding=padding),)
        
        close_button = widgets.ToggleButton(
        value=False,
        tooltip="Close the tool",
        icon="times",
        button_style="primary",
        layout=widgets.Layout(height="28px", width="28px", padding=padding),)

        roi_button = widgets.Button(

            description="创建ROI",
            button_style='info',
            layout=widgets.Layout(height="28px", width=widget_width, padding=padding),
        )


        # radio_buttons = widgets.RadioButtons(
        # options=["Foreground", "Background"],
        # value=None,
        # description="Class Type:",
        # disabled=False,
        # style=style,
        # layout=widgets.Layout(width=widget_width, padding=padding),)

        checkbox_label = widgets.Label(value='Class Type:')
        Foreground_cb =  widgets.Checkbox(description='Foreground')
        Background_cb =  widgets.Checkbox(description='Background')

        def handle_checkbox_change(change):
            if change['owner'] == Foreground_cb and Foreground_cb.value:
                Background_cb.value = False
            elif change['owner'] == Background_cb and Background_cb.value:
                Foreground_cb.value = False
        
        Foreground_cb.observe(handle_checkbox_change, names='value')
        Background_cb.observe(handle_checkbox_change, names='value')
        radio_buttons =  widgets.VBox([checkbox_label,Foreground_cb, Background_cb])
        fg_count = widgets.IntText(
            value=0,
            description="Foreground #:",
            disabled=True,
            style=style,
            layout=widgets.Layout(width="135px", padding=padding),
        )
        bg_count = widgets.IntText(
            value=0,
            description="Background #:",
            disabled=True,
            style=style,
            layout=widgets.Layout(width="135px", padding=padding),
        )

        segment_button = widgets.ToggleButton(
            description="Segment",
            value=False,
            button_style="primary",
            layout=widgets.Layout(padding=padding),
        )
        # save_button = widgets.ToggleButton(
        # description="Save", value=False, button_style="primary"
        # )
        reset_button = widgets.ToggleButton(
            description="Reset", value=False, button_style="primary"
        )
        segment_button.layout.width = button_width
        # save_button.layout.width = button_width
        reset_button.layout.width = button_width

        opacity_slider = widgets.FloatSlider(
            description="Mask opacity:",
            min=0,
            max=1,
            value=0.5,
            readout=True,
            continuous_update=True,
            layout=widgets.Layout(width=widget_width, padding=padding),
            style=style,
        )
        
        output = widgets.Output(
            layout=widgets.Layout(
                #  width=widget_width, padding=padding, max_width=widget_width,#overflow='auto',
                width='100%',
                height='auto',
                max_height='1000px',
                overflow="visible"#'hidden scroll',
            )
        )

        buttons = widgets.VBox(
            [   roi_button,
                radio_buttons,
                widgets.HBox([fg_count, bg_count]),
                opacity_slider,
                widgets.HBox(
                    [segment_button,  reset_button], #save_button,
                    layout=widgets.Layout(padding="0px 4px 0px 4px"),
                ),
            ]
        )

        toolbar_header = widgets.HBox()
        toolbar_header.children = [close_button,  toolbar_button]

        toolbar_footer = widgets.VBox()
        toolbar_footer.children = [
            buttons,
            output,
        ]
        toolbar_widget = widgets.VBox()
        toolbar_widget.children = [toolbar_header, toolbar_footer]

        def toolbar_btn_click(change):
            if change["new"]:
                close_button.value = False
                toolbar_widget.children = [toolbar_header, toolbar_footer]
            else:
                if not close_button.value:
                    toolbar_widget.children = [toolbar_button]
        toolbar_button.observe(toolbar_btn_click, "value")

        def close_btn_click(change):
            if change["new"]:
                toolbar_button.value = False
                # toolbar_widget.close()
                toolbar_widget.children = [toolbar_button]
        close_button.observe(close_btn_click, "value")

        TEMP_IMG_DIR = "temp_IMG"
        temp_dir_path = os.path.join(find_pie_dir(),TEMP_IMG_DIR)

        def roi_btn_click(button): 
            # print(self.user_rois)
            if button.description == "创建ROI":
                button.button_style = 'warning'
                button.description = "创建中,请等待..."
                bbox_list = roi_to_bbox(self.user_rois)
                temp_roi_path = os.path.join(temp_dir_path,'roi')
                print(f'找到路径{temp_roi_path}')

                if not os.path.exists(temp_roi_path):
                    os.makedirs(temp_roi_path)

                # 清空之前的文件
                for filename in os.listdir(temp_roi_path):
                    file_path = os.path.join(temp_roi_path, filename)
                    os.remove(file_path)
                print(f'已清空{temp_roi_path}')

                try:
                    for bbox in bbox_list:
                        with tempfile.NamedTemporaryFile(mode="w", suffix=".tif", dir=temp_roi_path,delete=False) as temp_file:
                            temp_file_name = temp_file.name
                            tms_to_geotiff(temp_file_name,bbox,self.zoom,overwrite=True)
                            # self.addLocalRaster(temp_roi_path + temp_file_name ) ## 可以试试513行 add与不add的区别
                            self.sam.set_image(temp_file_name)
                            print('sam image设置好了')
                    # 下载
                    button.button_style = 'success'
                    button.description = "成功创建"
                except Exception as e:
                    button.button_style = 'warning'
                    button.description = "创建失败"
                    print(f"创建失败，异常为：{e}")
            elif button.description == "创建失败" or "创建成功":
                button.description = "创建ROI"
                button.button_style = 'info'
                self.clear_drawings()
            else:
                pass
        roi_button.on_click(roi_btn_click)

        def handle_map_interaction(**kwargs):
            try:
                # print(kwargs.get("type"))
                if kwargs.get("type") == "click":
                # if kwargs.get("type") in ["dbclick", "contextmenu"]: # 右击是contextmenu，双击是dbclick 
                # if kwargs.get("type") == "contextmenu":
                    latlon = kwargs.get("coordinates")
                    if Foreground_cb.value:
                        marker = Marker(
                            location=latlon,
                            icon=AwesomeIcon(
                                name="plus-circle",
                                marker_color="green",
                                icon_color="darkred",
                            ),
                        )
                        fg_layer.add(marker)
                        self.fg_markers.append(marker)
                        fg_count.value = len(self.fg_markers)
                    elif Background_cb.value :
                        marker = Marker(
                            location=latlon,
                            icon=AwesomeIcon(
                                name="minus-circle",
                                marker_color="red",
                                icon_color="darkred",
                            ),
                        )
                        bg_layer.add(marker)
                        self.bg_markers.append(marker)
                        bg_count.value = len(self.bg_markers)

            except (TypeError, KeyError) as e:
                print(f"Error handling map interaction: {e}")

        self.on_interaction(handle_map_interaction)    

        def segment_button_click(change):
            if change["new"]:
                segment_button.value = False
                if len(self.fg_markers) == 0:
                    print("Please add some foreground markers.")
                    segment_button.value = False
                    return
                else:
                    try:
                        self.fg_points = [
                            [marker.location[1], marker.location[0]]
                            for marker in self.fg_markers
                        ]
                        self.bg_points = [
                            [marker.location[1], marker.location[0]]
                            for marker in self.bg_markers
                        ]
                        point_coords = self.fg_points + self.bg_points
                        point_labels = [1] * len(self.fg_points) + [0] * len(self.bg_points)
                        filename = "masks_"+ os.path.basename(self.sam.image)
                        out_dir =  os.path.join(temp_dir_path,'mask')
                        if not os.path.exists(out_dir):
                            os.mkdir(out_dir)
                        MAX_FILE_AGE = 3600  # 1 hour
                        def cleanup_temp_files(tempdir):
                            """Remove all temporary files in the TEMP_PY_DIR directory that are older than MAX_FILE_AGE"""
                            now = time.time()
                            for _filename in os.listdir(tempdir):
                                file_path = os.path.join(tempdir, _filename)
                                if os.stat(file_path).st_mtime < now - MAX_FILE_AGE:
                                    os.remove(file_path)
                        cleanup_temp_files(out_dir)
                        filename = os.path.join(out_dir, filename)
                        self.sam.predict(
                            point_coords=point_coords,
                            point_labels=point_labels,
                            point_crs="EPSG:4326",
                            output=filename,
                        )
                        print('mask已经生成到',filename)

                        if self.find_layer("Masks") is not None:
                            self.remove_layer(self.find_layer("Masks"))

                        if hasattr(self.sam, "prediction_fp") and os.path.exists(
                            self.sam.prediction_fp
                        ):
                            os.remove(self.sam.prediction_fp)
                        # Skip the image layer if localtileserver is not available
                        try:
                            self.addLocalRaster(
                                filename,
                                palette ="Blues",
                                opacity=opacity_slider.value,
                                layer_name="Masks",
                                zoom_to_layer=True,
                            )
                        except:
                            pass
                        segment_button.value = False
                    except Exception as e:
                        segment_button.value = False
                        print(e)
        segment_button.observe(segment_button_click, "value")

        def opacity_changed(change):
            if change["new"]:
                mask_layer = self.find_layer("Masks")
                if mask_layer is not None:
                    mask_layer.interact(opacity=opacity_slider.value)
        opacity_slider.observe(opacity_changed, "value")

        def reset_button_click(change):
            if change["new"]:
                segment_button.value = False
                # save_button.value = False
                reset_button.value = False
                opacity_slider.value = 0.5
                output.clear_output()

                roi_button.description = "创建ROI"
                roi_button.button_style = 'info'

                try:
                    
                    self.remove_layer(self.find_layer("Masks"))
                    self.clear_drawings()
                    with output:
                            print('drawing_clearing')
                    if hasattr(self, "fg_markers"):
                        self.user_rois = None
                        self.fg_markers = []
                        self.bg_markers = []
                        self.fg_points = []
                        self.bg_points = []
                        
                        self.fg_layer.clear_layers()
                        self.bg_layer.clear_layers()
                        fg_count.value = 0
                        bg_count.value = 0
                    os.remove(sam.prediction_fp)
                    self.remove_layer(self.find_layer("Masks"))
                except:
                    pass
        reset_button.observe(reset_button_click, "value")
        toolbar_control = WidgetControl(widget=toolbar_widget, position='topright')
        self.add(toolbar_control)

    def _addShowLatLon(self):
        """
        添加显示经纬度
        :return:
        """
        label = widgets.HTML()
        latLonControl = WidgetControl(widget=label, position='bottomright')
        self.add(latLonControl)
        def handle_interaction(**kwargs):
            _type = kwargs.get('type')
            if _type == 'mousemove':
                _coords = kwargs.get('coordinates')
                label.value = f"<div>纬度:{_coords[0]:.3f}<br/>经度:{_coords[1]:.3f}<br/>分辨率:{self.getScale():.1f}米</div>"
            elif _type == "mouseout":
                label.value = ""
        self.on_interaction(handle_interaction)

    def addLayer(self, pieObject, style=None, name="layer", visible=True, opacity=1.0):
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
        self.add(tileLayer)
    
    def getLayerNames(self):
        """Gets layer names as a list.

        Returns:
            list: A list of layer names.
        """
        layer_names = []

        for layer in list(self.layers):
            if len(layer.name) > 0:
                layer_names.append(layer.name)

        return layer_names

    def imgInfo(self, pieImage):
        """
        点击影像获取指定信息。
        :param pieImage:
        :return:
        """
        output_widget = widgets.Output(layout={'border': '1px solid black'})
        output_control = WidgetControl(widget=output_widget, position='bottomright')
        self.add(output_control)

        def handle_interaction(**kwargs):
            latlon = kwargs.get('coordinates')
            if kwargs.get('type') == 'click':
                point = PIEGeometry.Point([latlon[1], latlon[0]], None)
                reducer = PIEReducer().mean()
                scale = self.getScale()
                imgInfo = pieImage.reduceRegion(reducer, point, scale)
                self.default_style = {'cursor': 'wait'}
                with output_widget:
                    output_widget.clear_output()
                    print(imgInfo.getInfo())
                self.default_style = {'cursor': 'crosshair'}
        self.on_interaction(handle_interaction)

    def addGeoJSON(self, jsonfile, name="geojson"):
        """
        Load the JSON file
        args:
            jsonfile: the path of local json file
        """
        if name is None:
            name = str(jsonfile)

        with open(jsonfile, 'r', encoding="utf-8") as f:
            data = json.load(f)

        def random_color(feature):
            return {
                'color': 'black',
                'fillColor': random.choice(['red', 'yellow', 'green', 'orange']),
            }

        geo_json = GeoJSON(
            data=data,
            style={
                'opacity': 1,
                'fillOpacity': 0.8,
                'weight': 1
            },
            style_callback=random_color,
            hover_style={
                'color': 'red', 'fillOpacity': 0.5
            },
            name=name
        )
        self.add(geo_json)

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
            'attribution': attribution,
            'name': name
        }
        img_overlay = ImageOverlay(**kwargs)
        self.add(img_overlay)

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
            'url': url,
            'bounds': bounds,
            'attribution': attribution,
            'name': name
        }
        vid_overlay = VideoOverlay(**kwargs)
        self.add(vid_overlay)

    def getScale(self):
        """Returns the approximate pixel scale of the current map view, in meters.
        Returns:
            float: Map resolution in meters.
        """
        zoomLevel = self.zoom
        resolution = 156543.04 * math.cos(0) / math.pow(2, zoomLevel)
        # print("地图分辨率：", resolution)
        return resolution

    def findLayer(self, name):
        """
        Finds layer by name
        Args:
            name (str): Name of the layer to find.

        Returns:
            object: ipyleaflet layer object.
        """
        layers = self.layers
        for layer in layers:
            if layer.name == name:
                return layer
        return None

    def layerOpacity(self, name, value=1.0):
        """
        Changes layer opacity.
        Args:
            name (str): The name of the layer to change opacity.
            value (float, optional): The opacity value to set. Defaults to 1.0.
        """

        layer = self.findLayer(name)
        try:
            layer.opacity = value
        except Exception as e:
            print(e)

    def layerName(self, oldName, newName):
        """
        change the layer name
        args:
            name: the layer name
        """

        layer = self.findLayer(oldName)
        try:
            layer.name = newName
        except Exception as e:
            print(e)

    def centerObject(self, pieObject, zoom=None):
        """
        设置居中显示
        :param pieObject:
        :param zoom:
        :return:
        """
        _lon, _lat, _zoom = getCenter(pieObject, zoom)
        self.setCenter(_lon, _lat, _zoom)

    def splitMap(self, left_layer_name, right_layer_name):
        """
        分屏地图
        :param left_layer_name:
        :param right_layer_name:
        :return:
        """
        try:
            left_layer = None
            right_layer = None
            for layer in self.layers:
                if layer.name == left_layer_name:
                    left_layer = layer
                elif layer.name == right_layer_name:
                    right_layer = layer
            if not left_layer or not right_layer:
                return
            control = SplitMapControl(
                left_layer=left_layer, right_layer=right_layer
            )
            self.add(control)
        except Exception as e:
            print(e, "\n", 'The provided layers are invalid!')

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
            tileLayer = TileLayer(
                url=url,
                name=name,
                attribution=attribution,
                opacity=opacity,
                visible=True
            )
            self.add(tileLayer)
        except Exception as e:
            print(e, '\n', "Failed to add the specified tileLayer.")

    def addMiniMap(self, zoom=6, position="bottomright"):
        """
        添加缩略图
        :param zoom:
        :param position:
        :return:
        """
        minimap = Map(
            zoom_control=False,
            attribution_control=False,
            zoom=zoom,
            center=self.center,
            layers=[
                TileLayer(
                    url="https://webrd01.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}",
                    attribution='高德地图',
                    name='高德地图'
                )
            ]
        )
        minimap.layout.width = '135px'
        minimap.layout.height = '135px'
        link((minimap, 'center'), (self, 'center'))
        minimap_control = WidgetControl(widget=minimap, position=position)
        self.add(minimap_control)

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
            wmsLayer = WMSLayer(
                url=url,
                layers=layers,
                name=name,
                attribution=attribution,
                format=format,
                transparent=transparent,
                opacity=opacity,
                visible=True
            )
            self.add(wmsLayer)
        except Exception as e:
            print(e, '\n', "Failed to add the specified wms tilelayer.")

    def addLegend(self,
                  title='Legend',
                  legend_dict=None,
                  labels=None,
                  colors=None,
                  position='bottomright',
                  builtin_legend=None,
                  layer_name=None,
                  **kwargs):
        """
        添加图例
        :param title:
        :param legend_dict:
        :param labels:
        :param colors:
        :param position:
        :param builtin_legend:
        :param layer_name:
        :param kwargs:
        :return:
        """
        import pkg_resources
        from IPython.display import display

        pkg_dir = os.path.dirname(
            pkg_resources.resource_filename("pie", "/pieleaflet.py")
        )
        legend_template = os.path.join(pkg_dir, "data/templates/legend.html")

        if "min_width" not in kwargs.keys():
            min_width = None
        else:
            min_width = kwargs["min_width"]
        if "max_width" not in kwargs.keys():
            max_width = None
        else:
            max_width = kwargs["max_width"]
        if "min_height" not in kwargs.keys():
            min_height = None
        else:
            min_height = kwargs["min_height"]
        if "max_height" not in kwargs.keys():
            max_height = None
        else:
            max_height = kwargs["max_height"]
        if "height" not in kwargs.keys():
            height = None
        else:
            height = kwargs["height"]
        if "width" not in kwargs.keys():
            width = None
        else:
            width = kwargs["width"]

        if width is None:
            max_width = "300px"
        if height is None:
            max_height = "400px"

        if not os.path.exists(legend_template):
            print("The legend template does not exist.")
            return

        if labels is not None:
            if not isinstance(labels, list):
                print("The legend keys must be a list.")
                return
        else:
            labels = ["One", "Two", "Three", "Four", "etc"]

        if colors is not None:
            if not isinstance(colors, list):
                print("The legend colors must be a list.")
                return
            elif all(isinstance(item, tuple) for item in colors):
                try:
                    colors = [rgb_to_hex(x) for x in colors]
                except Exception as e:
                    print(e)
            elif all((item.startswith("#") and len(item) == 7) for item in colors):
                pass
            elif all((len(item) == 6) for item in colors):
                pass
            else:
                print("The legend colors must be a list of tuples.")
                return
        else:
            colors = [
                "#8DD3C7",
                "#FFFFB3",
                "#BEBADA",
                "#FB8072",
                "#80B1D3",
            ]

        if len(labels) != len(colors):
            print("The legend keys and values must be the same length.")
            return

        allowed_builtin_legends = builtin_legends.keys()
        if builtin_legend is not None:
            if builtin_legend not in allowed_builtin_legends:
                print(
                    "The builtin legend must be one of the following: {}".format(
                        ", ".join(allowed_builtin_legends)
                    )
                )
                return
            else:
                legend_dict = builtin_legends[builtin_legend]
                labels = list(legend_dict.keys())
                colors = list(legend_dict.values())

        if legend_dict is not None:
            if not isinstance(legend_dict, dict):
                print("The legend dict must be a dictionary.")
                return
            else:
                labels = list(legend_dict.keys())
                colors = list(legend_dict.values())
                if all(isinstance(item, tuple) for item in colors):
                    try:
                        colors = [rgb_to_hex(x) for x in colors]
                    except Exception as e:
                        print(e)

        allowed_positions = [
            "topleft",
            "topright",
            "bottomleft",
            "bottomright",
        ]
        if position not in allowed_positions:
            print(
                "The position must be one of the following: {}".format(
                    ", ".join(allowed_positions)
                )
            )
            return

        header = []
        content = []
        footer = []

        with open(legend_template) as f:
            lines = f.readlines()
            lines[3] = lines[3].replace("Legend", title)
            header = lines[:6]
            footer = lines[11:]

        for index, key in enumerate(labels):
            color = colors[index]
            if not color.startswith("#"):
                color = "#" + color
            item = "      <li><span style='background:{};'></span>{}</li>\n".format(
                color, key
            )
            content.append(item)

        legend_html = header + content + footer
        legend_text = "".join(legend_html)

        try:

            legend_output_widget = widgets.Output(
                layout={
                    # "border": "1px solid black",
                    "max_width": max_width,
                    "min_width": min_width,
                    "max_height": max_height,
                    "min_height": min_height,
                    "height": height,
                    "width": width,
                    "overflow": "scroll",
                }
            )
            legend_control = WidgetControl(
                widget=legend_output_widget, position=position
            )
            legend_widget = widgets.HTML(value=legend_text)
            with legend_output_widget:
                display(legend_widget)

            self.legend_widget = legend_output_widget
            self.legend_control = legend_control
            self.add(legend_control)

        except Exception as e:
            raise Exception(e)

    def addMarker(self, latlon, draggable=False, name="marker"):
        if not latlon:
            print("请输入具体位置")
            return
        marker = Marker(
            location=latlon,
            draggable=draggable,
            name=name
        )
        self.add(marker)

    def addLocalRaster(self, imageFile, band=1, palette=None, layer_name=None,**kwargs):
        """
        加载本地的tif
        :param imageFile:
        :param band:
        :param palette:
        :param layer_name:
        :return:
        """
        check_package("localtileserver")
        from localtileserver import get_leaflet_tile_layer,TileClient

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
        tile_layer = get_leaflet_tile_layer(
            tile_client,
            port=port,
            debug=debug,
            projection=projection,
            band=band,
            palette=palette,
            name=layer_name,
            **kwargs,
        )
        center = tile_client.center()
        self.add(tile_layer)
        self.centerObject(center)

    def playLayersAnimation(self, layers, style, loop=-1):
        """
        :param layers:
        [{layer: layer, name: name}]
        :param style:
        :param loop:
        :return:
        """
        if not isinstance(layers, list):
            raise ValueError("layers只能是列表")

        for layer in layers:
            self.addLayer(layer.get("layer"), style, layer.get("name"))
            self.layerOpacity(layer.get("name"), 0)
        self.layerOpacity(layers[0].get("name"), 1)
        labels = [_layer.get("name") for _layer in layers]

        slider = widgets.IntSlider(value=None, min=1, max=len(layers), step=1, readout=False, continuous_update=False,
                                   layout=widgets.Layout(width="200px"))
        label = widgets.Label(value=labels[0], layout=widgets.Layout(padding="0px, 5px, 0px, 5px"))
        playBtn = widgets.Button(icon="play", tooltip="the play the slider", botton_style="primary",
                                 layout=widgets.Layout(width="32px"))
        closeBtn = widgets.Button(icon="close", tooltip="the close the slider", botton_style="primary",
                                  layout=widgets.Layout(width="32px"))
        pauseBtn = widgets.Button(icon="pause", tooltip="the pause the slider", boton_style="primary",
                                  layout=widgets.Layout(width="32px"))

        playChk = widgets.Checkbox(value=False)
        sliderBox = widgets.HBox([slider, label, playBtn, pauseBtn, closeBtn])

        def play_click(b):
            playChk.value = True

            def play(slider):
                _loop = 0
                while playChk.value:
                    if slider.value < len(labels):
                        slider.value += 1
                    else:
                        slider.value = 1
                        _loop += 1
                        playChk.value = loop == -1 or _loop <= loop
                        if not playChk.value:
                            _loop = 0
                    time.sleep(1)

            thread = threading.Thread(target=play, args=(slider,))
            thread.start()

        playBtn.on_click(play_click)

        def pause_click(b):
            playChk.value = False

        pauseBtn.on_click(pause_click)

        def close_click(b):
            playChk.value = False
            slider.value = 0

        closeBtn.on_click(close_click)

        def slider_observe(change):
            index = int(slider.value) - 1
            label.value = labels[index]
            for i in range(len(layers)):
                if i != index:
                    self.layerOpacity(layers[i].get("name"), 0)
                else:
                    self.layerOpacity(layers[i].get("name"), 1)

        slider.observe(slider_observe, "value")

        slider_control = WidgetControl(widget=sliderBox, position="topright")
        self.add(slider_control)

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

    def toLocalApp(self, outfile, title='pieMap', width='100%', height='600px'):
        """
        导出为html
        :param outfile:
        :param title:
        :param width:
        :param height:
        :return:
        """
        try:
            if not outfile.endswith('.html'):
                print("The output file must end with .html")
                return

            outdir = os.path.dirname(outfile)
            if not os.path.exists(outdir):
                os.makedirs(outdir)

            before_width = self.layout.width
            before_height = self.layout.height

            if not isinstance(width, str):
                print("width must be a string.")
                return
            elif width.endswith('px') or width.endswith('%'):
                pass
            else:
                print("width must end with px or %")
                return

            if not isinstance(height, str):
                print("height is a string.")
                return
            elif not height.endswith('px'):
                print("height must end with px.")
                return

            self.layout.width = width
            self.layout.height = height

            self.save(outfile, title=title)

            self.layout.width = before_width
            self.layout.height = before_height

            new_lines = []
            with open(outfile) as f:
                lines = f.readlines()
                cdn_url = "https://cdnjs.cloudflare.com/ajax/libs/require.js"
                new_cdn_url = "https://cdn.bootcdn.net/ajax/libs/require.js"
                for line in lines:
                    if cdn_url in line:
                        line = line.replace(cdn_url, new_cdn_url)
                    new_lines.append(line)
            out_html = "".join(new_lines)
            os.remove(outfile)
            with open(outfile, "w") as f:
                f.write(out_html)

        except Exception as e:
            print(e)
    
    def toStreamlitLayer(
        self, width=800, height=400, responsive=True, scrolling=False, **kwargs
    ):
        """
        生成Streamlit的图层
        :param width:
        :param height:
        :param responsive:
        :param scrolling:
        :param kwargs:
        :return:
        """
        try:
            if responsive:
                make_map_responsive = """
                <style>
                [title~="st.iframe"] { width: 100%}
                </style>
                """
                st.markdown(make_map_responsive, unsafe_allow_html=True)
            return components.html(
                self.toHtml(), width=width, height=height, scrolling=scrolling
            )

        except Exception as e:
            raise Exception(e)

    def toHtml(
        self,
        outfile=None,
        title="My Map",
        width="100%",
        height="600px",
        add_layer_control=True,
        **kwargs,
    ):
        """
        保存文件为HTML
        :param outfile:
        :param title:
        :param width:
        :param height:
        :param add_layer_control:
        :param kwargs:
        :return:
        """
        try:

            save = True
            if outfile is not None:
                if not outfile.endswith(".html"):
                    raise ValueError("The output file extension must be html.")
                outfile = os.path.abspath(outfile)
                out_dir = os.path.dirname(outfile)
                if not os.path.exists(out_dir):
                    os.makedirs(out_dir)
            else:
                outfile = os.path.abspath(random_string() + ".html")
                save = False

            if add_layer_control and self.layer_control is None:
                layer_control = LayersControl(position="topright")
                self.layer_control = layer_control
                self.add(layer_control)

            before_width = self.layout.width
            before_height = self.layout.height

            if not isinstance(width, str):
                print("width must be a string.")
                return
            elif width.endswith("px") or width.endswith("%"):
                pass
            else:
                print("width must end with px or %")
                return

            if not isinstance(height, str):
                print("height must be a string.")
                return
            elif not height.endswith("px"):
                print("height must end with px")
                return

            self.layout.width = width
            self.layout.height = height

            self.save(outfile, title=title, **kwargs)

            self.layout.width = before_width
            self.layout.height = before_height

            if not save:
                out_html = ""
                with open(outfile) as f:
                    lines = f.readlines()
                    out_html = "".join(lines)
                os.remove(outfile)
                return out_html

        except Exception as e:
            raise Exception(e)

    def _addResourcePanel(self):
        search_button = widgets.ToggleButton(
            value=False,
            tooltip="资源集合",
            icon="database",
            layout=widgets.Layout(
                width="28px", height="28px", padding="0px 0px 0px 3px"
            )
        )

        search_type = widgets.ToggleButtons(
            options=["查询位置","公共数据集", "个人数据资源"],
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

        common_assets_dropdown = widgets.Dropdown(
            options=[],
            layout=widgets.Layout(min_width="311px", max_width="311px")
        )

        user_assets_tree = ipytree.Tree(
            nodes=[],
            layout=widgets.Layout(min_width="311px",
                                  max_width="311px",
                                  max_height="100px",
                                  overflow="scroll")
        )

        import_btn = widgets.Button(
            description="导入",
            button_style="primary",
            tooltip="点击导入引入资源",
            layout=widgets.Layout(min_width="57px", max_width="57px")
        )

        def import_btn_clicked(change):
            if self.select_tag == "公共数据集":
                if common_assets_dropdown.value is not None:
                    dropdown_index = common_assets_dropdown.index
                    dataset_uid = "dataset_" + random_string(string_length=3)
                    datasets = self.search_common_datasets
                    dataset = datasets[dropdown_index]
                    _id = dataset["id"]
                    if dataset.get("category") == "raster":
                        content = f"{dataset_uid} = pie.ImageCollection('{_id}')"
                    else:
                        content = f"{dataset_uid} = pie.FeatureCollection('{_id}')"
                    create_code_cell(content)
                else:
                    print("查找数据资源失败！")
                    return
            if self.select_tag == "个人数据资源":
                file_path = change['owner'].name
                if file_path is not None:
                    selected_dataset = self.search_user_datasets.get(file_path, None)
                    if not selected_dataset:
                        return
                    dataset_uid = "dataset_" + random_string(string_length=3)
                    _type = selected_dataset.get("type")
                    if _type == 2:
                        content = f"{dataset_uid} = pie.ImageCollection('{file_path}')"
                        create_code_cell(content)
                    elif _type == 3:
                        content = f"{dataset_uid} = pie.Image('{file_path}')"
                        create_code_cell(content)
                    elif _type == 4:
                        content = f"{dataset_uid} = pie.FeatureCollection('{file_path}')"
                        create_code_cell(content)
                    else:
                        print("找不到指定的类型")
                else:
                    print("查找数据资源失败！")
                    return


        import_btn.on_click(import_btn_clicked)

        html_widget = widgets.HTML()

        def dropdown_change(change):
            dropdown_index = common_assets_dropdown.index
            if dropdown_index is not None and dropdown_index >= 0:
                with search_output:
                    search_output.clear_output(wait=True)
                    print("Loading ...")
                    if self.select_tag == "公共数据集":
                        datasets = self.search_common_datasets
                        dataset = datasets[dropdown_index]
                        dataset_html = _pie_dataset_html(dataset)
                        html_widget.value = dataset_html
                        search_output.clear_output(wait=True)
                        display(html_widget)
                    else:
                        print("查找数据资源失败！")

        common_assets_dropdown.observe(dropdown_change, names="value")

        def tree_selected(event):
            if event['new']:
                fullPath = event['owner'].name
                value = self.search_user_datasets.get(fullPath, None)
                if not value:
                    return
                with search_output:
                    search_output.clear_output(wait=True)
                    print("Loading ...")
                    if self.select_tag == "个人数据资源":
                        dataset_html = _pie_user_asset_html(value)
                        html_widget.value = dataset_html
                        search_output.clear_output(wait=True)
                        display(html_widget)
                    else:
                        print("查找数据资源失败！")

        common_assets_combo = widgets.HBox()
        common_assets_combo.children = [import_btn, common_assets_dropdown]

        user_assets_combo = widgets.HBox()
        user_assets_combo.children = [import_btn, user_assets_tree]

        def search_btn_click(change):
            if change["new"]:
                search_widget.children = [search_button, search_result_widget]
                search_type.value = "查询位置"
            else:
                search_widget.children = [search_button]
                search_result_widget.children = [search_type, search_box]

        search_button.observe(search_btn_click, "value")

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
                    title = asset.get("title"),
                    start_time = asset.get("start_time"),
                    end_time = asset.get("end_time"),
                    snippet = asset.get("snippet"),
                    desc = asset.get("desc"),
                    id = asset.get("id"),
                    link=asset.get("link"),
                    thumbnail=asset.get("thumbnail")
                )
            except Exception as e:
                print(e)
            return text

        def _search_user_tree():
            urlInfo = config.getQueryCatalogURL()
            tree = ipytree.Tree()
            user = getUserInfo()
            name = user.get("name", None)
            root_node = ipytree.Node(f"user/{name}", icon="folder")

            def tree_get(url_Info):
                response = GET(url_Info)
                _data = response.get("data", [])
                _data = sorted(_data, key=lambda x: (x["type"], x['fullPath']))

                nodes = []
                _result = {}
                for file in _data:
                    _full_path = file.get("fullPath", "")
                    if not _full_path:
                        continue
                    _type = file.get("type")
                    _keys = _full_path.split("/")
                    if _type == 1:
                        node = ipytree.Node(_keys[-1], icon="folder")
                        node.open_icon = "plus-square"
                        node.open_icon_style = "success"
                        node.close_icon = "minus-square"
                        node.close_icon_style = "info"
                        node.opened = False
                        _url = urlInfo.get("url") + "?" + "parentId={}".format(file["uuid"])
                        _urlInfo = {"url": _url, "x-api": urlInfo.get("x-api")}
                        sub_nodes, sub_result = tree_get(_urlInfo)
                        _result.update(sub_result)
                        node.nodes = sub_nodes
                        nodes.append(node)
                    elif _type == 2 or _type == 3 or _type == 4:
                        _node_key = "/".join(_keys[2:])
                        nodes.append(ipytree.Node(_node_key, icon="file"))
                        _result[_node_key] = file
                return nodes, _result

            root_node.nodes, result = tree_get(urlInfo)
            root_node.open_icon = "plus-square"
            root_node.open_icon_style = "success"
            root_node.close_icon = "minus-square"
            root_node.close_icon_style = "info"
            root_node.opened = False
            tree.add_node(root_node)
            return tree, result

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
                if _type == 2 or _type==1:
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
            common_assets_dropdown.options = []
            self.select_tag = change['new']
            if change["new"] == "查询位置":
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
                    common_assets_combo,
                    search_output,
                ]
                # 逻辑操作
                self.default_style = {"cursor": "wait"}
                if not self.search_common_datasets:
                    self.search_common_datasets = _search_dataset()
                asset_titles = [x["title"] for x in self.search_common_datasets]
                common_assets_dropdown.options = asset_titles
                if len(self.search_common_datasets) > 0:
                    html_widget.value = _pie_dataset_html(self.search_common_datasets[0])
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
                    user_assets_combo,
                    search_output,
                ]

                # 逻辑操作
                self.default_style = {"cursor": "wait"}
                if not self.search_user_tree:
                    self.search_user_tree, self.search_user_datasets = _search_user_tree()
                user_assets_tree.nodes = self.search_user_tree.nodes
                if len(self.search_user_datasets) > 0:
                    key, value = list(self.search_user_datasets.items())[0]
                    html_widget.value = _pie_user_asset_html(value)
                with search_output:
                    search_output.clear_output()
                    display(html_widget)
                def traverse_node(node):
                    node.observe(tree_selected, 'selected')
                    if node.nodes:
                        for child_node in node.nodes:
                            node.observe(tree_selected, 'selected')
                            traverse_node(child_node)
                traverse_node(user_assets_tree)
                self.default_style = {"cursor": "default"}

        search_type.observe(search_type_changed, names="value")

        def search_box_callback(text):
            print(text.value)
            print(search_type.value)
            if text.value != "":
                with search_output:
                    search_output.clear_output()
                if search_type.value == "查询位置":
                    latlon = latlon_from_text(text.value)
                    if latlon:
                        if self.search_loc_marker is None:
                            marker = Marker(
                                location=latlon,
                                draggable=False,
                                name="位置",
                            )
                            self.search_loc_marker = marker
                            self.add(marker)
                            self.center = latlon
                        else:
                            marker = self.search_loc_marker
                            marker.location = latlon
                            self.center = latlon
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
        search_widget = widgets.HBox([search_button])

        data_control = WidgetControl(widget=search_widget, position="topleft")
        self.add(data_control)

    # def _addWhiteBoxTools(self):
    #     """
    #     Add Whiteboxgui in the map.
    #     @return:popup whiteboxgui window
    #     """
    #     toolbar_grid = widgets.GridBox(
    #         children=[widgets.ToggleButton(layout=widgets.Layout(
    #             width="auto", height="auto", padding="0px 0px 0px 0px"
    #         ), icon="wrench", tooltip="whitebox")],
    #         layout=widgets.Layout(
    #             width="31px",
    #             grid_template_columns="31px",
    #             grid_template_rows="31px",
    #             grid_gap="0px 0px",
    #             padding="0px")
    #     )
    #
    #     def tool_callback(change):
    #         if change["new"]:
    #             for tool in toolbar_grid.children:
    #                 tool.value = False
    #             tool = change["owner"]
    #             tool_name = tool.tooltip
    #             if tool_name == "whitebox":
    #                 tools_dict = wbt.get_wbt_dict()
    #                 wbt_toolbox = wbt.build_toolbox(tools_dict, max_width="800px", max_height="300px")
    #                 wbt_control = WidgetControl(widget=wbt_toolbox, position="topright")
    #                 self.add(wbt_control)
    #     for tool in toolbar_grid.children:
    #         tool.observe(tool_callback, "value")
    #
    #     toolbar_control = WidgetControl(widget=toolbar_grid, position="topright")
    #     self.add(toolbar_control)

    def find_layer(self, name):
        """
        """
        layers = self.layers

        for layer in layers:
            if layer.name == name:
                return layer
        return None
    
    # # def add_raster(self,source,band=None, palette=None,vmin=None,vmax=None
    #                ,nodata=None,attribution=None,layer_name="Local COG",zoom_to_layer=True,**kwargs,):
    #     tile_layer, tile_client = get_local_tile_layer(
    #         source,
    #         band=band,
    #         palette=palette,
    #         vmin=vmin,
    #         vmax=vmax,
    #         nodata=nodata,
    #         attribution=attribution,
    #         layer_name=layer_name,
    #         return_client=True,
    #         **kwargs,
    #     )


    #     self.add(tile_layer)
    #     bounds = tile_client.bounds() 
    #     bounds = (
    #         bounds[2],
    #         bounds[0],
    #         bounds[3],
    #         bounds[1],
    #     )  # [minx, miny, maxx, maxy]
    #     if zoom_to_layer:
    #         self.zoom_to_bounds(bounds)

    #     arc_add_layer(tile_layer.url, layer_name, True, 1.0)
    #     if zoom_to_layer:
    #         arc_zoom_to_extent(bounds[0], bounds[1], bounds[2], bounds[3])

    #     if not hasattr(self, "cog_layer_dict"):
    #         self.cog_layer_dict = {}
    #     band_names = list(tile_client.metadata()["bands"].keys())
    #     params = {
    #         "tile_layer": tile_layer,
    #         "tile_client": tile_client,
    #         "band": band,
    #         "band_names": band_names,
    #         "bounds": bounds,
    #         "type": "LOCAL",
    #     }
    #     self.cog_layer_dict[layer_name] = params


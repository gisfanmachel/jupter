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
import numpy as np
import time
import csv
import matplotlib.colors as colors
import xarray as xr
# import whiteboxgui.whiteboxgui as wbt
import threading
from random import randrange, randint
import json
# import geopandas as gpd
# import rioxarray
from traitlets import link, default, Unicode, Union, Dict, Instance
import ipywidgets as widgets
from ipywidgets import jslink, ColorPicker
from bqplot import pyplot as plt
from ipyleaflet import Map, TileLayer, SplitMapControl, WMSLayer, LegendControl, WidgetControl, Marker, MarkerCluster, \
    VideoOverlay, ImageOverlay, GeoJSON, LayersControl, basemap_to_tiles, AwesomeIcon, SearchControl, \
    DrawControl, MeasureControl, Polyline, Polygon, ScaleControl, FullScreenControl, Heatmap, GeoData, ZoomControl
from ipyleaflet.velocity import Velocity
from .utils.common import encodeJSON, encodeURIComponent
from .utils.config import config
from .utils.http import POST, GET
from .utils.common import calculate_center_coordinates, random_color
from .utils.geoTools import screen_capture, csv_to_txt, csv_to_shp
from .piebasemaps import pie_basemaps
from .featureCollection import PIEFeatureCollection
from .geometry import PIEGeometry
from .reducer import PIEReducer
from .image import PIEImage
from .feature import PIEFeature
from .imageCollection import PIEImageCollection

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
    def __init__(self, center=None, zoom=10, **kwargs):
        super().__init__()
        if center is None:
            center = [39.8948591963122,
                      116.33867898233117]
        self.pre = None
        self.statement = None
        self.center = center
        self.zoom = zoom
        self.touch_zoom = True
        self.scroll_wheel_zoom = True
        # 暂时屏蔽
        # self.__addSearchDataSet()
        self.add_control(ScaleControl(position='bottomleft'))
        self.add_control(FullScreenControl())
        self.__measuremap()
        self.__drawcontrol()
        self.__searchcontrol()
        self.__latlonpupop()
        self._addBasemap()
        # 暂时屏蔽
        # self.__addUserAsset()
        # 暂时屏蔽
        # self.addWhiteBoxTools()
        # self.tileLayer = tileLayer

        # self.__search_data()
        # self.addIndexModel()

        if 'zoom_control' not in kwargs.keys():
            kwargs['zoom_control'] = True

        # Collection of drawing tools and widgets
        self.random_marker = None
        self.plot_widget = None
        self.plot_control = None
        self.plot_marker_cluster = MarkerCluster(name="Marker Cluster")

        self.pie_raster_layers = []
        self.pie_layers = []
        self.pie_raster_layers = []
        self.pie_layer_names = []
        self.pie_layer_dict = {}
        self.pie_raster_layer_names = []

        # Dropdown widget for plotting
        self.plot_dropdown_control = None
        self.plot_dropdown_widget = None
        self.chart_points = []
        self.chart_labels = []
        self.chart_values = []

        self.search_locations = None
        self.search_datasets = None
        self.search_loc_marker = None

        search_type = widgets.ToggleButtons(options=['name/address', 'lat-lng', 'data'],
                                            tooltips=['Search by place name or address',
                                                      'Search by lat-lng coordinates', 'Search PIE Engine data catalog'])
        search_type.style.button_width = '100px'
        search_output = widgets.Output(layout={'max_width': '340px',
                                               'max_height': '250px',
                                               'overflow': 'scroll'})
        search_results = widgets.RadioButtons()

        search_box=  widgets.Text(placeholder='Search by place name or address', tooltip='Search location')
        search_box.layout.width = '340px'

        # Add button click
        assets_dropdown = widgets.Dropdown()
        assets_dropdown.layout.min_width = '279px'
        assets_dropdown.layout.max_width = '279px'
        assets_dropdown.options = []

        import_btn = widgets.Button(
            description='import',
            button_style='primary',
            tooltip='Click to import the selected asset',
        )
        import_btn.layout.min_width = '57px'
        import_btn.layout.max_width = '57px'

        # import_btn.on_click(import_btn_clicked)
        html_widget = widgets.HTML()

        assets_combo = widgets.HBox()
        assets_combo.children = [import_btn, assets_dropdown]

        search_widget = widgets.HBox()
        data_control = WidgetControl(widget=search_widget, position='topleft')

        search_result_widget = widgets.VBox()
        search_result_widget.children = [search_type, search_box]


        draw_control_lite = DrawControl(marker={}, rectangle={'shapeOptions': {'color': '#0000FF'}}, circle={'shapeOptions': {'color': '#0000FF'}},
                                        circlemarker={}, polyline={}, polygon={})

        self.draw_control_lite = draw_control_lite

        # Dropdown widget for plotting
        self.plot_dropdown_control = None
        self.plot_dropdown_widget = None
        self.plot_options = {}

        self.plot_coordinates = []
        self.plot_markers = []
        self.plot_last_click = []
        self.plot_all_clicks = []

        # def handle_interaction(**kwargs):
        #     latlon = kwargs.get("coordinates")
        #     if kwargs.get("type") == "click":
        #         self.default_style = {"cursor": "wait"}
        #         self.chart_points.append(latlon)
        #         self.default_style = {'cursor': 'crosshair'}
        # self.on_interaction(handle_interaction)

    @staticmethod
    def name():
        return "PIEMap"

    def setCenter(self, lon, lat, zoom=None):
        self.center = (lat, lon)
        if zoom is not None:
            self.zoom = zoom

    # use GaoDeMap as the basemap
    basemap = Union((Dict(), Instance(TileLayer)),
                    default_value=dict(
                        # url="http://t1.tianditu.gov.cn/img_w/wmts?tk=1e5a8aeb87fbf336c3d7780f91b7fdfc&SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=img&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}",
                        url="https://webst04.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}",
                        max_zoom=19,
                        attribution="Map data (c) PIE-Engine Studio",
                        name="高德地图"
                    ))
    mapsdate = Unicode('today').tag(sync=True)

    @default("layers")
    def _default_layers(self):
        basemap = self.basemap if isinstance(self.basemap, TileLayer) \
            else basemap_to_tiles(self.basemap, self.mapsdate)
        basemap.base = True
        return (basemap,)


    def _addBasemap(self):
        """
        Add Base Layer
        """
        try:
            self.add_layer(pie_basemaps['Gaode'])
            self.add_layer(pie_basemaps['TDT_ibo'])
            self.add_layer(pie_basemaps['TDT_cia'])
            self.layer_control = LayersControl(position='topright')
            self.add_control(self.layer_control)
        except Exception as e:
            print("addBasemap existx errors {}".format(e))

    def addBasemap(self, map='Gaode'):
        """
        Add Base Layer
        args:
            map: a map name from pie_basemaps
        """
        # self.remove_layer(pie_basemaps[map])
        try:
            self.add_layer(pie_basemaps[map])
        except Exception as e:
            print("Basemap can only be one of the following:\n {}".format(
                '\n '.join(pie_basemaps.keys())
            ))
            print("addBasemap exists error %e" % e)

    def addImageToMap(self, pieObject, style, name, visible, opacity):
        """
        Add the RS image to map.
        @param pieObject:the PIEImage or PIEImageCollection
        @param style:the style of show in the map
        @param name:layer name
        @param visible:True or False
        @param opacity
        @return:
        """
        _opacity = opacity
        if style:
            if "opacity" in style:
                _opacity = style.get("opacity")
        else:
            style = {}
        style['opacity'] = _opacity
        statement = encodeURIComponent(encodeJSON(pieObject.statement))
        render_style = encodeURIComponent(encodeJSON(style))
        params = {
            "statement": statement,
            "style": render_style
        }
        _layerUrl = config.getLayerURL()
        # print(_layerUrl)
        response = POST(_layerUrl, params)
        # print(response)
        if response:
            _data = response.get("data", {})
            _id = _data.get("id")
            _url = _data.get("url")
            kwargs = {
                "url": config.getTilesURL(_url).get("url"),
                "name": name
            }
        else:
            return
        tilelayer = TileLayer(
            url=kwargs.get("url"),
            attribution="Pie Engine Image",
            name=kwargs.get('name'),
            show_loading=True,
            visible=visible,
        )

        # __data = data.get("data").get("data")
        # # __data = PIEArray(__data)
        # # __data = np.array(__data, np.uint8)
        # # url = config.getTilesURL(_url),
        # _tileLayer = self.tileLayer(
        #                             url=kwargs.get("url"),
        #                             attribution="image000",
        #                             name="image000",
        #                             buffer=0,
        #                             # path="D:/work6/test.png",
        #                             image_value=data,
        #                             value=__data)
        # __tileLayer = VectorTileLayer(vector_tile_layer_styles=data)
        self.add_layer(tilelayer)

    def addLayer(self, pieObject, style, name, visible=True, opacity=1.0):
        """
        Add a image layer to the map
        args:
            pieObject: a RS image or geometry from pie engine
            style: a show style of the pieObject
            name: the name of pieObject to show in the topright layerControl widget
        """

        if isinstance(pieObject, PIEImage) or isinstance(pieObject, PIEImageCollection):
            self.addImageToMap(pieObject, style, name, visible, opacity=opacity)
        elif isinstance(pieObject, PIEGeometry):
            coordinates = pieObject.getInfo().get("coordinates")
            if not style.get("color"):
                _color = "red"
            else:
                _color = style.get("color")
            _polygon = Polygon(locations=coordinates, color=_color, fill=False, name=name, weight=3, opacity=opacity)
            self.add_layer(_polygon)

        elif isinstance(pieObject, PIEFeature):
            coordinates = pieObject.geometry().getInfo().get('coordinates')
            if not style.get("color"):
                _color = "red"
            else:
                _color = style.get("color")
            _feature = Polygon(locations=coordinates, color=_color, fill=False, name=name, weight=3, opacity=opacity)
            self.add_layer(_feature)

        elif isinstance(pieObject, PIEFeatureCollection):
            index = 0
            coordinatesList = []
            number = int(pieObject.size().getInfo())
            if number > 1:
                while index <= number-1:
                    coordinates = pieObject.getAt(index).geometry().getInfo().get("coordinates")
                    coordinatesList.append(coordinates)
                    index = index + 1
            else:
                coordinatesList = pieObject.getAt(0).geometry().getInfo().get("coordinates")
            if not style.get("color"):
                _color = "red"
            else:
                _color = style.get("color")

            _line = Polyline(locations=coordinatesList, color=_color, fill=False, name=name, weight=3, opacity=opacity)
            self.add_layer(_line)
        else:
            print("The pieObject must be the follows object: {}".format("PIEImage, PIEImageCollection, PIEGeometry, PIEFeature, PIEFeatureCollection"))


    def __measuremap(self):
        """
        Add measurement tools
        """
        measure = MeasureControl(position="bottomleft",
                                 active_color='#ABE67E',
                                 completed_color='#C8F2BE',
                                 primary_length_unit='meters',
                                 secondary_length_unit='feet',
                                 primary_area_unit='hectares',
                                 secondary_area_unit='sqmeters')
        self.add_control(measure)

    def __drawcontrol(self):
        """
        Add a drawing tool
        """
        draw_control = DrawControl()
        draw_control.polyline = {
            "shapeOptions":{
                "color": "#6bc2e5",
                "weight": 8,
                "opacity": 1.0
            }
        }
        draw_control.polygon = {
            "shapeOptions": {
                "fillColor": "#6be5c3",
                "color": "#6be5c3",
                "fillOpacity": 1.0
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
                "fillOpacity": 1.0
            }
        }
        draw_control.rectangle = {
            "shapeOptions": {
                "fillColor": "#fca45d",
                "color": "#fca45d",
                "fillOpacity": 1.0
            }
        }

        self.add_control(draw_control)

    def __searchcontrol(self):
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
        self.add_control(search_control)

    def splitMap(self, left_map, right_map):
        """
        Displays different maps left and right
        args：
            left_map: the map name in the left
            right_map: the map name in the right
        """
        global left_layer, right_layer
        try:
            if left_map in pie_basemaps.keys():
                left_layer = pie_basemaps[left_map]
            if right_map in pie_basemaps.keys():
                right_layer = pie_basemaps[right_map]
            control = SplitMapControl(
                left_layer=left_layer, right_layer=right_layer
            )
            self.add_control(control)
        except Exception as e:
            print(e, "\n", 'The provided layers are invalid!')

    def layerControl(self, layer_map, position, name):
        """
        Add custom map to layer
        args：
            layer_map: a map url
            position: topright\topleft\bottomright\bottomleft
            name: the name of map
        """
        layer_map = basemap_to_tiles(layer_map)
        self.add_layer(layer_map)
        control = LayersControl(position=position, name=name)
        self.add_control(control)

    def __latlonpupop(self):
        """
        Click on the map to show latitude and longitude
        """
        output_widget = widgets.Output(layout={'border': '1px solid black'})
        output_control = WidgetControl(widget=output_widget, position='bottomright')
        self.add_control(output_control)
        def handle_interaction(**kwargs):
            latlon = kwargs.get('coordinates')
            if kwargs.get('type') == 'click':
                self.default_style = {'cursor': 'wait'}
                with output_widget:
                    output_widget.clear_output()
                    print(latlon)
                self.default_style = {'cursor': 'crosshair'}
        self.on_interaction(handle_interaction)

    def imgInfo(self, pieImage):
        """
        Click on the image to display the pixel value or area
        args:
            image: a image to show the map
        """
        output_widget = widgets.Output(layout={'border': '1px solid black'})
        output_control = WidgetControl(widget=output_widget, position='bottomright')
        self.add_control(output_control)
        def handle_interaction(**kwargs):
            latlon = kwargs.get('coordinates')
            geometry = PIEGeometry()
            point = geometry.Point([latlon[1], latlon[0]], None)
            polygon = PIEGeometry.Polygon([
                [
                    120.25399999999945,
                    41.80396593974288
                ],
                [
                    120.42978124999689,
                    41.713817711114245
                ],
                [
                    120.23202734374973,
                    41.48377827918594
                ],
                [
                    120.25399999999945,
                    41.80396593974288
                ]
            ], None)
            imginfo = pieImage.reduceRegion(PIEReducer.mean(), point, None)
            area = 100.00
            if kwargs.get('type') == 'click':
                self.default_style = {'cursor': 'wait'}
                with output_widget:
                    output_widget.clear_output()
                    print("Area:", area)
                self.default_style = {'cursor': 'crosshair'}
        self.on_interaction(handle_interaction)

    def marker(self, location, draggable, name="Marker"):
        """
        Add tag
        args:
            location: the list style location to show the map, like [lat, lon]
            draggable: a bool value of the control to marker drag, value is 1 or 0
        """
        marker = Marker(location=location, draggable=draggable, name=name)
        self.add_layer(marker)

    def geoJson(self, jsonfile, name=None):
        """
        Load the JSON file
        args:
            jsonfile: the path of local json file
        """
        if name is None:
            name = str(jsonfile)

        with open(jsonfile, 'r') as f:
            data = json.load(f)
        geo_json = GeoJSON(data=data,
                           style={
                                'opacity': 1, 'dashArray': '9', 'fillOpacity': 0.1, 'weight': 1
                           },
                           hover_style={
                               'color': 'white', 'dashArray': '0', 'fillOpacity': 0.5
                           },
                           style_callback=None,
                           name=name
                           )
        self.add_layer(geo_json)

    # def geoData(self, datapath, name=None):
    #     """
    #     Loading geographic data
    #     args:
    #         datapath: the local path of geographic data
    #     """
    #     if name is None:
    #         name = str(datapath)
    #
    #     data = gpd.read_file(datapath)
    #     geodata = GeoData(geo_dataframe=data,
    #                       style={'color': 'black', 'fillColor': '#3366cc', 'opacity': 0.05, 'weight': 1.9,
    #                              'dashArray': '2', 'fillOpacity': 0.6},
    #                       hover_style={'fillColor': 'red', 'fillOpacity': 0.2},
    #                       name=name
    #                       )
    #     self.add_layer(geodata)

    def imageOverlay(self, url, bounds, attribution="", name=None):
        """
        Load the image file on the map
        https://ipyleaflet.readthedocs.io/en/latest/api_reference/image_video_overlay.html
        args:
            url: string, default ""
                Url to the local or remote image file.
            bounds: list, default [0., 0]
                SW and NE corners of the image.
            attribution: string, default ""
                Image attribution.
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
        self.add_layer(img_overlay)

    def videoOverlay(self, url, bounds, attribution="", name=None):
        """
        Load the video file on the map
        Args:
            url: string, default ""
        Url to the local or remote video file.
            bounds: list, default [0., 0]
        SW and NE corners of the video.
            attribution: string, default ""
        Video attribution.
        """
        if (name is None):
            name = str(url)

        kwargs = {
            'url': url,
            'bounds': bounds,
            'attribution': attribution,
            'name': name
        }
        vid_overlay = VideoOverlay(**kwargs)
        self.add_layer(vid_overlay)

    def getScale(self):
        """Returns the approximate pixel scale of the current map view, in meters.
        Returns:
            float: Map resolution in meters.
        """
        zoomLevel = self.zoom
        resolution = 156543.04 * math.cos(0) / math.pow(2, zoomLevel)
        print("地图分辨率：", resolution)


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
        """Centers the map view on a given object.
        Args:
            PIEObject: An PIE Engine object to center on - a geometry, image or feature.
            zoom (int, optional): The zoom level, from 1 to 24. Defaults to None.
        """
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
        self.setCenter(lon, lat, zoom)

    def addTileLayer(self, url, name=None, attribution="", opacity=1):
        """Adds a TileLayer to the map.
        Args:
            url (str, optional): The URL of the tile layer. Defaults to 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'.
            name (str, optional): The layer name to use for the layer. Defaults to None.
            attribution (str, optional): The attribution to use. Defaults to ''.
            opacity (float, optional): The opacity of the layer. Defaults to 1.
            shown (bool, optional): A flag indicating whether the layer should be on by default. Defaults to True.
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
            self.add_layer(tileLayer)
        except Exception as e:
            print(e, '\n', "Failed to add the specified tileLayer.")

    def addMiniMap(self, zoom=6, position="bottomright"):
        """Adds a minimap (overview) to the ipyleaflet map.
        Args:
            zoom (int, optional): Initial map zoom level. Defaults to 5.
            position (str, optional): Position of the minimap. Defaults to "bottomright".
        """
        minimap = Map(
            zoom_control=False, attribution_control=False,
            zoom=zoom, center=self.center, layers=[pie_basemaps['Gaode']]
        )

        minimap.layout.width = '135px'
        minimap.layout.height = '135px'
        link((minimap, 'center'), (self, 'center'))
        minimap_control = WidgetControl(widget=minimap, position=position)
        self.add_control(minimap_control)

    def addWmsLyaer(self, url, layers, name=None, attribution='', format='image/jpeg', transparent=False, opacity=1.0):
        """
        Add a wms layer to the map.
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
            self.add_layer(wmsLayer)
        except Exception as e:
            print(e, '\n', "Failed to add the specified wms tilelayer.")

    def markerCluster(self):
        """Adds a marker cluster to the map and returns a list of pie.feature, which can be accessed using PIEMap.markerCluster.
        Returns:
            object: a list of pie.feature
        """
        coordinates = []
        markers = []
        marker_cluster = MarkerCluster(name="Marker Cluster")
        self.last_click = []
        self.all_clicks = []
        self.pie_markers = []
        self.add_layer(marker_cluster)
        def handle_interaction(**kwargs):
            latlon = kwargs.get('coordinates')
            if kwargs.get('type') == 'click':
                coordinates.append(latlon)
                geom = PIEGeometry.Point((latlon[1], latlon[0]), "EPSG3857")
                feature = PIEFeature(geom)
                self.pie_markers.append(feature)
                self.last_click = latlon
                self.all_clicks = coordinates
                markers.append(Marker(location=latlon, rise_on_hover=True))
                marker_cluster.markers = markers
                marker_cluster.set_trait("markers", (10, 10))
            elif kwargs.get('type') == 'mousemove':
                pass
            self.default_style = {'cursor': 'crosshair'}
        self.on_interaction(handle_interaction)

    def setPlotOptions(self, add_marker_cluster=False, sample_scale=None, plot_type=None, overlay=False, position='bottomright', min_width=None, max_width=None, min_height=None, max_height=None, **kwargs):
        """Sets plotting options.
        Args:
            add_marker_cluster (bool, optional): Whether to add a marker cluster. Defaults to False.
            sample_scale (float, optional):  A nominal scale in meters of the projection to sample in . Defaults to None.
            plot_type (str, optional): The plot type can be one of "None", "bar", "scatter" or "hist". Defaults to None.
            overlay (bool, optional): Whether to overlay plotted lines on the figure. Defaults to False.
            position (str, optional): Position of the control, can be ‘bottomleft’, ‘bottomright’, ‘topleft’, or ‘topright’. Defaults to 'bottomright'.
            min_width (int, optional): Min width of the widget (in pixels), if None it will respect the content size. Defaults to None.
            max_width (int, optional): Max width of the widget (in pixels), if None it will respect the content size. Defaults to None.
            min_height (int, optional): Min height of the widget (in pixels), if None it will respect the content size. Defaults to None.
            max_height (int, optional): Max height of the widget (in pixels), if None it will respect the content size. Defaults to None.
        """
        plot_options_dict = {}
        plot_options_dict['add_marker_cluster'] = add_marker_cluster
        plot_options_dict['sample_scale'] = sample_scale
        plot_options_dict['plot_type'] = plot_type
        plot_options_dict['overlay'] = overlay
        plot_options_dict['position'] = position
        plot_options_dict['min_width'] = min_width
        plot_options_dict['max_width'] = max_width
        plot_options_dict['min_height'] = min_height
        plot_options_dict['max_height'] = max_height

        for key in kwargs.keys():
            plot_options_dict[key] = kwargs[key]

        self.plot_options = plot_options_dict

        if add_marker_cluster and (self.plot_marker_cluster not in self.layers):
            self.add_layer(self.plot_marker_cluster)

    def plot(self, x, y, plot_type=None, overlay=False, position='bottomright', min_width=None, max_width=None, min_height=None, max_height=None, **kwargs):
        """Creates a plot based on x-array and y-array data.
        Args:
            x (numpy.ndarray or list): The x-coordinates of the plotted line.
            y (numpy.ndarray or list): The y-coordinates of the plotted line.
            plot_type (str, optional): The plot type can be one of "None", "bar", "scatter" or "hist". Defaults to None.
            overlay (bool, optional): Whether to overlay plotted lines on the figure. Defaults to False.
            position (str, optional): Position of the control, can be ‘bottomleft’, ‘bottomright’, ‘topleft’, or ‘topright’. Defaults to 'bottomright'.
            min_width (int, optional): Min width of the widget (in pixels), if None it will respect the content size. Defaults to None.
            max_width (int, optional): Max width of the widget (in pixels), if None it will respect the content size. Defaults to None.
            min_height (int, optional): Min height of the widget (in pixels), if None it will respect the content size. Defaults to None.
            max_height (int, optional): Max height of the widget (in pixels), if None it will respect the content size. Defaults to None.
        """
        if self.plot_widget is not None:
            plot_widget = self.plot_widget
        else:
            plot_widget = widgets.Output(layout={"border": "1px solid black"})
            plot_control = WidgetControl(widget=plot_widget, position=position, min_width=min_width,
                                         max_width=max_width, min_height=min_height, max_height=max_height)
            self.plot_widget = plot_widget
            self.plot_control = plot_control
            self.add_control(plot_control)

        if max_width is None:
            max_width = 500
        if max_height is None:
            max_height = 300

        if (plot_type is None) and ('markers' not in kwargs.keys()):
            kwargs['markers'] = 'circle'

        with plot_widget:
            try:
                fig = plt.figure(1, **kwargs)
                if max_width is not None:
                    fig.layout.width = str(max_width) + 'px'
                if max_height is not None:
                    fig.layout.height = str(max_height) + 'px'

                plot_widget.clear_output(wait=True)
                if not overlay:
                    plt.clear()

                if plot_type is None:
                    if 'marker' not in kwargs.keys():
                        kwargs['marker'] = 'circle'
                    plt.plot(x, y, **kwargs)
                elif plot_type == 'bar':
                    plt.bar(x, y, **kwargs)
                elif plot_type == 'scatter':
                    plt.scatter(x, y, **kwargs)
                elif plot_type == 'hist':
                    plt.hist(y, **kwargs)
                plt.show()
            except Exception as e:
                print(e, '\n', "Failed to create plot.")

    def plotDemo(self, iterations=10, plot_type=None, overlay=False, position='bottomright', min_width=None, max_width=None, min_height=None, max_height=None, **kwargs):
        """A demo of interactive plotting using random pixel coordinates.
        Args:
            iterations (int, optional): How many iterations to run for the demo. Defaults to 20.
            plot_type (str, optional): The plot type can be one of "None", "bar", "scatter" or "hist". Defaults to None.
            overlay (bool, optional): Whether to overlay plotted lines on the figure. Defaults to False.
            position (str, optional): Position of the control, can be ‘bottomleft’, ‘bottomright’, ‘topleft’, or ‘topright’. Defaults to 'bottomright'.
            min_width (int, optional): Min width of the widget (in pixels), if None it will respect the content size. Defaults to None.
            max_width (int, optional): Max width of the widget (in pixels), if None it will respect the content size. Defaults to None.
            min_height (int, optional): Min height of the widget (in pixels), if None it will respect the content size. Defaults to None.
            max_height (int, optional): Max height of the widget (in pixels), if None it will respect the content size. Defaults to None.
        """
        if self.random_marker is not None:
            self.remove_layer(self.random_marker)

        image = PIEImage('LC08/01/T1').select([0, 1, 2, 3, 4, 6])
        self.addLayer(image, {"bands": ['B4', 'B3', 'B2'], 'gamma': 1.4}, "LC08/01/T1")

        self.setCenter(-50.078877, 25.190030, 3)
        band_names = image.bandNames().getInfo()
        # band_count = len(band_names)

        latitudes = np.random.uniform(30, 48, size=iterations)
        longitudes = np.random.uniform(-121, -76, size=iterations)

        marker = Marker(location=(0, 0))
        self.random_marker = marker
        self.add_layer(marker)

        for i in range(iterations):
            try:
                coordinate = PIEGeometry.Point([longitudes[i], latitudes[i]])
                dict_values = image.sample(coordinate).first().toDictionary().getInfo()
                band_values = list(dict_values.values())
                title = '{}/{}: Spectral signature at ({}, {})'.format(i+1, iterations,
                                                                       round(latitudes[i], 2), round(longitudes[i], 2))
                marker.location = (latitudes[i], longitudes[i])
                self.plot(band_names, band_values, plot_type=plot_type, overlay=overlay,
                          min_width=min_width, max_width=max_width, min_height=min_height, max_height=max_height, title=title, **kwargs)
                time.sleep(0.3)
            except Exception as e:
                print(e)

    def plotRaster(self, pieObject=None, sample_scale=None, plot_type=None, overlay=False, position='bottomright', min_width=None, max_width=None, min_height=None, max_height=None, **kwargs):
        """Interactive plotting of PIE Engine data by clicking on the map.
        Args:
            ee_object (object, optional): The pie.Image or pie.ImageCollection to sample. Defaults to None.
            sample_scale (float, optional): A nominal scale in meters of the projection to sample in. Defaults to None.
            plot_type (str, optional): The plot type can be one of "None", "bar", "scatter" or "hist". Defaults to None.
            overlay (bool, optional): Whether to overlay plotted lines on the figure. Defaults to False.
            position (str, optional): Position of the control, can be ‘bottomleft’, ‘bottomright’, ‘topleft’, or ‘topright’. Defaults to 'bottomright'.
            min_width (int, optional): Min width of the widget (in pixels), if None it will respect the content size. Defaults to None.
            max_width (int, optional): Max width of the widget (in pixels), if None it will respect the content size. Defaults to None.
            min_height (int, optional): Min height of the widget (in pixels), if None it will respect the content size. Defaults to None.
            max_height (int, optional): Max height of the widget (in pixels), if None it will respect the content size. Defaults to None.

        """
        if self.plot_control is not None:
            del self.plot_widget
            self.remove_layer(self.plot_control)
        if self.random_marker is not None:
            self.remove_layer(self.random_marker)

        plot_widget = widgets.Output(layout={'border': '0.5px solid black'})
        plot_contorl = WidgetControl(widget=plot_widget, position=position, min_width=min_width,
                                     max_width=max_width, min_height=min_height, max_height=max_height)
        self.plot_widget = plot_widget
        self.plot_control = plot_contorl
        self.add_control(plot_contorl)

        self.default_style = {'cursor': 'crosshair'}
        msg = "The plot function can only be used on pie.Image or pie.ImageCollection with more than one band."
        if (pieObject is None) and len(self.pie_raster_layers) > 0:
            pieObject = self.pie_raster_layers[-1]
            if isinstance(pieObject, PIEImageCollection):
                pieObject = pieObject.mosaic()
        elif isinstance(pieObject, PIEImageCollection):
            pieObject = pieObject.mosaic()
        elif not isinstance(pieObject, PIEImage):
            print(msg)
            return

        if sample_scale is None:
            sample_scale = self.getScale()
        if max_width is None:
            max_width = 500

        band_names = pieObject.bandNames().getInfo()

        coordinates = []
        markers = []
        marker_cluster = MarkerCluster(name="Marker Cluster")
        self.last_click = []
        self.all_clicks = []
        self.add_layer(marker_cluster)

        def handle_interaction(**kwargs2):
            latlon = kwargs2.get('coordinates')
            if kwargs2.get('type') == 'click':
                try:
                    coordinates.append(latlon)
                    self.last_click = latlon
                    self.all_clicks = coordinates
                    markers.append(Marker(location=latlon))
                    marker_cluster.markers = markers
                    self.default_style = {'cursor': 'wait'}
                    xy = PIEGeometry.Point(latlon[::-1])
                    dict_values = pieObject.sample(
                        xy, scale=sample_scale
                    ).first().toDictionary().getInfo()
                    band_values = list(dict_values.values())
                    self.plot(band_names, band_values, plot_type=plot_type, overlay=overlay,
                              min_width=min_width, max_width=max_width, min_height=min_height, max_height=max_height, **kwargs)
                    self.default_style = {'cursor': 'crosshair'}
                except Exception as e:
                    if self.plot_widget is not None:
                        with self.plot_widget:
                            self.plot_widget.clear_output()
                            print("No data for the clicked location")
                    else:
                        print(e)
                    self.default_style = {'cursor': 'crosshair'}
        self.on_interaction(handle_interaction)

    def basemapDemo(self):
        """A demo for using piemap basemaps.

        """
        mapName = [key for key in pie_basemaps.keys()]
        dropdown = widgets.Dropdown(
            options=mapName,
            value='Gaode',
            description='PIEBasemaps'
        )

        def on_click(change):
            basemap_name = change['new']
            old_basemap = self.layers[-1]
            self.substitute_layer(old_basemap, pie_basemaps[basemap_name])

        dropdown.observe(on_click, 'value')
        basemap_control = WidgetControl(widget=dropdown, position='topright')
        self.remove_control(self.inspector_control)
        self.add_control(basemap_control)

    def toImage(self, outfile=None, monitor=1):
        """
        Save the map to a image.
        """

        if outfile is None:
            outfile = os.path.join(os.getcwd(), 'Mymap.png')

        if outfile.endswith('.png') or outfile.endswith('.jpg'):
            pass
        else:
            print('The output file must be a PNG or JPG image.')
            return
        work_dir = os.path.dirname(outfile)
        if not os.path.exists(work_dir):
            os.makedirs(work_dir)

        self.screenshot =  screen_capture(outfile, monitor)

    def toHtml(self, outfile, title='Mymap', width='100%', height='880px'):
        """
        Save the map as a html file.
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
        except Exception as e:
            print(e)

    def extractValues(self, filename):
        """
        Extract pixel values to a csv file.
        """
        filename = os.path.abspath(filename)
        allowed_formats = ['csv', 'shp', 'txt']
        file_format = filename[-3:]

        if file_format not in allowed_formats:
            print("The output file must be one of the following: {}".format(", ".join(allowed_formats)))
            return None

        outdir = os.path.dirname(filename)
        outcsv = filename[:-3] + 'csv'
        outshp = filename[:-3] + 'shp'
        outtxt = filename[:-3] + 'txt'
        if not os.path.exists(outdir):
            os.makedirs(outdir)

        count = len(self.chart_points)
        if self.chart_labels == None: self.chart_labels.append("{}".format(filename))
        out_list = []
        if count > 0:
            header = ['id', 'longitude', 'latitude'] + self.chart_labels
            out_list.append(header)

            for i in range(0, count):
                id = i + 1
                line = [id] + self.chart_points[i]
                out_list.append(line)

            with open(outcsv , "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(out_list)

            if file_format == 'csv':
                print("The csv lat-lon file has been saved to: {}".format(outcsv))
            elif file_format == 'txt':
                csv_to_txt(outcsv, outtxt)
                print("The txt lat-lon file has been saved to: {}".format(outtxt))
            else:
                csv_to_shp(outcsv, outshp)
                print("The shapefile lat-lon has been saved to: {}".format(outshp))

    def saveClickPoints(self, filepath):
        """
        Save lat-lon points
        @param filepath:save file path
        @return:
        """

        def handle_interaction(**kwargs):
            latlon = kwargs.get("coordinates")
            if kwargs.get("type") == "click":
                self.default_style = {"cursor": "wait"}
                self.chart_points.append(latlon)
                self.extractValues(filename=filepath)
                self.default_style = {'cursor': 'crosshair'}
        self.on_interaction(handle_interaction)

    # def addLocalRaster(self, imagefile, bands=1, layer_name=None, colormap=None, x_dim='x', y_dim='y'):
    #     """
    #     Load the local image to map.
    #     :param imagefile:
    #     :param bands:
    #     :param layer_name:
    #     :param colormap:
    #     :param x_dim:
    #     :param y_dim:
    #     :return:
    #     """
    #     try:
    #         if not os.path.exists(imagefile):
    #             print("the {} file is not exists".format(imagefile))
    #             return False
    #         if layer_name is None:
    #             imageName = os.path.basename(imagefile)
    #             layer_name = str(imageName)
    #         if colormap is None:
    #             colormap = colors.XKCD_COLORS["xkcd:purple"]
    #
    #         data = rioxarray.open_rasterio(imagefile, masked=True).sel(bands)
    #         data_layer = data.plot(x_dim=x_dim, y_dim=y_dim, colormap=colormap)
    #         data_layer.name = layer_name
    #
    #     except Exception as e:
    #         print(e)


    def removeDrawn(self):
        """
        Remove user drawn geometries from the map.
        """
        if self.draw_layer is not None:
            self.remove_layer(self.draw_layer)
            self.draw_count = 0
            self.draw_features = []
            self.draw_last_feature = None
            self.draw_layer = None
            self.draw_last_json = None
            self.draw_last_bounds = None
            self.user_roi = None
            self.user_rois = None
            self.chart_values = []
            self.chart_points = []
            self.chart_labels = None

    def heatMap(self, locations, radius, min_opacity, gradient):
        """
        Show the heat map
        @param locations: just like the [[uniform(31, 41), uniform(31, 41)] for i in range(20000)]
        @param radius: int
        @param min_opacity: 0.0~1.0
        @param gradient: just like the {0.3: 'green', 0.5: 'cyan', 0.6: 'lime', 0.7: 'yellow', 1.0: 'red'}
        @return: 
        """
        heatmap = Heatmap(locations=locations, radius=radius, min_opacity=min_opacity, graident=gradient)
        self.add_layer(heatmap)

    def velocityMap(self, data, velocity_scale=0.01, max_velocity=20, **kwargs):
        """
        Show the velocity data in the map
        @param data: the *.nc format of data
        @param velocity_scale:
        @param max_velocity:
        @param kwargs:
        @return:
        """
        data = xr.open_dataset(data)
        _zonal_speed = kwargs.get("zonal_speed", 'u_wind')
        _meridional_speed = kwargs.get("meridional_speed", 'v_wind')
        _latitude_dimension = kwargs.get("latitude_dimension", 'lat')
        _longitude_dimension = kwargs.get("longitude_dimension", 'lon')
        displayOptions = {'velocityType': 'Global Wind',
                'displayPosition': 'bottomleft',
                'displayEmptyString': 'No wind data'}
        _display_options = kwargs.get("display_options", displayOptions)
        velocity_data = Velocity(data=data,
                 zonal_speed=_zonal_speed,
                 meridional_speed=_meridional_speed,
                 latitude_dimension=_latitude_dimension,
                 longitude_dimension=_longitude_dimension,
                 velocity_scale=velocity_scale,
                 max_velocity=max_velocity,
                 display_options=_display_options)
        self.add_layer(velocity_data)
    # TODO:LSW 暂时屏蔽
    # def addWhiteBoxTools(self):
    #     """
    #     Add Whiteboxgui in the map.
    #     @return:popup whiteboxgui window
    #     """
    #     toolbar_grid = widgets.GridBox(children=[widgets.ToggleButton(layout=widgets.Layout(
    #         width="auto", height="auto", padding="0px 0px 0px 0px"
    #     ), button_style="success", icon="wrench", tooltip="whitebox",)],
    #         layout=widgets.Layout(width="31px", grid_template_columns="31px",
    #                               grid_template_rows="31px",
    #                               grid_gap="0px 0px",
    #                               padding="0px"),)
    #
    #     def tool_callback(change):
    #         if change["new"]:
    #             for tool in toolbar_grid.children:
    #                 tool.value = False
    #             tool = change["owner"]
    #             tool_name = tool.tooltip
    #             if tool_name == "whitebox":
    #                 tools_dict = wbt.get_wbt_dict()
    #                 wbt_toolbox = wbt.build_toolbox(tools_dict, max_width="800px", max_height="500px")
    #                 wbt_control = WidgetControl(widget=wbt_toolbox, position="bottomleft")
    #                 self.add_control(wbt_control)
    #     for tool in toolbar_grid.children:
    #         tool.observe(tool_callback, "value")
    #
    #     toolbar_control = WidgetControl(widget=toolbar_grid, position="topleft")
    #     self.add_control(toolbar_control)

    def addTimeSlider(self, pieObject:(PIEImageCollection or PIEFeatureCollection), style:dict, name=None):
        """
        Show the time series image or imageCollection in the map.
        @param pieObject:PIEImageCollection
        @param style:show style in the map
        @param name:the name of layer
        @return:
        """
        if not isinstance(pieObject, PIEImageCollection) and not isinstance(pieObject, PIEFeatureCollection):
            raise ValueError("The pie object is the following item: {0}".format("PIEImageCollection, PIEFeatureCollection"))

        firstObject = pieObject.getAt(0)
        self.addLayer(firstObject, style, str(firstObject.name()))
        numbers = int(pieObject.size().getInfo())
        labels = [str(i) for i in range(numbers)]

        slider = widgets.IntSlider(value=None, min=1, max=numbers, step=1, readout=False, continuous_update=False, layout=widgets.Layout(width="200px"))
        label = widgets.Label(value=labels[0], layout=widgets.Layout(padding=("0px, 5px, 0px, 5px")))
        playBtn = widgets.Button(icon="play", tooltip="the play the slider", botton_style="primary" , layout=widgets.Layout(width="32px"))
        closeBtn = widgets.Button(icon="close", tooltip="the close the slider", botton_style="primary", layout=widgets.Layout(width="32px"))
        pauseBtn = widgets.Button(icon="pause", tooltip="the pause the slider", boton_style="primary", layout=widgets.Layout(width="32px"))

        playChk = widgets.Checkbox(value=False)
        sliderBox = widgets.HBox([slider, label, playBtn, pauseBtn, closeBtn])
        sliderBox = widgets.HBox([slider, label, playBtn, pauseBtn, closeBtn])

        def play_click(b):
            playChk.value = True
            def play(slider):
                while playChk.value:
                    if slider.value < len(labels):
                        slider.value += 1
                        randomNumber = tuple([randrange(1, 100, randint(1,100)) for i in range(3)])
                        rand_color = random_color(randomNumber)
                        style['color'] = rand_color
                    else:
                        slider.value = 1
                        playChk.value = False
                    time.sleep(0.5)
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
            index = slider.value - 1
            label.value = labels[index]
            self.addLayer(pieObject.getAt(index), style, str(pieObject.getAt(index).name()))
        slider.observe(slider_observe, "value")

        slider_control = WidgetControl(widget=sliderBox, position="topright")
        self.add_control(slider_control)

    def addZoomSlider(self):
        """
        Add a the zoom slider control in the map
        @param pieObject:
        @return:
        """
        zoom_slider = widgets.IntSlider(value=7, min=0, max=15, description="Map Zoom", readout=False, continuous_update=False)
        jslink((zoom_slider, "value"), (self, "zoom"))
        zoom_control = WidgetControl(widget=zoom_slider, position="topright")
        self.add_control(zoom_control)

    def addTakeColor(self):
        """
        Add a take color tool in the map
        @return:
        """
        take_color = ColorPicker(description="Take a color")
        take_color_control = WidgetControl(widget=take_color, position="bottomright")
        self.add_control(take_color_control)

    def addLegend(self, legendList):
        """
         add a legend
        @param legendList:
        @return:
        """
        title = legendList.get("title")
        colors = legendList.get("colors")
        labels = legendList.get("labels")
        infos = legendList.get("infos")
        legendContent = dict()
        for i in range(len(colors)):
            legendContent.setdefault(labels[i], colors[i])

        legend = LegendControl(legend=legendContent, name="Legend", position="topright")
        legend.name = title
        self.add_control(legend)

    def __addSearchDataSet(self):
        """
        Search PIE data id
        @return:
        """

        from IPython.display import display
        searchBtn = widgets.Button(icon="search", tooltip="search button", botton_style="primary",
                                 layout=widgets.Layout(width="32px"))

        id_data_list = list()
        id_data_list2 = list()
        urlInfo = config.getFuzzyQuery()
        result = GET(urlInfo=urlInfo)
        _data = result.get("data")
        for id in _data:
            id_data_list.append(id.get("title"))
            id_data_list2.append(id.get("id"))
        def search_data_id(c):
            id_output.clear_output()
            search_id = "{}".format(id_comb.value)
            if id_data_list.__contains__(search_id):
                id_output.clear_output()
                html_widget.value = ''.join(["ID: ", id_data_list2[id_data_list.index(search_id)], "<br>"])
            else:
                html_widget.value = "no data"
            with id_output:
                display(html_widget)

        id_comb = widgets.Combobox(
            value='{}'.format(id_data_list[0]),
            placeholder='',
            options=id_data_list,
            description='',
            ensure_option=False,
            disabled=False
        )
        html_widget = widgets.HTML()
        id_output = widgets.Output(
            layout={
                "max_width": "340px",
                "max_height": "250px",
                "overflow": "scroll",
            }
        )
        searchBtn.on_click(search_data_id, html_widget.value)
        Hbox = widgets.HBox([id_comb, searchBtn])
        Vbox = widgets.VBox([Hbox, id_output], layout=widgets.Layout(padding="0px 6px 0px 6px"))
        Vbox.box_style = "info"
        Vbox_control = WidgetControl(widget=Vbox, position='topleft')
        self.add_control(Vbox_control)

    def __addUserAsset(self):
        """
        To show user assets
        @return:
        """
        urlInfo = config.getQueryCatalog()
        asset_image = dict()
        asset_vector = dict()
        asset_model = dict()
        def recur_get(url_Info):
            result = GET(url_Info)
            _data = result.get("data")
            for d in _data:
                if d.get("type") == 1:
                    _uuid = d.get("uuid")
                    _url = urlInfo.get("url") + "?" + "parentId={}".format(_uuid)
                    _urlInfo = {"url": _url, "x-api": urlInfo.get("x-api")}
                    recur_get(_urlInfo)
                elif d.get("type") == 3:
                    asset_image["{}".format(d.get("name"))] = d.get("fullPath")
                elif d.get("type") == 4:
                    asset_vector['{}'.format(d.get("name"))] = d.get("fullPath")
                elif d.get("type") == 5:
                    asset_model['{}'.format(d.get("name"))] = d.get("fullPath")
        recur_get(urlInfo)
        html_vector = widgets.HTML(
            value="".join(["{} id: ".format(k)+str(asset_vector.get(k))+"<br>" for k in asset_vector.keys()]),
        )
        html_image = widgets.HTML(
            value="".join(["{} id: ".format(k)+str(asset_image.get(k))+"<br>" for k in asset_image.keys()])
        )
        # html_model = widgets.HTML(
        #     value="".join(["{} id: ".format(k)+str(asset_model.get(k))+"<br>" for k in asset_model.keys()])
        # )
        accordion2 = widgets.Accordion(children=[html_image, html_vector])
        accordion2.set_title(0, "影像")
        accordion2.set_title(1, "矢量")
        accordion = widgets.Accordion(children=[accordion2])
        accordion.set_title(0, '用户资源')
        accordion_control = WidgetControl(widget=accordion, position="bottomright")
        self.add_control(accordion_control)

    def addIndexModel(self):
        """

        @return:
        """
        from ipywidgets import GridspecLayout
        from .imageCollection import PIEImageCollection
        from .featureCollection import PIEFeatureCollection
        from .filter import PIEFilter


        index_dropdown = widgets.Dropdown(
            value="roi",
            placeholder="",
            options=["roi", "NDVI", "NDWI", "EVI", "MNDWI"],
            description="选择指数:",
            ensure_option=False,
            disabled=False,
        )
        administrative_area_number_text = widgets.Text(
            value='110000',
            placeholder='Type something',
            description='行政编号:',
            disabled=False
        )

        start_date_text = widgets.Text(
            value='2020-04-01',
            placeholder='Type something',
            description='开始日期:',
            disabled=False
        )
        end_date_text = widgets.Text(
            value='2020-05-01',
            placeholder='Type something',
            description='结束日期:',
            disabled=False
        )

        #加载影像，定义模型
        def create_mask(image):
            qa = image.select("BQA")
            cloudMask = qa.bitwiseAnd(1 << 4).eq(0)
            return image.updateMask(cloudMask)
        def ndvi_model(l8Col_filter):
            b5 = l8Col_filter.select("B5")
            b4 = l8Col_filter.select("B4")
            ndvi = (b5.subtract(b4)).divide(b5.add(b4))
            return ndvi
        def ndwi_model(l8Col_filter):
            b5 = l8Col_filter.select("B5")
            b3 = l8Col_filter.select("B3")
            ndwi = (b3.subtract(b5)).divide(b3.add(b5))
            return ndwi
        def evi_model(l8Col_filter):
            nir = l8Col_filter.select("B5").divide(10000)
            red = l8Col_filter.select("B4").divide(10000)
            blue = l8Col_filter.select("B2").divide(10000)
            evi = ((nir.subtract(red)).multiply(2.5)).divide(nir.add(red.multiply(6)).subtract(blue.multiply(7.5)).add(1))
            return evi
        def mndwi_model(l8Col_filter):
            b3 = l8Col_filter.select("B3")
            b6 = l8Col_filter.select("B6")
            mndwi = (b3.subtract(b6)).divide(b3.add(b6))
            return mndwi


        l8Col = PIEImageCollection("LC08/01/T1")
        def cacluate_index(index_dropdown_value):
            def cacluate_index_in(c):
                if self.findLayer("NDVI"):
                    self.remove_layer(self.findLayer("NDVI"))
                elif self.findLayer("NDWI"):
                    self.remove_layer(self.findLayer("NDWI"))
                elif self.findLayer("roi"):
                    self.remove_layer(self.findLayer("roi"))
                elif self.findLayer("EVI"):
                    self.remove_layer(self.findLayer("EVI"))
                elif self.findLayer("MNDWI"):
                    self.remove_layer(self.findLayer("MNDWI"))

                roi = PIEFeatureCollection('NGCC/CHINA_PROVINCE_BOUNDARY') \
                    .filter(PIEFilter().eq("code", administrative_area_number_text.value)).getAt(0).geometry()
                l8Col_filter = l8Col.filterDate(start_date_text.value, end_date_text.value) \
                                    .select(["B2", "B3", "B4", "B5", "B6", "BQA"]) \
                                    .filterBounds(roi) \
                                    .map(create_mask)

                if "NDVI" == index_dropdown.value:
                    ndvi = l8Col_filter.map(ndvi_model).mean().clip(roi)
                    return ndvi
                elif "NDWI" == index_dropdown.value:
                    ndwi = l8Col_filter.map(ndwi_model).mean().clip(roi)
                    return ndwi
                elif "EVI" == index_dropdown.value:
                    evi = l8Col_filter.map(evi_model).mean().clip(roi)
                    return evi
                elif "MNDWI" == index_dropdown.value:
                    mndwi = l8Col_filter.map(mndwi_model).mean().clip(roi)
                    return mndwi
                elif "roi" == index_dropdown.value:
                    return roi
            th0 = threading.Thread(target=cacluate_index_in, args=str(index_dropdown.value)[0])
            th0.start()
            th0.join()
            return cacluate_index_in(1)

        show_visparam = {
            "NDVI": {
                    'min': -0.2,
                    'max': 0.8,
                    'palette': 'CA7A41, CE7E45, DF923D, F1B555, FCD163, 99B718, ' +
                             '74A901, 66A000, 529400,3E8601, 207401, 056201, 004C00,' +
                             '023B01, 012E01, 011D01, 011301'},
            "NDWI": {
                    'min': -1,
                    'max': 0.3,
                    'palette': 'FFFFFF,0000FF'},
            "roi": {
                "color": "red",},
            "EVI": {
                'min': -0.2,
                'max': 0.8,
                'palette': 'CA7A41, CE7E45, DF923D, F1B555, FCD163, 99B718, '+
                    '74A901, 66A000, 529400,3E8601, 207401, 056201, 004C00,'+
                    '023B01, 012E01, 011D01, 011301'},
            "MNDWI": {
                'min': -1,
                'max': 0.3,
                'palette': 'FFFFFF,0000FF'},
        }

        def show_object(c):
            result = cacluate_index(1)
            visParam = show_visparam[index_dropdown.value]
            self.addLayer(result, visParam, index_dropdown.value)
        index_dropdown.observe(show_object)


        grid = GridspecLayout(4, 1)
        grid[0, 0] = index_dropdown
        grid[1, 0] = administrative_area_number_text
        grid[2, 0] = start_date_text
        grid[3, 0] = end_date_text

        grid_control = WidgetControl(widget=grid, position="bottomright")
        self.add_control(grid_control)






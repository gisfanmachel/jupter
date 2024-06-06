# -*- coding:utf-8 -*-
"""
@Project :   PyCharm
@File    :   leafletTileLayer.py
@Time    :   2021/4/18 18:28 下午
@Author  :   lsw
@Version :   1.0
@Contact :   shi_weihappy@126.com
@License :   (C)Copyright 2019-2020, lsw
@Desc    :   None
"""
import builtins
from ipyleaflet import *

# 重写TileLayer
class tileLayer(TileLayer):
    _view_name = Unicode('LeafletTileLayerView').tag(sync=True)#LeafletTileLayerView
    _model_name = Unicode('LeafletTileLayerModel').tag(sync=True)#LeafletTileLayerModel

    url = \
        Unicode('https://engine.piesat.cn/v1alpha/projects/earthengine-legacy/maps/4cf1fbdcf2407c55abcb3264a4e6bc08&x={x}&y={y}&z={z}.png').tag(sync=True)
    min_zoom = Int(0).tag(sync=True, o=True)
    max_zoom = Int(18).tag(sync=True, o=True)
    attribution = Unicode("TileLayer Map").tag(sync=True, o=True)
    buffer = Int(1).tag(sync=True, o=True)

    # path = Unicode('D:/work6/test.png').tag(sync=True)
    image_value = Instance(dict, allow_none=True)
    value = Union(
        [Instance(builtins.list, read_only=True, allow_none=True),
         Instance(builtins.list, read_only=True, allow_none=True),]
    )


    def __init__(self, **kwargs):
        super(tileLayer, self).__init__(**kwargs)
        _load_callbacks = Instance(CallbackDispatcher, ())

    def _handle_leaflet_event(self, _, content, buffers):
        if content.get("event", "") == "load":
            self._load_callbacks(**content)

    def on_load(self, callback, remove=False):
        self._load_callbacks.register_callback(callback, remove=remove)

    def redraw(self):
        self.send({"msg": "redraw"})

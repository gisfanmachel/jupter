# -*- coding:utf-8 -*-
"""
@Project :   LearnPython3
@File    :   foliumPIERasterTileLayer.py
@Time    :   2022/7/18 16:03
@Author  :   lishiwei
@Version :   1.0
@Contact :   shi_weihappy@126.com
@License :   (C)Copyright 2021-2022, lishiwei
@Desc    :   None
"""
from folium.elements import JSCSSMixin
from folium.map import Layer
from jinja2 import Template

class PIEVectorTileLayer(JSCSSMixin, Layer):
    _template = Template(
        u"""
            {% macro script(this, kwargs) -%}
            var {{ this.get_name() }} = L.pieVectorTileLayer(
                '{{ this.url }}',
                {% if this.options is not none %}
                {{ this.options|tojson }}).addTo({{ this._parent.get_name() }});
                {% else %}
                {{ null }}).addTo({{ this._parent.get_name() }});
                {% endif %}
            {%- endmacro %}
            """
    )  # noqa

    default_js = [
        (
            "vectorGrid",
            "https://pie-engine-static-data.obs.cn-north-4.myhuaweicloud.com/engine_studio_sdk/libs/Leaflet.VectorGrid.bundled.js"
        ),
        (
            "pieVectorTileLayer",
            "https://pie-engine-static-data.obs.cn-north-4.myhuaweicloud.com/engine_studio_sdk/libs/Leaflet.PIEVectorTileLayer.js"
        )
    ]

    def __init__(self, url, name=None, overlay=True, control=True, show=True, options=None):
        super(PIEVectorTileLayer, self).__init__(name=name,
                                                 overlay=overlay,
                                                 control=control,
                                                 show=show)

        self.url = url
        self._name = "PIEVectorTileLayer"
        self.options = options
'''
.. graphviz::

   digraph G_libs{
        rankdir=LR;
        size="8,5";
        concentrate=true;
        node  [style="rounded,filled", shape=box, fixedsize=true, width=2.8, fontname="Arial"];

        "python3-shapely"     [fillcolor="#a0ffa0"];
        "python3-mapnik"     [fillcolor="#a0ffa0"];
        "python3-pyproj"     [fillcolor="#a0ffa0"];
        "python3-fiona"     [fillcolor="#a0ffa0"];
        "python3-gdal"     [fillcolor="#a0ffa0"];
        "python3-mpltoolkits.basemap"     [fillcolor="#a0ffa0"];

        "spatialite-bin"    [fillcolor="#ffa0a0"];
        "mapnik-utils"    [fillcolor="#ffa0a0"];
        "gdal-bin"    [fillcolor="#ffa0a0"];
        "proj-bin"    [fillcolor="#ffa0a0"];

        libgdal20 -> "gdal-bin";
        libgdal20 -> "python3-gdal";
        libproj12 -> libgdal20 ;
        "libgeos-c1v5" -> libgdal20 ;
        "libgeos-c1v5" -> "python3-mpltoolkits.basemap" ;
        "libgeos-c1v5" ->  "python3-shapely" ;
        "libgeos-c1v5" ->  libspatialite7;
        "libgeos-c1v5" ->  "spatialite-bin" ;

        libproj12 -> "python3-mapnik";
        libproj12 -> "proj-bin";
        libproj12 ->  "spatialite-bin" ;
        libproj12 ->   "mapnik-utils" ;
        libproj12 -> "python3-pyproj";
        libproj12 ->  libspatialite7;


        libgdal20 -> "python3-fiona";
        libspatialite7 ->  "spatialite-bin" ;
        "libmapnik3.0" -> "python3-mapnik" ;
        "libmapnik3.0" -> "mapnik-utils" ;

   }
'''

import os

from helper.textool import get_tmp_file
# from pygraphviz import Digraph

# from graphviz import Digraph, Graph

import pygraphviz as pgv

G = pgv.AGraph(directed=True, rankdir="LR", size=[8, 5], concentrate=True)
# g = Graph(format='png')
# dot = Digraph()
# dot.format = 'png'
#
#
# dot = Digraph(comment='The Round Table')

cfg = {
    'shape': 'box',
    'fixedsize': True,
    'style': 'rounded,filled',
    'width': 2,
    'fontname': 'Arial',
    'fontsize': 10,
    'concentrate': True,
}

cfg2 = {
    'shape': 'ellipse',
    'fixedsize': True,
    'style': 'rounded,filled',
    'width': 2,
    'fontname': 'Arial',
    'fontsize': 10,
    'concentrate': True,
}

for node_name in ['region_popu.shp', 'xx_couties.shp']:
    G.add_node(node_name, fillcolor="#ffffff", **cfg)

cfg['style'] = 'filled'
for node_name in ['region_popu', 'new_region', 'new_region2']:
    G.add_node(node_name, fillcolor="#99ffff", **cfg)

# for node_name in ['region_popu', 'new_region', 'new_region2']:
#     G.add_node(node_name, fillcolor="#99ffff", **cfg2)

G.add_edge('region_popu.shp', 'region_popu', label='ogr2ogr')
G.add_edge('region_popu', 'xx_couties.shp', label='.dump')
G.add_edge('xx_couties.shp', 'new_region', '.loadshp')
G.add_edge('xx_couties.shp', 'new_region2', '.loadshp')


G.layout(prog='dot')  # default to neato
G.draw(get_tmp_file(__file__, '1', file_ext='pdf'))
G.draw(get_tmp_file(__file__, '1', file_ext='png'))

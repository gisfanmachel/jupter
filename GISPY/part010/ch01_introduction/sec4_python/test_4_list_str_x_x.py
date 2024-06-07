#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
list_val = [1, '3', 5 ,'4']
list_val
###############################################################################
ran_val = range(5,0, -1)
ran_val
###############################################################################
list_val = list(ran_val)
list_val
###############################################################################
list_val.append(6)
list_val
list_val = list_val + [7,8]
list_val
###############################################################################
list_val.extend([9, 10])
list_val
###############################################################################
list_val.insert(5, 0)
list_val
###############################################################################
tep_a = list_val.pop()
list_val
tep_a
###############################################################################
tep_a = list_val.pop(5)
list_val
tep_a
###############################################################################
idx = list_val.index(4)
idx
###############################################################################
list_val.remove(1)
list_val
###############################################################################
list_val.sort()
list_val
###############################################################################
list_val.reverse()
list_val
###############################################################################
a = list(range(8))
a
b = tuple(a)
b
c = list(b)
c
###############################################################################
list_val = list(range(8))
list_val[-2]
list_val[2:]
list_val[2:-2]
list_val[:]
###############################################################################
dict_demo = {'GIS': 'Geographic Information System',
        'RS': 'Remote Sencing',
        'GPS': 'Global Positioning System',
        'DEM': 'Dynamic Effect Model'}
###############################################################################
dict_demo['GPS']
###############################################################################
dict_demo.items()
###############################################################################
dict_demo['DEM'] = 'Digital Elevation Model'
dict_demo['DEM']
###############################################################################
'RS' in dict_demo
'rs' in dict_demo
dict_demo['rs'] = 'Remote Sencing'
dict_demo.keys()
del(dict_demo['rs'])
dict_demo.keys()
for s_name, l_name in dict_demo.items():
    print(('Short: %4s -> Long: %s') % (s_name, l_name))


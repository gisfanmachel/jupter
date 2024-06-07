# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_dataprepare_collector\object_detection_training_data.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 1900 bytes
from iobjectspy.ml.vision._sample.create_object_detection_data_mask import CreateObjectDetectionDataMask
from _sample.create_object_detection_data import CreateObjectDetectionData

def create_voc_data(input_data, input_label, label_class_field, output_path, output_name, training_data_format, tile_format='jpg', tile_size_x=1024, tile_size_y=1024, tile_offset_x=512, tile_offset_y=512, tile_start_index=0, save_nolabel_tiles=False, **kwargs):
    create_td = CreateObjectDetectionData(input_data, input_label, label_class_field, output_path, output_name, 
     training_data_format, 
     tile_format, tile_size_x, tile_size_y, tile_offset_x, 
     tile_offset_y, 
     tile_start_index, 
     save_nolabel_tiles, **kwargs)
    create_td.create_voc()


def create_voc_mask_data(input_data, input_label, label_class_field, output_path, output_name, training_data_format, tile_format='jpg', tile_size_x=1024, tile_size_y=1024, tile_offset_x=512, tile_offset_y=512, tile_start_index=0, save_nolabel_tiles=False, **kwargs):
    create_td = CreateObjectDetectionDataMask(input_data, input_label, label_class_field, output_path, output_name, 
     training_data_format, 
     tile_format, tile_size_x, tile_size_y, tile_offset_x, 
     tile_offset_y, 
     tile_start_index, 
     save_nolabel_tiles, **kwargs)
    create_td.create_voc_mask()

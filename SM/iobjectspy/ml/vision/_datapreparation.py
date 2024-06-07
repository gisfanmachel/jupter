# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_datapreparation.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 8705 bytes
import os, tempfile
from iobjectspy import DatasetVector, conversion
from iobjectspy._jsuperpy._utils import check_lic
from ._dataprepare_collector import create_binary_classification_data
from ._dataprepare_collector import create_multi_classification_data
from ._dataprepare_collector import create_scene_classification_data
from ._dataprepare_collector import create_voc_data, create_voc_mask_data
from toolkit._toolkit import _is_image_file, get_input_dataset, _get_dataset_readonly, del_dir

class DataPreparation:
    __doc__ = "\n    图像数据准备流程入口\n\n    "

    @staticmethod
    def create_training_data(input_data, input_label, label_class_field, output_path, output_name, training_data_format, tile_format='jpg', tile_size_x=1024, tile_size_y=1024, tile_offset_x=512, tile_offset_y=512, tile_start_index=0, save_nolabel_tiles=False, **kwargs):
        """
        训练数据生成

        | 将整幅影像数据和与其匹配的矢量标注数据切分为指定大小的瓦片，用于深度学习训练。
        | 生成的训练数据一般包括图片、标注、以及相关元信息，其中切分后的图片和标注文件名一一对应。

        :param input_data: 输入的影像数据，支持影像文件
        :type input_data: str
        :param input_label: 输入的矢量标注数据，支持矢量数据集
        :type input_label: str ot DatasetVector
        :param label_class_field: 矢量标注数据的类型字段，如指定None则认定全部标注为同一类型
        :type label_class_field: str or None
        :param output_path: 输出的训练数据存储路径
        :type output_path: str
        :param training_data_format: 输出的训练数据格式，支持 VOC, MULTI_C, BINARY_C, SCENE_C
        :type training_data_format: str
        :param tile_format: 影像瓦片格式，支持 tif, jpg, png, origin
        :type tile_format: str
        :param tile_size_x: x方向瓦片大小
        :type tile_size_x: int
        :param tile_size_y: y方向瓦片大小
        :type tile_size_y: int
        :param tile_offset_x: x方向瓦片偏移量
        :type tile_offset_x: int
        :param tile_offset_y: y方向瓦片偏移量
        :type tile_offset_y: int
        :param tile_start_index: 瓦片命名起始索引值，默认为0，当调用该接口处理多幅影像时可设置为-1
        :type tile_start_index: int
        :param save_nolabel_tiles: 是否保存无标签覆盖的瓦片
        :type save_nolabel_tiles: bool
        :return: None

        VOC格式：
         | ./VOC
         | ./VOC/Annotations/000000001.xml 标签瓦片
         | ./VOC/Images/000000001.jpg 影像瓦片
         | ./VOC/ImageSets/Main/train.txt, val.txt, test.txt, trainval.txt 训练集瓦片名称、验证集瓦片名称、测试集瓦片名称、训练集与验证集瓦片名称
         | ./VOC/VOC.sda 训练数据配置文件

        MULTI_C格式：
         | ./MULTI_C
         | ./MULTI_C/Images/00000000.tif 影像瓦片
         | ./MULTI_C/Masks/00000000.png 标签瓦片
         | ./MULTI_C/MULTI_C.sda 训练数据配置文件

        BINARY_C格式：
         | ./BINARY_C
         | ./BINARY_C/Images/00000000.tif 影像瓦片
         | ./BINARY_C/Masks/00000000.png 标签瓦片
         | ./BINARY_C/BINARY_C.sda 训练数据配置文件

        SCENE_C格式：
         | ./SCENE_C
         | ./SCENE_C/0/00000000.tif 影像瓦片
         | ./SCENE_C/1/00000000.png 影像瓦片
         | ./SCENE_C/2/00000000.tif 影像瓦片
         | ....
         | ./SCENE_C/scene_classification.csv 保存影像文件路径与类别映射关系
         | ./SCENE_C/SCENE_C.sda 训练数据配置文件

        """
        check_lic()
        if isinstance(input_data, str):
            if os.path.isdir(input_data):
                is_del_tmp_file = False
            elif _is_image_file(input_data):
                is_del_tmp_file = False
            else:
                is_del_tmp_file = True
                input_data = _get_dataset_readonly(input_data)
                temp_tif_path = os.path.join(tempfile.mkdtemp(), "temp") + ".tif"
                conversion.export_to_tif(input_data, temp_tif_path)
                input_data = temp_tif_path
        else:
            is_del_tmp_file = True
            input_data = _get_dataset_readonly(input_data)
            temp_tif_path = os.path.join(tempfile.mkdtemp(), "temp") + ".tif"
            conversion.export_to_tif(input_data, temp_tif_path)
            input_data = temp_tif_path
        if isinstance(input_data, str) and not os.path.exists(input_data):
            raise Exception("input_data does not exist ")
        else:
            if not _is_image_file(input_data):
                raise Exception("input_data must be images ")
            else:
                _source_input_label = get_input_dataset(input_label)
                if _source_input_label is None:
                    raise ValueError("source input_data is None")
                if not isinstance(_source_input_label, DatasetVector):
                    raise ValueError("source input_data must be DatasetVector")
                if not isinstance(output_path, str):
                    raise TypeError("output_path must be str ")
                if not isinstance(training_data_format, str):
                    raise TypeError("training_data_format must be str ")
                if not isinstance(tile_format, str):
                    raise TypeError("tile_format must be str ")
                if tile_start_index < -1:
                    raise TypeError("tile_start_index must be greater than -1 ")
                else:
                    outpath = os.path.join(output_path, output_name)
                    if os.path.exists(outpath) & (tile_start_index != -1):
                        files = os.listdir(outpath)
                        if files:
                            raise TypeError("`{:s}` is not empty or tile_start_index is not -1 ".format(outpath))
                        if training_data_format == "VOC":
                            create_voc_data(input_data, _source_input_label, label_class_field, output_path, output_name, 
                             training_data_format, 
                             tile_format, tile_size_x, tile_size_y, tile_offset_x, tile_offset_y, tile_start_index, 
                             save_nolabel_tiles, **kwargs)
                    elif training_data_format == "VOC_MASK":
                        create_voc_mask_data(input_data, _source_input_label, label_class_field, output_path, output_name, 
                         training_data_format, 
                         tile_format, tile_size_x, tile_size_y, tile_offset_x, tile_offset_y, tile_start_index, 
                         save_nolabel_tiles, **kwargs)
                    else:
                        if training_data_format == "MULTI_C":
                            create_multi_classification_data(input_data, _source_input_label, label_class_field, output_path, 
                             output_name, 
                             training_data_format, 
                             tile_format, tile_size_x, tile_size_y, tile_offset_x, tile_offset_y, 
                             tile_start_index, 
                             save_nolabel_tiles, **kwargs)
                        else:
                            if training_data_format == "BINARY_C":
                                create_binary_classification_data(input_data, _source_input_label, label_class_field, output_path, 
                                 output_name, 
                                 training_data_format, 
                                 tile_format, tile_size_x, tile_size_y, tile_offset_x, tile_offset_y, 
                                 tile_start_index, 
                                 save_nolabel_tiles, **kwargs)
                            else:
                                if training_data_format == "SCENE_C":
                                    create_scene_classification_data(input_data, _source_input_label, label_class_field, output_path, 
                                     output_name, 
                                     training_data_format, 
                                     tile_format, tile_size_x, tile_size_y, tile_offset_x, tile_offset_y, 
                                     tile_start_index, 
                                     save_nolabel_tiles, **kwargs)
                                else:
                                    raise Exception("{} Format not supported".format(training_data_format))
            del_dir(os.path.abspath(os.path.join(input_data, os.path.pardir)), is_del_tmp_file)
            print("The create training data have done!")

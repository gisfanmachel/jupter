# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_inference.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 15607 bytes
import os, sys, tempfile, time, warnings
from iobjectspy import Dataset, conversion
from iobjectspy._jsuperpy._utils import check_lic
from ._inference_collector import ObjectDetection, BinaryClassification, MultiClassification, SceneClassification, ImageClassification, ObjectExtraction
from toolkit._toolkit import _is_image_file, del_dir, _get_dataset_readonly, get_config_from_yaml, get_pic_path_from_dir

class Inference:

    def __init__(self, input_data, model_path, out_data, out_dataset_name):
        """
        图像数据模型推理功能入口

        :param input_data: 待推理的数据
        :type  input_data: str or Dataset
        :param model_path: 模型存储路径
        :type  model_path: str
        :param out_data: 输出文件(或数据源)路径
        :type  out_data: str or Datasource or DatasourceConnectionInfo
        :param out_dataset_name: 输出文件(或数据集)名称
        :type  out_dataset_name: str
        """
        if isinstance(input_data, str):
            if os.path.isdir(input_data):
                self.is_del_tmp_file = False
            elif _is_image_file(input_data):
                self.is_del_tmp_file = False
            else:
                self.is_del_tmp_file = True
                input_data = _get_dataset_readonly(input_data)
                temp_tif_path = os.path.join(tempfile.mkdtemp(), "temp") + ".tif"
                conversion.export_to_tif(input_data, temp_tif_path)
                input_data = temp_tif_path
        else:
            self.is_del_tmp_file = True
            input_data = _get_dataset_readonly(input_data)
            temp_tif_path = os.path.join(tempfile.mkdtemp(), "temp") + ".tif"
            conversion.export_to_tif(input_data, temp_tif_path)
            input_data = temp_tif_path
        self.input_data = input_data
        self.model_path = model_path
        self.out_data = out_data
        self.out_dataset_name = out_dataset_name
        check_lic()

    def object_detect_infer(self, category_name, nms_thresh=0.3, score_thresh=0.5):
        """
        影像数据目标检测

        | 支持 tif、img(Erdas Image)等影像文件，以及 jpg、png等图像文件，检测结果为矢量面数据集

        需要注意:
            - 当 input_data 为待检测文件时，out_data 为输出数据源路径(或数据源对象)，out_dataset_name 为数据集名
            - 当 input_data 为待路径时，out_data 为输出数据源路径(或数据源对象)，out_dataset_name 不生效，dataset_name从input_data文件列表中获取

        :param category_name: 目标检测类别，支持多类别检测
        :type  category_name: list[str] or str
        :param nms_thresh: nms的阈值
        :type  nms_thresh: float
        :param score_thresh: 类别分数的阈值
        :type  score_thresh: float
        :return: None
        """
        result = ObjectDetection(self.input_data, self.model_path, category_name, self.out_data, self.out_dataset_name, nms_thresh, score_thresh).infer()
        del_dir(os.path.abspath(os.path.join(self.input_data, os.path.pardir)), self.is_del_tmp_file)
        return result

    def object_detect_pic_infer(self, category_name, nms_thresh=0.3, score_thresh=0.5):
        """
        图片目标检测

        | 支持 jpg、png等图像文件，检测结果为xml

        需要注意:
            - 当 input_data 为待检测文件时，out_data 为输出路径，out_dataset_name 文件名
            - 当 input_data 为待路径时，out_data 为输出路径，out_dataset_name不生效，dataset_name从input_data文件列表中获取
        :param category_name: 目标检测类别，支持多类别检测
        :type  category_name: list[str] or str
        :param nms_thresh: nms的阈值
        :type  nms_thresh: float
        :param score_thresh: 类别分数的阈值
        :type  score_thresh: float
        :return: None
        """
        result = ObjectDetection(self.input_data, self.model_path, category_name, self.out_data, self.out_dataset_name, nms_thresh, score_thresh).infer_pic()
        del_dir(os.path.abspath(os.path.join(self.input_data, os.path.pardir)), self.is_del_tmp_file)
        return result

    def binary_classify_infer(self, offset, result_type, **kwargs):
        """
        遥感影像数据二元分类
        支持 tif、img(Erdas Image)等影像文件，以及 jpg、png等图像文件，分类结果为二值栅格或矢量文件
        支持SuperMap SDX下的影像数据集，分类结果为矢量或栅格数据集

        可添加关键字参数：'dsm_dataset' 输入与影像相匹配的DSM数据，实现基于DOM和DSM提取建筑物面。
        其中影像和DSM可以使用SuperMap iDesktop 桌面基于倾斜摄影数据提取：
            打开三维场景，使用 三维分析->生成DOM 三维分析->生成DSM，分辨率建议选择0.1m

        :param offset: 图像分块偏移，大幅图像需分块预测，其值为分块间重叠部分大小，以提高图像块边缘预测结果
        :type offset: int
        :param result_type: 结果返回类型，支持矢量面和栅格: 'region' or 'grid'
        :type result_type: str
        :return: 数据集名字
        """
        binaryclassification = BinaryClassification((self.model_path), **kwargs)
        result = (binaryclassification.infer)((self.input_data), (self.out_data), (self.out_dataset_name), offset, 
         result_type, **kwargs)
        binaryclassification.close_model()
        del_dir(os.path.abspath(os.path.join(self.input_data, os.path.pardir)), self.is_del_tmp_file)
        return result

    def scene_classify_infer(self, result_type, **kwargs):
        """
        遥感影像数据场景分类
        支持 tif、img(Erdas Image)等影像文件，以及 jpg、png等图像文件，分类结果为二值栅格或矢量文件
        支持SuperMap SDX下的影像数据集，分类结果为矢量或栅格数据集

        :param result_type: 结果返回类型，支持矢量面和栅格: 'region' or 'grid'
        :type result_type: str
        :return: 数据集名字
        """
        result = SceneClassification((self.input_data), (self.model_path), (self.out_data), (self.out_dataset_name), 
         result_type, **kwargs).infer()
        del_dir(os.path.abspath(os.path.join(self.input_data, os.path.pardir)), self.is_del_tmp_file)
        return result

    def multi_classify_infer(self, offset, result_type, **kwargs):
        """
        遥感影像数据多分类，地物分类
        支持 tif、img(Erdas Image)等影像文件，以及 jpg、png等图像文件，分类结果为多值栅格或矢量文件
        支持SuperMap SDX下的影像数据集，分类结果为矢量或栅格数据集

        :param offset: 图像分块偏移，大幅图像需分块预测，其值为分块间重叠部分大小，以提高图像块边缘预测结果
        :type offset: int
        :param result_type: 结果返回类型，支持矢量面和栅格: 'region' or 'grid'
        :type result_type: str
        :return: 数据集名字
        """
        result = MultiClassification((self.input_data), (self.model_path), (self.out_data), (self.out_dataset_name), offset, 
         result_type, **kwargs).infer()
        del_dir(os.path.abspath(os.path.join(self.input_data, os.path.pardir)), self.is_del_tmp_file)
        return result

    def image_classify_infer(self, **kwargs):
        """
        image分类
        支持 tif、img(Erdas Image)等影像文件，以及 jpg、png等图像文件，分类结果为二值栅格或矢量文件
        支持SuperMap SDX下的影像数据集，分类结果为矢量或栅格数据集

        :param result_type: 结果返回类型，支持矢量面和栅格: 'region' or 'grid'
        :type result_type: str
        :return: 数据集名字
        """
        result = ImageClassification((self.input_data), (self.model_path), (self.out_data), (self.out_dataset_name), **kwargs).infer()
        return result

    def object_extract_infer(self, score_thresh=0.5, nms_thresh=0.3, return_bbox=False):
        """
        遥感影像数据对象提取
        支持 tif、img(Erdas Image)等影像文件，以及 jpg、png等图像文件，分类结果为矢量文件
        支持SuperMap SDX下的影像数据集，分类结果为矢量

        :param score_thresh: 类别分数的阈值
        :type  score_thresh: float
        :param nms_thresh: nms的阈值
        :type  nms_thresh: float
        :param return_bbox: 是否返回对象的最小外接矩形
        :type  return_bbox: bool
        :return: 数据集名称
        """
        objectextraction = ObjectExtraction(self.model_path)
        result = objectextraction.infer(self.input_data, self.out_data, self.out_dataset_name, score_thresh, nms_thresh, return_bbox)
        objectextraction.close_model()
        del_dir(os.path.abspath(os.path.join(self.input_data, os.path.pardir)), self.is_del_tmp_file)
        return result


class _ImageryInference:

    def __init__(self, model_path, **kwargs):
        check_lic()
        self.config = get_config_from_yaml(model_path)
        self.model_path = model_path
        self.tmp_data_dir = tempfile.mkdtemp()
        self.kwargs = kwargs
        self._ImageryInference__func_class = "".join([x.capitalize() for x in self.config.model_type.split("_")])
        self._ImageryInference__inferece_obj = (eval(self._ImageryInference__func_class))((self.model_path), **kwargs)
        self._ImageryInference__is_del_tmp_file = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self._ImageryInference__inferece_obj.close_model()
        del_dir(os.path.abspath(self.tmp_data_dir), self._ImageryInference__is_del_tmp_file)

    def object_detect_infer(self, input_data, out_data, out_dataset_name, category_name, nms_thresh=0.3, score_thresh=0.5):
        pass

    def binary_classify_infer(self, input_data, out_data, out_dataset_name, offset, result_type, **kwargs):
        self._ImageryInference__before_infer(input_data)
        result = (self._ImageryInference__inferece_obj.infer)(input_data, out_data, out_dataset_name, offset, result_type, **kwargs)
        return result

    def multi_classify_infer(self):
        pass

    def scene_classify_infer(self):
        pass

    def object_extract_infer(self, input_data, out_data, out_dataset_name, score_thresh=0.5, nms_thresh=0.1, return_bbox=False):
        self._ImageryInference__before_infer(input_data)
        result = self._ImageryInference__inferece_obj.infer(input_data, out_data, out_dataset_name, score_thresh, nms_thresh, return_bbox)
        return result

    def __get_tmp_input_data_path(self, input_data):
        if isinstance(input_data, str):
            if os.path.isdir(input_data):
                self._ImageryInference__is_del_tmp_file = False
            elif _is_image_file(input_data):
                self._ImageryInference__is_del_tmp_file = False
        else:
            self._ImageryInference__is_del_tmp_file = True
            input_data = _get_dataset_readonly(input_data)
            temp_tif_path = os.path.join(self.tmp_data_dir, self._ImageryInference__func_class.lower() + str(round(time.time() * 1000)) + ".tif")
            conversion.export_to_tif(input_data, temp_tif_path)
            input_data = temp_tif_path
        return input_data

    def __before_infer(self, input_data):
        return self._ImageryInference__get_tmp_input_data_path(input_data)


class _PictureInference:

    def __init__(self, model_path, **kwargs):
        check_lic()
        self.config = get_config_from_yaml(model_path)
        self.model_path = model_path
        self.tmp_data_dir = tempfile.mkdtemp()
        self.kwargs = kwargs
        self._PictureInference__func_class = "".join([x.capitalize() for x in self.config.model_type.split("_")])
        self._PictureInference__inferece_obj = (eval(self._PictureInference__func_class))((self.model_path), **kwargs)
        self._PictureInference__is_del_tmp_file = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self._PictureInference__inferece_obj.close_model()
        del_dir(os.path.abspath(self.tmp_data_dir), self._PictureInference__is_del_tmp_file)

    def object_detect_infer(self, input_data, out_data, out_dataset_name, category_name, nms_thresh=0.3, score_thresh=0.5):
        pass

    def picture_classify_infer(self):
        pass

    def object_extract_infer(self, input_data, out_data, out_dataset_name, score_thresh=0.5, nms_thresh=0.1):
        image_path_list = self._PictureInference__before_infer(input_data)
        result = self._PictureInference__inferece_obj.infer_pic(input_data, image_path_list, out_data, out_dataset_name, score_thresh, nms_thresh)
        return result

    def __get_tmp_input_data_path(self, input_data):
        if isinstance(input_data, str):
            if os.path.isdir(input_data):
                self._PictureInference__is_del_tmp_file = False
            elif _is_image_file(input_data):
                self._PictureInference__is_del_tmp_file = False
        else:
            self._PictureInference__is_del_tmp_file = True
            input_data = _get_dataset_readonly(input_data)
            temp_tif_path = os.path.join(self.tmp_data_dir, self._PictureInference__func_class.lower() + str(round(time.time() * 1000)) + ".tif")
            conversion.export_to_tif(input_data, temp_tif_path)
            input_data = temp_tif_path
        return input_data

    def __before_infer(self, input_data):
        input_data = self._PictureInference__get_tmp_input_data_path(input_data)
        image_path_list = self._PictureInference__get_image_path(input_data)
        return image_path_list

    def __get_image_path(self, input_data, get_all_dir=False, suffix=None):
        """
        判断输入是单个文件还是文件夹;
        设置参数判断是否读取嵌套的子文件目录;
        通过后缀来过滤图片，将他们的完整路径都保存到一个列表;

        :param input_data: 输入数据的路径
        :type input_data: str
        :param get_all_dir: 是否推理输入路径下所有子目录内图片
        :type get_all_dir: bool
        :param suffix: 指定待推理图片的后缀，并以此来过滤文件夹下数据
        :type suffix: list

        :return image_path_list: 所有待推理图片的完整路径
        :type image_path_list: list
        """
        image_path_list = []
        if not os.path.exists(input_data):
            raise ValueError("The input path doesn't exist, please check the  path {}".format(input_data))
        elif suffix is None:
            suffix = [
             'jpg', 'tif', 'png', 'jpeg', 'JPG', 'TIF', 
             'PNG', 'JPEG']
        if os.path.isdir(input_data):
            image_path_list = get_pic_path_from_dir(input_data, get_all_dir, suffix)
        else:
            image_path_list.append(input_data)
        return image_path_list

# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_inference_collector\object_detection_infer.py
# Compiled at: 2020-09-28 17:51:20
# Size of source mod 2**32: 9223 bytes
import os, re, yaml
from dotmap import DotMap
from iobjectspy import Datasource
from toolkit._toolkit import get_config_from_yaml

class ObjectDetection:

    def __init__(self, input_data, model_path, category_name, out_data, out_dataset_name, nms_thresh, score_thresh):
        self.input_data = input_data
        self.config = model_path
        self.model_path = os.path.abspath(os.path.join(model_path, os.path.pardir))
        self.category_name = category_name
        self.out_data = out_data
        self.out_dataset_name = out_dataset_name
        self.nms_thresh = nms_thresh
        self.score_thresh = score_thresh

    def infer(self):
        """
        根据func_str拼接字符串自动执行各个网络的函数
        :return:
        """
        func_config = get_config_from_yaml(self.config)
        func_str = "self." + func_config.model_architecture + "_" + func_config.framework
        return eval(func_str)()

    def infer_pic(self):
        """
        根据func_str拼接字符串自动执行各个网络的函数
        :return:
        """
        func_config = get_config_from_yaml(self.config)
        func_str = "self." + func_config.model_architecture + "_" + func_config.framework + "_pic"
        return eval(func_str)()

    def faster_rcnn_tensorflow(self):
        from _models.object_detection.faster_rcnn._detection import FasterRCNNEstimation
        if self.category_name is None:
            with open(self.config) as f:
                config_dict = yaml.load(f, Loader=(yaml.FullLoader))
            config = DotMap(config_dict)
            config.get("model").get("categorys").remove("__background__")
            category_name = config.get("model").get("categorys")
            category_name = [str(i) for i in category_name]
            self.category_name = category_name
        else:
            regex = ",|，"
            self.category_name = re.split(regex, self.category_name)
        if not isinstance(self.model_path, str):
            raise TypeError("model_path must be str ")
        else:
            if not os.path.exists(self.model_path):
                raise Exception("model_path does not exist ")
            elif not isinstance(self.out_data, (str, Datasource)):
                raise TypeError("out_data must be str or Datasource ")
            if not isinstance(self.out_dataset_name, str):
                raise TypeError("out_dataset_name must be str ")
            if isinstance(self.input_data, str):
                if os.path.isdir(self.input_data):
                    run_prediction = FasterRCNNEstimation(self.model_path, self.config)
                    result = run_prediction.estimation_dir(self.input_data, self.category_name, self.out_data, self.nms_thresh, self.score_thresh)
                else:
                    run_prediction = FasterRCNNEstimation(self.model_path, self.config)
                    result = run_prediction.estimation_img(self.input_data, self.category_name, self.out_data, self.out_dataset_name, self.nms_thresh, self.score_thresh)
            else:
                raise TypeError("input_data must be str or Dataset")
            return result

    def faster_rcnn_tensorflow_pic(self):
        from _models.object_detection.faster_rcnn._detection import FasterRCNNEstimation
        if self.category_name is None:
            with open(self.config) as f:
                config_dict = yaml.load(f, Loader=(yaml.FullLoader))
            config = DotMap(config_dict)
            config.get("model").get("categorys").remove("__background__")
            category_name = config.get("model").get("categorys")
            category_name = [str(i) for i in category_name]
            self.category_name = category_name
        else:
            regex = ",|，"
            self.category_name = re.split(regex, self.category_name)
        if not isinstance(self.model_path, str):
            raise TypeError("model_path must be str ")
        else:
            if not os.path.exists(self.model_path):
                raise Exception("model_path does not exist ")
            elif not isinstance(self.out_data, str):
                raise TypeError("out_data must be str ")
            if not isinstance(self.out_dataset_name, str):
                raise TypeError("out_dataset_name must be str ")
            if isinstance(self.input_data, str):
                if os.path.isdir(self.input_data):
                    run_prediction = FasterRCNNEstimation(self.model_path, self.config)
                    result = run_prediction.estimation_pic_dir(self.input_data, self.category_name, self.out_data, self.nms_thresh, self.score_thresh)
                else:
                    run_prediction = FasterRCNNEstimation(self.model_path, self.config)
                    result = run_prediction.estimation_pic(self.input_data, self.category_name, self.out_data, self.out_dataset_name, self.nms_thresh, self.score_thresh)
            else:
                raise TypeError("input_data must be str or Dataset")
            return result

    def yolo_keras(self):
        from _models.object_detection.yolo._detection import YoloEstimation
        if self.category_name is None:
            with open(self.config) as f:
                config_dict = yaml.load(f, Loader=(yaml.FullLoader))
            config = DotMap(config_dict)
            config.get("model").get("categorys").remove("__background__")
            category_name = config.get("model").get("categorys")
            category_name = [str(i) for i in category_name]
            self.category_name = category_name
        else:
            regex = ",|，"
            self.category_name = re.split(regex, self.category_name)
        if not isinstance(self.model_path, str):
            raise TypeError("model_path must be str ")
        else:
            if not os.path.exists(self.model_path):
                raise Exception("model_path does not exist ")
            elif not isinstance(self.out_data, str):
                raise TypeError("out_data must be str ")
            if not isinstance(self.out_dataset_name, str):
                raise TypeError("out_dataset_name must be str ")
            assert isinstance(self.input_data, str), "input_data must be str "
            run_prediction = YoloEstimation(self.model_path, self.config)
            result = run_prediction.detect_img_dir(self.input_data, self.category_name, self.out_data, self.nms_thresh, self.score_thresh)
            return result


class ObjectDetectionWithTile:

    def __init__(self, model_path):
        from _models.object_detection.faster_rcnn._detection import FasterRCNNEstimation
        config = model_path
        self.config = get_config_from_yaml(model_path)
        self.model_path = os.path.abspath(os.path.join(model_path, os.path.pardir))
        self.estimate = FasterRCNNEstimation(self.model_path, config)

    def load_model(self):
        func_str = "self." + self.config.model_architecture + "_" + self.config.framework + "_load_model"
        return eval(func_str)()

    def infer_tile(self, image_data, category_name, nms_thresh, score_thresh):
        func_str = "self." + self.config.model_architecture + "_" + self.config.framework + "_tile"
        return eval(func_str)(image_data, category_name, nms_thresh, score_thresh)

    def faster_rcnn_tensorflow_tile(self, image_data, category_name, nms_thresh, score_thresh):
        """使用numpy进行目标检测,输入图像数组，输出为特征数组
                :return:
                """
        return self.estimate.estimation_numpy(image_data, category_name, nms_thresh, score_thresh)

    def close_model(self):
        self.estimation.close_model()

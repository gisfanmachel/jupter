'''
    模型发布
'''
import cv2
import numpy as np
from typing import List, Iterable, Dict, Union

from pie.pre_center.common.pred_image import estimate_image
from pre_yolo_def import load_model, preprocess, postprocess, load_arguments


class PredictModel:
    def __init__(self):
        # 获取模型
        args = load_arguments(mode='estimate')
        self.args = args
        self.envs = args['trans_pipelines']

        model = load_model(**args)
        self.model = model.eval()

    # names和meta为可选参数，预留参数。函数返回类型是ndarray
    def predict(self, X: np.ndarray, X2: np.ndarray, names: Iterable[str] = None, meta: Dict = None) -> Union[
        np.ndarray, List, str, bytes]:

        args = self.args
        outputs = estimate_image(self.model, X, X2,self.envs, preprocess, postprocess,**args)
        return outputs


# if __name__ == '__main__':
#     x1 = cv2.imread("./0_1_A.tif")
#     x2 = cv2.imread("./0_1_B.tif")
#     # print(x.shape)
#     # model对象在http服务中会一直存在
#     model = PredictModel()
#     outputs = model.predict(x1,x2)
#     print(outputs.shape)
#     print(np.unique(outputs))
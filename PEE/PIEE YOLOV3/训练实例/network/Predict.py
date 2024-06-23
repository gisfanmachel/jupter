'''
    预测 dinknet
'''
from pie.pre_center.common.predict_step import predict_image
from pre_yolo_def import load_model, postprocess, \
    preprocess, load_arguments

if __name__ == '__main__':

    platform_arguments = load_arguments()

    model = load_model(**platform_arguments)
    print(platform_arguments)

    predict_image(**platform_arguments)
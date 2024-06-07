# uncompyle6 version 3.9.1
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.8.19 (default, Mar 20 2024, 19:55:45) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\semantic_seg\_seg_models\encs\preprocessing.py
# Compiled at: 2020-09-28 17:51:21
# Size of source mod 2**32: 1019 bytes
"""
Image pre-processing functions.
Images are assumed to be read in uint8 format (range 0-255).
"""
from keras.applications import vgg16
from keras.applications import vgg19
from keras.applications import densenet
from keras.applications import inception_v3
from keras.applications import inception_resnet_v2
identical = lambda x: x
bgr_transpose = lambda x: x[(..., None[None:-1])]
models_preprocessing = {'vgg16':vgg16.preprocess_input, 
 'vgg19':vgg19.preprocess_input, 
 'resnet18':bgr_transpose, 
 'resnet34':bgr_transpose, 
 'resnet50':bgr_transpose, 
 'resnet101':bgr_transpose, 
 'resnet152':bgr_transpose, 
 'resnext50':identical, 
 'resnext101':identical, 
 'densenet121':densenet.preprocess_input, 
 'densenet169':densenet.preprocess_input, 
 'densenet201':densenet.preprocess_input, 
 'inceptionv3':inception_v3.preprocess_input, 
 'inceptionresnetv2':inception_resnet_v2.preprocess_input}

def get_preprocessing(backbone):
    return models_preprocessing[backbone]

# -*- coding:utf-8 -*-
"""
@Project :   PyCharm
@File    :   __init__.py.py
@Time    :   2021/11/11 18:03 下午
@Author  :   lsw
@Version :   1.0
@Contact :   shi_weihappy@126.com
@License :   (C)Copyright 2020-2021, lsw
@Desc    :   None
"""
from pie.Classifier.classifierANN import PIEClassifierANN as ann
from pie.Classifier.classifierKNN import PIEClassifierKNN as knn
from pie.Classifier.classifierDT import PIEClassifierDT as dTrees
from pie.Classifier.classifierRT import PIEClassifierRT as rTrees
from pie.Classifier.classifierSVM import PIEClassifierSVM as svm
from pie.Classifier.classifierNormalBayes import PIEClassifierNormalBayes as normalBayes
from pie.Classifier.classifierBoost import PIEClassifierBoost as boost
from pie.Classifier.classifierSAM import PIEClassifierSAM as sam

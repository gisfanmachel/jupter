# -*- coding:utf-8 -*-
__version__ = "0.19.0"

from pie.utils import pieHttp
from pie.number import PIENumber as Number
from pie.string import PIEString as String
from pie.list import PIEList as List
from pie.date import PIEDate as Date
from pie.dictionary import PIEDictionary as Dictionary
from pie.projection import PIEProjection as Projection
from pie.export import PIEExport as Export
from pie.filter import Filter
from pie.kernel import PIEKernel as Kernel
from pie.reducer import Reducer
from pie.array import PIEArray as Array
from pie.model import Model
from pie.matrix import PIEMatrix as Matrix
from pie.palette import PIEPalette as Palette
from pie.confusionMatrix import PIEConfusionMatrix as ConfusionMatrix
from pie.vector import Geometry, Feature, FeatureCollection
from pie.image import Image, ImageCollection, Terrain
from pie.chart import PIEChart as Chart
from pie.map import Map
from pie.Algorithm import *
from pie.STK import *
from pie.Clusterer import *
from pie.Classifier import *
from pie.ui import *
from pie.utils.codeTools import parseCell, generateLink
from pie.utils.resourceTools import generateStorageURLs, checkStorageFiles
from pie.utils.taskTools import getTaskList, getTaskDetail, clearTask, cancelTask
from pie.utils.common import pngsToGif, vectorToGif

def authorization(name=None, password=None):
    """
    重新登录
    :param name:
    :param password:
    :return:
    """
    pieHttp.login(True, name, password)

def initialize(name=None, password=None):
    """
    初始化验证信息
    :param name:
    :param password:
    :return:
    """
    pieHttp.login(False, name, password)

def credentials():
    return pieHttp.getCredentials()
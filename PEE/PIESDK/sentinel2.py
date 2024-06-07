# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   sentinel2.py
@Time    :   2020/8/6 下午5:19
@Author  :   liuxiaodong
@Version :   1.0
@Contact :   2152550864@qq.com
@License :   (C)Copyright 2019-2020, liuxiaodong
@Desc    :   哨兵2处理算法
"""
from .object import PIEObject
from .utils.error import ArgsIsNull

class PIEPlugin_Sentinel2(PIEObject):
    def __init__(self):
        super(PIEPlugin_Sentinel2, self).__init__()
        self.pre = None
        self.statement = None

    @staticmethod
    def name():
        return "PIEPlugin_Sentinel2"

    @staticmethod
    def cloudMask(image):
        """
        哨兵2去云
        :param image:
        :return:
        """
        if image is None:
            raise ArgsIsNull("image")

        qaBand = image.select("QA60")
        cloudBitMask = 1 << 10
        cirrusBitMask = 1 << 11
        mask = qaBand.bitwiseAnd(cloudBitMask).And(qaBand.bitwiseAnd(cirrusBitMask))
        return mask
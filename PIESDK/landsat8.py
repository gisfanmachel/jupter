# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   landsat8.py
@Time    :   2020/8/6 下午5:19
@Author  :   liuxiaodong
@Version :   1.0
@Contact :   2152550864@qq.com
@License :   (C)Copyright 2019-2020, liuxiaodong
@Desc    :   None
"""
from .object import PIEObject
from .utils.error import ArgsIsNull

class PIEPlugin_Landsat8(PIEObject):
    def __init__(self):
        super(PIEPlugin_Landsat8, self).__init__()
        self.pre = None
        self.statement = None

    @staticmethod
    def name():
        return "PIEPlugin_Landsat8"

    @staticmethod
    def cloudMask(input):
        if input is None:
            raise ArgsIsNull("input")
        # 选择QA波段
        image_BQA = input.select("BQA")
        # 云比特位
        cloudsBitMask = 1 << 4
        # 云置信度比特位
        cloudConfidenceBitMask = 1 << 6
        # 云掩膜 云1，其他0
        mask1 = image_BQA.bitwiseAnd(cloudsBitMask)
        # 云置信度掩膜 云1，其他0
        mask2 = image_BQA.bitwiseAnd(cloudConfidenceBitMask)
        # 与运算
        mask = mask1.And(mask2)
        return mask
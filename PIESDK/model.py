# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   model.py
@Time    :   2020/8/6 下午5:19
@Author  :   liuxiaodong
@Version :   1.0
@Contact :   2152550864@qq.com
@License :   (C)Copyright 2019-2020, liuxiaodong
@Desc    :   None
"""
from pie.object import PIEObject
from pie.utils.error import ArgsIsNull

def _generatePIEModel(pre, statement):
    """
    生成 PIEModel 对象
    :param pre:
    :param statement:
    :return:
    """
    _object = PIEModel()
    _object.pre = pre
    _object.statement = statement
    return _object

def _generatePIEImage(pre, statement):
    """
    生成 PIEImage 对象
    :param pre:
    :param statement:
    :return:
    """
    from pie.image.image import PIEImage
    _object = PIEImage()
    _object.pre = pre
    _object.statement = statement
    return _object

class PIEModel(PIEObject):
    def __init__(self, args=None):
        super(PIEModel, self).__init__()
        if type(args).__name__ == self.name()\
            or type(args).__name__ == PIEObject.name():
            self.pre = args.pre
            self.statement = args.statement
        else:
            self.pre = None
            self.statement = self.getStatement(
                functionName = "Model.constructors",
                arguments = {"args": self.formatValue(args)}
            )

    @staticmethod
    def name():
        return "PIEModel"

    def listAiPlatModels(self, name):
        """
        根据名称罗列AI模型
        :param name:
        :return:
        """
        if name is None:
            raise ArgsIsNull("name")

        _obj = {
            "type": "Invocation",
            "arguments": {
                "name": name
            },
            "functionName": "Model.listAiPlatModels"
        }
        return _generatePIEModel(self, _obj)

    def fromAiPlatformPredictor(self, appname,username,tokenname,options=None):
        """
        生成预测器
        :param appname:
        :param username:
        :param tokenname:
        :param options:
        :return:
        """
        if appname is None \
            or username is None \
            or tokenname is None:
            raise ArgsIsNull('name、tileExtend')

        _obj = self.getStatement(
            functionName="Model.fromAiPlatformPredictor",
            arguments={
                "appname": appname,
                "username": username,
                "tokenname": tokenname,
                "options": options
            }
        )
        return _generatePIEModel(self, _obj)

    def predictImage(self, input):
        """
        预测结果
        :param input:
        :return:
        """
        if input is None:
            raise ArgsIsNull('input')

        _obj = self.getStatement(
            functionName="Model.predictImage",
            arguments={
                "model": self.statement,
                "image": self.formatValue(input)
            }
        )
        return _generatePIEImage(self, _obj)

    def predictChange(self, image1, image2):
        """
        预测变化
        :param image1:
        :param image2:
        :return:
        """
        if image1 is None or image2 is None:
            raise ArgsIsNull('image1,image2')

        _obj = self.getStatement(
            functionName="Model.predictChanges",
            arguments={
                "model": self.statement,
                "image1": self.formatValue(image1),
                "image2": self.formatValue(image2)
            }
        )
        return _generatePIEImage(self, _obj)

Model = PIEModel()




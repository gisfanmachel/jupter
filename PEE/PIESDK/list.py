# -*- coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   list.py
@Time    :   2020/10/10 上午10:14
@Author  :   lsw
@Version :   1.0
@Contact :   shi_weihappy@126.com
@License :   (C)Copyright 2019-2020, lsw
@Desc    :   None
"""
from pie.object import PIEObject, _generatePIEObject
from pie.utils.error import ArgsIsNull

def _generatePIEString(pre, statement):
    """
    生成 PIEString 对象
    :param pre:
    :param statement:
    :return:
    """
    from pie.string import PIEString
    _object = PIEString()
    _object.pre = pre
    _object.statement = statement
    return _object

def _generatePIENumber(pre, statement):
    """
    生成 PIENumber 对象
    :param pre:
    :param statement:
    :return:
    """
    from pie.number import PIENumber
    _object = PIENumber()
    _object.pre = pre
    _object.statement = statement
    return _object

def _generatePIEList(pre, statement):
    """
    生成 PIEList 对象
    :param pre:
    :param statement:
    :return:
    """
    _object = PIEList()
    _object.pre = pre
    _object.statement = statement
    return _object

def _generatePIEDictionary(pre, statement):
    """
    生成 PIEDictionary 对象
    :param pre:
    :param statement:
    :return:
    """
    from pie.dictionary import PIEDictionary
    _object = PIEDictionary()
    _object.pre = pre
    _object.statement = statement
    return _object

class PIEList(PIEObject):
    def __init__(self, args=None):
        super(PIEList, self).__init__()
        self.pre = None
        self.statement = None
        if args is None:
            return

        if type(args).__name__  == self.name() \
            or type(args).__name__ == PIEObject.name():
            self.pre = args.pre
            self.statement = args.statement
        else:
            self.pre = None
            self.statement = self.getStatement(
                functionName="List.constructors",
                arguments={"args": self.formatValue(args)}
            )

    @staticmethod
    def name():
        return "PIEList"

    def repeat(self, value, count):
        """
        生成指定数据的列表
        :param value:
        :param count:
        :return:
        """
        _obj = self.getStatement(
            functionName="List.repeat",
            arguments={
                "value": self.formatValue(value),
                "count": self.formatValue(count)
            }
        )
        return _generatePIEList(self, _obj)

    def add(self, value):
        """
        增加数据
        :param value:
        :return:
        """
        if value is None:
            raise ArgsIsNull("value")
        _input = self.statement
        _obj = self.getStatement(
            functionName="List.add",
            arguments={
                "input": _input,
                "value": self.formatValue(value)
            }
        )
        return _generatePIEList(self, _obj)

    def get(self, index):
        """
        获取指定索引数据
        :param index:
        :return:
        """
        if index is None:
            raise ArgsIsNull("index")

        _input = self.statement
        _obj = self.getStatement(
            functionName="List.get",
            arguments={
                "input": _input,
                "index": self.formatValue(index)
            },
            compute=True
        )
        return _generatePIEObject(self, _obj)

    def length(self):
        """
        返回长度
        :return:
        """
        _obj = self.getStatement(
            functionName="List.length",
            arguments={
                "input": self.statement
            },
            compute=True
        )
        return _generatePIENumber(self, _obj)

    def cat(self, right):
        """
        拼接
        :param right:
        :return:
        """
        if right is None:
            raise ArgsIsNull('right')
        _obj = self.getStatement(
            functionName="List.cat",
            arguments={
                "input": self.statement,
                "right": self.formatValue(right)
            },
            compute=True
        )
        return _generatePIEList(self, _obj)

    def equals(self, right):
        """
        判断相等
        :param right:
        :return:
        """
        if right is None:
            raise ArgsIsNull('right')
        _obj = self.getStatement(
            functionName="List.equals",
            arguments={
                "input": self.statement,
                "right": self.formatValue(right)
            },
            compute=True
        )
        return _generatePIEObject(self, _obj)

    def contains(self, right):
        """
        是否包含
        :param right:
        :return:
        """
        if right is None:
            raise ArgsIsNull('right')
        _obj = self.getStatement(
            functionName="List.contains",
            arguments={
                "input": self.statement,
                "right": self.formatValue(right)
            },
            compute=True
        )
        return _generatePIEObject(self, _obj)

    def containsAll(self, right):
        """

        :param right:
        :return:
        """
        if right is None:
            raise ArgsIsNull('right')
        _obj = self.getStatement(
            functionName="List.containsAll",
            arguments={
                "input": self.statement,
                "right": self.formatValue(right)
            },
            compute=True
        )
        return _generatePIEObject(self, _obj)

    def insert(self, index, element):
        """

        :param index:
        :param element:
        :return:
        """
        if index is None and element is None:
            raise ArgsIsNull('index,element')
        _obj = self.getStatement(
            functionName="List.insert",
            arguments={
                "input": self.statement,
                "index": self.formatValue(index),
                "element": self.formatValue(element)
            },
            compute=True
        )
        return _generatePIEList(self, _obj)

    def indexOf(self, element):
        """

        :param element:
        :return:
        """
        if element is None:
            raise ArgsIsNull('element')
        _obj = self.getStatement(
            functionName="List.indexOf",
            arguments={
                "input": self.statement,
                "element": self.formatValue(element)
            },
            compute=True
        )
        return _generatePIENumber(self, _obj)

    def getNumber(self, index):
        """

        :param index:
        :return:
        """
        if index is None:
            raise ArgsIsNull('index')
        _obj = self.getStatement(
            functionName="List.getNumber",
            arguments={
                "input": self.statement,
                "index": self.formatValue(index)
            },
            compute=True
        )
        return _generatePIENumber(self, _obj)

    def getString(self, index):
        """

        :param index:
        :return:
        """
        if index is None:
            raise ArgsIsNull('index')
        _obj = self.getStatement(
            functionName="List.getString",
            arguments={
                "input": self.statement,
                "index": self.formatValue(index)
            },
            compute=True
        )
        return _generatePIEString(self, _obj)

    def distinct(self):
        """
        去重
        :return:
        """
        _obj = self.getStatement(
            functionName="List.distinct",
            arguments={
                "input": self.statement
            }
        )
        return _generatePIEList(self, _obj)

    def reduce(self, reducer):
        """
        计算
        :param reducer:
        :return:
        """
        if reducer is None:
            raise ArgsIsNull('reducer')
        _obj = self.getStatement(
            functionName="List.reduce",
            arguments={
                "input": self.statement,
                "reducer": self.formatValue(reducer)
            }
        )
        return _generatePIEDictionary(self, _obj)

    def lastIndexOfSubList(self, target):
        """

        :param target:
        :return:
        """
        if target is None:
            raise ArgsIsNull("target")
        _input = self.statement
        _obj = self.getStatement(
            functionName="List.lastIndexOfSubList",
            arguments={
                "input": _input,
                "target": self.formatValue(target)
            },
            compute=True
        )
        return _generatePIENumber(self, _obj)


    def reverse(self):
        """
        反转
        :return:
        """
        _input = self.statement
        _obj = self.getStatement(
            functionName="List.reverse",
            arguments={
                "input": _input,
            }
        )
        return _generatePIEList(self, _obj)

    def rotate(self, distance):
        """

        :param distance:
        :return:
        """
        if distance is None:
            raise ArgsIsNull("distance")

        _input = self.statement
        _obj = self.getStatement(
            functionName="List.rotate",
            arguments={
                "input": _input,
                "distance": self.formatValue(distance)
            }
        )
        return _generatePIEList(self, _obj)

    def set(self, index, element):
        """

        :param index:
        :param element:
        :return:
        """
        if index is None or element is None:
            raise ArgsIsNull("index,element")
        _input = self.statement
        _obj = self.getStatement(
            functionName="List.set",
            arguments={
                "input": _input,
                "index": self.formatValue(index),
                "element": self.formatValue(element)
            },
            compute=True
        )
        return _generatePIEList(self, _obj)

    def slice(self, start, end, step):
        """

        :param start:
        :param end:
        :param step:
        :return:
        """
        if start is None or end is None or step is None:
            raise ArgsIsNull("start,end,step")

        _input = self.statement
        _obj = self.getStatement(
            functionName="List.slice",
            arguments={
                "input": _input,
                "start": self.formatValue(start),
                "end": self.formatValue(end),
                "step": self.formatValue(step)
            },
            compute=True
        )

        return _generatePIEList(self, _obj)

    def splice(self, start, count, other):
        """

        :param start:
        :param count:
        :param other:
        :return:
        """
        if start is None or count is None or other is None:
            raise ArgsIsNull("start,count,other")

        _input = self.statement
        _obj = self.getStatement(
            functionName="List.splice",
            arguments={
                "input": _input,
                "start": self.formatValue(start),
                "count": self.formatValue(count),
                "other": self.formatValue(other)
            },
            compute=True
        )

        return _generatePIEList(self, _obj)

    def swap(self, pos1, pos2):
        """
        交换
        :param pos1:
        :param pos2:
        :return:
        """
        if pos1 is None or pos2 is None:
            raise ArgsIsNull("pos1,pos2")
        _input = self.statement
        _obj = self.getStatement(
            functionName="List.swap",
            arguments={
                "input": _input,
                "pos1": self.formatValue(pos1),
                "pos2":self.formatValue(pos2)
            },
            compute=True
        )

        return _generatePIEList(self, _obj)

    def zip(self, other):
        """

        :param other:
        :return:
        """
        if other is None:
            raise ArgsIsNull("other")

        _input = self.statement
        _obj = self.getStatement(
            functionName="List.zip",
            arguments={
                "input": _input,
                "other": self.formatValue(other)
            },
            compute=True
        )

        return _generatePIEList(self, _obj)

    def remove(self, element):
        """

        :param element:
        :return:
        """
        if element is None:
            raise ArgsIsNull("element")
        _input = self.statement
        _obj = self.getStatement(
            functionName="List.remove",
            arguments={
                "input": _input,
                "element": self.formatValue(element)
            },
            compute=True
        )

        return _generatePIEList(self, _obj)

    def removeAll(self, other):
        """

        :param other:
        :return:
        """
        if other is None:
            raise ArgsIsNull("other")
        _input = self.statement
        _obj = self.getStatement(
            functionName="List.removeAll",
            arguments={
                "input": _input,
                "other": self.formatValue(other)
            },
            compute=True
        )

        return _generatePIEList(self, _obj)

    def sequence(self, start, end, count, step=1):
        """

        @param start:
        @param end:
        @param count:
        @param step:
        @return:
        """
        if start is None \
            or end is None \
            or count is None \
            or step is None:
            raise ArgsIsNull("start,end,step")

        _input = self.statement
        _obj = self.getStatement(
            functionName="List.sequence",
            arguments={
                "input": _input,
                "start": self.formatValue(start),
                "count": self.formatValue(count),
                "end": self.formatValue(end),
                "step": self.formatValue(step),
            },
            compute=True
        )

        return _generatePIEList(self, _obj)

    def map(self, algorithm, dropNulls):
        """

        :param algorithm:
        :param dropNulls:
        :return:
        """
        objElement = {
            "type": "Function",
            "arguments": [
                "_MAPPING_VAR_0_0"
            ]
        }
        _lists = list([_generatePIEObject(self, objElement)])
        _listMap = list(map(algorithm, _lists))
        _body = self.formatValue(_listMap[0])
        _baseAlgorithm = {
            "type": "Function",
            "arguments": [
                "_MAPPING_VAR_0_0"
            ],
            "body": _body
        }
        _obj = self.getStatement(
            functionName="List.map",
            arguments={
                "collection": self.statement,
                "baseAlgorithm": _baseAlgorithm
            }
        )
        return _generatePIEList(self, _obj)






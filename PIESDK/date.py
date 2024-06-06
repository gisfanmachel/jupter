# -*-coding:utf-8 -*-
"""
@Project :   PIE-Engine-Python
@File    :   date.py
@Time    :   2020/8/6 下午5:19
@Author  :   liuxiaodong
@Version :   1.0
@Contact :   2152550864@qq.com
@License :   (C)Copyright 2019-2020, liuxiaodong
@Desc    :   None
"""
import datetime
import pytz
from pie.object import PIEObject
from pie.utils.error import ArgsIsNull, ArgsRangeIsError

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

def _generatePIEDate(pre, statement):
    """
    生成 PIEDate 对象
    :param pre:
    :param statement:
    :return:
    """
    _object = PIEDate()
    _object.pre = pre
    _object.statement = statement
    return _object

class PIEDate(PIEObject):
    def __init__(self, data=None, timeZone=None):
        super(PIEDate, self).__init__()

        self.pre = None
        self.statement = None
        if data is None:
            return
        timeZone = timeZone if timeZone else "Asia/Shanghai"
        utc_tz = pytz.timezone(timeZone)
        if isinstance(data, datetime.datetime):
            data = data.replace(tzinfo=utc_tz).strftime("%Y-%m-%d %H:%M:%S")
            self.statement = self.getStatement(
                functionName="Date.constructors",
                arguments={
                    "date": data,
                    "timeZone": timeZone
                }
            )
        elif isinstance(data, datetime.date):
            data = datetime.datetime(data.year, data.month, data.day)
            data = data.replace(tzinfo=utc_tz).strftime("%Y-%m-%d %H:%M:%S")
            self.statement = self.getStatement(
                functionName="Date.constructors",
                arguments={
                    "date": data,
                    "timeZone": timeZone
                }
            )
        elif isinstance(data, str):
            data_list = data.strip().split(" ")
            if len(data_list) == 2:
                data = datetime.datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
            else:
                data = datetime.datetime.strptime(data, "%Y-%m-%d")
            data = data.replace(tzinfo=utc_tz).strftime("%Y-%m-%d %H:%M:%S")
            self.statement = self.getStatement(
                functionName="Date.constructors",
                arguments={
                    "date": data,
                    "timeZone": timeZone
                }
            )
        elif isinstance(data, int) or isinstance(data, float):
            data = datetime.datetime.fromtimestamp(data/1000)
            data = data.replace(tzinfo=utc_tz).strftime("%Y-%m-%d %H:%M:%S")
            self.statement = self.getStatement(
                functionName="Date.constructors",
                arguments={
                    "date": data,
                    "timeZone": timeZone
                }
            )
        elif type(data).__name__ == self.name() \
                or type(data).__name__ == PIEObject.name():
            self.pre = data.pre
            self.statement = data.statement
        elif type(data).__name__ in ["PIENumber","PIEString"]:
            self.statement = self.getStatement(
                functionName="Date.constructors",
                arguments={
                    "date": self.getStatement(data),
                    "timeZone": timeZone
                }
            )

    @staticmethod
    def name():
        return "PIEDate"

    def _now(self, timeZone="Asia/Shanghai"):
        """
        获取当前时间
        @param timeZone:
        @return:
        """
        _obj = self.getStatement(
            functionName="Date.now",
            arguments={
                "timeZone": timeZone
            }
        )
        return _generatePIEDate(self, _obj)

    @staticmethod
    def now(timeZone="Asia/Shanghai"):
        """
        返回当前系统的时间
        @param timeZone:
        @return:
        """
        return PIEDate()._now(timeZone)

    def _fromYMD(self, year, month, day, timeZone=None):
        """
        解析年月日
        @param year:
        @param month:
        @param day:
        @param timeZone:
        @return:
        """
        if year is None or month is None or day is None:
            raise ArgsIsNull("参数不能为空")
        if year <= 0 or year > 9999:
            raise ArgsRangeIsError("year")
        if month <= 0 or month > 12:
            raise ArgsRangeIsError("month")
        if day <= 0 or day > 31:
            raise ArgsRangeIsError("day")

        _obj = self.getStatement(functionName="Date.fromYMD",
                                 arguments={
                                     "year": year,
                                     "month": month,
                                     "day": day,
                                     "timeZone": timeZone
                                 })
        return _generatePIEDate(self, _obj)

    @staticmethod
    def fromYMD(year, month, day, timeZone="Asia/Shanghai"):
        """
        解析年月日
        @param year:
        @param month:
        @param day:
        @param timeZone:
        @return:
        """
        return PIEDate()._fromYMD(year, month, day, timeZone)

    def _parse(self, format, date, timeZone="Asia/Shanghai"):
        """

        @param format:
        @param date:
        @param timeZone:
        @return:
        """
        if not format or not date:
            raise ArgsIsNull("format,date")
        _obj = self.getStatement(functionName="Date.parse",
                                 arguments={
                                     "format": format,
                                     "date": date,
                                     "timeZone": timeZone,
                                 })
        return _generatePIEDate(self, _obj)

    @staticmethod
    def parse(format, date, timeZone="Asia/Shanghai"):
        """
        按指定格式解析日期时间
        @param format:
        @param date:
        @param timeZone:
        @return:
        """
        return PIEDate()._parse(format, date, timeZone)

    def get(self, unit="day", timeZone="Asia/Shanghai"):
        """
        获取指定日期类型的值
        :param unit:
        :param timeZone:
        :return:
        """
        if unit is None:
            raise ArgsIsNull('unit')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Date.get",
            arguments={
                "input": _input,
                "unit": self.formatValue(unit),
                "timeZone": timeZone
            }
        )
        return _generatePIENumber(self, _obj)

    def difference(self, start, unit="day"):
        """

        :param start:
        :param unit:
        :return:
        """
        if not start or not unit:
            raise ArgsIsNull('start,unit')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Date.difference",
            arguments={
                "input": _input,
                "start": self.formatValue(start),
                "unit": self.formatValue(unit)
            }
        )
        return _generatePIENumber(self, _obj)

    def getFraction(self, unit="day"):
        """
        :param unit:
        :return:
        """
        if not unit:
            raise ArgsIsNull('unit')
        _input = self.statement
        _obj = self.getStatement(
            functionName="Date.getFraction",
            arguments={
                "input": _input,
                "unit": self.formatValue(unit)
            }
        )
        return _generatePIENumber(self, _obj)

    def format(self, pattern, timeZone="Asia/Shanghai"):
        """
        @param pattern:
        @param timeZone:
        @return:
        """
        if not pattern:
            raise ArgsIsNull('pattern')
        _input = self.statement
        _obj = self.getStatement(functionName="Date.format",
                                 arguments={
                                     "input": _input,
                                     "format": self.formatValue(pattern),
                                     "timeZone": timeZone,
                                 })
        return _generatePIEString(self, _obj)

    def millis(self):
        """
        返回毫秒数
        @return:
        """
        _input = self.statement
        _obj = self.getStatement(
            functionName="Date.millis",
            arguments={
                "input": _input
            })
        return _generatePIENumber(self, _obj)

    def advance(self, delta, unit="day", timeZone="Asia/Shanghai"):
        """
        获取指定间隔日期的时间
        @param delta:
        @param unit:
        @param timeZone:
        @return:
        """
        if not isinstance(delta, int) \
            or isinstance(delta, float):
            raise ArgsIsNull('delta')
        units = ['year', 'month' 'week', 'day', 'hour', 'minute', 'second']
        if unit not in units:
            raise ArgsRangeIsError("year,month,week,day,hour,minute,second'")

        _input = self.statement
        _obj = self.getStatement(functionName="Date.advance",
                                 arguments={
                                     "input": _input,
                                     "delta": self.formatValue(delta),
                                     "unit": self.formatValue(unit),
                                     "timeZone": timeZone
                                 })

        return _generatePIEDate(self, _obj)

    def toString(self, timeZone="Asia/Shanghai"):
        """
        @param timeZone:
        @return:
        """
        _input = self.statement
        _obj = self.getStatement(functionName="Date.toString",
                                 arguments={
                                     "input": _input,
                                     "timeZone": timeZone
                                 })
        return _generatePIEString(self, _obj)
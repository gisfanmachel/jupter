# -*- coding: utf-8 -*-
"""
@Project : PIE-Engine-Python 
@File    : mapstyle.py
@Time    : 2023/2/26 12:07
@Author  : lishiwei
@Version : 1.0
@Contact : shi_weihappy@126.com
@License : (C)Copyright 2022-2023, lishiwei
@Desc    : None
"""
from pie.utils.colorTools import convertColorToHex

def formatStyle(style):
    if not style:
        style = {}
        return style
    if not isinstance(style, dict):
        print("样式style只能为字典对象数据！")
        return {}
    style_color = style.get("color", None)
    if style_color is not None:
        color = convertColorToHex(style_color)
        if color:
            style["color"] = color[:7]
    if "fillColor" in style:
        _fillColor = style.get("fillColor")
    elif "fill-color" in style:
        _fillColor = style.get("fill-color")
    else:
        _fillColor = None
    if _fillColor is not None:
        fillColor = convertColorToHex(_fillColor)
        if fillColor:
            style["fillColor"] = fillColor
    if "palette" in style:
        style_palette = style.get("palette")
        if isinstance(style_palette, str):
            palette = style_palette.split(",")
            temp = []
            for p in palette:
                p = p.strip()
                if not p:
                    continue
                temp.append(p)
            palette = temp
        elif isinstance(style_palette, (list, set)):
            temp = []
            for p in style_palette:
                p = p.strip()
                if not p:
                    continue
                temp.append(p)
            palette = temp
        else:
            print("颜色图例palette只能为数组列表或者字符串！")
            return {}
        temp = []
        for p in palette:
            color = convertColorToHex(p)
            if color:
                temp.append(color.replace("#", ""))
            else:
                temp.append(color)
        style["palette"] = ",".join(temp)
    return style

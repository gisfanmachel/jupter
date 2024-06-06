# -*- coding: utf-8 -*-
"""
@Project : PIE-Engine-Python 
@File    : colorTools.py
@Time    : 2023/2/26 12:05
@Author  : lishiwei
@Version : 1.0
@Contact : shi_weihappy@126.com
@License : (C)Copyright 2022-2023, lishiwei
@Desc    : None
"""
import math
import random
import re


def getRandomColor():
    """
    随机颜色
    :return: 
    """
    colors = list(colorNameAndHex().values())
    index = math.floor(random.random() * len(colors))
    if 0 <= index < len(colors):
        return colors[index]
    return colors[0]

def colorNameAndHex():
    """颜色名称对比表"""
    return {
        "aliceblue": "#f0f8ff",
        "antiquewhite": "#faebd7",
        "aqua": "#00ffff",
        "aquamarine": "#7fffd4",
        "azure": "#f0ffff",
        "beige": "#f5f5dc",
        "bisque": "#ffe4c4",
        "black": "#000000",
        "blanchedalmond": "#ffebcd",
        "blue": "#0000ff",
        "blueviolet": "#8a2be2",
        "brown": "#a52a2a",
        "burlywood": "#deb887",
        "cadetblue": "#5f9ea0",
        "chartreuse": "#7fff00",
        "chocolate": "#d2691e",
        "coral": "#ff7f50",
        "cornflowerblue": "#6495ed",
        "cornsilk": "#fff8dc",
        "crimson": "#dc143c",
        "cyan": "#00ffff",
        "darkblue": "#00008b",
        "darkcyan": "#008b8b",
        "darkgoldenrod": "#b8860b",
        "darkgray": "#a9a9a9",
        "darkgreen": "#006400",
        "darkgrey": "#a9a9a9",
        "darkkhaki": "#bdb76b",
        "darkmagenta": "#8b008b",
        "darkolivegreen": "#556b2f",
        "darkorange": "#ff8c00",
        "darkorchid": "#9932cc",
        "darkred": "#8b0000",
        "darksalmon": "#e9967a",
        "darkseagreen": "#8fbc8f",
        "darkslateblue": "#483d8b",
        "darkslategray": "#2f4f4f",
        "darkslategrey": "#2f4f4f",
        "darkturquoise": "#00ced1",
        "darkviolet": "#9400d3",
        "deeppink": "#ff1493",
        "deepskyblue": "#00bfff",
        "dimgray": "#696969",
        "dimgrey": "#696969",
        "dodgerblue": "#1e90ff",
        "firebrick": "#b22222",
        "floralwhite": "#fffaf0",
        "forestgreen": "#228b22",
        "fuchsia": "#ff00ff",
        "gainsboro": "#dcdcdc",
        "ghostwhite": "#f8f8ff",
        "goldenrod": "#daa520",
        "gold": "#ffd700",
        "gray": "#808080",
        "green": "#008000",
        "greenyellow": "#adff2f",
        "grey": "#808080",
        "honeydew": "#f0fff0",
        "hotpink": "#ff69b4",
        "indianred": "#cd5c5c",
        "indigo": "#4b0082",
        "ivory": "#fffff0",
        "khaki": "#f0e68c",
        "lavenderblush": "#fff0f5",
        "lavender": "#e6e6fa",
        "lawngreen": "#7cfc00",
        "lemonchiffon": "#fffacd",
        "lightblue": "#add8e6",
        "lightcoral": "#f08080",
        "lightcyan": "#e0ffff",
        "lightgoldenrodyellow": "#fafad2",
        "lightgray": "#d3d3d3",
        "lightgreen": "#90ee90",
        "lightgrey": "#d3d3d3",
        "lightpink": "#ffb6c1",
        "lightsalmon": "#ffa07a",
        "lightseagreen": "#20b2aa",
        "lightskyblue": "#87cefa",
        "lightslategray": "#778899",
        "lightslategrey": "#778899",
        "lightsteelblue": "#b0c4de",
        "lightyellow": "#ffffe0",
        "lime": "#00ff00",
        "limegreen": "#32cd32",
        "linen": "#faf0e6",
        "magenta": "#ff00ff",
        "maroon": "#800000",
        "mediumaquamarine": "#66cdaa",
        "mediumblue": "#0000cd",
        "mediumorchid": "#ba55d3",
        "mediumpurple": "#9370db",
        "mediumseagreen": "#3cb371",
        "mediumslateblue": "#7b68ee",
        "mediumspringgreen": "#00fa9a",
        "mediumturquoise": "#48d1cc",
        "mediumvioletred": "#c71585",
        "midnightblue": "#191970",
        "mintcream": "#f5fffa",
        "mistyrose": "#ffe4e1",
        "moccasin": "#ffe4b5",
        "navajowhite": "#ffdead",
        "navy": "#000080",
        "oldlace": "#fdf5e6",
        "olive": "#808000",
        "olivedrab": "#6b8e23",
        "orange": "#ffa500",
        "orangered": "#ff4500",
        "orchid": "#da70d6",
        "palegoldenrod": "#eee8aa",
        "palegreen": "#98fb98",
        "paleturquoise": "#afeeee",
        "palevioletred": "#db7093",
        "papayawhip": "#ffefd5",
        "peachpuff": "#ffdab9",
        "peru": "#cd853f",
        "pink": "#ffc0cb",
        "plum": "#dda0dd",
        "powderblue": "#b0e0e6",
        "purple": "#800080",
        "rebeccapurple": "#663399",
        "red": "#ff0000",
        "rosybrown": "#bc8f8f",
        "royalblue": "#4169e1",
        "saddlebrown": "#8b4513",
        "salmon": "#fa8072",
        "sandybrown": "#f4a460",
        "seagreen": "#2e8b57",
        "seashell": "#fff5ee",
        "sienna": "#a0522d",
        "silver": "#c0c0c0",
        "skyblue": "#87ceeb",
        "slateblue": "#6a5acd",
        "slategray": "#708090",
        "slategrey": "#708090",
        "snow": "#fffafa",
        "springgreen": "#00ff7f",
        "steelblue": "#4682b4",
        "tan": "#d2b48c",
        "teal": "#008080",
        "thistle": "#d8bfd8",
        "tomato": "#ff6347",
        "turquoise": "#40e0d0",
        "violet": "#ee82ee",
        "wheat": "#f5deb3",
        "white": "#ffffff",
        "whitesmoke": "#f5f5f5",
        "yellow": "#ffff00",
        "yellowgreen": "#9acd32"
    }

def getColorByName(name):
    """
    通过颜色的名称获取对应的16进制Hex值
    :param name:
    :return:
    """
    if not name:
        return None
    name = name.strip()
    allColors = colorNameAndHex()
    return allColors.get(name)

def getValidColorName():
    """
    返回有效的颜色名称列表
    :return:
    """
    return colorNameAndHex().keys()

def colorRgb (sColor):
    """
    将hex表示方式转换为rgb表示方式(这里返回rgb数组模式)
    :param sColor:
    :return:
    """
    reg = r"^#([0-9a-fA-f]{3}|[0-9a-fA-f]{6})$"
    if sColor and re.match(reg, sColor):
        if len(sColor) == 4:
            sColorNew = "#"
            for i in range(1, 4):
                sColorNew += sColor.slice(i, i + 1).concat(sColor.slice(i, i + 1))
            sColor = sColorNew
        #处理六位的颜色值
        sColorChange = []
        for j in range(1, 7, 2):
            sColorChange.append(int("0x" + sColor.slice(j, j + 2)))
        return sColorChange
    else:
        return sColor

# /**
#  * 将颜色字符串转为Hex格式
#  */
def convertColorToHex(color):
    if not color or not isinstance(color, str):
        print(f"转换的参数{color}必须为字符串！")
        return None

    color = color.lower().strip()
    sColorNew = getColorByName(color)
    if sColorNew:
        return sColorNew

    hexReg = r"^#([0-9a-fA-f]{3}|[0-9a-fA-f]{6}|[0-9a-fA-f]{8})$"
    if re.match(hexReg, color):
        if len(color) == 4:
            sColorNew = "#"
            for i in range(1, 4):
                sColorNew += f"{color[i]}{color[i]}"
            return sColorNew
        elif len(color) == 7 or len(color) == 9:
            return color
        else:
            print(f"颜色{color}格式不正确！")
            return None
    hexReg2 = r"^([0-9a-fA-f]{3}|[0-9a-fA-f]{6}|[0-9a-fA-f]{8})$"
    if re.match(hexReg2, color):
        sColorNew = "#"
        if len(color) == 3:
            for i in range(1, 4):
                sColorNew += f"{color[i]}{color[i]}"
            return sColorNew
        elif len(color) == 6 or len(color) == 8:
            return sColorNew+color
        else:
            print(f"颜色{color}格式不正确！")
            return None

    rgbReg = r"^rgb"
    if re.match(rgbReg, color):
        color = color.replace("rgb", "").replace("rgba", "").replace("(", "").replace(")", "")
        aColor = color.split(",")
        if len(aColor) < 3:
            print(f"颜色{color}格式不正确！")
            return None
        strHex = "#"
        for i in range(len(aColor)):
            if i > 3:
                print("颜色数组rgba最大是4组！")
                break
            try:
                temp = int(aColor[i])
            except Exception as e:
                temp = int(aColor[i], 16)
            if temp < 16:
                _hex = f"0{hex(temp)}"
            else:
                _hex = hex(temp)
            strHex += _hex
        return strHex
    return None

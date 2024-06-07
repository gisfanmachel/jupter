'''
    @author: yuchende
    @create date: 2020.6.10
    @function:
        将单通道 图片转换为 多通道图片
        0~4 单通道像素值取值范围，每个数字代表一个分类
        


'''


from PIL import Image
import matplotlib.pyplot as plt
import os

classes = [0,1,2,3,4]
color = [(0,0,0),(0,255,127),(220,20,60),(255,255,0),(0,191,255)]
#  黑色 - 其他 - 0 ,绿色 - 植被 - 1 , 红色 - 道路 - 2, 黄色 - 建筑 - 3 ,蓝色 - 河流 - 4
#  植被（标记1）、建筑（标记2）、水体（标记3）、道路（标记4）以及其他(标记0)

base_path = r'E:\dataset\BDCI2017-jiage-Semi\training\label'
save_path = r'E:\dataset\BDCI2017-jiage-Semi\training\labels'

img_name = os.listdir(base_path)

def sigleToThree(img_path,save_path):
    img1 = Image.open(img_path)  #打开图像
    img2 = Image.new("RGB",img1.size)
    print(img1.size)
    print(img2.size)
    for x in range(0,img1.size[0]):
        for y in range(0,img2.size[1]):
            k = img1.getpixel((x,y))
            img2.putpixel((x,y),color[k])
    print('finshed:  ' + img_path)
    img2.show()
    img2.save(save_path)

# begin to translate

for i in range(len(img_name)):
    sigleToThree(os.path.join(base_path + '/',img_name[i]), os.path.join(save_path + '/', img_name[i]))

print('translate end')
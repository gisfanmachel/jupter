
文件夹 ./training/label
	这个文件夹中，是单通道图片，即看着是黑白图的标签。

	像素值    分类代表
	0 ------- 其他
	1 ------- 植被
	2 ------- 道路
	3 ------- 建筑
	4 ------- 河流

文件夹 ./training/labels
	彩色标签的每个颜色，分类
		color = [(0,0,0),(0,255,127),(220,20,60),(255,255,0),(0,191,255)]
		#  黑色 - 其他 - 0 ,绿色 - 植被 - 1 , 红色 - 道路 - 2, 黄色 - 建筑 - 3 ,蓝色 - 河流 - 4
	
	
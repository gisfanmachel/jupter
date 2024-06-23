模型上传压缩包分为两部分：
1.networkMeta.json 
	说明网络结构代码的相关内容，包括必填项和选填项。
	必填项：
		name:  网络结构名称，例如：dinknet
		description：网络结构描述，例如：该模型是基于pytorch 1.2深度学习框架
		language： 代码的语言名称，例如：python
		weight_format: 训练模型生成的权重文件后缀，例如：TH

	选填项：
		networkImage:  网络结构构造图,名称固定为"model.jpg",
		input_h:  模型适合的图片大小,
		input_w: 模型适合的图片大小,
		input_data_type: 输入图片的数据类型，例如："byte",
		input_interval: 输入图片的样式，例如："bip",
		input_bands: 输入图片的维度，例如："3",
		output_format: "ndarray ,geojson",
		output_data_type: 输出图片的数据类型，例如："byte",
		output_bands: 输出图片的维度，例如："3"
			
	详细信息可查看networkMeta.json文件
	相关书写规范需严格按照json格式
	
2.network文件夹
	存放训练代码，包括模型训练代码及预测代码
	
	注：1. 网络结构代码中包含trin.py、Predinct.py 、PredictModel.py
		2. train.py 训练脚本名称，获取得到输入参数（参数详情可参照traincfg.json）
		3. Predict.py 模型评估。输入图片，进行预测后生成图片，保存并可查看；
			输入参数：image_path(图片路径)、weight_path(权重文件路径)、gpu_num(使用gpu个数)
			输出：语义分割、变化检测：ndarray数组
				  目标识别：geojson 包括 类别,概率,矩形坐标
		4. PredictModel.py  模型预测。输入图片路径，输出的是预测后的数组或目标识别预测后的geojson文件
			输入参数：image_path(图片路径)、weight_path(权重文件路径)、gpu_num(使用gpu个数)
			输出：语义分割、变化检测、目标识别：生成图片
		5. 输出内容包括：
			权重文件：存放在basedir本地文件夹中
			中间输出图片：存放在basedir+'/picture'，根据不同类型，图片名称固定
			语义分割：
				image.png 原始图片名称
				label.png 标签图片名称
				pred.png  预测图片名称
			变化检测：
				A.png  变化前图片名称
				B.png  变化后图片名称
				label.png 标签图片名称
				pred.png  预测图片名称
			目标识别：
				pred.png 预测图片名称
			
				
		
ģ���ϴ�ѹ������Ϊ�����֣�
1.networkMeta.json 
	˵������ṹ�����������ݣ������������ѡ���
	�����
		name:  ����ṹ���ƣ����磺dinknet
		description������ṹ���������磺��ģ���ǻ���pytorch 1.2���ѧϰ���
		language�� ������������ƣ����磺python
		weight_format: ѵ��ģ�����ɵ�Ȩ���ļ���׺�����磺TH

	ѡ���
		networkImage:  ����ṹ����ͼ,���ƹ̶�Ϊ"model.jpg",
		input_h:  ģ���ʺϵ�ͼƬ��С,
		input_w: ģ���ʺϵ�ͼƬ��С,
		input_data_type: ����ͼƬ���������ͣ����磺"byte",
		input_interval: ����ͼƬ����ʽ�����磺"bip",
		input_bands: ����ͼƬ��ά�ȣ����磺"3",
		output_format: "ndarray ,geojson",
		output_data_type: ���ͼƬ���������ͣ����磺"byte",
		output_bands: ���ͼƬ��ά�ȣ����磺"3"
			
	��ϸ��Ϣ�ɲ鿴networkMeta.json�ļ�
	�����д�淶���ϸ���json��ʽ
	
2.network�ļ���
	���ѵ�����룬����ģ��ѵ�����뼰Ԥ�����
	
	ע��1. ����ṹ�����а���trin.py��Predinct.py ��PredictModel.py
		2. train.py ѵ���ű����ƣ���ȡ�õ������������������ɲ���traincfg.json��
		3. Predict.py ģ������������ͼƬ������Ԥ�������ͼƬ�����沢�ɲ鿴��
			���������image_path(ͼƬ·��)��weight_path(Ȩ���ļ�·��)��gpu_num(ʹ��gpu����)
			���������ָ�仯��⣺ndarray����
				  Ŀ��ʶ��geojson ���� ���,����,��������
		4. PredictModel.py  ģ��Ԥ�⡣����ͼƬ·�����������Ԥ���������Ŀ��ʶ��Ԥ����geojson�ļ�
			���������image_path(ͼƬ·��)��weight_path(Ȩ���ļ�·��)��gpu_num(ʹ��gpu����)
			���������ָ�仯��⡢Ŀ��ʶ������ͼƬ
		5. ������ݰ�����
			Ȩ���ļ��������basedir�����ļ�����
			�м����ͼƬ�������basedir+'/picture'�����ݲ�ͬ���ͣ�ͼƬ���ƹ̶�
			����ָ
				image.png ԭʼͼƬ����
				label.png ��ǩͼƬ����
				pred.png  Ԥ��ͼƬ����
			�仯��⣺
				A.png  �仯ǰͼƬ����
				B.png  �仯��ͼƬ����
				label.png ��ǩͼƬ����
				pred.png  Ԥ��ͼƬ����
			Ŀ��ʶ��
				pred.png Ԥ��ͼƬ����
			
				
		
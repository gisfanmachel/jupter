import xml.etree.ElementTree as ET
import requests
from boto3.session import Session
from botocore.client import Config
import io
from PIL import Image
import numpy as np
import os
from concurrent.futures import ThreadPoolExecutor
from urllib3 import encode_multipart_formdata

try:
    from osgeo import gdal
except ImportError:
    import gdal

#aiUrl = os.environ['AI_DATASET']
# aiUrl = os.getenv('AI_DATASET', 'null')
aiUrl = "http://161.189.202.63:30094/pie_training_dataset/"

class s3GetImg:

    def __init__(self, datasetId=None):
        if datasetId == None:
            datasetId = os.getenv('AI_DATASET_ID', 'null')
        accessKey, secretKey, region, bucketName, datasetPath = self.getS3Params(datasetId)
        session = Session(aws_access_key_id=accessKey,
                          aws_secret_access_key=secretKey,
                          region_name=region)
        s3_config = Config(max_pool_connections=200, retries={'max_attempts': 20})
        self.s3 = session.client('s3', config=s3_config)
        self.bucketName = bucketName
        self.path = datasetPath
        self.gdal = self.getGDAL(accessKey,secretKey,region)

    def getS3Params(self, datasetId):
        headers = {
            "x-api": "engine.ai.getS3Params",
            "x-app": "75559a0d4d1689fcb26793f39d772a31",
            "x-client": "WEB",
            "x-gw-version": "2",
            "x-host-app-id": "engine",
            "x-nonce": "0cd5ed87-7bd8-4a8e-93a7-ce6697326252",
            "x-ts": "1619489324528"
        }
        url = aiUrl + "uploadS3/getS3Params?datasetId=" + datasetId
        requests.DEFAULT_RETRIES = 3
        ret = requests.get(url, headers=headers)
        ret.raise_for_status()
        ret.close()
        data = ret.json().get('data')
        if data:
            accessKey = data.get('accessKey')
            secretKey = data.get('secretKey')
            bucketName = data.get('bucketName')
            region = data.get('region')
            datasetPath = data.get('keyPrefix')
        else:
            raise RuntimeError("Not get S3 params: " + url + "\n")
        return accessKey, secretKey, region, bucketName, datasetPath

    def pullImage(self, filepath,upload_key=None):
        if upload_key is None:
            upload_key = self.path
        if upload_key.split('/')[-1].split('.')[-1] != '':
            list = [upload_key]
            one_img=True
        else:
            list=self.getImages(os.path.join(upload_key,'train'),True)+self.getImages(os.path.join(upload_key,'valid'),True)
            one_img = False
        with ThreadPoolExecutor(max_workers=20) as executor:
            for i in list:
                if i.split('/')[-1].split('.')[-1] !='':
                    if one_img:
                        new_path=filepath
                    else:
                        x=(i.split('/')[-3]+i.split(i.split('/')[-3])[-1]).replace((i.split('/')[-3]+i.split(i.split('/')[-3])[-1]).split('/')[-1],'')
                        new_path = os.path.join(filepath, x)
                    if not os.path.exists(new_path):
                        os.makedirs(new_path)
                    isWeight = False
                    upload_weight_key = i
                    if upload_weight_key.split('/')[0] == 's3:':
                        upload_weight_key = "/".join(upload_weight_key.split("/")[3:])
                    try:
                        s3WightKey = self.s3.head_object(Bucket=self.bucketName, Key=upload_weight_key)
                    except:
                        return isWeight
                    kwards={
                            "s3WightKey":s3WightKey,
                            "filename":os.path.join(new_path,upload_weight_key.split('/')[-1]),
                            "key":upload_weight_key
                        }
                    executor.submit(self.down,**kwards)
    def down(self,**kwargs):
        s3WightKey=kwargs.get('s3WightKey')
        filename=kwargs.get('filename')
        upload_weight_key=kwargs.get('key')
        try:
            if s3WightKey:
                self.s3.download_file(Filename=filename, Key=upload_weight_key,
                                      Bucket=self.bucketName)
        except:
            raise RuntimeError("Not get img: %s " % (upload_weight_key))

    def getFileList(self, filepath):
        keyNamePrefix = filepath
        if keyNamePrefix.split('/')[0] == 's3:':
            keyNamePrefix = "/".join(keyNamePrefix.split("/")[3:])

        paginator = self.s3.get_paginator('list_objects_v2')
        files = []
        responseIterator = paginator.paginate(
            Bucket=self.bucketName,
            Prefix=keyNamePrefix
        )
        for page in responseIterator:
            if "Contents" in page:
                for n in page["Contents"]:
                    key = n["Key"]
                    files.append(key)

        if len(files) == 0:
            raise RuntimeError("Found 0 files in subfolders of: " + filepath + "\n")
        return files

    def getImages(self, datasetPath,is_xml=False):
        keyNamePrefix = datasetPath
        if keyNamePrefix.split('/')[0] == 's3:':
            keyNamePrefix = "/".join(keyNamePrefix.split("/")[3:])

        paginator = self.s3.get_paginator('list_objects_v2')
        images = []
        responseIterator = paginator.paginate(
            Bucket=self.bucketName,
            Prefix=keyNamePrefix
        )
        for page in responseIterator:
            if "Contents" in page:
                for n in page["Contents"]:
                    key = n["Key"]
                    if is_xml:
                        if ".jpg" in key or ".tif" in key or ".tiff" in key or \
                                ".png" in key or ".TIF" or ".bmp" in key or ".xml" or ".XML" in key:
                            images.append(key)
                    else:
                        if ".jpg" in key or ".tif" in key or ".tiff" in key or \
                                ".png" in key or ".TIF" in key or ".bmp" in key:
                            images.append(key)

        if len(images) == 0:
            raise RuntimeError("Found 0 images in subfolders of: " + datasetPath + "\n")
        return images

    def getImgXmlArray(self, dataPath):
        data_path = dataPath
        if data_path.split('/')[0] == 's3:':
            data_path = "/".join(data_path.split("/")[3:])
        try:
            s3dataKey = self.s3.head_object(Bucket=self.bucketName, Key=data_path)
        except:
            raise RuntimeError("S3 not have data path: %s " % (data_path))
        s3Object = ""
        if s3dataKey:
            for i in range(3):
                try:
                    s3Object = self.s3.get_object(Bucket=self.bucketName, Key=data_path)
                    if s3Object.get("ResponseMetadata").get("HTTPStatusCode") == 200:
                        break
                except:
                    raise RuntimeError("Not get S3 Imag data: %s " % (data_path))

        if s3Object['Body']:
            dataBody = s3Object['Body'].read()
            if dataBody == "":
                raise RuntimeError("Imag data: %s is none " % (dataPath))
        return dataBody

    def downS3Weight(self, file_name, upload_key):
        isWeight = False
        upload_weight_key = upload_key
        if upload_weight_key.split('/')[0] == 's3:':
            upload_weight_key = "/".join(upload_weight_key.split("/")[3:])
        # 判断权重文件是否存在
        try:
            s3WightKey = self.s3.head_object(Bucket=self.bucketName,Key=upload_weight_key)
        except:
            return isWeight
        try:
            if s3WightKey:
                isWeight = True
                self.s3.download_file(Filename=file_name, Key=upload_weight_key, Bucket=self.bucketName)
        except:
            raise RuntimeError("Not get weight: %s " % (upload_weight_key))
        return isWeight

    def getObjectSize(self, dataPath):
        fileSize = None
        data_path = dataPath
        if data_path.split('/')[0] == 's3:':
            data_path = "/".join(data_path.split("/")[3:])
        try:
            print(self.bucketName)
            print(data_path)
            s3dataKey = self.s3.head_object(Bucket=self.bucketName, Key=data_path)
        except:
            raise RuntimeError("S3 not have data path: %s " % (data_path))
        s3Object = ""
        if s3dataKey:
            for i in range(3):
                try:
                    s3Object = self.s3.get_object(Bucket=self.bucketName, Key=data_path)
                    if s3Object.get("ResponseMetadata").get("HTTPStatusCode") == 200:
                        break
                except:
                    raise RuntimeError("Not get S3 Imag data: %s " % (data_path))

        if s3Object['ContentLength']:
            fileSize = s3Object['ContentLength']

        return fileSize

    def getGDAL(self,accessKey,secretKey,region):
        # 设置gdal 可以读取s3文件
        gdal.SetConfigOption("AWS_REGION", region)
        gdal.SetConfigOption("AWS_SECRET_ACCESS_KEY", secretKey)
        gdal.SetConfigOption("AWS_ACCESS_KEY_ID", accessKey)
        gdal.SetConfigOption("AWS_S3_ENDPOINT", "s3.cn-northwest-1.amazonaws.com.cn")

        return gdal

if __name__ == '__main__':
    s3 = s3GetImg()
    gdal3 = s3.gdal
    path = '/vsis3/pie-engine-ai/devel/system/dataset/segmentation/f87b0e1b-1f9c-40d0-aed9-1310501e61f4/train/images/0_0_493.tif'
    x = gdal3.Open(path)
    print(x)
    exit(1)
    paht = "s3://pie-engine-ai/ai-images/qVWnbPFqAB8yPzcYRDVkF/0/269d99a9d23c909c6a5f2114d81ad7b7/GF1C_PMS_E116.4_N36.8_20201124_L1A1021673269-GEO_RS-COG.tif"
    xx = s3.getObjectSize(paht)
    # xx2 = s3.getImgXmlArray(paht)
    print(xx)
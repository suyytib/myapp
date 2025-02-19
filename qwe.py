import base64
from io import BytesIO
import io
import os
from PIL import Image
from flask import Blueprint, jsonify, request, session
from flask import render_template
import pydicom
from functool import captcha__is_login
from table_config import db
from model import Dataset, User,Assess
from datetime import datetime
import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider

# auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())
# bucket = oss2.Bucket(auth, 'https://oss-cn-shanghai.aliyuncs.com', 'userimages-yyzxw')
# with open('./examplefile.txt', 'rb') as fileobj:
#     fileobj.seek(os.SEEK_SET)
#     current = fileobj.tell()
#     bucket.put_object('qweqwe/exampleobject.txt', fileobj)
# with open(r'examplefile.txt','a+',encoding='utf-8') as test:
#     test.truncate(0)
#上传


# auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())
# bucket = oss2.Bucket(auth, 'http://oss-cn-shanghai.aliyuncs.com', 'userimages-yyzxw')
# bucket.get_object_to_file('exampleobject.txt', 'D:\\Model_evaluation_accelerated_Flask\\examplefile.txt')  
#下载



# with open("examplefile.txt", 'rb') as file:
#     file=file.read()
# img_data = base64.b64decode(file)
# dcm = pydicom.dcmread(io.BytesIO(img_data))#转码
# dcm.save_as("2123.dcm") #保存到本地

#转dcm
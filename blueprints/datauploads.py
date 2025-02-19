import base64
import io
import os
import shutil
import subprocess
from flask import Blueprint, jsonify, request, session
from flask import render_template
import numpy as np
import pydicom as pd
import zipfile
from functool import captcha__is_login
from table_config import db
from model import Dataset, User,Assess,Fastmri,Fastnon2d,Fastnon3d,Dwi
from datetime import datetime
from skimage.metrics import peak_signal_noise_ratio as compare_psnr
from skimage.metrics import structural_similarity as compare_ssim
import os
from PIL import Image
import cv2
import pydicom as pd
def copy_filenames(src_folder, dest_folder):
    # 获取源文件夹中的所有文件名
    filenames = os.listdir(src_folder)
    filenames.sort(key=lambda x: os.path.getmtime(os.path.join(src_folder, x)))
    filenames2 = os.listdir(dest_folder)
    filenames2.sort(key=lambda x: os.path.getmtime(os.path.join(dest_folder, x)))
    # 遍历目标文件夹中的所有文件
    for i, file in enumerate(filenames2):
        src_file = os.path.join(src_folder, filenames[i])
        dest_file = os.path.join(dest_folder, file)
        print(src_file)
        print(dest_file)
        os.rename(dest_file, os.path.join(dest_folder, filenames[i]))
def png_to_dicom(input_filepath, output_dcm_path):
    png_image = cv2.imread(input_filepath, cv2.IMREAD_GRAYSCALE)  # 以灰度模式读取
    template_dicom = pd.dcmread("TEST.dcm")
    ds = template_dicom.copy()
    ds.file_meta.FileMetaInformationGroupLength = 184
    ds.file_meta.FileMetaInformationVersion = b'\x00\x01'
    ds.file_meta.MediaStorageSOPClassUID = pd.uid.UID('1.2.840.10008.5.1.4.1.1.7')
    ds.file_meta.MediaStorageSOPInstanceUID =pd.uid.generate_uid()
    ds.file_meta.TransferSyntaxUID = pd.uid.UID('1.2.840.10008.1.2')
    ds.file_meta.ImplementationClassUID = pd.uid.UID('1.2.276.0.7230010.3.0.3.5.4')
    ds.file_meta.ImplementationVersionName = 'ANNET_DCMBK_100'


    ds.Rows = png_image.shape[0]
    ds.Columns = png_image.shape[1]
    ds.SamplesPerPixel = 1  # 灰度图像通常是1
    ds.PhotometricInterpretation = "MONOCHROME2"  # 灰度图像通常是MONOCHROME2
    ds.PixelRepresentation = 0  # 无符号整数
    ds.BitsStored = 16  # 每个像素存储的位数（与你的NumPy数组dtype匹配）
    ds.BitsAllocated = 16  # 每个像素分配的位数（通常与BitsStored相同）
    ds.HighBit = 15  # 最高有效位（对于16位图像是15）
    ds.PatientID = "123456"
    ds.PatientBirthDate = "19700101"
    ds.PatientSex = "M"
    ds.PatientName = "Anonymous"
    ds.StudyDescription = "PNG to DICOM"
    ds.SamplesPerPixel = 1
    ds.BitsAllocated = 8
    ds.BitsStored = 8
    ds.HighBit = 7
    ds.PixelRepresentation = 0
    # 数据显示格式
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.PixelData = png_image.tobytes()  # 直接使用灰度图像的字节数据

    # 保存DICOM数据集到文件
    ds.is_little_endian = True
    ds.is_implicit_VR = True  # 使用隐式VR
    ds.PixelData = png_image.tobytes()

    # 保存新的DICOM文件
    ds.save_as(output_dcm_path)
def rel_norm_error(x, y):
    norm_diff = np.linalg.norm(x - y)
    norm_x = np.linalg.norm(x)
    return norm_diff / norm_x
def get_filenames(file_dir,file_type):
    filenames=[]
    if not os.path.exists(file_dir):
        return -1
    for root,dirs,names in os.walk(file_dir):
        for filename in names:
            if os.path.splitext(filename)[1] == file_type:
                filenames.append(os.path.join(root,filename))
    return filenames
def Calculate_objective_indicators(teamcode,filename,Methodnum):
    ##################################################################################################
    patha = "./static/images/{0}/{1}/Reference".format(teamcode,filename)
    pathb ="./static/images/{0}/{1}/MethodA".format(teamcode,filename)
    pathc = "./static/images/{0}/{1}/MethodB".format(teamcode,filename)
    pathd ="./static/images/{0}/{1}/MethodC".format(teamcode,filename)
    a=get_filenames(patha,".dcm")
    b=get_filenames(pathb,".dcm")
    PSNRa=0
    SSIMa=0
    RLNEa=0
    if Methodnum>=2:
        for t in range(len(a)):
            imga= pd.dcmread(a[t], force=True)
            imga =imga.pixel_array
            imga = imga.astype(np.float32) / np.max(imga) 
            imgb= pd.dcmread(b[t], force=True)
            imgb =imgb.pixel_array
            imgb = imgb.astype(np.float32) / np.max(imgb) 
            PSNRa+=compare_psnr(imga, imgb)
            ab=imga.max()-imgb.min()
            SSIMa+=compare_ssim(imga, imgb,data_range=ab, multichannel=True)
            RLNEa+=rel_norm_error(imga, imgb)

    a=get_filenames(patha,".dcm")
    b=get_filenames(pathc,".dcm")
    PSNRb=0
    SSIMb=0
    RLNEb=0
    if Methodnum>=3:
        for t in range(len(a)):
            imga= pd.dcmread(a[t], force=True)
            imga =imga.pixel_array
            imga = imga.astype(np.float32) / np.max(imga) 
            imgb= pd.dcmread(b[t], force=True)
            imgb =imgb.pixel_array
            imgb = imgb.astype(np.float32) / np.max(imgb) 
            PSNRb+=compare_psnr(imga, imgb)
            ab=imga.max()-imgb.min()
            SSIMb+=compare_ssim(imga, imgb,data_range=ab, multichannel=True)
            RLNEb+=rel_norm_error(imga, imgb)

    a=get_filenames(patha,".dcm")
    b=get_filenames(pathd,".dcm")
    PSNRc=0
    SSIMc=0
    RLNEc=0
    if Methodnum>=4:
        for t in range(len(a)):
            imga= pd.dcmread(a[t], force=True)
            imga =imga.pixel_array
            imga = imga.astype(np.float32) / np.max(imga) 
            imgb= pd.dcmread(b[t], force=True)
            imgb =imgb.pixel_array
            imgb = imgb.astype(np.float32) / np.max(imgb) 
            PSNRc+=compare_psnr(imga, imgb)
            ab=imga.max()-imgb.min()
            SSIMc+=compare_ssim(imga, imgb,data_range=ab, multichannel=True)
            RLNEc+=rel_norm_error(imga, imgb)
    datas = Dataset.query.filter_by(datasname=filename,teamcode=teamcode).first()
    if datas and datas.kind=="Fastmri":
        datas = Fastmri.query.filter_by(projectname=filename,teamcode=teamcode).first()
    elif datas and datas.kind=="Fastnon2d":
        datas = Fastnon2d.query.filter_by(projectname=filename,teamcode=teamcode).first()
    elif datas and datas.kind=="Fastnon3d":
        datas = Fastnon3d.query.filter_by(projectname=filename,teamcode=teamcode).first()
    elif datas and datas.kind=="Dwi":
        datas = Dwi.query.filter_by(projectname=filename,teamcode=teamcode).first()
    datas.PSNRA=PSNRa/len(a)
    datas.PSNRB=PSNRb/len(a)
    datas.PSNRC=PSNRc/len(a)
    datas.SSIMA=SSIMa/len(a)
    datas.SSIMB=SSIMb/len(a)
    datas.SSIMC=SSIMc/len(a)
    datas.RLNEA=RLNEa/len(a)
    datas.RLNEB=RLNEb/len(a)
    datas.RLNEC=RLNEc/len(a)
    db.session.commit()
    ##################################################################################################
    # 计算客观指标
bp=Blueprint("datauploads",__name__,url_prefix="/datauploads")
@bp.route('/')
@captcha__is_login
def datauploads():
    # 根
    temp = session.get("user_id") 
    user = User.query.get(temp) 
    if user.teamcode=="0":
        return render_template('datauploads.html')
    # 没有资格
    datas = Fastmri.query.filter_by(teamcode=user.teamcode).all()+Fastnon2d.query.filter_by(teamcode=user.teamcode).all()+Fastnon3d.query.filter_by(teamcode=user.teamcode).all()+Dwi.query.filter_by(teamcode=user.teamcode).all()
    # 4种方法之一
    return render_template('datauploads.html',datas=datas)

@bp.route('/filesuploads',methods=["POST"])
@captcha__is_login
def filesuploads():
    # 保存文件
    temp = session.get("user_id") 
    users = User.query.get(temp) 
    if users.teamcode=="0":
        return jsonify({"code":404, "message": "fail!", "datas": None})
    # 没有资格
    filename=request.form.get('filename')
    print(filename)
    img=request.form.get('data')
    name=request.form.get('name')
    print(name)
    kind=request.form.get('kind')
    print(kind)
    alls=request.form.get('alls')
    print(alls)
    listname=request.form.get('listname')
    print(listname)
    motaikind=request.form.get('motaikind')
    print(motaikind)
    Reconstruct=request.form.get('Reconstruct')
    print(Reconstruct)
    handlerawdata=request.form.get('handlerawdata')
    print(handlerawdata)
    Methodnum=int(request.form.get('Methodnum'))
    print(Methodnum)
    # 获取文件名，blob流，当前进度，方法类型，总份数，模态类型，是否重建
    try:
        str=datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        # 当前时间
        datas = Dataset.query.filter_by(datasname=filename,teamcode=users.teamcode).first()
        if datas and datas.kind=="Fastmri":
            datas = Fastmri.query.filter_by(projectname=filename,teamcode=users.teamcode).first()
        elif datas and datas.kind=="Fastnon2d":
            datas = Fastnon2d.query.filter_by(projectname=filename,teamcode=users.teamcode).first()
        elif datas and datas.kind=="Fastnon3d":
            datas = Fastnon3d.query.filter_by(projectname=filename,teamcode=users.teamcode).first()
        elif datas and datas.kind=="Dwi":
            datas = Dwi.query.filter_by(projectname=filename,teamcode=users.teamcode).first()
        if datas:
            datas.fenshu=int(name)+1
            db.session.commit()
            # 添加
        else:
            # 还没有写入数据库
            if kind=="Fastmri":
                leader = Fastmri(projectname=filename,teamcode=users.teamcode,time=str,fenshu=1,updatetime=str,motaikind=motaikind)
            elif kind=="Fastnon2d":
                leader = Fastnon2d(projectname=filename,teamcode=users.teamcode,time=str,fenshu=1,updatetime=str,motaikind=motaikind)
            elif kind=="Fastnon3d":
                leader = Fastnon3d(projectname=filename,teamcode=users.teamcode,time=str,fenshu=1,updatetime=str,motaikind=motaikind)
            elif kind=="Dwi":
                leader = Dwi(projectname=filename,teamcode=users.teamcode,time=str,fenshu=1,updatetime=str,motaikind=motaikind)
            leaders=Dataset(datasname=filename,teamcode=users.teamcode,kind=kind)
            db.session.add(leader)
            db.session.add(leaders)
            db.session.commit()
            # 写入数据库
        if not os.path.exists("./static/images/{0}/{1}/Reference".format(users.teamcode,filename)):
            os.makedirs("./static/images/{0}/{1}/Reference".format(users.teamcode,filename))
            os.makedirs("./static/images/{0}/{1}/MethodA".format(users.teamcode,filename))
            os.makedirs("./static/images/{0}/{1}/MethodB".format(users.teamcode,filename))
            os.makedirs("./static/images/{0}/{1}/MethodC".format(users.teamcode,filename)),
            os.makedirs("./static/images/{0}/{1}/originalmat".format(users.teamcode,filename))
        #创建文件夹
        head,context=img.split(",")
        img_data = base64.b64decode(context)
        str=str+'-'+name
        # Blob流转字节流
        if Reconstruct=='Yes':
            if handlerawdata=='No':
                with open("./static/images/{0}/{1}/originalmat/slice{2}.mat".format(users.teamcode,filename,int(name)+1), "ab") as dcm_file:
                    dcm_file.write(img_data)
            if handlerawdata=='Yes':
                if listname.split('.')[1]=="data":
                    with open("./static/images/{0}/{1}/originalmat/raw_slice1.data".format(users.teamcode,filename), "ab") as dcm_file:
                        dcm_file.write(img_data)
                if listname.split('.')[1]=="mat":
                    with open("./static/images/{0}/{1}/originalmat/slice{2}.mat".format(users.teamcode,filename,int(name)+1), "ab") as dcm_file:
                        dcm_file.write(img_data)
                if listname.split('.')[1]=="raw":
                    with open("./static/images/{0}/{1}/originalmat/raw_slice1.raw".format(users.teamcode,filename), "ab") as dcm_file:
                        dcm_file.write(img_data)
                if listname.split('.')[1]=="list":
                    with open("./static/images/{0}/{1}/originalmat/raw_slice1.list".format(users.teamcode,filename), "ab") as dcm_file:
                        dcm_file.write(img_data)
                if listname.split('.')[1]=="dat":
                    with open("./static/images/{0}/{1}/originalmat/slice{2}.dat".format(users.teamcode,filename,int(name)+1), "ab") as dcm_file:
                        dcm_file.write(img_data)
            # 重建，写入mat文件
        else:
            if int(alls)/Methodnum>=int(name)+1:
                with open("./static/images/{0}/{1}/Reference/{2}.dcm".format(users.teamcode,filename,str), "wb") as dcm_file:
                    dcm_file.write(img_data)
                assess=Assess(username=users.username,imgname=str,kinds=name,datasname=filename,teamcode=users.teamcode)
                db.session.add(assess)
            elif Methodnum>=2 and int(alls)/Methodnum*2>=int(name)+1:
                with open("./static/images/{0}/{1}/MethodA/{2}.dcm".format(users.teamcode,filename,str), "wb") as dcm_file:
                    dcm_file.write(img_data)
            elif Methodnum>=3 and int(alls)/Methodnum*3>=int(name)+1:
                with open("./static/images/{0}/{1}/MethodB/{2}.dcm".format(users.teamcode,filename,str), "wb") as dcm_file:
                    dcm_file.write(img_data)
            elif Methodnum>=4 and int(alls)/Methodnum*4>=int(name)+1:
                with open("./static/images/{0}/{1}/MethodC/{2}.dcm".format(users.teamcode,filename,str), "wb") as dcm_file:
                    dcm_file.write(img_data)
            # 文件放置操作
            db.session.commit()
            if int(name)+1==int(alls):
                datas.fenshu=datas.fenshu/Methodnum
                db.session.commit()
                src_folder = "./static/images/{0}/{1}/Reference".format(users.teamcode,filename)
                if Methodnum>=2:
                    dest_folder = "./static/images/{0}/{1}/MethodA".format(users.teamcode,filename)
                    copy_filenames(src_folder, dest_folder)
                if Methodnum>=3:
                    dest_folder = "./static/images/{0}/{1}/MethodB".format(users.teamcode,filename)
                    copy_filenames(src_folder, dest_folder)
                if Methodnum>=4:
                    dest_folder = "./static/images/{0}/{1}/MethodC".format(users.teamcode,filename)
                    copy_filenames(src_folder, dest_folder)
                path="./static/images/{0}/{1}/originalmat".format(users.teamcode,filename)
                shutil.rmtree(path) 
                # 统一文件名
                path="./static/images/{0}/{1}".format(users.teamcode,filename)
                pathzip=path+'.zip'
                with zipfile.ZipFile(pathzip, 'w') as zipObj:
                    for root, dirs, files in os.walk(path):
                        for file in files:
                            zipObj.write(os.path.join(root, file))
                # 压缩打包
                Calculate_objective_indicators(users.teamcode,filename,Methodnum)
                db.session.commit()
        return jsonify({"code":200, "message": "success!", "datas": None})
    except Exception as e:
        print(e)
        try: 
            data = Dataset.query.filter_by(datasname=filename,teamcode=users.teamcode).first()
            if data.kind=="Fastmri":
                dataw = Fastmri.query.filter_by(projectname=filename,teamcode=users.teamcode).first()
            elif data.kind=="Fastnon2d":
                dataw = Fastnon2d.query.filter_by(projectname=filename,teamcode=users.teamcode).first()
            elif data.kind=="Fastnon3d":
                dataw = Fastnon3d.query.filter_by(projectname=filename,teamcode=users.teamcode).first()
            elif data.kind=="Dwi":
                dataw = Dwi.query.filter_by(projectname=filename,teamcode=users.teamcode).first()
            datas = Assess.query.filter_by(datasname=filename,teamcode=users.teamcode).all()
            for each in datas:
                db.session.delete(each)
                db.session.commit()
            db.session.delete(data)
            db.session.delete(dataw)
            db.session.commit()
            path="./static/images/{0}/{1}".format(users.teamcode,filename)
            shutil.rmtree(path)  
            os.remove("./static/images/{0}/{1}".format(users.teamcode,filename)+'.zip')
        except Exception as et:
            print(et)
        # 清除请求内容操作
        return jsonify({"code":404, "message": "fail!", "datas": None})
    
@bp.route('/delete/',methods=["GET"])
@captcha__is_login
def delete():
    temp = session.get("user_id") 
    user = User.query.get(temp) 
    if user.teamcode=="0":
        return render_template('datauploads.html')
    datasname =request.args["datasname"]
    try:
        datas = Assess.query.filter_by(datasname=datasname,teamcode=user.teamcode).all()
        for each in datas:
            db.session.delete(each)
            db.session.commit()
        data = Dataset.query.filter_by(datasname=datasname,teamcode=user.teamcode).first()
        if data.kind=="Fastmri":
            dataw = Fastmri.query.filter_by(projectname=datasname,teamcode=user.teamcode).first()
        elif data.kind=="Fastnon2d":
            dataw = Fastnon2d.query.filter_by(projectname=datasname,teamcode=user.teamcode).first()
        elif data.kind=="Fastnon3d":
            dataw = Fastnon3d.query.filter_by(projectname=datasname,teamcode=user.teamcode).first()
        elif data.kind=="Dwi":
            dataw = Dwi.query.filter_by(projectname=datasname,teamcode=user.teamcode).first()
        db.session.delete(data)
        db.session.delete(dataw)
        db.session.commit()
        path="./static/images/{0}/{1}".format(user.teamcode,datasname)
        shutil.rmtree(path)  
        os.remove("./static/images/{0}/{1}".format(user.teamcode,datasname)+'.zip')
    except Exception as et:
        print(et)
    datas = Fastmri.query.filter_by(teamcode=user.teamcode).all()+Fastnon2d.query.filter_by(teamcode=user.teamcode).all()+Fastnon3d.query.filter_by(teamcode=user.teamcode).all()+Dwi.query.filter_by(teamcode=user.teamcode).all()
    return render_template('datauploads.html',datas=datas)
    # 删除命令

@bp.route('/objdatastatistics/',methods=["GET"])
@captcha__is_login
def objdatastatistics():
    temp = session.get("user_id") 
    user = User.query.get(temp) 
    if user.teamcode=="0":
        return render_template('objdatastatistics.html')
    tt=request.args["datasname"]
    try:
        t=Dataset.query.filter_by(datasname=tt,teamcode=user.teamcode).first()
        if t.kind=="Fastmri":
            t = Fastmri.query.filter_by(projectname=tt,teamcode=user.teamcode).first()
        elif t.kind=="Fastnon2d":
            t = Fastnon2d.query.filter_by(projectname=tt,teamcode=user.teamcode).first()
        elif t.kind=="Fastnon3d":
            t = Fastnon3d.query.filter_by(projectname=tt,teamcode=user.teamcode).first()
        elif t.kind=="Dwi":
            t = Dwi.query.filter_by(projectname=tt,teamcode=user.teamcode).first()
        b1=t.PSNRA
        b2=t.SSIMA
        b3=t.RLNEA
        b4=t.PSNRB
        b5=t.SSIMB
        b6=t.RLNEB
        b7=t.PSNRC
        b8=t.SSIMC
        b9=t.RLNEC
        Numberofmethods=t.Numberofmethods
        return render_template('objdatastatistics.html',b1=b1,b2=b2,b3=b3,b4=b4,b5=b5,b6=b6,b7=b7,b8=b8,b9=b9,Numberofmethods=Numberofmethods)
    except Exception as e:
        print(e)
        return render_template('objdatastatistics.html')
    # 客观指标统计图

@bp.route('/makeprogram/',methods=["POST"])
@captcha__is_login
def makeprogram():
    temp = session.get("user_id") 
    user = User.query.get(temp) 
    try:
        name = request.values.get('name')
        Anatomy = request.values.get('a')
        Samplingpattern = request.values.get('d')
        Samplingrate = request.values.get('e')
        Subjecttoscore = request.values.get('f')
        Reconstructionmethod = request.values.get('g')
        SNR  = request.values.get('j')
        Overallquality  = request.values.get('h')
        Artifactsuppression  = request.values.get('k')
        datas=Dataset.query.filter_by(datasname=name,teamcode=user.teamcode).first()
        if datas.kind=="Fastmri":
            datas = Fastmri.query.filter_by(projectname=name,teamcode=user.teamcode).first()
        elif datas.kind=="Fastnon2d":
            datas = Fastnon2d.query.filter_by(projectname=name,teamcode=user.teamcode).first()
        elif datas.kind=="Fastnon3d":
            datas = Fastnon3d.query.filter_by(projectname=name,teamcode=user.teamcode).first()
        elif datas.kind=="Dwi":
            datas = Dwi.query.filter_by(projectname=name,teamcode=user.teamcode).first()
        datas.anatomy=Anatomy
        datas.samplingpattern=Samplingpattern
        datas.Samplingrate=Samplingrate
        if Samplingrate=="2":
            Samplingrate="0.5"
        elif Samplingrate=="3":
            Samplingrate="0.33"
        elif Samplingrate=="4":
            Samplingrate="0.25"
        elif Samplingrate=="5":
            Samplingrate="0.2"
        if Subjecttoscore=="Yes":
            datas.subjecttoscore=1
        datas.targetanalysismethod=Reconstructionmethod
        datas.SNR=SNR
        datas.Numberofmethods=2
        datas.Overallquality=Overallquality
        datas.Artifactsuppression=Artifactsuppression
        db.session.commit()
        subprocess.run(['static\\images\\Demo_old.exe','static\\images\\{0}\\{1}'.format(user.teamcode,name),Samplingrate,Reconstructionmethod,Samplingpattern], check=True)         
        index=0
        images_dir = "./static/images/{0}/{1}/ReconstructedbypFISTA".format(user.teamcode,name)
        for root, dirs, files in os.walk(images_dir):
            for file in files:
                str=datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                png_to_dicom(os.path.join(root,file),"./static/images/{0}/{1}/MethodA/{2}-{3}.dcm".format(user.teamcode,name,str,index))
                assess=Assess(username=user.username,imgname="{0}-{1}".format(str,index),kinds=index,datasname=name,teamcode=user.teamcode)
                db.session.add(assess)
                db.session.commit()
                index=index+1
        datas.fenshu=index
        db.session.commit()
        index=0
        images_dir = "./static/images/{0}/{1}/References".format(user.teamcode,name)
        print("0")
        for root, dirs, files in os.walk(images_dir):
            for file in files:
                str=datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                png_to_dicom(os.path.join(root,file),"./static/images/{0}/{1}/Reference/{2}-{3}.dcm".format(user.teamcode,name,str,index))
                index=index+1
        copy_filenames("./static/images/{0}/{1}/MethodA".format(user.teamcode,name), "./static/images/{0}/{1}/Reference".format(user.teamcode,name))
        print("1")
        Calculate_objective_indicators(user.teamcode,name,2)
        print("2")
        path="./static/images/{0}/{1}/ReconstructedbypFISTA".format(user.teamcode,name)
        shutil.rmtree(path)  
        path="./static/images/{0}/{1}/References".format(user.teamcode,name)
        shutil.rmtree(path)  
        path="./static/images/{0}/{1}/originalmat".format(user.teamcode,name)
        shutil.rmtree(path)  
        path="./static/images/{0}/{1}".format(user.teamcode,name)
        pathzip=path+'.zip'
        print("3")
        with zipfile.ZipFile(pathzip, 'w') as zipObj:
            for root, dirs, files in os.walk(path):
                for file in files:
                    zipObj.write(os.path.join(root, file))
        print("4")
        # 压缩打包  
    except Exception as e:
        print(e)
    return {
            'success': True,
            'message': '添加成功！',
        }

@bp.route('/makeprogramb/',methods=["POST"])
@captcha__is_login
def makeprogramb():
    temp = session.get("user_id") 
    user = User.query.get(temp) 
    try:
        name = request.values.get('name')
        Anatomy = request.values.get('a')
        Trajectory  = request.values.get('b')
        print(Trajectory)
        Accelerationfactor   = request.values.get('c')
        print(Accelerationfactor)
        Subjecttoscore = request.values.get('d')
        Targetanalysismethod  = request.values.get('e')
        SNR  = request.values.get('j')
        Overallquality  = request.values.get('h')
        Reconstruct=request.values.get('qw')
        Artifactsuppression  = request.values.get('k')
        handlerawdata  = request.values.get('o')
        Numberofmethods  = request.values.get('wew')
        listname  = request.values.get('listname')
        datas=Dataset.query.filter_by(datasname=name,teamcode=user.teamcode).first()
        if datas.kind=="Fastmri":
            datas = Fastmri.query.filter_by(projectname=name,teamcode=user.teamcode).first()
        elif datas.kind=="Fastnon2d":
            datas = Fastnon2d.query.filter_by(projectname=name,teamcode=user.teamcode).first()
        elif datas.kind=="Fastnon3d":
            datas = Fastnon3d.query.filter_by(projectname=name,teamcode=user.teamcode).first()
        elif datas.kind=="Dwi":
            datas = Dwi.query.filter_by(projectname=name,teamcode=user.teamcode).first()
        datas.anatomy=Anatomy
        datas.trajectory=Trajectory
        datas.accelerationfactor=int(Accelerationfactor)
        datas.Numberofmethods=int(Numberofmethods)
        if Subjecttoscore=="Yes":
            datas.subjecttoscore=1
        if handlerawdata=="Yes":
            datas.handlerawdata=1
        datas.targetanalysismethod=Targetanalysismethod
        datas.SNR=SNR
        datas.Overallquality=Overallquality
        datas.Artifactsuppression=Artifactsuppression
        db.session.commit()
        if Trajectory=='Pseudo golden angle':
            if handlerawdata=='Yes':
                if listname.split('.')[1]=="data":
                    subprocess.run(['static\\images\\Step3_Demo_pFISTA_Radial_Reconstruction_old.exe','static\\images\\{0}\\{1}'.format(user.teamcode,name),Accelerationfactor,Trajectory,'yes','data'], check=True)         
                else:
                    subprocess.run(['static\\images\\Step3_Demo_pFISTA_Radial_Reconstruction_old.exe','static\\images\\{0}\\{1}'.format(user.teamcode,name),Accelerationfactor,Trajectory,'yes','mat'], check=True)  
            if handlerawdata=='No':
                subprocess.run(['static\\images\\Step3_Demo_pFISTA_Radial_Reconstruction_old.exe','static\\images\\{0}\\{1}'.format(user.teamcode,name),Accelerationfactor,Trajectory,'no','o'], check=True)  
        if Trajectory=='Golden angle':
            if handlerawdata=='Yes':
                if listname.split('.')[1]=="raw":
                    subprocess.run(['static\\images\\Step3_Demo_pFISTA_Radial_Reconstruction_old.exe','static\\images\\{0}\\{1}'.format(user.teamcode,name),Accelerationfactor,Trajectory,"yes",'raw'], check=True)       
            if handlerawdata=='No':  
                subprocess.run(['static\\images\\Step3_Demo_pFISTA_Radial_Reconstruction_old.exe','static\\images\\{0}\\{1}'.format(user.teamcode,name),Accelerationfactor,Trajectory,"no",'o'], check=True)    
        index=0
        images_dir = "./static/images/{0}/{1}/ReconstructedbypFISTA".format(user.teamcode,name)
        for root, dirs, files in os.walk(images_dir):
            for file in files:
                str=datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                png_to_dicom(os.path.join(root,file),"./static/images/{0}/{1}/MethodA/{2}-{3}.dcm".format(user.teamcode,name,str,index))
                assess=Assess(username=user.username,imgname="{0}-{1}".format(str,index),kinds=index,datasname=name,teamcode=user.teamcode)
                db.session.add(assess)
                db.session.commit()
                index=index+1
        datas.fenshu=index
        db.session.commit()
        index=0
        images_dir = "./static/images/{0}/{1}/References".format(user.teamcode,name)
        print("0")
        for root, dirs, files in os.walk(images_dir):
            for file in files:
                str=datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                png_to_dicom(os.path.join(root,file),"./static/images/{0}/{1}/Reference/{2}-{3}.dcm".format(user.teamcode,name,str,index))
                index=index+1
        copy_filenames("./static/images/{0}/{1}/MethodA".format(user.teamcode,name), "./static/images/{0}/{1}/Reference".format(user.teamcode,name))
        print("1")
        Calculate_objective_indicators(user.teamcode,name,2)
        print("2")
        path="./static/images/{0}/{1}/ReconstructedbypFISTA".format(user.teamcode,name)
        shutil.rmtree(path)  
        path="./static/images/{0}/{1}/References".format(user.teamcode,name)
        shutil.rmtree(path)  
        path="./static/images/{0}/{1}/imzerofilling".format(user.teamcode,name)
        shutil.rmtree(path)  
        path="./static/images/{0}/{1}/Error(10x)".format(user.teamcode,name)
        shutil.rmtree(path)  
        path="./static/images/{0}/{1}/originalmat".format(user.teamcode,name)
        shutil.rmtree(path)  
        path="./static/images/{0}/{1}".format(user.teamcode,name)
        pathzip=path+'.zip'
        print("3")
        with zipfile.ZipFile(pathzip, 'w') as zipObj:
            for root, dirs, files in os.walk(path):
                for file in files:
                    zipObj.write(os.path.join(root, file))
        print("4")
        # 压缩打包
    except Exception as ee:
        print(ee)
        try:
            datas = Assess.query.filter_by(datasname=name,teamcode=user.teamcode).all()
            for each in datas:
                db.session.delete(each)
                db.session.commit()
            data = Dataset.query.filter_by(datasname=name,teamcode=user.teamcode).first()
            if data.kind=="Fastmri":
                dataw = Fastmri.query.filter_by(projectname=name,teamcode=user.teamcode).first()
            elif data.kind=="Fastnon2d":
                dataw = Fastnon2d.query.filter_by(projectname=name,teamcode=user.teamcode).first()
            elif data.kind=="Fastnon3d":
                dataw = Fastnon3d.query.filter_by(projectname=name,teamcode=user.teamcode).first()
            elif data.kind=="Dwi":
                dataw = Dwi.query.filter_by(projectname=name,teamcode=user.teamcode).first()
            db.session.delete(data)
            db.session.delete(dataw)
            db.session.commit()
            path="./static/images/{0}/{1}".format(user.teamcode,name)
            shutil.rmtree(path)  
            os.remove("./static/images/{0}/{1}".format(user.teamcode,name)+'.zip')
        except Exception as e:
            print(e)
        return {
            'success': False,
            'message': '添加失败！',
        }
    return {
            'success': True,
            'message': '添加成功！',
        }


@bp.route('/makeprogramc/',methods=["POST"])
@captcha__is_login
def makeprogramc():
    temp = session.get("user_id") 
    user = User.query.get(temp) 
    try:
        name = request.values.get('name')
        Anatomy = request.values.get('a')
        Trajectory  = request.values.get('b')
        Accelerationfactor   = request.values.get('c')
        Subjecttoscore = request.values.get('d')
        Targetanalysismethod  = request.values.get('e')
        SNR  = request.values.get('j')
        Overallquality  = request.values.get('h')
        Artifactsuppression  = request.values.get('k')
        handlerawdata  = request.values.get('o')
        datas=Dataset.query.filter_by(datasname=name,teamcode=user.teamcode).first()
        if datas.kind=="Fastmri":
            datas = Fastmri.query.filter_by(projectname=name,teamcode=user.teamcode).first()
        elif datas.kind=="Fastnon2d":
            datas = Fastnon2d.query.filter_by(projectname=name,teamcode=user.teamcode).first()
        elif datas.kind=="Fastnon3d":
            datas = Fastnon3d.query.filter_by(projectname=name,teamcode=user.teamcode).first()
        elif datas.kind=="Dwi":
            datas = Dwi.query.filter_by(projectname=name,teamcode=user.teamcode).first()
        datas.anatomy=Anatomy
        datas.trajectory=Trajectory
        datas.accelerationfactor=int(Accelerationfactor)
        if Subjecttoscore=="Yes":
            datas.subjecttoscore=1
        if handlerawdata=="Yes":
            datas.handlerawdata=1
        datas.targetanalysismethod=Targetanalysismethod
        datas.Numberofmethods=2
        datas.SNR=SNR
        datas.Overallquality=Overallquality
        datas.Artifactsuppression=Artifactsuppression
        db.session.commit()
        if handlerawdata=='No':
            subprocess.run(['static\\images\\Demo_dceliver_RC_old.exe','static\\images\\{0}\\{1}'.format(user.teamcode,name),Accelerationfactor,'no'], check=True) 
        if handlerawdata=='Yes':
            subprocess.run(['static\\images\\Demo_dceliver_RC_old.exe','static\\images\\{0}\\{1}'.format(user.teamcode,name),Accelerationfactor,'yes'], check=True) 
        index=0
        images_dir = "./static/images/{0}/{1}/gif".format(user.teamcode,name)
        for root, dirs, files in os.walk(images_dir):
            for file in files:
                str=datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                os.rename(os.path.join(root, file), os.path.join(root, "{0}-{1}.gif".format(str,index)))
                assess=Assess(username=user.username,imgname="{0}-{1}".format(str,index),kinds=index,datasname=name,teamcode=user.teamcode)
                db.session.add(assess)
                db.session.commit()
                index=index+1
        datas.fenshu=index
        db.session.commit()
        # path="./static/images/{0}/{1}/ReconstructedbypFISTA".format(user.teamcode,name)
        # shutil.rmtree(path)  
        path="./static/images/{0}/{1}/originalmat".format(user.teamcode,name)
        shutil.rmtree(path)  
        path="./static/images/{0}/{1}".format(user.teamcode,name)
        pathzip=path+'.zip'
        print("3")
        with zipfile.ZipFile(pathzip, 'w') as zipObj:
            for root, dirs, files in os.walk(path):
                for file in files:
                    zipObj.write(os.path.join(root, file))
        print("4")
        # 压缩打包
    except Exception as ee:
        print(ee)
        try:
            datas = Assess.query.filter_by(datasname=name,teamcode=user.teamcode).all()
            for each in datas:
                db.session.delete(each)
                db.session.commit()
            data = Dataset.query.filter_by(datasname=name,teamcode=user.teamcode).first()
            if data.kind=="Fastmri":
                dataw = Fastmri.query.filter_by(projectname=name,teamcode=user.teamcode).first()
            elif data.kind=="Fastnon2d":
                dataw = Fastnon2d.query.filter_by(projectname=name,teamcode=user.teamcode).first()
            elif data.kind=="Fastnon3d":
                dataw = Fastnon3d.query.filter_by(projectname=name,teamcode=user.teamcode).first()
            elif data.kind=="Dwi":
                dataw = Dwi.query.filter_by(projectname=name,teamcode=user.teamcode).first()
            db.session.delete(data)
            db.session.delete(dataw)
            db.session.commit()
            path="./static/images/{0}/{1}".format(user.teamcode,name)
            shutil.rmtree(path)  
            os.remove("./static/images/{0}/{1}".format(user.teamcode,name)+'.zip')
        except Exception as e:
            print(e)
        return {
            'success': False,
            'message': '添加失败！',
        }
    return {
            'success': True,
            'message': '添加成功！',
        }

@bp.route('/makeprogramd/',methods=["POST"])
@captcha__is_login
def makeprogramd():
    temp = session.get("user_id") 
    user = User.query.get(temp) 
    try:
        name = request.values.get('name')
        Anatomy = request.values.get('a')
        Subjecttoscore = request.values.get('d')
        SNR  = request.values.get('j')
        Overallquality  = request.values.get('h')
        Artifactsuppression  = request.values.get('k')
        Numberofmethods  = request.values.get('wew')
        datas=Dataset.query.filter_by(datasname=name,teamcode=user.teamcode).first()
        if datas.kind=="Fastmri":
            datas = Fastmri.query.filter_by(projectname=name,teamcode=user.teamcode).first()
        elif datas.kind=="Fastnon2d":
            datas = Fastnon2d.query.filter_by(projectname=name,teamcode=user.teamcode).first()
        elif datas.kind=="Fastnon3d":
            datas = Fastnon3d.query.filter_by(projectname=name,teamcode=user.teamcode).first()
        elif datas.kind=="Dwi":
            datas = Dwi.query.filter_by(projectname=name,teamcode=user.teamcode).first()
        datas.anatomy=Anatomy
        if Subjecttoscore=="Yes":
            datas.subjecttoscore=1
        datas.SNR=SNR
        datas.Numberofmethods=int(Numberofmethods)
        datas.Overallquality=Overallquality
        datas.Artifactsuppression=Artifactsuppression
        db.session.commit()
    except Exception as e:
        print(e)
    return {
            'success': True,
            'message': '添加成功！',
        }
    
@bp.route('/yiyi')
@captcha__is_login
def yiyi():
    teamcode=request.values.get('teamcode')
    filename=request.values.get('filename')
    T=request.values.get('T')
    if T is not None and T.isnumeric():
        T= int(T)+1
    images_dir = "static/images/{0}/{1}/saveimg/{2}".format(teamcode,filename,T)
    print(images_dir)
    supported_formats = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    image_addresses = []
    image= []
    imagenum= []
    imagename= []
    index = 0
    temp=0
    indext = 0
    try:
        slice= int(request.args.get('slice'))
        if slice<1 or slice>20:
            slice=1
    except:
        slice=1
    for root, dirs, files in os.walk(images_dir):
        files.sort(key=lambda x: os.path.getmtime(os.path.join(root, x)))
        for file in files:
            if index%slice==0:
                if indext%3==0 and indext!=0:
                    image_addresses.append(zip(image, imagenum,imagename))
                    image=[]
                    imagenum=[]
                    imagename= []
                    temp+=1
                if os.path.splitext(file)[1].lower() in supported_formats:
                    # 构建完整的图片地址
                    image_path ="\\"+ os.path.join(root, file)
                    image_name=index+1
                    # 将图片地址分配到二维数组的子数组中
                    image.append(image_path)
                    imagenum.append(indext)
                    imagename.append(image_name)
                    indext += 1
            index += 1
    image_addresses.append(zip(image, imagenum,imagename))
    return render_template('yiyi.html',image_addresses=image_addresses,lastpath="/static/images/{0}/{1}/saveimg/{2}/im_rec_iter1.png".format(teamcode,filename,T),some=indext,teamcode=teamcode,filename=filename,T=T-1)


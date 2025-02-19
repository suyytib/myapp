import base64
from datetime import datetime
import os
from flask import Blueprint, request, session
from flask import render_template
from matplotlib import pyplot as plt
import numpy as np
from functool import captcha__is_login
from model import Dataset, Dwi, Fastmri, Fastnon2d, Fastnon3d, User,Assess
from table_config import db
from PIL import Image
from scipy.interpolate import make_interp_spline
def is_red(pixel, tolerance=0):
    r, g, b, a = pixel
    return (r >= 255 - tolerance and g <= tolerance and b <= tolerance)


bp=Blueprint("subjectivealls",__name__,url_prefix="/subjectivealls")
@bp.route('/')
@captcha__is_login
def subjectivealls():
    temp = session.get("user_id") 
    user = User.query.get(temp) 
    if user.teamcode=="0":
        return render_template('subjectivealls.html')
    datas = Fastmri.query.filter_by(teamcode=user.teamcode).all()+Fastnon2d.query.filter_by(teamcode=user.teamcode).all()+Fastnon3d.query.filter_by(teamcode=user.teamcode).all()+Dwi.query.filter_by(teamcode=user.teamcode).all()
    op=[]
    for t in datas:
        if t.subjecttoscore==0:
            continue
        data=Assess.query.filter_by(teamcode=user.teamcode,datasname=t.projectname).all()
        ui=0
        for y in data:
            if y.username==user.username:
                ui=ui+1
        op.append(ui)
    datas = zip(datas, op)
    team = User.query.filter_by(teamcode=user.teamcode).all()
    return render_template('subjectivealls.html',datas=datas,team=team)


@bp.route('/subjective/',methods=["GET"])
@captcha__is_login
def subjective():
    T=[]
    temp = session.get("user_id") 
    user = User.query.get(temp) 
    if user.teamcode=="0":
        return render_template('subjective.html')
    datasname=request.args["datasname"]
    datas = Dataset.query.filter_by(teamcode=user.teamcode,datasname=datasname).first()
    gif=""
    if datas.kind=="Fastmri":
        data = Fastmri.query.filter_by(projectname=datasname,teamcode=user.teamcode).first()
    elif datas.kind=="Fastnon2d":
        data = Fastnon2d.query.filter_by(projectname=datasname,teamcode=user.teamcode).first()
    elif datas.kind=="Fastnon3d":
        data = Fastnon3d.query.filter_by(projectname=datasname,teamcode=user.teamcode).first()
    elif datas.kind=="Dwi":
        data = Dwi.query.filter_by(projectname=datasname,teamcode=user.teamcode).first()
    SNR=data.SNR
    Numberofmethods=data.Numberofmethods
    Overallquality=data.Overallquality
    Artifactsuppression=data.Artifactsuppression
    userass=Assess.query.filter_by(username=user.username,teamcode=user.teamcode,datasname=datasname).first()
    if datas.kind=="Fastnon3d":
        gif="/static/images/{0}/{1}/gif/{2}.gif".format(user.teamcode,datasname,userass.imgname)
    ex1=userass.gradeaOverallquality
    ex2=userass.gradeaSNR 
    ex3=userass.gradeaArtifactsuppression 
    ex4=userass.gradebOverallquality
    ex5=userass.gradebSNR 
    ex6=userass.gradebArtifactsuppression 
    ex7=userass.gradecOverallquality 
    ex8=userass.gradecSNR 
    ex9=userass.gradecArtifactsuppression 
    try:
        a="/static/images/{0}/{1}/Reference/{2}.dcm".format(user.teamcode,datasname,userass.imgname)
        T.append("/static/images/{0}/{1}/MethodA/{2}.dcm".format(user.teamcode,datasname,userass.imgname))
        T.append("/static/images/{0}/{1}/MethodB/{2}.dcm".format(user.teamcode,datasname,userass.imgname))
        T.append("/static/images/{0}/{1}/MethodC/{2}.dcm".format(user.teamcode,datasname,userass.imgname))
    except:
        print("!")
    # random.shuffle(T)
    return render_template('subjective.html',datasname=datasname,kinds=userass.kinds,kinda=a,kindb=T[0],kindc=T[1],kindd=T[2],e1=ex1,e2=ex2,e3=ex3,e4=ex4,e5=ex5,e6=ex6,e7=ex7,e8=ex8,e9=ex9,SNR=SNR,Artifactsuppression=Artifactsuppression,Overallquality=Overallquality,Numberofmethods=Numberofmethods,gif=gif,teamcode=user.teamcode)

@bp.route('/updata',methods=["POST"]) 
@captcha__is_login
def updata():
    temp = session.get("user_id") 
    user = User.query.get(temp) 
    if user.teamcode=="0":
        return render_template('subjective.html')
    t=request.form.get("ht")  #当前第几个切片
    if t is not None and t.isnumeric():
        t= int(t)

    str=request.form.get("hh")
    ex1=request.form.get("ex1")
    ex2=request.form.get("ex2")
    ex3=request.form.get("ex3")
    ex4=request.form.get("ex4")
    ex5=request.form.get("ex5")
    ex6=request.form.get("ex6")
    ex7=request.form.get("ex7")
    ex8=request.form.get("ex8")
    ex9=request.form.get("ex9")
    
    datasname=request.form.get("datasname")
    strr=datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    data = Dataset.query.filter_by(teamcode=user.teamcode,datasname=datasname).first()
    if data.kind=="Fastmri":
        data = Fastmri.query.filter_by(projectname=datasname,teamcode=user.teamcode).first()
    elif data.kind=="Fastnon2d":
        data = Fastnon2d.query.filter_by(projectname=datasname,teamcode=user.teamcode).first()
    elif data.kind=="Fastnon3d":
        data = Fastnon3d.query.filter_by(projectname=datasname,teamcode=user.teamcode).first()
    elif data.kind=="Dwi":
        data = Dwi.query.filter_by(projectname=datasname,teamcode=user.teamcode).first()
    data.updatetime=strr
    SNR=data.SNR
    Numberofmethods=data.Numberofmethods
    Overallquality=data.Overallquality
    Artifactsuppression=data.Artifactsuppression
    userass=Assess.query.filter_by(kinds=t,username=user.username,teamcode=user.teamcode,datasname=datasname).first()
    if ex1:
        userass.gradeaOverallquality=ex1
    if ex2:
        userass.gradeaSNR = ex2
    if ex3:
        userass.gradeaArtifactsuppression =ex3
    if ex4:
        userass.gradebOverallquality =ex4
    if ex5:
        userass.gradebSNR = ex5
    if ex6:
        userass.gradebArtifactsuppression = ex6
    if ex7:
        userass.gradecOverallquality = ex7
    if ex8:
        userass.gradecSNR = ex8
    if ex9:
        userass.gradecArtifactsuppression = ex9
    if SNR==1 and (ex2=="0" or ex5=="0" or ex8=="0"):
        userass.had = 0
    elif Overallquality==1 and (ex1=="0" or ex4=="0" or ex7=="0"):
        userass.had = 0
    elif Artifactsuppression==1 and (ex3=="0" or ex6=="0" or ex9=="0"):
        userass.had = 0
    else:
        userass.had = 1
    users=Assess.query.filter_by(datasname=datasname,teamcode=user.teamcode).all()
    ww=1
    for tp in users:
        if tp.had==0:
            ww=0
    if ww==1:
        tem=Dataset.query.filter_by(teamcode=user.teamcode,datasname=datasname).first()
        if tem.kind=="Fastmri":
            tem = Fastmri.query.filter_by(projectname=datasname,teamcode=user.teamcode).first()
        elif tem.kind=="Fastnon2d":
            tem = Fastnon2d.query.filter_by(projectname=datasname,teamcode=user.teamcode).first()
        elif tem.kind=="Fastnon3d":
            tem = Fastnon3d.query.filter_by(projectname=datasname,teamcode=user.teamcode).first()
        elif tem.kind=="Dwi":
            tem = Dwi.query.filter_by(projectname=datasname,teamcode=user.teamcode).first()
        tem.already=1
        db.session.commit()  #标记全完成
    users=Assess.query.filter_by(username=user.username,datasname=datasname,teamcode=user.teamcode).all()
    ass=""
    asskind=0
    w=False
    if str=="up":
        for tp in users:
            if tp.kinds==t:
                ass=tp.imgname
                asskind=tp.kinds
                ex1=tp.gradeaOverallquality
                ex2=tp.gradeaSNR 
                ex3=tp.gradeaArtifactsuppression 
                ex4=tp.gradebOverallquality
                ex5=tp.gradebSNR 
                ex6=tp.gradebArtifactsuppression 
                ex7=tp.gradecOverallquality 
                ex8=tp.gradecSNR 
                ex9=tp.gradecArtifactsuppression 
                w=True
            elif w:
                ass=tp.imgname
                asskind=tp.kinds
                ex1=tp.gradeaOverallquality
                ex2=tp.gradeaSNR 
                ex3=tp.gradeaArtifactsuppression 
                ex4=tp.gradebOverallquality
                ex5=tp.gradebSNR 
                ex6=tp.gradebArtifactsuppression 
                ex7=tp.gradecOverallquality 
                ex8=tp.gradecSNR 
                ex9=tp.gradecArtifactsuppression 
                break
    else:
        for tp in reversed(users):
            if tp.kinds==t:
                ass=tp.imgname
                asskind=tp.kinds
                w=True
                ex1=tp.gradeaOverallquality
                ex2=tp.gradeaSNR 
                ex3=tp.gradeaArtifactsuppression 
                ex4=tp.gradebOverallquality
                ex5=tp.gradebSNR 
                ex6=tp.gradebArtifactsuppression 
                ex7=tp.gradecOverallquality 
                ex8=tp.gradecSNR 
                ex9=tp.gradecArtifactsuppression 
            elif w:
                ass=tp.imgname
                asskind=tp.kinds
                ex1=tp.gradeaOverallquality
                ex2=tp.gradeaSNR 
                ex3=tp.gradeaArtifactsuppression 
                ex4=tp.gradebOverallquality
                ex5=tp.gradebSNR 
                ex6=tp.gradebArtifactsuppression 
                ex7=tp.gradecOverallquality 
                ex8=tp.gradecSNR 
                ex9=tp.gradecArtifactsuppression 
                break
    T=[]
    gif=""
    tem=Dataset.query.filter_by(teamcode=user.teamcode,datasname=datasname).first()
    if tem.kind=="Fastnon3d":
        gif="/static/images/{0}/{1}/gif/{2}.gif".format(user.teamcode,datasname,ass)
    a="/static/images/{0}/{1}/Reference/{2}.dcm".format(user.teamcode,datasname,ass)
    T.append("/static/images/{0}/{1}/MethodA/{2}.dcm".format(user.teamcode,datasname,ass))
    T.append("/static/images/{0}/{1}/MethodB/{2}.dcm".format(user.teamcode,datasname,ass))
    T.append("/static/images/{0}/{1}/MethodC/{2}.dcm".format(user.teamcode,datasname,ass))
    # random.shuffle(T)
    db.session.commit() 
    print(asskind)
    return render_template('subjective.html',datasname=datasname,kinds=asskind,kinda=a,kindb=T[0],kindc=T[1],kindd=T[2],e1=ex1,e2=ex2,e3=ex3,e4=ex4,e5=ex5,e6=ex6,e7=ex7,e8=ex8,e9=ex9,SNR=SNR,Artifactsuppression=Artifactsuppression,Overallquality=Overallquality,Numberofmethods=Numberofmethods,gif=gif)


@bp.route('/distributed/',methods=["POST"])
@captcha__is_login
def distributed():#分发
    temp = session.get("user_id") 
    user = User.query.get(temp) 
    if user.teamcode=="0":
        return render_template('subjectivealls.html')
    datasname=request.form.get("inputField")
    data=Assess.query.filter_by(teamcode=user.teamcode,datasname=datasname).all()
    have=0 #我有多少
    for y in data:
        if y.username==user.username:
            have=have+1
    team = User.query.filter_by(teamcode=user.teamcode).all()
    if have==0:
        datas = Fastmri.query.filter_by(teamcode=user.teamcode).all()+Fastnon2d.query.filter_by(teamcode=user.teamcode).all()+Fastnon3d.query.filter_by(teamcode=user.teamcode).all()+Dwi.query.filter_by(teamcode=user.teamcode).all()
        op=[]
        for t in datas:
            data=Assess.query.filter_by(teamcode=user.teamcode,datasname=t.datasname).all()
            ui=0
            for y in data:
                if(y.username==user.username):
                    ui=ui+1
            op.append(ui)
        datas = zip(datas, op)
        return render_template('subjectivealls.html',datas=datas,team=team)
    for t in team:
        h=request.form.get(t.username)
        if h is not None and h.isnumeric():
            h= int(h)
        else:
            h=0
        have=have-h
        if have<=0 :
            for bt in range(have+h):
                ass = Assess.query.filter_by(username=user.username,teamcode=user.teamcode,datasname=datasname).first()
                ass.username=t.username
                db.session.commit()
        else:
            for bt in range(h):
                ass = Assess.query.filter_by(username=user.username,teamcode=user.teamcode,datasname=datasname).first()
                ass.username=t.username
                db.session.commit()
        db.session.commit()
    db.session.commit()
    datas = Fastmri.query.filter_by(teamcode=user.teamcode).all()+Fastnon2d.query.filter_by(teamcode=user.teamcode).all()+Fastnon3d.query.filter_by(teamcode=user.teamcode).all()+Dwi.query.filter_by(teamcode=user.teamcode).all()
    op=[]
    for t in datas:
        data=Assess.query.filter_by(teamcode=user.teamcode,datasname=t.projectname).all()
        ui=0
        for y in data:
            if(y.username==user.username):
                ui=ui+1
        op.append(ui)
    datas = zip(datas, op)
    return render_template('subjectivealls.html',team=team,datas=datas)

@bp.route('/canvas/')
@captcha__is_login
def canvas():#曲线
    gif=request.args["gif"]
    teamcode=request.args["teamcode"]
    filename=request.args["filename"]
    T=request.args["T"]
    print(gif)
    print(teamcode)
    print(filename)
    with Image.open('.'+gif) as img:
        # 获取图片的长宽
        width, height = img.size
    return render_template('SignalStrengthCurve.html',T=T,gif=gif,width=width,height=height,teamcode=teamcode,filename=filename,ans="/static/images/{0}/{1}/ans.png".format(teamcode,filename))

@bp.route('/quxian/',methods=["POST"])
@captcha__is_login
def quxian():#曲线
    img=request.values.get('img')
    gif=request.values.get('gif')
    teamcode=request.values.get('teamcode')
    filename=request.values.get('filename')
    T=request.values.get('T')
    print(T)
    if T is not None and T.isnumeric():
        T= int(T)+1
    print(teamcode)
    print(filename)
    head,context=img.split(",")
    img_data = base64.b64decode(context)
    path="./static/images/{0}/{1}/image.png".format(teamcode,filename)
    try:
        os.remove(path)  
    except:
        print("1")
    with open("./static/images/{0}/{1}/image.png".format(teamcode,filename), "ab") as dcm_file:
        dcm_file.write(img_data)
    image = Image.open("./static/images/{0}/{1}/image.png".format(teamcode,filename))
    width, height = image.size
    zhen=[]
    for y in range(height):
        for x in range(width):
            # 获取当前像素点的颜色值（RGBA格式）
            point=[]
            pixel = image.getpixel((x, y))
            if pixel[:3] == (255, 0, 0):
                for filenames in os.listdir("./static/images/{0}/{1}/saveimg/{2}".format(teamcode,filename,T)):
                    if filenames.endswith('.png'):
                        file_path = os.path.join("./static/images/{0}/{1}/saveimg/{2}".format(teamcode,filename,T), filenames)
                        with Image.open(file_path) as image2:
                            pixel=image2.getpixel((x, y))
                            point.append(pixel)
                zhen.append(point)
    ans=[]
    anst=[]
    sum=0
    for y in range(len(zhen[0])):
        sum=0
        anst.append(y+1)
        for x in range(len(zhen)):
            sum=sum+zhen[x][y]
        ans.append(sum/len(zhen)/255)
    print(ans)
    plt.figure()
    # plt.plot(anst, ans, marker='o', color='r', label='y1-data')

    m = make_interp_spline(anst, ans)
    xs = np.linspace(1, len(zhen[0]), 100)
    ys = m(xs)
    plt.plot(xs, ys)
# 显示图例（使绘制生效）
    plt.legend()
    plt.xlabel('Temporal frames')
    plt.ylabel('Normalization Signal Intensity (a.u.)')
    plt.savefig("./static/images/{0}/{1}/ans.png".format(teamcode,filename))
    return {
            'success': True,
            'message': '添加成功！',
        }
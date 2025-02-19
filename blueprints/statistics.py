from flask import Blueprint, jsonify, request, session
from flask import render_template
import numpy as np
from scipy import stats
from table_config import db
from functool import captcha__is_login
from model import Assess, Dataset, Dwi, Fastmri, Fastnon2d, Fastnon3d, User
import pyecharts
import json
bp=Blueprint("statistics",__name__,url_prefix="/statistics")
@bp.route('/')
@captcha__is_login
def statistics():
    temp = session.get("user_id") 
    user = User.query.get(temp) 
    if user.teamcode=="0":
        return render_template('statistics.html')
    datas = Fastmri.query.filter_by(teamcode=user.teamcode,subjecttoscore=1).all()+Fastnon2d.query.filter_by(teamcode=user.teamcode,subjecttoscore=1).all()+Fastnon3d.query.filter_by(teamcode=user.teamcode,subjecttoscore=1).all()+Dwi.query.filter_by(teamcode=user.teamcode,subjecttoscore=1).all()
    op=[]
    for t in datas:
        data=Assess.query.filter_by(teamcode=user.teamcode,datasname=t.projectname).all()
        ui=0
        for y in data:
            if y.had==1:
                ui=ui+1
        op.append(ui)
    datas = zip(datas, op)
    return render_template('statistics.html',datas=datas)

@bp.route('/datastatistics', methods=['GET'])
@captcha__is_login
def datastatistics():
    temp = session.get("user_id") 
    user = User.query.get(temp) 
    if user.teamcode=="0":
        return render_template('datastatistics.html')
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
        if t.already==0:
            datas = Fastmri.query.filter_by(teamcode=user.teamcode).all()+Fastnon2d.query.filter_by(teamcode=user.teamcode).all()+Fastnon3d.query.filter_by(teamcode=user.teamcode).all()+Dwi.query.filter_by(teamcode=user.teamcode).all()
            op=[]
            for tq in datas:
                data=Assess.query.filter_by(teamcode=user.teamcode,datasname=tq.projectname).all()
                ui=0
                for y in data:
                    if y.had==1:
                        ui=ui+1
                op.append(ui)
            datas = zip(datas, op)
            return render_template('statistics.html',datas=datas)
        b1=t.PSNRA
        b2=t.SSIMA
        b3=t.RLNEA
        b4=t.PSNRB
        b5=t.SSIMB
        b6=t.RLNEB
        b7=t.PSNRC
        b8=t.SSIMC
        b9=t.RLNEC
        data0=[]
        data1=[]
        data2=[]
        e1 = []
        e2 = []
        e3 = []
        e4 = []
        e5 = []
        e6 = []
        e7 = []
        e8 = []
        e9 = []

        data = Assess.query.filter_by(datasname=t.projectname,teamcode=user.teamcode).all()
        for m in data:
            e1.append(m.gradeaOverallquality)
            e2.append(m.gradeaSNR )
            e3.append(m.gradeaArtifactsuppression )
            e4.append(m.gradebOverallquality)
            e5.append(m.gradebSNR )
            e6.append(m.gradebArtifactsuppression)
            e7.append(m.gradecOverallquality )
            e8.append(m.gradecSNR )
            e9.append(m.gradecArtifactsuppression)
        try:
            ea = stats.levene(e3, e1, center='median').pvalue
            if ea>0.05:
                ea=stats.stats.ttest_ind(e3, e1, equal_var=True).pvalue
                if ea>0.05:
                    ea=f"{ea:.2e}>0.05"
                else:
                    ea=f"{ea:.2e}<0.05"
            else:
                ea=0.00e+00
        except:
            ea=None

        try:
            eb = stats.levene(e3, e2, center='median').pvalue
            if eb>0.05:
                eb=stats.stats.ttest_ind(e3, e2, equal_var=True).pvalue
                if eb>0.05:
                    eb=f"{eb:.2e}>0.05"
                else:
                    eb=f"{eb:.2e}<0.05"
            else:
                eb=0.00e+00
        except:
            eb=None

        try:
            ec = stats.levene(e6, e4, center='median').pvalue
            if ec>0.05:
                ec=stats.stats.ttest_ind(e6, e5, equal_var=True).pvalue
                if ec>0.05:
                    ec=f"{ec:.2e}>0.05"
                else:
                    ec=f"{ec:.2e}<0.05"
            else:
                ec=0.00e+00
        except:
            ec=None

        try:
            ed = stats.levene(e6, e5, center='median').pvalue
            if ed>0.05:
                ed=stats.stats.ttest_ind(e6, e5, equal_var=True).pvalue
                if ed>0.05:
                    ed=f"{ed:.2e}>0.05"
                else:
                    ed=f"{ed:.2e}<0.05"
            else:
                ed=0.00e+00
        except:
            ed=None

        try:
            ee = stats.levene(e9, e7, center='median').pvalue
            if ee>0.05:
                ee=stats.stats.ttest_ind(e9, e7, equal_var=True).pvalue
                if ee>0.05:
                    ee=f"{ee:.2e}>0.05"
                else:
                    ee=f"{ee:.2e}<0.05"
            else:
                ee=0.00e+00
        except:
            ee=None

        try:
            ef = stats.levene(e9, e8, center='median').pvalue
            if ef>0.05:
                ef=stats.stats.ttest_ind(e9, e8, equal_var=True).pvalue
                if ef>0.05:
                    ef=f"{ef:.2e}>0.05"
                else:
                    ef=f"{ef:.2e}<0.05"
            else:
                ef=0.00e+00
        except:
            ef=None

        try:
            eaa=stats.wilcoxon(e3,e1,correction=True,alternative='greater').pvalue
            if eaa>0.05:
                eaa=f"{eaa:.2e}>0.05"
            else:
                eaa=f"{eaa:.2e}<0.05"
        except:
            eaa=None

        try:    
            ebb=stats.wilcoxon(e3,e2,correction=True,alternative='greater').pvalue
            if ebb>0.05:
                ebb=f"{ebb:.2e}>0.05"
            else:
                ebb=f"{ebb:.2e}<0.05"
        except:
            ebb=None

        try:
            ecc=stats.wilcoxon(e6,e4,correction=True,alternative='greater').pvalue
            if ecc>0.05:
                ecc=f"{ecc:.2e}>0.05"
            else:
                ecc=f"{ecc:.2e}<0.05"
        except:
            ecc=None

        try:
            edd=stats.wilcoxon(e6,e5,correction=True,alternative='greater').pvalue
            if edd>0.05:
                edd=f"{edd:.2e}>0.05"
            else:
                edd=f"{edd:.2e}<0.05"
        except:
            edd=None

        try:
            eee=stats.wilcoxon(e9,e7,correction=True,alternative='greater').pvalue
            if eee>0.05:
                eee=f"{eee:.2e}>0.05"
            else:
                eee=f"{eee:.2e}<0.05"
        except:
            eee=None

        try:
            eff=stats.wilcoxon(e9,e8,correction=True,alternative='greater').pvalue
            if eff>0.05:
                eff=f"{eff:.2e}>0.05"
            else:
                eff=f"{eff:.2e}<0.05"
        except:
            eff=None

        data0.append(e1)
        data0.append(e4)
        data0.append(e7)
        data1.append(e2)
        data1.append(e5)
        data1.append(e8)
        data2.append(e3)
        data2.append(e6)
        data2.append(e9)
        return render_template('datastatistics.html',tt=tt,e1=format(np.median(np.array(e1)),'.2f'),
                            e2=format(np.median(np.array(e2)),'.2f'),
                            e3=format(np.median(np.array(e3)),'.2f'),
                            e4=format(np.median(np.array(e4)),'.2f'),
                            e5=format(np.median(np.array(e5)),'.2f'),
                            e6=format(np.median(np.array(e6)),'.2f'),
                            e7=format(np.median(np.array(e7)),'.2f'),
                            e8=format(np.median(np.array(e8)),'.2f'),
                            e9=format(np.median(np.array(e9)),'.2f'),
                            e11='{0}±{1}'.format(format(np.mean(np.array(e1)),'.2f'),format(np.std(np.array(e1)),'.2f')),
                            e22='{0}±{1}'.format(format(np.mean(np.array(e2)),'.2f'),format(np.std(np.array(e2)),'.2f')),
                            e33='{0}±{1}'.format(format(np.mean(np.array(e3)),'.2f'),format(np.std(np.array(e3)),'.2f')),
                            e44='{0}±{1}'.format(format(np.mean(np.array(e4)),'.2f'),format(np.std(np.array(e4)),'.2f')),
                            e55='{0}±{1}'.format(format(np.mean(np.array(e5)),'.2f'),format(np.std(np.array(e5)),'.2f')),
                            e66='{0}±{1}'.format(format(np.mean(np.array(e6)),'.2f'),format(np.std(np.array(e6)),'.2f')),
                            e77='{0}±{1}'.format(format(np.mean(np.array(e7)),'.2f'),format(np.std(np.array(e7)),'.2f')),
                            e88='{0}±{1}'.format(format(np.mean(np.array(e8)),'.2f'),format(np.std(np.array(e8)),'.2f')),
                            e99='{0}±{1}'.format(format(np.mean(np.array(e9)),'.2f'),format(np.std(np.array(e9)),'.2f')),
                            ea=ea,
                            eb=eb,
                            ec=ec,
                            ed=ed,
                            ee=ee,
                            ef=ef,
                            eaa=eaa,
                            ebb=ebb,
                            ecc=ecc,
                            edd=edd,
                            eee=eee,
                            eff=eff,
                            b1=b1,
                            b2=b2,
                            b3=b3,
                            b4=b4,
                            b5=b5,
                            b6=b6,
                            b7=b7,
                            b8=b8,
                            b9=b9)
    except Exception as e:
        print(e)

@bp.route('/statisticsajax', methods=['POST'])
@captcha__is_login
def statisticsajax():
    temp = session.get("user_id") 
    user = User.query.get(temp) 
    if user.teamcode=="0":
        return jsonify({"data0":[],"data1":[],"data2":[]})
    data0=[]
    data1=[]
    data2=[]
    e1 = []
    e2 = []
    e3 = []
    e4 = []
    e5 = []
    e6 = []
    e7 = []
    e8 = []
    e9 = []
    try:
        ta=request.form.get('data')
        te=Dataset.query.filter_by(datasname=ta,teamcode=user.teamcode).first()
        if te.kind=="Fastmri":
            t = Fastmri.query.filter_by(projectname=ta,teamcode=user.teamcode).first()
        elif te.kind=="Fastnon2d":
            t = Fastnon2d.query.filter_by(projectname=ta,teamcode=user.teamcode).first()
        elif te.kind=="Fastnon3d":
            t = Fastnon3d.query.filter_by(projectname=ta,teamcode=user.teamcode).first()
        elif te.kind=="Dwi":
            t = Dwi.query.filter_by(projectname=ta,teamcode=user.teamcode).first()
        data = Assess.query.filter_by(datasname=t.projectname,teamcode=user.teamcode).all()
        for m in data:
            e1.append(m.gradeaOverallquality)
            e2.append(m.gradeaSNR )
            e3.append(m.gradeaArtifactsuppression )
            e4.append(m.gradebOverallquality)
            e5.append(m.gradebSNR )
            e6.append(m.gradebArtifactsuppression)
            e7.append(m.gradecOverallquality )
            e8.append(m.gradecSNR )
            e9.append(m.gradecArtifactsuppression)
        data0.append(e1)
        data0.append(e4)
        data0.append(e7)
        data1.append(e2)
        data1.append(e5)
        data1.append(e8)
        data2.append(e3)
        data2.append(e6)
        data2.append(e9)
        return jsonify({"data0":data0,"data1":data1,"data2":data2})
    except Exception as e:
        print(e)
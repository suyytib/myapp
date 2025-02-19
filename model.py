# 从table_config模块中导入数据库实例db  
from table_config import db

# 用户表  
class User(db.Model):  
    # 定义数据库中的表名  
    __tablename__ = "user"

    # 定义用户ID列，类型为整数，是主键且自动增长  
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 

    # 定义用户名列，类型为最大长度为10的字符串，不可为空  
    username = db.Column(db.String(10), nullable=False)

    # 定义密码列，类型为最大长度为200的字符串，不可为空  
    password = db.Column(db.String(200), nullable=False) 

    # 定义邮箱列，类型为最大长度为255的字符串，不可为空  
    email = db.Column(db.String(255), nullable=False)

    status=db.Column(db.String(255), nullable=False)

    permissions=db.Column(db.Integer, nullable=False)

    teamcode=db.Column(db.String(255), nullable=False)


class Captcha(db.Model):  
    # 定义数据库中的表名  
    __tablename__ = "captcha"

    # 定义验证码ID列，类型为整数，是主键且自动增长  
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # 定义邮箱列，类型为最大长度为255的字符串，不可为空  
    email = db.Column(db.String(255), nullable=False)

    # 定义验证码列，类型为最大长度为255的字符串，不可为空  
    captcha = db.Column(db.String(255), nullable=False)

class Assess(db.Model):  
    # 定义数据库中的表名  
    __tablename__ = "assess"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    imgname = db.Column(db.String(255), nullable=False)
    kinds= db.Column(db.Integer,default=0)
    gradeaOverallquality = db.Column(db.Float,default=0)
    gradeaSNR = db.Column(db.Float,default=0)
    gradeaArtifactsuppression = db.Column(db.Float,default=0)
    gradebOverallquality = db.Column(db.Float,default=0)
    gradebSNR = db.Column(db.Float,default=0)
    gradebArtifactsuppression = db.Column(db.Float,default=0)
    gradecOverallquality = db.Column(db.Float,default=0)
    gradecSNR = db.Column(db.Float,default=0)
    gradecArtifactsuppression = db.Column(db.Float,default=0)
    had = db.Column(db.Integer,default=0)
    datasname = db.Column(db.String(255), nullable=False)
    teamcode = db.Column(db.String(255), nullable=False)

class Dataset(db.Model):  
    # 定义数据库中的表名  
    __tablename__ = "dataset"  
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    datasname = db.Column(db.String(255), nullable=False)
    teamcode = db.Column(db.String(255), nullable=False)
    kind = db.Column(db.String(255), nullable=False)

class Fastnon3d(db.Model):  
    # 定义数据库中的表名  
    __tablename__ = "fastnoncartesian3dreconstruction"  
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    projectname = db.Column(db.String(255), nullable=False)
    PSNRA = db.Column(db.Float ,default=0)
    SSIMA = db.Column(db.Float ,default=0)
    RLNEA = db.Column(db.Float,default=0)
    PSNRB = db.Column(db.Float ,default=0)
    SSIMB = db.Column(db.Float,default=0)
    RLNEB = db.Column(db.Float ,default=0)
    PSNRC = db.Column(db.Float ,default=0)
    SSIMC = db.Column(db.Float ,default=0)
    RLNEC = db.Column(db.Float ,default=0)
    teamcode = db.Column(db.String(255),default=0)
    time = db.Column( db.String(255),default=0)
    already = db.Column(db.Integer ,default=0)
    fenshu = db.Column(db.Integer ,default=0)
    updatetime = db.Column(db.String(255),default=0)
    motaikind = db.Column(db.String(255),default=0)
    Overallquality = db.Column(db.Integer ,default=0)
    SNR = db.Column(db.Integer ,default=0)
    Artifactsuppression = db.Column(db.Integer ,default=0)
    #####################################
    targetanalysismethod = db.Column(db.String(255),default=0)
    subjecttoscore = db.Column(db.Integer ,default=0)
    anatomy = db.Column(db.String(255),default=0)
    trajectory = db.Column(db.String(255),default=0)
    accelerationfactor = db.Column(db.Integer ,default=0)
    handlerawdata = db.Column(db.String(255),default=0)
    Numberofmethods = db.Column(db.Integer ,default=2)

class Fastnon2d(db.Model):  
    # 定义数据库中的表名  
    __tablename__ = "fastnoncartesian2dreconstruction"  
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    projectname = db.Column(db.String(255), nullable=False)
    PSNRA = db.Column(db.Float ,default=0)
    SSIMA = db.Column(db.Float ,default=0)
    RLNEA = db.Column(db.Float,default=0)
    PSNRB = db.Column(db.Float ,default=0)
    SSIMB = db.Column(db.Float,default=0)
    RLNEB = db.Column(db.Float ,default=0)
    PSNRC = db.Column(db.Float ,default=0)
    SSIMC = db.Column(db.Float ,default=0)
    RLNEC = db.Column(db.Float ,default=0)
    teamcode = db.Column(db.String(255),default=0)
    time = db.Column( db.String(255),default=0)
    already = db.Column(db.Integer ,default=0)
    fenshu = db.Column(db.Integer ,default=0)
    updatetime = db.Column(db.String(255),default=0)
    Overallquality = db.Column(db.Integer ,default=0)
    motaikind = db.Column(db.String(255),default=0)
    SNR = db.Column(db.Integer ,default=0)
    Artifactsuppression = db.Column(db.Integer ,default=0)
    #####################################
    targetanalysismethod = db.Column(db.String(255),default=0)
    subjecttoscore = db.Column(db.Integer ,default=0)
    anatomy = db.Column(db.String(255),default=0)
    trajectory = db.Column(db.String(255),default=0)
    accelerationfactor = db.Column(db.Integer ,default=0)
    handlerawdata = db.Column(db.String(255),default=0)
    Numberofmethods = db.Column(db.Integer ,default=2)

class Fastmri(db.Model):  
    # 定义数据库中的表名  
    __tablename__ = "fastmri"  
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    projectname = db.Column(db.String(255), nullable=False)
    PSNRA = db.Column(db.Float ,default=0)
    SSIMA = db.Column(db.Float ,default=0)
    RLNEA = db.Column(db.Float,default=0)
    PSNRB = db.Column(db.Float ,default=0)
    SSIMB = db.Column(db.Float,default=0)
    RLNEB = db.Column(db.Float ,default=0)
    PSNRC = db.Column(db.Float ,default=0)
    SSIMC = db.Column(db.Float ,default=0)
    RLNEC = db.Column(db.Float ,default=0)
    teamcode = db.Column(db.String(255),default=0)
    time = db.Column( db.String(255),default=0)
    already = db.Column(db.Integer ,default=0)
    motaikind = db.Column(db.String(255),default=0)
    fenshu = db.Column(db.Integer ,default=0)
    updatetime = db.Column(db.String(255),default=0)
    Overallquality = db.Column(db.Integer ,default=0)
    SNR = db.Column(db.Integer ,default=0)
    Artifactsuppression = db.Column(db.Integer ,default=0)
    #####################################
    contrast = db.Column(db.String(255),default=0)
    section = db.Column(db.String(255),default=0)
    samplingpattern = db.Column(db.String(255),default=0)
    targetanalysismethod = db.Column(db.String(255),default=0)
    samplingrate = db.Column(db.Float ,default=0)
    subjecttoscore = db.Column(db.Integer ,default=0)
    anatomy = db.Column(db.String(255),default=0)
    Numberofmethods = db.Column(db.Integer ,default=2)

class Dwi(db.Model):  
    # 定义数据库中的表名  
    __tablename__ = "multishotiepidwi"  
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    projectname = db.Column(db.String(255), nullable=False)
    PSNRA = db.Column(db.Float ,default=0)
    SSIMA = db.Column(db.Float ,default=0)
    RLNEA = db.Column(db.Float,default=0)
    PSNRB = db.Column(db.Float ,default=0)
    SSIMB = db.Column(db.Float,default=0)
    RLNEB = db.Column(db.Float ,default=0)
    PSNRC = db.Column(db.Float ,default=0)
    SSIMC = db.Column(db.Float ,default=0)
    RLNEC = db.Column(db.Float ,default=0)
    teamcode = db.Column(db.String(255),default=0)
    time = db.Column( db.String(255),default=0)
    already = db.Column(db.Integer ,default=0)
    fenshu = db.Column(db.Integer ,default=0)
    updatetime = db.Column(db.String(255),default=0)
    motaikind = db.Column(db.String(255),default=0)
    Overallquality = db.Column(db.Integer ,default=0)
    SNR = db.Column(db.Integer ,default=0)
    Artifactsuppression = db.Column(db.Integer ,default=0)
    #####################################
    reconstructionmatrixsize = db.Column(db.String(255),default=0)
    targetanalysismethod = db.Column(db.String(255),default=0)
    numberofshots = db.Column(db.Integer ,default=0)
    accelerationfactor = db.Column(db.Integer ,default=0)
    subjecttoscore = db.Column(db.Integer ,default=0)
from flask import Blueprint
from flask import render_template

from functool import captcha__is_login
bp=Blueprint("root",__name__,url_prefix="/")
@bp.route('/')
@captcha__is_login
def root():
    return render_template('enter-the-animation.html')

@bp.route('/home')
@captcha__is_login
def home():
    return render_template('root.html')


import subprocess
import threading
import time
from flask import Blueprint, jsonify, request, session
from flask import render_template
from table_config import db
from functool import captcha__is_login
from model import User
bp=Blueprint("teammates",__name__,url_prefix="/teammates")
@bp.route('/')
@captcha__is_login
def teammates():
    temp = session.get("user_id") 
    user = User.query.get(temp) 
    team=[]
    if user.teamcode!="0":
        team = User.query.filter_by(teamcode=user.teamcode).all()
    return render_template('teammates.html',team=team)

@bp.route('/add/', methods=['POST'])
@captcha__is_login
def add():
    temp = session.get("user_id") 
    users = User.query.get(temp) 
    name = request.values.get('title')
    user = User.query.filter_by(username=name).first()
    if user and user.teamcode=="0" and users.teamcode!="0":
        user.teamcode=users.teamcode
        db.session.commit()
        return {
            'success': True,
            'message': '添加成功！',
        }
    else:
        return {
                'success': False,
                'message': '添加失败！',
            }
    
@bp.route('/leave/')
@captcha__is_login
def leave():
    temp = session.get("user_id") 
    users = User.query.get(temp) 
    if users.teamcode!="0":
        teams=User.query.filter_by(teamcode=users.teamcode).all()
        for te in teams:
            te.teamcode="0"
    else:
        users.teamcode="0"
    db.session.commit()
    return render_template('teammates.html',team=[])

@bp.route('/delete/')
@captcha__is_login
def delete():
    temp = session.get("user_id") 
    users = User.query.get(temp) 
    name =request.args["name"]
    user = User.query.filter_by(username=name).first()
    user.teamcode="0"
    db.session.commit()
    team=[]
    if users.teamcode!="0":
        team = User.query.filter_by(teamcode=users.teamcode).all()
    return render_template('teammates.html',team=team)

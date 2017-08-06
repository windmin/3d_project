#coding=utf8
from flask import render_template,session,redirect,url_for,flash,request,jsonify,send_from_directory
#蓝本
from . import main
#表单
# from .forms import BengxuanxingListbiao,Bengxuanxingtiaomu,TianjiaBaojia,TianjiaTiaomu,Editmotor,Editmotorjishu,Editbengjiage,Editcaizhixishu,Editdianjijiage,Editmifengjiage,Editshuilv,EditBaojia,Editmaoli,Editothers,Editxishu,Maoliduibi,Editgroup
from .. import db
#数据表
# from ..models import
from flask_login import login_required,current_user
from ..decorators import admin_required

import time
import datetime
import os



@main.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)

@main.route('/')
def index():
    # return render_template('index.html')
    return jsonify(username="username",
                   email="email",
                   id="id")
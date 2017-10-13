#coding=utf8
from flask import render_template,session,redirect,url_for,flash,request,jsonify,send_from_directory
#蓝本
from . import main
#表单
from .forms import SelectShebeiForm, CreateShebeiForm
from .. import db
#数据表
from ..models import ShebeiTable
from flask_login import login_required,current_user
from ..decorators import admin_required
from .process_function import calculate_slot, calculate_one_front_front, calculate_one_back_back, \
    calculate_two_front_front,calculate_two_back_back,calculate_one_back_front,calculate_two_back_front, \
    calculate_one_front_back, calculate_two_front_back

import time
import datetime
import os


# 机架管理
@main.route('/shebei',methods=['GET','POST'])
@login_required
def shebei():
    form = CreateShebeiForm()

    form.front_slotNums.render_kw = {'disabled':'true'}
    form.front_slot_rows.render_kw = {'disabled':'true'}
    form.front_slot_cols.render_kw = {'disabled':'true'}
    form.back_slotNums.render_kw = {'disabled':'true'}
    form.back_slot_rows.render_kw = {'disabled':'true'}
    form.back_slot_cols.render_kw = {'disabled':'true'}

    shebeiTables = ShebeiTable.query.order_by(ShebeiTable.shebei_name.asc()).all()

    if form.submit.data:
        shebei_name = form.shebei_name.data
        front_slotNums = form.front_slotNums.data
        front_slot_rows = form.front_slot_rows.data
        front_slot_cols = form.front_slot_cols.data
        back_slotNums = form.back_slotNums.data
        back_slot_rows = form.back_slot_rows.data
        back_slot_cols = form.back_slot_cols.data
        shebei_place = form.shebei_place.data

        if shebei_name != '' and front_slotNums != '' and front_slot_rows != '' \
                and front_slot_cols != '' and back_slotNums != '' and back_slot_rows != '' \
                and back_slot_cols != '' and shebei_place != '':
            if ShebeiTable.query.filter_by(shebei_name=shebei_name).first():
                flash('%s已存在，无法新增成功！' %(shebei_name))
            else:
                db.session.add(ShebeiTable(shebei_name=shebei_name, \
                                           front_slotNums=front_slotNums, \
                                           front_slot_rows=front_slot_rows, \
                                           front_slot_cols=front_slot_cols, \
                                           back_slotNums=back_slotNums, \
                                           back_slot_rows=back_slot_rows, \
                                           back_slot_cols=back_slot_cols, \
                                           shebei_place=shebei_place))
                db.session.commit()
            return redirect(url_for('main.shebei'))

    elif request.method == 'POST':
        if request.form["search"] == "搜索":
            number = request.form.get('Number')
            if number !='':
                shebeiTables = ShebeiTable.query.filter(ShebeiTable.shebei_name.like('%'+number+'%')).all()
                if not shebeiTables:
                    flash('未找到搜索结果！')
            else:
                return redirect(url_for('main.shebei'))


    results = ShebeiTable.query.order_by(ShebeiTable.shebei_name.asc()).all()
    if results:
        if results[-1].shebei_name[1:2] == '号':
            form.shebei_name.data = str(int(results[-1].shebei_name[0:1]) + 1) + '号机架'
        else:
            form.shebei_name.data = ''
    return render_template('shebei.html', shebeiTables=shebeiTables, form=form)


# 选择设备、正背面、端口、计算
@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = SelectShebeiForm()

    if request.method == 'POST':
        if request.form["submit"] == "下一步 >":
            jiechushebei_side = request.form.get('jiechushebei_side')
            jierushebei_side = request.form.get('jierushebei_side')
    if form.submit.data:
        shebei_count = form.shebei_count.data
        jiechushebei = form.jiechushebei.data
        # jiechushebei_side = form.jiechushebei_side.data
        jierushebei = form.jierushebei.data
        # jierushebei_side = form.jierushebei_side.data

        if shebei_count == 1:
            if jiechushebei != jierushebei:
                flash('跳纤机架数=1时，接出机架和接入机架必须是同一台！请重新选择！')
                return redirect(url_for('main.index'))
        elif shebei_count > 1 :
            if jiechushebei == jierushebei:
                flash('跳纤机架数>1时，接出机架和接入机架必须时不同的！请重新选择！')
                return redirect(url_for('main.index'))
        shebei_dict = {
            'shebei_count': shebei_count,
            'jiechushebei': jiechushebei,
            'jiechushebei_side': jiechushebei_side,
            'jierushebei': jierushebei,
            'jierushebei_side': jierushebei_side
            }
        # if (jiechushebei_side == jierushebei_side == '96芯设备单元' \
        #         or jiechushebei_side == jierushebei_side == '72芯配线单元') \
        #         and jiechushebei == jierushebei:
        #     return redirect(url_for('main.slot', shebei_dict=shebei_dict))
        # elif jiechushebei != jierushebei and jiechushebei_side == jierushebei_side == '96芯设备单元':
        #     return redirect(url_for('main.slot', shebei_dict=shebei_dict))
        # else:
        #     flash('目前只支持计算相同机架相同单元；和不同机架的96芯设备单元间的跳纤计算')
        # if jiechushebei_side == '96芯设备单元' and jierushebei == '72芯配线单元':
        #     flash('目前不支持96芯设备单元跳向72芯配线单元间！')
        # else:
        return redirect(url_for('main.slot', shebei_dict=shebei_dict))

    # elif form.reset.data:
    #     return redirect(url_for('main.index'))
    # elif form.step.data:
    #     print('step')
    return render_template('index.html', form=form)

# 选择slot端口
@main.route('/slot/<shebei_dict>', methods=['GET', 'POST'])
def slot(shebei_dict):
    shebei_dict = eval(shebei_dict)
    # 1. 接出设备
    jiechushebei_info = ShebeiTable.query.filter_by(shebei_name=shebei_dict['jiechushebei']).first()
    if shebei_dict['jiechushebei_side'] == '96芯设备单元':
        jiechushebei_slotNums = range(1,jiechushebei_info.front_slotNums+1)
        jiechushebei_slot_rows = range(1,jiechushebei_info.front_slot_rows+1)
        jiechushebei_slot_cols = range(1,jiechushebei_info.front_slot_cols+1)
    elif shebei_dict['jiechushebei_side'] == '72芯配线单元':
        jiechushebei_slotNums = range(1,jiechushebei_info.back_slotNums+1)
        jiechushebei_slot_rows = range(1,jiechushebei_info.back_slot_rows+1)
        jiechushebei_slot_cols = range(1,jiechushebei_info.back_slot_cols+1)
    jiechushebei_slot = []
    jiechushebei_slot = calculate_slot(len(jiechushebei_slot_rows), len(jiechushebei_slot_cols), jiechushebei_slot)

    # 2. 接入设备
    jierushebei_info = ShebeiTable.query.filter_by(shebei_name=shebei_dict['jierushebei']).first()
    if shebei_dict['jierushebei_side'] == '96芯设备单元':
        jierushebei_slotNums = range(1,jierushebei_info.front_slotNums+1)
        jierushebei_slot_rows = range(1,jierushebei_info.front_slot_rows+1)
        jierushebei_slot_cols = range(1,jierushebei_info.front_slot_cols+1)
    elif shebei_dict['jierushebei_side'] == '72芯配线单元':
        jierushebei_slotNums = range(1,jierushebei_info.back_slotNums+1)
        jierushebei_slot_rows = range(1,jierushebei_info.back_slot_rows+1)
        jierushebei_slot_cols = range(1,jierushebei_info.back_slot_cols+1)
    jierushebei_slot = []
    jierushebei_slot = calculate_slot(len(jierushebei_slot_rows),len(jierushebei_slot_cols),jierushebei_slot)

    # 数据库记录 正面used，背面used
    # 正面used实例：
    # jiechushebei_usedlist_dict = {3:[(1,4),(2,17)], \
    #                               4:[(3,12)], \
    #                               1:[(1,24)]}
    jiechushebei_usedlist_dict = {}
    jierushebei_usedlist_dict = {}

    if len(jiechushebei_slotNums) > len(jierushebei_slotNums):
        difference_slotNums = range(len(jierushebei_slotNums)+1,len(jiechushebei_slotNums)+1)
    elif len(jiechushebei_slotNums) < len(jierushebei_slotNums):
        difference_slotNums = range(len(jiechushebei_slotNums)+1,len(jierushebei_slotNums)+1)
    else:
        difference_slotNums = []


    shebei_dict['jiechushebei_slotNums'] = jiechushebei_slotNums #range(1,10) #9
    shebei_dict['jiechushebei_slot'] = jiechushebei_slot #96
    shebei_dict['jiechushebei_slot_rows'] = jiechushebei_slot_rows #4
    shebei_dict['jiechushebei_slot_cols'] = jiechushebei_slot_cols #24

    shebei_dict['jierushebei_slotNums'] = jierushebei_slotNums #12
    shebei_dict['jierushebei_slot'] = jierushebei_slot #72
    shebei_dict['jierushebei_slot_rows'] = jierushebei_slot_rows #6
    shebei_dict['jierushebei_slot_cols'] = jierushebei_slot_cols #12

    shebei_dict['jiechushebei_usedlist_dict'] = jiechushebei_usedlist_dict
    shebei_dict['jierushebei_usedlist_dict'] = jierushebei_usedlist_dict

    shebei_dict['difference_slotNums'] = difference_slotNums

    if request.method == 'POST':
        if request.form["submit"] == "开始计算":
            jiechushebei_radio = request.form.get('jiechushebei')
            jierushebei_radio = request.form.get('jierushebei')
            if jierushebei_radio is None or jierushebei_radio is None:
                flash('请选择需要连接的两个端口！')
            else:
                shebei_dict['jiechushebei_radio'] = jiechushebei_radio.split(',') #['1', '1', '24']
                shebei_dict['jierushebei_radio'] = jierushebei_radio.split(',')
                if shebei_dict['jiechushebei_radio'] == shebei_dict['jierushebei_radio']:
                    flash('不能选择同一个设备的同一个端口,请重新选择！')
                elif int(shebei_dict['jiechushebei_radio'][0]) > int(shebei_dict['jierushebei_radio'][0]):
                    flash('接出端口必需高于接入端口！')
                elif shebei_dict['jiechushebei_radio'][0] == '12' and shebei_dict['jiechushebei_side'] == '72芯配线单元':
                    flash('接出端口不能是最后一个单元！')
                elif shebei_dict['jiechushebei_radio'][0] == '9' and shebei_dict['jiechushebei_side'] == '96芯设备单元':
                    flash('接出端口不能是最后一个单元！')
                else:
                    return redirect(url_for('main.step',shebei_dict=shebei_dict))
    return render_template('slot.html', shebei_dict=shebei_dict)


@main.route('/step/<shebei_dict>',methods=['GET','POST'])
def step(shebei_dict):
    shebei_dict = eval(shebei_dict)
    shebei_dict2 = shebei_dict.copy()
    del shebei_dict2['jiechushebei_slot']
    del shebei_dict2['jierushebei_slot']
    # 同一个设备相连
    if shebei_dict['jiechushebei'] == shebei_dict['jierushebei']:
        # 同side相连
        if shebei_dict['jiechushebei_side'] == shebei_dict['jierushebei_side']:
            if shebei_dict['jiechushebei_side'] == '96芯设备单元':
                step_list, log_list, session['json_list'] =calculate_one_front_front(shebei_dict['jiechushebei_radio'],shebei_dict['jierushebei_radio'], \
                                          shebei_dict['jiechushebei_slot_rows'],shebei_dict['jiechushebei_slot_cols'],\
                                          shebei_dict['jierushebei_slot_rows'],shebei_dict['jierushebei_slot_cols'],\
                                          shebei_dict['jiechushebei'],shebei_dict['jierushebei'])
                return render_template('step.html',shebei_dict=shebei_dict2,step_list=step_list,log_list=log_list)
            elif shebei_dict['jiechushebei_side'] == '72芯配线单元':
                step_list, log_list, session['json_list'] = calculate_one_back_back(shebei_dict['jiechushebei_radio'],shebei_dict['jierushebei_radio'], \
                                          shebei_dict['jiechushebei'],shebei_dict['jierushebei'])
                return render_template('step_back.html', shebei_dict=shebei_dict2, step_list=step_list, log_list=log_list)
        # 不同side相连
        elif shebei_dict['jiechushebei_side'] != shebei_dict['jierushebei_side']:
            if shebei_dict['jiechushebei_side'] == '72芯配线单元':
                step_list, log_list, session['json_list'] = calculate_one_back_front(shebei_dict['jiechushebei_radio'],shebei_dict['jierushebei_radio'], \
                                                                                     shebei_dict['jiechushebei_slot_rows'],shebei_dict['jiechushebei_slot_cols'], \
                                                                                     shebei_dict['jierushebei_slot_rows'],shebei_dict['jierushebei_slot_cols'],\
                                                                                     shebei_dict['jiechushebei'],shebei_dict['jierushebei'])
                return render_template('step_back_front.html', shebei_dict=shebei_dict2, step_list=step_list, log_list=log_list)
            elif shebei_dict['jiechushebei_side'] == '96芯设备单元':
                step_list, log_list, session['json_list'] = calculate_one_front_back(shebei_dict['jiechushebei_radio'],shebei_dict['jierushebei_radio'], \
                                          shebei_dict['jiechushebei_slot_rows'],shebei_dict['jiechushebei_slot_cols'],\
                                          shebei_dict['jierushebei_slot_rows'],shebei_dict['jierushebei_slot_cols'],\
                                          shebei_dict['jiechushebei'],shebei_dict['jierushebei'])
                return render_template('step_front_back.html', shebei_dict=shebei_dict2, step_list=step_list, log_list=log_list)
    # 不同设备相连
    elif shebei_dict['jiechushebei'] != shebei_dict['jierushebei']:
        if shebei_dict['jiechushebei_side'] == shebei_dict['jierushebei_side'] and shebei_dict['jiechushebei_side'] == '96芯设备单元':
            step_list, log_list, session['json_list'] = calculate_two_front_front(shebei_dict['jiechushebei_radio'],shebei_dict['jierushebei_radio'], \
                                          shebei_dict['jiechushebei_slot_rows'],shebei_dict['jiechushebei_slot_cols'],\
                                          shebei_dict['jierushebei_slot_rows'],shebei_dict['jierushebei_slot_cols'],\
                                          shebei_dict['jiechushebei'],shebei_dict['jierushebei'],\
                                          shebei_dict['shebei_count'])
            return render_template('step_two_front.html', shebei_dict=shebei_dict2, step_list=step_list, log_list=log_list)
        elif shebei_dict['jiechushebei_side'] == shebei_dict['jierushebei_side'] and shebei_dict['jiechushebei_side'] == '72芯配线单元':
            step_list, log_list, session['json_list'] = calculate_two_back_back(shebei_dict['jiechushebei_radio'],shebei_dict['jierushebei_radio'], \
                                          shebei_dict['jiechushebei'],shebei_dict['jierushebei'],shebei_dict['shebei_count'])
            return render_template('step_two_back.html', shebei_dict=shebei_dict2, step_list=step_list, log_list=log_list)
        elif shebei_dict['jiechushebei_side'] == '72芯配线单元' and shebei_dict['jierushebei_side'] == '96芯设备单元':
            step_list, log_list, session['json_list'] = calculate_two_back_front(shebei_dict['jiechushebei_radio'],shebei_dict['jierushebei_radio'], \
                                                                                 shebei_dict['jiechushebei_slot_rows'],shebei_dict['jiechushebei_slot_cols'], \
                                                                                 shebei_dict['jierushebei_slot_rows'],shebei_dict['jierushebei_slot_cols'], \
                                                                                 shebei_dict['jiechushebei'],shebei_dict['jierushebei'],\
                                                                                 shebei_dict['shebei_count'])
            return render_template('step_two_back_front.html', shebei_dict=shebei_dict2, step_list=step_list, log_list=log_list)
        elif shebei_dict['jiechushebei_side'] == '96芯设备单元' and shebei_dict['jierushebei_side'] == '72芯配线单元':
            step_list, log_list, session['json_list'] = calculate_two_front_back(shebei_dict['jiechushebei_radio'],shebei_dict['jierushebei_radio'], \
                                          shebei_dict['jiechushebei_slot_rows'],shebei_dict['jiechushebei_slot_cols'],\
                                          shebei_dict['jierushebei_slot_rows'],shebei_dict['jierushebei_slot_cols'],\
                                          shebei_dict['jiechushebei'],shebei_dict['jierushebei'],\
                                          shebei_dict['shebei_count'])
            return render_template('step_two_front_back.html', shebei_dict=shebei_dict2, step_list=step_list, log_list=log_list)

    # return render_template('step.html',shebei_dict=shebei_dict2,step_list=step_list,log_list=log_list)


@main.route('/modf')
def modf():
    return render_template('webgl_loader_obj_mtl.html')

@main.route('/shebei/delete/<id>',methods=['GET','POST'])
@login_required
def shebei_delete(id):
    result = ShebeiTable.query.filter_by(id=id).first()
    db.session.delete(result)
    db.session.commit()
    return redirect(url_for('main.shebei'))
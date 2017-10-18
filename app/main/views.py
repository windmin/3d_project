#coding=utf8
from flask import render_template,session,redirect,url_for,flash,request,jsonify,send_from_directory
#蓝本
from . import main
#表单
from .forms import SelectShebeiForm, CreateShebeiForm, SettingForm
from .. import db
#数据表
from ..models import ShebeiTable, DuankouTable, Log, LineTable, CompanyTable
from flask_login import login_required,current_user
from ..decorators import admin_required
from .process_function import calculate_slot, calculate_one_front_front, calculate_one_back_back, \
    calculate_two_front_front,calculate_two_back_back,calculate_one_back_front,calculate_two_back_front, \
    calculate_one_front_back, calculate_two_front_back

import time
import datetime
import os

from datetime import datetime


# 72芯配线单元ABCD EFGH IJKL
PEIXIAN_DANYUAN = {
    '1': '12',
    '2': '11',
    '3': '10',
    '4': '9',
    '5': '8',
    '6': '7',
    '7': '6',
    '8': '5',
    '9': '4',
    '10': '3',
    '11': '2',
    '12': '1'
}


def format_radio_96(row, col):
    return 1+24*(int(row)-1)+(int(col)-1)


def format_duankou(side, row, col):
    if side == '96芯设备单元':
        result = str(1+24*(int(row)-1)+(int(col)-1))
    elif side == '72芯配线单元':
        result = str(row)+','+str(col)
    return result


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
@main.route('/new-jumping', methods=['GET', 'POST'])
@login_required
def index():
    form = SelectShebeiForm()

    if request.method == 'POST':
        if request.form["submit"] == "下一步 >":
            jiechushebei_side = request.form.get('jiechushebei_side')
            jierushebei_side = request.form.get('jierushebei_side')
    if form.submit.data:
        # shebei_count = form.shebei_count.data
        jiechushebei = form.jiechushebei.data
        # jiechushebei_side = form.jiechushebei_side.data
        jierushebei = form.jierushebei.data
        # jierushebei_side = form.jierushebei_side.data

        shebei_count = abs(int(jierushebei[0])-int(jiechushebei[0])) + 1
        # if shebei_count == 1:
        #     if jiechushebei != jierushebei:
        #         flash('跳纤机架数=1时，接出机架和接入机架必须是同一台！请重新选择！')
        #         return redirect(url_for('main.index'))
        # elif shebei_count > 1 :
        #     if jiechushebei == jierushebei:
        #         flash('跳纤机架数>1时，接出机架和接入机架必须时不同的！请重新选择！')
        #         return redirect(url_for('main.index'))
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
                # elif int(shebei_dict['jiechushebei_radio'][0]) > int(shebei_dict['jierushebei_radio'][0]):
                #     flash('接出端口必需高于接入端口！')
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
                step_list, log_list, session['json_list'], line =calculate_one_front_front(shebei_dict['jiechushebei_radio'],shebei_dict['jierushebei_radio'], \
                                          shebei_dict['jiechushebei_slot_rows'],shebei_dict['jiechushebei_slot_cols'],\
                                          shebei_dict['jierushebei_slot_rows'],shebei_dict['jierushebei_slot_cols'],\
                                          shebei_dict['jiechushebei'],shebei_dict['jierushebei'])
                jiechu_duankou = format_radio_96(shebei_dict2['jiechushebei_radio'][1],
                                                 shebei_dict2['jiechushebei_radio'][2])
                jieru_duankou = format_radio_96(shebei_dict2['jierushebei_radio'][1],
                                                shebei_dict2['jierushebei_radio'][2])
                return render_template('step.html',shebei_dict=shebei_dict2,step_list=step_list,log_list=log_list, line=line, jiechu_duankou=jiechu_duankou, jieru_duankou=jieru_duankou)
            elif shebei_dict['jiechushebei_side'] == '72芯配线单元':
                step_list, log_list, session['json_list'], line = calculate_one_back_back(shebei_dict['jiechushebei_radio'],shebei_dict['jierushebei_radio'], \
                                          shebei_dict['jiechushebei'],shebei_dict['jierushebei'])
                return render_template('step_back.html', shebei_dict=shebei_dict2, step_list=step_list, log_list=log_list, line=line)
        # 不同side相连
        elif shebei_dict['jiechushebei_side'] != shebei_dict['jierushebei_side']:
            if shebei_dict['jiechushebei_side'] == '72芯配线单元':
                step_list, log_list, session['json_list'], line = calculate_one_back_front(shebei_dict['jiechushebei_radio'],shebei_dict['jierushebei_radio'], \
                                                                                     shebei_dict['jiechushebei_slot_rows'],shebei_dict['jiechushebei_slot_cols'], \
                                                                                     shebei_dict['jierushebei_slot_rows'],shebei_dict['jierushebei_slot_cols'],\
                                                                                     shebei_dict['jiechushebei'],shebei_dict['jierushebei'])
                jieru_duankou = format_radio_96(shebei_dict2['jierushebei_radio'][1],
                                                shebei_dict2['jierushebei_radio'][2])
                return render_template('step_back_front.html', shebei_dict=shebei_dict2, step_list=step_list, log_list=log_list, line=line, jieru_duankou=jieru_duankou)
            elif shebei_dict['jiechushebei_side'] == '96芯设备单元':
                step_list, log_list, session['json_list'], line = calculate_one_front_back(shebei_dict['jiechushebei_radio'],shebei_dict['jierushebei_radio'], \
                                          shebei_dict['jiechushebei_slot_rows'],shebei_dict['jiechushebei_slot_cols'],\
                                          shebei_dict['jierushebei_slot_rows'],shebei_dict['jierushebei_slot_cols'],\
                                          shebei_dict['jiechushebei'],shebei_dict['jierushebei'])
                jiechu_duankou = format_radio_96(shebei_dict2['jiechushebei_radio'][1],
                                                 shebei_dict2['jiechushebei_radio'][2])
                return render_template('step_front_back.html', shebei_dict=shebei_dict2, step_list=step_list, log_list=log_list, line=line, jiechu_duankou=jiechu_duankou)
    # 不同设备相连
    elif shebei_dict['jiechushebei'] != shebei_dict['jierushebei']:
        if shebei_dict['jiechushebei_side'] == shebei_dict['jierushebei_side'] and shebei_dict['jiechushebei_side'] == '96芯设备单元':
            step_list, log_list, session['json_list'], line = calculate_two_front_front(shebei_dict['jiechushebei_radio'],shebei_dict['jierushebei_radio'], \
                                          shebei_dict['jiechushebei_slot_rows'],shebei_dict['jiechushebei_slot_cols'],\
                                          shebei_dict['jierushebei_slot_rows'],shebei_dict['jierushebei_slot_cols'],\
                                          shebei_dict['jiechushebei'],shebei_dict['jierushebei'],\
                                          shebei_dict['shebei_count'])
            jiechu_duankou = format_radio_96(shebei_dict2['jiechushebei_radio'][1],
                                             shebei_dict2['jiechushebei_radio'][2])
            jieru_duankou = format_radio_96(shebei_dict2['jierushebei_radio'][1],
                                            shebei_dict2['jierushebei_radio'][2])
            return render_template('step_two_front.html', shebei_dict=shebei_dict2, step_list=step_list, log_list=log_list, line=line, jiechu_duankou=jiechu_duankou, jieru_duankou=jieru_duankou)
        elif shebei_dict['jiechushebei_side'] == shebei_dict['jierushebei_side'] and shebei_dict['jiechushebei_side'] == '72芯配线单元':
            step_list, log_list, session['json_list'], line = calculate_two_back_back(shebei_dict['jiechushebei_radio'],shebei_dict['jierushebei_radio'], \
                                          shebei_dict['jiechushebei'],shebei_dict['jierushebei'],shebei_dict['shebei_count'])
            return render_template('step_two_back.html', shebei_dict=shebei_dict2, step_list=step_list, log_list=log_list, line=line)
        elif shebei_dict['jiechushebei_side'] == '72芯配线单元' and shebei_dict['jierushebei_side'] == '96芯设备单元':
            step_list, log_list, session['json_list'], line = calculate_two_back_front(shebei_dict['jiechushebei_radio'],shebei_dict['jierushebei_radio'], \
                                                                                 shebei_dict['jiechushebei_slot_rows'],shebei_dict['jiechushebei_slot_cols'], \
                                                                                 shebei_dict['jierushebei_slot_rows'],shebei_dict['jierushebei_slot_cols'], \
                                                                                 shebei_dict['jiechushebei'],shebei_dict['jierushebei'],\
                                                                                 shebei_dict['shebei_count'])
            jieru_duankou = format_radio_96(shebei_dict2['jierushebei_radio'][1],
                                            shebei_dict2['jierushebei_radio'][2])
            return render_template('step_two_back_front.html', shebei_dict=shebei_dict2, step_list=step_list, log_list=log_list, line=line, jieru_duankou=jieru_duankou)
        elif shebei_dict['jiechushebei_side'] == '96芯设备单元' and shebei_dict['jierushebei_side'] == '72芯配线单元':
            step_list, log_list, session['json_list'], line = calculate_two_front_back(shebei_dict['jiechushebei_radio'],shebei_dict['jierushebei_radio'], \
                                          shebei_dict['jiechushebei_slot_rows'],shebei_dict['jiechushebei_slot_cols'],\
                                          shebei_dict['jierushebei_slot_rows'],shebei_dict['jierushebei_slot_cols'],\
                                          shebei_dict['jiechushebei'],shebei_dict['jierushebei'],\
                                          shebei_dict['shebei_count'])
            jiechu_duankou = format_radio_96(shebei_dict2['jiechushebei_radio'][1],
                                             shebei_dict2['jiechushebei_radio'][2])
            return render_template('step_two_front_back.html', shebei_dict=shebei_dict2, step_list=step_list, log_list=log_list, line=line, jiechu_duankou=jiechu_duankou)
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


@main.route('/step/save/<shebei_dict2>/<line>', methods=['GET', 'POST'])
def save(shebei_dict2, line):
    shebei_dict = eval(shebei_dict2)
    jiechu_jijia = shebei_dict['jiechushebei']
    jiechu_side = shebei_dict['jiechushebei_side']
    jiechu_slotnum = shebei_dict['jiechushebei_radio'][0]
    jiechu_row = shebei_dict['jiechushebei_radio'][1]
    jiechu_col = shebei_dict['jiechushebei_radio'][2]

    jieru_jijia = shebei_dict['jierushebei']
    jieru_side = shebei_dict['jierushebei_side']
    jieru_slotnum = shebei_dict['jierushebei_radio'][0]
    jieru_row = shebei_dict['jierushebei_radio'][1]
    jieru_col = shebei_dict['jierushebei_radio'][2]

    updated_time = datetime.now()
    if jiechu_side == '96芯设备单元':
        jiechu_slotname = 'H'+jiechu_slotnum
    else:
        jiechu_slotname = 'L'+PEIXIAN_DANYUAN[jiechu_slotnum]
    if jieru_jijia == '96芯设备单元':
        jieru_slotname = 'H'+jieru_slotnum
    else:
        jieru_slotname = 'L'+PEIXIAN_DANYUAN[jieru_slotnum]

    qidian = DuankouTable.query.filter_by(jiechu_jijia=jiechu_jijia,
                                           jiechu_side=jiechu_side,
                                           jiechu_slotnum=jiechu_slotnum,
                                           jiechu_row=jiechu_row,
                                           jiechu_col=jiechu_col).first()

    mubiao = DuankouTable.query.filter_by(jiechu_jijia=jieru_jijia,
                                           jiechu_side=jieru_side,
                                           jiechu_slotnum=jieru_slotnum,
                                           jiechu_row=jieru_row,
                                           jiechu_col=jieru_col).first()

    if not qidian:
        if mubiao:
            # 删除目标(2个)
            mubiao_jieru = DuankouTable.query.filter_by(jiechu_jijia=mubiao.jieru_jijia,
                                                        jiechu_side=mubiao.jieru_side,
                                                        jiechu_slotnum=mubiao.jieru_slotnum,
                                                        jiechu_row=mubiao.jieru_row,
                                                        jiechu_col=mubiao.jieru_col).first()
            db.session.delete(mubiao)
            db.session.delete(mubiao_jieru)

            # 删除日志
            db.session.add(Log(updated_time=updated_time,
                               type='删除跳纤',
                               content='删除' + jieru_jijia + jieru_side + jieru_slotname + '端口（' + format_duankou(jieru_side, jieru_row, jieru_col) + '）',
                               user_id=current_user.id))
            db.session.add(Log(updated_time=updated_time,
                               type='删除跳纤',
                               content='删除' + mubiao.jieru_jijia + mubiao.jieru_side + str(mubiao.jieru_slotnum) + '端口（' + format_duankou(mubiao.jieru_side, mubiao.jieru_row, mubiao.jieru_col) + '）',
                               user_id=current_user.id))

        # 新增跳纤
        db.session.add(DuankouTable(jiechu_jijia=jiechu_jijia,
                                    jiechu_side=jiechu_side,
                                    jiechu_slotnum=jiechu_slotnum,
                                    jiechu_row=jiechu_row,
                                    jiechu_col=jiechu_col,
                                    jieru_jijia=jieru_jijia,
                                    jieru_side=jieru_side,
                                    jieru_slotnum=jieru_slotnum,
                                    jieru_row=jieru_row,
                                    jieru_col=jieru_col,
                                    line=line,
                                    updated_time=updated_time,
                                    username=current_user.username))
        db.session.add(DuankouTable(jiechu_jijia=jieru_jijia,
                                    jiechu_side=jieru_side,
                                    jiechu_slotnum=jieru_slotnum,
                                    jiechu_row=jieru_row,
                                    jiechu_col=jieru_col,
                                    jieru_jijia=jiechu_jijia,
                                    jieru_side=jiechu_side,
                                    jieru_slotnum=jiechu_slotnum,
                                    jieru_row=jiechu_row,
                                    jieru_col=jiechu_col,
                                    line=line,
                                    updated_time=updated_time,
                                    username=current_user.username))

        db.session.add(Log(updated_time=updated_time,
                           type='新增跳纤',
                           content='新增从' + jiechu_jijia + jiechu_side + jiechu_slotname + '端口（' + format_duankou(jiechu_side, jiechu_row, jiechu_col) + '）' + \
                                   '到' + jieru_jijia + jieru_side + jieru_slotname + '端口（' + format_duankou(jieru_side, jieru_row, jieru_col) + '）',
                           user_id=current_user.id))
        db.session.add(Log(updated_time=updated_time,
                           type='新增跳纤',
                           content='新增从' + jieru_jijia + jieru_side + jieru_slotname + '端口（' + format_duankou(jieru_side, jieru_row, jieru_col) + '）' + \
                                   '到' + jiechu_jijia + jiechu_side + jiechu_slotname + '端口（' + format_duankou(jiechu_side, jiechu_row, jiechu_col) + '）',
                           user_id=current_user.id))
        db.session.commit()


    elif qidian:
        # 删除元目标
        original_mubiao = DuankouTable.query.filter_by(jiechu_jijia=qidian.jieru_jijia,
                                                       jiechu_side=qidian.jieru_side,
                                                       jiechu_slotnum=qidian.jieru_slotnum,
                                                       jiechu_row=qidian.jieru_row,
                                                       jiechu_col=qidian.jieru_col).first()

        db.session.delete(original_mubiao)

        # 删除日志
        db.session.add(Log(updated_time=updated_time,
                           type='删除跳纤',
                           content='删除' + qidian.jieru_jijia + qidian.jieru_side + str(qidian.jieru_slotnum) + '端口（' + format_duankou(qidian.jieru_side, qidian.jieru_row, qidian.jieru_col) + '）',
                           user_id=current_user.id))
        # 目标有连接
        if mubiao:
            # 删除目标(2个)
            mubiao_jieru = DuankouTable.query.filter_by(jiechu_jijia=mubiao.jieru_jijia,
                                                        jiechu_side=mubiao.jieru_side,
                                                        jiechu_slotnum=mubiao.jieru_slotnum,
                                                        jiechu_row=mubiao.jieru_row,
                                                        jiechu_col=mubiao.jieru_col).first()
            db.session.delete(mubiao)
            db.session.delete(mubiao_jieru)

            # 删除日志
            db.session.add(Log(updated_time=updated_time,
                               type='删除跳纤',
                               content='删除' + jieru_jijia + jieru_side + jieru_slotname + '端口（' + format_duankou(jieru_side, jieru_row, jieru_col) + '）',
                               user_id=current_user.id))
            db.session.add(Log(updated_time=updated_time,
                               type='删除跳纤',
                               content='删除' + mubiao.jieru_jijia + mubiao.jieru_side + mubiao.jieru_slotnum + '端口（' + format_duankou(mubiao.jieru_side, mubiao.jieru_row, mubiao.jieru_col) + '）',
                               user_id=current_user.id))

        # 更新跳纤
        qidian.jieru_jijia = jieru_jijia
        qidian.jieru_side = jieru_side
        qidian.jieru_slotnum = jieru_slotnum
        qidian.jieru_row = jieru_row
        qidian.jieru_col = jieru_col
        db.session.add(qidian)

        db.session.add(DuankouTable(jiechu_jijia=jieru_jijia,
                                    jiechu_side=jieru_side,
                                    jiechu_slotnum=jieru_slotnum,
                                    jiechu_row=jieru_row,
                                    jiechu_col=jieru_col,
                                    jieru_jijia=jiechu_jijia,
                                    jieru_side=jiechu_side,
                                    jieru_slotnum=jiechu_slotnum,
                                    jieru_row=jiechu_row,
                                    jieru_col=jiechu_col,
                                    line=line,
                                    updated_time=updated_time,
                                    username=current_user.username))

        # 写入日志
        db.session.add(Log(updated_time=updated_time,
                           type='修改跳纤',
                           content=jiechu_jijia+jiechu_side+jiechu_slotname+'端口（'+format_duankou(jiechu_side, jiechu_row, jiechu_col)+'）',
                           user_id=current_user.id))
        db.session.add(Log(updated_time=updated_time,
                           type='新增跳纤',
                           content='新增从' + jieru_jijia + jieru_side + jieru_slotname + '端口（' + format_duankou(jieru_side, jieru_row, jieru_col) + '）' + \
                                   '到' + jiechu_jijia + jiechu_side + jiechu_slotname + '端口（' + format_duankou(jiechu_side, jiechu_row, jiechu_col) + '）',
                           user_id=current_user.id))
        db.session.commit()

    return redirect(url_for('main.index'))


# 端口列表
@main.route('/interface', methods=['GET','POST'])
@login_required
def duankou():
    page = request.args.get('page', 1, type=int)
    pagination = DuankouTable.query.paginate(page, per_page=100, error_out=False)
    duankouTables = pagination.items

    if request.method == 'POST':
        if request.form["search"] == "搜索":
            jijiahao = request.form.get('jijiahao')
            side = request.form.get('side')
            slotnum = request.form.get('slotnum')
            status = request.form.get('status')

            if side == '72芯配线单元':
                if slotnum:
                    slotnum = PEIXIAN_DANYUAN[slotnum]
            pagination = DuankouTable.query.filter_by(jiechu_jijia='NONE').paginate(page, per_page=20, error_out=False)
            # if jijiahao:
            if status == '在用':
                duankouTables = DuankouTable.query.filter(DuankouTable.jiechu_jijia.like('%' + jijiahao + '%'), \
                                                          DuankouTable.jiechu_side==side, DuankouTable.jiechu_slotnum.like('%'+slotnum+'%')).all()
            elif status == '未用':
                if not jijiahao and not slotnum:
                    flash('搜索「未用」端口时必须输入「机架号」和「单元数」后搜索才生效')

    return render_template('duankou.html', duankouTables=duankouTables, pagination=pagination)


# 跳纤管理
@main.route('/', methods=['GET', 'POST'])
@login_required
def manage_jumping():
    page = request.args.get('page', 1, type=int)
    pagination = DuankouTable.query.paginate(page, per_page=100, error_out=False)
    duankouTables = pagination.items

    return render_template('manage_jumping.html', duankouTables=duankouTables, pagination=pagination)


# 删除跳纤
@main.route('/jumping/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_jumping(id):
    result = DuankouTable.query.filter_by(id=id).first()
    if result:
        jijiahao = result.jieru_jijia
        side = result.jieru_side
        slotnum = result.jieru_slotnum
        row = result.jieru_row
        col = result.jieru_col

        updated_time = datetime.now()

        db.session.delete(result)
        result2 = DuankouTable.query.filter_by(jiechu_jijia=jijiahao,
                                               jiechu_side=side,
                                               jiechu_slotnum=slotnum,
                                               jiechu_row=row,
                                               jiechu_col=col).first()
        db.session.add(Log(updated_time=updated_time,
                           type='删除跳纤',
                           content='删除' + jijiahao + side + str(slotnum) + '端口（' + format_duankou(side, row, col) + '）',
                           user_id=current_user.id))
        if result2:
            db.session.delete(result2)
            # 删除日志

            db.session.add(Log(updated_time=updated_time,
                               type='删除跳纤',
                               content='删除' + result2.jiechu_jijia + result2.jiechu_side + str(result2.jiechu_slotnum) + '端口（' + format_duankou(result2.jiechu_side, result2.jiechu_row, result2.jiechu_col) + '）',
                               user_id=current_user.id))
        db.session.commit()
    else:
        flash('删除失败')
    return redirect(url_for('main.manage_jumping'))


# 操作日志
@main.route('/log', methods=['GET', 'POST'])
@login_required
def log():
    page = request.args.get('page', 1, type=int)
    pagination = Log.query.paginate(page, per_page=100, error_out=False)
    LogTables = pagination.items

    return render_template('log.html', LogTables=LogTables, pagination=pagination)


# 删除跳纤日志
@main.route('/log/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_log(id):
    result = Log.query.filter_by(id=id).first()
    if result:
        db.session.delete(result)
        db.session.commit()
    else:
        flash('删除失败')
    return redirect(url_for('main.log'))


@main.route('/setting', methods=['GET', 'POST'])
@login_required
def setting():
    # if current_user.role.id == '2':
    #     flash('无权')
    form = SettingForm()
    form.company_name.render_kw = {'class': 'form-control'}
    form.company_address.render_kw = {'class': 'form-control'}
    form.company_tel.render_kw = {'class': 'form-control'}
    form.line_name.render_kw = {'class': 'form-control'}
    form.line.render_kw = {'class': 'form-control'}
    form.line_color.render_kw = {'class': 'form-control demo',
                                 'data-control': 'hue'}
    form.line_place.render_kw = {'class': 'form-control'}
    form.kuapai_buchang.render_kw = {'class': 'form-control'}


    lineTables = LineTable.query.all()
    companyTables = CompanyTable.query.all()

    if request.method == 'POST':
        if 'save_company' in request.form:
            company_name = form.company_name.data
            company_address = form.company_address.data
            company_tel = form.company_tel.data
            if not companyTables:
                print('this way')
                db.session.add(CompanyTable(company_name=company_name,
                                            company_address=company_address,
                                            company_tel=company_tel))
                db.session.commit()
            else:
                print(company_name,company_address,company_tel)
                companyTables[0].company_name = company_name
                companyTables[0].company_address = company_address
                companyTables[0].company_tel = company_tel
                db.session.add(companyTables[0])
                db.session.commit()
            return  redirect(url_for('main.setting'))

        elif 'add_xiancai' in request.form:
            line_name = form.line_name.data
            line = form.line.data
            line_color = form.line_color.data
            line_place = form.line_place.data

            if line_name != '' and line != '' and line_color != '' and line_place != '':
                if not isinstance(line, int):
                    flash('线材长度必须输入整数')
                else:
                    if LineTable.query.filter_by(line_name=line_name).first():
                        flash(line_name+'已存在，请删除后重新添加')
                    elif LineTable.query.filter_by(line=line).first():
                        flash(str(line)+'米长的线材已存在，请删除后重新添加')
                    else:
                        db.session.add(LineTable(line_name=line_name,
                                                 line=line,
                                                 line_color=line_color,
                                                 line_place=line_place))
                        db.session.commit()
                return redirect(url_for('main.setting'))

    if companyTables:
        form.company_name.data = companyTables[0].company_name
        form.company_address.data = companyTables[0].company_address
        form.company_tel.data = companyTables[0].company_tel
    return  render_template('setting.html', form=form, lineTables=lineTables, companyTables=companyTables)


# 删除setting的线材
@main.route('/setting/line/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_line(id):
    result = LineTable.query.filter_by(id=id).first()
    if result:
        db.session.delete(result)
        db.session.commit()
    else:
        flash('删除失败')
    return redirect(url_for('main.setting'))
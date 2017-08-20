# 网线长度 1m=100cm 1cm=10mm
CABLE_LENGTH = [1500, 2000, 3000, 5000, 8000, 10000, 12000] #mm

# 挂纤轮本身直径
WHEEL = 103

# 13个挂纤轮底部圆弧到底部的距离，每个间距228
WHEEL_DISTANCE = [3044, 2816, 2588, 2363, 2135, 1907, 1679, 1451, 1223, 995, 767, 539, 311]
# WHEEL_DISTANCE = {
#     '1': 3150,
#     '2': 2922,
#     '3': 2694,
#     '4': 2466,
#     '5': 2238,
#     '6': 2010,
#     '7': 1782,
#     '8': 1554,
#     '9': 1326,
#     '10': 1098,
#     '11': 870,
#     '12': 642,
#     '13': 414
# }

# 正面大线环1底边框到底部的距离（每块slot的border-bottom到底部距离）,每个间距340
BIGLINE_DISTANCE = {
    '1': 2886,
    '2': 2546,
    '3': 2206,
    '4': 1866,
    '5': 1526,
    '6': 1186,
    '7': 846,
    '8': 506,
    '9': 166
}

#大线环2底边框到底部距离，（每个大线环2之间340mm），（大线环1和大线环2之间83mm），（大线环2本身高度67mm）
BIGLINE2_DISTANCE = {
    '1': 2803,
    '2': 2463,
    '3': 2123,
    '4': 1783,
    '5': 1443,
    '6': 1103,
    '7': 763,
    '8': 423,
    '9': 83
}


# 组合线环底边框到底部距离，每个组合线环之间169mm，每4个之间相距527mm
COMBINATION_RING = {
    '1': 3017.5,
    '2': 2848.5,
    '3': 2679.5,
    '4': 2510.5,
    '5': 1983.5,
    '6': 1814.5,
    '7': 1645.5,
    '8': 1476.5,
    '9': 949.5,
    '10': 780.5,
    '11': 611.5,
    '12': 442.5
}


# 计算每块slot的端口数，用户template模板渲染
def calculate_slot(rows,cols,list):
    cols = range(1,cols+1)
    rows = range(1,rows+1)
    for r in rows:
        for c in cols:
            list.append((r,c))
    return list

# 计算同一设备、同side、正面，跳纤方式
def calculate_one_front_front(jiechushebei_radio,jierushebei_radio, \
                              jiechushebei_slot_rows,jiechushebei_slot_cols, \
                              jierushebei_slot_rows,jierushebei_slot_cols, \
                              jiechushebei,jierushebei):
    step_list = []
    log_list = []
    json_list = ['front_front']
    if int(jierushebei_radio[0]) <= int(jierushebei_radio[0]):
        if int(jiechushebei_radio[2]) > int(jierushebei_radio[2]):
            from_point = jierushebei_radio
            to_point = jiechushebei_radio
            from_slot_rows = jierushebei_slot_rows
            from_slot_cols = jierushebei_slot_cols
            to_slot_rows = jiechushebei_slot_rows
            to_slot_cols = jiechushebei_slot_cols
            from_name = jierushebei
            to_name = jiechushebei
        else:
            from_point = jiechushebei_radio
            to_point = jierushebei_radio
            from_slot_rows = jiechushebei_slot_rows
            from_slot_cols = jiechushebei_slot_cols
            to_slot_rows = jierushebei_slot_rows
            to_slot_cols = jierushebei_slot_cols
            from_name = jiechushebei
            to_name = jierushebei
        print('from_point'+str(from_point))
        print('to_point'+str(to_point))
        json_list.append(from_point)  # [1]
        json_list.append(from_point[0])  # [2]
        # 1. 先往下走到小线环
        distance_step_1 = (len(from_slot_rows) - int(from_point[1]) + 1) * 35
        print('1. 先从'+from_name+'的#'+from_point[0]+'('+from_point[1]+','+from_point[2]+')'+'端口出来往下经过下方最近的8位小线环:' + str(distance_step_1))
        log_list.append('1. 先从'+from_name+'的#'+from_point[0]+'('+from_point[1]+','+from_point[2]+')'+'端口出来往下经过下方最近的8位小线环。')
        pic_step1 = (215+(int(from_point[2])-1)*17, 290+(int(from_point[0])-1)*320+(int(from_point[1])-1)*35)
        pic_step2 = (pic_step1[0], pic_step1[1]+35*(5-int(from_point[1])))
        step_list.append(pic_step1)
        step_list.append(pic_step2)
        print('pic_step1:'+str(pic_step1))
        print('pic_step2:'+str(pic_step2))

        # 2. 往右穿过中线环，最后一个端口到slot边框/中线环是26mm，（到大线环1左边框是99mm，）,从中线环顶边到大线环2底边是190mm
        if int(from_point[2]) < 12 :
            distance_step_2 = (len(from_slot_cols) - int(from_point[2])) * 18 + 12 + 26 + 190
        else:
            distance_step_2 = (len(from_slot_cols) - int(from_point[2])) * 18 + 26 + 190
        print('2. 再经过中线环到大线环2:' + str(distance_step_2))
        log_list.append('2. 往右穿过中线环再到大线环2。')
        pic_step3 = (pic_step2[0]+distance_step_2-190,pic_step2[1])
        pic_step4 = (pic_step3[0]+80,pic_step3[1]+90)
        step_list.append(pic_step3)
        step_list.append(pic_step4)
        print(pic_step3)
        print(pic_step4)

        # 3. 往下走直到侧面最下面那个挂纤轮调头向上走
        bigline2_distance = BIGLINE2_DISTANCE[from_point[0]] #正面第几个slot大线环2到底部的距离
        wheel_distance = WHEEL_DISTANCE[-1] #最后一个挂纤轮到底部的距离
        distance_step_3 = abs(bigline2_distance - wheel_distance)
        print('3. 从大线环2出去，向下直到侧面最下面那个挂纤轮：' + str(distance_step_3))
        log_list.append('3. 从大线环2出去，向下直到侧面最下面那个挂纤轮。')
        pic_step5 = (240,550+(int(from_point[0])-1)*320)
        pic_step6 = (280,550+(int(from_point[0])-1)*320)
        pic_step7 = (650,2930)
        pic_step8 = []
        step_list.append(pic_step5)
        step_list.append(pic_step6)
        step_list.append(pic_step7)
        step_list.append(pic_step8)
        print('pic_step5'+str(pic_step5))
        print('pic_step6'+str(pic_step6))
        print('pic_step7'+str(pic_step7))
        # 这里多余长度绕圈
        log_list.append('[3]')
        log_list.append('[4]')
        json_list.append('[3]')

        # 4. 调头向上进入端口所在slot的大线环2
        distance_step_4 = BIGLINE2_DISTANCE[to_point[0]] - WHEEL_DISTANCE[-1]
        if distance_step_4 >= 0:
            print('调头向上进入端口所在slot的大线环2:' + str(distance_step_4))
            pic_step9 = (670,550+(int(to_point[0])-1)*320)
            step_list.append(pic_step9)
            log_list.append('5. 调头向上进入'+to_name+'#'+to_point[0]+'的大线环2。')
            print('pic_step9'+str(pic_step9))
        else:
            distance_step_4 = WHEEL_DISTANCE[-1] - BIGLINE2_DISTANCE[to_point[0]]
            print('继续向下进入最下面那个大线环2:' + str(distance_step_4))
            log_list.append('5. 继续向下进入最下面那个大线环2')
            pic_step9 = (230,3120)
            step_list.append(pic_step9)
            print('pic_step9'+str(pic_step9))
        json_list.append(to_point[0])  # [4]

        # 6. 往左进入slot的中线环，进入该端口邻近的8位小线环
        if int(to_point[2]) < 12 :
            distance_step_6 = (len(to_slot_cols) - int(to_point[2])) * 18 + 12 + 26 + 190
        else:
            distance_step_6 = (len(to_slot_cols) - int(to_point[2])) * 18 + 26 + 190
        print('6. 往左进入slot的中线环，进入该端口邻近的8位小线环:' + str(distance_step_6))
        log_list.append('6. 从大线环2出来后，往左进入'+to_name+'#'+to_point[0]+'的中线环，并将线嵌入与'+to_point[2]+'列相近的小线环。') #[6]
        pic_step10 = (215+(int(to_point[2])-1)*17, 290+(int(to_point[0])-1)*320+(int(to_point[1])-1)*35)
        pic_step11 = (pic_step10[0] , pic_step10[1]+35*(5-int(to_point[1])))
        pic_step12 = (pic_step11[0]+distance_step_6-190,pic_step11[1])
        pic_step13 = (pic_step12[0]+80,pic_step12[1]+90)
        step_list.append(pic_step10)
        step_list.append(pic_step11)
        step_list.append(pic_step12)
        step_list.append(pic_step13)
        print('pic_step13'+str(pic_step13))
        print('pic_step12'+str(pic_step12))
        print('pic_step11'+str(pic_step11))
        print('pic_step10'+str(pic_step10))

        # 7. 往上插入端口
        distance_step_7 = (len(to_slot_rows) - int(to_point[1]) + 1) * 35
        print('往上插入端口:' + str(distance_step_7))
        log_list.append('7. 最后往上将线插入'+to_name+'#'+to_point[0]+'('+to_point[1]+','+to_point[2]+')端口。') #[7]
        used_distance = distance_step_1+distance_step_2+distance_step_3+distance_step_4+distance_step_6+distance_step_7
        print('总共需要线长：' + str(used_distance))
        json_list.append(to_point)  # [5]

        remaining_cable = 0
        cable_list = []
        for cable in CABLE_LENGTH:
            if cable > used_distance:
                # print('网线：'+ str(cable))
                cable_list.append(cable)
                raoquan_xianchang = (cable - used_distance)/328
                if (int(raoquan_xianchang))%2 == 0:
                    print('绕选网线：' + str(cable))
                    log_list[3] = '请选择一根长度为：' + str(int(cable/1000)) + '米的网线。'
                    print(raoquan_xianchang)
                    cegualun_raoguo_geshu = int(int(raoquan_xianchang)/2+1)
                    if cegualun_raoguo_geshu == 1:
                        raoquan_real_changdu = 0
                        print('不用再侧面绕圈')
                        log_list[4] = '4. 绕过侧面最下面那个挂纤轮。'
                        pic_step8_1 = ('','')
                        pic_step8_2 = ('','')
                        pic_step8_3 = ('','')
                        pic_step8_4 = ('','')
                        pic_step8_5 = ('','')
                        step8_list = []
                        step8_list.append(pic_step8_1)
                        step8_list.append(pic_step8_2)
                        step8_list.append(pic_step8_3)
                        step8_list.append(pic_step8_4)
                        step8_list.append(pic_step8_5)
                        step_list[7] = step8_list
                        json_list[3] = ['13']
                    elif cegualun_raoguo_geshu > 13 :
                        print('从侧面最下面那个挂纤轮开始经过13个侧挂轮绕1圈')
                        print('再从侧面最下面那个挂纤轮开始经过'+str(cegualun_raoguo_geshu-1-12+1)+'个侧挂轮绕1圈')
                        log_list[4] = '4. 从侧面最下面那个挂纤轮开始经过13个侧挂轮绕1圈。<br />再从侧面最下面那个挂纤轮开始经过'+str(cegualun_raoguo_geshu-1-12+1)+'个侧挂轮绕1圈。'
                        raoquan_real_changdu = 12 * 2 * 328 + (cegualun_raoguo_geshu-1-12) * 2 * 328
                        pic_step8_1 = (650,240)
                        pic_step8_2 = (530,240)
                        pic_step8_3 = (530,2950)
                        pic_step8_4 = (670,2950)
                        pic_step8_5 = (670,(2950-(cegualun_raoguo_geshu-1-12)*215)-110-20)
                        step8_list = []
                        step8_list.append(pic_step8_1)
                        step8_list.append(pic_step8_2)
                        step8_list.append(pic_step8_3)
                        step8_list.append(pic_step8_4)
                        step8_list.append(pic_step8_5)
                        step_list[7] = step8_list
                        json_list[3] = ['13', '1', '13', str(13-(cegualun_raoguo_geshu-1-12+1)+1), '13']
                    else:
                        raoquan_real_changdu = (cegualun_raoguo_geshu - 1 ) * 2 * 328
                        print('从侧面最下面那个挂纤轮开始经过'+str(cegualun_raoguo_geshu)+'个侧挂轮绕1圈')
                        log_list[4] = '4. 从侧面最下面那个挂纤轮开始经过'+str(cegualun_raoguo_geshu)+'个侧挂轮绕1圈。'
                        pic_step8_1 = ('','')
                        pic_step8_2 = ('','')
                        pic_step8_3 = ('','')
                        pic_step8_4 = ('','')
                        pic_step8_5 = (650,(2930-(cegualun_raoguo_geshu-1)*215)-110)
                        step8_list = []
                        step8_list.append(pic_step8_1)
                        step8_list.append(pic_step8_2)
                        step8_list.append(pic_step8_3)
                        step8_list.append(pic_step8_4)
                        step8_list.append(pic_step8_5)
                        step_list[7] = step8_list
                        json_list[3] = ['13', str(13-cegualun_raoguo_geshu+1), '13']
                    remaining_cable = cable - used_distance - raoquan_real_changdu
                    print('剩余线长：' + str(remaining_cable))
                    # print(int(raoquan_xianchang)*328)
                    # print(raoquan_real_changdu)
                    break
        if remaining_cable == 0:
            cable = cable_list[0]
            raoquan_xianchang = (cable - used_distance)/328
            if (int(raoquan_xianchang)-1)%2 == 0:
                print('绕选网线：' + str(cable))
                log_list[3] = '请选择一根长度为：' + str(int(cable/1000)) + '米的网线。'
                print(raoquan_xianchang)
                cegualun_raoguo_geshu = int((int(raoquan_xianchang)-1)/2+1)
                if cegualun_raoguo_geshu == 1:
                    raoquan_real_changdu = 0
                    print('不用再侧面绕圈')
                    log_list[4] = '4. 绕过侧面最下面那个挂纤轮。'
                    pic_step8_1 = ('','')
                    pic_step8_2 = ('','')
                    pic_step8_3 = ('','')
                    pic_step8_4 = ('','')
                    pic_step8_5 = ('','')
                    step8_list = []
                    step8_list.append(pic_step8_1)
                    step8_list.append(pic_step8_2)
                    step8_list.append(pic_step8_3)
                    step8_list.append(pic_step8_4)
                    step8_list.append(pic_step8_5)
                    step_list[7] = step8_list
                elif cegualun_raoguo_geshu > 13 :
                    print('从侧面最下面那个挂纤轮开始经过13个侧挂轮绕1圈')
                    print('再从侧面最下面那个挂纤轮开始经过'+str(cegualun_raoguo_geshu-1-12+1)+'个侧挂轮绕1圈')
                    log_list[4] = '4. 从侧面最下面那个挂纤轮开始经过13个侧挂轮绕1圈。<br />再从侧面最下面那个挂纤轮开始经过'+str(cegualun_raoguo_geshu-1-12+1)+'个侧挂轮绕1圈。'
                    raoquan_real_changdu = 12 * 2 * 328 + (cegualun_raoguo_geshu-1-12) * 2 * 328
                    pic_step8_1 = (650,240)
                    pic_step8_2 = (530,240)
                    pic_step8_3 = (530,2950)
                    pic_step8_4 = (670,2950)
                    pic_step8_5 = (670,(2950-(cegualun_raoguo_geshu-1-12)*215)-110-20)
                    step8_list = []
                    step8_list.append(pic_step8_1)
                    step8_list.append(pic_step8_2)
                    step8_list.append(pic_step8_3)
                    step8_list.append(pic_step8_4)
                    step8_list.append(pic_step8_5)
                    step_list[7] = step8_list
                else:
                    raoquan_real_changdu = (cegualun_raoguo_geshu - 1 ) * 2 * 328
                    print('从侧面最下面那个挂纤轮开始经过'+str(cegualun_raoguo_geshu)+'个侧挂轮绕1圈')
                    log_list[4] = '4. 从侧面最下面那个挂纤轮开始经过'+str(cegualun_raoguo_geshu)+'个侧挂轮绕1圈。'
                    pic_step8_1 = ('','')
                    pic_step8_2 = ('','')
                    pic_step8_3 = ('','')
                    pic_step8_4 = ('','')
                    pic_step8_5 = (650,(2930-(cegualun_raoguo_geshu-1)*215)-110)
                    step8_list = []
                    step8_list.append(pic_step8_1)
                    step8_list.append(pic_step8_2)
                    step8_list.append(pic_step8_3)
                    step8_list.append(pic_step8_4)
                    step8_list.append(pic_step8_5)
                    step_list[7] = step8_list
                remaining_cable = cable - used_distance - raoquan_real_changdu
                print('剩余线长：' + str(remaining_cable))
                # print(int(raoquan_xianchang)*328)
                # print(raoquan_real_changdu)
        print(step_list)
        return step_list, log_list, json_list


# 计算同一设备、同side、背面，跳纤方式
def calculate_one_back_back(jiechushebei_radio,jierushebei_radio, \
                              jiechushebei_slot_rows,jiechushebei_slot_cols, \
                              jierushebei_slot_rows,jierushebei_slot_cols, \
                              jiechushebei,jierushebei):
    log_list = ['']
    step_list = []
    json_list = []
    from_point = jiechushebei_radio
    to_point = jierushebei_radio
    from_slot_rows = jiechushebei_slot_rows
    from_slot_cols = jiechushebei_slot_cols
    to_slot_rows = jierushebei_slot_rows
    to_slot_cols = jierushebei_slot_cols
    from_name = jiechushebei
    to_name = jierushebei
    print('from_point'+str(from_point))
    print('to_point'+str(to_point))
    # 1. 先从第几排托盘往左出来
    distance_step_1 = 84 + 20.5 * (int(from_point[2])-1)
    print('1. 先从'+from_name+'的'+from_point[0]+'号72芯配线单元的('+str(from_point[1])+','+str(from_point[2])+')托盘出来:' + str(distance_step_1))
    log_list.append('1. 先从'+from_name+'的'+from_point[0]+'号72芯配线单元的('+str(from_point[1])+','+str(from_point[2])+')托盘出来:' )
    if int(from_point[0]) <= 4:
        pic_step1 = (325 + (int(from_point[2]) - 1) * 20, 205 + (int(from_point[0]) - 1) * 160 + (int(from_point[1]) - 1) * 25)
    elif int(from_point[0]) > 4 and int(from_point[0]) <= 8:
        pic_step1 = (325 + (int(from_point[2]) - 1) * 20, 205 + (int(from_point[0]) - 1) * 160 + (int(from_point[1]) - 1) * 25 +335)
    elif int(from_point[0]) > 8 and int(from_point[0]) <= 12:
        pic_step1 = (325 + (int(from_point[2]) - 1) * 20, 205 + (int(from_point[0]) - 1) * 160 + (int(from_point[1]) - 1) * 25 +335 * 2)
    pic_step2 = (250, pic_step1[1])
    step_list.append(pic_step1)
    step_list.append(pic_step2)
    print('pic_step1:'+str(pic_step1))
    print('pic_step2:'+str(pic_step2))

    # 2. 进入组合线环#XX中的小孔
    distance_step_2 = 34 + 26 * (6 - int(from_point[1]))
    print('2. 进入组合线环'+str(from_point[0])+'中的小孔:' + str(distance_step_2))
    log_list.append('2. 进入组合线环'+str(from_point[0])+'中的小孔。')
    if int(from_point[0]) <= 4:
        pic_step3 = (250, 400 + 160 * (int(from_point[0])-1))
    elif int(from_point[0]) > 4 and int(from_point[0]) <= 8:
        pic_step3 = (250, 400 + 160 * (int(from_point[0]) - 1) + 340)
    elif int(from_point[0]) > 8 and int(from_point[0]) <= 12:
        pic_step3 = (250, 400 + 160 * (int(from_point[0]) - 1) + 340 * 2)
    step_list.append(pic_step3)
    print('pic_step3'+str(pic_step3))

    # 3. 进入组合线环#XX+1的大孔
    if int(from_point[0]) < 12:
        distance_step_3 = 169  # 组合线环之间相距169mm
        print('3. 进入组合线环'+str(int(from_point[0])+1)+'中的大孔:'+str(distance_step_3))
        log_list.append('3. 进入组合线环'+str(int(from_point[0])+1)+'中的大孔。')
        if int(from_point[0]) <= 4:
            pic_step4 = (250, 400 + 160 * int(from_point[0]))
        elif int(from_point[0]) > 4 and int(from_point[0]) <= 8:
            pic_step4 = (250, 400 + 160 * int(from_point[0]) + 340)
        elif int(from_point[0]) > 8 and int(from_point[0]) <= 12:
            pic_step4 = (250, 400 + 160 * int(from_point[0]) + 340 * 2)
    elif int(from_point[0]) == 12:
        distance_step_3 = 0
        print('3. 不用进入下一个组合线环的大孔')
        log_list.append('')
        pic_step4 = ('', '')
    step_list.append(pic_step4)
    print('pic_step4:'+str(pic_step4))

    # 4. 往上至最上面的挂纤轮
    if int(from_point[0]) < 12 :
        distance_step_4 = WHEEL_DISTANCE[0] + WHEEL - COMBINATION_RING[str(int(from_point[0])+1)]
        log_list.append('4. 往上至侧面最上面的挂纤轮。')
    else:
        distance_step_4 = WHEEL_DISTANCE[0] + WHEEL - COMBINATION_RING[from_point[0]]
        log_list.append('3. 往上至侧面最上面的挂纤轮。')
    print('4. 往上至侧面最上面的挂纤轮:' + str(distance_step_4))



    # 5. 往下至最下面的挂纤轮
    distance_step_5 = WHEEL_DISTANCE[0] + WHEEL - WHEEL_DISTANCE[-1]
    print('5. 往下至最下面的挂纤轮:'+str(distance_step_5))
    if int(from_point[0]) < 12:
        log_list.append('5. 从最上面的挂纤轮往下至最下面的挂纤轮。')
    else:
        log_list.append('4. 从最上面的挂纤轮往下至最下面的挂纤轮。')

    # 6. 绕圈
    log_list.append('[6]')
    step_list.append('[4]')

    # 7. 调转方向向上进入to_point组合线环#XX+1的大孔
    if int(to_point[0]) < 12:
        distance_step_6 = COMBINATION_RING[str(int(to_point[0])+1)] - WHEEL_DISTANCE[-1]
        print('7. 调转方向向上进入组合线环'+str(int(to_point[0])+1)+'的大孔:'+str(distance_step_6))
        if int(from_point[0]) < 12:
            log_list.append('7. 调转方向向上进入组合线环'+str(int(to_point[0])+1)+'的大孔。')
        else:
            log_list.append('6. 调转方向向上进入组合线环' + str(int(to_point[0]) + 1) + '的大孔。')
        if int(to_point[0]) <= 4:
            pic_step5 = (1080, 340 + 160 * int(to_point[0]))
        elif int(to_point[0]) > 4 and int(to_point[0]) <= 8:
            pic_step5 = (1080, 340 + 160 * int(to_point[0]) + 340)
        elif int(to_point[0]) > 8 and int(to_point[0]) <= 12:
            pic_step5 = (1080, 340 + 160 * int(to_point[0]) + 340 * 2)
    elif int(to_point[0]) == 12:
        distance_step_6 = 0
        print('不用进入下一个组合线环的大孔')
        log_list.append('')
        pic_step5 = ('','')
    step_list.append(pic_step5)
    print('pic_step5:' + str(pic_step5))

    # 8. 再向上进入to_point组合线环#XX的小孔
    if int(to_point[0]) < 12 :
        distance_step_7 = COMBINATION_RING[to_point[0]] - COMBINATION_RING[str(int(to_point[0])+1)]
    else:
        distance_step_7 = COMBINATION_RING[to_point[0]] - WHEEL_DISTANCE[-1]
    if int(to_point[0]) <= 4:
        pic_step6 = (1080, 340 + 160 * (int(to_point[0]) - 1))
    elif int(to_point[0]) > 4 and int(to_point[0]) <= 8:
        pic_step6 = (1080, 340 + 160 * (int(to_point[0]) - 1) + 340)
    elif int(to_point[0]) > 8 and int(to_point[0]) <= 12:
        pic_step6 = (1080, 340 + 160 * (int(to_point[0]) - 1) + 340 * 2)
    step_list.append(pic_step6)
    print('pic_step6:'+str(pic_step6))
    print('8. 再向上进入组合线环'+str(to_point[0])+'的小孔:'+str(distance_step_7))
    if int(from_point[0]) < 12 and int(to_point[0]) < 12:
        log_list.append('8. 再向上进入组合线环'+str(to_point[0])+'的小孔。')
    elif int(from_point[0]) == 12 and int(to_point[0]) == 12:
        log_list.append('6. 再向上进入组合线环' + str(to_point[0]) + '的小孔。')
    else:
        log_list.append('7. 再向上进入组合线环' + str(to_point[0]) + '的小孔。')

    # 9. 往右进入指定托盘
    distance_step_8 = 34 + 26 * (6 - int(to_point[1])) + 84 + 20.5 * (int(to_point[2])-1)
    print('9. 往右进入'+to_name+'的'+str(to_point[0])+'号72芯配线单元的('+str(to_point[1])+','+str(to_point[2])+')托盘:'+str(distance_step_8))
    log_list.append('从组合线环的小孔出来后往右进入'+to_name+'的'+str(to_point[0])+'号72芯配线单元的('+str(to_point[1])+','+str(to_point[2])+')托盘。')

    if int(to_point[0]) <= 4:
        pic_step9 = (250, 400 + 160 * (int(to_point[0])-1))
        pic_step11 = (325 + (int(to_point[2]) - 1) * 20, 205 + (int(to_point[0]) - 1) * 160 + (int(to_point[1]) - 1) * 25)
    elif int(to_point[0]) > 4 and int(to_point[0]) <= 8:
        pic_step9 = (250, 400 + 160 * (int(to_point[0]) - 1) + 340)
        pic_step11 = (325 + (int(to_point[2]) - 1) * 20, 205 + (int(to_point[0]) - 1) * 160 + (int(to_point[1]) - 1) * 25 + 335)
    elif int(to_point[0]) > 8 and int(to_point[0]) <= 12:
        pic_step9 = (250, 400 + 160 * (int(to_point[0]) - 1) + 340 * 2)
        pic_step11 = (325 + (int(to_point[2]) - 1) * 20, 205 + (int(to_point[0]) - 1) * 160 + (int(to_point[1]) - 1) * 25 + 335 * 2)
    pic_step10 = (250, pic_step11[1])
    step_list.append(pic_step9)
    step_list.append(pic_step10)
    step_list.append(pic_step11)
    print('pic_step9:'+str(pic_step9))
    print('pic_step10:'+str(pic_step10))
    print('pic_step11:'+str(pic_step11))

    print(log_list)


    used_distance = distance_step_1 + distance_step_2 + distance_step_3 + distance_step_4 + \
                    distance_step_5 + distance_step_6 + distance_step_7 + distance_step_8
    print('总共需要线长：' + str(used_distance))

    remaining_cable = 0
    cable_list = []
    for cable in CABLE_LENGTH:
        if cable > used_distance:
            # print('网线：'+ str(cable))
            cable_list.append(cable)
            raoquan_xianchang = (cable - used_distance) / 328
            if (int(raoquan_xianchang)) % 2 == 0:
                print('绕选网线：' + str(cable))
                log_list[0] = '请选择一根长度为：' + str(int(cable / 1000)) + '米的网线。'
                print(raoquan_xianchang)
                cegualun_raoguo_geshu = int(int(raoquan_xianchang) / 2 + 1)
                if cegualun_raoguo_geshu == 1:
                    raoquan_real_changdu = 0
                    print('不用再侧面绕圈')
                    if int(from_point[0]) < 12:
                        log_list[6] = '6. 绕过侧面最下面那个挂纤轮。'
                    else:
                        log_list[6] = '5. 绕过侧面最下面那个挂纤轮。'
                    pic_step8_1 = ('', '')
                    pic_step8_2 = ('', '')
                    pic_step8_3 = ('', '')
                    pic_step8_4 = ('', '')
                    pic_step8_5 = ('', '')
                    step8_list = []
                    step8_list.append(pic_step8_1)
                    step8_list.append(pic_step8_2)
                    step8_list.append(pic_step8_3)
                    step8_list.append(pic_step8_4)
                    step8_list.append(pic_step8_5)
                    step_list[4] = step8_list
                    # json_list[3] = ['13']
                elif cegualun_raoguo_geshu > 13:
                    print('从侧面最下面那个挂纤轮开始经过13个侧挂轮绕1圈')
                    print('再从侧面最下面那个挂纤轮开始经过' + str(cegualun_raoguo_geshu - 1 - 12 + 1) + '个侧挂轮绕1圈')
                    # log_list[4] = '4. 从侧面最下面那个挂纤轮开始经过13个侧挂轮绕1圈。<br />再从侧面最下面那个挂纤轮开始经过' + str(cegualun_raoguo_geshu - 1 - 12 + 1) + '个侧挂轮绕1圈。'
                    raoquan_real_changdu = 12 * 2 * 328 + (cegualun_raoguo_geshu - 1 - 12) * 2 * 328
                    # pic_step8_1 = (650, 240)
                    # pic_step8_2 = (530, 240)
                    # pic_step8_3 = (530, 2950)
                    # pic_step8_4 = (670, 2950)
                    # pic_step8_5 = (670, (2950 - (cegualun_raoguo_geshu - 1 - 12) * 215) - 110 - 20)
                    # step8_list = []
                    # step8_list.append(pic_step8_1)
                    # step8_list.append(pic_step8_2)
                    # step8_list.append(pic_step8_3)
                    # step8_list.append(pic_step8_4)
                    # step8_list.append(pic_step8_5)
                    # step_list[7] = step8_list
                    # json_list[3] = ['13', '1', '13', str(13 - (cegualun_raoguo_geshu - 1 - 12 + 1) + 1), '13']
                else:
                    raoquan_real_changdu = (cegualun_raoguo_geshu - 1) * 2 * 328
                    print('从侧面最下面那个挂纤轮开始经过' + str(cegualun_raoguo_geshu) + '个侧挂轮绕1圈')
                    if int(from_point[0]) < 12:
                        log_list[6] = '6. 从侧面最下面那个挂纤轮开始经过' + str(cegualun_raoguo_geshu) + '个挂纤轮绕1圈。'
                    else:
                        log_list[6] = '5. 从侧面最下面那个挂纤轮开始经过' + str(cegualun_raoguo_geshu) + '个挂纤轮绕1圈。'
                    pic_step8_1 = ('', '')
                    pic_step8_2 = ('', '')
                    pic_step8_3 = ('', '')
                    pic_step8_4 = ('', '')
                    pic_step8_5 = (650, (2930 - (cegualun_raoguo_geshu - 1) * 215) - 110)
                    step8_list = []
                    step8_list.append(pic_step8_1)
                    step8_list.append(pic_step8_2)
                    step8_list.append(pic_step8_3)
                    step8_list.append(pic_step8_4)
                    step8_list.append(pic_step8_5)
                    step_list[4] = step8_list
                    # json_list[3] = ['13', str(13 - cegualun_raoguo_geshu + 1), '13']
                remaining_cable = cable - used_distance - raoquan_real_changdu
                print('剩余线长：' + str(remaining_cable))
                # print(int(raoquan_xianchang)*328)
                # print(raoquan_real_changdu)
                break
    if remaining_cable == 0:
        cable = cable_list[0]
        raoquan_xianchang = (cable - used_distance) / 328
        if (int(raoquan_xianchang) - 1) % 2 == 0:
            print('绕选网线：' + str(cable))
            # log_list[3] = '请选择一根长度为：' + str(int(cable / 1000)) + '米的网线。'
            print(raoquan_xianchang)
            cegualun_raoguo_geshu = int((int(raoquan_xianchang) - 1) / 2 + 1)
            if cegualun_raoguo_geshu == 1:
                raoquan_real_changdu = 0
                print('不用再侧面绕圈')
                if int(from_point[0]) < 12:
                    log_list[6] = '6. 绕过侧面最下面那个挂纤轮。'
                else:
                    log_list[6] = '5. 绕过侧面最下面那个挂纤轮。'
                pic_step8_1 = ('', '')
                pic_step8_2 = ('', '')
                pic_step8_3 = ('', '')
                pic_step8_4 = ('', '')
                pic_step8_5 = ('', '')
                step8_list = []
                step8_list.append(pic_step8_1)
                step8_list.append(pic_step8_2)
                step8_list.append(pic_step8_3)
                step8_list.append(pic_step8_4)
                step8_list.append(pic_step8_5)
                step_list[4] = step8_list
            elif cegualun_raoguo_geshu > 13:
                print('从侧面最下面那个挂纤轮开始经过13个侧挂轮绕1圈')
                print('再从侧面最下面那个挂纤轮开始经过' + str(cegualun_raoguo_geshu - 1 - 12 + 1) + '个侧挂轮绕1圈')
                # log_list[4] = '4. 从侧面最下面那个挂纤轮开始经过13个侧挂轮绕1圈。<br />再从侧面最下面那个挂纤轮开始经过' + str(cegualun_raoguo_geshu - 1 - 12 + 1) + '个侧挂轮绕1圈。'
                raoquan_real_changdu = 12 * 2 * 328 + (cegualun_raoguo_geshu - 1 - 12) * 2 * 328
                # pic_step8_1 = (650, 240)
                # pic_step8_2 = (530, 240)
                # pic_step8_3 = (530, 2950)
                # pic_step8_4 = (670, 2950)
                # pic_step8_5 = (670, (2950 - (cegualun_raoguo_geshu - 1 - 12) * 215) - 110 - 20)
                # step8_list = []
                # step8_list.append(pic_step8_1)
                # step8_list.append(pic_step8_2)
                # step8_list.append(pic_step8_3)
                # step8_list.append(pic_step8_4)
                # step8_list.append(pic_step8_5)
                # step_list[7] = step8_list
            else:
                raoquan_real_changdu = (cegualun_raoguo_geshu - 1) * 2 * 328
                print('从侧面最下面那个挂纤轮开始经过' + str(cegualun_raoguo_geshu) + '个侧挂轮绕1圈')
                if int(from_point[0]) < 12:
                    log_list[6] = '6. 从侧面最下面那个挂纤轮开始经过' + str(cegualun_raoguo_geshu) + '个挂纤轮绕1圈。'
                else:
                    log_list[6] = '5. 从侧面最下面那个挂纤轮开始经过' + str(cegualun_raoguo_geshu) + '个挂纤轮绕1圈。'
                pic_step8_1 = ('', '')
                pic_step8_2 = ('', '')
                pic_step8_3 = ('', '')
                pic_step8_4 = ('', '')
                pic_step8_5 = (650, (2930 - (cegualun_raoguo_geshu - 1) * 215) - 110)
                step8_list = []
                step8_list.append(pic_step8_1)
                step8_list.append(pic_step8_2)
                step8_list.append(pic_step8_3)
                step8_list.append(pic_step8_4)
                step8_list.append(pic_step8_5)
                step_list[4] = step8_list
            remaining_cable = cable - used_distance - raoquan_real_changdu
            print('剩余线长：' + str(remaining_cable))
    print(step_list)
    return step_list, log_list, json_list
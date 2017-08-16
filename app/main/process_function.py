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
                              jierushebei_slot_rows,jierushebei_slot_cols):
    step_list = []
    if int(jierushebei_radio[0]) <= int(jierushebei_radio[0]):
        if int(jiechushebei_radio[2]) > int(jierushebei_radio[2]):
            from_point = jierushebei_radio
            to_point = jiechushebei_radio
            from_slot_rows = jierushebei_slot_rows
            from_slot_cols = jierushebei_slot_cols
            to_slot_rows = jiechushebei_slot_rows
            to_slot_cols = jiechushebei_slot_cols
        else:
            from_point = jiechushebei_radio
            to_point = jierushebei_radio
            from_slot_rows = jiechushebei_slot_rows
            from_slot_cols = jiechushebei_slot_cols
            to_slot_rows = jierushebei_slot_rows
            to_slot_cols = jierushebei_slot_cols
        print('from_point'+str(from_point))
        print('to_point'+str(to_point))
        # 1. 先往下走到小线环
        distance_step_1 = (len(from_slot_rows) - int(from_point[1]) + 1) * 35
        print('1. 先从from_point端口出来往下经过下方最近的8位小线环:' + str(distance_step_1))
        pic_step1 = (215+(int(from_point[2])-1)*17 , 290+(int(from_point[0])-1)*320+(int(from_point[1])-1)*35)
        pic_step2 = (pic_step1[0] , pic_step1[1]+35*(5-int(from_point[1])))
        step_list.append(pic_step1)
        step_list.append(pic_step2)
        print(pic_step1)
        print(pic_step2)

        # 2. 往右穿过中线环，最后一个端口到slot边框/中线环是26mm，（到大线环1左边框是99mm，）,从中线环顶边到大线环2底边是190mm
        if int(from_point[2]) < 12 :
            distance_step_2 = (len(from_slot_cols) - int(from_point[2])) * 18 + 12 + 26 + 190
        else:
            distance_step_2 = (len(from_slot_cols) - int(from_point[2])) * 18 + 26 + 190
        print('2. 再经过中线环到大线环2:' + str(distance_step_2))
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

        # 4. 调头向上进入端口所在slot的大线环2
        distance_step_4 = BIGLINE2_DISTANCE[to_point[0]] - WHEEL_DISTANCE[-1]
        if distance_step_4 >= 0:
            print('调头向上进入端口所在slot的大线环2:' + str(distance_step_4))
            pic_step9 = (670,550+(int(to_point[0])-1)*320)
            step_list.append(pic_step9)
            print('pic_step9'+str(pic_step9))
        else:
            distance_step_4 = WHEEL_DISTANCE[-1] - BIGLINE2_DISTANCE[to_point[0]]
            print('继续向下进入最下面那个大线环2')
            pic_step9 = (230,3120)
            step_list.append(pic_step9)
            print('pic_step9'+str(pic_step9))
        # 6. 往左进入slot的中线环，进入该端口邻近的8位小线环
        if int(to_point[2]) < 12 :
            distance_step_6 = (len(to_slot_cols) - int(to_point[2])) * 18 + 12 + 26 + 190
        else:
            distance_step_6 = (len(to_slot_cols) - int(to_point[2])) * 18 + 26 + 190
        print('往左进入slot的中线环，进入该端口邻近的8位小线环:' + str(distance_step_6))
        # 7. 往上插入端口
        distance_step_7 = (len(to_slot_rows) - int(to_point[1]) + 1) * 35
        print('往上插入端口:' + str(distance_step_7))
        used_distance = distance_step_1+distance_step_2+distance_step_3+distance_step_4+distance_step_6+distance_step_7
        print('总共需要线长：' + str(used_distance))

        remaining_cable = 0
        cable_list = []
        for cable in CABLE_LENGTH:
            if cable > used_distance:
                # print('网线：'+ str(cable))
                cable_list.append(cable)
                raoquan_xianchang = (cable - used_distance)/328
                if (int(raoquan_xianchang))%2 == 0:
                    print('绕选网线：' + str(cable))
                    print(raoquan_xianchang)
                    cegualun_raoguo_geshu = int(int(raoquan_xianchang)/2+1)
                    if cegualun_raoguo_geshu == 1:
                        raoquan_real_changdu = 0
                        print('不用再侧面绕圈')
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
                    break
        if remaining_cable == 0:
            cable = cable_list[0]
            raoquan_xianchang = (cable - used_distance)/328
            if (int(raoquan_xianchang)-1)%2 == 0:
                print('绕选网线：' + str(cable))
                print(raoquan_xianchang)
                cegualun_raoguo_geshu = int((int(raoquan_xianchang)-1)/2+1)
                if cegualun_raoguo_geshu == 1:
                    raoquan_real_changdu = 0
                    print('不用再侧面绕圈')
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
        return step_list
    # elif int(jierushebei_radio[0]) > int(jierushebei_radio[0]):
    #     print('暂不支持！')
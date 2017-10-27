from ..models import DuankouTable

import xlsxwriter
import time, os


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

def str_len(str):
    try:
        row_l=len(str)
        utf8_l=len(str.encode('utf-8'))
        return (utf8_l-row_l)/2+row_l
    except:
        return row_l
    return row_l


# format 时间
def format_time(t):
    t = t.strftime("%Y-%m-%d")
    return t


# format 审核
def format_confirm(confirm):
    if confirm:
        return '已确认'
    else:
        return '未确认'


# format 单元号，如果是96的 => H1; 72 => L12
def format_slotnum(side, slotnum):
    if side == '72芯配线单元':
        return 'L' + str(PEIXIAN_DANYUAN[str(slotnum)])
    elif side == '96芯设备单元':
        return 'H' + str(slotnum)

# format 端口号，96 => (2) 72 => (1,2)
def format_duankou(side, row, col):
    if side == '96芯设备单元':
        return '('+ str(1 + 24 * (row-1) + (col - 1)) + ')'
    elif side == '72芯配线单元':
        return '(' + str(row) + ',' + str(col) + ')'


def export_excel_jumping(exportdir):
    localtime = time.strftime("%Y-%m-%d", time.localtime())
    filename = localtime + ".xlsx"
    # return excel.make_response_from_query_sets(query_sets, column_names, "xls", file_name=filename, sheet_name="泵选型报价条目")

    workbook = xlsxwriter.Workbook(os.path.join(exportdir, filename))
    worksheet = workbook.add_worksheet()


    #设置第一行样式
    titleformat = workbook.add_format()
    titleformat.set_align('center') # 设置水平居中对齐
    titleformat.set_align('vcenter') # 设置垂直居中对齐
    titleformat.set_font_name('Arial')
    titleformat.set_font_size(10)
    titleformat.set_text_wrap() # 自动换行
    titleformat.set_bg_color('#FFFFFF')
    titleformat.set_top(1)
    titleformat.set_bottom(1)
    titleformat.set_left(1)
    titleformat.set_right(1)
    # 将titleformat应用在第一行，此行为标题
    worksheet.set_row(0, None, titleformat)

    #设置行样式
    rowsformat = workbook.add_format()
    rowsformat.set_align('center')
    rowsformat.set_align('vcenter')
    rowsformat.set_font_name('Arial')
    rowsformat.set_font_size(10)
    rowsformat.set_top(1)
    rowsformat.set_bottom(1)
    rowsformat.set_left(1)
    rowsformat.set_right(1)


    #写行首
    worksheet.write(0,0,'编号')
    worksheet.write(0,1,'时间')
    worksheet.write(0,2,'操作人员')
    worksheet.write(0,3,'接出机架号')
    worksheet.write(0,4,'接出单元类型')
    worksheet.write(0,5,'接出单元号')
    worksheet.write(0,6,'接出端口')
    worksheet.write(0,7,'接入机架号')
    worksheet.write(0,8,'接入单元类型')
    worksheet.write(0,9,'接入单元号')
    worksheet.write(0,10,'接入端口')
    worksheet.write(0,11,'跳纤长度')
    worksheet.write(0,12,'审核确认')
    worksheet.write(0,13,'备注')

    # #设置泵单价和电机单价样式
    # bengformat = workbook.add_format()
    # bengformat.set_align('center')
    # bengformat.set_align('vcenter')
    # bengformat.set_font_name('Arial')
    # bengformat.set_font_size(10)
    # bengformat.set_top(1)
    # bengformat.set_bottom(1)
    # bengformat.set_left(1)
    # bengformat.set_right(1)
    # bengformat.set_num_format('#,##0')

    #从数据库写入数据

    xuhao_list, updated_time_list, username_list, \
    jiechu_jijia_list, jiechu_side_list, jiechu_slotnum_list, jiechu_row_col_list, \
    jieru_jijia_list, jieru_side_list, jieru_slotnum_list, jieru_row_col_list, \
    line_list, confirm_list, remark_list = [],[],[],[],[],[],[],[],[],[],[],[],[],[]
    xuhao = 1
    for result in DuankouTable.query.all():
        worksheet.set_row(xuhao, 29, rowsformat) #30是行高
        worksheet.write(xuhao,0,xuhao)
        xuhao_list.append(xuhao)
        worksheet.write(xuhao,1,format_time(result.updated_time))
        updated_time_list.append(format_time(result.updated_time))
        worksheet.write(xuhao,2,result.username)
        username_list.append(result.username)
        worksheet.write(xuhao,3,result.jiechu_jijia)
        jiechu_jijia_list.append(result.jiechu_jijia)
        worksheet.write(xuhao,4,result.jiechu_side)
        jiechu_side_list.append(result.jiechu_side)
        worksheet.write(xuhao,5,format_slotnum(result.jiechu_side,result.jiechu_slotnum))
        jiechu_slotnum_list.append(format_slotnum(result.jiechu_side,result.jiechu_slotnum))
        worksheet.write(xuhao,6,format_duankou(result.jiechu_side, result.jiechu_row, result.jiechu_col))
        jiechu_row_col_list.append(format_duankou(result.jiechu_side, result.jiechu_row, result.jiechu_col))
        worksheet.write(xuhao,7,result.jieru_jijia)
        jieru_jijia_list.append(result.jieru_jijia)
        worksheet.write(xuhao,8,result.jieru_side)
        jieru_side_list.append(result.jieru_side)
        worksheet.write(xuhao,9,format_slotnum(result.jieru_side,result.jieru_slotnum))
        jieru_slotnum_list.append(format_slotnum(result.jieru_side,result.jieru_slotnum))
        worksheet.write(xuhao,10,format_duankou(result.jieru_side, result.jieru_row, result.jieru_col))
        jieru_row_col_list.append(format_duankou(result.jieru_side, result.jieru_row, result.jieru_col))
        worksheet.write(xuhao,11,result.line)
        line_list.append(result.line)
        worksheet.write(xuhao,12,format_confirm(result.confirm))
        confirm_list.append(format_confirm(result.confirm))
        worksheet.write(xuhao,13,result.remark)
        remark_list.append(result.remark)

        xuhao = xuhao + 1


    # #写入最后一行总价
    # shuliangheiji = sum(shuliang_list)
    # zongjiaheji = sum(zongjia_list)
    # worksheet.write(xuhao,3,'Q‘ty',rowsformat)
    # worksheet.write(xuhao,4,shuliangheiji,rowsformat)
    # # bold = workbook.add_format({'bold': 1})
    # worksheet.write(xuhao,25,'Total',totalformat)
    # worksheet.write(xuhao,26,zongjiaheji,lastcellformat)
    # zongjia_list.append(zongjiaheji)
    # #最后一行样式
    # worksheet.set_row(xuhao, 29) #30是行高
    # worksheet.write_blank(xuhao,1,None,lastrowformat)
    # worksheet.write_blank(xuhao,2,None,lastrowformat)
    # for i in range(5,25):
    #     worksheet.write_blank(xuhao,i,None,lastrowformat)


    #计算每列列宽
    if str_len('序号') > str_len(str(max(xuhao_list))):
        worksheet.set_column('A:A', int(str_len('编号')))
    else:
        worksheet.set_column('A:A', int(str_len(str(max(xuhao_list)))))

    if str_len('时间') > str_len(str(max(updated_time_list))):
        worksheet.set_column('B:B', int(str_len('时间')))
    else:
        worksheet.set_column('B:B', int(str_len(str(max(updated_time_list)))))

    if str_len('操作人员') > str_len(str(max(username_list))):
        worksheet.set_column('C:C', int(str_len('操作人员')))
    else:
        worksheet.set_column('C:C', int(str_len(str(max(username_list)))))

    if str_len('接出机架号') > str_len(str(max(jiechu_jijia_list))):
        worksheet.set_column('D:D', int(str_len('接出机架号')))
    else:
        worksheet.set_column('D:D', int(str_len(str(max(jiechu_jijia_list)))))

    if str_len('接出单元类型') > str_len(str(max(jiechu_side_list))):
        worksheet.set_column('E:E', int(str_len('接出单元类型')))
    else:
        worksheet.set_column('E:E', int(str_len(str(max(jiechu_side_list)))))

    if str_len('接出单元号') > str_len(str(max(jiechu_slotnum_list))):
        worksheet.set_column('F:F', int(str_len('接出单元号')))
    else:
        worksheet.set_column('F:F', int(str_len(str(max(jiechu_slotnum_list)))))

    if str_len('接出端口') >  str_len(str(max(jiechu_row_col_list))):
        worksheet.set_column('G:G', int(str_len('接出端口')))
    else:
        worksheet.set_column('G:G', int(str_len(str(max(jiechu_row_col_list)))))

    if str_len('接入机架号') > str_len(str(max(jieru_jijia_list))):
        worksheet.set_column('H:H', int(str_len('接入机架号')))
    else:
        worksheet.set_column('H:H', int(str_len(str(max(jieru_jijia_list)))))

    if str_len('接入单元类型') > str_len(str(max(jieru_side_list))):
        worksheet.set_column('I:I', int(str_len('接入单元类型')))
    else:
        worksheet.set_column('I:I', int(str_len(str(max(jieru_side_list)))))

    if str_len('接入单元号') > str_len(str(max(jieru_slotnum_list))):
        worksheet.set_column('J:J', int(str_len('接入单元号')))
    else:
        worksheet.set_column('J:J', int(str_len(str(max(jieru_slotnum_list)))))


    if str_len('接入端口') > str_len(str(max(jieru_row_col_list))):
        worksheet.set_column('K:K', int(str_len('接入端口')))
    else:
        worksheet.set_column('K:K', int(str_len(str(max(jieru_row_col_list)))))

    if str_len('跳纤长度') > str_len(str(max(line_list))):
        worksheet.set_column('L:L', int(str_len('跳纤长度')))
    else:
        worksheet.set_column('L:L', int(str_len(str(max(line_list)))))

    if str_len('审核确认') > str_len(str(max(confirm_list))):
        worksheet.set_column('M:M', int(str_len('审核确认')))
    else:
        worksheet.set_column('M:M', int(str_len(str(max(confirm_list)))))

    # if str_len('备注') > str_len(str(max(remark_list))):
    #     worksheet.set_column('N:N', int(str_len('备注')))
    # else:
    #     worksheet.set_column('N:N', int(str_len(str(max(remark_list)))))
    #计算每列列宽END


    # worksheet.print_area(0, 0, xuhao, 26)
    worksheet.set_paper(9) #A4
    worksheet.fit_to_pages(1, 0)

    workbook.close()

    return filename
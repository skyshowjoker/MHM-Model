# coding=utf-8
import os

import xlrd
import xlwt  # 操作excel模块
from xlrd import open_workbook
from xlutils.copy import copy

def excel_export():
    root = r'C:\Users\perlicue\Desktop\spacial_feature\multi_seq_train'
    dir = r'C:\Users\perlicue\Desktop\spacial_feature\multi_seq_train\match_label_dicom'
    file_path = root + '\\map_name_number_list.xlsx'  # sys.path[0]为要获取当前路径，filenamelist为要写入的文件
    f = xlwt.Workbook(encoding='utf-8', style_compression=0)  # 新建一个excel
    sheet = f.add_sheet('sheet1')  # 新建一个sheet
    pathDir = os.listdir(dir)  # 文件放置在当前文件夹中，用来获取当前文件夹内所有文件目录

    i = 0  # 将文件列表写入test.xls
    for s in pathDir:
        if s.__contains__(''):
            sheet.write(i, 0, s)  # 参数i,0,s分别代表行，列，写入值
            # if i<60:
            #     s = s.split('_')[1] + '_' + s.split('_')[2] + '_' + s.split('_')[3]
            # s = s.split('_')[0] + '_' + s.split('_')[1] + '_' + s.split('_')[2]
            # sheet.write(i, 0, s)
            sheet.write(i, 1, i + 1)
            i = i + 1

    print(file_path)
    print(i)  # 显示文件名数量
    f.save(file_path)

def excel_match_add_category():
    output = r'C:\Users\perlicue\Desktop\spacial_feature\multi_seq_train\new_MRI_dicom_name_list.xlsx'
    input = r'C:\Users\perlicue\Desktop\spacial_feature\pathology_name_list.xlsx'
    workbook2 = xlrd.open_workbook(input)
    table2 = workbook2.sheet_by_name('Sheet1')
    rows2 = table2.nrows

    rexcel = open_workbook(output, formatting_info=True)  # 保留原有样式
    # 用 xlrd 提供的方法获得现在已有的行数
    rows = rexcel.sheets()[0].nrows
    # 用 xlutils 提供的copy方法将 xlrd 的对象转化为 xlwt 的对象
    excel = copy(rexcel)
    # 用 xlwt 对象的方法获得要操作的 sheet
    table3 = rexcel.sheet_by_name('sheet1')
    table = excel.get_sheet(0)
    for i in range(0, rows):
        for j in range(0, rows2):
            if table3.cell(i, 0).value.strip().__contains__(table2.cell(j, 1).value.strip()):
                table.write(i, 3, table2.cell(j, 7).value.strip())
                table.write(i, 4, table2.cell(j, 8).value.strip())

    excel.save(output)

if __name__ == '__main__':
    excel_match_add_category()
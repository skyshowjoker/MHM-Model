import os

import xlrd
import xlwt
from tqdm import tqdm

from xlutils.copy import copy

from calculation.volumn_estimate import get_centoid, calculate_label


def get_full_name(c1, c2):
    workbook = xlrd.open_workbook(c1)
    table = workbook.sheet_by_name('Sheet1')
    rows = table.nrows
    workbook2 = xlrd.open_workbook(c2)
    table2 = workbook2.sheet_by_name('sheet1')
    rows2 = table2.nrows



    # 用 xlutils 提供的copy方法将 xlrd 的对象转化为 xlwt 的对象
    excel = copy(workbook)
    # 用 xlwt 对象的方法获得要操作的 sheet
    table_w = excel.get_sheet(0)

    count = 0
    for i in range(rows):
        for j in range(rows2):
            if table2.cell(j, 0).value.__contains__(table.cell(i, 0).value):
                table_w.write(i, 4, table2.cell(j, 0).value)
                table_w.write(i, 5, table2.cell(j, 1).value)
                table_w.write(i, 6, count)
                count += 1
                print(table.cell(i, 0).value)
                break
    excel.save(c1)

def cal_vol(dir):
    file_path = r"C:\Users\perlicue\Desktop\master_lecture\xiaowen\volume_cal2\temp_plus.xlsx"
    f = xlwt.Workbook(encoding='utf-8', style_compression=0)  # 新建一个excel
    sheet = f.add_sheet('Sheet1')
    patients = os.listdir(dir)
    count = 1
    for patient in tqdm(patients):
        patient = r"C:\Users\perlicue\Desktop\master_lecture\xiaowen\volume_cal2\13" + os.sep + patient
        left = calculate_label(patient, 1) + calculate_label(patient, 2)
        right = calculate_label(patient, 9) + calculate_label(patient, 10)
        sheet.write(count, 0, str(left))
        sheet.write(count, 1, str(right))
        count += 1
    f.save(file_path)
if __name__ == '__main__':
    input_file = r"C:\Users\perlicue\Desktop\master_lecture\xiaowen\input.xlsx"
    ref = r"C:\joey\master\resource\lymphoma\patient_name_seq.xlsx"
    dir = r"C:\Users\perlicue\Desktop\master_lecture\xiaowen\volume_cal2\13"
    # get_full_name(input_file, ref)
    cal_vol(dir)
# coding=utf-8
import os
import xlwt  # 操作excel模块
from tqdm import tqdm

root = r'C:\Users\perlicue\Desktop\master_lecture\xiaowen\volume_cal2\output_fold'
dir = r'C:\Users\perlicue\Desktop\master_lecture\xiaowen\wjq'
file_path = dir + '\wjq_num_list.xlsx'  # sys.path[0]为要获取当前路径，filenamelist为要写入的文件

def export_MRI(root, dir):
    f = xlwt.Workbook(encoding='utf-8', style_compression=0)  # 新建一个excel
    sheet = f.add_sheet('sheet1')  # 新建一个sheet
    pathDir = os.listdir(dir)  # 文件放置在当前文件夹中，用来获取当前文件夹内所有文件目录

    i = 0  # 将文件列表写入test.xls
    for s in tqdm(pathDir):
        s = s.split('.')[0]
        if s.__contains__('MRI'):
            sheet.write(i, 0, s)  # 参数i,0,s分别代表行，列，写入值
            sheet.write(i, 1, i)
            i = i + 1
    f.save(file_path)

def export_filename(root, dir):
    f = xlwt.Workbook(encoding='utf-8', style_compression=0)  # 新建一个excel
    sheet = f.add_sheet('Sheet1')  # 新建一个sheet
    pathDir = os.listdir(root)  # 文件放置在当前文件夹中，用来获取当前文件夹内所有文件目录

    i = 0  # 将文件列表写入test.xls
    for s in tqdm(pathDir):
            sheet.write(i, 0, s)  # 参数i,0,s分别代表行，列，写入值
            sheet.write(i, 1, i)
            i = i + 1
    f.save(file_path)



if __name__ == '__main__':
    export_filename(root, dir)
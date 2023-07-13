import shutil
import SimpleITK as sitk
import zipfile

import xlrd
import xlwt
from tqdm import tqdm
import os
import glob
def move_label():
    origin_dir = r"C:\Users\perlicue\Desktop\spacial_feature\multi_seq_train\unzip_path"
    target_dir = r"C:\joey\master\resource\lymphoma\dataset\nnUNet_raw_data_base\nnUNet_raw_data\Task028_lymphoma\labelsTr"
    label_path = r"C:\Users\perlicue\Desktop\spacial_feature\multi_seq_train\all_label"
    fileList = os.listdir(label_path)
    for file in tqdm(fileList):

        filename = glob.glob(label_path + os.sep + file + os.sep + '*.nii.gz')[0]
        img_name = "lymphoma_%03.0d.nii.gz" % int(file)
        newname = target_dir + os.sep + img_name

        shutil.copy(filename, newname)
def move_file():
    origin_dir = r"C:\Users\perlicue\Desktop\spacial_feature\multi_seq_train\unzip_path"
    target_dir = r"C:\Users\perlicue\Desktop\spacial_feature\multi_seq_train\match_label_dicom"
    label_path = r"C:\Users\perlicue\Desktop\spacial_feature\multi_seq_train\all_label"
    fileList = os.listdir(label_path)
    for file in tqdm(fileList):
        filename = origin_dir + os.sep + file
        if os.path.isdir(target_dir+os.sep+file) == False:
            shutil.move(filename, target_dir)
def move_from_wjq_file(origin_dir, target_dir):
    fileList = os.listdir(origin_dir)
    for file in tqdm(fileList):
        fileList2 = os.listdir(origin_dir + os.sep + file)
        for file2 in tqdm(fileList2):
            shutil.move(origin_dir + os.sep + file + os.sep + file2, target_dir)
def get_MRI_unzip():
    excel = r'C:\Users\perlicue\Desktop\spacial_feature\multi_seq_train\MRI_dicom_name_list.xlsx'
    excel_out = r'C:\Users\perlicue\Desktop\spacial_feature\multi_seq_train\temp_MRI_dicom_name_list.xlsx'
    mri_path = r'C:\joey\master\resource\lymphoma\PACS.Lymphoma.Spider\output'
    unzip_path = r'C:\Users\perlicue\Desktop\spacial_feature\multi_seq_train\unzip_path'
    zip_path = r'C:\Users\perlicue\Desktop\spacial_feature\multi_seq_train\zip_path'
    workbook = xlrd.open_workbook(excel)
    table = workbook.sheet_by_name('sheet1')
    f = xlwt.Workbook(encoding='utf-8', style_compression=0)  # 新建一个excel
    sheet = f.add_sheet('sheet1')  # 新建一个sheet

    # 通过nrows和ncols获取到表格中数据的行数和列数
    rows = table.nrows
    cols = table.ncols
    for index in range(0, rows):
        filename = table.cell(index, 1).value
        path = mri_path + os.sep + filename + '.zip'
        dirs = os.listdir(zip_path)
        primary_name = filename.split('_')[0] + '_' + filename.split('_')[1] + '_' + filename.split('_')[2]
        for dir in dirs:
            if(dir.__contains__(primary_name)):
                # shutil.copy(mri_path + os.sep + dir, zip_path + os.sep + dir)
                sheet.write(index, 0, 1)
    f.save(excel_out)
        # if os.path.exists(path):
        #     try:
        #         zf = zipfile.ZipFile(path, 'r')
        #     except zipfile.BadZipFile:
        #         print("zip error: " + path)
        #     # Extract all members from the archive to the current working directory
        #     in_path = unzip_path + os.sep + filename
        #     if os.path.isdir(in_path) == False:
        #         zf.extractall(in_path)
        # else:
        #     print(path)
        #     print('no zip:', index)

if __name__ == '__main__':
    # origin_dir = r'C:\Users\perlicue\Desktop\master_lecture\helper\wjq\补充影像_有对照'
    # target_dir = r'C:\Users\perlicue\Desktop\master_lecture\helper\wjq\dicom'

    # move_file(origin_dir, target_dir)
    move_label()
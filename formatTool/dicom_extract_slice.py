# 有bug，报错了重复跑
import glob

import pydicom as dicom
from tqdm import tqdm
import os
import shutil
import zipfile
import xlrd
import re



def get_patients(INPUT_FOLDER):
    workbook = xlrd.open_workbook(INPUT_FOLDER)
    table = workbook.sheet_by_name('Sheet1')
    rows = table.nrows
    result = []
    for i in range(rows):
        if table.cell(i, 0).value != "":
            result.append(table.cell(i, 0).value.split('.')[0])
    return result


# patients.sort()

def load_scan(path, out_path):
    # slices = [dicom.read_file(path + '/' + s) for s in os.listdir(path)]
    # slices = [s.pixel_array for s in slices if hasattr(s, 'SeriesDescription') and s.SeriesDescription == 't2_tse_fs_tra']
    for s in os.listdir(path):
        dicom_file = path + os.sep + s
        out_dicom = out_path + os.sep + s
        slice = dicom.read_file(dicom_file)
        # if slice.SeriesDescription == 't2_tse_fs_tra':
        # if slice.SeriesDescription == 't2_tse_dixon_tra_384_3mm_W':
        #https://www.runoob.com/python/python-reg-expressions.html
        #t2
        # pattern = 't2.*tra.*|T2.*tra$|t2_tse.*tra.*w$|eT2W_mDIXON_tra|t2_tse_fs-dixon_tra_320_W$|.*Ax T2 fs FSE.*|.*Ax T2 FRFSE.*fs.*'
        # pattern += '|.*T2W_HR_mDIXON_TSE_RL.*|.*T2W_HR_mDIXON_TSE.*'
        #t1
        # pattern = 'O*Ax T1 FSE|t1_(t|f)*se_tra|T1W_T*SE|t1_tse_fs-dixon_tra_W'

        #enhance
        pattern = 't1_se_tra|t1_fse_tra_fs_3mm|t1_vibe_fs_tra_Dynamic|Ax T1 FS.*c|t1_fse_wfi_tra_Echo1|ep2d_diff_.*DWI.*|t1_tse_tra.*C FS|T1W_SPIRC.*|T1W_SPIR.*|t1_tse_dixon_tra_3mm_W|T1W_mDIXON_TSE_Fast|T1WI_SPIR_C|T1W_SPIR C|T1WI_SPIRC|T1W_mDIXON_TSEC_pass|t1_spirC'
        try:
            if re.match(pattern, slice.SeriesDescription, re.I):
                shutil.copy(dicom_file, out_dicom)
        except AttributeError:
            print("error: "+out_dicom)
def load_scan_single(path, out_path):

    # slices = [dicom.read_file(path + '/' + s) for s in os.listdir(path)]
    # slices = [s.pixel_array for s in slices if hasattr(s, 'SeriesDescription') and s.SeriesDescription == 't2_tse_fs_tra']

    for s in os.listdir(path):
        dicom_file = path + os.sep + s
        out_dicom = out_path + os.sep + s
        slice = dicom.read_file(dicom_file)
        # if slice.SeriesDescription == 't2_tse_fs_tra':
        # if slice.SeriesDescription == 't2_tse_dixon_tra_384_3mm_W':
        pattern = 't2_tse_dixon_tra_384_3mm_W$'

        print(slice.SeriesDescription)
        print(re.match(pattern, slice.SeriesDescription, re.I))
        try:
            if re.match(pattern, slice.SeriesDescription, re.I):
                shutil.copy(dicom_file, out_dicom)
        except AttributeError:
            print("error: "+out_dicom)

def extract_single_seq():
    input_path = r'C:\Users\perlicue\Desktop\spacial_feature\multi_seq_train\match_label_dicom'
    output_path = r'C:\Users\perlicue\Desktop\spacial_feature\multi_seq_train\seqs\enhance'
    filelist = os.listdir(input_path)
    for file in tqdm(filelist):
        in_path = input_path + os.sep + file
        out_path = output_path + os.sep + file
        if os.path.isdir(out_path) == False:
            os.mkdir(out_path)
            load_scan(in_path, out_path)
        elif not os.listdir(out_path):
            load_scan(in_path, out_path)
def search(path):
    path_t2 = r'C:\Users\perlicue\Desktop\spacial_feature\multi_seq_train\seqs\t2'
    path_enhance = r'C:\Users\perlicue\Desktop\spacial_feature\multi_seq_train\seqs\enhance'
    files=os.listdir(path)   #查找路径下的所有的文件夹及文件
    for filee in  files:
      f= path+"/"+filee  #使用绝对路径
      f2 = path_t2+"/"+filee
      f3 = path_enhance + "/" + filee
      # dicom_file = glob.glob(f + '/*')[0]
      # slice1 = dicom.read_file(dicom_file)
      # dicom_file = glob.glob(f2 + '/*')[0]
      # slice2 = dicom.read_file(dicom_file)
      # dicom_file = glob.glob(f3 + '/*')[0]
      # slice3 = dicom.read_file(dicom_file)
      if os.path.isdir(f):  #判断是文件夹还是文件
        if not os.listdir(f):  #判断文件夹是否为空
            print(str(filee))
        else:
            print('f',filee,len(os.listdir(f)), ' vs ', len(os.listdir(f2)), ' vs ', len(os.listdir(f3)))

# for patient in patients:
#     path = INPUT_FOLDER + patient
#     zf = zipfile.ZipFile(path + '.zip', 'r')
#
#     # Extract all members from the archive to the current working directory
#
#     zf.extractall(unzip_path + patient)
#     in_path = unzip_path + patient
#     out_path = OUTPUT_FOLDER + patient
#     if os.path.isdir(out_path) == False:
#         os.mkdir(out_path)
#         load_scan(in_path, out_path)
#         print(out_path)

def extract():
    for patient in tqdm(patients):
        path = INPUT_FOLDER + os.sep + patient + ".zip"
        if os.path.exists(path):
            try:
                zf = zipfile.ZipFile(path, 'r')
            except zipfile.BadZipFile:
                print("zip error: " + path)
            # Extract all members from the archive to the current working directory
            in_path = unzip_path + os.sep + patient
            if os.path.isdir(in_path) == False:
                zf.extractall(in_path)

            out_path = OUTPUT_FOLDER + patient
            if os.path.isdir(out_path) == False:
                os.mkdir(out_path)
                load_scan(in_path, out_path)
                print(out_path)
            elif not os.listdir(out_path):
                load_scan(in_path, out_path)
        else:
            print(path)
def unzip(input_dir, output_dir):
    dirs = os.listdir(input_dir)
    for patient in tqdm(dirs):
        path = input_dir + os.sep + patient
        if os.path.exists(path):
            try:
                zf = zipfile.ZipFile(path, 'r')
            except zipfile.BadZipFile:
                print("zip error: " + path)
            # Extract all members from the archive to the current working directory
            out_path = output_dir + os.sep + patient.split('.')[0]
            if os.path.isdir(out_path) == False:
                zf.extractall(out_path)

excel = r"C:\Users\perlicue\Desktop\master_lecture\xiaowen\wjq\list_already.xlsx"
patients = get_patients(excel)
if __name__ == '__main__':
    # unzip -> extract seq -> to nii
    INPUT_FOLDER = r"C:\joey\master\resource\lymphoma\PACS.Lymphoma.Spider\output"

    OUTPUT_FOLDER = r"C:\Users\perlicue\Desktop\master_lecture\xiaowen\volume_cal2\output_fold\\"
    # label_folder = r"C:\joey\master\resource\lymphoma\tag\label_file"
    input_path = r'C:\Users\perlicue\Desktop\spacial_feature\multi_seq_train\all_zip_path'
    unzip_path = r"C:\Users\perlicue\Desktop\spacial_feature\multi_seq_train\unzip_path"
    # extract_single_seq()

    path = r'C:\Users\perlicue\Desktop\spacial_feature\multi_seq_train\match_label_dicom\10'
    # load_scan_single(path, r'C:\Users\perlicue\Desktop\spacial_feature\multi_seq_train\seqs\t2\10')
    search(r'C:\Users\perlicue\Desktop\spacial_feature\multi_seq_train\seqs\t1')

# if __name__ == '__main__':
#     in_path = r"C:\joey\master\resource\lymphoma\tag\To_Weilai\0001308661_钱金贵_2021-03-09_眼眶MRI增强_3829681_7087505\0001308661_钱金贵_2021-03-09_眼眶MRI增强_3829681_7087505"
#     out_path = r"C:\joey\master\resource\lymphoma\dataset\t2_dicom3\0001308661_钱金贵_2021-03-09_眼眶MRI增强_3829681_7087505"
#     path = r"C:\joey\master\resource\lymphoma\dataset\t2_dicom3"
#     if os.path.isdir(out_path) == False:
#         os.mkdir(out_path)
#         load_scan(in_path, out_path)
#     elif not os.listdir(out_path):
#         load_scan(in_path, out_path)
#     search(path)
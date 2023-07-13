# 有bug，报错了重复跑
import pydicom as dicom
from tqdm import tqdm
import os
import shutil
import zipfile
import xlrd
import re
INPUT_FOLDER = r"C:\joey\master\resource\lymphoma\PACS.Lymphoma.Spider\output"
excel = r"C:\joey\master\resource\lymphoma\book2.xlsx"
OUTPUT_FOLDER = r"C:\joey\master\resource\lymphoma\dataset\third_label_data\output\\"
label_folder = r"C:\joey\master\resource\lymphoma\dataset\third_label_data\new add"
unzip_path = r"C:\joey\master\resource\lymphoma\dataset\third_label_data\unzip_dicom3\\"


def get_patients(label_folder):
    files = os.listdir(label_folder)
    return files
patients = get_patients(label_folder)
# patients.sort()

def load_scan(path, out_path):

    # slices = [dicom.read_file(path + '/' + s) for s in os.listdir(path)]
    # slices = [s.pixel_array for s in slices if hasattr(s, 'SeriesDescription') and s.SeriesDescription == 't2_tse_fs_tra']

    for s in os.listdir(path):
        slice = dicom.read_file(path + '/' + s)
        # if slice.SeriesDescription == 't2_tse_fs_tra':
        # if slice.SeriesDescription == 't2_tse_dixon_tra_384_3mm_W':
        pattern = 't2.*tra$|t2_tse.*tra.*w$|eT2W_mDIXON_tra'
        try:
            if re.match(pattern, slice.SeriesDescription, re.I):
                shutil.copy(path + '/' + s, out_path + '/' + s)
        except AttributeError:
            print("error: "+out_path)
def search(path):
  files=os.listdir(path)   #查找路径下的所有的文件夹及文件
  for filee in  files:
      f=path+"/"+filee  #使用绝对路径
      if os.path.isdir(f):  #判断是文件夹还是文件
        if not os.listdir(f):  #判断文件夹是否为空
          print(str(filee))
        else:
            print('f',f,len(os.listdir(f)))

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
        path = INPUT_FOLDER + os.sep + patient
        if os.path.exists(path + '.zip'):
            zf = zipfile.ZipFile(path + '.zip', 'r')

            # Extract all members from the archive to the current working directory

            zf.extractall(unzip_path + patient)
            in_path = unzip_path + patient
            out_path = OUTPUT_FOLDER + patient
            if os.path.isdir(out_path) == False:
                os.mkdir(out_path)
                load_scan(in_path, out_path)
                print(out_path)
            elif not os.listdir(out_path):
                load_scan(in_path, out_path)
        else:
            print(path)




if __name__ == '__main__':
    extract()
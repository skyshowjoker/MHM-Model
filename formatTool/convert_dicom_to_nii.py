import shutil

import pydicom as dicom
from tqdm import tqdm
import os
import zipfile
import re
import SimpleITK as sitk

def unzip(path, file_name):
    if os.path.exists(path):
        try:
            zf = zipfile.ZipFile(path, 'r')
        except zipfile.BadZipFile:
            print("zip error: " + path)
        # Extract all members from the archive to the current working directory

        if os.path.isdir(file_name) == False:
            zf.extractall(file_name)

def load_scan(path):
    for s in os.listdir(path):
        dicom_file = path + os.sep + s
        slice = dicom.read_file(dicom_file)
        # if slice.SeriesDescription == 't2_tse_fs_tra':
        # if slice.SeriesDescription == 't2_tse_dixon_tra_384_3mm_W':
        # https://www.runoob.com/python/python-reg-expressions.html
        # t2
        # pattern = 't2.*tra.*|T2.*tra$|t2_tse.*tra.*w$|eT2W_mDIXON_tra|t2_tse_fs-dixon_tra_320_W$|.*Ax T2 fs FSE.*|.*Ax T2 FRFSE.*fs.*'
        # pattern += '|.*T2W_HR_mDIXON_TSE_RL.*|.*T2W_HR_mDIXON_TSE.*'
        # t1
        # pattern = 'O*Ax T1 FSE|t1_(t|f)*se_tra|T1W_T*SE|t1_tse_fs-dixon_tra_W'

        # enhance
        pattern = 't1_se_tra|t1_fse_tra_fs_3mm|t1_vibe_fs_tra_Dynamic|Ax T1 FS.*c|t1_fse_wfi_tra_Echo1|ep2d_diff_.*DWI.*|t1_tse_tra.*C FS|T1W_SPIRC.*|T1W_SPIR.*|t1_tse_dixon_tra_3mm_W|T1W_mDIXON_TSE_Fast|T1WI_SPIR_C|T1W_SPIR C|T1WI_SPIRC|T1W_mDIXON_TSEC_pass|t1_spirC'
        try:
            if not re.match(pattern, slice.SeriesDescription, re.I):
                # shutil.copy(dicom_file, out_dicom)
                try:
                    # 删除文件
                    os.remove(dicom_file)
                    print(f"文件 {dicom_file} 已被删除")
                except FileNotFoundError:
                    print(f"文件 {dicom_file} 不存在")
                except PermissionError:
                    print(f"没有权限删除文件 {dicom_file}")
                except Exception as e:
                    print(f"删除文件时发生错误: {e}")
        except AttributeError:
            print("error")

            
def readdcm(filepath):
    reader = sitk.ImageSeriesReader()
    reader.MetaDataDictionaryArrayUpdateOn()
    reader.LoadPrivateTagsOn()
    series_id = reader.GetGDCMSeriesIDs(filepath)
    print(series_id)
    series_file_names = reader.GetGDCMSeriesFileNames(filepath, series_id[0])

    reader.SetFileNames(series_file_names)
    images = reader.Execute()

    return images
def dcm2nii(dcm_path, save_path):
    dcm_images = readdcm(dcm_path)
    sitk.WriteImage(dcm_images, '{}.nii.gz'.format(save_path))

if __name__ == '__main__':
    file = r"/Users/mac/Downloads/01.zip"
    temp_file = r"/Users/mac/Downloads/file1"
    unzip(file, temp_file)
    load_scan(temp_file)
    dcm2nii(temp_file, temp_file)
    shutil.rmtree(temp_file)

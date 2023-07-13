# 文件名不能包含非ascii码
import SimpleITK as sitk
import os
from tqdm import tqdm
def dcm2nii(dcms_path, nii_path):
	# 1.构建dicom序列文件阅读器，并执行（即将dicom序列文件“打包整合”）
    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(dcms_path)
    reader.SetFileNames(dicom_names)
    image2 = reader.Execute()
	# 2.将整合后的数据转为array，并获取dicom文件基本信息
    image_array = sitk.GetArrayFromImage(image2)  # z, y, x
    origin = image2.GetOrigin()  # x, y, z
    spacing = image2.GetSpacing()  # x, y, z
    direction = image2.GetDirection()  # x, y, z
	# 3.将array转为img，并保存为.nii.gz
    image3 = sitk.GetImageFromArray(image_array)
    image3.SetSpacing(spacing)
    image3.SetDirection(direction)
    image3.SetOrigin(origin)
    sitk.WriteImage(image3, nii_path)

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

out_path = r'C:\Users\perlicue\Desktop\spacial_feature\multi_seq_train\seqs\enhance_nii'

file_root = r"C:\Users\perlicue\Desktop\spacial_feature\multi_seq_train\seqs\enhance"
if __name__ == '__main__':
    file_list = os.listdir(file_root)
    print(file_list)
    for img_name in tqdm(file_list):
        # if img_name.endswith('.dcm'):
        dcm_path = file_root + os.sep + img_name
        print(dcm_path)
        #
        dcm_images = readdcm(dcm_path)
        img_name = "lymphoma_%03.0d_0002" % int(img_name)
        save_path = out_path + os.sep + img_name
        sitk.WriteImage(dcm_images, '{}.nii.gz'.format(save_path))
        # if os.path.isdir(save_path) == False:
        #     os.mkdir(save_path)
        #     sitk.WriteImage(dcm_images, os.path.join(save_path + os.sep + "t2_tra",
        #                                              '{}.nii.gz'.format(save_path + os.sep + "t2_tra")))

        # dcm2nii(dcm_path,os.path.join(save_path + os.sep + img_name + os.sep + "t2_tra", '{}.nii.gz'.format(save_path + os.sep + img_name + os.sep + "t2_tra")))
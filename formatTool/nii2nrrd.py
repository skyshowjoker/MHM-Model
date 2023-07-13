import os
from tqdm import tqdm
import nrrd
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

def nii2nrrd(nii_path, nrrd_path):
    img = nib.load(nii_path).get_fdata()
    data = np.asarray(img)
    nrrd.write(nrrd_path, data)
def modify_label(nii_path):
    img = nib.load(nii_path)
    data = img.get_fdata()

    data[data == 2] = 1
    data[data == 9] = 1
    new_img = nib.Nifti1Image(data.astype(np.uint8), img.affine, img.header)
    nib.save(new_img, nii_path)

if __name__ == '__main__':
    base_path = r'C:\joey\master\resource\lymphoma\dataset\nnUNet_raw_data_base\nnUNet_raw_data\labelsTr'
    files = os.listdir(base_path)
    for item in tqdm(files):
        data_path = base_path + os.sep + item


        modify_label(data_path)

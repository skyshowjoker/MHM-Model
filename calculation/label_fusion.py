import nibabel as nib
import numpy as np
import SimpleITK as sitk
from tqdm import tqdm
import os
file = r'C:\joey\master\resource\lymphoma\dataset\Task04_lymphoma\imageTr\lymphoma_029.nii.gz'
def convert(nii_file, num_class1, num_class2):
    img = nib.load(nii_file)
    nii_header = img.header
    data = np.asarray(img.dataobj)
    [rows, cols, slices] = data.shape
    # data process
    # data[data==num_class1] = num_class2
    for i in range(rows):
        for j in range(cols):
            for k in range(slices):
                if data[i, j, k] == num_class1:
                    data[i, j, k] = num_class2
    img = nib.Nifti1Image(data, img.affine, img.header)
    nib.save(img, nii_file)




if __name__ == '__main__':
    path = r'C:\joey\master\resource\lymphoma\dataset\Task06 - 副本\labelsTr'
    files = os.listdir(path)
    for file in tqdm(files):
        file = path + os.sep + file
        for i in range(7):
            # convert(file, i+2, i+1)
            # convert(file, i+9, i+8)
            print(i)

import numpy as np
from tqdm import tqdm

import volumn_estimate as ve
import xlrd
import os

from calculation.model.EFD import get_efd_feature
from calculation.model.GLCM import get_glcm, get_glcm_by

excel_path = r"C:\Users\perlicue\Desktop\spacial_feature\multi_seq_train\new_MRI_dicom_name_list.xlsx"

def normalize(x):
    if np.max(x) - np.min(x) == 0:
        return x
    return (x - np.min(x)) / (np.max(x) - np.min(x))
def get_patients(INPUT_FOLDER):
    workbook = xlrd.open_workbook(INPUT_FOLDER)
    table = workbook.sheet_by_name('sheet1')
    rows = table.nrows
    results = []
    labels = []
    label2 = []
    for i in range(rows):
        if table.cell(i, 3).value is None:
            continue
        results.append(int(table.cell(i, 2).value))
        label2.append(int(table.cell(i, 3).value))
        labels.append(int(table.cell(i, 4).value))
    return results, label2, labels
patients, label1, labels = get_patients(excel_path)

# def get_name_from_excel(var, file_name, in_col, out_col, sheet):
#     workbook = xlrd.open_workbook(file_name)
#     table = workbook.sheet_by_name(sheet)
#     rows = table.nrows
#     cols = table.ncols
#     for i in range(rows):
#         if table.cell(i, in_col).value == var.split(".")[0]:
def get_cal_nii2(path):
    p = []
    result = ""
    for i in range(1, 17):
        if i == 1 | i == 3 | i == 9 | i == 11:
            p = ve.get_centoid(path, i)
            result += str(p[0]) + " " + str(p[1]) + " " + str(p[2]) + " "
    LE = ve.calculate_label(path, 3)
    RE = ve.calculate_label(path, 11)
    LAL = ve.calculate_label(path, 1)
    RAL = ve.calculate_label(path, 9)
    result += str(LE) + " " + str(RE) + " " + str(LAL) + " " + str(RAL)
    return result
def get_cal_nii(path):
    p = []
    result = ""
    for i in range(1, 17):
        if i == 1 | i == 3 | i == 9 | i == 11:
            p = ve.get_centoid(path, i)
            result += str(p[0]) + " " + str(p[1]) + " " + str(p[2]) + " "

    LAL = ve.calculate_label(path, 1)
    RAL = ve.calculate_label(path, 9)
    result += str(LAL) + " " + str(RAL)
    return result
def get_WD_from_position(p, index, num):
    W = np.zeros((8, 8), dtype=int)
    D = np.zeros((8, 8), dtype=int)
    L = np.zeros((8, 8), dtype=int)
    # get W
    for i in range(0, 8):
        if p[i][0] > 0:
            dis = ve.euclideanDistance(p[0],p[i], 3)
            # texture2 = get_glcm_by(index, num + i)
            # dis = dis * texture2
            W[0][i] = W[i][0] = dis
    for i in range(0, 8):
        if p[i][0] > 0:
            dis = ve.euclideanDistance(p[2],p[i], 3)
            # texture2 = get_glcm_by(index, num + i)
            # dis = dis * texture2
            W[2][i] = W[i][2] = dis
    for i in range(0, 8):
        if p[i][0] > 0:
            dis = ve.euclideanDistance(p[1],p[i], 3)
            # texture2 = get_glcm_by(index, num + i)
            # dis = dis * texture2
            W[1][i] = W[i][1] = dis

    # get D
    # W = c(W)
    for i in range(0, 8):
        D[i][i] = sum(W[i])

    # get L
    L = D - W
    c = np.linalg.eig(L)
    return c[0]

def get_WD_from_vol(p, index, nii_path):
    W = np.zeros((8, 8), dtype=int)
    D = np.zeros((8, 8), dtype=int)
    L = np.zeros((8, 8), dtype=int)
    # get W
    for i in range(0, 8):
        if p[i][0] > 0:
            dis = ve.euclideanDistance(p[0],p[i], 3)
            texture1 = ve.calculate_label(nii_path, i)
            dis = dis * texture1
            W[0][i] = W[i][0] = dis
    for i in range(0, 8):
        if p[i][0] > 0:
            dis = ve.euclideanDistance(p[2],p[i], 3)
            texture1 = ve.calculate_label(nii_path, i)
            dis = dis * texture1
            W[2][i] = W[i][2] = dis
    for i in range(0, 8):
        if p[i][0] > 0:
            dis = ve.euclideanDistance(p[1],p[i], 3)
            texture1 = ve.calculate_label(nii_path, i)
            dis = dis * texture1
            W[1][i] = W[i][1] = dis

    # get D
    # W = c(W)
    for i in range(0, 8):
        D[i][i] = sum(W[i])

    # get L
    L = D - W
    c = np.linalg.eig(L)
    return c[0]
def get_WD(nii_path, index):
    p = np.zeros((8, 3), dtype=int)
    LAL = ve.calculate_label(nii_path, 1)
    RAL = ve.calculate_label(nii_path, 9)
    le = ve.get_centoid(nii_path, 11)
    re = ve.get_centoid(nii_path, 3)
    mid = ve.get_mid(re, le)
    if LAL < 10 & RAL < 10:
        return np.zeros(1)
    elif LAL > RAL:
        for i in range(0, 8):
            if i == 1:
                p[i] = mid
            else:
                p[i] = ve.get_centoid(nii_path, i+1)
        return get_WD_from_position(p, index, 1)
    else:
        for i in range(0,8):
            if i == 1:
                p[i] = mid
            else:
                p[i] = ve.get_centoid(nii_path, i+9)
        return get_WD_from_position(p, index, 9)
def get_WD_from_plane(nii_path, index):
    p = np.zeros((8, 3), dtype=int)
    sum = np.zeros(8)
    LAL = ve.calculate_label(nii_path, 1)
    RAL = ve.calculate_label(nii_path, 9)
    le = ve.get_centoid(nii_path, 11)
    re = ve.get_centoid(nii_path, 3)
    mid = ve.get_mid(re, le)
    if LAL < 10 & RAL < 10:
        return np.zeros(1)
    elif LAL > RAL:
        for i in range(0,8):
            if i == 0:
                result = ve.get_centoid_plane(nii_path, i+1)
                if len(result) == 0:
                    return np.zeros(1)
            if i == 1:
                p[i] = mid
            else:
                p[i] = ve.get_centoid(nii_path, i+1)
        for plane in range(0, len(result)):
            p[0] = result[plane]
            sum = sum + get_WD_from_position(p, index, 1)
        return sum
    else:
        for i in range(0, 8):
            if i == 0:
                result = ve.get_centoid_plane(nii_path, i + 9)
                if len(result) == 0:
                    return np.zeros(1)
            if i == 1:
                p[i] = mid
            else:
                p[i] = ve.get_centoid(nii_path, i + 9)
        for plane in range(0, len(result)):
            p[0] = result[plane]
            sum = sum + get_WD_from_position(p, index, 9)
        return sum
def generate_WD():
    global str
    nii_path = r"C:\joey\master\resource\lymphoma\volume_calculate\12_Aug"
    f = open("data\wd_134_A.txt", "w")
    for i in range(0, len(patients)):
    # for i in range(0, 3):
    #     path = nii_path + os.sep + str(int(patients[i])) + ".nii.gz"
        code = "lymphoma_%03.0d" % int(patients[i])
        path = r"C:\Users\perlicue\Desktop\spacial_feature\multi_seq_train\seqs\labelsTr" + os.sep + code + r".nii.gz"
        if not os.path.exists(path):
            continue
        feature = get_WD(path, i)
        if feature.size == 1:
            continue
        result = ""
        for j in range(0, 7):
            result += str(np.round(feature[j], 4)) + " "
        f.write(result)
        f.write(str(labels[i]))
        f.write("\n")
        print(i)
def generate_efd():
    global str
    nii_path = r"C:\joey\master\resource\lymphoma\volume_calculate\12_Aug"
    f = open("data\data_11_EFD_norm5_aug.txt", "w")
    for i in range(0, len(patients)):
        try:
            feature = normalize(get_efd_feature(i))
        except FileNotFoundError:
            continue

        if feature.size == 1:
            continue
        result = ""
        for j in range(0, 5):
            result += str(np.round(feature[j], 4)) + " "
        f.write(result)
        f.write(str(labels[i]))
        f.write("\n")
        print(i)
def generate_WD_plane():
    global str
    nii_path = r"C:\joey\master\resource\lymphoma\volume_calculate\12_Aug"
    f = open("data\data_11_WD_plane2_weight.txt", "w")
    for i in range(0, len(patients)):
        print(i)
        # for i in range(0, 3):
        path = nii_path + os.sep + str(int(patients[i])) + ".nii.gz"
        if not os.path.exists(path):
            continue
        feature = normalize(get_WD_from_plane(path, i))
        if feature.size == 1:
            continue
        result = ""
        for j in range(0, 7):
            result += str(np.round(feature[j], 4)) + " "
        f.write(result)
        f.write(str(labels[i]))
        f.write("\n")
        print(i)

def generate_glcm_data():
    global str
    f = open("data\glcm_134_A.txt", "w")
    for i in range(0, len(patients)):
    # for i in range(0, 3):

        try:
            feature = get_glcm(patients[i])
        except FileNotFoundError:
            continue
        result = ""
        for j in range(0, 4):
            result += str(np.round(feature[j], 4)) + " "

        f.write(result)
        f.write(str(labels[i]))
        f.write("\n")
        print(i)
def generate_glcmAndWD_data():
    global str
    nii_path = r"C:\joey\master\resource\lymphoma\volume_calculate\12_Aug"
    f = open("data\glcmAndwd_134_A.txt", "w")
    for i in range(0, len(patients)):
        # path = nii_path + os.sep + str(int(patients[i])) + ".nii.gz"
        code = "lymphoma_%03.0d" % int(patients[i])
        label_file = r"C:\Users\perlicue\Desktop\spacial_feature\multi_seq_train\seqs\labelsTr" + os.sep + code + r".nii.gz"
        if not os.path.exists(label_file):
            continue
        feature = get_WD(label_file, patients[i])
        if feature.size == 1:
            continue
        result = ""
        for j in range(0, 7):
            result += str(np.round(feature[j], 4)) + " "

        feature = get_glcm(patients[i])
        for j in range(0, 4):
            result += str(np.round(feature[j], 4)) + " "
        f.write(result)
        f.write(str(labels[i]))
        f.write("\n")
        print(i)
def generate_glcmAndWD_plane_data():
    global str
    nii_path = r"C:\joey\master\resource\lymphoma\volume_calculate\12_Aug"
    f = open("data\data_11_glcmAndwd_plane_weight.txt", "w")
    for i in range(0, len(patients)):
        print(i)
        path = nii_path + os.sep + str(int(patients[i])) + ".nii.gz"
        if not os.path.exists(path):
            continue
        feature = normalize(get_WD_from_plane(path, i))
        if feature.size == 1:
            continue
        result = ""
        for j in range(0, 7):
            result += str(np.round(feature[j], 4)) + " "

        feature = get_glcm(i)
        for j in range(0, 4):
            result += str(np.round(feature[j], 4)) + " "
        f.write(result)
        f.write(str(labels[i]))
        f.write("\n")
        print(i)

def generate_glcmAndWD_planeAndEFD_data():
    global str
    nii_path = r"C:\joey\master\resource\lymphoma\volume_calculate\12_Aug"
    f = open("data\data_11_glcmAndwd_planeAndEFD_weight.txt", "w")
    for i in range(0, len(patients)):
        print(i)
        path = nii_path + os.sep + str(int(patients[i])) + ".nii.gz"
        if not os.path.exists(path):
            continue
        feature = normalize(get_WD_from_plane(path, i))
        if feature.size == 1:
            continue
        result = ""
        for j in range(0, 7):
            result += str(np.round(feature[j], 4)) + " "
        #glcm
        feature = get_glcm(i)
        for j in range(0, 4):
            result += str(np.round(feature[j], 4)) + " "
        #efd
        feature = normalize(get_efd_feature(i))
        for j in range(0, 5):
            result += str(np.round(feature[j], 4)) + " "
        f.write(result)
        f.write(str(labels[i]))
        f.write("\n")
        print(i)

def generate_all_data():
    global str
    nii_path = r"C:\joey\master\resource\lymphoma\volume_calculate\12_Aug"
    f = open("data\data_11_all_weight.txt", "w")
    for i in range(0, len(patients)):
        path = nii_path + os.sep + str(int(patients[i])) + ".nii.gz"
        if not os.path.exists(path):
            continue
        feature = normalize(get_WD(path, i))
        if feature.size == 1:
            continue
        result = ""
        for j in range(0, 7):
            result += str(np.round(feature[j], 4)) + " "
        feature = normalize(get_WD_from_plane(path, i))
        if feature.size == 1:
            continue
        result = ""
        for j in range(0, 7):
            result += str(np.round(feature[j], 4)) + " "
        #glcm
        feature = normalize(get_glcm(i))
        for j in range(0, 4):
            result += str(np.round(feature[j], 4)) + " "
        #efd
        feature = normalize(get_efd_feature(i))
        for j in range(0, 5):
            result += str(np.round(feature[j], 4)) + " "
        f.write(result)
        f.write(str(labels[i]))
        f.write("\n")
if __name__ == '__main__':


    generate_glcm_data()
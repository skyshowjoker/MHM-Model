import os

import os
import volumn_estimate as ve
import numpy as np
import xlrd
from tqdm import tqdm

from calculation.model.EFD import get_efd_feature, get_efd_feature_by_label
from calculation.model.GLCM import get_glcm, get_glcm_by

excel_path = r"C:\Users\perlicue\Desktop\spacial_feature\diagnosis_name_list_full.xlsx"

def normalize(x):
    if np.max(x) - np.min(x) == 0:
        return x
    return (x - np.min(x)) / (np.max(x) - np.min(x))
def get_patients(INPUT_FOLDER):
    workbook = xlrd.open_workbook(INPUT_FOLDER)
    table = workbook.sheet_by_name('Sheet1')
    rows = table.nrows
    results = []
    labels = []
    for i in range(rows):
        if i == 0:
            continue
        results.append(table.cell(i, 4).value)
        labels.append(table.cell(i, 2).value)
    return results, labels
patients, labels = get_patients(excel_path)
def generate():
    global str
    nii_path = r"C:\joey\master\resource\lymphoma\volume_calculate\12_Aug"
    f1 = open("gcn_data\DS_graph_indicator.txt", "w")
    f2 = open("gcn_data\DS_graph_labels.txt", "w")
    f3 = open("gcn_data\DS_node_labels.txt", "w")
    f4 = open("gcn_data\DS_A.txt", "w")
    f5 = open("gcn_data\DS_node_attributes.txt", "w")
    # f6 = open("gcn_data\DS_edge_attributes.txt", "w")
    node = 0
    for i in tqdm(range(0, len(patients))):
        n = node * 8 + 1
        #DS_node_attributes.txt
        path = nii_path + os.sep + str(int(patients[i])) + ".nii.gz"
        try:
            LAL = ve.calculate_label(path, 1)
            RAL = ve.calculate_label(path, 9)
        except FileNotFoundError:
            continue

        num = 0
        if LAL < 10 & RAL < 10:
            continue
        elif LAL > RAL:
            num = 1
        else:
            num = 9
        for issue in range(0, 8):
            try:
                input_label = issue + num
                feature = get_glcm_by(i, input_label)
            except FileNotFoundError:
                continue
            result = ""
            for j in range(0, 3):
                result += str(np.round(feature[j], 4)) + ", "
            result += str(np.round(feature[3], 4))
            f5.write(result)
            f5.write("\n")

        for j in range(0, 8):

            # DS_graph_indicator.txt
            f1.write(str(node+1))
            f1.write("\n")
            #DS_node_labels.txt
            f3.write(str(j+1))
            f3.write("\n")
        # DS_A.txt

        for k in range(1,8):
            f4.write(str(n) + ', ' + str(n+k))
            f4.write("\n")
            # p1 = ve.get_centoid(path, k+num)
            # p2 = ve.get_centoid(path, 0+num)
            # dis = ve.euclideanDistance(p1, p2, 3)
            # f6.write(str(np.round(dis, 4)))
            # f6.write("\n")
        for k in range(2,8):
            f4.write(str(n+1) + ', ' + str(n+k))
            f4.write("\n")
            # p1 = ve.get_centoid(path, k + num)
            # p2 = ve.get_centoid(path, 1 + num)
            # dis = ve.euclideanDistance(p1, p2, 3)
            # f6.write(str(np.round(dis, 4)))
            # f6.write("\n")
        for k in range(3,8):
            f4.write(str(n+2) + ', ' + str(n+k))
            f4.write("\n")
            # p1 = ve.get_centoid(path, k + num)
            # p2 = ve.get_centoid(path, 2 + num)
            # dis = ve.euclideanDistance(p1, p2, 3)
            # f6.write(str(np.round(dis, 4)))
            # f6.write("\n")
        # DS_graph_labels.txt
        f2.write(str(labels[i]))
        f2.write("\n")
        node = node+1
def generate_glcmAndEfd():
    global str
    nii_path = r"C:\joey\master\resource\lymphoma\volume_calculate\12_Aug"
    f1 = open("gcn_data\DS_graph_indicator.txt", "w")
    f2 = open("gcn_data\DS_graph_labels.txt", "w")
    f3 = open("gcn_data\DS_node_labels.txt", "w")
    f4 = open("gcn_data\DS_A.txt", "w")
    f5 = open("gcn_data\DS_node_attributes.txt", "w")
    f6 = open("gcn_data\DS_edge_attributes.txt", "w")
    node = 0
    for i in tqdm(range(0, len(patients))):
        n = node * 8 + 1
        #DS_node_attributes.txt
        path = nii_path + os.sep + str(int(patients[i])) + ".nii.gz"
        try:
            LAL = ve.calculate_label(path, 1)
            RAL = ve.calculate_label(path, 9)
        except FileNotFoundError:
            continue

        num = 0
        if LAL < 10 & RAL < 10:
            continue
        elif LAL > RAL:
            num = 1
        else:
            num = 9
        for issue in range(0, 8):
            result = ""
            #glcm
            try:
                input_label = issue + num
                feature = get_glcm_by(i, input_label)
            except FileNotFoundError:
                continue

            for j in range(0, 3):
                result += str(np.round(feature[j], 4)) + ", "
            result += str(np.round(feature[3], 4)) + ","

            #efd
            try:
                input_label = issue + num
                feature = get_efd_feature_by_label(i, input_label)
            except FileNotFoundError:
                continue
            for j in range(0, 19):
                result += str(np.round(feature[j], 4)) + ", "
            result += str(np.round(feature[19], 4))

            f5.write(result)
            f5.write("\n")

        for j in range(0, 8):

            # DS_graph_indicator.txt
            f1.write(str(node+1))
            f1.write("\n")
            #DS_node_labels.txt
            f3.write(str(j+1))
            f3.write("\n")
        # DS_A.txt

        for k in range(1,8):
            f4.write(str(n) + ', ' + str(n+k))
            f4.write("\n")
            p1 = ve.get_centoid(path, k+num)
            p2 = ve.get_centoid(path, 0+num)
            dis = ve.euclideanDistance(p1, p2, 3)
            f6.write(str(np.round(dis, 4)))
            f6.write("\n")
        for k in range(2,8):
            f4.write(str(n+1) + ', ' + str(n+k))
            f4.write("\n")
            p1 = ve.get_centoid(path, k + num)
            p2 = ve.get_centoid(path, 1 + num)
            dis = ve.euclideanDistance(p1, p2, 3)
            f6.write(str(np.round(dis, 4)))
            f6.write("\n")
        for k in range(3,8):
            f4.write(str(n+2) + ', ' + str(n+k))
            f4.write("\n")
            p1 = ve.get_centoid(path, k + num)
            p2 = ve.get_centoid(path, 2 + num)
            dis = ve.euclideanDistance(p1, p2, 3)
            f6.write(str(np.round(dis, 4)))
            f6.write("\n")
        # DS_graph_labels.txt
        f2.write(str(labels[i]))
        f2.write("\n")
        node = node+1
if __name__ == '__main__':
    generate_glcmAndEfd()
import concurrent
import math
import os
import threading
import time
from enum import Enum

import xlwt
from scipy.spatial import distance
from tqdm import tqdm
import nrrd
import nibabel as nib
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

Position = Enum("pos", ('右眼内侧上方', '右眼外侧上方', '右眼外侧下方', '右眼内侧下方', '左眼外侧上方', '左眼内侧上方', '左眼内侧下方', '左眼外侧下方', '左眼无肿瘤', '右眼无肿瘤'))
def getOrigin(data_file, label_file, num_class):
    img_data = nib.load(data_file)
    data = np.asarray(img_data.get_fdata())
    img_label = nib.load(label_file)
    label = np.asarray(img_label.get_fdata())
    [rows, cols, slices] = data.shape
    for i in range(rows):
        for j in range(cols):
            for k in range(slices):
                if label[i, j, k] != num_class:
                    data[i, j, k] = 0
    return data
def get_mid(re, le):
    for i in range(0, len(re)):
        re[i] = (re[i] + le[i])/2
    return re

def getOrigin_gray(data_file, label_file, num_class):
    img_data = nib.load(data_file)
    data = np.asarray(img_data.get_fdata())
    img_label = nib.load(label_file)
    label = np.asarray(img_label.get_fdata())
    [rows, cols, slices] = data.shape
    for i in range(rows):
        for j in range(cols):
            for k in range(slices):
                if label[i, j, k] == 1 or label[i, j, k] == 9:
                    data[i, j, k] = 255
                else:
                    data[i, j, k] = 0
    return data
def getOrigin_gray(data_file, label_file, num_class):
    img_data = nib.load(data_file)
    data = np.asarray(img_data.get_fdata())
    img_label = nib.load(label_file)
    label = np.asarray(img_label.get_fdata())
    [rows, cols, slices] = data.shape
    for i in range(rows):
        for j in range(cols):
            for k in range(slices):
                if label[i, j, k] == num_class:
                    data[i, j, k] = 255
                else:
                    data[i, j, k] = 0
    return data
def calculate_label(nii_file, num_class):
    img = nib.load(nii_file)
    nii_header = img.header
    # print(nii_header['pixdim'])
    v_pix = nii_header['pixdim'][1] * nii_header['pixdim'][2] * nii_header['pixdim'][3]
    data = np.asarray(img.get_fdata())
    [rows, cols, slices] = data.shape
    count = 0
    for i in range(rows):
        for j in range(cols):
            for k in range(slices):
                if data[i, j, k] == num_class:
                    count+=1
    return int(count*v_pix)
def calculate_max_diameter(nii_file, num_class):
    img = nib.load(nii_file)
    nii_header = img.header
    print(nii_header['pixdim'][3])
    data = np.asarray(img.get_fdata())
    node_1, node_2 = max_diameter(data, num_class)
    node_1 = [nii_header['pixdim'][1]*node_1[0], nii_header['pixdim'][2]*node_1[1], nii_header['pixdim'][3]*node_1[2]]
    node_2 = [nii_header['pixdim'][1] * node_2[0], nii_header['pixdim'][2] * node_2[1],
              nii_header['pixdim'][3] * node_2[2]]
    return distance.euclidean(node_1, node_2)
def max_diameter(array, num_class):
    [rows, cols, slices] = array.shape
    points = []
    for i in range(rows):
        for j in range(cols):
            for k in range(slices):
                if array[i,j,k] == num_class:
                    points.append([i,j,k])
    if len(points)==0:
        return [0, 0, 0], [0, 0, 0]
    max_diameter = 0
    max_set1 = 0
    max_set2 = 0
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            d = distance.euclidean(points[i], points[j])
            if d > max_diameter:
                max_set1 = i
                max_set2 = j
                max_diameter = d

    return points[max_set1], points[max_set2]
def get_centoid_plane(nii_file, num_class):
    img = nib.load(nii_file)
    nii_header = img.header
    data = np.asarray(img.get_fdata())
    [rows, cols, slices] = data.shape
    count = 0
    sum_x = 0
    sum_y = 0
    sum_z = 0
    for i in range(rows):
        for j in range(cols):
            for k in range(slices):
                if data[i, j, k] == num_class:
                    count += 1
                    sum_x += i
                    sum_y += j
                    sum_z += k
    if count == 0:
        return [0, 0, 0]
    sum_x = sum_x * nii_header['pixdim'][1] / count
    sum_y = sum_y * nii_header['pixdim'][2] / count
    sum_z = sum_z * nii_header['pixdim'][3] / count
    return [int(sum_x), int(sum_y), int(sum_z)]
def get_centoid_plane(nii_file, num_class):
    img = nib.load(nii_file)
    nii_header = img.header
    data = np.asarray(img.get_fdata())
    [rows, cols, slices] = data.shape
    result = []
    for k in range(slices):
        count = 0
        sum_x = 0
        sum_y = 0
        sum_z = 0
        for i in range(rows):
            for j in range(cols):
                if data[i, j, k] == num_class:
                    count += 1
                    sum_x += i
                    sum_y += j
                    sum_z += k
        if count == 0:
            continue
        sum_x = sum_x * nii_header['pixdim'][1] / count
        sum_y = sum_y * nii_header['pixdim'][2] / count
        sum_z = sum_z * nii_header['pixdim'][3] / count
        result.append([int(sum_x), int(sum_y), int(sum_z)])
    return result
def get_centoid(nii_file, num_class):
    if num_class == 2 | num_class == 10:
        return get_mid(get_centoid(nii_file, 3), get_centoid(nii_file, 11))
    img = nib.load(nii_file)
    nii_header = img.header
    data = np.asarray(img.get_fdata())
    [rows, cols, slices] = data.shape
    count = 0
    sum_x = 0
    sum_y = 0
    sum_z = 0
    for i in range(rows):
        for j in range(cols):
            for k in range(slices):
                if data[i, j, k] == num_class:
                    count += 1
                    sum_x += i
                    sum_y += j
                    sum_z += k
    if count == 0:
        return [0, 0, 0]
    sum_x = sum_x * nii_header['pixdim'][1] / count
    sum_y = sum_y * nii_header['pixdim'][2] / count
    sum_z = sum_z * nii_header['pixdim'][3] / count
    return [int(sum_x), int(sum_y), int(sum_z)]


def get_right_position(lym, eye, sr, ur, ir, er):
    y = get_point_status(lym, eye, ir, er)
    x = get_point_status(lym, eye, ur, sr)
    if x > 0 and y > 0:
        return 1
    elif x < 0 < y:
        return 2
    elif x < 0 and y < 0:
        return 3
    elif x > 0 > y:
        return 4


def get_left_position(lym, eye, sr, ur, ir, er):
    y = get_point_status(lym, eye, er, ir)
    x = get_point_status(lym, eye, ur, sr)

    if x > 0 and y > 0:
        return 5
    elif x < 0 < y:
        return 6
    elif x < 0 and y < 0:
        return 7
    elif x > 0 > y:
        return 8


def get_point_status(p0, p1, p2, p3):
    a = (p2[1]-p1[1])*(p3[2]-p1[2])-(p3[1]-p1[1])*(p2[2]-p1[2])
    b = (p2[2]-p1[2])*(p3[0]-p1[0])-(p3[2]-p1[2])*(p2[0]-p1[0])
    c = (p2[0]-p1[0])*(p3[1]-p1[1])-(p3[0]-p1[0])*(p2[1]-p1[1])
    result = a*(p0[0]-p1[0]) + b*(p0[1]-p1[1]) + c*(p0[2]-p1[2])
    return result


def isInRange(B, error):
    if B <= error:
        return False
    else:
        return True

def euclideanDistance(instance1,instance2,dimension):
    distance = 0
    for i in range(dimension):
        distance += (instance1[i] - instance2[i])**2

    return math.sqrt(distance)

def get_position_description(nii_file, flag):
    pos = [[0]*3]*17
    for i in range(1,17):
        pos[i] = get_centoid(nii_file, i)
    left_lym = calculate_label(nii_file, 1)
    right_lym = calculate_label(nii_file, 9)
    print(left_lym)
    print(right_lym)
    left_des = 9
    if isInRange(left_lym, 300):
        if flag:
            left_des = get_left_position(pos[1], pos[3], pos[4], pos[5], pos[6], pos[7])
        else:
            under_shift = pos[3]
            under_shift[2] -= 1
            right_shift = pos[3]
            right_shift[0] += 1
            left_des = get_left_position(pos[1], pos[3], pos[8], under_shift, pos[8], right_shift)

    right_des = 10
    if isInRange(right_lym, 300):
        if flag:
            right_des = get_right_position(pos[9], pos[11], pos[12], pos[13], pos[14], pos[15])
        else:
            under_shift = pos[11]
            under_shift[2] -= 1
            right_shift = pos[11]
            right_shift[0] += 1
            right_des = get_right_position(pos[9], pos[11], pos[16], under_shift, pos[16], right_shift)
            print(under_shift)
            print(right_shift)
    return Position(left_des).name + " " + Position(right_des).name


def get_compared_portion(file1, file2, num_class):
    v1 = calculate_label(file1, num_class)
    v2 = calculate_label(file2, num_class)
    print('比例：{:.0%}'.format(v2/v1))
    return v2/v1
def get_excel_output(predict, excel_name):
    file_path = predict + os.sep+ excel_name+ '.xlsx'  # sys.path[0]为要获取当前路径，filenamelist为要写入的文件
    f = xlwt.Workbook(encoding='utf-8', style_compression=0)  # 新建一个excel
    sheet = f.add_sheet('sheet1')  # 新建一个sheet
    fileList = os.listdir(predict)  # 文件放置在当前文件夹中，用来获取当前文件夹内所有文件目录

    i = 0  # 将文件列表写入test.xls
    for s in tqdm(fileList):
        path = predict + os.sep + s
        vl = calculate_label(path, 1)
        vr = calculate_label(path, 9)
        sheet.write(i, 0, s)  # 参数i,0,s分别代表行，列，写入值
        sheet.write(i, 1, vl)
        sheet.write(i, 2, vr)
        sheet.write(i, 3, vr+vl)
        i = i + 1
    f.save(file_path)
def get_pixdim(path):
    fileList = os.listdir(path)
    i =  0
    for file in fileList:
        img = nib.load(path+os.sep+file)
        nii_header = img.header
        print(file, ": ", nii_header['pixdim'][1])
        i+=1

def get_filelist():
    path = r'C:\joey\master\resource\lymphoma\PACS.Lymphoma.Spider\output'
    file_path = r'C:\Users\perlicue\Desktop\master_lecture\xiaowen' + os.sep + 'filelist' + '.xlsx'  # sys.path[0]为要获取当前路径，filenamelist为要写入的文件
    f = xlwt.Workbook(encoding='utf-8', style_compression=0)  # 新建一个excel
    sheet = f.add_sheet('sheet1')
    fileList = os.listdir(path)  # 文件放置在当前文件夹中，用来获取当前文件夹内所有文件目录
    try:
        i=0
        for s in tqdm(fileList):
            sheet.write(i, 0, s)  # 参数i,0,s分别代表行，列，写入值
            i+=1
    except Exception:
        f.save(file_path)

    f.save(file_path)
def get_max_diameter_excel(predict, excel_name):
    file_path = r'C:\Users\perlicue\Desktop\master_lecture\xiaowen' + os.sep+ excel_name+ '.xlsx'  # sys.path[0]为要获取当前路径，filenamelist为要写入的文件
    f = xlwt.Workbook(encoding='utf-8', style_compression=0)  # 新建一个excel
    sheet = f.add_sheet('sheet1')  # 新建一个sheet
    fileList = os.listdir(predict)  # 文件放置在当前文件夹中，用来获取当前文件夹内所有文件目录
    try:
        i = 0  # 将文件列表写入test.xls
        for s in tqdm(fileList):
            path = predict + os.sep + s
            vl = calculate_max_diameter(path, 1)
            vr = calculate_max_diameter(path, 9)
            sheet.write(i, 0, s)  # 参数i,0,s分别代表行，列，写入值
            sheet.write(i, 1, vl)
            sheet.write(i, 2, vr)
            i = i + 1
    except Exception:
        f.save(file_path)


    f.save(file_path)
def task(s):
    # 在这里写每个循环需要执行的任务
    print("线程{}正在执行第{}次循环".format(threading.current_thread().name, i))
    time.sleep(1)

def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        for i in range(10):
            executor.submit(task, i)
if __name__ == '__main__':
    nii_file = r"C:\Users\perlicue\Desktop\master_lecture\xiaowen\volume_cal2\pre_out"
    nii_file2 = r"C:\Users\perlicue\Desktop\分割结果\50例结果\lymphoma_040.nii.gz"
    num_class = 3
    start_time = time.time()  # 记录代码开始执行的时间
    result = calculate_max_diameter(nii_file, num_class)
    print(get_pixdim(nii_file))
    get_filelist()
    print(result)


    # 在这里写需要计时的代码

    end_time = time.time()  # 记录代码执行结束的时间

    time_cost = end_time - start_time  # 计算代码执行的时间差

    print("代码执行时间：{}秒".format(time_cost))
    result2 =  calculate_label(nii_file2, num_class)
    print("result1 : ", str(result))
    print("result2 : " + str(result2))
    print("proportion : " + str(result2/result))

    point = get_centoid(nii_file, num_class)
    point2 = get_centoid(nii_file2, num_class)
    print(point)
    print(point2)
    plt.figure()
    ax = plt.subplot(111, projection='3d')
    ax.set_xlim(0, 200)  # X轴，横向向右方向
    ax.set_ylim(200, 0)  # Y轴,左向与X,Z轴互为垂直
    ax.set_zlim(0, 200)  # 竖向为Z轴
    ax.scatter([point[0]],[point[1]],point[2])
    # 肿瘤
    point = get_centoid(nii_file, 1)
    ax.scatter([point[0]], [point[1]], point[2])
    for i in range(1,17):
        point = get_centoid(nii_file, i)
        print(i)
        print("---")
        print(point)
        ax.scatter([point[0]], [point[1]], point[2])

    plt.show()
    p0 = [0, 0, 0];
    p1 = [1, 0, 0];
    p2 = [0, 1, 0];
    p3 = [0, 0, 1];
    result = get_point_status(p0, p1, p2, p3)
    print(result)
    result = get_position_description(nii_file2,True)
    get_compared_portion(nii_file, nii_file2, 3)
    print(result)
    path = r"C:\Users\perlicue\Desktop\master_lecture\xiaowen\volume_cal2\post_34"
    get_max_diameter_excel(path, "get_max_diameter_excel2")

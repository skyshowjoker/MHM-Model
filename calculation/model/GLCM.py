#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os

import cv2
import math
import numpy as np

#定义最大灰度级数
from calculation.volumn_estimate import getOrigin, calculate_label, get_centoid

gray_level = 16

def maxGrayLevel(img):
    max_gray_level=0
    (height,width)=img.shape
    # print ("图像的高宽分别为：height,width", height, width)
    for y in range(height):
        for x in range(width):
            if img[y][x] > max_gray_level:
                max_gray_level = img[y][x]
    # print("max_gray_level:",max_gray_level)
    return max_gray_level+1

def getGlcm(input,d_x,d_y):
    srcdata=input.copy()
    ret=[[0.0 for i in range(gray_level)] for j in range(gray_level)]
    (height,width) = input.shape

    max_gray_level=maxGrayLevel(input)
    #若灰度级数大于gray_level，则将图像的灰度级缩小至gray_level，减小灰度共生矩阵的大小
    if max_gray_level > gray_level:
        for j in range(height):
            for i in range(width):
                srcdata[j][i] = srcdata[j][i]*gray_level / max_gray_level

    for j in range(height-d_y):
        for i in range(width-d_x):
            rows = srcdata[j][i]
            cols = srcdata[j + d_y][i+d_x]
            ret[rows][cols]+=1.0

    for i in range(gray_level):
        for j in range(gray_level):
            ret[i][j]/=float(height*width)

    return ret

def feature_computer(p):
    #con:对比度反应了图像的清晰度和纹理的沟纹深浅。纹理越清晰反差越大对比度也就越大。
    #eng:熵（Entropy, ENT）度量了图像包含信息量的随机性，表现了图像的复杂程度。当共生矩阵中所有值均相等或者像素值表现出最大的随机性时，熵最大。
    #agm:角二阶矩（能量），图像灰度分布均匀程度和纹理粗细的度量。当图像纹理均一规则时，能量值较大；反之灰度共生矩阵的元素值相近，能量值较小。
    #idm:反差分矩阵又称逆方差，反映了纹理的清晰程度和规则程度，纹理清晰、规律性较强、易于描述的，值较大。
    Con=0.0
    Eng=0.0
    Asm=0.0
    Idm=0.0
    for i in range(gray_level):
        for j in range(gray_level):
            Con+=(i-j)*(i-j)*p[i][j]
            Asm+=p[i][j]*p[i][j]
            Idm+=p[i][j]/(1+(i-j)*(i-j))
            if p[i][j]>0.0:
                Eng+=p[i][j]*math.log(p[i][j])
    return Asm,Con,-Eng,Idm
def get_mask(data_file, label_file):
    p = np.zeros((8, 3), dtype=int)
    LAL = calculate_label(label_file, 1)
    RAL = calculate_label(label_file, 9)
    if LAL < 50 & RAL < 50:
        return np.zeros(1)
    elif LAL > RAL:
        return getOrigin(data_file, label_file, 1)
    else:
        return getOrigin(data_file, label_file, 9)

def get_glcm_by(num, i):
    label_file = r"C:\joey\master\resource\lymphoma\volume_calculate\12_Aug" + os.sep + str(num) + r".nii.gz"
    data_file = r"C:\joey\master\resource\lymphoma\volume_calculate\nii_list_aug" + os.sep + str(num) + r".nii.gz"
    vol = calculate_label(label_file, i)
    asm = 1
    con = 1
    eng = 1
    idm = 1
    if vol < 1:
        return [asm, con, eng, idm]
    else:
        data = getOrigin(data_file, label_file, i)
    glcm = np.zeros((16, 16), dtype=int)

    for j in range(data.shape[2]):
        glcm = glcm + getGlcm(data[:, :, j].astype(int), 1, 0)
        a, b, c, d = feature_computer(glcm)
        asm += a
        con += b
        eng += c
        idm += d
    # glcm_0 = getGlcm(img_gray, 1, 0)
    # glcm_1=getGlcm(src_gray, 0,1)
    # glcm_2=getGlcm(src_gray, 1,1)
    # glcm_3=getGlcm(src_gray, -1,1)
    return [asm, con, eng, idm]
    # return asm+con+eng+idm
def get_glcm(num):
    # img = cv2.imread(image_name)
    # print(img.shape)
    # try:
    #     img_shape=img.shape
    # except:
    #     print ('imread error')
    #     return
    code = "lymphoma_%03.0d" % int(num)
    label_file = r"C:\Users\perlicue\Desktop\spacial_feature\multi_seq_train\seqs\labelsTr" + os.sep + code + r".nii.gz"
    data_file = r"C:\Users\perlicue\Desktop\spacial_feature\multi_seq_train\seqs\00" + os.sep + code + r"_0000.nii.gz"
    data = get_mask(data_file, label_file)
    if data.shape == np.zeros(1).shape:
        return [0, 0, 0, 0]
    #这里如果用‘/’会报错TypeError: integer argument expected, got float
    #其实主要的错误是因为 因为cv2.resize内的参数是要求为整数
    # img=cv2.resize(img,(img_shape[1]//2,img_shape[0]//2),interpolation=cv2.INTER_CUBIC)
    # print(img.shape)
    # img_gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # print(img_gray.shape)
    glcm = np.zeros((16, 16), dtype=int)
    for i in range(data.shape[2]):
        glcm = glcm + getGlcm(data[:, :, i].astype(int), 1,0)
    # glcm_0 = getGlcm(img_gray, 1, 0)
    #glcm_1=getGlcm(src_gray, 0,1)
    #glcm_2=getGlcm(src_gray, 1,1)
    #glcm_3=getGlcm(src_gray, -1,1)
    asm, con, eng, idm = feature_computer(glcm)

    return [asm, con, eng, idm]

if __name__=='__main__':
    result = get_glcm(r"C:\Users\perlicue\Pictures\test.jpg")
    print(result)
    # label_file = r"C:\joey\master\resource\lymphoma\volume_calculate\11_new\lymphoma_lymphoma_000.nii.gz"
    # data_file = r"C:\joey\master\resource\lymphoma\volume_calculate\nii_list-0000\lymphoma_lymphoma_000_0000.nii.gz"
    # getOrigin(data_file, label_file)
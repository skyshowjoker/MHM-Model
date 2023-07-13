import math
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
import time
import matplotlib.pyplot as plt
import cv2
from PIL import Image
import os
from skimage.feature import greycomatrix, greycoprops

def get_img(s): # s为图像路径
    values_temp = []
    input = cv2.imread(s, cv2.IMREAD_GRAYSCALE) # 读取图像，灰度模式
    # 得到共生矩阵，参数：图像矩阵，距离，方向，灰度级别，是否对称，是否标准化
    # [0, np.pi / 4, np.pi / 2, np.pi * 3 / 4] 一共计算了四个方向，你也可以选择一个方向
    # 统计得到glcm
    glcm = greycomatrix(input, [2, 8, 16], [0, np.pi / 4, np.pi / 2, np.pi * 3 / 4], 256, symmetric=True, normed=True)  # , np.pi / 4, np.pi / 2, np.pi * 3 / 4
    print(glcm.shape)
    # 循环计算表征纹理的参数
    for prop in {'contrast', 'dissimilarity','homogeneity', 'energy', 'correlation', 'ASM'}:
        temp = greycoprops(glcm, prop)
        # temp=np.array(temp).reshape(-1)
        values_temp.append(temp)
        print(prop, temp)
        print('len:',len(temp))
        print('')
    return (values_temp)
values = []
if __name__ == '__main__':

    temp_ = get_img(r'C:\Users\perlicue\Pictures\test.jpg')
    print(temp_)
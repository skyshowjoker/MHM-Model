import random

import numpy as np
from scipy import stats
from sklearn.model_selection import train_test_split

from calculation.model.classifier1 import loadDataSet

def test_fc(data1, data2):
    # 进行Levene’s方差齐性检验
    stat, p = stats.levene(data1, data2)

    # 打印测试结果
    print('Levene’s统计量：', stat)
    print('p值：', p)

    # 根据p值进行假设检验
    alpha = 0.05
    if p > alpha:
        print('样本方差相等')
    else:
        print('样本方差不相等')
def test_zt(data):
    stat, p = stats.shapiro(data)

    # 打印测试结果
    print('Shapiro-Wilk统计量：', stat)
    print('p值：', p)

    # 根据p值进行假设检验
    alpha = 0.05
    if p > alpha:
        print('样本数据符合正态分布')
    else:
        print('样本数据不符合正态分布')
def m(vol):
    file_path = r"C:\Users\perlicue\Desktop\data\feature_glcm_enhance.txt"

    data, target = loadDataSet(file_path)
    x = []
    y = []
    for i in range(134):
        if target[i] == 1.0:  # no_emzl
            x.append(data[i][vol])
        else:
            y.append(data[i][vol])
    kruskal = stats.kruskal(x, y)
    # print(x)
    # result = stats.kruskal(data[0], data[10])
    print('----')
    print(vol)
    print('----no_emzl')
    # print("median", np.median(x))
    # # print(np.std(x))
    # print("min", np.min(x))
    # print("max", np.max(x))
    result = str(np.round(np.median(x), 2)) + '(' + str(np.round(np.min(x), 2))
    result += '-' + str(np.round(np.max(x), 2)) + ')'
    print(result)
    # print("median", np.median(y))
    #
    # # print(np.std(y))
    # print("min", np.min(y))
    # print("max", np.max(y))
    result = str(np.round(np.median(y), 2)) + '(' + str(np.round(np.min(y), 2))
    result += '-' + str(np.round(np.max(y), 2)) + ')'
    print(result)
    print(kruskal)
    # print(test_fc(x, y))
    # print(test_zt(data))



if __name__ == '__main__':

    for i in range(4):
        m(i)


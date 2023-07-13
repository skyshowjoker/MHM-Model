#  14.4 特征提取之傅里叶描述子 Elliptical Fourier Descriptors
import os

import cv2
import numpy as np
from matplotlib import pyplot as plt
from numpy import float64

from calculation.volumn_estimate import getOrigin, calculate_label, get_centoid, getOrigin_gray


def truncFFT(fftCnt, pLowF=64):  # 截短傅里叶描述子
        fftShift = np.fft.fftshift(fftCnt)  # 中心化，将低频分量移动到频域中心
        center = int(len(fftShift)/2)
        low, high = center - int(pLowF/2), center + int(pLowF/2)
        fftshiftLow = fftShift[low:high]
        fftLow = np.fft.ifftshift(fftshiftLow)  # 逆中心化
        return fftLow

def reconstruct(img, fftCnt, scale, ratio=1.0):  # 由傅里叶描述子重建轮廓图
    pLowF = int(fftCnt.shape[0] * ratio)  # 截短长度 P<=K
    fftLow = truncFFT(fftCnt, pLowF)  # 截短傅里叶描述子，删除高频系数
    ifft = np.fft.ifft(fftLow)  # 傅里叶逆变换 (P,)
    # cntRebuild = np.array([ifft.real, ifft.imag])  # 复数转为数组 (2, P)
    # cntRebuild = np.transpose(cntRebuild)  # (P, 2)
    cntRebuild = np.stack((ifft.real, ifft.imag), axis=-1)  # 复数转为数组 (P, 2)
    if cntRebuild.min() < 0:
         cntRebuild -= cntRebuild.min()
    cntRebuild *= scale / cntRebuild.max()
    cntRebuild = cntRebuild.astype(np.int32)
    # print("ratio={}, fftCNT:{}, fftLow:{}".format(ratio, fftCnt.shape, fftLow.shape))

    rebuild = np.ones(img.shape, np.uint8)*255  # 创建空白图像
    cv2.rectangle(rebuild, (2,3), (568,725), (0,0,0), )  # 绘制边框
    cv2.polylines(rebuild, [cntRebuild], True, 0, thickness=2)  # 绘制多边形，闭合曲线
    return rebuild

    # 特征提取之傅里叶描述子
def get_EFD(gray):

    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)
    # print(gray.shape)  # (727, 570)

    # 寻找二值化图中的轮廓，method=cv2.CHAIN_APPROX_NONE 输出轮廓的每个像素点
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # OpenCV4~
    cnts = sorted(contours, key=cv2.contourArea, reverse=True)  # 所有轮廓按面积排序
    cnt = cnts[0]  # 第 0 个轮廓，面积最大的轮廓，(664, 1, 2)
    cntPoints = np.squeeze(cnt)  # 删除维度为 1 的数组维度，(2867, 1, 2)->(2867,2)
    lenCnt = cnt.shape[0]  # 轮廓点的数量
    # print("length of max contour:", lenCnt)
    imgCnts = np.zeros(gray.shape[:2], np.uint8)  # 创建空白图像
    cv2.drawContours(imgCnts, cnt, -1, (255, 255, 255), 2)  # 绘制轮廓

    # 离散傅里叶变换，生成傅里叶描述子 fftCnt
    cntComplex = np.empty(cntPoints.shape[0], dtype=complex)  # 声明复数数组 (2867,)
    cntComplex = cntPoints[:, 0] + 1j * cntPoints[:, 1]  # (xk,yk)->xk+j*yk
    # print("cntComplex", cntComplex.shape)
    fftCnt = np.fft.fft(cntComplex)  # 离散傅里叶变换，生成傅里叶描述子

    # 由全部傅里叶描述子重建轮廓曲线
    scale = cntPoints.max()  # 尺度系数
    rebuild = reconstruct(gray, fftCnt, scale)  # 傅里叶逆变换重建轮廓曲线，傅里叶描述子 (2866,)
    # 由截短傅里叶系数重建轮廓曲线
    # rebuild1 = reconstruct(gray, fftCnt, scale, ratio=0.2)  # 截短比例 20%，傅里叶描述子 (572,)
    # rebuild2 = reconstruct(gray, fftCnt, scale, ratio=0.05)  # 截短比例 5%，傅里叶描述子 (142,)
    # rebuild3 = reconstruct(gray, fftCnt, scale, ratio=0.02)  # 截短比例 2%，傅里叶描述子 (56,)
    # plt.figure(figsize=(9, 6))
    # plt.subplot(221), plt.axis('off'), plt.title("Origin")
    # plt.imshow(cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))
    # plt.subplot(222), plt.axis('off'), plt.title("Contour")
    # plt.imshow(cv2.cvtColor(imgCnts, cv2.COLOR_BGR2RGB))
    # plt.subplot(223), plt.axis('off'), plt.title("rebuild (100%)")
    # plt.imshow(cv2.cvtColor(rebuild, cv2.COLOR_BGR2RGB))
    # plt.subplot(224), plt.axis('off'), plt.title("rebuild1 (20%)")
    # plt.imshow(cv2.cvtColor(rebuild1, cv2.COLOR_BGR2RGB))

    # plt.figure(figsize=(9, 6))
    # plt.subplot(231), plt.axis('off'), plt.title("Origin")
    # plt.imshow(cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))
    # plt.subplot(232), plt.axis('off'), plt.title("Contour")
    # plt.imshow(cv2.cvtColor(imgCnts, cv2.COLOR_BGR2RGB))
    # plt.subplot(233), plt.axis('off'), plt.title("rebuild (100%)")
    # plt.imshow(cv2.cvtColor(rebuild, cv2.COLOR_BGR2RGB))
    # plt.subplot(234), plt.axis('off'), plt.title("rebuild1 (20%)")
    # plt.imshow(cv2.cvtColor(rebuild1, cv2.COLOR_BGR2RGB))
    # plt.subplot(235), plt.axis('off'), plt.title("rebuild2 (5%)")
    # plt.imshow(cv2.cvtColor(rebuild2, cv2.COLOR_BGR2RGB))
    # plt.subplot(236), plt.axis('off'), plt.title("rebuild3 (2%)")
    # plt.imshow(cv2.cvtColor(rebuild3, cv2.COLOR_BGR2RGB))
    # plt.tight_layout()
    # plt.show()
    return fftCnt
def get_efd_feature_by_label(num, label):
    # img = cv2.imread(image_name)
    # print(img.shape)
    # try:
    #     img_shape=img.shape
    # except:
    #     print ('imread error')
    #     return

    label_file = r"C:\joey\master\resource\lymphoma\volume_calculate\12_Aug" + os.sep + str(num) + r".nii.gz"
    data_file = r"C:\joey\master\resource\lymphoma\volume_calculate\nii_list_aug" + os.sep + str(num) + r".nii.gz"
    data = getOrigin_gray(data_file, label_file, label)
    [_, _, plane] = data.shape
    #这里如果用‘/’会报错TypeError: integer argument expected, got float
    #其实主要的错误是因为 因为cv2.resize内的参数是要求为整数
    # img=cv2.resize(img,(img_shape[1]//2,img_shape[0]//2),interpolation=cv2.INTER_CUBIC)
    # print(img.shape)
    # img_gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # print(img_gray.shape)
    # efd = np.zeros((16, 16), dtype=int)
    param = 20
    result = np.zeros(param)
    # print(plane)
    if plane > 14:
        plane = 14
    for i in range(0, plane):
        try:
            efd = get_EFD(data[:, :, i].astype("uint8"))
            if len(efd) < param:
                continue
            result += np.asarray(efd[0:param], dtype=float64)
        except IndexError:
            continue
    # for i in range(data.shape[2]):
    #     efd = get_EFD(data[:, :, i].astype(int))



    return result
def get_efd_feature(num):
    # img = cv2.imread(image_name)
    # print(img.shape)
    # try:
    #     img_shape=img.shape
    # except:
    #     print ('imread error')
    #     return

    label_file = r"C:\joey\master\resource\lymphoma\volume_calculate\12_Aug" + os.sep + str(num) + r".nii.gz"
    data_file = r"C:\joey\master\resource\lymphoma\volume_calculate\nii_list_aug" + os.sep + str(num) + r".nii.gz"
    data = getOrigin_gray(data_file, label_file, num)
    [_, _, plane] = data.shape
    #这里如果用‘/’会报错TypeError: integer argument expected, got float
    #其实主要的错误是因为 因为cv2.resize内的参数是要求为整数
    # img=cv2.resize(img,(img_shape[1]//2,img_shape[0]//2),interpolation=cv2.INTER_CUBIC)
    # print(img.shape)
    # img_gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # print(img_gray.shape)
    # efd = np.zeros((16, 16), dtype=int)
    result = np.zeros(5)
    # print(plane)
    if plane > 14:
        plane = 14
    for i in range(0, plane):
        try:
            efd = get_EFD(data[:, :, i].astype("uint8"))
            if len(efd) < 5:
                continue
            result += np.asarray(efd[0:5], dtype=float64)
        except IndexError:
            print("exception ")
            print(i)
            continue
    # for i in range(data.shape[2]):
    #     efd = get_EFD(data[:, :, i].astype(int))



    return result

def excute():
    img = cv2.imread(r"C:\Users\perlicue\Pictures\test2.png", flags=1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 灰度图像
    print(gray)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)
    print(gray.shape)  # (727, 570)

    # 寻找二值化图中的轮廓，method=cv2.CHAIN_APPROX_NONE 输出轮廓的每个像素点
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)  # OpenCV4~
    cnts = sorted(contours, key=cv2.contourArea, reverse=True)  # 所有轮廓按面积排序
    cnt = cnts[0]  # 第 0 个轮廓，面积最大的轮廓，(664, 1, 2)
    cntPoints = np.squeeze(cnt)  # 删除维度为 1 的数组维度，(2867, 1, 2)->(2867,2)
    lenCnt = cnt.shape[0]  # 轮廓点的数量
    # print("length of max contour:", lenCnt)
    imgCnts = np.zeros(gray.shape[:2], np.uint8)  # 创建空白图像
    cv2.drawContours(imgCnts, cnt, -1, (255, 255, 255), 2)  # 绘制轮廓

    # 离散傅里叶变换，生成傅里叶描述子 fftCnt
    cntComplex = np.empty(cntPoints.shape[0], dtype=complex)  # 声明复数数组 (2867,)
    cntComplex = cntPoints[:, 0] + 1j * cntPoints[:, 1]  # (xk,yk)->xk+j*yk
    # print("cntComplex", cntComplex.shape)
    fftCnt = np.fft.fft(cntComplex)  # 离散傅里叶变换，生成傅里叶描述子
    print("length of max contour:", fftCnt.shape)
    # print(fftCnt)
    # 由全部傅里叶描述子重建轮廓曲线
    scale = cntPoints.max()  # 尺度系数
    rebuild = reconstruct(img, fftCnt, scale)  # 傅里叶逆变换重建轮廓曲线，傅里叶描述子 (2866,)
    # 由截短傅里叶系数重建轮廓曲线
    rebuild1 = reconstruct(img, fftCnt, scale, ratio=0.2)  # 截短比例 20%，傅里叶描述子 (572,)
    rebuild2 = reconstruct(img, fftCnt, scale, ratio=0.05)  # 截短比例 5%，傅里叶描述子 (142,)
    rebuild3 = reconstruct(img, fftCnt, scale, ratio=0.02)  # 截短比例 2%，傅里叶描述子 (56,)

    plt.figure(figsize=(9, 6))
    plt.subplot(231), plt.axis('off'), plt.title("Origin")
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.subplot(232), plt.axis('off'), plt.title("Contour")
    plt.imshow(cv2.cvtColor(imgCnts, cv2.COLOR_BGR2RGB))
    plt.subplot(233), plt.axis('off'), plt.title("rebuild (100%)")
    plt.imshow(cv2.cvtColor(rebuild, cv2.COLOR_BGR2RGB))
    plt.subplot(234), plt.axis('off'), plt.title("rebuild1 (20%)")
    plt.imshow(cv2.cvtColor(rebuild1, cv2.COLOR_BGR2RGB))
    plt.subplot(235), plt.axis('off'), plt.title("rebuild2 (5%)")
    plt.imshow(cv2.cvtColor(rebuild2, cv2.COLOR_BGR2RGB))
    plt.subplot(236), plt.axis('off'), plt.title("rebuild3 (2%)")
    plt.imshow(cv2.cvtColor(rebuild3, cv2.COLOR_BGR2RGB))
    plt.tight_layout()
    plt.show()
if __name__=='__main__':
    # excute()
    result = get_efd_feature(47)
    # np.round(result, 4)
    print(len(result))
    print(result)
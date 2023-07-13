import numpy
import numpy as np
from sklearn.cluster import KMeans
import sys

from calculation.utils.util import cal_score
if __name__ == '__main__':
    sys.path.append("..")
    from calculation.model import classifier2

    data = np.random.rand(100, 3)  # 生成一个随机数据，样本大小为100, 特征数为3
    X, y = svm.loadDataSet(r"../data/wd_134_A.txt")
    X = numpy.array(X)
    y = numpy.array(y)
    # 假如我要构造一个聚类数为3的聚类器
    estimator = KMeans(n_clusters=1)  # 构造聚类器
    estimator.fit(X)  # 聚类
    print(y)
    label_pred = estimator.labels_  # 获取聚类标签
    centroids = estimator.cluster_centers_  # 获取聚类中心
    inertia = estimator.inertia_  # 获取聚类准则的总和
    print(label_pred)
    print(centroids)
    print(inertia)
    print(cal_score(y, label_pred))
    # 4 16
    # 17 64
    # 13 50
    # 81
    # 50 13
    # 16 4
    # 准确率：0.77
    # 假阳：13
    # 假阴：16
    # 假阳性率：0.76
    # 假阴性率：0.24

    # 2

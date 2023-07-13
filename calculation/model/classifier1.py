import os
import random

import xlwt
from xgboost import XGBClassifier
import numpy as np
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import roc_auc_score
from sklearn import metrics

from calculation.utils.util import cal_score

fold = 20
parameters = {
    'max_depth': [1,2,3,4,5, 10, 15, 20, 25],
    'learning_rate': [0.01, 0.02, 0.05, 0.1, 0.15],
    'n_estimators': [50, 100, 200, 300, 500],
    'min_child_weight': [0, 2, 5, 10, 20],
    'max_delta_step': [0, 0.2, 0.6, 1, 2],
    'subsample': [0.6, 0.7, 0.8, 0.85, 0.95],
    'colsample_bytree': [0.5, 0.6, 0.7, 0.8, 0.9],
    'reg_alpha': [0, 0.25, 0.5, 0.75, 1],
    'reg_lambda': [0.2, 0.4, 0.6, 0.8, 1],
    'scale_pos_weight': [0.2, 0.4, 0.6, 0.8, 1]
}
parameter = {

    'scale_pos_weight': [0.2, 0.4, 0.6, 0.8, 1]
}
def normalize(x):
    return (x - np.min(x)) / (np.max(x) - np.min(x))


def loadDataSet(filename):
    fr = open(filename)
    data = []
    label = []
    for line in fr.readlines():
        lineAttr = line.strip().split(' ')
        try:
            data.append([float(x) for x in lineAttr[:-1]])
            label.append(float(lineAttr[-1]))
        except ValueError:
            print(lineAttr)
    return data, label
def save_model(clf, filename='filename.pkl'):
    joblib.dump(clf, filename)

# version = str("_11_glcmAndwd")
version = str("wd_134_A")
# version = str("_11_all_mid")


def score(y, y_test):
    right_count = 0
    for i in range(len(y)):
        if y[i] == y_test[i]:
            right_count += 1
    return right_count / len(y)

def train(data, target, save_path):
    xlf = XGBClassifier(max_depth=5,
                            learning_rate=0.01,
                            n_estimators=100,
                            objective='binary:logistic',
                            nthread=-1,
                            gamma=0,
                            min_child_weight=5,
                            max_delta_step=0,
                            subsample=0.85,
                            colsample_bytree=0.7,
                            colsample_bylevel=1,
                            reg_alpha=0,
                            reg_lambda=1,
                            scale_pos_weight=0.2,
                            seed=1440,
                            missing=None)
    xlf = XGBClassifier(n_estimators=4, max_depth=5, learning_rate=1, objective='binary:logistic')
    xlf.fit(data, target)
    print(cal_score(target, xlf.predict(data)))
    print(xlf.get_booster().get_score())
    gsearch = GridSearchCV(xlf, param_grid=parameter, scoring='accuracy', cv=3)
    gsearch.fit(data, target)
    print("Best score: %0.3f" % gsearch.best_score_)
    print("Best parameters set:")

    best_parameters = gsearch.best_estimator_.get_params()
    for param_name in sorted(parameters.keys()):
        print("\t%s: %r" % (param_name, best_parameters[param_name]))
    # clf.fit(data[:-fold], target[:-fold])
    save_model(xlf, save_path)

def predict(data, target, path):
    clf = joblib.load(path)
    re = clf.predict(data)
    return re

def enough_test(data, target, n, model_path):
    acc = np.zeros(n)
    P = np.zeros(n)
    R = np.zeros(n)
    for i in range(0, n):
        random_num = random.randint(0, 1000)
        X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=.3, random_state=random_num)
        train(X_train, y_train, model_path)
        result = predict(X_test, y_test, model_path)
        acc[i], P[i], R[i] = cal_score(y_test, result)
    return np.mean(acc), np.mean(P), np.mean(R), np.std(acc), np.std(P), np.std(R)

def get_ROC():
    version = ["wd_134_A", "glcm_134_A", "glcmAndwd_134_A"]
    color = ["yellowgreen", "lightcoral", "mediumslateblue"]
    name = ["LSF" , "LTF" , "CLSTF"]
    plt.figure()
    lw = 2
    file = r"C:\Users\perlicue\Desktop\master_lecture" + '\\export2.xlsx'  # sys.path[0]为要获取当前路径，filenamelist为要写入的文件
    f = xlwt.Workbook(encoding='utf-8', style_compression=0)  # 新建一个excel
    sheet = f.add_sheet('sheet1')  # 新建一个sheet




    for i in range(0, len(version)):
        file_path = r"../data/" + version[i] + ".txt"
        model_path = r"../pkl/XGB_model" + version[i] + ".pkl"
        data1, target1 = loadDataSet(file_path)
        clf = joblib.load(model_path)
        y_pred_proba = clf.predict_proba(data1)
        j = 0  # 将文件列表写入test.xls
        for s in y_pred_proba[:, 1]:
            sheet.write(j+1, i+1, str(s))  # 参数i,0,s分别代表行，列，写入值
            j = j + 1
        print(y_pred_proba[:, 1])
        print(target1)
        fpr, tpr, thresholds = metrics.roc_curve(target1, y_pred_proba[:, 1], pos_label=1)
        print(i)
        # print(fpr)
        # print(tpr)
        # print(thresholds)

        roc_auc = metrics.auc(fpr, tpr)
        plt.plot(
            fpr,
            tpr,
            color=color[i],
            lw=lw,
            label="ROC curve of " + name[i] + "(area = %0.2f)" % roc_auc,
        )
    # clf = joblib.load(path)
    # y_pred_proba = clf.predict_proba(data)
    # fpr, tpr, thresholds = metrics.roc_curve(target, y_pred_proba[:, 1], pos_label=1)
    # roc_auc = metrics.auc(fpr, tpr)

    # f.save(file)

    plt.plot([0, 1], [0, 1], color="navy", lw=lw, linestyle="--")
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("Receiver-operating characteristic (ROC) curves")
    plt.legend(loc="lower right")
    plt.savefig('auc_roc.pdf')
    plt.show()

def batch(ver):
    param = []
    param.append("_11_WD"+ver)
    param.append("_11_WD_plane" + ver)
    param.append("_11_glcm" + ver)
    param.append("_11_EFD_norm5" + ver)
    param.append("_11_glcmAndwd" + ver)
    param.append("_11_glcmAndwd_plane" + ver)
    param.append("_11_glcmAndwd_planeAndEFD" + ver)

    for i in range(0, 7):
        file_path = r"../data/data" + param[i] + ".txt"
        model_path = r"../pkl/XGB_model" + param[i] + ".pkl"
        try:
            data, target = loadDataSet(file_path)
            X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=.3, random_state=62)
            train(X_train, y_train, model_path)
            result = predict(X_test, y_test, model_path)
        except:
            continue
        # get_ROC()
        print(file_path)
        print(y_test)
        print(result)
        print(cal_score(y_test, result))
        print(enough_test(data, target, 100, model_path))
if __name__ == '__main__':
    file_path = r"../data/" + version + ".txt"
    model_path = r"../pkl/XGB_model"+version+".pkl"
    # file = r"C:\Users\perlicue\Desktop\data\data_11_glcm_aug.txt"
    data, target = loadDataSet(file_path)
    X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=.3, random_state=62)

    target = [0 if i == -1 else 1 for i in target]
    train(X_train, X_test, model_path)

    enough_test(X_train, y_train, 80, model_path)

    result = predict(X_test, y_train, model_path)

    print(y_test)
    print(result)
    print(cal_score(y_test, result))
    print(enough_test(data, target, 1, model_path))

    batch("_aug")
    get_ROC()
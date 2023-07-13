import random

import pandas as pd
from sklearn import datasets
from sklearn import svm
import joblib
from sklearn import preprocessing
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report

from calculation import LE
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split

from calculation.utils.util import cal_score

fold = 20


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

# version = str("_11_glcm")


def score(y, y_test):
    right_count = 0
    for i in range(len(y)):
        if y[i] == y_test[i]:
            right_count += 1
    return right_count / len(y)
param_grid = {'C': [0.1,1, 10, 100],
              'gamma': [1,0.1,0.01,0.001],
              'kernel': ['rbf', 'poly', 'sigmoid']}
def grid_search(data, target):
    grid = GridSearchCV(SVC(), param_grid, refit=True, verbose=2)
    grid.fit(data, target)
    print(grid.best_estimator_)
    grid_predictions = grid.predict(X_test)
    print(confusion_matrix(y_test, grid_predictions))
    print(classification_report(y_test, grid_predictions))
def train(data, target, save_path):
    clf = svm.SVC(gamma=0.01, C=10.)
    clf.fit(data, target)
    save_model(clf, save_path)

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


version = str("_11_WD_aug")
def batch(ver):
    param = []
    param.append("_11_WD"+ver)
    param.append("_11_WD_plane2" + ver)
    param.append("_11_glcm" + ver)
    param.append("_11_EFD_norm5" + ver)
    param.append("_11_glcmAndwd" + ver)
    param.append("_11_glcmAndwd_plane" + ver)
    param.append("_11_glcmAndwd_planeAndEFD" + ver)

    for i in range(0, 7):
        file_path = r"../data/data" + param[i] + ".txt"
        model_path = r"../pkl/model" + param[i] + ".pkl"
        # try:
        #     data, target = loadDataSet(file_path)
        #     X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=.3, random_state=62)
        #     train(X_train, y_train, model_path)
        #     result = predict(X_test, y_test, model_path)
        # except:
        #     continue
        data, target = loadDataSet(file_path)
        X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=.3, random_state=62)
        train(X_train, y_train, model_path)
        # result = predict(X_test, y_test, model_path)
        # get_ROC()
        print(file_path)
        # print(y_test)
        # print(result)
        # print(cal_score(y_test, result))
        print(enough_test(data, target, 100, model_path))
if __name__ == '__main__':
    # batch("_aug")
    file_path = r"../data/data"+version+".txt"
    model_path = r"../pkl/model"+version+"mock.pkl"
    file = r"C:\Users\perlicue\Desktop\data\data_11_glcm_aug.txt"
    data, target = loadDataSet(file)
    X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=.3, random_state=99)


    train(X_train, y_train, model_path)
    result = predict(X_test, y_test, model_path)
    print(y_test)
    print(result)
    print(cal_score(y_test, result))
    print(enough_test(data, target, 10, model_path))





    # data = LE.get_le(file_path)
    # data = preprocessing.scale(data)
    # print(data)
    # data = normalize(data)
    # print(data)
    # data = StandardScaler().fit_transform(data)
    # parameters = {'C': [0.001, 0.003, 0.006, 0.009, 0.01, 0.04, 0.08, 0.1],
    #               'kernel': ('linear', 'rbf',),
    #               'gamma': [0.001, 0.005, 0.1, 0.15, 0.20, 0.23, 0.27],
    #               'decision_function_shape': ['ovo', 'ovr'],
    #               # 'class_weight': [{1: 7, 2: 1.83, 3: 3.17}],
    #               }

    # grid = GridSearchCV(SVC(), param_grid={"C": [ 0.00001, 0.001, 0.01, 0.05, 0.1, 1, 5, 10], "gamma": [1000, 100, 10, 1, 0.1, 0.2, 0.5, 0.01, 0.001]}, cv=4)
    # grid = GridSearchCV(SVC(), param_grid={"C": [ 1], "gamma": [ 0.01]}, cv=4)
    # grid = GridSearchCV(SVC(), parameters);
    # grid.fit(X_train, y_train)
    # grid.fit(data, target)
    # a = pd.DataFrame(grid.cv_results_)

    # 按照mean_test_score降序排列
    # a.sort(['mean_test_score'], ascending=False)
    # print("%s The best parameters are %s with a score of %0.2f" % (grid.best_estimator_, grid.best_params_, grid.best_score_))
    # print("predict: %s", grid.predict(data))

    # train(data, target, model_path)
    # result = predict(data, target, model_path)
    # print(result)


    # iris = datasets.load_iris()
    # digits = datasets.load_iris()
    # print(digits.data[:-1].shape)
    # print(digits.target[:-1])

    # clf = svm.SVC(gamma=0.001, C=100.)
    # clf.fit(digits.data[:-1], digits.target[:-1])
    # clf = joblib.load('filename.pkl')
    # re = clf.predict(digits.data[-1:])
    # print(re)
    # save_model(clf)

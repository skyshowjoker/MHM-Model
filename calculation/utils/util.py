


def cal_score(target, predict):
    TP, TN, FP, FN = 0, 0, 0, 0


    for i in range(0, len(target)):
        target[i] = int(target[i])
        if predict[i] < 1 and target[i] < 1:
            TP += 1
        if predict[i] == 1 and target[i] == 1:
            TN += 1
        if predict[i] < 1 and target[i] == 1:
            FP += 1
        if predict[i] == 1 and target[i] < 1:
            FN += 1



    P = TP / (TP + FP)
    R = TP / (TP + FN)
    F1 = 2 * P * R / (P + R)
    acc = (TP + TN) / (TP + TN + FP + FN)
    return acc, P, R
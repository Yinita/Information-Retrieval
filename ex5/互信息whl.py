import numpy as np

def mutualInfo(data):
    X = np.asarray(data.iloc[:, 0])
    Y = np.asarray(data.iloc[:, 1])
    # 使用字典统计每一个x元素出现的次数
    d_x = dict()  # x的字典
    for x in X:
        if x in d_x:
            d_x[x] += 1
        else:
            d_x[x] = 1
    # 计算每个元素出现的概率
    p_x = dict()
    for x in d_x.keys():
        p_x[x] = d_x[x] / X.size

    # 使用字典统计每一个y元素出现的次数
    d_y = dict()  # y的字典
    for y in Y:
        if y in d_y:
            d_y[y] += 1
        else:
            d_y[y] = 1
    # 计算每个元素出现的概率
    p_y = dict()
    for y in d_y.keys():
        p_y[y] = d_y[y] / Y.size

    # 使用字典统计每一个(x,y)元素出现的次数
    d_xy = dict()  # x的字典
    for i in range(X.size):
        if (X[i], Y[i]) in d_xy:
            d_xy[X[i], Y[i]] += 1
        else:
            d_xy[X[i], Y[i]] = 1
    # 计算每个元素出现的概率
    p_xy = dict()
    for xy in d_xy.keys():
        p_xy[xy] = d_xy[xy] / X.size
    # print(d_x, d_y, d_xy)
    # print(p_x, p_y, p_xy)

    # 初始化互信息值为0
    mi = 0
    for xy in p_xy.keys():
        mi += p_xy[xy] * np.log(p_xy[xy] / (p_x[xy[0]] * p_y[xy[1]]))
    # print(mi)

    return mi

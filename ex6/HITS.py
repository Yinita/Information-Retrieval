import numpy as np
from numpy import linalg as LA
# 定义转移矩阵
A = np.array([[0, 0, 0, 0, 0, 1, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 1, 0, 0, 0, 0, 1, 0],
               [0, 0, 0, 0, 0, 0, 0, 1, 0],
               [0, 0, 0, 0, 0, 0, 0, 1, 1],
               [0, 1, 1, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [1, 0, 0, 0, 0, 0, 1, 0, 0]])

A1 = np.array([[0, 0, 1, 0, 0, 0, 0],
              [0, 1, 1, 0, 0, 0, 0],
              [1, 0, 1, 2, 0, 0, 0],
              [0, 0, 0, 1, 1, 0, 0],
              [0, 0, 0, 0, 0, 0, 1],
              [0, 0, 0, 0, 0, 1, 1],
              [0, 0, 0, 2, 1, 0, 1]])


# 初始化hub和authority得分
h = np.ones(A.shape[0])
a = np.ones(A.shape[0])

# 迭代计算，直到收敛
for _ in range(100):
    a_new = np.matmul(A.T, h)
    h_new = np.matmul(A, a_new)
    '''# 将hub和authority向量标准化,进行L2正则
    a_new /= LA.norm(a_new)
    h_new /= LA.norm(h_new)'''
    # 检查是否收敛
    if np.allclose(a_new, a) and np.allclose(h_new, h):
        break

    # 进行L1正则
    a, h = a_new, h_new
    a /= np.sum(np.abs(a))
    h /= np.sum(np.abs(h))

# 打印最终的hub和authority得分，保留两位小数
print("Hub scores: ", np.round(h, 2))
print("Authority scores: ", np.round(a, 2))
# 这是贴合课本的输出

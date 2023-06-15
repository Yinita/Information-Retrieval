import numpy as np

# 定义邻接矩阵
M = np.array([[0, 1, 1, 1],
              [0, 0, 1, 1],
              [0, 0, 0, 1],
              [0, 0, 1, 0]])

# 初始化每个节点的 PR 值，由于有四个节点，每个节点的初始 PR 值为 1/4
pr = np.array([0.25, 0.25, 0.25, 0.25])

# teleportation rate
alpha = 0.1

# 计算所有节点出度的倒数，用于后面的更新公式
out_degree_inverse = np.zeros(4)
for i in range(4):
    out_degree_inverse[i] = 1 / np.sum(M[i])

print("初始化 PageRank 值：", pr)

# 进行 power iteration
for iter in range(100):
    pr_new = (1 - alpha) * np.matmul(M.T, pr * out_degree_inverse) + alpha / 4
    # 打印每一步迭代的结果
    print("第", iter+1, "轮迭代后的 PageRank 值：", pr_new)
    # 检查是否收敛
    if np.sum(abs(pr_new - pr)) < 1e-6:
        break
    pr = pr_new

print("最终的 PageRank 值为：", pr)


import numpy as np

# 定义转移概率矩阵P
P = np.array([[0, 0, 0, 0],
             [0, 0, 0, 0],
             [1/2, 1/2, 0, 1],
             [1/2, 1/2, 1, 0]])

# 定义阻尼系数
d = 0.9

# 计算阻尼系数矩阵
G = d * P + (1-d) / P.shape[0]

# 计算单位矩阵
I = np.eye(P.shape[0])

# 计算阻尼系数矩阵和单位矩阵的差的逆矩阵
inverse_matrix = np.linalg.inv(I - G)

# 计算PageRank值
pr = np.matmul(inverse_matrix, np.ones(P.shape[0]) / P.shape[0])
pr = pr/pr.sum()
print("PageRank值为：", pr)

'''import networkx as nx
 # 创建有向图
G = nx.DiGraph()
# 有向图之间边的关系
edges = [("A", "C"), ("A", "D"), ("B", "C"), ("B", "D"), ("C", "D"),("D", "C")]
for edge in edges:
     G.add_edge(edge[0], edge[1])
pagerank_list = nx.pagerank(G, alpha=0.9)
print("pagerank 值是：", pagerank_list)
'''
# 定义转移概率矩阵P
P = np.array([[0, 0, 0, 0],
             [0, 0, 0, 0],
             [1/2, 1/2, 0, 1],
             [1/2, 1/2, 1, 0]])

# 定义阻尼系数
d = 0.9
G = d * P + (1-d) / P.shape[0]
I = np.eye(P.shape[0])

inverse_matrix = np.linalg.inv(I - G)
pr = np.matmul(inverse_matrix, np.ones(P.shape[0]) / P.shape[0])
print(G)
print(I)
print((I - G))
print(inverse_matrix)
print(pr)
pr = pr/pr.sum()
print(np.ones(P.shape[0]) / P.shape[0])

A = np.array([[1, 0, -0.9/2, -0.9/2],
              [0, 1, -0.9/2, -0.9/2],
              [0, 0, 1, -0.9],
              [0, 0, -0.9, 1]])
inverse_matrix = np.linalg.inv(A)
print(inverse_matrix)
A = np.array([[0.1/4, 0.1/4,0.1/4,0.1/4]
              ])
print(inverse_matrix)
xasx=np.matmul(A, inverse_matrix)
print(xasx)
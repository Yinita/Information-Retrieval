import numpy as np
import os
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
from collections import Counter
import re

# 读取数据
folder_paths = ["D:\homework//2023 -1l\IR\ex5\党政办公室", "D:\homework//2023 -1l\IR\ex5\招生办公室",
                "D:\homework//2023 -1l\IR\ex5\教务处", "D:\homework//2023 -1l\IR\ex5\研究生院", "D:\homework//2023 -1l\IR\ex5\科学技术部"]


def mutual_info(X):
    """
    计算互信息
    """
    mutual_infos = np.zeros(X.shape)
    sum_x = np.sum(X)  # 优化
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):

            # px = np.sum(X[i, :] / sum_x  # 特征
            # py = np.sum(X[:, j]) / sum_x  # 类别
            pxy = X[i, j] / sum_x
            if pxy == 0:  # 避免log(0)
                mutual_infos[i, j] = 0
            else:
                mutual_infos[i, j] = pxy * np.log(sum_x * X[i, j] / (np.sum(X[:, j]) * np.sum(X[i, :])))
                #pxy * np.log(pxy / (px * py))
    return mutual_infos


def chi_square(X):
    """
    计算卡方统计量
    """
    chi_squares = np.zeros(X.shape)
    N = np.sum(X)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            # 计算期望值
            E = np.sum(X[i, :]) * np.sum(X[:, j]) / N
            # 计算卡方统计量
            chi_squares[i, j] = (X[i, j] - E) ** 2 / E
    return chi_squares


def select_k_best_features(X, k):
    """
    根据互信息选择每个类别前k个最高的特征
    """
    mutual_infos = mutual_info(X)   # chi_square, mutual_info
    top_k_features = []
    for i in range(X.shape[0]):
        # 获取互信息最大的前k个特征的索引
        top_k_indices = np.argsort(mutual_infos[i, :])[-k:]
        top_k_values = mutual_infos[i, top_k_indices]
        top_k_features.append(list(zip(top_k_indices, top_k_values)))
    return top_k_features

def get_class_name(folder_path):
    # 使用正则表达式匹配"\ex5\"后的所有字符
    match = re.search(r"\\ex5\\(.+)$", folder_path)
    if match:
        return match.group(1)
    else:
        return "Unknown"


def read_txt_files(folder_paths):
    texts, labels = [], []
    for label, folder_path in enumerate(folder_paths):
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.txt'):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, 'r', encoding='utf-8') as f:
                    words = f.read().split()  # 使用空格进行分词
                    texts.append(Counter(words))
                labels.append(label)
    return texts, labels


texts, labels = read_txt_files(folder_paths)

# 创建词汇表
vocab = set()
for text in texts:
    vocab.update(text.keys())
vocab = list(vocab)
label_num = len(set(labels))
# 创建特征矩阵
X = np.zeros((label_num, len(vocab)))

for i, text in enumerate(texts):
    for word, count in text.items():
        if word in vocab:
            j = vocab.index(word)
            X[labels[i]][j] += count


# print(X)
# print(label_num)
# print(len(vocab))

# 获取每个类别的最好特征
top_k_features = select_k_best_features(X, 10)

# 对每个类别，打印最好的特征及其互信息值
for i, features in enumerate(top_k_features):
    class_name = get_class_name(folder_paths[i])
    print(f"Class {class_name}:")
    for j, value in features:
        print(f"{vocab[j]}: {value:.2f}")

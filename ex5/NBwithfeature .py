import numpy as np
import os
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
from collections import Counter
import re
import random
# 读取数据
folder_paths = ["D:\homework//2023 -1l\IR\ex5\党政办公室", "D:\homework//2023 -1l\IR\ex5\招生办公室",
                "D:\homework//2023 -1l\IR\ex5\教务处", "D:\homework//2023 -1l\IR\ex5\研究生院",
                "D:\homework//2023 -1l\IR\ex5\科学技术部"]



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


def read_txt_files(folder_paths, test_rate=0.25):
    train_texts, train_labels = [], []
    test_texts, test_labels = [], []
    for label, folder_path in enumerate(folder_paths):
        file_names = os.listdir(folder_path)
        file_names = [file_name for file_name in file_names if file_name.endswith('.txt')]
        #random.shuffle(file_names)  # 随机排列文件名(随机划分)
        test_num = int(len(file_names) * test_rate)
        test_file_names = file_names[:test_num]
        train_file_names = file_names[test_num:]
        for file_name in train_file_names:
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r', encoding='utf-8') as f:
                words = f.read().split()  # 使用空格进行分词
                train_texts.append(Counter(words))
                train_labels.append(label)
        for file_name in test_file_names:
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r', encoding='utf-8') as f:
                words = f.read().split()  # 使用空格进行分词
                test_texts.append(Counter(words))
                test_labels.append(label)
    return train_texts, train_labels, test_texts, test_labels


class NaiveBayesClassifier:
    """
        初始化函数中，我们定义两个变量来存储模型参数。class_log_prior_
        存储每个类别的对数先验概率，feature_log_prob_
        存储在每个类别中每个特征的对数条件概率
    """

    def __init__(self, class_prior=None, fit_prior=True):
        self.class_prior = class_prior
        self.fit_prior = fit_prior


    '''
        训练函数，计算每个类别的先验概率和特征的条件概率。
        首先计算每个类别的样本数量和每个类别中每个特征的总数
        然后，我们计算每个类别的对数先验概率，这就是每个类别的样本数量除以总样本数量的对数
        最后，我们计算每个特征在每个类别中的对数条件概率。这是在知道样本属于某个类别的前提下，特征出现的概率的对数
        我们使用拉普拉斯平滑（加1平滑）来处理那些在训练集中没有出现过的特征。
        '''

    def fit(self, X):
        n_classes, n_features = X.shape
        count_sample_per_class = np.sum(X, axis=1)
        feature_count_per_class = X.copy()

        self.class_log_prior_ = np.log(count_sample_per_class) - np.log(np.sum(count_sample_per_class))
        self.feature_log_prob_ = np.log(feature_count_per_class + 1) - np.log(
            np.sum(feature_count_per_class, axis=1).reshape(-1, 1) + n_features)
        return self

    def predict(self, X):  # 预测模块
        if len(X.shape) == 1:  # 1 -> (1, n_features)
            X = X.reshape(1, -1)
        return np.argmax(X @ self.feature_log_prob_.T + self.class_log_prior_, axis=1)

    '''预测函数，它计算每个输入样本最可能的类别。对于每个输入样本，我们计算它在每个类别下的对数概率
       这是通过将输入样本的特征向量和每个类别的特征对数条件概率向量进行点积，然后加上类别的对数先验概率得到的
       然后，我们返回对数概率最高的类别作为预测结果。'''


train_texts, train_labels, test_texts, test_labels = read_txt_files(folder_paths, test_rate=0.25)
# print(test_texts)
# 创建词汇表
vocab = set()
for text in train_texts:
    vocab.update(text.keys())
vocab = list(vocab)
label_num = len(set(train_labels))
# 创建特征矩阵
X = np.zeros((label_num, len(vocab)))

for i, text in enumerate(train_texts):
    for word, count in text.items():
        if word in vocab:
            j = vocab.index(word)
            X[train_labels[i]][j] += count

# 选择每个类别前k个最好的特征
k = 500
top_k_features = select_k_best_features(X, k)

# 构建新的词汇表，只包含最好的特征
new_vocab = set()
for features in top_k_features:
    for j, _ in features:
        new_vocab.add(vocab[j])
new_vocab = list(new_vocab)

# 构建新的特征矩阵，只包含最好的特征
new_X = np.zeros((label_num, len(new_vocab)))
for i, text in enumerate(train_texts):
    for word, count in text.items():
        if word in new_vocab:
            j = new_vocab.index(word)
            new_X[train_labels[i]][j] += count


# 初始化模型
model = NaiveBayesClassifier()

# 训练模型
model.fit(new_X)

# 创建一部字典来存储每个类别的正确预测数和总数
class_stats = {i: [0, 0] for i in range(len(folder_paths))}

# 对每个测试样本进行预测
for i in range(len(test_texts)):
    # 注意，如果训练集中没有这个词项，那么这个词项将被跳过
    test_vector = np.zeros((1, len(new_vocab)))
    for word, count in test_texts[i].items():
        if word in new_vocab:
            j = new_vocab.index(word)
            test_vector[0, j] = count

    # 更新类别统计
    label = test_labels[i]
    class_stats[label][1] += 1  # 总数增加

    # 预测
    prediction = model.predict(test_vector)
    if prediction == label:
        class_stats[label][0] += 1  # 正确预测数增加

sum_accuracy = 0
# 输出每个类别的精确度
for label, (correct, total) in class_stats.items():
    class_name = get_class_name(folder_paths[label])
    accuracy = correct / total if total > 0 else 0
    print(f"{class_name} Accuracy: {accuracy:.2f}")
    sum_accuracy += accuracy

print(f"Average Accuracy: {sum_accuracy/label_num:.2f}")


from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

sk_model = MultinomialNB()
labels=[0,1,2,3,4]
sk_model.fit(new_X, labels)

sk_predictions = []

for i in range(len(test_texts)):
    test_vector = np.zeros((1, len(new_vocab)))
    for word, count in test_texts[i].items():
        if word in new_vocab:
            j = new_vocab.index(word)
            test_vector[0, j] = count

    prediction = sk_model.predict(test_vector)
    sk_predictions.append(prediction[0])
# print(sk_predictions)

sk_accuracy = accuracy_score(test_labels, sk_predictions)

print(f"Sklearn MultinomialNB Accuracy: {sk_accuracy:.2f}")


# 进行k-score研究
'''
import csv

A = len(vocab)  # Assuming A is the size of the vocabulary

with open('k_accuracy.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["k", "accuracy"])

    for stride in range(1, 100):
        step = 10
        k = stride * step
        print(f"Running for k = {k}")
        top_k_features = select_k_best_features(X, k)

        new_vocab = set()
        for features in top_k_features:
            for j, _ in features:
                new_vocab.add(vocab[j])
        new_vocab = list(new_vocab)

        new_X = np.zeros((label_num, len(new_vocab)))
        for i, text in enumerate(train_texts):
            for word, count in text.items():
                if word in new_vocab:
                    j = new_vocab.index(word)
                    new_X[train_labels[i]][j] += count

        model = NaiveBayesClassifier()
        model.fit(new_X)

        class_stats = {i: [0, 0] for i in range(len(folder_paths))}

        for i in range(len(test_texts)):
            test_vector = np.zeros((1, len(new_vocab)))
            for word, count in test_texts[i].items():
                if word in new_vocab:
                    j = new_vocab.index(word)
                    test_vector[0, j] = count

            label = test_labels[i]
            # print(class_stats)
            class_stats[label][1] += 1  # 总数增加

            prediction = model.predict(test_vector)
            if prediction == label:
                class_stats[label][0] += 1  # 正确预测数增加

        sum_accuracy = 0
        for label, (correct, total) in class_stats.items():
            accuracy = correct / total if total > 0 else 0
            sum_accuracy += accuracy
        score = sum_accuracy / label_num

        writer.writerow([k, score])
'''
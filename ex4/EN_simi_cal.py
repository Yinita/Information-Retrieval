from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List, Dict
from collections import Counter
import math

# 从文件中读取数据
def read_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        # 分词转小写
        documents = [line.strip().lower() for line in f.readlines()]
    return documents

# 将文档转换为TF-IDF向量
def vectorize_documents_(documents):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)
    return tfidf_matrix

# 计算文档之间余弦相似度
def calculate_cosine_similarity_(tfidf_matrix):
    return cosine_similarity(tfidf_matrix)




# 计算词频（TF）
def calculate_term_frequencies(documents):
    term_frequencies = []
    for document in documents:
        # 对每个文档进行分词并计算词频
        term_frequency = Counter(document.split())
        term_frequencies.append(term_frequency)

    return term_frequencies


# 计算逆文档频率（IDF）
def calculate_inverse_document_frequencies(documents, term_frequencies):
    document_count = len(documents)  # 文档总数
    # 获取所有文档中的所有独立词汇
    unique_terms = set(term for doc in term_frequencies for term in doc)
    inverse_document_frequencies = {}

    for term in unique_terms:
        # 计算包含该词汇的文档数量
        docs_containing_term = sum(1 for tf in term_frequencies if term in tf)

        # 计算逆文档频率
        idf = math.log(document_count / docs_containing_term+1)+1
        inverse_document_frequencies[term] = idf
    return inverse_document_frequencies

def l2_norm(vector):
    # 计算 L2 范数
    sum_of_squares = sum([value ** 2 for value in vector.values()])
    return math.sqrt(sum_of_squares)

def normalize_tfidf_vectors(tfidf_vectors):
    normalized_vectors = []

    for tfidf_vector in tfidf_vectors:
        norm = l2_norm(tfidf_vector)

        # 归一化 TF-IDF 向量
        normalized_vector = {term: tfidf / norm for term, tfidf in tfidf_vector.items()}
        normalized_vectors.append(normalized_vector)

    return normalized_vectors

# 计算 TF-IDF 向量
def calculate_tfidf_vectors(term_frequencies, inverse_document_frequencies):
    tfidf_vectors = []

    for term_frequency in term_frequencies:
        tfidf_vector = {}
        for term, count in term_frequency.items():
            # 计算 TF-IDF 值
            tfidf = count * inverse_document_frequencies[term]
            tfidf_vector[term] = tfidf
        tfidf_vectors.append(tfidf_vector)


    normalized_tfidf_vectors = normalize_tfidf_vectors(tfidf_vectors)
    return normalized_tfidf_vectors


# 计算余弦相似度
def calculate_cosine_similarity(tfidf_vectors: List[Dict[str, float]]) -> np.ndarray:
    def dot_product(vector1, vector2): # 点积
        return sum(vector1.get(term, 0) * vector2.get(term, 0) for term in set(vector1) | set(vector2))

    def norm(vector):  # l2正则
        return sum(value for value in vector.values())
        #return np.sqrt(sum(value**2 for value in vector.values()))

    document_count = len(tfidf_vectors)
    similarity_matrix = np.zeros((document_count, document_count))
    # 词数 相似矩阵
    for i in range(document_count):
        for j in range(i, document_count):
            numerator = dot_product(tfidf_vectors[i], tfidf_vectors[j])  # 上面
            denominator = norm(tfidf_vectors[i]) * norm(tfidf_vectors[j])  # 下面
            similarity = numerator / (denominator + 1e-8)  # 避免除以零
            similarity_matrix[i][j] = similarity_matrix[j][i] = similarity

    return similarity_matrix




def vectorize_documents(documents):
    term_frequencies = calculate_term_frequencies(documents)

    inverse_document_frequencies = calculate_inverse_document_frequencies(documents, term_frequencies)
    tfidf_vectors = calculate_tfidf_vectors(term_frequencies, inverse_document_frequencies)

    return tfidf_vectors

# 输出相似度最大的5个文档
def find_top_similar_documents(similarity_matrix, num_top_docs=5):
    top_similar_docs = {}
    for i in range(10):
        # 用表存
        # 获取排序后的索引，首先按文档编号降序排序，然后按相似度降序排序
        sorted_indices = np.lexsort((-np.arange(similarity_matrix.shape[0]), -similarity_matrix[i]))
        # 获取最相似的文档（不包括自身）
        similar_docs = sorted_indices[1:num_top_docs + 1]
        # 将文档编号从0开始的索引转换为从1开始，并将其添加到字典中
        top_similar_docs[i + 1] = [doc + 1 for doc in similar_docs]
        '''similar_docs = np.argsort(similarity_matrix[i])[:-num_top_docs-2:-1]
        top_similar_docs[i+1] = [doc+1 for doc in similar_docs if doc != i][:num_top_docs]'''
    return top_similar_docs

if __name__ == "__main__":
    file_path = "HW4_1.txt"
    documents = read_data(file_path)
    tfidf_matrix = vectorize_documents(documents)
    similarity_matrix = calculate_cosine_similarity(tfidf_matrix)
    top_similar_docs = find_top_similar_documents(similarity_matrix)

    for doc, similar_docs in top_similar_docs.items():
        print(f"对于文档 {doc}，相似度最大的5个文档为：{', '.join(map(str, similar_docs))}")

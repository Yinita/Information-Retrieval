from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List, Dict
from collections import Counter
import math
import jieba
import re
from nltk.stem import SnowballStemmer
import os
# 使用jieba库进行中文分词
# 使用SnowballStemmer进行中文分词
stemmer = SnowballStemmer("english")


def tokenize(text):
    return ' '.join(jieba.cut(text))


# 加载停用词表
with open("stopwords.txt", "r", encoding="utf-8") as f:
    stopwords = set(line.strip() for line in f)

# 从文件中读取数据
def read_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        documents = [tokenize(line.strip()) for line in f.readlines()]
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
def calculate_cosine_similarity(query_vector, tfidf_vectors):
    def dot_product(vector1, vector2): # 点积
        return sum(vector1.get(term, 0) * vector2.get(term, 0) for term in set(vector1) | set(vector2))
    document_count = len(tfidf_vectors)
    similarity_scores = np.zeros(document_count)

    for i in range(document_count):
        numerator = dot_product(query_vector, tfidf_vectors[i])  # 上面
        denominator = l2_norm(query_vector) * l2_norm(tfidf_vectors[i])  # 下面
        similarity = numerator / (denominator + 1e-8)  # 避免除以零
        similarity_scores[i] = similarity

    return similarity_scores


def vectorize_documents(documents):
    term_frequencies = calculate_term_frequencies(documents)
    inverse_document_frequencies = calculate_inverse_document_frequencies(documents, term_frequencies)
    tfidf_vectors = calculate_tfidf_vectors(term_frequencies, inverse_document_frequencies)

    return tfidf_vectors


# 输出相似度最大的10个文档（已弃用）
def find_top_similar_documents(similarity_matrix, num_top_docs=5):
    top_similar_docs = {}
    for i in range(10):
        # 获取排序后的索引，首先按文档编号降序排序，然后按相似度降序排序
        sorted_indices = np.lexsort((-np.arange(similarity_matrix.shape[0]), -similarity_matrix[i]))
        # 获取最相似的文档（不包括自身）
        similar_docs = sorted_indices[1:num_top_docs + 1]
        # 将文档编号从0开始的索引转换为从1开始，并将其添加到字典中
        top_similar_docs[i + 1] = [doc + 1 for doc in similar_docs]

    return top_similar_docs

def read_file_and_tokenize(file_path, mode=1, title=0):
    if mode == 2:
        dir_prefixes = {"mtbd": "1", "tzgg": "2", "xqxw": "3"}
        for i in dir_prefixes:
            if i in file_path:   # 这里读取的是原文档
                document_id = dir_prefixes[i] + os.path.splitext(os.path.basename(file_path))[0]
                break
    else:
        # Extract document ID from the file path
        document_id = os.path.splitext(os.path.basename(file_path))[0]

    # 读取文件内容
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    if title == 0:
        text = content
    else:
        # Split the content into title and text
        title_txt, text = content.split("—", 1)

    def process_text(text, is_title):
        # 使用 jieba 分词
        words = jieba.cut(text)
        processed_words = []
        for word in words:
            # 如果是链接，直接添加
            if word.startswith('http') or word.startswith('www'):
                processed_words.append(word)
            else:
                # 只保留非停用词的中文、英文字符和标题中的数字
                if word not in stopwords:
                    if re.search(r'[\u4e00-\u9fa5]', word):  # 如果是中文
                        processed_words.append(word)
                    elif word.isalpha() or (is_title and word.isdigit()):  # 如果是英文，或者在标题中且是数字
                        stemmed_word = stemmer.stem(word)
                        processed_words.append(stemmed_word)
        return processed_words

    processed_text = process_text(text, False)
    if title:
        processed_title = process_text(title_txt, True)
        return [document_id, processed_text, processed_title]
    else:
        return [document_id, processed_text]

    return [document_id, processed_text, processed_title]


def rank_results(query, documents, k):
    # 分词处理查询字符串
    query_tokens = jieba.cut(query, cut_all=False)
    query = ' '.join(query_tokens)
    for q in query:
        if q.isalpha():  # 如果是英文，转词干
            q = stemmer.stem(q)
    query = [query]  # 转[[xxx,yyy]]
    # 将每个文档的词汇列表连接成一个字符串，并与其ID一起存储
    documents = [(' '.join(doc[1]), doc[0]) for doc in documents]
    # 将查询添加到文档列表中
    documents_with_query = [query[0]] + [doc[0] for doc in documents]
    tfidf_vectors = vectorize_documents(documents_with_query)
    # 计算查询和所有文档的余弦相似度
    similarity_scores = calculate_cosine_similarity(tfidf_vectors[0], tfidf_vectors[1:])
    # 获取与查询最相关的k个文档的索引                 # 查询, 文档
    top_k_indices = np.argsort(similarity_scores)[::-1][:k+1]
    # 返回最相关的k个文档的ID和它们的相关性评分
    top_k_docs_with_scores = [(documents[i][1], similarity_scores[i]) for i in top_k_indices if i != 0]

    return top_k_docs_with_scores


def calculate_hit_rate(query, title):  # 计算命中率
    query_words = set(query.split())
    title_words = set(title.split())
    hit_rate = len(query_words & title_words) / len(query_words)
    return hit_rate



def rank_results_with_weights(query, documents, k, alpha=0.7):
    # 分词处理查询字符串
    query_tokens = jieba.cut(query, cut_all=False)
    query_list = [word for word in query_tokens if word not in stopwords]
    query = ' '.join(query_list)
    for q in query:
        if q.isalpha():  # 如果是英文，转词干
            q = stemmer.stem(q)
    query = [query]  # 转[[xxx,yyy]]
    # 将每个文档的词汇列表和标题列表分别连接成一个字符串，并与其ID一起存储
    documents_content = [(' '.join(doc[1]), doc[0]) for doc in documents]
    documents_title = [(' '.join(doc[2]), doc[0]) for doc in documents]
    # 计算内容的TF-IDF向量
    documents_with_query_content = [query[0]] + [doc[0] for doc in documents_content]
    tfidf_vectors_content = vectorize_documents(documents_with_query_content)
    # 计算查询和所有文档内容的余弦相似度
    similarity_scores_content = calculate_cosine_similarity(tfidf_vectors_content[0], tfidf_vectors_content[1:])
    # 计算标题的命中率
    hit_rates = np.array([calculate_hit_rate(query[0], title[0]) for title in documents_title])
    # 定义内容和标题的权重
    weight_content = alpha
    weight_hit_rate = 1 - alpha
    # 得分加权叠加
    combined_scores = weight_content * similarity_scores_content + weight_hit_rate * hit_rates
    # 创建一个包含ID和相似度得分的元组列表
    doc_ids_with_scores = [(documents[i][0], combined_scores[i]) for i in range(len(documents))]
    # 根据相似度得分对元组列表进行排序
    sorted_doc_ids_with_scores = sorted(doc_ids_with_scores, key=lambda x: x[1], reverse=True)
    # 获取与查询最相关的k个文档的ID和它们的相关性评分
    top_k_docs_with_scores = sorted_doc_ids_with_scores[:k + 1]
    return top_k_docs_with_scores


if __name__ == "__main__":
    '''file_path = "HW4_1.txt"
    documents = read_data(file_path)
    tfidf_matrix = vectorize_documents(documents)
    similarity_matrix = calculate_cosine_similarity(tfidf_matrix)
    top_similar_docs = find_top_similar_documents(similarity_matrix)

    for doc, similar_docs in top_similar_docs.items():
        print(f"对于文档 {doc}，相似度最大的5个文档为：{', '.join(map(str, similar_docs))}")'''

    query = "深圳大学 内部网"
    list = [(470428, 2), (479267, 2), (487555, 2), (487615, 2), (487633, 2), (487840, 2), (487992, 2), (487995, 2),
     (487996, 2), (488083, 2), (488160, 2), (488278, 2), (488329, 2), (488575, 2), (488603, 2), (488850, 2),
     (489017, 2), (489377, 2), (489534, 2), (489598, 2), (490600, 2), (490702, 2), (491275, 2), (491748, 2),
     (492374, 2), (492412, 2), (492552, 2), (492589, 2), (493030, 2), (493052, 2), (493108, 2), (493568, 2),
     (493828, 2), (493835, 2), (493972, 2), (494216, 2), (494453, 2), (494924, 2), (495052, 2), (495179, 2)]
    list = [(470428, 2), (479267, 2)]
    #rank_results(query, documents, k)
import jieba
import chardet
import numpy as np
import string
import os
from nltk.stem import PorterStemmer
stemmer = PorterStemmer()
def encode_vb(numbers):
    # 进行vb编码，接受一个列表，对每个传入的数字，使用一个(int8)列表来存储
    byte_arrays = []
    for number in numbers:
        bytes_list = []
        while True:
            bytes_list.insert(0, number % 128)
            # 最高位恒为0
            if number < 128:
                break
            number = number // 128
        # 最后的数据节的最高位变成1
        bytes_list[-1] += 128
        byte_arrays.append(bytearray(bytes_list))
    return bytearray().join(byte_arrays)


def decode_vb(byte_array):
    #对传入的数据进行解码
    numbers = []
    n = 0
    for byte in byte_array:
        if byte < 128:
            n = 128 * n + byte
        else:
            n = 128 * n + (byte - 128)
            numbers.append(n)
            n = 0
    return numbers


def read_and_tokenize_files(directory):
    tokenized_texts = []  # 初始化一个列表，用于保存所有文件的分词结果

    for file_name in os.listdir(directory):    # 避免误读
        if file_name.endswith('.txt') and not file_name.endswith('msg.txt') and not file_name.endswith('link.txt'):
            file_path = os.path.join(directory, file_name)

            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            for line in lines:
                doc_id, *tokens = line.strip().split(' ')  # *用来解包
                tokenized_texts.append((doc_id, tokens))

    return tokenized_texts

def build_inverted_index(tokenized_texts):
    inverted_index = {}

    for doc_id, tokens in tokenized_texts:
        for token in tokens:
            if token not in inverted_index:
                inverted_index[token] = []
            inverted_index[token].append(doc_id)

    # 对每个token的文档ID列表进行排序
    for token in inverted_index:
        inverted_index[token].sort()

    for token in inverted_index:
        '''可以在这里加入vb编码'''
        doc_ids = sorted(map(int, inverted_index[token]))
        '''gaps = compute_gaps(doc_ids)
        inverted_index[token] = encode_vb(gaps)'''
        inverted_index[token] = doc_ids

    return inverted_index



# 计算token总数和term总数
def count_tokens_and_terms(tokenized_texts):
    token_count = 0
    term_set = set()

    for _, tokens in tokenized_texts:
        token_count += len(tokens)
        term_set.update(tokens)
    return token_count, len(term_set)


def search(query, inverted_index):
    document_ids = []

    for token in query:
        if token in inverted_index:
            '''gaps = decode_vb(inverted_index[token])
            doc_ids = [gaps[0]] + [sum(gaps[:i+1]) for i in range(1, len(gaps))]
            str_doc_ids = list(map(str, doc_ids))

            # 将文档 ID 添加到结果列表中，同时检查重复
            for doc_id in str_doc_ids:
                if int(doc_id) not in document_ids:    #在这里我去除了vb，它浪费了时间
                    document_ids.append(int(doc_id))'''
            for doc_id in inverted_index[token]:
                if not document_ids:   # 为空 进行优化
                    document_ids.extend(inverted_index[token])
                    continue
                if doc_id not in document_ids:
                    document_ids.append(doc_id)
    # 对结果列表进行排序
    document_ids.sort()
    return document_ids


def compute_gaps(numbers):
    #计算gap,第一个存原始数据，之后都是存gap
    gaps = [numbers[0]] + [numbers[i] - numbers[i - 1] for i in range(1, len(numbers))]
    return gaps


def int_list_to_bin_string(int_list):   # 格式转换
    return ''.join(format(i, '08b') for i in int_list)

with open("stopwords.txt", "r", encoding="utf-8") as f:
    stopwords = set(line.strip() for line in f)


def pool_query_results(query, inverted_index, length=10):
    # 在这个函数中，我们返回的结果越靠前，表示跟搜索的文档更相似，也就是更接近于AND搜索， 返回的文档本身可以理解为OR搜索
    # 由于NOT需求不大，因此不加入了（可以做减法）
    terms = jieba.cut(query, cut_all=False)
    results_pool = {}
    # 对原始查询进行分词和词干化处理，然后保存到query中
    processed_query = []
    for term in list(terms):
        term = term.translate(str.maketrans('', '', string.punctuation))  # 去除标点符号
        if not term:
            continue
        if term.lower() not in stopwords and term.isalpha():
            term = stemmer.stem(term)
            processed_query.append(term)
            if len(processed_query) == length:
                break
        if term.isdigit():
            processed_query.append(term)

    searched_list = search(processed_query, inverted_index)
    for doc_id in searched_list:
        if doc_id not in results_pool:
            results_pool[doc_id] = 0
        results_pool[doc_id] += 1
    results = sorted(results_pool.items(), key=lambda x: x[1], reverse=True)
    return results  # {docID: times} as {645111:2, 612111:1}



if __name__ == '__main__':
    directory = "data"  # 替换为你的目录路径
    tokenized_texts = read_and_tokenize_files(directory)
    token_count, term_count = count_tokens_and_terms(tokenized_texts)  # 统计token和term总数
    inverted_index = build_inverted_index(tokenized_texts)  # 构建倒排索引
    print(inverted_index)
    print(token_count, term_count)
    print("请输入查询： ")
    queries = input()

    # queries = "一经 侵权 可能"
    sorted_results = pool_query_results(queries, inverted_index)
    print(f"查询 '{queries}' 的文档ID：{sorted_results}")

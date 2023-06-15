import jieba
import chardet
import numpy as np



# 读取文本文件，每行代表一个文件
def read_txt_file(file_path):
    with open(file_path, 'rb') as f:
        file_data = f.read()
        detected_encoding = chardet.detect(file_data)['encoding']

    with open(file_path, 'r', encoding=detected_encoding) as f:
        file_texts = [(str(index), line.strip()) for index, line in enumerate(f.readlines())]
    return file_texts


# 对文本进行分词
def tokenize_texts(texts):
    tokenized_texts = []
    for file, text in texts:
        tokens = jieba.lcut_for_search(text)
        tokenized_texts.append((file, tokens))
    return tokenized_texts



# 计算token总数和term总数
def count_tokens_and_terms(tokenized_texts):
    token_count = 0
    term_set = set()

    for _, tokens in tokenized_texts:
        token_count += len(tokens)
        term_set.update(tokens)
    return token_count, len(term_set)

'''
# 构建倒排索引
def build_inverted_index(tokenized_texts):
    inverted_index = {}
    for file, tokens in tokenized_texts:
        for token in tokens:
            if token not in inverted_index:
                inverted_index[token] = []
            inverted_index[token].append(int(file))
    return inverted_index


# 根据查询搜索文档ID
def search(query, inverted_index,way):
    tokens = jieba.lcut(query)
    document_ids = []
    if way == 1:
        for token in tokens:
            if token in inverted_index:
                document_ids.extend(inverted_index[token])
    else :
        if query in inverted_index:
            document_ids.extend(inverted_index[query])
    return sorted(set(document_ids))'''


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
def build_inverted_index(tokenized_texts):
    inverted_index = {}
    for file, tokens in tokenized_texts:
        for token in tokens:
            if token not in inverted_index:
                inverted_index[token] = []
            inverted_index[token].append(file)

    for token in inverted_index:
        doc_ids = sorted(map(int, inverted_index[token]))
        gaps = compute_gaps(doc_ids)
        inverted_index[token] = encode_vb(gaps)
    return inverted_index

def search(query, inverted_index):
    tokens = jieba.lcut(query)
    document_ids = []

    for token in tokens:
        if token in inverted_index:
            gaps = decode_vb(inverted_index[token])
            doc_ids = [gaps[0]] + [sum(gaps[:i+1]) for i in range(1, len(gaps))]
            str_doc_ids = list(map(str, doc_ids))

            # 将文档 ID 添加到结果列表中，同时检查重复
            for doc_id in str_doc_ids:
                if doc_id not in document_ids:
                    document_ids.append(int(doc_id))

    # 对结果列表进行排序
    document_ids.sort()
    return document_ids

def compute_gaps(numbers):
    #计算gap,第一个存原始数据，之后都是存gap
    gaps = [numbers[0]] + [numbers[i] - numbers[i - 1] for i in range(1, len(numbers))]
    return gaps


def compute_gaps(numbers):
    #计算gap,第一个存原始数据，之后都是存gap
    gaps = [numbers[0]] + [numbers[i] - numbers[i - 1] for i in range(1, len(numbers))]
    return gaps


def int_list_to_bin_string(int_list):
    return ''.join(format(i, '08b') for i in int_list)

def test_encode_decode_vb():
    test_cases = [
        [722, 936, 724],
        [1, 2, 3, 4, 5],
        [128, 256, 512, 1024],
        [100, 200, 300, 400, 500, 600],
        [345, 879, 1234, 5678, 9012]
    ]

    for test_case in test_cases:
        encoded = encode_vb(test_case)
        decoded = decode_vb(encoded)

        if decoded == test_case:
            print(f"测试通过: 原始输入 = {test_case}, 解码后的输出 = {decoded}")
        else:
            print(f"测试失败: 原始输入 = {test_case}, 解码后的输出 = {decoded}")


def gamma_encode(numbers):
    # 定义一个辅助函数，将数字转换为不带 '0b' 前缀的二进制字符串表示
    def binary_repr(number):
        return bin(number)[2:]

    encoded_bits = ""
    for number in numbers:
        # 计算数字的二进制表示的长度，减去第一个 '1' 以计算 p (即用于表示长度的 '0' 的数量)
        p = len(binary_repr(number)) - 1
        # 构建长度部分（length_part），它是由 p 个 '0' 组成的字符串
        length_part = '0' * p
        # 构建偏移量部分（offset_part），它是数字的二进制表示，但去掉了第一个 '1'
        offset_part = binary_repr(number)[1:]
        # 将长度部分和偏移量部分连接在一起，并将其添加到最终的编码比特串中
        encoded_bits += length_part + offset_part
    # 返回编码后的比特串
    return encoded_bits


if __name__ == '__main__':
    file_path = 'mapping.txt'
    jieba.load_userdict("dict/custom_dict.txt") # 个人词典
    texts = read_txt_file(file_path)  # 读取文本文件
    tokenized_texts = tokenize_texts(texts)  # 分词
    token_count, term_count = count_tokens_and_terms(tokenized_texts)  # 统计token和term总数
    inverted_index = build_inverted_index(tokenized_texts)  # 构建倒排索引



    queries = ["迁移", "迁移学习", "推荐", "深度学习", "隐私", "跨领域", "跨域"]
    for query in queries:
        document_ids = search(query, inverted_index)
        #document_ids = search(query, inverted_index,0)  # 搜索文档ID 0表示全词搜索，1表示拆开
        print(f"查询 '{query}' 的文档ID：{document_ids}")

    # 第一题的解决

        '''
        print(f"Token 总数: {token_count}")
        print(f"Term 总数: {term_count}")
        query=input()
        document_ids = search(query, inverted_index)  # 搜索文档ID 0表示全词搜索，1表示拆开
        print(f"查询 '{query}' 的文档ID：{document_ids}")'''
    # 这是更一般的输入
    '''
    
    
    doc_ids = [722,936,724]
    gaps = compute_gaps(doc_ids)
    print(gaps)  # 输出：[722, 214, -212]
    doc_ids = [824,829,215406]
    gaps = compute_gaps(doc_ids)
    print(gaps)  # 输出：[824, 5, 214577]'''

    '''numbers = [722, 936, 724]

    # 将每个数字转换为其二进制表示
    binary_representations = [format(number, 'b') for number in numbers]
    # 对每个数字进行 VB 编码
    encoded_numbers = [encode_vb([number]) for number in numbers]

    # 将整数列表转换为二进制字符串表示
    bin_strings = [int_list_to_bin_string(encoded_number) for encoded_number in encoded_numbers]
    for number, binary_repr in zip(numbers, binary_representations):
        print(f"数字 {number} 的普通二进制编码为：{binary_repr}")

    for number, bin_string in zip(numbers, bin_strings):
        print(f"VB 编码后的数字 {number} 的二进制存储结果为：{bin_string}")'''
    '''number=936
    binary_representation = [format(number, 'b')]
    print(f"数字 {number} 的普通二进制编码为：{binary_representation}")

    gamma_test_number = [number] #722，936，724
    gamma_encoded = gamma_encode(gamma_test_number)
    print(gamma_encoded)'''

    # test_encode_decode_vb()

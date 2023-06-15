import os
from nltk.stem import PorterStemmer
import re
import jieba
# 加载停用词表
with open("stopwords.txt", "r", encoding="utf-8") as f:
    stopwords = set(line.strip() for line in f)
stemmer = PorterStemmer()


directory = "data"  # 数据目录路径
def process_files(directory="data"):
    for root, dirs, _ in os.walk(directory):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            with open(f"data/{dir_name}.txt", "w", encoding="utf-8") as output_file:
                for file_name in os.listdir(dir_path):
                    if file_name.endswith(".txt"):
                        # 提取文件名中的数字
                        doc_id = re.match(r"(\d+)\.txt", file_name).group(1)
                    else:
                        continue
                    # 读取文件内容
                    with open(os.path.join(dir_path, file_name), "r", encoding="utf-8") as file:
                        content = file.read()
                    # 使用 jieba 分词
                    words = jieba.cut(content)
                    processed_words = []
                    for word in words:
                        if word in stopwords:
                            continue
                        # 只保留中文和英文字符
                        if re.search(r'[\u4e00-\u9fa5]', word):  # 如果是中文
                            processed_words.append(word)
                        elif word.isalpha():  # 如果是英文
                            stemmed_word = stemmer.stem(word)
                            processed_words.append(stemmed_word)



                    # 将文档ID和处理后的文本写入到新的文件中
                    output_file.write(doc_id + ' ' + ' '.join(processed_words) + '\n')


# 创建一个字典来保存目录名和前缀的对应关系
dir_prefixes = {"mtbd": "1", "tzgg": "2", "xqxw": "3"}

def process_files_xqxw(directory="xq_70_data"):
    for root, dirs, _ in os.walk(directory):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            with open(f"{directory}/{dir_name}.txt", "w", encoding="utf-8") as output_file:
                for file_name in os.listdir(dir_path):
                    if file_name.endswith(".txt"):
                        # 提取文件名中的数字
                        doc_id = re.match(r"(\d+)\.txt", file_name).group(1)
                    else:
                        continue
                    # 检查当前目录名是否在字典中，如果在，将前缀添加到文档ID前面
                    if dir_name in dir_prefixes:
                        doc_id = dir_prefixes[dir_name] + doc_id

                    # 读取文件内容
                    with open(os.path.join(dir_path, file_name), "r", encoding="utf-8") as file:
                        content = file.read()
                    # 使用 jieba 分词
                    words = jieba.cut(content)
                    processed_words = []
                    for word in words:
                        # 如果是链接，直接添加
                        if word.startswith('http') or word.startswith('www'):
                            processed_words.append(word)
                        else:
                            if word in stopwords:
                                continue
                            # 只保留中文和英文字符
                            if re.search(r'[\u4e00-\u9fa5]', word):  # 如果是中文
                                processed_words.append(word)
                            elif word.isalpha():  # 如果是英文
                                stemmed_word = stemmer.stem(word)
                                processed_words.append(stemmed_word)
                    # 将文档ID和处理后的文本写入到新的文件中
                    output_file.write(doc_id + ' ' + ' '.join(processed_words) + '\n')

process_files_xqxw()
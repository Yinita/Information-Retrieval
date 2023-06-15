import os
# 加载停用词表
with open("stopwords.txt", "r", encoding="utf-8") as f:
    stopwords = set(line.strip() for line in f)

folder_paths = [
    "D:\homework//2023 -1l\IR\ex5\党政办公室",
    "D:\homework//2023 -1l\IR\ex5\招生办公室",
    "D:\homework//2023 -1l\IR\ex5\教务处",
    "D:\homework//2023 -1l\IR\ex5\研究生院",
    "D:\homework//2023 -1l\IR\ex5\科学技术部",
]

import re
import jieba

for folder_path in folder_paths:
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            # 读取文件内容
            with open(os.path.join(folder_path, file_name), "r", encoding="utf-8") as file:
                content = file.read()
            # 使用 jieba 分词
            words = jieba.cut(content)
            # 只保留中文字符
            words = [word for word in words if re.search(r'[\u4e00-\u9fa5]', word)]
            # 去除停用词
            filtered_words = [word for word in words if word not in stopwords]
            # 将处理后的文本保存到同名的 txt 文件
            with open(os.path.join(folder_path, file_name), "w", encoding="utf-8") as file:
                file.write(' '.join(filtered_words))
